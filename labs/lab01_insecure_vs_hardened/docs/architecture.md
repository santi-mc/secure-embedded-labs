# LAB 01 — Arquitectura

## Índice

- [Objetivo](#objetivo)
- [Vista de componentes](#vista-de-componentes)
- [Dependencias](#dependencias)
- [HAL/BSP](#halbsp)
- [Decisiones arquitectónicas](#decisiones-arquitectónicas)
- [Estado](#estado)

## Objetivo

Describir la arquitectura del firmware LAB 01 y su separación por responsabilidades.

## Vista de componentes

```text
main
 └── app_core
      ├── command_console
      ├── app_config
      ├── sensor_sim
      ├── security_status
      ├── secure_log
      └── board_hal
```

## Dependencias

| Componente | Responsabilidad | Dependencias principales |
|---|---|---|
| `app_core` | Composición de aplicación y perfil activo. | Todos los servicios. |
| `command_console` | Parsing y despacho de comandos. | Config, sensor, status, log. |
| `app_config` | Configuración en RAM y políticas INSECURE/HARDENED. | Dominio, log. |
| `secure_log` | Logs JSON/NDJSON. | Reloj abstracto. |
| `board_hal` | Consola stdio y reloj ESP-IDF. | `esp_timer`, stdio. |
| `security_status` | Estado de Secure Boot / Flash Encryption. | `bootloader_support`, `efuse`. |
| `sensor_sim` | Sensor simulado determinista. | Ninguna crítica. |
| `lab01_domain` | Contratos, tipos e interfaces. | Ninguna. |

## HAL/BSP

La consola se accede mediante `IConsoleInput`; el dominio no usa `uart_read_bytes`, UART0 ni APIs directas de driver UART. El reloj se accede mediante `IClock`.

## Decisiones arquitectónicas

| ID | Decisión | Justificación | Consecuencia |
|---|---|---|---|
| ADR-001 | Usar USB Serial/JTAG vía stdio. | Evita dependencia de conversor USB-UART externo. | Requiere `CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG`. |
| ADR-002 | Mantener configuración en RAM. | El foco del LAB 01 es fuga/validación, no NVS. | No hay persistencia entre resets. |
| ADR-003 | Dos perfiles por Kconfig. | Permite comparar vulnerabilidad y mitigación con el mismo código base. | Requiere dos builds para evidencia completa. |

## Estado

```text
CUMPLE:
- Arquitectura por componentes definida.
- HAL de consola y reloj definido.

NO VALIDADO:
- Build real pendiente.
```
