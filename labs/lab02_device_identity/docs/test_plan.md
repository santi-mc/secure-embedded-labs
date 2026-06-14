# Plan de pruebas LAB 02

## Índice

- [Objetivo](#objetivo)
- [Pruebas INSECURE](#pruebas-insecure)
- [Pruebas HARDENED](#pruebas-hardened)
- [Captura automática](#captura-automática)
- [Gates](#gates)
- [Estado](#estado)

## Objetivo

Definir pruebas mínimas para validar el comportamiento didáctico del LAB 02.

## Pruebas INSECURE

```text
[ ] Arranca con profile=INSECURE.
[ ] get_identity muestra device_id clonable.
[ ] get_claim expone token compartido de laboratorio.
[ ] set_device_id acepta un ID arbitrario.
[ ] get_identity confirma el ID modificado.
```

## Pruebas HARDENED

```text
[ ] Arranca con profile=HARDENED.
[ ] get_identity muestra device_id derivado.
[ ] raw_hardware_id aparece como <redacted>.
[ ] get_claim no incluye token ni secreto.
[ ] set_device_id queda rechazado por política.
[ ] get_identity posterior confirma que el ID no cambia.
```

## Captura automática

Captura INSECURE:

```powershell
python labs/lab02_device_identity/tools/capture_console_evidence.py `
  --port COMx `
  --profile insecure `
  --output labs/lab02_device_identity/evidence/lab02_insecure_console.log
```

Captura HARDENED:

```powershell
python labs/lab02_device_identity/tools/capture_console_evidence.py `
  --port COMx `
  --profile hardened `
  --output labs/lab02_device_identity/evidence/lab02_hardened_console.log
```

Validación:

```powershell
python labs/lab02_device_identity/tools/check_lab02_identity_logs.py labs/lab02_device_identity/evidence/lab02_insecure_console.log --profile insecure
python labs/lab02_device_identity/tools/check_lab02_identity_logs.py labs/lab02_device_identity/evidence/lab02_hardened_console.log --profile hardened
```

## Gates

```text
[ ] python tools/repo_quality_gates/run_static_repo_gates.py
[ ] python labs/lab02_device_identity/tools/run_static_gates.py
[ ] python labs/lab02_device_identity/tools/capture_static_gates.py
[ ] idf.py build sin warnings
```

## Estado

```text
CUMPLE:
- Plan actualizado con captura automática.
- Validación manual INSECURE/HARDENED realizada por el operador.

PENDIENTE:
- Generar evidencias automáticas.
- Capturar build completo.
```
