# Hoja de ruta · Detección e investigación

[Volver al README](../README.md)

**Estado:** planificación. Los siguientes casos aún no están implementados ni validados.

## Punto de partida

- [Caso 001](casos/001-autenticacion-ssh.md): fallos y acceso correcto a una cuenta existente; análisis manual de la secuencia.
- [Caso 002](casos/002-fuerza-bruta-ssh.md): correlación automática de intentos con usuario inexistente y control posterior.

La siguiente fase prioriza desarrollar una detección y utilizar las evidencias para investigar una hipótesis. El montaje completo se conserva en [estado-del-laboratorio.md](estado-del-laboratorio.md).

## Prioridad 1 · Fallos seguidos de éxito con regla propia

### Pregunta

¿Podemos generar una alerta cuando varios fallos SSH de una cuenta existente van seguidos de un acceso correcto desde la misma IP y con la misma cuenta dentro de un intervalo definido?

### Diseño pendiente

1. Revisar las reglas instaladas relacionadas con los fallos y los accesos correctos. En el caso 001 se observaron `5760` y `5715`; habrá que comprobar si alguna regla base de correlación es reutilizable.
2. Definir un umbral y una ventana temporal, justificar ambos y decidir cómo mantener la asociación entre IP de origen, usuario y agente. No basta con que coincida solo la IP.
3. Preparar la regla propia y pruebas con registros de muestra. Confirmar cómo trata el motor los eventos anteriores y el orden de evaluación antes de desplegarla.
4. Validar la sintaxis y el comportamiento en el entorno de pruebas; después realizar una simulación sobre la cuenta existente del laboratorio.
5. Conservar la configuración, los registros utilizados y los resultados esperados y obtenidos. Añadir el caso 003 al índice de casos completados solo después de verificarlo.

### Matriz mínima de pruebas

| Prueba | Resultado esperado |
| --- | --- |
| Varios fallos y éxito: misma IP, usuario y agente, dentro de la ventana | Activación de la regla propia |
| Un acceso correcto sin fallos previos | Sin activación de esta regla |
| Fallos repetidos sin acceso correcto | Sin activación de esta regla; pueden activarse otras reglas |
| Fallos para un usuario y éxito para otro desde la misma IP | Sin correlación como si fuera la misma cuenta |
| Fallos y éxito desde IPs distintas | Sin correlación para este caso de uso |
| Éxito fuera de la ventana establecida | Sin activación de esta regla |

El umbral y los intervalos se decidirán al revisar el motor y los registros reales. La alerta indicará una secuencia que merece investigación; no debe declarar automáticamente que la cuenta está comprometida.

### Entregables

Regla versionada, resultados de las pruebas positivas y negativas, consulta de investigación, evidencias y ticket simulado con una decisión de cierre o escalado justificada.

## Prioridad 2 · Búsqueda a partir de una hipótesis

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

Añadir Windows y sus registros de seguridad, telemetría de procesos, integridad de archivos y visibilidad de red según lo que requieran los casos. Utilizar Python para automatizar tareas concretas que aparezcan durante las investigaciones.
