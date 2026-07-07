# Matriz MQTT — LAB 03

## Índice

- [Matriz](#matriz)
- [Criterio](#criterio)
- [Estado](#estado)

## Matriz

| Sublab | Escenario | Puerto | TLS | Auth | Estado |
| --- | --- | ---: | --- | --- | --- |
| LAB 03A | M03-1883 | 1883 | No | No | CUMPLE dry-run |
| LAB 03B | M03-1884 | 1884 | No | Usuario/password | PENDIENTE |
| LAB 03C | M03-8883 / M03-8886 | 8883 / 8886 | Sí | No | PENDIENTE |
| LAB 03D | M03-8885 | 8885 | Sí | Usuario/password | PENDIENTE |
| LAB 03E | M03-8884 | 8884 | Sí | Certificado cliente | PENDIENTE |
| LAB 03F | M03-8887 | 8887 | Sí, expirado | No | PENDIENTE |
| LAB 03G | M03-8080/8081/8090/8091 | 8080/8081/8090/8091 | Mixto | Mixto | PENDIENTE |

## Criterio

Los escenarios sin TLS pueden ser funcionales, pero no cumplen seguridad para credenciales ni datos sensibles.

## Estado

```text
CUMPLE:
- Matriz documentada.

PENDIENTE:
- Completar LAB 03B y siguientes con evidencias propias.
```
