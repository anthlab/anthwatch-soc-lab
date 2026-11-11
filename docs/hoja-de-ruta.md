# Hoja de ruta · Detección e investigación

[Volver al README](../README.md)

**Actualización:** 11/11/2026. Documenté cinco casos (001–005), el hunt de SSH y sudo y los procedimientos de comprobación operativa y triaje. Conservé registros, capturas y manifiestos de integridad.

## Completado

- [Caso 001](casos/001-autenticacion-ssh.md): eventos SSH y revisión manual.
- [Caso 002](casos/002-usuario-inexistente-repetido.md): correlación y control contrastado con journal.
- [Caso 003](casos/003-ssh-fallos-seguidos-de-exito.md): regla propia y prueba real original.
- [Caso 004](casos/004-portal-nominas.md): decodificación de un registro de aplicación, correlación por IP y prueba en vivo.
- [Revalidación real con auth.log](validaciones/caso-003-auth-log/README.md): corrección de rsyslog y tres fallos seguidos de éxito, con extractos y capturas.
- [Controles del 24/10](casos/003-revalidacion.md): XML equivalente; positivo, identidad y expiración. Distingo 130,003 s declarados por el generador de 132,122 s entre las marcas externas.
- [Hunt 001](hunts/hunt-001/README.md): secuencia controlada, 120 filas de accesos/sesiones e inventario ampliado a 28 comandos sudo, incluidos los dos `5403` que mi filtro inicial excluía.

- [Anexo de duplicados](anexos/duplicados-indexacion.md). Contraste de emisión e indexación de 68 alertas.

- [Caso 005](casos/005-fim-usuarios-sudo.md). FIM en tiempo real y ciclo de usuarios contrastados con 32 alertas de Anthwatch.

## Siguiente prioridad

1. Ampliar telemetría de procesos y atribución por sesión para contrastar SSH, sudo y actividad posterior con controles legítimos.
2. Repetir el control temporal conservando el generador y mediciones monotónicas para explicar la diferencia de 2,119 s, manteniendo el resultado actual fuera de la ventana de 120 s.

## Prioridad baja · Robustez de correlación

- La revisión de 68 alertas respalda una duplicación posterior a la emisión del manager.
- Queda reproducir la causa con registros completos y ampliar los controles de ráfagas, reordenación y aislamiento entre agentes.
- El [anexo técnico](anexos/duplicados-indexacion.md) conserva los límites, los prefijos NUL y la hipótesis de reenvío de Filebeat.

## Ampliaciones posteriores

La creación, modificación y eliminación de archivos y el ciclo de cuentas están documentados en el caso 005. Queda ampliar la validación del inventario de paquetes y la atribución de cambios a procesos. Usaré Python para tareas repetidas que aparezcan durante la investigación.

Windows permanece aplazado por los 16 GB de RAM del portátil. Mantengo las tres máquinas Ubuntu. [Estado y arquitectura](estado-del-laboratorio.md).
