# Hunt 001 · SSH y sudo

[Volver al README](../../README.md) · [Informe completo](hunt-001/README.md) · [Ticket](../tickets/HUNT-001.md)

Investigué accesos SSH y actividad posterior con sudo. Conservé el extracto `auth-1907.log`, su hash, los CSV históricos y las capturas 07–14. La secuencia controlada del 22/10/2026 enlaza el acceso desde `.101:55578` con `sudo /usr/bin/id` en `pts/1`, 12,003146 s después.

Amplié el filtro inicial de `5402` e identifiqué dos comandos `5403` que también habían llegado a Wazuh. El inventario corregido tiene **28 comandos: 26 `5402` y 2 `5403`**. El CSV histórico de sesiones conserva 120 filas y nueve repeticiones adicionales exactas; no cuento esas filas como nuevas conexiones.

No identifiqué actividad no autorizada en la muestra revisada. Investigo como hipótesis reintentos de entrega posteriores a la correlación; no conservo una exportación de los dos documentos con `_id` y `_index`, ni los logs de Filebeat de esa franja. Considero poco probable que un duplicado generado después de la correlación infle su contador; todavía debo comprobar dónde se produjo.

- [Informe, fuentes, cronología y límites](hunt-001/README.md).
- [Repeticiones del CSV e hipótesis de entrega](hunt-001/repeticiones-exportacion.md).
- [Inventario histórico de 26 alertas](hunt-001/revision-sudo.md) y [exportación corregida de 28 comandos](../evidencias/hunt-001/sudo-eventos.csv).
- [Evidencias originales y verificación](../evidencias/hunt-001/README.md).
- [Revalidación real con auth.log](../validaciones/caso-003-auth-log/README.md) y [controles completos del 24/10](../casos/003-revalidacion.md).
