// Textos generales del kit (todo lo que no es un encuentro).
// Voseo rioplatense, frases cortas, sin tono juguetón. Nada de prometer prevención.

export const CUADERNO = {
  portada: {
    titulo: "La hora del té",
    marca: "Mente Viva · NeuroGym",
    bajada: "4 semanas para estar juntas",
    tipo: "Cuaderno · 8 encuentros",
  },
  bienvenida: {
    kick: "Antes de empezar",
    titulo: "Un regalo para estar juntas",
    intro:
      "Este cuaderno las acompaña durante 4 semanas. Son 8 encuentros de 45 minutos para charlar, recordar, jugar y crear.",
    roles: [
      { quien: "Mamá", que: "Es la protagonista. Pone sus recuerdos, su ritmo y su voz." },
      { quien: "Hija", que: "Acompaña. Escucha, pregunta y ayuda a escribir." },
    ],
    comoUsarloTitulo: "Cómo usarlo",
    comoUsarlo: [
      "Elijan un momento tranquilo, dos veces por semana.",
      "Leé el encuentro antes. Te lleva 5 minutos.",
      "Sigan los seis momentos, en orden.",
      "Marquen cada encuentro en la pizarra de la heladera.",
    ],
    reglas: "No hay respuestas equivocadas. No hay nota. Si un día no hay ganas, se deja para mañana.",
    importante: "Importante",
  },
  ritmo: {
    kick: "Ritmo",
    titulo: "Las 4 semanas",
    bajada: "Cada semana tiene el mismo ritmo.",
    filas: [
      { semana: 1, nombre: "Empezar" },
      { semana: 2, nombre: "Sostener" },
      { semana: 3, nombre: "Desafiarse" },
      { semana: 4, nombre: "Cerrar" },
    ],
    cols: { app: "App", encuentros: "Encuentros", movimiento: "Movimiento" },
    app: "3 veces, de 30 a 40 minutos",
    mov: "Todos los días, 10 minutos de la lámina",
    nota: "Con 3 veces por semana en la app alcanza. Más no es mejor: descansar también cuenta. La app tiene ejercicios con niveles que se ajustan a vos.",
  },
  encuentro: {
    kick: "Cada encuentro",
    titulo: "Cómo es un encuentro",
    bajada: "Siempre tiene la misma forma. Así se vuelve fácil.",
    momentos: [
      "Una canción para entrar en clima.",
      "Un ratito para ubicarse en el día, con la pizarra.",
      "El tema del encuentro: recuerdos, comida, sonidos y más.",
      "Una serie o un problema, en tres versiones.",
      "Se pregunta una opinión o un recuerdo, no datos.",
      "Un mandala para pintar con calma.",
    ],
    reglasTitulo: "Cuatro reglas de oro",
    reglas: ["No se corrige.", "No se examina.", "No hay respuestas equivocadas.", "Se puede parar cuando quiera."],
  },
  razonamientoIntro: "Elegí una versión. Las respuestas están al final.",
  comoMeSenti: "¿Cómo me sentí hoy?",
  cierreMarcar: "Marquen el encuentro en la pizarra de la heladera.",
  mandalaTitulo: "Mandala de cierre",
  mandalaMarcador: "Acá va el mandala de cierre",
  respuestas: {
    kick: "Al final",
    titulo: "Respuestas posibles",
    intro:
      "Para mirar juntas, sin corregir. Una serie puede seguir de más de una forma: esta es la más común.",
  },
  registro: {
    kick: "Registro",
    titulo: "Mis 4 semanas",
    bajada: "Marcá cada círculo cuando lo hagas.",
    cols: ["Encuentros", "Movimiento", "App"],
    semana: "Semana",
    pie: "Una cosa linda de estas 4 semanas:",
  },
  final: {
    kick: "Cierre",
    titulo: "Y ahora, ¿qué sigue?",
    intro: "Terminaron los 8 encuentros. Lo que armaron juntas sigue ahí.",
    seguir: [
      "La app, 3 veces por semana.",
      "Un encuentro cuando puedan: elijan un tema y unas tarjetas.",
      "Los 10 minutos de movimiento, todos los días.",
      "Una caminata, una llamada o un té, cada tanto, solo para charlar.",
    ],
    preguntas: ["Lo que más me gustó fue…", "Lo que quiero repetir es…", "La próxima vez me gustaría…"],
  },
  diploma: {
    kick: "Para terminar",
    titulo: "Completamos 4 semanas",
    texto: "Nos dimos tiempo para recordar, conversar y crear juntas.",
    mama: "Mamá",
    hija: "Hija",
    fecha: "Fecha",
  },
  dinero: {
    kick: "Recortable",
    titulo: "Monedas y billetes de juguete",
    bajada: "Recortá por las líneas. Son de juguete: no sirven para pagar.",
    leyenda: "DE JUGUETE",
  },
  contratapa: {
    texto: "Mente activa, cuerpo en movimiento, tiempo juntas.",
  },
};

// Una página al final de cada semana. Texto de controles: Dani lo ajusta.
export const PAUSAS = [
  {
    semana: 1,
    titulo: "Salí a caminar",
    texto:
      "Caminar unos 30 minutos, de a poco y mejor acompañada. Empezá con lo que puedas y sumá un poco cada día. Marcá cada caminata en la pizarra.",
    campos: ["¿Dónde voy a caminar?", "¿A qué hora?", "¿Con quién?"],
    nota: "Si tenés alguna indicación médica sobre la actividad, consultá antes de aumentarla.",
  },
  {
    semana: 2,
    titulo: "Respirá",
    texto:
      "Dos minutos de respiración tranquila. Inhalá por la nariz contando hasta 4. Exhalá despacio contando hasta 6. Repetí durante dos minutos.",
    pasos: ["Sentate con la espalda apoyada.", "Inhalá contando 4.", "Exhalá contando 6.", "Repetí durante 2 minutos."],
    campos: ["¿Cuándo me viene bien respirar?"],
    nota: "En la app podés usar «Respiración Consciente».",
  },
  {
    semana: 3,
    titulo: "Tomate el té y conversá",
    texto:
      "Un rato sin pantallas. Una taza, una silla cómoda y una persona querida. Esta semana, llamá o visitá a alguien que hace tiempo no ves.",
    pregunta: "Una pregunta para charlar: ¿qué es lo mejor que te pasó este mes?",
    campos: ["¿A quién voy a llamar o visitar?", "¿Cuándo?"],
  },
  {
    semana: 4,
    titulo: "Controles que no hay que dejar pasar",
    texto:
      "Ver y oír bien te ayuda a conversar, a moverte con seguridad y a disfrutar de lo que hacés. Si hace más de un año que no te controlás la vista y el oído, pedí un turno esta semana.",
    controles: [
      { que: "Vista", quien: "Oftalmólogo" },
      { que: "Oído", quien: "Fonoaudiólogo u otorrinolaringólogo, con audiometría" },
    ],
    campos: ["Fecha del turno de vista:", "Fecha del turno de oído:"],
  },
];

export const GUIA_HIJA = {
  portada: {
    tipo: "Para la hija",
    titulo: "Guía para vos",
    bajada: "Acompañar sin corregir ni examinar",
    frase: "No le regales otra cosa. Regalale 4 semanas juntas.",
    producto: "La hora del té · Mente Viva · NeuroGym",
  },
  lugar: {
    kick: "Para empezar",
    titulo: "Tu lugar en estos encuentros",
    parrafos: [
      "Le estás regalando a tu mamá tiempo, atención y compañía. Eso es lo más importante del kit.",
      "En los encuentros, ella es la protagonista. Vos no sos la maestra ni la evaluadora. Sos quien escucha, pregunta con cariño y ayuda a escribir.",
      "Lo que importa es lo que opina y recuerda tu mamá, no que acierte. No hace falta que salga perfecto. Alcanza con que estén juntas, con calma.",
    ],
  },
  siNo: {
    kick: "Qué hacer",
    titulo: "Lo que sí y lo que no",
    siTitulo: "Sí",
    noTitulo: "No",
    si: [
      "Escuchar sin apuro.",
      "Preguntar con curiosidad.",
      "Esperar. El silencio también es parte.",
      "Celebrar lo que cuenta, no lo que acierta.",
    ],
    no: [
      "Corregirla: fechas, nombres, datos.",
      "Completar sus frases.",
      "Decir «ya me lo contaste».",
      "Tomarlo como una prueba.",
    ],
  },
  frases: {
    kick: "Qué decir",
    titulo: "Frases",
    ayudanTitulo: "Para decir",
    ayudan: ["«Contame más.»", "«¿Y después qué pasó?»", "«¿Cómo era eso?»", "«Miremos juntas.»", "«Me gusta escucharte.»"],
    cambiarTitulo: "Mejor no decir",
    cambiar: ["«¿Cómo que no te acordás?»", "«No, no fue así.»", "«Dale, pensá.»", "«Mejor te lo cuento yo.»"],
  },
  siPasa: {
    kick: "Qué pasa si…",
    titulo: "Si se traba, se cansa o se emociona",
    casos: [
      { cuando: "Se traba", que: "Cambiá de tarjeta o de pregunta. Probá con un olor, un sonido o un color. Si no sale, no pasa nada." },
      { cuando: "Se cansa", que: "Hagan una pausa con agua o té. Si hace falta, terminen antes. Mejor poco y con calma." },
      { cuando: "Se emociona", que: "Quedate al lado. Tomale la mano. No cambies de tema enseguida. Seguí cuando ella quiera." },
      { cuando: "Se enoja", que: "No discutas. Bajá el ritmo. Agradecele que te cuente." },
    ],
  },
  encuentro: {
    kick: "Cada encuentro",
    titulo: "Los seis momentos",
    bajada: "Son 45 minutos.",
    consejo: "Mirá el reloj solo para ordenarte. Si un momento lleva más tiempo, está bien.",
  },
  preparar: {
    kick: "Tu preparación",
    titulo: "Qué preparar antes",
    bajada: "Con 5 minutos alcanza.",
  },
  ritmo: {
    kick: "Ritmo",
    titulo: "La semana de tu mamá",
    items: [
      { que: "App", texto: "3 veces por semana, de 30 a 40 minutos. Con 3 veces alcanza. Más no es mejor: descansar también cuenta." },
      { que: "Encuentros", texto: "2 por semana, de 45 minutos, con vos." },
      { que: "Movimiento", texto: "10 minutos de la lámina todos los días. Y una caminata de unos 30 minutos, 4 veces por semana, de a poco." },
    ],
    nota: "Si tu mamá tiene alguna indicación médica sobre la actividad, consultá antes de aumentarla.",
  },
  controles: {
    kick: "Salud",
    titulo: "Turnos de vista y oído",
    texto:
      "Ver y oír bien ayuda a conversar, a moverse con seguridad y a disfrutar de lo que se hace. Si hace más de un año que tu mamá no se controla la vista y el oído, ayudala a sacar los turnos.",
    comoTitulo: "Cómo ayudar",
    como: [
      "Preguntale con calma cuándo fue el último control.",
      "Ofrecete a sacar el turno con ella, por teléfono o por internet.",
      "Para la vista: oftalmólogo. Para el oído: fonoaudiólogo u otorrino, con audiometría.",
      "Acompañala el día del turno. Que lleve los anteojos o audífonos que usa hoy.",
      "Anoten las fechas en la página de la semana 4 del cuaderno.",
    ],
    cierre: "Si le cuesta aceptarlo, hablalo sin presionar y volvé a proponerlo otro día.",
  },
  cuidate: {
    kick: "Para vos",
    titulo: "Cuidate vos también",
    parrafos: [
      "Acompañar cansa, aunque sea lindo. Tomate un rato para vos después de cada encuentro.",
      "Si notás cambios en la memoria de tu mamá que te preocupan, hablalo con ella y consultá a un profesional.",
    ],
    importante: "Importante",
  },
  contratapa: "Mente activa, cuerpo en movimiento, tiempo juntas.",
};

export const PIZARRA = {
  titulo: "Hoy es…",
  campos: ["Día", "Número", "Mes"],
  semana: "Esta semana",
  filas: [
    { clave: "encuentro", nombre: "Encuentro" },
    { clave: "movimiento", nombre: "Movimiento" },
    { clave: "app", nombre: "App" },
  ],
  dias: ["L", "M", "M", "J", "V", "S", "D"],
  pie: "Una cosa linda de esta semana:",
};

export const LAMINA = {
  kick: "Mente Viva · NeuroGym",
  titulo: "10 minutos de fuerza y equilibrio",
  bajada: "Para hacer todos los días, con calma.",
  antes: [
    "Zapatos cómodos y una silla firme.",
    "Una mesada o un respaldo para apoyarte.",
    "Si algo te duele, te marea o te falta el aire, pará.",
  ],
  aviso:
    "Esta lámina no reemplaza la evaluación ni el tratamiento médico. Ante dudas, consultá a un profesional.",
};

export const TARJETAS_TEXTOS = {
  dorsoTitulo: "Recuerdos",
  dorsoBajada: "La hora del té",
};

export const TARJETA_APP = {
  titulo: "Mente Viva",
  bajada: "Mantené la mente activa y desafiada, a tu ritmo.",
  pasos: ["Creá tu cuenta con tu mail.", "Elegí un ejercicio.", "Seguí 3 veces por semana."],
  direccion: "menteviva.daninavarro.com.ar/app.html",
  url: "https://menteviva.daninavarro.com.ar/app.html",
};
