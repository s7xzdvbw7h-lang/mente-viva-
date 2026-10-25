"""Código QR en vector (SVG): negro sobre blanco, sin colores ni adornos, con margen blanco alrededor.

El QR se dibuja en unidades de módulo (todas las coordenadas son enteras, así los módulos vecinos se tocan sin
rendijas) y el SVG se escala a milímetros: `lado` es lo que miden los módulos y `margen` el blanco que los rodea.
"""
import segno

ERROR = "q"          # corrección de errores nivel Q (25 %): aguanta manchas y roces del papel impreso


def matriz(url):
    """Filas de módulos (1 = negro) del QR de `url`, sin el margen."""
    qr = segno.make(url, error=ERROR, micro=False, boost_error=False)
    return [list(fila) for fila in qr.matrix], qr.version


def svg_qr(url, lado=28.0, margen=4.0):
    """(svg, módulos por lado, versión): QR de `lado` mm con `margen` mm de blanco, negro puro sobre blanco puro."""
    filas, version = matriz(url)
    n = len(filas)
    modulo = lado / n                         # mm por módulo
    b = margen / modulo                       # margen en módulos
    total = n + 2 * b
    trazos = []
    for y, fila in enumerate(filas):          # una tira por cada corrida de módulos negros seguidos
        x = 0
        while x < n:
            if fila[x]:
                inicio = x
                while x < n and fila[x]:
                    x += 1
                trazos.append(f"M{inicio} {y}h{x - inicio}v1h-{x - inicio}z")
            else:
                x += 1
    mm = lado + 2 * margen
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{mm:g}mm" height="{mm:g}mm" viewBox="0 0 {total:.6f} {total:.6f}">'
           f'<rect width="{total:.6f}" height="{total:.6f}" fill="#FFFFFF"/>'
           f'<g transform="translate({b:.6f} {b:.6f})"><path fill="#000000" d="{"".join(trazos)}"/></g></svg>')
    return svg, n, version
