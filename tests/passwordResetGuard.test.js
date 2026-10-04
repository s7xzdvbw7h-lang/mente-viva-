import { test } from "node:test";
import assert from "node:assert/strict";
import { mvCanRequestPasswordReset } from "../lib/passwordResetGuard.js";

const NOW = "2026-10-04T12:00:00.000Z";

test("primer pedido, nunca nadie pidió nada -> se puede", () => {
  const r = mvCanRequestPasswordReset({ lastForEmail: null, lastGlobal: null, now: NOW });
  assert.equal(r.allowed, true);
});

test("ese mismo correo ya pidió hace 2 minutos -> se frena (freno por correo)", () => {
  const r = mvCanRequestPasswordReset({
    lastForEmail: "2026-10-04T11:58:00.000Z",
    lastGlobal: "2026-10-04T11:58:00.000Z",
    now: NOW,
  });
  assert.equal(r.allowed, false);
  assert.match(r.reason, /correo|unos minutos/i);
});

test("ese mismo correo ya pidió hace 10 minutos -> se puede pedir de nuevo", () => {
  const r = mvCanRequestPasswordReset({
    lastForEmail: "2026-10-04T11:50:00.000Z",
    lastGlobal: "2026-10-04T11:50:00.000Z",
    now: NOW,
  });
  assert.equal(r.allowed, true);
});

test("otro correo distinto pidió hace 10 segundos -> se frena igual (freno general, protege la cuota compartida)", () => {
  const r = mvCanRequestPasswordReset({
    lastForEmail: null,
    lastGlobal: "2026-10-04T11:59:50.000Z",
    now: NOW,
  });
  assert.equal(r.allowed, false);
});

test("otro correo distinto pidió hace 2 minutos -> ya se puede", () => {
  const r = mvCanRequestPasswordReset({
    lastForEmail: null,
    lastGlobal: "2026-10-04T11:58:00.000Z",
    now: NOW,
  });
  assert.equal(r.allowed, true);
});
