# LAB 01 — Modelo temporal

## Índice

- [Objetivo](#objetivo)
- [Modelo elegido](#modelo-elegido)
- [Actividades](#actividades)
- [Timeouts](#timeouts)
- [Estado](#estado)

## Objetivo

Declarar el comportamiento temporal del LAB 01.

## Modelo elegido

El LAB 01 usa un modelo **event-driven cooperativo por consola bloqueante**. No implementa tareas periódicas ni scheduling de tiempo real porque el objetivo es analizar comandos locales, logs y configuración.

## Actividades

| Actividad | Tipo | Periodo | Deadline | Stack | Política |
|---|---|---:|---:|---:|---|
| `CommandConsole::runForever` | Bloqueante por entrada | N/A | N/A | task principal ESP-IDF | Procesa línea y vuelve a esperar. |
| `sample` | Bajo demanda | N/A | N/A | task principal | Emite muestra determinista. |
| `security_status` | Bajo demanda | N/A | N/A | task principal | Consulta eFuse/Secure Boot. |

## Timeouts

No hay operaciones de bus externas ni red. La consola limita longitud de línea mediante `CONFIG_LAB01_CONSOLE_LINE_MAX`.

## Estado

```text
CUMPLE:
- Modelo temporal explícito y acotado.

NO CUMPLE como sistema de tiempo real:
- No demuestra WCET ni jitter porque no es el objetivo del LAB 01.
```
