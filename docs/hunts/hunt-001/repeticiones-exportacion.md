# Duplicado documental · Análisis y cierre

**Revisión inicial cerrada el 25/10 y ampliada el 26/10/2026: 68 parejas de documentos confirmadas; causa histórica indeterminada.**

Comparé las 120 filas del CSV histórico: contienen 111 combinaciones distintas y nueve repeticiones adicionales. Las nueve parejas son journald y se concentran entre 00:28:51 y 01:01:55 del 22/10. Después consulté directamente el índice para verificar una de ellas con sus identificadores.

## Comparación de documentos

La [consulta conservada](../../evidencias/duplicados-001/consulta.http) devuelve exactamente dos documentos, sin timeout y con los tres shards consultados correctamente. La [respuesta JSON](../../evidencias/duplicados-001/respuesta.json) contiene:

| Campo | Documento 1 | Documento 2 |
| --- | --- | --- |
| `_index` | `wazuh-alerts-4.x-2026.10.21` | `wazuh-alerts-4.x-2026.10.21` |
| `_id` | `_G3EYKEB2FcM32JORPmE` | `hoGYYKEBuyfJP5vvDryk` |
| `id` de alerta | `1792621933.6071` | `1792621933.6071` |
| `timestamp` | `2026-10-21T22:32:13.629+0000` | `2026-10-21T22:32:13.629+0000` |
| Agente / regla | `001`, `anthwatch-server` / `5715` | `001`, `anthwatch-server` / `5715` |
| Fuente | `journald` | `journald` |

Los campos exportados de `_source` coinciden por completo, incluido `full_log`: acceso correcto de `anthlab` desde `.101:60176`, proceso `sshd[2097]`. El evento corresponde al **22/10 a las 00:32:13.629 en Madrid**. El nombre del índice conserva la fecha UTC.

`_id` identifica cada documento del índice; `id` identifica la alerta del manager. Los dos documentos representan la misma alerta. Sus `_score` son distintos: son puntuaciones de búsqueda y no aportan una cronología de entrega.

La [extracción original del manager](../../evidencias/ingesta-journald/alerta-original-1792621933-6071.txt) conserva una coincidencia para ese `id`, con el mismo mensaje, timestamp y regla. Con la evidencia disponible sitúo la duplicación en la entrega/indexación de la alerta, después de su emisión. La comparación descarta que esta pareja sea solo una repetición del CSV.

## Ampliación a todos los índices consultados · 26/10

Consulté `wazuh-alerts-4.x-*` y agrupé por `id`, con dos documentos completos por grupo. La [respuesta original](../../evidencias/duplicados-001/duplicados-ampliados.console.txt) incluye **1.672 documentos**, 21 shards consultados correctamente y ningún timeout. La agregación devuelve **68 grupos de dos documentos**: **136 documentos**, con `_id` distintos y `_source` idéntico en las 68 parejas. `sum_other_doc_count` y el margen de error son cero; el listado cabe completo en el tamaño solicitado.

La [comparación derivada](../../evidencias/duplicados-001/comparacion-ampliada.json) recoge los identificadores y comprobaciones. Contrasté las nueve parejas del CSV original: las nueve coinciden con grupos de esta respuesta en todos sus campos exportados.

| Agente | Parejas |
| --- | ---: |
| `anthwatch-server` (`001`) | 43 |
| `anthwatch-client` (`002`) | 15 |
| `anthwatch-wazuh` (`000`) | 10 |
| Total | 68 |

Hay 66 parejas en `wazuh-alerts-4.x-2026.10.21`, entre **22/10 00:27:58.962 y 01:03:34.576 de Madrid**. Las otras dos están en `wazuh-alerts-4.x-2026.10.22`, a las **20:38:47.533 y 20:38:47.642 de Madrid**: cierre de sesión (`5502`) y parada del agente (`506`). Los dos nombres de índice representan fechas UTC; las 68 parejas corresponden al mismo día local, el 22/10.

| Regla | Parejas | Regla | Parejas | Regla | Parejas |
| --- | ---: | --- | ---: | --- | ---: |
| `5710` | 15 | `5501` | 12 | `5503` | 9 |
| `5715` | 7 | `5502` | 7 | `5760` | 4 |
| `2904` | 4 | `503` | 2 | `5402` | 2 |
| `502` | 1 | `2502` | 1 | `5712` | 1 |
| `2902` | 1 | `5551` | 1 | `506` | 1 |

La ampliación confirma que la repetición documental también afecta a cuatro alertas de fallo SSH `5760`. No aparecen grupos repetidos de `100100` por `id` en esta consulta. Esto corrige el alcance de la primera revisión, centrada en una pareja `5715`.

## Revisión de Filebeat

Consulté el journal y recogí los archivos rotados de `/var/log/filebeat`. La [recogida conservada](../../evidencias/duplicados-001/README.md) contiene ocho archivos; el registro más antiguo es del **22/10 a las 16:13:57.069+02:00**. La franja investigada era **00:27–01:15+02:00**, por lo que falta el detalle de entrega de esa madrugada. La consulta al journal mostró arranques del servicio, sin mensajes de publicación útiles para atribuir la causa.

Los archivos conservan errores `connection refused`, respuestas `503` y conexiones restablecidas en horas posteriores. Los trato como contexto operativo de esas horas, no como evidencia causal de este duplicado.

El [log del manager](../../evidencias/ingesta-journald/manager-0020-0115.log) sí cubre la franja: registra arranque de módulos a las 00:27:39, errores `No available server` desde 00:28:07 e inicializaciones correctas desde 00:31:57. Esos mensajes pertenecen al conector de inventario/estados del manager, distinto de Filebeat.

## Valoración de la hipótesis

Los reintentos de entrega siguen siendo una explicación posible. Elastic documenta que Filebeat puede reenviar eventos cuando falta la confirmación y producir documentos duplicados: [documentación oficial](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-deduplication). La coincidencia temporal con problemas del indexador orientó la revisión, pero falta el log de Filebeat de esa franja para atribuir este caso a ese mecanismo.

## Dos parejas junto a la parada de Filebeat

Las alertas `5502` y `506` tienen marcas de las **20:38:47.533 y 20:38:47.642+02:00**. En [filebeat.3](../../evidencias/duplicados-001/filebeat/filebeat.3), Filebeat registra `Stopping filebeat` a las **20:38:49.807** y un error de publicación a las **20:38:49.871**: `failed to perform any bulk index operations`, petición a `https://127.0.0.1:9200/_bulk` terminada con `EOF`. Después aparecen mensajes del reintentador y la parada a las 20:38:49.921. El siguiente archivo, [filebeat.2](../../evidencias/duplicados-001/filebeat/filebeat.2), comienza a las **21:10:11.056**. Todas estas horas son de Madrid, el 22/10.

**Inferencia:** un lote recibido por el indexador cuya confirmación se perdió al apagar podría reenviarse tras el arranque y producir las dos copias. Encaja con la entrega al menos una vez descrita por Elastic. El log no identifica las alertas del lote ni conserva una confirmación de su reenvío; por eso mantengo esta explicación como candidata para las dos parejas tardías.

## Pista temporal en la captura del caso 001

Volví a revisar la [captura del dashboard](../../capturas/ssh-eventos-dashboard.png): muestra `Last 15 minutes`, un gráfico hasta aproximadamente las 00:33 y un total de **6**, repartido en **4 fallos y 2 éxitos**. La consulta ampliada actual contiene cuatro parejas `5760` y siete `5715` en la franja de madrugada.

**Inferencia:** si el panel contaba documentos y las seis alertas ya tenían ambas copias dentro de la misma ventana y filtros, cabría esperar 12 resultados. Los seis visibles apuntan a que las copias llegaron después de la captura, mediante un reenvío posterior. La captura no conserva una exportación de sus seis `id` ni la consulta interna del panel; no fija el momento exacto de duplicación ni identifica el componente que reenvió.

Añadí una nota a los [casos 001](../../casos/001-autenticacion-ssh.md) y [002](../../casos/002-usuario-inexistente-repetido.md): sus capturas conservan los recuentos de entonces y una consulta actual puede devolver más documentos. La ejecución original del 002, hacia las 01:02–01:03, coincide con las 15 parejas `5710` y la pareja `5712`. El caso 003 de las 14:13 queda fuera de la franja duplicada identificada.

## Contraste de emisión de los 68 identificadores · 26/10

Recogí los archivos reales del manager: estaban **sin comprimir**, con extensión `.json`, en `/var/ossec/logs/alerts/2026/Oct/`. Conservé sus bytes en [manager/](../../evidencias/duplicados-001/manager/) y conté cada `id` exacto de las 68 parejas en ambos archivos combinados.

| Archivo | Registros JSON leídos | IDs objetivo con una aparición |
| --- | ---: | ---: |
| `ossec-alerts-21.json` | 110 | 66 |
| `ossec-alerts-22.json` | 423 | 2 |
| Total | 533 | 68 |

**Los 68 identificadores aparecen una sola vez en los archivos del manager y dos veces en el índice.** No falta ninguno y ninguno aparece varias veces en los dos originales combinados. Contrasté además todos los campos de cada registro del manager con ambas copias indexadas: coinciden. Las copias del índice añaden `input` y `@timestamp`; no los traté como campos emitidos por el manager. Conservé el [resultado por ID y línea](../../evidencias/duplicados-001/comparacion-manager.json) y el [script reproducible](../../evidencias/duplicados-001/contrastar-manager.py).

Encontré un prefijo de **978 bytes NUL** antes del registro de la línea 67 del archivo del 21 y otro de **2.928 bytes NUL** antes del de la línea 353 del archivo del 22. Retiré únicamente esos prefijos en memoria para leer los registros; los originales permanecen intactos. Todos los registros resultantes son JSON válido. Ninguno de los 68 registros objetivo lleva un prefijo NUL. El informe registra offsets, líneas y hashes. La causa de esos bloques y una posible pérdida previa de contenido quedan sin determinar; el recuento describe los archivos conservados, no garantiza la integridad de toda la emisión histórica.

Este contraste respalda que las 68 parejas se duplicaron después de la emisión conservada del manager. Cierro el límite de las otras 67 parejas respecto a estos dos archivos; el componente y el mecanismo concretos siguen sin atribuirse.

## Efecto sobre 100100

La ampliación incluye cuatro parejas documentales `5760`, además de los éxitos y sesiones. Distingo el punto donde se duplica un dato: dos documentos con el mismo `id` de alerta y `_source` idéntico representan una alerta repetida en el índice; duplicar líneas antes del análisis puede generar una nueva correlación. Considero poco probable que la repetición documental posterior a la emisión infle por sí misma el contador de `100100`. El contraste de los dos archivos históricos respalda una única emisión conservada para cada una de las 68 alertas, incluidas las cuatro `5760`. Así sitúo estas copias después de la correlación en el alcance revisado; los prefijos NUL y la cobertura histórica quedan documentados aparte.

La [prueba sintética de duplicados](../../validaciones/caso-003-auth-log/evidencias/duplicados-logtest/) evalúa otro punto: duplicar entradas antes de analizarlas. Con dos fallos repetidos dos veces y un éxito, logtest activa `100100`; sin repetición termina en `5715`. La mantengo como control de robustez de prioridad baja.

## Límites

- La consulta inicial exporta campos seleccionados; la ampliada conserva `_source` completo para las 68 parejas. Contrasté todos los campos presentes en los 68 registros del manager con ambas copias indexadas. Los archivos contienen dos prefijos NUL, tratados solo en memoria; su causa y una posible pérdida previa quedan indeterminadas. El contraste abarca estos dos archivos, no todos los posibles archivos históricos.
- Verifiqué ambas copias completas de los 68 grupos de `id` repetido y contrasté las nueve parejas del CSV. El alcance depende de los índices retenidos y accesibles a la cuenta el 26/10; agrupar por `id` no busca todas las formas posibles de duplicación entre IDs diferentes.
- La retención disponible de Filebeat impide confirmar la causa histórica. Tampoco asigno la duplicación a rotación del journal ni a los errores del conector de inventario.
- Comprobé `keepfiles: 7` en el extracto de `filebeat.yml` del 26/10. `rotateonstartup` no aparece en ese extracto; su [valor predeterminado en 7.10.2](https://github.com/elastic/beats/blob/v7.10.2/libbeat/logp/config.go#L63-L72) es `true`. Los ocho archivos y sus inicios encajan con esa política. No audité los argumentos del servicio ni el historial de borrado. Para futuras pruebas copiaré los logs al terminar cada sesión; ampliar `keepfiles` es otra mejora, todavía sin aplicar.
- Confirmé duplicación documental de cuatro alertas `5760`; la duplicación de entradas antes de correlacionar y un posible falso positivo histórico de `100100` siguen sin demostrarse. Las dos parejas de las 20:38 tienen como candidato un reenvío tras el `_bulk` con `EOF` durante la parada; el contenido del lote y su reenvío siguen sin verificar.

## Decisión

Cierro la ampliación con **68 parejas documentales confirmadas y causa histórica indeterminada**. Las nueve parejas del CSV están verificadas y conservé consultas, respuestas, comparación, logs y hashes. No cambié el XML, no borré documentos y no apliqué contención. Una reproducción futura con registros completos permitiría comprobar el mecanismo; el `EOF` al apagar y la captura inicial orientan las hipótesis, sin resolver el vacío de madrugada. Los 68 `id` tienen una sola aparición en los dos archivos conservados del manager; el contraste de emisión queda completado con el límite de los prefijos NUL documentado.

## Parejas del CSV histórico

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
