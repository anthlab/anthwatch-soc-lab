# Evidencias · Revisión del duplicado y Filebeat

[Análisis y cierre](../../hunts/hunt-001/repeticiones-exportacion.md)

**Recogida inicial:** 25/10/2026, `anthwatch-wazuh`; **ampliación:** 26/10/2026. Conservé la consulta de Dev Tools y su respuesta JSON, además de los ocho logs de Filebeat. La respuesta está formateada como JSON para su lectura; el manifiesto fija los bytes de esta copia. El filtrado `_source` de la consulta delimita los campos comparados.

| Archivo | Contenido |
| --- | --- |
| [consulta.http](consulta.http) | Consulta por el ID de alerta `1792621933.6071` en el índice del 21/10 UTC |
| [respuesta.json](respuesta.json) | Dos resultados; `_id` distintos y campos exportados de `_source` idénticos |
| [consulta-ampliada.http](consulta-ampliada.http) | Agregación por `id` sobre los índices accesibles, con dos documentos completos por grupo |
| [duplicados-ampliados.console.txt](duplicados-ampliados.console.txt) | Respuesta original de Dev Tools del 26/10, conservada con sus cadenas de comillas triples |
| [comparacion-ampliada.json](comparacion-ampliada.json) | Comparación derivada de las 68 parejas y contraste con las nueve del CSV |
| [logging-config-extracto.txt](logging-config-extracto.txt) | Transcripción de la salida de grep de la configuración; incluye `keepfiles: 7` |
| [manager/](manager/) | Los dos JSON originales del manager, sin comprimir y sin modificar sus bytes |
| [comparacion-manager.json](comparacion-manager.json) | Recuento de los 68 IDs por archivo y línea, comparación de campos y registro de los prefijos NUL |
| [contrastar-manager.py](contrastar-manager.py) | Script reproducible del contraste con el manager, usando solo la biblioteca estándar de Python |
| [filebeat/](filebeat/) | Los ocho archivos extraídos, conservados sin modificar sus bytes |
| [SHA256SUMS](SHA256SUMS) | Hashes generados al conservar esta recogida, con rutas relativas |

## Cobertura de los logs

| Archivo | Líneas | Primera marca | Última marca |
| --- | ---: | --- | --- |
| filebeat/filebeat | 33 | 2026-10-25T20:42:04.016000+01:00 | 2026-10-25T20:42:32.033000+01:00 |
| filebeat/filebeat.1 | 68 | 2026-10-24T18:24:27.217000+02:00 | 2026-10-24T20:19:19.576000+02:00 |
| filebeat/filebeat.2 | 82 | 2026-10-22T21:10:11.056000+02:00 | 2026-10-22T21:32:15.676000+02:00 |
| filebeat/filebeat.3 | 91 | 2026-10-22T20:19:06.822000+02:00 | 2026-10-22T20:38:49.921000+02:00 |
| filebeat/filebeat.4 | 73 | 2026-10-22T19:01:42.245000+02:00 | 2026-10-22T20:03:49.897000+02:00 |
| filebeat/filebeat.5 | 53 | 2026-10-22T18:45:39.380000+02:00 | 2026-10-22T18:47:47.829000+02:00 |
| filebeat/filebeat.6 | 119 | 2026-10-22T18:26:44.537000+02:00 | 2026-10-22T18:41:16.818000+02:00 |
| filebeat/filebeat.7 | 78 | 2026-10-22T16:13:57.069000+02:00 | 2026-10-22T16:53:03.675000+02:00 |

El registro más antiguo es del 22/10 a las **16:13:57.069+02:00**. Ninguno cubre **00:27–01:15+02:00 del 22/10**. Los errores de conexión y recuperaciones de otras franjas quedan en los archivos, pero no explican el duplicado de madrugada.

## Ampliación del 26/10

Conservé la [consulta ampliada](consulta-ampliada.http) y la [respuesta original de Dev Tools](duplicados-ampliados.console.txt). La respuesta usa 12 cadenas con comillas triples de la consola: mantuve sus bytes y normalicé esas cadenas en memoria para analizarla como JSON.

La [comparación derivada](comparacion-ampliada.json) registra los 68 pares, sus `_id`, índice, agente, regla y marcas temporales; incluye la igualdad de `_source` y el SHA-256 de su representación canónica (claves ordenadas, UTF-8, sin espacios separadores). Ese hash sirve para comparar contenido, no sustituye al de los archivos originales.

Verifiqué 68 grupos de dos documentos, todos con `_source` idéntico. Las nueve parejas del CSV coinciden en todos sus campos exportados con nueve grupos. La consulta no tuvo timeout ni shards fallidos; el margen de error de la agregación y `sum_other_doc_count` son cero. El alcance se limita a los índices accesibles a la cuenta de consulta en ese momento.

El [extracto de configuración](logging-config-extracto.txt) transcribe la salida de grep del 26/10: `keepfiles: 7` está declarado. El extracto no incluye `rotateonstartup`; su valor predeterminado en Filebeat 7.10.2 es `true`, aunque los argumentos del servicio no se auditaron en esta recogida.

## Contraste con el manager · 26/10

Copié `ossec-alerts-21.json` y `ossec-alerts-22.json` de `/var/ossec/logs/alerts/2026/Oct/` en `anthwatch-wazuh`. Los archivos contienen 110 y 423 registros respectivamente. Los 68 IDs objetivo aparecen una sola vez: 66 en el primero y dos en el segundo. Todos los campos emitidos por el manager coinciden con ambas copias del índice; allí se añaden `input` y `@timestamp`.

El archivo del 21 tiene un prefijo de 978 bytes NUL en la línea 67 (offset 64558); el del 22 tiene uno de 2.928 en la línea 353 (offset 319757). Los offsets empiezan en cero. El script retira solo esos prefijos en memoria y detiene el análisis si encuentra otro error de JSON. Los 533 registros resultantes son válidos y ninguno de los 68 objetivo lleva ese prefijo. Conservé los originales intactos. La causa de los NUL y una posible pérdida previa quedan indeterminadas; el recuento se limita a estos archivos.

Para reproducir el resultado desde esta carpeta sin sobrescribir la evidencia:

```bash
python3 contrastar-manager.py > /tmp/comparacion-manager-recalculada.json
diff -u comparacion-manager.json /tmp/comparacion-manager-recalculada.json
```

## Verificación

Desde esta carpeta:

```bash
sha256sum -c SHA256SUMS
```

Para volver a consultar el índice, usar `consulta.http` o `consulta-ampliada.http` en Dev Tools mientras los documentos sigan retenidos. La consulta inicial corresponde al 25/10 y la ampliada al 26/10; consultas posteriores pueden cambiar si se modifica el índice.
