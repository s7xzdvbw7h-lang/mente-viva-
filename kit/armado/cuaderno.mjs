// Cuaderno "La hora del té": A4 vertical espiralado, páginas dobles (verso | recto).
// El margen del espiral (20 mm) va del lado interior: a la derecha en las páginas pares, a la izquierda en las impares.
import { SANGRADO as S, esc } from "./base.mjs";
import {
  encuentros, SEMANAS, MOMENTOS, NIVELES, AVISO, FIRMA, MARCA, PRODUCTO,
} from "../contenido/encuentros.mjs";
import { CUADERNO, PAUSAS } from "../contenido/generales.mjs";
import { C, icono, loto, escenaTe, lenguetas, avance, anilloMomentos } from "./diseno.mjs";
import { ILUS } from "./ilustraciones.mjs";

export const CUAD = { W: 210 + 2 * S, H: 297 + 2 * S };
const W = CUAD.W, H = CUAD.H;

// Zona del libro de mandalas dentro de la página (mm, medidos desde el borde con sangrado).
export const RECT_MANDALA = { x0: S + 24, y0: S + 46, x1: W - (S + 20), y1: H - (S + 30) };

export const CSS_CUADERNO = `
:root{--velado:#E4D3CD;--suave:#EEE3DC;}
.pagina{background:var(--marfil);}
.zona{overflow:hidden;}
.pf{position:absolute;display:flex;align-items:center;gap:6mm;}
.pnum{width:11mm;height:11mm;border-radius:50%;background:var(--rosa);color:var(--marfil);font-family:'Fraunces',serif;font-weight:600;font-size:16pt;display:flex;align-items:center;justify-content:center;}
.pagina.sobre-rosa .pnum{background:var(--marfil);color:var(--rosa);}
.pdots svg{display:block;}

.chip{display:inline-block;padding:1mm 4.2mm;border-radius:20mm;background:var(--rosa);color:var(--marfil);font-weight:700;font-size:16pt;letter-spacing:.07em;text-transform:uppercase;line-height:1.3;white-space:nowrap;}
.chip.o{background:transparent;color:var(--rosa);border:.45mm solid var(--rosa);padding:.7mm 4mm;}
.chips{display:flex;gap:3mm;flex-wrap:wrap;margin-bottom:4mm;}

h1.tema{font-size:54pt;line-height:1;margin:0 0 1.5mm;}
h1.gr{font-size:38pt;line-height:1.04;margin:0 0 3mm;}
.titulo{font-family:'Fraunces',serif;font-style:italic;font-weight:400;font-size:24pt;color:var(--rosa);line-height:1.15;}
.cabeza{display:flex;gap:6mm;align-items:flex-start;margin-bottom:5mm;}
.cabeza .tx{flex:1;}
.ilus{flex:none;width:56mm;height:56mm;border-radius:50%;background:var(--velado);padding:6mm;margin-top:0;}
.ilus svg{width:100%;height:100%;display:block;}
.idea{font-size:19pt;line-height:1.3;margin-top:3.5mm;}
.adorno{height:6mm;margin:0 0 4mm;}
.adorno svg{height:100%;width:62mm;display:block;}

.panel{background:var(--suave);border-radius:5mm;padding:5mm 6.5mm 3.4mm;margin-bottom:6mm;}
.panel.v{background:var(--velado);}
.panel h3{display:flex;align-items:center;gap:3mm;font-size:22pt;line-height:1.1;margin-bottom:2.4mm;}
.panel h3 .ic{width:9mm;height:9mm;flex:none;}
.panel h3 .sub{font-family:'Manrope',sans-serif;font-weight:600;font-size:16pt;color:var(--rosa);margin-left:auto;}
ul.chk{list-style:none;}
ul.chk li{position:relative;padding-left:10mm;margin-bottom:2.6mm;font-size:18pt;line-height:1.3;}
ul.chk li::before{content:"";position:absolute;left:0;top:.9mm;width:6mm;height:6mm;border-radius:50%;border:.6mm solid var(--rosa);background:var(--marfil);}
ul.pts li{font-size:17pt;line-height:1.3;}

.mom{display:flex;gap:5.5mm;padding:5mm 0;border-top:.5mm dotted var(--rosa);}
.mom:first-child{border-top:none;padding-top:0;}
.ib{flex:none;width:16mm;height:16mm;border-radius:50%;background:var(--rosa);display:flex;align-items:center;justify-content:center;}
.ib svg{width:9mm;height:9mm;}
.mc{flex:1;min-width:0;}
.mh{display:flex;align-items:center;gap:3.5mm;flex-wrap:wrap;margin-bottom:2mm;}
.mh h2{font-size:26pt;line-height:1.08;}
.pill{display:inline-block;padding:.3mm 3.2mm;border-radius:20mm;border:.45mm solid var(--rosa);color:var(--rosa);font-weight:700;font-size:16pt;line-height:1.1;white-space:nowrap;vertical-align:.4mm;}
.cons{font-size:19pt;line-height:1.3;}
.bur{position:relative;background:var(--suave);border-radius:4.5mm;padding:3mm 5mm 3mm 14mm;margin-top:3.5mm;font-family:'Fraunces',serif;font-style:italic;color:var(--rosa);font-size:19pt;line-height:1.3;}
.bur .co{position:absolute;left:4.4mm;top:3.6mm;width:6.4mm;height:6.4mm;}
.bur::after{content:"";position:absolute;left:8mm;bottom:-2.2mm;width:4.6mm;height:4.6mm;background:var(--suave);transform:rotate(45deg);border-radius:0 0 1.2mm 0;}
.nota{margin-top:5mm;font-size:18pt;line-height:1.3;}
.canc{margin-top:2.4mm;font-size:18pt;line-height:1.3;}
.canc b{color:var(--rosa);}
.hoy{display:flex;gap:3mm;margin-top:3mm;align-items:flex-end;}
.hoy div{flex:1;border-bottom:.45mm solid var(--rosa);height:10mm;}
.hoy div.m{flex:1.5;}
.hoy-et{display:flex;gap:3mm;font-weight:700;font-size:16pt;color:var(--rosa);}
.hoy-et span{flex:1;}
.hoy-et span.m{flex:1.5;}

.pasos{position:relative;margin:2mm 0 3mm;}
.pasos.c .pt{font-size:18pt;}
.pasos.c .paso{padding-bottom:3.2mm;}
.extra .panel{margin-bottom:3.4mm;padding:3.6mm 6mm 2.2mm;}
.extra .panel h3{margin-bottom:1.6mm;}
.paso{display:flex;gap:5mm;position:relative;padding-bottom:4.6mm;}
.paso:not(:last-child)::before{content:"";position:absolute;left:6mm;top:12.5mm;bottom:.5mm;border-left:.55mm dotted var(--rosa);}
.pl{flex:none;width:12.5mm;height:12.5mm;border-radius:50%;background:var(--marfil);border:.65mm solid var(--rosa);color:var(--rosa);font-family:'Fraunces',serif;font-weight:600;font-size:20pt;display:flex;align-items:center;justify-content:center;position:relative;z-index:1;}
.pt{flex:1;font-size:19pt;line-height:1.3;padding-top:.6mm;}
.pt .pill{margin-left:2mm;font-size:16pt;}
.titulo-act{font-family:'Fraunces',serif;font-style:italic;font-weight:400;font-size:23pt;color:var(--rosa);margin-bottom:3mm;}
.grupo-pal{display:inline-flex;gap:2.2mm;align-items:center;}
.pal{display:inline-block;width:5.5mm;height:5.5mm;border-radius:50%;border:.6mm solid var(--rosa);}
.pal.f{background:var(--rosa);}
.palmas{background:var(--suave);border-radius:4.5mm;padding:3.5mm 5.5mm;margin:1mm 0 4mm;}

.niv{border-radius:5mm;background:var(--suave);padding:3.5mm 6mm 2.5mm;margin-bottom:4.5mm;}
.niv.n2{background:var(--velado);}
.niv.n3{background:var(--velado);box-shadow:inset 0 0 0 .5mm var(--rosa);}
.nh{display:flex;align-items:center;gap:3.5mm;margin-bottom:1mm;}
.nh h3{font-size:23pt;}
.nh .fl{display:flex;gap:.8mm;margin-left:auto;}
.nh .fl svg{width:8.6mm;height:8.6mm;}
.fila{display:flex;align-items:flex-end;gap:3mm;flex-wrap:wrap;min-height:14mm;}
.fila .l{font-size:18pt;line-height:1.25;padding-bottom:1.6mm;}
.fila .s{font-size:23pt;font-weight:700;line-height:1.25;padding-bottom:1.2mm;}
.fila .b{flex:1;min-width:26mm;height:11mm;border-bottom:.45mm solid var(--rosa);}
.prob .l{font-size:19pt;line-height:1.3;margin:2mm 0 0;}

.cita{background:var(--velado);border-radius:6mm;padding:6mm 8mm;margin-bottom:4mm;position:relative;}
.cita .q{font-family:'Fraunces',serif;font-weight:600;font-size:27pt;line-height:1.18;}
.cita .ic{position:absolute;right:6mm;top:5mm;width:12mm;height:12mm;}
.cinta{position:absolute;left:0;right:0;bottom:0;background:var(--rosa);color:var(--marfil);border-radius:5mm;padding:4mm 6mm;display:flex;gap:4.5mm;align-items:center;font-family:'Fraunces',serif;font-weight:600;font-size:20pt;line-height:1.2;}
.cinta svg{width:12mm;height:12mm;flex:none;}

.marco-m{position:absolute;border:.7mm solid var(--rosa);border-radius:6mm;}
.marco-m::before{content:"";position:absolute;inset:2.2mm;border:.3mm solid var(--rosa);border-radius:4.2mm;}

.pagina.sobre-rosa{background:var(--rosa);color:var(--marfil);}
.pagina.sobre-rosa .kick,.pagina.sobre-rosa h1,.pagina.sobre-rosa h2{color:var(--marfil);}

/* portada y contratapa */
.portada .marco{position:absolute;left:${S + 11}mm;right:${S + 11}mm;top:${S + 11}mm;bottom:${S + 11}mm;border:.7mm solid var(--marfil);border-radius:8mm;}
.portada .marco::before{content:"";position:absolute;inset:2.6mm;border:.3mm solid var(--marfil);border-radius:5.8mm;}
.sello{position:absolute;width:44mm;height:44mm;border-radius:50%;background:var(--marfil);color:var(--rosa);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;transform:rotate(-9deg);box-shadow:0 0 0 1.4mm var(--rosa),0 0 0 1.9mm var(--marfil);}
.sello b{font-family:'Fraunces',serif;font-size:42pt;line-height:.95;}
.sello span{font-weight:700;font-size:16pt;line-height:1.15;}

.ind{display:flex;align-items:baseline;gap:2.5mm;margin-bottom:1.5mm;font-size:17pt;}
.ind .p{flex:1;border-bottom:.45mm dotted var(--rosa);transform:translateY(-1.4mm);}
.ind .n{font-family:'Fraunces',serif;font-weight:600;color:var(--rosa);}
.ind.sem{margin:2.6mm 0 1.4mm;font-family:'Fraunces',serif;font-weight:600;font-size:20pt;}
.ind.sem span:first-child{color:var(--rosa);}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:4.5mm;}
.card{background:var(--suave);border-radius:5mm;padding:4.5mm 5.5mm;}
.card.v{background:var(--velado);}
.card .ic{width:13mm;height:13mm;border-radius:50%;background:var(--rosa);display:flex;align-items:center;justify-content:center;margin-bottom:2.5mm;}
.card .ic svg{width:7.4mm;height:7.4mm;}
.card h3{font-size:22pt;line-height:1.1;margin-bottom:1.4mm;}
.card p{font-size:17pt;line-height:1.3;}

.sem-card{display:flex;gap:4.5mm;background:var(--suave);border-radius:5mm;padding:2.4mm 5mm;margin-bottom:2.2mm;}
.sem-card:nth-child(even){background:var(--velado);}
.sem-n{flex:none;width:21mm;height:21mm;border-radius:50%;background:var(--rosa);color:var(--marfil);display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Fraunces',serif;font-weight:600;line-height:1;}
.sem-n b{font-size:30pt;}
.sem-r{flex:1;}
.sem-r h3{font-size:20pt;line-height:1.1;margin-bottom:1mm;display:flex;gap:3mm;align-items:baseline;}
.sem-r h3 i{font-style:italic;font-weight:400;color:var(--rosa);font-size:19pt;}
.fl-r{display:flex;gap:3mm;align-items:center;margin-bottom:.8mm;font-size:16pt;line-height:1.22;}
.fl-r svg{width:7mm;height:7mm;flex:none;}
.fl-r b{color:var(--rosa);}

.leg{display:flex;gap:4mm;align-items:center;margin-bottom:3.4mm;}
.leg .ib{width:14mm;height:14mm;}
.leg .ib svg{width:8mm;height:8mm;}
.leg .t{flex:1;font-size:17pt;line-height:1.25;}
.leg .t h3{font-size:20pt;display:flex;gap:3mm;align-items:center;}

.resp .e{background:var(--suave);border-radius:5mm;padding:3.5mm 6mm 2.5mm;margin-bottom:4mm;}
.resp .e h3{font-size:21pt;margin-bottom:1.2mm;}
.resp .e .r{display:flex;gap:3mm;font-size:17pt;line-height:1.3;margin-bottom:1mm;}
.resp .e .r b{color:var(--rosa);flex:none;width:49mm;}

table.reg{width:100%;border-collapse:collapse;}
table.reg th{font-family:'Fraunces',serif;font-weight:600;font-size:20pt;color:var(--rosa);padding-bottom:2mm;}
table.reg td{height:27mm;border-top:.4mm solid var(--rosa);text-align:center;vertical-align:middle;}
table.reg td.e{text-align:left;}
table.reg td.e div{display:flex;gap:3mm;align-items:center;font-family:'Fraunces',serif;font-weight:600;font-size:18pt;line-height:1.05;}
table.reg td.e svg{width:11mm;height:11mm;flex:none;}
.cir{display:inline-block;width:12.5mm;height:12.5mm;border-radius:50%;border:.55mm solid var(--rosa);}

.sobre-rosa .renglon{border-bottom:.4mm solid var(--marfil);}
.sobre-rosa .et{color:var(--marfil);font-weight:700;}
.pausa-ic{width:38mm;height:38mm;border-radius:50%;background:var(--marfil);display:flex;align-items:center;justify-content:center;margin:2mm 0 8mm;}
.pausa-ic svg{width:21mm;height:21mm;}
.pausa-tx{font-size:20pt;line-height:1.32;margin-bottom:5mm;}
.pausa-nota{border:.5mm solid var(--marfil);border-radius:5mm;padding:4mm 6mm;font-size:18pt;line-height:1.3;margin-top:5mm;}
.ctl{display:grid;grid-template-columns:1fr 1fr;gap:4.5mm;margin:3mm 0 5mm;}
.ctl div{border:.5mm solid var(--marfil);border-radius:5mm;padding:3.5mm 5mm;}
.ctl h3{font-size:22pt;color:var(--marfil);margin-bottom:1mm;}
.ctl p{font-size:17pt;line-height:1.28;}

.billete{position:absolute;width:85mm;height:33mm;border:.5mm solid var(--rosa);border-radius:2.5mm;background:var(--marfil);}
.billete .in{position:absolute;inset:2mm;border:.3mm solid var(--rosa);border-radius:1.5mm;}
.billete .lo{position:absolute;left:3mm;top:3mm;width:25mm;height:25mm;}
.billete .v{position:absolute;right:5mm;top:2mm;font-family:'Fraunces',serif;font-weight:600;font-size:28pt;line-height:1.1;color:var(--cacao);}
.billete .t{position:absolute;right:5mm;top:15.5mm;font-size:16pt;font-weight:700;color:var(--rosa);text-align:right;line-height:1.1;white-space:nowrap;}
.billete .j{position:absolute;right:5mm;bottom:3.8mm;text-align:right;font-size:16pt;font-weight:700;letter-spacing:.08em;color:var(--rosa);white-space:nowrap;}
.moneda{position:absolute;width:48mm;height:48mm;border:.5mm solid var(--rosa);border-radius:50%;background:var(--marfil);text-align:center;}
.moneda .in{position:absolute;inset:1.8mm;border:.3mm solid var(--rosa);border-radius:50%;}
.moneda .v{position:absolute;left:0;right:0;top:9mm;font-family:'Fraunces',serif;font-weight:600;font-size:30pt;line-height:1.1;color:var(--cacao);}
.moneda .j{position:absolute;left:0;right:0;top:25mm;font-size:16pt;font-weight:700;color:var(--rosa);line-height:1.1;}
`;

// ----------------------------------------------------------------------------- piezas comunes
const li = (a) => a.map((x) => `<li>${esc(x)}</li>`).join("");
const margenes = (n) => {
  const v = n % 2 === 0;
  return { izq: S + (v ? 16 : 20), der: S + (v ? 20 : 16), v };
};
const zona = (n, extra = "") => {
  const m = margenes(n);
  return `left:${m.izq}mm;right:${m.der}mm;top:${S + 15}mm;bottom:${S + 25}mm;${extra}`;
};

const fondoLoto = (rosa = false) => {
  const t = rosa ? 128 : 156, b = rosa ? -58 : -46; // sobre rosa va más chico y más bajo, para no pisar el texto
  return `<div style="position:absolute;left:${(W - t) / 2}mm;bottom:${b}mm;width:${t}mm;height:${t}mm">${rosa ? loto(C.rosaLinea, 1.3, C.rosaSobre) : loto(C.velado, 1.3, C.suave)}</div>`;
};

function pag(n, cuerpo, o = {}) {
  const m = margenes(n);
  const tabs = o.tab ? lenguetas({ W, H, S, esVerso: m.v, actual: o.tab }) : "";
  const puntos = o.tab ? `<div class="pdots">${avance(o.tab)}</div>` : "";
  const pie = o.sinPie ? "" : `<div class="pf" style="left:${m.izq}mm;right:${m.der}mm;bottom:${S + 8}mm;justify-content:${m.v ? "flex-start" : "flex-end"};flex-direction:${m.v ? "row" : "row-reverse"}"><div class="pnum">${n}</div>${puntos}</div>`;
  return `<section class="pagina ${o.clase || ""}">${o.fondo ? fondoLoto(o.fondo === "rosa") : ""}${tabs}<div class="zona" style="${zona(n, o.zonaExtra || "")}">${cuerpo}</div>${pie}</section>`;
}

const adorno = () => `<div class="adorno">${ramita()}</div>`;
import { ramita } from "./diseno.mjs";

const ib = (nombre) => `<div class="ib">${icono(nombre, C.marfil, 1.9)}</div>`;
const pill = (t) => `<span class="pill">${esc(t)}</span>`;
const bur = (t) => `<div class="bur"><div class="co">${icono("corazon", C.rosa, 2)}</div>${esc(t)}</div>`;
const minDe = (n) => MOMENTOS.find((m) => m.n === n).min;
const nombreDe = (n) => MOMENTOS.find((m) => m.n === n).nombre;
const ICO_MOM = { 1: "nota", 2: "calendario", 3: "cartas", 4: "bombilla", 5: "charla", 6: "loto" };
const momento = (n, cuerpo, titulo = nombreDe(n)) =>
  `<div class="mom">${ib(ICO_MOM[n])}<div class="mc"><div class="mh"><h2>${esc(titulo)}</h2>${pill(minDe(n) + " min")}</div>${cuerpo}</div></div>`;
const panel = (titulo, icon, cuerpo, sub = "", clase = "") =>
  `<div class="panel ${clase}"><h3><span class="ic">${icono(icon, C.rosa, 1.9)}</span>${esc(titulo)}${sub ? `<span class="sub">${esc(sub)}</span>` : ""}</h3>${cuerpo}</div>`;

const ILUS_TEMA = { Infancia: "trompo", Comida: "mate", Sonidos: "radio", "Caras y escenas": "cine", "Usar dinero": "almacen", "Juegos de palabras": "pizarron", Noticias: "kiosco", Crear: "cartuchera" };

// ----------------------------------------------------------------------------- un encuentro: 6 páginas (A|B, C|D, E|F)
function paginasEncuentro(e, n0, extra = {}) {
  const out = [];
  const sem = SEMANAS.find((s) => s.encuentros.includes(e.n));
  let n = n0;
  const o = { tab: e.n };
  const oF = { tab: e.n, fondo: true };

  // A · preparación
  out.push(pag(n++, `
<div class="chips"><span class="chip">Encuentro ${e.n} de 8</span><span class="chip o">Semana ${sem.n} · ${esc(sem.nombre)}</span></div>
<div class="cabeza"><div class="tx"><h1 class="tema">${esc(e.tema)}</h1><div class="titulo">${esc(e.titulo)}</div><p class="idea">${esc(e.idea)}</p></div><div class="ilus">${ILUS[ILUS_TEMA[e.tema]]}</div></div>
${adorno()}
${panel("Necesitamos", "check", `<ul class="chk">${li(e.materiales)}</ul>`, "", "v")}
${panel("Antes de empezar", "reloj", `<ul class="chk">${li(e.antes)}</ul>`, "Para vos · 5 min")}`, oF));

  // B · canción y día
  const hoy = `<div class="hoy-et"><span>Día</span><span>Número</span><span class="m">Mes</span></div><div class="hoy"><div></div><div></div><div class="m"></div></div>`;
  out.push(pag(n++, `
${momento(1, `<p class="cons">${esc(e.bienvenida.texto)}</p><p class="canc"><b>Para elegir:</b> ${e.bienvenida.canciones.map((c) => `«${esc(c)}»`).join(", ")}.</p>${bur(e.bienvenida.guion.replace(/[«»]/g, ""))}`)}
${momento(2, `<p class="cons">${esc(e.queDia.texto)}</p>${hoy}${bur(e.queDia.guion.replace(/[«»]/g, ""))}<p class="nota">${esc(e.queDia.siSeTraba)}</p>`)}`, oF));

  // C · actividad principal
  const p = e.principal;
  const palma = (x) => [...x].filter((c) => c !== " ").map((c) => `<i class="pal ${c === "●" ? "f" : ""}"></i>`).join("");
  const palmas = p.palmas
    ? `<div class="palmas"><div style="display:flex;flex-wrap:wrap;gap:3mm 11mm">${p.palmas.map((x) => `<span class="grupo-pal">${palma(x)}</span>`).join("")}</div><div style="margin-top:2mm;display:flex;gap:7mm;align-items:center;color:var(--rosa);font-weight:700"><span style="display:flex;gap:2mm;align-items:center"><i class="pal f"></i>palma fuerte</span><span style="display:flex;gap:2mm;align-items:center"><i class="pal"></i>palma suave</span></div></div>`
    : "";
  out.push(pag(n++, `
${momento(3, `<div class="titulo-act">${esc(p.titulo)}</div>
<div class="pasos ${p.pasos.length >= 4 ? "c" : ""}">${p.pasos.map((s, i) => `<div class="paso"><div class="pl">${"abcdef"[i]}</div><div class="pt">${esc(s.texto)}${pill(s.min + " min")}</div></div>`).join("")}</div>${palmas}
${bur(p.guion.map((g) => g.replace(/[«»]/g, "")).join("  ·  "))}`)}
${panel("Si se traba", "brote", `<ul class="chk">${li(p.siSeTraba)}</ul>${p.cuidado ? `<p class="nota" style="color:var(--rosa);margin-top:2mm">${esc(p.cuidado)}</p>` : ""}`, "", "v")}`, o));

  // C2 · material de juego (solo el encuentro 6)
  if (e.extra) {
    out.push(pag(n++, `
<div class="chips"><span class="chip">Encuentro ${e.n}</span><span class="chip o">${esc(e.tema)}</span></div>
<h1 class="gr">${esc(e.extra.titulo)}</h1>
<div class="extra">${e.extra.bloques.map((b) => panel(b.titulo, "estrella", `<ul class="pts" style="list-style:none">${b.items.map((it, i) => `<li style="margin-bottom:2mm"><span class="cons">${esc(it)}</span> <i style="font-family:Fraunces;color:var(--rosa);font-size:17pt">${esc(b.respuestas[i])}</i></li>`).join("")}</ul>`, "", b.titulo.startsWith("Adiv") ? "v" : "")).join("")}</div>`, o));
  }

  // D · razonamiento
  const sinRaya = (t) => esc(t).replace(/:\s*_{2,}/g, ":").replace(/,?\s*_{2,}/g, ",");
  const item = (it) =>
    it.serie
      ? `<div class="fila"><span class="l">Completá:</span><span class="s">${sinRaya(it.serie)}</span><span class="b"></span></div>`
      : `<div class="prob"><div class="l">${sinRaya(it.consigna)}</div><div class="renglon"></div></div>`;
  out.push(pag(n++, `
${momento(4, `<p class="cons" style="margin-bottom:1mm">${esc(CUADERNO.razonamientoIntro)}</p>`)}
${NIVELES.map((nv) => `<div class="niv n${nv.puntos}"><div class="nh"><h3>${esc(nv.nombre)}</h3><div class="fl">${Array.from({ length: nv.puntos }, () => icono("loto", C.rosa, 1.9)).join("")}</div></div>${e.razonamiento[nv.clave].map(item).join("")}</div>`).join("")}`, o));

  // E · charla de cierre y registro
  out.push(pag(n++, `
${momento(5, `<div class="cita"><div class="ic">${icono("charla", C.rosa, 1.8)}</div><div class="q" style="padding-right:14mm">${esc(e.cierre.pregunta)}</div></div>${bur(e.cierre.guion.replace(/[«»]/g, ""))}`)}
${panel(CUADERNO.comoMeSenti, "corazon", `<div class="renglon"></div><div class="renglon"></div><div class="renglon"></div>`, "", "")}
<p class="cons" style="margin-top:1mm">${esc(CUADERNO.cierreMarcar)}</p>
<div class="cinta">${icono(e.pie.icono, C.marfil, 1.8)}<span>${esc(e.pie.texto)}</span></div>`, oF));

  // E2 · hoja de notas (solo si hace falta para que el mandala caiga en página impar)
  if (extra.notasAntesMandala) out.push(pagNotas(n++, o));

  // F · mandala (página impar: va del lado del frente de la hoja)
  const mandalaN = n;
  out.push(paginaMandala(n++, e, o));
  return { paginas: out, siguiente: n, mandala: mandalaN };
}

function paginaMandala(n, e, o) {
  const r = RECT_MANDALA;
  const marco = `<div class="marco-m" style="left:${r.x0 - 4}mm;top:${r.y0 - 4}mm;width:${r.x1 - r.x0 + 8}mm;height:${r.y1 - r.y0 + 8}mm;"></div>`;
  const sin = globalThis.__SIN_MARCADOR;
  const marcador = sin ? "" : `<div style="position:absolute;left:${r.x0}mm;top:${r.y0}mm;width:${r.x1 - r.x0}mm;height:${r.y1 - r.y0}mm;display:flex;align-items:center;justify-content:center;text-align:center"><div><div class="fr" style="font-size:26pt">${esc(CUADERNO.mandalaMarcador)}</div><p style="margin-top:3mm;font-size:17pt">Página del libro de mandalas de ${esc(FIRMA)}.</p></div></div>`;
  const m = margenes(n);
  return `<section class="pagina">${lenguetas({ W, H, S, esVerso: m.v, actual: e.n })}
<div class="zona" style="${zona(n)}"><div class="chips"><span class="chip">Encuentro ${e.n} · ${esc(e.tema)}</span></div><h1 class="gr" style="margin-bottom:0">${esc(CUADERNO.mandalaTitulo)}</h1></div>
${marco}${marcador}
<div class="pf" style="left:${m.izq}mm;right:${m.der}mm;bottom:${S + 8}mm;justify-content:flex-end;flex-direction:row-reverse"><div class="pnum">${n}</div><div class="pdots">${avance(e.n)}</div></div></section>`;
}

function pagNotas(n, o = {}) {
  return pag(n, `<div class="chips"><span class="chip">Notas</span></div><h1 class="gr">Mis notas</h1>${adorno()}<div class="renglones" style="height:192mm"></div>`, o);
}
function pagDorsoBlanco(n) {
  return pag(n, `<div style="position:absolute;left:0;right:0;bottom:0;text-align:center;color:var(--rosa);font-size:17pt">Dorso en blanco, para poder recortar.</div>`);
}

// ----------------------------------------------------------------------------- páginas especiales
function portada() {
  const P = CUADERNO.portada;
  return `<section class="pagina sobre-rosa portada" style="background:var(--rosa)">
<div class="marco"></div>
<div class="zona" style="left:${S + 18}mm;right:${S + 18}mm;top:${S + 20}mm;bottom:${S + 18}mm;text-align:center;overflow:visible;color:var(--marfil)">
<div class="kick" style="color:var(--marfil);letter-spacing:.24em">${esc(P.tipo)}</div>
<h1 style="font-size:82pt;line-height:.98;margin-top:7mm;letter-spacing:-.01em;color:var(--marfil)">La hora<br>del té</h1>
<div class="fr" style="font-style:italic;font-weight:400;font-size:28pt;color:var(--velado);margin-top:4mm">${esc(P.bajada)}</div>
<div style="width:166mm;margin:3mm auto 0">${escenaTe({ sobreRosa: true })}</div>
<div style="position:absolute;left:0;right:0;bottom:0">
<div class="kick" style="color:var(--velado)">${esc(P.marca)}</div>
<div class="fr" style="font-size:27pt;margin-top:2mm;color:var(--marfil)">${esc(FIRMA)}</div>
<div class="kick" style="color:var(--velado);margin-top:1mm;font-size:16pt">${esc(MARCA)}</div></div></div>
<div class="sello" style="right:${S + 17}mm;top:${S + 118}mm"><b>8</b><span>encuentros<br>de 45 min</span></div></section>`;
}

function guarda(n) {
  return pag(n, `
<div style="text-align:center">
<div class="kick">Este cuaderno es de</div>
<div style="width:112mm;margin:6mm auto 8mm">${escenaTe({ sobreRosa: false })}</div>
${["Mamá", "Hija"].map((q) => `<div style="text-align:left;margin-bottom:1mm"><b style="color:var(--rosa);font-size:18pt">${q}</b><div class="renglon"></div></div>`).join("")}
<div style="text-align:left;margin-top:3mm"><b style="color:var(--rosa);font-size:18pt">Empezamos el</b><div class="renglon"></div></div>
<div style="text-align:left;margin-top:3mm"><b style="color:var(--rosa);font-size:18pt">Nuestro té favorito</b><div class="renglon"></div></div></div>`);
}

function bienvenida(n) {
  const B = CUADERNO.bienvenida;
  return pag(n, `
<div class="chips"><span class="chip">${esc(B.kick)}</span></div>
<h1 class="gr">${esc(B.titulo)}</h1>
<p class="cons" style="margin-bottom:5mm">${esc(B.intro)}</p>
<div class="grid2" style="margin-bottom:5mm">
 <div class="card"><div class="ic">${icono("estrella", C.marfil, 1.9)}</div><h3>${esc(B.roles[0].quien)}</h3><p>${esc(B.roles[0].que)}</p></div>
 <div class="card v"><div class="ic">${icono("corazon", C.marfil, 1.9)}</div><h3>${esc(B.roles[1].quien)}</h3><p>${esc(B.roles[1].que)}</p></div>
</div>
<h2 style="font-size:25pt;margin-bottom:3mm">${esc(B.comoUsarloTitulo)}</h2>
<div class="pasos">${B.comoUsarlo.map((t, i) => `<div class="paso" style="padding-bottom:3.4mm"><div class="pl">${i + 1}</div><div class="pt">${esc(t)}</div></div>`).join("")}</div>
<p class="fr" style="font-style:italic;font-weight:400;color:var(--rosa);font-size:22pt;line-height:1.25;margin-top:2mm">${esc(B.reglas)}</p>`, { fondo: true });
}

function semanas(n) {
  const R = CUADERNO.ritmo;
  return pag(n, `
<div class="chips"><span class="chip">${esc(R.kick)}</span></div>
<h1 class="gr">${esc(R.titulo)}</h1>
<p class="cons" style="margin-bottom:3mm">${esc(R.bajada)}</p>
${R.filas.map((f) => `<div class="sem-card"><div class="sem-n"><b>${f.semana}</b></div><div class="sem-r"><h3>Semana ${f.semana}<i>${esc(f.nombre)}</i></h3>
<div class="fl-r">${icono("celular", C.rosa, 1.8)}<span><b>${esc(R.cols.app)}:</b> ${esc(R.app)}</span></div>
<div class="fl-r">${icono("taza", C.rosa, 1.8)}<span><b>${esc(R.cols.encuentros)}:</b> ${SEMANAS[f.semana - 1].encuentros.map((i) => `${i}. ${esc(encuentros[i - 1].tema)}`).join(" · ")}</span></div>
<div class="fl-r">${icono("caminar", C.rosa, 1.8)}<span><b>${esc(R.cols.movimiento)}:</b> ${esc(R.mov)}</span></div></div></div>`).join("")}
<p style="font-size:17pt;line-height:1.3;margin-top:1mm">${esc(R.nota)}</p>`);
}

function comoEs(n) {
  const E = CUADERNO.encuentro;
  return pag(n, `
<div class="chips"><span class="chip">${esc(E.kick)}</span></div>
<h1 class="gr">${esc(E.titulo)}</h1>
<p class="cons" style="margin-bottom:3mm">${esc(E.bajada)}</p>
<div style="position:relative;width:58mm;height:58mm;margin:0 auto 5mm"><div style="position:absolute;inset:0">${anilloMomentos(MOMENTOS)}</div>
<div style="position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center"><div class="fr" style="font-size:34pt;line-height:1">45</div><div style="font-weight:700;color:var(--rosa);font-size:16pt;line-height:1.1">minutos</div></div></div>
${MOMENTOS.map((m, i) => `<div class="leg">${ib(ICO_MOM[m.n])}<div class="t"><h3>${esc(m.nombre)}${pill(m.min + " min")}</h3>${esc(E.momentos[i])}</div></div>`).join("")}`, { fondo: true });
}

function reglas(n) {
  const E = CUADERNO.encuentro, B = CUADERNO.bienvenida;
  const ics = ["ojo", "lapiz", "estrella", "brote"];
  return pag(n, `
<div class="chips"><span class="chip">En todos los encuentros</span></div>
<h1 class="gr">${esc(E.reglasTitulo)}</h1>
<div class="grid2" style="margin-bottom:6mm">${E.reglas.map((r, i) => `<div class="card ${i % 3 === 0 ? "" : "v"}" style="min-height:44mm"><div class="ic">${icono(ics[i], C.marfil, 1.9)}</div><h3 style="font-size:21pt">${esc(r)}</h3></div>`).join("")}</div>
<div style="background:var(--rosa);color:var(--marfil);border-radius:6mm;padding:6mm 8mm"><h3 style="font-size:24pt;margin-bottom:2mm;color:var(--marfil)">${esc(B.importante)}</h3><p style="font-size:19pt;line-height:1.3">${esc(AVISO)}</p></div>`, { fondo: true });
}

function indice(n, pags) {
  const filas = [];
  SEMANAS.forEach((s) => {
    filas.push(`<div class="ind sem"><span>Semana ${s.n}</span><span class="fr" style="font-style:italic;font-weight:400;color:var(--rosa)">${esc(s.nombre)}</span></div>`);
    s.encuentros.forEach((i) => filas.push(`<div class="ind"><span>Encuentro ${i} · ${esc(encuentros[i - 1].tema)}</span><span class="p"></span><span class="n">${pags.e[i] ?? ""}</span></div>`));
    const pa = PAUSAS.find((x) => x.semana === s.n);
    filas.push(`<div class="ind"><span style="color:var(--rosa)">Pausa de vida · ${esc(pa.titulo.length > 24 ? pa.titulo.slice(0, 24).replace(/\s+\S*$/, "") + "…" : pa.titulo)}</span><span class="p"></span><span class="n">${pags.p[s.n] ?? ""}</span></div>`);
  });
  filas.push(`<div class="ind sem"><span>Al final</span></div>`);
  [["Diploma", pags.diploma], ["Y ahora, ¿qué sigue?", pags.final], ["Respuestas posibles", pags.respuestas], ["Monedas y billetes de juguete", pags.dinero]].forEach(([t, p]) =>
    filas.push(`<div class="ind"><span>${esc(t)}</span><span class="p"></span><span class="n">${p ?? ""}</span></div>`));
  return pag(n, `<div class="chips"><span class="chip">Índice</span></div><h1 class="gr">Lo que vamos a hacer</h1>${filas.join("")}`);
}

function pausa(p, n) {
  const pasos = p.pasos ? `<div class="pausa-tx" style="margin-bottom:3mm">${p.pasos.map((x, i) => `<div style="display:flex;gap:4mm;margin-bottom:1.6mm"><b class="fr" style="font-size:20pt">${i + 1}</b><span>${esc(x)}</span></div>`).join("")}</div>` : "";
  const controles = p.controles ? `<div class="ctl">${p.controles.map((c) => `<div><h3>${esc(c.que)}</h3><p>${esc(c.quien)}</p></div>`).join("")}</div>` : "";
  const campos = (p.campos || []).map((c) => `<div style="margin-bottom:1mm"><b class="et" style="font-size:18pt">${esc(c)}</b><div class="renglon"></div></div>`).join("");
  const IC = { 1: "caminar", 2: "respirar", 3: "taza", 4: "ojo" };
  return pag(n, `
<div class="kick" style="color:var(--marfil)">Pausa de vida · Semana ${p.semana}</div>
<div class="pausa-ic">${icono(IC[p.semana], C.rosa, 1.6)}</div>
<h1 style="font-size:38pt;line-height:1.05;margin-bottom:4mm;color:var(--marfil)">${esc(p.titulo)}</h1>
<p class="pausa-tx">${esc(p.texto)}</p>${pasos}${controles}
${p.pregunta ? `<p class="fr" style="font-size:21pt;font-style:italic;font-weight:400;margin-bottom:4mm">${esc(p.pregunta)}</p>` : ""}
${campos}
${p.nota ? `<div class="pausa-nota">${esc(p.nota)}</div>` : ""}`, { clase: "sobre-rosa", fondo: "rosa" });
}

function registro(sem, n) {
  const R = CUADERNO.registro;
  const filas = [["encuentro", "taza", "Encuentro"], ["movimiento", "caminar", "Movimiento"], ["app", "celular", "App"]];
  return pag(n, `
<div class="chips"><span class="chip">${esc(R.kick)}</span><span class="chip o">Semana ${sem.n} · ${esc(sem.nombre)}</span></div>
<h1 class="gr">Mi semana ${sem.n}</h1>
<p class="cons" style="margin-bottom:4mm">${esc(R.bajada)}</p>
<table class="reg"><tr><th></th>${["L", "M", "M", "J", "V", "S", "D"].map((d) => `<th>${d}</th>`).join("")}</tr>
${filas.map(([k, ic, t]) => `<tr><td class="e"><div>${icono(ic, C.rosa, 1.8)}<span>${t}</span></div></td>${[1, 2, 3, 4, 5, 6, 7].map(() => `<td><span class="cir"></span></td>`).join("")}</tr>`).join("")}</table>
<div style="margin-top:7mm"><b style="color:var(--rosa);font-size:19pt">Una cosa linda de esta semana</b><div class="renglon"></div><div class="renglon"></div></div>
<div style="margin-top:3mm"><b style="color:var(--rosa);font-size:19pt">Lo que quiero repetir</b><div class="renglon"></div></div>`);
}

function diploma(n) {
  const D = CUADERNO.diploma;
  const marco = `<div class="marco-m" style="left:${S + 14}mm;top:${S + 14}mm;right:${S + 14}mm;bottom:${S + 14}mm;"></div>`;
  return `<section class="pagina">${marco}<div class="zona" style="left:${S + 26}mm;right:${S + 26}mm;top:${S + 26}mm;bottom:${S + 26}mm;text-align:center;overflow:visible">
<div class="kick">${esc(D.kick)}</div>
<div style="width:96mm;margin:4mm auto 4mm">${escenaTe({ sobreRosa: false })}</div>
<h1 style="font-size:42pt;line-height:1.02;margin-top:3mm">${esc(D.titulo)}</h1>
<p class="titulo" style="margin:4mm auto 0;max-width:120mm;font-size:22pt">${esc(D.texto)}</p>
<div style="display:flex;gap:10mm;margin-top:14mm;text-align:left"><div style="flex:1"><div class="renglon"></div><b style="color:var(--rosa)">${esc(D.mama)}</b></div><div style="flex:1"><div class="renglon"></div><b style="color:var(--rosa)">${esc(D.hija)}</b></div></div>
<div style="width:70mm;margin:5mm auto 0;text-align:left"><div class="renglon"></div><b style="color:var(--rosa)">${esc(D.fecha)}</b></div>
<div style="position:absolute;left:0;right:0;bottom:0"><div class="fr" style="font-size:22pt">${esc(FIRMA)}</div><div class="kick" style="margin-top:1mm">${esc(MARCA)}</div></div></div></section>`;
}

function final(n) {
  const F = CUADERNO.final;
  const ics = ["celular", "taza", "caminar", "charla"];
  return pag(n, `
<div class="chips"><span class="chip">${esc(F.kick)}</span></div>
<h1 class="gr">${esc(F.titulo)}</h1>
<p class="cons" style="margin-bottom:5mm">${esc(F.intro)}</p>
${F.seguir.map((t, i) => `<div class="leg">${ib(ics[i])}<div class="t" style="font-size:18pt">${esc(t)}</div></div>`).join("")}
<div style="margin-top:5mm">${F.preguntas.map((q) => `<div style="margin-bottom:1mm"><b style="color:var(--rosa);font-size:19pt">${esc(q)}</b><div class="renglon"></div></div>`).join("")}</div>`);
}

function respuestas(lista, n0) {
  const out = [];
  for (let i = 0; i < lista.length; i += 3) {
    const grupo = lista.slice(i, i + 3), R = CUADERNO.respuestas;
    out.push(pag(n0 + out.length, `
<div class="chips"><span class="chip">${esc(R.kick)}</span></div>
<h1 class="gr" style="font-size:34pt">${esc(R.titulo)}${i ? ` (${i / 3 + 1})` : ""}</h1>${i === 0 ? `<p style="font-size:17pt;line-height:1.3;margin-bottom:4mm">${esc(R.intro)}</p>` : ""}
<div class="resp">${grupo.map((e) => `<div class="e"><h3>Encuentro ${e.n} · ${esc(e.tema)}</h3>${NIVELES.map((nv) => `<div class="r"><b>${esc(nv.nombre)}</b><span>${e.razonamiento[nv.clave].map((x, k) => `${"ab"[k]}) ${esc(x.respuesta)}`).join("   ")}</span></div>`).join("")}</div>`).join("")}</div>`));
  }
  return out;
}

const VALORES_BILLETES = [100, 100, 200, 200, 500, 500, 1000, 1000, 1000, 2000, 2000, 5000];
const VALORES_MONEDAS = [5, 10, 10, 20, 20, 50, 50, 100, 100, 100, 200, 200];
const pesos = (v) => "$" + String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ".");
function paginasDinero(n) {
  const D = CUADERNO.dinero;
  const billetes = VALORES_BILLETES.map((v, i) => {
    const x = (i % 2) * 89, y = Math.floor(i / 2) * 36;
    return `<div class="billete" style="left:${x}mm;top:${y}mm"><div class="in"></div><div class="lo">${loto(C.rosa, 0.9)}</div><div class="v">${pesos(v)}</div><div class="t">La hora del té</div><div class="j">${D.leyenda}</div></div>`;
  }).join("");
  const monedas = VALORES_MONEDAS.map((v, i) => {
    const x = (i % 3) * 58, y = Math.floor(i / 3) * 52;
    return `<div class="moneda" style="left:${x}mm;top:${y}mm"><div class="in"></div><div class="v">${pesos(v)}</div><div class="j">DE<br>JUGUETE</div></div>`;
  }).join("");
  const cab = (t) => `<div class="chips"><span class="chip">${esc(D.kick)} · ${t}</span></div><h1 class="gr" style="font-size:30pt;margin-bottom:1mm">${esc(D.titulo)}</h1><p style="margin-bottom:4mm;font-size:17pt">${esc(D.bajada)}</p>`;
  return [
    pag(n, `${cab("billetes")}<div style="position:relative;height:212mm;margin-left:1mm">${billetes}</div>`),
    pag(n + 2, `${cab("monedas")}<div style="position:relative;height:212mm;margin-left:3mm">${monedas}</div>`),
  ];
}

function contratapa(n) {
  return `<section class="pagina sobre-rosa" style="background:var(--rosa)">
<div class="portada"><div class="marco"></div></div>
<div class="zona" style="left:${S + 22}mm;right:${S + 22}mm;top:${S + 26}mm;bottom:${S + 22}mm;text-align:center;overflow:visible;color:var(--marfil)">
<div style="width:92mm;margin:0 auto">${loto(C.rosaLinea, 1.2, C.rosaSobre)}</div>
<h1 style="font-size:36pt;line-height:1.08;margin:8mm 0 4mm;color:var(--marfil)">Un cuaderno para estar juntas</h1>
<p style="font-size:20pt;line-height:1.32;margin-bottom:6mm">${esc(CUADERNO.bienvenida.intro)}</p>
<p class="fr" style="font-style:italic;font-weight:400;font-size:23pt;color:var(--velado);line-height:1.25">${esc(CUADERNO.contratapa.texto)}</p>
<div style="position:absolute;left:0;right:0;bottom:0"><p style="font-size:16pt;line-height:1.3;margin-bottom:6mm">${esc(AVISO)}</p><div class="fr" style="font-size:24pt;color:var(--marfil)">${esc(FIRMA)}</div><div class="kick" style="color:var(--velado);margin-top:1mm">${esc(MARCA)}</div></div></div></section>`;
}

// ----------------------------------------------------------------------------- armado del libro
function construir(pagsPrevias) {
  const pg = [];
  const ind = { e: {}, p: {}, diploma: 0, final: 0, respuestas: 0, dinero: 0 };
  const slots = [];
  let n = 1;
  const push = (html, k = 1) => { pg.push(html); n += k; };

  push(portada());                      // 1
  push(guarda(n));                      // 2
  push(bienvenida(n));                  // 3
  push(semanas(n));                     // 4
  push(comoEs(n));                      // 5
  push(reglas(n));                      // 6
  push(indice(n, pagsPrevias || ind));  // 7
  for (const e of encuentros) {
    ind.e[e.n] = n;
    const r = paginasEncuentro(e, n, { notasAntesMandala: !!e.extra });
    pg.push(...r.paginas);
    slots.push(r.mandala);
    n = r.siguiente;
    if (e.n % 2 === 0) {
      const sem = SEMANAS[e.semana - 1];
      ind.p[sem.n] = n;
      push(pausa(PAUSAS.find((x) => x.semana === sem.n), n));
      push(registro(sem, n));
    }
  }
  ind.diploma = n; push(diploma(n));
  ind.final = n; push(final(n));
  ind.respuestas = n;
  const resp = respuestas(encuentros, n); pg.push(...resp); n += resp.length;
  // Recortables: cada uno va en el frente de una hoja (página impar) con el dorso en blanco.
  if (n % 2 === 0) push(pagNotas(n));
  ind.dinero = n;
  const d = paginasDinero(n);
  pg.push(d[0], pagDorsoBlanco(n + 1), d[1], pagDorsoBlanco(n + 3)); n += 4;
  if (n % 2 === 1) push(pagNotas(n));   // la contratapa tiene que ser par
  push(contratapa(n));
  return { pg, ind, slots };
}

export function armarCuaderno(modo = "completo", opciones = {}) {
  globalThis.__SIN_MARCADOR = !!opciones.sinMarcador;
  const primera = construir(null);
  const { pg, slots } = construir(primera.ind);
  return {
    nombre: opciones.sinMarcador ? "cuaderno-base-para-mandalas" : "cuaderno-la-hora-del-te",
    titulo: "La hora del té · Cuaderno",
    W, H, paginas: pg, css: CSS_CUADERNO, sangrado: S,
    slots,
    rectMandala: RECT_MANDALA,
  };
}
