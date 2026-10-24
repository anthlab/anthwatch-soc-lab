# HUNT-001 · Investigación SSH y sudo

[Informe completo](../hunts/001-ssh-y-sudo.md) · [Volver al README](../../README.md)

**Ticket simulado.** Investigación del 22/10/2026, revisada el 24/10/2026. Estado: investigación documentada; seguimiento de calidad del dato pendiente. No se ha enviado a terceros.

| Campo | Resultado |
| --- | --- |
| Equipo y cuenta | `anthwatch-server`, `anthlab` |
| Hipótesis | Acceso SSH seguido de actividad con privilegios que podría requerir investigación |
| Secuencia de prueba | SSH desde `.101:55578` a las 19:07:16; sudo `/usr/bin/id` en `pts/1` a las 19:07:28 del 22/10, hora local |
| Inventario corregido | 28 comandos: 26 `5402`, 2 `5403`; comprobado en CSV |
| Clasificación | Actividad de prueba autorizada; compromiso no confirmado |
| Decisión | Sin contención ni escalado de incidente; conservar evidencias y mejorar cobertura |

Identifiqué un filtro inicial incompleto de sudo, el cambio journald → auth.log, agrupación de mensajes repetidos corregida y nueve parejas exactas en el CSV de accesos/sesiones. No conservé la exportación con `_id` de los dos documentos; investigaré reintentos con Filebeat antes de localizar la duplicación o atribuirle una causa.

La revalidación de `100100` conserva controles de identidad y tiempo con hashes. Conservé también auth.log, los CSV históricos y las capturas de la secuencia controlada. Considero poco probable que una duplicación posterior a la correlación afecte a su contador; la prueba sintética de duplicados queda con prioridad baja. Escalar a N2 si el acceso no está autorizado, se niega la actividad o aparecen comandos incompatibles con el contexto. La cercanía temporal y el uso de sudo no acreditan por sí solos un ataque.
