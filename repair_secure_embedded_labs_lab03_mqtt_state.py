#!/usr/bin/env python3
"""Sanea la migración de LAB 03 a familia MQTT.

Ejecutar desde la raíz de secure-embedded-labs.
No implementa LAB 03B ni toca firmware de forma intencionada.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABS = ROOT / "labs"
LAB03 = LABS / "lab03_mqtt"
LEGACY_LAB03 = LABS / "lab03_mqtt_tls"
BOOK = ROOT / "book"
DOCS = ROOT / "docs"
TOOLS = ROOT / "tools"

REQUIRED_LAB_README_SECTIONS = [
    "## Índice",
    "## Objetivo",
    "## Objetivos de aprendizaje",
    "## Prerrequisitos",
    "## Alcance",
    "## Fuera de alcance",
    "## Hardware requerido",
    "## Software requerido",
    "## Arquitectura prevista",
    "## Modelo temporal",
    "## Threat model",
    "## Requisitos",
    "## Cómo compilar",
    "## Cómo flashear",
    "## Cómo probar",
    "## Evidencias esperadas",
    "## Errores comunes",
    "## Ejercicios",
    "## Preguntas de repaso",
    "## Fuentes",
    "## Estado",
]

SUBLABS = [
    ("lab03a_m03_1883_plain_no_auth", "LAB 03A", "M03-1883", "MQTT TCP plano sin TLS y sin autenticación", "CUMPLE dry-run", "1883", "No", "No"),
    ("lab03b_m03_1884_plain_auth", "LAB 03B", "M03-1884", "MQTT TCP plano con usuario/password", "PENDIENTE", "1884", "No", "Usuario/password"),
    ("lab03c_m03_8883_8886_tls_server_auth", "LAB 03C", "M03-8883 / M03-8886", "MQTT TLS con validación de servidor", "PENDIENTE", "8883 / 8886", "Sí", "No"),
    ("lab03d_m03_8885_tls_userpass", "LAB 03D", "M03-8885", "MQTT TLS con usuario/password", "PENDIENTE", "8885", "Sí", "Usuario/password"),
    ("lab03e_m03_8884_mtls_client_cert", "LAB 03E", "M03-8884", "MQTT con certificado cliente mTLS", "PENDIENTE", "8884", "Sí", "Certificado cliente"),
    ("lab03f_m03_8887_expired_cert_rejection", "LAB 03F", "M03-8887", "Rechazo de certificado servidor expirado", "PENDIENTE", "8887", "Sí, expirado", "No"),
    ("lab03g_m03_websockets", "LAB 03G", "M03-8080/8081/8090/8091", "MQTT over WebSockets y WebSockets Secure", "PENDIENTE", "8080/8081/8090/8091", "Mixto", "Mixto"),
]


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = "\n".join(line.rstrip() for line in text.strip().splitlines()) + "\n"
    path.write_text(normalized, encoding="utf-8", newline="\n")
    print(f"wrote: {path.relative_to(ROOT)}")


def touch_gitkeep(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    keep = path / ".gitkeep"
    if not keep.exists():
        keep.write_text("", encoding="utf-8")


def remove_if_exists(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
        print(f"removed directory: {path.relative_to(ROOT)}")
    elif path.exists():
        path.unlink()
        print(f"removed file: {path.relative_to(ROOT)}")


def ensure_lab03_tree() -> None:
    if LEGACY_LAB03.exists() and not LAB03.exists():
        LEGACY_LAB03.rename(LAB03)
        print("renamed legacy lab03_mqtt_tls -> lab03_mqtt")
    elif LEGACY_LAB03.exists() and LAB03.exists():
        shutil.rmtree(LEGACY_LAB03)
        print("removed legacy lab03_mqtt_tls")

    for rel in ["common", "docs", "evidence", "tools"]:
        (LAB03 / rel).mkdir(parents=True, exist_ok=True)

    for name, *_ in SUBLABS:
        sub = LAB03 / name
        for rel in ["docs", "evidence", "firmware", "test", "tools"]:
            (sub / rel).mkdir(parents=True, exist_ok=True)
        # Mantener subdirectorios futuros en Git aunque estén vacíos.
        if name != "lab03a_m03_1883_plain_no_auth":
            for rel in ["docs", "evidence", "firmware", "test", "tools"]:
                touch_gitkeep(sub / rel)


def root_readme() -> str:
    return """
# Secure Embedded Labs

**Estado:** EN CURSO
**Objetivo:** laboratorios reproducibles de ciberseguridad embebida para ESP32-S3.

## Índice

- [Objetivo](#objetivo)
- [Estado de laboratorios](#estado-de-laboratorios)
- [Árbol principal](#arbol-principal)
- [Criterio de cierre](#criterio-de-cierre)
- [Gates mínimos](#gates-minimos)

## Objetivo

`secure-embedded-labs` es un repositorio-libro de laboratorios de ciberseguridad embebida.
Cada laboratorio debe mantener firmware, documentación, evidencias, herramientas y gates alineados.

## Estado de laboratorios

| Lab | Tema | Estado |
| --- | --- | --- |
| LAB 01 | Firmware inseguro vs endurecido | CUMPLE |
| LAB 02 | Identidad única de dispositivo | CUMPLE |
| LAB 03 | Familia MQTT contra `test.mosquitto.org` | EN CURSO |
| LAB 04...LAB 10 | Fases futuras | PENDIENTE |

## Árbol principal

```text
secure-embedded-labs/
├── book/
├── docs/
├── labs/
│   ├── lab01_insecure_vs_hardened/
│   ├── lab02_device_identity/
│   └── lab03_mqtt/
├── standard/
└── tools/
```

## Criterio de cierre

Un laboratorio solo puede declararse `CUMPLE` cuando existen implementación, documentación, evidencias y gates en PASS.
Las fases dry-run deben diferenciarse explícitamente de las conexiones reales.

## Gates mínimos

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
```
"""


def roadmap() -> str:
    return """
# Roadmap — Secure Embedded Labs

## Índice

- [Estado general](#estado-general)
- [LAB 01](#lab-01)
- [LAB 02](#lab-02)
- [LAB 03](#lab-03)
- [Fases futuras](#fases-futuras)

## Estado general

El proyecto evoluciona como repositorio-libro audit-grade. Cada cambio debe mantener alineados código, documentación, libro, evidencias, gates y changelog.

## LAB 01

```text
CUMPLE:
- Firmware inseguro vs endurecido validado para el alcance actual.
```

## LAB 02

```text
CUMPLE:
- Identidad clonable frente a identidad derivada de hardware validada para el alcance actual.
```

## LAB 03

LAB 03 queda organizado como familia MQTT contra `test.mosquitto.org`.

```text
CUMPLE:
- LAB 03A — M03-1883 / MQTT TCP plano sin TLS ni autenticación / dry-run.

PENDIENTE:
- LAB 03B — M03-1884 / MQTT TCP plano con usuario/password.
- LAB 03C — M03-8883 y M03-8886 / MQTT TLS servidor.
- LAB 03D — M03-8885 / MQTT TLS con usuario/password.
- LAB 03E — M03-8884 / mTLS con certificado cliente.
- LAB 03F — M03-8887 / rechazo de certificado expirado.
- LAB 03G — MQTT over WebSockets.
```

## Fases futuras

LAB 04 a LAB 10 permanecen como placeholders hasta definición y evidencias.
"""


def changelog() -> str:
    return """
# Changelog

## Índice

- [Unreleased](#unreleased)

## Unreleased

### Changed

- Reorganizado LAB 03 desde `labs/lab03_mqtt_tls/` a `labs/lab03_mqtt/`.
- Convertido LAB 03 en familia MQTT con sublaboratorios LAB 03A a LAB 03G.
- Aislado LAB 03A como `lab03a_m03_1883_plain_no_auth`.
- Corregida la documentación transversal para reflejar matriz MQTT, no solo TLS.

### Fixed

- Saneados gates y documentación tras la migración estructural de LAB 03.
- Eliminadas referencias activas a la ruta legacy `lab03_mqtt_tls`.
"""


def labs_readme() -> str:
    return """
# Laboratorios

## Índice

- [Resumen](#resumen)
- [Tabla de laboratorios](#tabla-de-laboratorios)
- [Árbol](#arbol)
- [Estado](#estado)

## Resumen

Los laboratorios están organizados como unidades auditables. Cada uno debe mantener documentación, firmware, herramientas, test y evidencias.

## Tabla de laboratorios

| Lab | Directorio | Tema | Estado |
| --- | --- | --- | --- |
| LAB 01 | `lab01_insecure_vs_hardened` | Firmware inseguro vs endurecido | CUMPLE |
| LAB 02 | `lab02_device_identity` | Identidad única de dispositivo | CUMPLE |
| LAB 03 | `lab03_mqtt` | Familia MQTT contra `test.mosquitto.org` | EN CURSO |
| LAB 04...LAB 10 | placeholders | Fases futuras | PENDIENTE |

## Árbol

```text
labs/
├── _template/
├── lab01_insecure_vs_hardened/
├── lab02_device_identity/
├── lab03_mqtt/
│   ├── common/
│   ├── docs/
│   ├── evidence/
│   ├── tools/
│   ├── lab03a_m03_1883_plain_no_auth/
│   ├── lab03b_m03_1884_plain_auth/
│   ├── lab03c_m03_8883_8886_tls_server_auth/
│   ├── lab03d_m03_8885_tls_userpass/
│   ├── lab03e_m03_8884_mtls_client_cert/
│   ├── lab03f_m03_8887_expired_cert_rejection/
│   └── lab03g_m03_websockets/
└── lab04...lab10/
```

## Estado

```text
CUMPLE:
- LAB 01 y LAB 02 cerrados para el alcance actual.
- LAB 03A cerrado como dry-run dentro de la familia MQTT.

PENDIENTE:
- LAB 03B y siguientes.
```
"""


def book_readme() -> str:
    return """
# Libro — Secure Embedded Labs

## Índice

- [Propósito](#proposito)
- [Capítulos](#capitulos)
- [Estado](#estado)

## Propósito

El libro acompaña al repositorio técnico y explica la narrativa de seguridad de cada laboratorio.
No sustituye a las evidencias ni a los gates.

## Capítulos

| Capítulo | Tema | Estado |
| --- | --- | --- |
| 01 | Firmware inseguro vs endurecido | CUMPLE |
| 02 | Identidad única de dispositivo | CUMPLE |
| 03 | Matriz MQTT | EN CURSO |

## Estado

```text
CUMPLE:
- El libro refleja LAB 01, LAB 02 y la reorganización de LAB 03 como matriz MQTT.

PENDIENTE:
- Ampliar capítulos conforme se cierren nuevos sublaboratorios.
```
"""


def publishing_model() -> str:
    return """
# Modelo de publicación

## Índice

- [Criterio](#criterio)
- [Cierre transversal](#cierre-transversal)
- [Estado](#estado)

## Criterio

Cada entrega debe mantener sincronizados repositorio, libro, roadmap, changelog, documentación de laboratorio, herramientas y evidencias.

## Cierre transversal

Antes de continuar con un laboratorio nuevo deben pasar, como mínimo:

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
```

Cuando aplique LAB 03:

```powershell
python labs/lab03_mqtt/tools/run_static_gates.py
python labs/lab03_mqtt/tools/capture_static_gates.py
```

## Estado

```text
CUMPLE:
- El modelo exige sincronización documental y evidencial antes de avanzar.
```
"""


def repository_tree_doc() -> str:
    return """
# Árbol contractual del repositorio

## Índice

- [Árbol principal](#arbol-principal)
- [LAB 03](#lab-03)
- [Estado](#estado)

## Árbol principal

```text
secure-embedded-labs/
├── book/
├── docs/
├── labs/
├── standard/
└── tools/
```

## LAB 03

```text
labs/lab03_mqtt/
├── common/
├── docs/
├── evidence/
├── tools/
├── lab03a_m03_1883_plain_no_auth/
├── lab03b_m03_1884_plain_auth/
├── lab03c_m03_8883_8886_tls_server_auth/
├── lab03d_m03_8885_tls_userpass/
├── lab03e_m03_8884_mtls_client_cert/
├── lab03f_m03_8887_expired_cert_rejection/
└── lab03g_m03_websockets/
```

## Estado

```text
CUMPLE:
- LAB 03 queda representado como familia MQTT y no como laboratorio exclusivamente TLS.
```
"""


def lab03_family_readme() -> str:
    return """
# LAB 03 — Familia MQTT contra test.mosquitto.org

**Versión:** 0.2.0
**Estado:** EN CURSO
**Modelo:** familia de sublaboratorios independientes

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
- [Cómo compilar](#como-compilar)
- [Cómo flashear](#como-flashear)
- [Cómo probar](#como-probar)
- [Evidencias esperadas](#evidencias-esperadas)
- [Errores comunes](#errores-comunes)
- [Ejercicios](#ejercicios)
- [Preguntas de repaso](#preguntas-de-repaso)
- [Fuentes](#fuentes)
- [Estado](#estado)

## Objetivo

Organizar una matriz MQTT reproducible contra `test.mosquitto.org`, separando cada escenario en un sublaboratorio auditable.

## Objetivos de aprendizaje

- Diferenciar conectividad funcional de diseño seguro.
- Separar autenticación, confidencialidad, validación de certificados y mTLS.
- Evidenciar que MQTT plano no protege credenciales ni payloads sensibles.
- Mantener trazabilidad escenario → diseño → firmware → test → evidencia.

## Prerrequisitos

- Repositorio limpio de artefactos generados.
- Python 3 para herramientas y gates.
- ESP-IDF cuando se compile firmware.
- No usar secretos reales contra brokers públicos.

## Alcance

Esta familia cubre los escenarios MQTT publicados por `test.mosquitto.org` mediante sublaboratorios independientes.

## Fuera de alcance

- Declarar conexión real si solo existe dry-run.
- Versionar secretos, claves privadas reales o credenciales operativas.
- Tratar LAB 03 como un único firmware monolítico.

## Hardware requerido

- ESP32-S3 compatible.
- Cable USB de datos.
- Consola USB Serial/JTAG para fases dry-run.
- Conectividad Wi-Fi solo cuando el sublaboratorio declare conexión real.

## Software requerido

- Git.
- Python 3.
- ESP-IDF compatible con ESP32-S3.
- PowerShell o terminal equivalente.

## Arquitectura prevista

```text
lab03_mqtt/
├── common/
├── docs/
├── evidence/
├── tools/
├── lab03a_m03_1883_plain_no_auth/
├── lab03b_m03_1884_plain_auth/
├── lab03c_m03_8883_8886_tls_server_auth/
├── lab03d_m03_8885_tls_userpass/
├── lab03e_m03_8884_mtls_client_cert/
├── lab03f_m03_8887_expired_cert_rejection/
└── lab03g_m03_websockets/
```

La carpeta superior contiene contrato común, documentación de matriz, gates agregados y evidencias transversales. Cada sublaboratorio mantiene su propio cierre documental y técnico.

## Modelo temporal

Las fases dry-run usan interacción por consola. No hay tareas de red reales ni dependencia temporal externa.
Cuando se introduzca conexión real, el sublaboratorio deberá documentar tareas, timeouts, retry, backoff y deadlines.

## Threat model

Amenazas mínimas:

- exposición de credenciales;
- ausencia de confidencialidad;
- validación incorrecta de certificados;
- uso de broker público;
- publicación accidental de secretos;
- confusión entre autenticación y cifrado.

## Requisitos

- Logs sin secretos.
- Evidencias reproducibles.
- Gates globales y específicos en PASS.
- Separación explícita entre dry-run y conexión real.
- Estados `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` y `PENDIENTE`.

## Cómo compilar

Para LAB 03A:

```powershell
cd labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/firmware
idf.py set-target esp32s3
idf.py build
```

## Cómo flashear

Para LAB 03A:

```powershell
idf.py -p COMx flash monitor
```

Sustituir `COMx` por el puerto real.

## Cómo probar

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
python labs/lab03_mqtt/tools/run_static_gates.py
python labs/lab03_mqtt/tools/capture_static_gates.py
```

## Evidencias esperadas

- Evidencia agregada de gates: `evidence/lab03_static_gates.txt`.
- Evidencia LAB 03A: `lab03a_m03_1883_plain_no_auth/evidence/lab03_m03_1883_console.log`.
- Evidencias propias para LAB 03B y siguientes cuando se implementen.

## Errores comunes

- Confundir autenticación con confidencialidad.
- Declarar seguro un escenario sin TLS.
- Mantener rutas legacy tras una migración.
- Reutilizar evidencias de otro sublaboratorio.

## Ejercicios

- Clasificar cada escenario como funcional, inseguro, mitigado o no validado.
- Identificar qué activo protege cada mitigación.
- Revisar si los logs contienen secretos.

## Preguntas de repaso

- ¿Por qué usuario/password sin TLS no protege credenciales?
- ¿Qué diferencia hay entre TLS y mTLS?
- ¿Por qué un certificado expirado debe provocar fallo de conexión?

## Fuentes

- Documentación pública de `test.mosquitto.org`.
- Documentación oficial de ESP-IDF.
- Estándar audit-grade interno del proyecto.

## Estado

```text
CUMPLE:
- LAB 03 queda modelado como familia MQTT.
- LAB 03A queda aislado como sublaboratorio para M03-1883.

NO VALIDADO:
- LAB 03B y posteriores no están cerrados.
- Conexión MQTT real todavía no forma parte del cierre dry-run.

PENDIENTE:
- Continuar con LAB 03B después de cerrar gates y evidencia estática.
```
"""


def sublab_readme(name: str, label: str, scenario: str, title: str, status: str, port: str, tls: str, auth: str) -> str:
    is_03a = name.startswith("lab03a_")
    return f"""
# {label} — {scenario} / {title}

**Estado:** {status}
**Escenario:** {scenario}
**Puerto:** {port}

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
- [Cómo compilar](#como-compilar)
- [Cómo flashear](#como-flashear)
- [Cómo probar](#como-probar)
- [Evidencias esperadas](#evidencias-esperadas)
- [Errores comunes](#errores-comunes)
- [Ejercicios](#ejercicios)
- [Preguntas de repaso](#preguntas-de-repaso)
- [Fuentes](#fuentes)
- [Estado](#estado)

## Objetivo

Validar el escenario `{scenario}` dentro de la familia LAB 03 MQTT.

## Objetivos de aprendizaje

- Separar comportamiento funcional de cumplimiento de seguridad.
- Identificar el efecto de TLS, autenticación y validación de certificados.
- Mantener evidencia propia del sublaboratorio.

## Prerrequisitos

- Revisar `../README.md`.
- Mantener limpio el árbol de artefactos generados.
- No usar secretos reales contra brokers públicos.

## Alcance

Este sublaboratorio cubre `{scenario}`: {title}.

## Fuera de alcance

- Reutilizar evidencias de otro sublaboratorio.
- Declarar conexión real si solo existe dry-run.
- Introducir credenciales reales en firmware, logs o documentación.

## Hardware requerido

- ESP32-S3 compatible.
- Cable USB de datos.
- Consola USB Serial/JTAG para fases dry-run.

## Software requerido

- Git.
- Python 3.
- ESP-IDF compatible con ESP32-S3 cuando exista firmware.
- PowerShell o terminal equivalente.

## Arquitectura prevista

```text
{name}/
├── README.md
├── CHANGELOG.md
├── docs/
├── evidence/
├── firmware/
├── test/
└── tools/
```

## Modelo temporal

La fase dry-run usa interacción por consola. Las conexiones reales deberán declarar timeouts, retry y política de fallo.

## Threat model

Propiedades del escenario:

```text
TLS: {tls}
Auth: {auth}
Broker: test.mosquitto.org
```

## Requisitos

- Logs sin secretos.
- Evidencia propia del escenario.
- Separación explícita entre dry-run y conexión real.
- Gates en PASS antes de declarar cierre.

## Cómo compilar

{"```powershell\ncd labs\\lab03_mqtt\\lab03a_m03_1883_plain_no_auth\\firmware\nidf.py set-target esp32s3\nidf.py build\n```" if is_03a else "Este sublaboratorio todavía no tiene firmware propio validado."}

## Cómo flashear

{"```powershell\nidf.py -p COMx flash monitor\n```" if is_03a else "No aplica hasta que exista firmware propio validado."}

## Cómo probar

```powershell
python tools/repo_quality_gates/run_static_repo_gates.py
python labs/lab03_mqtt/tools/run_static_gates.py
```

## Evidencias esperadas

{"- `evidence/lab03_m03_1883_console.log`.\n- Evidencia agregada de gates en `../evidence/lab03_static_gates.txt`." if is_03a else "- Evidencia de consola propia cuando se implemente.\n- Evidencia de gates tras integrar el sublaboratorio."}

## Errores comunes

- Confundir autenticación con confidencialidad.
- Publicar secretos reales.
- Dar por validada una conexión no probada.

## Ejercicios

- Clasificar el escenario como seguro, inseguro o no validado.
- Identificar qué propiedades de seguridad faltan.
- Revisar si la evidencia disponible justifica el estado declarado.

## Preguntas de repaso

- ¿Qué protege TLS en este escenario?
- ¿Qué protege la autenticación?
- ¿Qué evidencia permite declarar `CUMPLE`?

## Fuentes

- Documentación pública de `test.mosquitto.org`.
- Documentación oficial de ESP-IDF.
- Estándar audit-grade interno del proyecto.

## Estado

```text
{status}
```
"""


def lab03_changelog() -> str:
    return """
# Changelog — LAB 03 MQTT

## Índice

- [Unreleased](#unreleased)

## Unreleased

### Changed

- LAB 03 queda organizado como familia MQTT en `labs/lab03_mqtt/`.
- LAB 03A queda aislado como sublaboratorio independiente para `M03-1883`.
- LAB 03B a LAB 03G quedan preparados como sublaboratorios pendientes.

### Fixed

- Saneados README y gates tras la migración desde `lab03_mqtt_tls`.
"""


def sublab_changelog(label: str, scenario: str, status: str) -> str:
    return f"""
# Changelog — {label}

## Índice

- [Unreleased](#unreleased)

## Unreleased

### Estado

```text
{status}
```

### Notas

- Sublaboratorio asociado a `{scenario}` dentro de LAB 03 MQTT.
"""


def evidence_readme() -> str:
    return """
# Evidencias — LAB 03 MQTT

## Índice

- [Resumen](#resumen)
- [Evidencias](#evidencias)
- [Estado](#estado)

## Resumen

Esta carpeta contiene evidencias agregadas de la familia LAB 03 MQTT.

## Evidencias

| Evidencia | Estado |
| --- | --- |
| `lab03_static_gates.txt` | CUMPLE cuando se regenere con gates actuales |
| LAB 03A consola | Ver `../lab03a_m03_1883_plain_no_auth/evidence/` |

## Estado

```text
PENDIENTE:
- Regenerar `lab03_static_gates.txt` después del saneamiento.
```
"""


def scenario_matrix_doc() -> str:
    return """
# Matriz MQTT — LAB 03

## Índice

- [Matriz](#matriz)
- [Criterio](#criterio)
- [Estado](#estado)

## Matriz

| Sublab | Escenario | Puerto | TLS | Auth | Estado |
| --- | --- | ---: | --- | --- | --- |
| LAB 03A | M03-1883 | 1883 | No | No | CUMPLE dry-run |
| LAB 03B | M03-1884 | 1884 | No | Usuario/password | PENDIENTE |
| LAB 03C | M03-8883 / M03-8886 | 8883 / 8886 | Sí | No | PENDIENTE |
| LAB 03D | M03-8885 | 8885 | Sí | Usuario/password | PENDIENTE |
| LAB 03E | M03-8884 | 8884 | Sí | Certificado cliente | PENDIENTE |
| LAB 03F | M03-8887 | 8887 | Sí, expirado | No | PENDIENTE |
| LAB 03G | M03-8080/8081/8090/8091 | 8080/8081/8090/8091 | Mixto | Mixto | PENDIENTE |

## Criterio

Los escenarios sin TLS pueden ser funcionales, pero no cumplen seguridad para credenciales ni datos sensibles.

## Estado

```text
CUMPLE:
- Matriz documentada.

PENDIENTE:
- Completar LAB 03B y siguientes con evidencias propias.
```
"""


def book_chapter_03() -> str:
    return """
# Capítulo 03 — Matriz MQTT

## Índice

- [Objetivo](#objetivo)
- [Idea central](#idea-central)
- [Matriz](#matriz)
- [Estado](#estado)

## Objetivo

Explicar LAB 03 como una matriz de escenarios MQTT contra `test.mosquitto.org`.

## Idea central

MQTT funcional no implica MQTT seguro. La seguridad depende de confidencialidad, autenticación, validación de certificados, gestión de credenciales y evidencia real.

## Matriz

LAB 03 se divide en sublaboratorios independientes desde LAB 03A hasta LAB 03G.

## Estado

```text
CUMPLE:
- LAB 03A queda documentado como baseline dry-run.

PENDIENTE:
- Completar capítulos conforme se cierren LAB 03B y siguientes.
```
"""


def global_gate() -> str:
    lab_list = "\n".join(f'    "{lab}",' for lab in [
        "lab01_insecure_vs_hardened",
        "lab02_device_identity",
        "lab03_mqtt",
        "lab04_signed_ota",
        "lab05_secure_remote_config",
        "lab06_physical_interface_hardening",
        "lab07_sbom_release_traceability",
        "lab08_secure_boot_flash_encryption",
        "lab09_secure_multi_interface_gateway",
        "lab10_mini_psirt",
    ])
    sections = "\n".join(f'    "{section}",' for section in REQUIRED_LAB_README_SECTIONS)
    return f'''#!/usr/bin/env python3
"""Static repository gates for Secure Embedded Labs."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_FILES = [
    "README.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "DISCLAIMER.md",
    "CHANGELOG.md",
    "LICENSE",
    "LICENSE-DOCS",
    "standard/estandar_diseno_embebido_audit_grade.md",
    "labs/README.md",
    "labs/_template/README.md",
    "book/README.md",
]

LAB_DIRS = [
{lab_list}
]

REQUIRED_LAB_README_SECTIONS = [
{sections}
]

FORBIDDEN_PATH_PARTS = {{"build", "managed_components", ".pytest_cache", "__pycache__"}}
FORBIDDEN_FILES = {{"sdkconfig", "sdkconfig.old", "dependencies.lock"}}


def fail(message: str) -> None:
    print(f"FAIL: {{message}}")
    raise SystemExit(1)


def check_required_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"required file missing: {{rel}}")


def check_lab_readmes() -> None:
    for lab in LAB_DIRS:
        readme = ROOT / "labs" / lab / "README.md"
        if not readme.is_file():
            fail(f"lab README missing: {{readme.relative_to(ROOT)}}")
        text = readme.read_text(encoding="utf-8")
        for section in REQUIRED_LAB_README_SECTIONS:
            if section not in text:
                fail(f"{{readme.relative_to(ROOT)}} missing section: {{section}}")


def check_forbidden_artifacts() -> None:
    for path in ROOT.rglob("*"):
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts:
            continue
        if set(rel.parts) & FORBIDDEN_PATH_PARTS:
            fail(f"forbidden generated directory present: {{rel}}")
        if path.name in FORBIDDEN_FILES:
            fail(f"forbidden generated/config file present: {{rel}}")


def check_markdown_indices() -> None:
    for md in ROOT.rglob("*.md"):
        rel = md.relative_to(ROOT)
        if ".git" in rel.parts:
            continue
        text = md.read_text(encoding="utf-8")
        if "## Índice" not in text and md.name.upper() != "LICENSE.md":
            fail(f"Markdown without index: {{rel}}")


def main() -> int:
    check_required_files()
    check_lab_readmes()
    check_forbidden_artifacts()
    check_markdown_indices()
    print("PASS: static repository gates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def lab03_gate() -> str:
    sections = "\n".join(f'    "{section}",' for section in REQUIRED_LAB_README_SECTIONS)
    required_dirs = "\n".join(f'    "{name}",' for name in [
        "common",
        "docs",
        "evidence",
        "tools",
        *[name for name, *_ in SUBLABS],
    ])
    return f'''#!/usr/bin/env python3
"""Static gates for LAB 03 MQTT family."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
LAB03 = ROOT / "labs" / "lab03_mqtt"
LEGACY = ROOT / "labs" / "lab03_mqtt_tls"

REQUIRED_DIRS = [
{required_dirs}
]

REQUIRED_LAB_README_SECTIONS = [
{sections}
]


def fail(message: str) -> None:
    print(f"FAIL: {{message}}")
    raise SystemExit(1)


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing file: {{path.relative_to(ROOT)}}")


def require_dir(path: Path) -> None:
    if not path.is_dir():
        fail(f"missing directory: {{path.relative_to(ROOT)}}")


def check_readme(path: Path) -> None:
    require_file(path)
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_LAB_README_SECTIONS:
        if section not in text:
            fail(f"{{path.relative_to(ROOT)}} missing section: {{section}}")


def check_markdown_indexes() -> None:
    for md in LAB03.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if "## Índice" not in text:
            fail(f"Markdown without index: {{md.relative_to(ROOT)}}")


def main() -> int:
    if LEGACY.exists():
        fail("legacy directory still present: labs/lab03_mqtt_tls")

    require_dir(LAB03)
    check_readme(LAB03 / "README.md")
    require_file(LAB03 / "CHANGELOG.md")

    for rel in REQUIRED_DIRS:
        require_dir(LAB03 / rel)

    for name in [
{chr(10).join(f'        "{name}",' for name, *_ in SUBLABS)}
    ]:
        check_readme(LAB03 / name / "README.md")
        require_file(LAB03 / name / "CHANGELOG.md")

    check_markdown_indexes()
    print("PASS: LAB 03 static gates completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def capture_static_gates() -> str:
    return '''#!/usr/bin/env python3
"""Capture static gate evidence for LAB 03 MQTT."""
from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "labs" / "lab03_mqtt" / "evidence" / "lab03_static_gates.txt"


def run_command(args: list[str]) -> tuple[int, str]:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return proc.returncode, proc.stdout


def main() -> int:
    commands = [
        [sys.executable, "tools/repo_quality_gates/run_static_repo_gates.py"],
        [sys.executable, "labs/lab03_mqtt/tools/run_static_gates.py"],
    ]

    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    chunks: list[str] = ["# LAB 03 static gates evidence", ""]
    ok = True

    for command in commands:
        chunks.append(f"$ {' '.join(command)}")
        rc, output = run_command(command)
        chunks.append(output.rstrip())
        chunks.append(f"# returncode={rc}")
        chunks.append("")
        if rc != 0:
            ok = False

    if ok:
        chunks.append("# capture_validation result=PASS")
    else:
        chunks.append("# capture_validation result=FAIL")

    EVIDENCE.write_text("\n".join(chunks) + "\n", encoding="utf-8", newline="\n")

    if not ok:
        print(f"FAIL: static gates evidence written to {EVIDENCE}")
        return 1

    print(f"PASS: static gates evidence written to {EVIDENCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''


def clean_temp_files() -> None:
    temp_files = [
        ROOT / "fix_lab03_mqtt_migration_contract.ps1",
        ROOT / "repair_lab03_mqtt_migration.py",
        ROOT / "repair_secure_embedded_labs_lab03_mqtt_state.py",
        TOOLS / "maintenance" / "fix_lab03_mqtt_family_gates.py",
        TOOLS / "maintenance" / "normalize_lab03_mqtt_migration_contract.py",
        TOOLS / "maintenance" / "normalize_lab03_readme_contract.py",
        TOOLS / "maintenance" / "normalize_lab03_readme_contract_from_gate.py",
    ]
    for path in temp_files:
        if path.exists() and path != Path(__file__).resolve():
            remove_if_exists(path)


def add_index_if_missing(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "## Índice" in text:
        normalized = "\n".join(line.rstrip() for line in text.splitlines()) + "\n"
        path.write_text(normalized, encoding="utf-8", newline="\n")
        return
    lines = text.splitlines()
    if not lines:
        return
    new = [lines[0], "", "## Índice", "", "- [Contenido](#contenido)", "", "## Contenido", ""] + lines[1:]
    path.write_text("\n".join(line.rstrip() for line in new) + "\n", encoding="utf-8", newline="\n")
    print(f"added index: {path.relative_to(ROOT)}")


def main() -> int:
    if not (ROOT / ".git").exists():
        print("FAIL: ejecutar desde la raíz del repositorio secure-embedded-labs")
        return 1

    ensure_lab03_tree()
    clean_temp_files()

    write_text(ROOT / "README.md", root_readme())
    write_text(ROOT / "ROADMAP.md", roadmap())
    write_text(ROOT / "CHANGELOG.md", changelog())
    write_text(LABS / "README.md", labs_readme())
    write_text(BOOK / "README.md", book_readme())
    write_text(DOCS / "publishing_model.md", publishing_model())
    write_text(DOCS / "repository_tree.md", repository_tree_doc())
    write_text(BOOK / "chapters" / "03_matriz_mqtt.md", book_chapter_03())
    remove_if_exists(BOOK / "chapters" / "03_matriz_mqtt_tls.md")

    write_text(LAB03 / "README.md", lab03_family_readme())
    write_text(LAB03 / "CHANGELOG.md", lab03_changelog())
    write_text(LAB03 / "evidence" / "README.md", evidence_readme())
    write_text(LAB03 / "docs" / "scenario_matrix.md", scenario_matrix_doc())

    for name, label, scenario, title, status, port, tls, auth in SUBLABS:
        sub = LAB03 / name
        write_text(sub / "README.md", sublab_readme(name, label, scenario, title, status, port, tls, auth))
        write_text(sub / "CHANGELOG.md", sublab_changelog(label, scenario, status))

    write_text(TOOLS / "repo_quality_gates" / "run_static_repo_gates.py", global_gate())
    write_text(LAB03 / "tools" / "run_static_gates.py", lab03_gate())
    write_text(LAB03 / "tools" / "capture_static_gates.py", capture_static_gates())

    # Garantía mínima: todos los Markdown de LAB 03 deben tener índice.
    for md in LAB03.rglob("*.md"):
        add_index_if_missing(md)

    # Limpieza de artefactos generados.
    for path in ROOT.rglob("*"):
        if path.name in {"build", "managed_components", ".pytest_cache", "__pycache__"} and path.is_dir():
            remove_if_exists(path)
        elif path.name in {"sdkconfig", "sdkconfig.old", "dependencies.lock"} and path.is_file():
            remove_if_exists(path)

    print("PASS: saneamiento LAB 03 MQTT aplicado")
    print("Siguiente paso:")
    print("  git diff --check")
    print("  python labs/lab03_mqtt/tools/run_static_gates.py")
    print("  python tools/repo_quality_gates/run_static_repo_gates.py")
    print("  python labs/lab03_mqtt/tools/capture_static_gates.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
