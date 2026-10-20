# Anthwatch

Mi laboratorio personal de operaciones de seguridad con Wazuh.

**Estado:** Wazuh 4.14.9 está instalado y los agentes de `anthwatch-server` y `anthwatch-client` aparecen activos en el dashboard. Las tres máquinas se comunican por la red solo-anfitrión y se administran por SSH. El siguiente paso es comprobar la recogida de eventos de autenticación SSH.

## Sobre el proyecto

Estoy montando Anthwatch para practicar el trabajo de un analista SOC: revisar eventos, investigar alertas y escribir lo que he encontrado.

En cada caso quiero entender qué ha pasado, cómo lo ha detectado Wazuh y qué decisión tomaría con la información disponible.

El laboratorio estará en una red separada de mi red doméstica. Todas las pruebas se harán contra mis propias máquinas virtuales y con cuentas de prueba; no se atacarán sistemas ajenos.

## Entorno

| Componente | Estado |
| --- | --- |
| VirtualBox | Instalado y con las tres máquinas creadas |
| Ubuntu Server | Instalado en las tres máquinas |
| Wazuh | Versión 4.14.9 instalada; dashboard accesible |
| Agentes Wazuh | `anthwatch-server` y `anthwatch-client` activos |
| Administración | Acceso por SSH desde el portátil |

Las versiones y los pasos de configuración están documentados en `docs/instalacion/`.

## Máquinas instaladas

Las tres máquinas virtuales ya están creadas en VirtualBox y tienen Ubuntu Server instalado. Sus funciones y recursos son:

| Máquina | Función | IP de laboratorio | CPU virtuales | RAM | Disco |
| --- | --- | --- | ---: | ---: | ---: |
| `anthwatch-wazuh` | Servidor Wazuh, indexador y panel en una misma VM | `192.168.56.103` | 4 | 8 GiB | 50 GB |
| `anthwatch-server` | Ubuntu Server con SSH y agente de Wazuh | `192.168.56.102` | 2 | 2 GiB | 20 GB |
| `anthwatch-client` | Ubuntu Server con agente de Wazuh, desde el que generaré los intentos de acceso | `192.168.56.101` | 1 | 2 GiB | 15 GB |

Las máquinas están conectadas entre sí mediante `vboxnet0` (adaptador solo-anfitrión). Conservan un adaptador NAT para instalar y actualizar paquetes; se desconectará durante las simulaciones.

Wazuh está desplegado en `anthwatch-wazuh` con el manager, el indexador y el dashboard en una misma VM. Los otros dos equipos tienen instalado el agente 4.14.9 y aparecen como activos. La conexión de los agentes está verificada; la validación de eventos y alertas SSH sigue pendiente.

### Capturas de configuración

Estas capturas muestran la configuración de las máquinas en VirtualBox:

**anthwatch-wazuh**

![Configuración de anthwatch-wazuh en VirtualBox](docs/capturas/anthwatch-wazuh-config.png)

**anthwatch-server**

![Configuración de anthwatch-server en VirtualBox](docs/capturas/anthwatch-server-config.png)

**anthwatch-client**

![Configuración de anthwatch-client en VirtualBox](docs/capturas/anthwatch-client-config.png)

## Wazuh y agentes conectados

El dashboard está disponible en `https://192.168.56.103` desde el portátil.

### Dashboard de Wazuh

Acceso al dashboard tras completar la instalación, antes de registrar los agentes:

![Dashboard de Wazuh tras la instalación](docs/capturas/wazuh-dashboard.png)

### Agentes activos

La comprobación del 21 de octubre de 2026 muestra los dos agentes activos, sin agentes desconectados, pendientes ni que nunca hayan conectado:

| Agente | ID | IP | Versión | Estado |
| --- | --- | --- | --- | --- |
| `anthwatch-server` | `001` | `192.168.56.102` | 4.14.9 | Activo |
| `anthwatch-client` | `002` | `192.168.56.101` | 4.14.9 | Activo |

![Agentes anthwatch-server y anthwatch-client activos en Wazuh](docs/capturas/agentes-activos.png)

El dashboard muestra dos agentes porque corresponden a los dos equipos monitorizados; `anthwatch-wazuh` actúa como servidor central.

## Primera versión

El primer caso será investigar varios intentos fallidos de acceso por SSH, seguidos de un acceso correcto desde la misma IP y con la misma cuenta de prueba.

Para completar esta versión tendré que:

- [x] Crear las tres máquinas virtuales con los recursos indicados.
- [x] Instalar Ubuntu Server 24.04.5 LTS en las tres máquinas.
- [x] Configurar la red solo-anfitrión y comprobar la comunicación entre las máquinas.
- [x] Habilitar la administración por SSH desde el portátil.
- [x] Instalar Wazuh y conectar los agentes de `anthwatch-server` y `anthwatch-client`.
- [ ] Verificar la recogida de eventos de autenticación SSH.
- [ ] Generar una secuencia de fallos y comprobar la alerta que produce.
- [ ] Realizar un acceso correcto y compararlo con los fallos anteriores.
- [ ] Escribir el informe con las evidencias y la conclusión.

La simulación de intentos de contraseña se relacionará con [T1110.001 — Password Guessing](https://attack.mitre.org/techniques/T1110/001/). Añadiré [T1078 — Valid Accounts](https://attack.mitre.org/techniques/T1078/) si el escenario incluye un uso no autorizado simulado de la cuenta.

Un acceso correcto después de varios fallos no demuestra por sí solo que la cuenta esté comprometida. En el informe distinguiré lo que he simulado de lo que puedo confirmar con los registros.

## Ficha de investigación

Usaré una misma plantilla para todos los casos. Recogerá:

- Qué pasó: equipo, IP de origen, usuario y horarios.
- Qué alerta apareció y qué evidencias encontré.
- Qué simulé frente a qué demuestran los registros.
- Técnica MITRE asociada.
- Qué prioridad le daría y por qué.
- Qué pude confirmar y qué información falta.
- Qué medidas propondría y cuándo escalaría el caso.

La plantilla se preparará cuando comience el primer caso de investigación.

## Próximas fases

Después del caso SSH, probaré cambios en archivos monitorizados, creación de usuarios y actividad con `sudo`. Más adelante añadiré reglas propias y practicaré búsquedas de actividad sospechosa a partir de una hipótesis.

El analizador de logs en Python será otro proyecto. Usará datos exportados de Anthwatch para agrupar eventos y ordenar lo ocurrido en una cronología.

## Documentación

Documentación disponible:

- [Máquinas virtuales en VirtualBox](docs/instalacion/virtualbox.md).
- [Instalación de Ubuntu Server y administración por SSH](docs/instalacion/ubuntu-server.md).
- [Instalación de Wazuh y conexión de agentes](docs/instalacion/wazuh.md).
- [Configuración y comprobación de la red](docs/arquitectura/red-del-laboratorio.md).
- [Diagrama de red](docs/arquitectura/diagrama-red.png).

Los documentos de instalación recogen el estado actual; los detalles aún no verificados están indicados como pendientes. Añadiré las investigaciones conforme complete las primeras pruebas de detección.

En mi [portfolio](https://anthlab.github.io/projects/anthwatch/) mostraré el proyecto y los casos que vaya completando.

## Referencias

- [Guía de inicio rápido de Wazuh](https://documentation.wazuh.com/current/quickstart.html)
- [Detección de fuerza bruta con Wazuh](https://documentation.wazuh.com/current/proof-of-concept-guide/detect-brute-force-attack.html)
- [Documentación de VirtualBox](https://docs.oracle.com/en/virtualization/virtualbox/index.html)
