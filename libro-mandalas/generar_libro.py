#!/usr/bin/env python3
"""MANDALAS DE LOS 7 CHAKRAS · Un color a la vez
Creado por Dani Navarro (Daniela Navarro · Longevidad Emocional).

Genera el libro para colorear (8,5 × 11 pulgadas, vertical, listo para KDP):
  - svg/      cada mandala como SVG vectorial (geometría calculada en mandalas.py)
  - preview/  un PNG por página impresa (recortado al tamaño final)
  - libro-chakras-venta.pdf y libro-chakras-mama.pdf  con sangrado de 0,125" (42 páginas)

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
    ["Pintá despacio, respirá profundo", "y disfrutá cada página."],
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
COLOR_PRINCIPAL = "Color principal:"
ANTES_DE_EMPEZAR = "Antes de empezar, buscá una posición cómoda. Elegí los colores que más te gusten."
LEER_FRASE = "Al terminar, mirá tu mandala y, si lo sentís, decilo en voz alta:"
TITULO_RESPIRAR = "Una respiración para volver a vos"
TITULO_RECORDAR = "Un momento para vos"
NOTA_BLANCA = "Esta hoja queda en blanco a propósito, para que los marcadores no traspasen. Pintá con tranquilidad."

INTEGRACION_TITULO = "Todos juntos"
INTEGRACION_ARRIBA = "Siete flores, una para cada chakra."
INTEGRACION_COLORES = ("rojo", "naranja", "amarillo", "verde", "azul", "indigo", "violeta", "dorado")
INTEGRACION_ABAJO = "Podés usar estos colores o elegir los que vos quieras."
INTEGRACION_FRASE = ["Cada color, una historia.", "Cada página, un momento para vos."]

COMPARTIR_TITULO = "Un momento para compartir"
COMPARTIR_LINEAS = [
    "Este libro también se puede disfrutar en compañía.",
    "Podés colorear con alguien que quieras: tu familia, una amistad o alguien especial.",
    "Elegí una página.",
    "Elegí los colores.",
    "Mientras colorean, dejen que aparezca una historia.",
]
COMPARTIR_FRASE = "A veces, una conversación empieza con un color."
COMPARTIR_NOTA = "Estas dos flores son para colorear de a dos."

CIERRE_TITULO = "Gracias por regalarte este rato."
FRASE_FINAL = ["Un color a la vez,", "un momento a la vez."]
CIERRE_SENTI = "Hoy me sentí…"
CIERRE_AYUDA = "Puede ser una palabra, un color o un dibujo."
CIERRE_FECHA = "Fecha:"
CIERRE_NOTA = "Podés volver a leer esta página cuando quieras recordar cómo te sentiste."

# Página 40 (las dos ediciones): mensaje de la autora y firma, sin la web.
CONTRA_TITULO = "Antes de cerrar este libro…"
CONTRA_LINEAS = [
    "Hola, soy Daniela.",
    "Desde 2012 acompaño a personas a cuidar su bienestar emocional.",
    "Hice este libro para que tengas un momento de calma, un espacio solo tuyo para respirar y tratarte con un poquito más de amor.",
    "No tenés que tener todas las respuestas ni poder con todo. A veces, el primer paso es darte permiso para parar y escucharte.",
    "Vos también merecés el cuidado y el cariño que tantas veces das a los demás.",
    "Si este libro te hizo bien, compartilo con alguien que quieras.",
]
CONTRA_CARINO = "Con cariño,"
CONTRA_NOMBRE = "Daniela Navarro"
CONTRA_MARCA = "Longevidad Emocional"
CONTRA_USUARIO = "@daninavarro.bienestar"
# Página 41 (las dos ediciones): el QR, el isotipo y el usuario van en su propia página porque con la carta no entran
QR_TEXTO = "Si querés seguir cuidando tu mente, escaneá este código con la cámara de tu celular."
QR_URL = "https://menteviva.daninavarro.com.ar"      # va dentro del QR; la dirección no se escribe en el libro
QR_NOMBRE = "MenteViva"
QR_LADO = 28          # mm que miden los módulos del QR (nunca menos de 25)
QR_MARGEN = 4         # mm de blanco alrededor

LEGAL_TITULO = ["MANDALAS DE LOS 7 CHAKRAS", "Un color a la vez"]
LEGAL_AUTORA = ["Creado por Dani Navarro", "Longevidad Emocional"]
LEGAL_DERECHOS = ("© 2026 Dani Navarro. Todos los derechos reservados. "
                  "Prohibida la reproducción total o parcial sin autorización de la autora.")
LEGAL_AVISO = "Este libro propone un momento de calma y disfrute. No reemplaza la consulta con profesionales de la salud."
LEGAL_CONTACTO = "¿Querés contarnos cómo te fue? Escribinos a hola@daninavarro.com.ar"
LEGAL_EDICION = "Primera edición · 2026"

QUE_ES_TITULO = "Siete lugares de tu cuerpo para volver a vos"
QUE_ES_PARRAFOS = [
    "«Chakra» significa «rueda». Desde hace miles de años se habla de siete lugares del cuerpo, cada uno con su color y lo que necesita para estar bien.",
    "Podés sentirlos a tu manera: frená un momento, respirá y preguntate cómo estás ahí.",
]
QUE_ES_CIERRE = "Siete colores, siete momentos para volver a vos."
QUE_ES_TEMAS = {"raiz": "sentirte a salvo", "sacro": "disfrutar", "plexo": "confiar en vos",
                "corazon": "querer y dejarte querer", "garganta": "decir lo que sentís",
                "tercer_ojo": "escuchar tu intuición", "corona": "estar en paz"}

DEDIC_DE = "De:"           # edición para vender: la persona que regala escribe su nombre

# Cada chakra: nombre, párrafo de presentación, respiración, preguntas, texto de ayuda (una idea por línea)
# y la frase que se lee al terminar el mandala. `mama` reemplaza campos en la edición para mamá.
CHAKRAS = [
    dict(clave="raiz", nombre="Raíz",
         parrafo="Raíz es el primer chakra. Está en la base de tu columna, donde tu cuerpo se apoya. Tiene que ver con sentir que estás a salvo, que tenés un lugar y que algo te sostiene.",
         respiracion="Quedate en la posición que te resulte más cómoda. Sentí cómo tu cuerpo se apoya. Tomá aire despacio por la nariz y soltalo despacio por la boca. Repetilo tres veces.",
         preguntas=["¿Qué te hace sentir a salvo?", "¿Quién te hace sentir a salvo?"],
         nota=["Puede ser una persona, un lugar, una mascota o una canción. Si te cuesta escribir, podés contárselo a alguien. Si hoy no aparece nada, también está bien."],
         afirmacion=["Estoy a salvo.", "La vida me sostiene."]),
    dict(clave="sacro", nombre="Sacro",
         parrafo="Sacro es el segundo chakra. Está en el bajo vientre, un poco más abajo del ombligo. Tiene que ver con disfrutar, con crear y con regalarte momentos lindos.",
         respiracion="Quedate en la posición que te resulte más cómoda. Aflojá los hombros y la panza. Tomá aire despacio por la nariz y soltalo despacio por la boca. Repetilo tres veces.",
         preguntas=["¿Qué te encantaba hacer cuando eras joven o en tu infancia?"],
         nota=["Puede ser algo chiquito: jugar, cantar, bailar, dibujar, cocinar. Si te cuesta escribir, podés contárselo a alguien. Si hoy no aparece nada, también está bien."],
         afirmacion=["Me permito disfrutar."]),
    dict(clave="plexo", nombre="Plexo solar",
         parrafo="Plexo solar es el tercer chakra. Está en la boca del estómago, un poco más arriba del ombligo. Tiene que ver con confiar en vos, con tu fuerza interior y con elegir con tranquilidad.",
         respiracion="Quedate en la posición que te resulte más cómoda. Si querés, apoyá una mano en la boca del estómago. Tomá aire despacio por la nariz y soltalo muy despacio por la boca, como si soplaras una vela sin apagarla. Repetilo tres veces.",
         preguntas=["Si mirás tu vida hacia atrás, ¿qué te da orgullo?"],
         nota=["Antes de escribir, poné una mano en el corazón.",
               "Sentí cómo late y dejá que aparezca ese orgullo.",
               "Puede ser algo grande o chiquito: un trabajo, una decisión difícil, haber cuidado a alguien, haber dicho que no.",
               "Si te cuesta escribir, podés contárselo a alguien. Si hoy no aparece nada, también está bien."],
         afirmacion=["Confío en mí", "y en mis decisiones."]),
    dict(clave="corazon", nombre="Corazón",
         parrafo="Corazón es el cuarto chakra. Está en el centro del pecho. Tiene que ver con querer, con agradecer y con dejarte querer.",
         respiracion="Quedate en la posición que te resulte más cómoda. Apoyá las manos abiertas sobre tus piernas, con las palmas hacia arriba, como para recibir. Tomá aire despacio por la nariz y soltalo despacio por la boca. Imaginá que tu pecho se abre un poquito con cada respiración. Repetilo tres veces.",
         preguntas=["¿A quién querés agradecerle hoy?"],
         nota=["Puede ser alguien que está o alguien que ya no está. Una persona, una mascota o la vida misma. Si te cuesta escribir, podés contárselo a alguien. Si hoy no aparece nadie, también está bien."],
         afirmacion=["Puedo dar y recibir amor."]),
    dict(clave="garganta", nombre="Garganta",
         parrafo="Garganta es el quinto chakra. Está en el cuello, donde nace tu voz. Tiene que ver con decir lo que sentís y con que te escuchen.",
         respiracion="Quedate en la posición que te resulte más cómoda. Aflojá el cuello y los hombros. Tomá aire despacio por la nariz y soltalo por la boca con un suspiro suave, como diciendo «ahhh». Repetilo tres veces.",
         preguntas=["¿Qué consejo le darías a alguien que querés mucho?"],
         nota=["Puede ser alguien de tu familia, una amistad o vos cuando eras joven. Escribilo como si se lo dijeras en voz alta. Si te cuesta escribir, podés contárselo a alguien. Si hoy no aparece nada, también está bien."],
         afirmacion=["Mi voz y mis palabras", "importan."],
         mama=dict(preguntas=["¿Qué consejo le darías a tu nieto?"],
                   nota=["Escribilo como si se lo dijeras en voz alta. Si te cuesta escribir, podés contárselo a alguien. Si hoy no aparece nada, también está bien."])),
    dict(clave="tercer_ojo", nombre="Tercer ojo",
         parrafo="Tercer ojo es el sexto chakra. Está en el centro de la frente, entre las cejas. Tiene que ver con tu intuición, esa voz interior que a veces te avisa algo.",
         respiracion="Quedate en la posición que te resulte más cómoda. Cerrá los ojos si te resulta cómodo, o dejá la mirada suave en un punto. Tomá aire despacio por la nariz y soltalo despacio por la boca. Con cada respiración, llevá tu atención al centro de la frente, entre las cejas. Repetilo tres veces.",
         preguntas=["¿Tuviste alguna vez una corazonada que se cumplió?", "¿Cuándo te dejaste guiar por tu intuición?"],
         nota=["Una corazonada es eso que sentís por dentro antes de que algo pase. Puede ser algo chiquito. Si te cuesta escribir, podés contárselo a alguien. Si hoy no aparece nada, también está bien."],
         afirmacion=["Escucho lo que siento", "por dentro."]),
    dict(clave="corona", nombre="Corona",
         parrafo="Corona es el séptimo chakra. Está en lo alto de tu cabeza, como una corona. Tiene que ver con la paz y con sentirte en calma.",
         respiracion="Quedate en la posición que te resulte más cómoda. Tomá aire despacio por la nariz. Al soltarlo por la boca, imaginá una luz suave sobre tu cabeza. Repetilo tres veces.",
         preguntas=["¿Qué te da paz hoy?"],
         nota=["Puede ser un lugar, una persona, una música o un silencio. Si te cuesta escribir, podés contárselo a alguien. Si hoy no aparece nada, también está bien."],
         afirmacion=["Estoy en paz", "en este momento."]),
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
DESPLAZ_I = MARGEN_INT - MARGEN_EXT   # en las páginas izquierdas el margen ancho (lomo) queda a la derecha: todo se corre esto a la izquierda
CX_I = CX - DESPLAZ_I
PESTANA_ANCHO = 8
PESTANA_ALTO = 32
PESTANA_PASO = 35         # cada capítulo baja un escalón, para encontrarlo al hojear
RADIO = M.RADIO_MANDALA
# Encabezado de las páginas de mandala (mm desde arriba del corte): título, "Color principal", leyenda de colores y,
# en la página para pintar, el texto "Antes de empezar". El mandala ocupa el resto, y debajo va la frase.
Y_PRINCIPAL = MARGEN_SUP + 15.3
Y_LEYENDA = MARGEN_SUP + 28.3
Y_ANTES = Y_LEYENDA + 12.5
Y_LEYENDA_INT = MARGEN_SUP + 26.5     # leyenda de 8 colores (dos filas) de Todos juntos
CENTRO_MANDALA_Y = 139.5  # centro del mandala, desde arriba del corte
CENTRO_INTEGRACION_Y = 152.0
FONDO = "#FFFBF5"         # fondo de todas las páginas
TINTA = "#222222"         # texto de cuerpo
TINTA_CHICA = "#333333"   # textos chicos
COLOR_RENGLON = "#8A8178"  # líneas para escribir

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
        (fri, "Fraunces-ItalicaTexto.ttf", {"wght": 500, "opsz": 14, "SOFT": 0, "WONK": 0}),   # cursiva de texto (18 pt)
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
_FAMILIAS = {"cuerpo": "Manrope-Medium.ttf", "negrita": "Manrope-Bold.ttf", "titulo": "Fraunces-Titulo.ttf",
             "cursiva": "Fraunces-ItalicaTexto.ttf"}


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
@font-face {{ font-family: 'FrauncesTexto'; font-weight: 500; font-style: italic; src: url('{f}/Fraunces-ItalicaTexto.ttf'); }}
@font-face {{ font-family: 'FrauncesCreado'; font-weight: 600; font-style: normal; src: url('{f}/Fraunces-Creado.ttf'); }}
@font-face {{ font-family: 'FrauncesMama'; font-weight: 500; font-style: italic; src: url('{f}/Fraunces-Mama.ttf'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 500; src: url('{f}/Manrope-Medium.ttf'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 700; src: url('{f}/Manrope-Bold.ttf'); }}
@font-face {{ font-family: 'Manrope'; font-weight: 800; src: url('{f}/Manrope-ExtraBold.ttf'); }}
@page {{ size: {PAG_W}mm {PAG_H}mm; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: {FONDO}; }}
body {{ font-family: 'Manrope', sans-serif; font-weight: 500; font-size: 18pt; line-height: 1.5; color: {TINTA}; }}
/* la página lleva sangrado; todo se ubica dentro de .recorte, que es el tamaño final (desde el corte) */
.pagina {{ position: relative; width: {PAG_W}mm; height: {PAG_H}mm; overflow: hidden;
          page-break-after: always; background: {FONDO}; }}
.pagina:last-child {{ page-break-after: auto; }}
.recorte {{ position: absolute; left: 0; top: {SANGRE}mm; width: {ANCHO}mm; height: {ALTO}mm; }}
.contenido {{ position: absolute; top: 0; width: {ANCHO}mm; height: {ALTO}mm; }}
.caja {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; }}
.num {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; bottom: {MARGEN_INF}mm; text-align: center;
        font-weight: 700; font-size: 18pt; line-height: 1.2; }}
.pestana {{ position: absolute; right: -{SANGRE}mm; width: {PESTANA_ANCHO + SANGRE}mm; height: {PESTANA_ALTO}mm;
            border-radius: 3mm 0 0 3mm; }}
.pestana.izq {{ right: auto; left: -{SANGRE}mm; border-radius: 0 3mm 3mm 0; }}
h1, h2, .serif {{ font-family: 'Fraunces', serif; font-weight: 700; margin: 0; }}
p {{ margin: 0; }}
b {{ font-weight: 800; }}
img {{ display: block; }}
.centrado {{ text-align: center; }}
.chica {{ color: {TINTA_CHICA}; }}
.cursiva {{ font-family: 'FrauncesTexto', serif; font-style: italic; font-weight: 500; color: {TINTA_CHICA}; }}

/* portada: el diseño de Dani. El arte (tarjeta, banda, flores) es un SVG; los textos se ubican por línea base */
.arte {{ position: absolute; left: 0; top: 0; width: {ANCHO}mm; height: {ALTO}mm; }}
.tb {{ position: absolute; left: 0; width: {ANCHO}mm; text-align: center; line-height: 1; white-space: nowrap; }}

/* dedicatoria */
.dedic {{ text-align: center; font-size: 20pt; line-height: 1.5; }}
.dedic h2 {{ font-size: 32pt; line-height: 1.2; margin-bottom: 8mm; }}
.dedic .estrofa {{ margin-bottom: 6mm; }}
.dedic .dest {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 22pt; }}
.dedic .firma {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 28pt; line-height: 1.4; }}
.dedic .de {{ display: flex; align-items: flex-end; justify-content: center; margin-top: 3mm; font-family: 'Fraunces', serif; font-weight: 700; font-size: 26pt; line-height: 1.2; }}
.dedic .de .linea {{ width: 95mm; height: 10mm; margin-left: 5mm; border-bottom: 1.5px solid {COLOR_RENGLON}; }}

/* legal y autora */
.legal {{ text-align: center; }}
.legal .t1 {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 26pt; line-height: 1.2; }}
.legal .t2 {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 22pt; line-height: 1.3; margin-top: 2mm; }}
.legal p {{ font-size: 18pt; line-height: 1.5; margin-top: 7mm; color: {TINTA_CHICA}; }}
.legal .autora {{ font-weight: 700; margin-top: 11mm; color: {TINTA}; }}

/* qué es un chakra */
.que-es-t {{ font-size: 36pt; line-height: 1.15; margin-bottom: 8mm; }}
.que-es-p {{ font-size: 20pt; line-height: 1.5; margin-bottom: 5mm; }}
.que-es-lista {{ margin: 6mm 0 6mm 0; }}
.que-es-lista .f {{ display: flex; align-items: center; height: 12.5mm; font-size: 20pt; line-height: 1; white-space: nowrap; }}
.que-es-lista .f svg {{ flex: 0 0 10mm; margin-right: 4mm; }}
.que-es-lista b {{ font-weight: 800; }}
.que-es-cierre {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 24pt; line-height: 1.3; margin-top: 4mm; }}

/* cómo usar */
.titulo-uso {{ font-size: 44pt; line-height: 1.1; }}
.paso {{ display: flex; align-items: center; margin-bottom: 7mm; }}
.paso .n {{ flex: 0 0 15mm; width: 15mm; height: 15mm; border: 0.75mm solid {TINTA}; border-radius: 50%;
           text-align: center; font-family: 'Fraunces', serif; font-weight: 700; font-size: 24pt; line-height: 13.5mm; }}
.paso .t {{ margin-left: 8mm; font-size: 24pt; line-height: 1.5; }}
.nota-uso {{ border: 0.75mm solid {TINTA}; border-radius: 6mm; padding: 7mm 9mm; font-size: 22pt; line-height: 1.5; }}

/* página del mandala: nombre, color principal y leyenda arriba; frase abajo */
.cab {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; }}
.titulo-mandala {{ font-size: 40pt; line-height: 1.05; }}
.principal {{ display: flex; align-items: center; margin: 0.5mm 0 0 0; font-weight: 700; font-size: 18pt; line-height: 1; height: 10.5mm; white-space: nowrap; }}
.principal svg {{ flex: 0 0 10mm; margin: 0 2.5mm 0 3mm; }}
.fila-paleta {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; height: 10.5mm; display: flex; justify-content: space-between; align-items: center; }}
.fila-paleta.dos {{ justify-content: center; gap: 9mm; }}
.fila-paleta .sw {{ display: flex; align-items: center; font-size: 18pt; line-height: 1; white-space: nowrap; }}
.fila-paleta .sw svg {{ flex: 0 0 10mm; margin-right: 2.5mm; }}
.sub-ejemplo {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; font-family: 'Fraunces', serif; font-weight: 700; font-size: 26pt; line-height: 1.2; }}
.nota-ejemplo {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; text-align: center; font-size: 18pt; line-height: 1.5; color: {TINTA_CHICA}; }}
.antes {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; font-size: 18pt; line-height: 1.5; }}
.etiqueta-frase {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; text-align: center; font-weight: 700; font-size: 18pt; line-height: 1.5; }}
.pie-afirmacion {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; text-align: center;
                   font-family: 'Fraunces', serif; font-weight: 700; font-size: 32pt; line-height: 1.22; }}

/* página de texto: la tarea, después de decir la frase */
.titulo-cap {{ line-height: 1.1; margin-bottom: 4mm; }}
.parrafo {{ line-height: 1.5; margin-bottom: 5mm; }}
.sub {{ font-size: 22pt; line-height: 1.2; margin-bottom: 2mm; }}
.respiracion {{ line-height: 1.5; margin-bottom: 5mm; }}
.pregunta {{ font-weight: 700; font-size: 22pt; line-height: 1.5; margin-bottom: 1mm; }}
.nota-escribir {{ font-size: 18pt; line-height: 1.5; color: {TINTA_CHICA}; }}
.nota-escribir + .nota-escribir {{ margin-top: 0; }}
.renglon {{ height: 14mm; border-bottom: 1.5px solid {COLOR_RENGLON}; }}
.renglones {{ margin-top: 1mm; }}

/* hojas en blanco: solo una nota y el número */
.nota-blanca {{ position: absolute; left: {X0}mm; width: {ANCHO_UTIL}mm; bottom: {MARGEN_INF + 10}mm; text-align: center;
                font-size: 18pt; line-height: 1.5; color: {TINTA_CHICA}; }}

/* todos juntos */
.int-texto {{ font-size: 18pt; line-height: 1.5; }}
.int-frase {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 24pt; line-height: 1.2; text-align: center; margin-top: 2mm; }}

/* un momento para compartir */
.comp-titulo {{ font-size: 34pt; line-height: 1.1; margin-bottom: 5mm; }}
.comp-p {{ font-size: 18pt; line-height: 1.5; margin-bottom: 2mm; }}
.comp-frase {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 24pt; line-height: 1.25; margin-top: 4mm; }}
.comp-nota {{ font-size: 18pt; line-height: 1.5; color: {TINTA_CHICA}; text-align: center; }}

/* cierre */
.cierre-titulo {{ text-align: center; font-size: 28pt; line-height: 1.2; }}
.cierre-frase {{ text-align: center; font-family: 'Fraunces', serif; font-weight: 700; font-size: 32pt; line-height: 1.2; margin-top: 3mm; }}
.cierre-senti {{ font-weight: 700; font-size: 24pt; line-height: 1.2; }}
.cierre-ayuda {{ font-size: 18pt; line-height: 1.5; color: {TINTA_CHICA}; }}
.cierre-fecha {{ display: flex; align-items: flex-end; font-weight: 700; font-size: 22pt; line-height: 1.2; }}
.cierre-fecha .linea {{ flex: 1; height: 11mm; margin-left: 5mm; border-bottom: 1.5px solid {COLOR_RENGLON}; }}
.cierre-nota {{ text-align: center; font-weight: 700; font-size: 18pt; line-height: 1.5; }}

/* página 40 */
.contra {{ text-align: center; }}
.contra h1 {{ line-height: 1.15; }}
.contra p {{ font-size: 20pt; line-height: 1.5; color: {TINTA}; }}
.contra .nombre {{ font-family: 'Fraunces', serif; font-weight: 700; font-size: 26pt; line-height: 1.25; }}
.contra .marca {{ font-size: 18pt; color: {TINTA_CHICA}; }}
.contra .usuario {{ font-size: 18pt; color: {TINTA_CHICA}; }}
"""


# ================================================================= PÁGINAS (HTML)
def esc(t):
    return html.escape(t, quote=False)


def pagina(contenido, lado="D", tab=""):
    """lado D = página derecha (recto: sangrado a la derecha), I = izquierda (reverso: sangrado a la izquierda).
    En las izquierdas el margen ancho del lomo queda a la derecha, así que el contenido se corre a la izquierda."""
    izq = SANGRE if lado == "I" else 0
    desp = -DESPLAZ_I if lado == "I" else 0
    return (f'<section class="pagina"><div class="recorte" style="left:{izq}mm">{tab}'
            f'<div class="contenido" style="left:{desp}mm">{contenido}</div></div></section>')


def pagina_blanca(n):
    """Reverso en blanco de una página que se pinta con marcador: solo una nota y el número de página."""
    return pagina(f'<p class="nota-blanca">{partir(NOTA_BLANCA, "cuerpo", 18, ANCHO_UTIL * 0.9)}</p>{numero(n)}', "I")


def pestana(indice, clave, lado="D"):
    top = MARGEN_SUP + indice * PESTANA_PASO
    clase = "pestana izq" if lado == "I" else "pestana"
    return f'<div class="{clase}" style="top:{top}mm; background:{M.COLORES[clave]}"></div>'


def numero(n):
    return f'<div class="num">{n}</div>'


def _svg_img(ruta_svg, ancho_mm):
    return f'<img src="{(AQUI / ruta_svg).as_uri()}" style="width:{ancho_mm}mm">'


_HEX_A_NOMBRE = {v.upper(): k for k, v in M.PALETA.items()}


def _punto(color, mm=10):
    """Círculo de color de las leyendas: relleno sólido y borde fino (2 px) de un tono más oscuro del mismo color."""
    borde = M.BORDE_COLOR.get(_HEX_A_NOMBRE.get(color.upper()), M.NEGRO)
    g = 2 * 25.4 / 96                                     # 2 px
    r = mm / 2
    return (f'<svg width="{mm}mm" height="{mm}mm" viewBox="0 0 {mm} {mm}" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="{r}" cy="{r}" r="{r - g / 2:.3f}" fill="{color}" stroke="{borde}" stroke-width="{g:.3f}"/></svg>')


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


def pagina_dedicatoria(edicion="venta"):
    """Edición "mama": firmada por Dani. Edición "venta": una línea para que escriba su nombre quien regala."""
    corazon = M.corazon_linea()
    ancho = 2 * (M.RADIO_CORAZON + 1)
    cuerpo = ""
    for i, lineas in enumerate(DEDIC_ESTROFAS):
        html_l = "<br>".join(_linea_dedic(l) for l in lineas)
        if i == len(DEDIC_ESTROFAS) - 1 and edicion == "mama":
            html_l += f'<br><span class="firma">{esc(DEDIC_FIRMA)}</span>'
        cuerpo += f'<p class="estrofa">{html_l}</p>'
    if edicion != "mama":
        cuerpo += f'<div class="de">{esc(DEDIC_DE)}<div class="linea"></div></div>'
    return pagina(f"""
  <div style="position:absolute; left:{CX - ancho / 2}mm; top:24mm; width:{ancho}mm">{corazon}</div>
  <div class="caja dedic" style="top:104mm"><h2>{esc(DEDIC_TITULO)}</h2>{cuerpo}</div>
""", "D")


def pagina_legal():
    """Página 2 (reverso de la portada): autora, derechos y aviso de bienestar."""
    ancho = 36
    return pagina(f"""
  <div style="position:absolute; left:{CX - ancho / 2}mm; top:38mm; width:{ancho}mm">{_svg_img("svg/dedicatoria_corazon.svg", ancho)}</div>
  <div class="caja legal" style="top:84mm">
    <div class="t1">{esc(LEGAL_TITULO[0])}</div>
    <div class="t2">{esc(LEGAL_TITULO[1])}</div>
    <p class="autora">{"<br>".join(esc(l) for l in LEGAL_AUTORA)}</p>
    <p>{partir(LEGAL_DERECHOS, "cuerpo", 18, ANCHO_UTIL * 0.95)}</p>
    <p>{partir(LEGAL_AVISO, "cuerpo", 18, ANCHO_UTIL * 0.95)}</p>
    <p>{partir(LEGAL_CONTACTO, "cuerpo", 18, ANCHO_UTIL * 0.95)}</p>
    <p>{esc(LEGAL_EDICION)}</p>
  </div>
""", "I")


def pagina_que_es(n):
    """Siete lugares de tu cuerpo para volver a vos: dos párrafos y los siete chakras con su color y lo que necesitan."""
    parrafos = "".join(f'<p class="que-es-p">{partir(t, "cuerpo", 20, ANCHO_UTIL)}</p>' for t in QUE_ES_PARRAFOS)
    filas = "".join(f'<div class="f">{_punto(M.COLORES[c["clave"]])}<b>{esc(c["nombre"])}</b>&nbsp;·&nbsp;{esc(QUE_ES_TEMAS[c["clave"]])}</div>'
                    for c in CHAKRAS)
    return pagina(f"""
  <div class="caja" style="top:{MARGEN_SUP + 2}mm">
    <h1 class="que-es-t">{partir(QUE_ES_TITULO, "titulo", 36, ANCHO_UTIL)}</h1>
    {parrafos}
    <div class="que-es-lista">{filas}</div>
    <p class="que-es-cierre">{partir(QUE_ES_CIERRE, "titulo", 24, ANCHO_UTIL)}</p>
  </div>
  {numero(n)}
""", "I")


def pagina_como_usar(n):
    pasos = "".join(
        f'<div class="paso"><div class="n">{i}</div><div class="t">{"<br>".join(esc(l) for l in t.split(chr(10)))}</div></div>'
        for i, t in enumerate(COMO_USAR_PASOS, 1))
    return pagina(f"""
  <div class="caja" style="top:{MARGEN_SUP + 4}mm">
    <h1 class="titulo-uso" style="margin-bottom:11mm">{esc(COMO_USAR_TITULO)}</h1>
    {pasos}
    <div class="nota-uso" style="margin-top:9mm">{partir(COMO_USAR_NOTA, "cuerpo", 22, ANCHO_UTIL - 2 * 9 - 4)}</div>
  </div>
  {numero(n)}
""", "D")


def paleta_de(clave):
    """Nombres de los colores de la paleta sugerida del chakra (el primero es el principal)."""
    return M.PALETAS[clave]


def _cabecera(titulo, color_principal=None):
    """Título y, si hay, "Color principal" en una línea propia debajo."""
    linea = ""
    if color_principal:
        linea = (f'<p class="principal">{esc(COLOR_PRINCIPAL)}{_punto(M.PALETA[color_principal])}'
                 f'{M.NOMBRE_COLOR[color_principal]}</p>')
    return f'<div class="cab" style="top:{MARGEN_SUP}mm"><h1 class="titulo-mandala">{esc(titulo)}</h1>{linea}</div>'


def _fila_paleta(nombres, top, dos=False):
    """Colores de la leyenda, en una fila: círculo de color y nombre."""
    items = "".join(f'<div class="sw">{_punto(M.PALETA[c])}{M.NOMBRE_COLOR[c]}</div>' for c in nombres)
    return f'<div class="fila-paleta{" dos" if dos else ""}" style="top:{top}mm">{items}</div>'


def _filas_leyenda(nombres, top):
    """Leyenda de 8 colores en dos filas de 4."""
    mitad = (len(nombres) + 1) // 2
    return _fila_paleta(nombres[:mitad], top, True) + _fila_paleta(nombres[mitad:], top + 10.5, True)


def _mandala_img(ruta_svg, centro_y, radio):
    ancho = 2 * (radio + 2)
    return (f'<div style="position:absolute; left:{CX - ancho / 2}mm; top:{centro_y - ancho / 2}mm; width:{ancho}mm">'
            f'{_svg_img(ruta_svg, ancho)}</div>')


def pagina_ejemplo(ch, indice, n, ruta_svg):
    """Página izquierda del capítulo: el mandala pintado ("Así podría quedar"), con su paleta."""
    clave = ch["clave"]
    base = CENTRO_MANDALA_Y + RADIO + 2
    return pagina(f"""
  {_cabecera(ch["nombre"], paleta_de(clave)[0])}
  <p class="sub-ejemplo" style="top:{MARGEN_SUP + 27.5}mm">{esc(TITULO_EJEMPLO)}</p>
  {_mandala_img(ruta_svg, CENTRO_MANDALA_Y, RADIO)}
  {_fila_paleta(paleta_de(clave), base + 2.5)}
  <p class="nota-ejemplo" style="top:{base + 15}mm">{partir(NOTA_EJEMPLO, "cuerpo", 18, ANCHO_UTIL * 0.8)}</p>
  {numero(n)}
""", "I", pestana(indice, clave, "I"))


def pagina_mandala(ch, indice, n, ruta_svg):
    """Página derecha del capítulo: se pinta. Nombre, color principal y leyenda arriba, y abajo la frase."""
    clave = ch["clave"]
    base = CENTRO_MANDALA_Y + RADIO + 2
    afirmacion = "<br>".join(esc(l) for l in ch["afirmacion"])
    return pagina(f"""
  {_cabecera(ch["nombre"], paleta_de(clave)[0])}
  {_fila_paleta(paleta_de(clave), Y_LEYENDA)}
  <p class="antes cursiva" style="top:{Y_ANTES}mm">{partir(ANTES_DE_EMPEZAR, "cursiva", 18, ANCHO_UTIL)}</p>
  {_mandala_img(ruta_svg, CENTRO_MANDALA_Y, RADIO)}
  <div class="etiqueta-frase" style="top:{base}mm">{partir(LEER_FRASE, "negrita", 18, ANCHO_UTIL * 0.97)}</div>
  <div class="pie-afirmacion" style="top:{base + 21}mm">{afirmacion}</div>
  {numero(n)}
""", "D", pestana(indice, clave))


# Página de texto de cada chakra: el cuerpo nunca baja de 18 pt; si no entra, se achica el título y luego el cuerpo
# (hasta 18 pt) y, si aun así no entra, queda marcado en verificar.py.
LIMITE_Y_TEXTO = 257.0
OPCIONES_TEXTO = [(48, 20, 22), (44, 20, 22), (44, 19, 22), (40, 19, 22), (40, 18, 22), (40, 18, 20), (40, 18, 18),
                  (36, 18, 18), (32, 18, 18)]
_MM = 25.4 / 72


def _n_lineas(texto, familia, pt, ancho=None):
    ancho = (ancho or ANCHO_UTIL) * 0.97          # margen: la letra real se corta un poco antes que la medida
    n, actual = 1, ""
    for palabra in texto.split():
        prueba = (actual + " " + palabra).strip()
        if ancho_mm(prueba, familia, pt) <= ancho:
            actual = prueba
        else:
            n, actual = n + 1, palabra
    return n


def _datos_reflexion(ch, edicion):
    d = dict(ch)
    if edicion == "mama" and "mama" in ch:
        d.update(ch["mama"])
    return d


def _alto_reflexion(d, pt_t, pt_c, pt_q=22):
    """Alto aproximado (mm) de la página de texto, con los mismos márgenes que el CSS."""
    h = pt_t * _MM * 1.1 + 4
    h += _n_lineas(d["parrafo"], "cuerpo", pt_c) * pt_c * _MM * 1.5 + 5
    h += pt_q * _MM * 1.2 + 2
    h += _n_lineas(d["respiracion"], "cuerpo", pt_c) * pt_c * _MM * 1.5 + 5
    h += pt_q * _MM * 1.2 + 2
    for q in d["preguntas"]:
        h += _n_lineas(q, "negrita", pt_q) * pt_q * _MM * 1.5 + 1
    for linea in d["nota"]:
        h += _n_lineas(linea, "cuerpo", 18) * 18 * _MM * 1.5
    return h + 1 + 14 * 2 * len(d["preguntas"])


def _tamanos_propios(ch, edicion):
    d = _datos_reflexion(ch, edicion)
    for pt_t, pt_c, pt_q in OPCIONES_TEXTO:
        if MARGEN_SUP + _alto_reflexion(d, pt_t, pt_c, pt_q) <= LIMITE_Y_TEXTO:
            return pt_t, pt_c, pt_q
    return OPCIONES_TEXTO[-1]


def tamanos_texto(ch, edicion="venta"):
    """(título, cuerpo, preguntas) en pt. El cuerpo y las preguntas son los más grandes con los que entra la página;
    el título es el mismo en los siete chakras (el menor de los que entran), para que el libro sea parejo."""
    pt_t = min(_tamanos_propios(c, e)[0] for c in CHAKRAS for e in EDICIONES)
    _, pt_c, pt_q = _tamanos_propios(ch, edicion)
    return pt_t, pt_c, pt_q


def pagina_reflexion(ch, indice, n, edicion="venta"):
    """Después de leer la frase: respirar y la pregunta (o las preguntas), con dos renglones por pregunta."""
    d = _datos_reflexion(ch, edicion)
    pt_t, pt_c, pt_q = tamanos_texto(ch, edicion)
    preguntas = "".join(f'<p class="pregunta" style="font-size:{pt_q}pt">{esc(q)}</p>' for q in d["preguntas"])
    nota = "".join(f'<p class="nota-escribir">{esc(t)}</p>' for t in d["nota"])
    renglones = '<div class="renglon"></div>' * (2 * len(d["preguntas"]))
    return pagina(f"""
  <div class="caja" style="top:{MARGEN_SUP}mm">
    <h1 class="titulo-cap" style="font-size:{pt_t}pt">{esc(d["nombre"])}</h1>
    <p class="parrafo" style="font-size:{pt_c}pt">{esc(d["parrafo"])}</p>
    <h2 class="sub" style="font-size:{pt_q}pt">{esc(TITULO_RESPIRAR)}</h2>
    <p class="respiracion" style="font-size:{pt_c}pt">{esc(d["respiracion"])}</p>
    <h2 class="sub" style="font-size:{pt_q}pt">{esc(TITULO_RECORDAR)}</h2>
    {preguntas}
    {nota}
    <div class="renglones">{renglones}</div>
  </div>
  {numero(n)}
""", "D", pestana(indice, ch["clave"]))


def pagina_ejemplo_integracion(n, ruta_svg):
    """Todos juntos, pintado: cada flor con el color de su chakra; leyenda de 8 colores en dos filas."""
    return pagina(f"""
  {_cabecera(INTEGRACION_TITULO)}
  <p class="sub-ejemplo" style="top:{MARGEN_SUP + 15.5}mm">{esc(TITULO_EJEMPLO)}</p>
  {_filas_leyenda(INTEGRACION_COLORES, Y_LEYENDA_INT)}
  {_mandala_img(ruta_svg, CENTRO_INTEGRACION_Y, M.RADIO_INTEGRACION)}
  <p class="nota-ejemplo" style="top:{CENTRO_INTEGRACION_Y + M.RADIO_INTEGRACION + 4}mm">{partir(NOTA_EJEMPLO, "cuerpo", 18, ANCHO_UTIL * 0.8)}</p>
  {numero(n)}
""", "I")


def pagina_integracion(n, ruta_svg):
    """Los siete chakras juntos: un mandala para pintar, con la leyenda de colores arriba."""
    base = CENTRO_INTEGRACION_Y + M.RADIO_INTEGRACION + 2
    return pagina(f"""
  {_cabecera(INTEGRACION_TITULO)}
  <p class="int-texto" style="position:absolute; left:{X0}mm; top:{MARGEN_SUP + 15.5}mm; width:{ANCHO_UTIL}mm">{esc(INTEGRACION_ARRIBA)}</p>
  {_filas_leyenda(INTEGRACION_COLORES, Y_LEYENDA_INT)}
  <p class="antes cursiva" style="top:{Y_LEYENDA_INT + 22}mm">{partir(ANTES_DE_EMPEZAR, "cursiva", 18, ANCHO_UTIL)}</p>
  {_mandala_img(ruta_svg, CENTRO_INTEGRACION_Y, M.RADIO_INTEGRACION)}
  <div class="caja" style="top:{base}mm">
    <p class="int-texto centrado">{partir(INTEGRACION_ABAJO, "cuerpo", 18, ANCHO_UTIL)}</p>
    <p class="int-frase">{"<br>".join(esc(l) for l in INTEGRACION_FRASE)}</p>
  </div>
  {numero(n)}
""", "D")


def pagina_compartir(n, ruta_svg):
    """Un momento para compartir: invitación a colorear acompañado, con dos flores grandes para pintar de a dos."""
    ancho = 2 * (M.RADIO_PAR + 1)
    lineas = "".join(f'<p class="comp-p" style="font-size:20pt">{partir(t, "cuerpo", 20, ANCHO_UTIL)}</p>' for t in COMPARTIR_LINEAS)
    return pagina(f"""
  <div class="caja" style="top:{MARGEN_SUP + 2}mm">
    <h1 class="comp-titulo">{partir(COMPARTIR_TITULO, "titulo", 34, ANCHO_UTIL)}</h1>
    {lineas}
    <p class="comp-frase">{partir(COMPARTIR_FRASE, "titulo", 24, ANCHO_UTIL * 0.9)}</p>
    <p class="comp-nota" style="margin-top:8mm">{esc(COMPARTIR_NOTA)}</p>
    <div style="margin-top:6mm">{_svg_img(ruta_svg, ancho).replace('style="', 'style="margin:0 auto; ')}</div>
  </div>
  {numero(n)}
""", "D")


def pagina_cierre(n):
    """Cierre emocional: un corazón, la frase final y renglones para escribir cómo se sintió."""
    frase = "<br>".join(esc(l) for l in FRASE_FINAL)
    renglones = '<div class="renglon"></div>' * 3
    return pagina(f"""
  <div class="caja" style="top:{MARGEN_SUP + 2}mm">
    <div style="width:46mm; margin:0 auto 5mm auto">{_svg_img("svg/dedicatoria_corazon.svg", 46)}</div>
    <div class="cierre-titulo">{esc(CIERRE_TITULO)}</div>
    <div class="cierre-frase">{frase}</div>
    <p class="cierre-senti" style="margin-top:9mm">{esc(CIERRE_SENTI)}</p>
    <p class="cierre-ayuda">{esc(CIERRE_AYUDA)}</p>
    <div class="renglones">{renglones}</div>
    <div class="cierre-fecha" style="margin-top:2mm">{esc(CIERRE_FECHA)}<div class="linea"></div></div>
    <p class="cierre-nota" style="margin-top:8mm">{partir(CIERRE_NOTA, "negrita", 18, ANCHO_UTIL * 0.9)}</p>
  </div>
  {numero(n)}
""", "D")


def ruta_logo():
    """El isotipo de la autora (corazón de manos con brote), si está en libro-mandalas/assets/ (isotipo.svg, .png...)."""
    carpeta = AQUI / "assets"
    return next(iter(sorted(carpeta.glob("isotipo.*"))), None) if carpeta.exists() else None


LOGO_ANCHO = 25                  # ancho del isotipo (mm); va sin fondo ni recuadro y con sus colores originales
LOGO_PROPORCION = 717 / 731      # alto / ancho del isotipo (assets/isotipo.svg)
LOGO_AIRE = 8                    # mm de aire arriba y abajo del isotipo
# (tamaño del título en pt, espacio entre párrafos en mm): de lo más cómodo a lo más ajustado. El texto nunca baja de 20 pt.
OPCIONES_CONTRA = [(36, 6), (36, 5), (36, 4), (36, 3.5), (34, 3)]


def _alto_contra(pt_t, gap):
    """Alto aproximado (mm) de la carta de la página 40 (título, párrafos y firma), con los tamaños del CSS."""
    h = pt_t * _MM * 1.15 + 6
    h += sum(_n_lineas(t, "cuerpo", 20) * 20 * _MM * 1.5 for t in CONTRA_LINEAS) + gap * (len(CONTRA_LINEAS) - 1)
    h += gap + 2 + 20 * _MM * 1.5 + 26 * _MM * 1.25 + 18 * _MM * 1.5          # firma
    return h - 2.4                                                            # medido en el PDF: el estimador sobrestima unos 2,4 mm


def distribucion_contra():
    """Elige la primera opción que entra en la página: devuelve (pt del título, espacio entre párrafos, top)."""
    libre = ALTO - MARGEN_INF - MARGEN_SUP
    for pt_t, gap in OPCIONES_CONTRA:
        h = _alto_contra(pt_t, gap)
        if h <= libre - 1.5:                                                    # 1,5 mm de aire contra el margen de abajo
            return pt_t, gap, MARGEN_SUP + min((libre - h) / 2, 10)
    pt_t, gap = OPCIONES_CONTRA[-1]
    return pt_t, gap, MARGEN_SUP


def pagina_contratapa():
    """Página 40 (las dos ediciones): "Antes de cerrar este libro…", la carta de Daniela y su firma."""
    pt_t, gap, top = distribucion_contra()
    parrafos = "".join(f'<p style="margin-bottom:{gap}mm">{partir(t, "cuerpo", 20, ANCHO_UTIL)}</p>' for t in CONTRA_LINEAS)
    return pagina(f"""
  <div class="caja contra" style="top:{top}mm">
    <h1 style="font-size:{pt_t}pt; margin-bottom:6mm">{esc(CONTRA_TITULO)}</h1>
    {parrafos}
    <p style="margin-top:2mm">{esc(CONTRA_CARINO)}</p>
    <p class="nombre">{esc(CONTRA_NOMBRE)}</p>
    <p class="marca">{esc(CONTRA_MARCA)}</p>
  </div>
""", "I")


QR_ARCHIVO = "svg/qr_menteviva.svg"
QR_TOP = 68      # mm desde arriba del corte: el bloque (texto, QR, nombre, logo y usuario) queda al medio de la página


def pagina_qr():
    """Página 41 (a la derecha): texto, QR de 28 mm, "MenteViva", isotipo de 25 mm y usuario, todo centrado."""
    logo = ruta_logo()
    if logo:
        img = f'<img src="{logo.as_uri()}" style="width:{LOGO_ANCHO}mm; margin:0 auto">'
    else:
        img = f'<div style="height:{LOGO_ANCHO * LOGO_PROPORCION}mm"></div>'          # hueco reservado: falta el archivo del logo
    mm = QR_LADO + 2 * QR_MARGEN
    return pagina(f"""
  <div class="caja contra" style="top:{QR_TOP}mm">
    <p>{partir(QR_TEXTO, "cuerpo", 20, ANCHO_UTIL)}</p>
    <div style="margin-top:6mm">{_svg_img(QR_ARCHIVO, mm).replace('style="', 'style="margin:0 auto; ')}</div>
    <p class="nombre" style="margin-top:3mm">{esc(QR_NOMBRE)}</p>
    <div style="margin-top:{LOGO_AIRE + 4}mm">{img}</div>
    <p class="usuario" style="margin-top:{LOGO_AIRE}mm">{esc(CONTRA_USUARIO)}</p>
  </div>
""", "D")


def pagina_en_blanco_total():
    """Página 42: completamente en blanco, sin nota ni número, para que el total sea par."""
    return pagina("", "I")


# ===================================================================== ARMADO
# El libro se arma por pliegos (página izquierda + derecha). La portada es la página 1 (derecha); cada
# mandala y cada página para pintar va en una página derecha, con su reverso (izquierda) en blanco, así el
# marcador no traspasa. El ejemplo pintado va en la izquierda, enfrente del mandala, para mirarlo a la vez.
EDICIONES = {"venta": "libro-chakras-venta.pdf", "mama": "libro-chakras-mama.pdf"}


def armar_secuencia(edicion="venta"):
    """Lista de todas las páginas, en orden: dict(nombre, lado, html, info). La posición decide el lado
    (impar = derecha, par = izquierda) y el número de página."""
    seq = []

    def add(nombre, lado, html, **info):
        seq.append(dict(nombre=nombre, lado=lado, html=html, info=dict(nombre=nombre, lado=lado, **info)))

    def n():
        return len(seq) + 1

    ancho_c = 2 * (M.RADIO_CORAZON + 1)
    ancho_l = 36
    add("portada", "D", pagina_portada(), numero=None)
    add("legal", "I", pagina_legal(), numero=None,
        imagenes=[(CX - ancho_l / 2, 38, CX - ancho_l / 2 + ancho_l, 38 + ancho_l)], x_dibujos="I")
    add("dedicatoria", "D", pagina_dedicatoria(edicion), numero=None, edicion=edicion,
        imagenes=[(CX - ancho_c / 2, 24, CX + ancho_c / 2, 24 + ancho_c)], lineas_cortas=1 if edicion == "venta" else 0)
    add("que_es_un_chakra", "I", pagina_que_es(n()), numero=n())
    add("como_usar", "D", pagina_como_usar(n()), numero=n())
    base = CENTRO_MANDALA_Y + RADIO + 2
    for i, ch in enumerate(CHAKRAS):
        clave = ch["clave"]
        paleta = [M.PALETA[c] for c in paleta_de(clave)]
        comun = dict(clave=clave, paleta=paleta, protagonista=paleta[0])
        add(f"{clave}_ejemplo", "I", pagina_ejemplo(ch, i, n(), f"ejemplos/{clave}.svg"), numero=n(), a_color=True,
            mandala=(CX_I, CENTRO_MANDALA_Y, RADIO), fila_paleta=base + 2.5, **comun)
        add(f"{clave}_mandala", "D", pagina_mandala(ch, i, n(), f"svg/{clave}.svg"), numero=n(), marcador=True,
            afirmacion=ch["afirmacion"], mandala=(CX, CENTRO_MANDALA_Y, RADIO), fila_paleta=Y_LEYENDA, **comun)
        add(f"{clave}_en_blanco", "I", pagina_blanca(n()), en_blanco=True, numero=n(), centrado=True)
        add(f"{clave}_reflexion", "D", pagina_reflexion(ch, i, n(), edicion), numero=n(), clave=clave,
            sin_texto=ch["afirmacion"], tamanos=tamanos_texto(ch, edicion),
            renglones=2 * len(_datos_reflexion(ch, edicion)["preguntas"]))     # la frase aparece una sola vez por capítulo
    colores_int = [M.PALETA[c] for c in INTEGRACION_COLORES]
    add("integracion_ejemplo", "I", pagina_ejemplo_integracion(n(), "ejemplos/integracion.svg"), numero=n(),
        a_color=True, sin_proporcion=True, mandala=(CX_I, CENTRO_INTEGRACION_Y, M.RADIO_INTEGRACION),
        paleta=colores_int, fila_paleta=Y_LEYENDA_INT)
    add("integracion", "D", pagina_integracion(n(), "svg/integracion.svg"), numero=n(), marcador=True,
        mandala=(CX, CENTRO_INTEGRACION_Y, M.RADIO_INTEGRACION), sin_proporcion=True, paleta=colores_int,
        fila_paleta=Y_LEYENDA_INT)
    add("integracion_en_blanco", "I", pagina_blanca(n()), en_blanco=True, numero=n(), centrado=True)
    add("compartir", "D", pagina_compartir(n(), "svg/par_de_flores.svg"), numero=n(), marcador=True, imagenes=True)
    add("compartir_en_blanco", "I", pagina_blanca(n()), en_blanco=True, numero=n(), centrado=True)
    add("cierre", "D", pagina_cierre(n()), numero=n(), afirmacion=FRASE_FINAL, renglones=3, lineas_cortas=1)
    # el final es igual en las dos ediciones: la carta (40), el QR con el isotipo (41) y una hoja en blanco (42)
    add("contratapa", "I", pagina_contratapa(), numero=None, edicion=edicion, centrado=True,
        titulo_pt=distribucion_contra()[0])
    add("cierre_qr", "D", pagina_qr(), numero=None, edicion=edicion, centrado=True, logo=ruta_logo() is not None,
        logo_ancho=LOGO_ANCHO, qr=dict(url=QR_URL, lado=QR_LADO, margen=QR_MARGEN))
    add("final_en_blanco", "I", pagina_en_blanco_total(), en_blanco=True, sin_nota=True, numero=None)
    for k, p in enumerate(seq):                              # impar = derecha, par = izquierda
        assert p["lado"] == ("D" if k % 2 == 0 else "I"), (k + 1, p["nombre"], p["lado"])
    return seq


def ejemplos_colores_integracion():
    import ejemplos
    return ejemplos.colores_integracion()


def informacion_paginas(edicion="venta"):
    """Descripción de cada página, para los controles de verificar.py."""
    return [p["info"] for p in armar_secuencia(edicion)]


def construir():
    preparar_fuentes()
    for carpeta in ("svg", "preview", "ejemplos", "_tmp"):
        (AQUI / carpeta).mkdir(exist_ok=True)

    mandalas_svg = {c["clave"]: M.MANDALAS[c["clave"]]() for c in CHAKRAS}
    mandalas_svg["integracion"] = M.integracion()
    mandalas_svg["par_de_flores"] = M.par_de_flores()
    for clave, svg in mandalas_svg.items():
        (AQUI / "svg" / f"{clave}.svg").write_text(svg, encoding="utf-8")
    # ejemplos pintados ("Así podría quedar"): el mismo dibujo, con los colores de la paleta, en vector
    import ejemplos
    for viejo in (AQUI / "ejemplos").glob("*"):
        viejo.unlink()
    for c in CHAKRAS:
        (AQUI / "ejemplos" / f"{c['clave']}.svg").write_text(ejemplos.ejemplo(c["clave"]), encoding="utf-8")
    (AQUI / "ejemplos" / "integracion.svg").write_text(ejemplos.ejemplo_integracion(), encoding="utf-8")
    (AQUI / "svg" / "portada_arte.svg").write_text(M.portada_arte(), encoding="utf-8")
    (AQUI / "svg" / "dedicatoria_corazon.svg").write_text(M.corazon_linea(), encoding="utf-8")
    import codigo_qr
    qr_svg, qr_modulos, qr_version = codigo_qr.svg_qr(QR_URL, QR_LADO, QR_MARGEN)
    (AQUI / QR_ARCHIVO).write_text(qr_svg, encoding="utf-8")
    print(f"QR: versión {qr_version}, {qr_modulos} módulos, {QR_LADO / qr_modulos:.2f} mm por módulo")

    for viejo in ("libro_mandalas_chakras.pdf", "libro_para_mama.pdf"):          # nombres anteriores
        (AQUI / viejo).unlink(missing_ok=True)
    if ruta_logo() is None:
        print("AVISO: falta el isotipo de la página 41 (edición para vender): ponelo en libro-mandalas/assets/isotipo.svg")
    from weasyprint import HTML
    from pypdf import PdfReader, PdfWriter
    from pypdf.generic import RectangleObject
    pt = 72 / 25.4
    corte_d = RectangleObject([0, SANGRE * pt, ANCHO * pt, (PAG_H - SANGRE) * pt])               # el sangrado queda a la derecha
    corte_i = RectangleObject([SANGRE * pt, SANGRE * pt, PAG_W * pt, (PAG_H - SANGRE) * pt])     # y a la izquierda
    sangrado = RectangleObject([0, 0, PAG_W * pt, PAG_H * pt])
    paginas = None
    for edicion, archivo in EDICIONES.items():
        paginas = armar_secuencia(edicion)
        documento = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Mandalas de los 7 chakras · Un color a la vez</title><style>{css()}</style></head>
<body>{"".join(p["html"] for p in paginas)}</body></html>"""
        (AQUI / "_tmp" / f"libro_{edicion}.html").write_text(documento, encoding="utf-8")
        crudo = AQUI / "_tmp" / f"crudo_{edicion}.pdf"
        HTML(string=documento, base_url=str(AQUI)).write_pdf(str(crudo))
        # Todas las páginas llevan las cajas de corte y de sangrado, como pide la imprenta.
        lector = PdfReader(str(crudo))
        assert len(lector.pages) == len(paginas), (len(lector.pages), len(paginas))
        escritor = PdfWriter()
        for p, datos in zip(lector.pages, paginas):
            pag = escritor.add_page(p)
            pag.trimbox = corte_i if datos["lado"] == "I" else corte_d
            pag.bleedbox = sangrado
        escritor.add_metadata({"/Title": "Mandalas de los 7 chakras · Un color a la vez",
                               "/Author": "Dani Navarro (Daniela Navarro · Longevidad Emocional)"})
        with open(AQUI / archivo, "wb") as fh:
            escritor.write(fh)
        print(f"PDF: {archivo} ({len(paginas)} páginas = {len(paginas) // 2} hojas)")

    # PNG de revisión (edición para vender), recortados al tamaño final, y pliegos (izquierda + derecha)
    from PIL import Image
    paginas = armar_secuencia("venta")
    prev = AQUI / "preview"
    for viejo in list(prev.glob("*.png")) + list((prev / "pliegos").glob("*.png") if (prev / "pliegos").exists() else []):
        viejo.unlink()
    (prev / "pliegos").mkdir(exist_ok=True)
    dpi = 110
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(AQUI / EDICIONES["venta"]), str(prev / "p")], check=True)
    generados = sorted(prev.glob("p-*.png"))      # pdftoppm numera p-1, p-01… según la cantidad
    assert len(generados) == len(paginas), (len(generados), len(paginas))
    px = dpi / 25.4
    recortes = []
    for i, (origen, datos) in enumerate(zip(generados, paginas), 1):
        x0 = round(SANGRE * px) if datos["lado"] == "I" else 0
        img = Image.open(origen).crop((x0, round(SANGRE * px), x0 + round(ANCHO * px), round((SANGRE + ALTO) * px)))
        img.save(prev / f"{i:02d}_{datos['nombre']}.png")
        recortes.append(img)
        origen.unlink()
    for i in range(1, len(recortes) - 1, 2):     # pliegos: izquierda (par) + derecha (impar siguiente)
        izq, der = recortes[i], recortes[i + 1]
        lienzo = Image.new("RGB", (izq.width + der.width, izq.height), "#d8d2c8")
        lienzo.paste(izq, (0, 0)); lienzo.paste(der, (izq.width, 0))
        lienzo.save(prev / "pliegos" / f"pliego_{i + 1:02d}-{i + 2:02d}.png")
    print("PNG:", len(list(prev.glob('*.png'))), "páginas y", len(list((prev / 'pliegos').glob('*.png'))), "pliegos")
    return mandalas_svg


if __name__ == "__main__":
    construir()
