# Triaje de varias fuentes en Anthwatch

[Procedimiento SSH](ssh-autenticacion.md) · [Hunt SSH y sudo](../hunts/001-ssh-y-sudo.md)

Uso este procedimiento para ampliar el análisis cuando aparecen eventos de autenticación, comandos privilegiados, cuentas, archivos o aplicaciones en una misma ventana. Recoge lo aprendido al analizar una cola sintética de clase y las pruebas de Anthwatch.

1. Registrar el agente, la regla, el nivel, el mensaje completo y las zonas horarias. Mantener la marca original y expresar la cronología en una zona común.
2. Agrupar por equipo, cuenta, IP y proximidad temporal. Revisar también los eventos sin IP de origen, entre ellos FIM, sudo y altas de cuentas.
3. Contrastar el historial de acceso con los comandos y cambios posteriores. Usar PID, terminal, sesión y registros de procesos cuando estén disponibles.
4. Asignar prioridad según el posible impacto y los indicios de acceso conseguido. Una alerta de nivel alto puede corresponder a una prueba autorizada.
5. Separar los hechos documentados de las hipótesis que necesitan comprobación. Anotar la evidencia que falta y la consulta que permitiría obtenerla.
6. Conservar la exportación, las capturas y un manifiesto de integridad junto al informe o ticket.

## Aplicación al laboratorio

| Situación | Evidencia a revisar | Decisión que permite apoyar |
| --- | --- | --- |
| Fallos SSH seguidos de éxito | Caso 003, IP, cuenta, historial y autorización | Investigar el acceso y su actividad posterior |
| Sudo o creación de cuentas | Caso 005, usuario, comando, PID y terminal | Identificar cambios y contrastar quién los autorizó |
| Cambio de archivo | Ruta, hashes, tamaño y modo de FIM del caso 005 | Comparar versiones y buscar el proceso que escribió el archivo |
| Exportación externa | Cuenta, IP, volumen y autorización del caso 004 | Priorizar una posible exposición de datos |
| Alertas repetidas | ID, contenido y contraste con el manager del hunt | Evaluar si representan acciones distintas o copias documentales |

## Ejemplos de criterio

La exportación del director en el escenario del portal era un benigno esperado por su autorización. El acceso de `lucia` tras los fallos y la exportación de 4812 registros justificaban investigar un posible compromiso.

En el caso 005, los PID y tiempos distinguieron dos ciclos de creación y borrado de `ic-prueba`. Las alertas FIM demostraron los cambios del archivo. La atribución a una sesión concreta exige correlacionar esos datos con registros adicionales.

Al reproducir registros históricos con logtest, anotar que la ventana temporal depende del procesamiento. El caso 004 muestra cómo una segunda alerta de ráfaga puede aparecer al enviar el fichero completo aunque la cronología original contenga menos fallos dentro del umbral.

## Cierre o escalado

Documentar el motivo de la clasificación, las comprobaciones pendientes y la acción propuesta. Una escalada puede solicitar autorización del cambio, registros de sesión, contenido y hashes del archivo o logs de acceso de la aplicación. Registrar cualquier medida de contención que llegue a ejecutarse y su resultado.
