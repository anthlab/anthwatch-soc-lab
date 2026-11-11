# Hoja de ruta

[Índice de documentación](README.md)

**Actualización:** 11/11/2026. Los resultados completados están en los informes del índice. Esta página recoge las próximas prioridades.

## Siguiente prioridad

1. Ampliar la telemetría de procesos y la atribución por sesión para contrastar SSH, sudo y actividad posterior.
2. Repetir el control temporal con el generador conservado y mediciones monotónicas. El detalle actual está en la [validación del caso 003](casos/003-revalidacion.md).
3. Adaptar las redes y los orígenes autorizados del portal mediante una lista CDB y controles de cuenta, siguiendo la [mejora propuesta del caso 004](casos/004-portal-nominas.md).

## Ampliaciones posteriores

- Ampliar los controles de ráfagas, reordenación y aislamiento entre agentes.
- Reproducir los duplicados con registros completos; la causa sigue pendiente en el [anexo técnico](anexos/duplicados-indexacion.md).
- Validar inventario de paquetes y atribución de cambios a procesos. Automatizar con Python tareas repetidas de investigación.

Windows permanece aplazado por los 16 GB de RAM del portátil. Mantengo las tres VMs Ubuntu del [laboratorio](estado-del-laboratorio.md).
