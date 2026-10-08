#!/usr/bin/env python3
"""MANDALAS DE LOS 7 CHAKRAS · Un color a la vez
Creado por Dani Navarro (Daniela Navarro · Longevidad Emocional).

Genera el libro para colorear (8,5 × 11 pulgadas, vertical, listo para KDP):
  - svg/      cada mandala como SVG vectorial (geometría calculada en mandalas.py)
  - preview/  un PNG por página impresa (recortado al tamaño final)
  - libro_mandalas_chakras.pdf  con sangrado de 0,125" y una hoja en blanco detrás de cada página

Uso:
    python3 generar_libro.py              # el libro completo (27 páginas impresas)
    python3 verificar.py                  # controles de calidad sobre lo generado

Dependencias: weasyprint, pypdf, cairosvg, fonttools, pillow, numpy, scipy, pdfminer.six
y `pdftoppm` (poppler) para los PNG de revisión.
"""
import html
import subprocess
from pathlib import Path

import mandalas as M

AQUI = Path(__file__).resolve().parent

# ===================================================================== TEXTOS
# Todo lo que se lee en el libro está acá, fácil de editar.

DEDIC_TITULO = "Para vos, mamá"
# cada línea que empieza con ** va en negrita
DEDIC_ESTROFAS = [
    ["Que siempre estuviste a mi lado", "y me diste fuerza para salir adelante."],
    ["Hoy te devuelvo un poco de todo eso:", "**un rato de calma,", "**un color a la vez."],
    ["Pintá despacio, respirá tranquila", "y disfrutá cada página."],
    ["Te amo con todo mi corazón,"],
]
DEDIC_FIRMA = "Dani"

TITULO_LIBRO = ("MANDALAS", "DE LOS 7 CHAKRAS")
SUBTITULO = "Un color a la vez"
TAGLINE = "Para colorear, reflexionar y disfrutar"
BANDA = "LIBRO PARA COLOREAR"
CREADO_POR = "Creado por Dani Navarro"
PARA_MAMA = "Para mamá, con todo mi amor."

COMO_USAR_TITULO = "Cómo usar este libro"
COMO_USAR_PASOS = [
    "Elegí un mandala.\nMirá el ejemplo, si querés.",
    "Respirá tres veces, bien lento.",
    "Pintá sin apuro.",
    "Al terminar, leé la frase en voz alta.",
    "Si querés, respondé la pregunta\nde la página siguiente.",
]
COMO_USAR_NOTA = ("Usá lápices de colores o marcadores de punta suave. "
                  "Si usás marcadores, poné una hoja protectora detrás.")

TITULO_EJEMPLO = "Así podría quedar"
NOTA_EJEMPLO = "Este es solo un ejemplo. Podés copiarlo o elegir tus propios colores."
LEER_FRASE = "Al terminar, leé en voz alta:"
TEXTO_ESCRIBIR = "Podés escribirlo o contárselo a alguien."
TITULO_RESPIRAR = "Una respiración para volver al presente"
TITULO_RECORDAR = "Para recordar"

INTEGRACION_TITULO = "TODOS JUNTOS"
INTEGRACION_ARRIBA = "Las siete flores representan los siete chakras."
INTEGRACION_COLORES = "Rojo · naranja · amarillo · verde · azul · índigo · violeta"
INTEGRACION_ABAJO = "Podés colorearlas siguiendo la paleta sugerida o crear tu propia combinación."
INTEGRACION_FRASE = ["Cada color, una historia.", "Cada página, un momento para vos."]

COMPARTIR_TITULO = "Un momento para compartir"
COMPARTIR_PARRAFOS = [
    ["Este libro también puede disfrutarse acompañado."],
    ["Podés colorear junto a tu hija, tu hijo, una nieta, un nieto, una amiga o alguien especial."],
    ["Elegí una página.", "Elegí los colores."],
    ["Y mientras colorean, dejá que aparezca una historia."],
]
COMPARTIR_FRASE = "A veces, una conversación comienza con un color."

CIERRE_TITULO = "Gracias por regalarte este rato."
FRASE_FINAL = ["Un color a la vez,", "un momento a la vez."]
CIERRE_SENTI = "Hoy me sentí…"
CIERRE_FECHA = "Fecha:"
CIERRE_NOTA = "Podés volver a esta página cada vez que quieras recordar cómo te sentiste."

# clave, nombre, "relación" (qué cuida), afirmación (líneas), respiración (líneas), pregunta
CHAKRAS = [
    dict(clave="raiz", nombre="Raíz",
         relacion="Está relacionado con la sensación de seguridad, pertenencia y sostén.",
         afirmacion=["Estoy a salvo.", "La vida me sostiene."],
         respiracion=["Sentí tus pies apoyados.", "Inhalá suavemente y soltá el aire despacio."],
         pregunta="¿Qué cosa buena aprendiste de tu familia que todavía llevás con vos?"),
    dict(clave="sacro", nombre="Sacro",
         relacion="Está relacionado con el disfrute, la creatividad y el placer de vivir.",
         afirmacion=["Me permito disfrutar."],
         respiracion=["Aflojá la panza y los hombros.", "Inhalá suavemente y soltá el aire despacio."],
         pregunta="¿Qué te encantaba hacer cuando eras joven?"),
    dict(clave="plexo", nombre="Plexo solar",
         relacion="Está relacionado con la confianza, la fuerza interior y la claridad.",
         afirmacion=["Confío en mí", "y en mis decisiones."],
         respiracion=["Sentí el centro de tu cuerpo.", "Inhalá suavemente y soltá despacio,", "como apagando una vela."],
         pregunta="¿Qué decisión tuya te da orgullo?"),
    dict(clave="corazon", nombre="Corazón",
         relacion="Está relacionado con el amor, la gratitud y la apertura hacia los demás.",
         afirmacion=["Doy y recibo amor", "con facilidad."],
         respiracion=["Poné una mano sobre tu pecho.", "Inhalá suavemente y soltá el aire despacio."],
         pregunta="¿A quién querés agradecerle hoy?"),
    dict(clave="garganta", nombre="Garganta",
         relacion="Está relacionado con la voz, la expresión y la comunicación sincera.",
         afirmacion=["Mi voz y mis palabras", "importan."],
         respiracion=["Sentí el cuello y los hombros sueltos.", "Inhalá y soltá con un suspiro suave."],
         pregunta="¿Qué consejo le darías a tu nieto?"),
    dict(clave="tercer_ojo", nombre="Tercer ojo",
         relacion="Está relacionado con la intuición, la percepción y la mirada interior.",
         afirmacion=["Confío en mi intuición", "y en mi propia mirada."],
         respiracion=["Cerrá los ojos, si te resulta cómodo.", "Inhalá suavemente y soltá el aire despacio."],
         pregunta="¿Cuándo tu intuición te guió bien?"),
    dict(clave="corona", nombre="Corona",
         relacion="Está relacionado con la paz, el sentido y la contemplación.",
         afirmacion=["Estoy en paz", "en este momento."],
         respiracion=["Inhalá suavemente.", "Al soltar el aire, imaginá una luz suave."],
         pregunta="¿Qué te da paz en este momento de tu vida?"),
]

# Colores de texto de la portada (tomados de la portada original de Dani)
COLOR_TITULO = "#1F3466"   # MANDALAS
COLOR_TEXTO = "#4A3B33"    # subtítulo, tagline y "Creado por"
COLOR_MAMA = "#253A6A"     # "Para mamá, con todo mi amor."

# ================================================================== MEDIDAS (mm)
ANCHO, ALTO = M.ANCHO_PAGINA, M.ALTO_PAGINA      # 8,5 × 11 pulgadas (tamaño final, ya cortado)
SANGRE = 3.175                                    # 0,125": KDP pide sangrado arriba, abajo y afuera
PAG_W, PAG_H = ANCHO + SANGRE, ALTO + 2 * SANGRE  # tamaño del PDF con sangrado: 8,625 × 11,25"
MARGEN_INT = 19.05        # 0,75" del lado del lomo (izquierda en las páginas impares, que son las que se imprimen)
MARGEN_EXT = 15.0
MARGEN_SUP = 12.7         # 0,5"
MARGEN_INF = 12.7
X0 = MARGEN_INT
X1 = ANCHO - MARGEN_EXT
ANCHO_UTIL = X1 - X0
CX = (X0 + X1) / 2        # eje de la composición (el lomo "se come" unos mm, así se ve centrado)
PESTANA_ANCHO = 8
PESTANA_ALTO = 32
PESTANA_PASO = 35         # cada capítulo baja un escalón, para encontrarlo al hojear
RADIO = M.RADIO_MANDALA
CENTRO_MANDALA_Y = 128.5  # centro del mandala, desde arriba del corte
CENTRO_INTEGRACION_Y = 128.5
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


def partir(texto, familia, pt, ancho_max=None):
    """Corta `texto` en la menor cantidad de líneas, con largos parejos. Devuelve HTML con <br>."""
    ancho_max = ancho_max or ANCHO_UTIL * 0.96
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
@page {{ size: {PAG_W}mm {PAG_H}mm; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #fff; }}
body {{ font-family: 'Manrope', sans-serif; font-weight: 500; font-size: 18pt; line-height: 1.4; color: {TINTA}; }}
/* la página lleva sangrado; todo se ubica dentro de .recorte, que es el tamaño final (desde el corte) */
.pagina {{ position: relative; width: {PAG_W}mm; height: {PAG_H}mm; overflow: hidden;
          page-break-after: always; background: #fff; }}
.pagina:last-child {{ page-break-after: auto; }}
.recorte {{ position: absolute; left: 0; top: {SANGRE}mm; width: {ANCHO}mm; height: {ALTO}mm; }}
.caja {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; }}
.num {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; bottom: {MARGEN_INF}mm; text-align: center;
        font-weight: 700; font-size: 18pt; line-height: 1.2; }}
.pestana {{ position: absolute; right: -{SANGRE}mm; width: {PESTANA_ANCHO + SANGRE}mm; height: {PESTANA_ALTO}mm;
            border-radius: 3mm 0 0 3mm; }}
h1, h2, .serif {{ font-family: 'Fraunces', serif; font-weight: 700; margin: 0; }}
p {{ margin: 0; }}
b {{ font-weight: 800; }}
img {{ display: block; }}
.centrado {{ text-align: center; }}

/* portada: el diseño de Dani. El arte (tarjeta, banda, flores) es un SVG; los textos se ubican por línea base */
.arte {{ position: absolute; left: 0; top: 0; width: {ANCHO}mm; height: {ALTO}mm; }}
.tb {{ position: absolute; left: 0; width: {ANCHO}mm; text-align: center; line-height: 1; white-space: nowrap; }}

/* dedicatoria */
.dedic {{ text-align: center; font-size: 20pt; line-height: 1.65; }}
.dedic h2 {{ font-size: 32pt; line-height: 1.2; margin-bottom: 9mm; }}
.dedic .estrofa {{ margin-bottom: 7mm; }}
.dedic .dest {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 22pt; }}
.dedic .firma {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 28pt; line-height: 1.5; }}

/* cómo usar */
.titulo-uso {{ font-size: 44pt; line-height: 1.1; }}
.paso {{ display: flex; align-items: center; margin-bottom: 8.5mm; }}
.paso .n {{ flex: 0 0 15mm; width: 15mm; height: 15mm; border: 0.75mm solid {TINTA}; border-radius: 50%;
           text-align: center; font-family: 'Fraunces', serif; font-weight: 700; font-size: 24pt; line-height: 13.5mm; }}
.paso .t {{ margin-left: 8mm; font-size: 24pt; line-height: 1.3; }}
.nota-uso {{ border: 0.75mm solid {TINTA}; border-radius: 6mm; padding: 8mm 9mm; font-size: 22pt; line-height: 1.45; }}

/* página del mandala: nombre y color protagonista arriba, paleta en una fila, frase abajo */
.cab {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; display: flex; justify-content: space-between; align-items: flex-end; }}
.titulo-mandala {{ font-size: 40pt; line-height: 1.05; }}
.protag {{ display: flex; align-items: center; margin: 0 0 1mm 0; font-weight: 700; font-size: 18pt; line-height: 1; height: 9mm; white-space: nowrap; }}
.protag svg {{ flex: 0 0 8mm; margin: 0 2.5mm 0 3mm; }}
.fila-paleta {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; height: 9mm; display: flex; justify-content: space-between; align-items: center; }}
.fila-paleta .sw {{ display: flex; align-items: center; font-size: 18pt; line-height: 1; white-space: nowrap; }}
.fila-paleta .sw svg {{ flex: 0 0 8mm; margin-right: 2.5mm; }}
.sub-ejemplo {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; font-family: 'Fraunces', serif; font-weight: 700; font-size: 26pt; line-height: 1.2; }}
.nota-ejemplo {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; text-align: center; font-size: 18pt; line-height: 1.4; }}
.etiqueta-frase {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; text-align: center; font-weight: 700; font-size: 18pt; }}
.pie-afirmacion {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; text-align: center;
                   font-family: 'Fraunces', serif; font-weight: 700; font-size: 32pt; line-height: 1.22; }}

/* página de reflexión: la tarea, después de decir la frase */
.titulo-cap {{ font-size: 58pt; line-height: 1.05; margin-bottom: 9mm; }}
.relacion {{ font-size: 20pt; line-height: 1.4; margin-bottom: 12mm; }}
.sub {{ font-size: 24pt; line-height: 1.2; margin-bottom: 3mm; }}
.respiracion {{ font-size: 20pt; line-height: 1.4; margin-bottom: 12mm; }}
.pregunta {{ font-weight: 700; font-size: 22pt; line-height: 1.35; margin-bottom: 3mm; }}
.renglon {{ height: 24mm; border-bottom: 0.75mm solid {TINTA}; }}
.nota-escribir {{ font-size: 18pt; margin-bottom: 3mm; }}

/* todos juntos */
.int-texto {{ font-size: 18pt; line-height: 1.35; }}
.int-colores {{ font-weight: 700; font-size: 18pt; line-height: 1.35; margin-top: 1.5mm; }}
.int-frase {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 24pt; line-height: 1.2; text-align: center; margin-top: 4mm; }}

/* un momento para compartir */
.comp-titulo {{ font-size: 38pt; line-height: 1.1; margin-bottom: 7mm; }}
.comp-p {{ font-size: 20pt; line-height: 1.4; margin-bottom: 5mm; }}
.comp-frase {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 28pt; line-height: 1.25; margin-top: 4mm; }}

/* cierre */
.cierre-titulo {{ text-align: center; font-size: 30pt; line-height: 1.2; }}
.cierre-frase {{ text-align: center; font-family: 'Fraunces', serif; font-weight: 700; font-size: 34pt; line-height: 1.2; }}
.cierre-senti {{ font-weight: 700; font-size: 24pt; line-height: 1.2; }}
.cierre-fecha {{ display: flex; align-items: flex-end; font-weight: 700; font-size: 22pt; line-height: 1.2; }}
.cierre-fecha .linea {{ flex: 1; height: 11mm; margin-left: 5mm; border-bottom: 0.75mm solid {TINTA}; }}
.cierre-nota {{ text-align: center; font-weight: 700; font-size: 20pt; line-height: 1.4; }}
"""


# ================================================================= PÁGINAS (HTML)
def esc(t):
    return html.escape(t, quote=False)


def pagina(contenido):
    return f'<section class="pagina"><div class="recorte">{contenido}</div></section>'


def pestana(indice, clave):
    top = MARGEN_SUP + indice * PESTANA_PASO
    return f'<div class="pestana" style="top:{top}mm; background:{M.COLORES[clave]}"></div>'


def numero(n):
    return f'<div class="num">{n}</div>'


def _svg_img(ruta_svg, ancho_mm):
    return f'<img src="{(AQUI / ruta_svg).as_uri()}" style="width:{ancho_mm}mm">'


def _punto(color, mm):
    r = mm / 2
    return (f'<svg width="{mm}mm" height="{mm}mm" viewBox="0 0 {mm} {mm}" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="{r}" cy="{r}" r="{r - 0.4}" fill="{color}" stroke="{M.NEGRO}" stroke-width="{M.LINEA_FINA}"/></svg>')


_METRICAS = {}


def _metricas(ttf):
    """(ascenso, descenso) de la tipografía, en em (tabla hhea), para ubicar textos por su línea base."""
    if ttf not in _METRICAS:
        from fontTools.ttLib import TTFont
        f = TTFont(AQUI / "fuentes" / "estaticas" / ttf)
        _METRICAS[ttf] = (f["hhea"].ascent / f["head"].unitsPerEm, -f["hhea"].descent / f["head"].unitsPerEm)
    return _METRICAS[ttf]


def texto_base(contenido, ttf, familia, pt, base_mm, color, peso=400, estilo="normal", tracking=0.0):
    """Texto centrado cuya línea base cae exactamente en `base_mm` (mm desde arriba del corte)."""
    asc, desc = _metricas(ttf)
    cuerpo = pt * 25.4 / 72
    top = base_mm - cuerpo * (1 + asc - desc) / 2          # con line-height:1 la base queda a (1+asc-desc)/2 del tope
    return (f'<div class="tb" style="top:{top:.3f}mm; font-family:\'{familia}\'; font-weight:{peso}; font-style:{estilo}; '
            f'font-size:{pt}pt; letter-spacing:{tracking}em; color:{color}">{contenido}</div>')


def pagina_portada():
    """La portada de Dani, a todo color, en formato 8,5 × 11". Cambia el título (7 chakras), el
    subtítulo ("Un color a la vez") y suma la línea "Para colorear, reflexionar y disfrutar"."""
    colores = [M.COLORES_FLOR[c]["linea"] for c in ("rojo", "naranja", "amarillo", "verde", "azul", "indigo", "centro")]
    letras, i = "", 0
    for ch in TITULO_LIBRO[1]:
        if ch == " ":
            letras += " "
        elif ch.isdigit():                       # el "7" va en violeta y no corre los colores de las letras
            letras += f'<span style="color:{colores[6]}">{ch}</span>'
        else:
            letras += f'<span style="color:{colores[i % 7]}">{ch}</span>'
            i += 1
    t = M.PORTADA_TEXTOS
    return pagina(f"""
  <div class="arte">{M.portada_arte()}</div>
  {texto_base(esc(TITULO_LIBRO[0]), "Fraunces-Portada.ttf", "FrauncesPortada", 64.9, t["titulo"], COLOR_TITULO, 600)}
  {texto_base(letras, "Manrope-ExtraBold.ttf", "Manrope", 33.7, t["chakras"], COLOR_TITULO, 800, tracking=0.02)}
  {texto_base(esc(SUBTITULO), "Fraunces-Italica.ttf", "FrauncesItalica", 32, t["subtitulo"], COLOR_TEXTO, 400, "italic")}
  {texto_base(esc(TAGLINE), "Manrope-Medium.ttf", "Manrope", 20, t["tagline"], COLOR_TEXTO, 500)}
  {texto_base(esc(CREADO_POR), "Fraunces-Creado.ttf", "FrauncesCreado", 20.0, t["creado"], COLOR_TEXTO, 600)}
  {texto_base(esc(BANDA), "Manrope-ExtraBold.ttf", "Manrope", 26.2, t["banda"], "#fff", 800, tracking=0.03)}
  {texto_base(esc(PARA_MAMA), "Fraunces-Mama.ttf", "FrauncesMama", 21.7, t["mama"], COLOR_MAMA, 500, "italic")}
""")


def _linea_dedic(l):
    return f'<span class="dest">{esc(l[2:])}</span>' if l.startswith("**") else esc(l)


def pagina_dedicatoria(n):
    corazon = M.corazon_linea()
    ancho = 2 * (M.RADIO_CORAZON + 1)
    cuerpo = ""
    for i, lineas in enumerate(DEDIC_ESTROFAS):
        html_l = "<br>".join(_linea_dedic(l) for l in lineas)
        if i == len(DEDIC_ESTROFAS) - 1:
            html_l += f'<br><span class="firma">{esc(DEDIC_FIRMA)}</span>'
        cuerpo += f'<p class="estrofa">{html_l}</p>'
    return pagina(f"""
  <div style="position:absolute; left:{CX - ancho / 2}mm; top:30mm; width:{ancho}mm">{corazon}</div>
  <div class="caja dedic" style="top:112mm"><h2>{esc(DEDIC_TITULO)}</h2>{cuerpo}</div>
""")


def pagina_como_usar(n):
    pasos = "".join(
        f'<div class="paso"><div class="n">{i}</div><div class="t">{"<br>".join(esc(l) for l in t.split(chr(10)))}</div></div>'
        for i, t in enumerate(COMO_USAR_PASOS, 1))
    return pagina(f"""
  <div class="caja" style="top:{MARGEN_SUP + 8}mm">
    <h1 class="titulo-uso" style="margin-bottom:15mm">{esc(COMO_USAR_TITULO)}</h1>
    {pasos}
    <div class="nota-uso" style="margin-top:11mm">{partir(COMO_USAR_NOTA, "cuerpo", 22, ANCHO_UTIL - 2 * 9 - 4)}</div>
  </div>
  {numero(n)}
""")


def paleta_de(clave):
    """Nombres de los colores de la paleta sugerida del chakra (el primero es el protagonista)."""
    return M.PALETAS[clave]


def _cabecera(ch):
    """Nombre del chakra a la izquierda y su color protagonista a la derecha."""
    protagonista = paleta_de(ch["clave"])[0]
    return (f'<div class="cab" style="top:{MARGEN_SUP}mm"><h1 class="titulo-mandala">{esc(ch["nombre"])}</h1>'
            f'<p class="protag">Color protagonista:{_punto(M.PALETA[protagonista], 8)}{M.NOMBRE_COLOR[protagonista]}</p></div>')


def _fila_paleta(clave, top):
    """Los 5 colores de la paleta sugerida, en una fila: punto de color y nombre."""
    items = "".join(f'<div class="sw">{_punto(M.PALETA[c], 8)}{M.NOMBRE_COLOR[c]}</div>' for c in paleta_de(clave))
    return f'<div class="fila-paleta" style="top:{top}mm">{items}</div>'


def pagina_ejemplo(ch, indice, n, ruta_svg):
    """Primera página del capítulo: el mandala pintado ("Así podría quedar"), con su paleta."""
    clave = ch["clave"]
    ancho = 2 * (RADIO + 2)
    top = CENTRO_MANDALA_Y - ancho / 2
    return pagina(f"""
  {pestana(indice, clave)}
  {_cabecera(ch)}
  <p class="sub-ejemplo" style="top:{MARGEN_SUP + 17.3}mm">{esc(TITULO_EJEMPLO)}</p>
  <div style="position:absolute; left:{CX - ancho / 2}mm; top:{top}mm; width:{ancho}mm">{_svg_img(ruta_svg, ancho)}</div>
  {_fila_paleta(clave, CENTRO_MANDALA_Y + ancho / 2 + 2.5)}
  <p class="nota-ejemplo" style="top:{CENTRO_MANDALA_Y + ancho / 2 + 15.5}mm">{partir(NOTA_EJEMPLO, "cuerpo", 18, ANCHO_UTIL * 0.8)}</p>
  {numero(n)}
""")


def pagina_mandala(ch, indice, n, ruta_svg):
    """Segunda página del capítulo: se pinta. Nombre y paleta arriba, mandala en blanco y negro, y abajo la frase."""
    clave = ch["clave"]
    ancho = 2 * (RADIO + 2)
    top = CENTRO_MANDALA_Y - ancho / 2
    afirmacion = "<br>".join(esc(l) for l in ch["afirmacion"])
    return pagina(f"""
  {pestana(indice, clave)}
  {_cabecera(ch)}
  {_fila_paleta(clave, MARGEN_SUP + 18.3)}
  <div style="position:absolute; left:{CX - ancho / 2}mm; top:{top}mm; width:{ancho}mm">{_svg_img(ruta_svg, ancho)}</div>
  <div class="etiqueta-frase" style="top:{CENTRO_MANDALA_Y + ancho / 2 + 3}mm">{esc(LEER_FRASE)}</div>
  <div class="pie-afirmacion" style="top:{CENTRO_MANDALA_Y + ancho / 2 + 12.5}mm">{afirmacion}</div>
  {numero(n)}
""")


def pagina_reflexion(ch, indice, n):
    """Después de leer la frase: la tarea (pregunta de recuerdo). La frase no se repite acá."""
    resp = "<br>".join(esc(l) for l in ch["respiracion"])
    return pagina(f"""
  {pestana(indice, ch["clave"])}
  <div class="caja" style="top:{MARGEN_SUP}mm">
    <h1 class="titulo-cap">{esc(ch["nombre"])}</h1>
    <p class="relacion">{partir(ch["relacion"], "cuerpo", 20, ANCHO_UTIL * 0.9)}</p>
    <h2 class="sub">{esc(TITULO_RESPIRAR)}</h2>
    <p class="respiracion">{resp}</p>
    <h2 class="sub">{esc(TITULO_RECORDAR)}</h2>
    <p class="pregunta">{partir(ch["pregunta"], "negrita", 22, ANCHO_UTIL * 0.92)}</p>
    <p class="nota-escribir">{esc(TEXTO_ESCRIBIR)}</p>
    <div class="renglon"></div><div class="renglon"></div><div class="renglon"></div>
  </div>
  {numero(n)}
""")


def pagina_integracion(n, ruta_svg):
    """Los siete chakras juntos: un mandala para pintar y el texto de la paleta."""
    ancho = 2 * (M.RADIO_INTEGRACION + 2)
    top = CENTRO_INTEGRACION_Y - ancho / 2
    base = CENTRO_INTEGRACION_Y + ancho / 2
    return pagina(f"""
  <div class="caja" style="top:{MARGEN_SUP}mm">
    <h1 class="titulo-mandala">{esc(INTEGRACION_TITULO)}</h1>
    <p class="int-texto" style="margin-top:2.5mm">{esc(INTEGRACION_ARRIBA)}</p>
    <p class="int-colores">{esc(INTEGRACION_COLORES)}</p>
  </div>
  <div style="position:absolute; left:{CX - ancho / 2}mm; top:{top}mm; width:{ancho}mm">{_svg_img(ruta_svg, ancho)}</div>
  <div class="caja" style="top:{base + 3}mm">
    <p class="int-texto centrado">{partir(INTEGRACION_ABAJO, "cuerpo", 18, ANCHO_UTIL * 0.8)}</p>
    <p class="int-frase">{"<br>".join(esc(l) for l in INTEGRACION_FRASE)}</p>
  </div>
  {numero(n)}
""")


def pagina_compartir(n, ruta_svg):
    """Un momento para compartir: invitación a colorear acompañada, con dos flores para pintar de a dos."""
    ancho = 2 * (M.RADIO_PAR + 1)
    parrafos = "".join('<p class="comp-p">' + "<br>".join(partir(l, "cuerpo", 20, ANCHO_UTIL * 0.95) for l in p) + "</p>"
                       for p in COMPARTIR_PARRAFOS)
    return pagina(f"""
  <div class="caja" style="top:{MARGEN_SUP + 4}mm">
    <h1 class="comp-titulo">{esc(COMPARTIR_TITULO)}</h1>
    {parrafos}
    <p class="comp-frase">{partir(COMPARTIR_FRASE, "titulo", 28, ANCHO_UTIL * 0.85)}</p>
  </div>
  <div style="position:absolute; left:{CX - ancho / 2}mm; top:{ALTO - MARGEN_INF - 22 - ancho * M.RAZON_PAR}mm; width:{ancho}mm">{_svg_img(ruta_svg, ancho)}</div>
  {numero(n)}
""")


def pagina_cierre(n):
    """Cierre emocional: un corazón, la frase final y renglones grandes para escribir cómo se sintió."""
    frase = "<br>".join(esc(l) for l in FRASE_FINAL)
    renglones = '<div class="renglon" style="height:21mm"></div>' * 3
    return pagina(f"""
  <div style="position:absolute; left:{CX - 25}mm; top:{MARGEN_SUP + 4}mm; width:50mm">{_svg_img("svg/dedicatoria_corazon.svg", 50)}</div>
  <div class="caja cierre-titulo" style="top:73mm">{esc(CIERRE_TITULO)}</div>
  <div class="caja cierre-frase" style="top:87mm">{frase}</div>
  <div class="caja" style="top:127mm">
    <p class="cierre-senti" style="margin-bottom:2mm">{esc(CIERRE_SENTI)}</p>
    {renglones}
  </div>
  <div class="caja cierre-fecha" style="top:206mm">{esc(CIERRE_FECHA)}<div class="linea"></div></div>
  <div class="caja cierre-nota" style="top:224mm">{partir(CIERRE_NOTA, "negrita", 20, ANCHO_UTIL * 0.9)}</div>
  {numero(n)}
""")


# ===================================================================== ARMADO
def informacion_paginas():
    """Descripción de cada página impresa, para los controles de verificar.py."""
    ancho_c = 2 * (M.RADIO_CORAZON + 1)
    info = [dict(nombre="portada", numero=None),
            dict(nombre="dedicatoria", numero=None, imagenes=[(CX - ancho_c / 2, 30, CX + ancho_c / 2, 30 + ancho_c)]),
            dict(nombre="como_usar", numero=3)]
    n = 4
    for i, ch in enumerate(CHAKRAS):
        paleta = [M.PALETA[c] for c in paleta_de(ch["clave"])]
        comun = dict(clave=ch["clave"], mandala=(CX, CENTRO_MANDALA_Y, RADIO), paleta=paleta, protagonista=paleta[0])
        info.append(dict(nombre=f"{ch['clave']}_ejemplo", numero=n, a_color=True,
                         fila_paleta=CENTRO_MANDALA_Y + RADIO + 4.5, **comun))
        info.append(dict(nombre=f"{ch['clave']}_mandala", numero=n + 1, afirmacion=ch["afirmacion"],
                         fila_paleta=MARGEN_SUP + 18.3, **comun))
        info.append(dict(nombre=f"{ch['clave']}_reflexion", numero=n + 2, clave=ch["clave"],
                         sin_texto=ch["afirmacion"]))      # la frase aparece una sola vez por capítulo
        n += 3
    info.append(dict(nombre="integracion", numero=n, mandala=(CX, CENTRO_INTEGRACION_Y, M.RADIO_INTEGRACION)))
    ancho_par = 2 * (M.RADIO_PAR + 1)
    alto_par = ancho_par * M.RAZON_PAR
    info.append(dict(nombre="compartir", numero=n + 1,
                     imagenes=[(CX - ancho_par / 2, ALTO - MARGEN_INF - 22 - alto_par, CX + ancho_par / 2, ALTO - MARGEN_INF - 22)]))
    info.append(dict(nombre="cierre", numero=n + 2, afirmacion=FRASE_FINAL,
))
    return info


def construir():
    preparar_fuentes()
    (AQUI / "svg").mkdir(exist_ok=True)
    (AQUI / "preview").mkdir(exist_ok=True)

    mandalas_svg = {c["clave"]: M.MANDALAS[c["clave"]]() for c in CHAKRAS}
    mandalas_svg["integracion"] = M.integracion()
    mandalas_svg["par_de_flores"] = M.par_de_flores()
    for clave, svg in mandalas_svg.items():
        (AQUI / "svg" / f"{clave}.svg").write_text(svg, encoding="utf-8")
    # ejemplos pintados ("Así podría quedar"): el mismo dibujo, con los colores de la paleta, en vector
    import ejemplos
    (AQUI / "ejemplos").mkdir(exist_ok=True)
    for viejo in (AQUI / "ejemplos").glob("*"):
        viejo.unlink()
    for c in CHAKRAS:
        (AQUI / "ejemplos" / f"{c['clave']}.svg").write_text(ejemplos.ejemplo(c["clave"]), encoding="utf-8")
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
    for i, ch in enumerate(CHAKRAS):
        paginas.append((f"{ch['clave']}_ejemplo", pagina_ejemplo(ch, i, n, f"ejemplos/{ch['clave']}.svg")))
        n += 1
        paginas.append((f"{ch['clave']}_mandala", pagina_mandala(ch, i, n, f"svg/{ch['clave']}.svg")))
        n += 1
        paginas.append((f"{ch['clave']}_reflexion", pagina_reflexion(ch, i, n)))
        n += 1
    paginas.append(("integracion", pagina_integracion(n, "svg/integracion.svg")))
    n += 1
    paginas.append(("compartir", pagina_compartir(n, "svg/par_de_flores.svg")))
    n += 1
    paginas.append(("cierre", pagina_cierre(n)))

    documento = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Mandalas de los 7 chakras · Un color a la vez</title><style>{css()}</style></head>
<body>{"".join(h for _, h in paginas)}</body></html>"""
    (AQUI / "_tmp").mkdir(exist_ok=True)
    (AQUI / "_tmp" / "libro.html").write_text(documento, encoding="utf-8")

    from weasyprint import HTML
    pdf_paginas = AQUI / "_tmp" / "paginas_impresas.pdf"
    HTML(string=documento, base_url=str(AQUI)).write_pdf(str(pdf_paginas))

    # PDF final: cada página impresa va seguida de su reverso en blanco (el marcador no traspasa).
    # Todas las páginas llevan las cajas de corte y de sangrado, como pide la imprenta.
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject
    pt = 72 / 25.4
    lector = PdfReader(str(pdf_paginas))
    escritor = PdfWriter()
    corte = RectangleObject([0, SANGRE * pt, ANCHO * pt, (PAG_H - SANGRE) * pt])
    sangrado = RectangleObject([0, 0, PAG_W * pt, PAG_H * pt])
    for p in lector.pages:
        for pag in (escritor.add_page(p), escritor.add_blank_page(width=p.mediabox.width, height=p.mediabox.height)):
            pag.trimbox = corte
            pag.bleedbox = sangrado
    escritor.add_metadata({"/Title": "Mandalas de los 7 chakras · Un color a la vez",
                           "/Author": "Dani Navarro (Daniela Navarro · Longevidad Emocional)"})
    salida = AQUI / "libro_mandalas_chakras.pdf"
    with open(salida, "wb") as fh:
        escritor.write(fh)

    # PNG de revisión (solo páginas impresas), recortados al tamaño final
    from PIL import Image
    prev = AQUI / "preview"
    for viejo in prev.glob("*.png"):
        viejo.unlink()
    dpi = 110
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf_paginas), str(prev / "p")], check=True)
    generados = sorted(prev.glob("p-*.png"))      # pdftoppm numera p-1, p-01… según la cantidad
    assert len(generados) == len(paginas), (len(generados), len(paginas))
    px = dpi / 25.4
    for i, (origen, (nombre, _)) in enumerate(zip(generados, paginas), 1):
        Image.open(origen).crop((0, round(SANGRE * px), round(ANCHO * px), round((SANGRE + ALTO) * px))).save(prev / f"{i:02d}_{nombre}.png")
        origen.unlink()
    print(f"PDF: {salida.name} ({len(lector.pages)} páginas impresas, {2 * len(lector.pages)} con reversos)")
    print("PNG:", ", ".join(sorted(p.name for p in prev.glob('*.png'))))
    return mandalas_svg


if __name__ == "__main__":
    construir()
