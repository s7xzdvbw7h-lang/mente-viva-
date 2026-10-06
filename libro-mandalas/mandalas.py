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


# Paleta de marca "Luz plena" v2. Máximo 3 colores por pieza, contando el fondo.
MARFIL = "#F7F1E9"        # fondo
CACAO = "#4A3B33"         # tinta
ROSA_CENIZAS = "#8E4E52"  # acento único


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


def borde_festoneado(r_valle, r_max, n, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Contorno de n arcos hacia afuera, apoyados en un círculo de radio r_valle.
    La cresta de cada arco llega justo a r_max."""
    paso = 360 / n
    punto_medio = r_valle * math.cos(math.radians(paso / 2))   # distancia al centro de la cuerda
    altura = r_max - punto_medio
    cuerda = 2 * r_valle * math.sin(math.radians(paso / 2))
    rho = (cuerda ** 2 / 4 + altura ** 2) / (2 * altura)
    pts = [polar(r_valle, paso * k) for k in range(n)]
    d = f"M{_n(pts[0][0])},{_n(pts[0][1])}"
    for k in range(1, n + 1):
        x, y = pts[k % n]
        d += f" A{_n(rho)},{_n(rho)} 0 0 1 {_n(x)},{_n(y)}"
    return trazo(d + " Z", fill, stroke, w)


def rombo(cx, cy, d, fill=BLANCO, stroke=NEGRO, w=LINEA):
    return poligono([(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy)], fill, stroke, w)


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
RADIO_MANDALA = 86  # deja lugar arriba (nombre y color) y abajo (frase) dentro de los márgenes de 15 mm


_ACENTO = "@ACENTO@"


def raiz(radio=RADIO_MANDALA, ancho_petalo=34, r_piedra=47, d_piedra=15,
         fondo=BLANCO, trazo_color=NEGRO, acento=None):
    """Muladhara · 4 pétalos · cuadrado (tierra).

    Del centro hacia afuera: triángulo hacia abajo dentro de un cuadrado, 4 pétalos
    (cada uno con su corazón) que nacen de los lados del cuadrado, 4 "piedras" (rombos)
    en los huecos, y dos anillos de 8 ladrillos escalonados, el exterior festoneado.
    Los pétalos son SOLO 4: el resto de las formas son de tierra (cuadrados, rombos).
    """
    k = radio / 89
    r = lambda v: v * k
    e = []
    # Borde festoneado dividido en 8 ladrillos, y anillo liso
    e.append(borde_festoneado(r(84), radio, 16))
    for i in range(8):
        a = 22.5 + 45 * i
        e.append(linea(polar(r(74), a), polar(r(84), a)))
    e.append(circulo(r(74)))
    # Segundo anillo, también de ladrillos pero escalonados (juntas desfasadas), como un muro
    for i in range(8):
        a = 45 * i
        e.append(linea(polar(r(62), a), polar(r(74), a)))
    e.append(circulo(r(62)))
    # Piedras en las diagonales: rombos lisos
    for i in range(4):
        x, y = polar(r(r_piedra), 45 + 90 * i)
        e.append(rombo(x, y, r(d_piedra), fill=_ACENTO))
    # 4 pétalos, cada uno con su corazón (pétalo interior)
    for i in range(4):
        a = 90 * i
        e.append(petalo(a, r(14), r(62), r(ancho_petalo)))
        e.append(petalo(a, r(29), r(51), r(ancho_petalo - 20), fill=_ACENTO, clase="petalo-interior"))
    # Cuadrado central con triángulo hacia abajo y una semilla
    h = r(20)
    e.append(cuadrado(0, 0, h))
    e.append(poligono([(-h, -h), (h, -h), (0, h)]))
    e.append(circulo(r(6.5), 0, -r(8), fill=_ACENTO))
    svg = documento(e, radio).replace(_ACENTO, acento or fondo)
    if fondo != BLANCO:
        svg = svg.replace(f'fill="{BLANCO}"', f'fill="{fondo}"')
    if trazo_color != NEGRO:
        svg = svg.replace(f'stroke="{NEGRO}"', f'stroke="{trazo_color}"')
    return svg


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
RADIO_PORTADA = 70


def portada_mandala(radio=RADIO_PORTADA):
    """Mandala de la portada: el mismo lenguaje de formas que el interior, en los
    colores de marca (líneas cacao sobre marfil y un solo acento: rosa de las cenizas).
    Un color a la vez: lo único "pintado" es el acento."""
    return raiz(radio=radio, fondo=MARFIL, trazo_color=CACAO, acento=ROSA_CENIZAS)
