// Base común: tamaños, estilos de marca y render a PDF.
// Reglas de diseño: nada menor a 16 pt, consignas de 18 a 22 pt, renglones de 12 mm.
// Marca Luz plena v3: máximo 3 colores y 2 tipografías por pieza (marfil, cacao, rosa de las cenizas · Fraunces y Manrope).
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const require = createRequire("/opt/node-tools/");
export const { chromium } = require("playwright");

export const AQUI = path.dirname(fileURLToPath(import.meta.url));
export const RAIZ = path.resolve(AQUI, "..");
export const HTML_DIR = path.join(AQUI, "_html");
export const PDF_DIR = path.join(RAIZ, "pdf");
export const ENTRADAS = path.join(RAIZ, "entradas");
for (const d of [HTML_DIR, PDF_DIR]) fs.mkdirSync(d, { recursive: true });

export const SANGRADO = 3; // mm por lado
export const MARFIL = "#F7F1E9";
export const CACAO = "#4A3B33";
export const ROSA = "#8E4E52";

export const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

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

// Todo texto es de 16 pt o más.
export const CSS_BASE = `
${FUENTES_CSS}
:root{--marfil:${MARFIL};--cacao:${CACAO};--rosa:${ROSA};}
*{box-sizing:border-box;margin:0;padding:0;}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
body{font-family:'Manrope',sans-serif;color:var(--cacao);font-size:16pt;line-height:1.36;}
h1,h2,h3,.fr{font-family:'Fraunces',serif;font-weight:600;}
.pagina{width:var(--W);height:var(--H);position:relative;overflow:hidden;background:var(--marfil);break-after:page;page-break-after:always;}
.pagina:last-child{break-after:auto;page-break-after:auto;}
.zona{position:absolute;overflow:hidden;}
.kick{font-size:16pt;font-weight:700;letter-spacing:.1em;color:var(--rosa);text-transform:uppercase;}
.min{font-family:'Manrope',sans-serif;font-weight:700;font-size:16pt;color:var(--rosa);margin-left:3mm;white-space:nowrap;}
.rosa{color:var(--rosa);}
.it{font-family:'Fraunces',serif;font-style:italic;font-weight:400;}
.guion{font-family:'Fraunces',serif;font-style:italic;font-weight:400;color:var(--rosa);font-size:17pt;line-height:1.3;}
ul.pts{list-style:none;}
ul.pts li{position:relative;padding-left:7mm;margin-bottom:1.6mm;}
ul.pts li::before{content:"";position:absolute;left:0;top:2.7mm;width:2.4mm;height:2.4mm;border-radius:50%;background:var(--rosa);}
.renglon{height:12mm;border-bottom:.35mm solid var(--rosa);}
.renglones{background-image:repeating-linear-gradient(to bottom,transparent 0,transparent 11.65mm,var(--rosa) 11.65mm,var(--rosa) 12mm);}
.caja{border:.4mm solid var(--rosa);border-radius:3mm;padding:3.5mm 5mm;}
.caja h3{font-size:19pt;line-height:1.15;margin-bottom:1.5mm;}
.folio{position:absolute;display:flex;justify-content:space-between;font-size:16pt;color:var(--rosa);font-weight:600;}
.circ{flex:none;width:12mm;height:12mm;border-radius:50%;background:var(--rosa);color:var(--marfil);font-family:'Fraunces',serif;font-weight:600;font-size:19pt;display:flex;align-items:center;justify-content:center;}
`;

export function documento(titulo, W, H, paginas, extra = "") {
  return `<!doctype html><html lang="es"><head><meta charset="utf-8"><title>${esc(titulo)}</title>
<style>@page{size:${W}mm ${H}mm;margin:0;}${CSS_BASE}:root{--W:${W}mm;--H:${H}mm;}${extra}</style></head>
<body>${paginas.join("\n")}</body></html>`;
}

// Arma el PDF y avisa si algún texto se sale de su página.
export async function renderizar(browser, pieza) {
  const html = documento(pieza.titulo, pieza.W, pieza.H, pieza.paginas, pieza.css || "");
  const archivo = path.join(HTML_DIR, `${pieza.nombre}.html`);
  fs.writeFileSync(archivo, html);
  const page = await browser.newPage();
  await page.goto("file://" + archivo, { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  const desbordes = await page.evaluate(() =>
    [...document.querySelectorAll(".pagina")].flatMap((p, i) => {
      const out = [];
      for (const z of p.querySelectorAll(".zona, .chequear")) {
        const sobra = z.scrollHeight - z.clientHeight;
        if (sobra > 1) out.push({ pagina: i + 1, sobra: Math.round(sobra * 10) / 10 });
      }
      return out;
    }),
  );
  // Nada menor a 16 pt: revisa el tamaño real de cada texto.
  const chicos = await page.evaluate(() => {
    const res = new Map();
    const paginas = [...document.querySelectorAll(".pagina")];
    paginas.forEach((p, i) => {
      for (const el of p.querySelectorAll("*")) {
        if (!el.childNodes.length) continue;
        const tieneTexto = [...el.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
        if (!tieneTexto) continue;
        const px = parseFloat(getComputedStyle(el).fontSize);
        const pt = px * 0.75;
        if (pt < 15.9) res.set(i + 1 + ":" + Math.round(pt * 10) / 10, { pagina: i + 1, pt: Math.round(pt * 10) / 10, texto: el.textContent.trim().slice(0, 40) });
      }
    });
    return [...res.values()];
  });
  const salida = path.join(PDF_DIR, `${pieza.nombre}.pdf`);
  await page.pdf({ path: salida, width: `${pieza.W}mm`, height: `${pieza.H}mm`, printBackground: true, preferCSSPageSize: true });
  await page.close();
  if (pieza.sangrado > 0) execFileSync("python3", [path.join(AQUI, "cajas.py"), salida, String(pieza.sangrado)]);
  const paginasPdf = Number(execFileSync("pdfinfo", [salida], { encoding: "utf8" }).match(/Pages:\s+(\d+)/)[1]);
  return { salida, desbordes, chicos, paginasPdf, esperadas: pieza.paginas.length };
}
