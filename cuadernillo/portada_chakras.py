"""Portadas "Mandalas de los Chakras": 7 lotos vectoriales (uno por chakra)
con geometría dorada. Genera salida/portada_regalo.pdf y salida/portada_amazon.pdf
(más sus PNG).

    python portada_chakras.py
"""
import math
import subprocess

from jinja2 import Template
from weasyprint import HTML

import graficos as g
from construir import RAIZ, cargar

# Del chakra raíz a la corona. Tonos oscuros para que el texto y el trazo
# tengan contraste sobre marfil.
CHAKRAS = [
    ("Raíz", "#B3362C"), ("Sacro", "#C8651B"), ("Plexo solar", "#B8890A"),
    ("Corazón", "#3D8A45"), ("Garganta", "#2F72B5"), ("Tercer ojo", "#43449B"),
    ("Corona", "#7A4A9E"),
]
AZUL_NOCHE = "#1F3466"
PETROLEO = "#1F5F78"

TEXTOS = {
    "titulo": "Mandalas",
    "subtitulo": "de los Chakras",
    "autora": "Creado por Dani Navarro",
    "banda_1": "Libro para colorear",
}

# Dos tapas: el regalo personal (A4, imprenta local, sin sangrado) y la de
# Amazon KDP (8,5 x 11 in + 0,125 in de sangrado, fondo a sangre).
VARIANTES = {
    "regalo": {
        "formato": "a4",
        "para": "Mente Viva",
        "banda_2": "Mandalas, ejercicios para la mente y frases positivas",
        "dedicatoria": "Para mamá, con todo mi amor.",
    },
    "amazon": {
        "formato": "kdp",
        "para": "para Adultos Mayores",
        "banda_2": "Letra grande · Mandalas simples · Ejercicios para la mente",
        "dedicatoria": "",
    },
}

FORMATOS = {
    # ancho, alto de la hoja (mm), margen de página, margen de seguridad interior
    "a4": {"ancho": 210, "alto": 297, "margen": 15, "seguro": 0, "radio": 4},
    # 8,625 x 11,25 in: tapa frontal con sangrado; el texto queda a 0,375 in
    # del corte (6,35 mm + 3,175 mm de sangrado)
    "kdp": {"ancho": 219.075, "alto": 285.75, "margen": 0, "seguro": 12.7, "radio": 0},
}


def geometria(dorado: str, lado: float, r_anillo: float) -> str:
    """Círculo, hexágono y radios finos en dorado detrás de las flores."""
    c = lado / 2
    pts = [(c + r_anillo * math.sin(i * math.pi / 3), c - r_anillo * math.cos(i * math.pi / 3)) for i in range(6)]
    hexa = " ".join(f"{x:.2f},{y:.2f}" for x, y in pts)
    radios = "".join(f'<line x1="{c}" y1="{c}" x2="{x:.2f}" y2="{y:.2f}"/>' for x, y in pts)
    estrella = " ".join(f"{pts[i][0]:.2f},{pts[i][1]:.2f}" for i in (0, 2, 4)) 
    estrella2 = " ".join(f"{pts[i][0]:.2f},{pts[i][1]:.2f}" for i in (1, 3, 5))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{lado}mm" height="{lado}mm" viewBox="0 0 {lado} {lado}">'
            f'<g fill="none" stroke="{dorado}" stroke-width="0.35">'
            f'<circle cx="{c}" cy="{c}" r="{r_anillo}"/><circle cx="{c}" cy="{c}" r="{r_anillo * 1.18}"/>'
            f'<polygon points="{hexa}"/><polygon points="{estrella}"/><polygon points="{estrella2}"/>{radios}</g></svg>')


def main():
    cfg = cargar(RAIZ / "config.json")
    p = cfg["paleta"]
    fuentes = (RAIZ / "fuentes").as_uri()
    lado, r_anillo, d_centro, d_flor = 150.0, 52.0, 60.0, 40.0
    flores = []
    # corona al centro; los otros seis alrededor, empezando arriba
    for i, (nombre, color) in enumerate(CHAKRAS[:6]):
        ang = i * math.pi / 3
        x = lado / 2 + r_anillo * math.sin(ang) - d_flor / 2
        y = lado / 2 - r_anillo * math.cos(ang) - d_flor / 2
        flores.append({"x": x, "y": y, "svg": g.loto(color, d_flor, k=8)})
    centro = {"x": (lado - d_centro) / 2, "y": (lado - d_centro) / 2,
              "svg": g.loto(CHAKRAS[6][1], d_centro, k=12)}
    letras = [(ch, CHAKRAS[i % 7][1]) for i, ch in enumerate(TEXTOS["subtitulo"].replace(" ", " "))]
    # los espacios no consumen color: se recalcula saltándolos
    letras, n = [], 0
    for ch in TEXTOS["subtitulo"]:
        if ch == " ":
            letras.append((" ", AZUL_NOCHE))
        else:
            letras.append((ch, CHAKRAS[n % 7][1])); n += 1

    for nombre, v in VARIANTES.items():
        fmt = FORMATOS[v["formato"]]
        t = {**TEXTOS, **v}
        html = Template(PLANTILLA).render(
            f=fuentes, p=p, t=t, fmt=fmt, lado=lado, flores=flores, centro=centro, letras=letras,
            geo=geometria(p["dorado"], lado, r_anillo), azul=AZUL_NOCHE, petroleo=PETROLEO)
        pdf = RAIZ / "salida" / f"portada_{nombre}.pdf"
        HTML(string=html, base_url=str(RAIZ)).write_pdf(pdf)
        subprocess.run(["pdftoppm", "-r", "110", "-png", "-singlefile", str(pdf),
                        str(RAIZ / "salida" / "png" / f"portada_{nombre}")], check=True)
        print("ok:", pdf.relative_to(RAIZ))


PLANTILLA = """<!doctype html><html lang="es-AR"><head><meta charset="utf-8">
<title>Mandalas de los Chakras</title><style>
@font-face { font-family: Manrope; font-weight: 700; src: url('{{ f }}/Manrope-Bold.ttf'); }
@font-face { font-family: Manrope; font-weight: 800; src: url('{{ f }}/Manrope-ExtraBold.ttf'); }
@font-face { font-family: Manrope; font-weight: 500; src: url('{{ f }}/Manrope-Medium.ttf'); }
@font-face { font-family: Fraunces; font-weight: 600; src: url('{{ f }}/Fraunces-SemiBold.ttf'); }
@font-face { font-family: Fraunces; font-style: italic; src: url('{{ f }}/Fraunces-Italic.ttf'); }
@page { size: {{ fmt.ancho }}mm {{ fmt.alto }}mm; margin: {{ fmt.margen }}mm; }
body { margin: 0; color: {{ azul }}; }
.hoja { box-sizing: border-box; height: {{ fmt.alto - 2 * fmt.margen }}mm; background: {{ p.papel }}; border-radius: {{ fmt.radio }}mm;
        position: relative; text-align: center; padding-top: {{ (6 if t.dedicatoria else 9) + fmt.seguro }}mm; overflow: hidden; }
h1 { font-family: Fraunces; font-weight: 600; font-size: 66pt; line-height: 1.05; margin: 0;
     text-transform: uppercase; letter-spacing: 0.01em; }
.sub { font-family: Manrope; font-weight: 800; font-size: 34pt; line-height: 1.2; text-transform: uppercase; letter-spacing: 0.02em; }
.para { font-family: Fraunces; font-weight: 600; font-size: 24pt; color: #4A3B33; margin-top: 1mm; }
.flores { position: relative; width: {{ lado }}mm; height: {{ lado }}mm; margin: 5mm auto 3mm; }
.flores > div { position: absolute; }
.autora { font-family: Fraunces; font-weight: 600; font-size: 20pt; color: #4A3B33; }
{% if not t.dedicatoria %}.flores { margin-top: 8mm; margin-bottom: 6mm; }{% else %}.flores { margin-top: 2mm; margin-bottom: 1.5mm; }{% endif %}
.banda { position: absolute; left: 0; right: 0; bottom: {{ (19 + fmt.seguro) if t.dedicatoria else 0 }}mm;{% if not t.dedicatoria %} padding-bottom: {{ fmt.seguro + 3 }}mm !important;{% endif %} background: {{ petroleo }}; color: #fff; padding: 3.5mm 0 4mm; }
.banda .b1 { font-family: Manrope; font-weight: 800; font-size: 26pt; text-transform: uppercase; letter-spacing: 0.04em; line-height: 1.2; }
.banda .b2 { font-family: Manrope; font-weight: 500; font-size: 17pt; line-height: 1.3; }
.dedic { position: absolute; left: 0; right: 0; bottom: {{ 5 + fmt.seguro }}mm; font-family: Fraunces; font-style: italic; font-size: 22pt; }
</style></head><body><div class="hoja">
<h1>{{ t.titulo }}</h1>
<div class="sub">{% for ch, c in letras %}<span style="color: {{ c }}">{{ ch }}</span>{% endfor %}</div>
<div class="para">{{ t.para }}</div>
<div class="flores">
  <div style="left:0;top:0">{{ geo }}</div>
  {% for fl in flores %}<div style="left: {{ '%.2f'|format(fl.x) }}mm; top: {{ '%.2f'|format(fl.y) }}mm">{{ fl.svg }}</div>{% endfor %}
  <div style="left: {{ '%.2f'|format(centro.x) }}mm; top: {{ '%.2f'|format(centro.y) }}mm">{{ centro.svg }}</div>
</div>
<div class="autora">{{ t.autora }}</div>
<div class="banda"><div class="b1">{{ t.banda_1 }}</div><div class="b2">{{ t.banda_2 }}</div></div>
{% if t.dedicatoria %}<div class="dedic">{{ t.dedicatoria }}</div>{% endif %}
</div></body></html>"""

if __name__ == "__main__":
    main()
