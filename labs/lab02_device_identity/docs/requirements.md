# Requisitos LAB 02

## Índice

- [Objetivo](#objetivo)
- [Requisitos funcionales](#requisitos-funcionales)
- [Requisitos de calidad](#requisitos-de-calidad)
- [Trazabilidad](#trazabilidad)
- [Estado](#estado)

## Objetivo

Definir requisitos verificables para el laboratorio de identidad única.

## Requisitos funcionales

| ID | Requisito | Verificación |
| --- | --- | --- |
| LAB02-FR-001 | El firmware debe mostrar estado de identidad. | `identity_status` |
| LAB02-FR-002 | INSECURE debe usar ID clonable. | log INSECURE |
| LAB02-FR-003 | INSECURE debe permitir sobrescribir ID por consola. | `set_device_id` |
| LAB02-FR-004 | HARDENED debe derivar ID estable desde fuente hardware. | log HARDENED |
| LAB02-FR-005 | HARDENED debe rechazar sobrescritura de ID. | `set_device_id` |

## Requisitos de calidad

| ID | Requisito | Verificación |
| --- | --- | --- |
| LAB02-QR-001 | Logs JSON/NDJSON. | inspección de consola |
| LAB02-QR-002 | Sin secretos en HARDENED. | scanner de logs |
| LAB02-QR-003 | Gates estáticos propios. | `tools/run_static_gates.py` |
| LAB02-QR-004 | Build sin warnings. | `idf.py build` |

## Trazabilidad

La trazabilidad se cerrará en `docs/audit_evidence.md` tras capturar evidencias reales.

## Estado

```text
CUMPLE:
- Requisitos iniciales definidos.

NO VALIDADO:
- Evidencias reales pendientes.
```
