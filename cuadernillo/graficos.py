"""Gráficos simples en SVG para las páginas: íconos de nivel, símbolos de la
grilla de "tachar", caritas y marcas. Todo vectorial, sin imágenes."""
from __future__ import annotations

import math
import random

PT = 25.4 / 72  # mm por punto


def _svg(contenido: str, ancho_mm: float, alto_mm: float, vb: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{ancho_mm}mm" height="{alto_mm}mm" '
            f'viewBox="{vb}">{contenido}</svg>')


# --------------------------------------------------------------------------
# Íconos de nivel (semilla, brote, flor)
# --------------------------------------------------------------------------

def icono_nivel(nivel: str, color: str, fondo: str, tam_mm: float = 10) -> str:
    sw = 1.6
    if nivel == "semilla":
        c = (f'<path d="M12 3.5 C17.5 8 17.5 16 12 20.5 C6.5 16 6.5 8 12 3.5 Z" fill="{fondo}" '
             f'stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>'
             f'<path d="M12 7.5 C13.6 10.5 13.6 13.5 12 16.5" fill="none" stroke="{color}" '
             f'stroke-width="{sw}" stroke-linecap="round"/>')
    elif nivel == "brote":
        c = (f'<path d="M12 21 V11" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>'
             f'<path d="M12 14 C7.5 14 4.5 11 4.5 6.5 C9 6.5 12 9.5 12 14 Z" fill="{fondo}" '
             f'stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>'
             f'<path d="M12 11.5 C12 7 15 4 19.5 4 C19.5 8.5 16.5 11.5 12 11.5 Z" fill="{fondo}" '
             f'stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>'
             f'<path d="M7 21 H17" stroke="{color}" stroke-width="{sw}" stroke-linecap="round"/>')
    elif nivel == "flor":
        petalos = "".join(
            f'<ellipse cx="12" cy="6.6" rx="3.2" ry="4.3" transform="rotate({a} 12 12)" '
            f'fill="{fondo}" stroke="{color}" stroke-width="{sw}"/>' for a in range(0, 360, 72))
        c = petalos + f'<circle cx="12" cy="12" r="2.8" fill="{color}"/>'
    else:
        raise ValueError(nivel)
    return _svg(c, tam_mm, tam_mm, "0 0 24 24")


# --------------------------------------------------------------------------
# Símbolos para tachar
# --------------------------------------------------------------------------

def _forma(nombre: str, cx: float, cy: float, r: float) -> str:
    if nombre == "estrella":
        pts = []
        for i in range(10):
            ang = -math.pi / 2 + i * math.pi / 5
            rr = r if i % 2 == 0 else r * 0.45
            pts.append(f"{cx + rr * math.cos(ang):.2f},{cy + rr * math.sin(ang) + r * 0.08:.2f}")
        return f'<polygon points="{" ".join(pts)}"/>'
    if nombre == "circulo":
        return f'<circle cx="{cx}" cy="{cy}" r="{r * 0.82:.2f}"/>'
    if nombre == "cuadrado":
        s = r * 1.45
        return f'<rect x="{cx - s / 2:.2f}" y="{cy - s / 2:.2f}" width="{s:.2f}" height="{s:.2f}"/>'
    if nombre == "triangulo":
        h = r * 0.95
        return (f'<polygon points="{cx:.2f},{cy - h:.2f} {cx + h * 1.0:.2f},{cy + h * 0.75:.2f} '
                f'{cx - h * 1.0:.2f},{cy + h * 0.75:.2f}"/>')
    if nombre == "corazon":
        return (f'<path d="M{cx} {cy + r * 0.85} C{cx - r * 1.4} {cy - r * 0.1} {cx - r * 0.7} '
                f'{cy - r * 1.1} {cx} {cy - r * 0.35} C{cx + r * 0.7} {cy - r * 1.1} {cx + r * 1.4} '
                f'{cy - r * 0.1} {cx} {cy + r * 0.85} Z"/>')
    raise ValueError(nombre)


def grilla_tachar(bloque: dict) -> list[list[str]]:
    """Devuelve la grilla (filas x columnas) de nombres de símbolos. Siempre la
    misma para la misma semilla, con exactamente `cantidad` objetivos."""
    rng = random.Random(bloque["semilla"])
    f, c = bloque["filas"], bloque["columnas"]
    total = f * c
    pos = set(rng.sample(range(total), bloque["cantidad"]))
    celdas = []
    for i in range(total):
        celdas.append(bloque["objetivo"] if i in pos else rng.choice(bloque["distractores"]))
    return [celdas[r * c:(r + 1) * c] for r in range(f)]


def svg_grilla(grilla, celda_mm: float, color: str, trazo_pt: float = 2.0,
               marcar: str | None = None, color_marca: str = "#AD8079") -> str:
    filas, cols = len(grilla), len(grilla[0])
    sw = trazo_pt * PT
    partes = [f'<g fill="none" stroke="{color}" stroke-width="{sw:.3f}" stroke-linejoin="round">']
    marcas = []
    for r, fila in enumerate(grilla):
        for c, nombre in enumerate(fila):
            cx, cy = (c + 0.5) * celda_mm, (r + 0.5) * celda_mm
            partes.append(_forma(nombre, cx, cy, celda_mm * 0.34))
            if marcar and nombre == marcar:
                marcas.append(f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{celda_mm * 0.47:.2f}" '
                              f'fill="none" stroke="{color_marca}" stroke-width="{sw * 1.1:.3f}"/>')
    partes.append("</g>")
    partes += marcas
    return _svg("".join(partes), cols * celda_mm, filas * celda_mm,
                f"0 0 {cols * celda_mm} {filas * celda_mm}")


def svg_simbolo_tachado(nombre: str, tam_mm: float, color: str, color_cruz: str) -> str:
    sw = 2.0 * PT
    m = tam_mm * 0.12
    c = (f'<g fill="none" stroke="{color}" stroke-width="{sw:.3f}" stroke-linejoin="round">'
         f'{_forma(nombre, tam_mm / 2, tam_mm / 2, tam_mm * 0.34)}</g>'
         f'<path d="M{m} {m} L{tam_mm - m} {tam_mm - m} M{tam_mm - m} {m} L{m} {tam_mm - m}" '
         f'stroke="{color_cruz}" stroke-width="{sw * 1.4:.3f}" stroke-linecap="round"/>')
    return _svg(c, tam_mm, tam_mm, f"0 0 {tam_mm} {tam_mm}")


# --------------------------------------------------------------------------
# Caritas "¿Cómo me sentí hoy?"
# --------------------------------------------------------------------------

def carita(tipo: str, color: str, tam_mm: float = 16) -> str:
    boca = {
        "bien": "M13 24 Q20 31 27 24",
        "regular": "M13.5 26 L26.5 26",
        "costo": "M13.5 28 Q20 22.5 26.5 28",
    }[tipo]
    c = (f'<circle cx="20" cy="20" r="17.5" fill="none" stroke="{color}" stroke-width="2"/>'
         f'<circle cx="14" cy="16" r="2.1" fill="{color}"/>'
         f'<circle cx="26" cy="16" r="2.1" fill="{color}"/>'
         f'<path d="{boca}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>')
    return _svg(c, tam_mm, tam_mm, "0 0 40 40")


def adorno(color: str, ancho_mm: float = 40) -> str:
    """Filete con un pequeño rombo central, para separar en la portada."""
    a = ancho_mm
    c = (f'<path d="M0 3 H{a / 2 - 4} M{a / 2 + 4} 3 H{a}" stroke="{color}" stroke-width="0.5"/>'
         f'<path d="M{a / 2} 0.6 L{a / 2 + 2.4} 3 L{a / 2} 5.4 L{a / 2 - 2.4} 3 Z" fill="{color}"/>')
    return _svg(c, a, 6, f"0 0 {a} 6")


# --------------------------------------------------------------------------
# Íconos de ejercicio (trazo blanco sobre un círculo rosa ceniza)
# --------------------------------------------------------------------------

_ICONOS = {
    # lupa
    "tachar": '<circle cx="10.5" cy="10.5" r="5"/><path d="M14.3 14.3 L18.5 18.5"/>',
    # libro abierto
    "palabras": '<path d="M12 7.5 C10 6 7.5 5.8 5 6.3 V17 C7.5 16.5 10 16.8 12 18.2 C14 16.8 16.5 16.5 19 17 V6.3 '
                'C16.5 5.8 14 6 12 7.5 Z M12 7.5 V18"/>',
    # lamparita
    "series": '<path d="M9.3 15.2 C7.7 14 6.8 12.3 6.8 10.4 A5.2 5.2 0 0 1 17.2 10.4 C17.2 12.3 16.3 14 14.7 15.2 '
              'V16.6 H9.3 Z"/><path d="M9.8 19 H14.2"/>',
    # globos de diálogo
    "conversar": '<path d="M5 6.5 H15 V13.5 H9.5 L6.5 16 V13.5 H5 Z"/><path d="M17 9.5 H19 V15.5 H17.5 V17.5 L15 15.5 H11"/>',
    # lápiz
    "fluidez": '<path d="M6 18 L7 14 L15.5 5.5 L18.5 8.5 L10 17 Z"/><path d="M13.5 7.5 L16.5 10.5"/>',
    # canasta
    "agrupar": '<path d="M4.5 10 H19.5 L17.8 18 H6.2 Z"/><path d="M8 10 L11 5.5 M16 10 L13 5.5"/>'
               '<path d="M9.5 12.5 V15.5 M12 12.5 V15.5 M14.5 12.5 V15.5"/>',
    # lista numerada
    "ordenar": '<path d="M10 7 H19 M10 12 H19 M10 17 H19"/><circle cx="6" cy="7" r="1.2"/>'
               '<circle cx="6" cy="12" r="1.2"/><circle cx="6" cy="17" r="1.2"/>',
}


def icono_ejercicio(tipo: str, fondo: str, tam_mm: float = 9) -> str:
    trazo = _ICONOS.get(tipo, '<circle cx="12" cy="12" r="3"/>')
    c = (f'<circle cx="12" cy="12" r="12" fill="{fondo}"/>'
         f'<g fill="none" stroke="#FFFFFF" stroke-width="1.7" stroke-linecap="round" '
         f'stroke-linejoin="round">{trazo}</g>')
    return _svg(c, tam_mm, tam_mm, "0 0 24 24")


def esquinero(color: str, tam_mm: float = 14) -> str:
    """Adorno de esquina para el marco de la portada (se rota con CSS)."""
    c = (f'<path d="M1 23 V9 Q1 1 9 1 H23" fill="none" stroke="{color}" stroke-width="0.9"/>'
         f'<path d="M5 23 V11 Q5 5 11 5 H23" fill="none" stroke="{color}" stroke-width="0.5"/>'
         f'<circle cx="9.5" cy="9.5" r="1.6" fill="{color}"/>')
    return _svg(c, tam_mm, tam_mm, "0 0 24 24")


# --------------------------------------------------------------------------
# Lotos de los chakras (vista superior), para portadas
# --------------------------------------------------------------------------

def _mezcla(hex_color: str, blanco: float) -> str:
    """Aclara un color mezclándolo con blanco (0 = igual, 1 = blanco)."""
    r, g_, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    m = lambda c: round(c + (255 - c) * blanco)
    return f"#{m(r):02X}{m(g_):02X}{m(b):02X}"


def _petalo(r0: float, r1: float, ancho: float, ang: float) -> str:
    """Pétalo de loto: panza ancha y redonda, punta suave en r1."""
    L = r1 - r0
    pts = [(r0, 0), (r0 + 0.15 * L, -ancho * 1.05), (r0 + 0.7 * L, -ancho * 0.95), (r1, 0),
           (r0 + 0.7 * L, ancho * 0.95), (r0 + 0.15 * L, ancho * 1.05)]
    c, s = math.cos(ang), math.sin(ang)
    P = [(x * c - y * s, x * s + y * c) for x, y in pts]
    f = lambda p: f"{p[0]:.2f} {p[1]:.2f}"
    return (f"M{f(P[0])} C{f(P[1])} {f(P[2])} {f(P[3])} "
            f"C{f(P[4])} {f(P[5])} {f(P[0])} Z")


def loto(color: str, diametro_mm: float, k: int = 8) -> str:
    """Flor de loto vista desde arriba: pétalos de fondo, pétalos de frente
    con una línea interior y un centro redondo. Trazo en el tono oscuro."""
    R = 50.0
    oscuro, medio, claro, palido = color, _mezcla(color, 0.35), _mezcla(color, 0.6), _mezcla(color, 0.82)
    sw = 1.6
    partes = []
    paso = TAU_ / k
    for j in range(k):  # fondo, más largos, intercalados
        partes.append(f'<path d="{_petalo(10, R - 1, 70 / k + 5, (j + 0.5) * paso - math.pi / 2)}" '
                      f'fill="{claro}" stroke="{oscuro}" stroke-width="{sw}" stroke-linejoin="round"/>')
    for j in range(k):  # frente
        a = j * paso - math.pi / 2
        partes.append(f'<path d="{_petalo(9, R * 0.8, 70 / k + 5.5, a)}" fill="{medio}" '
                      f'stroke="{oscuro}" stroke-width="{sw}" stroke-linejoin="round"/>')
        partes.append(f'<path d="{_petalo(17, R * 0.64, 70 / k * 0.45 + 1.5, a)}" fill="{palido}" '
                      f'stroke="{oscuro}" stroke-width="{sw * 0.75}" stroke-linejoin="round"/>')
    partes.append(f'<circle r="15" fill="{palido}" stroke="{oscuro}" stroke-width="{sw}"/>')
    partes.append(f'<circle r="9" fill="{medio}" stroke="{oscuro}" stroke-width="{sw * 0.8}"/>')
    partes.append(f'<circle r="3.2" fill="{oscuro}"/>')
    return _svg("".join(partes), diametro_mm, diametro_mm, f"{-R} {-R} {2 * R} {2 * R}")


TAU_ = 2 * math.pi
