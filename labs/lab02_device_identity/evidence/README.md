# LAB 02 — Evidencias

## Índice

- [Objetivo](#objetivo)
- [Evidencias versionadas](#evidencias-versionadas)
- [Evidencias pendientes](#evidencias-pendientes)
- [Criterio de auditoría](#criterio-de-auditoría)
- [Estado](#estado)

## Objetivo

Este directorio contiene evidencias capturadas en placa real durante el LAB 02.

Las evidencias demuestran el contraste entre identidad clonable/mutable en `INSECURE` e identidad derivada/no mutable en `HARDENED`.

## Evidencias versionadas

| Fichero | Estado | Descripción |
| --- | --- | --- |
| `lab02_insecure_console.log` | CUMPLE | Evidencia del perfil INSECURE con identidad mutable y claim clonable. |
| `lab02_hardened_console.log` | CUMPLE | Evidencia del perfil HARDENED con identidad derivada, raw hardware ID redactado y `set_device_id` rechazado. |
| `lab02_static_gates.txt` | CUMPLE | Evidencia de gates estáticos globales y del LAB 02. |

## Evidencias pendientes

| Fichero | Estado | Motivo |
| --- | --- | --- |
| `lab02_build_esp32s3.txt` | PENDIENTE | Falta capturar stdout completo de `idf.py build` con cero warnings. |

## Criterio de auditoría

`INSECURE` debe demostrar la vulnerabilidad intencionada. `HARDENED` debe demostrar que el identificador no es mutable por consola y que no se exponen identificadores brutos.

Los logs deben incluir `capture_validation result=PASS` cuando han sido capturados por el script automático.

## Estado

```text
CUMPLE:
- Evidencias funcionales INSECURE/HARDENED capturadas.
- Validadores de identidad ejecutados con PASS.
- Gates estáticos capturados con PASS.

NO VALIDADO:
- Build completo con stdout y cero warnings pendiente de evidencia versionada.
```
