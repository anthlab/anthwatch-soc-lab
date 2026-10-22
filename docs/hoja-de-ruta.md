# Hoja de ruta · Detección e investigación

[Volver al README](../README.md)

**Estado:** casos 001, 002 y 003 completados. La búsqueda de threat hunting está pendiente.

## Punto de partida

- [Caso 001](casos/001-autenticacion-ssh.md): fallos y acceso correcto a una cuenta existente; análisis manual de la secuencia.
- [Caso 002](casos/002-usuario-inexistente-repetido.md): correlación automática de intentos con usuario inexistente; control adicional de una conexión contrastado entre journal y Wazuh.
- [Caso 003](casos/003-ssh-fallos-seguidos-de-exito.md): regla propia `100100` validada con logtest y SSH real, con controles documentados.

La siguiente fase utiliza las evidencias para investigar una hipótesis. El montaje completo se conserva en [estado-del-laboratorio.md](estado-del-laboratorio.md).

## Detección propia completada

El caso 003 incluye la regla versionada, los registros de muestra, las pruebas positivas y negativas, una simulación real y el ticket SOC-003. Se detectaron tres fallos seguidos de éxito para la misma cuenta e IP en 23 segundos. Los límites de validación están recogidos en el informe.

## Siguiente prioridad · Búsqueda a partir de una hipótesis

### Hipótesis propuesta

«Si una cuenta se utiliza sin autorización tras varios fallos SSH, podrían observarse un acceso correcto desde un origen inusual y actividad posterior de reconocimiento o elevación de privilegios».

La hipótesis orienta la búsqueda; no se da por demostrada ni se parte exclusivamente de una alerta.

### Investigación prevista

1. Definir el intervalo, los equipos, las cuentas y qué se considerará un origen habitual en el laboratorio.
2. Inventariar qué registros llegan realmente: SSH, sesiones, `sudo` y, si se dispone de ella, telemetría de comandos o procesos. La cobertura de estas últimas fuentes debe comprobarse; no se presupone.
3. Formular consultas que relacionen usuario, IP, destino y tiempo. Conservar también las búsquedas sin resultados y sus filtros.
4. Contrastar una secuencia de prueba con actividad administrativa legítima y documentar por qué se mantiene o descarta la sospecha.
5. Redactar hallazgos, evidencias contradictorias, visibilidad que falta y próximos pasos. La ausencia de un registro no prueba ausencia de actividad si esa fuente no se está recogiendo.

### Entregables

Hipótesis, inventario de fuentes, consultas reproducibles, cronología, conclusión y posibles mejoras de detección. El informe será una búsqueda guiada por una pregunta, con resultado abierto a confirmar o rechazar la hipótesis.

## Ampliaciones posteriores

Windows queda aplazado: el portátil tiene 16 GB de RAM y no se añadirá otra VM en esta fase. La búsqueda se realizará con las tres máquinas Ubuntu existentes. Ampliar telemetría de procesos, integridad de archivos y visibilidad de red según lo que requieran los casos. Utilizar Python para automatizar tareas concretas que aparezcan durante las investigaciones.
