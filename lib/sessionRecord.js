// Arma la fila que se guarda en `sessions` cada vez que se completa un
// ejercicio, con los 6 datos que pide el PRD (fecha/hora las pone la base de
// datos sola con el valor por defecto de la columna). Separado de la
// pantalla para poder probarlo sin necesidad de un navegador ni una cuenta.

export function mvBuildSessionRecord({ userId, exId, score, nivel, duracionSeg, mensaje }) {
  const duracion = Number.isFinite(duracionSeg) && duracionSeg > 0 ? duracionSeg : 0;
  return {
    user_id: userId,
    ex_id: exId,
    score,
    nivel: nivel || null,
    duracion_seg: duracion,
    mensaje: mensaje || null,
  };
}
