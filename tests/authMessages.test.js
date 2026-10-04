import { test } from "node:test";
import assert from "node:assert/strict";
import { mvLoginErrorMessage } from "../lib/authMessages.js";

test("email no confirmado → mensaje claro que explica revisar el correo", () => {
  const r = mvLoginErrorMessage({ message: "Email not confirmed" });
  assert.match(r.text, /confirm.*email|revis.*correo|revis.*mail/i);
  assert.equal(r.canResend, true);
});

test("credenciales inválidas → mensaje claro, sin reenviar nada", () => {
  const r = mvLoginErrorMessage({ message: "Invalid login credentials" });
  assert.match(r.text, /email o contraseña|usuario o contraseña/i);
  assert.equal(r.canResend, false);
});

test("error desconocido → mensaje genérico amable, sin tecnicismos ni en inglés", () => {
  const r = mvLoginErrorMessage({ message: "some weird internal thing" });
  assert.doesNotMatch(r.text, /[a-z]+ [a-z]+ (error|failed|invalid)/i);
  assert.equal(r.canResend, false);
});

test("sin error → no hay nada que mostrar", () => {
  assert.equal(mvLoginErrorMessage(null), null);
});
