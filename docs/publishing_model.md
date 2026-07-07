# Modelo de publicación

## Índice

- [Criterio](#criterio)
- [Cierre transversal](#cierre-transversal)
- [Estado](#estado)

## Criterio

Cada entrega debe mantener sincronizados repositorio, libro, roadmap, changelog, documentación de laboratorio, herramientas y evidencias.

## Cierre transversal

Antes de continuar con un laboratorio nuevo deben pasar, como mínimo:

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
```

Cuando aplique LAB 03:

```powershell
python labs/lab03_mqtt/tools/run_static_gates.py
python labs/lab03_mqtt/tools/capture_static_gates.py
```

## Estado

```text
CUMPLE:
- El modelo exige sincronización documental y evidencial antes de avanzar.
```
