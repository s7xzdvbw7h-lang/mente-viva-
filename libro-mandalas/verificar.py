"""Controles automáticos de calidad. Uso: python3 verificar.py

Mandalas (a partir del SVG, rasterizado a 8 px/mm):
  - cantidad de zonas para pintar (regiones blancas cerradas);
  - tamaño de cada zona: diámetro del círculo más grande que entra adentro (10 mm o más) y
    superficie (1 cm² o más): nada de zonas diminutas ni de líneas que se cortan;
  - grosor de línea: 2,25 pt en las divisiones y 2,63 pt en los contornos (gris #3A3A3A);
  - cantidad de pétalos de cada chakra.

PDF (los dos que se imprimen: libro-chakras-venta.pdf y libro-chakras-mama.pdf):
  - 8,5 × 11" con sangrado de 0,125" (cajas de corte y sangrado), fuentes incrustadas, fondo #FFFBF5;
  - hojas en blanco (reversos): solo la nota de 18 pt y el número de página, nada más;
  - texto de 18 pt o más (número de página también), afirmaciones de 30 pt o más;
  - textos dentro de los márgenes y sin superponerse entre sí ni con el mandala;
  - mandalas para colorear sin color adentro del dibujo;
  - paleta sugerida: 5 colores, el principal primero; reparto del ejemplo según el chakra; pestaña de 8 mm;
  - todos los textos pedidos están y no vuelven los que se sacaron ("Está relacionado…", "Color protagonista"…);
  - las dos ediciones son iguales salvo la dedicatoria (p.3), Garganta (p.25) y la página 40.
"""
import io
import re
import sys
import unicodedata
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

PX_POR_MM = 8
ZONA_MIN_MM = 10.0      # diámetro mínimo exigido por zona
ZONA_AVISO_MM = 12.0    # por debajo de esto se cuenta como "zona ajustada" (válida)
AREA_RUIDO_MM2 = 0.25      # por debajo de esto es ruido de rasterizado (la punta de un pétalo), no una zona
TOLERANCIA_PROTAGONISTA = 0.01    # 1 punto de tolerancia por el rasterizado (el rango sale de ejemplos.rango_protagonista)
ZONA_MIN_AREA_MM2 = 100.0   # 1 cm²
MM_A_PT = 72 / 25.4
LINEA_MIN_PT = 2.1      # las divisiones internas miden 2,25 pt (25 % menos que antes)
LINEA_MAX_PT = 3.0      # los contornos miden 2,63 pt
NEGRO_LINEA = "#3A3A3A"
FONDO_PAGINA = "#FFFBF5"

# Zonas esperadas por dibujo (±1): si baja, probablemente hay una línea cortada que une dos zonas
ZONAS_ESPERADAS = {"raiz": 22, "sacro": 26, "plexo": 26, "corazon": 23, "garganta": 26, "tercer_ojo": 16,
                   "corona": 25, "integracion": 49, "par_de_flores": 18}


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
RENGLON_COLOR = "#8A8178"
TEXTO_COLORES = {"#222222", "#333333"}          # el texto va en #222 (cuerpo) o #333 (textos chicos)


def _norm(t):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", t).replace(" ", " ")).strip()


def _lineas_pdf(ruta_pdf):
    """Por página: (líneas de texto con bbox en mm —origen arriba-izquierda—, tamaños y color de letra;
    cajas de los dibujos: curvas, líneas y rectángulos; rellenos con su color)."""
    from pdfminer.high_level import extract_pages
    from pdfminer.layout import LAParams, LTChar, LTCurve, LTLine, LTRect, LTTextContainer, LTTextLine
    paginas = []
    for pag in extract_pages(ruta_pdf, laparams=LAParams(line_margin=0.1, char_margin=4)):
        alto = pag.height
        lineas, dibujos, rellenos = [], [], []
        for caja in pag:
            if isinstance(caja, (LTCurve, LTLine, LTRect)):
                if (caja.x1 - caja.x0) * MM < 0.9 * pag.width * MM:          # sin el fondo de la página
                    caja_mm = (caja.x0 * MM, (alto - caja.y1) * MM, caja.x1 * MM, (alto - caja.y0) * MM)
                    dibujos.append(caja_mm)
                    if isinstance(caja, LTRect) and caja.fill:
                        color = caja.non_stroking_color
                        if isinstance(color, (tuple, list)) and len(color) == 3:
                            rellenos.append(caja_mm + ("#%02X%02X%02X" % tuple(round(c * 255) for c in color),))
                continue
            if not isinstance(caja, LTTextContainer):
                continue
            for linea in caja:
                if not isinstance(linea, LTTextLine):
                    continue
                chars = [c for c in linea if isinstance(c, LTChar)]
                if not chars:
                    continue
                color = chars[0].graphicstate.ncolor
                if isinstance(color, (int, float)):
                    color = (color,) * 3
                lineas.append({
                    "texto": linea.get_text().strip(),
                    "x0": linea.x0 * MM, "x1": linea.x1 * MM,
                    "y0": (alto - linea.y1) * MM, "y1": (alto - linea.y0) * MM,
                    "pt": min(c.size for c in chars), "pt_max": max(c.size for c in chars),
                    "fuente": chars[0].fontname,
                    "color": ("#%02X%02X%02X" % tuple(round(c * 255) for c in color)) if color and len(color) == 3 else None,
                })
        paginas.append((lineas, dibujos, rellenos))
    return paginas


def _raster(ruta_pdf, pagina_1, dpi):
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        base = f"{tmp}/pag"
        subprocess.run(["pdftoppm", "-r", str(dpi), "-f", str(pagina_1), "-l", str(pagina_1), "-png", "-singlefile",
                        ruta_pdf, base], check=True)
        return np.array(Image.open(base + ".png").convert("RGB"))


def _renglones(rellenos):
    """Rayas para escribir: rellenos finos del color de los renglones. Cada raya sale como dos rectángulos que
    comparten el borde de abajo (el grosor es la diferencia). Devuelve [(centro_y, grosor, ancho, x0, color)]."""
    candidatos = [r for r in rellenos if r[4] == RENGLON_COLOR and (r[2] - r[0]) >= 20]
    grupos = []
    for r in sorted(candidatos, key=lambda r: (r[3], r[0])):
        for g_ in grupos:
            if abs(g_[0][3] - r[3]) < 0.7 and abs(g_[0][0] - r[0]) < 0.5 and abs(g_[0][2] - r[2]) < 0.5:
                g_.append(r)
                break
        else:
            grupos.append([r])
    rayas = []
    for g_ in grupos:
        fondos = [r[3] for r in g_]
        rayas.append(((max(fondos) + min(fondos)) / 2, max(fondos) - min(fondos), g_[0][2] - g_[0][0], g_[0][0], g_[0][4]))
    return sorted(rayas)


def _esperado_en_pagina(info, g, edicion):
    """Textos que tiene que haber en la página (lista de frases), según el pedido."""
    nombre, clave = info["nombre"], info.get("clave")
    ch = next((c for c in g.CHAKRAS if c["clave"] == clave), None)
    if nombre == "legal":
        return ["© 2026", "No reemplaza", "hola@daninavarro.com.ar", "Primera edición"]
    if nombre == "dedicatoria":
        return [g.DEDIC_TITULO]
    if nombre == "que_es_un_chakra":
        return ([g.QUE_ES_TITULO] + list(g.QUE_ES_PARRAFOS) + [g.QUE_ES_CIERRE]
                + [f'{c["nombre"]} · {g.QUE_ES_TEMAS[c["clave"]]}' for c in g.CHAKRAS])
    if nombre == "como_usar":
        return [g.COMO_USAR_TITULO] + [parte for t in g.COMO_USAR_PASOS for parte in t.split("\n")]
    if nombre.endswith("_ejemplo") and ch:
        return [ch["nombre"], g.COLOR_PRINCIPAL, g.TITULO_EJEMPLO, g.NOTA_EJEMPLO]
    if nombre.endswith("_mandala") and ch:
        return [ch["nombre"], g.COLOR_PRINCIPAL, g.ANTES_DE_EMPEZAR, g.LEER_FRASE] + list(ch["afirmacion"])
    if nombre.endswith("_reflexion") and ch:
        d = g._datos_reflexion(ch, edicion)
        return ([d["nombre"], d["parrafo"], g.TITULO_RESPIRAR, d["respiracion"], g.TITULO_RECORDAR]
                + list(d["preguntas"]) + list(d["nota"]))
    if nombre == "final_en_blanco":
        return []
    if nombre.endswith("_en_blanco"):
        return [g.NOTA_BLANCA]
    if nombre == "integracion_ejemplo":
        return [g.INTEGRACION_TITULO, g.TITULO_EJEMPLO, g.NOTA_EJEMPLO]
    if nombre == "integracion":
        return [g.INTEGRACION_TITULO, g.INTEGRACION_ARRIBA, g.ANTES_DE_EMPEZAR, g.INTEGRACION_ABAJO] + list(g.INTEGRACION_FRASE)
    if nombre == "compartir":
        return [g.COMPARTIR_TITULO] + list(g.COMPARTIR_LINEAS) + [g.COMPARTIR_FRASE, g.COMPARTIR_NOTA]
    if nombre == "cierre":
        return ([g.CIERRE_TITULO] + [l.rstrip(",") for l in g.FRASE_FINAL]
                + [g.CIERRE_SENTI, g.CIERRE_AYUDA, g.CIERRE_FECHA, g.CIERRE_NOTA])
    if nombre == "contratapa":
        return ([g.CONTRA_MAMA_TITULO, g.CONTRA_PARA, g.CONTRA_DE] if edicion == "mama" else
                [g.CONTRA_TITULO] + list(g.CONTRA_LINEAS) + [g.CONTRA_CARINO, g.CONTRA_NOMBRE, g.CONTRA_MARCA])
    if nombre == "cierre_qr":
        return [g.QR_TEXTO, g.QR_NOMBRE, g.CONTRA_USUARIO]
    return []


# Palabras que no pueden volver (textos que se sacaron o que no son neutros en género)
PROHIBIDOS = ["No hay forma de hacerlo mal", "Está en:", "Emoción que cuida", "Usá papel de 120", "Color protagonista",
              "Para recordar", "Al terminar, leé en voz alta", "Está relacionado", "Doy y recibo amor",
              "Confío en mi intuición", "TODOS JUNTOS", "chacra", "Chacra"]
PROHIBIDOS_REGEX = [r"\b(tranquila|orgullosa|cansada|contenta|sola|segura de ti)\b", r"\bsentirte bien contigo\b"]


def verificar_pdf(ruta_pdf, paginas_info, g, edicion="venta", completo=True):
    """paginas_info: lista (una por página impresa) de dicts (ver generar_libro.informacion_paginas).
    g: geometría y textos del libro (módulo generar_libro). completo=False salta los controles de imagen caros
    (pestañas, paleta, mandalas, grosor de línea) y deja solo los de texto: sirve para la segunda edición."""
    import subprocess
    from pypdf import PdfReader
    import mandalas as M
    import ejemplos
    fallos, notas = [], []
    lector = PdfReader(ruta_pdf)
    n_imp = len(paginas_info)
    if len(lector.pages) != n_imp:
        fallos.append(f"el PDF tiene {len(lector.pages)} páginas, se esperaban {n_imp}")
        return fallos, notas
    S = g.SANGRE
    if n_imp % 2:
        fallos.append(f"el libro tiene {n_imp} páginas: el total tiene que ser par para imprimir")
    else:
        notas.append(f"total de páginas: {n_imp} (par)" + ("" if n_imp % 4 == 0 else
                     "; no es múltiplo de 4, importa solo si la imprenta cose o abrocha cuadernillos"))
    # impar = derecha, par = izquierda; el reverso de cada página para pintar con marcador tiene que estar en blanco
    for k, info in enumerate(paginas_info):
        if info["lado"] != ("D" if k % 2 == 0 else "I"):
            fallos.append(f"página {k + 1} ({info['nombre']}): debería ser {'derecha' if k % 2 == 0 else 'izquierda'}")
        if info.get("marcador") and not (k + 1 < n_imp and paginas_info[k + 1].get("en_blanco")):
            fallos.append(f"página {k + 1} ({info['nombre']}): se pinta con marcador y su reverso no está en blanco")
    for k in (9, 13, 17, 21, 25, 29, 33):                                # texto de cada chakra: p.9, 13, …, 33
        if k - 1 < n_imp and not paginas_info[k - 1]["nombre"].endswith("_reflexion"):
            fallos.append(f"la página {k} debería ser la de texto de un chakra ({paginas_info[k - 1]['nombre']})")
    for k in (8, 12, 16, 20, 24, 28, 32, 36, 38):                        # hojas en blanco
        if k - 1 < n_imp and not paginas_info[k - 1].get("en_blanco"):
            fallos.append(f"la página {k} debería ser una hoja en blanco ({paginas_info[k - 1]['nombre']})")

    # tamaño con sangrado, cajas de corte y fondo de la página (#FFFBF5)
    fondo = HEX(FONDO_PAGINA)
    for i, p in enumerate(lector.pages):
        w, h = float(p.mediabox.width) * MM, float(p.mediabox.height) * MM
        if abs(w - g.PAG_W) > 0.3 or abs(h - g.PAG_H) > 0.3:
            fallos.append(f"página {i + 1}: tamaño {w:.2f}×{h:.2f} mm (con sangrado debe ser {g.PAG_W:.2f}×{g.PAG_H:.2f})")
        corte = [float(x) * MM for x in p.trimbox]
        ox = S if paginas_info[i]["lado"] == "I" else 0          # el sangrado está del lado de afuera
        if (abs(corte[0] - ox) > 0.1 or abs(corte[1] - S) > 0.1 or abs(corte[2] - (ox + g.ANCHO)) > 0.1
                or abs(corte[3] - (g.PAG_H - S)) > 0.1):
            fallos.append(f"página {i + 1}: la caja de corte no es 8,5 × 11\" ({[round(c, 2) for c in corte]})")
        if i > 0:                                                 # la portada tiene su propio arte
            img = _raster(ruta_pdf, i + 1, 30).astype(int)
            esquinas = [img[2, 2], img[2, -3], img[-3, 2], img[-3, -3]]
            if any(np.abs(c - fondo).sum() > 6 for c in esquinas):
                fallos.append(f"página {i + 1}: el fondo no es {FONDO_PAGINA} ({[tuple(int(v) for v in c) for c in esquinas][:1]})")
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

    # Texto: tamaños, márgenes, superposición, orden y color (todas las páginas, también las hojas en blanco)
    texto_por_pagina = _lineas_pdf(ruta_pdf)
    for k, info in enumerate(paginas_info):
        lineas, dibujos, rellenos = texto_por_pagina[k]
        ox = S if info["lado"] == "I" else 0
        dibujos = [(a - ox, b - S, c - ox, d - S) for a, b, c, d in dibujos]
        rellenos = [(a - ox, b - S, c - ox, d - S, col) for a, b, c, d, col in rellenos]
        for l in lineas:                                  # a coordenadas del corte (sin el sangrado)
            l["y0"] -= S
            l["y1"] -= S
            l["x0"] -= ox
            l["x1"] -= ox
        etiqueta = f"p.{k + 1} {info['nombre']}"
        d_i = g.DESPLAZ_I if info["lado"] == "I" else 0
        eje = g.CX - d_i
        x0, x1 = info.get("x_limites", (g.X0 - d_i, g.X1 - d_i))
        y0, y1 = info.get("y_limites", (g.MARGEN_SUP, g.ALTO - g.MARGEN_INF))
        candidatas = [l for l in lineas if info.get("numero") is not None and l["texto"] == str(info["numero"])]
        linea_numero = max(candidatas, key=lambda l: l["y0"]) if candidatas else None
        if info.get("numero") is not None and linea_numero is None:
            fallos.append(f"{etiqueta}: no encuentro el número de página {info['numero']}")
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
                if abs(centro - eje) > 1.0:
                    fallos.append(f"{etiqueta}: número de página descentrado ({centro:.1f} mm, eje en {eje:.1f})")
            if info["nombre"] != "portada" and l["color"] and (l["color"] not in TEXTO_COLORES):
                oscuro = max(int(l["color"][i:i + 2], 16) for i in (1, 3, 5))
                if oscuro < 20 or oscuro > 70:
                    fallos.append(f"{etiqueta}: «{l['texto'][:25]}» en color {l['color']} (el texto va en #222 o #333)")
            for p in PROHIBIDOS:
                if p in l["texto"]:
                    fallos.append(f"{etiqueta}: volvió un texto que se sacó: «{p}»")
            for rx in PROHIBIDOS_REGEX:
                if re.search(rx, l["texto"], re.IGNORECASE):
                    fallos.append(f"{etiqueta}: texto que no es neutro en género: «{l['texto'][:40]}»")
        # superposición entre líneas
        for a in range(len(lineas)):
            for b in range(a + 1, len(lineas)):
                A, B = lineas[a], lineas[b]
                ix = min(A["x1"], B["x1"]) - max(A["x0"], B["x0"])
                iy = min(A["y1"], B["y1"]) - max(A["y0"], B["y0"])
                if ix > 0.5 and iy > 1.0:
                    fallos.append(f"{etiqueta}: se superponen «{A['texto'][:25]}» y «{B['texto'][:25]}»")
        # centrado (hojas en blanco, mensaje de la página 40)
        if info.get("centrado"):
            for l in lineas:
                if l is linea_numero:
                    continue
                if abs((l["x0"] + l["x1"]) / 2 - eje) > 1.5:
                    fallos.append(f"{etiqueta}: «{l['texto'][:30]}» no está centrado ({(l['x0'] + l['x1']) / 2:.1f} mm, eje en {eje:.1f})")
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
        # texto vs dibujos: en las páginas donde hay un dibujo ornamental, ninguna línea de texto lo pisa
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
        # renglones para escribir: #8A8178, 1,5 px de grosor, uno cada 14 mm, sin pisar el texto ni el número
        rayas = _renglones(rellenos)
        largas = [r for r in rayas if r[2] >= g.ANCHO_UTIL - 1]
        cortas = [r for r in rayas if 20 <= r[2] < g.ANCHO_UTIL - 1]
        esperadas = info.get("renglones", 0)
        if len(largas) != esperadas:
            fallos.append(f"{etiqueta}: {len(largas)} renglones para escribir, se esperaban {esperadas}")
        if len(cortas) != info.get("lineas_cortas", 0):
            fallos.append(f"{etiqueta}: {len(cortas)} líneas cortas (Fecha / Para / De), se esperaban {info.get('lineas_cortas', 0)}")
        for r in largas + cortas:
            if abs(r[1] - 0.397) > 0.12:
                fallos.append(f"{etiqueta}: renglón de {r[1]:.2f} mm de grosor (debe ser 1,5 px = 0,40 mm)")
                break
        for a, b in zip(largas, largas[1:]):
            if abs((b[0] - a[0]) - 14.0) > 0.3:
                fallos.append(f"{etiqueta}: renglones separados {b[0] - a[0]:.1f} mm (deben ser 14 mm)")
                break
        for r in largas + cortas:
            for l in lineas:
                if l is not linea_numero and l["y0"] + 1 < r[0] < l["y1"] - 1 and min(l["x1"], r[3] + r[2]) - max(l["x0"], r[3]) > 1:
                    fallos.append(f"{etiqueta}: un renglón pisa el texto «{l['texto'][:25]}»")
                    break
            if linea_numero is not None and r[0] > linea_numero["y0"] - 2:
                fallos.append(f"{etiqueta}: un renglón queda pegado al número de página")
                break
        # hoja en blanco: solo la nota y el número
        if info.get("en_blanco") and info.get("sin_nota"):            # página 42: en blanco del todo, sin nota ni número
            if lineas or dibujos or rellenos:
                fallos.append(f"{etiqueta}: debe estar completamente en blanco (sin nota ni número)")
            img = _raster(ruta_pdf, k + 1, 40).astype(int)
            if (np.abs(img - fondo).sum(axis=2) > 12).any():
                fallos.append(f"{etiqueta}: la página no es del color de fondo liso")
        elif info.get("en_blanco"):
            sin_numero = [l for l in lineas if l is not linea_numero]
            if _norm(" ".join(l["texto"] for l in sin_numero)) != _norm(g.NOTA_BLANCA):
                fallos.append(f"{etiqueta}: la hoja en blanco debe tener solo la nota «{g.NOTA_BLANCA[:30]}…» y el número")
            if dibujos or rellenos:
                fallos.append(f"{etiqueta}: la hoja en blanco tiene dibujos o rayas")
            if sin_numero and linea_numero is not None and max(l["y1"] for l in sin_numero) > linea_numero["y0"] - 0.5:
                fallos.append(f"{etiqueta}: la nota debe quedar arriba del número de página")
            if any(abs(l["pt"] - 18) > 0.3 or l["color"] != "#333333" for l in sin_numero):
                fallos.append(f"{etiqueta}: la nota debe ser de 18 pt en #333")
            if lineas and info.get("numero") is not None:
                img = _raster(ruta_pdf, k + 1, 40).astype(int)
                pxmm = 40 / 25.4
                marca = np.abs(img - fondo).sum(axis=2) > 12
                for l in lineas:                          # lo que no es texto tiene que ser fondo liso
                    xa, xb = int((l["x0"] + ox - 1.5) * pxmm), int((l["x1"] + ox + 1.5) * pxmm)
                    ya, yb = int((l["y0"] + S - 1.5) * pxmm), int((l["y1"] + S + 1.5) * pxmm)
                    marca[max(ya, 0):yb, max(xa, 0):xb] = False
                if marca.any():
                    fallos.append(f"la página {k + 1} (reverso) no está en blanco: {int(marca.sum())} píxeles fuera de la nota y el número")
        # las dos flores de "compartir" empiezan debajo de «Estas dos flores…»
        if info["nombre"] == "compartir" and dibujos:
            nota_flores = [l for l in lineas if _norm(g.COMPARTIR_NOTA)[:25] in _norm(l["texto"])]
            if nota_flores and min(d[1] for d in dibujos) < nota_flores[0]["y1"] - 0.5:
                fallos.append(f"{etiqueta}: las flores deben empezar debajo de «{g.COMPARTIR_NOTA[:30]}…»")

    # Todos los títulos de capítulo y "Todos juntos" con la misma tipografía y tamaño
    pts_titulos = {}
    for k, info in enumerate(paginas_info):
        lineas = texto_por_pagina[k][0]
        n = info["nombre"]
        if n.endswith(("_ejemplo", "_mandala", "_reflexion")) or n in ("integracion", "integracion_ejemplo"):
            candidato = (min(lineas, key=lambda l: l["y0"]) if lineas else None)
            if candidato is not None:
                pts_titulos[f"p.{k + 1}"] = (round(candidato["pt"], 1), candidato["fuente"].split("+")[-1], candidato["texto"])
    if len({(v[0], v[1]) for v in pts_titulos.values()}) != 1:
        fallos.append("los títulos de los capítulos y de «Todos juntos» no tienen el mismo tamaño/tipografía: " +
                      ", ".join(f"{k} {v[2]} {v[0]}" for k, v in list(pts_titulos.items())[:12]))
    else:
        v = next(iter(pts_titulos.values()))
        notas.append(f"títulos de capítulo y «Todos juntos»: {v[0]:g} pt {v[1]} en las {len(pts_titulos)} páginas")

    # Portada: que estén todos los textos pedidos
    if paginas_info[0]["nombre"] == "portada":
        todo = " ".join(l["texto"] for l in texto_por_pagina[0][0])
        for esperado in ("MANDALAS", "CHAKRAS", "Un color a la vez", "Para colorear, reflexionar y disfrutar",
                         "Creado por Dani Navarro", "LIBRO PARA COLOREAR", "Para mamá, con todo mi amor."):
            if esperado not in todo:
                fallos.append(f"portada: falta el texto «{esperado}»")
        if "7" not in todo:
            fallos.append("portada: falta el 7 de «DE LOS 7 CHAKRAS»")

    # Contenido pedido en cada página, con el texto exacto, y su orden de arriba hacia abajo
    for k, info in enumerate(paginas_info):
        lineas = texto_por_pagina[k][0]
        ox = S if info["lado"] == "I" else 0
        eje = g.CX - (g.DESPLAZ_I if info["lado"] == "I" else 0)
        todo = _norm(" ".join(l["texto"] for l in sorted(lineas, key=lambda l: (round(l["y0"]), l["x0"]))))
        for t in _esperado_en_pagina(info, g, edicion):
            if _norm(t) not in todo:
                fallos.append(f"p.{k + 1} {info['nombre']}: falta el texto «{_norm(t)[:60]}»")
        if info["nombre"] == "dedicatoria":
            if edicion == "venta" and ("De:" not in todo or "Dani" in todo):
                fallos.append("dedicatoria (venta): debe tener la línea «De:» y no la firma de Dani")
            if edicion == "mama" and ("Dani" not in todo or "De:" in todo):
                fallos.append("dedicatoria (mamá): debe estar firmada por Dani")
        if info["nombre"] == "garganta_reflexion":
            if edicion == "mama" and ("nieto" not in todo or "alguien que querés" in todo):
                fallos.append("Garganta (mamá): la pregunta debe ser la del nieto")
            if edicion == "venta" and ("nieto" in todo or "alguien que querés mucho" not in todo):
                fallos.append("Garganta (venta): la pregunta debe ser la de «alguien que querés mucho»")
        def pos(frase):
            hit = [l for l in lineas if _norm(frase)[:25] in _norm(l["texto"])]
            return hit[0] if hit else None

        def debajo(a, b, que):
            la, lb = pos(a), pos(b)
            if la and lb and not la["y1"] <= lb["y0"] + 0.5:
                fallos.append(f"p.{k + 1} {info['nombre']}: {que}")

        n = info["nombre"]
        if n.endswith(("_ejemplo", "_mandala")) and info.get("clave"):
            debajo(g.CHAKRAS[[c["clave"] for c in g.CHAKRAS].index(info["clave"])]["nombre"], g.COLOR_PRINCIPAL,
                   "«Color principal» debe ir en una línea propia debajo del título")
        if n.endswith("_mandala"):
            debajo(g.COLOR_PRINCIPAL, g.ANTES_DE_EMPEZAR, "«Antes de empezar…» debe ir debajo del título y de los colores")
            debajo(g.ANTES_DE_EMPEZAR, g.LEER_FRASE, "«Al terminar…» debe ir debajo del mandala")
            la, lb = pos(g.ANTES_DE_EMPEZAR), pos(g.LEER_FRASE)
            if la and info.get("fila_paleta") and la["y0"] < info["fila_paleta"] + 9.5:
                fallos.append(f"p.{k + 1} {n}: «Antes de empezar…» se mete en la fila de colores")
        if n.endswith("_reflexion"):
            d = g._datos_reflexion(next(c for c in g.CHAKRAS if c["clave"] == info["clave"]), edicion)
            debajo(d["parrafo"], g.TITULO_RESPIRAR, "orden de la página de texto: párrafo, respiración, preguntas")
            debajo(d["respiracion"], g.TITULO_RECORDAR, "la respiración debe ir antes de «Un momento para vos»")
            debajo(g.TITULO_RECORDAR, d["preguntas"][0], "las preguntas van debajo de «Un momento para vos»")
            for q1, q2 in zip(d["preguntas"], d["preguntas"][1:]):
                debajo(q1, q2, "las preguntas deben ir una debajo de la otra")
            debajo(d["preguntas"][-1], d["nota"][0], "la nota va debajo de las preguntas")
            for q in d["preguntas"]:
                hit = pos(q)
                if hit and hit["fuente"].find("Bold") < 0:
                    fallos.append(f"p.{k + 1} {n}: la pregunta «{q[:30]}» debe ir en negrita")
        if n == "integracion":
            debajo(g.INTEGRACION_TITULO, g.INTEGRACION_ARRIBA, "«Siete flores…» debe ir debajo del título")
            debajo(g.INTEGRACION_ARRIBA, g.ANTES_DE_EMPEZAR, "«Antes de empezar…» debe ir debajo de la leyenda")
            debajo(g.ANTES_DE_EMPEZAR, g.INTEGRACION_ABAJO, "«Podés usar estos colores…» debe ir debajo del mandala")
            debajo(g.INTEGRACION_ABAJO, g.INTEGRACION_FRASE[0], "la frase final debe ir debajo de «Podés usar estos colores…»")
        if n == "compartir":
            lin = list(g.COMPARTIR_LINEAS)
            for a, b in zip(lin, lin[1:]):
                debajo(a, b, "una idea por línea, en orden")
            debajo(lin[-1], g.COMPARTIR_FRASE, "la frase final va debajo de las ideas")
            debajo(g.COMPARTIR_FRASE, g.COMPARTIR_NOTA, "«Estas dos flores…» va entre el texto y las flores")
        if n == "cierre":
            debajo(g.CIERRE_SENTI, g.CIERRE_AYUDA, "«Puede ser una palabra…» va debajo de «Hoy me sentí…»")
            debajo(g.CIERRE_AYUDA, g.CIERRE_FECHA, "los renglones y la fecha van debajo")
            debajo(g.CIERRE_FECHA, g.CIERRE_NOTA, "la nota final va debajo de la fecha")
        if n in ("contratapa", "cierre_qr") and re.search(r"www|http|\.com|\.ar\b", todo, re.IGNORECASE):
            fallos.append(f"p.{k + 1} {n}: no se escribe la dirección web (solo va dentro del QR)")
        if n == "contratapa" and edicion == "mama":
            titulo = pos(g.CONTRA_MAMA_TITULO)
            if titulo and ("Fraunces" not in titulo["fuente"] or "Bold" not in titulo["fuente"] or titulo["pt"] < 30):
                fallos.append(f"p.{k + 1} {n}: el título debe ir en serif negrita, grande ({titulo['fuente']} {titulo['pt']:.0f} pt)")
            debajo(g.CONTRA_MAMA_TITULO, g.CONTRA_PARA, "«Para:» va debajo del título")
            debajo(g.CONTRA_PARA, g.CONTRA_DE, "«De:» va debajo de «Para:»")
            if re.search(r"Daniela|Longevidad|MenteViva|daninavarro", todo):
                fallos.append(f"p.{k + 1} {n}: la versión de mamá no lleva carta, firma, QR, logo ni usuario")
        if n == "contratapa" and edicion == "venta":
            lin = list(g.CONTRA_LINEAS)
            debajo(g.CONTRA_TITULO, lin[0], "el título va arriba de todo")
            for a, b in zip(lin, lin[1:] + [g.CONTRA_CARINO]):
                debajo(a, b, "los párrafos van en orden, cada uno debajo del anterior")
            debajo(g.CONTRA_CARINO, g.CONTRA_NOMBRE, "la firma va en orden: «Con cariño,», nombre y marca")
            debajo(g.CONTRA_NOMBRE, g.CONTRA_MARCA, "«Longevidad Emocional» va debajo del nombre")
            titulo = pos(g.CONTRA_TITULO)
            if titulo and ("Fraunces" not in titulo["fuente"] or "Bold" not in titulo["fuente"] or titulo["pt"] < 30):
                fallos.append(f"p.{k + 1} {n}: el título debe ir en serif negrita, grande ({titulo['fuente']} {titulo['pt']:.0f} pt)")
            for t, pt_esp, color, serif in ((g.CONTRA_CARINO, 20, "#222222", False), (g.CONTRA_NOMBRE, None, "#222222", True),
                                            (g.CONTRA_MARCA, 18, "#333333", False)):
                l = pos(t)
                if l is None:
                    continue
                if pt_esp and abs(l["pt"] - pt_esp) > 0.3:
                    fallos.append(f"p.{k + 1} {n}: «{t}» debe medir {pt_esp} pt (mide {l['pt']:.1f})")
                if l["color"] != color:
                    fallos.append(f"p.{k + 1} {n}: «{t}» debe ir en {color} (va en {l['color']})")
                if serif and ("Fraunces" not in l["fuente"] or "Bold" not in l["fuente"]):
                    fallos.append(f"p.{k + 1} {n}: «{t}» debe ir en serif negrita")
            for t in lin:
                l = pos(t)
                if l and (abs(l["pt"] - 20) > 0.3 or l["color"] != "#222222"):
                    fallos.append(f"p.{k + 1} {n}: el párrafo «{t[:25]}…» debe ir en 20 pt #222")
            # espacio entre párrafos: más que el que hay entre las líneas de un mismo párrafo
            ls = sorted((l for l in lineas if l["y0"] > pos(lin[0])["y0"] - 1 and l["y1"] < (pos(g.CONTRA_CARINO) or {"y0": 1e9})["y0"]),
                        key=lambda l: l["y0"])
            interno = [b["y0"] - a["y1"] for a, b in zip(ls, ls[1:]) if b["y0"] - a["y1"] < 6]
            entre = [b["y0"] - a["y1"] for a, b in zip(ls, ls[1:]) if b["y0"] - a["y1"] >= 6]
            if len(entre) < len(lin) - 1:
                fallos.append(f"p.{k + 1} {n}: no hay espacio visible entre todos los párrafos")
            elif interno and min(entre) < max(interno) + 2.0:
                fallos.append(f"p.{k + 1} {n}: el espacio entre párrafos ({min(entre):.1f} mm) apenas se nota frente al de las líneas ({max(interno):.1f} mm)")
            if re.search(r"MenteViva|QR|escaneá|@", todo):
                fallos.append(f"p.{k + 1} {n}: el QR, el logo y el usuario van en la página 41, no en la carta")
            notas.append(f"p.{k + 1}: página 40 (venta): carta y firma, título de {info.get('titulo_pt')} pt")
        if n == "cierre_qr":
            debajo(g.QR_TEXTO, g.QR_NOMBRE, "el QR y «MenteViva» van debajo del texto")
            debajo(g.QR_NOMBRE, g.CONTRA_USUARIO, "el logo y el usuario van debajo de «MenteViva»")
            for t, pt_esp, color, serif in ((g.QR_TEXTO, 20, "#222222", False), (g.QR_NOMBRE, None, "#222222", True),
                                            (g.CONTRA_USUARIO, 18, "#333333", False)):
                l = pos(t)
                if l is None:
                    continue
                if pt_esp and abs(l["pt"] - pt_esp) > 0.3:
                    fallos.append(f"p.{k + 1} {n}: «{t[:30]}» debe medir {pt_esp} pt (mide {l['pt']:.1f})")
                if l["color"] != color:
                    fallos.append(f"p.{k + 1} {n}: «{t[:30]}» debe ir en {color} (va en {l['color']})")
                if serif and ("Fraunces" not in l["fuente"] or "Bold" not in l["fuente"]):
                    fallos.append(f"p.{k + 1} {n}: «{t}» debe ir en serif negrita")
            lt, lm, lu = pos(g.QR_TEXTO), pos(g.QR_NOMBRE), pos(g.CONTRA_USUARIO)
            lt = dict(lt, y1=max(l["y1"] for l in lineas if l["y1"] < lm["y0"]))          # el texto tiene dos líneas: se cuenta hasta la última
            img = _raster(ruta_pdf, k + 1, 300).astype(int)
            pxmm = 300 / 25.4
            x_ini, x_fin = int(ox * pxmm), int((ox + g.ANCHO) * pxmm)
            # el QR: lo negro entre el texto y «MenteViva»
            reg_y0, reg_y1 = int((S + lt["y1"] + 1) * pxmm), int((S + lm["y0"]) * pxmm)
            reg = img[reg_y0:reg_y1, x_ini:x_fin]
            negro = reg.max(axis=2) < 110
            if not negro.any():
                fallos.append(f"p.{k + 1} {n}: no se ve el código QR entre el texto y «MenteViva»")
            else:
                ys, xs = np.nonzero(negro)
                lado_mm = (xs.max() - xs.min() + 1) / pxmm
                alto_mm = (ys.max() - ys.min() + 1) / pxmm
                centro = (xs.max() + xs.min()) / 2 / pxmm
                arriba = (reg_y0 + ys.min()) / pxmm - S
                abajo = (reg_y0 + ys.max() + 1) / pxmm - S
                q = info["qr"]
                notas.append(f"p.{k + 1}: QR de {lado_mm:.1f} × {alto_mm:.1f} mm, centrado en {centro:.1f} mm (eje {eje:.1f}); "
                             f"queda a {arriba - lt['y1']:.0f} mm del texto y a {lm['y0'] - abajo:.0f} mm de «MenteViva»")
                if abs(lado_mm - q["lado"]) > 0.5 or abs(alto_mm - q["lado"]) > 0.5:
                    fallos.append(f"p.{k + 1} {n}: el QR mide {lado_mm:.1f} × {alto_mm:.1f} mm y debería medir {q['lado']} mm de lado")
                if min(lado_mm, alto_mm) < 25:
                    fallos.append(f"p.{k + 1} {n}: el QR mide menos de 25 mm")
                if abs(centro - eje) > 1.0:
                    fallos.append(f"p.{k + 1} {n}: el QR no está centrado")
                # margen blanco puro de 4 mm alrededor, y ningún color adentro
                m = int(q["margen"] * pxmm) - 2
                caja = img[reg_y0 + ys.min() - m:reg_y0 + ys.max() + 1 + m, x_ini + xs.min() - m:x_ini + xs.max() + 1 + m]
                borde = np.ones(caja.shape[:2], bool)
                borde[m - 6:-(m - 6), m - 6:-(m - 6)] = False                 # sin el borde suave de los módulos (6 px)
                if (caja[borde].min(axis=1) < 250).any():
                    fallos.append(f"p.{k + 1} {n}: el margen de {q['margen']} mm alrededor del QR no es blanco")
                dentro = img[reg_y0 + ys.min():reg_y0 + ys.max() + 1, x_ini + xs.min():x_ini + xs.max() + 1]
                if int((dentro.max(axis=2) - dentro.min(axis=2) > 12).sum()):
                    fallos.append(f"p.{k + 1} {n}: hay color dentro del QR (debe ser negro sobre blanco)")
                if arriba - 4 < lt["y1"] + 0.5 or abajo + 0.5 > lm["y0"]:
                    fallos.append(f"p.{k + 1} {n}: el QR toca el texto o «MenteViva»")
                try:
                    import zxingcpp
                    pagina_img = np.array(Image.fromarray(img.astype(np.uint8)).convert("L"))
                    leidos = [r.text for r in zxingcpp.read_barcodes(pagina_img)]
                    if leidos != [q["url"]]:
                        fallos.append(f"p.{k + 1} {n}: el QR se lee como {leidos}, debería leerse {q['url']}")
                    else:
                        notas.append(f"p.{k + 1}: el QR se lee bien y lleva a {leidos[0]}")
                except ImportError:
                    notas.append(f"p.{k + 1}: no se pudo leer el QR (falta zxing-cpp); instalalo con pip para probarlo")
            # el isotipo: entre «MenteViva» y el usuario, con aire alrededor, sin fondo y con sus colores
            hueco = lu["y0"] - lm["y1"]
            logo_alto = info.get("logo_ancho", g.LOGO_ANCHO) * g.LOGO_PROPORCION
            if hueco < logo_alto + 2 * 4:
                fallos.append(f"p.{k + 1} {n}: no queda aire para el isotipo entre «MenteViva» y el usuario ({hueco:.0f} mm, hacen falta {logo_alto + 8:.0f})")
            if info.get("logo"):
                reg = img[int((S + lm["y1"] + 1) * pxmm):int((S + lu["y0"] - 1) * pxmm), x_ini:x_fin]
                marca = np.abs(reg - fondo).sum(axis=2) > 30
                if not marca.any():
                    fallos.append(f"p.{k + 1} {n}: el isotipo no se ve en la página")
                else:
                    ys_l, xs_l = np.nonzero(marca)
                    ancho_logo = (xs_l.max() - xs_l.min() + 1) / pxmm
                    centro_logo = (xs_l.max() + xs_l.min()) / 2 / pxmm
                    arriba_l = (int((S + lm["y1"] + 1) * pxmm) + ys_l.min()) / pxmm - S
                    abajo_l = (int((S + lm["y1"] + 1) * pxmm) + ys_l.max() + 1) / pxmm - S
                    notas.append(f"p.{k + 1}: isotipo de {ancho_logo:.1f} mm de ancho (pedido: 25), centrado en {centro_logo:.1f} mm (eje {eje:.1f}); "
                                 f"aire: {arriba_l - lm['y1']:.0f} mm arriba y {lu['y0'] - abajo_l:.0f} mm abajo")
                    if abs(centro_logo - eje) > 1.0:
                        fallos.append(f"p.{k + 1} {n}: el isotipo no está centrado")
                    if abs(ancho_logo - info.get("logo_ancho", g.LOGO_ANCHO)) > 1.0:
                        fallos.append(f"p.{k + 1} {n}: el isotipo mide {ancho_logo:.1f} mm y debería medir {info.get('logo_ancho', g.LOGO_ANCHO)}")
                    if arriba_l - lm["y1"] < 4 or lu["y0"] - abajo_l < 4:
                        fallos.append(f"p.{k + 1} {n}: el isotipo no tiene aire alrededor (menos de 4 mm)")
                    # colores intactos: solo los tres de la marca, sin recuadro ni fondo
                    pix = reg[marca]
                    marca_cols = [HEX(h) for h in ("#8E4E52", "#C2A878", "#E4D3CD")]
                    cerca = np.zeros(len(pix), bool)
                    for c in marca_cols:
                        cerca |= np.abs(pix - c).sum(axis=1) < 24
                    notas.append(f"p.{k + 1}: el {100 * cerca.mean():.0f} % de los píxeles del isotipo son de sus tres colores (el resto son bordes suaves)")
                    if cerca.mean() < 0.9:
                        fallos.append(f"p.{k + 1} {n}: los colores del isotipo no son los de la marca (#8E4E52, #C2A878, #E4D3CD)")
                    fondo_logo = reg[:3, :].reshape(-1, 3)
                    if (np.abs(fondo_logo - fondo).sum(axis=1) > 6).any():
                        fallos.append(f"p.{k + 1} {n}: el isotipo tiene un recuadro o fondo")
            else:
                notas.append(f"PENDIENTE p.{k + 1} (venta): falta el isotipo (assets/isotipo.svg)")
        if info.get("tamanos"):
            notas.append(f"p.{k + 1}: tamaños de la página de texto (título/cuerpo/preguntas) = {info['tamanos']} pt")

    if not completo:
        return fallos, notas

    # Pestaña (8 mm del color del chakra, hasta el borde con sangrado: a la derecha en las páginas derechas,
    # a la izquierda en las izquierdas) y paleta sugerida
    pxmm = 200 / 25.4
    for k, info in enumerate(paginas_info):
        if info.get("en_blanco") or not (info.get("clave") or info.get("a_color") or info.get("paleta")):
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
            todos_colores = list(M.PALETA.values())

            def colores_en(desde, hasta):
                reg = img[int((S + desde) * pxmm):int((S + hasta) * pxmm), int((ox + x_desde) * pxmm):int((ox + x_hasta) * pxmm)]
                return {h: int((np.abs(reg - HEX(h)).sum(axis=2) < 30).sum()) for h in todos_colores}

            if info.get("sin_proporcion"):                # "Todos juntos": los 8 colores en dos filas, en las dos páginas
                fila = colores_en(info["fila_paleta"] - 1, info["fila_paleta"] + 21)
                faltan = set(info["paleta"]) - {h for h, c in fila.items() if c > 150}
                if faltan:
                    fallos.append(f"p.{k + 1}: la leyenda no muestra los 8 colores (faltan {sorted(faltan)})")
                else:
                    notas.append(f"p.{k + 1}: la leyenda de «Todos juntos» muestra los {len(info['paleta'])} colores")
            elif info.get("a_color"):                     # ejemplo pintado: cabecera con el principal; fila de paleta abajo
                cab = colores_en(g.MARGEN_SUP - 1, g.MARGEN_SUP + 27)
                if [h for h, c in cab.items() if c > 150] != [info["protagonista"]]:
                    fallos.append(f"p.{k + 1}: la cabecera debe mostrar solo el color principal")
                fila = colores_en(info["fila_paleta"] - 1, info["fila_paleta"] + 10)
                if sorted(h for h, c in fila.items() if c > 150) != sorted(info["paleta"]):
                    fallos.append(f"p.{k + 1}: la fila de colores no muestra los 5 de la paleta sugerida")
            else:
                cuentas = colores_en(g.MARGEN_SUP - 1, info["fila_paleta"] + 10)
                visibles = [h for h, c in cuentas.items() if c > 150]
                if sorted(visibles) != sorted(info["paleta"]):
                    fallos.append(f"p.{k + 1}: la paleta visible no es la sugerida ({len(visibles)} colores en la cabecera, se esperaban {len(info['paleta'])})")
                elif cuentas[info["protagonista"]] <= max(c for h, c in cuentas.items() if h != info["protagonista"]):
                    fallos.append(f"p.{k + 1}: el color principal no es el que más se ve en la cabecera")

    # Mandalas sin color adentro (para colorear) y grosor de línea medido a 600 dpi:
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
            recorte = img[dentro.any(axis=1)][:, dentro.any(axis=0)]
            if info.get("sin_proporcion"):                 # "Todos juntos": 7 colores + dorado + crema
                partes, ajenos = ejemplos.medir(recorte, info["paleta"] + [ejemplos.CREMA])
                notas.append(f"p.{k + 1}: Todos juntos pintado: " + ", ".join(f"{p * 100:.0f}%" for p in partes))
                if partes.min() < 0.005:
                    fallos.append(f"p.{k + 1}: hay un color del ejemplo casi sin usar")
            else:
                partes, ajenos = ejemplos.medir(recorte, info["paleta"])
                notas.append(f"p.{k + 1}: reparto de colores del ejemplo: " +
                             ", ".join(f"{n} {p * 100:.0f}%" for n, p in zip(M.PALETAS[info["clave"]], partes)))
                lo, hi = ejemplos.rango_protagonista(info["clave"])
                lo, hi = lo - TOLERANCIA_PROTAGONISTA, hi + TOLERANCIA_PROTAGONISTA
                if not lo <= partes[0] <= hi:
                    fallos.append(f"p.{k + 1}: el color principal ocupa {partes[0] * 100:.1f} % de lo pintado "
                                  f"(debe estar entre {lo * 100:.0f} y {hi * 100:.0f} %)")
                if partes.min() < 0.015:
                    fallos.append(f"p.{k + 1}: hay un color de la paleta casi sin usar ({partes.min() * 100:.1f} %)")
            if ajenos > 60:
                fallos.append(f"p.{k + 1}: {ajenos} píxeles con colores que no son de la paleta")
        elif con_color:
            fallos.append(f"p.{k + 1}: hay {con_color} píxeles con color adentro del mandala (debe estar sin colorear)")
        img = _raster(ruta_pdf, k + 1, 600)
        px_mm = 600 / 25.4
        oscuro = img.astype(int).max(axis=2) < 156         # mitad entre la línea (#3A3A3A) y el papel: el grosor real de la línea
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


def _comparar_ediciones(ruta_a, ruta_b, esperadas):
    """Páginas (1-based) donde las dos ediciones se ven distintas; tienen que ser exactamente las esperadas."""
    import subprocess
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        for nombre, ruta in (("a", ruta_a), ("b", ruta_b)):
            subprocess.run(["pdftoppm", "-r", "60", "-png", ruta, f"{tmp}/{nombre}"], check=True)
        pa = sorted(Path(tmp).glob("a-*.png"))
        pb = sorted(Path(tmp).glob("b-*.png"))
        distintas = []
        for i, (a, b) in enumerate(zip(pa, pb), 1):
            ia = ndimage.gaussian_filter(np.array(Image.open(a).convert("L")).astype(float), 1.5)
            ib = ndimage.gaussian_filter(np.array(Image.open(b).convert("L")).astype(float), 1.5)
            # un cambio de texto da miles de píxeles distintos; el ruido de dibujado (medio píxel) no llega a ninguno
            if ia.shape != ib.shape or int((np.abs(ia - ib) > 25).sum()) > 300:
                distintas.append(i)
    return distintas, len(pa), len(pb)


def main():
    import generar_libro as G
    import mandalas as M
    import ejemplos
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
    for ch in G.CHAKRAS:
        clave = ch["clave"]
        pintado = (G.AQUI / "ejemplos" / f"{clave}.svg").read_text(encoding="utf-8")
        base = (G.AQUI / "svg" / f"{clave}.svg").read_text(encoding="utf-8")
        problemas = []
        usados = set(re.findall(r'fill="(#[0-9A-Fa-f]{6})"', pintado)) - {"#FFFFFF", M.NEGRO, M.BLANCO}
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
        lo, hi = ejemplos.rango_protagonista(clave)
        if not lo - TOLERANCIA_PROTAGONISTA <= prot <= hi + TOLERANCIA_PROTAGONISTA:
            problemas.append(f"el color principal ocupa {prot * 100:.1f} % de lo pintado (debe estar entre {lo * 100:.0f} y {hi * 100:.0f} %)")
        print(f"  {ch['nombre']}: " + " · ".join(f"{n} {p * 100:.0f}%" for n, p in partes.items()))
        for p in problemas:
            print("    ✗", p)
        problemas_total += len(problemas)
    pintado = (G.AQUI / "ejemplos" / "integracion.svg").read_text(encoding="utf-8")
    base = (G.AQUI / "svg" / "integracion.svg").read_text(encoding="utf-8")
    problemas = []
    usados = set(re.findall(r'fill="(#[0-9A-Fa-f]{6})"', pintado)) - {"#FFFFFF", M.NEGRO, M.BLANCO}
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
    # todas las líneas en gris #3A3A3A (ni negro puro ni otros tonos)
    otros = set()
    for archivo in list((G.AQUI / "svg").glob("*.svg")) + list((G.AQUI / "ejemplos").glob("*.svg")):
        if archivo.name == "portada_arte.svg":
            continue
        otros |= set(re.findall(r'stroke="(#[0-9A-Fa-f]{6})"', archivo.read_text(encoding="utf-8"))) - {NEGRO_LINEA}
    if M.NEGRO != NEGRO_LINEA:
        print(f"    ✗ el color de línea es {M.NEGRO}, debe ser {NEGRO_LINEA}")
        problemas_total += 1
    if otros:
        print(f"    ✗ líneas que no son {NEGRO_LINEA}:", sorted(otros))
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
    rutas = {ed: G.AQUI / arch for ed, arch in G.EDICIONES.items()}
    faltan = [r.name for r in rutas.values() if not r.exists()]
    if faltan:
        print("  (faltan PDF generados:", ", ".join(faltan), ")")
        return 1
    for edicion, pdf in rutas.items():
        info = G.informacion_paginas(edicion)
        # la portada tiene sus propios márgenes (los de la tarjeta)
        info[0]["x_limites"] = (15.0, G.ANCHO - 15.0)
        info[0]["y_limites"] = (G.MARGEN_SUP, G.ALTO - G.MARGEN_INF)
        fallos, notas = verificar_pdf(str(pdf), info, G, edicion=edicion, completo=(edicion == "venta"))
        print(f"  {pdf.name}: {len(info)} páginas impresas" + ("" if edicion == "venta" else " (controles de texto; los de imagen son los de la otra edición)"))
        for n in notas:
            print("   ·", n)
        for f in fallos:
            print("    ✗", f)
        problemas_total += len(fallos)
    distintas, n_venta, n_mama = _comparar_ediciones(str(rutas["venta"]), str(rutas["mama"]), (3, 25, 40))
    errores = []
    if (n_venta, n_mama) != (42, 40):
        errores.append(f"se esperaban 42 páginas (venta: con el QR en la 41 y la 42 en blanco) y 40 (mamá); hay {n_venta} y {n_mama}")
    if distintas != [3, 25, 40]:
        errores.append(f"las ediciones tienen que diferir solo en las páginas 3 (De:/firma), 25 (Garganta) y 40 (las páginas 41 y 42 son solo de la edición para vender); difieren en {distintas}")
    print(f"  ediciones comparadas página por página (las {min(n_venta, n_mama)} primeras): difieren en {distintas}"
          + (f" (dedicatoria, Garganta y página 40, como se pidió); venta {n_venta} páginas, mamá {n_mama}" if not errores else ""))
    for e in errores:
        print("    ✗", e)
    problemas_total += len(errores)
    print("\nRESULTADO:", "todo en orden ✔" if problemas_total == 0 else f"{problemas_total} problema(s) ✗")
    return 0 if problemas_total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
