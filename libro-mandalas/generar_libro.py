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

Te amo con todo mi corazón,
Dani"""

TITULO_LIBRO = ("MANDALAS", "DE LOS CHAKRAS")
SUBTITULO = "Un color a la vez"
BANDA = "LIBRO PARA COLOREAR"
BANDA_SUB = "Diseñado con mandalas simples y frases positivas"
CREADO_POR = "Creado por Dani Navarro"
PARA_MAMA = "Para mamá, con todo mi amor."

COMO_USAR_TITULO = "Cómo usar este libro"
COMO_USAR_PASOS = [
    "Elegí un mandala.",
    "Respirá tres veces, bien lento.",
    "Pintá sin apuro.",
    "No hay forma de hacerlo mal.",
    "Al terminar, leé la frase en voz alta.",
    "Después, respondé la pregunta de la página siguiente.",
]
COMO_USAR_NOTA = ("Usá papel de 120 g o más, y lápices o marcadores gruesos, "
                  "fáciles de agarrar.")

TEXTO_COLOR = "Este es su color, pero podés usar los que quieras."
TEXTO_ESCRIBIR = "Podés escribirlo o contárselo a alguien."
LEER_FRASE = "Al terminar, leé en voz alta:"

# clave, nombre, "Está en", emoción que cuida, afirmación (líneas), respiración, pregunta
CHAKRAS = [
    dict(clave="raiz", nombre="Raíz", petalos=4, zonas=(25, 30),   # 27 zonas
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

# Colores de texto de la portada (tomados de portada.png)
COLOR_TITULO = "#1F3466"   # MANDALAS
COLOR_TEXTO = "#4A3B33"    # subtítulo y "Creado por"
COLOR_MAMA = "#253A6A"     # "Para mamá, con todo mi amor."

# ================================================================== MEDIDAS (mm)
MARGEN = 15
ANCHO, ALTO = 210, 297
ANCHO_UTIL = ANCHO - 2 * MARGEN
PESTANA_ANCHO = 8
PESTANA_ALTO = 34
CENTRO_MANDALA_Y = 134      # centro del mandala medido desde arriba (deja lugar al nombre y a la frase)
PESTANA_PASO = 38          # cada capítulo baja un escalón, para encontrarlo al hojear
TINTA = "#1b1b1b"

# ======================================================================= FUENTES
def preparar_fuentes():
    """Crea las instancias estáticas de Fraunces y Manrope (si faltan o si cambiaron los parámetros)."""
    import json
    destino = AQUI / "fuentes" / "estaticas"
    fr = "Fraunces[SOFT,WONK,opsz,wght].ttf"
    fri = "Fraunces-Italic[SOFT,WONK,opsz,wght].ttf"
    trabajos = [
        (fr, "Fraunces-Titulo.ttf", {"wght": 700, "opsz": 36, "SOFT": 100, "WONK": 0}),
        # portada (diseño de Dani): título, subtítulo, "Creado por" y "Para mamá"
        (fr, "Fraunces-Portada.ttf", {"wght": 600, "opsz": 36, "SOFT": 0, "WONK": 0}),
        (fri, "Fraunces-Italica.ttf", {"wght": 400, "opsz": 72, "SOFT": 30, "WONK": 0}),
        (fr, "Fraunces-Creado.ttf", {"wght": 600, "opsz": 72, "SOFT": 50, "WONK": 0}),
        (fri, "Fraunces-Mama.ttf", {"wght": 500, "opsz": 48, "SOFT": 50, "WONK": 0}),
        ("Manrope[wght].ttf", "Manrope-Medium.ttf", {"wght": 500}),
        ("Manrope[wght].ttf", "Manrope-Bold.ttf", {"wght": 700}),
        ("Manrope[wght].ttf", "Manrope-ExtraBold.ttf", {"wght": 800}),
    ]
    marca = destino / ".trabajos.json"
    firma = json.dumps(trabajos, sort_keys=True)
    if marca.exists() and marca.read_text() == firma and all((destino / dst).exists() for _, dst, _ in trabajos):
        return
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    destino.mkdir(parents=True, exist_ok=True)
    for src, dst, ejes in trabajos:
        fuente = TTFont(AQUI / "fuentes" / src)
        instancer.instantiateVariableFont(fuente, ejes).save(destino / dst)
    marca.write_text(firma)


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
@font-face {{ font-family: 'FrauncesPortada'; font-weight: 600; font-style: normal; src: url('{f}/Fraunces-Portada.ttf'); }}
@font-face {{ font-family: 'FrauncesItalica'; font-weight: 400; font-style: italic; src: url('{f}/Fraunces-Italica.ttf'); }}
@font-face {{ font-family: 'FrauncesCreado'; font-weight: 600; font-style: normal; src: url('{f}/Fraunces-Creado.ttf'); }}
@font-face {{ font-family: 'FrauncesMama'; font-weight: 500; font-style: italic; src: url('{f}/Fraunces-Mama.ttf'); }}
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

/* portada: el diseño de Dani. El arte (tarjeta, banda, flores) es un SVG; los textos se ubican por línea base */
.arte {{ position: absolute; left: 0; top: 0; width: {ANCHO}mm; height: {ALTO}mm; }}
.tb {{ position: absolute; left: {MARGEN}mm; width: {ANCHO_UTIL}mm; text-align: center; line-height: 1; white-space: nowrap; }}

/* dedicatoria */
.dedic {{ text-align: center; font-size: 20pt; line-height: 1.7; }}
.dedic .firma {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 28pt; line-height: 1.5; }}
.dedic .estrofa {{ margin-bottom: 7mm; }}

/* cómo usar */
.titulo-uso {{ font-size: 44pt; line-height: 1.1; }}
.paso {{ display: flex; align-items: center; margin-bottom: 8.5mm; }}
.paso .n {{ flex: 0 0 15mm; width: 15mm; height: 15mm; border: 0.75mm solid {TINTA}; border-radius: 50%;
           text-align: center; font-family: 'Fraunces', serif; font-weight: 700; font-size: 24pt; line-height: 13.5mm; }}
.paso .t {{ margin-left: 8mm; font-size: 24pt; line-height: 1.3; }}
.nota-uso {{ border: 0.75mm solid {TINTA}; border-radius: 6mm; padding: 8mm 9mm; font-size: 22pt; line-height: 1.45; }}

/* página del mandala: nombre + color arriba, frase abajo */
.cab-fila {{ display: flex; align-items: center; }}
.cab-fila svg {{ flex: 0 0 15mm; }}
.titulo-mandala {{ margin-left: 6mm; font-size: 40pt; line-height: 1.05; }}
.color-texto {{ margin-top: 3mm; font-size: 18pt; line-height: 1.35; }}
.etiqueta-frase {{ position: absolute; left: {MARGEN}mm; width: {ANCHO_UTIL}mm; text-align: center; font-weight: 700; font-size: 18pt; }}
.pie-afirmacion {{ position: absolute; left: {MARGEN}mm; width: {ANCHO_UTIL}mm; text-align: center;
                   font-family: 'Fraunces', serif; font-weight: 700; font-size: 32pt; line-height: 1.22; }}

/* página de reflexión: la tarea, después de decir la frase */
.titulo-cap {{ font-size: 58pt; line-height: 1.05; margin-bottom: 9mm; }}
.esta-en {{ font-size: 18pt; margin-bottom: 6mm; }}
.emocion {{ font-size: 20pt; line-height: 1.35; margin-bottom: 14mm; }}
.respiracion {{ font-size: 18pt; line-height: 1.4; margin-bottom: 16mm; }}
.pregunta {{ font-weight: 700; font-size: 20pt; line-height: 1.35; margin-bottom: 4mm; }}
.renglon {{ height: 25mm; border-bottom: 0.75mm solid {TINTA}; }}
.nota-escribir {{ font-size: 18pt; margin-top: 6mm; }}
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


_METRICAS = {}


def _metricas(ttf):
    """(ascenso, descenso) de la tipografía, en em (tabla hhea), para ubicar textos por su línea base."""
    if ttf not in _METRICAS:
        from fontTools.ttLib import TTFont
        f = TTFont(AQUI / "fuentes" / "estaticas" / ttf)
        _METRICAS[ttf] = (f["hhea"].ascent / f["head"].unitsPerEm, -f["hhea"].descent / f["head"].unitsPerEm)
    return _METRICAS[ttf]


def texto_base(contenido, ttf, familia, pt, base_mm, color, peso=400, estilo="normal", tracking=0.0):
    """Texto centrado cuya línea base cae exactamente en `base_mm` (mm desde arriba)."""
    asc, desc = _metricas(ttf)
    cuerpo = pt * 25.4 / 72
    top = base_mm - cuerpo * (1 + asc - desc) / 2          # con line-height:1 la base queda a (1+asc-desc)/2 del tope
    return (f'<div class="tb" style="top:{top:.3f}mm; font-family:\'{familia}\'; font-weight:{peso}; font-style:{estilo}; '
            f'font-size:{pt}pt; letter-spacing:{tracking}em; color:{color}">{contenido}</div>')


def pagina_portada():
    """La portada de Dani, a todo color. Solo cambia el subtítulo ("Un color a la vez")."""
    colores = [M.COLORES_FLOR[c]["linea"] for c in ("rojo", "naranja", "amarillo", "verde", "azul", "indigo", "centro")]
    letras, i = "", 0
    for ch in TITULO_LIBRO[1]:
        if ch == " ":
            letras += " "
        else:
            letras += f'<span style="color:{colores[i % 7]}">{ch}</span>'
            i += 1
    return f"""
<section class="pagina">
  <div class="arte">{M.portada_arte()}</div>
  {texto_base(esc(TITULO_LIBRO[0]), "Fraunces-Portada.ttf", "FrauncesPortada", 64.9, 44.8 - M.SUBIR_TITULO, COLOR_TITULO, 600)}
  {texto_base(letras, "Manrope-ExtraBold.ttf", "Manrope", 33.7, 60.0 - M.SUBIR_TITULO, COLOR_TITULO, 800, tracking=0.02)}
  {texto_base(esc(SUBTITULO), "Fraunces-Italica.ttf", "FrauncesItalica", 32, 73.2 - M.SUBIR_TITULO, COLOR_TEXTO, 400, "italic")}
  {texto_base(esc(CREADO_POR), "Fraunces-Creado.ttf", "FrauncesCreado", 20.0, 239.1 - M.SUBIR_RESTO, COLOR_TEXTO, 600)}
  {texto_base(esc(BANDA), "Manrope-ExtraBold.ttf", "Manrope", 26.2, 255.7 - M.SUBIR_RESTO, "#fff", 800, tracking=0.03)}
  {texto_base(esc(BANDA_SUB), "Manrope-Medium.ttf", "Manrope", 18, 264.6 - M.SUBIR_RESTO, "#fff", 500, tracking=0.02)}
  {texto_base(esc(PARA_MAMA), "Fraunces-Mama.ttf", "FrauncesMama", 21.7, 282.4 - M.SUBIR_RESTO, COLOR_MAMA, 500, "italic")}
</section>"""


def pagina_dedicatoria(n):
    corazon = M.corazon_linea()
    ancho = 2 * (M.RADIO_CORAZON + 1)
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
  <div style="position:absolute; left:{(ANCHO - ancho) / 2}mm; top:38mm; width:{ancho}mm">{corazon}</div>
  <div class="caja dedic" style="top:124mm">{cuerpo}</div>
</section>"""


def pagina_como_usar(n):
    pasos = "".join(
        f'<div class="paso"><div class="n">{i}</div><div class="t">{esc(t)}</div></div>'
        for i, t in enumerate(COMO_USAR_PASOS, 1))
    return f"""
<section class="pagina">
  <div class="caja" style="top:{MARGEN + 8}mm">
    <h1 class="titulo-uso" style="margin-bottom:15mm">{esc(COMO_USAR_TITULO)}</h1>
    {pasos}
    <div class="nota-uso" style="margin-top:11mm">{partir(COMO_USAR_NOTA, "cuerpo", 22, ANCHO_UTIL - 2 * 9 - 4)}</div>
  </div>
  {numero(n)}
</section>"""


def pagina_mandala(ch, indice, n, ruta_svg, radio):
    """Primero se pinta: nombre y color arriba, mandala, y abajo la frase para leer al terminar."""
    color = M.COLORES[ch["clave"]]
    circulo = (f'<svg width="15mm" height="15mm" viewBox="0 0 15 15" xmlns="http://www.w3.org/2000/svg">'
               f'<circle cx="7.5" cy="7.5" r="7.1" fill="{color}" stroke="{M.NEGRO}" stroke-width="{M.LINEA}"/></svg>')
    ancho = 2 * (radio + 2)
    top = CENTRO_MANDALA_Y - ancho / 2
    afirmacion = "<br>".join(esc(l) for l in ch["afirmacion"])
    return f"""
<section class="pagina">
  {pestana(indice, ch["clave"])}
  <div class="caja" style="top:{MARGEN}mm">
    <div class="cab-fila">{circulo}<h1 class="titulo-mandala">{esc(ch["nombre"])}</h1></div>
    <p class="color-texto">{esc(TEXTO_COLOR)}</p>
  </div>
  <div style="position:absolute; left:{(ANCHO - ancho) / 2}mm; top:{top}mm; width:{ancho}mm">{_svg_img(ruta_svg, ancho)}</div>
  <div class="etiqueta-frase" style="top:{CENTRO_MANDALA_Y + radio + 8}mm">{esc(LEER_FRASE)}</div>
  <div class="pie-afirmacion" style="top:{CENTRO_MANDALA_Y + radio + 18}mm">{afirmacion}</div>
  {numero(n)}
</section>"""


def pagina_reflexion(ch, indice, n):
    """Después de leer la frase: la tarea (pregunta de recuerdo). La frase no se repite acá."""
    return f"""
<section class="pagina">
  {pestana(indice, ch["clave"])}
  <div class="caja" style="top:{MARGEN}mm">
    <h1 class="titulo-cap">{esc(ch["nombre"])}</h1>
    <p class="esta-en"><b>Está en:</b> {esc(ch["esta_en"])}.</p>
    <p class="emocion"><b>Emoción que cuida:</b> {partir(ch["emocion"] + ".", "cuerpo", 20, ANCHO_UTIL * 0.96 - ancho_mm("Emoción que cuida: ", "negrita", 20))}</p>
    <p class="respiracion"><b>Respirá:</b> {esc(ch["respiracion"])}</p>
    <p class="pregunta">{partir(ch["pregunta"], "negrita", 20)}</p>
    <div class="renglon"></div><div class="renglon"></div><div class="renglon"></div>
    <p class="nota-escribir">{esc(TEXTO_ESCRIBIR)}</p>
  </div>
  {numero(n)}
</section>"""


# ===================================================================== ARMADO
def informacion_paginas(fase=1):
    """Descripción de cada página impresa, para los controles de verificar.py."""
    info = [dict(nombre="portada", numero=None), dict(nombre="dedicatoria", numero=None),
            dict(nombre="como_usar", numero=3)]
    n = 4
    for i, ch in enumerate(CHAKRAS[:1] if fase == 1 else CHAKRAS):
        info.append(dict(nombre=f"{ch['clave']}_mandala", numero=n, clave=ch["clave"], afirmacion=ch["afirmacion"],
                         mandala=(ANCHO / 2, CENTRO_MANDALA_Y, M.RADIO_MANDALA)))
        info.append(dict(nombre=f"{ch['clave']}_reflexion", numero=n + 1, clave=ch["clave"],
                         sin_texto=ch["afirmacion"]))      # la frase aparece una sola vez por capítulo
        n += 2
    return info


def construir(fase):
    preparar_fuentes()
    (AQUI / "svg").mkdir(exist_ok=True)
    (AQUI / "preview").mkdir(exist_ok=True)

    mandalas_svg = {"raiz": M.raiz()}
    for clave, svg in mandalas_svg.items():
        (AQUI / "svg" / f"{clave}.svg").write_text(svg, encoding="utf-8")
    (AQUI / "svg" / "portada_arte.svg").write_text(M.portada_arte(), encoding="utf-8")
    (AQUI / "svg" / "dedicatoria_corazon.svg").write_text(M.corazon_linea(), encoding="utf-8")

    # (nombre de archivo del PNG, html)
    paginas = []
    n = 1
    paginas.append(("portada", pagina_portada()))
    n += 1
    paginas.append(("dedicatoria", pagina_dedicatoria(n)))
    n += 1
    paginas.append(("como_usar", pagina_como_usar(n)))
    n += 1
    chakras = CHAKRAS[:1] if fase == 1 else CHAKRAS
    for i, ch in enumerate(chakras):
        paginas.append((f"{ch['clave']}_mandala", pagina_mandala(ch, i, n, f"svg/{ch['clave']}.svg", M.RADIO_MANDALA)))
        n += 1
        paginas.append((f"{ch['clave']}_reflexion", pagina_reflexion(ch, i, n)))
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
