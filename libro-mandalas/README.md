# Mandalas de los 7 chakras · Un color a la vez

Libro para colorear (8,5 × 11 pulgadas, vertical, listo para KDP o para una imprenta). Creado por Dani Navarro.
Los mandalas se calculan con geometría (no son imágenes): salen como SVG vectorial y se arman en PDF.
Las páginas para colorear no llevan color adentro del dibujo (línea gris oscuro #3A3A3A); los colores aparecen como
referencia: la paleta sugerida y, enfrente de cada mandala, una página "Así podría quedar" con el mismo dibujo pintado.

## Regenerar el libro

    pip install -r requirements.txt     # una sola vez (y poppler, ver requirements.txt)
    python3 generar_libro.py            # arma las dos ediciones y las vistas previas
    python3 verificar.py                # controles de calidad (tarda unos 5 minutos)

Salen dos PDF de 42 páginas cada uno, iguales salvo las páginas 3 y 25:

- `libro-chakras-venta.pdf`: **edición para vender**. Dedicatoria con una línea "De: ______" para que escriba su nombre
  quien regala; Garganta pregunta "¿Qué consejo le darías a alguien que querés mucho?".
- `libro-chakras-mama.pdf`: la edición de Dani. Dedicatoria firmada "Dani"; Garganta pregunta "¿Qué consejo le darías a tu
  nieto?".

El final es igual en las dos: la página 40 lleva "Antes de cerrar este libro…", el mensaje de Daniela y su firma
("Con cariño, Daniela Navarro, Longevidad Emocional"); la 41 lleva el QR, "MenteViva", el isotipo y `@daninavarro.bienestar`
(sin la web escrita); la 42 queda en blanco.

**El QR** de la página 41 lleva a `https://menteviva.daninavarro.com.ar` (`QR_URL` en `generar_libro.py`; no hubo acceso para
comprobar que la dirección responda). Se dibuja en vector con `codigo_qr.py` (módulos de 28 mm de lado y 4 mm de blanco
alrededor, negro sobre blanco, nivel de corrección Q) y `verificar.py` lo lee del PDF para confirmar que lleva a esa dirección.
La dirección no se escribe en el libro. La carta y la firma ocupan toda la página 40, por eso el QR, el isotipo y el usuario
pasaron a la 41 y se agregó la 42 en blanco para que el total sea par.

**El isotipo** de la página 41 (las dos ediciones) es `assets/isotipo.svg`: el corazón de manos con brote en su versión a
color (`isotipo-color` de la marca: #8E4E52, #E4D3CD y #C2A878), sin fondo ni recuadro y sin tocar los colores, de 25 mm de
ancho y centrado, con 8 mm de aire arriba y abajo, y debajo `@daninavarro.bienestar` en 18 pt #333. Se usó el SVG de la marca
(vectorial, como indica el manual) en lugar del PNG `color-transparente-isotipo.png`, que está en la computadora de Daniela y no se ve desde
este entorno. Los cinco archivos que llegaron están en `assets/originales/`; para usar otro isotipo, copialo como
`assets/isotipo.svg` (o `.png`) y volvé a correr `python3 generar_libro.py`. `ruta_logo()` busca cualquier `assets/isotipo.*`.

También salen un PNG por página en `preview/`, los pliegos (página izquierda + derecha) en `preview/pliegos/`, cada
mandala en `svg/` y cada ejemplo pintado en `ejemplos/`.

## Cómo está armado el PDF

42 páginas = 21 hojas en las dos ediciones (par, pero no múltiplo de 4). Tamaño final 8,5 × 11" con sangrado de 0,125" arriba, abajo y **del lado de afuera**
(a la derecha en las páginas impares, a la izquierda en las pares), como pide KDP. Cada página trae las cajas de corte y de
sangrado. Márgenes: 0,75" del lado del lomo y 0,5" en el resto. Todas las páginas llevan fondo #FFFBF5 (papel cálido) hasta
el borde de sangrado, así que hay que imprimir a color. Las pestañas de color (8 mm) llegan al borde con sangrado, en el lado
de afuera de cada página.

Se lee por pliegos. El ejemplo pintado va en la página izquierda, enfrente del mandala para pintar; detrás de cada página
que se pinta con marcador hay una hoja en blanco con una nota de 18 pt ("Esta hoja queda en blanco a propósito…") y el
número de página, así el marcador no traspasa.

| Páginas | Contenido |
|---|---|
| 1 | Portada (derecha) |
| 2 · 3 | Legal y autora (©, aviso de bienestar, contacto) · Dedicatoria |
| 4 · 5 | **Qué es un chakra** ("Siete lugares de tu cuerpo para volver a vos") · Cómo usar este libro |
| 6–33 | 7 capítulos de 4 páginas: **Así podría quedar** (izquierda) · **mandala para pintar** (derecha) · hoja en blanco con nota (izquierda) · **respiración y preguntas** (derecha). Raíz 6–9, Sacro 10–13, Plexo solar 14–17, Corazón 18–21, Garganta 22–25, Tercer ojo 26–29, Corona 30–33 |
| 34 · 35 | Todos juntos: pintado · para pintar (leyenda de 8 colores en las dos) |
| 36 · 37 | Hoja en blanco · Un momento para compartir |
| 38 · 39 | Hoja en blanco · Gracias por regalarte este rato |
| 40 | Carta de cierre de Daniela con su firma |
| 41 · 42 | QR, "MenteViva", isotipo y usuario · hoja en blanco (sin nota ni número) |

Cada chakra tiene su propia forma (en `mandalas.py`): Raíz 4 pétalos, cuadrado con círculo central y 4 rombos grandes;
Sacro 6 pétalos, 6 gotas grandes y luna; Plexo solar 8 pétalos anchos con 8 zonas grandes entre ellos y triángulo central;
Corazón 8 pétalos y estrella de seis puntas más corta y gruesa; Garganta 8 pétalos, círculo central grande y aro en 8
partes; Tercer ojo ojo con anillos, 8 lóbulos de borde y centro grande; Corona loto de 8 pétalos grandes con círculo
central grande y 8 lóbulos de borde. Nada de microdetalles: zonas de 10 mm o más y de 1 cm² o más (casi todas de 12 mm o
más; ver `AUDITORIA.md` para las excepciones).
Líneas: 2,63 pt en los contornos y 2,25 pt en las divisiones (un 25 % más finas que antes), en gris #3A3A3A. Los mandalas se
dibujan en unidades de diseño (radio 76) y se imprimen con radio 63 mm (12,6 cm de diámetro): `escalado` achica la
geometría y compensa el grosor de línea para que siga midiendo 2,63 y 2,25 pt. Se achicó el mandala (no el texto) para que
todo el texto pueda ser de 18 pt o más.

## Colores

Paleta viva y luminosa, sin tonos terrosos (`PALETA` en `mandalas.py`): rojo #E63946, naranja #FF8A2B, amarillo #FFC93C,
rosa #FF7EB6, violeta #A855F7, verde #34C27A, azul #3FA9F5, índigo #5B5BD6, turquesa #2EC4B6, lila #D9B8FF, dorado #F2B705.
Los círculos de la leyenda son sólidos y de 10 mm, con un borde de un tono más oscuro (`BORDE_COLOR`).
Cada chakra tiene un color principal y una paleta de 5 colores, el principal primero (`PALETAS`):
Raíz rojo · Sacro naranja · Plexo solar amarillo · Corazón verde · Garganta azul · Tercer ojo índigo · Corona violeta.
Dentro de cada paleta la distancia de color (CIELAB ΔE) es de 29 o más a simple vista; con daltonismo el par más cercano
baja a 7,6 (turquesa–rosa en Garganta, con deuteranopía). Cada color lleva su nombre escrito, así no depende solo de distinguirlo.

Los ejemplos pintados (`ejemplos.py`) usan las mismas funciones que los mandalas, pasándoles qué color lleva cada
parte (`ESQUEMAS`): así las líneas son exactamente las mismas. Reglas: solo los 5 colores de la paleta, colores
planos, el color principal ocupa entre el 60 y el 70 % de lo pintado (en Raíz, 35–55 %, para que el rojo no domine todo),
se usan los 5 y el reparto es simétrico. "Todos juntos" pintado lleva cada flor con el color de su chakra, centros
dorados y fondo crema.

## Dónde se editan los textos

Todo está al principio de `generar_libro.py`: dedicatoria, legal y autora, qué es un chakra, cómo usar, `CHAKRAS`
(nombre, párrafo, respiración, preguntas, nota, afirmación y la variante `mama`), "Todos juntos", "Un momento para
compartir", cierre, el mensaje de la página 40 y los textos de la portada. Todo el texto va en Manrope o Fraunces, de 18 pt
o más, en #222 (cuerpo) o #333 (textos chicos), con interlineado 1,5. Si un texto no entra, se achica el título y luego el
cuerpo (nunca por debajo de 18 pt); el tamaño elegido de cada página de texto queda anotado en `verificar.py`.

## Qué controla `verificar.py`

- Mandalas: cantidad de zonas, que ninguna mida menos de 10 mm ni 1 cm², que no haya líneas cortadas, cantidad de
  pétalos de cada chakra, grosor de línea (declarado y medido en el PDF a 600 dpi, entre 2,1 y 3,0 pt) y que todas las
  líneas sean #3A3A3A.
- Páginas (las dos ediciones): texto de 18 pt o más (también el número de página), frases de 30 pt o más, márgenes
  (distintos en páginas izquierdas y derechas), textos que no se superpongan ni toquen el mandala o los dibujos, fuentes
  incrustadas, cajas de corte y sangrado de cada lado, fondo #FFFBF5, texto en #222 o #333, títulos del mismo tamaño en
  todos los capítulos y en "Todos juntos", renglones para escribir (#8A8178, 1,5 px, cada 14 mm) y que no pisen el texto.
- Hojas en blanco (8, 12, 16, 20, 24, 28, 32, 36, 38): solo la nota de 18 pt #333 centrada, arriba del número de página.
- Texto: que estén todos los textos pedidos, con su texto exacto y en el orden pedido, y que no vuelvan los que se
  sacaron ("Está relacionado…", "Color protagonista", "chacra", palabras en femenino…).
- Color: ningún color adentro de los mandalas para colorear; la paleta sugerida tiene 5 colores (8 en "Todos juntos") y el
  principal es el que más se ve; pestaña de 8 mm del color del chakra que llega al borde con sangrado.
- Ejemplos pintados: solo colores de la paleta, usa los 5, el principal ocupa su rango, y sin los colores el dibujo es
  idéntico al mandala para colorear (mismas líneas).
- Las dos ediciones, comparadas página por página: solo difieren las páginas 3 y 25 (las dos tienen 42 páginas, un total par).
- Página 40: textos, orden, tamaños, colores, espacio entre párrafos y que no figure la web.
- Página 41: el QR mide 28 mm (nunca menos de 25), está centrado, tiene 4 mm de blanco alrededor, es negro sin
  colores y se lee como `https://menteviva.daninavarro.com.ar`; el isotipo mide 25 mm, está centrado, con aire alrededor, sin fondo ni recuadro y con los tres colores de la marca (si faltara el archivo, lo
  avisa como PENDIENTE). Página 42: completamente en blanco, sin nota.

## Tipografías

Fraunces (títulos) y Manrope (texto), de Google Fonts, con licencia OFL (en `fuentes/`).
