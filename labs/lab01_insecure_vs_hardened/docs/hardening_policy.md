# LAB 01 — Política de hardening

## Índice

- [Objetivo](#objetivo)
- [Perfil INSECURE](#perfil-insecure)
- [Perfil HARDENED](#perfil-hardened)
- [Estado](#estado)

## Objetivo

Definir la diferencia entre vulnerabilidad intencionada y mitigación.

## Perfil INSECURE

El perfil `INSECURE` existe para demostrar fallos: exposición de secretos, parsing débil, logging inseguro y reset sin protección.

## Perfil HARDENED

El perfil `HARDENED` aplica mitigaciones mínimas: redacción, parser estricto, validación de rango, rechazo por política y logs seguros.

## Estado

```text
CUMPLE:
- Política de hardening definida.

NO CUMPLE como producto:
- No incluye hardening físico ni arranque seguro.
```
