# Caso 005 · Integridad de archivos, usuarios y sudo

[Volver al README](../../README.md)

El 29 de octubre de 2026 amplié las comprobaciones de Anthwatch sobre `anthwatch-server`. Revisé cómo el agente comunica cambios de archivos, altas y bajas de cuentas y errores de autenticación con sudo. Este caso amplía la investigación de [SSH y sudo](../hunts/001-ssh-y-sudo.md) con evidencia de cambios concretos.

## Evidencia y alcance

Conservé una exportación de 124 alertas durante un ejercicio de Incidentes de Ciberseguridad. Para este caso seleccioné las 32 alertas de `anthwatch-server` del 29 de octubre entre las 17:09 y las 18:00 UTC. Cada línea del extracto conserva el contenido original. La prueba se hizo en Wazuh 4.14.9 sobre las VMs de Anthwatch. La numeración 005 corresponde al orden de incorporación al proyecto.

[Extracto JSONL](../evidencias/caso-005/alertas.jsonl) · [SHA-256](../evidencias/caso-005/SHA256SUMS)

## Resultados observados

Las horas corresponden a la emisión de la alerta, en UTC.

| Hora | Regla y nivel | Resultado |
| --- | --- | --- |
| 17:09:20.914 | `5503`, 5 | Fallo de autenticación PAM de sudo |
| 17:09:28.922 | `5404`, 10 | Tres intentos incorrectos al solicitar sudo para `/usr/bin/true` |
| 17:11:54.056 | `5901`, 8; `5902`, 8; `5903`, 3 | Creación del grupo y de la cuenta `ic-prueba`, seguida de su borrado |
| 17:12:59.693–17:13:07.978 | `5901–5903` | Segunda ejecución del ciclo de creación y borrado |
| 17:14:47.227 | `554`, 5 | Alta de `/opt/ic-lab/monitor/triaje.txt` |
| 17:15:02.329 | `550`, 7 | Modificación del archivo, de 13 a 28 bytes, con cambio de hashes |
| 17:15:20.251 | `553`, 7 | Borrado del archivo |

Las tres alertas FIM indican `Mode: realtime`. Los registros de creación y borrado de usuarios tienen PID diferentes en las dos ejecuciones. Los interpreté como acciones repetidas. La [investigación histórica de duplicados](../hunts/hunt-001/repeticiones-exportacion.md) utiliza otro criterio, basado en comparar el contenido de las alertas y su emisión en el manager.

## Interpretación y continuidad

Estas operaciones fueron pruebas controladas. El nivel 10 de sudo expresa la condición detectada por la regla; la prioridad de investigación también depende de la autorización y del contexto.

Ante cambios similares después de un acceso sospechoso, empezaría con el [procedimiento SSH](../playbooks/ssh-autenticacion.md), contrastaría los comandos con el hunt y añadiría las cuentas y rutas afectadas a la cronología. Una coincidencia temporal requiere evidencia adicional de sesión o proceso para atribuir las acciones al mismo actor.

En el ejercicio también comprobé un mensaje de `logger` en journald. Su recepción por el manager quedó pendiente de demostrar en esa prueba. El [caso 004](004-portal-nominas.md) conserva posteriormente la cadena completa del portal, desde `/var/log/syslog` hasta la alerta del Dashboard.

## Procedencia

Las operaciones y la exportación se realizaron en Anthwatch durante un ejercicio de triaje de José Picón. Este informe recoge las pruebas ejecutadas en el servidor y su utilidad para la investigación del laboratorio.
