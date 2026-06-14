# LAB 02 — Plan de pruebas

## Índice

- [Objetivo](#objetivo)
- [Pruebas INSECURE](#pruebas-insecure)
- [Pruebas HARDENED](#pruebas-hardened)
- [Pruebas de gates](#pruebas-de-gates)
- [Pruebas pendientes](#pruebas-pendientes)
- [Estado](#estado)

## Objetivo

Definir las pruebas necesarias para cerrar el LAB 02 con evidencias auditables.

## Pruebas INSECURE

| Prueba | Estado | Evidencia |
| --- | --- | --- |
| Boot INSECURE | CUMPLE | `evidence/lab02_insecure_console.log` |
| `identity_status` muestra identidad mutable | CUMPLE | `evidence/lab02_insecure_console.log` |
| `set_device_id CLONED-DEVICE-001` aceptado | CUMPLE | `evidence/lab02_insecure_console.log` |
| `get_claim` emite claim clonable | CUMPLE | `evidence/lab02_insecure_console.log` |

## Pruebas HARDENED

| Prueba | Estado | Evidencia |
| --- | --- | --- |
| Boot HARDENED | CUMPLE | `evidence/lab02_hardened_console.log` |
| `identity_status` muestra identidad derivada | CUMPLE | `evidence/lab02_hardened_console.log` |
| `raw_hardware_id` aparece redactado | CUMPLE | `evidence/lab02_hardened_console.log` |
| `set_device_id` rechazado | CUMPLE | `evidence/lab02_hardened_console.log` |
| `get_claim` no expone token secreto | CUMPLE | `evidence/lab02_hardened_console.log` |

## Pruebas de gates

| Prueba | Estado | Evidencia |
| --- | --- | --- |
| Gate global del repo | CUMPLE | `evidence/lab02_static_gates.txt` |
| Gate estático LAB 02 | CUMPLE | `evidence/lab02_static_gates.txt` |
| Validador de logs INSECURE | CUMPLE | `evidence/lab02_insecure_console.log` |
| Validador de logs HARDENED | CUMPLE | `evidence/lab02_hardened_console.log` |

## Pruebas pendientes

| Prueba | Estado | Motivo |
| --- | --- | --- |
| Build completo con stdout | PENDIENTE | Falta `evidence/lab02_build_esp32s3.txt`. |

## Estado

```text
CUMPLE:
- Pruebas funcionales INSECURE/HARDENED validadas.
- Gates estáticos capturados con PASS.

NO VALIDADO:
- Build completo con stdout versionado.
```
