// Pide a Supabase que mande el correo de "recuperar contraseña", pero
// primero revisa el freno (lib/passwordResetGuard.js) — la cuota de
// correos del proyecto es de solo 2 por hora, compartida entre todas las
// usuarias, así que esto evita que alguien la vacíe mandando el
// formulario varias veces seguidas (con el mismo correo o con varios
// distintos). No hace falta estar logueada para pedir esto, por eso no
// se valida ningún JWT acá — es al revés de las otras funciones.

import { mvApplyCors } from "../lib/cors.js";
import { mvCanRequestPasswordReset } from "../lib/passwordResetGuard.js";

const SUPABASE_URL = "https://nfnxoqqyyfydmqxohjrm.supabase.co";
const PUBLISHABLE_KEY = "sb_publishable_mMuwApoUvLJE8PY9cwuG-Q_x3C6ltmb";

export default async function handler(req, res) {
  if (mvApplyCors(req, res)) return;

  if (req.method !== "POST") {
    res.status(405).json({ error: "method_not_allowed" });
    return;
  }

  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!serviceRoleKey) {
    res.status(500).json({ error: "server_not_configured" });
    return;
  }

  const email = (req.body?.email || "").trim().toLowerCase();
  const redirectTo = req.body?.redirectTo;
  if (!email || !redirectTo) {
    res.status(400).json({ error: "bad_request" });
    return;
  }

  const adminHeaders = {
    apikey: serviceRoleKey,
    Authorization: `Bearer ${serviceRoleKey}`,
  };

  const [emailRowResp, globalRowResp] = await Promise.all([
    fetch(
      `${SUPABASE_URL}/rest/v1/password_reset_requests?email=eq.${encodeURIComponent(email)}&select=requested_at`,
      { headers: adminHeaders }
    ),
    fetch(
      `${SUPABASE_URL}/rest/v1/password_reset_requests?select=requested_at&order=requested_at.desc&limit=1`,
      { headers: adminHeaders }
    ),
  ]);
  const emailRows = await emailRowResp.json();
  const globalRows = await globalRowResp.json();

  const guard = mvCanRequestPasswordReset({
    lastForEmail: Array.isArray(emailRows) && emailRows[0] ? emailRows[0].requested_at : null,
    lastGlobal: Array.isArray(globalRows) && globalRows[0] ? globalRows[0].requested_at : null,
    now: new Date().toISOString(),
  });

  if (!guard.allowed) {
    res.status(429).json({ error: "rate_limited", detail: guard.reason });
    return;
  }

  // Anotamos el pedido antes de mandarlo, para que dos pedidos casi
  // simultáneos no se cuelen los dos antes de que el freno se entere.
  await fetch(`${SUPABASE_URL}/rest/v1/password_reset_requests`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...adminHeaders,
      Prefer: "resolution=merge-duplicates,return=minimal",
    },
    body: JSON.stringify({ email, requested_at: new Date().toISOString() }),
  });

  await fetch(`${SUPABASE_URL}/auth/v1/recover`, {
    method: "POST",
    headers: { "Content-Type": "application/json", apikey: PUBLISHABLE_KEY },
    body: JSON.stringify({ email, options: { redirectTo } }),
  });

  res.status(200).json({ ok: true });
}
