import { test } from "node:test";
import assert from "node:assert/strict";
import { mvTodayCompletedIds, mvTrialDaysLeft } from "../lib/progress.js";

test("sin sesiones → nada completado hoy", () => {
  assert.deepEqual(mvTodayCompletedIds([], "2026-10-03"), []);
});

test("solo cuenta las sesiones de HOY, ignora otros días", () => {
  const sessions = [
    { date: "2026-10-03", exId: "speed" },
    { date: "2026-10-02", exId: "memory" },
    { date: "2026-10-03", exId: "stroop" },
  ];
  const ids = mvTodayCompletedIds(sessions, "2026-10-03");
  assert.deepEqual([...ids].sort(), ["speed", "stroop"]);
});

test("no repite el mismo ejercicio si se hizo dos veces hoy", () => {
  const sessions = [
    { date: "2026-10-03", exId: "speed" },
    { date: "2026-10-03", exId: "speed" },
  ];
  assert.deepEqual(mvTodayCompletedIds(sessions, "2026-10-03"), ["speed"]);
});

test("trial recién empezado → quedan todos los días", () => {
  assert.equal(mvTrialDaysLeft("2026-10-03", "2026-10-03", 7), 7);
});

test("trial a mitad de camino → van quedando menos días", () => {
  assert.equal(mvTrialDaysLeft("2026-10-01", "2026-10-03", 7), 5);
});

test("trial vencido → no quedan días negativos, da 0", () => {
  assert.equal(mvTrialDaysLeft("2026-09-01", "2026-10-03", 7), 0);
});

test("sin fecha de inicio todavía → trial completo (recién se va a crear)", () => {
  assert.equal(mvTrialDaysLeft(null, "2026-10-03", 7), 7);
});
