# Evidencias · Diagnóstico de ingesta journald

[Hunt 001](../../hunts/hunt-001/README.md) · [Hipótesis y siguiente contraste](../../hunts/hunt-001/repeticiones-exportacion.md)

Conservé una copia de los archivos originales de `anthwatch-ingesta-manager.tar.gz`:

- `manager-0020-0115.log`: mensajes del manager del 22/10/2026 00:20–01:15; arranque a las 00:27:39, errores del conector e inicializaciones correctas desde 00:31:57. El conector de inventario/estados no es el proceso Filebeat.
- `alerta-original-1792621933-6071.txt`: una coincidencia de la alerta `5715` con ese ID, extraída con número de línea.
- `alerta-1792621933-6071.txt`: búsqueda general que también devuelve mis comandos sudo que contienen el ID. No cuento esas coincidencias como copias de la alerta SSH.
- `SHA256SUMS`: manifiesto original, que verifico desde esta carpeta con `sha256sum -c SHA256SUMS`.

El 25/10 conservé la [consulta y respuesta con los dos `_id`](../duplicados-001/README.md), además de los ocho logs de Filebeat disponibles. Confirman la pareja documental, pero la cobertura de Filebeat empieza a las 16:13 del 22/10 y deja fuera la madrugada. El 26/10 la [consulta ampliada](../duplicados-001/README.md) confirmó 68 parejas, incluidas las nueve del CSV. El contraste posterior con los dos archivos originales del manager encontró una sola aparición de cada `id` y campos coincidentes con ambas copias del índice; los prefijos NUL quedan documentados en el análisis. El [análisis](../../hunts/hunt-001/repeticiones-exportacion.md) mantiene la causa histórica indeterminada.
