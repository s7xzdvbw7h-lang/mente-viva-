import { test } from "node:test";
import assert from "node:assert/strict";
import { mvCanSeeAdminPanel, mvAdminUserRow } from "../lib/admin.js";

test("perfil sin is_admin → no puede ver el panel", () => {
  assert.equal(mvCanSeeAdminPanel({ is_admin: false }), false);
});

test("perfil sin cargar todavía (null) → no puede ver el panel", () => {
  assert.equal(mvCanSeeAdminPanel(null), false);
});

test("perfil con is_admin true → puede ver el panel", () => {
  assert.equal(mvCanSeeAdminPanel({ is_admin: true }), true);
});

test("fila de usuaria sin plan → estado gratis", () => {
  const row = mvAdminUserRow(
    { id: "u1", nombre: "Marta", email: "marta@example.com" },
    null,
    "2026-10-03"
  );
  assert.equal(row.nombre, "Marta");
  assert.equal(row.email, "marta@example.com");
  assert.equal(row.tienePlan, false);
  assert.equal(row.estado, "Plan gratis");
});

test("fila de usuaria con plan activo → estado y próximo cobro", () => {
  const row = mvAdminUserRow(
    { id: "u2", nombre: "Ana", email: "ana@example.com" },
    { status: "authorized", current_period_end: "2026-11-01" },
    "2026-10-03"
  );
  assert.equal(row.tienePlan, true);
  assert.equal(row.estado, "Plan completo");
  assert.match(row.proximoCobro, /1 de noviembre/);
});

test("fila de usuaria sin nombre cargado → usa el email como respaldo", () => {
  const row = mvAdminUserRow({ id: "u3", nombre: null, email: "sinNombre@example.com" }, null, "2026-10-03");
  assert.equal(row.nombre, "sinNombre@example.com");
});
