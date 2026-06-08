# Evidencias LAB 01

## Índice

- [Prop?sito](#prop?sito)
- [Evidencias incluidas](#evidencias-incluidas)
- [Evidencias pendientes](#evidencias-pendientes)
- [Criterio de auditor?a](#criterio-de-auditor?a)

## Propósito

Este directorio contiene evidencias funcionales y de calidad asociadas al LAB 01.

Las evidencias versionadas deben ser peque?as, legibles y reproducibles. No deben incluir secretos reales, credenciales privadas, tokens, claves, certificados privados ni datos de infraestructura sensible.

## Evidencias incluidas

| Fichero | Estado | Descripci?n |
| --- | --- | --- |
| `lab01_insecure_console.log` | CUMPLE | Evidencia funcional del perfil INSECURE en ESP32-S3. |
| `lab01_hardened_console.log` | CUMPLE | Evidencia funcional del perfil HARDENED en ESP32-S3. |
| `lab01_static_gates_reported.txt` | CUMPLE | Resultado reportado de gates est?ticos del repo y del LAB 01. |

## Evidencias pendientes

| Evidencia | Estado | Motivo |
| --- | --- | --- |
| `lab01_build_esp32s3.txt` | PENDIENTE | Falta capturar stdout completo de `idf.py build`. |
| `lab01_secret_scan.txt` | PENDIENTE | Falta capturar stdout real del scanner de secretos sobre logs. |

## Criterio de auditoría

Una evidencia solo debe marcarse como `CUMPLE` cuando exista salida real capturada o una observaci?n manual expl?cita y trazable.

No se deben generar evidencias sint?ticas para simular builds, tests, gates o an?lisis de seguridad.
