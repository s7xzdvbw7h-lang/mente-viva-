// Antes, nada decía explícitamente quién puede llamar a las funciones del
// servidor — funcionaba porque el navegador bloquea solo los pedidos de
// otras páginas que llevan la credencial de sesión, pero no era una regla
// escrita a propósito. Esto la deja explícita: solo el sitio real de la
// app puede llamar a estas funciones desde un navegador.

const ALLOWED_ORIGIN = "https://menteviva.daninavarro.com.ar";

export function mvApplyCors(req, res, { methods = "POST, OPTIONS" } = {}) {
  res.setHeader("Access-Control-Allow-Origin", ALLOWED_ORIGIN);
  res.setHeader("Access-Control-Allow-Methods", methods);
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") {
    res.status(204).end();
    return true;
  }
  return false;
}
