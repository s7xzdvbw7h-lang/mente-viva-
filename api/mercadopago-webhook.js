// MercadoPago llama acá cada vez que cambia el estado de una suscripción
// (se activa, se pausa, se cancela, falla un cobro). Confirmamos el estado
// real consultando directo a la API de MercadoPago (nunca confiamos en lo
// que venga en el body de la notificación), y actualizamos Supabase.

const SUPABASE_URL = "https://nfnxoqqyyfydmqxohjrm.supabase.co";

function addOneMonth(date) {
  const d = new Date(date);
  d.setMonth(d.getMonth() + 1);
  return d.toISOString().slice(0, 10);
}

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).end();
    return;
  }

  const accessToken = process.env.MERCADOPAGO_ACCESS_TOKEN;
  const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;
  if (!accessToken || !serviceRoleKey) {
    res.status(500).end();
    return;
  }

  const body = req.body || {};
  const preapprovalId =
    body?.data?.id ||
    req.query?.id ||
    (body?.type === "subscription_preapproval" ? body?.data?.id : null);

  const type = body?.type || req.query?.topic;
  if (!preapprovalId || (type && type !== "preapproval" && type !== "subscription_preapproval")) {
    // No es una notificación de suscripción (puede ser de pago suelto u otra cosa) — la ignoramos.
    res.status(200).end();
    return;
  }

  const mpResp = await fetch(`https://api.mercadopago.com/preapproval/${preapprovalId}`, {
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  if (!mpResp.ok) {
    res.status(200).end(); // devolvemos 200 igual para que MP no reintente en loop
    return;
  }
  const preapproval = await mpResp.json();

  const userId = preapproval.external_reference;
  if (!userId) {
    res.status(200).end();
    return;
  }

  // Estados de MercadoPago: pending, authorized, paused, cancelled.
  const mpStatus = preapproval.status;
  const isActive = mpStatus === "authorized";
  const nextPaymentDate =
    preapproval.auto_recurring?.next_payment_date?.slice(0, 10) || addOneMonth(new Date());

  const supabaseHeaders = {
    "Content-Type": "application/json",
    apikey: serviceRoleKey,
    Authorization: `Bearer ${serviceRoleKey}`,
    Prefer: "return=minimal",
  };

  await fetch(
    `${SUPABASE_URL}/rest/v1/subscriptions?mp_preapproval_id=eq.${preapprovalId}`,
    {
      method: "PATCH",
      headers: supabaseHeaders,
      body: JSON.stringify({
        status: mpStatus,
        current_period_end: nextPaymentDate,
        updated_at: new Date().toISOString(),
      }),
    }
  );

  await fetch(`${SUPABASE_URL}/rest/v1/profiles?id=eq.${userId}`, {
    method: "PATCH",
    headers: supabaseHeaders,
    body: JSON.stringify({
      is_pro: isActive,
      pro_since: isActive ? new Date().toISOString().slice(0, 10) : null,
      pro_source: isActive ? "mercadopago" : null,
      updated_at: new Date().toISOString(),
    }),
  });

  res.status(200).end();
}
