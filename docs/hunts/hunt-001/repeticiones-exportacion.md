# Repeticiones exactas en la exportación de accesos y sesiones

Comparé todos los campos: conservé 120 filas y 111 combinaciones distintas. Nueve repeticiones adicionales forman nueve parejas exactas, todas journald, entre 00:28:51 y 01:01:55 del 22/10. Hasta las 01:07 hay tres registros adicionales sin repetir. No cuento las parejas como nuevas conexiones.

## Lo que puedo comprobar

- El CSV conserva las parejas de la tabla inferior, pero no contiene `_id` ni `_index`.
- La [extracción original del manager](../../evidencias/ingesta-journald/alerta-original-1792621933-6071.txt) conserva una coincidencia de `id: 1792621933.6071`, `5715`, a las 00:32:13.629 de Madrid.
- El [log del manager](../../evidencias/ingesta-journald/manager-0020-0115.log) registra arranque de módulos a las 00:27:39, errores `No available server` desde 00:28:07 y primeras inicializaciones correctas del conector a las 00:31:57. Las inicializaciones de otros índices continúan después. No interpreto estos mensajes como un log de Filebeat: corresponden al conector de inventario/estados del manager.
- No conservé la exportación de los dos documentos del índice con sus `_id`. Por ello no doy por verificada aquí una duplicación posterior a la alerta ni su causa.

## Hipótesis y siguiente contraste

Investigo si hubo reintentos de entrega tras problemas de disponibilidad del indexador. Elastic documenta que la entrega al menos una vez de Filebeat puede reenviar eventos cuando falta la confirmación y producir documentos duplicados: [documentación oficial](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-deduplication). Es un mecanismo posible; la coincidencia horaria no demuestra que ocurriera en este despliegue ni que los errores del conector fueran errores de Filebeat.

En `anthwatch-wazuh`, recogeré la franja del 22/10 con zona explícita:

```bash
sudo journalctl -u filebeat \
  --since '2026-10-22 00:27:00 Europe/Madrid' \
  --until '2026-10-22 01:15:00 Europe/Madrid' \
  --output=short-iso-precise --no-pager > filebeat-0027-0115.log
sha256sum filebeat-0027-0115.log > filebeat-0027-0115.sha256
```

Si el journal no conserva mensajes del servicio, revisaré su configuración de logging y los archivos rotados antes de concluir ausencia de errores. Exportaré ambos documentos con `_index`, `_id`, `id`, `timestamp`, `agent`, `rule`, `location` y `full_log`, y contrastaré reintentos, reconexiones y confirmaciones con la alerta del manager. No he ejecutado esta recogida en la VM ni dispongo todavía de su resultado.

## Efecto posible sobre 100100

Considero **poco probable que una duplicación posterior a la correlación afecte al recuento de fallos**: si una alerta única se entrega dos veces al índice, esas copias no son entradas nuevas del motor. Es una valoración condicionada al punto de duplicación, que sigue pendiente de verificar.

La prueba sintética conservada de dos fallos duplicados seguida de éxito activa `100100`; el control sin duplicación termina en `5715`. Es un caso distinto: duplica entradas antes de correlacionar. La mantengo como control de robustez de **prioridad baja**, sin afirmar duplicación real de `5760` ni falso positivo histórico. [Entradas y salidas](../../validaciones/caso-003-auth-log/evidencias/duplicados-logtest/).

## Parejas conservadas

| Timestamp del dashboard | Regla | Apariciones | full_log |
|---|---|---:|---|
| Oct 22, 2026 @ 00:28:51.554 | 5501 | 2 | Oct 21 22:28:50 anthwatch-server sshd[1641]: pam_unix(sshd:session): session opened for user anthlab(uid=1000) by anthlab(uid=0) |
| Oct 22, 2026 @ 00:28:51.554 | 5715 | 2 | Oct 21 22:28:50 anthwatch-server sshd[1641]: Accepted password for anthlab from 192.168.56.1 port 38944 ssh2 |
| Oct 22, 2026 @ 00:28:51.571 | 5501 | 2 | Oct 21 22:28:51 anthwatch-server (systemd)[1776]: pam_unix(systemd-user:session): session opened for user anthlab(uid=1000) by anthlab(uid=0) |
| Oct 22, 2026 @ 00:32:13.629 | 5715 | 2 | Oct 21 22:32:13 anthwatch-server sshd[2097]: Accepted password for anthlab from 192.168.56.101 port 60176 ssh2 |
| Oct 22, 2026 @ 00:32:13.721 | 5501 | 2 | Oct 21 22:32:13 anthwatch-server sshd[2097]: pam_unix(sshd:session): session opened for user anthlab(uid=1000) by anthlab(uid=0) |
| Oct 22, 2026 @ 00:32:36.249 | 5502 | 2 | Oct 21 22:32:35 anthwatch-server sshd[2097]: pam_unix(sshd:session): session closed for user anthlab |
| Oct 22, 2026 @ 00:38:59.087 | 5715 | 2 | Oct 21 22:38:57 anthwatch-server sshd[2222]: Accepted password for anthlab from 192.168.56.101 port 45230 ssh2 |
| Oct 22, 2026 @ 00:38:59.117 | 5501 | 2 | Oct 21 22:38:57 anthwatch-server sshd[2222]: pam_unix(sshd:session): session opened for user anthlab(uid=1000) by anthlab(uid=0) |
| Oct 22, 2026 @ 01:01:55.130 | 5502 | 2 | Oct 21 23:01:53 anthwatch-server sshd[2222]: pam_unix(sshd:session): session closed for user anthlab |
