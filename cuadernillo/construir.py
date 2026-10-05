"""Arma el cuadernillo: lee config.json y contenido/*.json, genera los mandalas,
renderiza las plantillas HTML/CSS y exporta PDF (WeasyPrint) + PNG por página.

    python construir.py              # salida/muestra.pdf + salida/png/*.png
    python construir.py --sin-png    # solo el PDF
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from weasyprint import HTML

import graficos as g
from mandalas.generador import MM_POR_PT, generar

RAIZ = Path(__file__).parent
CONTENIDO = RAIZ / "contenido"
NOMBRES_NIVEL = {"semilla": "Semilla", "brote": "Brote", "flor": "Flor"}


def cargar(ruta: Path):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


# --------------------------------------------------------------------------
# Mandalas
# --------------------------------------------------------------------------

def preparar_mandala(spec: dict, cfg: dict, diametro_mm: float | None = None) -> dict:
    mc = cfg["mandalas"]
    d = diametro_mm or mc["diametro_mm"]
    simetrico = spec.get("modo") == "simetria" or spec.get("simetria", True)
    m = generar(spec["nivel"], spec["semilla"], petalos=spec.get("petalos"),
                anillos=spec.get("anillos"), simetria=simetrico)
    rellenos = {int(k): v["hex"] for k, v in cfg["colores_para_pintar"].items()}
    datos = {"obj": m, "diametro": d, "verificacion": m.verificar(), "numeros": []}
    modo = spec.get("modo", "libre")
    datos["svg"] = m.svg("simetria" if modo == "simetria" else "libre", diametro_mm=d,
                         trazo_pt=mc["trazo_pt"])
    datos["lado_mm"] = d + mc["trazo_pt"] * MM_POR_PT
    if modo == "numerado":
        esc = d / (2 * m.radio)
        c = datos["lado_mm"] / 2
        datos["numeros"] = [(c + x * esc, c + y * esc, cod) for x, y, cod in m.numeros()]
    # versiones chicas para la página de soluciones
    if modo == "numerado":
        datos["svg_solucion"] = m.svg("color", diametro_mm=52, trazo_pt=1.2, rellenos=rellenos)
    else:
        datos["svg_solucion"] = m.svg("libre", diametro_mm=52, trazo_pt=1.2)
    return datos


def color_portada(r, p: dict) -> str:
    """Relleno por anillos para la portada: rosa ceniza y dorado alternados."""
    pares = [(p["rosa_ceniza"], p["rosa_palido"]), (p["dorado"], p["dorado_palido"]),
             (p["rosa_palido"], p["papel"]), (p["dorado"], p["rosa_ceniza"])]
    if r.tipo == "centro":
        return p["dorado"]
    fuerte, suave = pares[(r.anillo - 1) % len(pares)]
    if r.tipo == "petalo_interior":
        return suave
    if r.tipo == "hueco":
        return suave
    return fuerte if r.j % 2 == 0 or r.tipo == "petalo" else suave


def guardar_svgs(nombre: str, m, cfg: dict):
    """Exporta las tres versiones del mandala como archivos SVG sueltos."""
    dest = RAIZ / "salida" / "mandalas"
    dest.mkdir(parents=True, exist_ok=True)
    mc = cfg["mandalas"]
    rellenos = {int(k): v["hex"] for k, v in cfg["colores_para_pintar"].items()}
    (dest / f"{nombre}_libre.svg").write_text(m.svg("libre", trazo_pt=mc["trazo_pt"]))
    (dest / f"{nombre}_color.svg").write_text(m.svg("color", trazo_pt=mc["trazo_pt"], rellenos=rellenos))
    if m.simetrico:
        (dest / f"{nombre}_simetria.svg").write_text(m.svg("simetria", trazo_pt=mc["trazo_pt"]))
    (dest / f"{nombre}.json").write_text(json.dumps(m.describir(), ensure_ascii=False, indent=2))


# --------------------------------------------------------------------------
# Bloques de ejercicios: datos calculados + solución
# --------------------------------------------------------------------------

def preparar_bloque(b: dict, cfg: dict) -> dict:
    p = cfg["paleta"]
    b = dict(b)
    b["icono"] = g.icono_ejercicio(b["tipo"], p["rosa_ceniza"], 8)
    if b["tipo"] == "tachar":
        grilla = g.grilla_tachar(b)
        b["svg_grilla"] = g.svg_grilla(grilla, 10, p["cacao"])
        b["svg_ejemplo"] = g.svg_simbolo_tachado(b["objetivo"], 13, p["cacao"], p["rosa_ceniza"])
        b["svg_solucion"] = g.svg_grilla(grilla, 6.2, p["cacao"], trazo_pt=1.4,
                                         marcar=b["objetivo"], color_marca=p["rosa_ceniza"])
        b["cuenta"] = sum(f.count(b["objetivo"]) for f in grilla)
    elif b["tipo"] == "ordenar":
        b["filas"] = [{"n": i + 1, "texto": b["pasos"][i], "ejemplo": i == b.get("ejemplo")}
                      for i in b["orden_mostrado"]]
    elif b["tipo"] == "agrupar":
        ej = b.get("ejemplo") or {}
        b["columnas_cat"] = [{"nombre": n, "ejemplo": ej.get("palabra") if ej.get("categoria") == n else None}
                             for n in b["categorias"]]
    return b


def preparar_sesion(ses: dict, cfg: dict) -> dict:
    ses = dict(ses)
    ses["nombre_nivel"] = NOMBRES_NIVEL[ses["nivel"]]
    ses["icono"] = g.icono_nivel(ses["nivel"], cfg["paleta"]["rosa_ceniza"], cfg["paleta"]["rosa_palido"], 9)
    ses["icono_chico"] = g.icono_nivel(ses["nivel"], cfg["paleta"]["rosa_ceniza"], cfg["paleta"]["rosa_palido"], 7)
    ses["bloques"] = [preparar_bloque(b, cfg) for b in ses["pagina_a"]["bloques"]]
    pb = dict(ses["pagina_b"])
    pb["mandala_datos"] = preparar_mandala(pb["mandala"], cfg)
    guardar_svgs(f"sesion_{ses['numero']:02d}", pb["mandala_datos"]["obj"], cfg)
    ses["pagina_b"] = pb
    return ses


def cargar_sesiones(spec) -> list[dict]:
    if spec == "todas":
        rutas = sorted((CONTENIDO / "sesiones").glob("sesion_*.json"))
    else:
        rutas = [CONTENIDO / "sesiones" / r for r in spec]
    sesiones = [cargar(r) for r in rutas]
    return sorted(sesiones, key=lambda s: s["numero"])


# --------------------------------------------------------------------------
# Armado
# --------------------------------------------------------------------------

def armar_html(cfg: dict) -> tuple[str, list[dict]]:
    cuaderno = cargar(CONTENIDO / "cuaderno.json")
    p = cfg["paleta"]
    formato = cfg["formatos"][cfg["formato_activo"]]

    paginas, sesiones = [], []
    for item in cuaderno["paginas"]:
        pl = item["plantilla"]
        if pl == "portada":
            md = preparar_mandala({**item["mandala"], "modo": "libre"}, cfg, diametro_mm=100)
            m = md["obj"]
            md["svg"] = m.svg("color", diametro_mm=100, trazo_pt=1.2, color_trazo=p["cacao"],
                              rellenos=lambda r: color_portada(r, p))
            guardar_svgs("portada", m, cfg)
            paginas.append({"plantilla": "portada", "mandala": md,
                            "adorno": g.adorno(p["rosa_ceniza"], 46),
                            "esquinero": g.esquinero(p["rosa_ceniza"], 14)})
        elif pl == "como_usar":
            datos = cargar(CONTENIDO / item["contenido"])
            for n in datos["niveles"]:
                n["icono"] = g.icono_nivel(n["id"], p["rosa_ceniza"], p["rosa_palido"], 11)
            paginas.append({"plantilla": "como_usar", "datos": datos})
        elif pl == "sesiones":
            for s in cargar_sesiones(item["sesiones"]):
                s = preparar_sesion(s, cfg)
                sesiones.append(s)
                paginas.append({"plantilla": "sesion_a", "sesion": s})
                paginas.append({"plantilla": "sesion_b", "sesion": s})
        elif pl == "soluciones":
            paginas.append({"plantilla": "soluciones", "sesiones": sesiones})
        else:
            raise ValueError(f"plantilla desconocida: {pl}")

    for i, pg in enumerate(paginas, start=1):
        pg["numero"] = i

    env = Environment(loader=FileSystemLoader(RAIZ / "plantillas"), undefined=StrictUndefined,
                      autoescape=False, trim_blocks=True, lstrip_blocks=True)
    caritas = {t: g.carita(t, p["cacao"], 15) for t in ("bien", "regular", "costo")}
    html = env.get_template("cuaderno.html.j2").render(
        cfg=cfg, p=p, formato=formato, paginas=paginas, caritas=caritas,
        fuentes=(RAIZ / "fuentes").as_uri(), producto=cfg["producto"],
        colores=cfg["colores_para_pintar"])
    return html, paginas


def exportar_png(pdf: Path, carpeta: Path, dpi: int):
    carpeta.mkdir(parents=True, exist_ok=True)
    for viejo in carpeta.glob("pagina-*.png"):
        viejo.unlink()
    subprocess.run(["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(carpeta / "pagina")], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-png", action="store_true")
    args = ap.parse_args()

    cfg = cargar(RAIZ / "config.json")
    html, paginas = armar_html(cfg)
    salida = RAIZ / cfg["salida"]["pdf"]
    salida.parent.mkdir(parents=True, exist_ok=True)
    (RAIZ / "salida" / "cuaderno.html").write_text(html, encoding="utf-8")
    HTML(string=html, base_url=str(RAIZ)).write_pdf(salida)
    print(f"PDF: {salida.relative_to(RAIZ)} ({len(paginas)} páginas esperadas)")
    for pg in paginas:
        s = pg.get("sesion")
        if s and pg["plantilla"] == "sesion_b":
            v = s["pagina_b"]["mandala_datos"]["verificacion"]
            print(f"  mandala sesión {s['numero']}: {v['regiones']} regiones, ok={v['ok']}")
    if not args.sin_png and shutil.which("pdftoppm"):
        exportar_png(salida, RAIZ / cfg["salida"]["png_dir"], cfg["salida"]["png_dpi"])
        print(f"PNG: {cfg['salida']['png_dir']}/")


if __name__ == "__main__":
    main()
