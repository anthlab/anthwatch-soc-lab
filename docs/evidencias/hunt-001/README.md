# Evidencias · Hunt 001

[Informe completo](../../hunts/hunt-001/README.md)

Los CSV iniciales y `auth-1907.log` están en [las evidencias de la recogida inicial](../../hunts/hunt-001/evidencias/); esta carpeta contiene la ampliación a 28 comandos.

Conservé dos recogidas con alcances distintos:

| Recogida | Archivos y alcance |
| --- | --- |
| Inicial, 22/10 | [auth-1907.log](../../hunts/hunt-001/evidencias/auth-1907.log), [hash original](../../hunts/hunt-001/evidencias/auth-1907.sha256), CSV de 26 `5402`, CSV de 120 filas de accesos/sesiones y capturas 07–14 en [hunt-001](../../hunts/hunt-001/README.md) |
| Ampliación, 24/10 | [sudo-eventos.csv](sudo-eventos.csv): 28 filas, 26 `5402` y 2 `5403`; conservé los bytes originales de `events-2026-10-24T17_07_24.188Z.csv` |

Verifiqué `auth-1907.log`: seis líneas, SHA-256 `071271c0081329c11533e034f31f31640f0f81ba1e7fb09a0e99756e6c41462d`. Las capturas respaldan terminal, cuenta, IP/puerto, TTY y detalle de la secuencia.

El CSV ampliado contiene eventos de `anthwatch-server`, `anthlab` → `root`, entre el 16/10/2026 11:24:12.086 y el 22/10/2026 20:20:12.490 según `timestamp`. Son extremos observados, no una prueba de recogida continua. No conservé en este CSV el filtro y el intervalo exactos de la ampliación. La consulta histórica del 22/10 sí está documentada en el informe y las capturas.

Distingo el `timestamp` de presentación de la marca original de `full_log`: journald conserva UTC sin sufijo; auth.log usa ISO con zona explícita. No aplico una suma fija de horas a todas las filas.

Desde esta carpeta, verifico el CSV ampliado con:

```bash
sha256sum -c SHA256SUMS
```

Desde `docs/hunts/hunt-001`, verifico los originales y capturas restaurados con:

```bash
sha256sum -c SHA256SUMS
(cd evidencias && sha256sum -c auth-1907.sha256)
```

El segundo comando entra en `evidencias/` porque el hash original referencia `auth-1907.log`. Los hashes detectan cambios en los bytes, no certifican por sí solos una cadena de custodia.
