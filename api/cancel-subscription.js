// Cancela la suscripción recurrente de la usuaria logueada en MercadoPago.
// El plan sigue activo hasta el final del período ya pagado (eso lo calcula
// lib/plan.js del lado del frontend a partir de current_period_end).

import { mvApplyCors } from "../lib/cors.js";

const SUPABASE_URL = "https://nfnxoqqyyfydmqxohjrm.supabase.co";

export default async function handler(req, res) {
  if (mvApplyCors(req, res)) return;

  if (req.method !== "POST") {
    res.status(405).json({ error: "method_not_allowed" });
    return;
  }

  const accessToken = process.env.MERCADOPAGO_ACCESS_TOKEN;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!accessToken || !serviceRoleKey) {
    res.status(500).json({ error: "server_not_configured" });
    return;
  }

  const authHeader = req.headers.authorization || "";
  const userJwt = authHeader.startsWith("Bearer ") ? authHeader.slice(7) : null;
  if (!userJwt) {
    res.status(401).json({ error: "missing_auth" });
    return;
  }

  const userResp = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
    headers: { Authorization: `Bearer ${userJwt}`, apikey: serviceRoleKey },
  });
  if (!userResp.ok) {
    res.status(401).json({ error: "invalid_session" });
    return;
  }
  const user = await userResp.json();
  const userId = user.id;

  const subResp = await fetch(
    `${SUPABASE_URL}/rest/v1/subscriptions?user_id=eq.${userId}&order=created_at.desc&limit=1`,
    { headers: { apikey: serviceRoleKey, Authorization: `Bearer ${serviceRoleKey}` } }
  );
  const subs = await subResp.json();
  const sub = Array.isArray(subs) ? subs[0] : null;

  if (!sub || !sub.mp_preapproval_id) {
    res.status(404).json({ error: "no_subscription" });
    return;
  }

  const mpResp = await fetch(
    `https://api.mercadopago.com/preapproval/${sub.mp_preapproval_id}`,
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({ status: "cancelled" }),
    }
  );

  if (!mpResp.ok) {
    const detail = await mpResp.text();
    res.status(502).json({ error: "mercadopago_error", detail });
    return;
  }

  await fetch(`${SUPABASE_URL}/rest/v1/subscriptions?id=eq.${sub.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`,
      Prefer: "return=minimal",
    },
    body: JSON.stringify({ status: "cancelled", updated_at: new Date().toISOString() }),
  });

  res.status(200).json({ ok: true });
}
