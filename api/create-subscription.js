// Crea una suscripción recurrente real en MercadoPago para una usuaria logueada
// y la deja registrada en Supabase con estado "pending" hasta que MercadoPago
// confirme el pago (eso lo hace mercadopago-webhook.js).

import { mvCanCreateSubscription } from "../lib/subscriptionGuard.js";
import { mvApplyCors } from "../lib/cors.js";

const SUPABASE_URL = "https://nfnxoqqyyfydmqxohjrm.supabase.co";
const PLAN_PRICE_ARS = 13500;
const SITE_URL = "https://menteviva.daninavarro.com.ar";

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

  // La usuaria tiene que venir identificada por un JWT de Supabase válido,
  // nunca confiamos en un userId que mande el propio navegador sin probarlo.
  const authHeader = req.headers.authorization || "";
  const userJwt = authHeader.startsWith("Bearer ") ? authHeader.slice(7) : null;
  if (!userJwt) {
    res.status(401).json({ error: "missing_auth" });
    return;
  }

  const userResp = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
    headers: {
      Authorization: `Bearer ${userJwt}`,
      apikey: serviceRoleKey,
    },
  });
  if (!userResp.ok) {
    res.status(401).json({ error: "invalid_session" });
    return;
  }
  const user = await userResp.json();
  const userId = user.id;
  const email = user.email;

  if (!userId || !email) {
    res.status(400).json({ error: "missing_user_data" });
    return;
  }

  // Freno contra abuso: no dejar pedir otra suscripción si ya tiene una
  // activa, o si pidió una hace muy poquito (evita juntar pedidos
  // "pendientes" repetidos y saturar la cuenta de MercadoPago).
  const latestSubResp = await fetch(
    `${SUPABASE_URL}/rest/v1/subscriptions?user_id=eq.${userId}&order=created_at.desc&limit=1`,
    { headers: { apikey: serviceRoleKey, Authorization: `Bearer ${serviceRoleKey}` } }
  );
  const latestSubs = await latestSubResp.json();
  const latestSub = Array.isArray(latestSubs) ? latestSubs[0] : null;
  const guard = mvCanCreateSubscription(latestSub, new Date().toISOString());
  if (!guard.allowed) {
    res.status(429).json({ error: "subscription_cooldown", detail: guard.reason });
    return;
  }

  // Crea la suscripción recurrente mensual en MercadoPago.
  const mpResp = await fetch("https://api.mercadopago.com/preapproval", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${accessToken}`,
    },
    body: JSON.stringify({
      reason: "MenteViva - Plan completo",
      external_reference: userId,
      payer_email: email,
      back_url: `${SITE_URL}/?suscripcion=gracias`,
      auto_recurring: {
        frequency: 1,
        frequency_type: "months",
        transaction_amount: PLAN_PRICE_ARS,
        currency_id: "ARS",
      },
      status: "pending",
    }),
  });

  if (!mpResp.ok) {
    console.error("create-subscription mercadopago_error:", await mpResp.text());
    res.status(502).json({ error: "mercadopago_error" });
    return;
  }

  const preapproval = await mpResp.json();

  // Lo dejamos registrado en Supabase (con la clave de administrador, porque
  // esta función corre del lado del servidor, no como la usuaria).
  await fetch(`${SUPABASE_URL}/rest/v1/subscriptions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      apikey: serviceRoleKey,
      Authorization: `Bearer ${serviceRoleKey}`,
      Prefer: "resolution=merge-duplicates,return=minimal",
    },
    body: JSON.stringify({
      user_id: userId,
      mp_preapproval_id: preapproval.id,
      status: "pending",
    }),
  });

  res.status(200).json({ init_point: preapproval.init_point });
}
