# Modelo de concurrencia LAB 02

## Índice

- [Objetivo](#objetivo)
- [Modelo](#modelo)
- [Recursos compartidos](#recursos-compartidos)
- [ISR](#isr)
- [Estado](#estado)

## Objetivo

Documentar la política de concurrencia del LAB 02.

## Modelo

El laboratorio usa una única tarea de aplicación mediante `app_main()`. La consola se procesa de forma cooperativa con backoff cuando no hay datos.

## Recursos compartidos

No hay recursos compartidos entre tareas de aplicación. El estado de identidad se mantiene dentro de `IdentityService`.

## ISR

No hay ISR propias de aplicación.

## Estado

```text
CUMPLE:
- Modelo de concurrencia explícito.
```
