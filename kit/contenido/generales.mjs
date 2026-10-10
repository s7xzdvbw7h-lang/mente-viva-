// Textos generales del kit (todo lo que no es un encuentro).
// Voseo, frases cortas, sin lenguaje técnico.

export const CUADERNO = {
  portada: {
    titulo: "Mente Viva",
    marca: "NeuroGym",
    bajada: "4 semanas de mente activa, cuerpo en movimiento y tiempo juntas",
    tipo: "Cuaderno guía · 8 encuentros",
  },
  bienvenida: {
    titulo: "Un regalo para estar juntas",
    intro:
      "Este cuaderno las acompaña durante 4 semanas. Son 8 encuentros de 45 minutos para charlar, recordar, jugar y crear.",
    roles: [
      { quien: "Mamá", que: "Es la protagonista. Pone sus recuerdos, su ritmo y su voz." },
      { quien: "Hija", que: "Acompaña. Escucha, pregunta y ayuda a escribir." },
    ],
    comoUsarlo: [
      "Elegí un momento tranquilo, dos veces por semana.",
      "Leé el encuentro antes. Te lleva 5 minutos.",
      "Sigan los cuatro momentos, en orden.",
      "Marquen cada encuentro en la pizarra de la heladera.",
    ],
    reglas: "No hay respuestas equivocadas. No hay nota. Si un día no hay ganas, se deja para mañana.",
  },
  semana: {
    titulo: "Su semana",
    bajada: "Un ritmo simple para cuatro semanas.",
    bloques: [
      { grande: "3", unidad: "veces por semana", nombre: "La app", texto: "Ejercicios para hacer sola, con la app Mente Viva. Con 20 a 30 minutos por vez alcanza." },
      { grande: "2", unidad: "veces por semana", nombre: "Los encuentros", texto: "45 minutos juntas. Siempre igual: canción, ¿qué día es hoy?, actividad y charla." },
      { grande: "10", unidad: "minutos por día", nombre: "Movimiento", texto: "Fuerza y equilibrio, todos los días. Está en la lámina." },
    ],
    cuadro: "Los 8 encuentros",
  },
  encuentro: {
    titulo: "Cómo es cada encuentro",
    bajada: "Siempre tiene la misma forma. Así se vuelve fácil.",
    partes: [
      { min: 5, nombre: "Canción de bienvenida", texto: "Una canción para entrar en clima." },
      { min: 5, nombre: "¿Qué día es hoy?", texto: "Un ratito para ubicarse en el día, charlando." },
      { min: 25, nombre: "Actividad principal", texto: "Cada encuentro tiene su tema: recuerdos, comida, sonidos y más." },
      { min: 10, nombre: "Charla de cierre", texto: "Tres preguntas, un registro y la fecha del próximo." },
    ],
    reglasTitulo: "Cuatro reglas de oro",
    reglas: [
      "No se corrige.",
      "No se examina.",
      "No hay respuestas equivocadas.",
      "Se puede parar cuando quiera.",
    ],
  },
  cierreEncuentro: "Después: marquen el encuentro en la pizarra de la heladera y anoten cuándo es el próximo.",
  comoMeSenti: "¿Cómo me sentí hoy?",
  final: {
    titulo: "Y ahora, ¿qué sigue?",
    intro: "Terminaron los 8 encuentros. Lo que armaron juntas sigue ahí.",
    seguir: [
      "La app, 3 veces por semana.",
      "Un encuentro cuando puedan: elijan un tema y una tarjeta.",
      "Los 10 minutos de movimiento, todos los días.",
      "Una llamada o un mate, cada tanto, solo para charlar.",
    ],
    preguntas: ["Lo que más me gustó fue…", "Lo que quiero repetir es…", "La próxima vez me gustaría…"],
  },
  recuerdos: {
    titulo: "Mis recuerdos",
    bajada: "Un lugar para escribir lo que se acuerden, con la letra y el ritmo que quieran.",
  },
  contratapa: {
    texto: "Mente activa, cuerpo en movimiento, tiempo juntas.",
  },
};

export const GUIA_HIJA = {
  portada: {
    titulo: "Guía para vos",
    bajada: "Acompañar sin corregir ni examinar",
    tipo: "Para la hija · Mente Viva NeuroGym",
  },
  lugar: {
    titulo: "Tu lugar en estos encuentros",
    parrafos: [
      "Le estás regalando a tu mamá tiempo, atención y compañía. Eso es lo más importante del kit.",
      "En los encuentros, ella es la protagonista. Vos no sos la maestra ni la evaluadora. Sos quien escucha, pregunta con cariño y ayuda a escribir.",
      "No hace falta que sea perfecto. Alcanza con que estén juntas, con calma.",
    ],
  },
  siNo: {
    titulo: "Lo que sí y lo que no",
    si: [
      "Escuchar sin apuro.",
      "Preguntar con curiosidad.",
      "Esperar. El silencio también es parte.",
      "Reírte con ella.",
      "Celebrar lo que cuenta, no lo que «acierta».",
    ],
    no: [
      "Corregirla: fechas, nombres, datos.",
      "Completar sus frases por ella.",
      "Decir «ya me lo contaste».",
      "Tomarle los ejercicios como una prueba.",
      "Hacer comparaciones con otras personas.",
    ],
    siTitulo: "Sí",
    noTitulo: "No",
  },
  frases: {
    titulo: "Frases que ayudan",
    ayudan: [
      "«Contame más.»",
      "«¿Y después qué pasó?»",
      "«¿Cómo era eso?»",
      "«No me acuerdo yo tampoco. Miremos juntas.»",
      "«Me encanta escucharte.»",
    ],
    evitar: [
      "«¿Cómo que no te acordás?»",
      "«No, no fue así.»",
      "«Dale, pensá.»",
      "«Mejor te lo cuento yo.»",
    ],
    ayudanTitulo: "Para decir",
    evitarTitulo: "Para evitar",
  },
  siPasa: {
    titulo: "Si se traba, se cansa o se emociona",
    casos: [
      { cuando: "Se traba", que: "Cambiá de tarjeta o de pregunta. Probá con un olor, un sonido o un color. Si no sale, no pasa nada." },
      { cuando: "Se cansa", que: "Hagan una pausa con agua o mate. Si hace falta, terminen antes. Mejor poco y bien." },
      { cuando: "Se emociona", que: "Quedate al lado. Tomale la mano. No cambies de tema enseguida. Seguí cuando ella quiera." },
      { cuando: "Se enoja o se frustra", que: "No discutas. Bajá el ritmo. Dale las gracias por contarte." },
    ],
  },
  semana: {
    titulo: "Qué preparar antes de cada encuentro",
    bajada: "Con 5 minutos alcanza.",
  },
  cuidate: {
    titulo: "Cuidate vos también",
    parrafos: [
      "Acompañar cansa, aunque sea lindo. Tomate un rato para vos después de cada encuentro.",
      "Si notás cambios en su memoria o en su día a día que te preocupan, hablalo con ella y consultá a un profesional.",
    ],
  },
  contratapa: "Mente activa, cuerpo en movimiento, tiempo juntas.",
};

export const PIZARRA = {
  titulo: "Mi semana",
  bajada: "Pegala en la heladera. Marcá cada círculo cuando lo hagas.",
  columnas: [
    { nombre: "Encuentros", n: 2 },
    { nombre: "App", n: 3 },
    { nombre: "Movimiento", n: 7, dias: ["L", "M", "M", "J", "V", "S", "D"] },
  ],
  pie: "Una cosa linda de esta semana:",
};

export const LAMINA = {
  titulo: "10 minutos de fuerza y equilibrio",
  bajada: "Para hacer todos los días, con calma y sin apuro.",
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
  dorsoBajada: "Mente Viva · NeuroGym",
  enBlanco: "Tu recuerdo",
  enBlancoBajada: "Escribilo o dibujalo acá.",
};

export const MANDALAS = {
  titulo: "Mandala de la semana",
  bajada: "Pintalo con calma. No hay colores equivocados.",
};
