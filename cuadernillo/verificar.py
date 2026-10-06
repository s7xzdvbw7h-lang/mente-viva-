"""Verificación antes de entregar. Corre sobre salida/muestra.pdf:

  1. cantidad de páginas esperada (nada se desbordó a otra página)
  2. ningún texto menor a 16 pt
  3. nada (texto ni dibujo) se sale del margen
  4. fuentes incrustadas (pdffonts) y solo Fraunces / Manrope
  5. palabras prohibidas
  6. mandalas: regiones cerradas, partición sin huecos ni superposiciones,
     cantidad por nivel, área mínima, números que entran, simetría,
     trazo negro >= 1,5 pt, sin grises ni rellenos en las páginas de colorear

    python verificar.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

import pymupdf as fitz

import construir
from mandalas.generador import MM_POR_PT

RAIZ = Path(__file__).parent
PT_POR_MM = 72 / 25.4
TOL_MM = 0.3

fallas: list[str] = []


def ok(cond: bool, texto: str):
    print(("  ✔ " if cond else "  ✘ ") + texto)
    if not cond:
        fallas.append(texto)


def sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def main():
    cfg = construir.cargar(RAIZ / "config.json")
    fmt = cfg["formatos"][cfg["formato_activo"]]
    pdf_path = RAIZ / cfg["salida"]["pdf"]
    doc = fitz.open(pdf_path)
    _, paginas = construir.armar_html(cfg)

    print("1. Páginas")
    # cada página fija ocupa exactamente una hoja; las soluciones pueden seguir
    # en varias hojas cuando hay muchas sesiones
    sol = next((pg for pg in paginas if pg["plantilla"] == "soluciones"), None)
    if sol:
        inicio = next((i for i, page in enumerate(doc, 1)
                       for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
                       for s in l["spans"] if s["text"].strip() == "Soluciones" and s["size"] >= 26), None)
        ok(inicio == sol["numero"], f"ninguna página se desbordó: las soluciones empiezan en la pág. {inicio} "
                                    f"(esperada {sol['numero']})")
        ok(len(doc) >= len(paginas), f"{len(doc)} páginas en el PDF ({len(paginas) - 1} fijas + soluciones)")
    else:
        ok(len(doc) == len(paginas), f"{len(doc)} páginas en el PDF, {len(paginas)} esperadas")

    print("2. Tamaño mínimo de texto")
    minimo = cfg["tipografia"]["tamanio_minimo_pt"]
    peor = (99, "", 0)
    for i, page in enumerate(doc, 1):
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip() and s["size"] < peor[0]:
                        peor = (s["size"], s["text"].strip(), i)
    ok(peor[0] >= minimo - 0.05, f"texto más chico: {peor[0]:.2f} pt (pág. {peor[2]}: «{peor[1][:30]}»)")

    print("3. Márgenes")
    m = (fmt["margen_mm"] + fmt["sangrado_mm"]) * PT_POR_MM
    mi = fmt.get("margen_interior_mm", fmt["margen_mm"]) * PT_POR_MM
    tol = TOL_MM * PT_POR_MM
    for i, page in enumerate(doc, 1):
        W, H = page.rect.width, page.rect.height
        izq, der = (mi, m) if i % 2 else (m, mi)   # impares = páginas derechas
        if i <= len(paginas) and paginas[i - 1]["plantilla"].startswith("portada"):
            izq = der = m                            # la tapa no lleva margen de espiral
        caja = fitz.Rect(izq - tol, m - tol, W - der + tol, H - m + tol)
        fuera = []
        for d in page.get_drawings():
            r = fitz.Rect(d["rect"])
            w = (d.get("width") or 0) / 2 if d.get("color") else 0
            r = fitz.Rect(r.x0 - w, r.y0 - w, r.x1 + w, r.y1 + w)
            if not caja.contains(r):
                fuera.append(f"dibujo {tuple(round(v / PT_POR_MM, 1) for v in r)}")
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip() and not caja.contains(fitz.Rect(s["bbox"])):
                        fuera.append(f"texto «{s['text'][:20]}»")
        ok(not fuera, f"pág. {i}: todo dentro del margen de {fmt['margen_mm']} mm"
           + (f" — fuera: {fuera[:3]}" if fuera else ""))

    print("4. Fuentes incrustadas (pdffonts)")
    salida = subprocess.run(["pdffonts", str(pdf_path)], capture_output=True, text=True, check=True).stdout
    print("     " + salida.replace("\n", "\n     ").rstrip())
    filas = salida.strip().splitlines()[2:]
    ok(len(filas) > 0 and all(f.split()[-5] == "yes" for f in filas), "todas las fuentes incrustadas (emb = yes)")
    familias = {re.sub(r"^[A-Z]{6}\+", "", f.split()[0]).split("-")[0] for f in filas}
    ok(familias <= {"Fraunces", "Manrope"}, f"familias usadas: {sorted(familias)}")

    print("5. Palabras prohibidas")
    texto = sin_tildes(" ".join(p.get_text() for p in doc))
    fuentes_txt = sin_tildes(" ".join(p.read_text(encoding="utf-8")
                                      for p in (RAIZ / "contenido").rglob("*.json")))
    for palabra in cfg["palabras_prohibidas"]:
        patron = r"\b" + re.escape(sin_tildes(palabra)) + r"\b"
        ok(not re.search(patron, texto) and not re.search(patron, fuentes_txt), f"no aparece «{palabra}»")

    print("6. Mandalas")
    for pg in paginas:
        if pg["plantilla"] != "sesion_b":
            continue
        s = pg["sesion"]
        md = s["pagina_b"]["mandala_datos"]
        v = md["verificacion"]
        modo = s["pagina_b"]["mandala"]["modo"]
        print(f"   Sesión {s['numero']} ({s['nivel']}, {modo}) → {json.dumps(v, ensure_ascii=False)}")
        ok(v["todas_cerradas"], "todas las regiones son polígonos cerrados y válidos")
        ok(v["particion_sin_huecos"] and v["sin_superposiciones"], "partición exacta: sin huecos ni superposiciones")
        ok(v["en_rango"], f"{v['regiones']} regiones (nivel {s['nivel']}: {v['rango_nivel'][0]}-{v['rango_nivel'][1]})")
        ok(v["area_ok"], f"área mínima {v['area_min_cm2']} cm²")
        if modo == "numerado":
            ok(v["numeros_entran"], f"cada número tiene {v['radio_libre_min_mm']} mm libres alrededor")
            ok(v["colores_vecinos_distintos"], "zonas vecinas con números distintos")
        if modo == "simetria":
            ok(v.get("simetria_espejo", False), "la mitad derecha es espejo exacto de la izquierda")
        diam = md["diametro"]
        ok(170 <= diam <= 180, f"diámetro {diam:.0f} mm")

        page = doc[pg["numero"] - 1]
        negros = [d for d in page.get_drawings() if d.get("color") and
                  all(abs(c) < 1e-3 for c in d["color"]) and d.get("width")]
        if not negros:
            ok(False, "no se encontraron trazos negros del mandala")
            continue
        bbox = fitz.Rect(negros[0]["rect"])
        for d in negros:
            bbox |= d["rect"]
        gruesos = [d for d in negros if d["width"] >= cfg["mandalas"]["trazo_pt"] - 0.01]
        medido = max(bbox.width, bbox.height) / PT_POR_MM  # alto: la mitad derecha queda en blanco
        ok(abs(medido - diam) < 1.5, f"mandala medido en el PDF: {medido:.1f} mm")
        ok(min(d["width"] for d in negros) >= cfg["mandalas"]["trazo_minimo_pt"] - 0.01,
           f"trazo negro: {max(d['width'] for d in negros):.2f} pt (mínimo {min(d['width'] for d in negros):.2f} pt)")
        continuos = [d for d in negros if not (d.get("dashes") or "").strip("[] 0")]
        ok(all(d["width"] >= cfg["mandalas"]["trazo_pt"] - 0.01 for d in continuos),
           f"contornos de regiones a {cfg['mandalas']['trazo_pt']:.0f} pt "
           f"({len(continuos)} trazos continuos; las guías punteadas pueden ser más finas)")
        grises = []
        for d in page.get_drawings():
            if not bbox.intersects(d["rect"]) or d in negros:
                continue
            f = d.get("fill")
            if f is not None and not all(c > 0.999 for c in f):
                grises.append(f)
        ok(not grises, "página de colorear: sin grises ni rellenos dentro del mandala")
        if modo == "numerado":
            nums = [sp for b in page.get_text("dict")["blocks"] for l in b.get("lines", [])
                    for sp in l["spans"] if bbox.contains(fitz.Rect(sp["bbox"])) and sp["text"].strip()]
            ok(len(nums) == v["regiones"], f"{len(nums)} números impresos para {v['regiones']} regiones")
            ok(all(sp["size"] >= cfg["mandalas"]["numero_pt"] - 0.05 and sp["color"] == 0 for sp in nums),
               f"números a {cfg['mandalas']['numero_pt']} pt en negro")

    print()
    if fallas:
        print(f"✘ {len(fallas)} verificación(es) fallaron")
        sys.exit(1)
    print("✔ Todo verificado")


if __name__ == "__main__":
    main()
