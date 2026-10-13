# Anthwatch

Mi laboratorio personal de operaciones de seguridad con Wazuh.

**Estado:** preparando el laboratorio. Todavía no hay investigaciones completadas.

## Sobre el proyecto

Estoy montando Anthwatch para practicar el trabajo de un analista SOC: revisar eventos, investigar alertas y escribir lo que he encontrado.

En cada caso quiero entender qué ha pasado, cómo lo ha detectado Wazuh y qué decisión tomaría con la información disponible.

El laboratorio estará en una red separada de mi red doméstica. Todas las pruebas se harán contra mis propias máquinas virtuales y con cuentas de prueba; no se atacarán sistemas ajenos.

## Entorno

Anotaré las versiones al instalar cada componente:

| Componente | Versión instalada |
| --- | --- |
| Wazuh | Pendiente |
| Ubuntu Server | Pendiente |
| VirtualBox | Pendiente |

## Montaje previsto

Usaré VirtualBox con tres máquinas virtuales:

| Máquina | Función | CPU virtuales | RAM | Disco |
| --- | --- | ---: | ---: | ---: |
| `anthwatch-wazuh` | Servidor Wazuh, indexador y panel en una misma VM | 4 | 8 GiB | 50 GB |
| `anthwatch-server` | Ubuntu Server con SSH y agente de Wazuh | 2 | 2 GiB | 20 GB |
| `anthwatch-client` | Ubuntu Server desde el que generaré los intentos de acceso | 1 | 2 GiB | 15 GB |

Las máquinas compartirán una red solo-anfitrión para comunicarse entre ellas y con mi ordenador. Añadiré un adaptador NAT para instalar y actualizar paquetes, y lo desconectaré durante las simulaciones.

Los recursos de Wazuh siguen su guía de inicio rápido. Los de las otras máquinas son una propuesta inicial.

## Primera versión

El primer caso será investigar varios intentos fallidos de acceso por SSH, seguidos de un acceso correcto desde la misma IP y con la misma cuenta de prueba.

Para completar esta versión tendré que:

- [ ] Preparar las máquinas, comprobar su comunicación, anotar las versiones y crear instantáneas.
- [ ] Instalar Wazuh y conectar el agente del servidor Ubuntu.
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

Añadiré aquí el enlace a la plantilla cuando la prepare.

## Próximas fases

Después del caso SSH, probaré cambios en archivos monitorizados, creación de usuarios y actividad con `sudo`. Más adelante añadiré reglas propias y practicaré búsquedas de actividad sospechosa a partir de una hipótesis.

El analizador de logs en Python será otro proyecto. Usará datos exportados de Anthwatch para agrupar eventos y ordenar lo ocurrido en una cronología.

## Documentación

Guardaré en este repositorio el montaje, las configuraciones y las investigaciones, con los pasos para repetir cada prueba.

En mi [portfolio](https://anthlab.github.io/projects/anthwatch/) mostraré el proyecto y los casos que vaya completando.

## Referencias

- [Guía de inicio rápido de Wazuh](https://documentation.wazuh.com/current/quickstart.html)
- [Detección de fuerza bruta con Wazuh](https://documentation.wazuh.com/current/proof-of-concept-guide/detect-brute-force-attack.html)
- [Documentación de VirtualBox](https://docs.oracle.com/en/virtualization/virtualbox/index.html)
