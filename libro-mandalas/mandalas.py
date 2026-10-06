"""Geometría de los mandalas: SVG calculado a mano, sin imágenes externas.

Unidades: milímetros. El origen (0, 0) es el centro del mandala; 0° apunta
hacia arriba y los ángulos crecen en sentido horario.

Los dibujos se arman "de atrás hacia adelante" (método del pintor): cada forma
lleva relleno blanco y trazo negro, así lo que queda tapado no deja líneas
sueltas que fabriquen zonas diminutas.
"""
import math

# Grosor de línea: 0,75 mm = 2,83 px a 96 dpi (el rango pedido es 2,5 a 3 px).
LINEA = 0.75
NEGRO = "#111111"
BLANCO = "#ffffff"

# Colores de los chakras (usados en pestañas, círculo de color y portada).
COLORES = {
    "raiz": "#D62F2F",
    "sacro": "#F28A1E",
    "plexo": "#F2C318",
    "corazon": "#2F9E5B",
    "garganta": "#3FA7DC",
    "tercer_ojo": "#3B3FA6",
    "corona": "#8E4BB5",
}


# ---------------------------------------------------------------- utilidades
def _n(x):
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def polar(r, grados):
    a = math.radians(grados)
    return (r * math.sin(a), -r * math.cos(a))


def _local(grados, u, v):
    """Punto a distancia u sobre el eje que apunta a `grados` y v hacia un costado."""
    ax, ay = polar(1, grados)
    return (u * ax - v * ay, u * ay + v * ax)


def _attrs(fill, stroke, w):
    s = f'fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{_n(w)}" stroke-linejoin="round" stroke-linecap="round"'
    return s


def circulo(r, cx=0, cy=0, fill=BLANCO, stroke=NEGRO, w=LINEA):
    return f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(r)}" {_attrs(fill, stroke, w)}/>'


def poligono(puntos, fill=BLANCO, stroke=NEGRO, w=LINEA):
    pts = " ".join(f"{_n(x)},{_n(y)}" for x, y in puntos)
    return f'<polygon points="{pts}" {_attrs(fill, stroke, w)}/>'


def trazo(d, fill="none", stroke=NEGRO, w=LINEA):
    return f'<path d="{d}" {_attrs(fill, stroke, w)}/>'


def linea(p, q, stroke=NEGRO, w=LINEA):
    return trazo(f"M{_n(p[0])},{_n(p[1])} L{_n(q[0])},{_n(q[1])}", stroke=stroke, w=w)


def cuadrado(cx, cy, medio_lado, fill=BLANCO, stroke=NEGRO, w=LINEA):
    h = medio_lado
    return poligono([(cx - h, cy - h), (cx + h, cy - h), (cx + h, cy + h), (cx - h, cy + h)], fill, stroke, w)


def petalo_d(grados, r0, r1, ancho, forma=(0.22, 0.66, 0.62, 0.66)):
    """Contorno de un pétalo (almendra con punta) sobre el eje `grados`.

    r0: radio de la base, r1: radio de la punta, ancho: ancho máximo.
    forma = (a1, h1, a2, h2): puntos de control como fracción del largo (a) y
    del ancho (h) en cada lado. Dos curvas cúbicas, simétricas.
    """
    L = r1 - r0
    a1, h1, a2, h2 = forma
    base = _local(grados, r0, 0)
    punta = _local(grados, r1, 0)

    def lado(signo):
        c1 = _local(grados, r0 + a1 * L, signo * h1 * ancho)
        c2 = _local(grados, r0 + a2 * L, signo * h2 * ancho)
        return c1, c2

    c1, c2 = lado(+1)
    d1, d2 = lado(-1)
    P = lambda p: f"{_n(p[0])},{_n(p[1])}"
    return f"M{P(base)} C{P(c1)} {P(c2)} {P(punta)} C{P(d2)} {P(d1)} {P(base)} Z"


def petalo(grados, r0, r1, ancho, fill=BLANCO, stroke=NEGRO, w=LINEA, forma=(0.22, 0.66, 0.62, 0.66), clase="petalo"):
    return f'<g class="{clase}">' + trazo(petalo_d(grados, r0, r1, ancho, forma), fill, stroke, w) + "</g>"


def media_luna(cx, cy, r_ext, r_int, desplazamiento, grados=0, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Media luna (creciente) = círculo grande menos otro círculo desplazado."""
    # Intersección de los dos círculos para cerrar el trazo con arcos.
    dx, dy = polar(desplazamiento, grados)
    d = desplazamiento
    a = (r_ext**2 - r_int**2 + d**2) / (2 * d)
    h = math.sqrt(max(r_ext**2 - a**2, 0))
    ux, uy = dx / d, dy / d
    mx, my = cx + ux * a, cy + uy * a
    p1 = (mx - uy * h, my + ux * h)
    p2 = (mx + uy * h, my - ux * h)
    P = lambda p: f"{_n(p[0])},{_n(p[1])}"
    dpath = (f"M{P(p1)} A{_n(r_ext)},{_n(r_ext)} 0 1 1 {P(p2)} "
             f"A{_n(r_int)},{_n(r_int)} 0 0 0 {P(p1)} Z")
    return trazo(dpath, fill, stroke, w)


def estrella(cx, cy, r, puntas, rot=0, fill=BLANCO, stroke=NEGRO, w=LINEA):
    pts = [polar(r, rot + 360 * k / puntas) for k in range(puntas)]
    pts = [(x + cx, y + cy) for x, y in pts]
    return poligono(pts, fill, stroke, w)


def documento(cuerpo, radio, margen=2.0, fondo=None):
    """Envuelve los elementos en un <svg> cuyo tamaño en mm coincide con el viewBox."""
    lado = 2 * (radio + margen)
    bg = f'<rect x="{_n(-lado/2)}" y="{_n(-lado/2)}" width="{_n(lado)}" height="{_n(lado)}" fill="{fondo}"/>' if fondo else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{_n(lado)}mm" height="{_n(lado)}mm" '
            f'viewBox="{_n(-lado/2)} {_n(-lado/2)} {_n(lado)} {_n(lado)}">{bg}{"".join(cuerpo)}</svg>')


# ------------------------------------------------------------------- RAÍZ
RADIO_MANDALA = 89  # cabe justo en el ancho útil (A4 menos márgenes de 15 mm)

def raiz():
    """Muladhara · 4 pétalos · cuadrado (tierra).

    Del centro hacia afuera: triángulo hacia abajo dentro de un cuadrado,
    4 pétalos que nacen de los lados del cuadrado, 4 "piedras" cuadradas en
    los huecos, un anillo liso y un anillo de 8 ladrillos.
    """
    e = []
    R = RADIO_MANDALA
    # Anillo exterior de 8 ladrillos + anillo liso
    e.append(circulo(R))
    for k in range(8):
        a = 22.5 + 45 * k
        e.append(linea(polar(78, a), polar(R, a)))
    e.append(circulo(78))
    e.append(circulo(66))
    # Piedras cuadradas en los huecos (diagonales)
    for k in range(4):
        x, y = polar(47, 45 + 90 * k)
        e.append(cuadrado(x, y, 8))
    # 4 pétalos, cada uno con su corazón (pétalo interior)
    for k in range(4):
        a = 90 * k
        e.append(petalo(a, 14, 66, 42))
        e.append(petalo(a, 31, 55, 18, clase="petalo-interior"))
    # Cuadrado central con triángulo hacia abajo y una semilla
    h = 21
    e.append(cuadrado(0, 0, h))
    e.append(poligono([(-h, -h), (h, -h), (0, h)]))
    e.append(circulo(6.5, 0, -8))
    return documento(e, R)


# ------------------------------------------------- DEDICATORIA (solo línea)
def corazon_linea():
    """Pequeño mandala de corazón: 12 pétalos, solo línea (para la dedicatoria)."""
    e = []
    R = 27
    e.append(circulo(R))
    e.append(circulo(R - 4))
    for k in range(12):
        e.append(petalo(30 * k, 8, 23, 9, clase="petalo-dedicatoria"))
    e.append(circulo(8))
    return documento(e, R, margen=1.0)


# ----------------------------------------------------------------- PORTADA
def _clarear(hex_color, t):
    c = hex_color.lstrip("#")
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(int(v + (255 - v) * t) for v in (r, g, b))


# (chakra, cantidad de pétalos, radio de la base, radio de la punta, ancho)
_ANILLOS_PORTADA = [
    ("raiz", 4, 0, 19, 15),
    ("sacro", 6, 11, 28, 15),
    ("plexo", 10, 20, 37, 13),
    ("corazon", 12, 29, 46, 13),
    ("garganta", 16, 38, 55, 12),
    ("tercer_ojo", 2, 47, 64, 22),
    ("corona", 36, 56, 72, 9.5),
]
CONTORNO_PORTADA = "#ffffff"


def portada_mandala(radio=72):
    """Loto de siete anillos, del centro (Raíz) hacia afuera (Corona), en color."""
    e = []
    for chakra, n, r0, r1, ancho in reversed(_ANILLOS_PORTADA):
        color = COLORES[chakra]
        if chakra == "tercer_ojo":
            # dos pétalos grandes a los costados (ojo), sobre un disco liso
            e.append(circulo(57, fill=_clarear(color, 0.78), stroke=CONTORNO_PORTADA, w=1.0))
            angulos = [90, 270]
        else:
            angulos = [360 * k / n for k in range(n)]
        for a in angulos:
            e.append(petalo(a, r0, r1, ancho, fill=color, stroke=CONTORNO_PORTADA, w=1.0, clase="petalo-portada"))
    e.append(circulo(5.5, fill="#ffffff", stroke=COLORES["corona"], w=1.2))
    e.append(circulo(2.2, fill=COLORES["plexo"], stroke=None))
    return documento(e, radio, margen=1.0)
