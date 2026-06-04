# LAB 01 — Requisitos

## Índice

- [Objetivo](#objetivo)
- [Requisitos funcionales](#requisitos-funcionales)
- [Requisitos de calidad](#requisitos-de-calidad)
- [Trazabilidad inicial](#trazabilidad-inicial)
- [Estado](#estado)

## Objetivo

Definir los requisitos funcionales y de calidad del LAB 01.

## Requisitos funcionales

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| FR-001 | El firmware debe exponer una consola interactiva por USB Serial/JTAG. | `help` responde desde `idf.py monitor`. |
| FR-002 | El firmware debe soportar perfiles `INSECURE` y `HARDENED` seleccionables por Kconfig. | `boot.profile` refleja el perfil activo. |
| FR-003 | Deben existir comandos `help`, `status`, `security_status`, `sample`, `get_config`, `set_period`, `set_mqtt_password` y `factory_reset`. | Todos aparecen en `help` y producen logs JSON. |
| FR-004 | El sensor simulado debe emitir una muestra determinista. | `sample` genera `sensor_sample`. |
| FR-005 | La configuración debe residir en RAM para este laboratorio. | `factory_reset` restaura defaults solo en RAM. |

## Requisitos de calidad

| ID | Requisito | Criterio de aceptación |
|---|---|---|
| QR-001 | Build ESP32-S3 limpio. | `idf.py build` sin errores ni warnings. |
| QR-002 | No usar UART0 directa para comandos. | Gate estático no detecta `uart_read_bytes`, `driver/uart.h` ni `UART_NUM_0`. |
| QR-003 | Logs JSON línea a línea. | Eventos parseables y con `schema_version`. |
| QR-004 | Documentación audit-grade mínima. | Docs del laboratorio presentes y con índice. |

## Trazabilidad inicial

| Requisito | Diseño | Implementación | Test | Evidencia |
|---|---|---|---|---|
| FR-001 | `board_hal::StdioConsoleInput` | `firmware/components/board_hal` | `help` en monitor | Pendiente |
| FR-002 | Kconfig `LAB01_SECURITY_PROFILE` | `main/Kconfig.projbuild` | Build de ambos perfiles | Pendiente |
| QR-002 | Consola stdio | `command_console` + HAL | `tools/run_static_gates.py` | Pendiente |

## Estado

```text
CUMPLE:
- Requisitos iniciales definidos.

NO VALIDADO:
- Evidencia real pendiente de hardware.
```
