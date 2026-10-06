# Mandalas con Mente Viva · Cuaderno 1

Sistema para armar el cuadernillo cognitivo de la línea Mente Viva
(Daniela Navarro · Longevidad Emocional): páginas en HTML/CSS → PDF con
WeasyPrint, mandalas vectoriales generados por código.

```
cuadernillo/
├── config.json            paleta, tipografía, formato (A4 activo / KDP preparado), reglas de mandalas
├── construir.py           arma salida/muestra.pdf + salida/png/
├── verificar.py           controles antes de entregar (tamaños, márgenes, fuentes, mandalas…)
├── graficos.py            íconos de nivel, símbolos para tachar, caritas
├── mandalas/generador.py  generador paramétrico de mandalas (SVG)
├── contenido/
│   ├── cuaderno.json      orden de las páginas
│   ├── como_usar.json
│   └── sesiones/sesion_NN.json
├── plantillas/            Jinja2: estilos, páginas y bloques de ejercicios
├── fuentes/               Fraunces y Manrope (SIL OFL), se incrustan en el PDF
└── salida/                muestra.pdf, png/, mandalas/ (SVG sueltos)
```

## Uso

```bash
pip install -r requirements.txt     # requiere también poppler-utils (pdftoppm, pdffonts)
python construir.py                 # PDF + PNG
python verificar.py                 # tiene que terminar en "✔ Todo verificado"
```

## Cómo agregar la sesión siguiente

1. Copiá `contenido/sesiones/sesion_01.json` como `sesion_02.json` (el nombre
   define el orden; se toman solas todas las `sesion_*.json`).
2. Cambiá `numero`, `nivel` (`semilla` | `brote` | `flor`) y los textos.
3. En `pagina_b.mandala` elegí el modo y una **semilla** nueva:
   - `"numerado"`: colorear por código (leyenda de 4 colores).
   - `"simetria"`: mitad derecha en blanco para completar.
   - `"libre"`: el mandala completo para pintar a gusto.
   Opcionales: `petalos` (6, 8, 10, 12…) y `anillos`.
4. `python construir.py && python verificar.py` y mirá los PNG.

Para ver muchos diseños antes de elegir semilla:

```bash
python -m mandalas.generador brote 14     # imprime la verificación de esa semilla
```

### Tipos de bloque disponibles (página A)

| tipo        | campos principales |
|-------------|--------------------|
| `tachar`    | `objetivo`, `distractores`, `filas`, `columnas`, `cantidad`, `semilla` |
| `palabras`  | `palabras` (3), `ayuda` |
| `series`    | `ejemplo` {items, respuesta, pista}, `series` [{items, respuesta, pista}] |
| `conversar` | `pregunta`, `nota`, `lineas` |
| `fluidez`   | `ejemplo`, `lineas`, `columnas`, `ideas` (para soluciones) |
| `agrupar`   | `palabras`, `categorias` {nombre: [palabras]}, `ejemplo` |
| `ordenar`   | `pasos` (orden correcto), `orden_mostrado`, `ejemplo` |

Las soluciones se arman solas a partir de esos datos. Un tipo nuevo se agrega
en `plantillas/bloques.j2` (macros `bloque` y `solucion`).

## Reglas que controla `verificar.py`

- Ninguna página se desborda; nada fuera de los márgenes de 15 mm.
- Ningún texto menor a 16 pt (números de mandala a 16 pt).
- Fuentes incrustadas y solo Fraunces / Manrope.
- Ninguna palabra de `palabras_prohibidas` en el PDF ni en los JSON.
- Mandalas: regiones cerradas, partición exacta, cantidad por nivel
  (Semilla 12-24, Brote 25-40, Flor 40-60), área mínima, cada número con
  espacio libre, simetría espejo exacta, diámetro 170 mm, trazo negro 2 pt,
  sin grises ni rellenos en las páginas de colorear.

## Formato KDP

`config.json → formatos.kdp_carta` ya tiene 8,5 × 11 in con 0,125 in de
sangrado (hoja de 8,625 × 11,25 in, margen interior de lomo de 0,75 in).
Se activa cambiando `formato_activo` a `"kdp_carta"`. Todavía no se usa:
la hoja es 17,6 mm más baja que A4 y hoy varias páginas se desbordan
(`verificar.py` lo marca). Antes de pasar a KDP hay que bajar el mandala a
~160 mm o reacomodar los cierres.

## Fuentes

`fuentes/variables/` tiene los archivos originales de Google Fonts.
`python fuentes/preparar_fuentes.py` regenera las instancias estáticas.
Licencias en `fuentes/OFL-*.txt`.

## Portadas "Mandalas de los Chakras"

`python portada_chakras.py` genera dos tapas con 7 lotos vectoriales:

- `salida/portada_regalo.pdf`: A4 sin sangrado, con dedicatoria y sin "para Adultos Mayores".
- `salida/portada_amazon.pdf`: tapa frontal KDP 8,625 × 11,25 in (8,5 × 11 + sangrado),
  con "para Adultos Mayores", texto dentro de la zona segura de 0,375 in.
  Para subir a KDP falta la tapa completa (contratapa + lomo), que depende de la
  cantidad de páginas del interior.

Los textos de cada versión están en `VARIANTES`, dentro del script.

## Libro "Mandalas de los Chakras" (7 capítulos × 3 sesiones)

- `config.json → capitulos`: chakra, color, nivel, sesiones, frase y tema de cada
  capítulo. Cada sesión toma el color de su capítulo (acentos, íconos, leyenda de
  colores para pintar) y antes de la primera sesión de cada capítulo se agrega su
  página de apertura.
- Lotos para colorear: `"mandala": {"tipo": "loto", "modo": "numerado" | "simetria" | "libre", "nivel": ...}`
  (`mandalas/loto.py`). Pasan las mismas verificaciones que los mandalas.
- Cada sesión puede llevar `"frase"` (frase del día, arriba de la página A).
- Encuadernación espiralada: margen de 20 mm del lado del espiral
  (`formatos.a4.margen_interior_mm`), alternando izquierda/derecha.
- La portada de regalo se antepone sola al PDF (`{"plantilla": "portada_chakras"}` en `cuaderno.json`).
