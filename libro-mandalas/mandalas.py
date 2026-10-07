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


FORMA_PETALO = (0.20, 0.72, 0.74, 0.40)      # pétalo de loto: cuerpo lleno y punta fina
FORMA_CORAZON = (0.14, 0.78, 0.70, 0.45)     # el corazón de cada pétalo: gota


def capa_petalos(n, r0, r1, ancho, forma=FORMA_PETALO, fase=0.0, orden=None, clase="petalo"):
    """n pétalos parejos alrededor del centro (el primero apunta a `fase` grados, 0 = arriba).
    `orden` es el apilado de atrás hacia adelante; por defecto, en dos capas (pares atrás, impares
    adelante) si n es par, así queda simétrico."""
    if orden is None:
        orden = list(range(0, n, 2)) + list(range(1, n, 2)) if n % 2 == 0 else list(range(n))
    return [petalo(fase + 360 * k / n, r0, r1, ancho, forma=forma, clase=clase) for k in orden]


def sectores(r0, r1, n, fase=0.0):
    """n rayitas radiales (divisiones de un anillo)."""
    return [linea(polar(r0, fase + 360 * k / n), polar(r1, fase + 360 * k / n)) for k in range(n)]


def perlas(n, r_centro, r_perla, fase=0.0):
    """n círculos iguales sobre un anillo."""
    return [circulo(r_perla, *polar(r_centro, fase + 360 * k / n)) for k in range(n)]


def borde_dientes(r_valle, r_max, n, fase=0.0, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Borde en zigzag de n dientes (llamas / rayos) apoyados en un círculo de radio r_valle."""
    paso = 360 / n
    pts = []
    for k in range(n):
        pts.append(polar(r_valle, fase + paso * k))
        pts.append(polar(r_max, fase + paso * (k + 0.5)))
    return poligono(pts, fill, stroke, w)


def borde_concavo(r_valle, r_max, n, fase=0.0, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Estrella de n puntas con los lados curvados hacia adentro (como remolinos de aire)."""
    paso = 360 / n
    cuerda = 2 * r_max * math.sin(math.radians(paso / 2))
    # la hondura del arco hace que el punto medio de cada lado quede en r_valle
    hondo = r_max * math.cos(math.radians(paso / 2)) - r_valle
    rho = (cuerda ** 2 / 4 + hondo ** 2) / (2 * hondo)
    pts = [polar(r_max, fase + paso * k) for k in range(n)]
    d = f"M{_n(pts[0][0])},{_n(pts[0][1])}"
    for k in range(1, n + 1):
        x, y = pts[k % n]
        d += f" A{_n(rho)},{_n(rho)} 0 0 0 {_n(x)},{_n(y)}"
    return trazo(d + " Z", fill, stroke, w)


def hexagrama(r, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Estrella de seis puntas (dos triángulos) con su hexágono central: 7 zonas."""
    pts = []
    for k in range(6):
        pts.append(polar(r, 60 * k))
        pts.append(polar(r / math.sqrt(3), 60 * k + 30))
    hexa = [polar(r / math.sqrt(3), 60 * k + 30) for k in range(6)]
    return poligono(pts, fill, stroke, w) + poligono(hexa, "none", stroke, w)


def triangulo_abajo(r, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Triángulo con la punta hacia abajo, inscrito en un círculo de radio r."""
    return poligono([polar(r, 180), polar(r, 300), polar(r, 60)], fill, stroke, w)


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


def borde_festoneado(r_valle, r_max, n, fase=0.0, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Contorno de n arcos hacia afuera, apoyados en un círculo de radio r_valle.
    La cresta de cada arco llega justo a r_max. `fase` gira el borde (grados)."""
    paso = 360 / n
    punto_medio = r_valle * math.cos(math.radians(paso / 2))   # distancia al centro de la cuerda
    altura = r_max - punto_medio
    cuerda = 2 * r_valle * math.sin(math.radians(paso / 2))
    rho = (cuerda ** 2 / 4 + altura ** 2) / (2 * altura)
    pts = [polar(r_valle, paso * k + fase) for k in range(n)]
    d = f"M{_n(pts[0][0])},{_n(pts[0][1])}"
    for k in range(1, n + 1):
        x, y = pts[k % n]
        d += f" A{_n(rho)},{_n(rho)} 0 0 1 {_n(x)},{_n(y)}"
    return trazo(d + " Z", fill, stroke, w)


def rombo_suave(cx, cy, d, suavidad=0.3, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Rombo de semidiagonal d con las cuatro puntas redondeadas (suavidad = fracción del lado)."""
    v = [(cx, cy - d), (cx + d, cy), (cx, cy + d), (cx - d, cy)]
    lerp = lambda a, b, t: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
    desc = ""
    for i in range(4):
        ant, p, sig = v[i - 1], v[i], v[(i + 1) % 4]
        a, b = lerp(p, ant, suavidad), lerp(p, sig, suavidad)
        desc += ("M" if i == 0 else "L") + f"{_n(a[0])},{_n(a[1])} Q{_n(p[0])},{_n(p[1])} {_n(b[0])},{_n(b[1])} "
    return trazo(desc + "Z", fill, stroke, w)


def cuadrado_suave(cx, cy, medio_lado, radio_esquina, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Cuadrado con las esquinas redondeadas."""
    h, rr = medio_lado, radio_esquina
    x0, x1, y0, y1 = cx - h, cx + h, cy - h, cy + h
    desc = (f"M{_n(x0 + rr)},{_n(y0)} L{_n(x1 - rr)},{_n(y0)} Q{_n(x1)},{_n(y0)} {_n(x1)},{_n(y0 + rr)} "
            f"L{_n(x1)},{_n(y1 - rr)} Q{_n(x1)},{_n(y1)} {_n(x1 - rr)},{_n(y1)} "
            f"L{_n(x0 + rr)},{_n(y1)} Q{_n(x0)},{_n(y1)} {_n(x0)},{_n(y1 - rr)} "
            f"L{_n(x0)},{_n(y0 + rr)} Q{_n(x0)},{_n(y0)} {_n(x0 + rr)},{_n(y0)} Z")
    return trazo(desc, fill, stroke, w)


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


def raiz(radio=RADIO_MANDALA):
    """Muladhara · 4 pétalos · cuadrado (tierra).

    Del centro hacia afuera: cuadrado con un círculo, 4 pétalos (cada uno con su corazón) que
    nacen de los lados del cuadrado, 4 "piedras" (rombos) en los huecos, un anillo liso y un
    borde de puntillas dividido en 8 ladrillos. Los pétalos son SOLO 4: el resto de las formas
    son de tierra (cuadrados, rombos). Sin triángulo: ese símbolo (fuego) es del Plexo solar.
    """
    k = radio / 89
    r = lambda v: v * k
    e = []
    # Borde de puntillas (24, tres por ladrillo) dividido en 8 ladrillos, y anillo liso
    e.append(borde_festoneado(r(84), radio, 24, fase=7.5))
    for i in range(8):
        a = 22.5 + 45 * i
        e.append(linea(polar(r(74), a), polar(r(84), a)))
    e.append(circulo(r(74)))
    e.append(circulo(r(62)))
    # Piedras en las diagonales: rombos de puntas suaves
    for i in range(4):
        x, y = polar(r(47), 45 + 90 * i)
        e.append(rombo_suave(x, y, r(16.5), 0.30))
    # 4 pétalos, cada uno con su corazón
    for i in range(4):
        a = 90 * i
        e.append(petalo(a, r(14), r(62), r(36), forma=FORMA_PETALO))
        e.append(petalo(a, r(29), r(51), r(18), forma=FORMA_CORAZON, clase="petalo-interior"))
    # Cuadrado central de esquinas suaves, con un círculo
    e.append(cuadrado_suave(0, 0, r(20), r(3)))
    e.append(circulo(r(10)))
    return documento(e, radio)


# ------------------------------------------------------- LOS OTROS SEIS
# Todos comparten el mismo esqueleto (borde, anillo con divisiones, aro liso, pétalos y centro) para
# que se lean como una familia, y cada uno se distingue por su borde, su número de pétalos y el
# símbolo del centro. Las zonas crecen de a poco: Raíz 27 → Corona 64.
def _escala(radio):
    k = radio / 89
    return k, (lambda v: v * k)


def _aro(radio_aro):
    """Círculo sin relleno que se dibuja DESPUÉS de los pétalos: tapa las puntas que lo tocan."""
    return circulo(radio_aro, fill="none")


def sacro(radio=RADIO_MANDALA):
    """Svadhisthana · 6 pétalos · luna creciente (agua)."""
    k, r = _escala(radio)
    e = [borde_festoneado(r(84), radio, 12, fase=15)]
    e += sectores(r(74), r(84), 6, fase=15)
    e += [circulo(r(74)), circulo(r(62))]
    for i in range(6):                                   # 6 gotas de agua entre los pétalos
        e.append(circulo(r(6.5), *polar(r(47), 30 + 60 * i)))
    for i in range(6):
        a = 60 * i
        e.append(petalo(a, r(16), r(62) + 0.3, r(38), forma=FORMA_PETALO))
        e.append(petalo(a, r(30), r(54), r(18), forma=FORMA_CORAZON, clase="petalo-interior"))
    e.append(_aro(r(62)))
    e.append(circulo(r(27)))
    e.append(media_luna(0, 0, r(22), r(18), r(8), 0))
    return documento(e, radio)


def plexo(radio=RADIO_MANDALA):
    """Manipura · 10 pétalos · triángulo hacia abajo (fuego), borde de llamitas."""
    k, r = _escala(radio)
    e = [borde_dientes(r(78), radio, 20, fase=0)]
    e += sectores(r(74), r(78), 10, fase=0)
    e += [circulo(r(74)), circulo(r(62))]
    e += capa_petalos(10, r(18), r(62) + 0.3, r(22), orden=list(range(10)))
    e.append(_aro(r(62)))
    e += [circulo(r(27)), triangulo_abajo(r(27))]
    return documento(e, radio)


def corazon(radio=RADIO_MANDALA):
    """Anahata · 12 pétalos · hexagrama (aire)."""
    k, r = _escala(radio)
    e = [borde_concavo(r(78), radio, 12, fase=0)]
    e += sectores(r(74), r(78), 6, fase=15)
    e += [circulo(r(74)), circulo(r(62))]
    e += capa_petalos(12, r(18), r(62) + 0.3, r(18), forma=(0.30, 0.62, 0.70, 0.62), fase=0, orden=list(range(12)))
    e.append(_aro(r(62)))
    e += [circulo(r(32)), hexagrama(r(32))]
    return documento(e, radio)


def garganta(radio=RADIO_MANDALA):
    """Vishuddha · 16 pétalos · círculo (éter), con un collar de perlas."""
    k, r = _escala(radio)
    e = [circulo(radio)]
    e += sectores(r(77), radio, 16, 0)
    e.append(circulo(r(77)))
    e += perlas(16, r(68.5), r(5.4), fase=11.25)
    e.append(circulo(r(60)))
    e += capa_petalos(16, r(20), r(54), r(22), forma=(0.30, 0.62, 0.70, 0.62))
    e += [circulo(r(28)), circulo(r(13))]
    return documento(e, radio)


def tercer_ojo(radio=RADIO_MANDALA):
    """Ajna · 2 pétalos grandes (las alas) · círculo central (el ojo), con dos abanicos de rayos."""
    k, r = _escala(radio)
    e = [borde_festoneado(r(84), radio, 16, fase=0)]
    e += sectores(r(74), r(84), 16, fase=0)
    e.append(circulo(r(74)))
    e += sectores(r(62), r(74), 8, fase=0)
    e.append(circulo(r(62)))
    for base in (0, 180):                                # abanicos de rayos arriba y abajo
        for i in range(6):
            a = base - 50 + 100 * i / 5
            e.append(linea(polar(r(26), a), polar(r(62), a)))
        p, q = polar(r(45), base - 50), polar(r(45), base + 50)
        e.append(trazo(f"M{_n(p[0])},{_n(p[1])} A{_n(r(45))},{_n(r(45))} 0 0 1 {_n(q[0])},{_n(q[1])}"))
    for a in (90, 270):
        e.append(petalo(a, r(14), r(62) + 0.3, r(46), forma=FORMA_PETALO))
        e.append(petalo(a, r(30), r(52), r(22), forma=FORMA_CORAZON, clase="petalo-interior"))
    e.append(_aro(r(62)))
    e += [circulo(r(26)), circulo(r(12))]
    return documento(e, radio)


def corona(radio=RADIO_MANDALA):
    """Sahasrara · loto de 3 capas (12 + 12 + 6 = 30 pétalos), borde de 36 puntillas."""
    k, r = _escala(radio)
    e = [borde_festoneado(r(84), radio, 36, fase=0)]
    e += sectores(r(74), r(84), 18, 0)
    e += [circulo(r(74)), circulo(r(62))]
    e += capa_petalos(12, r(32), r(62) + 0.3, r(24))                                      # capa de atrás
    e += capa_petalos(12, r(32), r(48), r(12), fase=15)                                   # entre los grandes
    e += capa_petalos(6, r(24), r(36), r(26))                                             # capa del frente
    e.append(_aro(r(62)))
    e += [circulo(r(20)), circulo(r(10))]
    return documento(e, radio)


# ------------------------------------------------------------ INTEGRACIÓN
# Los siete chakras juntos, como en la portada: la flor del centro (Corona) y seis flores alrededor
# (Raíz arriba y, en sentido horario, Sacro, Plexo solar, Corazón, Garganta y Tercer ojo), unidas por
# un aro y por radios. Para colorear: las flores son simples (zonas grandes), no la versión de la portada.
RADIO_INTEGRACION = 87
ORDEN_SATELITES = ("raiz", "sacro", "plexo", "corazon", "garganta", "tercer_ojo")   # horario desde arriba


def _flor_colorear(x, y, R, n, base, ancho, centro, forma, giro=0):
    """Flor simple de n pétalos con un círculo en el centro, ubicada en (x, y) y girada `giro` grados."""
    cuerpo = capa_petalos(n, base, R, ancho, forma=forma, clase="petalo-flor") + [circulo(centro)]
    return [f'<g transform="translate({_n(x)},{_n(y)}) rotate({_n(giro)})">{"".join(cuerpo)}</g>']


def integracion(radio=RADIO_INTEGRACION):
    """Siete flores (una por chakra) dentro de un aro. Todas las zonas miden más de 10 mm."""
    Rc, Rs, hueco = 34, 21, 8
    D = Rc + Rs + hueco                      # distancia del centro a cada flor de alrededor
    afuera = D + Rs + 3                      # círculo exterior
    e = [circulo(afuera), circulo(D, fill="none")]
    for i in range(6):                       # divisiones entre las flores, en el anillo de afuera
        e.append(linea(polar(D, 30 + 60 * i), polar(afuera, 30 + 60 * i)))
        e.append(linea((0, 0), polar(D, 60 * i)))                       # radios hacia cada flor
    e += _flor_colorear(0, 0, Rc, 12, 10, 15, 13, (0.30, 0.62, 0.70, 0.62))
    for i in range(6):
        x, y = polar(D, 60 * i)
        e += _flor_colorear(x, y, Rs, 6, 5, 16, 7.5, FORMA_PETALO, giro=60 * i)
    return documento(e, afuera)


# Cuántos pétalos tiene cada uno (los "petalo-interior" son corazones de adentro, no cuentan)
MANDALAS = {"raiz": raiz, "sacro": sacro, "plexo": plexo, "corazon": corazon,
            "garganta": garganta, "tercer_ojo": tercer_ojo, "corona": corona}
PETALOS = {"raiz": 4, "sacro": 6, "plexo": 10, "corazon": 12, "garganta": 16, "tercer_ojo": 2, "corona": 30}


# ------------------------------------------------- DEDICATORIA (solo línea)
RADIO_CORAZON = 36


def corazon_linea():
    """Pequeño mandala de corazón: 12 pétalos en dos capas (los pares atrás, los impares adelante,
    así queda simétrico), solo línea. Todas sus zonas miden más de 8 mm."""
    orden = list(range(0, 12, 2)) + list(range(1, 12, 2))
    e = [petalo(30 * k, 5, RADIO_CORAZON, 14, forma=(0.30, 0.62, 0.70, 0.62), clase="petalo-dedicatoria") for k in orden]
    e.append(circulo(10))
    return documento(e, RADIO_CORAZON, margen=1.0)


# ----------------------------------------------------------------- PORTADA
# La portada es la que diseñó Dani: siete flores de colores unidas por una red dorada, sobre una
# tarjeta crema, con una banda turquesa. Todas las medidas se tomaron de portada.png (4,333 px/mm).
# Cada flor: pétalos exteriores claros, pétalos medios con una gota clara adentro, y un centro de
# disco, aro y punto. La flor central es la satélite agrandada, con 12 pétalos en lugar de 8.
COLORES_FLOR = {
    "centro":   dict(linea="#7A4A9E", exterior="#CAB7D8", medio="#A989C0", claro="#E7DEEE"),
    "rojo":     dict(linea="#B3362C", exterior="#E1AFAB", medio="#CE7C76", claro="#F1DBD9"),
    "naranja":  dict(linea="#C8651B", exterior="#E9C1A4", medio="#DB9B6B", claro="#F5E3D6"),
    "amarillo": dict(linea="#B8890A", exterior="#E3D09D", medio="#D1B260", claro="#F2EAD3"),
    "verde":    dict(linea="#3D8A45", exterior="#B1D0B5", medio="#81B386", claro="#DCEADE"),
    "azul":     dict(linea="#2F72B5", exterior="#ACC7E1", medio="#78A3CF", claro="#DAE6F2"),
    "indigo":   dict(linea="#43449B", exterior="#B4B4D7", medio="#8585BE", claro="#DDDDED"),
}
# Colores de los chakras en el interior (pestañas y círculo de color): los mismos de la portada de Dani.
COLORES = {k: COLORES_FLOR[f]["linea"] for k, f in (
    ("raiz", "rojo"), ("sacro", "naranja"), ("plexo", "amarillo"), ("corazon", "verde"),
    ("garganta", "azul"), ("tercer_ojo", "indigo"), ("corona", "centro"))}

ORO_PORTADA = "#C2A878"        # oro de la marca: red de líneas
FONDO_PORTADA = "#FDFAF5"      # tarjeta crema
BANDA_PORTADA = "#1F5F78"      # banda turquesa
# forma de las flores (mm), ajustada por comparación píxel a píxel con portada.png
FLOR_SAT = dict(n=8, R_o=19.590, r0_o=8.685, w_o=8.865, f_o=(0.177, 0.517, 0.600, 0.525), R_m=15.800, r0_m=3.511,
                w_m=9.000, f_m=(0.185, 0.619, 0.737, 0.611), h_r0=6.948, h_r1=12.700, h_w=3.120,
                f_h=(0.045, 0.756, 0.787, 0.629), disc=5.986, circ=3.553, dot=1.156, trazo=0.670)
FLOR_CEN = dict(n=12, R_o=29.600, r0_o=13.440, w_o=10.640, f_o=(-0.010, 0.558, 0.542, 0.550), R_m=24.100, r0_m=6.064,
                w_m=10.640, f_m=(0.080, 0.663, 0.674, 0.620), h_r0=10.200, h_r1=19.400, h_w=3.641,
                f_h=(0.210, 0.852, 0.711, 0.528), disc=9.034, circ=5.400, dot=1.900, trazo=0.914)

# Para que todo entre en los márgenes de 15 mm de impresión, la composición original se subió:
# el título y el subtítulo SUBIR_TITULO mm y todo lo demás SUBIR_RESTO mm (el borde de abajo de la
# tarjeta pasa de 290,8 a 282 mm). El original tenía "Para mamá" a 13 mm del borde de la hoja.
SUBIR_TITULO = 3.5
SUBIR_RESTO = 7.0

# centros de las flores en portada.png (mm, posición original) y ya subidos
_CENTROS_ORIGINAL = {"centro": (104.83, 154.07), "rojo": (105.12, 101.89), "naranja": (149.39, 127.43),
                     "amarillo": (149.32, 179.93), "verde": (105.20, 205.69), "azul": (60.17, 179.98),
                     "indigo": (60.24, 127.42)}
CENTROS_PORTADA = {k: (x, y - SUBIR_RESTO) for k, (x, y) in _CENTROS_ORIGINAL.items()}
SATELITES = ("rojo", "naranja", "amarillo", "verde", "azul", "indigo")   # en sentido horario desde arriba
TARJETA = (15.0, 15.0, 194.8, 282.0, 4.0)       # x0, y0, x1, y1, radio de las esquinas (el original llegaba a 290,8)
BANDA = (15.0, 243.5 - SUBIR_RESTO, 194.8, 269.5 - SUBIR_RESTO)   # x0, y0, x1, y1 (de borde a borde de la tarjeta)
LINEA_ORO = 0.3


def _orden_petalos(n, orden):
    """Orden en que se apilan los pétalos medios (de atrás hacia adelante)."""
    if isinstance(orden, tuple):            # (inicio, sentido): apilado secuencial desde `inicio`
        inicio, sentido = orden
        return [(inicio + sentido * j) % n for j in range(n)]
    return list(range(n))


def flor(cx, cy, P, col):
    """Una flor de la portada centrada en (cx, cy). Devuelve un grupo SVG (de atrás hacia adelante)."""
    n, e = P["n"], []
    w = P["trazo"]
    L, F, S = col["linea"], col["exterior"], col["medio"]
    # pétalos exteriores: entre los medios (medio paso de giro)
    for k in range(n):
        a = 180 / n + 360 * k / n
        e.append(trazo(petalo_d(a, P["r0_o"], P["R_o"], P["w_o"], P["f_o"]), F, L, w))
    # pétalos medios, cada uno con su gota clara
    for k in _orden_petalos(n, P.get("orden", "sec")):
        a = 360 * k / n
        e.append(trazo(petalo_d(a, P["r0_m"], P["R_m"], P["w_m"], P["f_m"]), S, L, w))
        e.append(trazo(petalo_d(a, P["h_r0"], P["h_r1"], P["h_w"], P["f_h"]), col["claro"], L, w))
    # centro: disco claro, aro y punto
    e.append(circulo(P["disc"], 0, 0, fill=col["claro"], stroke=L, w=w))
    e.append(circulo(P["circ"], 0, 0, fill=S, stroke=L, w=w))
    e.append(circulo(P["dot"], 0, 0, fill=L, stroke=None))
    return f'<g transform="translate({_n(cx)},{_n(cy)})">' + "".join(e) + "</g>"


def portada_arte():
    """Toda la parte gráfica de la portada (sin textos): tarjeta, banda, red dorada y las 7 flores.
    Página A4 completa en mm."""
    x0, y0, x1, y1, rx = TARJETA
    e = [f'<rect x="{_n(x0)}" y="{_n(y0)}" width="{_n(x1 - x0)}" height="{_n(y1 - y0)}" rx="{_n(rx)}" fill="{FONDO_PORTADA}"/>']
    bx0, by0, bx1, by1 = BANDA
    e.append(f'<rect x="{_n(bx0)}" y="{_n(by0)}" width="{_n(bx1 - bx0)}" height="{_n(by1 - by0)}" fill="{BANDA_PORTADA}"/>')
    # red dorada: dos círculos, hexágono, estrella de seis puntas y rayos del centro a cada flor
    c0 = (104.85, 153.8 - SUBIR_RESTO)
    oro = dict(fill="none", stroke=ORO_PORTADA, w=LINEA_ORO)
    e.append(circulo(61.0, c0[0], c0[1], **oro))
    e.append(circulo(51.6, c0[0], c0[1], **oro))
    pts = [CENTROS_PORTADA[n] for n in SATELITES]
    e.append(poligono(pts, **oro))
    e.append(poligono([pts[0], pts[2], pts[4]], **oro))
    e.append(poligono([pts[1], pts[3], pts[5]], **oro))
    for p in pts:
        e.append(linea(CENTROS_PORTADA["centro"], p, stroke=ORO_PORTADA, w=LINEA_ORO))
    # flores
    for n in SATELITES:
        e.append(flor(*CENTROS_PORTADA[n], FLOR_SAT, COLORES_FLOR[n]))
    e.append(flor(*CENTROS_PORTADA["centro"], FLOR_CEN, COLORES_FLOR["centro"]))
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297">'
            + "".join(e) + "</svg>")
