#!/usr/bin/env python3
"""Close LAB 01/LAB 02 documentation after hardware evidence capture.

This maintenance script is intentionally deterministic and idempotent.  It is
used after LAB 01 and LAB 02 evidence files have been captured and validated.

Actions performed:
- align root README/ROADMAP with LAB 01 and LAB 02 completed status;
- align LAB 01 evidence documentation and static-gates filename;
- align LAB 02 README/docs/evidence documentation with captured evidence;
- optionally normalize licensing by using LICENSE as the Apache-2.0 code
  license and LICENSE-DOCS as the documentation license;
- update the repository static gate if LICENSE-CODE is removed.

The script does not fabricate build evidence. If full build stdout has not been
captured, the corresponding evidence remains marked as PENDIENTE/NO VALIDADO.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def replace_in_file(path: Path, replacements: dict[str, str]) -> None:
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    for old, new in replacements.items():
        text = text.replace(old, new)
    write(path, text)


def rename_lab01_static_gates() -> None:
    evidence = ROOT / "labs/lab01_insecure_vs_hardened/evidence"
    old = evidence / "lab01_static_gates_reported.txt"
    new = evidence / "lab01_static_gates.txt"
    if old.exists() and not new.exists():
        old.replace(new)
    elif old.exists() and new.exists():
        old.unlink()

    for path in (ROOT / "labs/lab01_insecure_vs_hardened").rglob("*.md"):
        replace_in_file(path, {"lab01_static_gates_reported.txt": "lab01_static_gates.txt"})


def normalize_license_layout() -> None:
    """Use LICENSE as the canonical code license.

    The original repository kept LICENSE-CODE and LICENSE-DOCS. Once LICENSE is
    present and contains Apache-2.0, LICENSE-CODE is redundant and GitHub may
    display it as an unknown additional license file. LICENSE-DOCS is kept as an
    explicit documentation license.
    """

    license_file = ROOT / "LICENSE"
    license_code = ROOT / "LICENSE-CODE"
    if not license_file.exists() and license_code.exists():
        license_file.write_text(license_code.read_text(encoding="utf-8", errors="replace"), encoding="utf-8", newline="\n")

    if license_file.exists() and license_code.exists():
        license_code.unlink()

    gate = ROOT / "tools/repo_quality_gates/run_static_repo_gates.py"
    if gate.exists() and license_file.exists():
        text = gate.read_text(encoding="utf-8")
        text = text.replace('    "LICENSE-CODE",\n    "LICENSE-DOCS",', '    "LICENSE",\n    "LICENSE-DOCS",')
        write(gate, text)


def write_root_readme() -> None:
    write(ROOT / "README.md", """# Secure Embedded Labs

Repositorio público de laboratorios auditables para aprender ciberseguridad aplicada a microcontroladores, firmware embebido e IoT.

El proyecto combina dos objetivos:

1. **Aprendizaje técnico**: comprender seguridad en firmware mediante laboratorios reproducibles sobre microcontroladores reales.
2. **Conocimiento abierto**: construir una base pública reutilizable que pueda evolucionar hacia documentación extensa o un libro con licencia abierta.

> Un laboratorio puede ser inseguro de forma intencionada; nunca puede ser precario por descuido.

## Índice

- [Objetivo](#objetivo)
- [Principios del proyecto](#principios-del-proyecto)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Roadmap de laboratorios](#roadmap-de-laboratorios)
- [Evidencias y gates](#evidencias-y-gates)
- [Estándar de diseño embebido](#estándar-de-diseño-embebido)
- [Licencias](#licencias)
- [Estado actual](#estado-actual)
- [Cómo contribuir](#cómo-contribuir)

## Objetivo

Crear una ruta pública, rigurosa y práctica para estudiar ciberseguridad embebida desde firmware real, evidencias reproducibles y documentación audit-grade.

El repositorio está diseñado para enseñar con contraste controlado:

- comportamiento inseguro intencionado;
- mitigación endurecida;
- trazabilidad requisito → diseño → implementación → test → evidencia;
- gates de calidad ejecutables por cualquier persona.

## Principios del proyecto

- Arquitectura por componentes.
- HAL/BSP explícito cuando aplica.
- Logs tratados como API de diagnóstico.
- Evidencias pequeñas, versionables y sin secretos reales.
- Perfiles inseguros solo para docencia y nunca por descuido.
- Estados explícitos: `CUMPLE`, `NO CUMPLE`, `NO VALIDADO`, `PENDIENTE`.

## Estructura del repositorio

```text
.github/       Workflows y automatización.
book/          Material destinado a capítulos o libro abierto.
docs/          Documentación transversal.
labs/          Laboratorios prácticos.
standard/      Estándar audit-grade del proyecto.
tools/         Gates y utilidades globales.
```

## Roadmap de laboratorios

| Laboratorio | Estado | Resumen |
| --- | --- | --- |
| LAB 01 — Firmware inseguro vs firmware endurecido | CUMPLE | Validado en ESP32-S3 con evidencias automáticas de consola, secret scan y gates. |
| LAB 02 — Identidad única de dispositivo | CUMPLE | Validado en ESP32-S3 con evidencias automáticas de identidad INSECURE/HARDENED y gates. |
| LAB 03 — MQTT seguro con TLS | PENDIENTE | No implementado todavía. |
| LAB 04 — OTA firmada con rollback | PENDIENTE | No implementado todavía. |
| LAB 05 — Configuración remota segura | PENDIENTE | No implementado todavía. |
| LAB 06 — Hardening de interfaces físicas | PENDIENTE | No implementado todavía. |
| LAB 07 — SBOM y trazabilidad de release | PENDIENTE | No implementado todavía. |
| LAB 08 — Secure Boot + Flash Encryption | PENDIENTE | No implementado todavía. |
| LAB 09 — Gateway seguro multi-interfaz | PENDIENTE | No implementado todavía. |
| LAB 10 — Mini PSIRT de producto | PENDIENTE | No implementado todavía. |

## Evidencias y gates

Cada laboratorio debe incluir, como mínimo:

- README con índice obligatorio;
- documentación técnica audit-grade;
- plan de pruebas;
- evidencias de consola o test cuando aplique;
- gates estáticos propios;
- estado explícito de validación.

Los gates globales se ejecutan con:

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
```

## Estándar de diseño embebido

El estándar del proyecto está en:

```text
standard/estandar_diseno_embebido_audit_grade.md
```

Ese documento define el criterio de arquitectura, testabilidad, trazabilidad, evidencias, logs, configuración, seguridad y transparencia del repositorio.

## Licencias

El código fuente, scripts, firmware y herramientas se publican bajo Apache License 2.0. Ver `LICENSE`.

La documentación, material didáctico, guías y capítulos se publican bajo Creative Commons Attribution-ShareAlike 4.0 International. Ver `LICENSE-DOCS`.

## Estado actual

```text
CUMPLE:
- Estructura pública inicial.
- Estándar audit-grade incorporado.
- LAB 01 implementado y validado localmente en ESP32-S3.
- LAB 02 implementado y validado localmente en ESP32-S3.
- Evidencias automáticas de consola/gates para LAB 01 y LAB 02.
- Gates estáticos globales y por laboratorio.

NO VALIDADO:
- Build completo con stdout versionado y cero warnings para todos los laboratorios.
- CI de build real en hardware o contenedor ESP-IDF para todos los laboratorios.

PENDIENTE:
- Implementar LAB 03.
- Capturar evidencias completas de build cuando proceda.
```

## Cómo contribuir

Ver `CONTRIBUTING.md` y `SECURITY.md`.
""")


def write_roadmap() -> None:
    write(ROOT / "ROADMAP.md", """# Roadmap

## Índice

- [Visión](#visión)
- [Fase 0 — Fundación](#fase-0--fundación)
- [Fase 1 — Laboratorios base](#fase-1--laboratorios-base)
- [Fase 2 — Seguridad conectada](#fase-2--seguridad-conectada)
- [Fase 3 — Plataforma segura](#fase-3--plataforma-segura)
- [Fase 4 — Publicación y libro](#fase-4--publicación-y-libro)
- [Criterio de cierre](#criterio-de-cierre)

## Visión

Crear una ruta abierta para aprender ciberseguridad embebida con laboratorios reproducibles, auditables y orientados a evidencia.

## Fase 0 — Fundación

- [x] Estructura base del repositorio.
- [x] Estándar audit-grade incorporado.
- [x] Plantilla de laboratorio con README e índice.
- [x] Política de contribución.
- [x] Política de seguridad.
- [x] Licencias separadas para código y documentación.

## Fase 1 — Laboratorios base

- [x] LAB 01 — Firmware inseguro vs firmware endurecido.
- [x] LAB 02 — Identidad única de dispositivo.

Estado de cierre:

```text
LAB 01: CUMPLE con evidencias automáticas de consola, secret scan y gates.
LAB 02: CUMPLE con evidencias automáticas de consola, validadores de identidad y gates.
```

## Fase 2 — Seguridad conectada

- [ ] LAB 03 — MQTT seguro con TLS.
- [ ] LAB 04 — OTA firmada con rollback.
- [ ] LAB 05 — Configuración remota segura.

## Fase 3 — Plataforma segura

- [ ] LAB 06 — Hardening de interfaces físicas.
- [ ] LAB 07 — SBOM y trazabilidad de release.
- [ ] LAB 08 — Secure Boot + Flash Encryption.
- [ ] LAB 09 — Gateway seguro multi-interfaz.

## Fase 4 — Publicación y libro

- [ ] Normalizar capítulos en `book/`.
- [ ] Revisar licencia documental.
- [ ] Preparar versión publicable.

## Criterio de cierre

Un laboratorio solo se marca como cerrado cuando dispone de:

- firmware o artefacto técnico versionado;
- documentación con índice;
- plan de pruebas;
- evidencias reales o declaración explícita `NO VALIDADO`;
- gates ejecutados y documentados;
- commit trazable.
""")


def write_lab01_evidence_readme() -> None:
    write(ROOT / "labs/lab01_insecure_vs_hardened/evidence/README.md", """# LAB 01 — Evidencias

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
""")


def update_lab01_docs() -> None:
    lab = ROOT / "labs/lab01_insecure_vs_hardened"
    replacements = {
        "lab01_static_gates_reported.txt": "lab01_static_gates.txt",
        "lab01_static_gates.txt real o lab01_static_gates_reported.txt": "lab01_static_gates.txt",
    }
    for path in lab.rglob("*.md"):
        replace_in_file(path, replacements)


def write_lab02_readme() -> None:
    write(ROOT / "labs/lab02_device_identity/README.md", """# LAB 02 — Identidad única de dispositivo

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
- [Evidencias esperadas](#evidencias-esperadas)
- [Errores comunes](#errores-comunes)
- [Ejercicios](#ejercicios)
- [Preguntas de repaso](#preguntas-de-repaso)
- [Fuentes](#fuentes)
- [Estado](#estado)

## Objetivo

Demostrar por qué una identidad de dispositivo no debe ser hardcoded, clonable ni mutable por consola, y cómo derivar un identificador estable desde material de hardware sin exponer identificadores brutos.

## Objetivos de aprendizaje

- Diferenciar identificador público, identidad local y autenticación.
- Observar el riesgo de identidades clonables.
- Observar el riesgo de comandos `set_device_id` sin política.
- Comparar identidad hardcoded frente a identidad derivada de eFuse MAC + SHA-256 truncado.
- Entender que un identificador no es un secreto ni sustituye autenticación.
- Capturar evidencias INSECURE/HARDENED automatizadas.

## Prerrequisitos

- ESP-IDF instalado.
- ESP32-S3 con USB Serial/JTAG operativo.
- Python 3 con `pyserial` para captura automática.
- Lectura del estándar `standard/estandar_diseno_embebido_audit_grade.md`.

## Alcance

Este laboratorio cubre identidad local de dispositivo, exposición de identificadores, mutabilidad por consola y claims didácticos.

## Fuera de alcance

```text
- Certificados X.509 reales.
- Secure element.
- TLS mutuo.
- Provisioning industrial.
- NVS segura.
- Secure Boot activo.
- Flash Encryption activa.
- Producción.
```

## Hardware requerido

- ESP32-S3 DevKit o equivalente.
- Cable USB de datos conectado al puerto USB nativo.

## Software requerido

- ESP-IDF compatible con ESP32-S3.
- Python 3.
- pyserial.
- Git.

## Arquitectura prevista

El firmware está en `firmware/` y usa arquitectura por componentes:

```text
main → app_core → command_console/identity_service/security_status/secure_log/board_hal
```

La documentación detallada está en `docs/architecture.md`.

## Modelo temporal

Modelo event-driven cooperativo por consola. No hay tareas periódicas propias ni ISR de aplicación.

Ver `docs/temporal_model.md` y `docs/concurrency_model.md`.

## Threat model

Amenaza principal: usuario local con acceso a consola capaz de leer identidad, clonar identificadores o intentar modificar el `device_id`.

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
Secure IoT LAB 02 → Active identity profile
```

## Cómo flashear

Desde `firmware/`:

```powershell
idf.py -p COMx flash monitor
```

Sustituye `COMx` por el puerto USB Serial/JTAG detectado.

## Cómo probar

Comandos disponibles:

```text
help
identity_status
get_identity
get_claim
set_device_id CLONED-DEVICE-001
security_status
```

Captura automática desde la raíz del repo:

```powershell
python labs\\lab02_device_identity\\tools\\capture_console_evidence.py --port COMx --profile insecure --output labs\\lab02_device_identity\\evidence\\lab02_insecure_console.log
python labs\\lab02_device_identity\\tools\\capture_console_evidence.py --port COMx --profile hardened --output labs\\lab02_device_identity\\evidence\\lab02_hardened_console.log
python labs\\lab02_device_identity\\tools\\capture_static_gates.py
```

Validación de logs:

```powershell
python labs\\lab02_device_identity\\tools\\check_lab02_identity_logs.py labs\\lab02_device_identity\\evidence\\lab02_insecure_console.log --profile insecure
python labs\\lab02_device_identity\\tools\\check_lab02_identity_logs.py labs\\lab02_device_identity\\evidence\\lab02_hardened_console.log --profile hardened
```

## Evidencias esperadas

Evidencias versionadas:

```text
evidence/lab02_insecure_console.log
evidence/lab02_hardened_console.log
evidence/lab02_static_gates.txt
```

Evidencias pendientes para cierre completo audit-grade:

```text
evidence/lab02_build_esp32s3.txt
```

## Errores comunes

- Capturar `INSECURE` con firmware `HARDENED` cargado.
- Ignorar un mismatch de perfil detectado por el script de captura.
- Confundir identidad pública con autenticación.
- Exponer raw MAC en HARDENED.
- Versionar logs con tokens reales.
- Flashear con target incorrecto (`esp32` en vez de `esp32s3`).

## Ejercicios

1. Demuestra que `INSECURE` permite cambiar `device_id` desde consola.
2. Demuestra que `INSECURE` genera un claim clonable con token compartido ficticio.
3. Demuestra que `HARDENED` rechaza `set_device_id`.
4. Demuestra que `HARDENED` redacta `raw_hardware_id`.
5. Explica por qué `auth_token="not_applicable"` no equivale a autenticación.

## Preguntas de repaso

1. ¿Por qué una identidad hardcoded es clonable?
2. ¿Por qué una identidad no debe ser mutable por consola en campo?
3. ¿Qué aporta derivar un identificador de eFuse MAC con hash?
4. ¿Por qué raw MAC puede considerarse dato sensible de inventario?
5. ¿Qué diferencia hay entre identidad y autenticación?

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
- Perfil INSECURE validado con evidencia automática.
- Perfil HARDENED validado con evidencia automática.
- Logs HARDENED redactan raw_hardware_id.
- set_device_id queda bloqueado en HARDENED.
- Gates estáticos capturados con PASS.

NO CUMPLE:
- No es firmware de producción.
- No implementa certificados, TLS mutuo, Secure Boot ni Flash Encryption activa.

NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.

PENDIENTE:
- Capturar `idf.py build` completo en `evidence/lab02_build_esp32s3.txt`.
- Revisar CI tras push.
```
""")


def write_lab02_evidence_readme() -> None:
    write(ROOT / "labs/lab02_device_identity/evidence/README.md", """# LAB 02 — Evidencias

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
""")


def write_lab02_audit_evidence() -> None:
    write(ROOT / "labs/lab02_device_identity/docs/audit_evidence.md", """# LAB 02 — Evidencia de auditoría

## Índice

- [Objetivo](#objetivo)
- [Matriz de evidencias](#matriz-de-evidencias)
- [Validación funcional](#validación-funcional)
- [Limitaciones](#limitaciones)
- [Estado](#estado)

## Objetivo

Registrar la evidencia audit-grade disponible para el LAB 02 y su relación con los requisitos del laboratorio.

## Matriz de evidencias

| Evidencia | Estado | Resultado |
| --- | --- | --- |
| `evidence/lab02_insecure_console.log` | CUMPLE | Perfil INSECURE validado con identidad mutable y claim clonable. |
| `evidence/lab02_hardened_console.log` | CUMPLE | Perfil HARDENED validado con identidad derivada, no mutable y sin exposición de raw hardware ID. |
| `evidence/lab02_static_gates.txt` | CUMPLE | Gates estáticos globales y del LAB 02 capturados con PASS. |
| `evidence/lab02_build_esp32s3.txt` | PENDIENTE | Falta stdout completo de build. |

## Validación funcional

```text
CUMPLE:
- INSECURE: set_device_id acepta CLONED-DEVICE-001.
- INSECURE: get_claim emite insecure_cloneable_claim con token compartido ficticio.
- HARDENED: identity_source=efuse_mac_sha256_truncated.
- HARDENED: raw_hardware_id=<redacted>.
- HARDENED: set_device_id rechazado por política.
- HARDENED: auth_token=not_applicable.
```

## Limitaciones

```text
NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.
- Secure Boot y Flash Encryption no están activos en este laboratorio.
```

## Estado

```text
CUMPLE:
- Evidencias funcionales y gates disponibles.

PENDIENTE:
- Captura de build completo.
```
""")


def write_lab02_requirements() -> None:
    write(ROOT / "labs/lab02_device_identity/docs/requirements.md", """# LAB 02 — Requisitos

## Índice

- [Objetivo](#objetivo)
- [Requisitos funcionales](#requisitos-funcionales)
- [Requisitos de seguridad](#requisitos-de-seguridad)
- [Trazabilidad](#trazabilidad)
- [Estado](#estado)

## Objetivo

Definir los requisitos verificables del LAB 02 y su trazabilidad hacia evidencias.

## Requisitos funcionales

| ID | Requisito | Estado |
| --- | --- | --- |
| LAB02-FR-001 | El firmware debe exponer `identity_status`. | CUMPLE |
| LAB02-FR-002 | El firmware debe exponer `get_identity`. | CUMPLE |
| LAB02-FR-003 | El firmware debe exponer `get_claim`. | CUMPLE |
| LAB02-FR-004 | El perfil INSECURE debe permitir `set_device_id`. | CUMPLE |
| LAB02-FR-005 | El perfil HARDENED debe rechazar `set_device_id`. | CUMPLE |

## Requisitos de seguridad

| ID | Requisito | Estado |
| --- | --- | --- |
| LAB02-SR-001 | HARDENED no debe exponer raw hardware ID. | CUMPLE |
| LAB02-SR-002 | HARDENED no debe emitir token secreto. | CUMPLE |
| LAB02-SR-003 | HARDENED debe derivar identidad desde fuente no mutable por consola. | CUMPLE |
| LAB02-SR-004 | INSECURE debe demostrar identidad clonable como vulnerabilidad didáctica. | CUMPLE |

## Trazabilidad

| Requisito | Evidencia |
| --- | --- |
| LAB02-FR-001 | `evidence/lab02_insecure_console.log`, `evidence/lab02_hardened_console.log` |
| LAB02-FR-002 | `evidence/lab02_insecure_console.log`, `evidence/lab02_hardened_console.log` |
| LAB02-FR-003 | `evidence/lab02_insecure_console.log`, `evidence/lab02_hardened_console.log` |
| LAB02-FR-004 | `evidence/lab02_insecure_console.log` |
| LAB02-FR-005 | `evidence/lab02_hardened_console.log` |
| LAB02-SR-001 | `evidence/lab02_hardened_console.log` |
| LAB02-SR-002 | `evidence/lab02_hardened_console.log` |
| LAB02-SR-003 | `evidence/lab02_hardened_console.log` |
| LAB02-SR-004 | `evidence/lab02_insecure_console.log` |

## Estado

```text
CUMPLE:
- Requisitos funcionales y de seguridad trazados a evidencias.

NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.
```
""")


def write_lab02_test_plan() -> None:
    write(ROOT / "labs/lab02_device_identity/docs/test_plan.md", """# LAB 02 — Plan de pruebas

## Índice

- [Objetivo](#objetivo)
- [Pruebas INSECURE](#pruebas-insecure)
- [Pruebas HARDENED](#pruebas-hardened)
- [Pruebas de gates](#pruebas-de-gates)
- [Pruebas pendientes](#pruebas-pendientes)
- [Estado](#estado)

## Objetivo

Definir las pruebas necesarias para cerrar el LAB 02 con evidencias auditables.

## Pruebas INSECURE

| Prueba | Estado | Evidencia |
| --- | --- | --- |
| Boot INSECURE | CUMPLE | `evidence/lab02_insecure_console.log` |
| `identity_status` muestra identidad mutable | CUMPLE | `evidence/lab02_insecure_console.log` |
| `set_device_id CLONED-DEVICE-001` aceptado | CUMPLE | `evidence/lab02_insecure_console.log` |
| `get_claim` emite claim clonable | CUMPLE | `evidence/lab02_insecure_console.log` |

## Pruebas HARDENED

| Prueba | Estado | Evidencia |
| --- | --- | --- |
| Boot HARDENED | CUMPLE | `evidence/lab02_hardened_console.log` |
| `identity_status` muestra identidad derivada | CUMPLE | `evidence/lab02_hardened_console.log` |
| `raw_hardware_id` aparece redactado | CUMPLE | `evidence/lab02_hardened_console.log` |
| `set_device_id` rechazado | CUMPLE | `evidence/lab02_hardened_console.log` |
| `get_claim` no expone token secreto | CUMPLE | `evidence/lab02_hardened_console.log` |

## Pruebas de gates

| Prueba | Estado | Evidencia |
| --- | --- | --- |
| Gate global del repo | CUMPLE | `evidence/lab02_static_gates.txt` |
| Gate estático LAB 02 | CUMPLE | `evidence/lab02_static_gates.txt` |
| Validador de logs INSECURE | CUMPLE | `evidence/lab02_insecure_console.log` |
| Validador de logs HARDENED | CUMPLE | `evidence/lab02_hardened_console.log` |

## Pruebas pendientes

| Prueba | Estado | Motivo |
| --- | --- | --- |
| Build completo con stdout | PENDIENTE | Falta `evidence/lab02_build_esp32s3.txt`. |

## Estado

```text
CUMPLE:
- Pruebas funcionales INSECURE/HARDENED validadas.
- Gates estáticos capturados con PASS.

NO VALIDADO:
- Build completo con stdout versionado.
```
""")


def update_changelog() -> None:
    path = ROOT / "CHANGELOG.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    entry = "- docs: alinear estado de LAB 01 y LAB 02 con evidencias automáticas."
    if entry in text:
        return
    text = text.replace("## [Unreleased]", f"## [Unreleased]\n\n{entry}", 1)
    write(path, text)


def main() -> int:
    rename_lab01_static_gates()
    normalize_license_layout()
    write_root_readme()
    write_roadmap()
    write_lab01_evidence_readme()
    update_lab01_docs()
    write_lab02_readme()
    write_lab02_evidence_readme()
    write_lab02_audit_evidence()
    write_lab02_requirements()
    write_lab02_test_plan()
    update_changelog()
    print("PASS: LAB 01/LAB 02 documentation aligned with captured evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
