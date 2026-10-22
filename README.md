# Anthwatch

Laboratorio personal de operaciones de seguridad orientado al análisis SOC N1.  
Wazuh 4.14.9 sobre tres máquinas Ubuntu Server conectadas en VirtualBox.  
Tres casos SSH completados, con evidencias y pruebas de control.  
Cada investigación incluye análisis, límites, decisión y un ticket simulado.  
Todas las pruebas se realizan sobre mis propias máquinas y cuentas del laboratorio.  
Regla propia validada; próximo objetivo: una búsqueda de threat hunting basada en una hipótesis.

## Casos completados

| ID | Regla | MITRE asociado | Resultado | Informe |
| --- | --- | --- | --- | --- |
| 001 | `5760`, `5715` | `T1110.001`, `T1021.004`; `T1078`, `T1021` | Fallos y acceso autorizado verificados; relación analizada manualmente | [Autenticación SSH](docs/casos/001-autenticacion-ssh.md) |
| 002 | `5710`, `5712` | `T1110` en la alerta correlacionada | Alerta de nivel 10; control de una conexión con dos `5710` y sin `5712` | [Intentos SSH repetidos](docs/casos/002-usuario-inexistente-repetido.md) |
| 003 | `100100` (propia) | `T1110.001`, `T1078` | Tres fallos + éxito en 23 s; controles previos con logtest | [Correlación SSH](docs/casos/003-ssh-fallos-seguidos-de-exito.md) |

## Documentación

- [Estado, recursos y evidencias del montaje](docs/estado-del-laboratorio.md).
- [Arquitectura de red](docs/arquitectura/red-del-laboratorio.md) · [Instalación de Wazuh](docs/instalacion/wazuh.md).
- [Procedimiento de análisis N1](docs/playbooks/ssh-autenticacion.md) · [SOC-001](docs/tickets/SOC-001.md) · [SOC-002](docs/tickets/SOC-002.md) · [SOC-003](docs/tickets/SOC-003.md).
- [Regla propia](rules/anthwatch_ssh_rules.xml) · [Pruebas reproducibles](tests/caso-003/README.md).
- [Hoja de ruta: threat hunting](docs/hoja-de-ruta.md).

[Portfolio](https://anthlab.github.io/) · [Licencia MIT](LICENSE)
