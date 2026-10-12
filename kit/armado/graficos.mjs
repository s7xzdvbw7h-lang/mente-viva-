// Gráficos hechos por código. Solo decoración original: un loto fino y cuatro íconos.
// (Los mandalas para pintar son los del libro terminado de Dani: no se generan acá.)

const PT = 25.4 / 72;

function petalo(rIn, rOut, ancho) {
  const h = rOut - rIn;
  const y1 = -(rIn + h * 0.25);
  const y2 = -(rOut - h * 0.3);
  return (
    `M0 ${-rIn} C ${-ancho} ${y1}, ${-ancho} ${y2}, 0 ${-rOut} ` +
    `C ${ancho} ${y2}, ${ancho} ${y1}, 0 ${-rIn} Z`
  );
}

// Loto fino para portada, contratapa y dorso de tarjetas. No es para pintar.
export function lotoDecorativo(color, trazoPt = 1, lado = 200) {
  const anillos = [
    { n: 12, rIn: 52, rOut: 94 },
    { n: 12, rIn: 34, rOut: 72 },
    { n: 8, rIn: 16, rOut: 50 },
  ];
  let cuerpo = "";
  anillos.forEach((a, idx) => {
    const rW = a.rIn + 0.55 * (a.rOut - a.rIn);
    const ancho = (0.46 * ((2 * Math.PI * rW) / a.n)) / 0.75;
    const giro = (idx % 2) * (180 / a.n);
    const d = petalo(a.rIn, a.rOut, ancho);
    for (let i = 0; i < a.n; i++) cuerpo += `<path d="${d}" transform="rotate(${(giro + (360 / a.n) * i).toFixed(3)})"/>`;
  });
  cuerpo += `<circle r="10"/>`;
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" viewBox="${-lado / 2} ${-lado / 2} ${lado} ${lado}" ` +
    `fill="none" stroke="${color}" stroke-width="${(trazoPt * PT * (200 / lado)).toFixed(3)}" stroke-linejoin="round" stroke-linecap="round">${cuerpo}</svg>`
  );
}

// Íconos de 24 × 24, línea rosa.
const ico = (cuerpo, color) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">${cuerpo}</svg>`;

export const ICONOS = {
  caminar: (c) =>
    ico(
      `<circle cx="13" cy="4.5" r="2"/><path d="M13 7.5 11 13l3 2.5 1 5.5M11 13l-3 7M12 9l-3.5 2L7 14M12.5 9.2l3 1.8 2.2-.8"/>`,
      c,
    ),
  charla: (c) =>
    ico(`<path d="M4 5h16v11H11l-4.5 3.5V16H4z"/><path d="M8 9.5h8M8 12.5h5"/>`, c),
  respirar: (c) =>
    ico(`<path d="M3 9h10a2.5 2.5 0 1 0-2.5-2.5M3 13h14a2.5 2.5 0 1 1-2.5 2.5M3 17h7a2 2 0 1 1-2 2"/>`, c),
  taza: (c) =>
    ico(`<path d="M5 10h12v4.5A4.5 4.5 0 0 1 12.5 19h-3A4.5 4.5 0 0 1 5 14.5z"/><path d="M17 11h1.5a2.5 2.5 0 0 1 0 5H16.5M8 3.5c-1 1 1 2-.2 3M12 3.5c-1 1 1 2-.2 3"/>`, c),
  celular: (c) =>
    ico(`<rect x="7" y="2.5" width="10" height="19" rx="2"/><path d="M11 18.5h2"/>`, c),
};
