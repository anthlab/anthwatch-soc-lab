# Hoja de ruta · Detección e investigación

[Volver al README](../README.md)

**Actualización:** 26/10/2026. Documenté los casos 001–003 y el primer hunt; conservé los originales de la prueba SSH/sudo, los CSV históricos, las capturas y la revalidación real con auth.log.

## Completado

- [Caso 001](casos/001-autenticacion-ssh.md): eventos SSH y revisión manual.
- [Caso 002](casos/002-usuario-inexistente-repetido.md): correlación y control contrastado con journal.
- [Caso 003](casos/003-ssh-fallos-seguidos-de-exito.md): regla propia y prueba real original.
- [Revalidación real con auth.log](validaciones/caso-003-auth-log/README.md): corrección de rsyslog y tres fallos seguidos de éxito, con extractos y capturas.
- [Controles del 24/10](casos/003-revalidacion.md): XML equivalente; positivo, identidad y expiración. Distingo 130,003 s declarados por el generador de 132,122 s entre las marcas externas.
- [Hunt 001](hunts/hunt-001/README.md): secuencia controlada, 120 filas de accesos/sesiones e inventario ampliado a 28 comandos sudo, incluidos los dos `5403` que mi filtro inicial excluía.

- [Revisión de duplicados](hunts/hunt-001/repeticiones-exportacion.md), ampliada el 26/10: 68 parejas con `_source` idéntico, incluidas las nueve del CSV y cuatro parejas `5760`. Conservé consultas, respuestas, comparación y ocho logs. Verifiqué `keepfiles: 7`; la causa histórica de madrugada queda indeterminada.

- [Contraste de emisión de los 68 IDs](hunts/hunt-001/repeticiones-exportacion.md): completado con los dos JSON del manager, recuentos por archivo y línea, comparación de campos y originales con hashes. Los dos prefijos NUL quedan documentados; su causa no se ha determinado.

## Siguiente prioridad

1. Ampliar telemetría de procesos y atribución por sesión para contrastar SSH, sudo y actividad posterior con controles legítimos.
2. Repetir el control temporal conservando el generador y mediciones monotónicas para explicar la diferencia de 2,119 s, manteniendo el resultado actual fuera de la ventana de 120 s.

## Prioridad baja · Robustez de correlación

Conservé la prueba sintética de fallos duplicados. Distingo esa prueba de la duplicación documental de cuatro alertas `5760` confirmada en el índice. Los 68 `id` aparecen una sola vez en los dos archivos conservados del manager y dos veces en el índice; todos los campos emitidos coinciden con ambas copias. El contraste respalda la duplicación posterior a la emisión, dentro de estos archivos. Documenté dos prefijos NUL, su tratamiento en memoria y el límite de integridad histórica. Considero poco probable que una copia documental posterior a la emisión infle el contador de correlación. La causa concreta sigue indeterminada. Las nueve parejas del CSV ya están verificadas. El `_bulk` con `EOF` durante la parada es un candidato para las dos parejas tardías; falta identificar el contenido del lote. La captura del caso 001 apunta a un reenvío posterior, suponiendo que el panel contaba documentos. Una reproducción con registros completos permitiría contrastar el mecanismo. Ampliaré los controles de aislamiento entre agentes, ráfagas, pérdida y reordenación cuando el alcance lo requiera. No he medido una tasa general de falsos positivos.

## Ampliaciones posteriores

Practicaré FIM e inventario de paquetes con evidencias de cambios concretos, usuarios y nuevas hipótesis. Usaré Python para tareas repetidas que aparezcan durante la investigación.

Windows permanece aplazado por los 16 GB de RAM del portátil. Mantengo las tres máquinas Ubuntu. [Estado y arquitectura](estado-del-laboratorio.md).
