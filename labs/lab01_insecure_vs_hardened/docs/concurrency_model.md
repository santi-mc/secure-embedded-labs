# LAB 01 — Modelo de concurrencia

## Índice

- [Objetivo](#objetivo)
- [Modelo](#modelo)
- [Recursos compartidos](#recursos-compartidos)
- [ISR](#isr)
- [Estado](#estado)

## Objetivo

Declarar política de concurrencia, ISR y recursos compartidos.

## Modelo

El firmware ejecuta la lógica de laboratorio en la tarea principal de ESP-IDF. No crea tareas adicionales propias, no usa mutexes y no define ISR de aplicación.

## Recursos compartidos

| Recurso | Propietario | Lectores | Escritores | Sincronización |
|---|---|---|---|---|
| `AppConfigData` | `AppConfigService` | `CommandConsole` | `CommandConsole` vía métodos | No requerida: acceso monohilo. |
| `JsonLog` | `Application` | Servicios | Servicios | No requerida: acceso monohilo. |
| `SensorSimulator` | `CommandConsole` | `CommandConsole` | Ninguno externo | No requerida. |

## ISR

No hay ISR de aplicación. Cualquier ISR interna del runtime ESP-IDF queda fuera del alcance del firmware LAB 01.

## Estado

```text
CUMPLE:
- Concurrencia monohilo documentada.
- Sin ISR de aplicación.
```
