# LAB 02 — Requisitos

## Índice

- [Objetivo](#objetivo)
- [Requisitos funcionales](#requisitos-funcionales)
- [Requisitos de seguridad](#requisitos-de-seguridad)
- [Trazabilidad](#trazabilidad)
- [Estado](#estado)

## Objetivo

Definir los requisitos verificables del LAB 02 y su trazabilidad hacia evidencias.

## Requisitos funcionales

| ID | Requisito | Estado |
| --- | --- | --- |
| LAB02-FR-001 | El firmware debe exponer `identity_status`. | CUMPLE |
| LAB02-FR-002 | El firmware debe exponer `get_identity`. | CUMPLE |
| LAB02-FR-003 | El firmware debe exponer `get_claim`. | CUMPLE |
| LAB02-FR-004 | El perfil INSECURE debe permitir `set_device_id`. | CUMPLE |
| LAB02-FR-005 | El perfil HARDENED debe rechazar `set_device_id`. | CUMPLE |

## Requisitos de seguridad

| ID | Requisito | Estado |
| --- | --- | --- |
| LAB02-SR-001 | HARDENED no debe exponer raw hardware ID. | CUMPLE |
| LAB02-SR-002 | HARDENED no debe emitir token secreto. | CUMPLE |
| LAB02-SR-003 | HARDENED debe derivar identidad desde fuente no mutable por consola. | CUMPLE |
| LAB02-SR-004 | INSECURE debe demostrar identidad clonable como vulnerabilidad didáctica. | CUMPLE |

## Trazabilidad

| Requisito | Evidencia |
| --- | --- |
| LAB02-FR-001 | `evidence/lab02_insecure_console.log`, `evidence/lab02_hardened_console.log` |
| LAB02-FR-002 | `evidence/lab02_insecure_console.log`, `evidence/lab02_hardened_console.log` |
| LAB02-FR-003 | `evidence/lab02_insecure_console.log`, `evidence/lab02_hardened_console.log` |
| LAB02-FR-004 | `evidence/lab02_insecure_console.log` |
| LAB02-FR-005 | `evidence/lab02_hardened_console.log` |
| LAB02-SR-001 | `evidence/lab02_hardened_console.log` |
| LAB02-SR-002 | `evidence/lab02_hardened_console.log` |
| LAB02-SR-003 | `evidence/lab02_hardened_console.log` |
| LAB02-SR-004 | `evidence/lab02_insecure_console.log` |

## Estado

```text
CUMPLE:
- Requisitos funcionales y de seguridad trazados a evidencias.

NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.
```
