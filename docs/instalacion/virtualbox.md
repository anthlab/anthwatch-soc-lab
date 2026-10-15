# Máquinas virtuales en VirtualBox

[Volver al README](../../README.md)

## Estado actual

VirtualBox está instalado y las tres máquinas del laboratorio están creadas. Ubuntu Server ya está instalado en cada una.

VirtualBox se descargó desde su [web oficial](https://www.virtualbox.org/). La versión utilizada es **7.2.6**.

## Recursos asignados

| Máquina | CPU virtuales | RAM | Disco | Función prevista |
| --- | ---: | ---: | ---: | --- |
| `anthwatch-wazuh` | 4 | 8 GiB | 50 GB | Alojar Wazuh, el indexador y el panel |
| `anthwatch-server` | 2 | 2 GiB | 20 GB | Servidor monitorizado con SSH y agente Wazuh |
| `anthwatch-client` | 1 | 2 GiB | 15 GB | Generar actividad de prueba |

Los nombres de las máquinas virtuales usan guiones. La configuración de los servicios se completará en las siguientes fases.

## Almacenamiento y configuración observada

Las capturas muestran discos en formato **VDI**, conectados al **puerto 0 de una controladora SATA**:

| Máquina | Archivo de disco | Capacidad virtual |
| --- | --- | ---: |
| `anthwatch-wazuh` | `anthwatch-wazuh.vdi` | 50 GB |
| `anthwatch-server` | `anthwatch-server.vdi` | 20 GB |
| `anthwatch-client` | `anthwatch-client.vdi` | 15 GB |

En las tres máquinas, la unidad óptica conectada a IDE aparece vacía. El adaptador 1 utiliza **Intel PRO/1000 MT Desktop en modo NAT**. El orden de arranque mostrado es disco duro, unidad óptica y disquete.

Las capturas no muestran explícitamente el modo de firmware ni si el disco se reservó dinámicamente o con tamaño fijo; esos valores no se dan por confirmados. La etiqueta «Normal» del disco no indica el tipo de reserva.

## Evidencias de configuración

### anthwatch-wazuh

![Configuración de anthwatch-wazuh](../capturas/anthwatch-wazuh-config.png)

### anthwatch-server

![Configuración de anthwatch-server](../capturas/anthwatch-server-config.png)

### anthwatch-client

![Configuración de anthwatch-client](../capturas/anthwatch-client-config.png)

## Red configurada

Las tres máquinas conservan el **Adaptador 1 en NAT** y tienen el **Adaptador 2** conectado a la red solo-anfitrión **`vboxnet0`**, con DHCP habilitado. La configuración de Ubuntu, las direcciones IP actuales y las pruebas de conectividad están recogidas en [red-del-laboratorio.md](../arquitectura/red-del-laboratorio.md).

## Pendiente

- Crear y documentar las instantáneas de referencia.

La instalación del sistema operativo se recoge en [Ubuntu Server](ubuntu-server.md).
