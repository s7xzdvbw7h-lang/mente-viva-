// Validación del formulario de "nueva contraseña" (pantalla a la que se
// llega desde el link del mail de recuperación).

export function mvValidateNewPassword(password, confirm) {
  if (password.length < 8) {
    return { ok: false, error: "La contraseña necesita 8 caracteres o más." };
  }
  if (password !== confirm) {
    return { ok: false, error: "Las contraseñas no coinciden." };
  }
  return { ok: true, error: null };
}
