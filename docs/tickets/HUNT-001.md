# HUNT-001 · Investigación SSH y sudo

[Informe completo](../hunts/001-ssh-y-sudo.md) · [Volver al README](../../README.md)

**Ticket simulado.** Investigación del 22/10/2026, revisada el 26/10/2026. Estado: cerrada la revisión histórica; duplicación documental confirmada y causa indeterminada. No se ha enviado a terceros.

| Campo | Resultado |
| --- | --- |
| Equipo y cuenta | `anthwatch-server`, `anthlab` |
| Hipótesis | Acceso SSH seguido de actividad con privilegios que podría requerir investigación |
| Secuencia de prueba | SSH desde `.101:55578` a las 19:07:16; sudo `/usr/bin/id` en `pts/1` a las 19:07:28 del 22/10, hora local |
| Inventario corregido | 28 comandos: 26 `5402`, 2 `5403`; comprobado en CSV |
| Clasificación | Actividad de prueba autorizada; compromiso no confirmado |
| Decisión | Sin contención ni escalado de incidente; conservar evidencias y mejorar cobertura |

Identifiqué un filtro inicial incompleto de sudo, el cambio journald → auth.log, agrupación de mensajes repetidos corregida y nueve parejas exactas en el CSV de accesos/sesiones. Conservé la consulta inicial y la ampliada: confirmé 68 parejas con `_id` distintos y `_source` idéntico. Los 68 `id` aparecen una sola vez en los dos archivos conservados del manager y sus campos coinciden con ambas copias del índice; el contraste respalda la duplicación posterior a la emisión. Documenté dos prefijos NUL en los originales, su tratamiento en memoria y el límite de integridad histórica. Las nueve parejas del CSV coinciden con esos grupos; cuatro parejas corresponden a `5760`. Los archivos de Filebeat empiezan después de la franja de madrugada: mantengo la causa histórica indeterminada. [Análisis y evidencias](../hunts/hunt-001/repeticiones-exportacion.md).

La revalidación de `100100` conserva controles de identidad y tiempo con hashes. Conservé también auth.log, los CSV históricos y las capturas de la secuencia controlada. Considero poco probable que una duplicación posterior a la correlación afecte a su contador; la prueba sintética de duplicados queda con prioridad baja. Escalar a N2 si el acceso no está autorizado, se niega la actividad o aparecen comandos incompatibles con el contexto. La cercanía temporal y el uso de sudo no acreditan por sí solos un ataque.
