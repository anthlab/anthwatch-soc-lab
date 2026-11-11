# Comprobación operativa de Anthwatch

[Arquitectura](../arquitectura/red-del-laboratorio.md) · [Instalación](../instalacion/wazuh.md)

Este procedimiento utiliza la instalación de Wazuh 4.14.9 como servicios en `anthwatch-wazuh`, el agente `001` de `anthwatch-server` y las rutas observadas en los casos del proyecto. Conviene anotar la fecha y guardar la salida cada vez que se repita.

## Servidor central

En `anthwatch-wazuh`:

```bash
systemctl is-active wazuh-manager wazuh-indexer wazuh-dashboard
sudo /var/ossec/bin/agent_control -l
```

El agente de `anthwatch-server` debe comunicar durante las pruebas. Consultar los registros del servicio que falle con `journalctl -u NOMBRE_DEL_SERVICIO` y comprobar conectividad con la dirección del manager, `192.168.56.103`.

## Agente y fuentes

En `anthwatch-server`:

```bash
systemctl is-active wazuh-agent
sudo grep -nE '<(address|location|log_format)>' /var/ossec/etc/ossec.conf
```

Los casos SSH utilizan `/var/log/auth.log`; el portal utiliza `/var/log/syslog`. Comparar el mensaje original, el agente, la fuente y la hora con el JSON del manager. Para FIM, contrastar la ruta vigilada y el modo que muestra la alerta.

## Validación de cambios

En el manager, ejecutar `sudo /var/ossec/bin/wazuh-analysisd -t` después de editar reglas o decodificadores. Probar las entradas con una nueva sesión de `wazuh-logtest`. Para guardar su salida, redirigir stdout y stderr con `> salida.txt 2>&1`.

Aplicar las reglas a los eventos del agente mediante `sudo systemctl restart wazuh-manager` cuando la validación termine correctamente. Comprobar de nuevo el servicio y la comunicación del agente.

Los [casos 003](../casos/003-ssh-fallos-seguidos-de-exito.md), [004](../casos/004-portal-nominas.md) y [005](../casos/005-fim-usuarios-sudo.md) conservan los resultados de las pruebas correspondientes.
