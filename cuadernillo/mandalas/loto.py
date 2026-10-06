"""Lotos para colorear: flor de loto vista desde arriba, con capas de pétalos
superpuestas. Las regiones visibles se calculan restando a cada capa las capas
de adelante (como un pintor que pinta de atrás hacia adelante), así que todas
quedan CERRADAS y sin superposiciones. El fondo entre las puntas de los
pétalos se cierra con un círculo, que enmarca la flor como un medallón.

Usa la misma clase base que los mandalas (verificación, números, simetría y
SVG), así que se intercambia con ellos en las sesiones:

    "mandala": {"tipo": "loto", "modo": "numerado", "nivel": "semilla"}
"""
from __future__ import annotations

import math

from shapely.geometry import Point, Polygon
from shapely.ops import polylabel, unary_union

from .generador import NIVELES, TAU, Mandala, Region

# Capas por nivel: (nombre, r0, r1, ancho relativo, desfase de medio pétalo)
CAPAS = {
    "semilla": dict(k=6, capas=[("externo", 0.30, 0.97, 1.00, True),
                                ("medio", 0.18, 0.70, 0.95, False)], centro=0.24, anillo_centro=False),
    "brote": dict(k=8, capas=[("externo", 0.32, 0.97, 1.00, True),
                              ("medio", 0.22, 0.76, 0.95, False),
                              ("interno", 0.15, 0.52, 0.85, True)], centro=0.19, anillo_centro=False),
    "flor": dict(k=10, capas=[("externo", 0.32, 0.97, 1.00, True),
                              ("medio", 0.22, 0.78, 0.95, False),
                              ("interno", 0.15, 0.56, 0.85, True)], centro=0.20, anillo_centro=True,
                 rayos=True),
}


def _bezier(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t ** 2 * (1 - t), t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0],
                    a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


def petalo(r0: float, r1: float, ancho: float, ang: float) -> Polygon:
    """Pétalo de loto (panza ancha, punta suave) que nace en r0 y llega a r1.
    ang = 0 apunta hacia arriba; crece en sentido horario."""
    L = r1 - r0
    a = [(r0, 0), (r0 + 0.12 * L, -ancho * 1.05), (r0 + 0.68 * L, -ancho * 0.95), (r1, 0)]
    b = [(r1, 0), (r0 + 0.68 * L, ancho * 0.95), (r0 + 0.12 * L, ancho * 1.05), (r0, 0)]
    pts = _bezier(*a) + _bezier(*b)[1:-1]
    # coordenadas locales: x a lo largo del radio -> giro a la dirección ang
    c, s = math.cos(ang - math.pi / 2), math.sin(ang - math.pi / 2)
    return Polygon([(x * c - y * s, x * s + y * c) for x, y in pts])


class MandalaLoto(Mandala):
    def __init__(self, nivel: str = "semilla", radio: float = 85.0, k: int | None = None,
                 semilla: int | None = None):
        self.nivel, self.semilla, self.simetrico = nivel, semilla, True
        self._radio = radio
        self.conf = dict(CAPAS[nivel])
        if k:
            self.conf["k"] = k
        self.centro = None
        self.anillos = []
        self._construir()

    @property
    def radio(self) -> float:
        return self._radio

    def _contorno(self) -> Polygon:
        return Point(0, 0).buffer(self._radio, quad_segs=128)

    def _guia_derecha(self) -> list:
        n = 360
        return [(self._radio * math.sin(math.pi * i / n), -self._radio * math.cos(math.pi * i / n))
                for i in range(n + 1)]

    def _construir(self):
        R, k = self._radio, self.conf["k"]
        paso = TAU / k
        # capas de atrás hacia adelante; el centro va último (adelante de todo)
        capas = []
        for nombre, r0, r1, ancho, desfase in self.conf["capas"]:
            # todos los pétalos nacen debajo del centro: así no quedan huecos
            # de fondo entre sus bases
            r0 = min(r0, self.conf["centro"] * 0.8)
            # medio ancho en la panza del pétalo, sin pisar a sus vecinos de capa
            r_panza = R * (r0 + 0.45 * (r1 - r0))
            w = r_panza * math.sin(math.pi / k) * ancho * 0.93
            polys = [petalo(R * r0, R * r1, w, (j + (0.5 if desfase else 0)) * paso)
                     for j in range(k)]
            capas.append((nombre, polys))
        centro = Point(0, 0).buffer(R * self.conf["centro"], quad_segs=64)
        piezas = []  # (tipo, j, polígono visible)
        cubierto = centro
        for nombre, polys in reversed(capas):
            union_capa = []
            for j, pol in enumerate(polys):
                vis = pol.difference(cubierto)
                for parte in getattr(vis, "geoms", [vis]):
                    if parte.area > 1.0:
                        piezas.append((nombre, j, parte))
                union_capa.append(pol)
            cubierto = unary_union([cubierto] + union_capa)
        # fondo: lo que queda dentro del círculo y fuera de todos los pétalos
        fondo = self._contorno().difference(cubierto)
        if self.conf.get("rayos"):
            # rayos desde la punta de cada pétalo externo hasta el borde: el
            # fondo se corta en cuñas exactas (una por espacio entre puntas)
            from shapely.geometry import MultiPolygon
            desfase = self.conf["capas"][0][4]
            partes = []
            for j in range(k):
                a0 = (j + (0.5 if desfase else 0)) * paso
                angs = [a0 + paso * t / 24 for t in range(25)]
                cuña = Polygon([(0, 0)] + [(1.2 * R * math.sin(a), -1.2 * R * math.cos(a)) for a in angs])
                pz = fondo.intersection(cuña)
                partes += [q for q in getattr(pz, "geoms", [pz]) if q.geom_type == "Polygon" and q.area > 0.5]
            fondo = MultiPolygon(partes)
        for j, parte in enumerate(sorted(getattr(fondo, "geoms", [fondo]),
                                         key=lambda p: math.atan2(p.centroid.x, -p.centroid.y))):
            piezas.append(("fondo", j, parte))
        if self.conf["anillo_centro"]:
            nucleo = Point(0, 0).buffer(R * self.conf["centro"] * 0.5, quad_segs=64)
            piezas.append(("centro", 0, centro.difference(nucleo)))
            piezas.append(("nucleo", 0, nucleo))
        else:
            piezas.append(("centro", 0, centro))

        piezas = self._absorber_astillas(piezas)
        regs = []
        for tipo, j, pol in piezas:
            pol = pol.buffer(0)
            ext = list(pol.exterior.coords)[:-1]
            huecos = [list(h.coords)[:-1] for h in pol.interiors]
            regs.append(Region(len(regs), 0, tipo, j, ext, Polygon(ext, huecos),
                               orbita=(0, tipo, 0), huecos=huecos))
        self.regiones = regs
        self._asignar_por_capa()

    def _absorber_astillas(self, piezas):
        """Las piezas demasiado chicas para pintar (entre las bases de los
        pétalos) se suman al centro, que queda como un cáliz con puntas.
        Si no tocan el centro, se suman a la vecina con más borde en común."""
        nv = NIVELES[self.nivel]
        def chica(pol):
            libre = pol.boundary.distance(polylabel(pol, 0.05)) if pol.area > 0 else 0
            return pol.area < nv["area_min_cm2"] * 100 * 1.5 or libre < nv["radio_libre_mm"]
        grandes = [list(p) for p in piezas if not chica(p[2])]
        chicas = [p for p in piezas if chica(p[2])]
        i_centro = next(i for i, p in enumerate(grandes) if p[0] == "centro")
        for tipo, j, pol in chicas:
            if pol.distance(grandes[i_centro][2]) < 0.05:
                destino = i_centro
            else:
                destino = max(range(len(grandes)),
                              key=lambda i: pol.buffer(0.05).intersection(grandes[i][2].boundary).length)
            # un leve engorde/afinado suelda las piezas que se tocan en un tramo mínimo
            unida = unary_union([grandes[destino][2], pol.buffer(0.08)]).buffer(-0.07)
            if unida.geom_type != "Polygon":
                grandes.append([tipo, j, pol])  # no se puede soldar: queda como está
                continue
            grandes[destino][2] = unida
        return [tuple(p) for p in grandes]

    def _asignar_por_capa(self):
        """Colores por capa, para que el loto pintado se vea como una flor:
        pétalos de afuera = 1, del medio = 2, internos = 3, fondo = 4..."""
        tiene_interno = any(r.tipo == "interno" for r in self.regiones)
        mapa = {"externo": 1, "medio": 2, "interno": 3, "fondo": 4,
                "centro": 1 if tiene_interno else 3, "nucleo": 4}
        for r in self.regiones:
            r.codigo = mapa[r.tipo]
        vec = self.vecinos()
        if any(self.regiones[a].codigo == self.regiones[b].codigo and
               self.regiones[a].tipo != self.regiones[b].tipo
               for a, ns in vec.items() for b in ns):
            self._asignar_codigos()  # respaldo: coloreo automático por órbitas

    def describir(self) -> dict:
        return {"tipo": "loto", "nivel": self.nivel, "k": self.conf["k"],
                "regiones": len(self.regiones),
                "capas": [c[0] for c in self.conf["capas"]]}


def generar_loto(nivel: str = "semilla", k: int | None = None, radio_mm: float = 85.0) -> MandalaLoto:
    return MandalaLoto(nivel, radio_mm, k)


if __name__ == "__main__":
    import json
    import sys
    m = generar_loto(sys.argv[1] if len(sys.argv) > 1 else "semilla")
    print(json.dumps(m.verificar(), ensure_ascii=False, indent=2))
