# Evidencias · Revalidación del caso 003

[Informe](../../casos/003-revalidacion.md)

Origen: archivo `anthwatch-validacion-final.tar.gz` de la revalidación. Conservé los bytes de todos sus archivos.

| Carpeta / archivo | Contenido |
| --- | --- |
| `control-130s/` | Entrada, salida íntegra de logtest, tiempos y manifiesto original |
| `controles-identidad/` | Entradas y salidas de positivo, otra IP y otro usuario; tiempos y manifiesto original |
| `xml-100100/` | XML recogido y manifiesto original con ruta absoluta |
| `diferencias-xml.txt` | Comparación histórica entre XML del repositorio y copia instalada |
| `xml-repositorio.sha256` | Hash histórico; la ruta `rules/…` se interpreta desde la raíz del repositorio |

Conservé intacto `xml-100100/SHA256SUMS`, que referencia `/home/anthlab/…`: **ese manifiesto no se puede verificar con `sha256sum -c` en este repositorio**. Para verificar la copia del XML aquí, uso únicamente `SHA256SUMS-relativo`, con rutas relativas. Este manifiesto adicional cubre los 11 archivos de la recogida sin modificar los originales. Desde esta carpeta:

```bash
sha256sum -c SHA256SUMS-relativo
```

Las entradas son muestras sintéticas enviadas a logtest. Los tiempos y salidas son registros de su ejecución; no deben presentarse como telemetría de conexiones reales.
