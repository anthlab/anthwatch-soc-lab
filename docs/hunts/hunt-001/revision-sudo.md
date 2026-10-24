# Inventario inicial · 26 alertas de sudo (`5402`)

Amplié esta revisión el 24/10: el [CSV corregido](../../evidencias/hunt-001/sudo-eventos.csv) contiene 28 comandos (26 `5402` y 2 `5403`). Esta tabla conserva la correspondencia con las 26 filas del CSV inicial, cuyo filtro excluía `5403`.

Las filas se ordenan por timestamp del dashboard; se conserva el número de fila de datos del CSV original (sin contar la cabecera). Todas corresponden a anthlab → root. Revisé los comandos y los comparé con las tareas que había realizado.

| ID | Fila CSV | Timestamp del dashboard | Fuente / TTY | Comando | Valoración |
|---|---:|---|---|---|---|
| S01 | 26 | Oct 22, 2026 @ 13:31:50.855 | journald / pts/0 | `/usr/bin/timedatectl set-timezone Europe/Madrid` | Administración del laboratorio |
| S02 | 25 | Oct 22, 2026 @ 13:31:52.868 | journald / pts/0 | `/usr/bin/timedatectl set-ntp true` | Administración del laboratorio |
| S03 | 24 | Oct 22, 2026 @ 16:20:22.064 | journald / pts/0 | `/usr/bin/journalctl -u ssh --since 2026-10-22T16:19:01+02:00 --until 2026-10-22T16:20:03+02:00 --output=short-iso --no-pager` | Administración del laboratorio |
| S04 | 23 | Oct 22, 2026 @ 18:31:51.167 | journald / pts/0 | `/usr/bin/journalctl -u ssh --since '24 hours ago' --no-pager -n 40` | Administración del laboratorio |
| S05 | 22 | Oct 22, 2026 @ 18:31:57.169 | journald / pts/0 | `/usr/bin/journalctl _COMM=sudo --since '24 hours ago' --no-pager -n 40` | Administración del laboratorio |
| S06 | 21 | Oct 22, 2026 @ 18:49:41.197 | journald / pts/0 | `/usr/bin/apt update` | Administración del laboratorio |
| S07 | 20 | Oct 22, 2026 @ 18:49:57.215 | journald / pts/0 | `/usr/bin/apt install -y rsyslog` | Administración del laboratorio |
| S08 | 19 | Oct 22, 2026 @ 18:49:57.221 | journald / pts/0 | `/usr/bin/timedatectl set-timezone Europe/Madrid` | Administración del laboratorio |
| S09 | 18 | Oct 22, 2026 @ 18:49:57.236 | journald / pts/0 | `/usr/bin/systemctl enable --now rsyslog` | Administración del laboratorio |
| S10 | 17 | Oct 22, 2026 @ 18:49:59.272 | journald / pts/0 | `/usr/bin/systemctl restart rsyslog` | Administración del laboratorio |
| S11 | 16 | Oct 22, 2026 @ 18:50:23.386 | journald / pts/0 | `/usr/bin/cp -a /var/ossec/etc/ossec.conf /var/ossec/etc/ossec.conf.bak-20261022-185022` | Administración del laboratorio |
| S12 | 15 | Oct 22, 2026 @ 18:50:27.402 | journald / pts/0 | `/usr/bin/nano /var/ossec/etc/ossec.conf` | Administración del laboratorio |
| S13 | 14 | Oct 22, 2026 @ 18:51:48.529 | journald / pts/0 | `/var/ossec/bin/wazuh-logcollector -t` | Administración del laboratorio |
| S14 | 13 | Oct 22, 2026 @ 18:51:48.535 | journald / pts/0 | `/usr/bin/systemctl restart wazuh-agent` | Administración del laboratorio |
| S15 | 12 | Oct 22, 2026 @ 18:52:16.575 | /var/log/auth.log / pts/0 | `/usr/bin/tail -n 5 /var/log/auth.log` | Administración del laboratorio |
| S16 | 11 | Oct 22, 2026 @ 19:07:29.897 | /var/log/auth.log / pts/1 | `/usr/bin/id` | Prueba autorizada: captura terminal, pts/1 y sesión sshd[2078] respaldan el vínculo |
| S17 | 10 | Oct 22, 2026 @ 19:23:28.008 | /var/log/auth.log / pts/0 | `/usr/bin/grep ^2026-10-22T19:07: /var/log/auth.log` | Administración del laboratorio |
| S18 | 9 | Oct 22, 2026 @ 20:03:47.417 | /var/log/auth.log / pts/0 | `/usr/bin/grep ^2026-10-22T19:56: /var/log/auth.log` | Administración del laboratorio |
| S19 | 8 | Oct 22, 2026 @ 20:05:12.062 | /var/log/auth.log / pts/0 | `/usr/bin/grep ^2026-10-22T19:56: /var/log/auth.log` | Administración del laboratorio |
| S20 | 7 | Oct 22, 2026 @ 20:05:18.092 | /var/log/auth.log / pts/0 | `/usr/bin/cp -a /etc/rsyslog.conf /etc/rsyslog.conf.bak-20261022-200517` | Administración del laboratorio |
| S21 | 6 | Oct 22, 2026 @ 20:05:18.143 | /var/log/auth.log / pts/0 | `/usr/bin/nano /etc/rsyslog.conf` | Administración del laboratorio |
| S22 | 5 | Oct 22, 2026 @ 20:05:51.005 | /var/log/auth.log / pts/0 | `/usr/sbin/rsyslogd -N1` | Administración del laboratorio |
| S23 | 4 | Oct 22, 2026 @ 20:05:51.026 | /var/log/auth.log / pts/0 | `/usr/bin/systemctl restart rsyslog` | Administración del laboratorio |
| S24 | 3 | Oct 22, 2026 @ 20:10:47.795 | /var/log/auth.log / pts/0 | `/usr/bin/grep -E ^2026-10-22T20:(07\|08): /var/log/auth.log` | Administración del laboratorio |
| S25 | 2 | Oct 22, 2026 @ 20:20:06.572 | /var/log/auth.log / pts/0 | `/usr/bin/sed -n /<localfile>/,/<\\\\/localfile>/p /var/ossec/etc/ossec.conf` | Administración del laboratorio |
| S26 | 1 | Oct 22, 2026 @ 20:20:12.490 | /var/log/auth.log / pts/0 | `/usr/bin/grep -n RepeatedMsgReduction /etc/rsyslog.conf` | Administración del laboratorio |

## Límites

La captura del terminal y `pts/1` respaldan el vínculo SSH de S16. En las otras 25 filas clasifiqué la tarea por su comando y contexto; su sesión SSH concreta queda sin atribuir. Este CSV solo incluye `5402`; la ampliación a `5403` está enlazada al principio.

Comparé `full_log` y las 26 filas son distintas. Para revisar duplicados distingo una copia del mismo registro de dos ejecuciones del mismo comando a horas diferentes. La cobertura de este inventario queda limitada al filtro y periodo exportados.
