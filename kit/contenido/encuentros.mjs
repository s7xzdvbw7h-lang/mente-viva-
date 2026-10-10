// Textos de los 8 encuentros del kit "Mente Viva · NeuroGym".
// Esta es la ÚNICA fuente: de acá salen el cuaderno en PDF y los .md para leer.
// Voseo, frases cortas, sin lenguaje técnico. Nada de corregir ni de examinar.

export const ESTRUCTURA = [
  { min: 5, nombre: "Canción de bienvenida" },
  { min: 5, nombre: "¿Qué día es hoy?" },
  { min: 25, nombre: "Actividad principal" },
  { min: 10, nombre: "Charla de cierre" },
];

export const SEMANAS = [
  { n: 1, encuentros: [1, 2] },
  { n: 2, encuentros: [3, 4] },
  { n: 3, encuentros: [5, 6] },
  { n: 4, encuentros: [7, 8] },
];

export const encuentros = [
  {
    n: 1,
    tema: "Infancia",
    titulo: "El plano de mi casa de chica",
    idea: "Volver a la casa, la calle y los juegos de cuando éramos chicas.",
    antes: [
      "Preparen una mesa cómoda, con buena luz.",
      "Té o mate, si a tu mamá le gusta.",
      "Celular en silencio, salvo para la música.",
    ],
    necesitamos: [
      "Las tarjetas de Infancia",
      "Hojas blancas y lápices o fibras",
      "La pizarra de la heladera",
    ],
    cancion: {
      que: "Pongan «Manuelita», de María Elena Walsh, o «Arroz con leche». O la que más le guste a tu mamá.",
      consejo: "Cantá bajito con ella. No hace falta cantar bien.",
    },
    queDia: {
      que: "Tu mamá busca el día de hoy en el almanaque o en el celular. Lo escribe grande en la pizarra: día, número y mes.",
      consejo: "Si se confunde, no se corrige. Se dice: «Miremos juntas».",
    },
    principal: {
      pasos: [
        "Tu mamá da vuelta una tarjeta de Infancia y la lee en voz alta. Si prefiere, la leés vos.",
        "En una hoja en blanco, dibuja el plano de la casa donde vivió de chica: la puerta, los cuartos, el patio. No tiene que quedar lindo.",
        "Mientras dibuja, cuenta. ¿Dónde dormía? ¿Dónde se comía? ¿Cuál era su rincón secreto?",
        "Vos preguntás con calma: «¿Y qué había acá?», «¿A qué olía esta pieza?».",
        "Con otra tarjeta, tu mamá cuenta a qué jugaba. Vos anotás en la pizarra las palabras que aparezcan: nombres, lugares, juegos.",
      ],
      siSeTraba: [
        "Probá con: «Empecemos por la puerta de entrada».",
        "Preguntale qué se escuchaba o qué olor había.",
        "Si no sale nada, pasen a otra tarjeta. No pasa nada.",
      ],
    },
    cierre: {
      preguntas: [
        "¿Qué parte de la casa te gustó más recordar?",
        "¿Qué juego te dan ganas de volver a jugar?",
        "¿Qué te gustaría que supiera la familia de esa casa?",
      ],
    },
    frase: "Hoy me regalo un rato para recordar con calma.",
    paraLaHija:
      "Tu trabajo es escuchar. No completes sus frases ni la corrijas. Si cuenta lo mismo dos veces, escuchala dos veces.",
  },
  {
    n: 2,
    tema: "Comida",
    titulo: "La receta de la familia",
    idea: "Una receta que marcó la vida de tu mamá, contada por ella.",
    antes: [
      "Pensá si hay un plato que tu mamá siempre cocinó. Podés preguntárselo antes.",
      "Dejá a mano el cuaderno y una lapicera de trazo grueso.",
    ],
    necesitamos: [
      "Las tarjetas de Comida",
      "Este cuaderno y lapicera",
      "Hojas, tijera y una cinta o ganchito para pegar",
    ],
    cancion: {
      que: "Elijan una canción de cocina o de reunión familiar. Por ejemplo, una chacarera, «Caminito» o «Mi Buenos Aires querido».",
      consejo: "Que la elija ella. Si quiere bailar un poquito, que baile.",
    },
    queDia: {
      que: "Tu mamá escribe en la pizarra el día de hoy. Después cuenta qué comió ayer.",
      consejo: "No importa si no se acuerda de todo. Con un plato alcanza.",
    },
    principal: {
      pasos: [
        "Tu mamá da vuelta una tarjeta de Comida. ¿Qué plato le hace acordar?",
        "Elige la receta que van a escribir. Vos sos la ayudante: tu mamá es la experta.",
        "Ella te dicta. Primero los ingredientes, después cómo se hace. Escribí con letra grande, en el cuaderno.",
        "Escribí cada paso en una tira de papel. Mezclalas sobre la mesa.",
        "Tu mamá las ordena como ella cree que va. Si algo cambia, lo charlan: puede haber más de una forma.",
        "Anoten un día para cocinar la receta juntas.",
      ],
      siSeTraba: [
        "Preguntale: «¿Quién te la enseñó?». Los recuerdos suelen aparecer por ahí.",
        "Si no se acuerda de una cantidad, anoten «a ojo». Así se hacía.",
        "Si no sale una receta, que cuente cómo olía la cocina de su casa.",
      ],
    },
    cierre: {
      preguntas: [
        "¿Qué sabor te lleva a una fiesta?",
        "¿Quién cocinaba en tu casa? ¿Qué te dejaban hacer a vos?",
        "¿Qué te gustaría cocinar de nuevo?",
      ],
    },
    frase: "Lo que sé hacer con las manos vale mucho.",
    paraLaHija:
      "Dejá que ella lleve la voz. Si querés probar algo distinto en la receta, esperá a cocinarla juntas.",
  },
  {
    n: 3,
    tema: "Sonidos",
    titulo: "La banda sonora de mi vida",
    idea: "Sonidos y canciones que están en la memoria de tu mamá.",
    antes: [
      "Buscá en el celular 5 o 6 sonidos de otra época: lluvia sobre chapa, un tren, campanas, una radio que se sintoniza, una pava que silba, un teléfono de disco.",
      "Ponelos en orden, listos para tocar.",
      "Elegí un parlante o subí un poco el volumen. Que se escuche bien.",
    ],
    necesitamos: [
      "Las tarjetas de Sonidos",
      "El celular con los sonidos",
      "Dos objetos para hacer ritmo: una cuchara y una mesa sirven",
    ],
    cancion: {
      que: "Pongan una canción de cuando tu mamá tenía unos 20 años. Por ejemplo, «La balsa» o «Yesterday».",
      consejo: "Preguntale: «¿Dónde estabas cuando la escuchaste por primera vez?».",
    },
    queDia: {
      que: "Tu mamá dice el día de hoy y lo escribe en la pizarra. Después cuenta qué sonidos escuchó hoy antes de que llegaras.",
      consejo: "Pájaros, tránsito, la radio, la pava. Todo vale.",
    },
    principal: {
      pasos: [
        "Pongan el primer sonido. Tu mamá cuenta qué cree que es y qué le hace acordar.",
        "Si no lo reconoce, no pasa nada. Lo escuchan otra vez o le contás vos qué es.",
        "Sigan con los demás, de a uno, sin apuro.",
        "Elijan una tarjeta de Sonidos y charlen. ¿Qué voz de tu familia reconocías enseguida?",
        "Para terminar, hagan ritmo juntas con la cuchara sobre la mesa. Una canción conocida: tu mamá marca y vos seguís. Después al revés.",
      ],
      siSeTraba: [
        "Si un sonido le trae tristeza, esperen. Tomale la mano. Siguen cuando ella quiera.",
        "Si no se acuerda de la letra de una canción, tarareen.",
        "Si el ritmo sale difícil, vayan más lento.",
      ],
    },
    cierre: {
      preguntas: [
        "¿Qué sonido extrañás de tu casa de chica?",
        "¿Qué canción te gustaría escuchar más seguido?",
        "¿Qué sonido te da calma?",
      ],
    },
    frase: "Hay canciones que me devuelven a mí.",
    paraLaHija:
      "No es un juego de acertar. Si no reconoce un sonido, lo importante es lo que cuenta alrededor.",
  },
  {
    n: 4,
    tema: "Caras y escenas",
    titulo: "Fotos que cuentan",
    idea: "Mirar fotos viejas y contar quiénes eran y qué pasaba.",
    antes: [
      "Elegí 4 o 5 fotos de la familia. Ojalá alguna con tu mamá joven.",
      "Si tenés pocas, usá las del celular.",
      "Si hay fotos de personas que ya no están, pensá cómo vas a acompañar si aparece tristeza.",
    ],
    necesitamos: [
      "Las tarjetas de Caras y escenas",
      "Las fotos",
      "Lápiz suave para escribir atrás",
    ],
    cancion: {
      que: "Pongan una canción que sonaba en las fiestas de la familia.",
      consejo: "Si hay ganas, miren la foto mientras suena la música.",
    },
    queDia: {
      que: "Tu mamá escribe el día de hoy en la pizarra. Después mira por la ventana y cuenta cómo está el día y con qué ropa salió.",
      consejo: "Es un ratito para estar en el presente, juntas.",
    },
    principal: {
      pasos: [
        "Pongan la primera foto sobre la mesa. Miren en silencio, unos 20 segundos.",
        "Tu mamá cuenta lo que ve y lo que recuerda: quiénes están, dónde fue, cómo estaban vestidos.",
        "Vos hacés una sola pregunta por foto: «¿Quién la sacó?» o «¿Qué día fue?».",
        "Ahora tapen la foto con una hoja. Tu mamá cuenta lo que se acuerda de la escena: «¿Qué había a la izquierda?». Después destapan y miran juntas. Sin puntos.",
        "Anoten atrás los nombres, el lugar y el año, más o menos: «alrededor de 1975».",
        "Dejen las fotos juntas sobre la mesa, como una pared de caras.",
      ],
      siSeTraba: [
        "Si no se acuerda de un nombre, dejalo. Anotá «no me acuerdo» y seguí.",
        "Si aparece tristeza, está bien. Quédense un rato en silencio.",
        "Probá con una tarjeta: «Contame cómo era tu primera amiga».",
      ],
    },
    cierre: {
      preguntas: [
        "¿Qué foto te hizo sonreír más?",
        "¿De quién te gustaría contarnos más la próxima vez?",
        "¿Qué foto querés tener en la heladera?",
      ],
    },
    frase: "Mirar atrás con cariño también me hace bien.",
    paraLaHija:
      "Si se emociona, no la apures a cambiar de tema. Acompañar es quedarte al lado.",
  },
  {
    n: 5,
    tema: "Usar dinero",
    titulo: "Hacemos las compras",
    idea: "Pensar en precios, sumar con calma y cuidar la plata.",
    antes: [
      "Juntá billetes y monedas de la casa, los que se usan hoy.",
      "Guardá un folleto de supermercado o de farmacia.",
      "Prepará una bolsita para el «almacén».",
    ],
    necesitamos: [
      "Las tarjetas de Usar dinero",
      "Billetes y monedas",
      "Un folleto de supermercado y lápiz",
    ],
    cancion: {
      que: "Pongan una canción alegre. Por ejemplo, «Color esperanza» o la que ella elija.",
      consejo: "Si quiere cantar, que cante. Después hablan de cosas serias.",
    },
    queDia: {
      que: "Tu mamá escribe el día de hoy en la pizarra. Después cuenta cuántos días faltan para el fin de semana.",
      consejo: "Que cuente con los dedos si quiere. No es una prueba.",
    },
    principal: {
      pasos: [
        "Charlen: ¿cuánto costaba el pan, el boleto o el cine cuando eras joven? Lo que ella recuerde.",
        "Armen una lista de 5 cosas con el folleto. Tu mamá suma más o menos, redondeando.",
        "Jueguen al almacén. Vos sos la cajera. Tu mamá paga con billetes y monedas. Después cambian los lugares.",
        "Tómense el tiempo. Contar la plata con calma es parte del juego.",
        "Hablen de cuidados: nadie del banco pide claves por teléfono. Nadie serio pide plata por mensaje urgente. Ante la duda, cortar y llamarte a vos.",
      ],
      siSeTraba: [
        "Probá con números redondos: de a 100, de a 500.",
        "Si no le gusta el juego, hagan la lista de compras de verdad para esta semana.",
        "Usá los billetes reales. Se ven y se tocan, y ayudan.",
      ],
    },
    cierre: {
      preguntas: [
        "¿Cuál fue tu primera plata propia? ¿En qué la usaste?",
        "¿Qué compraste una vez que te hizo muy feliz?",
        "¿Qué te da seguridad cuando manejás tu plata?",
      ],
    },
    frase: "Puedo manejar lo mío a mi ritmo.",
    paraLaHija:
      "Cuidar no es quitarle el manejo de su plata. Es acompañarla para que se sienta segura.",
  },
  {
    n: 6,
    tema: "Juegos de palabras",
    titulo: "Refranes y tutti frutti",
    idea: "Refranes, trabalenguas y un buen tutti frutti.",
    antes: [
      "Escribí 6 refranes por la mitad, en una hoja, para decir la primera parte.",
      "Preparen una hoja con 5 columnas para el tutti frutti.",
      "Dejá lapiceras que escriban fuerte.",
    ],
    necesitamos: [
      "Las tarjetas de Juegos de palabras",
      "Hoja y lapiceras",
      "Ganas de reírse",
    ],
    cancion: {
      que: "Pongan «Manuelita» o una canción con humor. Lo que más le guste a tu mamá.",
      consejo: "Hoy se juega. Que se rían.",
    },
    queDia: {
      que: "Tu mamá escribe el día de hoy. Después cuenta si conoce algún refrán de ese día de la semana.",
      consejo: "Por ejemplo: «martes 13, ni te cases ni te embarques».",
    },
    principal: {
      pasos: [
        "Refranes a medias: vos decís el comienzo y tu mamá lo completa. «Más vale pájaro en mano…», «A caballo regalado…», «Camarón que se duerme…».",
        "Después ella dice uno de los que se usaban en su casa y vos lo completás.",
        "Tutti frutti: una letra al azar y cuatro categorías, por ejemplo nombre, ciudad, fruta y animal. Sin cronómetro y sin puntos. Gana la que se divierte.",
        "Trabalenguas: «Tres tristes tigres tragaban trigo en un trigal». Primero lento, después un poco más rápido. Las risas son parte.",
        "Para terminar, inventen una palabra nueva y digan qué significa.",
      ],
      siSeTraba: [
        "Si no sale un refrán, pasen al siguiente. Ya vuelve.",
        "Si el tutti frutti cansa, hagan solo dos categorías.",
        "Si querés ayudarla, dale la primera letra de la palabra. Nada más.",
      ],
    },
    cierre: {
      preguntas: [
        "¿Qué dicho repetía tu mamá o tu abuela?",
        "¿Cuál es tu palabra favorita?",
        "¿Qué palabra inventada nos quedó para siempre?",
      ],
    },
    frase: "Reírme también es una forma de cuidarme.",
    paraLaHija:
      "Jugá de verdad. Si te equivocás vos, mejor. Así ella ve que equivocarse es normal.",
  },
  {
    n: 7,
    tema: "Noticias",
    titulo: "Lo que pasó y lo que pasa",
    idea: "Conversar sobre el mundo, lo de antes y lo de hoy.",
    antes: [
      "Elegí 3 noticias del diario, la radio o el celular.",
      "Que sean buenas o cercanas: del barrio, de la cultura, de la naturaleza, de deportes.",
      "Evitá las que angustian.",
    ],
    necesitamos: [
      "Las tarjetas de Noticias",
      "Diario, revista o celular",
      "Lápiz y una hoja para escribir un titular",
    ],
    cancion: {
      que: "Pongan una canción que les guste a las dos.",
      consejo: "Si no la hay, elijan una de las que ya escucharon en estas semanas.",
    },
    queDia: {
      que: "Tu mamá escribe el día de hoy. Vos buscás en el celular qué pasó un día como hoy hace muchos años y se lo leés.",
      consejo: "Preguntale: «¿Vos dónde estabas?».",
    },
    principal: {
      pasos: [
        "Leé un titular en voz alta. Tu mamá cuenta qué entendió y qué opina.",
        "Escuchá sin discutir. No hace falta que piensen igual.",
        "Hablen de lo que cambió: «¿Qué cosa de hoy no existía cuando eras joven?».",
        "Escriban juntas el titular de la semana de tu mamá. Por ejemplo: «Mamá recuperó la receta de los ñoquis».",
        "Lean el titular en voz alta, como si fuera el noticiero.",
      ],
      siSeTraba: [
        "Si la noticia le da miedo o tristeza, cámbienla. Hay otras.",
        "Si no quiere opinar, preguntale cómo lo habría contado ella.",
        "Si se enoja con la noticia, escuchala. No intentes convencerla.",
      ],
    },
    cierre: {
      preguntas: [
        "¿Qué hecho importante recordás haber vivido?",
        "¿Qué buena noticia te gustaría leer mañana?",
        "¿Qué cambió más desde que eras joven?",
      ],
    },
    frase: "Mi opinión cuenta.",
    paraLaHija:
      "No es un debate. Es una conversación. Escuchar otra forma de ver las cosas también es acompañar.",
  },
  {
    n: 8,
    tema: "Crear",
    titulo: "Algo nuestro",
    idea: "Crear algo juntas y cerrar el mes con cariño.",
    antes: [
      "Juntá revistas viejas, tijera, pegamento y hojas.",
      "Imprimí o separá el mandala de cierre.",
      "Tené a mano lápices de colores o fibras.",
      "Pensá una frase corta para decirle a tu mamá al final.",
    ],
    necesitamos: [
      "Las tarjetas de Crear",
      "Revistas, tijera, pegamento y hojas",
      "El mandala de cierre y lápices de colores",
    ],
    cancion: {
      que: "Volvé a la canción del primer encuentro. Es una forma de cerrar el círculo.",
      consejo: "Cantá con ella, como la primera vez.",
    },
    queDia: {
      que: "Tu mamá escribe el día de hoy con su mejor letra. Después miran la pizarra y repasan: ¿qué hicieron estas semanas?",
      consejo: "Que cuente lo que se acuerde. Vos completás si hace falta, con cariño.",
    },
    principal: {
      pasos: [
        "Repasen los 8 encuentros. ¿Cuál le gustó más? ¿Cuál menos?",
        "Hagan un collage: «Lo que me gusta de mi vida». Cada una recorta lo que le llama la atención de las revistas y lo pega.",
        "Pinten juntas el mandala de cierre, mientras suena la canción del primer encuentro. Sin apuro.",
        "Armen el plan para seguir: la app 3 veces por semana, un encuentro cuando puedan y los 10 minutos de movimiento todos los días.",
        "Para cerrar, leele a tu mamá la frase que pensaste. Sacate una foto con ella y con el collage.",
      ],
      siSeTraba: [
        "Si no sabe qué recortar, que mire las imágenes y señale las que le gustan.",
        "Si no quiere pintar, que mire cómo pintás vos.",
        "Si la despedida emociona, abrácense. Es parte del cierre.",
      ],
    },
    cierre: {
      preguntas: [
        "¿Qué me llevo de estas semanas?",
        "¿Qué quiero seguir haciendo?",
        "¿Qué quiero que hagamos juntas el mes que viene?",
      ],
    },
    frase: "Mi tiempo, mi ritmo, mi camino.",
    paraLaHija:
      "Cerrar no es terminar. Es poner fecha para el próximo rato juntas.",
  },
];

export const TARJETAS = [
  { tema: "Infancia", textos: [
    "¿Cómo se llamaba la calle donde vivías de chica? ¿Qué se veía desde la puerta?",
    "¿A qué jugabas? ¿Con quién? ¿Dónde?",
    "¿Qué olor te lleva directo a tu casa de chica?",
  ]},
  { tema: "Comida", textos: [
    "¿Cuál era la comida del domingo en tu casa?",
    "¿Quién cocinaba? ¿Qué te dejaban hacer a vos?",
    "¿Qué sabor te hace acordar a una fiesta?",
  ]},
  { tema: "Sonidos", textos: [
    "¿Qué canción te hace acordar a tu juventud?",
    "¿Qué sonido de tu casa de chica extrañás?",
    "¿Qué voz de tu familia reconocías enseguida?",
  ]},
  { tema: "Caras y escenas", textos: [
    "Pensá en una foto tuya de joven. ¿Dónde estabas? ¿Quién la sacó?",
    "¿Quién fue tu primera amiga? ¿Cómo era?",
    "Contame un día de fiesta en tu familia: ¿quiénes estaban? ¿Dónde se sentaba cada uno?",
  ]},
  { tema: "Usar dinero", textos: [
    "¿Cuál fue tu primera plata propia? ¿En qué la usaste?",
    "¿Cuánto costaba algo que recuerdes bien? El pan, el boleto, el cine.",
    "¿Qué compraste una vez que te hizo muy feliz?",
  ]},
  { tema: "Juegos de palabras", textos: [
    "Completá: «A caballo regalado…».",
    "Decí cinco palabras que empiecen con M.",
    "¿Qué dicho repetía tu mamá o tu abuela?",
  ]},
  { tema: "Noticias", textos: [
    "¿Qué hecho importante recordás haber vivido? ¿Dónde estabas?",
    "¿Qué cosa cambió más desde que eras joven?",
    "¿Qué buena noticia te gustaría leer mañana?",
  ]},
  { tema: "Crear", textos: [
    "¿Qué cosa hecha con tus manos recordás? Un tejido, una torta, una carta.",
    "Si hicieras un regalo con tus manos, ¿para quién sería? ¿Qué sería?",
    "¿Qué te gustaría crear con tiempo y sin apuro?",
  ]},
];

export const MOVIMIENTO = [
  { n: 1, nombre: "Entrar en calor", como: "Marchá en el lugar, con los brazos sueltos. Sentí que respirás.", dosis: "1 minuto", figura: "marcha" },
  { n: 2, nombre: "Sentarse y pararse", como: "Sentada en una silla firme, parate y volvé a sentarte, despacio. Usá las manos solo si lo necesitás.", dosis: "8 veces, 2 series", figura: "silla" },
  { n: 3, nombre: "Subir los talones", como: "De pie, apoyada en la mesada o el respaldo. Subí en puntas de pie y bajá lento.", dosis: "10 veces", figura: "talones" },
  { n: 4, nombre: "Un pie delante del otro", como: "Apoyada, poné un pie delante del otro, como en una línea. Contá hasta 10 y cambiá.", dosis: "10 segundos de cada lado", figura: "linea" },
  { n: 5, nombre: "Rodillas arriba", como: "Apoyada, subí una rodilla y después la otra, como si subieras un escalón.", dosis: "10 veces cada una", figura: "rodilla" },
  { n: 6, nombre: "Estirar y respirar", como: "Subí los brazos y respirá hondo. Soltá el aire despacio.", dosis: "5 respiraciones", figura: "brazos" },
];

export const AVISO = "Este cuaderno no reemplaza la evaluación ni el tratamiento médico. Ante cambios en la memoria, consultá a un profesional.";
export const FIRMA = "Daniela Navarro";
export const MARCA = "Longevidad Emocional";
export const LEMA = "Mente activa, cuerpo en movimiento, tiempo juntas.";
