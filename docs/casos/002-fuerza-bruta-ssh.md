# Caso 002 · Correlación de intentos SSH con usuario inexistente

[Volver al README](../../README.md)

**Fecha:** 22/10/2026, según el dashboard.  
**Estado:** detección correlacionada y control posterior observados.  
**Clasificación:** simulación autorizada en el laboratorio.  
**Resultado:** alerta `5712`, nivel 10, y eventos individuales `5710` sin nueva `5712` en la ventana de control.

## Objetivo y alcance

Comprobar si Wazuh detecta actividad SSH repetida desde el mismo origen contra una cuenta inexistente y comparar el resultado con una prueba posterior de menor volumen.

| Componente | Dirección | Función |
| --- | --- | --- |
| `anthwatch-client` | `192.168.56.101` | Origen de los intentos |
| `anthwatch-server` | `192.168.56.102` | Servidor SSH, agente `001` |
| `anthwatch-wazuh` | `192.168.56.103` | Manager, indexador y dashboard |

Se utilizó Wazuh 4.14.9 sobre Ubuntu Server 24.04.5 LTS. La cuenta de la prueba fue `soc_prueba_inexistente`. Los registros de SSH la identifican como usuario no válido. Es un escenario distinto del [caso 001](001-autenticacion-ssh.md), que utilizó la cuenta existente `anthlab`.

## Regla revisada

En la terminal de `anthwatch-wazuh` se consultó la regla instalada:

```bash
sudo grep -n -A 15 -B 3 'id="5712"' /var/ossec/ruleset/rules/0095-sshd_rules.xml
```

La captura muestra estos parámetros:

| Parámetro | Valor y significado |
| --- | --- |
| ID | `5712` |
| Nivel | `10` |
| `if_matched_sid` | `5710`: eventos de acceso con usuario inexistente |
| `frequency` | `8`: umbral de eventos coincidentes |
| `timeframe` | `120` segundos |
| `same_source_ip` | Los eventos deben compartir IP de origen |
| `ignore` | `60` segundos tras activarse, para limitar repeticiones |
| MITRE | `T1110` — Brute Force |

![Regla 5712 consultada en el manager](../capturas/ssh-regla-5712.png)

El umbral corresponde a eventos de log. No equivale necesariamente a ocho conexiones ni a ocho contraseñas: una conexión puede generar un registro de usuario inválido y otro de contraseña rechazada. La regla mostrada no exige mediante `same_user` que el usuario sea siempre el mismo.

## Procedimiento

### 1. Prueba de actividad repetida

Se indicó comprobar en `anthwatch-server` que la cuenta no existía:

```bash
getent passwd soc_prueba_inexistente
```

No se conserva la salida de ese comando. El mensaje posterior `invalid user` aporta evidencia de que SSH trató la cuenta como inexistente en el momento de los eventos.

En `anthwatch-client` se ejecutó este bloque, introduciendo una contraseña inventada en cada solicitud:

```bash
for intento in {1..8}; do
  ssh -o PubkeyAuthentication=no       -o PreferredAuthentications=password       -o NumberOfPasswordPrompts=1       soc_prueba_inexistente@192.168.56.102
done
```

La terminal muestra ocho solicitudes de contraseña y ocho resultados `Permission denied (publickey,password).`.

![Ocho conexiones de prueba desde el cliente](../capturas/ssh-fuerza-bruta-terminal.png)

### 2. Consulta de la alerta correlacionada

En **Threat Hunting → Events** se buscó:

```text
agent.name:"anthwatch-server" AND rule.id:5712
```

Al abrir el documento se verificaron el origen, el agente, el usuario, la regla y los mensajes anteriores incluidos en `previous_output`.

### 3. Control posterior de menor volumen

Se indicó esperar más de dos minutos desde el último intento y ejecutar una sola conexión con una contraseña inventada:

```bash
ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password -o NumberOfPasswordPrompts=1 soc_prueba_inexistente@192.168.56.102
```

La evidencia conservada del control es la consulta posterior en el dashboard. Contiene cuatro registros repartidos en dos pares temporales; no permite certificar que solo se ejecutara una conexión. Por eso se documenta como control posterior de menor volumen, sin equiparar cuatro registros con cuatro conexiones.

Se consultó el intervalo de los últimos cinco minutos con:

```text
agent.name:"anthwatch-server" AND data.srcip:"192.168.56.101" AND rule.groups:sshd
```

## Resultados y evidencias

### Alerta correlacionada

| Campo observado | Valor |
| --- | --- |
| `timestamp` mostrado | 22/10/2026 01:03:03.138 |
| `agent.name` / `agent.ip` | `anthwatch-server` / `192.168.56.102` |
| `data.srcip` | `192.168.56.101` |
| `data.srcuser` | `soc_prueba_inexistente` |
| `rule.id` / `rule.level` | `5712` / `10` |
| `rule.frequency` | `8` |
| `rule.firedtimes` | `1` en el documento examinado |
| `rule.description` | `sshd: brute force trying to get access to the system. Non existent user.` |
| `location` / `decoder.name` | `journald` / `sshd` |
| `rule.mitre.id` | `T1110` |

Fragmento de `full_log` transcrito de la captura:

```text
Oct 21 23:02:56 anthwatch-server sshd[2537]: Failed password for invalid user soc_prueba_inexistente from 192.168.56.101 port 40208 ssh2
```

![Detalle de la alerta 5712 de nivel 10](../capturas/ssh-fuerza-bruta-detalle.png)

El campo `previous_output` contiene registros anteriores de usuario inválido y contraseña rechazada. Parte de ese campo queda fuera de la zona visible de la captura, por lo que no se transcribe una secuencia completa de ocho eventos ni se atribuye la activación a la octava conexión del bucle.

### Control posterior

La captura conserva la ventana **22/10/2026 01:21:05.645–01:26:05.645**, según el dashboard. Aparecen cuatro resultados, todos de la regla `5710`, nivel 5:

| Hora aproximada mostrada | Regla | Descripción |
| --- | --- | --- |
| 01:23:43 | `5710` | Intento de acceso con usuario inexistente |
| 01:23:46 | `5710` | Intento de acceso con usuario inexistente |
| 01:24:24 | `5710` | Intento de acceso con usuario inexistente |
| 01:24:28 | `5710` | Intento de acceso con usuario inexistente |

Los milisegundos de las filas aparecen truncados. No se observa una nueva `5712` en esa consulta, que sí incluye todos los eventos SSH del agente y origen indicados en el intervalo.

![Control posterior con cuatro eventos 5710 y ninguna nueva 5712](../capturas/ssh-control-sin-correlacion.png)

## Análisis y límites

La alerta `5712` confirma una correlación automática de eventos de usuario inexistente desde el mismo origen. Esta capacidad amplía la detección de eventos individuales ya validada en el caso 001.

El control posterior muestra registros individuales sin una nueva alerta correlacionada en la ventana consultada. Es compatible con actividad por debajo del umbral, pero no constituye una medición de la tasa de falsos positivos ni demuestra el comportamiento de todos los casos posibles. Tampoco es una prueba independiente del valor exacto del umbral: ese valor se verificó en la configuración y en los metadatos de la alerta.

La alerta representa correctamente el patrón simulado. Se distingue una detección válida de actividad de prueba de una alerta incorrecta. El nivel 10 es el nivel de la regla; la prioridad operativa requiere valorar también el contexto.

No hubo acceso correcto con la cuenta ficticia en las evidencias examinadas. No se demuestra compromiso de cuenta ni acceso no autorizado al servidor. Las evidencias son capturas; no se conserva una exportación completa ni se confirma el número de conexiones que generó los cuatro eventos del control.

El mensaje original utiliza las 23:02 del día anterior y el dashboard las 01:03. Hay un desfase compatible con UTC y Europe/Madrid y unos segundos de diferencia entre el registro original y el evento. No se confirmó la configuración horaria exacta y no se interpreta ese desfase como dos horas de retraso de ingesta.

## Incidencia operativa durante la consulta

Se observó `wazuh-indexer.service` en estado `failed`. Después de reiniciar el servicio, sus registros mostraron carga de componentes con estado `activating/start`; tras dejar avanzar el arranque, se recuperó el acceso al dashboard. La causa inicial no quedó determinada. No se atribuye el fallo a la prueba SSH ni se concluye que hubo pérdida de eventos.

## Decisión N1

Se cierra como simulación autorizada con detección confirmada y control posterior documentado. No se aplicó contención ni se realizó un escalado real.

Si una secuencia similar no estuviera autorizada, se comprobarían el origen, el alcance, otras cuentas o servidores afectados y posibles accesos correctos posteriores. Se escalaría si el origen no se puede justificar, la actividad persiste o aparecen indicios de acceso no autorizado.

- [Ticket simulado SOC-002](../tickets/SOC-002.md).
- [Procedimiento N1 de análisis SSH](../playbooks/ssh-autenticacion.md).

## Siguientes pasos

Ampliar la cobertura con nuevos tipos de eventos y conservar exportaciones para futuras investigaciones. La detección de fallos seguidos de éxito con una cuenta existente sigue siendo un caso diferente y no está validada automáticamente por esta prueba.
