// Lógica de si una usuaria tiene el plan completo activo, separada de la
// pantalla para poder probarla sin necesidad de un navegador ni una cuenta real.
// Esta es la fuente de la verdad; el mismo texto se copia a mano dentro del
// bundle único que se sube a producción (no hay empaquetador en este proyecto).

export function computeHasPlan(subscription, todayISO) {
  if (!subscription) return false;
  if (subscription.status === "authorized") return true;
  if (subscription.current_period_end && subscription.current_period_end >= todayISO) {
    return true;
  }
  return false;
}

const MESES = [
  "enero", "febrero", "marzo", "abril", "mayo", "junio",
  "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
];

function formatFechaEs(isoDate) {
  const [y, m, d] = isoDate.split("-").map(Number);
  return `${d} de ${MESES[m - 1]}`;
}

export function planStatusText(subscription, todayISO) {
  const active = computeHasPlan(subscription, todayISO);

  if (!active) {
    return { active: false, label: "Plan gratis", nextLabel: null };
  }

  if (subscription.status === "cancelled") {
    return {
      active: true,
      label: `Plan completo — cancelado, no se renueva`,
      nextLabel: subscription.current_period_end
        ? `Tenés acceso hasta el ${formatFechaEs(subscription.current_period_end)}`
        : null,
    };
  }

  return {
    active: true,
    label: "Plan completo",
    nextLabel: subscription.current_period_end
      ? `Próximo cobro: ${formatFechaEs(subscription.current_period_end)}`
      : null,
  };
}
