"""Ejemplos pintados ("Así podría quedar"): el mismo dibujo del mandala, pero con colores.

Cada ejemplo se dibuja directamente en vector con las funciones de mandalas.py, pasándoles qué color
lleva cada parte (así las líneas y las zonas coinciden exactamente con el mandala para colorear).

Reglas del ejemplo (las controla verificar.py):
  - solo los 5 colores de la paleta del chakra, planos (sin degradé ni sombra);
  - el color protagonista (el primero de la paleta) ocupa entre el 60 % y el 70 % de lo pintado;
  - se usan los 5 colores;
  - es simétrico: cada parte repetida lleva el mismo color o alterna siempre igual.
"""
import io
import re

import numpy as np
from PIL import Image

import mandalas as M

PROTAGONISTA_MIN, PROTAGONISTA_MAX = 0.60, 0.70

# Qué color de la paleta (0 = protagonista) lleva cada parte. Una lista alterna los colores
# entre pétalos (o entre cuñas) en orden alrededor del centro.
ESQUEMAS = {
    "raiz":       dict(borde=0, fondo=0, piedra=3, petalos=[1, 2], cuadrado=4, punto=0),
    "sacro":      dict(borde=0, fondo=3, cunas=2, gotas=4, petalos=0, disco=2, luna=1),
    "plexo":      dict(borde=0, fondo=1, cunas=3, petalos=0, disco=2, triangulo=4),
    "corazon":    dict(borde=0, fondo=0, petalos=[1, 2, 1, 3], estrella=4),
    "garganta":   dict(banda=0, fondo=0, petalos=[1, 2, 1, 3], disco=0, centro=4),
    "tercer_ojo": dict(borde=0, fondo=0, interior=2, alas=3, disco=1, pupila=4),
    "corona":     dict(borde=0, fondo=0, grandes=[3, 2], medios=1, internos=4, disco=1),
}


def colores_de(clave):
    """Los 5 colores (hex) de la paleta del chakra, el protagonista primero."""
    return [M.PALETA[n] for n in M.PALETAS[clave]]


def esquema(clave):
    """{parte: hex o lista de hex} listo para pasarle a la función del mandala."""
    hexes = colores_de(clave)
    return {rol: ([hexes[i] for i in v] if isinstance(v, list) else hexes[v])
            for rol, v in ESQUEMAS[clave].items()}


def ejemplo(clave):
    """SVG del mandala de `clave` pintado con su paleta."""
    return M.MANDALAS[clave](esquema(clave))


CREMA = "#F7F0E3"       # fondo del ejemplo de "Todos juntos" (la tarjeta crema de la portada)


def esquema_integracion():
    """Cada flor lleva el color de su chakra (en el orden de la portada) y los centros son dorados."""
    p = M.PALETA
    return dict(fondo=CREMA, corona=p["violeta"], centros=p["dorado"],
                satelites=[p[n] for n in ("rojo", "naranja", "amarillo", "verde", "azul", "indigo")])


def colores_integracion():
    """Los 7 colores de los chakras, de la raíz a la corona."""
    return [M.PALETA[n] for n in ("rojo", "naranja", "amarillo", "verde", "azul", "indigo", "violeta")]


def ejemplo_integracion():
    return M.integracion(esquema_integracion())


def _hex_rgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def medir(img, paleta):
    """img: imagen RGB (alto, ancho, 3); paleta: lista de hex. Devuelve (parte de lo pintado que lleva cada
    color, cantidad de píxeles de color que no son de la paleta ni bordes suavizados de una línea)."""
    from scipy import ndimage
    img = img.astype(int)
    colores = np.array([_hex_rgb(h) for h in paleta])
    dist = np.abs(img[:, :, None, :] - colores[None, None, :, :]).sum(axis=3)           # (alto, ancho, n)
    mejor = dist.argmin(axis=2)
    exacto = dist.min(axis=2) <= 12                                                      # sin bordes suavizados
    cuenta = np.bincount(mejor[exacto], minlength=len(colores)).astype(float)
    crominancia = img.max(axis=2) - img.min(axis=2)
    cerca_borde = ndimage.binary_dilation((img.max(axis=2) < 70) | (img.min(axis=2) > 235), iterations=3)
    ajeno = (crominancia > 14) & (dist.min(axis=2) > 60) & ~cerca_borde
    return cuenta / cuenta.sum(), int(ajeno.sum())


def proporciones(clave, svg=None, px_por_mm=8):
    """Parte de lo pintado que lleva cada color de la paleta (se miden los píxeles ya dibujados)."""
    import cairosvg
    svg = svg or ejemplo(clave)
    ancho_mm = float(re.search(r'width="([\d.]+)mm"', svg).group(1))
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=round(ancho_mm * px_por_mm), background_color="white")
    partes, _ = medir(np.array(Image.open(io.BytesIO(png)).convert("RGB")), colores_de(clave))
    return dict(zip(M.PALETAS[clave], partes))


if __name__ == "__main__":
    for clave in M.MANDALAS:
        prop = proporciones(clave)
        print(f"{clave:11s}", "  ".join(f"{n} {v * 100:4.1f}%" for n, v in prop.items()))
