// Arma los PDF del kit "La hora del té" (Mente Viva · NeuroGym) desde kit/contenido.
// Uso:  node kit/armado/construir.mjs                 (todo)
//       node kit/armado/construir.mjs encuentro1      (solo el encuentro 1, para probar)
//       node kit/armado/construir.mjs cuaderno guia   (piezas sueltas)
import fs from "node:fs";
import path from "node:path";
import { chromium, renderizar, RAIZ, HTML_DIR } from "./base.mjs";
import { armarCuaderno } from "./cuaderno.mjs";

const PIEZAS = {
  encuentro1: () => armarCuaderno("encuentro1"),
  cuaderno: () => armarCuaderno("completo"),
};
// Las demás piezas se suman acá a medida que están listas.
for (const [clave, modulo, fn] of [
  ["guia", "./guia.mjs", "armarGuia"],
  ["pizarra", "./pizarra.mjs", "armarPizarra"],
  ["tarjetas", "./tarjetas.mjs", "armarTarjetas"],
  ["tarjeta-app", "./tarjeta-app.mjs", "armarTarjetaApp"],
  ["lamina", "./lamina.mjs", "armarLamina"],
]) {
  if (fs.existsSync(new URL(modulo, import.meta.url))) {
    const m = await import(modulo);
    PIEZAS[clave] = m[fn];
  }
}

const quiere = process.argv.slice(2);
const lista = quiere.length ? quiere : Object.keys(PIEZAS).filter((k) => k !== "encuentro1");
const browser = await chromium.launch();
let problemas = 0;
for (const clave of lista) {
  if (!PIEZAS[clave]) { console.log("· pieza todavía no disponible:", clave); continue; }
  const pieza = await PIEZAS[clave]();
  if (!pieza) { console.log("· se omite:", clave); continue; }
  const r = await renderizar(browser, pieza);
  const marca = r.desbordes.length || r.chicos.length || r.paginasPdf !== r.esperadas ? "⚠" : "✓";
  console.log(`${marca} ${path.relative(RAIZ, r.salida)}  (${r.paginasPdf} páginas)`);
  if (r.paginasPdf !== r.esperadas) console.log(`   páginas esperadas ${r.esperadas}, salieron ${r.paginasPdf}`);
  if (r.desbordes.length) console.log("   SE SALE DE LA PÁGINA:", JSON.stringify(r.desbordes));
  if (r.chicos.length) console.log("   TEXTO MENOR A 16 pt:", JSON.stringify(r.chicos.slice(0, 6)));
  if (r.desbordes.length || r.chicos.length || r.paginasPdf !== r.esperadas) problemas += 1;
  if (pieza.slots) fs.writeFileSync(path.join(HTML_DIR, `${pieza.nombre}.mandalas.json`), JSON.stringify(pieza.slots));
}
await browser.close();
process.exit(problemas ? 2 : 0);
