"""Geometría de los mandalas: SVG calculado a mano, sin imágenes externas.

Unidades: milímetros. El origen (0, 0) es el centro del mandala; 0° apunta
hacia arriba y los ángulos crecen en sentido horario.

Los dibujos se arman "de atrás hacia adelante" (método del pintor): cada forma
lleva relleno blanco y trazo negro, así lo que queda tapado no deja líneas
sueltas que fabriquen zonas diminutas.
"""
import math

# Grosor de línea: contorno principal de 3,5 pt (1,235 mm) y divisiones internas de 3 pt (1,058 mm).
# Nada más fino que 2,5 pt.
LINEA = 1.235          # contorno principal (3,5 pt)
LINEA_FINA = 1.058     # divisiones internas (3 pt)
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


_ESC = 1.0      # escala con la que se está armando el dibujo (ver `escalado`): el trazo se compensa


def _attrs(fill, stroke, w):
    s = f'fill="{fill}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{_n(w / _ESC)}" stroke-linejoin="round" stroke-linecap="round"'
    return s


def circulo(r, cx=0, cy=0, fill=BLANCO, stroke=NEGRO, w=LINEA):
    return f'<circle cx="{_n(cx)}" cy="{_n(cy)}" r="{_n(r)}" {_attrs(fill, stroke, w)}/>'


def poligono(puntos, fill=BLANCO, stroke=NEGRO, w=LINEA):
    pts = " ".join(f"{_n(x)},{_n(y)}" for x, y in puntos)
    return f'<polygon points="{pts}" {_attrs(fill, stroke, w)}/>'


def trazo(d, fill="none", stroke=NEGRO, w=LINEA):
    return f'<path d="{d}" {_attrs(fill, stroke, w)}/>'


def linea(p, q, stroke=NEGRO, w=LINEA_FINA):
    return trazo(f"M{_n(p[0])},{_n(p[1])} L{_n(q[0])},{_n(q[1])}", stroke=stroke, w=w)


def poligono_redondeado(puntos, radios, fill=BLANCO, stroke=NEGRO, w=LINEA):
    """Polígono con las esquinas redondeadas. `radios`: un número o uno por vértice (mm que se
    recorta de cada lado antes de la curva)."""
    n = len(puntos)
    if not isinstance(radios, (list, tuple)):
        radios = [radios] * n
    d = ""
    for i, p in enumerate(puntos):
        def hacia(q, dist):
            vx, vy = q[0] - p[0], q[1] - p[1]
            L = math.hypot(vx, vy)
            t = min(dist / L, 0.5)
            return (p[0] + vx * t, p[1] + vy * t)
        a, b = hacia(puntos[i - 1], radios[i]), hacia(puntos[(i + 1) % n], radios[i])
        d += ("M" if i == 0 else "L") + f"{_n(a[0])},{_n(a[1])} Q{_n(p[0])},{_n(p[1])} {_n(b[0])},{_n(b[1])} "
    return trazo(d + "Z", fill, stroke, w)


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


def capa_petalos(n, r0, r1, ancho, forma=FORMA_PETALO, fase=0.0, orden=None, clase="petalo", rellenos=None):
    """n pétalos parejos alrededor del centro (el primero apunta a `fase` grados, 0 = arriba).
    `orden` es el apilado de atrás hacia adelante; por defecto, en dos capas (pares atrás, impares
    adelante) si n es par, así queda simétrico."""
    if orden is None:
        orden = list(range(0, n, 2)) + list(range(1, n, 2)) if n % 2 == 0 else list(range(n))
    return [petalo(fase + 360 * k / n, r0, r1, ancho, forma=forma, clase=clase,
                   fill=(rellenos[k % len(rellenos)] if rellenos else BLANCO)) for k in orden]


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
    """Media luna (creciente) = círculo grande menos otro círculo desplazado `desplazamiento` hacia
    `grados`. Si r_ext = radio del disco que la contiene, las puntas tocan el borde del disco."""
    dx, dy = polar(desplazamiento, grados)
    d = desplazamiento
    a = (r_ext**2 - r_int**2 + d**2) / (2 * d)          # distancia del centro a la cuerda de las puntas
    h = math.sqrt(max(r_ext**2 - a**2, 0))
    ux, uy = dx / d, dy / d
    mx, my = cx + ux * a, cy + uy * a
    p1 = (mx - uy * h, my + ux * h)
    p2 = (mx + uy * h, my - ux * h)
    P = lambda p: f"{_n(p[0])},{_n(p[1])}"
    grande = 1 if a > d else 0                           # el arco interior que queda dentro del disco
    dpath = (f"M{P(p1)} A{_n(r_ext)},{_n(r_ext)} 0 1 1 {P(p2)} "
             f"A{_n(r_int)},{_n(r_int)} 0 {grande} 0 {P(p1)} Z")
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


def escalado(f):
    """Arma el dibujo en sus unidades de diseño y lo agranda con una transformación; los trazos se
    compensan, así las líneas siguen midiendo 3,5 y 3 pt."""
    def envuelta(p=None, escala=None):
        global _ESC
        _ESC = escala or ESCALA_MANDALA
        try:
            return f(p)
        finally:
            _ESC = 1.0
    envuelta.__doc__ = f.__doc__
    return envuelta


def documento(cuerpo, radio, margen=2.0, fondo=None):
    """Envuelve los elementos en un <svg> cuyo tamaño en mm coincide con el viewBox."""
    if _ESC != 1.0:
        cuerpo = [f'<g transform="scale({_n(_ESC)})">' + "".join(cuerpo) + "</g>"]
        radio = radio * _ESC
    lado = 2 * (radio + margen)
    bg = f'<rect x="{_n(-lado/2)}" y="{_n(-lado/2)}" width="{_n(lado)}" height="{_n(lado)}" fill="{fondo}"/>' if fondo else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{_n(lado)}mm" height="{_n(lado)}mm" '
            f'viewBox="{_n(-lado/2)} {_n(-lado/2)} {_n(lado)} {_n(lado)}">{bg}{"".join(cuerpo)}</svg>')


# ------------------------------------------------------------ LOS SIETE MANDALAS
# Todos comparten el mismo esqueleto, así se leen como una familia:
#   · borde exterior (cada chakra, el suyo) con el anillo dividido en "ladrillos",
#   · un aro liso donde terminan los pétalos,
#   · pétalos grandes y redondeados (los que cuenta cada chakra),
#   · un centro grande con el símbolo del elemento.
# Líneas de 3,5 pt (contornos) y 3 pt (divisiones). Nada de microdetalles: las zonas para pintar
# miden 10 mm o más y no hay puntos ni pétalos diminutos.
ANCHO_PAGINA, ALTO_PAGINA = 215.9, 279.4        # 8,5 × 11 pulgadas
RADIO_MANDALA = 82                  # radio con el que se imprime
_R, _RV, _RB = 76, 69, 57          # unidades de diseño: borde, valle del borde y aro de los pétalos
ESCALA_MANDALA = RADIO_MANDALA / _R
_FB = (0.30, 0.62, 0.70, 0.62)
_FD = (0.26, 0.80, 0.70, 0.50)


def _aro(radio_aro=_RB):
    """Círculo sin relleno que se dibuja DESPUÉS de los pétalos: tapa las puntas que lo tocan."""
    return circulo(radio_aro, fill="none")


def _c(p, rol, i=0):
    """Relleno del elemento `rol`: blanco en el dibujo para colorear; un color en el ejemplo pintado.
    Si el rol tiene varios colores, `i` elige uno (se repiten en ciclo)."""
    if not p or rol not in p:
        return BLANCO
    v = p[rol]
    return v[i % len(v)] if isinstance(v, (list, tuple)) else v


def _cuna(r, a0, a1, fill):
    """Sector de círculo (desde el centro), sin contorno: pinta el fondo entre dos pétalos."""
    x0, y0 = polar(r, a0)
    x1, y1 = polar(r, a1)
    return trazo(f"M0,0 L{_n(x0)},{_n(y0)} A{_n(r)},{_n(r)} 0 0 1 {_n(x1)},{_n(y1)} Z", fill, None)


def _lobulos(n, fase, p, valle=_RV):
    """Borde de n lóbulos redondeados, con el anillo dividido en n ladrillos (una línea en cada valle)."""
    return [borde_festoneado(valle, _R, n, fase=fase, fill=_c(p, "borde"))] + sectores(_RB, valle, n, fase)


def _estrella6(r, esquina, valle, fill=BLANCO):
    pts, rad = [], []
    for k in range(6):
        pts.append(polar(r, 60 * k)); rad.append(esquina)
        pts.append(polar(r / math.sqrt(3), 60 * k + 30)); rad.append(valle)
    return poligono_redondeado(pts, rad, fill)


@escalado
def raiz(p=None):
    """Muladhara · 4 pétalos · cuadrado (tierra): ladrillos de tierra y cuatro piedras."""
    e = _lobulos(8, 22.5, p) + [circulo(_RB, fill=_c(p, "fondo"))]
    for i in range(4):
        x, y = polar(40, 45 + 90 * i)
        e.append(rombo_suave(x, y, 14, 0.30, fill=_c(p, "piedra")))
    e += [petalo(90 * i, 14, _RB, 34, forma=FORMA_PETALO, fill=_c(p, "petalos", i)) for i in range(4)]
    e += [cuadrado_suave(0, 0, 17, 4, fill=_c(p, "cuadrado")), circulo(8, fill=_c(p, "punto"))]
    return documento(e, _R)


@escalado
def sacro(p=None):
    """Svadhisthana · 6 pétalos · luna (agua): seis gotas entre los pétalos."""
    e = _lobulos(6, 30, p) + [circulo(_RB, fill=_c(p, "fondo"))]
    if p and "cunas" in p:                                   # entre pétalos, de a dos colores
        e += [_cuna(_RB, 60 + 120 * j, 120 + 120 * j, _c(p, "cunas")) for j in range(3)]
    e.append(_aro())                                         # las cuñas tapan la mitad del aro: se vuelve a dibujar
    for i in range(6):
        e.append(circulo(7.5, *polar(42, 30 + 60 * i), fill=_c(p, "gotas")))
    e += [petalo(60 * i, 15, _RB, 28, forma=FORMA_PETALO, fill=_c(p, "petalos")) for i in range(6)]
    e += [circulo(24, fill=_c(p, "disco")), media_luna(0, 0, 24, 17, 9, 0, fill=_c(p, "luna"))]
    return documento(e, _R)


@escalado
def plexo(p=None):
    """Manipura · 10 pétalos · triángulo hacia abajo (fuego): borde de rayos redondeados."""
    n, paso, pts, rad = 10, 36, [], []
    for k in range(n):
        pts.append(polar(63, paso * (k - 0.5))); rad.append(3)
        pts.append(polar(_R, paso * k)); rad.append(7)
    e = [poligono_redondeado(pts, rad, _c(p, "borde"))] + sectores(_RB, 63, n, paso / 2)
    e += [circulo(_RB, fill=_c(p, "fondo"))]
    if p and "cunas" in p:                                   # entre pétalos, de a dos colores
        e += [_cuna(_RB, 36 + 72 * j, 72 + 72 * j, _c(p, "cunas")) for j in range(5)]
    e += capa_petalos(n, 12, _RB + 0.3, 18, forma=_FD, orden=list(range(n)), rellenos=[_c(p, "petalos")])
    e += [_aro(), circulo(24, fill=_c(p, "disco")),
          poligono_redondeado([polar(24, 180), polar(24, 300), polar(24, 60)], 5, _c(p, "triangulo"))]
    return documento(e, _R)


@escalado
def corazon(p=None):
    """Anahata · 12 pétalos · estrella de seis puntas (aire)."""
    e = _lobulos(12, 15, p) + [circulo(_RB, fill=_c(p, "fondo"))]
    pet = p["petalos"] if p else None
    e += capa_petalos(12, 20, _RB + 0.3, 18, forma=FORMA_PETALO, orden=list(range(12)), rellenos=pet)
    e += [_aro(), _estrella6(22, 5, 2.5, _c(p, "estrella"))]
    return documento(e, _R)


@escalado
def garganta(p=None):
    """Vishuddha · 16 pétalos · círculo (éter): un anillo ancho dividido en 8."""
    e = [circulo(_R, fill=_c(p, "banda"))] + sectores(_RB, _R, 8, 0) + [circulo(_RB, fill=_c(p, "fondo"))]
    pet = p["petalos"] if p else None
    e += capa_petalos(16, 16, _RB + 0.3, 18, forma=FORMA_PETALO, orden=list(range(16)), rellenos=pet)
    e += [_aro(), circulo(24, fill=_c(p, "disco")), circulo(12, fill=_c(p, "centro"))]
    return documento(e, _R)


@escalado
def tercer_ojo(p=None):
    """Ajna · 2 pétalos grandes (las alas) · círculo central, con un anillo que divide lo de arriba y lo de abajo."""
    e = _lobulos(16, 0, p) + [circulo(_RB, fill=_c(p, "fondo")), circulo(40, fill=_c(p, "interior"))]
    e += [petalo(a, 14, _RB + 0.3, 46, forma=FORMA_PETALO, fill=_c(p, "alas")) for a in (90, 270)]
    e += [_aro(), circulo(24, fill=_c(p, "disco")), circulo(11, fill=_c(p, "pupila"))]
    return documento(e, _R)


@escalado
def corona(p=None):
    """Sahasrara · loto de 3 capas (8 + 8 + 4 pétalos), borde de 18 lóbulos."""
    e = _lobulos(18, 0, p) + [circulo(_RB, fill=_c(p, "fondo"))]
    e += capa_petalos(8, 31, _RB + 0.3, 26, orden=list(range(8)), rellenos=[_c(p, "grandes", 0), _c(p, "grandes", 1)])   # capa de atrás
    e += capa_petalos(8, 26, 44, 18, fase=22.5, orden=list(range(8)), rellenos=[_c(p, "medios")])                          # entre los grandes
    e += capa_petalos(4, 20, 34, 24, orden=list(range(4)), rellenos=[_c(p, "internos")])                                   # capa del frente
    e += [_aro(), circulo(18, fill=_c(p, "disco"))]
    return documento(e, _R)


# ------------------------------------------------------------ INTEGRACIÓN
# Los siete chakras juntos, como en la portada: la flor del centro (Corona) y seis flores alrededor
# (Raíz arriba y, en sentido horario, Sacro, Plexo solar, Corazón, Garganta y Tercer ojo), unidas por
# un aro y por radios. Para colorear: las flores son simples (zonas grandes), no la versión de la portada.
RADIO_INTEGRACION = 76
ORDEN_SATELITES = ("raiz", "sacro", "plexo", "corazon", "garganta", "tercer_ojo")   # horario desde arriba


def _flor_colorear(x, y, R, n, base, ancho, centro, forma, giro=0):
    """Flor simple de n pétalos con un círculo en el centro, ubicada en (x, y) y girada `giro` grados."""
    cuerpo = capa_petalos(n, base, R, ancho, forma=forma, clase="petalo-flor") + [circulo(centro)]
    return [f'<g transform="translate({_n(x)},{_n(y)}) rotate({_n(giro)})">{"".join(cuerpo)}</g>']


def integracion():
    """Siete flores (una por chakra) dentro de un aro: las de alrededor de 4 pétalos y la del centro de 8."""
    Rc, Rs, hueco = 26, 20, 7
    D = Rc + Rs + hueco                      # distancia del centro a cada flor de alrededor
    afuera = D + Rs + 3                      # círculo exterior
    e = [circulo(afuera), circulo(D, fill="none")]
    for i in range(6):                       # divisiones entre las flores, en el anillo de afuera
        e.append(linea(polar(D, 30 + 60 * i), polar(afuera, 30 + 60 * i)))
        e.append(linea((0, 0), polar(D, 60 * i)))                       # radios hacia cada flor
    e += _flor_colorear(0, 0, Rc, 8, 8, 16, 11, _FB)
    for i in range(6):
        x, y = polar(D, 60 * i)
        e += _flor_colorear(x, y, Rs, 4, 5, 20, 7, _FB, giro=60 * i)
    return documento(e, afuera)


# Dos flores para pintar de a dos ("Un momento para compartir")
RADIO_PAR = 62
RAZON_PAR = 60 / 126          # alto / ancho del dibujo


def par_de_flores():
    """Dos flores iguales, una al lado de la otra, para colorear acompañada."""
    R, sep = 29, 62
    e = _flor_colorear(-sep / 2, 0, R, 8, 8, 20, 11, _FB) + _flor_colorear(sep / 2, 0, R, 8, 8, 20, 11, _FB)
    ancho, alto = 2 * (RADIO_PAR + 1), 2 * (R + 1)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{_n(ancho)}mm" height="{_n(alto)}mm" '
            f'viewBox="{_n(-ancho / 2)} {_n(-alto / 2)} {_n(ancho)} {_n(alto)}">{"".join(e)}</svg>')


# Cuántos pétalos cuenta cada chakra (los "petalo-flor" de la integración no cuentan)
MANDALAS = {"raiz": raiz, "sacro": sacro, "plexo": plexo, "corazon": corazon,
            "garganta": garganta, "tercer_ojo": tercer_ojo, "corona": corona}
PETALOS = {"raiz": 4, "sacro": 6, "plexo": 10, "corazon": 12, "garganta": 16, "tercer_ojo": 2, "corona": 20}


# ----------------------------------------------------------------- PALETAS
# Cada chakra tiene un color protagonista y una paleta sugerida de 5 colores (el protagonista primero).
# El interior del libro es blanco y negro: los colores son solo una referencia.
PALETA = {      # colores vivos y bien distintos entre sí (ΔE ≥ 38 dentro de cada paleta, medido en CIELAB)
    "rojo": "#CD1327", "naranja": "#FF8000", "amarillo": "#FFD60A", "verde": "#17B84B",
    "azul": "#0A7BFF", "indigo": "#20139A", "violeta": "#B03AEE",
    "rosa": "#F2639F", "turquesa": "#0AC3C7", "lila": "#BFA2EB", "dorado": "#E8A200",
}
NOMBRE_COLOR = {"indigo": "índigo"}
NOMBRE_COLOR = {k: NOMBRE_COLOR.get(k, k) for k in PALETA}
PALETAS = {
    "raiz": ("rojo", "naranja", "amarillo", "rosa", "violeta"),
    "sacro": ("naranja", "rojo", "amarillo", "rosa", "violeta"),
    "plexo": ("amarillo", "naranja", "rojo", "verde", "violeta"),
    "corazon": ("verde", "rosa", "amarillo", "azul", "violeta"),
    "garganta": ("azul", "turquesa", "verde", "violeta", "rosa"),
    "tercer_ojo": ("indigo", "violeta", "azul", "rosa", "lila"),
    "corona": ("violeta", "lila", "azul", "rosa", "dorado"),
}
# Color protagonista de cada chakra (pestaña de la página y punto de color): el primero de su paleta
COLORES = {clave: PALETA[nombres[0]] for clave, nombres in PALETAS.items()}


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

# La portada se arma en formato 8,5 × 11". La composición de las flores es la original de Dani (medidas
# tomadas de portada.png, en A4), reducida y centrada; los textos se ubican por línea base (PORTADA_TEXTOS).
ESCALA_PORTADA = 0.90
_CENTRO_ORIGINAL = (104.85, 146.8)       # centro de la composición en el original (ya subido para A4)
_CENTROS_ORIGINAL = {"centro": (104.83, 154.07 - 7.0), "rojo": (105.12, 101.89 - 7.0), "naranja": (149.39, 127.43 - 7.0),
                     "amarillo": (149.32, 179.93 - 7.0), "verde": (105.20, 205.69 - 7.0), "azul": (60.17, 179.98 - 7.0),
                     "indigo": (60.24, 127.42 - 7.0)}
CENTRO_PORTADA = (ANCHO_PAGINA / 2, 147.0)
CENTROS_PORTADA = {k: (CENTRO_PORTADA[0] + ESCALA_PORTADA * (x - _CENTRO_ORIGINAL[0]),
                       CENTRO_PORTADA[1] + ESCALA_PORTADA * (y - _CENTRO_ORIGINAL[1]))
                   for k, (x, y) in _CENTROS_ORIGINAL.items()}
SATELITES = ("rojo", "naranja", "amarillo", "verde", "azul", "indigo")   # en sentido horario desde arriba
TARJETA = (15.0, 12.7, ANCHO_PAGINA - 15.0, ALTO_PAGINA - 12.7, 4.0)       # x0, y0, x1, y1, radio de las esquinas
BANDA = (15.0, 231.0, ANCHO_PAGINA - 15.0, 247.0)                          # x0, y0, x1, y1 (de borde a borde de la tarjeta)
# línea base (mm desde arriba) de cada texto de la portada
PORTADA_TEXTOS = dict(titulo=38.6, chakras=53.8, subtitulo=67.0, tagline=76.5, creado=225.0, banda=242.3, mama=259.9)
LINEA_ORO = 0.3


def _orden_petalos(n, orden):
    """Orden en que se apilan los pétalos medios (de atrás hacia adelante)."""
    if isinstance(orden, tuple):            # (inicio, sentido): apilado secuencial desde `inicio`
        inicio, sentido = orden
        return [(inicio + sentido * j) % n for j in range(n)]
    return list(range(n))


def flor(cx, cy, P, col, esc=1.0):
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
    return f'<g transform="translate({_n(cx)},{_n(cy)}) scale({_n(esc)})">' + "".join(e) + "</g>"


def portada_arte():
    """Toda la parte gráfica de la portada (sin textos): tarjeta, banda, red dorada y las 7 flores.
    Página completa en mm (8,5 × 11")."""
    x0, y0, x1, y1, rx = TARJETA
    e = [f'<rect x="{_n(x0)}" y="{_n(y0)}" width="{_n(x1 - x0)}" height="{_n(y1 - y0)}" rx="{_n(rx)}" fill="{FONDO_PORTADA}"/>']
    bx0, by0, bx1, by1 = BANDA
    e.append(f'<rect x="{_n(bx0)}" y="{_n(by0)}" width="{_n(bx1 - bx0)}" height="{_n(by1 - by0)}" fill="{BANDA_PORTADA}"/>')
    # red dorada: dos círculos, hexágono, estrella de seis puntas y rayos del centro a cada flor
    c0 = CENTRO_PORTADA
    oro = dict(fill="none", stroke=ORO_PORTADA, w=LINEA_ORO)
    e.append(circulo(61.0 * ESCALA_PORTADA, c0[0], c0[1], **oro))
    e.append(circulo(51.6 * ESCALA_PORTADA, c0[0], c0[1], **oro))
    pts = [CENTROS_PORTADA[n] for n in SATELITES]
    e.append(poligono(pts, **oro))
    e.append(poligono([pts[0], pts[2], pts[4]], **oro))
    e.append(poligono([pts[1], pts[3], pts[5]], **oro))
    for p in pts:
        e.append(linea(CENTROS_PORTADA["centro"], p, stroke=ORO_PORTADA, w=LINEA_ORO))
    # flores
    for n in SATELITES:
        e.append(flor(*CENTROS_PORTADA[n], FLOR_SAT, COLORES_FLOR[n], ESCALA_PORTADA))
    e.append(flor(*CENTROS_PORTADA["centro"], FLOR_CEN, COLORES_FLOR["centro"], ESCALA_PORTADA))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{_n(ANCHO_PAGINA)}mm" height="{_n(ALTO_PAGINA)}mm" '
            f'viewBox="0 0 {_n(ANCHO_PAGINA)} {_n(ALTO_PAGINA)}">' + "".join(e) + "</svg>")
