// Guía para la hija: A5 vertical, 12 páginas. Cómo acompañar sin corregir ni examinar.
import { SANGRADO as S, ROSA, esc } from "./base.mjs";
import { encuentros, MOMENTOS, AVISO, FIRMA, MARCA } from "../contenido/encuentros.mjs";
import { CUADERNO, GUIA_HIJA as G } from "../contenido/generales.mjs";
import { lotoDecorativo } from "./graficos.mjs";

const A5 = { W: 148 + 2 * S, H: 210 + 2 * S };
const ZONA = `left:${S + 14}mm;top:${S + 13}mm;right:${S + 14}mm;bottom:${S + 17}mm;`;

const CSS = `
.zona.g h1{font-size:28pt;line-height:1.08;margin:1mm 0 4mm;}
.zona.g p{margin-bottom:3mm;}
.col{border:.4mm solid var(--rosa);border-radius:3mm;padding:3.5mm 5mm;margin-bottom:4mm;}
.col h3{font-size:20pt;color:var(--rosa);margin-bottom:1.5mm;}
.col ul.pts li{margin-bottom:1.2mm;}
.cs{border-bottom:.3mm solid var(--rosa);padding:2.4mm 0;}
.cs b{color:var(--rosa);}
.fila{padding:2mm 0 2.4mm;border-bottom:.3mm solid var(--rosa);}
.fila h3{font-size:19pt;line-height:1.1;margin-bottom:.8mm;}
.fila ul.pts li{margin-bottom:.4mm;}
.it2{margin-bottom:4mm;}
.it2 b{display:block;font-family:'Fraunces',serif;font-weight:600;font-size:20pt;color:var(--rosa);line-height:1.15;margin-bottom:.5mm;}
`;

const folio = (n) =>
  `<div class="folio" style="left:${S + 14}mm;right:${S + 14}mm;bottom:${S + 7}mm;"><span>Guía para vos</span><span>${n}</span></div>`;
const pg = (cuerpo, n) => `<section class="pagina"><div class="zona g" style="${ZONA}">${cuerpo}</div>${folio(n)}</section>`;
const li = (a) => a.map((x) => `<li>${esc(x)}</li>`).join("");

export function armarGuia() {
  const out = [];
  let n = 1;

  // 1. Portada
  out.push(`<section class="pagina"><div class="zona" style="left:${S + 12}mm;right:${S + 12}mm;top:${S + 18}mm;bottom:${S + 12}mm;text-align:center;">
<div class="kick">${esc(G.portada.tipo)}</div>
<h1 style="font-size:46pt;line-height:1.02;margin-top:8mm">${esc(G.portada.titulo)}</h1>
<p class="fr it" style="font-weight:400;font-size:22pt;color:var(--rosa);margin:5mm auto 0;max-width:110mm;line-height:1.2">${esc(G.portada.bajada)}</p>
<div style="width:70mm;height:70mm;margin:9mm auto 0">${lotoDecorativo(ROSA, 1, 200)}</div>
<p style="margin:7mm auto 0;max-width:110mm;font-size:18pt;line-height:1.3">${esc(G.portada.frase)}</p>
<div style="position:absolute;left:0;right:0;bottom:0"><div class="fr" style="font-size:20pt">${esc(FIRMA)}</div><div class="kick" style="margin-top:1mm;font-size:16pt">${esc(MARCA)}</div></div>
</div></section>`);

  // 2. Tu lugar
  n = 2;
  out.push(pg(`<div class="kick">${esc(G.lugar.kick)}</div><h1>${esc(G.lugar.titulo)}</h1>${G.lugar.parrafos.map((p) => `<p>${esc(p)}</p>`).join("")}`, n));

  // 3. Sí y no
  n = 3;
  out.push(pg(`<div class="kick">${esc(G.siNo.kick)}</div><h1>${esc(G.siNo.titulo)}</h1>
<div class="col"><h3>${esc(G.siNo.siTitulo)}</h3><ul class="pts">${li(G.siNo.si)}</ul></div>
<div class="col"><h3>${esc(G.siNo.noTitulo)}</h3><ul class="pts">${li(G.siNo.no)}</ul></div>`, n));

  // 4. Frases
  n = 4;
  out.push(pg(`<div class="kick">${esc(G.frases.kick)}</div><h1>${esc(G.frases.titulo)}</h1>
<div class="col"><h3>${esc(G.frases.ayudanTitulo)}</h3><ul class="pts">${li(G.frases.ayudan)}</ul></div>
<div class="col"><h3>${esc(G.frases.cambiarTitulo)}</h3><ul class="pts">${li(G.frases.cambiar)}</ul></div>`, n));

  // 5. Si se traba
  n = 5;
  out.push(pg(`<div class="kick">${esc(G.siPasa.kick)}</div><h1 style="font-size:24pt">${esc(G.siPasa.titulo)}</h1>
${G.siPasa.casos.map((c) => `<div class="cs"><b>${esc(c.cuando)}.</b> ${esc(c.que)}</div>`).join("")}`, n));

  // 6. Los seis momentos
  n = 6;
  out.push(pg(`<div class="kick">${esc(G.encuentro.kick)}</div><h1>${esc(G.encuentro.titulo)}</h1><p>${esc(G.encuentro.bajada)}</p>
${MOMENTOS.map((m, i) => `<div style="display:flex;gap:4mm;margin-bottom:1.6mm"><div class="circ">${m.n}</div><div style="flex:1"><b>${esc(m.nombre)}</b> <span class="rosa" style="font-weight:700">${m.min} min</span><div style="line-height:1.25">${esc(CUADERNO.encuentro.momentos[i])}</div></div></div>`).join("")}
<p class="guion" style="margin-top:2mm;margin-bottom:0">${esc(G.encuentro.consejo)}</p>`, n));

  // 7 y 8. Qué preparar (4 encuentros por página)
  for (let h = 0; h < 2; h++) {
    n += 1;
    const grupo = encuentros.slice(h * 4, h * 4 + 4);
    out.push(pg(`<div class="kick">${esc(G.preparar.kick)}</div><h1 style="font-size:24pt;margin-bottom:2mm">${esc(G.preparar.titulo)}${h ? " (2)" : ""}</h1>
${grupo.map((e) => `<div class="fila"><h3>${e.n}. ${esc(e.tema)}</h3><ul class="pts">${li(e.antes.slice(0, 2))}</ul></div>`).join("")}`, n));
  }

  // 9. Ritmo
  n += 1;
  out.push(pg(`<div class="kick">${esc(G.ritmo.kick)}</div><h1 style="font-size:25pt">${esc(G.ritmo.titulo)}</h1>
${G.ritmo.items.map((i) => `<div class="it2"><b>${esc(i.que)}</b><div>${esc(i.texto)}</div></div>`).join("")}
<div class="col" style="margin-top:3mm"><p style="margin:0">${esc(G.ritmo.nota)}</p></div>`, n));

  // 10. Turnos de vista y oído
  n += 1;
  out.push(pg(`<div class="kick">${esc(G.controles.kick)}</div><h1 style="font-size:25pt;margin-bottom:2mm">${esc(G.controles.titulo)}</h1>
<p style="margin-bottom:2mm">${esc(G.controles.texto)}</p>
<h3 class="fr rosa" style="font-size:19pt;margin-bottom:1mm">${esc(G.controles.comoTitulo)}</h3>
<ul class="pts">${li(G.controles.como)}</ul>
<p class="guion" style="margin-top:2mm">${esc(G.controles.cierre)}</p>`, n));

  // 11. Cuidate vos
  n += 1;
  out.push(pg(`<div class="kick">${esc(G.cuidate.kick)}</div><h1>${esc(G.cuidate.titulo)}</h1>${G.cuidate.parrafos.map((p) => `<p>${esc(p)}</p>`).join("")}
<div class="col" style="margin-top:4mm"><h3>${esc(G.cuidate.importante)}</h3><p style="margin:0">${esc(AVISO)}</p></div>`, n));

  // 12. Contratapa
  out.push(`<section class="pagina"><div class="zona" style="left:${S + 12}mm;right:${S + 12}mm;top:${S + 38}mm;bottom:${S + 14}mm;text-align:center;">
<div style="width:48mm;height:48mm;margin:0 auto">${lotoDecorativo(ROSA, 1, 200)}</div>
<p class="fr it" style="font-weight:400;font-size:22pt;color:var(--rosa);margin:9mm auto 0;max-width:110mm;line-height:1.25">${esc(G.contratapa)}</p>
<div style="position:absolute;left:0;right:0;bottom:0"><div class="fr" style="font-size:20pt">${esc(FIRMA)}</div><div class="kick" style="margin-top:1mm">${esc(MARCA)}</div></div>
</div></section>`);

  return { nombre: "guia-para-la-hija", titulo: "La hora del té · Guía para la hija", W: A5.W, H: A5.H, paginas: out, css: CSS, sangrado: S };
}
