"""Controles automáticos de calidad. Uso: python3 verificar.py

Mandalas (a partir del SVG, rasterizado a 8 px/mm):
  - cantidad de zonas para pintar (regiones blancas cerradas);
  - tamaño de cada zona: diámetro del círculo más grande que entra adentro;
  - zonas diminutas o líneas que se cortan;
  - grosor de línea declarado en el SVG y medido en el PDF a 600 dpi;
  - cantidad de pétalos de cada chakra.

PDF (el que se imprime):
  - tamaño A4, fuentes incrustadas, reversos realmente en blanco;
  - texto >= 18 pt (número de página 16 pt, afirmaciones >= 30 pt);
  - textos dentro de los márgenes de 15 mm y sin superponerse entre sí ni con el mandala;
  - pestaña de 8 mm con el color del chakra.
"""
import io
import re
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

PX_POR_MM = 8
ZONA_MIN_MM = 8.0       # diámetro mínimo exigido por zona
ZONA_AVISO_MM = 10.0    # por debajo de esto se avisa (todavía válido)
LINEA_MIN_PX96 = 2.5    # grosor mínimo de línea, en px a 96 dpi
MM_A_PX96 = 96 / 25.4


def rasterizar(svg_texto, px_por_mm=PX_POR_MM):
    import cairosvg
    m = re.search(r'width="([\d.]+)mm"', svg_texto)
    ancho_mm = float(m.group(1))
    png = cairosvg.svg2png(bytestring=svg_texto.encode(), output_width=int(round(ancho_mm * px_por_mm)),
                           background_color="white")
    return np.array(Image.open(io.BytesIO(png)).convert("L"))


def analizar_zonas(svg_texto, px_por_mm=PX_POR_MM):
    gris = rasterizar(svg_texto, px_por_mm)
    blanco = gris > 170
    etiquetas, total = ndimage.label(blanco)          # 4-conectividad
    fondo = etiquetas[0, 0]
    dist = ndimage.distance_transform_edt(blanco)
    zonas = []
    for i in range(1, total + 1):
        if i == fondo:
            continue
        mascara = etiquetas == i
        area_mm2 = mascara.sum() / px_por_mm**2
        diametro = 2 * dist[mascara].max() / px_por_mm
        ys, xs = np.nonzero(mascara)
        zonas.append({"id": i, "area_mm2": area_mm2, "diametro_mm": diametro,
                      "centro_mm": ((xs.mean() - gris.shape[1] / 2) / px_por_mm,
                                    (ys.mean() - gris.shape[0] / 2) / px_por_mm)})
    return zonas, etiquetas


def grosor_minimo_linea_px96(svg_texto):
    anchos = [float(x) for x in re.findall(r'stroke-width="([\d.]+)"', svg_texto)]
    return (min(anchos) * MM_A_PX96) if anchos else None


def informe_mandala(nombre, svg_texto, petalos_esperados=None, zonas_esperadas=None):
    zonas, _ = analizar_zonas(svg_texto)
    gris = rasterizar(svg_texto)
    borde = np.concatenate([gris[0, :], gris[-1, :], gris[:, 0], gris[:, -1]])
    diam = sorted(z["diametro_mm"] for z in zonas)
    problemas = []
    chicas = [z for z in zonas if z["diametro_mm"] < ZONA_MIN_MM]
    if chicas:
        problemas.append(f"{len(chicas)} zona(s) menores a {ZONA_MIN_MM:g} mm: " +
                         ", ".join(f"({z['centro_mm'][0]:.0f},{z['centro_mm'][1]:.0f}) {z['diametro_mm']:.1f} mm" for z in chicas))
    px = grosor_minimo_linea_px96(svg_texto)
    if px is not None and px < LINEA_MIN_PX96:
        problemas.append(f"línea de {px:.2f} px (<{LINEA_MIN_PX96})")
    if (borde < 170).any():
        problemas.append("hay líneas que tocan el borde del dibujo (posible corte)")
    if zonas_esperadas and not (zonas_esperadas[0] <= len(zonas) <= zonas_esperadas[1]):
        problemas.append(f"{len(zonas)} zonas, se esperaban entre {zonas_esperadas[0]} y {zonas_esperadas[1]} "
                         "(si es menos, puede haber una línea cortada que une dos zonas)")
    n_petalos = contar_petalos(svg_texto)
    if petalos_esperados is not None and n_petalos != petalos_esperados:
        problemas.append(f"pétalos: {n_petalos}, esperados {petalos_esperados}")
    linea = (f"{nombre}: {len(zonas)} zonas · zona más chica {diam[0]:.1f} mm · mediana {diam[len(diam)//2]:.1f} mm · "
             f"línea {px:.2f} px · {n_petalos} pétalos")
    return linea, problemas, zonas


def contar_petalos(svg_texto):
    """Pétalos exteriores = grupos class="petalo" (los interiores llevan otra clase)."""
    return len(re.findall(r'class="petalo"', svg_texto))



# ------------------------------------------------------------------ PDF
MM = 25.4 / 72  # mm por punto


def _lineas_pdf(ruta_pdf):
    """Por página: lista de líneas de texto con bbox en mm (origen arriba-izquierda) y tamaños de letra."""
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LAParams, LTChar, LTTextContainer, LTTextLine
    paginas = []
    for pag in extract_pages(ruta_pdf, laparams=LAParams(line_margin=0.1, char_margin=4)):
        alto = pag.height
        lineas = []
        for caja in pag:
            if not isinstance(caja, LTTextContainer):
                continue
            for linea in caja:
                if not isinstance(linea, LTTextLine):
                    continue
                chars = [c for c in linea if isinstance(c, LTChar)]
                if not chars:
                    continue
                lineas.append({
                    "texto": linea.get_text().strip(),
                    "x0": linea.x0 * MM, "x1": linea.x1 * MM,
                    "y0": (alto - linea.y1) * MM, "y1": (alto - linea.y0) * MM,
                    "pt": min(c.size for c in chars), "pt_max": max(c.size for c in chars),
                    "fuente": chars[0].fontname,
                })
        paginas.append(lineas)
    return paginas


def _raster(ruta_pdf, pagina_1, dpi):
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        base = f"{tmp}/pag"
        subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(pagina_1), "-l", str(pagina_1), "-png", "-singlefile",
                        ruta_pdf, base], check=True)
        return np.array(Image.open(base + ".png").convert("RGB"))


def verificar_pdf(ruta_pdf, paginas_info, margen_mm=15, ancho_mm=210, alto_mm=297):
    """paginas_info: lista (una por página impresa) de dicts con
    nombre, numero (int|None), clave (chakra|None), mandala (cx, cy, radio en mm|None), afirmacion (líneas|None)."""
    import subprocess
    from pypdf import PdfReader
    fallos, notas = [], []
    lector = PdfReader(ruta_pdf)
    n_imp = len(paginas_info)
    if len(lector.pages) != 2 * n_imp:
        fallos.append(f"el PDF tiene {len(lector.pages)} páginas, se esperaban {2 * n_imp} (impresas + reversos)")
        return fallos, notas

    # A4 y reversos en blanco
    for i, p in enumerate(lector.pages):
        w, h = float(p.mediabox.width) * MM, float(p.mediabox.height) * MM
        if abs(w - ancho_mm) > 0.5 or abs(h - alto_mm) > 0.5:
            fallos.append(f"página {i + 1}: tamaño {w:.1f}×{h:.1f} mm (no es A4)")
        if i % 2 == 1:
            contenido = p.get_contents()
            if contenido is not None and contenido.get_data().strip() or p.extract_text().strip():
                fallos.append(f"el reverso {i + 1} no está en blanco")

    # Fuentes incrustadas
    fuentes = subprocess.run(["pdffonts", ruta_pdf], capture_output=True, text=True).stdout.splitlines()[2:]
    for linea in fuentes:
        partes = linea.split()
        if len(partes) >= 6 and partes[-5] != "yes":      # columna "emb"
            fallos.append(f"fuente sin incrustar: {partes[0]}")
    notas.append(f"fuentes incrustadas: {sorted({l.split()[0].split('+')[-1] for l in fuentes if l.strip()})}")

    # Texto: tamaños, márgenes, superposición (solo páginas impresas = índices pares)
    texto_por_pagina = _lineas_pdf(ruta_pdf)
    for k, info in enumerate(paginas_info):
        lineas = texto_por_pagina[2 * k]
        etiqueta = f"p.{k + 1} {info['nombre']}"
        for l in lineas:
            es_numero = info.get("numero") is not None and l["texto"] == str(info["numero"])
            minimo = 16 if es_numero else 18
            if l["pt"] < minimo - 0.3:
                fallos.append(f"{etiqueta}: texto de {l['pt']:.1f} pt: «{l['texto'][:40]}»")
            if es_numero and abs(l["pt"] - 16) > 0.3:
                fallos.append(f"{etiqueta}: el número de página mide {l['pt']:.1f} pt (debe ser 16)")
            tol = 1.5 if es_numero else 0.5
            if (l["x0"] < margen_mm - tol or l["x1"] > ancho_mm - margen_mm + tol
                    or l["y0"] < margen_mm - tol or l["y1"] > alto_mm - margen_mm + tol):
                fallos.append(f"{etiqueta}: «{l['texto'][:30]}» se sale del margen de {margen_mm} mm "
                              f"(x {l['x0']:.1f}–{l['x1']:.1f}, y {l['y0']:.1f}–{l['y1']:.1f})")
            if es_numero:
                centro = (l["x0"] + l["x1"]) / 2
                if abs(centro - ancho_mm / 2) > 1.0:
                    fallos.append(f"{etiqueta}: número de página descentrado ({centro:.1f} mm)")
        # superposición entre líneas
        for a in range(len(lineas)):
            for b in range(a + 1, len(lineas)):
                A, B = lineas[a], lineas[b]
                ix = min(A["x1"], B["x1"]) - max(A["x0"], B["x0"])
                iy = min(A["y1"], B["y1"]) - max(A["y0"], B["y0"])
                if ix > 0.5 and iy > 1.0:
                    fallos.append(f"{etiqueta}: se superponen «{A['texto'][:25]}» y «{B['texto'][:25]}»")
        # afirmación: letra llena y >= 30 pt
        if info.get("afirmacion"):
            for linea_af in info["afirmacion"]:
                hit = [l for l in lineas if linea_af in l["texto"]]
                if not hit:
                    fallos.append(f"{etiqueta}: no encuentro la afirmación «{linea_af}»")
                elif hit[0]["pt"] < 30 or "Fraunces" not in hit[0]["fuente"]:
                    fallos.append(f"{etiqueta}: afirmación «{linea_af}» a {hit[0]['pt']:.1f} pt / {hit[0]['fuente']}")
        # texto vs mandala
        if info.get("mandala"):
            cx, cy, r = info["mandala"]
            for l in lineas:
                px = min(max(cx, l["x0"]), l["x1"])
                py = min(max(cy, l["y0"]), l["y1"])
                if ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5 < r + 3:
                    fallos.append(f"{etiqueta}: «{l['texto'][:30]}» toca el mandala")

    # Pestaña: ancho 8 mm y color del chakra (a 110 dpi)
    import mandalas as M
    for k, info in enumerate(paginas_info):
        if not info.get("clave"):
            continue
        img = _raster(ruta_pdf, 2 * k + 1, 200)
        px_mm = 200 / 25.4
        esperado = np.array([int(M.COLORES[info["clave"]][i:i + 2], 16) for i in (1, 3, 5)])
        cerca = np.abs(img.astype(int) - esperado).sum(axis=2) < 40
        ys, xs = np.nonzero(cerca[:, int(190 * px_mm):])
        if len(xs) == 0:
            fallos.append(f"p.{k + 1}: no se ve la pestaña de color {info['clave']}")
            continue
        ancho_tab = (xs.max() - xs.min() + 1) / px_mm
        if abs(ancho_tab - 8) > 0.3:
            fallos.append(f"p.{k + 1}: pestaña de {ancho_tab:.2f} mm (debe ser 8)")
        if (xs.max() + 1 + int(190 * px_mm)) < img.shape[1] - 2:
            fallos.append(f"p.{k + 1}: la pestaña no llega al borde derecho")

    # Grosor de línea medido en el PDF a 600 dpi (sobre el eje horizontal del mandala)
    for k, info in enumerate(paginas_info):
        if not info.get("mandala"):
            continue
        cx, cy, r = info["mandala"]
        img = _raster(ruta_pdf, 2 * k + 1, 600)
        px_mm = 600 / 25.4
        fila = (img[int(round(cy * px_mm)), :, :].astype(int).sum(axis=1) / 3) < 110
        xs = np.nonzero(fila[: int((cx - r + 8) * px_mm)])[0]       # borde izquierdo del círculo exterior
        if len(xs) == 0:
            fallos.append(f"p.{k + 1}: no encuentro el círculo exterior para medir la línea")
            continue
        corrida = 1
        while xs[corrida] == xs[0] + corrida if corrida < len(xs) else False:
            corrida += 1
        grosor_mm = corrida / px_mm
        grosor_px96 = grosor_mm * MM_A_PX96
        notas.append(f"p.{k + 1}: línea medida en el PDF = {grosor_mm:.2f} mm = {grosor_px96:.2f} px a 96 dpi")
        if grosor_px96 < LINEA_MIN_PX96 - 0.1:
            fallos.append(f"p.{k + 1}: línea de {grosor_px96:.2f} px (<{LINEA_MIN_PX96})")
    return fallos, notas


def main():
    import generar_libro as G
    import mandalas as M
    problemas_total = 0
    print("== MANDALAS (SVG) ==")
    for ch in G.CHAKRAS:
        ruta = G.AQUI / "svg" / f"{ch['clave']}.svg"
        if not ruta.exists():
            continue
        linea, problemas, _ = informe_mandala(ch["nombre"], ruta.read_text(encoding="utf-8"), petalos_esperados=ch["petalos"], zonas_esperadas=ch["zonas"])
        print(" ", linea)
        for p in problemas:
            print("    ✗", p)
        problemas_total += len(problemas)

    print("== PDF ==")
    pdfs = sorted(G.AQUI.glob("libro_mandalas_chakras*.pdf"), key=lambda p: p.stat().st_mtime)
    if not pdfs:
        print("  (no hay PDF generado)")
        return 1
    ruta_pdf = str(pdfs[-1])
    info = G.informacion_paginas(1 if "fase1" in pdfs[-1].name else 2)
    fallos, notas = verificar_pdf(ruta_pdf, info)
    print(f"  {pdfs[-1].name}: {len(info)} páginas impresas")
    for n in notas:
        print("   ·", n)
    for f in fallos:
        print("    ✗", f)
    problemas_total += len(fallos)
    print("\nRESULTADO:", "todo en orden ✔" if problemas_total == 0 else f"{problemas_total} problema(s) ✗")
    return 0 if problemas_total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
