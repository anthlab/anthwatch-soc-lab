# Evidencias originales y configuración horaria

## Archivos originales del laboratorio

| Archivo | Procedencia y contenido |
| --- | --- |
| [caso-002-control-journal.txt](caso-002-control-journal.txt) | Exportación de `journalctl -u ssh --output=short-iso`, guardada en `anthwatch-server` y copiada mediante SCP |
| [horas-anthwatch-wazuh.txt](horas-anthwatch-wazuh.txt) | `hostname`, `timedatectl` y fecha ISO de `.103`, 22/10/2026 16:43:45 CEST |
| [horas-anthwatch-server.txt](horas-anthwatch-server.txt) | Mismos comandos en `.102`, 22/10/2026 16:43:48 CEST |
| [horas-anthwatch-client.txt](horas-anthwatch-client.txt) | Mismos comandos en `.101`, 22/10/2026 16:43:51 CEST |

La [captura de exportación](../capturas/002-control-journal-exportacion.png) y la [lectura del archivo](../capturas/002-control-journal-texto.png) documentan la recogida del journal en el servidor.

## Estado horario verificado

Las tres salidas confirman **Europe/Madrid (CEST, +0200)**, **System clock synchronized: yes**, **NTP service: active** y RTC en UTC (`RTC in local TZ: no`). Las recogidas se ejecutaron sucesivamente entre 16:43:45 y 16:43:51; esos segundos distintos corresponden a momentos de consulta distintos.

La configuración horaria de las VMs se ajustó antes del caso 003 y queda documentada en texto en esta recogida posterior. Las capturas anteriores al ajuste conservan sus marcas originales.

## Representación horaria de journald en Wazuh 4.14.9

En Wazuh **4.14.9**, la función [`w_timestamp_to_string`, líneas 100–110](https://github.com/wazuh/wazuh/blob/v4.14.9/src/logcollector/journal_log.c#L100-L110), convierte la marca del journal con **`gmtime_r`, línea 103**, y la formatea con `strftime` como `%b %d %T`, línea 109. La función [`entry_as_syslog`, líneas 554–563](https://github.com/wazuh/wazuh/blob/v4.14.9/src/logcollector/journal_log.c#L554-L563), llama a ese conversor en la **línea 563**. Por esta ruta, el mensaje se construye en UTC sin sufijo de zona.

El comportamiento también se contrasta en las evidencias de los casos 002 y 003:

| Evidencia | Hora en el mensaje de Wazuh (UTC) | Hora local de Europe/Madrid |
| --- | --- | --- |
| Control adicional del caso 002 | `14:19:47` en `full_log` | `16:19:47+02:00` en el journal original |
| Acceso correcto del caso 003 | `12:13:03` en `full_log` | `14:13:03 CEST` en la terminal |

Los valores representan los mismos instantes. La diferencia de dos horas responde al formato UTC del colector y la presentación local; no es un retraso de ingesta de dos horas. Los tres archivos de `timedatectl` confirman por separado la configuración y sincronización actuales de las VMs.

## Contraste del control 002

La [vista general de Wazuh](../capturas/002-control-eventos-dashboard.png) conserva la consulta de agente, origen y grupo SSH, el filtro del manager y la ventana **22/10/2026 16:13:38.269–16:25:38.269**. Devuelve dos `5710`, nivel 5, a las **16:19:38.049** y **16:19:48.059**, sin `5712`.

El [detalle del fallo](../capturas/002-control-evento-detalle.png) y el journal coinciden en cuenta, origen, proceso `2044` y puerto `34332`. El inicio, fallo y cierre se atribuyen a una conexión. El procedimiento y el resultado completos están reunidos en el [caso 002](../casos/002-usuario-inexistente-repetido.md#repetir-el-control); el ticket y el playbook remiten a ese informe.

## Reproducir la recogida

Desde el portátil de administración, los siguientes comandos recogen el estado horario por SSH y copian el journal por SCP. Las direcciones y el usuario corresponden a este laboratorio. Cada ejecución utiliza una carpeta nueva e imprime su ruta al terminar.

```bash
(
set -e
salida=$(mktemp -d "${TMPDIR:-/tmp}/anthwatch-evidencias.XXXXXX")

for entrada in \
  anthwatch-wazuh:192.168.56.103 \
  anthwatch-server:192.168.56.102 \
  anthwatch-client:192.168.56.101
do
  equipo=${entrada%%:*}
  ip=${entrada#*:}
  ssh "anthlab@$ip" \
    'hostname && timedatectl && date --iso-8601=seconds' \
    > "$salida/horas-$equipo.txt"
done

scp anthlab@192.168.56.102:caso-002-control-journal.txt \
  "$salida/caso-002-control-journal.txt"
printf 'Evidencias guardadas en: %s\n' "$salida"
)
```

El journal copiado es el archivo del control ya generado en el servidor. Para crear un control nuevo, seguir [Repetir el control](../casos/002-usuario-inexistente-repetido.md#repetir-el-control).
