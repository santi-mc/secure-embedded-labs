# LAB 01 — Requisitos de seguridad

## Índice

- [Objetivo](#objetivo)
- [Vulnerabilidades intencionadas](#vulnerabilidades-intencionadas)
- [Mitigaciones obligatorias](#mitigaciones-obligatorias)
- [Requisitos de seguridad](#requisitos-de-seguridad)
- [Estado](#estado)

## Objetivo

Definir qué vulnerabilidades se enseñan y qué mitigaciones debe aplicar el perfil `HARDENED`.

## Vulnerabilidades intencionadas

| ID | Perfil | Vulnerabilidad | Evidencia esperada |
|---|---|---|---|
| V-001 | INSECURE | `get_config` expone `mqtt_password`. | Log `config_dump` con password. |
| V-002 | INSECURE | `set_period` acepta valores fuera de rango. | `set_period 0` aceptado. |
| V-003 | INSECURE | Parser débil acepta entradas mal formadas/parciales. | `set_period 10abc` aceptado como 10. |
| V-004 | INSECURE | Comandos brutos se registran en log. | `raw` contiene comando completo. |
| V-005 | INSECURE | Actualización de secreto imprime valor. | `secret_updated.value` contiene password. |
| V-006 | INSECURE | `factory_reset` disponible sin protección. | Evento `factory_reset` accepted. |

## Mitigaciones obligatorias

| ID | Perfil | Mitigación | Evidencia esperada |
|---|---|---|---|
| M-001 | HARDENED | `get_config` redacta secretos. | `mqtt_password` = `<redacted>`. |
| M-002 | HARDENED | `set_period` valida sintaxis estricta. | `set_period 10abc` rechazado. |
| M-003 | HARDENED | `set_period` valida rango. | `set_period 0` rechazado. |
| M-004 | HARDENED | Comandos sensibles no se loguean en bruto. | `args` = `<redacted>`. |
| M-005 | HARDENED | Actualización de secreto no imprime valor. | `secret_updated.value` = `<redacted>`. |
| M-006 | HARDENED | `factory_reset` queda bloqueado por política. | `command_rejected.reason` = `rejected_by_policy`. |

## Requisitos de seguridad

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| SR-001 | El perfil HARDENED no debe emitir secretos por logs. | `check_no_secrets_in_logs.py --profile hardened` PASS. |
| SR-002 | Toda entrada inválida debe rechazarse sin alterar configuración. | `get_config` antes/después conserva valor. |
| SR-003 | El perfil INSECURE debe demostrar vulnerabilidades, no ocultarlas. | `check_no_secrets_in_logs.py --profile insecure` PASS con fuga esperada. |

## Estado

```text
CUMPLE:
- Vulnerabilidades y mitigaciones están especificadas.

NO VALIDADO:
- Falta evidencia real de logs en placa.
```
