#!/usr/bin/env python3
"""MANDALAS DE LOS CHAKRAS · Un color a la vez
Creado por Dani Navarro (Daniela Navarro · Longevidad Emocional).

Genera el libro para colorear imprimible (A4 vertical, márgenes de 15 mm):
  - svg/      cada mandala como SVG vectorial (geometría calculada en mandalas.py)
  - preview/  un PNG por página impresa
  - libro_mandalas_chakras*.pdf

Uso:
    python3 generar_libro.py --fase 1     # portada, dedicatoria, cómo usar, Raíz
    python3 verificar.py                  # controles de calidad sobre lo generado

Dependencias: weasyprint, pypdf, cairosvg, fonttools, pillow, numpy, scipy, pdfminer.six
y `pdftoppm` (poppler) para los PNG de revisión.
"""
import argparse
import html
import subprocess
import sys
from pathlib import Path

import mandalas as M

AQUI = Path(__file__).resolve().parent

# ===================================================================== TEXTOS
# Todo lo que se lee en el libro está acá, fácil de editar.

DEDICATORIA = """Para vos, mamá,
que siempre estuviste a mi lado
y me diste fuerza para salir adelante.

Hoy te devuelvo un poco de todo eso:
un rato de calma, un color a la vez.

Pintá despacio, respirá tranquila
y disfrutá cada página.

Te quiero con todo mi corazón,
Dani"""

TITULO_LIBRO = ("MANDALAS", "DE LOS CHAKRAS")
SUBTITULO = "Un color a la vez"
BANDA = "LIBRO PARA COLOREAR"
CREADO_POR = "Creado por Dani Navarro"
PARA_MAMA = "Para mamá, con todo mi amor."

COMO_USAR_TITULO = "Cómo usar este libro"
COMO_USAR_PASOS = [
    "Elegí un mandala.",
    "Respirá tres veces, bien lento.",
    "Pintá sin apuro.",
    "No hay forma de hacerlo mal.",
    "Al terminar, leé la frase en voz alta.",
]
COMO_USAR_NOTA = ("Usá papel de 120 g o más, y lápices o marcadores gruesos, "
                  "fáciles de agarrar.")

TEXTO_COLOR = "Este es su color, pero podés usar los que quieras."
TEXTO_ESCRIBIR = "Podés escribirlo o contárselo a alguien."

# clave, nombre, "Está en", emoción que cuida, afirmación (líneas), respiración, pregunta
CHAKRAS = [
    dict(clave="raiz", nombre="Raíz", petalos=4, zonas=(26, 34),   # ≈30 zonas
         esta_en="la base de la columna y los pies",
         emocion="sentirme segura y sostenida",
         afirmacion=["Estoy a salvo.", "La vida me sostiene."],
         respiracion="inhalá en 4, soltá en 6, sintiendo tus pies.",
         pregunta="¿Qué te enseñaron tus padres que todavía llevás con vos?"),
    dict(clave="sacro", nombre="Sacro", petalos=6,
         esta_en="la parte baja de la panza",
         emocion="disfrute y creatividad",
         afirmacion=["Me permito disfrutar."],
         respiracion="inhalá en 4, soltá y aflojá la panza.",
         pregunta="¿Qué te encantaba hacer cuando eras joven?"),
    dict(clave="plexo", nombre="Plexo solar", petalos=10,
         esta_en="la boca del estómago",
         emocion="confianza y fuerza",
         afirmacion=["Confío en mí", "y en mis decisiones."],
         respiracion="inhalá en 4 y soltá como apagando una vela.",
         pregunta="¿De qué decisión tuya estás orgullosa?"),
    dict(clave="corazon", nombre="Corazón", petalos=12,
         esta_en="el centro del pecho",
         emocion="amor y perdón",
         afirmacion=["Doy y recibo amor", "con facilidad."],
         respiracion="una mano en el pecho, inhalá y soltá.",
         pregunta="¿A quién querés agradecerle hoy?"),
    dict(clave="garganta", nombre="Garganta", petalos=16,
         esta_en="la garganta y el cuello",
         emocion="expresarme",
         afirmacion=["Mi voz y mis palabras", "importan."],
         respiracion="inhalá por la nariz y soltá con un suspiro.",
         pregunta="¿Qué consejo le darías a tu nieto?"),
    dict(clave="tercer_ojo", nombre="Tercer ojo", petalos=2,
         esta_en="el centro de la frente",
         emocion="intuición y memoria",
         afirmacion=["Confío en lo que siento", "y recuerdo."],
         respiracion="cerrá los ojos, inhalá y soltá despacio.",
         pregunta="¿Qué recuerdo lindo vuelve seguido a tu mente?"),
    dict(clave="corona", nombre="Corona", petalos=36,
         esta_en="lo más alto de la cabeza",
         emocion="paz y sentido",
         afirmacion=["Estoy en paz.", "Todo está bien."],
         respiracion="inhalá y, al soltar, imaginá una luz suave.",
         pregunta="¿Qué te da paz en este momento de tu vida?"),
]

# La portada original (portada.png) no estaba disponible: esta portada es una
# recreación provisoria hecha a partir de la descripción. Poner en False cuando
# se reemplace por la fiel al original.
PORTADA_PROVISORIA = True

# ================================================================== MEDIDAS (mm)
MARGEN = 15
ANCHO, ALTO = 210, 297
ANCHO_UTIL = ANCHO - 2 * MARGEN
PESTANA_ANCHO = 8
PESTANA_ALTO = 34
CENTRO_MANDALA_Y = 111      # centro del mandala medido desde arriba
PESTANA_PASO = 38          # cada capítulo baja un escalón, para encontrarlo al hojear
TINTA = "#1b1b1b"

# ======================================================================= FUENTES
def preparar_fuentes():
    """Crea las instancias estáticas de Fraunces y Manrope (si faltan)."""
    destino = AQUI / "fuentes" / "estaticas"
    trabajos = [
        ("Fraunces[SOFT,WONK,opsz,wght].ttf", "Fraunces-Titulo.ttf", {"wght": 700, "opsz": 36, "SOFT": 100, "WONK": 0}),
        ("Manrope[wght].ttf", "Manrope-Medium.ttf", {"wght": 500}),
        ("Manrope[wght].ttf", "Manrope-Bold.ttf", {"wght": 700}),
        ("Manrope[wght].ttf", "Manrope-ExtraBold.ttf", {"wght": 800}),
    ]
    if all((destino / dst).exists() for _, dst, _ in trabajos):
        return
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    destino.mkdir(parents=True, exist_ok=True)
    for src, dst, ejes in trabajos:
        fuente = TTFont(AQUI / "fuentes" / src)
        instancer.instantiateVariableFont(fuente, ejes).save(destino / dst)


_PIL = {}
_FAMILIAS = {"cuerpo": "Manrope-Medium.ttf", "negrita": "Manrope-Bold.ttf", "titulo": "Fraunces-Titulo.ttf"}


def ancho_mm(texto, familia, pt):
    """Ancho aproximado de un texto, medido con la tipografía real."""
    from PIL import ImageFont
    if familia not in _PIL:
        _PIL[familia] = ImageFont.truetype(str(AQUI / "fuentes" / "estaticas" / _FAMILIAS[familia]), 1000)
    return _PIL[familia].getlength(texto) / 1000 * pt * 25.4 / 72


def partir(texto, familia, pt, ancho_max=ANCHO_UTIL * 0.96):
    """Corta `texto` en la menor cantidad de líneas, con largos parejos. Devuelve HTML con <br>."""
    palabras = texto.split()
    if ancho_mm(texto, familia, pt) <= ancho_max:
        return esc(texto)
    from itertools import combinations
    for n in (2, 3, 4):
        mejor = None
        for cortes in combinations(range(1, len(palabras)), n - 1):
            lim = (0, *cortes, len(palabras))
            lineas = [" ".join(palabras[a:b]) for a, b in zip(lim, lim[1:])]
            anchos = [ancho_mm(l, familia, pt) for l in lineas]
            if max(anchos) <= ancho_max and (mejor is None or max(anchos) < mejor[0]):
                mejor = (max(anchos), lineas)
        if mejor:
            return "<br>".join(esc(l) for l in mejor[1])
    raise ValueError(f"no se pudo partir: {texto!r}")


def css():
    f = (AQUI / "fuentes" / "estaticas").as_uri()
    return f"""
@font-face {{ font-family: 'Fraunces'; font-weight: 700; src: url('{f}/Fraunces-Titulo.ttf'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 500; src: url('{f}/Manrope-Medium.ttf'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 700; src: url('{f}/Manrope-Bold.ttf'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 800; src: url('{f}/Manrope-ExtraBold.ttf'); }}
@page {{ size: {ANCHO}mm {ALTO}mm; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #fff; }}
body {{ font-family: 'Manrope', sans-serif; font-weight: 500; font-size: 18pt; line-height: 1.4; color: {TINTA}; }}
.pagina {{ position: relative; width: {ANCHO}mm; height: {ALTO}mm; overflow: hidden;
          page-break-after: always; background: #fff; }}
.pagina:last-child {{ page-break-after: auto; }}
.caja {{ position: absolute; left: {MARGEN}mm; width: {ANCHO_UTIL}mm; }}
.num {{ position: absolute; left: 0; width: {ANCHO}mm; bottom: {MARGEN}mm; text-align: center;
        font-weight: 700; font-size: 16pt; line-height: 1.2; }}
.pestana {{ position: absolute; right: 0; width: {PESTANA_ANCHO}mm; height: {PESTANA_ALTO}mm;
            border-radius: 3mm 0 0 3mm; }}
h1, .serif {{ font-family: 'Fraunces', serif; font-weight: 700; margin: 0; }}
p {{ margin: 0; }}
b {{ font-weight: 800; }}
img {{ display: block; }}

/* portada */
.banda {{ position: absolute; left: {MARGEN}mm; width: {ANCHO_UTIL}mm; top: 17mm; height: 14mm;
          border-radius: 7mm; background: #5b2a86; color: #fff; text-align: center;
          font-weight: 800; font-size: 20pt; letter-spacing: 0.14em; line-height: 14mm; }}
.titulo-portada {{ text-align: center; font-size: 46pt; line-height: 1.08; color: #3b1f5c; }}
.subtitulo {{ text-align: center; font-size: 28pt; color: #8e4bb5; }}
.creado {{ text-align: center; font-weight: 800; font-size: 20pt; }}
.paramama {{ text-align: center; font-family: 'Fraunces', serif; font-weight: 700; font-size: 22pt; color: #3b1f5c; }}

/* dedicatoria */
.dedic {{ text-align: center; font-size: 20pt; line-height: 1.7; }}
.dedic .firma {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 28pt; line-height: 1.5; }}
.dedic .estrofa {{ margin-bottom: 7mm; }}

/* cómo usar */
.titulo-uso {{ font-size: 44pt; line-height: 1.1; }}
.paso {{ display: flex; align-items: center; margin-bottom: 12mm; }}
.paso .n {{ flex: 0 0 15mm; width: 15mm; height: 15mm; border: 0.75mm solid {TINTA}; border-radius: 50%;
           text-align: center; font-family: 'Fraunces', serif; font-weight: 700; font-size: 24pt; line-height: 13.5mm; }}
.paso .t {{ margin-left: 8mm; font-size: 24pt; line-height: 1.3; }}
.nota-uso {{ border: 0.75mm solid {TINTA}; border-radius: 6mm; padding: 8mm 9mm; font-size: 22pt; line-height: 1.45; }}

/* presentación de capítulo */
.titulo-cap {{ font-size: 58pt; line-height: 1.05; margin-bottom: 7mm; }}
.esta-en {{ font-size: 18pt; margin-bottom: 5mm; }}
.emocion {{ font-size: 20pt; line-height: 1.35; margin-bottom: 11mm; }}
.color-fila {{ display: flex; align-items: center; margin-bottom: 13mm; }}
.color-fila svg {{ flex: 0 0 22mm; }}
.color-fila p {{ margin-left: 7mm; font-size: 18pt; line-height: 1.35; }}
.afirmacion {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 32pt; line-height: 1.2; margin-bottom: 13mm; }}
.respiracion {{ font-size: 18pt; line-height: 1.4; margin-bottom: 13mm; }}
.pregunta {{ font-weight: 700; font-size: 20pt; line-height: 1.35; margin-bottom: 3mm; }}
.renglon {{ height: 16mm; border-bottom: 0.75mm solid {TINTA}; }}
.nota-escribir {{ font-size: 18pt; margin-top: 5mm; }}

/* mandala */
.pie-afirmacion {{ position: absolute; left: {MARGEN}mm; width: {ANCHO_UTIL}mm; text-align: center;
                   font-family: 'Fraunces', serif; font-weight: 700; font-size: 32pt; line-height: 1.22; }}
"""


# ================================================================= PÁGINAS (HTML)
def esc(t):
    return html.escape(t, quote=False)


def pestana(indice, clave):
    top = MARGEN + indice * PESTANA_PASO
    return f'<div class="pestana" style="top:{top}mm; background:{M.COLORES[clave]}"></div>'


def numero(n):
    return f'<div class="num">{n}</div>'


def _svg_img(ruta_svg, ancho_mm):
    return f'<img src="{(AQUI / ruta_svg).as_uri()}" style="width:{ancho_mm}mm">'


def pagina_portada():
    mandala = M.portada_mandala()
    ancho = 2 * (72 + 1)
    cy = 168
    top = cy - ancho / 2
    return f"""
<section class="pagina">
  <div class="banda">{esc(BANDA)}</div>
  <div class="caja titulo-portada serif" style="top:40mm">{esc(TITULO_LIBRO[0])}<br>{esc(TITULO_LIBRO[1])}</div>
  <div class="caja subtitulo serif" style="top:80mm">{esc(SUBTITULO)}</div>
  <div style="position:absolute; left:{(ANCHO - ancho) / 2}mm; top:{top}mm; width:{ancho}mm">{mandala}</div>
  <div class="caja creado" style="top:250mm">{esc(CREADO_POR)}</div>
  <div class="caja paramama" style="top:262mm">{esc(PARA_MAMA)}</div>
</section>"""


def pagina_dedicatoria(n):
    corazon = M.corazon_linea()
    ancho = 2 * (27 + 1)
    estrofas = [e.split("\n") for e in DEDICATORIA.strip().split("\n\n")]
    cuerpo = ""
    for i, lineas in enumerate(estrofas):
        ultima = i == len(estrofas) - 1
        if ultima:
            # la última línea (la firma) va en la tipografía de títulos
            lineas_html = "<br>".join(esc(l) for l in lineas[:-1]) + f'<br><span class="firma">{esc(lineas[-1])}</span>'
        else:
            lineas_html = "<br>".join(esc(l) for l in lineas)
        cuerpo += f'<p class="estrofa">{lineas_html}</p>'
    return f"""
<section class="pagina">
  <div style="position:absolute; left:{(ANCHO - ancho) / 2}mm; top:48mm; width:{ancho}mm">{corazon}</div>
  <div class="caja dedic" style="top:110mm">{cuerpo}</div>
</section>"""


def pagina_como_usar(n):
    pasos = "".join(
        f'<div class="paso"><div class="n">{i}</div><div class="t">{esc(t)}</div></div>'
        for i, t in enumerate(COMO_USAR_PASOS, 1))
    return f"""
<section class="pagina">
  <div class="caja" style="top:{MARGEN + 8}mm">
    <h1 class="titulo-uso" style="margin-bottom:20mm">{esc(COMO_USAR_TITULO)}</h1>
    {pasos}
    <div class="nota-uso" style="margin-top:18mm">{partir(COMO_USAR_NOTA, "cuerpo", 22, ANCHO_UTIL - 2 * 9 - 4)}</div>
  </div>
  {numero(n)}
</section>"""


def pagina_presentacion(ch, indice, n):
    color = M.COLORES[ch["clave"]]
    circulo = (f'<svg width="22mm" height="22mm" viewBox="0 0 22 22" xmlns="http://www.w3.org/2000/svg">'
               f'<circle cx="11" cy="11" r="10.5" fill="{color}" stroke="{M.NEGRO}" stroke-width="{M.LINEA}"/></svg>')
    afirmacion = "<br>".join(esc(l) for l in ch["afirmacion"])
    return f"""
<section class="pagina">
  {pestana(indice, ch["clave"])}
  <div class="caja" style="top:{MARGEN}mm">
    <h1 class="titulo-cap">{esc(ch["nombre"])}</h1>
    <p class="esta-en"><b>Está en:</b> {esc(ch["esta_en"])}.</p>
    <p class="emocion"><b>Emoción que cuida:</b> {partir(ch["emocion"] + ".", "cuerpo", 20, ANCHO_UTIL * 0.96 - ancho_mm("Emoción que cuida: ", "negrita", 20))}</p>
    <div class="color-fila">{circulo}<p>{esc(TEXTO_COLOR)}</p></div>
    <p class="afirmacion">{afirmacion}</p>
    <p class="respiracion"><b>Respirá:</b> {esc(ch["respiracion"])}</p>
    <p class="pregunta">{partir(ch["pregunta"], "negrita", 20)}</p>
    <div class="renglon"></div><div class="renglon"></div><div class="renglon"></div>
    <p class="nota-escribir">{esc(TEXTO_ESCRIBIR)}</p>
  </div>
  {numero(n)}
</section>"""


def pagina_mandala(ch, indice, n, ruta_svg, radio):
    ancho = 2 * (radio + 2)
    cy = CENTRO_MANDALA_Y
    top = cy - ancho / 2
    afirmacion = "<br>".join(esc(l) for l in ch["afirmacion"])
    return f"""
<section class="pagina">
  {pestana(indice, ch["clave"])}
  <div style="position:absolute; left:{(ANCHO - ancho) / 2}mm; top:{top}mm; width:{ancho}mm">{_svg_img(ruta_svg, ancho)}</div>
  <div class="pie-afirmacion" style="top:218mm">{afirmacion}</div>
  {numero(n)}
</section>"""


# ===================================================================== ARMADO
def informacion_paginas(fase=1):
    """Descripción de cada página impresa, para los controles de verificar.py."""
    info = [dict(nombre="portada", numero=None), dict(nombre="dedicatoria", numero=None),
            dict(nombre="como_usar", numero=3)]
    n = 4
    for i, ch in enumerate(CHAKRAS[:1] if fase == 1 else CHAKRAS):
        info.append(dict(nombre=f"{ch['clave']}_presentacion", numero=n, clave=ch["clave"], afirmacion=ch["afirmacion"]))
        info.append(dict(nombre=f"{ch['clave']}_mandala", numero=n + 1, clave=ch["clave"], afirmacion=ch["afirmacion"],
                         mandala=(ANCHO / 2, CENTRO_MANDALA_Y, M.RADIO_MANDALA)))
        n += 2
    return info


def construir(fase):
    preparar_fuentes()
    (AQUI / "svg").mkdir(exist_ok=True)
    (AQUI / "preview").mkdir(exist_ok=True)

    mandalas_svg = {"raiz": M.raiz()}
    for clave, svg in mandalas_svg.items():
        (AQUI / "svg" / f"{clave}.svg").write_text(svg, encoding="utf-8")
    (AQUI / "svg" / "portada_mandala.svg").write_text(M.portada_mandala(), encoding="utf-8")
    (AQUI / "svg" / "dedicatoria_corazon.svg").write_text(M.corazon_linea(), encoding="utf-8")

    # (nombre de archivo del PNG, html)
    paginas = []
    n = 1
    paginas.append(("portada_PROVISORIA" if PORTADA_PROVISORIA else "portada", pagina_portada()))
    n += 1
    paginas.append(("dedicatoria", pagina_dedicatoria(n)))
    n += 1
    paginas.append(("como_usar", pagina_como_usar(n)))
    n += 1
    chakras = CHAKRAS[:1] if fase == 1 else CHAKRAS
    for i, ch in enumerate(chakras):
        paginas.append((f"{ch['clave']}_presentacion", pagina_presentacion(ch, i, n)))
        n += 1
        paginas.append((f"{ch['clave']}_mandala", pagina_mandala(ch, i, n, f"svg/{ch['clave']}.svg", M.RADIO_MANDALA)))
        n += 1

    documento = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Mandalas de los chakras · Un color a la vez</title><style>{css()}</style></head>
<body>{"".join(h for _, h in paginas)}</body></html>"""
    (AQUI / "_tmp").mkdir(exist_ok=True)
    (AQUI / "_tmp" / "libro.html").write_text(documento, encoding="utf-8")

    from weasyprint import HTML
    pdf_paginas = AQUI / "_tmp" / "paginas_impresas.pdf"
    HTML(string=documento, base_url=str(AQUI)).write_pdf(str(pdf_paginas))

    # PDF final: cada página impresa va seguida de su reverso en blanco, así
    # el marcador no traspasa y la impresión doble faz sale bien.
    from pypdf import PdfReader, PdfWriter
    lector = PdfReader(str(pdf_paginas))
    escritor = PdfWriter()
    for p in lector.pages:
        escritor.add_page(p)
        escritor.add_blank_page(width=p.mediabox.width, height=p.mediabox.height)
    escritor.add_metadata({"/Title": "Mandalas de los chakras · Un color a la vez",
                           "/Author": "Dani Navarro (Daniela Navarro · Longevidad Emocional)"})
    salida = AQUI / ("libro_mandalas_chakras_fase1.pdf" if fase == 1 else "libro_mandalas_chakras.pdf")
    with open(salida, "wb") as fh:
        escritor.write(fh)

    # PNG de revisión (solo páginas impresas)
    prev = AQUI / "preview"
    for viejo in prev.glob("*.png"):
        viejo.unlink()
    subprocess.run(["pdftoppm", "-r", "110", "-png", str(pdf_paginas), str(prev / "p")], check=True)
    generados = sorted(prev.glob("p-*.png"))      # pdftoppm numera p-1, p-01… según la cantidad
    assert len(generados) == len(paginas), (len(generados), len(paginas))
    for i, (origen, (nombre, _)) in enumerate(zip(generados, paginas), 1):
        origen.rename(prev / f"{i:02d}_{nombre}.png")
    print(f"PDF: {salida.name} ({len(lector.pages)} páginas impresas, {2 * len(lector.pages)} con reversos)")
    print("PNG:", ", ".join(sorted(p.name for p in prev.glob('*.png'))))
    return mandalas_svg


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fase", type=int, default=1, choices=[1, 2])
    args = ap.parse_args()
    if args.fase == 2:
        sys.exit("La fase 2 (resto de los chakras, integración y cierre) se genera después de aprobar la fase 1.")
    construir(args.fase)
