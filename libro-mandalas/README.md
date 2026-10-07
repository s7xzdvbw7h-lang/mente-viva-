# Mandalas de los chakras · Un color a la vez

Libro para colorear imprimible (A4, una sola cara). Creado por Dani Navarro.
Los mandalas se calculan con geometría (no son imágenes): salen como SVG vectorial y se arman en PDF.

## Regenerar el libro

    pip install -r requirements.txt     # una sola vez (y poppler, ver requirements.txt)
    python3 generar_libro.py            # el libro completo (19 páginas impresas)
    python3 verificar.py                # controles de calidad

Salen: `libro_mandalas_chakras.pdf`, un PNG por página en `preview/` y cada mandala en `svg/`.
(`--fase 1` arma solo portada, dedicatoria, cómo usar y Raíz.)
El PDF trae una hoja en blanco detrás de cada página, para que el marcador no traspase
(38 hojas en total). Si imprimís en una sola cara, imprimí solo las páginas impares.

## Cómo está armado

| Página | Contenido |
|---|---|
| 1 | Portada (sin número) |
| 2 | Dedicatoria (sin número) |
| 3 | Cómo usar este libro |
| 4–17 | 7 capítulos de 2 páginas: primero el mandala (con la frase para leer al terminar), después la pregunta |
| 18 | Todos juntos: los siete chakras en un solo mandala, con la leyenda de colores |
| 19 | Cierre: frase final y renglones para "Hoy me sentí…" y "Fecha:" |

Cada chakra tiene su propia forma (en `mandalas.py`): Raíz 4 pétalos y cuadrado, Sacro 6 y luna,
Plexo solar 10 y triángulo, Corazón 12 y hexagrama, Garganta 16 y círculo con perlas, Tercer ojo 2 pétalos
grandes y un ojo, Corona un loto de tres capas (30 pétalos). Las zonas para pintar crecen de 27 (Raíz) a 64 (Corona).

## Dónde se editan los textos

Todo está al principio de `generar_libro.py`: `DEDICATORIA`, `COMO_USAR_PASOS`, `CHAKRAS`
(nombre, "Está en", emoción, afirmación, respiración y pregunta de cada chakra), `INTEGRACION_*`,
`CIERRE_*`, `FRASE_FINAL` y los textos de la portada.

## Qué controla `verificar.py`

- Mandalas (los 7 chakras, el de integración y el corazón de la dedicatoria): cantidad de zonas, que ninguna mida menos de 8 mm, que no haya líneas cortadas,
  cantidad de pétalos de cada chakra y grosor de línea (medido en el PDF, entre 2,5 y 3 px).
- Páginas: texto de 18 pt o más (número de página 16 pt, frases de 30 pt o más), márgenes de 15 mm,
  textos que no se superpongan ni toquen el mandala, fuentes incrustadas, reversos en blanco,
  pestaña de 8 mm y que la frase aparezca una sola vez por capítulo.
- Portada: se compara con `referencia/portada_original.png` (el diseño original de Dani).

## Tipografías

Fraunces (títulos) y Manrope (texto), de Google Fonts, con licencia OFL (en `fuentes/`).
