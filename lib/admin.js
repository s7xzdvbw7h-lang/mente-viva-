// Lógica del panel de administradora: quién puede entrar y cómo se arma
// cada fila de la lista de usuarias. Separada de la pantalla para poder
// probarla sin necesidad de un navegador ni una cuenta real.

import { computeHasPlan, planStatusText } from "./plan.js";

export function mvCanSeeAdminPanel(profile) {
  return !!profile?.is_admin;
}

export function mvAdminUserRow(profile, subscription, todayISO) {
  const status = planStatusText(subscription, todayISO);
  return {
    id: profile.id,
    nombre: profile.nombre || profile.email,
    email: profile.email,
    tienePlan: computeHasPlan(subscription, todayISO),
    estado: status.label,
    proximoCobro: status.nextLabel,
  };
}
