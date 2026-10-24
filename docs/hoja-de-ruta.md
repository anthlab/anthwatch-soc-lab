# Hoja de ruta · Detección e investigación

[Volver al README](../README.md)

**Actualización:** 24/10/2026. Documenté los casos 001–003 y el primer hunt; conservé los originales de la prueba SSH/sudo, los CSV históricos, las capturas y la revalidación real con auth.log.

## Completado

- [Caso 001](casos/001-autenticacion-ssh.md): eventos SSH y revisión manual.
- [Caso 002](casos/002-usuario-inexistente-repetido.md): correlación y control contrastado con journal.
- [Caso 003](casos/003-ssh-fallos-seguidos-de-exito.md): regla propia y prueba real original.
- [Revalidación real con auth.log](validaciones/caso-003-auth-log/README.md): corrección de rsyslog y tres fallos seguidos de éxito, con extractos y capturas.
- [Controles del 24/10](casos/003-revalidacion.md): XML equivalente; positivo, identidad y expiración. Distingo 130,003 s declarados por el generador de 132,122 s entre las marcas externas.
- [Hunt 001](hunts/hunt-001/README.md): secuencia controlada, 120 filas de accesos/sesiones e inventario ampliado a 28 comandos sudo, incluidos los dos `5403` que mi filtro inicial excluía.

## Siguiente prioridad

1. Recoger Filebeat del 22/10 00:27–01:15 en `anthwatch-wazuh` y exportar ambos documentos con `_id`, `_index` e `id` de alerta. Contrastar la [hipótesis de reintentos](hunts/hunt-001/repeticiones-exportacion.md); no darla por confirmada por los errores del conector del manager.
2. Ampliar telemetría de procesos y atribución por sesión para contrastar SSH, sudo y actividad posterior con controles legítimos.
3. Repetir el control temporal conservando el generador y mediciones monotónicas para explicar la diferencia de 2,119 s, manteniendo el resultado actual fuera de la ventana de 120 s.

## Prioridad baja · Robustez de correlación

Conservé la prueba sintética de fallos duplicados. No la considero evidencia de duplicación de fallos en producción. Es poco probable que copias generadas después de la correlación inflen su contador; debo verificar el punto de duplicación. Ampliaré los controles de aislamiento entre agentes, ráfagas, pérdida y reordenación cuando el alcance lo requiera. No he medido una tasa general de falsos positivos.

## Ampliaciones posteriores

Practicaré FIM e inventario de paquetes con evidencias de cambios concretos, usuarios y nuevas hipótesis. Usaré Python para tareas repetidas que aparezcan durante la investigación.

Windows permanece aplazado por los 16 GB de RAM del portátil. Mantengo las tres máquinas Ubuntu. [Estado y arquitectura](estado-del-laboratorio.md).
