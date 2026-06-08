#!/usr/bin/env python3
"""Update LAB 01 documentation and evidence after hardware validation.

This maintenance script is intentionally deterministic and has no external
runtime dependencies. It rewrites the documentation files that describe the
current LAB 01 state and creates evidence records from the operator-provided
hardware validation logs.

It does not modify firmware source files.
"""

from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current.parent, *current.parents]:
        if (parent / ".git").exists() and (parent / "labs").exists():
            return parent
    raise SystemExit("ERROR: repository root not found. Run inside secure-embedded-labs.")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


ROOT_README = """# Secure Embedded Labs

Repositorio público de laboratorios auditables para aprender ciberseguridad aplicada a microcontroladores, firmware embebido e IoT.

El proyecto combina dos objetivos:

1. **Aprendizaje técnico:** comprender seguridad en firmware mediante laboratorios reproducibles sobre microcontroladores reales.
2. **Conocimiento abierto:** construir una base pública reutilizable que pueda evolucionar hacia documentación extensa o un libro con licencia abierta.

> Un laboratorio puede ser inseguro de forma intencionada; nunca puede ser precario por descuido.

## Índice

- [Objetivo](#objetivo)
- [Principios del proyecto](#principios-del-proyecto)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Roadmap de laboratorios](#roadmap-de-laboratorios)
- [Estándar de diseño embebido](#estándar-de-diseño-embebido)
- [Licencias](#licencias)
- [Estado actual](#estado-actual)
- [Cómo contribuir](#cómo-contribuir)

## Objetivo

Crear una ruta pública, rigurosa y práctica para aprender desarrollo seguro en sistemas embebidos, con foco inicial en **ESP32-S3 / ESP-IDF**.

Cada laboratorio debe permitir:

```text
clonar → leer → compilar → flashear → reproducir → auditar → aprender
```

## Principios del proyecto

Todo laboratorio debe cumplir el estándar permanente de diseño embebido audit-grade:

- arquitectura por componentes;
- FULL HAL/BSP;
- diseño orientado a interfaces y encapsulación;
- modelo temporal explícito;
- política de concurrencia, ISR y recursos compartidos;
- presupuesto de recursos;
- configuración validada;
- logs como API sin secretos;
- seguridad desde diseño;
- trazabilidad requisito → diseño → implementación → test → evidencia;
- QA gates estrictos;
- cero warnings;
- documentación audit-grade;
- transparencia `CUMPLE / NO CUMPLE / NO VALIDADO / PENDIENTE`.

El estándar completo está en:

```text
standard/estandar_diseno_embebido_audit_grade.md
```

## Estructura del repositorio

```text
secure-embedded-labs/
├── standard/
├── docs/
├── labs/
├── book/
├── tools/
└── .github/
```

## Roadmap de laboratorios

| Lab | Tema | Estado |
|---:|---|---|
| 01 | Firmware inseguro vs firmware endurecido | Validado localmente en ESP32-S3 |
| 02 | Identidad única de dispositivo | Pendiente |
| 03 | MQTT seguro con TLS | Pendiente |
| 04 | OTA firmada con rollback | Pendiente |
| 05 | Configuración remota segura | Pendiente |
| 06 | Hardening de interfaces físicas | Pendiente |
| 07 | SBOM y trazabilidad de release | Pendiente |
| 08 | Secure Boot + Flash Encryption | Pendiente |
| 09 | Gateway seguro multi-interfaz | Pendiente |
| 10 | Mini PSIRT de producto | Pendiente |

## Estándar de diseño embebido

Este repositorio no acepta laboratorios precarios. Cada entrega debe clasificarse explícitamente:

```text
CUMPLE:
- ...

NO CUMPLE:
- ...

NO VALIDADO:
- ...

PENDIENTE:
- ...
```

## Licencias

- Código fuente, scripts y firmware: **Apache-2.0**. Véase `LICENSE-CODE` y `LICENSE`.
- Documentación, texto educativo, figuras propias y futuro material de libro: **CC BY-SA 4.0**. Véase `LICENSE-DOCS`.

Los datasheets, normas, libros, artículos y documentos de terceros no se redistribuirán salvo permiso explícito. Se citarán o enlazarán según corresponda.

## Estado actual

```text
CUMPLE:
- Repositorio público estructurado.
- Estándar audit-grade incluido.
- Readme principal con índice.
- Gates estáticos de estructura incluidos.
- LAB 01 implementado con firmware ESP-IDF para ESP32-S3.
- LAB 01 validado localmente en hardware en perfiles INSECURE y HARDENED.
- Evidencias funcionales de consola añadidas para LAB 01.

NO CUMPLE:
- No contiene todavía capítulos completos de libro.
- Los laboratorios posteriores al LAB 01 aún no están implementados.

NO VALIDADO:
- Build completo con cero warnings no queda cerrado hasta versionar stdout completo de `idf.py build`.
- CI real en GitHub queda pendiente de revisar tras cada push.

PENDIENTE:
- Capturar evidencia formal de build ESP-IDF completo.
- Capturar evidencia formal del scanner de secretos.
- Implementar LAB 02.
```

## Cómo contribuir

Lee `CONTRIBUTING.md` antes de abrir un Pull Request.
"""

LAB01_README = """# LAB 01 — Firmware inseguro vs firmware endurecido

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
set_mqtt_password MiPasswordSuperSecreta123
get_config
factory_reset
security_status
```

Secuencia completa en `test/manual_lab01_commands.txt`.

## Evidencias esperadas

Evidencias versionadas:

```text
evidence/lab01_insecure_console.log
evidence/lab01_hardened_console.log
evidence/lab01_static_gates_reported.txt
```

Evidencias aún pendientes para cierre completo audit-grade:

```text
evidence/lab01_build_esp32s3.txt
evidence/lab01_secret_scan.txt
```

Validación de logs:

```powershell
python tools/check_no_secrets_in_logs.py evidence/lab01_insecure_console.log --profile insecure
python tools/check_no_secrets_in_logs.py evidence/lab01_hardened_console.log --profile hardened
```

## Errores comunes

- Usar el puerto UART externo en vez del USB Serial/JTAG nativo.
- Probar solo un perfil y considerar cerrado el laboratorio.
- Usar una contraseña real en `set_mqtt_password`.
- No guardar logs como evidencia.
- Confundir `INSECURE` didáctico con firmware válido para producción.
- Ignorar avisos de checksum mismatch entre imagen compilada y flasheada.
- Usar un HUB USB inestable durante la validación.

## Ejercicios

1. Captura la fuga de `mqtt_password` en perfil `INSECURE`.
2. Demuestra que `set_period 25s` queda aceptado en `INSECURE` por parsing débil.
3. Demuestra que `set_period 25s` queda rechazado en `HARDENED`.
4. Demuestra que `set_period 0` queda rechazado en `HARDENED`.
5. Demuestra que `set_mqtt_password` no aparece en bruto en logs `HARDENED`.
6. Añade un nuevo comando no sensible y comprueba que el scanner no da falsos positivos.

## Preguntas de repaso

1. ¿Por qué `get_config` puede ser una fuga de información?
2. ¿Por qué loguear comandos brutos es peligroso?
3. ¿Qué diferencia hay entre validar sintaxis y validar rango?
4. ¿Por qué `factory_reset` debe tener política de autorización?
5. ¿Qué evidencias mínimas cierran el LAB 01?

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
- Gates estáticos reportados como PASS por el operador.

NO CUMPLE:
- No es firmware de producción.
- No implementa red, TLS, OTA, Secure Boot ni Flash Encryption activa.

NO VALIDADO:
- Build completo con cero warnings pendiente de evidencia stdout versionada.
- Scanner de secretos pendiente de evidencia stdout versionada.

PENDIENTE:
- Capturar `idf.py build` completo en `evidence/lab01_build_esp32s3.txt`.
- Capturar scanner de secretos en `evidence/lab01_secret_scan.txt`.
- Revisar CI tras push.
```
"""

AUDIT_EVIDENCE = """# LAB 01 — Evidencia de auditoría

## Índice

- [Resumen](#resumen)
- [Entorno](#entorno)
- [Evidencias versionadas](#evidencias-versionadas)
- [Validación funcional](#validación-funcional)
- [Gates](#gates)
- [Limitaciones](#limitaciones)
- [Estado](#estado)

## Resumen

Este documento registra la evidencia disponible para el LAB 01: firmware inseguro vs firmware endurecido.

El laboratorio fue probado localmente sobre ESP32-S3 con consola USB Serial/JTAG. Las evidencias de consola se guardan como logs NDJSON en `evidence/`.

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
|---|---|---|
| `evidence/lab01_insecure_console.log` | Log funcional INSECURE | CUMPLE |
| `evidence/lab01_hardened_console.log` | Log funcional HARDENED | CUMPLE |
| `evidence/lab01_static_gates_reported.txt` | Gates reportados por operador | CUMPLE con limitación |
| `evidence/lab01_build_esp32s3.txt` | Build completo ESP-IDF | PENDIENTE |
| `evidence/lab01_secret_scan.txt` | Scanner de secretos | PENDIENTE |

## Validación funcional

| Caso | Perfil | Resultado esperado | Resultado observado | Estado |
|---|---|---|---|---|
| Boot INSECURE | INSECURE | Arranque con perfil INSECURE | `profile":"INSECURE"` | CUMPLE |
| Consola sin spam EOF | INSECURE/HARDENED | Sin bucle `stdin_eof` | No aparece spam tras fixes | CUMPLE |
| Buffer de línea | INSECURE/HARDENED | `help` llega como línea completa | `raw":"help"` / `cmd":"help"` | CUMPLE |
| Comando desconocido | INSECURE | `period` rechazado | `unknown_command` | CUMPLE |
| Parser débil | INSECURE | `set_period 25s` aceptado como vulnerabilidad | `value":"25"` | CUMPLE |
| Parser estricto | HARDENED | `set_period 25s` rechazado | `invalid_uint32` | CUMPLE |
| Rango estricto | HARDENED | `set_period 0` rechazado | `out_of_range` | CUMPLE |
| Config válida | HARDENED | `set_period 60` aceptado | `value":"60"` | CUMPLE |
| Redacción de secretos | HARDENED | Password no visible | `args":"<redacted>"` y `value":"<redacted>"` | CUMPLE |
| Dump seguro | HARDENED | `mqtt_password` redactado | `mqtt_password":"<redacted>"` | CUMPLE |
| Reset protegido | HARDENED | `factory_reset` bloqueado | `rejected_by_policy` | CUMPLE |

## Gates

El operador reportó que pasaron:

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
python labs/lab01_insecure_vs_hardened/tools/run_static_gates.py
```

La salida raw completa debe guardarse como evidencia cuando se cierre el laboratorio con criterio audit-grade estricto.

## Limitaciones

```text
NO VALIDADO:
- No se versiona todavía stdout completo de `idf.py build`.
- No se versiona todavía stdout completo del scanner de secretos.
- No se aporta hash de binario flasheado.
- No se aporta versión exacta de ESP-IDF/toolchain en evidencia formal.
```

## Estado

```text
CUMPLE:
- Validación funcional INSECURE/HARDENED documentada.
- Evidencias de consola versionadas.
- Estados y limitaciones declarados.

PENDIENTE:
- Capturar build completo.
- Capturar scanner de secretos.
- Registrar versión ESP-IDF/toolchain.
```
"""

REQUIREMENTS = """# LAB 01 — Requisitos y trazabilidad

## Índice

- [Formato](#formato)
- [Requisitos](#requisitos)
- [Estado global](#estado-global)

## Formato

Cada requisito sigue la cadena:

```text
requisito → diseño → implementación → test → evidencia → estado
```

## Requisitos

| ID | Tipo | Descripción | Diseño / implementación | Test | Evidencia | Estado |
|---|---|---|---|---|---|---|
| LAB01-FW-001 | Funcional | El firmware debe arrancar e imprimir evento de boot parseable. | `main`, `app_core`, `secure_log` | Boot en monitor | `evidence/lab01_insecure_console.log`, `evidence/lab01_hardened_console.log` | CUMPLE |
| LAB01-CON-001 | Funcional | La consola debe aceptar comandos por USB Serial/JTAG. | `board_hal`, `command_console` | `help` | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-CON-002 | Calidad | La consola no debe procesar cada carácter como comando independiente. | Buffer de línea en HAL | `help` como línea completa | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-CON-003 | Calidad | La consola no debe generar spam cuando no hay datos en stdin. | Estado `NoData` + backoff | Monitor tras boot | Logs INSECURE/HARDENED | CUMPLE |
| LAB01-VUL-001 | Didáctico | INSECURE debe demostrar parsing débil. | Parser permisivo | `set_period 25s` | `lab01_insecure_console.log` | CUMPLE |
| LAB01-SEC-001 | Seguridad | HARDENED debe rechazar enteros mal formados. | Parser estricto | `set_period 25s` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-002 | Seguridad | HARDENED debe rechazar periodos fuera de rango. | Validación de rango | `set_period 0` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-003 | Seguridad | HARDENED no debe exponer secretos al actualizar password. | Redacción de argumentos | `set_mqtt_password test123` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-004 | Seguridad | HARDENED no debe exponer secretos en `get_config`. | Redacción de configuración | `get_config` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-SEC-005 | Seguridad | HARDENED debe bloquear `factory_reset`. | Política de autorización | `factory_reset` | `lab01_hardened_console.log` | CUMPLE |
| LAB01-QA-001 | Calidad | Gates estáticos del repo y del lab deben pasar. | Scripts QA | Ejecución local | `lab01_static_gates_reported.txt` | CUMPLE con limitación |
| LAB01-QA-002 | Calidad | Build ESP-IDF debe cerrarse con evidencia completa. | ESP-IDF build | `idf.py build` | `lab01_build_esp32s3.txt` | PENDIENTE |
| LAB01-QA-003 | Seguridad | Scanner de secretos debe cerrarse con evidencia completa. | `check_no_secrets_in_logs.py` | Scanner sobre logs | `lab01_secret_scan.txt` | PENDIENTE |

## Estado global

```text
CUMPLE:
- Trazabilidad funcional principal cerrada con evidencias de consola.
- Comportamientos INSECURE y HARDENED diferenciados.
- Fixes de consola validados.

NO VALIDADO:
- Build completo con cero warnings hasta versionar stdout.
- Scanner de secretos hasta versionar stdout.

PENDIENTE:
- Completar evidencias QA formales.
```
"""

TEST_PLAN = """# LAB 01 — Plan de pruebas

## Índice

- [Objetivo](#objetivo)
- [Pruebas funcionales](#pruebas-funcionales)
- [Pruebas de seguridad](#pruebas-de-seguridad)
- [Pruebas de regresión](#pruebas-de-regresión)
- [Gates](#gates)
- [Criterio de cierre](#criterio-de-cierre)

## Objetivo

Definir las pruebas mínimas para demostrar el contraste entre el perfil `INSECURE` y el perfil `HARDENED` del LAB 01.

## Pruebas funcionales

| ID | Perfil | Comando | Resultado esperado | Evidencia | Estado |
|---|---|---|---|---|---|
| TP-F-001 | INSECURE | `help` | Respuesta de ayuda | `lab01_insecure_console.log` | CUMPLE |
| TP-F-002 | HARDENED | `help` | Respuesta de ayuda | `lab01_hardened_console.log` | CUMPLE |
| TP-F-003 | HARDENED | `set_period 60` | Actualización aceptada | `lab01_hardened_console.log` | CUMPLE |

## Pruebas de seguridad

| ID | Perfil | Comando | Resultado esperado | Evidencia | Estado |
|---|---|---|---|---|---|
| TP-S-001 | INSECURE | `set_period 25s` | Aceptado como vulnerabilidad intencionada | `lab01_insecure_console.log` | CUMPLE |
| TP-S-002 | HARDENED | `set_period 25s` | Rechazado por sintaxis | `lab01_hardened_console.log` | CUMPLE |
| TP-S-003 | HARDENED | `set_period 0` | Rechazado por rango | `lab01_hardened_console.log` | CUMPLE |
| TP-S-004 | HARDENED | `set_mqtt_password test123` | Secreto redactado | `lab01_hardened_console.log` | CUMPLE |
| TP-S-005 | HARDENED | `get_config` | `mqtt_password` redactado | `lab01_hardened_console.log` | CUMPLE |
| TP-S-006 | HARDENED | `factory_reset` | Rechazado por política | `lab01_hardened_console.log` | CUMPLE |

## Pruebas de regresión

| ID | Incidencia | Resultado esperado | Estado |
|---|---|---|---|
| TP-R-001 | Spam `stdin_eof` | El monitor no se satura sin datos | CUMPLE |
| TP-R-002 | Lectura carácter a carácter | `help` se procesa como una única línea | CUMPLE |
| TP-R-003 | Checksum mismatch | No validar perfil si la imagen flasheada no coincide | Documentado |
| TP-R-004 | HUB USB inestable | Clasificar como incidencia externa, no firmware | Documentado |

## Gates

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
python labs/lab01_insecure_vs_hardened/tools/run_static_gates.py
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

NO VALIDADO audit-grade completo hasta:
- Adjuntar stdout completo de build ESP-IDF.
- Adjuntar stdout completo del scanner de secretos.
- Registrar versión ESP-IDF/toolchain.
```
"""

EVIDENCE_README = """# LAB 01 — Evidencias

Este directorio contiene evidencias reproducibles del LAB 01.

## Evidencias actuales

| Archivo | Contenido | Estado |
|---|---|---|
| `lab01_insecure_console.log` | Log funcional del perfil INSECURE | CUMPLE |
| `lab01_hardened_console.log` | Log funcional del perfil HARDENED | CUMPLE |
| `lab01_static_gates_reported.txt` | Gates reportados como PASS por operador | CUMPLE con limitación |

## Evidencias pendientes

| Archivo esperado | Motivo | Estado |
|---|---|---|
| `lab01_build_esp32s3.txt` | stdout completo de `idf.py build` | PENDIENTE |
| `lab01_secret_scan.txt` | stdout completo del scanner de secretos | PENDIENTE |

## Política

No se deben subir artefactos generados pesados ni contaminantes:

```text
firmware/build/
firmware/sdkconfig
firmware/sdkconfig.old
```

Sí se deben subir evidencias pequeñas y textuales que permitan auditar el resultado.
"""

INSECURE_LOG = """{"event":"boot","schema_version":1,"uptime_ms":14,"project":"secure_embedded_labs_lab01","fw_version":"0.1.0","lab":"LAB01","profile":"INSECURE","target":"esp32s3","console_transport":"usb_serial_jtag_stdio","build_gate":"not_executed_by_generator"}
{"event":"console_start","schema_version":1,"uptime_ms":15,"profile":"INSECURE","transport":"usb_serial_jtag_stdio","line_policy":"max_length_enforced"}
{"event":"command_received","schema_version":1,"uptime_ms":5059,"profile":"INSECURE","raw":"help"}
{"event":"help","schema_version":1,"uptime_ms":5060,"profile":"INSECURE","commands":"help,status,security_status,sample,get_config,set_period <s>,set_mqtt_password <value>,factory_reset"}
{"event":"command_received","schema_version":1,"uptime_ms":19058,"profile":"INSECURE","raw":"period"}
{"event":"command_rejected","schema_version":1,"uptime_ms":19059,"profile":"INSECURE","cmd":"period","reason":"unknown_command"}
{"event":"command_received","schema_version":1,"uptime_ms":33958,"profile":"INSECURE","raw":"set_period 25s"}
{"event":"config_update_accepted","schema_version":1,"uptime_ms":33959,"profile":"INSECURE","field":"sample_period_s","value":"25"}
"""

HARDENED_LOG = """I (127) main_task: Calling app_main()
{"event":"boot","schema_version":1,"uptime_ms":14,"project":"secure_embedded_labs_lab01","fw_version":"0.1.0","lab":"LAB01","profile":"HARDENED","target":"esp32s3","console_transport":"usb_serial_jtag_stdio","build_gate":"not_executed_by_generator"}
{"event":"console_start","schema_version":1,"uptime_ms":15,"profile":"HARDENED","transport":"usb_serial_jtag_stdio","line_policy":"max_length_enforced"}
{"event":"command_received","schema_version":1,"uptime_ms":22859,"profile":"HARDENED","cmd":"help"}
{"event":"help","schema_version":1,"uptime_ms":22860,"profile":"HARDENED","commands":"help,status,security_status,sample,get_config,set_period <s>,set_mqtt_password <value>,factory_reset"}
{"event":"command_received","schema_version":1,"uptime_ms":36408,"profile":"HARDENED","cmd":"set_period"}
{"event":"config_update_rejected","schema_version":1,"uptime_ms":36409,"profile":"HARDENED","field":"sample_period_s","reason":"invalid_uint32"}
{"event":"command_received","schema_version":1,"uptime_ms":49508,"profile":"HARDENED","cmd":"set_period"}
{"event":"config_update_rejected","schema_version":1,"uptime_ms":49509,"profile":"HARDENED","field":"sample_period_s","value":"0","reason":"out_of_range"}
{"event":"command_received","schema_version":1,"uptime_ms":58058,"profile":"HARDENED","cmd":"set_period"}
{"event":"config_update_accepted","schema_version":1,"uptime_ms":58059,"profile":"HARDENED","field":"sample_period_s","value":"60"}
{"event":"command_received","schema_version":1,"uptime_ms":70258,"profile":"HARDENED","cmd":"set_mqtt_password","args":"<redacted>"}
{"event":"secret_updated","schema_version":1,"uptime_ms":70259,"profile":"HARDENED","field":"mqtt_password","value":"<redacted>"}
{"event":"command_received","schema_version":1,"uptime_ms":84008,"profile":"HARDENED","cmd":"get_config"}
{"event":"config_dump","schema_version":1,"uptime_ms":84009,"profile":"HARDENED","device_id":"LAB01-UNPROVISIONED","sample_period_s":"60","mqtt_host":"mqtt.example.invalid","mqtt_port":"8883","mqtt_username":"lab_user","mqtt_password":"<redacted>"}
{"event":"command_received","schema_version":1,"uptime_ms":95058,"profile":"HARDENED","cmd":"factory_reset"}
{"event":"command_rejected","schema_version":1,"uptime_ms":95059,"profile":"HARDENED","cmd":"factory_reset","reason":"rejected_by_policy"}
"""

STATIC_GATES_REPORTED = """# LAB 01 — Static gates evidence

Estado: CUMPLE con limitación.

El operador reportó que los siguientes comandos pasaron correctamente tras validar el firmware en hardware:

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
python labs/lab01_insecure_vs_hardened/tools/run_static_gates.py
```

Limitación:
- Este archivo no es stdout raw capturado automáticamente.
- Sustituir o complementar por salida completa cuando se cierre la evidencia formal.
"""

APACHE_LICENSE = """                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS
"""


def main() -> None:
    root = repo_root()
    lab = root / "labs" / "lab01_insecure_vs_hardened"
    if not lab.exists():
        raise SystemExit("ERROR: LAB 01 directory not found.")

    write_text(root / "README.md", ROOT_README)
    write_text(lab / "README.md", LAB01_README)
    write_text(lab / "docs" / "audit_evidence.md", AUDIT_EVIDENCE)
    write_text(lab / "docs" / "requirements.md", REQUIREMENTS)
    write_text(lab / "docs" / "test_plan.md", TEST_PLAN)
    write_text(lab / "evidence" / "README.md", EVIDENCE_README)
    write_text(lab / "evidence" / "lab01_insecure_console.log", INSECURE_LOG)
    write_text(lab / "evidence" / "lab01_hardened_console.log", HARDENED_LOG)
    write_text(lab / "evidence" / "lab01_static_gates_reported.txt", STATIC_GATES_REPORTED)
    if not (root / "LICENSE").exists():
        write_text(root / "LICENSE", APACHE_LICENSE)

    print("Updated LAB 01 documentation and evidence.")
    print("Next: run gates, inspect diff, then commit.")


if __name__ == "__main__":
    main()
