// Mazo de 40 tarjetas de 9 × 13 cm, ilustradas. Hojas A4 con 4 tarjetas, marcas de corte y 3 mm de sangrado.
// El PDF alterna frente y dorso: se imprime a doble faz, girando por el borde largo.
import { SANGRADO as S, ROSA, esc } from "./base.mjs";
import { MAZO } from "../contenido/tarjetas.mjs";
import { TARJETAS_TEXTOS as T } from "../contenido/generales.mjs";
import { ILUS } from "./ilustraciones.mjs";
import { lotoDecorativo } from "./graficos.mjs";

export const W = 210, H = 297;
const CW = 90, CH = 130, GAP = 6;
const X0 = (W - (2 * CW + GAP)) / 2;
const Y0 = (H - (2 * CH + GAP)) / 2;

export const CSS_TARJETAS = `
.pagina{background:#fff;}
.tj{position:absolute;width:${CW + 2 * S}mm;height:${CH + 2 * S}mm;background:var(--marfil);}
.tj .m{position:absolute;left:${S + 5}mm;top:${S + 5}mm;right:${S + 5}mm;bottom:${S + 5}mm;border:.45mm solid var(--rosa);border-radius:3.5mm;padding:4mm 5mm 4mm;display:flex;flex-direction:column;align-items:center;text-align:center;overflow:hidden;}
.tj .gr{font-size:16pt;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--rosa);}
.tj .il{width:70mm;height:70mm;margin-top:5mm;flex:none;}
.tj .il svg{width:100%;height:100%;display:block;}
.tj .nom{font-family:"Fraunces",serif;font-weight:600;font-size:26pt;line-height:1.1;margin-top:5mm;}
.tj .det{font-family:'Fraunces',serif;font-style:italic;font-weight:400;font-size:19pt;color:var(--rosa);margin-top:1.5mm;}
.tj .preg{font-family:'Fraunces',serif;font-weight:600;font-size:25pt;line-height:1.2;flex:1;display:flex;align-items:center;}
.tj .pie{font-size:16pt;font-weight:600;color:var(--rosa);margin-top:auto;}
.tj.dorso .m{justify-content:center;}
`;

export function marcas() {
  const xs = [X0, X0 + CW, X0 + CW + GAP, X0 + 2 * CW + GAP];
  const ys = [Y0, Y0 + CH, Y0 + CH + GAP, Y0 + 2 * CH + GAP];
  let m = "";
  for (const x of xs) m += `<line x1="${x}" y1="${Y0 - 10}" x2="${x}" y2="${Y0 - 4.5}"/><line x1="${x}" y1="${Y0 + 2 * CH + GAP + 4.5}" x2="${x}" y2="${Y0 + 2 * CH + GAP + 10}"/>`;
  for (const y of ys) m += `<line x1="${X0 - 10}" y1="${y}" x2="${X0 - 4.5}" y2="${y}"/><line x1="${X0 + 2 * CW + GAP + 4.5}" y1="${y}" x2="${X0 + 2 * CW + GAP + 10}" y2="${y}"/>`;
  return `<svg style="position:absolute;left:0;top:0" width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}" stroke="#4A3B33" stroke-width=".2">${m}</svg>`;
}
export const pos = (i) => `left:${X0 + (i % 2) * (CW + GAP) - S}mm;top:${Y0 + Math.floor(i / 2) * (CH + GAP) - S}mm;`;

function frente(c, i) {
  const estilo = `style="${pos(i)}"`;
  if (c.pregunta) {
    return `<div class="tj" ${estilo}><div class="m chequear"><div class="gr">Pregunta</div><div style="width:26mm;height:26mm;margin-top:3mm;flex:none">${lotoDecorativo(ROSA, 1.1, 200)}</div><div class="preg">${esc(c.pregunta)}</div><div class="pie">La hora del té</div></div></div>`;
  }
  return `<div class="tj" ${estilo}><div class="m chequear"><div class="gr">${esc(c.grupo)}</div><div class="il">${ILUS[c.ilus]}</div><div class="nom">${esc(c.nombre)}</div>${c.detalle ? `<div class="det">${esc(c.detalle)}</div>` : ""}</div></div>`;
}
const dorso = (i) =>
  `<div class="tj dorso" style="${pos(i)}"><div class="m chequear"><div style="width:50mm;height:50mm;flex:none">${lotoDecorativo(ROSA, 1.1, 200)}</div><div class="fr" style="font-size:28pt;margin-top:5mm">${esc(T.dorsoTitulo)}</div><div class="pie" style="margin-top:3mm">${esc(T.dorsoBajada)}</div></div></div>`;

export function armarTarjetas() {
  const paginas = [];
  for (let h = 0; h < MAZO.length; h += 4) {
    const grupo = MAZO.slice(h, h + 4);
    paginas.push(`<section class="pagina">${grupo.map((c, i) => frente(c, i)).join("")}${marcas()}</section>`);
    paginas.push(`<section class="pagina">${Array.from({ length: grupo.length }, (_, i) => dorso(i)).join("")}${marcas()}</section>`);
  }
  return { nombre: "mazo-40-tarjetas", titulo: "La hora del té · Mazo de 40 tarjetas", W, H, paginas, css: CSS_TARJETAS, sangrado: 0 };
}
