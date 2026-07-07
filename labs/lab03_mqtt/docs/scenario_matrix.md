# Matriz de escenarios — LAB 03 MQTT

## Índice

- [Propósito](#proposito)
- [Matriz](#matriz)
- [Criterio de cierre](#criterio-de-cierre)
- [Estado](#estado)

## Propósito

Definir la matriz contractual MQTT contra `test.mosquitto.org`.

## Matriz

| Sublab | Escenario | Puerto | Transporte | TLS | Autenticación | Estado |
| --- | --- | ---: | --- | --- | --- | --- |
| LAB 03A | M03-1883 | 1883 | MQTT TCP | No | No | CUMPLE dry-run |
| LAB 03B | M03-1884 | 1884 | MQTT TCP | No | Usuario/password | PENDIENTE |
| LAB 03C | M03-8883 / M03-8886 | 8883 / 8886 | MQTT TCP | Sí | No | PENDIENTE |
| LAB 03D | M03-8885 | 8885 | MQTT TCP | Sí | Usuario/password | PENDIENTE |
| LAB 03E | M03-8884 | 8884 | MQTT TCP | Sí | Certificado cliente | PENDIENTE |
| LAB 03F | M03-8887 | 8887 | MQTT TCP | Sí, expirado | No | PENDIENTE |
| LAB 03G | M03-8080/8081/8090/8091 | Mixto | WebSockets | Mixto | Mixto | PENDIENTE |

## Criterio de cierre

Cada sublaboratorio debe tener documentación, evidencia propia, gates y estado explícito.

## Estado

```text
CUMPLE:
- Matriz definida.

PENDIENTE:
- Implementar y validar LAB 03B–LAB 03G.
```
