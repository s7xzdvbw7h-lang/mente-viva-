import { test } from "node:test";
import assert from "node:assert/strict";
import { mvValidateNewPassword } from "../lib/passwordReset.js";

test("contraseña corta → error claro", () => {
  const r = mvValidateNewPassword("abc", "abc");
  assert.equal(r.ok, false);
  assert.match(r.error, /8 caracteres/);
});

test("contraseña de 7 caracteres → sigue siendo corta", () => {
  const r = mvValidateNewPassword("abcdefg", "abcdefg");
  assert.equal(r.ok, false);
  assert.match(r.error, /8 caracteres/);
});

test("las dos contraseñas no coinciden → error claro", () => {
  const r = mvValidateNewPassword("abcdefgh", "abcdefgi");
  assert.equal(r.ok, false);
  assert.match(r.error, /no coinciden|iguales/i);
});

test("contraseña válida (8+) y coincide → ok", () => {
  const r = mvValidateNewPassword("abcdefgh", "abcdefgh");
  assert.equal(r.ok, true);
  assert.equal(r.error, null);
});
