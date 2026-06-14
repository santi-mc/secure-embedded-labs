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
| LAB02-FR-002 | INSECURE debe usar ID clonable. | `lab02_insecure_console.log` |
| LAB02-FR-003 | INSECURE debe permitir sobrescribir ID por consola. | `set_device_id` en `lab02_insecure_console.log` |
| LAB02-FR-004 | HARDENED debe derivar ID estable desde fuente hardware. | `lab02_hardened_console.log` |
| LAB02-FR-005 | HARDENED debe rechazar sobrescritura de ID. | `identity_update_rejected` en `lab02_hardened_console.log` |
| LAB02-FR-006 | El flujo de captura debe poder ejecutarse sin edición manual de logs. | `tools/capture_console_evidence.py` |

## Requisitos de calidad

| ID | Requisito | Verificación |
| --- | --- | --- |
| LAB02-QR-001 | Logs JSON/NDJSON. | inspección de consola y scanner |
| LAB02-QR-002 | Sin secretos en HARDENED. | `tools/check_lab02_identity_logs.py` |
| LAB02-QR-003 | Gates estáticos propios. | `tools/run_static_gates.py` |
| LAB02-QR-004 | Build sin warnings. | `idf.py build` |
| LAB02-QR-005 | Evidencias reproducibles por script. | `tools/capture_console_evidence.py` y `tools/capture_static_gates.py` |

## Trazabilidad

| Requisito | Implementación | Prueba | Evidencia |
| --- | --- | --- | --- |
| LAB02-FR-002 | `identity_service` INSECURE | `get_identity` | `evidence/lab02_insecure_console.log` |
| LAB02-FR-003 | `set_device_id` INSECURE | actualización aceptada | `evidence/lab02_insecure_console.log` |
| LAB02-FR-004 | `identity_service` HARDENED | `identity_status` | `evidence/lab02_hardened_console.log` |
| LAB02-FR-005 | política HARDENED | actualización rechazada | `evidence/lab02_hardened_console.log` |
| LAB02-QR-005 | scripts de captura | ejecución automática | logs generados en `evidence/` |

## Estado

```text
CUMPLE:
- Requisitos iniciales definidos.
- Trazabilidad actualizada para capturas automáticas.

NO VALIDADO:
- Evidencias automáticas pendientes de generación y commit.
- Build completo con cero warnings pendiente de evidencia.
```
