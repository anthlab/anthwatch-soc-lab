# Caso 003 — Revalidación de la regla 100100 con auth.log

- **Detecté:** la agrupación de fallos de rsyslog impedía reproducir la detección real con la nueva fuente.
- **Validé:** prueba positiva y controles negativos sintéticos; tres fallos reales seguidos de éxito disparan 100100 desde /var/log/auth.log después de desactivar la agrupación.
- **Aprendí:** una regla puede funcionar en logtest y no detectar la misma secuencia en una prueba real. En mi caso, rsyslog agrupaba los fallos y Wazuh no recibía cada intento por separado. Desde entonces, además de revisar la regla, compruebo cómo llegan los registros.

**Fecha:** 22/10/2026. **Resultado:** revalidación superada para el escenario probado. No se modificó el XML de la regla.

## Regla instalada

La captura 01 muestra `/var/ossec/etc/rules/anthwatch_ssh_rules.xml` en anthwatch-wazuh: regla 100100, nivel 10, frequency=4, timeframe=120, if_sid=5715, if_matched_sid=5760, same_srcip y same_user. No contiene filtros de location/journald. En la [recogida del 24/10](../../casos/003-revalidacion.md) conservé el XML instalado y comprobé su equivalencia con el del repositorio: solo difiere en líneas en blanco.

Comprobé el comportamiento tres fallos → éxito con las pruebas siguientes.

## Revalidación sintética

Se utilizaron líneas ISO 8601 con microsegundos y desplazamiento +02:00, como las escritas en auth.log. Cada control se ejecutó en una sesión nueva de wazuh-logtest. Estas muestras no son accesos reales y no se mezclan con los extractos del servidor.

| Prueba | Resultado observado | Captura |
|---|---|---|
| Tres Failed password para anthlab/.101 y Accepted password para anthlab/.101 | 5760 en los fallos; 100100 nivel 10 en el éxito | 02 |
| Dos fallos y éxito, misma cuenta/IP | 5715 al final; no 100100 | 03 |
| Tres fallos desde .101; éxito desde .1, mismo usuario | 5715 al final | 04 |
| Tres fallos para anthlab; éxito de otro_usuario desde .101 | 5715 al final | 05 |
| Tres fallos y éxito tras espera real de 130 segundos | 5715 al final | 06 |

El control temporal se ejecutó con un pipeline que introdujo tres fallos, esperó `sleep 130` y envió el éxito al mismo proceso. No se considera suficiente modificar las fechas de las líneas. La captura 06 acredita el resultado final; no conservé aquí el archivo de salida ni las marcas reales de la espera. Completé esa recogida el 24/10: conservé entrada, salida y tiempos del control temporal y de identidad. Distingo los 130,003 s declarados por el generador de los 132,122 s entre las marcas externas; el [informe posterior](../../casos/003-revalidacion.md) detalla la discrepancia.

## Primera prueba real: fallo de revalidación

Desde anthwatch-client se forzó autenticación password, sin reutilización de conexión (ControlPath=none), tres contraseñas incorrectas y una conexión nueva correcta. En el intervalo 19:55–19:58 se observaron dos alertas 5760 y una 5715; no 100100 en esa búsqueda (capturas 07 y 08).

El [extracto anterior a la corrección](evidencias/auth-1956-agrupado.log) muestra un Failed password individual y una línea `message repeated 2 times` que resume otros dos. No eran tres líneas independientes disponibles para la misma correlación. El resultado difiere de la entrada sintética.

## Corrección aplicada y representación horaria

Se cambió `$RepeatedMsgReduction on` por `$RepeatedMsgReduction off` en `/etc/rsyslog.conf`, tras guardar copia. `rsyslogd -N1` terminó sin errores y se reinició rsyslog; el XML de 100100 no se alteró.

La [salida real de configuración](evidencias/rsyslog-agrupacion.txt) contiene `32:$RepeatedMsgReduction off`. Los [bloques localfile extraídos del servidor](evidencias/fuentes-locales-aplicadas.txt) contienen auth.log, syslog, active-responses.log y dpkg.log, además de comandos de inventario. En este extracto no aparece un bloque journald.

El cambio previo de journald a auth.log se realizó para conservar en full_log la representación de hora local con zona explícita. Las capturas `hora-local-auth-log.png`, `hora-local-wazuh.png` y `ssh-hora-local.png` acreditan el resultado para sudo y SSH. No se corrigió un retraso demostrado del reloj: la diferencia anterior de dos horas era compatible con UTC frente a Madrid. Los eventos históricos se conservan sin reescritura.

El +02:00 corresponde a la fecha de la prueba; no es una suma fija válida todo el año. El campo timestamp de la alerta y la marca original de full_log son distintos; los tiempos de las secuencias se calculan con el segundo.

## Segunda prueba real: detección confirmada

El [extracto posterior](evidencias/auth-2007-2008-sin-agrupacion.log) contiene:

| Hora original, +02:00 | Resultado | PID/puerto |
|---|---|---|
| 20:07:49.077659 | Failed password, anthlab desde .101 | sshd[2655], puerto 52640 |
| 20:07:53.558096 | Failed password, misma cuenta/IP | sshd[2655], puerto 52640 |
| 20:07:57.321162 | Failed password, misma cuenta/IP | sshd[2655], puerto 52640 |
| 20:08:09.403719 | Accepted password, misma cuenta/IP | sshd[2657], puerto 60570 |

Duración primer fallo → éxito: **20,326060 segundos**, dentro de 120 segundos.

La captura 13 muestra tres alertas 5760 y una 100100. La captura 14 acredita nivel 10, location `/var/log/auth.log` y previous_output con los tres fallos originales. El timestamp de esa alerta es 20:08:09.697. La captura 12 y el extracto demuestran que la agrupación dejó de producirse en esta secuencia. Las capturas 10 y 11 respaldan configuración y ejecución manual.

## Prueba de sensibilidad a duplicados — 21:15 del 22/10

Ejecuté cada muestra en un proceso nuevo de wazuh-logtest y conservé las entradas, las salidas completas, las marcas de ejecución y los códigos de salida en [evidencias/duplicados-logtest/](evidencias/duplicados-logtest/). Los cuatro hashes del manifiesto original coinciden. La captura 15 muestra el resumen.

| Muestra sintética | Reglas observadas en orden | Código de salida |
|---|---|---|
| Dos fallos distintos y éxito | 5760, 5760, 5715 | 0 |
| Los mismos dos fallos, cada uno repetido exactamente dos veces, y éxito | 5760, 5760, 5760, 5760, 100100 | 0 |

Comprobé que la segunda entrada contiene exactamente las líneas 1, 1, 2, 2 y 3 de la primera, conservando sus bytes. La ejecución de control duró de 21:15:44,232034766 a 21:15:44,990983810; la duplicada, de 21:15:44,993346668 a 21:15:45,588153920, con zona +02:00. Las marcas dentro de las muestras son sintéticas y no describen accesos reales.

**Resultado:** al repetir las entradas, logtest cuenta cuatro fallos y activa `100100`. Conservé el XML y las dos salidas para mostrar esa sensibilidad. Mantengo el control con prioridad baja y sigo la [investigación de la entrega e indexación](../../hunts/hunt-001/repeticiones-exportacion.md).

## Límites

Validé el cambio en `anthwatch-server`. Quedan fuera los eventos exclusivos de journald que no se escriben en las rutas monitorizadas y la revisión completa de configuración centralizada y de las otras máquinas.

La duplicación sintética ocurre antes del análisis. El [cierre del 25/10](../../hunts/hunt-001/repeticiones-exportacion.md) confirma una pareja de documentos para la misma alerta `5715`, con una coincidencia conservada en el manager; la causa queda indeterminada por falta de Filebeat del periodo. Considero poco probable que esas copias posteriores a la emisión inflen el contador. La [ampliación del 26/10](../../hunts/hunt-001/repeticiones-exportacion.md) confirma cuatro parejas documentales `5760` entre 68 parejas. El contraste posterior encontró una sola aparición de cada uno de los 68 `id` en los dos archivos conservados del manager y campos coincidentes con ambas copias indexadas; el informe documenta los prefijos NUL y el límite de integridad histórica. La duplicación de entradas antes de analizar y un falso positivo histórico siguen sin demostrarse.

## Evidencia conservada

Los casos anteriores conservan sus evidencias y fuente originales. Esta revalidación documenta el estado posterior sin sustituirlos.

Los cuatro archivos de evidencia conservados pasan `sha256sum -c SHA256SUMS` dentro de [evidencias/](evidencias/). Desde esta carpeta, `sha256sum -c SHA256SUMS` verifica además las capturas y las evidencias del conjunto. Los manifiestos son relativos y conservan los bytes originales de los extractos.

Referencia técnica de la opción de rsyslog: https://docs.rsyslog.com/doc/configuration/action/rsconf1_repeatedmsgreduction.html

El manifiesto de esta carpeta incluye solo evidencias y capturas; editar este README no altera su verificación. Si cambia una evidencia, regeneraré el manifiesto.
