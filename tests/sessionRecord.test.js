import { test } from "node:test";
import assert from "node:assert/strict";
import { mvBuildSessionRecord } from "../lib/sessionRecord.js";

test("arma el registro completo con los 6 datos que pide el PRD", () => {
  const rec = mvBuildSessionRecord({
    userId: "u1",
    exId: "velocidad",
    score: 80,
    nivel: "naranja",
    duracionSeg: 47,
    mensaje: "¡Muy bien hecho!",
  });
  assert.equal(rec.user_id, "u1");
  assert.equal(rec.ex_id, "velocidad");
  assert.equal(rec.score, 80);
  assert.equal(rec.nivel, "naranja");
  assert.equal(rec.duracion_seg, 47);
  assert.equal(rec.mensaje, "¡Muy bien hecho!");
});

test("sin duración (undefined) → guarda 0, no undefined ni NaN", () => {
  const rec = mvBuildSessionRecord({ userId: "u1", exId: "memoria", score: 50 });
  assert.equal(rec.duracion_seg, 0);
});

test("sin nivel → guarda null, no se inventa un valor", () => {
  const rec = mvBuildSessionRecord({ userId: "u1", exId: "memoria", score: 50 });
  assert.equal(rec.nivel, null);
});

test("sin mensaje → guarda null, no se inventa un valor", () => {
  const rec = mvBuildSessionRecord({ userId: "u1", exId: "memoria", score: 50 });
  assert.equal(rec.mensaje, null);
});

test("duración negativa o rara se guarda en 0, nunca negativa", () => {
  const rec = mvBuildSessionRecord({ userId: "u1", exId: "memoria", score: 50, duracionSeg: -5 });
  assert.equal(rec.duracion_seg, 0);
});
