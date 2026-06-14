# Modelo temporal LAB 02

## Índice

- [Objetivo](#objetivo)
- [Modelo](#modelo)
- [Timeouts y backoff](#timeouts-y-backoff)
- [Estado](#estado)

## Objetivo

Documentar cómo se ejecuta temporalmente el firmware del laboratorio.

## Modelo

El firmware espera comandos de consola y responde con eventos JSON. No hay scheduler de aplicación ni temporización fija de negocio.

## Timeouts y backoff

Cuando no hay datos en consola, la HAL aplica un backoff de 50 ms para evitar saturación de CPU y logs.

## Estado

```text
CUMPLE:
- Modelo temporal explícito.
```
