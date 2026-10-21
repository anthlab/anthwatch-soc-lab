# Ubuntu Server

[Volver al README](../../README.md)

## Estado actual

Ubuntu Server está instalado en las tres máquinas del laboratorio:

| Máquina virtual | Estado |
| --- | --- |
| `anthwatch-wazuh` | Ubuntu Server instalado |
| `anthwatch-server` | Ubuntu Server instalado |
| `anthwatch-client` | Ubuntu Server instalado |

La versión anotada para el laboratorio es **24.04.5 LTS**.

## Nombres de host

Los nombres de host configurados dentro de Ubuntu coinciden con los nombres de las máquinas en VirtualBox:

| Máquina virtual | Nombre de host en Ubuntu |
| --- | --- |
| `anthwatch-wazuh` | `anthwatch-wazuh` |
| `anthwatch-server` | `anthwatch-server` |
| `anthwatch-client` | `anthwatch-client` |

## Medio de instalación

Se utilizó la ISO `ubuntu-24.04.5-live-server-amd64.iso`, correspondiente a Ubuntu Server 24.04.5 LTS para arquitectura AMD64.

## Almacenamiento

Cada máquina dispone de un disco virtual VDI conectado mediante SATA:

| Máquina | Disco disponible para Ubuntu |
| --- | ---: |
| `anthwatch-wazuh` | 50 GB |
| `anthwatch-server` | 20 GB |
| `anthwatch-client` | 15 GB |

Las capturas de VirtualBox confirman estos discos, pero no muestran las opciones elegidas en el instalador de Ubuntu. Por tanto, el uso del disco completo, LVM, cifrado y la distribución de particiones no están confirmados.

## Administración por SSH

Las máquinas se administran desde el portátil mediante SSH para ejecutar comandos y copiar y pegar con más comodidad:

```bash
ssh anthlab@192.168.56.103  # anthwatch-wazuh
ssh anthlab@192.168.56.102  # anthwatch-server
ssh anthlab@192.168.56.101  # anthwatch-client
```

En `anthwatch-client` se encontró el error `Connection refused` al intentar acceder al puerto 22. Se habilitó el servidor OpenSSH y después se confirmó el acceso por SSH:

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
sudo systemctl status ssh --no-pager
```

No se incluyen contraseñas ni credenciales de acceso en el repositorio.

## Documentación del montaje

Las tres capturas de configuración de las máquinas se encuentran en `docs/capturas/` y están enlazadas en [virtualbox.md](virtualbox.md).

## Siguiente fase

La red del laboratorio ya está configurada y comprobada; los detalles están en [red-del-laboratorio.md](../arquitectura/red-del-laboratorio.md). Wazuh y los dos agentes ya están instalados y conectados; los pasos y las evidencias se recogen en [wazuh.md](wazuh.md). La recogida de eventos SSH ya está validada y documentada en el [caso 001](../casos/001-autenticacion-ssh.md).
