# LAB 01 — Evidencias

## Índice

- [Objetivo](#objetivo)
- [Evidencias versionadas](#evidencias-versionadas)
- [Evidencias pendientes](#evidencias-pendientes)
- [Criterio de auditoría](#criterio-de-auditoría)
- [Estado](#estado)

## Objetivo

Este directorio contiene evidencias capturadas en placa real durante el LAB 01.

Las evidencias deben ser pequeñas, legibles, reproducibles y no contener secretos reales.

## Evidencias versionadas

| Fichero | Estado | Descripción |
| --- | --- | --- |
| `lab01_insecure_console.log` | CUMPLE | Evidencia del perfil INSECURE demostrando la fuga didáctica de secreto. |
| `lab01_hardened_console.log` | CUMPLE | Evidencia del perfil HARDENED con redacción de secretos. |
| `lab01_secret_scan.txt` | CUMPLE | Evidencia del scanner de secretos sobre logs INSECURE/HARDENED. |
| `lab01_static_gates.txt` | CUMPLE | Evidencia de gates estáticos globales y del LAB 01. |

## Evidencias pendientes

| Fichero | Estado | Motivo |
| --- | --- | --- |
| `lab01_build_esp32s3.txt` | PENDIENTE | Falta capturar stdout completo de `idf.py build` con cero warnings. |

## Criterio de auditoría

`INSECURE` debe demostrar la vulnerabilidad intencionada. `HARDENED` debe demostrar que los secretos no aparecen en bruto.

No se deben editar manualmente logs para forzar un resultado `PASS`.

## Estado

```text
CUMPLE:
- Evidencias funcionales INSECURE/HARDENED capturadas.
- Secret scan capturado con PASS.
- Gates estáticos capturados con PASS.

NO VALIDADO:
- Build completo con stdout y cero warnings pendiente de evidencia versionada.
```
