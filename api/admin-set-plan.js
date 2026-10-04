// Activa o desactiva el plan completo de una usuaria a mano, solo para la
// cuenta administradora (profiles.is_admin = true). Inserta una fila nueva
// en subscriptions (misma tabla que usa MercadoPago) en vez de tocar
// profiles.is_pro directamente, porque la app calcula el acceso a partir de
// la suscripción más reciente, no de esa columna vieja.

import { mvApplyCors } from "../lib/cors.js";

const SUPABASE_URL = "https://nfnxoqqyyfydmqxohjrm.supabase.co";

function addYears(isoDate, years) {
  const d = new Date(isoDate + "T00:00:00Z");
  d.setUTCFullYear(d.getUTCFullYear() + years);
  return d.toISOString().slice(0, 10);
}

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

  const authHeader = req.headers.authorization || "";
  const userJwt = authHeader.startsWith("Bearer ") ? authHeader.slice(7) : null;
  if (!userJwt) {
    res.status(401).json({ error: "missing_auth" });
    return;
  }

  const { targetUserId, action } = req.body || {};
  if (!targetUserId || (action !== "activate" && action !== "deactivate")) {
    res.status(400).json({ error: "bad_request" });
    return;
  }

  const userResp = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
    headers: { Authorization: `Bearer ${userJwt}`, apikey: serviceRoleKey },
  });
  if (!userResp.ok) {
    res.status(401).json({ error: "invalid_session" });
    return;
  }
  const caller = await userResp.json();

  const callerProfileResp = await fetch(
    `${SUPABASE_URL}/rest/v1/profiles?id=eq.${caller.id}&select=is_admin`,
    { headers: { apikey: serviceRoleKey, Authorization: `Bearer ${serviceRoleKey}` } }
  );
  const callerProfiles = await callerProfileResp.json();
  const isAdmin = Array.isArray(callerProfiles) && callerProfiles[0]?.is_admin === true;
  if (!isAdmin) {
    res.status(403).json({ error: "not_admin" });
    return;
  }

  const today = new Date().toISOString().slice(0, 10);
  const newRow =
    action === "activate"
      ? { user_id: targetUserId, status: "authorized", current_period_end: addYears(today, 1) }
      : { user_id: targetUserId, status: "cancelled", current_period_end: today };

  const insertResp = await fetch(`${SUPABASE_URL}/rest/v1/subscriptions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`,
      Prefer: "return=minimal",
    },
    body: JSON.stringify(newRow),
  });

  if (!insertResp.ok) {
    // El detalle técnico (puede traer nombres de tablas/columnas) queda
    // solo en el registro privado del servidor, nunca viaja al navegador.
    console.error("admin-set-plan db_error:", await insertResp.text());
    res.status(502).json({ error: "db_error" });
    return;
  }

  res.status(200).json({ ok: true });
}
