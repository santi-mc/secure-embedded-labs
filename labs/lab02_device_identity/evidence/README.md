# Evidencias LAB 02

## Índice

- [Propósito](#propósito)
- [Evidencias esperadas](#evidencias-esperadas)
- [Captura automática](#captura-automática)
- [Validación de logs](#validación-de-logs)
- [Criterio de auditoría](#criterio-de-auditoría)
- [Estado](#estado)

## Propósito

Este directorio contiene evidencias funcionales y de calidad asociadas al LAB 02.

Las evidencias versionadas deben ser pequeñas, legibles y reproducibles. No deben incluir secretos reales, credenciales privadas, tokens, claves, certificados privados ni datos de infraestructura sensible.

## Evidencias esperadas

| Fichero | Estado | Descripción |
| --- | --- | --- |
| `lab02_insecure_console.log` | PENDIENTE | Evidencia funcional del perfil INSECURE. |
| `lab02_hardened_console.log` | PENDIENTE | Evidencia funcional del perfil HARDENED. |
| `lab02_static_gates.txt` | PENDIENTE | Salida de gates estáticos. |
| `lab02_build_esp32s3.txt` | PENDIENTE | Salida completa de build ESP32-S3. |

## Captura automática

Desde la raíz del repositorio:

```powershell
python labs/lab02_device_identity/tools/capture_console_evidence.py `
  --port COMx `
  --profile insecure `
  --output labs/lab02_device_identity/evidence/lab02_insecure_console.log

python labs/lab02_device_identity/tools/capture_console_evidence.py `
  --port COMx `
  --profile hardened `
  --output labs/lab02_device_identity/evidence/lab02_hardened_console.log

python labs/lab02_device_identity/tools/capture_static_gates.py
```

## Validación de logs

```powershell
python labs/lab02_device_identity/tools/check_lab02_identity_logs.py labs/lab02_device_identity/evidence/lab02_insecure_console.log --profile insecure
python labs/lab02_device_identity/tools/check_lab02_identity_logs.py labs/lab02_device_identity/evidence/lab02_hardened_console.log --profile hardened
```

## Criterio de auditoría

No se deben versionar evidencias sintéticas. Cada fichero debe proceder de una ejecución real o estar marcado explícitamente como pendiente.

El script de captura añade líneas de comentario `# tx ...` para trazar comandos transmitidos. El scanner ignora líneas no JSON y valida únicamente eventos emitidos por el firmware.

## Estado

```text
CUMPLE:
- Documentado flujo automático de captura.

PENDIENTE:
- Capturar evidencias reales generadas por script.
```
