import { test } from "node:test";
import assert from "node:assert/strict";
import { computeHasPlan, planStatusText } from "../lib/plan.js";

// Criterio del PRD: "Que el plan siga activo después del mes pagado si la
// suscripción se canceló (hasta ese día sí sigue activo) o el cobro falló,
// o que se le cobre a una usuaria que ya canceló" NO puede pasar.

test("sin suscripción → no tiene plan", () => {
  assert.equal(computeHasPlan(null, "2026-10-03"), false);
});

test("suscripción authorized → tiene plan", () => {
  assert.equal(
    computeHasPlan({ status: "authorized", current_period_end: "2026-10-01" }, "2026-10-03"),
    true
  );
});

test("cancelada pero todavía dentro del período pagado → sigue con plan", () => {
  assert.equal(
    computeHasPlan({ status: "cancelled", current_period_end: "2026-10-10" }, "2026-10-03"),
    true
  );
});

test("cancelada y el período pagado ya pasó → sin plan", () => {
  assert.equal(
    computeHasPlan({ status: "cancelled", current_period_end: "2026-09-01" }, "2026-10-03"),
    false
  );
});

test("pending (nunca se confirmó el pago) → sin plan", () => {
  assert.equal(
    computeHasPlan({ status: "pending", current_period_end: null }, "2026-10-03"),
    false
  );
});

test("texto de estado: con plan activo muestra próxima fecha de cobro", () => {
  const r = planStatusText({ status: "authorized", current_period_end: "2026-11-03" }, "2026-10-03");
  assert.equal(r.active, true);
  assert.match(r.label, /completo/i);
  assert.match(r.nextLabel, /3 de noviembre|03\/11|2026-11-03/);
});

test("texto de estado: sin plan dice que es gratis", () => {
  const r = planStatusText(null, "2026-10-03");
  assert.equal(r.active, false);
  assert.match(r.label, /gratis/i);
});

test("texto de estado: cancelada pero vigente avisa que no se renueva", () => {
  const r = planStatusText({ status: "cancelled", current_period_end: "2026-10-20" }, "2026-10-03");
  assert.equal(r.active, true);
  assert.match(r.label, /cancelad|no se renueva|hasta el/i);
});
