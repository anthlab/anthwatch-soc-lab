# Caso 003 · Revalidación de la regla 100100

[Caso original](003-ssh-fallos-seguidos-de-exito.md) · [Pruebas](../../tests/caso-003/README.md) · [Hunt 001](../hunts/001-ssh-y-sudo.md)

**Fecha de controles conservados:** 24/10/2026. **Motor:** `wazuh-logtest` 4.14.9.  
**Resultado:** positiva, separación de identidades y expiración temporal comprobadas en las salidas adjuntas. La lógica XML permanece igual.

## Por qué repetir la validación

Validé el caso original el 22/10/2026 a las 14:13 mediante SSH real y journald. Durante el hunt cambié la recogida a `/var/log/auth.log` y comprobé que rsyslog agrupaba mensajes repetidos. Corregí la configuración a `$RepeatedMsgReduction off` y repetí la prueba real: obtuve `100100`.

Conservé el [extracto real posterior](../validaciones/caso-003-auth-log/evidencias/auth-2007-2008-sin-agrupacion.log), los hashes, la configuración de fuentes y rsyslog y las [capturas de la revalidación real](../validaciones/caso-003-auth-log/README.md). Hay tres fallos a las 20:07:49.077659, 20:07:53.558096 y 20:07:57.321162, y éxito a las 20:08:09.403719 del 22/10 (`+02:00`): 20,326060 s del primer fallo al éxito. Las capturas 13–14 conservan `100100`, nivel 10, `location: /var/log/auth.log` y los tres fallos previos. Esta prueba real complementa los controles sintéticos del 24/10 descritos abajo.

## Correspondencia del XML

La [copia recogida del XML](../evidencias/revalidacion-003/xml-100100/anthwatch_ssh_rules.xml) tiene SHA-256 `47cc6fce529ad2915500deaf003e08a119a11f682ce1dbabfc9d72387c8930e5`. La [regla del repositorio](../../rules/anthwatch_ssh_rules.xml) conserva SHA-256 `6c94f3d31069e2fbf118f11d5cdacd13c7450bc116c9b9b26cf522bbdf9d3371`.

El [diff original](../evidencias/revalidacion-003/diferencias-xml.txt) solo añade dos líneas en blanco. Comprobé además la equivalencia de elementos, atributos y contenido XML ignorando espacios de formato. No se ha modificado el umbral ni la condición de IP o usuario.

## Resultados con entradas y salidas completas

| Control | Hora de ejecución local del 24/10 | Resultado de las cuatro líneas |
| --- | --- | --- |
| Positivo, misma cuenta e IP | 19:44:29.742738–19:44:30.334175 | `5760`, `5760`, `5760`, `100100` nivel 10 |
| Otra IP en el éxito (`.102` frente a `.101`) | 19:44:30.334700–19:44:31.463781 | `5760`, `5760`, `5760`, `5715` |
| Otro usuario en el éxito (`soc_control` frente a `anthlab`) | 19:44:31.464172–19:44:32.067026 | `5760`, `5760`, `5760`, `5715` |
| Espera mayor de 120 s en la misma sesión | 19:38:55–19:41:07 | `5760`, `5760`, `5760`, `5715` |

Las tres ejecuciones de identidad finalizan con código 0 y cada salida tiene su propio arranque de logtest. Usé muestras sintéticas con PID, puertos, direcciones y horas del escenario.

## Control temporal medido

Conservé dos medidas diferentes en `tiempos.log` y en las entradas:

| Medida | Valor y respaldo |
| --- | --- |
| Espera declarada por el generador para `sleep` | **130,003 s**, línea `ESPERA REAL` |
| Entre `ESPERA DE 130 SEGUNDOS` (19:38:55.160655) y `EXITO ENVIADO` (19:41:07.282543) | **132,121888 s** |
| Entre el último fallo de la entrada (19:38:55.160637) y el éxito (19:41:07.282485) | **132,121848 s** |

La diferencia entre la medida declarada y el intervalo externo es aproximadamente **2,119 s**. Uso **132,122 s entre las marcas de fallo y éxito** al describir el control y mantengo **130,003 s como duración declarada de la espera**, sin presentarlas como la misma medida.

Ambas cifras superan los 120 s. La salida conserva tres `5760` y un `5715`, nivel 3, sin `100100`; la conclusión de este control no cambia. Para repetirlo necesito esperar tiempo real dentro de una misma sesión de logtest, registrar el programa y medir el intervalo con reloj monotónico. Alimentar el archivo completo de golpe no reproduce la espera.

## Integridad

Conservé sin modificar las entradas, salidas, tiempos, XML y los tres `SHA256SUMS` originales. Los **11 archivos referenciados** por esos manifiestos verifican correctamente. El manifiesto XML usa una ruta absoluta del equipo original: el [README de evidencias](../evidencias/revalidacion-003/README.md) ofrece un manifiesto adicional con rutas relativas.

## Límites

Los controles del 24/10 usan entradas sintéticas. Dos fallos y éxito aislado conservan sus capturas históricas; los fallos sin éxito aparecen como prefijo de las positivas. En esta revisión comprobé salidas, hashes y equivalencia XML, sin volver a ejecutar Wazuh.

Falta el generador y una medición monotónica para explicar los 2,119 s del control temporal. Quedan sin validar aislamiento entre agentes, ráfagas, reordenación, pérdida de eventos y tasa general de falsos positivos. Conservé también la [prueba sintética de entradas duplicadas](../validaciones/caso-003-auth-log/README.md), de prioridad baja; el efecto de las repeticiones históricas sobre la correlación sigue sujeto a la investigación de ingesta.

## Decisión

Mantengo la regla `100100` y documento la corrección de la fuente de logs. El control temporal ahora dispone de tiempos registrados con la discrepancia explicada y las condiciones de identidad cuentan con salidas completas.
