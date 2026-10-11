"""Coloca los 8 mandalas del libro terminado de Dani en las páginas reservadas del cuaderno.

Uso:
  node kit/armado/construir.mjs cuaderno-base          # arma el cuaderno con las 8 páginas libres
  python3 kit/armado/insertar_mandalas.py LIBRO.pdf 12,15,19,22,26,30,33,37

Los 8 números son las páginas del libro que van de cierre en los encuentros 1 a 8, en ese orden.
Cada página se achica para entrar en la zona útil (respeta los 20 mm del espiral) sin deformarse.
"""
import json
import sys
from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation, PageObject

MM = 72 / 25.4
RAIZ = Path(__file__).resolve().parent.parent
base = RAIZ / "pdf" / "cuaderno-base-para-mandalas.pdf"
slots = json.loads((RAIZ / "armado" / "_html" / "cuaderno-base-para-mandalas.mandalas.json").read_text())
salida = RAIZ / "pdf" / "cuaderno-la-hora-del-te.pdf"

libro = PdfReader(sys.argv[1])
paginas = [int(x) for x in sys.argv[2].split(",")]
assert len(paginas) == 8 and len(slots) == 8, "Hacen falta exactamente 8 páginas del libro"

S = 3  # sangrado
# Zona útil (en mm, desde el borde con sangrado): ancho sin los 20 mm del espiral, debajo del título y encima del pie.
X0, X1 = S + 20, S + 210 - 13
Y_TOP, Y_BOT = S + 34, S + 297 - 20

lector = PdfReader(str(base))
escritor = PdfWriter()
for i, pagina in enumerate(lector.pages, start=1):
    if i in slots:
        k = slots.index(i)
        origen = libro.pages[paginas[k] - 1]
        ow, oh = float(origen.mediabox.width), float(origen.mediabox.height)
        W, H = float(pagina.mediabox.width), float(pagina.mediabox.height)
        zw, zh = (X1 - X0) * MM, (Y_BOT - Y_TOP) * MM
        esc = min(zw / ow, zh / oh)
        tx = X0 * MM + (zw - ow * esc) / 2
        ty = H - Y_BOT * MM + (zh - oh * esc) / 2  # origen del PDF: abajo a la izquierda
        pagina.merge_transformed_page(origen, Transformation().scale(esc).translate(tx, ty))
    escritor.add_page(pagina)
escritor.add_metadata({"/Title": "La hora del té", "/Author": "Daniela Navarro · Longevidad Emocional"})
with open(salida, "wb") as f:
    escritor.write(f)
print("listo:", salida)
