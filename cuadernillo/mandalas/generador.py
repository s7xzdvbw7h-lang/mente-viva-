"""Generador paramétrico de mandalas vectoriales (SVG) para Mente Viva.

Idea central
------------
Un mandala es una partición exacta de un disco en regiones CERRADAS.
Se arma con *bordes* (curvas cerradas r = f(φ)) que separan *anillos*, y cada
anillo se divide en sectores o pétalos. Todo se calcula en un sistema
(φ, t): φ es el ángulo medido desde arriba en sentido horario y t ∈ [0, 1]
recorre el anillo de su borde interior a su borde exterior. Como las regiones
de un anillo cubren el rectángulo (φ, t) sin huecos ni superposiciones, el
resultado es siempre una partición: ninguna región queda abierta.

Cada región guarda su polígono (en mm, centro en 0,0), su área, su centroide
y el punto donde conviene escribir su número. Con eso se puede:

  a) numerar regiones para colorear por código   -> Mandala.svg("numerado")
  b) borrar la mitad derecha para completar       -> Mandala.svg("simetria")
  c) exportar la versión completa libre           -> Mandala.svg("libre")

Todos los estilos disponibles son simétricos respecto del eje vertical
(salvo "remolino", que solo se usa si se pide simetria=False), así que la
mitad izquierda alcanza para reconstruir la derecha.

Uso rápido:

    from mandalas.generador import generar
    m = generar(nivel="semilla", semilla=7)
    open("m.svg", "w").write(m.svg("numerado"))
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

from shapely.geometry import LineString, LinearRing, Point, Polygon, box
from shapely.ops import polylabel, unary_union

TAU = 2 * math.pi
MM_POR_PT = 25.4 / 72

NIVELES = {
    # regiones permitidas, área mínima (cm²), radio libre para el número (mm),
    # cantidades de pétalos posibles y cantidad de anillos (sin contar el centro)
    "semilla": dict(regiones=(12, 24), area_min_cm2=1.0, radio_libre_mm=5.0,
                    petalos=(6, 8), anillos=(2, 3), grosor_min_mm=13.0),
    "brote": dict(regiones=(25, 40), area_min_cm2=0.8, radio_libre_mm=4.5,
                  petalos=(8, 10), anillos=(3, 4), grosor_min_mm=10.0),
    "flor": dict(regiones=(40, 60), area_min_cm2=0.5, radio_libre_mm=4.0,
                 petalos=(8, 10, 12), anillos=(4, 5), grosor_min_mm=8.0),
}


# --------------------------------------------------------------------------
# Geometría básica
# --------------------------------------------------------------------------

@dataclass
class Borde:
    """Curva cerrada r = f(φ). Todas las variantes son pares si la fase es
    múltiplo de π/k, o sea simétricas respecto del eje vertical."""
    base: float
    estilo: str = "circulo"  # circulo | feston | ojival | onda
    k: int = 1
    fase: float = 0.0
    amplitud: float = 0.0

    def perfil(self, phi: float) -> float:
        """Valor entre 0 y 1 que modula la amplitud."""
        x = self.k * (phi - self.fase) / 2
        if self.estilo == "feston":      # arcos redondeados, puntas hacia adentro
            return abs(math.cos(x))
        if self.estilo == "ojival":      # pétalos en punta (tipo loto)
            return 1 - abs(math.sin(x))
        if self.estilo == "onda":        # ondulación suave
            return 0.5 + 0.5 * math.cos(2 * x)
        return 0.0

    def r(self, phi: float) -> float:
        if self.estilo == "circulo":
            return self.base
        return self.base + self.amplitud * self.perfil(phi)

    @property
    def r_max(self) -> float:
        return self.base + (self.amplitud if self.estilo != "circulo" else 0)


@dataclass
class Anillo:
    """Zona entre dos bordes, dividida en k sectores ("radial"/"remolino") o en
    k pétalos con k huecos entre ellos ("petalos")."""
    interior: Borde
    exterior: Borde
    division: str = "radial"  # radial | petalos | remolino | entero
    k: int = 8
    fase: float = 0.0
    ancho_petalo: float = 0.72   # fracción del medio sector que ocupa el pétalo
    punta_petalo: float = 0.18   # ancho del pétalo en sus extremos (fracción)
    giro: float = 0.5            # solo remolino: fracción de sector que gira
    alterna: int = 1             # 2 = sectores alternados en dos grupos de color
    forma_petalo: str = "lente"  # lente | gota (punta afuera) | hoja (dos puntas)
    petalo_interior: float = 0.0 # >0: dibuja un pétalo más chico dentro de cada pétalo

    def punto(self, phi: float, t: float) -> tuple[float, float]:
        ri, re = self.interior.r(phi), self.exterior.r(phi)
        r = ri + t * (re - ri)
        return (r * math.sin(phi), -r * math.cos(phi))

    def _w(self, t: float) -> float:
        """Medio ancho angular del pétalo a la altura t."""
        medio = math.pi / self.k
        if self.forma_petalo == "gota":     # base redonda, punta hacia afuera
            s, p = math.sin(math.pi * t ** 0.62), 0.06
        elif self.forma_petalo == "hoja":   # esbelta, en punta a los dos lados
            s, p = math.sin(math.pi * t) ** 1.3, 0.06
        else:                               # lente
            s, p = math.sin(math.pi * t) ** 0.85, self.punta_petalo
        return medio * (p + (self.ancho_petalo - p) * s)

    def lente_interior(self, c: float, t0=0.2, t1=0.84):
        """Contorno de un pétalo más chico, centrado en el ángulo c."""
        f = self.petalo_interior
        if self.forma_petalo == "gota":
            t0, t1 = 0.1, 0.72

        def w_in(t):
            u = (t - t0) / (t1 - t0)
            return f * self._w(t) * math.sin(math.pi * u) ** 0.75
        ts = _muestras(t0, t1, 1 / 80)
        pts = [self.punto(c + w_in(t), t) for t in ts]
        pts += [self.punto(c - w_in(t), t) for t in reversed(ts[1:-1])]
        return pts

    def particiones(self):
        """Devuelve (tipo, j, izquierda(t), derecha(t)) para cada región."""
        paso = TAU / self.k
        out = []
        if self.division == "entero":
            out.append(("anillo", 0, lambda t: self.fase - math.pi, lambda t: self.fase + math.pi))
            return out
        for j in range(self.k):
            c = self.fase + j * paso
            if self.division == "radial":
                out.append(("sector", j, (lambda c: lambda t: c - paso / 2)(c),
                            (lambda c: lambda t: c + paso / 2)(c)))
            elif self.division == "remolino":
                g = self.giro * paso
                out.append(("sector", j, (lambda c: lambda t: c - paso / 2 + g * t)(c),
                            (lambda c: lambda t: c + paso / 2 + g * t)(c)))
            elif self.division == "petalos":
                out.append(("petalo", j, (lambda c: lambda t: c - self._w(t))(c),
                            (lambda c: lambda t: c + self._w(t))(c)))
                out.append(("hueco", j, (lambda c: lambda t: c + self._w(t))(c),
                            (lambda c: lambda t: c + paso - self._w(t))(c)))
            else:
                raise ValueError(f"división desconocida: {self.division}")
        return out


@dataclass
class Region:
    id: int
    anillo: int
    tipo: str
    j: int
    puntos: list
    poligono: Polygon = field(repr=False)
    orbita: tuple = ()
    codigo: int = 0          # color para pintar por número (1..4)
    huecos: list = field(default_factory=list)  # contornos interiores (pétalo dentro de pétalo)

    @property
    def area_mm2(self) -> float:
        return self.poligono.area

    @property
    def area_cm2(self) -> float:
        return self.poligono.area / 100

    @property
    def centroide(self) -> tuple[float, float]:
        c = self.poligono.centroid
        return (c.x, c.y)

    def punto_numero(self, radio_necesario: float) -> tuple[float, float, float]:
        """Lugar para el número: el centroide si cae holgado adentro de la
        región; si no (formas cóncavas), el polo de inaccesibilidad.
        Devuelve (x, y, radio libre)."""
        c = self.poligono.centroid
        libre_c = self.poligono.boundary.distance(c) if self.poligono.contains(c) else 0
        if libre_c >= radio_necesario:
            return (c.x, c.y, libre_c)
        p = polylabel(self.poligono, tolerance=0.05)
        return (p.x, p.y, self.poligono.boundary.distance(p))


def _muestras(a: float, b: float, paso: float) -> list[float]:
    n = max(2, int(math.ceil(abs(b - a) / paso)) + 1)
    return [a + (b - a) * i / (n - 1) for i in range(n)]


def _muestras_t(n: int = 140) -> list[float]:
    """t de 0 a 1, más denso cerca de los extremos (donde las puntas de los
    pétalos cambian rápido de ancho)."""
    return [(1 - math.cos(math.pi * i / n)) / 2 for i in range(n + 1)]


def _poligono_region(an: Anillo, izq, der, res_ang=TAU / 900):
    ts = _muestras_t()
    pts = []
    for phi in _muestras(izq(0), der(0), res_ang):          # borde interior
        pts.append(an.punto(phi, 0))
    for t in ts[1:]:                                        # lado derecho
        pts.append(an.punto(der(t), t))
    for phi in _muestras(der(1), izq(1), res_ang)[1:]:      # borde exterior
        pts.append(an.punto(phi, 1))
    for t in reversed(ts[1:-1]):                            # lado izquierdo
        pts.append(an.punto(izq(t), t))
    limpio = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, limpio[-1]) > 1e-6:
            limpio.append(p)
    return limpio


def _poligono_borde(b: Borde, res_ang=TAU / 900):
    return [(b.r(f) * math.sin(f), -b.r(f) * math.cos(f))
            for f in _muestras(-math.pi, math.pi, res_ang)[:-1]]


# --------------------------------------------------------------------------
# Mandala
# --------------------------------------------------------------------------

@dataclass
class Mandala:
    centro: Borde
    anillos: list[Anillo]
    nivel: str
    semilla: int | None = None
    simetrico: bool = True
    regiones: list[Region] = field(default_factory=list)

    def __post_init__(self):
        self._construir()

    @property
    def radio(self) -> float:
        return self.anillos[-1].exterior.r_max if self.anillos else self.centro.r_max

    def _construir(self):
        regs = []
        pts = _poligono_borde(self.centro)
        regs.append(Region(0, 0, "centro", 0, pts, Polygon(pts), orbita=(0, "centro", 0)))
        for i, an in enumerate(self.anillos, start=1):
            for tipo, j, izq, der in an.particiones():
                pts = _poligono_region(an, izq, der)
                if not Polygon(pts).is_valid:
                    raise RuntimeError("región con bordes cruzados")
                grupo = j % an.alterna if tipo == "sector" else 0
                huecos = []
                if tipo == "petalo" and an.petalo_interior > 0:
                    huecos = [an.lente_interior(an.fase + j * TAU / an.k)]
                    lente = Polygon(huecos[0])
                    if not (lente.is_valid and Polygon(pts).buffer(-1.0).contains(lente)):
                        raise RuntimeError("el pétalo interior toca el borde del pétalo")
                regs.append(Region(len(regs), i, tipo, j, pts, Polygon(pts, huecos),
                                   orbita=(i, tipo, grupo), huecos=huecos))
                for h in huecos:
                    regs.append(Region(len(regs), i, "petalo_interior", j, h, Polygon(h),
                                       orbita=(i, "petalo_interior", 0)))
        self.regiones = regs
        self._asignar_codigos()

    # ---- colores por número ------------------------------------------------
    def vecinos(self) -> dict[int, set[int]]:
        """Regiones que comparten un tramo de borde (no solo un punto)."""
        if hasattr(self, "_vecinos"):
            return self._vecinos
        v = {r.id: set() for r in self.regiones}
        for a in self.regiones:
            for b in self.regiones:
                if b.id <= a.id or abs(a.anillo - b.anillo) > 1:
                    continue
                if a.poligono.distance(b.poligono) > 0.05:
                    continue
                comun = a.poligono.boundary.buffer(0.05).intersection(b.poligono.boundary)
                if comun.length > 1.0:
                    v[a.id].add(b.id)
                    v[b.id].add(a.id)
        self._vecinos = v
        return v

    def _asignar_codigos(self, colores=4):
        """Colorea por órbitas (todas las regiones equivalentes por rotación
        llevan el mismo número) de forma que órbitas vecinas no compartan
        color. Se procesa de adentro hacia afuera; cada órbita tiene a lo sumo
        3 órbitas vecinas ya coloreadas, así que 4 colores siempre alcanzan."""
        vec = self.vecinos()
        orbitas = []
        for r in self.regiones:
            if r.orbita not in orbitas:
                orbitas.append(r.orbita)
        de_orbita = {o: [r for r in self.regiones if r.orbita == o] for o in orbitas}
        uso = {c: 0 for c in range(1, colores + 1)}
        codigo_orbita = {}
        rng = random.Random(self.semilla)
        for o in orbitas:
            prohibidos = set()
            for r in de_orbita[o]:
                for n in vec[r.id]:
                    otro = self.regiones[n].orbita
                    if otro != o and otro in codigo_orbita:
                        prohibidos.add(codigo_orbita[otro])
            libres = [c for c in uso if c not in prohibidos]
            if not libres:
                raise RuntimeError("no alcanzan 4 colores para este diseño")
            menor = min(uso[c] for c in libres)
            elegido = rng.choice([c for c in libres if uso[c] == menor])
            codigo_orbita[o] = elegido
            uso[elegido] += 1
        for r in self.regiones:
            r.codigo = codigo_orbita[r.orbita]

    # ---- verificación -------------------------------------------------------
    def verificar(self, radio_numero_mm: float | None = None) -> dict:
        nv = NIVELES[self.nivel]
        radio_numero_mm = radio_numero_mm or nv["radio_libre_mm"]
        contorno = Polygon(_poligono_borde(self.anillos[-1].exterior))
        union = unary_union([r.poligono for r in self.regiones])
        suma = sum(r.area_mm2 for r in self.regiones)
        cerradas = all(r.poligono.is_valid and r.poligono.area > 0 and
                       all(LinearRing(c).is_ring for c in [r.puntos] + r.huecos)
                       for r in self.regiones)
        libres = [r.punto_numero(radio_numero_mm)[2] for r in self.regiones]
        res = {
            "regiones": len(self.regiones),
            "rango_nivel": nv["regiones"],
            "en_rango": nv["regiones"][0] <= len(self.regiones) <= nv["regiones"][1],
            "todas_cerradas": cerradas,
            "particion_sin_huecos": abs(union.area - contorno.area) / contorno.area < 0.002,
            "sin_superposiciones": abs(suma - union.area) / union.area < 0.002,
            "area_min_cm2": round(min(r.area_cm2 for r in self.regiones), 2),
            "area_ok": min(r.area_cm2 for r in self.regiones) >= nv["area_min_cm2"],
            "radio_libre_min_mm": round(min(libres), 2),
            "numeros_entran": min(libres) >= radio_numero_mm,
            "colores_vecinos_distintos": all(
                self.regiones[a].codigo != self.regiones[b].codigo or
                self.regiones[a].orbita == self.regiones[b].orbita
                for a, ns in self.vecinos().items() for b in ns),
            "diametro_mm": round(2 * self.radio, 2),
        }
        if self.simetrico:
            res["simetria_espejo"] = self._es_simetrico()
        res["ok"] = all(v for k, v in res.items() if isinstance(v, bool))
        return res

    def _es_simetrico(self, tol=0.01) -> bool:
        from shapely.affinity import scale
        for r in self.regiones:
            espejo = scale(r.poligono, xfact=-1, yfact=1, origin=(0, 0))
            if not any(espejo.symmetric_difference(s.poligono).area < tol * r.area_mm2
                       for s in self.regiones if s.anillo == r.anillo):
                return False
        return True

    # ---- SVG ---------------------------------------------------------------
    def numeros(self, radio_numero_mm: float | None = None):
        """[(x, y, código)] en mm, con origen en el centro del mandala."""
        rn = radio_numero_mm or NIVELES[self.nivel]["radio_libre_mm"]
        return [(*r.punto_numero(rn)[:2], r.codigo) for r in self.regiones]

    def svg(self, modo="libre", diametro_mm=170.0, trazo_pt=2.0, color_trazo="#000000",
            rellenos: dict | None = None, guia_punteada=True) -> str:
        """modo: "libre" (contornos), "numerado" (contornos, los números se
        superponen aparte), "color" (rellenos según `rellenos` {código: hex}),
        "simetria" (solo mitad izquierda, eje y borde derecho punteados).
        El SVG mide exactamente `diametro_mm` + el grosor del trazo."""
        esc = diametro_mm / (2 * self.radio)
        tr = trazo_pt * MM_POR_PT / esc            # grosor en unidades internas
        m = self.radio + tr
        lado = 2 * m * esc
        cab = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{lado:.3f}mm" '
               f'height="{lado:.3f}mm" viewBox="{-m:.3f} {-m:.3f} {2*m:.3f} {2*m:.3f}">')
        estilo = (f'fill="none" stroke="{color_trazo}" stroke-width="{tr:.4f}" '
                  f'stroke-linejoin="round" stroke-linecap="round"')
        partes = [cab]

        def d_poli(pts, cerrar=True):
            s = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts)
            return s + (" Z" if cerrar else "")

        if modo in ("libre", "numerado", "color"):
            for r in self.regiones:
                relleno = "none"
                if modo == "color" and rellenos:
                    relleno = rellenos[r.codigo] if isinstance(rellenos, dict) else rellenos(r)
                d = " ".join(d_poli(c) for c in [r.puntos] + r.huecos)
                partes.append(f'<path d="{d}" fill="{relleno}" fill-rule="evenodd" '
                              f'stroke="{color_trazo}" stroke-width="{tr:.4f}" '
                              f'stroke-linejoin="round"/>')
        elif modo == "simetria":
            medio = box(-m - 1, -m - 1, 0, m + 1)
            trazos = []
            for r in self.regiones:
                for anillo_pts in [r.puntos] + r.huecos:
                    corte = LineString(anillo_pts + [anillo_pts[0]]).intersection(medio)
                    for g in getattr(corte, "geoms", [corte]):
                        if g.geom_type == "LineString" and g.length > 0.01:
                            # descarta tramos que corren sobre el propio eje
                            if all(abs(x) < 1e-6 for x, _ in g.coords):
                                continue
                            trazos.append(list(g.coords))
            partes.append(f'<g {estilo}>')
            for t in trazos:
                partes.append(f'<path d="{d_poli(t, cerrar=False)}"/>')
            partes.append('</g>')
            eje = tr * 0.75
            partes.append(f'<line x1="0" y1="{-self.radio:.2f}" x2="0" y2="{self.radio:.2f}" '
                          f'stroke="{color_trazo}" stroke-width="{eje:.4f}" '
                          f'stroke-dasharray="{6*eje:.3f} {4*eje:.3f}"/>')
            if guia_punteada:
                ext = self.anillos[-1].exterior
                pts = [(ext.r(f) * math.sin(f), -ext.r(f) * math.cos(f))
                       for f in _muestras(0, math.pi, TAU / 900)]
                partes.append(f'<path d="{d_poli(pts, cerrar=False)}" fill="none" '
                              f'stroke="{color_trazo}" stroke-width="{eje:.4f}" '
                              f'stroke-linecap="round" stroke-dasharray="0 {4*eje:.3f}"/>')
        else:
            raise ValueError(f"modo desconocido: {modo}")
        partes.append("</svg>")
        return "\n".join(partes)

    def describir(self) -> dict:
        return {
            "nivel": self.nivel, "semilla": self.semilla, "regiones": len(self.regiones),
            "centro": vars(self.centro),
            "anillos": [{"division": a.division, "k": a.k, "fase": round(a.fase, 4),
                         "forma_petalo": a.forma_petalo, "petalo_interior": a.petalo_interior,
                         "borde_exterior": vars(a.exterior)} for a in self.anillos],
        }


# --------------------------------------------------------------------------
# Diseño aleatorio paramétrico
# --------------------------------------------------------------------------

def _disenio(rng: random.Random, nivel: str, radio: float, petalos: int | None,
             anillos: int | None, simetria: bool) -> Mandala:
    nv = NIVELES[nivel]
    k = petalos or rng.choice(nv["petalos"])
    n = anillos or rng.randint(*nv["anillos"])
    divisiones = ["radial", "petalos"] + ([] if simetria else ["remolino"])
    # bordes curvos más probables que el círculo: dan aspecto de pétalo
    estilos_borde = ["feston"] * 4 + ["ojival"] * 4 + ["onda"] * 2 + ["circulo"]
    estilos_exterior = ["feston", "ojival", "circulo", "circulo"]

    r_centro = radio * rng.uniform(0.16, 0.24)
    centro = Borde(r_centro, rng.choice(["circulo", "feston", "ojival"]), k=k, fase=0.0,
                   amplitud=r_centro * rng.uniform(0.15, 0.3))
    centro.base = r_centro - centro.amplitud * (centro.estilo != "circulo")

    # radios base de cada borde exterior, con algo de variación
    pesos = [rng.uniform(0.85, 1.25) for _ in range(n)]
    tramo = radio - r_centro
    acumulado, bases = 0.0, []
    for p in pesos:
        acumulado += p
        bases.append(r_centro + tramo * acumulado / sum(pesos))

    anillos_l = []
    interior = centro
    fase = 0.0
    for i in range(n):
        ultimo = i == n - 1
        ki = k
        if nivel != "semilla" and i >= 1 and rng.random() < 0.35:
            ki = 2 * k
        division = rng.choice(divisiones)
        if i > 0 and rng.random() < 0.6:
            fase = fase + math.pi / ki            # pétalos en tresbolillo
        fase = (fase % (TAU / ki))
        if simetria:  # fase múltiplo de π/k -> simétrico respecto del eje
            fase = round(fase / (math.pi / ki)) * (math.pi / ki)
        estilo = rng.choice(estilos_exterior if ultimo else estilos_borde)
        if ultimo:
            amp = radio * rng.uniform(0.05, 0.1) if estilo != "circulo" else 0
            base = radio - amp
        else:
            amp = (bases[i] - interior.r_max) * rng.uniform(0.25, 0.45) if estilo != "circulo" else 0
            base = bases[i] - amp * 0.5
        exterior = Borde(base, estilo, k=ki, fase=fase, amplitud=amp)
        alterna = 2 if (division == "radial" and ki % 2 == 0 and rng.random() < 0.5) else 1
        forma = rng.choice(["lente", "gota", "gota", "hoja"])
        interior_p = rng.uniform(0.45, 0.58) if (division == "petalos" and rng.random() < 0.55) else 0.0
        anillos_l.append(Anillo(interior, exterior, division, ki, fase,
                                ancho_petalo=rng.uniform(0.74, 0.9),
                                punta_petalo=rng.uniform(0.12, 0.22),
                                giro=rng.uniform(0.3, 0.6), alterna=alterna,
                                forma_petalo=forma, petalo_interior=interior_p))
        interior = exterior
    return centro, anillos_l


def _cantidad_regiones(anillos: list[Anillo]) -> int:
    n = 1
    for an in anillos:
        if an.division == "petalos":
            n += an.k * (3 if an.petalo_interior > 0 else 2)
        elif an.division == "entero":
            n += 1
        else:
            n += an.k
    return n


def _grosor_minimo(anillos: list[Anillo]) -> float:
    g = float("inf")
    for an in anillos:
        for f in _muestras(0, TAU, TAU / 720):
            g = min(g, an.exterior.r(f) - an.interior.r(f))
    return g


def generar(nivel: str = "semilla", semilla: int = 1, petalos: int | None = None,
            anillos: int | None = None, simetria: bool = True,
            radio_mm: float = 85.0, intentos: int = 400) -> Mandala:
    """Genera un mandala que cumple las reglas del nivel. Con la misma
    semilla siempre sale el mismo diseño."""
    nv = NIVELES[nivel]
    rng = random.Random(f"{nivel}-{semilla}")
    for _ in range(intentos):
        centro, anillos_l = _disenio(rng, nivel, radio_mm, petalos, anillos, simetria)
        # filtros baratos antes de construir la geometría
        if not (nv["regiones"][0] <= _cantidad_regiones(anillos_l) <= nv["regiones"][1]):
            continue
        if _grosor_minimo(anillos_l) < nv["grosor_min_mm"]:
            continue
        try:
            m = Mandala(centro, anillos_l, nivel, semilla=semilla, simetrico=simetria)
        except (RuntimeError, ValueError):
            continue
        except Exception as e:  # geometría degenerada (GEOS): se descarta el intento
            if "Topology" not in type(e).__name__ + str(e):
                raise
            continue
        try:
            if m.verificar()["ok"]:
                return m
        except Exception as e:
            if "Topology" not in type(e).__name__ + str(e):
                raise
    raise RuntimeError(f"no se encontró un mandala válido para {nivel}/{semilla}")


if __name__ == "__main__":
    import json
    import sys
    nivel = sys.argv[1] if len(sys.argv) > 1 else "semilla"
    sem = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    m = generar(nivel, sem)
    print(json.dumps(m.verificar(), ensure_ascii=False, indent=2))
