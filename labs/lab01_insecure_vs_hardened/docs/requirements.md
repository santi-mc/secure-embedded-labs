# LAB 01 — Requisitos y trazabilidad

## Índice

- [Formato](#formato)
- [Requisitos](#requisitos)
- [Automatización de evidencia](#automatización-de-evidencia)
- [Estado global](#estado-global)

## Formato

Cada requisito sigue la cadena:

```text
requisito → diseño → implementación → test → evidencia → estado
```

## Requisitos

| ID | Tipo | Descripción | Diseño / implementación | Test | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| LAB01-FW-001 | Funcional | El firmware debe arrancar e imprimir evento de boot parseable. | `main`, `app_core`, `secure_log` | Boot en monitor | `lab01_insecure_console.log`, `lab01_hardened_console.log` | CUMPLE |
| LAB01-CON-001 | Funcional | La consola debe aceptar comandos por USB Serial/JTAG. | `board_hal`, `command_console` | `help` | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-CON-002 | Calidad | La consola no debe procesar cada carácter como comando independiente. | Buffer de línea en HAL | `help` como línea completa | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-CON-003 | Calidad | La consola no debe generar spam cuando no hay datos en stdin. | Estado `NoData` + backoff | Monitor tras boot | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-VUL-001 | Didáctico | INSECURE debe demostrar parsing débil. | Parser permisivo | `set_period 25s` | `lab01_insecure_console.log` | CUMPLE |
| LAB01-VUL-002 | Didáctico | INSECURE debe demostrar fuga de secreto ficticio. | Logs/config inseguros | `set_mqtt_password ...`, `get_config` | `lab01_insecure_console.log` | CUMPLE |
| LAB01-SEC-001 | Seguridad | HARDENED debe rechazar enteros mal formados. | Parser estricto | `set_period 25s` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-002 | Seguridad | HARDENED debe rechazar periodos fuera de rango. | Validación de rango | `set_period 0` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-003 | Seguridad | HARDENED no debe exponer secretos al actualizar password. | Redacción de argumentos | `set_mqtt_password ...` | `lab01_secret_scan.txt` | CUMPLE si scanner PASS |
| LAB01-SEC-004 | Seguridad | HARDENED no debe exponer secretos en `get_config`. | Redacción de configuración | `get_config` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-005 | Seguridad | HARDENED debe bloquear `factory_reset`. | Política de autorización | `factory_reset` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-QA-001 | Calidad | Gates estáticos del repo y del lab deben pasar. | Scripts QA | Ejecución local | `lab01_static_gates.txt` | CUMPLE si gates PASS |
| LAB01-QA-002 | Calidad | Build ESP-IDF debe cerrarse con evidencia completa. | ESP-IDF build | `idf.py build` | `lab01_build_esp32s3.txt` | PENDIENTE |
| LAB01-QA-003 | Seguridad | Scanner de secretos debe cerrarse con evidencia completa. | `check_no_secrets_in_logs.py` | Scanner sobre logs | `lab01_secret_scan.txt` | CUMPLE si scanner PASS |

## Automatización de evidencia

| Script | Requisito cubierto |
| --- | --- |
| `tools/capture_console_evidence.py` | LAB01-FW-001, LAB01-CON-001, LAB01-VUL-001, LAB01-VUL-002, LAB01-SEC-001..005 |
| `tools/capture_static_gates.py` | LAB01-QA-001 |
| `tools/capture_secret_scan.py` | LAB01-QA-003 |

## Estado global

```text
CUMPLE:
- Trazabilidad funcional principal cerrada con evidencias de consola.
- Comportamientos INSECURE y HARDENED diferenciados.
- Fixes de consola validados.
- Automatización de evidencias añadida.

NO VALIDADO:
- Build completo con cero warnings hasta versionar stdout.

PENDIENTE:
- Regenerar evidencias automáticas.
- Completar evidencia de build formal.
```
