# Hunt 001 · SSH y sudo

[Volver al README](../../README.md) · [Informe completo](hunt-001/README.md) · [Ticket](../tickets/HUNT-001.md)

Investigué accesos SSH y actividad posterior con sudo. Conservé el extracto `auth-1907.log`, su hash, los CSV históricos y las capturas 07–14. La secuencia controlada del 22/10/2026 enlaza el acceso desde `.101:55578` con `sudo /usr/bin/id` en `pts/1`, 12,003146 s después.

Amplié el filtro inicial de `5402` e identifiqué dos comandos `5403` que también habían llegado a Wazuh. El inventario corregido tiene **28 comandos: 26 `5402` y 2 `5403`**. El CSV histórico de sesiones conserva 120 filas y nueve repeticiones adicionales exactas; no cuento esas filas como nuevas conexiones.

No identifiqué actividad no autorizada en la muestra revisada. El 25/10 confirmé una pareja documental y el 26/10 amplié la revisión a 68 parejas con `_id` distintos y `_source` idéntico. Las nueve parejas del CSV coinciden con esos grupos. Los 68 `id` aparecen una sola vez en los dos archivos conservados del manager y sus campos coinciden con ambas copias indexadas; el contraste respalda la duplicación posterior a la emisión. Hay cuatro parejas de alertas `5760`, lo que acredita repetición documental de fallos SSH; su duplicación antes del análisis sigue sin demostrarse. La causa histórica queda indeterminada por falta de Filebeat de madrugada.

- [Informe, fuentes, cronología y límites](hunt-001/README.md).
- [Repeticiones del CSV e hipótesis de entrega](hunt-001/repeticiones-exportacion.md).
- [Inventario histórico de 26 alertas](hunt-001/revision-sudo.md) y [exportación corregida de 28 comandos](../evidencias/hunt-001/sudo-eventos.csv).
- [Evidencias originales y verificación](../evidencias/hunt-001/README.md).
- [Revalidación real con auth.log](../validaciones/caso-003-auth-log/README.md) y [controles completos del 24/10](../casos/003-revalidacion.md).
