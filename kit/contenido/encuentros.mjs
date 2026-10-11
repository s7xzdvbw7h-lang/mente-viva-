// Los 8 encuentros del cuaderno "La hora del té" (Mente Viva · NeuroGym).
// ÚNICA fuente: de acá salen los PDF y los textos para leer.
// Voseo rioplatense. Frases cortas. Sin tono juguetón. Nunca se corrige: importa lo que opina la mamá.

export const AVISO =
  "Este cuaderno no reemplaza la evaluación ni el tratamiento médico. Ante cambios en la memoria, consultá a un profesional.";
export const FIRMA = "Daniela Navarro";
export const MARCA = "Longevidad Emocional";
export const PRODUCTO = "Mente Viva · NeuroGym";
export const LEMA = "Mente activa, cuerpo en movimiento, tiempo juntas.";

// Estructura fija de cada encuentro: 45 minutos.
export const MOMENTOS = [
  { n: 1, min: 3, nombre: "Bienvenida con una canción" },
  { n: 2, min: 3, nombre: "¿Qué día es hoy?" },
  { n: 3, min: 20, nombre: "Actividad principal" },
  { n: 4, min: 5, nombre: "Bloque de razonamiento" },
  { n: 5, min: 8, nombre: "Charla de cierre" },
  { n: 6, min: 6, nombre: "Mandala de cierre" },
];

export const SEMANAS = [
  { n: 1, nombre: "Empezar", encuentros: [1, 2] },
  { n: 2, nombre: "Sostener", encuentros: [3, 4] },
  { n: 3, nombre: "Desafiarse", encuentros: [5, 6] },
  { n: 4, nombre: "Cerrar", encuentros: [7, 8] },
];

export const NIVELES = [
  { clave: "tranquila", nombre: "Tranquila", puntos: 1 },
  { clave: "pensar", nombre: "Con ganas de pensar", puntos: 2 },
  { clave: "desafiar", nombre: "Me quiero desafiar", puntos: 3 },
];

const serie = (texto, respuesta) => ({ consigna: "Completá la serie:", serie: texto, respuesta });
const problema = (consigna, respuesta) => ({ consigna, respuesta });

export const encuentros = [
  // ---------------------------------------------------------------- 1
  {
    n: 1,
    semana: 1,
    tema: "Infancia",
    titulo: "Objetos de la infancia",
    idea: "Volver a los objetos de cuando éramos chicas y contar cómo eran.",
    materiales: [
      "Las 10 tarjetas de objetos de la infancia",
      "La pizarra de la heladera",
      "Lápiz o fibra",
      "Este cuaderno",
    ],
    antes: [
      "Despejá la mesa y buscá buena luz.",
      "Preparen té o mate, si quieren.",
      "Dejá la canción lista en el celular.",
      "Poné las 10 tarjetas de objetos boca arriba.",
    ],
    bienvenida: {
      texto: "Elijan una canción de las que se cantaban cuando eran chicas. Escúchenla juntas. Pueden cantar bajito.",
      canciones: ["Arroz con leche", "Manuelita", "Mambrú se fue a la guerra"],
      guion: "«Empecemos con una canción. ¿Cuál te gustaría?»",
    },
    queDia: {
      texto: "Con la pizarra de la heladera, tu mamá completa «Hoy es…»: el día de la semana, el número y el mes.",
      guion: "«¿Me ayudás a completar la pizarra?»",
      siSeTraba: "Si duda, miren el almanaque o el celular juntas. No se corrige: se mira.",
    },
    principal: {
      titulo: "Objetos de la infancia",
      pasos: [
        { min: 2, texto: "Cada una elige 3 tarjetas de objetos y las deja frente a sí." },
        { min: 10, texto: "Tu mamá cuenta, de a una tarjeta: cómo era ese objeto, quién se lo dio o dónde lo veía, y cómo se usaba o se jugaba. Vos escuchás y preguntás, sin corregir." },
        { min: 8, texto: "Ahora contás vos una de tus tarjetas. Tu mamá escucha y puede preguntarte lo que quiera." },
      ],
      guion: ["«¿Cómo era el tuyo?»", "«¿Con quién jugabas?»", "«¿Dónde lo guardabas?»"],
      siSeTraba: [
        "Preguntale de qué color era o dónde estaba.",
        "Si no se acuerda, miren la ilustración juntas y pasen a otra tarjeta.",
        "Si aparece tristeza, esperá. Quedate al lado.",
      ],
    },
    razonamiento: {
      tranquila: [serie("2, 4, 6, 8, ___", "10"), serie("Lunes, martes, miércoles, ___", "jueves")],
      pensar: [serie("20, 18, 16, 14, ___", "12"), serie("A, C, E, G, ___", "I")],
      desafiar: [
        serie("1, 3, 6, 10, ___", "15 (cada vez se suma uno más: +2, +3, +4, +5)"),
        problema("La escuela empieza a las 8:00. Salís de casa 25 minutos antes. ¿A qué hora salís?", "7:35"),
      ],
    },
    cierre: {
      pregunta: "¿Qué le contarías hoy a esa nena?",
      guion: "«Gracias por contarme.»",
    },
    mandala: "Pinten el mandala mientras suena otra vez la canción del comienzo. Sin apuro.",
    pie: { icono: "caminar", texto: "Mañana, salí a caminar 10 minutos." },
  },

  // ---------------------------------------------------------------- 2
  {
    n: 2,
    semana: 1,
    tema: "Comida",
    titulo: "Receta de familia",
    idea: "Una receta de la familia, contada paso a paso por tu mamá.",
    materiales: [
      "Las 8 tarjetas de comidas",
      "Tiras de papel (una hoja cortada en 8 partes)",
      "La pizarra de la heladera",
      "Este cuaderno y una lapicera",
    ],
    antes: [
      "Cortá una hoja en 8 tiras.",
      "Elegí la canción y dejala lista.",
      "Poné las tarjetas de comidas sobre la mesa.",
    ],
    bienvenida: {
      texto: "Elijan una canción de las que sonaban en la cocina o en las reuniones de familia.",
      canciones: ["Mi Buenos Aires querido", "Caminito", "Los ejes de mi carreta"],
      guion: "«¿Qué canción sonaba en tu casa los domingos?»",
    },
    queDia: {
      texto: "Tu mamá completa «Hoy es…» en la pizarra. Después cuenta qué comió ayer.",
      guion: "«¿Qué comiste ayer? ¿Con quién?»",
      siSeTraba: "Si no se acuerda de todo, no importa. Con un plato alcanza.",
    },
    principal: {
      titulo: "Receta de familia",
      pasos: [
        { min: 2, texto: "Tu mamá mira las tarjetas de comidas y elige una receta de su familia. No tiene que ser difícil." },
        { min: 8, texto: "La cuenta en voz alta. Vos escribís cada paso en una tira de papel, con letra grande." },
        { min: 6, texto: "Mezclás las tiras sobre la mesa. Tu mamá las ordena como cree que va. Si algo cambia, lo charlan." },
        { min: 4, texto: "Entre las dos arman el menú de un domingo ideal: entrada, plato principal, postre y algo para tomar. Lo anotan en el cuaderno." },
      ],
      guion: ["«¿Cómo empieza?»", "«¿Y después?»", "«¿Qué le ponía tu mamá?»"],
      siSeTraba: [
        "Preguntale quién le enseñó esa receta.",
        "Si no recuerda una cantidad, anotá «a ojo». Así se cocinaba.",
        "Si se confunde con el orden, dejá que pruebe de otra forma.",
      ],
    },
    razonamiento: {
      tranquila: [serie("10, 20, 30, ___", "40"), serie("Desayuno, almuerzo, merienda, ___", "cena")],
      pensar: [
        serie("50, 45, 40, 35, ___", "30"),
        problema("Panadería: pan. Carnicería: carne. Verdulería: ___", "verdura (o verduras)"),
      ],
      desafiar: [
        serie("2, 3, 5, 8, 12, ___", "17 (se suma 1, 2, 3, 4 y ahora 5)"),
        problema("Una receta usa 3 huevos para 4 personas. Vas a cocinar para 8. ¿Cuántos huevos usás?", "6"),
      ],
    },
    cierre: {
      pregunta: "¿Qué comida te hace sentir en casa?",
      guion: "«Me gustaría cocinar esa receta con vos.»",
    },
    mandala: "Pinten el mandala mientras suena otra vez la canción del comienzo. Sin apuro.",
    pie: { icono: "charla", texto: "Llamá hoy a alguien querido." },
  },

  // ---------------------------------------------------------------- 3
  {
    n: 3,
    semana: 2,
    tema: "Sonidos",
    titulo: "¿Cómo sonaba?",
    idea: "Sonidos de otras épocas y ritmos con las manos.",
    materiales: [
      "Tarjetas de épocas: radio, teléfono, tocadiscos y casetera",
      "Tarjetas de lugares: estación, cocina y escuela",
      "Este cuaderno",
    ],
    antes: [
      "Separá esas 7 tarjetas y ponelas sobre la mesa.",
      "Elegí la canción y dejala lista.",
      "Buscá un lugar sin ruidos de fondo.",
    ],
    bienvenida: {
      texto: "Elijan una canción de cuando tu mamá tenía unos 20 años. Escúchenla con atención.",
      canciones: ["La balsa", "Yesterday", "Gracias a la vida"],
      guion: "«¿Dónde estabas cuando la escuchaste por primera vez?»",
    },
    queDia: {
      texto: "Tu mamá completa «Hoy es…» en la pizarra. Después cuenta qué sonidos escuchó hoy antes de que llegaras.",
      guion: "«¿Qué escuchaste esta mañana?»",
      siSeTraba: "Pájaros, tránsito, la radio, la pava: todo vale.",
    },
    principal: {
      titulo: "¿Cómo sonaba?",
      pasos: [
        { min: 10, texto: "Den vuelta una tarjeta por vez: radio, teléfono, tocadiscos, casetera, tren, pava, campana de la escuela. Tu mamá cuenta cómo sonaba y qué recuerdo le trae. No hace falta imitarlo perfecto." },
        { min: 10, texto: "Secuencias de palmas. Vos hacés una secuencia y tu mamá la repite. Empiecen con 2 palmas y sigan hasta 6. Después cambian: ella propone y vos imitás." },
      ],
      palmas: ["● ●", "● ○ ●", "● ● ○ ●", "● ○ ● ● ○", "● ● ○ ● ○ ●"],
      palmasRef: "● palma fuerte    ○ palma suave",
      guion: ["«¿Cómo sonaba?»", "«¿Dónde lo escuchabas?»", "«Ahora repetí lo que hice yo.»"],
      siSeTraba: [
        "Si una secuencia se hace larga, volvé a una más corta.",
        "Si no recuerda un sonido, que lo describa con palabras.",
        "Si se ríe, seguí. Está bien.",
      ],
    },
    razonamiento: {
      tranquila: [serie("1, 2, 1, 2, 1, ___", "2"), serie("do, re, mi, fa, ___", "sol")],
      pensar: [serie("3, 6, 9, 12, ___", "15"), serie("A, B, A, B, A, ___", "B")],
      desafiar: [
        serie("2, 4, 3, 5, 4, 6, ___", "5 (se suma 2 y se resta 1, una y otra vez)"),
        problema("El tren sale a las 17:45 y llega a las 19:10. ¿Cuánto dura el viaje?", "1 hora y 25 minutos"),
      ],
    },
    cierre: {
      pregunta: "¿Qué sonido te da calma?",
      guion: "«A mí también me gusta ese.»",
    },
    mandala: "Pinten el mandala mientras suena otra vez la canción del comienzo. Sin apuro.",
    pie: { icono: "respirar", texto: "Respirá hondo 2 minutos." },
  },

  // ---------------------------------------------------------------- 4
  {
    n: 4,
    semana: 2,
    tema: "Caras y escenas",
    titulo: "Escenas de otra época",
    idea: "Mirar escenas ilustradas y contar qué pasa, de qué época es y qué cambió.",
    materiales: [
      "Tarjetas de lugares: plaza, almacén, cocina y estación",
      "Este cuaderno",
    ],
    antes: [
      "Poné las 4 tarjetas de lugares sobre la mesa.",
      "Elegí la canción y dejala lista.",
      "Pensá un lugar de tu infancia por si hace falta ayudar.",
    ],
    bienvenida: {
      texto: "Elijan una canción que hable de volver o de recordar.",
      canciones: ["Volver", "Alfonsina y el mar", "Como la cigarra"],
      guion: "«¿Qué te hace acordar esta canción?»",
    },
    queDia: {
      texto: "Tu mamá completa «Hoy es…» en la pizarra. Después cuenta cómo está el día y con qué ropa salió.",
      guion: "«¿Cómo amaneció hoy?»",
      siSeTraba: "Es un ratito para estar en el presente, juntas.",
    },
    principal: {
      titulo: "Escenas de otra época",
      pasos: [
        { min: 2, texto: "Cada una elige una tarjeta de lugar." },
        { min: 12, texto: "Tu mamá describe qué pasa en la escena: quiénes están, qué hacen, qué se escucha. Después dice de qué época le parece y qué cosas cambiaron hasta hoy." },
        { min: 6, texto: "Hacen lo mismo con otra tarjeta. Esta vez describís vos primero y tu mamá agrega lo que falta." },
      ],
      guion: ["«¿Qué está pasando acá?»", "«¿Cómo era en tu época?»", "«¿Qué cambió?»"],
      siSeTraba: [
        "Preguntale por un detalle: «¿Qué hay a la izquierda?».",
        "Si no sabe de qué época es, que diga cuál le parece.",
        "Si recuerda un lugar de verdad, dejá que lo cuente.",
      ],
    },
    razonamiento: {
      tranquila: [serie("5, 10, 5, 10, 5, ___", "10"), serie("Mañana, mediodía, tarde, ___", "noche")],
      pensar: [serie("9, 8, 7, 6, ___", "5"), serie("Abuela, mamá, hija, ___", "nieta")],
      desafiar: [
        serie("64, 32, 16, 8, ___", "4 (cada número es la mitad del anterior)"),
        problema("En la foto de la plaza hay 12 personas. 5 son adultos y el resto, chicos. ¿Cuántos chicos hay?", "7"),
      ],
    },
    cierre: {
      pregunta: "¿Qué lugar te gustaría volver a visitar?",
      guion: "«Contame cómo llegarías.»",
    },
    mandala: "Pinten el mandala mientras suena otra vez la canción del comienzo. Sin apuro.",
    pie: { icono: "caminar", texto: "Caminá hasta la plaza más cercana." },
  },

  // ---------------------------------------------------------------- 5
  {
    n: 5,
    semana: 3,
    tema: "Usar dinero",
    titulo: "Armamos la compra",
    idea: "Armar una compra, calcular el vuelto y comparar precios de antes y de hoy.",
    materiales: [
      "La hoja de monedas y billetes de juguete (en este cuaderno)",
      "Una lista de 5 productos con precios",
      "Tijera",
      "Este cuaderno",
    ],
    antes: [
      "Recortá la hoja de monedas y billetes de juguete.",
      "Armá una lista de 5 productos con su precio.",
      "Elegí la canción y dejala lista.",
    ],
    bienvenida: {
      texto: "Elijan una canción tranquila para empezar.",
      canciones: ["Color esperanza", "Como la cigarra", "Rosa, Rosa"],
      guion: "«Elegí vos la canción de hoy.»",
    },
    queDia: {
      texto: "Tu mamá completa «Hoy es…» en la pizarra. Después cuenta cuántos días faltan para el fin de semana.",
      guion: "«¿Cuántos días faltan para el sábado?»",
      siSeTraba: "Que cuente con los dedos, si quiere. No es una prueba.",
    },
    principal: {
      titulo: "Armamos la compra",
      pasos: [
        { min: 3, texto: "Miran juntas la lista de 5 productos con sus precios." },
        { min: 10, texto: "Tu mamá arma la compra con los billetes de juguete. Calcula cuánto paga y cuánto le dan de vuelto. Vos hacés de cajera." },
        { min: 7, texto: "Conversan: «¿Cuánto costaba un helado cuando eras joven? ¿Y hoy?». ¿Qué cosas cuestan más ahora? ¿Cuáles menos?" },
      ],
      guion: ["«¿Cuánto es?»", "«¿Con cuánto pagás?»", "«¿Cuánto tiene que darte de vuelto?»"],
      siSeTraba: [
        "Usá números redondos: de a 100 o de a 500.",
        "Si no quiere calcular, que cuente los billetes con los dedos.",
        "Dejá que se tome el tiempo que necesite.",
      ],
      cuidado: "Un cuidado: nadie del banco pide claves por teléfono. Ante la duda, cortar y llamar a alguien de confianza.",
    },
    razonamiento: {
      tranquila: [serie("100, 200, 300, ___", "400"), serie("5, 10, 15, 20, ___", "25")],
      pensar: [
        serie("1000, 900, 800, ___", "700"),
        problema("Compraste algo de $350 y pagaste con $500. ¿Cuánto te dan de vuelto?", "$150"),
      ],
      desafiar: [
        serie("50, 100, 200, 400, ___", "800 (cada número es el doble del anterior)"),
        problema("Un kilo de pan cuesta $2.000. ¿Cuánto cuestan 2 kilos y medio?", "$5.000"),
      ],
    },
    cierre: {
      pregunta: "¿Qué consejo sobre la plata le darías a vos misma a los 20 años?",
      guion: "«Es un buen consejo. Gracias.»",
    },
    mandala: "Pinten el mandala mientras suena otra vez la canción del comienzo. Sin apuro.",
    pie: { icono: "taza", texto: "Tomate un té y charlá con alguien." },
  },

  // ---------------------------------------------------------------- 6
  {
    n: 6,
    semana: 3,
    tema: "Juegos de palabras",
    titulo: "Refranes, adivinanzas y letras",
    idea: "Completar refranes, resolver adivinanzas, buscar palabras y ordenar letras.",
    materiales: [
      "La página «Material del juego» (la siguiente de este cuaderno)",
      "Lápiz",
      "Este cuaderno",
    ],
    antes: [
      "Leé la página «Material del juego» antes de empezar.",
      "Elegí la canción y dejala lista.",
      "Tené a mano un lápiz para cada una.",
    ],
    bienvenida: {
      texto: "Elijan una canción con letra para escuchar con atención.",
      canciones: ["Manuelita", "La vaca estudiosa", "El reino del revés"],
      guion: "«¿Te acordás de la letra?»",
    },
    queDia: {
      texto: "Tu mamá completa «Hoy es…» en la pizarra. Después dice si conoce algún dicho sobre ese día de la semana.",
      guion: "«¿Había algún dicho para hoy?»",
      siSeTraba: "Por ejemplo: «martes 13, ni te cases ni te embarques».",
    },
    principal: {
      titulo: "Refranes, adivinanzas y letras",
      pasos: [
        { min: 5, texto: "Refranes: vos decís el comienzo y tu mamá lo completa. Después ella dice uno que se usaba en su casa." },
        { min: 5, texto: "Adivinanzas: vos las leés despacio, tu mamá piensa y responde." },
        { min: 5, texto: "Una letra: eligen la M. Dicen todas las palabras que se les ocurran, sin contarlas." },
        { min: 5, texto: "Anagramas: ordenan las letras para formar una palabra." },
      ],
      guion: ["«Completá vos.»", "«Dame una pista, si querés.»", "«Probemos con otra letra.»"],
      siSeTraba: [
        "Si no sale un refrán, pasen al siguiente.",
        "En las adivinanzas, dale una pista: «Es una fruta».",
        "En los anagramas, empezá por la primera letra.",
      ],
    },
    extra: {
      titulo: "Material del juego",
      bloques: [
        {
          titulo: "Refranes (decí el comienzo)",
          items: [
            "Más vale pájaro en mano…",
            "A caballo regalado…",
            "En casa de herrero…",
            "Camarón que se duerme…",
            "No hay mal que…",
            "Al que madruga…",
          ],
          respuestas: ["…que cien volando.", "…no se le miran los dientes.", "…cuchillo de palo.", "…se lo lleva la corriente.", "…por bien no venga.", "…Dios lo ayuda."],
        },
        {
          titulo: "Adivinanzas",
          items: [
            "Blanca por dentro, verde por fuera. Si quieres que te lo diga, espera.",
            "Oro parece, plata no es. ¿Qué es?",
            "Tengo agujas y no sé coser, tengo números y no sé leer.",
          ],
          respuestas: ["La pera.", "El plátano (la banana).", "El reloj."],
        },
        {
          titulo: "Anagramas (ordená las letras)",
          items: ["OPSA", "ZAPLA", "NAMZANA"],
          respuestas: ["SOPA", "PLAZA", "MANZANA"],
        },
      ],
    },
    razonamiento: {
      tranquila: [serie("A, B, C, D, ___", "E"), serie("Uno, dos, tres, ___", "cuatro")],
      pensar: [serie("B, D, F, H, ___", "J"), serie("L, M, M, J, ___", "V (los días de la semana)")],
      desafiar: [
        serie("Z, Y, X, W, ___", "V"),
        serie("AB, CD, EF, GH, ___", "IJ"),
      ],
    },
    cierre: {
      pregunta: "¿Qué refrán te representa?",
      guion: "«Contame por qué.»",
    },
    mandala: "Pinten el mandala mientras suena otra vez la canción del comienzo. Sin apuro.",
    pie: { icono: "respirar", texto: "Probá la respiración de la app." },
  },

  // ---------------------------------------------------------------- 7
  {
    n: 7,
    semana: 4,
    tema: "Noticias",
    titulo: "Algo bueno de la semana",
    idea: "Conversar sobre lo bueno que pasó y armar el titular de la semana.",
    materiales: [
      "Un diario, una revista o el celular",
      "Hoja y lápiz",
      "Este cuaderno",
    ],
    antes: [
      "Elegí una nota amable: del barrio, de cultura, de naturaleza o de deportes.",
      "Dejá de lado las noticias duras.",
      "Elegí la canción y dejala lista.",
    ],
    bienvenida: {
      texto: "Elijan una canción que les guste a las dos.",
      canciones: ["Color esperanza", "Gracias a la vida", "Como la cigarra"],
      guion: "«Elegí vos.»",
    },
    queDia: {
      texto: "Tu mamá completa «Hoy es…» en la pizarra. Después cuenta cómo amaneció el día.",
      guion: "«¿Cómo amaneció hoy?»",
      siSeTraba: "Alcanza con una frase.",
    },
    principal: {
      titulo: "Algo bueno de la semana",
      pasos: [
        { min: 6, texto: "Cada una cuenta algo bueno que pasó esta semana, aunque sea pequeño." },
        { min: 7, texto: "Vos leés la nota amable que elegiste. Tu mamá cuenta qué le pareció y si recuerda algo parecido." },
        { min: 7, texto: "Inventan juntas el titular de la semana, como en un diario. Lo escriben en el cuaderno con letra grande." },
      ],
      guion: ["«¿Qué cosa buena pasó esta semana?»", "«¿Cómo lo contarías en un titular?»"],
      siSeTraba: [
        "Si no se le ocurre nada, empiecen por algo pequeño: una llamada, un mate, un día de sol.",
        "Si la nota la preocupa, cámbienla por otra.",
        "No discutan opiniones: escuchen.",
      ],
    },
    razonamiento: {
      tranquila: [serie("1, 3, 5, 7, ___", "9"), serie("Lunes, martes, miércoles, jueves, ___", "viernes")],
      pensar: [
        serie("8, 16, 24, 32, ___", "40"),
        problema("El diario llega a las 6:00 y la panadería abre a las 7:30. ¿Cuánto tiempo pasa entre uno y otro?", "1 hora y 30 minutos"),
      ],
      desafiar: [
        serie("1, 1, 2, 3, 5, 8, ___", "13 (cada número es la suma de los dos anteriores)"),
        problema("Salís de casa a las 10:00. Vas a la farmacia (15 minutos), al banco (20) y a la verdulería (10). Caminar entre un lugar y otro lleva 5 minutos, también desde y hasta tu casa. ¿A qué hora volvés?", "11:05 (45 minutos de trámites y 20 de caminata)"),
      ],
    },
    cierre: {
      pregunta: "¿Qué cosa buena de tu semana te gustaría que se supiera?",
      guion: "«Se la podemos contar a alguien hoy.»",
    },
    mandala: "Pinten el mandala mientras suena otra vez la canción del comienzo. Sin apuro.",
    pie: { icono: "charla", texto: "Contale a alguien lo bueno de tu semana." },
  },

  // ---------------------------------------------------------------- 8
  {
    n: 8,
    semana: 4,
    tema: "Crear",
    titulo: "Algo nuestro",
    idea: "Hacer algo juntas con lo que hay en casa y cerrar las 4 semanas.",
    materiales: [
      "Hojas, lápices o fibras",
      "Tijera y pegamento",
      "Revistas viejas o folletos, si tienen",
      "El celular, para una foto",
      "El diploma (hoja de este cuaderno)",
    ],
    antes: [
      "Juntá lo que haya en casa: hojas, revistas, telas, botones.",
      "Elegí la canción del primer encuentro.",
      "Pensá una frase corta para decirle al final.",
    ],
    bienvenida: {
      texto: "Vuelvan a la canción del primer encuentro. Es una forma de cerrar.",
      canciones: ["Arroz con leche", "Manuelita", "Mambrú se fue a la guerra"],
      guion: "«Esta fue la primera que escuchamos.»",
    },
    queDia: {
      texto: "Tu mamá completa «Hoy es…» en la pizarra. Después repasan en la pizarra qué hicieron en estas 4 semanas.",
      guion: "«¿Cuál fue tu encuentro favorito?»",
      siSeTraba: "Que cuente lo que se acuerde. Vos completás con cariño si hace falta.",
    },
    principal: {
      titulo: "Algo nuestro",
      pasos: [
        { min: 3, texto: "Eligen qué van a hacer: una carta, una receta ilustrada o un collage." },
        { min: 14, texto: "Lo hacen juntas, cada una a su ritmo. Tu mamá decide los colores, las palabras o las imágenes." },
        { min: 3, texto: "Se sacan una foto juntas con lo que hicieron." },
      ],
      guion: ["«¿Cómo lo querés hacer?»", "«Elegí vos los colores.»"],
      siSeTraba: [
        "Si no sabe qué recortar, que mire las imágenes y señale las que le gustan.",
        "Si no quiere dibujar, que dicte y escribís vos.",
        "Si la despedida emociona, abrácense. Es parte del cierre.",
      ],
    },
    razonamiento: {
      tranquila: [serie("10, 9, 8, 7, ___", "6"), serie("Rojo, azul, amarillo, rojo, azul, ___", "amarillo")],
      pensar: [
        serie("4, 8, 12, 16, ___", "20"),
        problema("Tenés 12 hojas y hacés 3 collages iguales. ¿Cuántas hojas usás en cada uno?", "4"),
      ],
      desafiar: [
        serie("2, 4, 8, 14, 22, ___", "32 (se suma 2, 4, 6, 8 y ahora 10)"),
        problema("Empezás una carta a las 16:30. Escribís 25 minutos, la leés 10 y la guardás en el sobre 5. ¿A qué hora terminás?", "17:10"),
      ],
    },
    cierre: {
      pregunta: "¿Qué te llevás de estas 4 semanas?",
      guion: "Leele a tu mamá la frase que pensaste. Después entréguenle el diploma.",
    },
    mandala: "Pinten el último mandala mientras suena la canción del primer encuentro.",
    pie: { icono: "caminar", texto: "Salí a caminar para festejar." },
  },
];
