// Cuaderno "La hora del té": A4 vertical espiralado (20 mm libres del lado del espiral).
import {
  SANGRADO as S, ROSA, MARFIL, esc,
} from "./base.mjs";
import {
  encuentros, SEMANAS, MOMENTOS, NIVELES, AVISO, FIRMA, MARCA, PRODUCTO,
} from "../contenido/encuentros.mjs";
import { CUADERNO, PAUSAS } from "../contenido/generales.mjs";
import { lotoDecorativo, ICONOS } from "./graficos.mjs";

export const CUAD = { W: 210 + 2 * S, H: 297 + 2 * S };
const ZONA = `left:${S + 20}mm;top:${S + 13}mm;right:${S + 13}mm;bottom:${S + 18}mm;`;

export const CSS_CUADERNO = `
h1.tema{font-size:44pt;line-height:1.02;margin:1mm 0 1mm;}
h1.gr{font-size:36pt;line-height:1.08;margin:1mm 0 3mm;}
.titulo{font-family:'Fraunces',serif;font-style:italic;font-weight:400;font-size:22pt;color:var(--rosa);line-height:1.15;}
.filete{height:.4mm;background:var(--rosa);margin:3mm 0 4mm;}
.parte{display:flex;gap:5mm;margin-bottom:5mm;}
.pc{flex:1;}
.pc h2{font-size:21pt;line-height:1.12;margin-bottom:1.5mm;}
.cons{font-size:18pt;line-height:1.3;}
ol.pasos{list-style:none;counter-reset:p;margin-bottom:3mm;}
ol.pasos li{counter-increment:p;position:relative;padding-left:10mm;margin-bottom:3mm;font-size:18pt;line-height:1.3;}
ol.pasos li::before{content:counter(p,lower-alpha);position:absolute;left:0;top:-.5mm;font-family:'Fraunces',serif;font-weight:600;color:var(--rosa);font-size:21pt;}
ol.pasos li b{color:var(--rosa);font-size:16pt;white-space:nowrap;}
.ver{border:.4mm solid var(--rosa);border-radius:3mm;padding:3mm 5mm 1mm;margin-bottom:4mm;}
.ver h3{font-size:20pt;display:flex;align-items:center;gap:3mm;margin-bottom:1mm;}
.dots{display:inline-flex;gap:1.6mm;}
.dots i{display:block;width:4mm;height:4mm;border-radius:50%;border:.5mm solid var(--rosa);}
.dots i.on{background:var(--rosa);}
.kick.sep{margin-bottom:4mm;}
.ej{margin-bottom:1mm;}
.ej .l{font-size:18pt;line-height:1.3;}
.ej .s{font-size:22pt;font-weight:700;letter-spacing:.02em;}
.pie{position:absolute;left:0;right:0;bottom:0;display:flex;gap:4mm;align-items:center;border-top:.4mm solid var(--rosa);padding-top:3mm;font-size:18pt;}
.pie svg{width:11mm;height:11mm;flex:none;}
.slot{position:absolute;left:0;right:0;top:34mm;bottom:0;border:.5mm dashed var(--rosa);border-radius:4mm;display:flex;align-items:center;justify-content:center;text-align:center;padding:10mm;}
.cuad2{display:grid;grid-template-columns:1fr 1fr;gap:4mm;}
table.reg{width:100%;border-collapse:collapse;}
table.reg th{font-family:'Fraunces',serif;font-weight:600;font-size:19pt;text-align:center;padding-bottom:2mm;border-bottom:.4mm solid var(--rosa);}
table.reg td{height:30mm;border-top:.3mm solid var(--rosa);text-align:center;vertical-align:middle;}
table.reg td.s{font-family:'Fraunces',serif;font-weight:600;font-size:19pt;text-align:left;}
.cir{display:inline-block;width:11mm;height:11mm;border-radius:50%;border:.5mm solid var(--rosa);margin:0 1.2mm;}
.resp .e{margin-bottom:4mm;}
.resp .e h3{font-size:19pt;margin-bottom:.8mm;}
.resp .e div{font-size:16pt;line-height:1.3;margin-bottom:.6mm;}
.billete{position:absolute;width:85mm;height:40mm;border:.5mm solid var(--rosa);border-radius:2.5mm;background:var(--marfil);}
.billete .in{position:absolute;inset:2mm;border:.3mm solid var(--rosa);border-radius:1.5mm;}
.billete .lo{position:absolute;left:3mm;top:3mm;width:28mm;height:28mm;}
.billete .v{position:absolute;right:5mm;top:3mm;font-family:'Fraunces',serif;font-weight:600;font-size:30pt;color:var(--cacao);}
.billete .t{position:absolute;right:5mm;top:19mm;font-size:16pt;font-weight:700;color:var(--rosa);text-align:right;line-height:1.1;}
.billete .j{position:absolute;left:0;right:0;bottom:3mm;text-align:center;font-size:16pt;font-weight:700;letter-spacing:.12em;color:var(--rosa);}
.moneda{position:absolute;width:38mm;height:38mm;border:.5mm solid var(--rosa);border-radius:50%;background:var(--marfil);text-align:center;}
.moneda .in{position:absolute;inset:1.8mm;border:.3mm solid var(--rosa);border-radius:50%;}
.moneda .v{position:absolute;left:0;right:0;top:7mm;font-family:'Fraunces',serif;font-weight:600;font-size:26pt;color:var(--cacao);}
.moneda .j{position:absolute;left:0;right:0;top:21mm;font-size:16pt;font-weight:700;color:var(--rosa);line-height:1.05;}
`;

const folio = (n) =>
  `<div class="folio" style="left:${S + 20}mm;right:${S + 13}mm;bottom:${S + 8}mm;"><span>La hora del té</span><span>${n}</span></div>`;
const pagina = (cuerpo, n, extra = "") =>
  `<section class="pagina"><div class="zona" style="${ZONA}${extra}">${cuerpo}</div>${n ? folio(n) : ""}</section>`;
const li = (a) => a.map((x) => `<li>${esc(x)}</li>`).join("");
const dots = (k) => `<span class="dots">${[1, 2, 3].map((i) => `<i class="${i <= k ? "on" : ""}"></i>`).join("")}</span>`;
const parte = (n, titulo, min, cuerpo) =>
  `<div class="parte"><div class="circ">${n}</div><div class="pc"><h2>${esc(titulo)}<span class="min">${min} min</span></h2>${cuerpo}</div></div>`;
const minDe = (n) => MOMENTOS.find((m) => m.n === n).min;
const nombreDe = (n) => MOMENTOS.find((m) => m.n === n).nombre;

// ---- Un encuentro: A (preparación y canción), B (día y actividad), [extra], C (razonamiento), D (cierre y mandala), E (mandala)
function paginasEncuentro(e, num) {
  const out = [];
  const sem = e.semana;

  // A
  out.push(
    pagina(
      `<div class="kick">Encuentro ${e.n} · Semana ${sem}</div>
<h1 class="tema">${esc(e.tema)}</h1>
<div class="titulo">${esc(e.titulo)}</div>
<div class="filete"></div>
<div class="caja" style="margin-bottom:4mm"><h3>Necesitamos</h3><ul class="pts">${li(e.materiales)}</ul></div>
<div class="caja" style="margin-bottom:6mm"><h3>Antes de empezar <span class="rosa" style="font-family:Manrope;font-weight:600;font-size:16pt;margin-left:2mm">Para vos · 5 minutos</span></h3><ul class="pts">${li(e.antes)}</ul></div>
${parte(1, nombreDe(1), minDe(1), `<p class="cons">${esc(e.bienvenida.texto)}</p>
<p style="margin-top:2mm"><b class="rosa">Para elegir:</b> ${e.bienvenida.canciones.map((c) => `«${esc(c)}»`).join(", ")}.</p>
<p class="guion" style="margin-top:2mm">${esc(e.bienvenida.guion)}</p>`)}`,
      num,
    ),
  );

  // B
  const p = e.principal;
  const palmas = p.palmas
    ? `<div class="caja" style="margin:2mm 0 3mm;padding:2.5mm 5mm"><div style="display:flex;flex-wrap:wrap;gap:2mm 9mm;font-size:22pt;letter-spacing:.12em;font-weight:700">${p.palmas.map((x) => `<span>${x}</span>`).join("")}</div><div style="font-size:16pt;margin-top:1mm" class="rosa">${esc(p.palmasRef)}</div></div>`
    : "";
  out.push(
    pagina(
      `${parte(2, nombreDe(2), minDe(2), `<p class="cons">${esc(e.queDia.texto)}</p>
<p class="guion" style="margin-top:1.5mm">${esc(e.queDia.guion)}</p>
<p style="margin-top:1.5mm">${esc(e.queDia.siSeTraba)}</p>`)}
<div class="parte" style="margin-bottom:2mm"><div class="circ">3</div><div class="pc"><h2>${esc(nombreDe(3))}<span class="min">${minDe(3)} min</span></h2>
<div class="titulo" style="font-size:20pt;margin-bottom:2.5mm">${esc(p.titulo)}</div>
<ol class="pasos">${p.pasos.map((s) => `<li>${esc(s.texto)} <b>${s.min} min</b></li>`).join("")}</ol>${palmas}
<p class="guion">${p.guion.join("  ")}</p></div></div>
<div class="caja" style="margin-top:3mm"><h3>Si se traba</h3><ul class="pts">${li(p.siSeTraba)}</ul>${p.cuidado ? `<p class="rosa" style="margin-top:1.5mm">${esc(p.cuidado)}</p>` : ""}</div>`,
      num + 1,
    ),
  );
  let k = num + 2;

  // Extra (material de juego)
  if (e.extra) {
    out.push(
      pagina(
        `<div class="kick">Encuentro ${e.n} · ${esc(e.tema)}</div>
<h1 class="gr">${esc(e.extra.titulo)}</h1>
${e.extra.bloques
  .map(
    (b) => `<div style="margin-bottom:5mm"><h2 style="font-size:20pt;margin-bottom:1.5mm">${esc(b.titulo)}</h2>
<ul class="pts">${b.items.map((it, i) => `<li><span class="cons">${esc(it)}</span> <span class="guion">${esc(b.respuestas[i])}</span></li>`).join("")}</ul></div>`,
  )
  .join("")}`,
        k,
      ),
    );
    k += 1;
  }

  // C: razonamiento, tres versiones
  // El "…" va pegado a la última palabra para que nunca quede solo en una línea.
  const sinRaya = (t) => esc(t).replace(/,?\s*_{2,}/g, ",\u00A0…").replace(/:\s*_{2,}/g, ":\u00A0…");
  const bloque = (it) =>
    it.serie
      ? `<div class="ej"><span class="l">${esc(it.consigna)}</span> <span class="s">${sinRaya(it.serie)}</span></div><div class="renglon"></div>`
      : `<div class="ej"><div class="l">${sinRaya(it.consigna)}</div></div><div class="renglon"></div>`;
  out.push(
    pagina(
      `<div class="kick sep">Encuentro ${e.n} · ${esc(e.tema)}</div>
${parte(4, nombreDe(4), minDe(4), `<p>${esc(CUADERNO.razonamientoIntro)}</p>`)}
${NIVELES.map((nv) => `<div class="ver"><h3>${esc(nv.nombre)} ${dots(nv.puntos)}</h3>${e.razonamiento[nv.clave].map(bloque).join("")}</div>`).join("")}`,
      k,
    ),
  );
  k += 1;

  // D: cierre y mandala
  out.push(
    pagina(
      `<div class="kick sep">Encuentro ${e.n} · ${esc(e.tema)}</div>
${parte(5, nombreDe(5), minDe(5), `<p class="fr" style="font-size:22pt;line-height:1.2;margin-bottom:2mm">${esc(e.cierre.pregunta)}</p>
<p class="guion">${esc(e.cierre.guion)}</p>`)}
<div style="margin:2mm 0 5mm"><h3 class="rosa" style="font-size:19pt">${esc(CUADERNO.comoMeSenti)}</h3><div class="renglon"></div><div class="renglon"></div><div class="renglon"></div></div>
<p style="margin-bottom:6mm">${esc(CUADERNO.cierreMarcar)}</p>
${parte(6, nombreDe(6), minDe(6), `<p class="cons">${esc(e.mandala)}</p><p style="margin-top:1.5mm">El mandala está en la página siguiente.</p>`)}
<div class="pie">${ICONOS[e.pie.icono](ROSA)}<span>${esc(e.pie.texto)}</span></div>`,
      k,
    ),
  );
  k += 1;

  // E: lugar del mandala del libro
  out.push(
    pagina(
      `<div class="kick">Encuentro ${e.n} · ${esc(e.tema)}</div>
<h1 class="gr">${esc(CUADERNO.mandalaTitulo)}</h1>
<div class="slot" data-mandala="${e.n}"><div><div class="fr" style="font-size:24pt">${esc(CUADERNO.mandalaMarcador)}</div><p style="margin-top:3mm">Página del libro de mandalas de ${esc(FIRMA)}.</p></div></div>`,
      k,
    ),
  );
  return { paginas: out, siguiente: k + 1, mandala: k };
}

function paginaPausa(p, num) {
  const pasos = p.pasos ? `<ol class="pasos">${li(p.pasos)}</ol>` : "";
  const controles = p.controles
    ? `<div class="cuad2" style="margin:2mm 0 4mm">${p.controles.map((c) => `<div class="caja"><h3>${esc(c.que)}</h3><p>${esc(c.quien)}</p></div>`).join("")}</div>`
    : "";
  const campos = (p.campos || [])
    .map((c) => `<div style="margin-bottom:1mm"><b class="rosa">${esc(c)}</b><div class="renglon"></div></div>`)
    .join("");
  return pagina(
    `<div class="kick">Pausa de vida · Semana ${p.semana}</div>
<h1 class="gr">${esc(p.titulo)}</h1>
<p class="cons" style="margin-bottom:4mm">${esc(p.texto)}</p>${pasos}${controles}
${p.pregunta ? `<p class="fr" style="font-size:20pt;color:var(--rosa);margin-bottom:4mm">${esc(p.pregunta)}</p>` : ""}
${campos}
${p.nota ? `<p class="caja" style="margin-top:4mm">${esc(p.nota)}</p>` : ""}`,
    num,
  );
}

function paginaRegistro(num) {
  const R = CUADERNO.registro;
  return pagina(
    `<div class="kick">${esc(R.kick)}</div><h1 class="gr">${esc(R.titulo)}</h1><p style="margin-bottom:4mm">${esc(R.bajada)}</p>
<table class="reg"><tr><th></th>${R.cols.map((c) => `<th>${esc(c)}</th>`).join("")}</tr>
${SEMANAS.map((s) => `<tr><td class="s">${esc(R.semana)} ${s.n}</td><td><span class="cir"></span><span class="cir"></span></td><td><span class="cir"></span><span class="cir"></span><span class="cir"></span><span class="cir"></span></td><td><span class="cir"></span><span class="cir"></span><span class="cir"></span></td></tr>`).join("")}
</table>
<p style="margin-top:6mm"><b class="rosa">${esc(R.pie)}</b></p><div class="renglon"></div><div class="renglon"></div>`,
    num,
  );
}

function paginaFinal(num) {
  const F = CUADERNO.final;
  return pagina(
    `<div class="kick">${esc(F.kick)}</div><h1 class="gr">${esc(F.titulo)}</h1><p style="margin-bottom:4mm">${esc(F.intro)}</p>
<ul class="pts" style="margin-bottom:6mm">${li(F.seguir)}</ul>
${F.preguntas.map((q) => `<div style="margin-bottom:1mm"><b class="rosa">${esc(q)}</b><div class="renglon"></div></div>`).join("")}`,
    num,
  );
}

function paginaDiploma(num) {
  const D = CUADERNO.diploma;
  return `<section class="pagina"><div class="zona" style="${ZONA}text-align:center;">
<div class="kick">${esc(D.kick)}</div>
<div style="width:62mm;height:62mm;margin:10mm auto 0">${lotoDecorativo(ROSA, 1, 200)}</div>
<h1 class="tema" style="font-size:40pt;margin-top:10mm">${esc(D.titulo)}</h1>
<p class="titulo" style="margin:4mm auto 0;max-width:130mm">${esc(D.texto)}</p>
<div style="display:flex;gap:12mm;margin-top:18mm;text-align:left">
 <div style="flex:1"><div class="renglon"></div><b class="rosa">${esc(D.mama)}</b></div>
 <div style="flex:1"><div class="renglon"></div><b class="rosa">${esc(D.hija)}</b></div>
</div>
<div style="width:70mm;margin:8mm auto 0;text-align:left"><div class="renglon"></div><b class="rosa">${esc(D.fecha)}</b></div>
<div style="position:absolute;left:0;right:0;bottom:0"><div class="fr" style="font-size:22pt">${esc(FIRMA)}</div><div class="kick" style="margin-top:1mm">${esc(MARCA)}</div></div>
</div>${folio(num)}</section>`;
}

const VALORES_BILLETES = [100, 100, 200, 200, 500, 500, 1000, 1000, 1000, 2000, 2000, 5000];
const VALORES_MONEDAS = [5, 5, 10, 10, 10, 20, 20, 20, 50, 50, 50, 100, 100, 100, 200, 200];
const pesos = (v) => "$" + String(v).replace(/\B(?=(\d{3})+(?!\d))/g, ".");

function paginasDinero(num) {
  const D = CUADERNO.dinero;
  const x0 = S + 20 + (176 - 170) / 2;
  const billetes = VALORES_BILLETES.map((v, i) => {
    const x = (i % 2) * 85, y = Math.floor(i / 2) * 40;
    return `<div class="billete" style="left:${x}mm;top:${y}mm"><div class="in"></div><div class="lo">${lotoDecorativo(ROSA, 0.9, 200)}</div><div class="v">${pesos(v)}</div><div class="t">La hora<br>del té</div><div class="j">${D.leyenda}</div></div>`;
  }).join("");
  const monedas = VALORES_MONEDAS.map((v, i) => {
    const x = (i % 4) * 44, y = Math.floor(i / 4) * 44;
    return `<div class="moneda" style="left:${x}mm;top:${y}mm"><div class="in"></div><div class="v">${pesos(v)}</div><div class="j">DE<br>JUGUETE</div></div>`;
  }).join("");
  return [
    pagina(`<div class="kick">${esc(D.kick)} · billetes</div><h1 class="gr" style="font-size:30pt;margin-bottom:1mm">${esc(D.titulo)}</h1><p style="margin-bottom:3mm">${esc(D.bajada)}</p><div style="position:relative;height:245mm;margin-left:3mm">${billetes}</div>`, num),
    pagina(`<div class="kick">${esc(D.kick)} · monedas</div><h1 class="gr" style="font-size:30pt;margin-bottom:1mm">${esc(D.titulo)}</h1><p style="margin-bottom:5mm">${esc(D.bajada)}</p><div style="position:relative;height:190mm;margin-left:2mm">${monedas}</div>`, num + 1),
  ];
}

function paginasRespuestas(lista, num) {
  const porPagina = 4;
  const out = [];
  for (let i = 0; i < lista.length; i += porPagina) {
    const grupo = lista.slice(i, i + porPagina);
    const R = CUADERNO.respuestas;
    out.push(
      pagina(
        `<div class="kick">${esc(R.kick)}</div><h1 class="gr" style="font-size:32pt">${esc(R.titulo)}</h1>${i === 0 ? `<p style="margin-bottom:4mm">${esc(R.intro)}</p>` : ""}
<div class="resp">${grupo
          .map(
            (e) => `<div class="e"><h3>Encuentro ${e.n} · ${esc(e.tema)}</h3>${NIVELES.map(
              (nv) => `<div><b class="rosa">${esc(nv.nombre)}:</b> ${e.razonamiento[nv.clave].map((x, i) => `${"ab"[i]}) ${esc(x.respuesta)}`).join("   ")}</div>`,
            ).join("")}</div>`,
          )
          .join("")}</div>`,
        num + out.length,
      ),
    );
  }
  return out;
}

function portada() {
  const C = CUADERNO.portada;
  return `<section class="pagina"><div class="zona" style="left:${S + 18}mm;right:${S + 14}mm;top:${S + 24}mm;bottom:${S + 14}mm;text-align:center;">
<div class="kick">${esc(C.tipo)}</div>
<h1 style="font-size:66pt;line-height:1;margin-top:10mm;letter-spacing:-.01em">${esc(C.titulo)}</h1>
<div class="fr it" style="font-size:30pt;color:var(--rosa);margin-top:3mm">${esc(C.marca)}</div>
<p style="font-size:22pt;margin:10mm auto 0;max-width:130mm;line-height:1.25">${esc(C.bajada)}</p>
<div style="width:118mm;height:118mm;margin:14mm auto 0">${lotoDecorativo(ROSA, 1, 200)}</div>
<div style="position:absolute;left:0;right:0;bottom:0"><div class="fr" style="font-size:24pt">${esc(FIRMA)}</div><div class="kick" style="margin-top:1mm">${esc(MARCA)}</div></div>
</div></section>`;
}

function contratapa() {
  return `<section class="pagina"><div class="zona" style="left:${S + 20}mm;right:${S + 13}mm;top:${S + 40}mm;bottom:${S + 16}mm;text-align:center;">
<div style="width:72mm;height:72mm;margin:0 auto">${lotoDecorativo(ROSA, 1, 200)}</div>
<p class="fr it" style="font-weight:400;font-size:26pt;color:var(--rosa);margin:12mm auto 0;max-width:130mm;line-height:1.25">${esc(CUADERNO.contratapa.texto)}</p>
<div style="position:absolute;left:0;right:0;bottom:0"><p style="max-width:140mm;margin:0 auto 6mm">${esc(AVISO)}</p><div class="fr" style="font-size:22pt">${esc(FIRMA)}</div><div class="kick" style="margin-top:1mm">${esc(MARCA)}</div></div>
</div></section>`;
}

function paginasApertura(num) {
  const B = CUADERNO.bienvenida, R = CUADERNO.ritmo, E = CUADERNO.encuentro;
  const out = [portada()];
  out.push(
    pagina(
      `<div class="kick">${esc(B.kick)}</div><h1 class="gr">${esc(B.titulo)}</h1><p class="cons" style="margin-bottom:4mm">${esc(B.intro)}</p>
<div class="cuad2">${B.roles.map((r) => `<div class="caja"><h3 class="rosa">${esc(r.quien)}</h3><p>${esc(r.que)}</p></div>`).join("")}</div>
<h2 style="font-size:21pt;margin:5mm 0 2mm">${esc(B.comoUsarloTitulo)}</h2><ul class="pts">${li(B.comoUsarlo)}</ul>
<p class="fr it" style="font-weight:400;color:var(--rosa);font-size:19pt;margin:4mm 0 5mm;line-height:1.25">${esc(B.reglas)}</p>
<div class="caja"><h3 class="rosa" style="font-size:18pt">${esc(B.importante)}</h3><p>${esc(AVISO)}</p></div>`,
      num + 1,
    ),
  );
  out.push(
    pagina(
      `<div class="kick">${esc(R.kick)}</div><h1 class="gr">${esc(R.titulo)}</h1><p style="margin-bottom:4mm">${esc(R.bajada)}</p>
${R.filas.map((f) => `<div class="caja" style="margin-bottom:3mm;padding:3mm 5mm"><div style="display:flex;justify-content:space-between;align-items:baseline"><h3 style="font-size:20pt;margin:0">Semana ${f.semana}</h3><span class="rosa fr it" style="font-weight:400;font-size:19pt">${esc(f.nombre)}</span></div>
<div style="margin-top:1mm"><b class="rosa">${esc(R.cols.app)}:</b> ${esc(R.app)}</div>
<div><b class="rosa">${esc(R.cols.encuentros)}:</b> ${SEMANAS[f.semana - 1].encuentros.map((i) => `${i}. ${esc(encuentros[i - 1].tema)}`).join("  ·  ")}</div>
<div><b class="rosa">${esc(R.cols.movimiento)}:</b> ${esc(R.mov)}</div></div>`).join("")}
<p style="margin-top:3mm">${esc(R.nota)}</p>`,
      num + 2,
    ),
  );
  out.push(
    pagina(
      `<div class="kick">${esc(E.kick)}</div><h1 class="gr">${esc(E.titulo)}</h1><p style="margin-bottom:4mm">${esc(E.bajada)}</p>
<div style="display:flex;height:8mm;border-radius:4mm;overflow:hidden;border:.4mm solid var(--rosa);margin-bottom:6mm">${MOMENTOS.map((m, i) => `<div style="flex:${m.min};background:${i % 2 === 0 ? ROSA : MARFIL}"></div>`).join("")}</div>
${MOMENTOS.map((m, i) => `<div class="parte" style="margin-bottom:3.5mm"><div class="circ">${m.n}</div><div class="pc"><h2 style="font-size:20pt;margin-bottom:.5mm">${esc(m.nombre)}<span class="min">${m.min} min</span></h2><p>${esc(E.momentos[i])}</p></div></div>`).join("")}
<div class="caja" style="margin-top:4mm"><h3 class="rosa">${esc(E.reglasTitulo)}</h3><ul class="pts">${li(E.reglas)}</ul></div>`,
      num + 3,
    ),
  );
  return out;
}

// modo "completo": todo el cuaderno. modo "encuentro1": solo el encuentro 1, para probarlo.
export function armarCuaderno(modo = "completo") {
  const slots = [];
  let pg = [];
  let n = 1;

  if (modo === "encuentro1") {
    const e = encuentros[0];
    const r = paginasEncuentro(e, 1);
    pg = r.paginas;
    n = r.siguiente;
    pg.push(...paginasRespuestas([e], n));
    return { nombre: "encuentro-1-para-probar", titulo: "La hora del té · Encuentro 1 para probar", W: CUAD.W, H: CUAD.H, paginas: pg, css: CSS_CUADERNO, sangrado: S, slots: [r.mandala] };
  }

  pg.push(...paginasApertura(0));
  n = 5;
  const pausaDe = (sem) => PAUSAS.find((p) => p.semana === sem);
  for (const e of encuentros) {
    const r = paginasEncuentro(e, n);
    pg.push(...r.paginas);
    slots.push(r.mandala);
    n = r.siguiente;
    if (e.n === 5) {
      const d = paginasDinero(n);
      pg.push(...d);
      n += d.length;
    }
    if (e.n % 2 === 0) {
      pg.push(paginaPausa(pausaDe(e.semana), n));
      n += 1;
    }
  }
  pg.push(paginaRegistro(n)); n += 1;
  pg.push(paginaDiploma(n)); n += 1;
  pg.push(paginaFinal(n)); n += 1;
  const resp = paginasRespuestas(encuentros, n);
  pg.push(...resp); n += resp.length;
  pg.push(contratapa());
  return { nombre: "cuaderno-la-hora-del-te", titulo: "La hora del té · Cuaderno", W: CUAD.W, H: CUAD.H, paginas: pg, css: CSS_CUADERNO, sangrado: S, slots };
}
