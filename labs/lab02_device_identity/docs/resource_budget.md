# Presupuesto de recursos LAB 02

## Índice

- [Objetivo](#objetivo)
- [Presupuesto inicial](#presupuesto-inicial)
- [Política de memoria](#política-de-memoria)
- [Estado](#estado)

## Objetivo

Definir expectativas de recursos para el laboratorio.

## Presupuesto inicial

| Recurso | Presupuesto | Observación |
| --- | ---:| --- |
| Flash app | < 1 MB | Laboratorio pequeño. |
| Heap dinámico | Bajo | Uso limitado de `std::string`. |
| Stack app_main | Default ESP-IDF | Sin recursión ni buffers grandes. |
| CPU | Ociosa salvo comandos | Backoff en consola sin datos. |

## Política de memoria

Se permite memoria dinámica acotada para simplicidad didáctica. No se usa en ISR.

## Estado

```text
NO VALIDADO:
- Medición real pendiente tras build.
```
