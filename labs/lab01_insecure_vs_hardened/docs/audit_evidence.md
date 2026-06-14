# LAB 01 — Evidencia de auditoría

## Índice

- [Resumen](#resumen)
- [Entorno](#entorno)
- [Evidencias versionadas](#evidencias-versionadas)
- [Captura automática](#captura-automática)
- [Validación funcional](#validación-funcional)
- [Gates](#gates)
- [Limitaciones](#limitaciones)
- [Estado](#estado)

## Resumen

Este documento registra la evidencia disponible para el LAB 01: firmware inseguro vs firmware endurecido.

El laboratorio fue probado localmente sobre ESP32-S3 con consola USB Serial/JTAG. A partir de esta actualización, las evidencias de consola, gates estáticos y scanner de secretos pueden regenerarse mediante scripts de captura.

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
| --- | --- | --- |
| `evidence/lab01_insecure_console.log` | Log funcional INSECURE | CUMPLE si `capture_validation result=PASS` |
| `evidence/lab01_hardened_console.log` | Log funcional HARDENED | CUMPLE si `capture_validation result=PASS` |
| `evidence/lab01_static_gates.txt` | Gates estáticos raw | CUMPLE si `capture_validation result=PASS` |
| `evidence/lab01_secret_scan.txt` | Scanner de secretos raw | CUMPLE si `capture_validation result=PASS` |
| `evidence/lab01_build_esp32s3.txt` | Build completo ESP-IDF | PENDIENTE |

## Captura automática

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py --port COMx --profile insecure --output labs\lab01_insecure_vs_hardened\evidence\lab01_insecure_console.log
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py --port COMx --profile hardened --output labs\lab01_insecure_vs_hardened\evidence\lab01_hardened_console.log
python labs\lab01_insecure_vs_hardened\tools\capture_static_gates.py
python labs\lab01_insecure_vs_hardened\tools\capture_secret_scan.py
```

## Validación funcional

| Caso | Perfil | Resultado esperado | Evidencia | Estado |
| --- | --- | --- | --- | --- |
| Boot INSECURE | INSECURE | Arranque con perfil INSECURE | `lab01_insecure_console.log` | CUMPLE |
| Consola sin spam EOF | INSECURE/HARDENED | Sin bucle `stdin_eof` | Logs de consola | CUMPLE |
| Buffer de línea | INSECURE/HARDENED | `help` llega como línea completa | Logs de consola | CUMPLE |
| Parser débil | INSECURE | `set_period 25s` aceptado como vulnerabilidad | `lab01_insecure_console.log` | CUMPLE |
| Parser estricto | HARDENED | `set_period 25s` rechazado | `lab01_hardened_console.log` | CUMPLE |
| Rango estricto | HARDENED | `set_period 0` rechazado | `lab01_hardened_console.log` | CUMPLE |
| Config válida | HARDENED | `set_period 60` aceptado | `lab01_hardened_console.log` | CUMPLE |
| Redacción de secretos | HARDENED | Password no visible | `lab01_secret_scan.txt` | CUMPLE si scanner PASS |
| Reset protegido | HARDENED | `factory_reset` bloqueado | `lab01_hardened_console.log` | CUMPLE |

## Gates

Los gates estáticos deben capturarse con:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_static_gates.py
```

El scanner de secretos debe capturarse con:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_secret_scan.py
```

## Limitaciones

```text
NO VALIDADO:
- No se versiona todavía stdout completo de `idf.py build`.
- No se aporta hash de binario flasheado.
- No se aporta versión exacta de ESP-IDF/toolchain en evidencia formal.
```

## Estado

```text
CUMPLE:
- Validación funcional INSECURE/HARDENED documentada.
- Scripts de captura automática añadidos.
- Estados y limitaciones declarados.

PENDIENTE:
- Regenerar evidencias automáticas en hardware local.
- Capturar build completo.
- Registrar versión ESP-IDF/toolchain.
```
