# Hunt 001 — Investigación de accesos SSH y uso de sudo

Las evidencias iniciales están en [evidencias/](evidencias/); el CSV ampliado a 28 comandos y la guía conjunta de verificación están en [docs/evidencias/hunt-001](../../evidencias/hunt-001/README.md).

- **Detecté:** una secuencia SSH → sudo en una prueba controlada y nueve filas repetidas en la exportación de accesos y sesiones.
- **Validé:** 28 comandos sudo (26 `5402` y 2 `5403`) y 120 filas de accesos/sesiones; reconozco las dos IP de origen como accesos propios.
- **Aprendí:** separar actividad autorizada, correlación temporal y atribución de sesión; comprobar la cobertura y conservar los registros antes de interpretar alertas.

**Fecha:** 22/10/2026. **Estado:** investigación completada con alcance limitado; sin actividad no autorizada identificada en los registros revisados. Las repeticiones se concentran en una franja de journald; investigo reintentos de entrega/indexación como hipótesis, pendiente de contrastar con Filebeat y documentos identificados por `_id`.

## Hipótesis

Una cuenta podría haberse utilizado para acceder por SSH y ejecutar acciones con privilegios sin autorización. Se revisan orígenes, cuentas, comandos y sesiones para buscar actividad que no encaje con la administración conocida del laboratorio.

La prueba controlada inicial verifica la visibilidad. La búsqueda retrospectiva posterior examina registros preexistentes dentro de la ventana, sin generar una secuencia específica para cada resultado de la muestra.

## Revisión del 24/10/2026

Amplié el inventario a **28 comandos sudo: 26 `5402` y 2 `5403`**. La [exportación ampliada](../../evidencias/hunt-001/sudo-eventos.csv) conserva dos comandos que mi filtro inicial excluía: `systemctl status wazuh-agent --no-pager`, el 16/10 a las 11:24:12.086, e `/usr/bin/id`, el 22/10 a las 18:52:16.575. Ambos aparecen como `5403`; la diferencia del primer comando respondía al filtro. El rango observado de la ampliación es 16/10 11:24:12.086–22/10 20:20:12.490.

Mantengo intactos el CSV inicial de 26 `5402` y el de 120 filas, con sus manifiestos y capturas. Los recuentos de la sección histórica siguiente describen esa recogida inicial, no el total corregido. Restauré también el extracto SSH/sudo y verifiqué su hash. El [diagnóstico de repeticiones](repeticiones-exportacion.md) incorpora el manager y el siguiente contraste con Filebeat.

## Alcance y fuentes

Servidor: `anthwatch-server` (`192.168.56.102`, agente `001`). Orígenes del laboratorio: anfitrión `192.168.56.1` y cliente `192.168.56.101`. Wazuh: `192.168.56.103`.

Ventana de búsqueda: **01/10/2026 00:00:00–22/10/2026 20:22:00, Europe/Madrid**. Las 26 alertas de sudo están fechadas el 22/10, entre 13:31:50.855 y 20:20:12.490, según el campo timestamp exportado. La exportación de sesiones contiene resultados desde el 16/10.

Fuentes primarias conservadas:

- [CSV de sudo, 26 filas](evidencias/events-2026-10-22T18_29_54.326Z.csv).
- [CSV de accesos y sesiones, 120 filas](evidencias/events-2026-10-22T18_31_19.384Z.csv).
- [Extracto de auth.log de la prueba controlada](evidencias/auth-1907.log) y [su hash original](evidencias/auth-1907.sha256).
- Capturas de la terminal y del dashboard. Reconozco todos los accesos revisados como propios.

## Consultas y método

En Threat Hunting → Events, con el intervalo absoluto anterior:

```text
agent.name:"anthwatch-server" AND rule.id:"5402"
```

```text
agent.name:"anthwatch-server" AND (rule.id:"5715" OR rule.id:"100100" OR rule.id:"5501" OR rule.id:"5502")
```

Se exportaron timestamp, agente, descripción, nivel, regla, comando, usuario origen/destino, TTY, location y full_log. Se revisó cada sudo en [el inventario de las 26 alertas](revision-sudo.md). Se compararon aperturas/cierres SSH por PID cuando estaba disponible, sin asignar sudo al último login por mera proximidad.

Para revisar el contexto de la prueba: `agent.name:"anthwatch-server"`, entre **19:07:00 y 19:08:00 del 22/10**. La captura 11 contiene ese intervalo absoluto. La captura 08 documenta una consulta distinta, limitada a 5715/5402 y con rango relativo de diez minutos (19:03:14.696–19:13:14.697); no se presenta como evidencia del intervalo absoluto de un minuto.

## Resultados de la recogida inicial del 22/10

| Elemento | Resultado |
|---|---|
| Sudo | 26 filas, todas regla 5402, anthlab → root |
| Fuentes de sudo | 14 journald y 12 /var/log/auth.log |
| Terminales de sudo | 25 pts/0 y 1 pts/1 |
| Duplicados exactos de las filas de sudo | Ninguno |
| Accesos/sesiones | 120 filas: 56 de 5501, 43 de 5502, 19 de 5715 y 2 de 100100 |
| Filas exactamente repetidas en ese CSV | 9 adicionales; 111 combinaciones de campos distintas |
| Accesos correctos | 21 filas; 18 representaciones full_log distintas |
| Orígenes de los 18 registros de acceso distintos | 10 desde .1 y 8 desde .101; usuario anthlab |

Los comandos revisados son compatibles con las tareas realizadas: ajuste horario/NTP, instalación y configuración de rsyslog, copia y edición de ossec.conf, validación y reinicio de servicios, extracción de evidencias e id de la prueba. Reconozco todos los accesos como propios.

Las nueve filas repetidas se conservan en el CSV original y se enumeran en [repeticiones-exportacion.md](repeticiones-exportacion.md). Todas las repeticiones son de journald y se concentran entre las 00:28 y las 01:01 del 22/10: 18 filas forman nueve parejas exactas. A las 01:07 hay otros tres registros sin repetir. La concentración motiva investigar la entrega y la indexación durante ese periodo. Conté esas parejas como repeticiones de filas.

La exportación no incluye algunos accesos que se habían visto en el journal local, por ejemplo el del 22/10 a las 18:31:27. Dejé esa diferencia anotada para revisar la cobertura de la consulta.

### Cobertura anterior al 22/10

En el CSV de accesos y sesiones hay tres registros del 16/10: una apertura y dos cierres PAM de sudo. Mi CSV inicial, filtrado por `5402`, no incluía el comando correspondiente. La ampliación del 24/10 recupera `systemctl status wazuh-agent --no-pager` como `5403` del 16/10: corrijo aquella limitación del filtro. El 21/10 hay cuatro filas: un acceso SSH correcto y tres eventos de sesión. La muestra del 21/10 contiene cero filas `5402`.

Mi investigación de comandos se concentra en el 22/10. Los resultados anteriores evidencian una cobertura incompleta para reconstruir toda la actividad privilegiada, pendiente de contrastar con los registros locales conservados.

## Secuencia controlada y atribución

Horas originales en Europe/Madrid, con desplazamiento +02:00:

| Hora | Evidencia | Interpretación |
|---|---|---|
| 19:07:16.502003 | sshd[2078], Accepted password | anthlab desde 192.168.56.101:55578 |
| 19:07:16.502731 | sshd[2078], session opened | Apertura SSH |
| 19:07:16.506958 | systemd-logind, New session 4 | Registro de sesión del usuario |
| 19:07:28.505149 | sudo, TTY=pts/1, USER=root, COMMAND=/usr/bin/id | Ejecución privilegiada controlada |
| 19:07:28.603679 | pam_unix(sudo:session), session opened | Apertura sudo para root |
| 19:07:28.603775 | pam_unix(sudo:session), session closed | Cierre sudo, no cierre SSH |
| 19:22:37.537869 | sshd[2078], session closed | Cierre SSH en el CSV de sesiones |

Autenticación → sudo: **12,003146 segundos**. El intervalo describe el tiempo de esta ejecución manual, incluida la interacción en el terminal. Un sudo a menos de un segundo del login me haría revisar si hay automatización; usaría ese tiempo para orientar la investigación, no como umbral de sospecha.

La captura del terminal muestra el mismo origen/puerto en SSH_CONNECTION, usuario anthlab, terminal pts/1 y resultado uid=0(root). Usé esos campos junto al extracto para vincular la ejecución controlada.

## Valoración y decisión

**No identifiqué actividad no autorizada en los registros revisados.** Reconozco los orígenes y los comandos son compatibles con las tareas documentadas. La hipótesis de uso no autorizado no queda respaldada por esta muestra. No apliqué contención.

Clasifiqué la actividad por los comandos, el contexto de las tareas y mi reconocimiento de los accesos.

## Límites

- Revisé las alertas y auth.log de un agente. El rango de la consulta es más amplio que la cobertura observada; quedan fuera los comandos sin registro en estas fuentes.
- Comparé fuentes anteriores y posteriores al cambio de recogida, respetando sus formatos horarios.
- El vínculo técnico SSH → sudo está respaldado para la prueba controlada. Las otras ejecuciones carecen de un identificador común de sesión SSH; la relación de la sesión 4 de logind con `pts/1` queda sin verificar. Las etiquetas MITRE describen reglas, no una clasificación de ataque.
- Mi siguiente contraste es el log de Filebeat y una exportación con `_id`, `_index` e `id` de alerta. El manager conserva una coincidencia para `1792621933.6071`; no conservo la exportación que permitiría verificar la pareja documental. La hipótesis de reintentos se detalla en [repeticiones-exportacion.md](repeticiones-exportacion.md).
- Conservé la prueba sintética de fallos duplicados como control de robustez de prioridad baja. Confirma sensibilidad cuando duplico entradas antes del análisis; no reproduce una duplicación posterior en el índice. Considero poco probable que esta última afecte a la correlación: si la copia se genera tras la alerta, no vuelve a alimentar el contador. Este CSV no contiene fallos `5760` ni demuestra un falso positivo histórico.
- Quedan pendientes telemetría de procesos y auditoría completa de ejecución.
- Se completó la [revalidación de 100100 con auth.log](../../validaciones/caso-003-auth-log/README.md), incluidos controles negativos y una prueba real después de corregir la agrupación de rsyslog.

## Capturas y verificación

Las capturas están en [capturas/](capturas/): 07 terminal; 08 búsqueda relativa SSH/sudo; 09 sudo; 10 SSH; 11 contexto absoluto; 12 cierre PAM; 13 búsqueda de la jornada; 14 columnas exportadas.

Desde esta carpeta, `sha256sum -c SHA256SUMS` comprueba las evidencias y capturas incluidas. El manifiesto incluye solo evidencias y capturas, no los textos Markdown. El hash detecta cambios respecto a la copia, no certifica por sí solo origen ni cadena de custodia.
