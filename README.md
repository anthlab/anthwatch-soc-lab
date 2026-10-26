# Anthwatch

Monté Anthwatch para empezar a familiarizarme con un SIEM y practicar tareas de un analista SOC. Además, estábamos trabajando con Wazuh en clase de Incidentes de Ciberseguridad y quería seguir practicando por mi cuenta. Mi objetivo era entender cómo llegan los registros, cómo se generan las alertas y cómo investigarlas usando mis propias máquinas.

Trabajo con Wazuh 4.14.9 y tres máquinas Ubuntu Server en VirtualBox. Empecé revisando fallos y accesos SSH, después probé una correlación con un usuario inexistente y acabé creando mi propia regla. En cada caso guardé evidencias, expliqué el resultado y redacté un ticket simulado. Todas las pruebas las hice con mis máquinas y cuentas del laboratorio.

Al probar la regla con conexiones reales apareció el problema de rsyslog: agrupaba los fallos y la secuencia que funcionaba en logtest dejaba de detectarse. Lo corregí y repetí las pruebas. Después amplié la investigación con un hunt de SSH y sudo, donde revisé la cobertura de las consultas y las repeticiones en los datos.

## Casos completados

| ID | Regla | MITRE asociado | Resultado | Informe |
| --- | --- | --- | --- | --- |
| 001 | `5760`, `5715` | `T1110.001`, `T1021.004`; `T1078`, `T1021` | Fallos y acceso autorizado verificados; relación analizada manualmente | [Autenticación SSH](docs/casos/001-autenticacion-ssh.md) |
| 002 | `5710`, `5712` | `T1110` en la alerta correlacionada | Alerta de nivel 10; control de una conexión con dos `5710` y sin `5712` | [Intentos SSH repetidos](docs/casos/002-usuario-inexistente-repetido.md) |
| 003 | `100100` (propia) | `T1110.001`, `T1078` | Tres fallos + éxito en 23 s; revalidación con salidas completas y control temporal de 130 s | [Correlación SSH](docs/casos/003-ssh-fallos-seguidos-de-exito.md) |

## Threat hunting y revalidación

- [Hunt 001: SSH y sudo](docs/hunts/001-ssh-y-sudo.md): secuencia de prueba y revisión de 28 comandos sudo (`5402` y `5403`), cambio de fuente y análisis de duplicación documental.
- [Revalidación del caso 003](docs/casos/003-revalidacion.md): positivo `100100`, controles por IP/usuario y control temporal con 130,003 s declarados de espera y 132,122 s entre las marcas; XML equivalente al del repositorio.
- [Evidencias del hunt](docs/evidencias/hunt-001/README.md) · [Evidencias de revalidación](docs/evidencias/revalidacion-003/README.md) · [HUNT-001](docs/tickets/HUNT-001.md).

Conservé extractos originales, CSV, capturas y hashes del hunt y la revalidación real. No identifiqué actividad no autorizada en la muestra. Amplié la [revisión de duplicados](docs/hunts/hunt-001/repeticiones-exportacion.md) a los índices consultados: confirmé 68 parejas con contenido idéntico, incluidas las nueve del CSV. Contrasté los 68 `id` con los dos archivos del manager: cada uno aparece una vez y sus campos coinciden con ambas copias indexadas. La duplicación posterior a la emisión queda respaldada en esos archivos; la causa concreta sigue indeterminada y faltan los logs de Filebeat de madrugada.

## Documentación

- [Estado, recursos y evidencias del montaje](docs/estado-del-laboratorio.md).
- [Arquitectura de red](docs/arquitectura/red-del-laboratorio.md) · [Instalación de Wazuh](docs/instalacion/wazuh.md).
- [Procedimiento de análisis N1](docs/playbooks/ssh-autenticacion.md) · [SOC-001](docs/tickets/SOC-001.md) · [SOC-002](docs/tickets/SOC-002.md) · [SOC-003](docs/tickets/SOC-003.md).
- [Regla propia](rules/anthwatch_ssh_rules.xml) · [Pruebas reproducibles](tests/caso-003/README.md).
- [Hoja de ruta y cobertura pendiente](docs/hoja-de-ruta.md).

[Portfolio](https://anthlab.github.io/) · [Licencia MIT](LICENSE)
