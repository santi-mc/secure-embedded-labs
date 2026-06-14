# Evidencias de auditoría LAB 02

## Índice

- [Objetivo](#objetivo)
- [Matriz de evidencias](#matriz-de-evidencias)
- [Comandos de captura](#comandos-de-captura)
- [Criterio de cierre](#criterio-de-cierre)
- [Estado](#estado)

## Objetivo

Registrar evidencias necesarias para cerrar el LAB 02 con trazabilidad requisito → implementación → prueba → evidencia.

## Matriz de evidencias

| Evidencia | Estado | Archivo esperado | Generación |
| --- | --- | --- | --- |
| Gates estáticos LAB 02 | PENDIENTE | `evidence/lab02_static_gates.txt` | `tools/capture_static_gates.py` |
| Build ESP32-S3 | PENDIENTE | `evidence/lab02_build_esp32s3.txt` | captura stdout de `idf.py build` |
| Perfil INSECURE | PENDIENTE | `evidence/lab02_insecure_console.log` | `tools/capture_console_evidence.py --profile insecure` |
| Perfil HARDENED | PENDIENTE | `evidence/lab02_hardened_console.log` | `tools/capture_console_evidence.py --profile hardened` |
| Scanner de logs | PENDIENTE | salida del scanner | `tools/check_lab02_identity_logs.py` |

## Comandos de captura

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

## Criterio de cierre

El laboratorio no se considerará cerrado como audit-grade hasta que existan logs reales de ambos perfiles, gates estáticos capturados y build real sin warnings.

La validación manual ya demostró el comportamiento INSECURE/HARDENED, pero el cierre documental exige evidencias versionadas generadas o capturadas desde el árbol de trabajo.

## Estado

```text
CUMPLE:
- Scripts de captura automática definidos.
- Validación funcional manual realizada por el operador en ESP32-S3.

NO VALIDADO:
- Evidencias automáticas aún pendientes de generación y commit.
- Build completo con stdout/cero warnings pendiente de evidencia.
```
