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

## Detalles pendientes de documentar

Este documento recoge el estado de la instalación. Todavía faltan los detalles necesarios para reproducirla paso a paso:

- Selección de OpenSSH durante la instalación y estado actual del servicio.

No se incluyen contraseñas ni credenciales.

## Documentación del montaje

Las tres capturas de configuración de las máquinas se encuentran en `docs/capturas/` y están enlazadas en [virtualbox.md](virtualbox.md).

## Siguiente fase

La red del laboratorio ya está configurada y comprobada; los detalles están en [red-del-laboratorio.md](../arquitectura/red-del-laboratorio.md). El siguiente paso es preparar instantáneas y desplegar Wazuh con sus agentes.
