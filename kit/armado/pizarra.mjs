// Pizarra de heladera: A4 vertical. "Hoy es…" y registro de la semana (encuentro · movimiento · app).
// Pensada para escribir encima con marcador: conviene imprimirla en material borrable o plastificarla.
import { SANGRADO as S, ROSA, esc } from "./base.mjs";
import { FIRMA, MARCA, PRODUCTO } from "../contenido/encuentros.mjs";
import { PIZARRA as P } from "../contenido/generales.mjs";
import { ICONOS } from "./graficos.mjs";

const CSS = `
.zona.p{left:${S + 14}mm;right:${S + 14}mm;top:${S + 12}mm;bottom:${S + 12}mm;}
.zona.p h1{font-size:46pt;line-height:1;margin:1mm 0 5mm;}
.campos{display:flex;gap:5mm;margin-bottom:9mm;}
.campo{flex:1;}
.campo .caja-e{height:38mm;border:.5mm solid var(--rosa);border-radius:4mm;}
.campo .et{margin-top:1.5mm;font-weight:700;font-size:16pt;color:var(--rosa);text-align:center;}
.campo.mes{flex:1.4;}
h2.sem{font-size:26pt;margin-bottom:3mm;}
.tabla{display:grid;grid-template-columns:50mm repeat(7,1fr);align-items:center;}
.tabla .d{text-align:center;font-weight:700;font-size:20pt;color:var(--rosa);padding-bottom:2mm;}
.tabla .e{height:28mm;display:flex;align-items:center;gap:3mm;border-top:.35mm solid var(--rosa);font-family:'Fraunces',serif;font-weight:600;font-size:17pt;line-height:1.05;}
.tabla .e svg{width:11mm;height:11mm;flex:none;}
.tabla .c{height:28mm;display:flex;align-items:center;justify-content:center;border-top:.35mm solid var(--rosa);}
.tabla .c i{display:block;width:14mm;height:14mm;border-radius:50%;border:.5mm solid var(--rosa);}
.pie-p{margin-top:6mm;}
.pie-p b{color:var(--rosa);}
.firma{position:absolute;left:0;right:0;bottom:0;display:flex;justify-content:space-between;align-items:flex-end;}
`;

export function armarPizarra() {
  const W = 210 + 2 * S, H = 297 + 2 * S;
  const iconos = { encuentro: ICONOS.taza(ROSA), movimiento: ICONOS.caminar(ROSA), app: ICONOS.celular(ROSA) };
  const pagina = `<section class="pagina"><div class="zona p">
<div class="kick">${esc(PRODUCTO)}</div>
<h1>${esc(P.titulo)}</h1>
<div class="campos">${P.campos.map((c, i) => `<div class="campo ${i === 2 ? "mes" : ""}"><div class="caja-e"></div><div class="et">${esc(c)}</div></div>`).join("")}</div>
<h2 class="sem">${esc(P.semana)}</h2>
<div class="tabla">
 <div></div>${P.dias.map((d) => `<div class="d">${d}</div>`).join("")}
 ${P.filas.map((f) => `<div class="e">${iconos[f.clave]}<span>${esc(f.nombre)}</span></div>${P.dias.map(() => `<div class="c"><i></i></div>`).join("")}`).join("")}
</div>
<div class="pie-p"><b>${esc(P.pie)}</b><div class="renglon"></div><div class="renglon"></div></div>
<div class="firma"><div class="fr" style="font-size:20pt">${esc(FIRMA)}</div><div class="kick">${esc(MARCA)}</div></div>
</div></section>`;
  return { nombre: "pizarra-de-heladera", titulo: "La hora del té · Pizarra de heladera", W, H, paginas: [pagina], css: CSS, sangrado: S };
}
