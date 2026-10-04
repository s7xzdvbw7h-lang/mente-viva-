import { test } from "node:test";
import assert from "node:assert/strict";
import { mvCanCreateSubscription } from "../lib/subscriptionGuard.js";

test("sin ninguna suscripción previa -> puede crear una", () => {
  const r = mvCanCreateSubscription(null, "2026-10-04T12:00:00.000Z");
  assert.equal(r.allowed, true);
});

test("ya tiene una suscripción autorizada (activa) -> no puede crear otra", () => {
  const r = mvCanCreateSubscription(
    { status: "authorized", created_at: "2026-09-01T12:00:00.000Z" },
    "2026-10-04T12:00:00.000Z"
  );
  assert.equal(r.allowed, false);
  assert.match(r.reason, /ya tenés|ya tiene/i);
});

test("tiene una pendiente creada hace 30 segundos -> no puede crear otra todavía (freno a los clicks repetidos)", () => {
  const r = mvCanCreateSubscription(
    { status: "pending", created_at: "2026-10-04T11:59:30.000Z" },
    "2026-10-04T12:00:00.000Z"
  );
  assert.equal(r.allowed, false);
});

test("tiene una pendiente creada hace 10 minutos -> ya puede volver a intentar", () => {
  const r = mvCanCreateSubscription(
    { status: "pending", created_at: "2026-10-04T11:50:00.000Z" },
    "2026-10-04T12:00:00.000Z"
  );
  assert.equal(r.allowed, true);
});

test("tiene una cancelada vieja -> puede crear una nueva sin problema", () => {
  const r = mvCanCreateSubscription(
    { status: "cancelled", created_at: "2026-01-01T12:00:00.000Z" },
    "2026-10-04T12:00:00.000Z"
  );
  assert.equal(r.allowed, true);
});
