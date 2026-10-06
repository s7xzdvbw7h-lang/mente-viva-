# Mandalas de los chakras · Un color a la vez

Libro para colorear imprimible (A4, una sola cara). Creado por Dani Navarro.
Los mandalas se calculan con geometría (no son imágenes): salen como SVG vectorial y se arman en PDF.

## Regenerar el libro

    pip install -r requirements.txt     # una sola vez (y poppler, ver requirements.txt)
    python3 generar_libro.py --fase 1   # portada, dedicatoria, cómo usar y capítulo Raíz
    python3 verificar.py                # controles de calidad

Salen: `libro_mandalas_chakras_fase1.pdf`, un PNG por página en `preview/` y cada mandala en `svg/`.
El PDF trae una hoja en blanco detrás de cada página, para que el marcador no traspase.
Si imprimís en una sola cara, imprimí solo las páginas impares.

## Dónde se editan los textos

Todo está al principio de `generar_libro.py`: `DEDICATORIA`, `COMO_USAR_PASOS`, `CHAKRAS`
(nombre, "Está en", emoción, afirmación, respiración y pregunta de cada chakra) y los textos de la portada.

## Qué controla `verificar.py`

- Mandalas: cantidad de zonas, que ninguna mida menos de 8 mm, que no haya líneas cortadas,
  cantidad de pétalos de cada chakra y grosor de línea (medido en el PDF, entre 2,5 y 3 px).
- Páginas: texto de 18 pt o más (número de página 16 pt, frases de 30 pt o más), márgenes de 15 mm,
  textos que no se superpongan ni toquen el mandala, fuentes incrustadas, reversos en blanco,
  pestaña de 8 mm y que la frase aparezca una sola vez por capítulo.
- Portada: se compara con `referencia/portada_original.png` (el diseño original de Dani).

## Tipografías

Fraunces (títulos) y Manrope (texto), de Google Fonts, con licencia OFL (en `fuentes/`).
