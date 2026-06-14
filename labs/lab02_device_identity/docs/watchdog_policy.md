# Política de watchdog LAB 02

## Índice

- [Objetivo](#objetivo)
- [Política](#política)
- [Estado](#estado)

## Objetivo

Documentar la política de supervisión del laboratorio.

## Política

El laboratorio no configura watchdog propio. Se apoya en los mecanismos por defecto de ESP-IDF. No hay tareas largas ni bucles de cómputo intensivo.

En una evolución de producto, el bucle de consola debería integrarse con un contrato explícito de watchdog por tarea.

## Estado

```text
NO VALIDADO:
- Watchdog dedicado no implementado por alcance didáctico.
```
