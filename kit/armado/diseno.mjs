// Sistema de diseño del cuaderno "La hora del té".
// Paleta Luz plena v3: marfil, cacao y rosa de las cenizas, con el rosa velado de la marca y un tono más claro
// de los mismos colores para fondos y paneles. Dos tipografías: Fraunces y Manrope.

export const C = {
  marfil: "#F7F1E9",
  cacao: "#4A3B33",
  rosa: "#8E4E52",
  velado: "#E4D3CD", // rosa velado de la marca
  suave: "#EEE3DC", // tono claro del mismo rosa sobre marfil
  rosaSobre: "#9B6264", // sobre el rosa de la portada: tono apenas más claro
  rosaLinea: "#B58789", // línea tono sobre tono sobre el rosa
};

// ---------------------------------------------------------------- íconos 24 × 24
const ico = (cuerpo, color, grosor = 1.7) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="${grosor}" stroke-linecap="round" stroke-linejoin="round">${cuerpo}</svg>`;

const FORMAS = {
  nota: `<path d="M9 18V6l10-2v12"/><circle cx="6.5" cy="18" r="2.5"/><circle cx="16.5" cy="16" r="2.5"/>`,
  calendario: `<rect x="4" y="5.5" width="16" height="14.5" rx="2.5"/><path d="M4 10h16M8.5 3.5v4M15.5 3.5v4M8 14h2M13 14h3M8 17h2"/>`,
  cartas: `<rect x="4.5" y="6" width="10.5" height="14" rx="2" transform="rotate(-9 10 13)"/><rect x="9.5" y="4" width="10.5" height="14" rx="2" transform="rotate(8 14 11)"/>`,
  bombilla: `<path d="M9 17.5h6M10 20.5h4M12 3.5a6 6 0 0 0-3.5 10.9c.7.6 1 1.3 1 2.1h5c0-.8.3-1.5 1-2.1A6 6 0 0 0 12 3.5z"/>`,
  charla: `<path d="M4 5h16v11H11l-4.5 3.5V16H4z"/><path d="M8 9.5h8M8 12.5h5"/>`,
  loto: `<path d="M12 4.5c-2.4 3.4-2.4 9 0 13 2.4-4 2.4-9.6 0-13zM4.5 8.5c3.4 0 6.6 3.2 7.5 9-4.4 0-7.5-3.4-7.5-9zM19.5 8.5c-3.4 0-6.6 3.2-7.5 9 4.4 0 7.5-3.4 7.5-9z"/><path d="M4 20h16"/>`,
  corazon: `<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/>`,
  brote: `<path d="M12 21v-9.5M12 11.5c0-4 3-6.5 7.5-6.5 0 4-3 6.5-7.5 6.5zM12 15c0-3-2.5-5-6.5-5 0 3 2.5 5 6.5 5z"/>`,
  reloj: `<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.2 2"/>`,
  check: `<path d="M5 12.5l4.5 4.5L19 7.5"/>`,
  tijera: `<circle cx="6.5" cy="7" r="2.6"/><circle cx="6.5" cy="17" r="2.6"/><path d="M8.7 8.4L20 17M8.7 15.6L20 7"/>`,
  lapiz: `<path d="M4 20l1-4.5L16.5 4a2 2 0 0 1 3 3L8 18.5 4 20z"/><path d="M14 6.5l3.5 3.5"/>`,
  caminar: `<circle cx="13" cy="4.5" r="2"/><path d="M13 7.5 11 13l3 2.5 1 5.5M11 13l-3 7M12 9l-3.5 2L7 14M12.5 9.2l3 1.8 2.2-.8"/>`,
  respirar: `<path d="M3 9h10a2.5 2.5 0 1 0-2.5-2.5M3 13h14a2.5 2.5 0 1 1-2.5 2.5M3 17h7a2 2 0 1 1-2 2"/>`,
  taza: `<path d="M5 10h12v4.5A4.5 4.5 0 0 1 12.5 19h-3A4.5 4.5 0 0 1 5 14.5z"/><path d="M17 11h1.5a2.5 2.5 0 0 1 0 5H16.5M8 3.5c-1 1 1 2-.2 3M12 3.5c-1 1 1 2-.2 3"/>`,
  celular: `<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/>`,
  ojo: `<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>`,
  estrella: `<path d="M12 3.5l2.6 5.6 6 .7-4.5 4.1 1.3 6L12 17l-5.4 2.9 1.3-6L3.4 9.8l6-.7z"/>`,
  libro: `<path d="M4 5.5c3-1.2 6-1.2 8 .8 2-2 5-2 8-.8v13c-3-1.2-6-1.2-8 .8-2-2-5-2-8-.8z"/><path d="M12 6.3v13"/>`,
};
export const icono = (nombre, color = C.rosa, grosor) => ico(FORMAS[nombre], color, grosor);

// ---------------------------------------------------------------- loto relleno / línea (grupo SVG)
function petalo(rIn, rOut, ancho) {
  const h = rOut - rIn;
  const y1 = -(rIn + h * 0.25);
  const y2 = -(rOut - h * 0.3);
  return `M0 ${-rIn} C ${-ancho} ${y1}, ${-ancho} ${y2}, 0 ${-rOut} C ${ancho} ${y2}, ${ancho} ${y1}, 0 ${-rIn} Z`;
}
export function lotoGrupo({ anillos, relleno = "none", linea = C.rosa, grosor = 1, centro }) {
  let g = "";
  anillos.forEach((a, idx) => {
    const rW = a.rIn + 0.55 * (a.rOut - a.rIn);
    const ancho = (0.46 * ((2 * Math.PI * rW) / a.n)) / 0.75;
    const giro = (idx % 2) * (180 / a.n);
    const d = petalo(a.rIn, a.rOut, ancho);
    for (let i = 0; i < a.n; i++) g += `<path d="${d}" transform="rotate(${(giro + (360 / a.n) * i).toFixed(2)})"/>`;
  });
  if (centro) g += `<circle r="${centro}"/>`;
  return `<g fill="${relleno}" stroke="${linea}" stroke-width="${grosor}" stroke-linejoin="round" stroke-linecap="round">${g}</g>`;
}
const ANILLOS_LOTO = [
  { n: 12, rIn: 52, rOut: 94 },
  { n: 12, rIn: 34, rOut: 72 },
  { n: 8, rIn: 16, rOut: 50 },
];
export const loto = (color = C.rosa, grosor = 1, relleno = "none", lado = 200) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-100 -100 200 200">${lotoGrupo({ anillos: ANILLOS_LOTO, relleno, linea: color, grosor: grosor * (200 / lado), centro: 10 })}</svg>`;

// ---------------------------------------------------------------- escena de té (portada, diploma, aperturas)
export function escenaTe({ sobreRosa = true } = {}) {
  const fondo = sobreRosa
    ? lotoGrupo({ anillos: ANILLOS_LOTO, relleno: C.rosaSobre, linea: C.rosaLinea, grosor: 1.6, centro: 10 })
    : lotoGrupo({ anillos: ANILLOS_LOTO, relleno: C.suave, linea: C.velado, grosor: 1.6, centro: 10 });
  const L = C.cacao, M = C.marfil, V = C.velado, R = C.rosa;
  const vapor = (x, y, esc = 1) =>
    `<path transform="translate(${x} ${y}) scale(${esc})" d="M0 0c-7-9 7-14 0-24s7-14 0-24" fill="none" stroke="${sobreRosa ? M : R}" stroke-width="3.4" stroke-linecap="round"/>`;
  const taza = (x) =>
    `<g transform="translate(${x} 0)">` +
    `<ellipse cx="0" cy="206" rx="36" ry="8" fill="${V}" stroke="${L}" stroke-width="3"/>` +
    `<path d="M-24 168 h48 c0 24 -10 38 -24 38 s-24 -14 -24 -38 z" fill="${M}" stroke="${L}" stroke-width="3"/>` +
    `<path d="M-23 180 h46" stroke="${R}" stroke-width="5" fill="none"/>` +
    `<path d="M24 174 c14 0 14 20 -2 22" fill="none" stroke="${L}" stroke-width="3" stroke-linecap="round"/>` +
    `<ellipse cx="0" cy="168" rx="24" ry="5" fill="${V}" stroke="${L}" stroke-width="3"/></g>`;
  const flor = (x, y, r, col) => {
    let p = "";
    for (let i = 0; i < 5; i++) p += `<ellipse cx="0" cy="${-r}" rx="${r * 0.62}" ry="${r}" fill="${col}" transform="rotate(${i * 72})"/>`;
    return `<g transform="translate(${x} ${y})" stroke="${L}" stroke-width="1.6">${p}<circle r="${r * 0.42}" fill="${C.marfil}" stroke="${L}" stroke-width="1.6"/></g>`;
  };
  const brillo = (x, y, s) =>
    `<path transform="translate(${x} ${y}) scale(${s})" d="M0-10C1 -3 3 -1 10 0 3 1 1 3 0 10-1 3-3 1-10 0-3-1-1-3 0-10z" fill="${sobreRosa ? M : R}"/>`;
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 250">` +
    `<g transform="translate(150 118) scale(1.18)">${fondo}</g>` +
    // mesa
    `<ellipse cx="150" cy="222" rx="132" ry="14" fill="${V}" stroke="${L}" stroke-width="3"/>` +
    `<ellipse cx="150" cy="218" rx="112" ry="9" fill="none" stroke="${R}" stroke-width="2.2" stroke-dasharray="1 6" stroke-linecap="round"/>` +
    taza(58) + taza(242) +
    // tetera
    `<path d="M127 196 h46 v10 a5 5 0 0 1 -5 5 h-36 a5 5 0 0 1 -5 -5 z" fill="${V}" stroke="${L}" stroke-width="3"/>` +
    `<path d="M104 112 C64 100 60 160 106 160" fill="none" stroke="${L}" stroke-width="12" stroke-linecap="round"/>` +
    `<path d="M104 112 C64 100 60 160 106 160" fill="none" stroke="${M}" stroke-width="5" stroke-linecap="round"/>` +
    `<path d="M196 118 C224 118 228 94 242 78 L252 86 C240 100 240 138 194 146 Z" fill="${M}" stroke="${L}" stroke-width="3" stroke-linejoin="round"/>` +
    `<path d="M100 130 C100 86 200 86 200 130 C200 176 176 198 150 198 C124 198 100 176 100 130 Z" fill="${M}" stroke="${L}" stroke-width="3"/>` +
    `<path d="M101 142 Q150 164 199 142" fill="none" stroke="${R}" stroke-width="5"/>` +
    flor(150, 118, 11, R) +
    `<g fill="${R}"><circle cx="118" cy="154" r="2.6"/><circle cx="134" cy="161" r="2.6"/><circle cx="150" cy="164" r="2.6"/><circle cx="166" cy="161" r="2.6"/><circle cx="182" cy="154" r="2.6"/></g>` +
    `<path d="M114 98 C118 70 182 70 186 98 Z" fill="${M}" stroke="${L}" stroke-width="3" stroke-linejoin="round"/>` +
    `<path d="M124 90 h52" stroke="${R}" stroke-width="3.4" stroke-linecap="round"/>` +
    `<circle cx="150" cy="66" r="8" fill="${R}" stroke="${L}" stroke-width="3"/>` +
    vapor(250, 72, 0.9) + vapor(58, 160, 0.7) + vapor(242, 160, 0.7) + vapor(150, 52, 0.8) +
    brillo(40, 70, 1.4) + brillo(262, 128, 1) + brillo(26, 150, 0.9) + brillo(276, 52, 1.1) + brillo(96, 28, 0.9) + brillo(212, 24, 1.2) +
    `</svg>`
  );
}

// ---------------------------------------------------------------- ramita (para divisores y esquinas)
export function ramita(color = C.rosa, relleno = C.velado, largo = 100) {
  const hoja = (x, y, ang) => `<ellipse cx="0" cy="-7" rx="3.4" ry="7.5" transform="translate(${x} ${y}) rotate(${ang})" fill="${relleno}"/>`;
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${largo} 24" fill="none" stroke="${color}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">` +
    `<path d="M2 12 H${largo - 2}"/>` +
    [0.14, 0.3, 0.46, 0.62, 0.78].map((f, i) => hoja(largo * f, 12, i % 2 ? 62 : -62) + hoja(largo * f + 6, 12, i % 2 ? -62 : 62)).join("") +
    `<circle cx="${largo / 2}" cy="12" r="3.2" fill="${color}"/></svg>`
  );
}

// ---------------------------------------------------------------- lengüetas laterales (un índice para ubicarse)
// 8 lengüetas sobre el borde exterior; la del encuentro actual va llena.
export function lenguetas({ W, H, S, esVerso, actual }) {
  const n = 8, alto = 26, sep = 3.2, top = S + 24;
  let h = "";
  for (let i = 1; i <= n; i++) {
    const y = top + (i - 1) * (alto + sep);
    const activa = i === actual;
    const bg = activa ? C.rosa : C.velado;
    const col = activa ? C.marfil : C.rosa;
    const ancho = activa ? 12 : 9; // mm visibles desde el corte (más el sangrado)
    const lado = esVerso ? `left:0;border-radius:0 4mm 4mm 0;` : `right:0;border-radius:4mm 0 0 4mm;`;
    const rel = esVerso ? `padding-left:${S}mm;justify-content:center;` : `padding-right:${S}mm;justify-content:center;`;
    h += `<div style="position:absolute;${lado}top:${y}mm;width:${ancho + S}mm;height:${alto}mm;background:${bg};color:${col};display:flex;align-items:center;${rel}font-family:'Fraunces',serif;font-weight:600;font-size:20pt;">${i}</div>`;
  }
  return h;
}

// ---------------------------------------------------------------- avance de las 8 sesiones (puntitos)
export function avance(actual, color = C.rosa) {
  let p = "";
  for (let i = 1; i <= 8; i++) {
    const lleno = i <= actual;
    p += `<circle cx="${(i - 1) * 9 + 4}" cy="4" r="3.2" fill="${lleno ? color : "none"}" stroke="${color}" stroke-width="1"/>`;
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 72 8" width="36mm" height="4mm">${p}</svg>`;
}

// ---------------------------------------------------------------- reloj de 45 minutos (anillo por momentos)
export function anilloMomentos(momentos, { radio = 52, grosor = 20 } = {}) {
  const total = momentos.reduce((s, m) => s + m.min, 0);
  const tonos = [C.rosa, C.cacao, C.rosa, C.cacao, C.rosa, C.cacao];
  let ang = -90, h = "";
  const R = radio, r = radio - grosor;
  const pt = (rad, a) => [rad * Math.cos((a * Math.PI) / 180), rad * Math.sin((a * Math.PI) / 180)];
  momentos.forEach((m, i) => {
    const barrido = (m.min / total) * 360, fin = ang + barrido, grande = barrido > 180 ? 1 : 0;
    const sep = 1.2;
    const [x1, y1] = pt(R, ang + sep), [x2, y2] = pt(R, fin - sep), [x3, y3] = pt(r, fin - sep), [x4, y4] = pt(r, ang + sep);
    h += `<path d="M${x1} ${y1} A${R} ${R} 0 ${grande} 1 ${x2} ${y2} L${x3} ${y3} A${r} ${r} 0 ${grande} 0 ${x4} ${y4} Z" fill="${i % 2 ? C.cacao : C.rosa}"/>`;
    ang = fin;
  });
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-60 -60 120 120">${h}</svg>`;
}
