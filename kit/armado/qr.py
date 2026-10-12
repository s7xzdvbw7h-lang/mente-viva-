"""Imprime un QR como SVG vectorial (sin imágenes). Uso: python3 qr.py URL COLOR"""
import sys
import qrcode

url, color = sys.argv[1], sys.argv[2]
q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0, box_size=1)
q.add_data(url)
q.make(fit=True)
m = q.get_matrix()
n = len(m)
rects = "".join(f"M{x} {y}h1v1h-1z" for y, fila in enumerate(m) for x, v in enumerate(fila) if v)
print(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-3 -3 {n + 6} {n + 6}" shape-rendering="crispEdges"><path d="{rects}" fill="{color}"/></svg>')
