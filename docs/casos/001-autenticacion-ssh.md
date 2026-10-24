# Caso 001 · Fallos de autenticación SSH y acceso correcto

[Volver al README](../../README.md)

Detecté fallos de contraseña y un acceso SSH correcto desde el cliente al servidor.  
Validé la recepción en Wazuh con las reglas `5760` y `5715` y revisé sus campos de origen y cuenta.  
Aprendí a reconstruir una secuencia y justificar el cierre N1 con el contexto del laboratorio.

**Fecha:** 22 de octubre de 2026, según el dashboard.  
**Estado:** prueba controlada completada; recogida de eventos SSH validada.  
**Clasificación:** actividad autorizada del laboratorio.  
**Prioridad del caso:** baja, por tratarse de una simulación conocida.

## Objetivo y alcance

Quería comprobar que los registros SSH de `anthwatch-server` llegaban a Wazuh y que podía distinguir un fallo de un acceso correcto, con su origen y usuario.

Desde `anthwatch-client` introduje una contraseña incorrecta tres veces. Después abrí otra conexión con la contraseña correcta. Usé `anthlab` en ambas conexiones.

| Componente | Dirección | Papel |
| --- | --- | --- |
| `anthwatch-client` | `192.168.56.101` | Origen de las conexiones SSH |
| `anthwatch-server` | `192.168.56.102` | Servidor SSH monitorizado, agente `001` |
| `anthwatch-wazuh` | `192.168.56.103` | Recepción, análisis y consulta de los eventos |

El entorno utiliza Ubuntu Server 24.04.5 LTS y Wazuh 4.14.9. Los eventos examinados indican `location: journald` y el decodificador `sshd`.

## Procedimiento realizado

### 1. Intentos con contraseña incorrecta

En la terminal de `anthwatch-client` ejecuté:

```bash
ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password -o NumberOfPasswordPrompts=3 anthlab@192.168.56.102
```

Introduje una contraseña incorrecta en las tres solicitudes. La terminal mostró dos mensajes `Permission denied, please try again.` y terminó con `Permission denied (publickey,password).`, devolviendo el control a la consola del cliente.

![Tres solicitudes de contraseña rechazadas desde anthwatch-client](../capturas/ssh-intentos-fallidos-terminal.png)

### 2. Búsqueda en Wazuh

En **Threat Hunting** seleccioné los últimos 15 minutos y apliqué este filtro:

```text
agent.name:"anthwatch-server" AND rule.groups:sshd
```

El panel mostró seis eventos: cuatro fallos y dos accesos correctos. Para entender qué correspondía a la prueba, abrí el detalle de los registros.

![Vista general de eventos SSH en Wazuh](../capturas/ssh-eventos-dashboard.png)

En **Events** revisé un fallo reciente. Comprobé el origen `192.168.56.101`, el destino monitorizado `anthwatch-server` y el usuario `anthlab`.

### 3. Acceso con contraseña correcta

Desde el mismo cliente abrí otra conexión con la contraseña correcta:

```bash
ssh -o PubkeyAuthentication=no -o PreferredAuthentications=password anthlab@192.168.56.102
```

El registro `Accepted password` de Wazuh confirma el acceso correcto.

## Cronología y evidencias

Las horas de la siguiente tabla corresponden al campo `timestamp` tal como aparece en el dashboard.

| Fecha y hora mostrada | Evento examinado | Origen y usuario | Regla | Nivel |
| --- | --- | --- | --- | ---: |
| 22/10/2026 00:33:13.314 | Contraseña rechazada | `192.168.56.101`, `anthlab` | `5760` — `sshd: authentication failed.` | 5 |
| 22/10/2026 00:38:59.087 | Contraseña aceptada | `192.168.56.101`, `anthlab` | `5715` — `sshd: authentication success.` | 3 |

### Fallo de autenticación

Fragmento de `full_log` transcrito de la captura:

```text
Oct 21 22:33:12 anthwatch-server sshd[2167]: Failed password for anthlab from 192.168.56.101 port 47774 ssh2
```

![Detalle del fallo SSH: regla 5760, origen y usuario](../capturas/ssh-fallo-detalle.png)

### Autenticación correcta

Fragmento de `full_log` transcrito de la captura:

```text
Oct 21 22:38:57 anthwatch-server sshd[2222]: Accepted password for anthlab from 192.168.56.101 port 45230 ssh2
```

![Detalle del acceso correcto SSH: regla 5715, origen y usuario](../capturas/ssh-acceso-correcto-detalle.png)

Este caso conserva las horas originales anteriores al ajuste horario. La configuración de las tres VMs se corrigió antes del caso 003. La recogida posterior de `timedatectl` documenta Europe/Madrid, sincronización y NTP activo en los tres equipos; el colector de journald formatea el mensaje en UTC. Véanse las [evidencias horarias](../evidencias/README.md).

## Análisis

Relacioné los dos eventos por el origen, el usuario y el agente del servidor. Los puertos de origen y los procesos `sshd` eran distintos: el fallo y el éxito pertenecían a conexiones diferentes.

La regla `5760`, de nivel 5, identifica el fallo. La regla `5715`, de nivel 3, identifica el acceso correcto. Los niveles son los valores de las reglas observadas; la prioridad del caso se valora además con el contexto de la prueba.

Revisé también `rule.firedtimes`: la captura del fallo muestra `4` y la del acceso correcto `6`.

### Etiquetas MITRE ATT&CK observadas

| Evento | Etiquetas presentes en la captura | Interpretación en este caso |
| --- | --- | --- |
| Fallo | `T1110.001` — Password Guessing; `T1021.004` — SSH | Metadatos de la regla, compatibles con el uso de SSH y la prueba de contraseñas incorrectas |
| Acceso correcto | `T1078` — Valid Accounts; `T1021` — Remote Services | Metadatos de la regla; el acceso realizado fue autorizado |

Las etiquetas MITRE facilitan la clasificación de los eventos observados.

## Resultado

Comprobé que Wazuh recibía y analizaba ambos tipos de registro. El fallo y el acceso correcto mostraban el cliente, el servidor y el usuario esperados.

## Límites

Relacioné los eventos manualmente. La detección automática de «fallos seguidos de éxito» la trabajé después en el caso 003. Esta primera prueba valida la recogida de autenticaciones, con actividad autorizada.

Las etiquetas MITRE son metadatos de las reglas y el acceso de la prueba fue autorizado. Tampoco se conservó una captura de `hostname` y `exit`.

Conservé la terminal con tres solicitudes fallidas, la vista general y el detalle de un fallo y un éxito. Falta una exportación completa para reconstruir cada intento. Los contadores del panel incluyen toda la ventana consultada y `rule.firedtimes` cuenta activaciones de la regla, no intentos de una conexión concreta. Tampoco conservé el estado del adaptador NAT durante la ejecución.

## Decisión y respuesta propuesta

Cerré el caso como actividad autorizada del laboratorio, sin aplicar contención.

En un entorno real comprobaría quién hizo el acceso, desde dónde y qué ocurrió después. Escalaría si el usuario lo niega, el origen es inesperado o aparecen acciones sospechosas. Con esos datos valoraría medidas sobre la cuenta, las sesiones y el origen.

## Próximos pasos

- Prueba posterior completada: [caso 002](002-usuario-inexistente-repetido.md), correlación con usuario inexistente y control de menor volumen. Sus resultados no se atribuyen al caso 001.
- Prueba posterior completada: [caso 003](003-ssh-fallos-seguidos-de-exito.md), regla propia para fallos SSH seguidos de éxito desde la misma IP y con el mismo usuario.
- Investigación posterior completada: [Hunt 001](../hunts/001-ssh-y-sudo.md), accesos SSH y actividad con sudo. El seguimiento está en la [hoja de ruta](../hoja-de-ruta.md).
- El ajuste horario se completó antes del caso 003. En las siguientes pruebas se conservarán también exportaciones de los registros.

## Documentación operativa

- [Procedimiento de análisis N1](../playbooks/ssh-autenticacion.md).
- [Ticket simulado SOC-001](../tickets/SOC-001.md).
