# Documentación de Anthwatch

[Volver al proyecto](../README.md)

Empieza por el **[caso 003](casos/003-ssh-fallos-seguidos-de-exito.md)**. Cada informe enlaza sus evidencias y documentos de apoyo.

## Informes principales

| Informe | Qué encontrarás |
| --- | --- |
| [001 · Autenticación SSH](casos/001-autenticacion-ssh.md) | Eventos individuales y triaje |
| [002 · Usuario inexistente](casos/002-usuario-inexistente-repetido.md) | Correlación y control de menor volumen |
| [003 · Regla SSH propia](casos/003-ssh-fallos-seguidos-de-exito.md) | Detección, controles y diagnóstico de ingesta |
| [004 · Portal simulado](casos/004-portal-nominas.md) | Decodificador, reglas y prueba en vivo |
| [005 · Archivos, cuentas y sudo](casos/005-fim-usuarios-sudo.md) | Cobertura de cambios y triaje |
| [Hunt 001 · SSH y sudo](hunts/001-ssh-y-sudo.md) | Investigación de actividad posterior al acceso |

## Laboratorio y procedimientos

- [Estado del laboratorio](estado-del-laboratorio.md) · [Arquitectura](arquitectura/red-del-laboratorio.md) · [Instalación](instalacion/wazuh.md).
- [Análisis N1 de SSH](playbooks/ssh-autenticacion.md).
- [Comprobación operativa](playbooks/comprobacion-operativa.md) · [Triaje de varias fuentes](playbooks/triaje-multifuente.md).
- [Hoja de ruta](hoja-de-ruta.md).

## Anexo

[Duplicados de indexación](anexos/duplicados-indexacion.md): investigación detallada, registros originales y límites de las conclusiones.
