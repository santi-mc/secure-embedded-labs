# Common — LAB 03 MQTT

## Índice

- [Objetivo](#objetivo)
- [Reglas](#reglas)
- [Estado](#estado)

## Objetivo

Contener componentes reutilizables, contratos de logs, utilidades y políticas compartidas por los sublaboratorios LAB 03A–LAB 03G.

## Reglas

- `common/` no puede ocultar el estado de un sublaboratorio.
- Toda reutilización debe ser explícita y trazable.
- Ningún secreto real debe almacenarse aquí.

## Estado

```text
CUMPLE:
- Directorio común creado como frontera explícita de reutilización.

PENDIENTE:
- Extraer componentes compartidos solo cuando exista una segunda necesidad real.
```
