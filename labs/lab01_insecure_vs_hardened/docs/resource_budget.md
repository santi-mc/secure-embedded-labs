# LAB 01 — Presupuesto de recursos

## Índice

- [Objetivo](#objetivo)
- [Presupuesto inicial](#presupuesto-inicial)
- [Política de memoria dinámica](#política-de-memoria-dinámica)
- [Estado](#estado)

## Objetivo

Fijar presupuesto inicial para LAB 01.

## Presupuesto inicial

| Recurso | Presupuesto | Observación |
|---|---:|---|
| Flash | < 512 KiB esperado | Pendiente medir tras build. |
| RAM estática | < 64 KiB esperado | Pendiente map file. |
| Heap mínimo libre | > 64 KiB esperado | Pendiente runtime. |
| Stack task principal | Default ESP-IDF | Pendiente validar si `idf.py build` advierte. |
| CPU | Interactivo, sin carga periódica | N/A. |
| Línea consola | 32..512 bytes | Default 160. |

## Política de memoria dinámica

El laboratorio usa C++ estándar (`std::string`, `std::vector`) en ruta de consola interactiva, no en una ruta hard real-time. Esta decisión se acepta por alcance didáctico, pero queda documentada como deuda si el patrón se promoviera a producto.

## Estado

```text
CUMPLE:
- Presupuesto inicial declarado.

NO VALIDADO:
- Map file, stack y heap pendientes de medición real.
```
