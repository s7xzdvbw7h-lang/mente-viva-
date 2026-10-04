// Freno contra el ataque más fácil de todos: la cuota de correos del
// proyecto es de solo 2 por hora, compartida entre TODAS las usuarias.
// Sin este freno, alguien podría vaciarla en segundos mandando el
// formulario de "olvidé mi contraseña" varias veces seguidas — con el
// mismo correo (molestando a una persona puntual) o con varios correos
// distintos, inventados o no (dejando a cualquier usuaria real sin poder
// recibir su propio correo esa hora).

const PER_EMAIL_COOLDOWN_MS = 5 * 60 * 1000; // 5 minutos
const GLOBAL_COOLDOWN_MS = 60 * 1000; // 1 minuto

function withinCooldown(lastISO, now, cooldownMs) {
  if (!lastISO) return false;
  return now - new Date(lastISO).getTime() < cooldownMs;
}

export function mvCanRequestPasswordReset({ lastForEmail, lastGlobal, now }) {
  const nowMs = new Date(now).getTime();

  if (withinCooldown(lastForEmail, nowMs, PER_EMAIL_COOLDOWN_MS)) {
    return {
      allowed: false,
      reason: "Ya te mandamos un link hace poco. Revisá tu correo (y spam), o probá de nuevo en unos minutos.",
    };
  }

  if (withinCooldown(lastGlobal, nowMs, GLOBAL_COOLDOWN_MS)) {
    return {
      allowed: false,
      reason: "Hay muchos pedidos ahora mismo. Probá de nuevo en un minuto.",
    };
  }

  return { allowed: true, reason: null };
}
