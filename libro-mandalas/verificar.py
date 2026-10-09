"""Controles automáticos de calidad. Uso: python3 verificar.py

Mandalas (a partir del SVG, rasterizado a 8 px/mm):
  - cantidad de zonas para pintar (regiones blancas cerradas);
  - tamaño de cada zona: diámetro del círculo más grande que entra adentro (10 mm o más) y
    superficie (1 cm² o más): nada de zonas diminutas ni de líneas que se cortan;
  - grosor de línea: 3 pt o más en las divisiones y hasta 3,5 pt en los contornos;
  - cantidad de pétalos de cada chakra.

PDF (el que se imprime):
  - 8,5 × 11" con sangrado de 0,125" (cajas de corte y sangrado), fuentes incrustadas, reversos en blanco;
  - texto de 18 pt o más (número de página también), afirmaciones de 30 pt o más;
  - textos dentro de los márgenes y sin superponerse entre sí ni con el mandala;
  - mandalas en blanco y negro: ningún color adentro del dibujo;
  - paleta sugerida: 5 colores, el protagonista primero y más grande; pestaña de 8 mm del color del chakra;
  - que no vuelvan los textos que se sacaron ("Está en:", "No hay forma de hacerlo mal").
"""
import io
import re
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

PX_POR_MM = 8
ZONA_MIN_MM = 10.0      # diámetro mínimo exigido por zona
ZONA_AVISO_MM = 12.0    # por debajo de esto se cuenta como "zona ajustada" (válida)
AREA_RUIDO_MM2 = 0.25      # por debajo de esto es ruido de rasterizado (la punta de un pétalo), no una zona
PROTAGONISTA_MIN, PROTAGONISTA_MAX = 0.59, 0.71   # 60–70 % con 1 punto de tolerancia por el rasterizado
ZONA_MIN_AREA_MM2 = 100.0   # 1 cm²
MM_A_PT = 72 / 25.4
LINEA_MIN_PT = 2.9      # las divisiones internas miden 3 pt
LINEA_MAX_PT = 3.7      # los contornos miden 3,5 pt

# Zonas esperadas por dibujo (±1): si baja, probablemente hay una línea cortada que une dos zonas
ZONAS_ESPERADAS = {"raiz": 22, "sacro": 26, "plexo": 32, "corazon": 31, "garganta": 42, "tercer_ojo": 24,
                   "corona": 48, "integracion": 51, "par_de_flores": 18}


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
        if area_mm2 < AREA_RUIDO_MM2:           # puntas de pétalos que se afinan hasta menos de un píxel: no son zonas
            continue
        diametro = 2 * dist[mascara].max() / px_por_mm
        ys, xs = np.nonzero(mascara)
        zonas.append({"id": i, "area_mm2": area_mm2, "diametro_mm": diametro,
                      "centro_mm": ((xs.mean() - gris.shape[1] / 2) / px_por_mm,
                                    (ys.mean() - gris.shape[0] / 2) / px_por_mm)})
    return zonas, etiquetas


def trazos_en_pt(svg_texto):
    """Grosores de línea declarados en el SVG, en puntos (solo los que se dibujan). Si el dibujo se agranda con
    <g transform="scale(k)">, el grosor que se imprime es el declarado por k."""
    escala = re.search(r'<g transform="scale\(([\d.]+)\)">', svg_texto)
    k = float(escala.group(1)) if escala else 1.0
    return [float(x) * k * MM_A_PT for x in re.findall(r'stroke-width="([\d.]+)"', svg_texto)]


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
    finas = [z for z in zonas if z["area_mm2"] < ZONA_MIN_AREA_MM2 and z["diametro_mm"] >= ZONA_MIN_MM]
    if finas:
        problemas.append(f"{len(finas)} zona(s) de menos de 1 cm²")
    pts = trazos_en_pt(svg_texto)
    if pts and (min(pts) < LINEA_MIN_PT or max(pts) > LINEA_MAX_PT):
        problemas.append(f"línea de {min(pts):.2f} a {max(pts):.2f} pt (se pide {LINEA_MIN_PT} a {LINEA_MAX_PT})")
    if (borde < 170).any():
        problemas.append("hay líneas que tocan el borde del dibujo (posible corte)")
    if zonas_esperadas is not None and abs(len(zonas) - zonas_esperadas) > 1:
        problemas.append(f"{len(zonas)} zonas, se esperaban {zonas_esperadas} "
                         "(si son menos, puede haber una línea cortada que une dos zonas)")
    n_petalos = contar_petalos(svg_texto)
    if petalos_esperados is not None and n_petalos != petalos_esperados:
        problemas.append(f"pétalos: {n_petalos}, esperados {petalos_esperados}")
    ajustadas = sum(1 for z in zonas if z["diametro_mm"] < ZONA_AVISO_MM)
    linea = (f"{nombre}: {len(zonas)} zonas · zona más chica {diam[0]:.1f} mm (menores a {ZONA_AVISO_MM:g} mm: {ajustadas}) · "
             f"mediana {diam[len(diam)//2]:.1f} mm · línea {min(pts):.1f}–{max(pts):.1f} pt · {n_petalos} pétalos")
    return linea, problemas, zonas


def contar_petalos(svg_texto):
    """Pétalos = grupos class="petalo" (los de las flores de la integración llevan otra clase)."""
    return len(re.findall(r'class="petalo"', svg_texto))


# ------------------------------------------------------------------ PDF
MM = 25.4 / 72  # mm por punto
HEX = lambda h: np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)])


def _lineas_pdf(ruta_pdf):
    """Por página: (líneas de texto con bbox en mm —origen arriba-izquierda— y tamaños de letra,
    cajas de los dibujos: curvas, líneas y rectángulos)."""
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LAParams, LTChar, LTCurve, LTLine, LTRect, LTTextContainer, LTTextLine
    paginas = []
    for pag in extract_pages(ruta_pdf, laparams=LAParams(line_margin=0.1, char_margin=4)):
        alto = pag.height
        lineas, dibujos = [], []
        for caja in pag:
            if isinstance(caja, (LTCurve, LTLine, LTRect)):
                if (caja.x1 - caja.x0) * MM < 0.9 * pag.width * MM:          # sin el fondo de la página
                    dibujos.append((caja.x0 * MM, (alto - caja.y1) * MM, caja.x1 * MM, (alto - caja.y0) * MM))
                continue
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
        paginas.append((lineas, dibujos))
    return paginas


def _raster(ruta_pdf, pagina_1, dpi):
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        base = f"{tmp}/pag"
        subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(pagina_1), "-l", str(pagina_1), "-png", "-singlefile",
                        ruta_pdf, base], check=True)
        return np.array(Image.open(base + ".png").convert("RGB"))


def verificar_pdf(ruta_pdf, paginas_info, g):
    """paginas_info: lista (una por página impresa) de dicts (ver generar_libro.informacion_paginas).
    g: geometría del libro (módulo generar_libro): ANCHO, ALTO, SANGRE, PAG_W, PAG_H, X0, X1, MARGEN_SUP, MARGEN_INF, CX."""
    import subprocess
    from pypdf import PdfReader
    import mandalas as M
    fallos, notas = [], []
    lector = PdfReader(ruta_pdf)
    n_imp = len(paginas_info)
    if len(lector.pages) != n_imp:
        fallos.append(f"el PDF tiene {len(lector.pages)} páginas, se esperaban {n_imp}")
        return fallos, notas
    S = g.SANGRE
    if n_imp % 4:
        notas.append(f"ojo: {n_imp} páginas no es múltiplo de 4 (importa solo si la imprenta cose o abrocha)")
    # impar = derecha, par = izquierda; el reverso de cada página para pintar con marcador tiene que estar en blanco
    for k, info in enumerate(paginas_info):
        if info["lado"] != ("D" if k % 2 == 0 else "I"):
            fallos.append(f"página {k + 1} ({info['nombre']}): debería ser {'derecha' if k % 2 == 0 else 'izquierda'}")
        if info.get("marcador") and not (k + 1 < n_imp and paginas_info[k + 1].get("en_blanco")):
            fallos.append(f"página {k + 1} ({info['nombre']}): se pinta con marcador y su reverso no está en blanco")

    # tamaño con sangrado, cajas de corte y reversos en blanco
    for i, p in enumerate(lector.pages):
        w, h = float(p.mediabox.width) * MM, float(p.mediabox.height) * MM
        if abs(w - g.PAG_W) > 0.3 or abs(h - g.PAG_H) > 0.3:
            fallos.append(f"página {i + 1}: tamaño {w:.2f}×{h:.2f} mm (con sangrado debe ser {g.PAG_W:.2f}×{g.PAG_H:.2f})")
        corte = [float(x) * MM for x in p.trimbox]
        ox = S if paginas_info[i]["lado"] == "I" else 0          # el sangrado está del lado de afuera
        if (abs(corte[0] - ox) > 0.1 or abs(corte[1] - S) > 0.1 or abs(corte[2] - (ox + g.ANCHO)) > 0.1
                or abs(corte[3] - (g.PAG_H - S)) > 0.1):
            fallos.append(f"página {i + 1}: la caja de corte no es 8,5 × 11\" ({[round(c, 2) for c in corte]})")
        if paginas_info[i].get("en_blanco"):
            if p.extract_text().strip() or (_raster(ruta_pdf, i + 1, 40) < 250).any():
                fallos.append(f"la página {i + 1} (reverso) no está en blanco")
    notas.append(f"tamaño: {g.ANCHO / 25.4:.2f} × {g.ALTO / 25.4:.2f} pulgadas de corte, {S / 25.4:.3f} pulgadas de sangrado")

    # Fuentes incrustadas
    fuentes = subprocess.run(["pdffonts", ruta_pdf], capture_output=True, text=True).stdout.splitlines()[2:]
    for linea in fuentes:
        partes = linea.split()
        if len(partes) >= 6 and partes[-5] != "yes":      # columna "emb"
            fallos.append(f"fuente sin incrustar: {partes[0]}")
    nombres = sorted({l.split()[0].split('+')[-1] for l in fuentes if l.strip()})
    notas.append(f"fuentes incrustadas: {nombres}")
    ajenas = [n for n in nombres if not n.startswith(("Fraunces", "Manrope"))]
    if ajenas:
        fallos.append(f"tipografías fuera de la marca (solo Fraunces y Manrope): {ajenas}")

    # Texto: tamaños, márgenes, superposición (solo páginas impresas = índices pares)
    texto_por_pagina = _lineas_pdf(ruta_pdf)
    prohibidos = ["No hay forma de hacerlo mal", "Está en:", "Emoción que cuida", "Usá papel de 120"]
    for k, info in enumerate(paginas_info):
        if info.get("en_blanco"):
            continue
        lineas, dibujos = texto_por_pagina[k]
        ox = S if info["lado"] == "I" else 0
        dibujos = [(a - ox, b - S, c - ox, d - S) for a, b, c, d in dibujos]
        for l in lineas:                                  # a coordenadas del corte (sin el sangrado)
            l["y0"] -= S
            l["y1"] -= S
            l["x0"] -= ox
            l["x1"] -= ox
        etiqueta = f"p.{k + 1} {info['nombre']}"
        d_i = g.DESPLAZ_I if info["lado"] == "I" else 0
        x0, x1 = info.get("x_limites", (g.X0 - d_i, g.X1 - d_i))
        y0, y1 = info.get("y_limites", (g.MARGEN_SUP, g.ALTO - g.MARGEN_INF))
        candidatas = [l for l in lineas if info.get("numero") is not None and l["texto"] == str(info["numero"])]
        linea_numero = max(candidatas, key=lambda l: l["y0"]) if candidatas else None
        for l in lineas:
            es_numero = l is linea_numero
            if l["pt"] < 18 - 0.3:
                fallos.append(f"{etiqueta}: texto de {l['pt']:.1f} pt: «{l['texto'][:40]}»")
            if es_numero and abs(l["pt"] - 18) > 0.3:
                fallos.append(f"{etiqueta}: el número de página mide {l['pt']:.1f} pt (debe ser 18)")
            tol = 1.5 if es_numero else 0.5
            if l["x0"] < x0 - tol or l["x1"] > x1 + tol or l["y0"] < y0 - tol or l["y1"] > y1 + tol:
                fallos.append(f"{etiqueta}: «{l['texto'][:30]}» se sale del margen "
                              f"(x {l['x0']:.1f}–{l['x1']:.1f}, y {l['y0']:.1f}–{l['y1']:.1f}; permitido x {x0:.1f}–{x1:.1f}, y {y0:.1f}–{y1:.1f})")
            if es_numero:
                centro = (l["x0"] + l["x1"]) / 2
                if abs(centro - (g.CX - d_i)) > 1.0:
                    fallos.append(f"{etiqueta}: número de página descentrado ({centro:.1f} mm, eje en {g.CX - d_i:.1f})")
            for p in prohibidos:
                if p in l["texto"]:
                    fallos.append(f"{etiqueta}: volvió un texto que se sacó: «{p}»")
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
                    fallos.append(f"{etiqueta}: no encuentro la frase «{linea_af}»")
                elif hit[0]["pt"] < 30 or "Fraunces" not in hit[0]["fuente"]:
                    fallos.append(f"{etiqueta}: frase «{linea_af}» a {hit[0]['pt']:.1f} pt / {hit[0]['fuente']}")
        # la frase aparece una sola vez por capítulo
        for t in info.get("sin_texto") or []:
            if any(t in l["texto"] for l in lineas):
                fallos.append(f"{etiqueta}: la frase «{t}» está repetida (ya figura bajo el mandala)")
        # texto vs dibujos: en las páginas donde solo hay un dibujo ornamental, ninguna línea de texto lo pisa
        if info.get("imagenes"):
            for l in lineas:
                for (ix0, iy0, ix1, iy1) in dibujos:
                    if min(l["x1"], ix1) - max(l["x0"], ix0) > 0.3 and min(l["y1"], iy1) - max(l["y0"], iy0) > 0.3:
                        fallos.append(f"{etiqueta}: «{l['texto'][:30]}» pisa un dibujo")
                        break
        # texto vs mandala
        if info.get("mandala"):
            cx, cy, r = info["mandala"]
            for l in lineas:
                px = min(max(cx, l["x0"]), l["x1"])
                py = min(max(cy, l["y0"]), l["y1"])
                if ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5 < r + 2.0:
                    fallos.append(f"{etiqueta}: «{l['texto'][:30]}» toca el mandala")

    # Portada: que estén todos los textos pedidos
    if paginas_info[0]["nombre"] == "portada":
        todo = " ".join(l["texto"] for l in texto_por_pagina[0][0])
        for esperado in ("MANDALAS", "CHAKRAS", "Un color a la vez", "Para colorear, reflexionar y disfrutar",
                         "Creado por Dani Navarro", "LIBRO PARA COLOREAR", "Para mamá, con todo mi amor."):
            if esperado not in todo:
                fallos.append(f"portada: falta el texto «{esperado}»")
        if "7" not in todo:
            fallos.append("portada: falta el 7 de «DE LOS 7 CHAKRAS»")

    # Contenido de las páginas nuevas y de la dedicatoria de cada edición
    esperados = {"legal": ["© 2026", "No reemplaza", "hola@daninavarro.com.ar", "Primera edición"],
                 "que_es_un_chakra": ["significa", "No hace falta creer", "Siete chakras", "Corona"],
                 "como_usar": ["Mirá el ejemplo"], "dedicatoria": ["Para vos, mamá"]}
    for k, info in enumerate(paginas_info):
        todo = " ".join(l["texto"] for l in texto_por_pagina[k][0])
        for t in esperados.get(info["nombre"], []):
            if t not in todo:
                fallos.append(f"p.{k + 1} {info['nombre']}: falta el texto «{t}»")
        if info["nombre"] == "dedicatoria":
            if info.get("edicion") == "venta" and ("De:" not in todo or "Dani" in todo):
                fallos.append("dedicatoria (venta): debe tener la línea «De:» y no la firma de Dani")
            if info.get("edicion") == "mama" and ("Dani" not in todo or "De:" in todo):
                fallos.append("dedicatoria (mamá): debe estar firmada por Dani")

    # Pestaña (8 mm del color del chakra, hasta el borde con sangrado: a la derecha en las páginas derechas,
    # a la izquierda en las izquierdas) y paleta sugerida
    pxmm = 200 / 25.4
    for k, info in enumerate(paginas_info):
        if info.get("en_blanco") or not (info.get("clave") or info.get("a_color")):
            continue
        izquierda = info["lado"] == "I"
        img = _raster(ruta_pdf, k + 1, 200).astype(int)
        if info.get("clave"):
            esperado = HEX(M.COLORES[info["clave"]])
            cerca = np.abs(img - esperado).sum(axis=2) < 40
            if izquierda:                                  # el corte empieza a S mm del borde izquierdo de la página
                limite = int((S + 12) * pxmm)
                ys, xs = np.nonzero(cerca[:, :limite])
            else:
                borde_x = int((g.ANCHO - 12) * pxmm)
                ys, xs = np.nonzero(cerca[:, borde_x:])
            if len(xs) == 0:
                fallos.append(f"p.{k + 1}: no se ve la pestaña de color {info['clave']}")
            elif izquierda:
                ancho_tab = (xs.max() + 1) / pxmm - S
                if abs(ancho_tab - 8) > 0.3:
                    fallos.append(f"p.{k + 1}: pestaña de {ancho_tab:.2f} mm (debe ser 8 mm desde el corte)")
                if xs.min() > 2:
                    fallos.append(f"p.{k + 1}: la pestaña no llega al borde del sangrado")
            else:
                izq = (xs.min() + borde_x) / pxmm
                if abs((g.ANCHO - izq) - 8) > 0.3:
                    fallos.append(f"p.{k + 1}: pestaña de {g.ANCHO - izq:.2f} mm (debe ser 8 mm desde el corte)")
                if (xs.max() + 1 + borde_x) < img.shape[1] - 2:
                    fallos.append(f"p.{k + 1}: la pestaña no llega al borde del sangrado")
        if info.get("paleta"):
            ox = S if izquierda else 0
            x_desde, x_hasta = ((12, g.ANCHO - g.MARGEN_INT) if izquierda else (g.X0, g.ANCHO - 12))

            def colores_en(desde, hasta):
                reg = img[int((S + desde) * pxmm):int((S + hasta) * pxmm), int((ox + x_desde) * pxmm):int((ox + x_hasta) * pxmm)]
                return {h: int((np.abs(reg - HEX(h)).sum(axis=2) < 30).sum()) for h in M.PALETA.values()}

            if info.get("sin_proporcion"):                # "Todos juntos": los 7 colores en dos filas
                fila = colores_en(info["fila_paleta"] - 1, info["fila_paleta"] + 21)
                if not set(info["paleta"]) <= {h for h, c in fila.items() if c > 150}:
                    fallos.append(f"p.{k + 1}: la fila de colores no muestra los 7 colores de los chakras")
            elif info.get("a_color"):                     # ejemplo pintado: cabecera con el protagonista; fila de paleta abajo
                cab = colores_en(g.MARGEN_SUP - 1, g.MARGEN_SUP + 15)
                if [h for h, c in cab.items() if c > 150] != [info["protagonista"]]:
                    fallos.append(f"p.{k + 1}: la cabecera debe mostrar solo el color protagonista")
                fila = colores_en(info["fila_paleta"] - 1, info["fila_paleta"] + 10)
                if sorted(h for h, c in fila.items() if c > 150) != sorted(info["paleta"]):
                    fallos.append(f"p.{k + 1}: la fila de colores no muestra los 5 de la paleta sugerida")
            else:
                cuentas = colores_en(g.MARGEN_SUP - 1, info["fila_paleta"] + 10)
                visibles = [h for h, c in cuentas.items() if c > 150]
                if sorted(visibles) != sorted(info["paleta"]):
                    fallos.append(f"p.{k + 1}: la paleta visible no es la sugerida ({len(visibles)} colores en la cabecera, se esperaban {len(info['paleta'])})")
                elif cuentas[info["protagonista"]] <= max(c for h, c in cuentas.items() if h != info["protagonista"]):
                    fallos.append(f"p.{k + 1}: el color protagonista no es el que más se ve en la cabecera")

    # Mandalas en blanco y negro (ningún color adentro del dibujo) y grosor de línea medido a 600 dpi:
    # largo de miles de cruces horizontales sobre el mandala (los perpendiculares dan el grosor real,
    # los oblicuos dan más); se toma el percentil 5.
    for k, info in enumerate(paginas_info):
        if not info.get("mandala"):
            continue
        cx, cy, r = info["mandala"]
        ox = S if info["lado"] == "I" else 0
        img = _raster(ruta_pdf, k + 1, 150).astype(int)
        p150 = 150 / 25.4
        yy, xx = np.ogrid[:img.shape[0], :img.shape[1]]
        dentro = ((xx / p150 - ox) - cx) ** 2 + ((yy / p150 - S) - cy) ** 2 <= (r + 1) ** 2
        croma = img.max(axis=2) - img.min(axis=2)
        con_color = int((croma[dentro] > 14).sum())
        if info.get("a_color"):
            import ejemplos
            recorte = img[dentro.any(axis=1)][:, dentro.any(axis=0)]
            if info.get("sin_proporcion"):                 # "Todos juntos": 7 colores + dorado + crema
                partes, ajenos = ejemplos.medir(recorte, info["paleta"] + [M.PALETA["dorado"], ejemplos.CREMA])
                notas.append(f"p.{k + 1}: Todos juntos pintado: " + ", ".join(f"{p * 100:.0f}%" for p in partes))
                if partes.min() < 0.005:
                    fallos.append(f"p.{k + 1}: hay un color del ejemplo casi sin usar")
            else:
                partes, ajenos = ejemplos.medir(recorte, info["paleta"])
                notas.append(f"p.{k + 1}: reparto de colores del ejemplo: " +
                             ", ".join(f"{n} {p * 100:.0f}%" for n, p in zip(M.PALETAS[info["clave"]], partes)))
                if not PROTAGONISTA_MIN <= partes[0] <= PROTAGONISTA_MAX:
                    fallos.append(f"p.{k + 1}: el color protagonista ocupa {partes[0] * 100:.1f} % de lo pintado "
                                  f"(debe estar entre {PROTAGONISTA_MIN * 100:.0f} y {PROTAGONISTA_MAX * 100:.0f} %)")
                if partes.min() < 0.015:
                    fallos.append(f"p.{k + 1}: hay un color de la paleta casi sin usar ({partes.min() * 100:.1f} %)")
            if ajenos > 60:
                fallos.append(f"p.{k + 1}: {ajenos} píxeles con colores que no son de la paleta")
        elif con_color:
            fallos.append(f"p.{k + 1}: hay {con_color} píxeles con color adentro del mandala (debe ser blanco y negro)")
        img = _raster(ruta_pdf, k + 1, 600)
        px_mm = 600 / 25.4
        oscuro = img.astype(int).max(axis=2) < 70          # solo el negro de la línea (no los colores oscuros)
        largos = []
        for y in range(int((S + cy - r) * px_mm), int((S + cy + r) * px_mm), 3):
            fila = oscuro[y, int((ox + cx - r - 1) * px_mm):int((ox + cx + r + 1) * px_mm)].astype(int)
            d = np.diff(np.concatenate(([0], fila, [0])))
            largos += list(np.nonzero(d == -1)[0] - np.nonzero(d == 1)[0])
        if len(largos) < 500:
            fallos.append(f"p.{k + 1}: no pude medir la línea ({len(largos)} cruces)")
            continue
        grosor_mm = float(np.percentile(largos, 5)) / px_mm
        pt = grosor_mm * MM_A_PT
        notas.append(f"p.{k + 1}: línea medida en el PDF = {grosor_mm:.2f} mm = {pt:.2f} pt ({len(largos)} cruces)")
        if not (LINEA_MIN_PT <= pt <= LINEA_MAX_PT):
            fallos.append(f"p.{k + 1}: línea de {pt:.2f} pt (se pide entre {LINEA_MIN_PT} y {LINEA_MAX_PT})")
    return fallos, notas


def main():
    import generar_libro as G
    import mandalas as M
    problemas_total = 0
    print("== MANDALAS (SVG) ==")
    for ch in G.CHAKRAS:
        ruta = G.AQUI / "svg" / f"{ch['clave']}.svg"
        linea, problemas, _ = informe_mandala(ch["nombre"], ruta.read_text(encoding="utf-8"),
                                              petalos_esperados=M.PETALOS[ch["clave"]], zonas_esperadas=ZONAS_ESPERADAS[ch["clave"]])
        print(" ", linea)
        for p in problemas:
            print("    ✗", p)
        problemas_total += len(problemas)
    print("== EJEMPLOS PINTADOS (SVG) ==")
    import ejemplos
    for ch in G.CHAKRAS:
        clave = ch["clave"]
        pintado = (G.AQUI / "ejemplos" / f"{clave}.svg").read_text(encoding="utf-8")
        base = (G.AQUI / "svg" / f"{clave}.svg").read_text(encoding="utf-8")
        problemas = []
        usados = set(re.findall(r'fill="(#[0-9A-Fa-f]{6})"', pintado)) - {"#FFFFFF", M.NEGRO}
        ajenos = usados - set(ejemplos.colores_de(clave))
        if ajenos:
            problemas.append(f"colores fuera de la paleta: {sorted(ajenos)}")
        if len(usados) != 5:
            problemas.append(f"usa {len(usados)} colores (deben ser 5)")
        # las líneas son las mismas que las del mandala para colorear: sin color, los dos dibujos son idénticos
        sin_color = pintado
        for h in usados:
            sin_color = sin_color.replace(f'fill="{h}"', f'fill="{M.BLANCO}"')
        dif = np.abs(rasterizar(sin_color).astype(int) - rasterizar(base).astype(int))
        if int((dif > 120).sum()) > 20:
            problemas.append(f"el ejemplo no tiene las mismas líneas que el mandala ({int((dif > 120).sum())} píxeles distintos)")
        partes = ejemplos.proporciones(clave, pintado)
        prot = partes[M.PALETAS[clave][0]]
        if not PROTAGONISTA_MIN <= prot <= PROTAGONISTA_MAX:
            problemas.append(f"el protagonista ocupa {prot * 100:.1f} % de lo pintado")
        print(f"  {ch['nombre']}: " + " · ".join(f"{n} {p * 100:.0f}%" for n, p in partes.items()))
        for p in problemas:
            print("    ✗", p)
        problemas_total += len(problemas)
    pintado = (G.AQUI / "ejemplos" / "integracion.svg").read_text(encoding="utf-8")
    base = (G.AQUI / "svg" / "integracion.svg").read_text(encoding="utf-8")
    problemas = []
    usados = set(re.findall(r'fill="(#[0-9A-Fa-f]{6})"', pintado)) - {"#FFFFFF", M.NEGRO}
    permitidos = set(ejemplos.colores_integracion()) | {M.PALETA["dorado"], ejemplos.CREMA}
    if usados != permitidos:
        problemas.append(f"colores de Todos juntos: sobran {sorted(usados - permitidos)} / faltan {sorted(permitidos - usados)}")
    sin_color = pintado
    for h in usados:
        sin_color = sin_color.replace(f'fill="{h}"', f'fill="{M.BLANCO}"')
    dif = np.abs(rasterizar(sin_color).astype(int) - rasterizar(base).astype(int))
    if int((dif > 120).sum()) > 20:
        problemas.append(f"Todos juntos pintado no tiene las mismas líneas que el dibujo ({int((dif > 120).sum())} píxeles distintos)")
    print("  Todos juntos: 7 colores de los chakras + centros dorados sobre fondo crema")
    for p in problemas:
        print("    ✗", p)
    problemas_total += len(problemas)
    # negro puro en todas las líneas (nada de grises)
    otros = set()
    for archivo in list((G.AQUI / "svg").glob("*.svg")) + list((G.AQUI / "ejemplos").glob("*.svg")):
        if archivo.name == "portada_arte.svg":
            continue
        otros |= set(re.findall(r'stroke="(#[0-9A-Fa-f]{6})"', archivo.read_text(encoding="utf-8"))) - {M.NEGRO}
    if otros:
        print("    ✗ líneas que no son negro puro:", sorted(otros))
        problemas_total += 1
    for nombre, archivo, clave in (("Integración (7 flores)", "integracion.svg", "integracion"),
                                   ("Dos flores (compartir)", "par_de_flores.svg", "par_de_flores"),
                                   ("Corazón (dedicatoria y cierre)", "dedicatoria_corazon.svg", None)):
        ruta = G.AQUI / "svg" / archivo
        linea, problemas, _ = informe_mandala(nombre, ruta.read_text(encoding="utf-8"), zonas_esperadas=ZONAS_ESPERADAS.get(clave))
        print(" ", linea.replace(" · 0 pétalos", ""))
        for p in problemas:
            print("    ✗", p)
        problemas_total += len(problemas)

    print("== PDF ==")
    pdf = G.AQUI / "libro_mandalas_chakras.pdf"
    if not pdf.exists():
        print("  (no hay PDF generado)")
        return 1
    info = G.informacion_paginas("venta")
    # la portada tiene sus propios márgenes (los de la tarjeta)
    info[0]["x_limites"] = (15.0, G.ANCHO - 15.0)
    info[0]["y_limites"] = (G.MARGEN_SUP, G.ALTO - G.MARGEN_INF)
    fallos, notas = verificar_pdf(str(pdf), info, G)
    print(f"  {pdf.name}: {len(info)} páginas impresas")
    for n in notas:
        print("   ·", n)
    for f in fallos:
        print("    ✗", f)
    problemas_total += len(fallos)
    mama = G.AQUI / G.EDICIONES["mama"]
    if not mama.exists():
        print("    ✗ falta", mama.name)
        problemas_total += 1
    else:
        from pypdf import PdfReader
        lector = PdfReader(str(mama))
        texto = lector.pages[2].extract_text()
        errores = []
        if len(lector.pages) != len(info):
            errores.append(f"tiene {len(lector.pages)} páginas, la otra edición {len(info)}")
        if "Dani" not in texto or "De:" in texto or "Para vos, mamá" not in texto:
            errores.append("la dedicatoria debe estar firmada por Dani y sin la línea «De:»")
        distintas = [i + 1 for i, (a, b) in enumerate(zip(lector.pages, PdfReader(str(pdf)).pages))
                     if i != 2 and a.extract_text() != b.extract_text()]
        if distintas:
            errores.append(f"las ediciones difieren en otras páginas: {distintas}")
        print(f"  {mama.name}: {len(lector.pages)} páginas; solo cambia la firma de la dedicatoria" if not errores else f"  {mama.name}")
        for e in errores:
            print("    ✗", e)
        problemas_total += len(errores)
    print("\nRESULTADO:", "todo en orden ✔" if problemas_total == 0 else f"{problemas_total} problema(s) ✗")
    return 0 if problemas_total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
