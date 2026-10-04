// Borra a la usuaria logueada de verdad: sus ejercicios, su suscripción, su
// perfil, y su cuenta de acceso. No hay vuelta atrás — por eso la pantalla
// de Mi cuenta pide confirmación dos veces antes de llamar a esto.

import { mvApplyCors } from "../lib/cors.js";

const SUPABASE_URL = "https://nfnxoqqyyfydmqxohjrm.supabase.co";

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

  const userResp = await fetch(`${SUPABASE_URL}/auth/v1/user`, {
    headers: { Authorization: `Bearer ${userJwt}`, apikey: serviceRoleKey },
  });
  if (!userResp.ok) {
    res.status(401).json({ error: "invalid_session" });
    return;
  }
  const user = await userResp.json();
  const userId = user.id;

  const adminHeaders = {
    apikey: serviceRoleKey,
    Authorization: `Bearer ${serviceRoleKey}`,
  };

  // No hay foreign keys con cascade en esta base, así que borramos a mano
  // de las 3 tablas antes de borrar la cuenta de acceso.
  await fetch(`${SUPABASE_URL}/rest/v1/sessions?user_id=eq.${userId}`, {
    method: "DELETE",
    headers: adminHeaders,
  });
  await fetch(`${SUPABASE_URL}/rest/v1/subscriptions?user_id=eq.${userId}`, {
    method: "DELETE",
    headers: adminHeaders,
  });
  await fetch(`${SUPABASE_URL}/rest/v1/profiles?id=eq.${userId}`, {
    method: "DELETE",
    headers: adminHeaders,
  });

  const delResp = await fetch(`${SUPABASE_URL}/auth/v1/admin/users/${userId}`, {
    method: "DELETE",
    headers: adminHeaders,
  });

  if (!delResp.ok) {
    console.error("delete-account auth_delete_failed:", await delResp.text());
    res.status(502).json({ error: "auth_delete_failed" });
    return;
  }

  res.status(200).json({ ok: true });
}
