// Lógica de avance que tiene que depender de lo guardado en la cuenta
// (Supabase), no de lo que haya en el navegador — para que cambiar de
// celular, cerrar sesión o borrar datos no haga perder nada.

export function mvTodayCompletedIds(sessions, todayISO) {
  const ids = sessions
    .filter((s) => s.date === todayISO)
    .map((s) => s.exId);
  return [...new Set(ids)];
}

export function mvTrialDaysLeft(trialStartISO, todayISO, totalDays) {
  if (!trialStartISO) return totalDays;
  const start = new Date(trialStartISO + "T00:00:00Z");
  const today = new Date(todayISO + "T00:00:00Z");
  const elapsed = Math.floor((today - start) / (1000 * 60 * 60 * 24));
  return Math.max(0, totalDays - elapsed);
}
