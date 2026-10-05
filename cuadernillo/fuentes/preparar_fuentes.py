"""Genera instancias estáticas de Fraunces y Manrope a partir de las fuentes
variables de Google Fonts (licencia SIL OFL 1.1, ver OFL-*.txt).

Las instancias estáticas se incrustan en el PDF de forma más predecible que
las variables. Se corre una sola vez (o si se cambian los pesos):

    python fuentes/preparar_fuentes.py
"""
from pathlib import Path

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

AQUI = Path(__file__).parent
VARIABLES = AQUI / "variables"

INSTANCIAS = {
    # archivo destino: (fuente variable, ejes, nombre de estilo)
    "Fraunces-SemiBold.ttf": ("Fraunces-VF.ttf", {"wght": 600, "opsz": 72, "SOFT": 50, "WONK": 0}, "SemiBold"),
    "Fraunces-Regular.ttf": ("Fraunces-VF.ttf", {"wght": 400, "opsz": 36, "SOFT": 50, "WONK": 0}, "Regular"),
    "Fraunces-Italic.ttf": ("Fraunces-Italic-VF.ttf", {"wght": 400, "opsz": 36, "SOFT": 50, "WONK": 1}, "Italic"),
    "Manrope-Medium.ttf": ("Manrope-VF.ttf", {"wght": 500}, "Medium"),
    "Manrope-Bold.ttf": ("Manrope-VF.ttf", {"wght": 700}, "Bold"),
    "Manrope-ExtraBold.ttf": ("Manrope-VF.ttf", {"wght": 800}, "ExtraBold"),
}


def main():
    for destino, (origen, ejes, estilo) in INSTANCIAS.items():
        fuente = TTFont(VARIABLES / origen)
        estatica = instantiateVariableFont(fuente, ejes, updateFontNames=False)
        familia = origen.split("-")[0]
        nombre = estatica["name"]
        for plat in ((3, 1, 0x409), (1, 0, 0)):
            nombre.setName(f"{familia} {estilo}", 4, *plat)
            nombre.setName(f"{familia}-{estilo}", 6, *plat)
            nombre.setName(estilo, 2, *plat)
        estatica.save(AQUI / destino)
        print("ok", destino)


if __name__ == "__main__":
    main()
