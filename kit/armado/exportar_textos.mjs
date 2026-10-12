// Textos para leer y revisar (sin diseño): lista de las 40 tarjetas.
//   node kit/armado/exportar_textos.mjs
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { MAZO } from "../contenido/tarjetas.mjs";

const SALIDA = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", "salida");
fs.mkdirSync(SALIDA, { recursive: true });

const grupos = [...new Set(MAZO.map((c) => c.grupo))];
let md = "# Mazo de 40 tarjetas · La hora del té\n\n9 × 13 cm, ilustradas. Las preguntas piden opinión y recuerdos, no datos.\n\n";
let n = 0;
for (const g of grupos) {
  const cartas = MAZO.filter((c) => c.grupo === g);
  md += `## ${g} (${cartas.length})\n\n`;
  for (const c of cartas) {
    n += 1;
    md += `${n}. ${c.pregunta ? c.pregunta : c.detalle ? `${c.nombre}: ${c.detalle}` : c.nombre}\n`;
  }
  md += "\n";
}
md += `Total: ${n} tarjetas.\n`;
fs.writeFileSync(path.join(SALIDA, "lista-de-las-40-tarjetas.md"), md);
console.log("✓ salida/lista-de-las-40-tarjetas.md", `(${n} tarjetas)`);
