// Arma los PDF del kit "Mente Viva · NeuroGym" desde los textos de kit/contenido.
// Uso:  node kit/armado/construir.mjs            (arma todo)
//       node kit/armado/construir.mjs cuaderno   (arma una pieza)
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { encuentros, SEMANAS, TARJETAS, MOVIMIENTO, AVISO, FIRMA, MARCA, LEMA } from "../contenido/encuentros.mjs";
import { CUADERNO, GUIA_HIJA, PIZARRA, LAMINA, TARJETAS_TEXTOS, MANDALAS } from "../contenido/generales.mjs";
import { lotoSVG, lotoDecorativo, LOTOS_SEMANA, FIGURAS } from "./graficos.mjs";

const require = createRequire("/opt/node-tools/");
const { chromium } = require("playwright");

const AQUI = path.dirname(fileURLToPath(import.meta.url));
const RAIZ = path.resolve(AQUI, "..");
const HTML_DIR = path.join(AQUI, "_html");
const PDF_DIR = path.join(RAIZ, "pdf");
const PREV_DIR = path.join(RAIZ, "vista-previa");
for (const d of [HTML_DIR, PDF_DIR, PREV_DIR]) fs.mkdirSync(d, { recursive: true });

const SANGRADO = 3; // mm por lado
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// Marca (Luz plena v3): máximo 3 colores y 2 tipografías por pieza.
const MARFIL = "#F7F1E9";
const CACAO = "#4A3B33";
const ROSA = "#8E4E52";

const FUENTES_CSS = [
  ["Fraunces", "normal", 400, "Fraunces-400.ttf"],
  ["Fraunces", "normal", 600, "Fraunces-600.ttf"],
  ["Fraunces", "italic", 400, "Fraunces-400-italic.ttf"],
  ["Manrope", "normal", 400, "Manrope-400.ttf"],
  ["Manrope", "normal", 600, "Manrope-600.ttf"],
  ["Manrope", "normal", 700, "Manrope-700.ttf"],
]
  .map(
    ([f, st, w, file]) =>
      `@font-face{font-family:'${f}';font-style:${st};font-weight:${w};src:url('../../fuentes/${file}') format('truetype');}`,
  )
  .join("\n");

const CSS_BASE = `
${FUENTES_CSS}
:root{--marfil:${MARFIL};--cacao:${CACAO};--rosa:${ROSA};}
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{font-family:'Manrope',sans-serif;color:var(--cacao);font-size:15pt;line-height:1.38;}
h1,h2,h3,.fr{font-family:'Fraunces',serif;font-weight:600;}
.pagina{width:var(--W);height:var(--H);position:relative;overflow:hidden;background:var(--marfil);break-after:page;page-break-after:always;}
.pagina:last-child{break-after:auto;page-break-after:auto;}
.zona{position:absolute;overflow:hidden;}
.kick{font-size:12pt;font-weight:700;letter-spacing:.14em;color:var(--rosa);text-transform:uppercase;}
.min{font-family:'Manrope',sans-serif;font-weight:700;font-size:12pt;color:var(--rosa);letter-spacing:.04em;margin-left:3mm;white-space:nowrap;}
.rosa{color:var(--rosa);}
ul.pts{list-style:none;}
ul.pts li{position:relative;padding-left:6mm;margin-bottom:1.6mm;}
ul.pts li::before{content:"";position:absolute;left:0;top:2.6mm;width:2.2mm;height:2.2mm;border-radius:50%;background:var(--rosa);}
.renglones{background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 8.65mm,var(--rosa) 8.65mm,var(--rosa) 9mm);}
.folio{position:absolute;display:flex;justify-content:space-between;font-size:11pt;color:var(--rosa);}
.folio b{font-weight:700;}
`;

function documento(titulo, W, H, paginas, extra = "") {
  return `<!doctype html><html lang="es"><head><meta charset="utf-8"><title>${esc(titulo)}</title>
<style>@page{size:${W}mm ${H}mm;margin:0;}${CSS_BASE}:root{--W:${W}mm;--H:${H}mm;}${extra}</style></head>
<body>${paginas.join("\n")}</body></html>`;
}

// ============================================================================
// 1. CUADERNO GUÍA (A4 vertical, 24 páginas, espiral del lado izquierdo)
// ============================================================================
const CUAD = { W: 210 + 2 * SANGRADO, H: 297 + 2 * SANGRADO };
const ZONA_CUAD = `left:${SANGRADO + 20}mm;top:${SANGRADO + 14}mm;right:${SANGRADO + 14}mm;bottom:${SANGRADO + 17}mm;`;
const folio = (n) =>
  `<div class="folio" style="left:${SANGRADO + 20}mm;right:${SANGRADO + 14}mm;bottom:${SANGRADO + 7}mm;"><span>Mente Viva · NeuroGym</span><b>${n}</b></div>`;

const CSS_CUAD = `
.zona.c{font-size:15pt;}
h1.tema{font-size:40pt;line-height:1.05;margin:1mm 0 1mm;}
.titulo{font-family:'Fraunces',serif;font-style:italic;font-size:21pt;color:var(--rosa);line-height:1.15;}
.idea{margin:3mm 0 4mm;}
.filete{height:.35mm;background:var(--rosa);margin:0 0 4mm;}
.dos{display:flex;gap:5mm;margin-bottom:4mm;}
.caja{border:.35mm solid var(--rosa);border-radius:3mm;padding:3.5mm 4.5mm;flex:1;}
.caja h3{font-size:16pt;margin-bottom:.5mm;}
.caja .peque{font-size:12pt;color:var(--rosa);margin-bottom:2mm;font-weight:600;}
.caja ul.pts li{margin-bottom:1.2mm;}
.parte{display:flex;gap:4.5mm;margin-bottom:4.5mm;}
.circ{flex:none;width:11mm;height:11mm;border-radius:50%;background:var(--rosa);color:var(--marfil);font-family:'Fraunces',serif;font-weight:600;font-size:17pt;display:flex;align-items:center;justify-content:center;margin-top:.5mm;}
.pc{flex:1;}
.pc h2{font-size:19pt;line-height:1.15;margin-bottom:1.5mm;}
.consejo{font-style:italic;color:var(--rosa);margin-top:1.5mm;font-size:14pt;}
.frase{font-family:'Fraunces',serif;font-style:italic;font-size:19pt;color:var(--rosa);text-align:center;margin:5mm 0 4mm;line-height:1.25;}
.hija{border-top:.35mm solid var(--rosa);padding-top:3mm;font-size:14pt;}
.hija b{color:var(--rosa);}
ol.pasos{list-style:none;counter-reset:p;}
ol.pasos li{counter-increment:p;position:relative;padding-left:9mm;margin-bottom:2.2mm;}
ol.pasos li::before{content:counter(p,lower-alpha);position:absolute;left:0;top:0;font-family:'Fraunces',serif;font-weight:600;color:var(--rosa);font-size:17pt;}
.traba{margin:1mm 0 4.5mm;}
.traba ul.pts li{margin-bottom:.8mm;font-size:14pt;}
ul.preg li{margin-bottom:1mm;}
.sentir h3{font-size:16pt;color:var(--rosa);margin-bottom:1mm;}
`;

function paginaEncuentroA(e, num) {
  const sem = SEMANAS.find((s) => s.encuentros.includes(e.n)).n;
  const li = (a) => a.map((x) => `<li>${esc(x)}</li>`).join("");
  return `<section class="pagina"><div class="zona c" style="${ZONA_CUAD}">
<div class="kick">Encuentro ${e.n} · Semana ${sem}</div>
<h1 class="tema">${esc(e.tema)}</h1>
<div class="titulo">${esc(e.titulo)}</div>
<p class="idea">${esc(e.idea)}</p>
<div class="filete"></div>
<div class="dos">
 <div class="caja"><h3>Antes de empezar</h3><div class="peque">Para vos · 5 minutos</div><ul class="pts">${li(e.antes)}</ul></div>
 <div class="caja"><h3>Necesitamos</h3><div class="peque">Para los dos</div><ul class="pts">${li(e.necesitamos)}</ul></div>
</div>
<div class="parte"><div class="circ">1</div><div class="pc"><h2>Canción de bienvenida<span class="min">5 min</span></h2><p>${esc(e.cancion.que)}</p><p class="consejo">${esc(e.cancion.consejo)}</p></div></div>
<div class="parte"><div class="circ">2</div><div class="pc"><h2>¿Qué día es hoy?<span class="min">5 min</span></h2><p>${esc(e.queDia.que)}</p><p class="consejo">${esc(e.queDia.consejo)}</p></div></div>
<div class="frase">«${esc(e.frase)}»</div>
<div class="hija"><b>Para vos:</b> ${esc(e.paraLaHija)}</div>
</div>${folio(num)}</section>`;
}

function paginaEncuentroB(e, num) {
  const li = (a) => a.map((x) => `<li>${esc(x)}</li>`).join("");
  return `<section class="pagina"><div class="zona c" style="${ZONA_CUAD}">
<div class="kick">Encuentro ${e.n} · ${esc(e.tema)}</div>
<div class="parte" style="margin-top:2mm"><div class="circ">3</div><div class="pc"><h2>Actividad principal<span class="min">25 min</span></h2>
<div class="titulo" style="font-size:17pt;margin-bottom:2.5mm">${esc(e.titulo)}</div>
<ol class="pasos">${li(e.principal.pasos)}</ol></div></div>
<div class="caja traba"><h3>Si se traba</h3><ul class="pts">${li(e.principal.siSeTraba)}</ul></div>
<div class="parte"><div class="circ">4</div><div class="pc"><h2>Charla de cierre<span class="min">10 min</span></h2>
<ul class="pts preg">${li(e.cierre.preguntas)}</ul><p class="consejo">${esc(CUADERNO.cierreEncuentro)}</p></div></div>
<div class="sentir"><h3>${esc(CUADERNO.comoMeSenti)}</h3><div class="renglones" style="height:18mm"></div></div>
</div>${folio(num)}</section>`;
}

function armarCuaderno() {
  const pg = [];
  let n = 0;
  const sec = (html) => { n += 1; pg.push(html(n)); };
  const C = CUADERNO;
  const lema = LEMA;

  // 1. Portada
  sec(() => `<section class="pagina">
<div class="zona" style="left:${SANGRADO + 18}mm;right:${SANGRADO + 18}mm;top:${SANGRADO + 26}mm;bottom:${SANGRADO + 14}mm;text-align:center;">
 <div class="kick" style="font-size:13pt">${esc(C.portada.tipo)}</div>
 <h1 style="font-size:74pt;line-height:1;margin-top:8mm;letter-spacing:-.01em">${esc(C.portada.titulo)}</h1>
 <div class="fr" style="font-style:italic;font-weight:400;font-size:40pt;color:var(--rosa);margin-top:1mm">${esc(C.portada.marca)}</div>
 <p style="font-size:19pt;margin:9mm auto 0;max-width:130mm;line-height:1.3">${esc(C.portada.bajada)}</p>
 <div style="width:120mm;height:120mm;margin:12mm auto 0">${lotoDecorativo(ROSA, 1, 200)}</div>
 <div style="position:absolute;left:0;right:0;bottom:0">
  <div class="fr" style="font-size:22pt">${esc(FIRMA)}</div>
  <div class="kick" style="margin-top:1mm">${esc(MARCA)}</div>
 </div>
</div></section>`);

  // 2. Bienvenida y cómo usarlo
  sec((k) => `<section class="pagina"><div class="zona c" style="${ZONA_CUAD}">
<div class="kick">Antes de empezar</div>
<h1 style="font-size:32pt;line-height:1.1;margin:1mm 0 4mm">${esc(C.bienvenida.titulo)}</h1>
<p style="margin-bottom:5mm">${esc(C.bienvenida.intro)}</p>
<div class="dos">${C.bienvenida.roles.map((r) => `<div class="caja"><h3 class="rosa">${esc(r.quien)}</h3><p style="font-size:14pt">${esc(r.que)}</p></div>`).join("")}</div>
<h2 style="font-size:20pt;margin:5mm 0 2mm">Cómo usarlo</h2>
<ul class="pts">${C.bienvenida.comoUsarlo.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>
<p class="fr" style="font-style:italic;font-weight:400;color:var(--rosa);font-size:17pt;margin:5mm 0 6mm;line-height:1.25">${esc(C.bienvenida.reglas)}</p>
<div class="caja" style="padding:4mm 5mm"><h3 style="font-size:14pt;margin-bottom:1mm" class="rosa">Importante</h3><p style="font-size:14pt">${esc(AVISO)}</p></div>
</div>${folio(k)}</section>`);

  // 3. Su semana
  sec((k) => `<section class="pagina"><div class="zona c" style="${ZONA_CUAD}">
<div class="kick">Ritmo</div>
<h1 style="font-size:32pt;line-height:1.1;margin:1mm 0 1mm">${esc(C.semana.titulo)}</h1>
<p style="margin-bottom:5mm">${esc(C.semana.bajada)}</p>
${C.semana.bloques.map((b) => `<div class="parte" style="align-items:center;margin-bottom:4mm;border:.35mm solid var(--rosa);border-radius:3mm;padding:3mm 4mm">
 <div style="flex:none;width:26mm;text-align:center"><div class="fr" style="font-size:36pt;line-height:1;color:var(--rosa)">${esc(b.grande)}</div><div style="font-size:11pt;font-weight:700;color:var(--rosa);line-height:1.15">${esc(b.unidad)}</div></div>
 <div class="pc"><h2 style="font-size:17pt;margin-bottom:.5mm">${esc(b.nombre)}</h2><p style="font-size:14pt">${esc(b.texto)}</p></div></div>`).join("")}
<h2 style="font-size:19pt;margin:6mm 0 2mm">${esc(C.semana.cuadro)}</h2>
${SEMANAS.map((s) => `<div style="display:flex;gap:4mm;align-items:baseline;padding:1.6mm 0;border-bottom:.3mm solid var(--rosa)"><b class="rosa" style="width:26mm;flex:none">Semana ${s.n}</b><span>${s.encuentros.map((i) => `${i}. ${esc(encuentros[i - 1].tema)}`).join("  ·  ")}</span></div>`).join("")}
</div>${folio(k)}</section>`);

  // 4. Cómo es cada encuentro
  sec((k) => `<section class="pagina"><div class="zona c" style="${ZONA_CUAD}">
<div class="kick">Cada encuentro</div>
<h1 style="font-size:32pt;line-height:1.1;margin:1mm 0 1mm">${esc(C.encuentro.titulo)}</h1>
<p style="margin-bottom:5mm">${esc(C.encuentro.bajada)}</p>
<div style="display:flex;height:7mm;border-radius:3.5mm;overflow:hidden;border:.35mm solid var(--rosa);margin-bottom:6mm">
 ${C.encuentro.partes.map((p, i) => `<div style="flex:${p.min};background:${i % 2 === 0 ? ROSA : MARFIL}"></div>`).join("")}
</div>
${C.encuentro.partes.map((p, i) => `<div class="parte"><div class="circ">${i + 1}</div><div class="pc"><h2>${esc(p.nombre)}<span class="min">${p.min} min</span></h2><p>${esc(p.texto)}</p></div></div>`).join("")}
<div class="caja" style="margin-top:7mm;padding:5mm 6mm"><h3 class="rosa" style="font-size:19pt;margin-bottom:2mm">${esc(C.encuentro.reglasTitulo)}</h3><ul class="pts" style="font-size:16pt">${C.encuentro.reglas.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>
</div>${folio(k)}</section>`);

  // 5 a 20. Los 8 encuentros (2 páginas cada uno)
  for (const e of encuentros) {
    sec((k) => paginaEncuentroA(e, k));
    sec((k) => paginaEncuentroB(e, k));
  }

  // 21. Y ahora, ¿qué sigue?
  sec((k) => `<section class="pagina"><div class="zona c" style="${ZONA_CUAD}">
<div class="kick">Cierre</div>
<h1 style="font-size:32pt;line-height:1.1;margin:1mm 0 2mm">${esc(C.final.titulo)}</h1>
<p style="margin-bottom:5mm">${esc(C.final.intro)}</p>
<ul class="pts" style="margin-bottom:6mm">${C.final.seguir.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>
${C.final.preguntas.map((p) => `<div style="margin-bottom:1mm"><b class="rosa">${esc(p)}</b><div class="renglones" style="height:18mm"></div></div>`).join("")}
</div>${folio(k)}</section>`);

  // 22 y 23. Mis recuerdos
  for (let i = 0; i < 2; i++) {
    sec((k) => `<section class="pagina"><div class="zona c" style="${ZONA_CUAD}">
<div class="kick">${esc(C.recuerdos.titulo)}</div>
${i === 0 ? `<p style="margin:2mm 0 4mm">${esc(C.recuerdos.bajada)}</p>` : `<div style="height:8mm"></div>`}
<div class="renglones" style="height:${i === 0 ? 216 : 234}mm"></div>
</div>${folio(k)}</section>`);
  }

  // 24. Contratapa
  sec(() => `<section class="pagina">
<div class="zona" style="left:${SANGRADO + 20}mm;right:${SANGRADO + 14}mm;top:${SANGRADO + 40}mm;bottom:${SANGRADO + 16}mm;text-align:center;">
 <div style="width:70mm;height:70mm;margin:0 auto">${lotoDecorativo(ROSA, 1, 200)}</div>
 <p class="fr" style="font-style:italic;font-weight:400;font-size:24pt;color:var(--rosa);margin:12mm auto 0;max-width:120mm;line-height:1.25">${esc(C.contratapa.texto)}</p>
 <div style="position:absolute;left:0;right:0;bottom:0">
  <p style="font-size:12pt;max-width:130mm;margin:0 auto 6mm">${esc(AVISO)}</p>
  <div class="fr" style="font-size:20pt">${esc(FIRMA)}</div>
  <div class="kick" style="margin-top:1mm">${esc(MARCA)}</div>
 </div>
</div></section>`);

  return { nombre: "cuaderno-guia", titulo: "Mente Viva NeuroGym · Cuaderno guía", W: CUAD.W, H: CUAD.H, paginas: pg, css: CSS_CUAD, sangrado: SANGRADO };
}

// ============================================================================
// 2. GUÍA PARA LA HIJA (A5 vertical, 8 páginas)
// ============================================================================
const A5 = { W: 148 + 2 * SANGRADO, H: 210 + 2 * SANGRADO };
const ZONA_A5 = `left:${SANGRADO + 14}mm;top:${SANGRADO + 14}mm;right:${SANGRADO + 14}mm;bottom:${SANGRADO + 16}mm;`;
const folioA5 = (n) =>
  `<div class="folio" style="left:${SANGRADO + 14}mm;right:${SANGRADO + 14}mm;bottom:${SANGRADO + 7}mm;"><span>Guía para vos</span><b>${n}</b></div>`;
const CSS_A5 = `
.zona.g{font-size:13.5pt;line-height:1.38;}
.zona.g h1{font-size:25pt;line-height:1.1;margin:1mm 0 4mm;}
.zona.g p{margin-bottom:3mm;}
.dos2{display:flex;gap:4mm;}
.col{flex:1;border:.35mm solid var(--rosa);border-radius:3mm;padding:3.5mm 4mm;}
.col h3{font-size:16pt;color:var(--rosa);margin-bottom:2mm;}
.col ul.pts li{margin-bottom:1.4mm;font-size:13pt;}
.cs{border-bottom:.3mm solid var(--rosa);padding:2.6mm 0;}
.cs b{color:var(--rosa);}
.fila{display:flex;gap:3mm;padding:2mm 0;border-bottom:.3mm solid var(--rosa);font-size:12pt;line-height:1.3;}
.fila b{flex:none;width:34mm;color:var(--rosa);}
`;

function armarGuiaHija() {
  const G = GUIA_HIJA;
  const pg = [];
  let n = 0;
  const sec = (html) => { n += 1; pg.push(html(n)); };
  const li = (a) => a.map((x) => `<li>${esc(x)}</li>`).join("");

  sec(() => `<section class="pagina"><div class="zona" style="left:${SANGRADO + 12}mm;right:${SANGRADO + 12}mm;top:${SANGRADO + 22}mm;bottom:${SANGRADO + 12}mm;text-align:center;">
 <div class="kick">${esc(G.portada.tipo)}</div>
 <h1 style="font-size:46pt;line-height:1.02;margin-top:10mm">${esc(G.portada.titulo)}</h1>
 <p class="fr" style="font-style:italic;font-weight:400;font-size:20pt;color:var(--rosa);margin:6mm auto 0;max-width:100mm;line-height:1.25">${esc(G.portada.bajada)}</p>
 <div style="width:78mm;height:78mm;margin:12mm auto 0">${lotoDecorativo(ROSA, 1, 200)}</div>
 <div style="position:absolute;left:0;right:0;bottom:0"><div class="fr" style="font-size:17pt">${esc(FIRMA)}</div><div class="kick" style="margin-top:1mm;font-size:10pt">${esc(MARCA)}</div></div>
</div></section>`);

  sec((k) => `<section class="pagina"><div class="zona g" style="${ZONA_A5}">
<div class="kick">Para empezar</div><h1>${esc(G.lugar.titulo)}</h1>
${G.lugar.parrafos.map((p) => `<p>${esc(p)}</p>`).join("")}
</div>${folioA5(k)}</section>`);

  sec((k) => `<section class="pagina"><div class="zona g" style="${ZONA_A5}">
<div class="kick">Qué hacer</div><h1>${esc(G.siNo.titulo)}</h1>
<div class="dos2">
 <div class="col"><h3>${esc(G.siNo.siTitulo)}</h3><ul class="pts">${li(G.siNo.si)}</ul></div>
 <div class="col"><h3>${esc(G.siNo.noTitulo)}</h3><ul class="pts">${li(G.siNo.no)}</ul></div>
</div></div>${folioA5(k)}</section>`);

  sec((k) => `<section class="pagina"><div class="zona g" style="${ZONA_A5}">
<div class="kick">Qué decir</div><h1>${esc(G.frases.titulo)}</h1>
<div class="col" style="margin-bottom:4mm"><h3>${esc(G.frases.ayudanTitulo)}</h3><ul class="pts">${li(G.frases.ayudan)}</ul></div>
<div class="col"><h3>${esc(G.frases.evitarTitulo)}</h3><ul class="pts">${li(G.frases.evitar)}</ul></div>
</div>${folioA5(k)}</section>`);

  sec((k) => `<section class="pagina"><div class="zona g" style="${ZONA_A5}">
<div class="kick">Qué pasa si…</div><h1>${esc(G.siPasa.titulo)}</h1>
${G.siPasa.casos.map((c) => `<div class="cs"><b>${esc(c.cuando)}.</b> ${esc(c.que)}</div>`).join("")}
</div>${folioA5(k)}</section>`);

  sec((k) => `<section class="pagina"><div class="zona g" style="${ZONA_A5}">
<div class="kick">Tu preparación</div><h1>${esc(G.semana.titulo)}</h1>
<p style="margin-bottom:2mm">${esc(G.semana.bajada)}</p>
${encuentros.map((e) => `<div class="fila"><b>${e.n}. ${esc(e.tema)}</b><span>${esc(e.antes[0])}</span></div>`).join("")}
</div>${folioA5(k)}</section>`);

  sec((k) => `<section class="pagina"><div class="zona g" style="${ZONA_A5}">
<div class="kick">Para vos</div><h1>${esc(G.cuidate.titulo)}</h1>
${G.cuidate.parrafos.map((p) => `<p>${esc(p)}</p>`).join("")}
<div class="col" style="margin-top:5mm"><h3>Importante</h3><p style="font-size:13pt;margin:0">${esc(AVISO)}</p></div>
</div>${folioA5(k)}</section>`);

  sec(() => `<section class="pagina"><div class="zona" style="left:${SANGRADO + 12}mm;right:${SANGRADO + 12}mm;top:${SANGRADO + 38}mm;bottom:${SANGRADO + 14}mm;text-align:center;">
 <div style="width:46mm;height:46mm;margin:0 auto">${lotoDecorativo(ROSA, 1, 200)}</div>
 <p class="fr" style="font-style:italic;font-weight:400;font-size:19pt;color:var(--rosa);margin:10mm auto 0;max-width:100mm;line-height:1.25">${esc(G.contratapa)}</p>
 <div style="position:absolute;left:0;right:0;bottom:0"><div class="fr" style="font-size:17pt">${esc(FIRMA)}</div><div class="kick" style="margin-top:1mm;font-size:10pt">${esc(MARCA)}</div></div>
</div></section>`);

  return { nombre: "guia-para-la-hija", titulo: "Mente Viva NeuroGym · Guía para la hija", W: A5.W, H: A5.H, paginas: pg, css: CSS_A5, sangrado: SANGRADO };
}

// ============================================================================
// 3. PIZARRA DE HELADERA (A4 apaisado)
// ============================================================================
function armarPizarra() {
  const W = 297 + 2 * SANGRADO, H = 210 + 2 * SANGRADO;
  const P = PIZARRA;
  const col = 18; // mm por círculo
  const gap = 8;
  const grid = `grid-template-columns:34mm repeat(2,${col}mm) ${gap}mm repeat(3,${col}mm) ${gap}mm repeat(7,${col}mm);`;
  const cab1 = `<div></div><div style="grid-column:span 2;text-align:center" class="g">${P.columnas[0].nombre}</div><div></div><div style="grid-column:span 3;text-align:center" class="g">${P.columnas[1].nombre}</div><div></div><div style="grid-column:span 7;text-align:center" class="g">${P.columnas[2].nombre}</div>`;
  const cab2 = `<div></div>${[1, 2].map((i) => `<div class="d">${i}</div>`).join("")}<div></div>${[1, 2, 3].map((i) => `<div class="d">${i}</div>`).join("")}<div></div>${P.columnas[2].dias.map((d) => `<div class="d">${d}</div>`).join("")}`;
  const circ = `<div class="o"><i></i></div>`;
  const filas = [1, 2, 3, 4].map((s) => `<div class="s">Semana ${s}</div>${circ.repeat(2)}<div></div>${circ.repeat(3)}<div></div>${circ.repeat(7)}`).join("");
  const css = `
.zona.p{left:${SANGRADO + 14}mm;right:${SANGRADO + 14}mm;top:${SANGRADO + 11}mm;bottom:${SANGRADO + 11}mm;}
.t{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:5mm;}
.t h1{font-size:34pt;line-height:1;}
.t p{font-size:13pt;margin-top:1.5mm;}
.tabla{display:grid;${grid}row-gap:0;align-items:center;}
.tabla .g{font-family:'Fraunces',serif;font-weight:600;font-size:16pt;color:var(--rosa);border-bottom:.4mm solid var(--rosa);padding-bottom:1mm;}
.tabla .d{text-align:center;font-weight:700;font-size:12pt;color:var(--rosa);padding:1.5mm 0;}
.tabla .s{font-family:'Fraunces',serif;font-weight:600;font-size:15pt;height:26mm;display:flex;align-items:center;border-top:.3mm solid var(--rosa);}
.tabla .o{height:26mm;display:flex;align-items:center;justify-content:center;border-top:.3mm solid var(--rosa);}
.tabla .o i{display:block;width:13mm;height:13mm;border-radius:50%;border:.5mm solid var(--rosa);}
.tabla > div:empty{border-top:.3mm solid var(--rosa);}
.pie{margin-top:3mm;font-weight:700;color:var(--rosa);font-size:13pt;}
`;
  const pagina = `<section class="pagina"><div class="zona p">
<div class="t"><div><h1>${esc(P.titulo)}</h1><p>${esc(P.bajada)}</p></div><div style="text-align:right"><div class="fr" style="font-size:16pt">Mente Viva · NeuroGym</div><div class="kick" style="font-size:10pt;margin-top:.5mm">${esc(FIRMA)} · ${esc(MARCA)}</div></div></div>
<div class="tabla">${cab1}${cab2}${filas}</div>
<div class="pie">${esc(P.pie)}</div><div class="renglones" style="height:18mm"></div>
</div></section>`;
  return { nombre: "pizarra-heladera-registro-semanal", titulo: "Mente Viva NeuroGym · Pizarra de heladera", W, H, paginas: [pagina], css, sangrado: SANGRADO };
}

// ============================================================================
// 4. LÁMINA "10 MINUTOS DE FUERZA Y EQUILIBRIO" (A4 vertical)
// ============================================================================
function armarLamina() {
  const W = 210 + 2 * SANGRADO, H = 297 + 2 * SANGRADO;
  const css = `
.zona.l{left:${SANGRADO + 15}mm;right:${SANGRADO + 15}mm;top:${SANGRADO + 13}mm;bottom:${SANGRADO + 11}mm;}
.zona.l h1{font-size:33pt;line-height:1.05;margin:1mm 0 2mm;}
.zona.l .b{font-size:15pt;margin-bottom:4mm;}
.antes{border:.35mm solid var(--rosa);border-radius:3mm;padding:3mm 5mm;margin-bottom:3.5mm;}
.antes ul.pts li{font-size:14pt;margin-bottom:.8mm;}
.ej{display:flex;gap:4mm;align-items:center;border-top:.3mm solid var(--rosa);height:30mm;}
.ej .n{flex:none;width:11mm;height:11mm;border-radius:50%;background:var(--rosa);color:var(--marfil);font-family:'Fraunces',serif;font-weight:600;font-size:17pt;display:flex;align-items:center;justify-content:center;}
.ej .f{flex:none;width:26mm;height:31mm;}
.ej .f svg{width:100%;height:100%;display:block;}
.ej h2{font-size:18pt;line-height:1.1;margin-bottom:.8mm;}
.ej p{font-size:14.5pt;line-height:1.3;}
.ej .dosis{color:var(--rosa);font-weight:700;font-size:13pt;margin-top:.8mm;}
.av{font-size:11.5pt;margin-top:2.5mm;border-top:.3mm solid var(--rosa);padding-top:2mm;}
`;
  const L_ = LAMINA;
  const pagina = `<section class="pagina"><div class="zona l">
<div class="kick">Mente Viva · NeuroGym</div>
<h1>${esc(L_.titulo)}</h1>
<p class="b">${esc(L_.bajada)}</p>
<div class="antes"><ul class="pts">${L_.antes.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>
${MOVIMIENTO.map((m) => `<div class="ej"><div class="n">${m.n}</div><div class="f"><svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg">${FIGURAS[m.figura]}</svg></div><div><h2>${esc(m.nombre)}</h2><p>${esc(m.como)}</p><div class="dosis">${esc(m.dosis)}</div></div></div>`).join("")}
<p class="av">${esc(L_.aviso)} <b class="rosa">${esc(FIRMA)} · ${esc(MARCA)}</b></p>
</div></section>`;
  return { nombre: "lamina-fuerza-y-equilibrio", titulo: "Mente Viva NeuroGym · 10 minutos de fuerza y equilibrio", W, H, paginas: [pagina], css, sangrado: SANGRADO };
}

// ============================================================================
// 5. MAZO DE TARJETAS DE RECUERDOS (A4, 3 hojas de frente + 1 hoja de dorso)
// ============================================================================
function armarTarjetas() {
  const W = 210, H = 297;
  const cw = 63, ch = 88, x0 = (W - 3 * cw) / 2, y0 = (H - 3 * ch) / 2;
  const marcas = () => {
    let m = "";
    const xs = [0, 1, 2, 3].map((i) => x0 + i * cw);
    const ys = [0, 1, 2, 3].map((j) => y0 + j * ch);
    for (const x of xs) {
      m += `<line x1="${x}" y1="${y0 - 8}" x2="${x}" y2="${y0 - 2}"/><line x1="${x}" y1="${y0 + 3 * ch + 2}" x2="${x}" y2="${y0 + 3 * ch + 8}"/>`;
    }
    for (const y of ys) {
      m += `<line x1="${x0 - 8}" y1="${y}" x2="${x0 - 2}" y2="${y}"/><line x1="${x0 + 3 * cw + 2}" y1="${y}" x2="${x0 + 3 * cw + 8}" y2="${y}"/>`;
    }
    return `<svg style="position:absolute;left:0;top:0" width="${W}mm" height="${H}mm" viewBox="0 0 ${W} ${H}" stroke="${CACAO}" stroke-width=".18">${m}</svg>`;
  };
  const posicion = (i) => `left:${x0 + (i % 3) * cw}mm;top:${y0 + Math.floor(i / 3) * ch}mm;`;
  const css = `
.zona,.tj{position:absolute;}
.tj{width:${cw}mm;height:${ch}mm;background:var(--marfil);}
.tj .m{position:absolute;inset:4mm;border:.4mm solid var(--rosa);border-radius:3mm;padding:5mm 4.5mm;display:flex;flex-direction:column;}
.tj .tm{font-size:9.5pt;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--rosa);}
.tj .tx{font-family:'Fraunces',serif;font-weight:400;font-size:15pt;line-height:1.28;margin-top:5mm;flex:1;}
.tj .pie{font-size:9.5pt;color:var(--rosa);font-weight:600;text-align:center;}
.tj.dorso .m{align-items:center;justify-content:center;text-align:center;}
`;
  const frente = (t, i) =>
    `<div class="tj" style="${posicion(i)}"><div class="m"><div class="tm">${esc(t.tema)}</div><div class="tx">${esc(t.texto)}</div><div class="pie">Mente Viva · NeuroGym</div></div></div>`;
  const todas = [];
  for (const g of TARJETAS) for (const tx of g.textos) todas.push({ tema: g.tema, texto: tx });
  for (let i = 0; i < 3; i++) todas.push({ tema: TARJETAS_TEXTOS.enBlanco, texto: TARJETAS_TEXTOS.enBlancoBajada, blanco: true });
  const hojas = [];
  for (let h = 0; h < 3; h++) {
    const grupo = todas.slice(h * 9, h * 9 + 9);
    hojas.push(`<section class="pagina" style="background:#fff">${grupo.map((t, i) => frente(t, i)).join("")}${marcas()}</section>`);
  }
  const dorso = `<div class="tj dorso" style="__POS__"><div class="m"><div style="width:30mm;height:30mm">${lotoDecorativo(ROSA, 1.1, 200)}</div><div class="fr" style="font-size:20pt;margin-top:4mm">${esc(TARJETAS_TEXTOS.dorsoTitulo)}</div><div class="tm" style="margin-top:2mm">${esc(TARJETAS_TEXTOS.dorsoBajada)}</div></div></div>`;
  hojas.push(`<section class="pagina" style="background:#fff">${Array.from({ length: 9 }, (_, i) => dorso.replace("__POS__", posicion(i))).join("")}${marcas()}</section>`);
  return { nombre: "mazo-tarjetas-recuerdos", titulo: "Mente Viva NeuroGym · Mazo de tarjetas de recuerdos", W, H, paginas: hojas, css, sangrado: 0, tarjetas: true };
}

// ============================================================================
// 6. MANDALAS DE CIERRE (A4, línea negra de 2 pt, sin grises)
// ============================================================================
function armarMandalas() {
  const W = 210, H = 297;
  const css = `
.pagina{background:#fff;}
.mz{position:absolute;left:0;right:0;top:0;bottom:0;text-align:center;color:#000;}
.mz h1{font-size:28pt;margin-top:18mm;color:#000;}
.mz p{font-size:14pt;margin-top:2mm;}
.mz .loto{position:absolute;left:10mm;top:60mm;width:190mm;height:190mm;}
.mz .loto svg{width:100%;height:100%;display:block;}
.mz .pie{position:absolute;left:0;right:0;bottom:14mm;font-size:11pt;}
`;
  const paginas = LOTOS_SEMANA.map((l) => {
    const { svg } = lotoSVG({ anillos: l.anillos, centro: l.centro, trazoPt: 2, color: "#000", relleno: "#fff", lado: 200 });
    return `<section class="pagina"><div class="mz"><h1>${esc(MANDALAS.titulo)} ${l.semana}</h1><p>${esc(MANDALAS.bajada)}</p><div class="loto">${svg}</div><div class="pie">${esc(FIRMA)} · ${esc(MARCA)}</div></div></section>`;
  });
  return { nombre: "mandalas-de-cierre", titulo: "Mente Viva NeuroGym · Mandalas de cierre", W, H, paginas, css, sangrado: 0 };
}

// ============================================================================
// Render
// ============================================================================
const PIEZAS = {
  cuaderno: armarCuaderno,
  guia: armarGuiaHija,
  pizarra: armarPizarra,
  lamina: armarLamina,
  tarjetas: armarTarjetas,
  mandalas: armarMandalas,
};

async function renderizar(browser, pieza) {
  const html = documento(pieza.titulo, pieza.W, pieza.H, pieza.paginas, pieza.css);
  const archivo = path.join(HTML_DIR, `${pieza.nombre}.html`);
  fs.writeFileSync(archivo, html);
  const page = await browser.newPage();
  await page.goto("file://" + archivo, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  // ¿Se sale algún texto de su página?
  const desbordes = await page.evaluate(() =>
    [...document.querySelectorAll(".pagina")].flatMap((p, i) => {
      const out = [];
      for (const z of p.querySelectorAll(".zona, .tj .m")) {
        const sobra = z.scrollHeight - z.clientHeight;
        if (sobra > 1) out.push({ pagina: i + 1, sobra: Math.round(sobra * 10) / 10 });
      }
      return out;
    }),
  );
  const salida = path.join(PDF_DIR, `${pieza.nombre}.pdf`);
  await page.pdf({ path: salida, width: `${pieza.W}mm`, height: `${pieza.H}mm`, printBackground: true, preferCSSPageSize: true });
  await page.close();
  // Cajas de corte y sangrado (para la imprenta)
  if (pieza.sangrado > 0) {
    execFileSync("python3", [path.join(AQUI, "cajas.py"), salida, String(pieza.sangrado)]);
  }
  return { salida, desbordes };
}

const quiere = process.argv.slice(2);
const lista = quiere.length ? quiere : Object.keys(PIEZAS);
const browser = await chromium.launch();
let hayDesborde = false;
for (const clave of lista) {
  if (!PIEZAS[clave]) { console.log("pieza desconocida:", clave); continue; }
  const pieza = PIEZAS[clave]();
  const { salida, desbordes } = await renderizar(browser, pieza);
  console.log(`${desbordes.length ? "⚠" : "✓"} ${path.relative(RAIZ, salida)}${desbordes.length ? "  SE SALE: " + JSON.stringify(desbordes) : ""}`);
  if (desbordes.length) hayDesborde = true;
}
await browser.close();
process.exit(hayDesborde ? 2 : 0);
