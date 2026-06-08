# LAB 01 — Evidencia de auditoría

## Índice

- [Resumen](#resumen)
- [Entorno](#entorno)
- [Evidencias versionadas](#evidencias-versionadas)
- [Validación funcional](#validación-funcional)
- [Gates](#gates)
- [Limitaciones](#limitaciones)
- [Estado](#estado)

## Resumen

Este documento registra la evidencia disponible para el LAB 01: firmware inseguro vs firmware endurecido.

El laboratorio fue probado localmente sobre ESP32-S3 con consola USB Serial/JTAG. Las evidencias de consola se guardan como logs NDJSON en `evidence/`.

## Entorno

```text
Proyecto: secure_embedded_labs_lab01
Firmware: 0.1.0
Target: esp32s3
Transporte consola: usb_serial_jtag_stdio
Perfiles probados: INSECURE, HARDENED
```

## Evidencias versionadas

| Evidencia | Tipo | Estado |
|---|---|---|
| `evidence/lab01_insecure_console.log` | Log funcional INSECURE | CUMPLE |
| `evidence/lab01_hardened_console.log` | Log funcional HARDENED | CUMPLE |
| `evidence/lab01_static_gates_reported.txt` | Gates reportados por operador | CUMPLE con limitación |
| `evidence/lab01_build_esp32s3.txt` | Build completo ESP-IDF | PENDIENTE |
| `evidence/lab01_secret_scan.txt` | Scanner de secretos | PENDIENTE |

## Validación funcional

| Caso | Perfil | Resultado esperado | Resultado observado | Estado |
|---|---|---|---|---|
| Boot INSECURE | INSECURE | Arranque con perfil INSECURE | `profile":"INSECURE"` | CUMPLE |
| Consola sin spam EOF | INSECURE/HARDENED | Sin bucle `stdin_eof` | No aparece spam tras fixes | CUMPLE |
| Buffer de línea | INSECURE/HARDENED | `help` llega como línea completa | `raw":"help"` / `cmd":"help"` | CUMPLE |
| Comando desconocido | INSECURE | `period` rechazado | `unknown_command` | CUMPLE |
| Parser débil | INSECURE | `set_period 25s` aceptado como vulnerabilidad | `value":"25"` | CUMPLE |
| Parser estricto | HARDENED | `set_period 25s` rechazado | `invalid_uint32` | CUMPLE |
| Rango estricto | HARDENED | `set_period 0` rechazado | `out_of_range` | CUMPLE |
| Config válida | HARDENED | `set_period 60` aceptado | `value":"60"` | CUMPLE |
| Redacción de secretos | HARDENED | Password no visible | `args":"<redacted>"` y `value":"<redacted>"` | CUMPLE |
| Dump seguro | HARDENED | `mqtt_password` redactado | `mqtt_password":"<redacted>"` | CUMPLE |
| Reset protegido | HARDENED | `factory_reset` bloqueado | `rejected_by_policy` | CUMPLE |

## Gates

El operador reportó que pasaron:

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
python labs/lab01_insecure_vs_hardened/tools/run_static_gates.py
```

La salida raw completa debe guardarse como evidencia cuando se cierre el laboratorio con criterio audit-grade estricto.

## Limitaciones

```text
NO VALIDADO:
- No se versiona todavía stdout completo de `idf.py build`.
- No se versiona todavía stdout completo del scanner de secretos.
- No se aporta hash de binario flasheado.
- No se aporta versión exacta de ESP-IDF/toolchain en evidencia formal.
```

## Estado

```text
CUMPLE:
- Validación funcional INSECURE/HARDENED documentada.
- Evidencias de consola versionadas.
- Estados y limitaciones declarados.

PENDIENTE:
- Capturar build completo.
- Capturar scanner de secretos.
- Registrar versión ESP-IDF/toolchain.
```
