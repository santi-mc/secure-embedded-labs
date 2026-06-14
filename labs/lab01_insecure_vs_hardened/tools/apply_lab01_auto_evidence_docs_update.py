#!/usr/bin/env python3
"""Apply LAB 01 documentation updates for automated evidence capture.

This maintenance helper rewrites the LAB 01 documentation files affected by the
automated evidence workflow. It is intentionally deterministic so it can be run
from a repository state whose Markdown formatting differs from the patch base.
"""

from __future__ import annotations

import re
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_ROOT.parents[1]
TOOLS = LAB_ROOT / "tools"
DOCS = LAB_ROOT / "docs"
EVIDENCE = LAB_ROOT / "evidence"


def write(path: Path, text: str) -> None:
    """Write UTF-8 Markdown with LF endings."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8", newline="\n")


def update_static_gate_requirements() -> None:
    """Require the new automation scripts from LAB 01 static gates."""

    path = TOOLS / "run_static_gates.py"
    text = path.read_text(encoding="utf-8", errors="replace")
    required = [
        "../tools/capture_console_evidence.py",
        "../tools/capture_console_evidence.ps1",
        "../tools/capture_static_gates.py",
        "../tools/capture_secret_scan.py",
        "../tools/apply_lab01_auto_evidence_docs_update.py",
        "../evidence/README.md",
    ]
    match = re.search(r"REQUIRED_FILES\s*=\s*\[(.*?)\]", text, flags=re.DOTALL)
    if not match:
        raise RuntimeError("Unable to find REQUIRED_FILES in run_static_gates.py")

    block = match.group(1)
    for item in required:
        if item not in block:
            block += f'\n    "{item}",'
    text = text[: match.start(1)] + block + text[match.end(1) :]
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    """Rewrite LAB 01 docs affected by evidence automation."""

    write(
        LAB_ROOT / "README.md",
        r"""
# LAB 01 — Firmware inseguro vs firmware endurecido

**Versión:** 0.1.0

## Índice

- [Objetivo](#objetivo)
- [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
- [Prerrequisitos](#prerrequisitos)
- [Alcance](#alcance)
- [Fuera de alcance](#fuera-de-alcance)
- [Hardware requerido](#hardware-requerido)
- [Software requerido](#software-requerido)
- [Arquitectura prevista](#arquitectura-prevista)
- [Modelo temporal](#modelo-temporal)
- [Threat model](#threat-model)
- [Requisitos](#requisitos)
- [Cómo compilar](#cómo-compilar)
- [Cómo flashear](#cómo-flashear)
- [Cómo probar](#cómo-probar)
- [Captura automática de evidencias](#captura-automática-de-evidencias)
- [Evidencias esperadas](#evidencias-esperadas)
- [Errores comunes](#errores-comunes)
- [Ejercicios](#ejercicios)
- [Preguntas de repaso](#preguntas-de-repaso)
- [Fuentes](#fuentes)
- [Estado](#estado)

## Objetivo

Demostrar, de forma controlada y reproducible, cómo un firmware embebido puede exponer secretos y aceptar configuración inválida por una consola local, y cómo mitigar esos fallos mediante un perfil endurecido.

## Objetivos de aprendizaje

- Entender que una consola local también es superficie de ataque.
- Observar cómo `get_config` y los logs pueden filtrar secretos.
- Comparar parsing débil frente a parsing estricto.
- Aplicar redacción de secretos en logs.
- Diferenciar vulnerabilidad intencionada de precariedad accidental.
- Practicar evidencias `INSECURE` vs `HARDENED`.

## Prerrequisitos

- ESP-IDF instalado.
- Python 3 con `pyserial` para captura automática.
- Conocimientos básicos de C++ embebido.
- Lectura del estándar `standard/estandar_diseno_embebido_audit_grade.md`.
- Hardware ESP32-S3 con USB Serial/JTAG operativo.

## Alcance

Este laboratorio cubre seguridad local de consola, logs, secretos ficticios y validación de configuración en RAM.

## Fuera de alcance

```text
- MQTT/TLS
- OTA
- Secure Boot activo
- Flash Encryption activa
- NVS segura
- Ataques remotos
- Producción
```

## Hardware requerido

- ESP32-S3 DevKit o equivalente.
- Cable USB de datos conectado al puerto USB nativo.

## Software requerido

- ESP-IDF compatible con ESP32-S3.
- Python 3.
- `pyserial` para `tools/capture_console_evidence.py`.
- Git.

## Arquitectura prevista

El firmware está en `firmware/` y usa arquitectura por componentes:

```text
main → app_core → command_console/app_config/sensor_sim/security_status/secure_log/board_hal
```

La documentación detallada está en `docs/architecture.md`.

## Modelo temporal

Modelo event-driven cooperativo por consola bloqueante. No hay tareas periódicas propias ni ISR de aplicación.

Ver `docs/temporal_model.md` y `docs/concurrency_model.md`.

## Threat model

Amenaza principal: usuario local con acceso a consola/monitor serie capaz de leer logs y ejecutar comandos.

Ver `docs/threat_model.md`.

## Requisitos

Los requisitos están en:

```text
docs/requirements.md
docs/security_requirements.md
```

## Cómo compilar

Desde la raíz del laboratorio:

```powershell
python tools/run_static_gates.py
cd firmware
idf.py set-target esp32s3
idf.py build
```

Para seleccionar perfil:

```powershell
idf.py menuconfig
```

Ruta de configuración:

```text
Secure IoT LAB 01 → Active security profile
```

## Cómo flashear

Desde `firmware/`:

```powershell
idf.py -p COMx flash monitor
```

Sustituye `COMx` por el puerto USB Serial/JTAG detectado.

## Cómo probar

Dentro del monitor:

```text
help
get_config
set_period 0
set_period 10abc
set_mqtt_password LAB01_TEST_PASSWORD
get_config
factory_reset
security_status
```

Secuencia completa en `test/manual_lab01_commands.txt`.

## Captura automática de evidencias

Instala `pyserial` si no está disponible:

```powershell
python -m pip install pyserial
```

Con el firmware `INSECURE` ya compilado y flasheado:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py `
  --port COMx `
  --profile insecure `
  --output labs\lab01_insecure_vs_hardened\evidence\lab01_insecure_console.log
```

Con el firmware `HARDENED` ya compilado y flasheado:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_console_evidence.py `
  --port COMx `
  --profile hardened `
  --output labs\lab01_insecure_vs_hardened\evidence\lab01_hardened_console.log
```

Captura de gates estáticos:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_static_gates.py
```

Captura del scanner de secretos:

```powershell
python labs\lab01_insecure_vs_hardened\tools\capture_secret_scan.py
```

## Evidencias esperadas

Evidencias automatizadas versionables:

```text
evidence/lab01_insecure_console.log
evidence/lab01_hardened_console.log
evidence/lab01_static_gates.txt
evidence/lab01_secret_scan.txt
```

Evidencia aún pendiente para cierre audit-grade completo:

```text
evidence/lab01_build_esp32s3.txt
```

Validación manual equivalente de logs:

```powershell
python labs\lab01_insecure_vs_hardened\tools\check_no_secrets_in_logs.py labs\lab01_insecure_vs_hardened\evidence\lab01_insecure_console.log --profile insecure
python labs\lab01_insecure_vs_hardened\tools\check_no_secrets_in_logs.py labs\lab01_insecure_vs_hardened\evidence\lab01_hardened_console.log --profile hardened
```

## Errores comunes

- Usar el puerto UART externo en vez del USB Serial/JTAG nativo.
- Probar solo un perfil y considerar cerrado el laboratorio.
- Usar una contraseña real en `set_mqtt_password`.
- Guardar metadatos de captura con comandos sensibles en claro.
- No validar que el perfil observado coincide con el perfil solicitado.
- Confundir `INSECURE` didáctico con firmware válido para producción.
- Ignorar avisos de checksum mismatch entre imagen compilada y flasheada.
- Usar un HUB USB inestable durante la validación.

## Ejercicios

1. Captura la fuga de `mqtt_password` en perfil `INSECURE`.
2. Demuestra que `set_period 25s` queda aceptado en `INSECURE` por parsing débil.
3. Demuestra que `set_period 25s` queda rechazado en `HARDENED`.
4. Demuestra que `set_period 0` queda rechazado en `HARDENED`.
5. Demuestra que `set_mqtt_password` no aparece en bruto en logs `HARDENED`.
6. Regenera las evidencias con `capture_console_evidence.py` y valida que ambas tienen `capture_validation result=PASS`.

## Preguntas de repaso

1. ¿Por qué `get_config` puede ser una fuga de información?
2. ¿Por qué loguear comandos brutos es peligroso?
3. ¿Qué diferencia hay entre validar sintaxis y validar rango?
4. ¿Por qué `factory_reset` debe tener política de autorización?
5. ¿Por qué una evidencia debe validar el perfil real observado y no solo el nombre del fichero?

## Fuentes

Ver `docs/references.md` y la bibliografía global del repositorio.

## Estado

```text
CUMPLE:
- README con índice obligatorio.
- Firmware ESP-IDF para ESP32-S3 añadido.
- Documentación audit-grade del laboratorio añadida.
- Gates estáticos del laboratorio añadidos.
- Consola USB Serial/JTAG validada en hardware.
- Perfil INSECURE validado en hardware como demostración vulnerable.
- Perfil HARDENED validado en hardware como mitigación.
- Logs HARDENED redactan secretos.
- factory_reset queda bloqueado en HARDENED.
- Captura automática de evidencias añadida.

NO CUMPLE:
- No es firmware de producción.
- No implementa red, TLS, OTA, Secure Boot ni Flash Encryption activa.

NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.

PENDIENTE:
- Regenerar evidencias con scripts automáticos.
- Capturar `idf.py build` completo en `evidence/lab01_build_esp32s3.txt`.
- Revisar CI tras push.
```
""",
    )

    write(
        EVIDENCE / "README.md",
        r"""
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
""",
    )

    write(
        DOCS / "audit_evidence.md",
        r"""
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
""",
    )

    write(
        DOCS / "test_plan.md",
        r"""
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
""",
    )

    write(
        DOCS / "requirements.md",
        r"""
# LAB 01 — Requisitos y trazabilidad

## Índice

- [Formato](#formato)
- [Requisitos](#requisitos)
- [Automatización de evidencia](#automatización-de-evidencia)
- [Estado global](#estado-global)

## Formato

Cada requisito sigue la cadena:

```text
requisito → diseño → implementación → test → evidencia → estado
```

## Requisitos

| ID | Tipo | Descripción | Diseño / implementación | Test | Evidencia | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| LAB01-FW-001 | Funcional | El firmware debe arrancar e imprimir evento de boot parseable. | `main`, `app_core`, `secure_log` | Boot en monitor | `lab01_insecure_console.log`, `lab01_hardened_console.log` | CUMPLE |
| LAB01-CON-001 | Funcional | La consola debe aceptar comandos por USB Serial/JTAG. | `board_hal`, `command_console` | `help` | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-CON-002 | Calidad | La consola no debe procesar cada carácter como comando independiente. | Buffer de línea en HAL | `help` como línea completa | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-CON-003 | Calidad | La consola no debe generar spam cuando no hay datos en stdin. | Estado `NoData` + backoff | Monitor tras boot | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-VUL-001 | Didáctico | INSECURE debe demostrar parsing débil. | Parser permisivo | `set_period 25s` | `lab01_insecure_console.log` | CUMPLE |
| LAB01-VUL-002 | Didáctico | INSECURE debe demostrar fuga de secreto ficticio. | Logs/config inseguros | `set_mqtt_password ...`, `get_config` | `lab01_insecure_console.log` | CUMPLE |
| LAB01-SEC-001 | Seguridad | HARDENED debe rechazar enteros mal formados. | Parser estricto | `set_period 25s` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-002 | Seguridad | HARDENED debe rechazar periodos fuera de rango. | Validación de rango | `set_period 0` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-003 | Seguridad | HARDENED no debe exponer secretos al actualizar password. | Redacción de argumentos | `set_mqtt_password ...` | `lab01_secret_scan.txt` | CUMPLE si scanner PASS |
| LAB01-SEC-004 | Seguridad | HARDENED no debe exponer secretos en `get_config`. | Redacción de configuración | `get_config` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-005 | Seguridad | HARDENED debe bloquear `factory_reset`. | Política de autorización | `factory_reset` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-QA-001 | Calidad | Gates estáticos del repo y del lab deben pasar. | Scripts QA | Ejecución local | `lab01_static_gates.txt` | CUMPLE si gates PASS |
| LAB01-QA-002 | Calidad | Build ESP-IDF debe cerrarse con evidencia completa. | ESP-IDF build | `idf.py build` | `lab01_build_esp32s3.txt` | PENDIENTE |
| LAB01-QA-003 | Seguridad | Scanner de secretos debe cerrarse con evidencia completa. | `check_no_secrets_in_logs.py` | Scanner sobre logs | `lab01_secret_scan.txt` | CUMPLE si scanner PASS |

## Automatización de evidencia

| Script | Requisito cubierto |
| --- | --- |
| `tools/capture_console_evidence.py` | LAB01-FW-001, LAB01-CON-001, LAB01-VUL-001, LAB01-VUL-002, LAB01-SEC-001..005 |
| `tools/capture_static_gates.py` | LAB01-QA-001 |
| `tools/capture_secret_scan.py` | LAB01-QA-003 |

## Estado global

```text
CUMPLE:
- Trazabilidad funcional principal cerrada con evidencias de consola.
- Comportamientos INSECURE y HARDENED diferenciados.
- Fixes de consola validados.
- Automatización de evidencias añadida.

NO VALIDADO:
- Build completo con cero warnings hasta versionar stdout.

PENDIENTE:
- Regenerar evidencias automáticas.
- Completar evidencia de build formal.
```
""",
    )

    write(
        LAB_ROOT / "CHANGELOG.md",
        r"""
# LAB 01 — Changelog

## Índice

- [Unreleased](#unreleased)
- [0.1.0](#010)

## Unreleased

- Añadida captura automática de evidencias de consola para `INSECURE` y `HARDENED`.
- Añadida validación automática de perfil observado en logs capturados.
- Añadida captura automática de gates estáticos.
- Añadida captura automática del scanner de secretos.
- Actualizada documentación de evidencias, test plan y trazabilidad.
- Corregido el buffer de línea de la consola para no tratar cada carácter USB Serial/JTAG como comando independiente.
- Corregido spam de `console_warning` cuando `stdin` no entrega una línea disponible todavía.

## 0.1.0

- Añadido firmware ESP-IDF para ESP32-S3.
- Añadidos perfiles `INSECURE` y `HARDENED`.
- Añadida consola USB Serial/JTAG por stdio.
- Añadidas vulnerabilidades intencionadas y mitigaciones.
- Añadidos documentos audit-grade del laboratorio.
- Añadidos gates estáticos y scanner de logs.
""",
    )

    write(
        LAB_ROOT / "COMMIT_MESSAGE.txt",
        r"""
test(lab01): automatizar captura de evidencias de consola

Añade automatización de evidencias para el LAB 01, alineada con el flujo usado en el LAB 02.

Cambios principales:
- añade capture_console_evidence.py para capturar logs INSECURE/HARDENED por puerto serie
- añade wrapper PowerShell capture_console_evidence.ps1
- añade capture_static_gates.py para guardar salida raw de gates estáticos
- añade capture_secret_scan.py para guardar salida raw del scanner de secretos
- añade validación de perfil observado en logs capturados
- actualiza README, evidence/README, audit_evidence, test_plan y requirements
- actualiza gates estáticos para exigir los scripts nuevos

Validación requerida:
- python labs/lab01_insecure_vs_hardened/tools/apply_lab01_auto_evidence_docs_update.py
- python tools/repo_quality_gates/run_static_repo_gates.py
- python labs/lab01_insecure_vs_hardened/tools/run_static_gates.py
- capturar logs INSECURE/HARDENED en ESP32-S3
- python labs/lab01_insecure_vs_hardened/tools/capture_secret_scan.py
- python labs/lab01_insecure_vs_hardened/tools/capture_static_gates.py

Estado:
- CUMPLE como automatización de evidencias si los scripts generan capture_validation result=PASS.
- NO VALIDADO como cierre audit-grade completo hasta adjuntar stdout completo de idf.py build.
""",
    )

    update_static_gate_requirements()
    print("PASS: LAB 01 documentation and gate requirements updated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
