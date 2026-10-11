// Tarjeta de la app: QR a Mente Viva y pasos para empezar. Mismo formato que el mazo (9 × 13 cm), hoja A4 con 4.
import { execFileSync } from "node:child_process";
import path from "node:path";
import { AQUI, ROSA, CACAO, esc } from "./base.mjs";
import { TARJETA_APP as T } from "../contenido/generales.mjs";
import { CSS_TARJETAS, marcas, pos, W, H } from "./tarjetas.mjs";
import { lotoDecorativo } from "./graficos.mjs";

const CSS = `${CSS_TARJETAS}
.tj .qr{width:40mm;height:40mm;margin-top:2mm;flex:none;}
.tj .qr svg{width:100%;height:100%;display:block;}
.tj .esc{font-size:17pt;font-weight:700;color:var(--rosa);margin-top:1.5mm;}
.tj ol{list-style:none;text-align:left;margin-top:3mm;width:100%;font-size:16pt;line-height:1.25;}
.tj ol li{display:flex;gap:2.5mm;margin-bottom:1.2mm;}
.tj ol li b{color:var(--rosa);flex:none;font-family:'Fraunces',serif;}
.tj .tit{font-family:'Fraunces',serif;font-weight:600;font-size:25pt;line-height:1.05;margin-top:1mm;}
.tj .dir{font-weight:700;font-size:16pt;line-height:1.3;margin-top:4mm;}
`;

export function armarTarjetaApp() {
  const qr = execFileSync("python3", [path.join(AQUI, "qr.py"), T.url, CACAO], { encoding: "utf8" });
  const frente = (i) =>
    `<div class="tj" style="${pos(i)}"><div class="m chequear"><div class="gr">${esc(T.titulo)}</div><div class="tit">Empezá hoy</div><div class="qr">${qr}</div><div class="esc">Escaneá el código</div><ol>${T.pasos.map((p, k) => `<li><b>${k + 1}</b><span>${esc(p)}</span></li>`).join("")}</ol></div></div>`;
  const dorso = (i) =>
    `<div class="tj dorso" style="${pos(i)}"><div class="m chequear"><div style="width:40mm;height:40mm;flex:none">${lotoDecorativo(ROSA, 1.1, 200)}</div><div class="fr" style="font-size:27pt;margin-top:4mm">${esc(T.titulo)}</div><p style="margin-top:2mm;font-size:17pt;line-height:1.25">${esc(T.bajada)}</p><div class="dir">${esc(T.direccion).replace(/\./g, ".<wbr>")}</div></div></div>`;
  const paginas = [
    `<section class="pagina">${[0, 1, 2, 3].map(frente).join("")}${marcas()}</section>`,
    `<section class="pagina">${[0, 1, 2, 3].map(dorso).join("")}${marcas()}</section>`,
  ];
  return { nombre: "tarjeta-de-la-app", titulo: "La hora del té · Tarjeta de la app", W, H, paginas, css: CSS, sangrado: 0 };
}
