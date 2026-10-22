# Registros de muestra · Caso 003

[Informe](../../docs/casos/003-ssh-fallos-seguidos-de-exito.md) · [Regla](../../rules/anthwatch_ssh_rules.xml)

Estos registros son sintéticos y reproducen las entradas utilizadas con `wazuh-logtest` 4.14.9. No son una exportación de eventos reales. Las IP y las horas escritas son datos del escenario.

## Cómo repetir las pruebas

En `anthwatch-wazuh`, guardar la regla en `/var/ossec/etc/rules/anthwatch_ssh_rules.xml`. Revisar que el ID `100100` no esté usado por otra regla local. Conservar una copia fuera del directorio de reglas antes de sustituir un archivo existente. No modificar las reglas de `/var/ossec/ruleset/rules/`.

Abrir `sudo /var/ossec/bin/wazuh-logtest` y pegar las líneas de un escenario, una por una. Terminar con `Ctrl+C` y abrir una sesión nueva para cada escenario independiente: el historial debe comenzar vacío. Completar las secuencias positivas y de identidad en menos de 120 segundos reales. No escribir comandos de shell dentro del prompt de logtest.

| Entrada | Resultado esperado y observado |
| --- | --- |
| `positivo.log` | `5760`, `5760`, `5760`, `100100` (nivel 10) |
| `dos-fallos.log` | `5760`, `5760`, `5715` (nivel 3) |
| `otro-usuario.log` | Tres `5760`; éxito de otra cuenta: `5715` |
| `otra-ip.log` | Tres `5760`; éxito desde otra IP: `5715` |
| `exito-solo.log` | `5715` sin `100100` |
| `fallos-sin-exito.log` | Tres `5760` sin `100100`; observado como prefijo de la prueba positiva, no como ejecución independiente |
| Archivos `fuera-ventana-*` | Tres `5760`; esperar 130 segundos reales y enviar el éxito en la misma sesión: `5715` |

Para el control temporal, pegar primero `fuera-ventana-fallos.log`, esperar 130 segundos reales desde el último fallo y pegar `fuera-ventana-exito.log` sin cerrar logtest. Cambiar únicamente la hora escrita no sustituye la espera. La captura conserva el resultado; no incluye un cronómetro ni una medición independiente de la espera.

Los resultados se conservaron mediante capturas y, para la prueba positiva, una transcripción completa de la salida compartida durante la ejecución. No se dispone de un volcado íntegro de todas las sesiones. No se ha medido una tasa general de falsos positivos ni se han probado umbrales más altos, mezcla entre agentes, reordenación, ráfagas o repetición de alertas.

La prueba positiva y el control de dos fallos validan el umbral de este escenario en la versión instalada. `frequency="4"` no se interpreta como cuatro contraseñas fallidas: la secuencia validada es tres fallos previos y un éxito actual.
