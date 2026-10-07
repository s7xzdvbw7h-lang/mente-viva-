# Mandalas de los 7 chakras · Un color a la vez

Libro para colorear (8,5 × 11 pulgadas, vertical, listo para KDP). Creado por Dani Navarro.
Los mandalas se calculan con geometría (no son imágenes): salen como SVG vectorial y se arman en PDF.
El interior es **blanco y negro**: los colores aparecen solo como referencia (color protagonista y paleta sugerida).

## Regenerar el libro

    pip install -r requirements.txt     # una sola vez (y poppler, ver requirements.txt)
    python3 generar_libro.py            # el libro completo (20 páginas impresas)
    python3 verificar.py                # controles de calidad

Salen: `libro_mandalas_chakras.pdf`, un PNG por página en `preview/` (recortado al tamaño final) y cada mandala en `svg/`.
El PDF mide 8,625 × 11,25" (8,5 × 11" más 0,125" de sangrado arriba, abajo y afuera, como pide KDP) y trae las
cajas de corte y de sangrado. Detrás de cada página hay una hoja en blanco, para que el marcador no traspase
(40 hojas en total). Si imprimís en una sola cara, imprimí solo las páginas impares.
Márgenes: 0,75" del lado del lomo y 0,5" en el resto.

## Cómo está armado

| Página | Contenido |
|---|---|
| 1 | Portada (sin número) |
| 2 | Dedicatoria (sin número) |
| 3 | Cómo usar este libro |
| 4–17 | 7 capítulos de 2 páginas: primero el mandala (nombre, color protagonista, paleta sugerida y la frase para leer al terminar), después la respiración y la pregunta |
| 18 | Todos juntos: los siete chakras en un solo mandala |
| 19 | Un momento para compartir |
| 20 | Cierre: frase final, "Hoy me sentí…" y "Fecha:" |

Cada chakra tiene su propia forma (en `mandalas.py`): Raíz 4 pétalos y cuadrado, Sacro 6 y luna, Plexo solar 10 y
triángulo, Corazón 12 y estrella de seis puntas, Garganta 16 y círculo, Tercer ojo 2 pétalos grandes y un círculo
central, Corona un loto de tres capas (8 + 8 + 4). Todos comparten el esqueleto: borde propio, aro liso, pétalos
grandes y un centro grande. Nada de microdetalles: zonas de 10 mm o más y de 1 cm² o más.
Líneas: 3,5 pt en los contornos y 3 pt en las divisiones.

Colores protagonistas y paletas (`PALETAS` en `mandalas.py`, 5 colores por chakra, el protagonista primero):
Raíz rojo · Sacro naranja · Plexo solar amarillo · Corazón verde · Garganta azul · Tercer ojo índigo · Corona violeta.

## Dónde se editan los textos

Todo está al principio de `generar_libro.py`: dedicatoria, cómo usar, `CHAKRAS` (nombre, relación, afirmación,
respiración y pregunta de cada chakra), "Todos juntos", "Un momento para compartir", cierre y los textos de la portada.
Los textos de relación y respiración de Sacro a Corona son borradores: conviene que Dani los revise.

## Qué controla `verificar.py`

- Mandalas: cantidad de zonas, que ninguna mida menos de 10 mm ni 1 cm², que no haya líneas cortadas, cantidad de
  pétalos de cada chakra y grosor de línea (declarado y medido en el PDF a 600 dpi, entre 2,9 y 3,7 pt).
- Páginas: texto de 18 pt o más (también el número de página), frases de 30 pt o más, márgenes, textos que no se
  superpongan ni toquen el mandala o los dibujos, fuentes incrustadas, reversos en blanco, cajas de corte y sangrado.
- Color: ningún color adentro de los mandalas; la paleta sugerida tiene 5 colores y el protagonista es el que más se ve;
  pestaña de 8 mm del color del chakra que llega al borde con sangrado.
- Que no vuelvan los textos que se sacaron ("Está en:", "No hay forma de hacerlo mal").

## Tipografías

Fraunces (títulos) y Manrope (texto), de Google Fonts, con licencia OFL (en `fuentes/`).
