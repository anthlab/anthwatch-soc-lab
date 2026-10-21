# Procedimiento N1 · Alertas de autenticación SSH

[Volver al README](../../README.md)

**Versión:** 1.1 · 22/10/2026.  
**Tipo:** procedimiento manual propuesto para el laboratorio.  
**Validación:** aplicado retrospectivamente a las evidencias del [caso 001](../casos/001-autenticacion-ssh.md) y ampliado con el [caso 002](../casos/002-fuerza-bruta-ssh.md). No es una automatización de respuesta.

## Objetivo

Determinar qué ocurrió, si el acceso es esperado y si hay información suficiente para cerrar la alerta o escalar la investigación. Un fallo seguido de un éxito requiere contexto; no demuestra por sí solo una intrusión.

## 1. Registrar la alerta

Crear un ticket con identificador, fecha, fuente y analista. Anotar el agente, el usuario, la IP de origen, la hora, la regla y su nivel. Adjuntar el registro original y el intervalo temporal de búsqueda. Separar la prioridad del ticket del nivel numérico de la regla.

Para el escenario actual, el destino esperado es `anthwatch-server` (`192.168.56.102`). El portátil de administración y `anthwatch-client` pueden generar conexiones distintas: no atribuir todas al mismo origen.

## 2. Comprobar el contexto y las evidencias

En **Threat Hunting → Events**, buscar por agente y por servicio:

```text
agent.name:"anthwatch-server" AND rule.groups:sshd
```

Para revisar las dos reglas ya observadas en este laboratorio y el origen del caso 001:

```text
agent.name:"anthwatch-server" AND data.srcip:"192.168.56.101" AND (rule.id:5760 OR rule.id:5715)
```

La segunda consulta es específica de este caso; no cubre todas las reglas ni todos los posibles errores SSH.

Revisar los siguientes datos en cada evento relevante:

| Campo | Qué comprobar |
| --- | --- |
| `agent.name`, `agent.ip` | Equipo que genera el registro |
| `data.srcip`, `data.srcport` | Origen y puerto de la conexión |
| `data.dstuser` o `data.srcuser` | Cuenta utilizada; revisar el campo que haya poblado el decodificador y contrastarlo con `full_log` |
| `rule.id`, `rule.description`, `rule.level` | Detección aplicada |
| `timestamp`, `full_log` | Hora mostrada y mensaje original |
| `location`, `decoder.name` | Fuente y decodificador |

Ampliar la búsqueda alrededor del evento para localizar fallos y éxitos del mismo origen y usuario. Para revisar el caso 001, usar un intervalo absoluto que incluya el 22/10/2026 de 00:25 a 00:45 en la zona horaria que mostraban las capturas. El filtro relativo de los últimos 15 minutos dejará de incluirlo conforme pase el tiempo.

Anotar las zonas horarias antes de comparar marcas de tiempo. No interpretar `rule.firedtimes` ni los contadores generales como intentos exactos de una única conexión. Conservar una exportación si está disponible y distinguirla de una transcripción desde una captura.

### Correlación de usuario inexistente

Para revisar la detección del caso 002:

```text
agent.name:"anthwatch-server" AND data.srcip:"192.168.56.101" AND rule.id:5712
```

La regla instalada tiene `frequency="8"`, `timeframe="120"`, `if_matched_sid` `5710`, misma IP e `ignore="60"`. Revisar `previous_output` cuando aparezca. No interpretar ocho eventos como ocho conexiones. Buscar el caso en un intervalo que incluya el 22/10/2026 a las 01:03 del dashboard; para el control, revisar 01:21–01:27.

Un control sin nueva alerta solo prueba el resultado observado en esa ventana; no demuestra por sí mismo ausencia general de falsos positivos. Para la revisión, distinguir una detección correcta de una actividad autorizada de una detección incorrecta.

## 3. Clasificar y priorizar

Preguntas para el análisis inicial:

- ¿La IP corresponde a un equipo esperado y quién lo utilizaba?
- ¿La cuenta está autorizada para acceder a ese servidor?
- ¿Los fallos encajan con un error al escribir o una prueba conocida?
- ¿Hay un acceso correcto posterior y está autorizado?
- ¿La cuenta tiene privilegios relevantes o el activo es crítico?
- ¿Existe evidencia de actividad posterior sospechosa? Si no se ha revisado, anotarlo como pendiente.

| Hallazgo | Decisión propuesta |
| --- | --- |
| Simulación documentada, origen y usuario esperados | Prioridad baja; cerrar como actividad autorizada tras conservar evidencias |
| Fallos sin explicación suficiente | Mantener abierto, comprobar contexto y valorar escalado |
| Acceso correcto desde origen inesperado o negado por el usuario | Elevar prioridad y escalar a N2 |
| Actividad posterior sospechosa o posible afectación de una cuenta privilegiada | Escalar con urgencia según el procedimiento de la organización |

Estas prioridades son una propuesta del laboratorio, no un SLA empresarial. Los fallos y el éxito pueden ser eventos correctamente detectados de actividad benigna; no se etiquetan automáticamente como falsos positivos.

## 4. Escalar cuando corresponda

Entregar a N2 el origen y destino, la cuenta, el intervalo y zona horaria, los eventos, una cronología, el impacto conocido, las comprobaciones realizadas y las dudas pendientes. Indicar por qué no se puede cerrar el caso y qué investigación se solicita.

No bloquear IPs, deshabilitar cuentas ni cerrar sesiones por defecto. Cualquier contención debe seguir la autorización y el procedimiento definidos para el entorno.

## 5. Cerrar y conservar evidencias

Registrar el motivo de cierre, la clasificación, las acciones realizadas y las limitaciones. Distinguir entre una actividad autorizada, una alerta incorrecta y un incidente confirmado.

En el caso 001 se observó el fallo `5760` y el acceso correcto `5715`, con el origen y usuario de la prueba. Se cierra como actividad autorizada; no se afirma detección automática de fuerza bruta ni compromiso de cuenta.

Ejemplos de tickets: [SOC-001](../tickets/SOC-001.md) y [SOC-002](../tickets/SOC-002.md).
