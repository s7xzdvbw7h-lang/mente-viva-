# Mandalas de los 7 chakras · Un color a la vez

Libro para colorear (8,5 × 11 pulgadas, vertical, listo para KDP o para una imprenta). Creado por Dani Navarro.
Los mandalas se calculan con geometría (no son imágenes): salen como SVG vectorial y se arman en PDF.
Las páginas para colorear son **blanco y negro** (línea negra pura); los colores aparecen como referencia: la paleta
sugerida y, enfrente de cada mandala, una página "Así podría quedar" con el mismo dibujo pintado.

## Regenerar el libro

    pip install -r requirements.txt     # una sola vez (y poppler, ver requirements.txt)
    python3 generar_libro.py            # arma las dos ediciones y las vistas previas
    python3 verificar.py                # controles de calidad (tarda unos 4 minutos)

Salen dos PDF, iguales salvo la firma de la dedicatoria:

- `libro_mandalas_chakras.pdf`: **edición para vender**. La dedicatoria termina con una línea "De: ______" para que escriba
  su nombre quien regala.
- `libro_para_mama.pdf`: la edición de Dani, firmada "Dani".

También salen un PNG por página en `preview/`, los pliegos (página izquierda + derecha) en `preview/pliegos/`, cada
mandala en `svg/` y cada ejemplo pintado en `ejemplos/`.

## Cómo está armado el PDF

40 páginas = 20 hojas (múltiplo de 4). Tamaño final 8,5 × 11" con sangrado de 0,125" arriba, abajo y **del lado de afuera**
(a la derecha en las páginas impares, a la izquierda en las pares), como pide KDP. Cada página trae las cajas de corte y de
sangrado. Márgenes: 0,75" del lado del lomo y 0,5" en el resto. Las pestañas de color (8 mm) llegan al borde con sangrado,
en el lado de afuera de cada página.

Se lee por pliegos. El ejemplo pintado va en la página izquierda, enfrente del mandala para pintar; detrás de cada página
que se pinta con marcador hay una página en blanco, así no traspasa.

| Páginas | Contenido |
|---|---|
| 1 | Portada (derecha) |
| 2 · 3 | Legal y autora (©, aviso de bienestar, contacto) · Dedicatoria |
| 4 · 5 | Qué es un chakra, en simple · Cómo usar este libro |
| 6–33 | 7 capítulos de 4 páginas: **Así podría quedar** (izquierda) · **mandala para pintar** (derecha) · en blanco (izquierda) · **respiración y pregunta** (derecha) |
| 34 · 35 | Todos juntos: pintado · para pintar |
| 36 · 37 | En blanco · Un momento para compartir |
| 38 · 39 | En blanco · Cierre |
| 40 | En blanco |

Cada chakra tiene su propia forma (en `mandalas.py`): Raíz 4 pétalos y cuadrado, Sacro 6 y luna, Plexo solar 10 y
triángulo, Corazón 12 y estrella de seis puntas, Garganta 16 y círculo, Tercer ojo 2 pétalos grandes y un círculo
central, Corona un loto de tres capas (8 + 8 + 4). Todos comparten el esqueleto: borde propio, aro liso, pétalos
grandes y un centro grande. Nada de microdetalles: zonas de 10 mm o más y de 1 cm² o más.
Líneas: 3,5 pt en los contornos y 3 pt en las divisiones. Los mandalas se dibujan en unidades de diseño (radio 76) y se
imprimen con radio 82 mm (16,4 cm de diámetro): `escalado` agranda la geometría y compensa el grosor de línea para
que siga midiendo 3,5 y 3 pt.

## Colores

Los colores del interior son suaves, vivos y terrosos, de la misma familia que las flores de la portada (`PALETA` en
`mandalas.py`). Cada chakra tiene un color protagonista y una paleta de 5 colores, el protagonista primero (`PALETAS`):
Raíz rojo · Sacro naranja · Plexo solar amarillo · Corazón verde · Garganta azul · Tercer ojo índigo · Corona violeta.
Dentro de cada paleta la distancia de color (CIELAB ΔE) es de 24 o más a simple vista, y de 13 o más con daltonismo
rojo-verde. Cada color lleva su nombre escrito, así no depende solo de distinguirlo a simple vista.

Los ejemplos pintados (`ejemplos.py`) usan las mismas funciones que los mandalas, pasándoles qué color lleva cada
parte (`ESQUEMAS`): así las líneas son exactamente las mismas. Reglas: solo los 5 colores de la paleta, colores
planos, el protagonista ocupa entre el 60 y el 70 % de lo pintado, se usan los 5 y el reparto es simétrico.
"Todos juntos" pintado lleva cada flor con el color de su chakra, centros dorados y fondo crema.

## Dónde se editan los textos

Todo está al principio de `generar_libro.py`: dedicatoria, legal y autora, qué es un chakra, cómo usar, `CHAKRAS`
(nombre, relación, afirmación, respiración y pregunta de cada chakra), "Todos juntos", "Un momento para compartir",
cierre y los textos de la portada. Los textos de relación y respiración de Sacro a Corona son borradores: conviene que
Dani los revise.

## Qué controla `verificar.py`

- Mandalas: cantidad de zonas, que ninguna mida menos de 10 mm ni 1 cm², que no haya líneas cortadas, cantidad de
  pétalos de cada chakra, grosor de línea (declarado y medido en el PDF a 600 dpi, entre 2,9 y 3,7 pt) y que todas las
  líneas sean negro puro.
- Páginas: texto de 18 pt o más (también el número de página), frases de 30 pt o más, márgenes (distintos en páginas
  izquierdas y derechas), textos que no se superpongan ni toquen el mandala o los dibujos, fuentes incrustadas, cajas de
  corte y sangrado de cada lado, y que el reverso de cada página que se pinta con marcador esté en blanco.
- Color: ningún color adentro de los mandalas para colorear; la paleta sugerida tiene 5 colores y el protagonista es el
  que más se ve; pestaña de 8 mm del color del chakra que llega al borde con sangrado.
- Ejemplos pintados: solo colores de la paleta, usa los 5, el protagonista ocupa 60–70 %, y sin los colores el dibujo es
  idéntico al mandala para colorear (mismas líneas).
- Las dos ediciones: solo cambia la firma de la dedicatoria.
- Que no vuelvan los textos que se sacaron ("Está en:", "No hay forma de hacerlo mal").

## Tipografías

Fraunces (títulos) y Manrope (texto), de Google Fonts, con licencia OFL (en `fuentes/`).
