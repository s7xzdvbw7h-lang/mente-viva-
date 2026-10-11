// check_lenguaje: busca palabras prohibidas en todo lo que sale del kit (textos, HTML y PDF).
// Falla (código 1) si encuentra alguna. Correrlo antes de cada entrega:
//   node kit/armado/check_lenguaje.mjs
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

// [patrón, por qué]
const PROHIBIDAS = [
  [/\bprevien\w*/i, "previene"],
  [/\bprevenci\w*/i, "prevención"],
  [/\bprevenir\b/i, "prevenir"],
  [/\bprotege\w*/i, "protege"],
  [/\bproteger\b/i, "proteger"],
  [/\bcura\b/i, "cura"],
  [/\bcurar\b/i, "curar"],
  [/deterior/i, "deterioro"],
  [/\bevit[aeá]\w*/i, "evita / evitar"],
  [/alzheimer/i, "Alzheimer"],
  [/demenc/i, "demencia"],
  [/cl[ií]nic/i, "clínicamente probado"],
  [/\bvalidad[oa]s?\b/i, "validado"],
  [/\bcomprobad[oa]s?\b/i, "comprobado"],
  [/\bprobad[oa]s?\b/i, "probado"],
  [/respaldad[oa]s?\s+cient/i, "respaldado científicamente"],
  [/mejora(r|n)?\s+(la|tu|su|mi)\s+memoria/i, "mejora la memoria"],
  // Siglas, métodos y marcas de terceros: no van en lo público
  [/\bACTIVE\b/, "sigla de un estudio"],
  [/\bPOINTER\b/, "sigla de un estudio"],
  [/\bMAPT\b/, "sigla de un estudio"],
  [/\bFINGERS?\b/, "sigla de un estudio"],
  [/latam-?fingers/i, "nombre de un estudio"],
  [/brainhq/i, "marca de terceros"],
  [/double\s+decision/i, "marca de terceros"],
  [/lumosity/i, "marca de terceros"],
  [/\bachieve\b/i, "nombre de un estudio"],
  [/lancet/i, "fuente de un estudio"],
  [/fleni/i, "nombre de una institución"],
];

function listar(dir, exts) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap((d) => {
    const p = path.join(dir, d.name);
    if (d.isDirectory()) return listar(p, exts);
    return exts.includes(path.extname(d.name).toLowerCase()) ? [p] : [];
  });
}

// Lo que se revisa: textos de contenido, HTML generado, markdown de salida y PDF.
const archivos = [
  ...listar(path.join(RAIZ, "contenido"), [".mjs", ".md", ".json"]),
  ...listar(path.join(RAIZ, "armado", "_html"), [".html"]),
  ...listar(path.join(RAIZ, "pdf"), [".pdf"]),
  ...listar(path.join(RAIZ, "salida"), [".md", ".txt"]),
];

function textoDe(archivo) {
  if (archivo.endsWith(".pdf")) {
    return execFileSync("pdftotext", ["-layout", archivo, "-"], { encoding: "utf8", maxBuffer: 1 << 26 });
  }
  return fs.readFileSync(archivo, "utf8");
}

let hallazgos = 0;
for (const archivo of archivos) {
  const lineas = textoDe(archivo).split("\n");
  lineas.forEach((linea, i) => {
    // Los comentarios del código no salen en ningún lado.
    if (/^\s*\/\//.test(linea)) return;
    for (const [patron, motivo] of PROHIBIDAS) {
      const m = linea.match(patron);
      if (m) {
        hallazgos += 1;
        console.log(`✗ ${path.relative(RAIZ, archivo)}:${i + 1}  «${m[0]}»  (${motivo})\n    ${linea.trim().slice(0, 140)}`);
      }
    }
  });
}

console.log(
  hallazgos
    ? `\n${hallazgos} problema(s) en ${archivos.length} archivos revisados.`
    : `✓ Sin palabras prohibidas en ${archivos.length} archivos revisados.`,
);
process.exit(hallazgos ? 1 : 0);
