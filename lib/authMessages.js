// Traduce los errores técnicos de Supabase Auth a mensajes que una persona
// sin conocimientos técnicos pueda entender y saber qué hacer.

export function mvLoginErrorMessage(error) {
  if (!error) return null;
  const msg = (error.message || "").toLowerCase();

  if (msg.includes("email not confirmed")) {
    return {
      text: "Todavía no confirmaste tu email. Revisá tu correo (y la carpeta de spam) y tocá el link que te mandamos para poder entrar.",
      canResend: true,
    };
  }
  if (msg.includes("invalid login credentials")) {
    return {
      text: "Email o contraseña incorrectos. Fijate bien y probá de nuevo.",
      canResend: false,
    };
  }
  return {
    text: "Algo no funcionó. Probá de nuevo en un rato, y si sigue sin andar, escribinos.",
    canResend: false,
  };
}
