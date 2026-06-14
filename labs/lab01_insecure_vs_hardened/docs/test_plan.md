# LAB 01 — Plan de pruebas

## Índice

- [Objetivo](#objetivo)
- [Pruebas funcionales](#pruebas-funcionales)
- [Pruebas de seguridad](#pruebas-de-seguridad)
- [Pruebas de regresión](#pruebas-de-regresión)
- [Automatización](#automatización)
- [Gates](#gates)
- [Criterio de cierre](#criterio-de-cierre)

## Objetivo

Definir las pruebas mínimas para demostrar el contraste entre el perfil `INSECURE` y el perfil `HARDENED` del LAB 01.

## Pruebas funcionales

| ID | Perfil | Comando | Resultado esperado | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- |
| TP-F-001 | INSECURE | `help` | Respuesta de ayuda | `lab01_insecure_console.log` | CUMPLE |
| TP-F-002 | HARDENED | `help` | Respuesta de ayuda | `lab01_hardened_console.log` | CUMPLE |
| TP-F-003 | HARDENED | `set_period 60` | Actualización aceptada | `lab01_hardened_console.log` | CUMPLE |

## Pruebas de seguridad

| ID | Perfil | Comando | Resultado esperado | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- |
| TP-S-001 | INSECURE | `set_period 25s` | Aceptado como vulnerabilidad intencionada | `lab01_insecure_console.log` | CUMPLE |
| TP-S-002 | INSECURE | `set_mqtt_password ...` | Secreto ficticio visible como fuga didáctica | `lab01_insecure_console.log` | CUMPLE |
| TP-S-003 | HARDENED | `set_period 25s` | Rechazado por sintaxis | `lab01_hardened_console.log` | CUMPLE |
| TP-S-004 | HARDENED | `set_period 0` | Rechazado por rango | `lab01_hardened_console.log` | CUMPLE |
| TP-S-005 | HARDENED | `set_mqtt_password ...` | Secreto redactado | `lab01_secret_scan.txt` | CUMPLE si scanner PASS |
| TP-S-006 | HARDENED | `get_config` | `mqtt_password` redactado | `lab01_hardened_console.log` | CUMPLE |
| TP-S-007 | HARDENED | `factory_reset` | Rechazado por política | `lab01_hardened_console.log` | CUMPLE |

## Pruebas de regresión

| ID | Incidencia | Resultado esperado | Estado |
| --- | --- | --- | --- |
| TP-R-001 | Spam `stdin_eof` | El monitor no se satura sin datos | CUMPLE |
| TP-R-002 | Lectura carácter a carácter | `help` se procesa como una única línea | CUMPLE |
| TP-R-003 | Checksum mismatch | No validar perfil si la imagen flasheada no coincide | Documentado |
| TP-R-004 | HUB USB inestable | Clasificar como incidencia externa, no firmware | Documentado |

## Automatización

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py --port COMx --profile insecure --output labs\lab01_insecure_vs_hardened\evidence\lab01_insecure_console.log
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py --port COMx --profile hardened --output labs\lab01_insecure_vs_hardened\evidence\lab01_hardened_console.log
python labs\lab01_insecure_vs_hardened\tools\capture_secret_scan.py
```

## Gates

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_static_gates.py
python tools\repo_quality_gates\run_static_repo_gates.py
python labs\lab01_insecure_vs_hardened\tools\run_static_gates.py
```

## Criterio de cierre

```text
CUMPLE funcionalmente si:
- INSECURE reproduce vulnerabilidad didáctica.
- HARDENED mitiga las vulnerabilidades del alcance.
- No hay spam de consola.
- Los comandos llegan como líneas completas.
- Los secretos quedan redactados en HARDENED.
- factory_reset queda bloqueado en HARDENED.
- Las evidencias automáticas incluyen capture_validation result=PASS.

NO VALIDADO audit-grade completo hasta:
- Adjuntar stdout completo de build ESP-IDF.
- Registrar versión ESP-IDF/toolchain.
```
