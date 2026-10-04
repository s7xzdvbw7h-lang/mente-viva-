import { test } from "node:test";
import assert from "node:assert/strict";
import { mvValidateNewPassword } from "../lib/passwordReset.js";

test("contraseña corta → error claro", () => {
  const r = mvValidateNewPassword("abc", "abc");
  assert.equal(r.ok, false);
  assert.match(r.error, /6 caracteres/);
});

test("las dos contraseñas no coinciden → error claro", () => {
  const r = mvValidateNewPassword("abcdef", "abcdeg");
  assert.equal(r.ok, false);
  assert.match(r.error, /no coinciden|iguales/i);
});

test("contraseña válida y coincide → ok", () => {
  const r = mvValidateNewPassword("abcdef", "abcdef");
  assert.equal(r.ok, true);
  assert.equal(r.error, null);
});
