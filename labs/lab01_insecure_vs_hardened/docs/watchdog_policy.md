# LAB 01 — Política de watchdog

## Índice

- [Objetivo](#objetivo)
- [Decisión](#decisión)
- [Justificación](#justificación)
- [Estado](#estado)

## Objetivo

Declarar explícitamente la política de watchdog.

## Decisión

El LAB 01 **no configura watchdog de aplicación propio**.

## Justificación

El laboratorio es interactivo, bloqueante por consola y sin control de proceso físico. Añadir watchdog de aplicación en esta fase introduciría ruido didáctico. Se documenta para no confundir ausencia de watchdog con olvido.

## Estado

```text
CUMPLE:
- Política documentada.

NO CUMPLE como producto:
- No hay contrato de supervisión de watchdog de aplicación.
```
