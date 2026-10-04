// Freno contra abuso: evita que una misma cuenta dispare pedidos de
// suscripción a MercadoPago uno atrás de otro sin parar. No protege plata
// directamente (MercadoPago no cobra por intento), pero evita juntar
// suscripciones "pendientes" repetidas y saturar el límite de llamadas de
// la cuenta de MercadoPago, lo que podría trabar pagos reales de otras
// clientas.

const COOLDOWN_MS = 2 * 60 * 1000; // 2 minutos

export function mvCanCreateSubscription(latestSubscription, nowISO) {
  if (!latestSubscription) {
    return { allowed: true, reason: null };
  }

  if (latestSubscription.status === "authorized") {
    return { allowed: false, reason: "Ya tenés una suscripción activa." };
  }

  if (latestSubscription.status === "pending") {
    const createdAt = new Date(latestSubscription.created_at).getTime();
    const now = new Date(nowISO).getTime();
    if (now - createdAt < COOLDOWN_MS) {
      return {
        allowed: false,
        reason: "Ya hay un pedido de suscripción reciente. Probá de nuevo en unos minutos.",
      };
    }
  }

  return { allowed: true, reason: null };
}
