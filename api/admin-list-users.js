// Devuelve la lista de usuarias con su plan actual, solo para la cuenta
// administradora (profiles.is_admin = true). Usa la clave de servicio para
// poder leer todas las filas, no solo la propia (eso es lo que hace que el
// panel sea posible sin abrirle un agujero de RLS a cualquier usuaria).

const SUPABASE_URL = "https://nfnxoqqyyfydmqxohjrm.supabase.co";

export default async function handler(req, res) {
  if (req.method !== "GET") {
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

  const profilesResp = await fetch(
    `${SUPABASE_URL}/rest/v1/profiles?select=id,nombre,email,is_pro,trial_start_date&order=id.asc`,
    { headers: { apikey: serviceRoleKey, Authorization: `Bearer ${serviceRoleKey}` } }
  );
  const profiles = await profilesResp.json();

  const subsResp = await fetch(
    `${SUPABASE_URL}/rest/v1/subscriptions?select=user_id,status,current_period_end,created_at&order=created_at.desc`,
    { headers: { apikey: serviceRoleKey, Authorization: `Bearer ${serviceRoleKey}` } }
  );
  const allSubs = await subsResp.json();

  const latestSubByUser = {};
  for (const sub of Array.isArray(allSubs) ? allSubs : []) {
    if (!latestSubByUser[sub.user_id]) latestSubByUser[sub.user_id] = sub;
  }

  const users = (Array.isArray(profiles) ? profiles : []).map((p) => ({
    profile: { id: p.id, nombre: p.nombre, email: p.email },
    subscription: latestSubByUser[p.id] || null,
  }));

  res.status(200).json({ users });
}
