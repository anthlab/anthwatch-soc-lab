# Anthwatch

Laboratorio personal de operaciones de seguridad orientado al análisis SOC N1.  
Wazuh 4.14.9 sobre tres máquinas Ubuntu Server conectadas en VirtualBox.  
Dos casos SSH completados, con evidencias y pruebas de control.  
Cada investigación incluye análisis, límites, decisión y un ticket simulado.  
Todas las pruebas se realizan sobre mis propias máquinas y cuentas del laboratorio.  
Próximo objetivo: una regla propia para detectar fallos SSH seguidos de un acceso correcto.

## Casos completados

| ID | Regla | Técnica MITRE observada | Resultado | Informe |
| --- | --- | --- | --- | --- |
| 001 | `5760`, `5715` | `T1110.001`, `T1021.004`; `T1078`, `T1021` | Fallos y acceso autorizado verificados; relación analizada manualmente | [Autenticación SSH](docs/casos/001-autenticacion-ssh.md) |
| 002 | `5710`, `5712` | `T1110` en la alerta correlacionada | Correlación de nivel 10 confirmada; control posterior sin nueva `5712` | [Intentos SSH repetidos](docs/casos/002-fuerza-bruta-ssh.md) |

Las etiquetas MITRE son metadatos de las reglas; las simulaciones no demuestran compromiso.

## Documentación

- [Estado, recursos y evidencias del montaje](docs/estado-del-laboratorio.md).
- [Arquitectura de red](docs/arquitectura/red-del-laboratorio.md) · [Instalación de Wazuh](docs/instalacion/wazuh.md).
- [Procedimiento de análisis N1](docs/playbooks/ssh-autenticacion.md) · [SOC-001](docs/tickets/SOC-001.md) · [SOC-002](docs/tickets/SOC-002.md).
- [Hoja de ruta: regla propia y threat hunting](docs/hoja-de-ruta.md).

[Portfolio](https://anthlab.github.io/) · [Licencia MIT](LICENSE)
