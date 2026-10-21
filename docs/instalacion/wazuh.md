# Wazuh y conexión de agentes

[Volver al README](../../README.md)

## Estado verificado

Wazuh 4.14.9 está instalado en `anthwatch-wazuh`. Los agentes de `anthwatch-server` y `anthwatch-client` aparecen activos en el dashboard, como se comprobó el 21 de octubre de 2026.

| Equipo | IP | Función | Estado |
| --- | --- | --- | --- |
| `anthwatch-wazuh` | `192.168.56.103` | Manager, indexador y dashboard | Dashboard accesible |
| `anthwatch-server` | `192.168.56.102` | Agente 4.14.9, ID `001` | Activo |
| `anthwatch-client` | `192.168.56.101` | Agente 4.14.9, ID `002` | Activo |

## Servidor central

Se utilizó el asistente oficial de instalación de Wazuh para un despliegue todo en uno en `anthwatch-wazuh`: manager, indexador, Filebeat y dashboard en una misma máquina.

El dashboard se abrió desde el navegador del portátil en:

```text
https://192.168.56.103
```

La captura se tomó después de acceder al dashboard y antes de registrar los agentes:

![Dashboard de Wazuh instalado](../capturas/wazuh-dashboard.png)

## Despliegue de agentes

En el dashboard se utilizó **Deploy new agent**, con el paquete **DEB amd64**, la dirección del manager `192.168.56.103` y un nombre distinto para cada equipo. Se mantuvo el grupo `default`.

Los comandos se ejecutaron por SSH en el equipo que se quería monitorizar.

### anthwatch-server

Dentro de la sesión SSH de `anthwatch-server`:

```bash
wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.9-1_amd64.deb
sudo WAZUH_MANAGER='192.168.56.103' WAZUH_AGENT_NAME='anthwatch-server' dpkg -i ./wazuh-agent_4.14.9-1_amd64.deb
```

### anthwatch-client

Dentro de la sesión SSH de `anthwatch-client`:

```bash
wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.9-1_amd64.deb
sudo WAZUH_MANAGER='192.168.56.103' WAZUH_AGENT_NAME='anthwatch-client' dpkg -i ./wazuh-agent_4.14.9-1_amd64.deb
```

### Inicio y comprobación del servicio

Después de instalar el paquete, se ejecutaron estos comandos en cada agente:

```bash
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
sudo systemctl status wazuh-agent --no-pager
```

El estado `active (running)` confirmó que el servicio estaba en ejecución y `enabled` que estaba habilitado para el arranque.

## Confirmación de conexión con Wazuh

Se actualizó el apartado **Endpoints** del dashboard y se comprobó:

- `anthwatch-server`: IP `192.168.56.102`, versión 4.14.9, estado `active`.
- `anthwatch-client`: IP `192.168.56.101`, versión 4.14.9, estado `active`.
- Dos agentes activos y cero desconectados, pendientes o que nunca hayan conectado.

![Los dos agentes conectados a Wazuh](../capturas/agentes-activos.png)

La comprobación del servicio por sí sola no confirma la conexión al manager. El estado de ambos agentes en el dashboard aporta la evidencia de esa conexión.

Las direcciones son las concesiones DHCP actuales de `vboxnet0`; si cambian, habrá que revisar la dirección del manager configurada en los agentes. La configuración de red está en [red-del-laboratorio.md](../arquitectura/red-del-laboratorio.md).

## Siguiente prueba

La instalación y conexión están completadas. La recogida de fallos y accesos correctos por SSH también está verificada en el [caso 001](../casos/001-autenticacion-ssh.md). Queda validar la detección correlacionada de varios fallos en otra prueba.

## Referencias

- [Inicio rápido de Wazuh](https://documentation.wazuh.com/current/quickstart.html).
- [Instalación del agente en Linux](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-linux.html).
