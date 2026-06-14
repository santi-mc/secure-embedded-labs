# Evidencias LAB 01

## Índice

- [Propósito](#propósito)
- [Evidencias incluidas](#evidencias-incluidas)
- [Evidencias pendientes](#evidencias-pendientes)
- [Captura automática](#captura-automática)
- [Criterio de auditoría](#criterio-de-auditoría)

## Propósito

Este directorio contiene evidencias funcionales y de calidad asociadas al LAB 01.

Las evidencias versionadas deben ser pequeñas, legibles y reproducibles. No deben incluir secretos reales, credenciales privadas, tokens, claves, certificados privados ni datos de infraestructura sensible.

## Evidencias incluidas

| Fichero | Estado | Descripción |
| --- | --- | --- |
| `lab01_insecure_console.log` | CUMPLE si `capture_validation result=PASS` | Evidencia funcional del perfil INSECURE en ESP32-S3. |
| `lab01_hardened_console.log` | CUMPLE si `capture_validation result=PASS` | Evidencia funcional del perfil HARDENED en ESP32-S3. |
| `lab01_static_gates.txt` | CUMPLE si `capture_validation result=PASS` | Resultado raw de gates estáticos del repo y del LAB 01. |
| `lab01_secret_scan.txt` | CUMPLE si `capture_validation result=PASS` | Resultado raw del scanner de secretos sobre logs INSECURE/HARDENED. |

## Evidencias pendientes

| Evidencia | Estado | Motivo |
| --- | --- | --- |
| `lab01_build_esp32s3.txt` | PENDIENTE | Falta capturar stdout completo de `idf.py build`. |

## Captura automática

Desde la raíz del repositorio:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py --port COMx --profile insecure --output labs\lab01_insecure_vs_hardened\evidence\lab01_insecure_console.log
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py --port COMx --profile hardened --output labs\lab01_insecure_vs_hardened\evidence\lab01_hardened_console.log
python labs\lab01_insecure_vs_hardened\tools\capture_static_gates.py
python labs\lab01_insecure_vs_hardened\tools\capture_secret_scan.py
```

## Criterio de auditoría

Una evidencia solo debe marcarse como `CUMPLE` cuando exista salida real capturada o una observación manual explícita y trazable.

No se deben generar evidencias sintéticas para simular builds, tests, gates o análisis de seguridad.
