"""Marca en cada página del PDF dónde se corta (TrimBox) y hasta dónde llega el sangrado (BleedBox).
Uso: python3 cajas.py archivo.pdf sangrado_en_mm
La página ya trae el sangrado: el tamaño final es la página menos ese margen por lado.
"""
import sys
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

MM = 72 / 25.4
ruta, sangrado_mm = sys.argv[1], float(sys.argv[2])
s = sangrado_mm * MM

lector = PdfReader(ruta)
escritor = PdfWriter()
for pagina in lector.pages:
    x0, y0, x1, y1 = (float(v) for v in pagina.mediabox)
    pagina.bleedbox = RectangleObject([x0, y0, x1, y1])
    pagina.trimbox = RectangleObject([x0 + s, y0 + s, x1 - s, y1 - s])
    escritor.add_page(pagina)
escritor.add_metadata({"/Title": "Mente Viva NeuroGym", "/Author": "Daniela Navarro · Longevidad Emocional"})
with open(ruta, "wb") as f:
    escritor.write(f)
