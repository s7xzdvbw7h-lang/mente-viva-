// Ilustraciones originales del mazo de tarjetas, dibujadas por código.
// Tres colores (marfil, cacao, rosa de las cenizas). Vista 0 0 100 100. Sin texto dentro del dibujo.
const C = "#4A3B33";
const R = "#8E4E52";
const M = "#F7F1E9";

const g = (cuerpo) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><g stroke="${C}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round" fill="none">${cuerpo}</g></svg>`;

function estrella(cx, cy, r1, r2, relleno) {
  const pts = [];
  for (let i = 0; i < 10; i++) {
    const r = i % 2 === 0 ? r1 : r2;
    const a = (Math.PI / 5) * i;
    pts.push(`${(cx + r * Math.sin(a)).toFixed(1)},${(cy - r * Math.cos(a)).toFixed(1)}`);
  }
  return `<polygon points="${pts.join(" ")}" fill="${relleno}"/>`;
}
const suelo = (y = 84, x1 = 8, x2 = 92) => `<line x1="${x1}" y1="${y}" x2="${x2}" y2="${y}"/>`;
const persona = (x, y, s = 1, cuerpoFill = R) =>
  `<g transform="translate(${x} ${y}) scale(${s})"><circle cx="0" cy="-17" r="4" fill="${M}"/><path d="M-5 -12 L5 -12 L7 4 L-7 4 Z" fill="${cuerpoFill}"/><line x1="-3" y1="4" x2="-3" y2="12"/><line x1="3" y1="4" x2="3" y2="12"/></g>`;

export const ILUS = {
  // ---------------------------------------------------------------- infancia
  trompo: g(
    `<path d="M50 20 C70 6 88 22 80 40 S92 68 84 82" stroke-dasharray="1 0"/>` +
      `<circle cx="50" cy="19" r="3.4" fill="${C}"/>` +
      `<path d="M50 24 L50 30"/>` +
      `<path d="M30 38 Q50 28 70 38 Q80 56 50 84 Q20 56 30 38 Z" fill="${R}"/>` +
      `<path d="M31 47 Q50 54 69 47"/><path d="M36 60 Q50 67 64 60"/>` +
      `<path d="M50 84 L50 92"/>`,
  ),
  figuritas: g(
    `<g transform="rotate(-16 36 60)"><rect x="20" y="26" width="32" height="46" rx="3" fill="${M}"/><rect x="25" y="31" width="22" height="26" rx="2"/><line x1="25" y1="63" x2="47" y2="63"/></g>` +
      `<g transform="rotate(14 66 58)"><rect x="50" y="24" width="32" height="46" rx="3" fill="${M}"/><rect x="55" y="29" width="22" height="26" rx="2"/><circle cx="66" cy="42" r="6" fill="${R}"/></g>` +
      `<rect x="35" y="22" width="32" height="48" rx="3" fill="${R}"/><rect x="40" y="27" width="22" height="28" rx="2" fill="${M}"/>${estrella(51, 41, 8, 3.4, R)}<line x1="40" y1="62" x2="62" y2="62" stroke="${M}"/>`,
  ),
  guardapolvo: g(
    `<path d="M38 18 L50 30 L62 18 L82 30 L74 46 L68 42 L68 86 L32 86 L32 42 L26 46 L18 30 Z" fill="${M}"/>` +
      `<path d="M38 18 L50 36 L62 18" fill="${R}"/>` +
      `<line x1="50" y1="36" x2="50" y2="86"/>` +
      `<circle cx="50" cy="48" r="2" fill="${C}"/><circle cx="50" cy="60" r="2" fill="${C}"/><circle cx="50" cy="72" r="2" fill="${C}"/>` +
      `<rect x="55" y="64" width="11" height="12" rx="1.5"/>`,
  ),
  pizarron: g(
    `<rect x="12" y="20" width="76" height="52" rx="3" fill="${R}"/>` +
      `<rect x="19" y="26" width="62" height="40" rx="1.5" fill="${C}"/>` +
      `<path d="M26 56 L33 33 L40 56 M29 48 L37 48" stroke="${M}"/>` +
      `<path d="M48 40 L72 40 M48 49 L66 49 M48 58 L72 58" stroke="${M}"/>` +
      `<line x1="12" y1="78" x2="88" y2="78"/>` +
      `<rect x="62" y="73" width="14" height="5" rx="1" fill="${M}"/><rect x="26" y="74" width="9" height="4" rx="1" fill="${M}"/>` +
      `<line x1="22" y1="72" x2="20" y2="88"/><line x1="78" y1="72" x2="80" y2="88"/>`,
  ),
  rayuela: g(
    `<rect x="40" y="76" width="20" height="14" fill="${M}"/>` +
      `<rect x="40" y="62" width="20" height="14" fill="${M}"/>` +
      `<rect x="30" y="48" width="20" height="14" fill="${M}"/><rect x="50" y="48" width="20" height="14" fill="${M}"/>` +
      `<rect x="40" y="34" width="20" height="14" fill="${M}"/>` +
      `<rect x="30" y="20" width="20" height="14" fill="${M}"/><rect x="50" y="20" width="20" height="14" fill="${M}"/>` +
      `<path d="M30 20 A20 11 0 0 1 70 20" fill="${R}"/>` +
      `<circle cx="50" cy="69" r="4.5" fill="${R}"/>` +
      `<path d="M14 84 L22 76 M86 84 L78 76" />`,
  ),
  soga: g(
    `<path d="M22 28 C10 96, 90 96, 78 28" stroke-width="3.2"/>` +
      `<rect x="14" y="14" width="12" height="22" rx="5" fill="${R}" transform="rotate(8 20 25)"/>` +
      `<rect x="74" y="14" width="12" height="22" rx="5" fill="${R}" transform="rotate(-8 80 25)"/>` +
      `<ellipse cx="50" cy="90" rx="26" ry="3.5"/>`,
  ),
  muneca: g(
    `<path d="M36 22 Q50 6 64 22" fill="${R}"/>` +
      `<path d="M36 22 Q30 36 34 50 M64 22 Q70 36 66 50" stroke-width="3"/>` +
      `<circle cx="50" cy="30" r="13" fill="${M}"/>` +
      `<circle cx="45" cy="29" r="1.6" fill="${C}"/><circle cx="55" cy="29" r="1.6" fill="${C}"/><path d="M46 36 Q50 39 54 36"/>` +
      `<path d="M38 46 L62 46 L72 84 L28 84 Z" fill="${R}"/>` +
      `<path d="M38 50 L20 62 M62 50 L80 62"/>` +
      `<rect x="44" y="64" width="12" height="10" fill="${M}"/><line x1="44" y1="69" x2="56" y2="69"/>` +
      `<line x1="40" y1="84" x2="40" y2="92"/><line x1="60" y1="84" x2="60" y2="92"/>`,
  ),
  pelota: g(
    `<ellipse cx="50" cy="90" rx="24" ry="3.5"/>` +
      `<circle cx="50" cy="52" r="32" fill="${R}"/>` +
      `<path d="M20 44 C36 32 64 32 80 44"/><path d="M20 60 C36 72 64 72 80 60"/>` +
      `<path d="M50 20 C40 38 40 66 50 84"/>` +
      `<path d="M30 36 Q34 31 40 30" stroke="${M}"/>`,
  ),
  barrilete: g(
    `<path d="M50 8 L74 36 L50 72 L26 36 Z" fill="${M}"/>` +
      `<path d="M50 8 L74 36 L50 36 Z" fill="${R}"/><path d="M26 36 L50 72 L50 36 Z" fill="${R}"/>` +
      `<line x1="50" y1="8" x2="50" y2="72"/><line x1="26" y1="36" x2="74" y2="36"/>` +
      `<path d="M50 72 C40 78 60 84 50 90 C44 94 54 96 50 98" />` +
      `<path d="M44 80 L50 76 L50 84 Z" fill="${R}"/><path d="M56 88 L50 84 L50 92 Z" fill="${M}"/>`,
  ),
  cartuchera: g(
    `<g transform="rotate(-14 38 46)"><rect x="34" y="16" width="9" height="30" fill="${M}"/><polygon points="34,16 43,16 38.5,6" fill="${C}"/></g>` +
      `<g transform="rotate(4 52 46)"><rect x="48" y="14" width="9" height="32" fill="${R}"/><polygon points="48,14 57,14 52.5,5" fill="${C}"/></g>` +
      `<g transform="rotate(18 66 46)"><rect x="62" y="18" width="9" height="28" fill="${M}"/><polygon points="62,18 71,18 66.5,9" fill="${C}"/></g>` +
      `<rect x="14" y="44" width="72" height="34" rx="9" fill="${R}"/>` +
      `<path d="M20 58 L80 58" stroke="${M}" stroke-dasharray="3 3"/>` +
      `<rect x="44" y="52" width="12" height="12" rx="3" fill="${M}"/>`,
  ),

  // ---------------------------------------------------------------- comidas
  mate: g(
    `<path d="M32 38 C24 58 34 86 50 86 C66 86 76 58 68 38 Z" fill="${R}"/>` +
      `<ellipse cx="50" cy="38" rx="18" ry="5.5" fill="${C}"/>` +
      `<path d="M33 58 Q50 66 67 58"/><path d="M37 70 Q50 76 63 70"/>` +
      `<line x1="56" y1="38" x2="76" y2="8" stroke-width="3"/><circle cx="76" cy="8" r="3" fill="${M}"/>` +
      `<line x1="42" y1="90" x2="58" y2="90"/>`,
  ),
  pan: g(
    `<path d="M14 60 C14 36 86 36 86 60 C86 74 70 78 50 78 C30 78 14 74 14 60 Z" fill="${R}"/>` +
      `<path d="M30 46 L40 62 M46 42 L56 60 M62 44 L72 60" stroke="${M}" stroke-width="3"/>` +
      `<path d="M32 22 C28 16 36 14 32 8 M48 22 C44 16 52 14 48 8 M64 22 C60 16 68 14 64 8" stroke-width="2"/>`,
  ),
  empanadas: g(
    `<ellipse cx="50" cy="86" rx="40" ry="6" fill="${M}"/>` +
      `<g transform="translate(14 -14)"><path d="M16 72 A32 32 0 0 1 80 72 Z" fill="${M}"/>` +
      `<path d="M24 72 A24 24 0 0 1 72 72" stroke="${R}" stroke-dasharray="3.2 3.2" stroke-width="2.6"/></g>` +
      `<path d="M10 80 A32 32 0 0 1 74 80 Z" fill="${R}"/>` +
      `<path d="M18 80 A24 24 0 0 1 66 80" stroke="${M}" stroke-dasharray="3.2 3.2" stroke-width="2.6"/>` +
      `<line x1="8" y1="80" x2="76" y2="80"/>`,
  ),
  milanesa: g(
    `<circle cx="50" cy="52" r="38" fill="${M}"/><circle cx="50" cy="52" r="29"/>` +
      `<path d="M26 44 C28 32 46 28 62 32 C76 36 80 50 72 60 C66 70 46 74 34 66 C26 62 24 52 26 44 Z" fill="${R}"/>` +
      `<circle cx="42" cy="44" r="1.3" fill="${M}" stroke="none"/><circle cx="56" cy="40" r="1.3" fill="${M}" stroke="none"/><circle cx="52" cy="54" r="1.3" fill="${M}" stroke="none"/><circle cx="64" cy="52" r="1.3" fill="${M}" stroke="none"/><circle cx="40" cy="58" r="1.3" fill="${M}" stroke="none"/>` +
      `<path d="M66 66 A12 12 0 0 1 86 62 Z" fill="${M}"/><line x1="76" y1="63" x2="73" y2="68"/>`,
  ),
  noquis: g(
    `<path d="M20 52 L80 52 C80 74 66 86 50 86 C34 86 20 74 20 52 Z" fill="${M}"/>` +
      `<ellipse cx="50" cy="52" rx="30" ry="6" fill="${R}"/>` +
      `<ellipse cx="38" cy="46" rx="9" ry="6" fill="${M}"/><ellipse cx="54" cy="42" rx="9" ry="6" fill="${M}"/><ellipse cx="66" cy="49" rx="8" ry="5.5" fill="${M}"/><ellipse cx="46" cy="52" rx="8" ry="5" fill="${M}"/>` +
      `<path d="M34 44 L42 48 M50 40 L58 44 M62 47 L70 51" stroke-width="1.6"/>` +
      `<path d="M36 28 C32 22 40 20 36 14 M50 26 C46 20 54 18 50 12 M64 28 C60 22 68 20 64 14" stroke-width="2"/>`,
  ),
  dulce: g(
    `<rect x="28" y="36" width="44" height="50" rx="7" fill="${R}"/>` +
      `<rect x="26" y="26" width="48" height="12" rx="3" fill="${C}"/>` +
      `<rect x="34" y="48" width="32" height="24" rx="2" fill="${M}"/>` +
      `<path d="M44 60 A6 6 0 1 1 56 60" stroke="${R}"/><line x1="50" y1="60" x2="50" y2="66" stroke="${R}"/>` +
      `<line x1="82" y1="20" x2="82" y2="62"/><ellipse cx="82" cy="66" rx="6" ry="8" fill="${R}"/>`,
  ),
  flan: g(
    `<ellipse cx="50" cy="72" rx="38" ry="8" fill="${M}"/>` +
      `<path d="M30 70 L35 42 Q50 32 65 42 L70 70 Z" fill="${R}"/>` +
      `<path d="M35 42 Q50 32 65 42 Q62 52 57 47 Q53 58 49 48 Q45 56 41 48 Q38 52 35 42 Z" fill="${C}"/>` +
      `<path d="M38 58 L62 58" stroke="${M}"/>`,
  ),
  tortas: g(
    `<ellipse cx="50" cy="82" rx="38" ry="6" fill="${M}"/>` +
      `<circle cx="38" cy="58" r="23" fill="${M}"/>` +
      `<circle cx="62" cy="50" r="23" fill="${R}"/>` +
      `<path d="M54 50 L70 50"/><path d="M30 58 L46 58"/>` +
      `<circle cx="56" cy="40" r="1.6" fill="${M}" stroke="none"/><circle cx="68" cy="42" r="1.6" fill="${M}" stroke="none"/><circle cx="72" cy="56" r="1.6" fill="${M}" stroke="none"/><circle cx="52" cy="60" r="1.6" fill="${M}" stroke="none"/><circle cx="64" cy="64" r="1.6" fill="${M}" stroke="none"/>`,
  ),

  // ---------------------------------------------------------------- lugares (escenas)
  plaza:
    g(
      suelo(82) +
        `<rect x="22" y="48" width="8" height="34" fill="${C}"/>` +
        `<circle cx="26" cy="38" r="16" fill="${R}"/><circle cx="14" cy="46" r="10" fill="${R}"/><circle cx="38" cy="46" r="10" fill="${R}"/>` +
        `<rect x="52" y="68" width="34" height="5" fill="${M}"/><rect x="52" y="58" width="34" height="4" fill="${M}"/>` +
        `<line x1="56" y1="73" x2="56" y2="82"/><line x1="82" y1="73" x2="82" y2="82"/><line x1="56" y1="62" x2="56" y2="68"/><line x1="82" y1="62" x2="82" y2="68"/>` +
        `<line x1="92" y1="82" x2="92" y2="28"/><circle cx="92" cy="24" r="5" fill="${M}"/>`,
    ).replace("</g></svg>", persona(42, 72, 0.9) + persona(70, 60, 0.8, M) + "</g></svg>"),
  almacen: g(
    `<rect x="14" y="34" width="72" height="48" fill="${M}"/>` +
      [0, 1, 2, 3, 4, 5].map((i) => `<path d="M${14 + i * 12} 24 L${26 + i * 12} 24 L${28 + i * 12} 36 L${12 + i * 12} 36 Z" fill="${i % 2 ? M : R}"/>`).join("") +
      `<rect x="56" y="46" width="22" height="36" fill="${R}"/><circle cx="73" cy="64" r="1.6" fill="${M}"/>` +
      `<rect x="22" y="46" width="26" height="22"/><line x1="22" y1="57" x2="48" y2="57"/>` +
      `<rect x="26" y="49" width="4" height="8" fill="${R}"/><rect x="33" y="49" width="4" height="8" fill="${R}"/><rect x="40" y="49" width="4" height="8" fill="${R}"/>` +
      `<rect x="26" y="60" width="18" height="6" fill="${M}"/>` +
      `<rect x="12" y="72" width="14" height="10" fill="${M}"/><line x1="12" y1="77" x2="26" y2="77"/>` +
      suelo(82, 6, 94),
  ),
  cocina: g(
    `<line x1="12" y1="26" x2="88" y2="26"/>` +
      `<line x1="26" y1="26" x2="26" y2="34"/><circle cx="26" cy="40" r="7" fill="${R}"/>` +
      `<line x1="50" y1="26" x2="50" y2="34"/><path d="M42 34 L58 34 L56 46 L44 46 Z" fill="${M}"/>` +
      `<line x1="76" y1="26" x2="76" y2="34"/><circle cx="76" cy="40" r="7" fill="${M}"/>` +
      `<rect x="16" y="58" width="68" height="28" fill="${M}"/>` +
      `<rect x="22" y="68" width="30" height="14"/><circle cx="64" cy="64" r="2.2" fill="${C}"/><circle cx="74" cy="64" r="2.2" fill="${C}"/><circle cx="64" cy="76" r="2.2" fill="${C}"/><circle cx="74" cy="76" r="2.2" fill="${C}"/>` +
      `<path d="M28 58 L28 52 C28 44 48 44 48 52 L48 58 Z" fill="${R}"/><path d="M48 50 L58 44" /><path d="M28 50 C20 40 36 38 40 44" />` +
      `<path d="M34 40 C31 36 37 34 34 30" stroke-width="1.8"/>`,
  ),
  estacion: g(
    `<path d="M8 74 L92 74"/>` +
      `<rect x="10" y="40" width="58" height="30" rx="4" fill="${R}"/>` +
      `<rect x="16" y="46" width="12" height="12" fill="${M}"/><rect x="32" y="46" width="12" height="12" fill="${M}"/><rect x="48" y="46" width="12" height="12" fill="${M}"/>` +
      `<line x1="10" y1="62" x2="68" y2="62"/>` +
      `<circle cx="22" cy="74" r="5" fill="${M}"/><circle cx="40" cy="74" r="5" fill="${M}"/><circle cx="58" cy="74" r="5" fill="${M}"/>` +
      `<path d="M26 40 L26 32 L40 32 L40 40"/>` +
      `<line x1="82" y1="82" x2="82" y2="34"/><circle cx="82" cy="26" r="9" fill="${M}"/><path d="M82 26 L82 20 M82 26 L87 28"/>` +
      `<path d="M8 82 L92 82"/>`,
  ),
  escuela: g(
    `<rect x="20" y="46" width="60" height="38" fill="${M}"/>` +
      `<path d="M16 46 L50 26 L84 46 Z" fill="${R}"/>` +
      `<path d="M44 26 L44 18 M56 26 L56 18"/><path d="M44 18 C44 10 56 10 56 18 Z" fill="${M}"/>` +
      `<path d="M42 84 L42 66 A8 8 0 0 1 58 66 L58 84 Z" fill="${R}"/>` +
      `<rect x="25" y="54" width="12" height="14"/><rect x="63" y="54" width="12" height="14"/>` +
      `<line x1="31" y1="54" x2="31" y2="68"/><line x1="69" y1="54" x2="69" y2="68"/>` +
      `<line x1="10" y1="84" x2="90" y2="84"/><line x1="88" y1="84" x2="88" y2="44"/><path d="M88 44 L98 48 L88 52 Z" fill="${R}"/>`,
  ),
  patio: g(
    `<line x1="14" y1="20" x2="14" y2="76"/><line x1="86" y1="20" x2="86" y2="76"/>` +
      `<path d="M14 26 Q50 40 86 26"/>` +
      `<path d="M26 31 L26 46 L40 46 L40 34 Z" fill="${M}"/><path d="M50 34 L50 50 L62 50 L62 33 Z" fill="${R}"/><path d="M70 31 L70 44 L80 44 L80 30 Z" fill="${M}"/>` +
      `<path d="M20 86 L24 70 L40 70 L44 86 Z" fill="${R}"/><path d="M32 70 C26 60 22 56 24 50 M32 70 C34 60 38 54 42 52 M32 70 L32 54" />` +
      `<path d="M62 86 L66 72 L80 72 L84 86 Z" fill="${M}"/><path d="M73 72 C70 64 66 60 66 56 M73 72 C76 64 80 60 82 58 M73 72 L73 58"/>` +
      `<path d="M8 86 L92 86"/><path d="M8 92 L92 92"/>`,
  ),
  kiosco: g(
    `<rect x="22" y="38" width="56" height="46" fill="${M}"/>` +
      [0, 1, 2, 3, 4].map((i) => `<path d="M${18 + i * 13} 26 L${31 + i * 13} 26 L${33 + i * 13} 40 L${16 + i * 13} 40 Z" fill="${i % 2 ? M : R}"/>`).join("") +
      `<rect x="28" y="48" width="44" height="22" fill="${R}"/>` +
      `<rect x="32" y="52" width="8" height="12" fill="${M}"/><rect x="43" y="52" width="8" height="12" fill="${M}"/><rect x="54" y="52" width="8" height="12" fill="${M}"/>` +
      `<line x1="26" y1="72" x2="74" y2="72" stroke-width="3.4"/>` +
      `<circle cx="34" cy="68" r="2.4" fill="${M}"/><circle cx="42" cy="68" r="2.4" fill="${M}"/><circle cx="50" cy="68" r="2.4" fill="${M}"/>` +
      `<line x1="12" y1="84" x2="88" y2="84"/><line x1="86" y1="84" x2="86" y2="46"/><circle cx="86" cy="42" r="5" fill="${R}"/>`,
  ),
  cine: g(
    `<rect x="14" y="40" width="72" height="44" fill="${M}"/>` +
      `<rect x="10" y="28" width="80" height="14" fill="${R}"/>` +
      [0, 1, 2, 3, 4, 5, 6, 7].map((i) => `<circle cx="${17 + i * 9.4}" cy="35" r="2" fill="${M}" stroke="none"/>`).join("") +
      `<circle cx="50" cy="14" r="9" fill="${M}"/><circle cx="46" cy="12" r="2"/><circle cx="54" cy="12" r="2"/><circle cx="46" cy="17" r="2"/><circle cx="54" cy="17" r="2"/>` +
      `<rect x="20" y="48" width="18" height="24" fill="${R}"/>${estrella(29, 59, 5, 2, M)}` +
      `<rect x="62" y="48" width="18" height="24" fill="${R}"/><circle cx="71" cy="57" r="4" fill="${M}"/><path d="M65 68 Q71 60 77 68" stroke="${M}"/>` +
      `<rect x="42" y="60" width="16" height="24" fill="${C}"/><line x1="50" y1="60" x2="50" y2="84"/>` +
      `<line x1="8" y1="84" x2="92" y2="84"/>`,
  ),

  // ---------------------------------------------------------------- épocas
  radio: g(
    `<rect x="14" y="30" width="72" height="50" rx="7" fill="${R}"/>` +
      `<circle cx="34" cy="55" r="15" fill="${M}"/><circle cx="34" cy="55" r="10"/><circle cx="34" cy="55" r="5"/>` +
      `<path d="M58 44 A14 14 0 0 1 82 44" fill="${M}"/><line x1="58" y1="44" x2="82" y2="44"/><path d="M62 44 L63 41 M70 44 L70 40 M78 44 L77 41" stroke-width="1.6"/>` +
      `<circle cx="64" cy="64" r="5" fill="${M}"/><circle cx="78" cy="64" r="5" fill="${M}"/>` +
      `<line x1="24" y1="80" x2="24" y2="88"/><line x1="76" y1="80" x2="76" y2="88"/>` +
      `<path d="M30 30 L24 14 M70 30 L78 12"/>`,
  ),
  telefono: g(
    `<path d="M16 30 C16 22 30 20 50 20 C70 20 84 22 84 30 C84 34 80 36 76 36 L24 36 C20 36 16 34 16 30 Z" fill="${R}"/>` +
      `<path d="M14 38 L86 38 L80 78 C79 84 74 86 70 86 L30 86 C26 86 21 84 20 78 Z" fill="${M}"/>` +
      `<circle cx="50" cy="62" r="19" fill="${R}"/><circle cx="50" cy="62" r="5" fill="${M}"/>` +
      [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => { const a = (-60 + i * 30) * Math.PI / 180; return `<circle cx="${(50 + 13 * Math.cos(a)).toFixed(1)}" cy="${(62 + 13 * Math.sin(a)).toFixed(1)}" r="2.8" fill="${M}"/>`; }).join(""),
  ),
  tocadiscos: g(
    `<rect x="12" y="50" width="76" height="34" rx="4" fill="${R}"/>` +
      `<ellipse cx="44" cy="52" rx="30" ry="12" fill="${C}"/>` +
      `<ellipse cx="44" cy="52" rx="22" ry="8.5" stroke="${M}" stroke-width="1.2"/><ellipse cx="44" cy="52" rx="14" ry="5.2" stroke="${M}" stroke-width="1.2"/>` +
      `<ellipse cx="44" cy="52" rx="7" ry="2.8" fill="${M}"/>` +
      `<circle cx="80" cy="42" r="4" fill="${M}"/><path d="M80 42 L64 24 L58 34" stroke-width="3"/>` +
      `<circle cx="22" cy="74" r="2.4" fill="${M}"/><circle cx="82" cy="74" r="2.4" fill="${M}"/>`,
  ),
  casetera: g(
    `<rect x="12" y="30" width="76" height="52" rx="5" fill="${M}"/>` +
      `<rect x="20" y="36" width="60" height="22" rx="2" fill="${R}"/>` +
      `<circle cx="36" cy="47" r="7" fill="${M}"/><circle cx="64" cy="47" r="7" fill="${M}"/>` +
      `<circle cx="36" cy="47" r="2" fill="${C}"/><circle cx="64" cy="47" r="2" fill="${C}"/><line x1="43" y1="47" x2="57" y2="47"/>` +
      `<path d="M30 82 L36 66 L64 66 L70 82" fill="${M}"/>` +
      `<circle cx="42" cy="73" r="1.8" fill="${C}"/><circle cx="50" cy="73" r="1.8" fill="${C}"/><circle cx="58" cy="73" r="1.8" fill="${C}"/>` +
      `<circle cx="17" cy="35" r="1.6" fill="${C}"/><circle cx="83" cy="35" r="1.6" fill="${C}"/>`,
  ),
  computadora: g(
    `<rect x="20" y="14" width="60" height="48" rx="6" fill="${M}"/>` +
      `<rect x="27" y="21" width="46" height="34" rx="2" fill="${C}"/>` +
      `<path d="M33 30 L43 30 M33 37 L53 37" stroke="${M}"/><line x1="33" y1="44" x2="38" y2="44" stroke="${M}" stroke-width="3"/>` +
      `<circle cx="70" cy="58" r="1.6" fill="${R}" stroke="none"/>` +
      `<path d="M38 62 L36 70 L64 70 L62 62" fill="${M}"/>` +
      `<rect x="16" y="74" width="68" height="14" rx="3" fill="${R}"/>` +
      `<path d="M22 79 L78 79 M22 84 L78 84" stroke="${M}" stroke-dasharray="4 3" stroke-width="2"/>`,
  ),
  celular: g(
    `<rect x="32" y="8" width="36" height="84" rx="8" fill="${C}"/>` +
      `<rect x="36" y="18" width="28" height="60" rx="2" fill="${M}"/>` +
      `<rect x="40" y="24" width="9" height="9" rx="2" fill="${R}"/><rect x="51" y="24" width="9" height="9" rx="2" fill="${R}"/>` +
      `<rect x="40" y="36" width="9" height="9" rx="2" fill="${R}"/><rect x="51" y="36" width="9" height="9" rx="2" fill="${R}"/>` +
      `<rect x="40" y="48" width="20" height="4" rx="2"/><rect x="40" y="56" width="14" height="4" rx="2"/>` +
      `<circle cx="50" cy="85" r="3" stroke="${M}"/><line x1="46" y1="13" x2="54" y2="13" stroke="${M}"/>`,
  ),
};
