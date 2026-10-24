# Evidencias · Diagnóstico de ingesta journald

[Hunt 001](../../hunts/hunt-001/README.md) · [Hipótesis y siguiente contraste](../../hunts/hunt-001/repeticiones-exportacion.md)

Conservé una copia de los archivos originales de `anthwatch-ingesta-manager.tar.gz`:

- `manager-0020-0115.log`: mensajes del manager del 22/10/2026 00:20–01:15; arranque a las 00:27:39, errores del conector e inicializaciones correctas desde 00:31:57. El conector de inventario/estados no es el proceso Filebeat.
- `alerta-original-1792621933-6071.txt`: una coincidencia de la alerta `5715` con ese ID, extraída con número de línea.
- `alerta-1792621933-6071.txt`: búsqueda general que también devuelve mis comandos sudo que contienen el ID. No cuento esas coincidencias como copias de la alerta SSH.
- `SHA256SUMS`: manifiesto original, que verifico desde esta carpeta con `sha256sum -c SHA256SUMS`.

No conservé la exportación de los dos documentos con `_id` y `_index`; no presento su comparación como una prueba reproducible. Investigo reintentos de entrega/indexación como hipótesis y dejo pendiente recoger Filebeat y exportar los documentos. El informe contiene el comando y los campos necesarios. No atribuyo las repeticiones a rotación del journal ni a los errores del conector sin esas comprobaciones.
