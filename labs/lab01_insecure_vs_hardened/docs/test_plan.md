# LAB 01 — Plan de pruebas

## Índice

- [Objetivo](#objetivo)
- [Gates estáticos](#gates-estáticos)
- [Build](#build)
- [Pruebas manuales](#pruebas-manuales)
- [Validación de logs](#validación-de-logs)
- [Estado](#estado)

## Objetivo

Definir cómo cerrar el LAB 01 con evidencias.

## Gates estáticos

```powershell
python labs/lab01_insecure_vs_hardened/tools/run_static_gates.py
```

## Build

Desde `labs/lab01_insecure_vs_hardened/firmware`:

```powershell
idf.py set-target esp32s3
idf.py build
```

## Pruebas manuales

Ejecutar los comandos de `test/manual_lab01_commands.txt` en dos builds:

```text
INSECURE
HARDENED
```

## Validación de logs

```powershell
python labs/lab01_insecure_vs_hardened/tools/check_no_secrets_in_logs.py evidence/lab01_insecure_console.log --profile insecure
python labs/lab01_insecure_vs_hardened/tools/check_no_secrets_in_logs.py evidence/lab01_hardened_console.log --profile hardened
```

## Estado

```text
CUMPLE:
- Plan de pruebas definido.

NO VALIDADO:
- Pruebas reales pendientes.
```
