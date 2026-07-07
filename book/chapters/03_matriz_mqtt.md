# Capítulo 03 — Matriz MQTT contra test.mosquitto.org

## Índice

- [Objetivo](#objetivo)
- [Idea central](#idea-central)
- [Matriz](#matriz)
- [Estado](#estado)

## Objetivo

Explicar LAB 03 como una familia de escenarios MQTT donde una conexión funcional no implica cumplimiento de seguridad.

## Idea central

MQTT puede funcionar sin confidencialidad, sin autenticación, con autenticación sin TLS, con TLS validado, con mTLS o sobre WebSockets. Cada combinación protege activos distintos y debe evidenciarse por separado.

## Matriz

LAB 03 se divide en:

- LAB 03A — M03-1883 / MQTT TCP plano sin autenticación.
- LAB 03B — M03-1884 / MQTT TCP plano con usuario/password.
- LAB 03C — M03-8883/M03-8886 / TLS servidor.
- LAB 03D — M03-8885 / TLS + usuario/password.
- LAB 03E — M03-8884 / mTLS.
- LAB 03F — M03-8887 / certificado expirado.
- LAB 03G — MQTT over WebSockets.

## Estado

```text
CUMPLE:
- LAB 03A documentado como baseline inseguro dry-run.

PENDIENTE:
- Completar LAB 03B–LAB 03G.
```
