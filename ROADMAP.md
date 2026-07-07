# Roadmap — Secure Embedded Labs

## Índice

- [Estado general](#estado-general)
- [LAB 01](#lab-01)
- [LAB 02](#lab-02)
- [LAB 03](#lab-03)
- [Fases futuras](#fases-futuras)

## Estado general

El proyecto evoluciona como repositorio-libro audit-grade. Cada cambio debe mantener alineados código, documentación, libro, evidencias, gates y changelog.

## LAB 01

```text
CUMPLE:
- Firmware inseguro vs endurecido validado para el alcance actual.
```

## LAB 02

```text
CUMPLE:
- Identidad clonable frente a identidad derivada de hardware validada para el alcance actual.
```

## LAB 03

LAB 03 queda organizado como familia MQTT contra `test.mosquitto.org`.

```text
CUMPLE:
- LAB 03A — M03-1883 / MQTT TCP plano sin TLS ni autenticación / dry-run.

PENDIENTE:
- LAB 03B — M03-1884 / MQTT TCP plano con usuario/password.
- LAB 03C — M03-8883 y M03-8886 / MQTT TLS servidor.
- LAB 03D — M03-8885 / MQTT TLS con usuario/password.
- LAB 03E — M03-8884 / mTLS con certificado cliente.
- LAB 03F — M03-8887 / rechazo de certificado expirado.
- LAB 03G — MQTT over WebSockets.
```

## Fases futuras

LAB 04 a LAB 10 permanecen como placeholders hasta definición y evidencias.
