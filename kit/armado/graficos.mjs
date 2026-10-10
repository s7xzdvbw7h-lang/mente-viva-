// Gráficos hechos por código: lotos para pintar y figuras de la lámina de movimiento.

const PT = 25.4 / 72; // 1 punto en milímetros

// Un pétalo apuntando hacia arriba, desde el radio rIn hasta el radio rOut.
function petalo(rIn, rOut, ancho) {
  const h = rOut - rIn;
  const y1 = -(rIn + h * 0.25);
  const y2 = -(rOut - h * 0.3);
  return (
    `M0 ${-rIn} C ${-ancho} ${y1}, ${-ancho} ${y2}, 0 ${-rOut} ` +
    `C ${ancho} ${y2}, ${ancho} ${y1}, 0 ${-rIn} Z`
  );
}

// Loto por anillos, de afuera hacia adentro (los de adentro tapan la base de los de afuera).
// Cada pétalo es una zona para pintar; el centro cuenta como una más.
export function lotoSVG({
  anillos,
  centro = 12,
  trazoPt = 2,
  color = "#000",
  relleno = "#fff",
  lado = 200,
}) {
  const sw = (trazoPt * PT).toFixed(3);
  let cuerpo = "";
  anillos.forEach((a, idx) => {
    const rW = a.rIn + 0.55 * (a.rOut - a.rIn);
    const arco = (2 * Math.PI * rW) / a.n;
    const ancho = (0.46 * arco) / 0.75;
    const giro = a.giro ?? (idx % 2) * (180 / a.n);
    const d = petalo(a.rIn, a.rOut, ancho);
    for (let i = 0; i < a.n; i++) {
      const ang = giro + (360 / a.n) * i;
      cuerpo += `<path d="${d}" transform="rotate(${ang.toFixed(3)})"/>`;
    }
  });
  cuerpo += `<circle r="${centro}"/>`;
  const zonas = 1 + anillos.reduce((s, a) => s + a.n, 0);
  return {
    zonas,
    svg:
      `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${-lado / 2} ${-lado / 2} ${lado} ${lado}" ` +
      `fill="${relleno}" stroke="${color}" stroke-width="${sw}" stroke-linejoin="round" stroke-linecap="round">${cuerpo}</svg>`,
  };
}

// Los 4 lotos de cierre, de menos a más zonas para pintar.
export const LOTOS_SEMANA = [
  { semana: 1, centro: 16, anillos: [{ n: 12, rIn: 40, rOut: 92 }, { n: 8, rIn: 16, rOut: 66 }] },
  {
    semana: 2,
    centro: 14,
    anillos: [
      { n: 12, rIn: 56, rOut: 94 },
      { n: 12, rIn: 34, rOut: 74 },
      { n: 8, rIn: 16, rOut: 52 },
    ],
  },
  {
    semana: 3,
    centro: 12,
    anillos: [
      { n: 12, rIn: 64, rOut: 95 },
      { n: 12, rIn: 46, rOut: 80 },
      { n: 12, rIn: 30, rOut: 62 },
      { n: 8, rIn: 14, rOut: 44 },
    ],
  },
  {
    semana: 4,
    centro: 12,
    anillos: [
      { n: 16, rIn: 70, rOut: 96 },
      { n: 16, rIn: 52, rOut: 82 },
      { n: 12, rIn: 34, rOut: 64 },
      { n: 12, rIn: 16, rOut: 44 },
    ],
  },
];

// Loto fino para decorar portada y dorso de tarjetas (no es para pintar).
export function lotoDecorativo(color, trazoPt = 0.9, lado = 200) {
  return lotoSVG({
    anillos: [
      { n: 12, rIn: 52, rOut: 94 },
      { n: 12, rIn: 34, rOut: 72 },
      { n: 8, rIn: 16, rOut: 50 },
    ],
    centro: 10,
    trazoPt,
    color,
    relleno: "none",
    lado,
  }).svg;
}

// ---- Figuras de la lámina ---------------------------------------------------
// Vista 0 0 100 120. Línea cacao para la persona, rosa para silla y mesada.

const L = (pts) => `<polyline points="${pts.map((p) => p.join(",")).join(" ")}"/>`;

function persona(cuerpo, cabeza = [50, 17]) {
  return (
    `<g stroke="#4A3B33" stroke-width="3.4" fill="none" stroke-linecap="round" stroke-linejoin="round">` +
    `<circle cx="${cabeza[0]}" cy="${cabeza[1]}" r="8" fill="#F7F1E9"/>${cuerpo}</g>`
  );
}
const apoyo = (x1, y, x2) =>
  `<g stroke="#8E4E52" stroke-width="3.4" stroke-linecap="round" fill="none"><line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}"/><line x1="${x2}" y1="${y}" x2="${x2}" y2="116"/></g>`;
const piso = `<line x1="8" y1="114" x2="92" y2="114" stroke="#8E4E52" stroke-width="1.6" stroke-linecap="round"/>`;
const flecha = (x, y1, y2) =>
  `<g stroke="#8E4E52" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"><line x1="${x}" y1="${y1}" x2="${x}" y2="${y2}"/><polyline points="${x - 5},${y2 + 6} ${x},${y2} ${x + 5},${y2 + 6}"/></g>`;

export const FIGURAS = {
  marcha:
    persona(
      L([[50, 26], [50, 64]]) +
        L([[50, 32], [36, 46], [34, 60]]) +
        L([[50, 32], [64, 44], [66, 33]]) +
        L([[50, 64], [42, 88], [42, 112]]) +
        L([[50, 64], [60, 80], [60, 98]]),
    ) + piso,
  silla:
    `<g stroke="#8E4E52" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round" fill="none">` +
    `<polyline points="18,40 18,78 62,78"/><line x1="18" y1="78" x2="18" y2="114"/><line x1="62" y1="78" x2="62" y2="114"/></g>` +
    persona(
      L([[44, 42], [40, 72]]) +
        L([[44, 48], [58, 56], [66, 64]]) +
        L([[40, 72], [68, 72], [68, 112]]),
      [46, 31],
    ) +
    flecha(86, 100, 58) +
    piso,
  talones:
    apoyo(66, 64, 94) +
    persona(
      L([[44, 26], [44, 66]]) +
        L([[44, 32], [58, 48], [68, 62]]) +
        L([[44, 66], [44, 90], [44, 104], [54, 111]]),
      [44, 17],
    ) +
    flecha(22, 104, 72) +
    piso,
  linea:
    apoyo(66, 64, 94) +
    persona(
      L([[44, 26], [44, 66]]) +
        L([[44, 32], [58, 48], [68, 62]]) +
        L([[44, 66], [38, 90], [30, 111]]) +
        L([[44, 66], [50, 90], [54, 111]]),
      [44, 17],
    ) +
    `<line x1="20" y1="114" x2="64" y2="114" stroke="#8E4E52" stroke-width="3.4" stroke-linecap="round"/>`,
  rodilla:
    apoyo(66, 64, 94) +
    persona(
      L([[44, 26], [44, 66]]) +
        L([[44, 32], [58, 48], [68, 62]]) +
        L([[44, 66], [44, 90], [44, 112]]) +
        L([[44, 66], [64, 68], [64, 92]]),
      [44, 17],
    ) +
    piso,
  brazos:
    persona(
      L([[50, 26], [50, 64]]) +
        L([[50, 32], [37, 18], [32, 4]]) +
        L([[50, 32], [63, 18], [68, 4]]) +
        L([[50, 64], [43, 88], [43, 112]]) +
        L([[50, 64], [57, 88], [57, 112]]),
      [50, 17],
    ) + piso,
};
