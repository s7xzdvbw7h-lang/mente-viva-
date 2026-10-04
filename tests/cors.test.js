import { test } from "node:test";
import assert from "node:assert/strict";
import { mvApplyCors } from "../lib/cors.js";

function fakeRes() {
  return {
    headers: {},
    statusCode: null,
    ended: false,
    setHeader(name, value) {
      this.headers[name] = value;
    },
    status(code) {
      this.statusCode = code;
      return this;
    },
    end() {
      this.ended = true;
    },
  };
}

test("deja pasar solo al dominio real de la app", () => {
  const res = fakeRes();
  mvApplyCors({ method: "POST" }, res);
  assert.equal(res.headers["Access-Control-Allow-Origin"], "https://menteviva.daninavarro.com.ar");
});

test("una petición OPTIONS (de verificación del navegador) se contesta sola, sin llegar al resto del código", () => {
  const res = fakeRes();
  const handled = mvApplyCors({ method: "OPTIONS" }, res);
  assert.equal(handled, true);
  assert.equal(res.statusCode, 204);
  assert.equal(res.ended, true);
});

test("una petición normal (POST) no se corta acá, sigue su curso", () => {
  const res = fakeRes();
  const handled = mvApplyCors({ method: "POST" }, res);
  assert.equal(handled, false);
});

test("se puede avisar qué métodos acepta cada función (GET para las de solo lectura)", () => {
  const res = fakeRes();
  mvApplyCors({ method: "GET" }, res, { methods: "GET, OPTIONS" });
  assert.equal(res.headers["Access-Control-Allow-Methods"], "GET, OPTIONS");
});
