#!/usr/bin/env python3
"""Reestructura LAB 03 como familia MQTT con sublaboratorios independientes.

Uso desde la raíz del repo:
    python tools/maintenance/migrate_lab03_mqtt_family.py

El script es idempotente: puede ejecutarse más de una vez y evita destruir
contenido existente. Su objetivo es corregir la estructura documental y de
árbol antes de continuar con LAB 03B.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
LABS = ROOT / "labs"
OLD_LAB = LABS / "lab03_mqtt"
FAMILY = LABS / "lab03_mqtt"
LAB03A = FAMILY / "lab03a_m03_1883_plain_no_auth"

SUBLABS = {
    "lab03a_m03_1883_plain_no_auth": {
        "title": "LAB 03A — M03-1883 / MQTT TCP plano sin autenticación",
        "scenario": "M03-1883",
        "port": "1883",
        "status": "CUMPLE dry-run",
        "objective": "Demostrar el baseline MQTT TCP plano sin TLS y sin autenticación.",
    },
    "lab03b_m03_1884_plain_auth": {
        "title": "LAB 03B — M03-1884 / MQTT TCP plano con usuario/password",
        "scenario": "M03-1884",
        "port": "1884",
        "status": "PENDIENTE",
        "objective": "Demostrar que autenticación sin TLS no protege credenciales ni confidencialidad.",
    },
    "lab03c_m03_8883_8886_tls_server_auth": {
        "title": "LAB 03C — M03-8883/M03-8886 / TLS con validación de servidor",
        "scenario": "M03-8883 / M03-8886",
        "port": "8883 / 8886",
        "status": "PENDIENTE",
        "objective": "Validar TLS de servidor y política de CA antes de tratar autenticación de aplicación.",
    },
    "lab03d_m03_8885_tls_userpass": {
        "title": "LAB 03D — M03-8885 / MQTT TLS con usuario/password",
        "scenario": "M03-8885",
        "port": "8885",
        "status": "PENDIENTE",
        "objective": "Validar usuario/password sobre canal TLS con redacción de secretos.",
    },
    "lab03e_m03_8884_mtls_client_cert": {
        "title": "LAB 03E — M03-8884 / mTLS con certificado cliente",
        "scenario": "M03-8884",
        "port": "8884",
        "status": "PENDIENTE",
        "objective": "Validar autenticación de cliente mediante certificado sin versionar claves privadas reales.",
    },
    "lab03f_m03_8887_expired_cert_rejection": {
        "title": "LAB 03F — M03-8887 / rechazo de certificado expirado",
        "scenario": "M03-8887",
        "port": "8887",
        "status": "PENDIENTE",
        "objective": "Demostrar que el fallo de conexión por certificado expirado es el PASS de seguridad esperado.",
    },
    "lab03g_m03_websockets": {
        "title": "LAB 03G — MQTT over WebSockets / WS y WSS",
        "scenario": "M03-8080 / M03-8081 / M03-8090 / M03-8091",
        "port": "8080 / 8081 / 8090 / 8091",
        "status": "PENDIENTE",
        "objective": "Cubrir MQTT sobre WebSockets, WebSockets Secure y autenticación sobre ambos transportes.",
    },
}

TEXT_SUFFIXES = {".md", ".py", ".txt", ".yml", ".yaml", ".json", ".cmake", ".ini", ".cfg"}
GENERATED_NAMES = {"build", "sdkconfig", "sdkconfig.old"}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path) if path.exists() else ""
    if marker in text:
        return
    write_text(path, text.rstrip() + "\n\n" + block.strip() + "\n")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def merge_dir(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    ensure_dir(dst)
    for child in list(src.iterdir()):
        target = dst / child.name
        if target.exists():
            if child.is_dir() and target.is_dir():
                merge_dir(child, target)
                if child.exists() and not any(child.iterdir()):
                    child.rmdir()
            else:
                print(f"WARN: no se sobrescribe {rel(target)}; se conserva {rel(child)}")
        else:
            child.rename(target)
    if src.exists() and src.is_dir() and not any(src.iterdir()):
        src.rmdir()


def move_path(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    if dst.exists():
        if src.is_dir() and dst.is_dir():
            merge_dir(src, dst)
        else:
            print(f"WARN: destino existente, no se mueve {rel(src)} -> {rel(dst)}")
        return
    ensure_dir(dst.parent)
    src.rename(dst)


def remove_generated_artifacts(root: Path) -> None:
    for path in sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if path.name not in GENERATED_NAMES:
            continue
        if path.is_dir():
            shutil.rmtree(path)
            print(f"removed generated directory: {rel(path)}")
        elif path.is_file():
            path.unlink()
            print(f"removed generated file: {rel(path)}")


def iter_text_files() -> Iterable[Path]:
    skip_parts = {".git", "build"}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in skip_parts for part in path.parts):
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in {"CMakeLists.txt"}:
            yield path


def replace_all(old: str, new: str) -> None:
    for path in iter_text_files():
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            continue
        if old not in text:
            continue
        write_text(path, text.replace(old, new))


def migrate_root_directory() -> None:
    if OLD_LAB.exists() and not FAMILY.exists():
        OLD_LAB.rename(FAMILY)
        print(f"renamed {rel(OLD_LAB)} -> {rel(FAMILY)}")
    elif OLD_LAB.exists() and FAMILY.exists():
        print("WARN: existen lab03_mqtt y lab03_mqtt; se intenta fusionar sin sobrescribir")
        merge_dir(OLD_LAB, FAMILY)

    ensure_dir(FAMILY)


def split_lab03a() -> None:
    for name in SUBLABS:
        sublab = FAMILY / name
        for folder in ["docs", "evidence", "firmware", "test", "tools"]:
            ensure_dir(sublab / folder)

    move_path(FAMILY / "firmware", LAB03A / "firmware")
    move_path(FAMILY / "test", LAB03A / "test")
    move_path(FAMILY / "COMMIT_MESSAGE.txt", LAB03A / "COMMIT_MESSAGE.txt")

    # La evidencia de escenario pertenece a LAB 03A; la evidencia de gates agregados queda en la familia.
    move_path(
        FAMILY / "evidence" / "lab03_m03_1883_console.log",
        LAB03A / "evidence" / "lab03_m03_1883_console.log",
    )

    # Las herramientas de captura/validación de consola son del sublaboratorio ejecutable 03A.
    move_path(
        FAMILY / "tools" / "capture_console_evidence.py",
        LAB03A / "tools" / "capture_console_evidence.py",
    )
    move_path(
        FAMILY / "tools" / "check_mqtt_scenario_logs.py",
        LAB03A / "tools" / "check_mqtt_scenario_logs.py",
    )

    ensure_dir(FAMILY / "common" / "tools")
    ensure_dir(FAMILY / "common" / "firmware_components")


def family_readme() -> str:
    return """# LAB 03 — Familia MQTT contra test.mosquitto.org

**Versión:** 0.2.0
**Estado:** EN CURSO
**Modelo:** familia de sublaboratorios independientes

## Índice

- [Objetivo](#objetivo)
- [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
- [Prerrequisitos](#prerrequisitos)
- [Alcance](#alcance)
- [Fuera de alcance](#fuera-de-alcance)
- [Estructura](#estructura)
- [Matriz contractual](#matriz-contractual)
- [Arquitectura](#arquitectura)
- [Cómo trabajar](#cómo-trabajar)
- [Evidencias](#evidencias)
- [Estado](#estado)

## Objetivo

Agrupar una matriz reproducible de escenarios MQTT contra `test.mosquitto.org`, separando cada puerto/propiedad de seguridad en sublaboratorios auditables.

LAB 03 no es un único firmware monolítico ni un laboratorio exclusivamente TLS. Es una familia de pruebas MQTT que cubre MQTT plano, autenticación sin TLS, TLS, TLS con credenciales, mTLS, rechazo de certificado expirado y MQTT over WebSockets.

## Objetivos de aprendizaje

- Distinguir conectividad funcional de diseño seguro.
- Comparar MQTT plano, MQTT autenticado, MQTT sobre TLS, mTLS y MQTT over WebSockets.
- Evidenciar que usuario/password sin TLS no protege credenciales.
- Evidenciar que una conexión TLS solo es aceptable si valida correctamente el certificado del servidor.
- Mantener trazabilidad escenario → diseño → firmware → test → evidencia.

## Prerrequisitos

- ESP32-S3 compatible con ESP-IDF.
- Consola USB Serial/JTAG operativa para los sublaboratorios dry-run.
- Python 3 para herramientas de captura y gates.
- Acceso de red a `test.mosquitto.org` solo cuando se introduzcan conexiones reales.
- Ningún secreto real debe usarse en el broker público.

## Alcance

Esta carpeta define el contrato común de la familia LAB 03 y contiene sublaboratorios independientes:

```text
lab03_mqtt/
├── README.md
├── CHANGELOG.md
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

## Fuera de alcance

- Mezclar todos los escenarios en un único laboratorio ejecutable.
- Tratar `lab03_mqtt/` como firmware final único.
- Versionar secretos reales, claves privadas reales o credenciales operativas.
- Declarar conexión real validada cuando solo exista dry-run.

## Estructura

- `docs/`: contrato común, matriz, política de broker, certificados, riesgos y evidencias agregadas.
- `evidence/`: evidencias agregadas de la familia, especialmente gates estáticos.
- `tools/`: gates y herramientas agregadas de la familia.
- `common/`: componentes reutilizables, helpers y contratos compartidos.
- `lab03a...lab03g/`: sublaboratorios con README, CHANGELOG, docs, evidence, firmware, test y tools propios.

## Matriz contractual

| Sublab | Escenario | Puerto | TLS | Auth | Estado |
| --- | --- | ---: | --- | --- | --- |
| LAB 03A | M03-1883 | 1883 | No | No | CUMPLE dry-run |
| LAB 03B | M03-1884 | 1884 | No | Usuario/password | PENDIENTE |
| LAB 03C | M03-8883 / M03-8886 | 8883 / 8886 | Sí | No | PENDIENTE |
| LAB 03D | M03-8885 | 8885 | Sí | Usuario/password | PENDIENTE |
| LAB 03E | M03-8884 | 8884 | Sí | Certificado cliente | PENDIENTE |
| LAB 03F | M03-8887 | 8887 | Sí, expirado | No | PENDIENTE |
| LAB 03G | M03-8080/8081/8090/8091 | 8080/8081/8090/8091 | Mixto | Mixto | PENDIENTE |

## Arquitectura

La arquitectura se divide en dos niveles:

```text
Familia LAB 03
├── contrato común MQTT
├── matriz de escenarios
├── política de broker público
├── gates agregados
└── sublaboratorios independientes

Sublaboratorio LAB 03x
├── firmware propio o reutilización explícita
├── herramientas propias
├── test manual/automático
├── evidencia propia
└── estado CUMPLE/NO CUMPLE/NO VALIDADO/PENDIENTE
```

## Cómo trabajar

No continuar con un sublaboratorio si el anterior no tiene documentación, evidencias y gates alineados.

Para LAB 03A:

```powershell
cd labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/firmware
idf.py set-target esp32s3
idf.py build
```

Para gates agregados:

```powershell
python labs/lab03_mqtt/tools/run_static_gates.py
python labs/lab03_mqtt/tools/capture_static_gates.py
```

## Evidencias

- Evidencia agregada de familia: `evidence/lab03_static_gates.txt`.
- Evidencia LAB 03A: `lab03a_m03_1883_plain_no_auth/evidence/lab03_m03_1883_console.log`.
- Cada sublaboratorio futuro debe tener evidencia propia.

## Estado

```text
CUMPLE:
- LAB 03 queda modelado como familia MQTT, no como único laboratorio TLS.
- LAB 03A conserva la evidencia dry-run de M03-1883.
- La matriz completa queda trazada por sublaboratorios independientes.

NO CUMPLE:
- Los escenarios sin TLS no son diseños seguros para credenciales ni payloads sensibles.

NO VALIDADO:
- Conexión real contra test.mosquitto.org.
- TLS/mTLS/WebSockets reales.
- Build formal cero warnings con stdout completo si no se aporta evidencia específica.

PENDIENTE:
- Implementar LAB 03B en su propio subdirectorio.
- Completar TLS, mTLS, certificado expirado y WebSockets en sublaboratorios separados.
```
"""


def sublab_readme(slug: str, meta: dict[str, str]) -> str:
    implemented = slug.startswith("lab03a_")
    status_block = (
        """CUMPLE:\n- Firmware dry-run y evidencia de consola M03-1883 migrados desde la estructura anterior.\n- El escenario queda aislado como sublaboratorio independiente.\n\nNO CUMPLE:\n- MQTT TCP plano sin TLS no es seguro para datos sensibles.\n\nNO VALIDADO:\n- Conexión real al broker.\n- Build formal cero warnings si no existe evidencia adicional.\n\nPENDIENTE:\n- Mantener gates y documentación alineados tras la migración.\n"""
        if implemented
        else """CUMPLE:\n- El sublaboratorio queda reservado y trazado dentro de la matriz LAB 03.\n\nNO CUMPLE:\n- No existe todavía implementación ni evidencia propia.\n\nNO VALIDADO:\n- Firmware.\n- Captura de consola.\n- Conexión real.\n- Gates específicos del sublaboratorio.\n\nPENDIENTE:\n- Diseñar, implementar, documentar y evidenciar esta fase antes de marcarla como CUMPLE.\n"""
    )
    return f"""# {meta['title']}

**Estado:** {meta['status']}
**Escenario:** {meta['scenario']}
**Puerto:** {meta['port']}

## Índice

- [Objetivo](#objetivo)
- [Objetivos de aprendizaje](#objetivos-de-aprendizaje)
- [Prerrequisitos](#prerrequisitos)
- [Alcance](#alcance)
- [Fuera de alcance](#fuera-de-alcance)
- [Estructura](#estructura)
- [Evidencias](#evidencias)
- [Estado](#estado)

## Objetivo

{meta['objective']}

## Objetivos de aprendizaje

- Separar comportamiento funcional de clasificación de seguridad.
- Mantener logs parseables y sin secretos reales.
- Generar evidencias reproducibles del escenario.
- Conservar trazabilidad con la matriz contractual de `../docs/scenario_matrix.md`.

## Prerrequisitos

- Revisar el README de la familia `../README.md`.
- Mantener limpio el árbol de artefactos generados.
- No usar secretos reales contra `test.mosquitto.org`.

## Alcance

Este directorio contiene el contrato, la implementación y las evidencias propias del escenario `{meta['scenario']}`.

## Fuera de alcance

- Reutilizar evidencias de otro sublaboratorio como si fueran propias.
- Mezclar firmware o herramientas de escenarios distintos sin declaración explícita en `../common/`.
- Declarar conexión real validada si solo existe dry-run.

## Estructura

```text
{slug}/
├── README.md
├── CHANGELOG.md
├── docs/
├── evidence/
├── firmware/
├── test/
└── tools/
```

## Evidencias

Las evidencias de este sublaboratorio deben residir en `evidence/`.

## Estado

```text
{status_block.rstrip()}
```
"""


def sublab_changelog(slug: str, meta: dict[str, str]) -> str:
    return f"""# Changelog — {meta['title']}

## Índice

- [Unreleased](#unreleased)

## Unreleased

### Added

- Directorio independiente `{slug}` dentro de la familia LAB 03 MQTT.
- Contrato documental mínimo para el escenario `{meta['scenario']}`.

### Status

- Estado actual: `{meta['status']}`.
"""


def write_family_docs() -> None:
    write_text(FAMILY / "README.md", family_readme())
    write_text(
        FAMILY / "CHANGELOG.md",
        """# Changelog — LAB 03 MQTT

## Índice

- [Unreleased](#unreleased)

## Unreleased

### Changed

- LAB 03 deja de representarse como `lab03_mqtt` y pasa a `lab03_mqtt`.
- La matriz MQTT se reorganiza como familia de sublaboratorios independientes.
- LAB 03A conserva la evidencia dry-run de M03-1883 en su propio subdirectorio.

### Added

- Estructura `lab03a` a `lab03g` para cubrir todos los escenarios MQTT del broker de pruebas.
- Directorio `common/` para contratos y reutilización explícita entre sublaboratorios.

### Status

```text
CUMPLE:
- Reorganización estructural de LAB 03 como familia MQTT.
- LAB 03A queda aislado como sublaboratorio.

NO VALIDADO:
- Gates locales tras aplicar la migración, hasta ejecutar las herramientas.
```
""",
    )
    write_text(
        FAMILY / "common" / "README.md",
        """# Common — LAB 03 MQTT

## Índice

- [Objetivo](#objetivo)
- [Reglas](#reglas)
- [Estado](#estado)

## Objetivo

Contener componentes reutilizables, contratos de logs, utilidades y políticas compartidas por los sublaboratorios LAB 03A–LAB 03G.

## Reglas

- `common/` no puede ocultar el estado de un sublaboratorio.
- Toda reutilización debe ser explícita y trazable.
- Ningún secreto real debe almacenarse aquí.

## Estado

```text
CUMPLE:
- Directorio común creado como frontera explícita de reutilización.

PENDIENTE:
- Extraer componentes compartidos solo cuando exista una segunda necesidad real.
```
""",
    )
    write_text(
        FAMILY / "docs" / "family_structure.md",
        """# Estructura de la familia LAB 03 MQTT

## Índice

- [Propósito](#propósito)
- [Árbol contractual](#árbol-contractual)
- [Reglas](#reglas)
- [Estado](#estado)

## Propósito

Documentar la decisión arquitectónica de convertir LAB 03 en una familia MQTT con sublaboratorios independientes.

## Árbol contractual

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

## Reglas

- Cada sublaboratorio tiene `README.md`, `CHANGELOG.md`, `docs/`, `evidence/`, `firmware/`, `test/` y `tools/`.
- La familia mantiene matriz, políticas y gates agregados.
- Los sublaboratorios mantienen evidencias propias.

## Estado

```text
CUMPLE:
- Estructura contractual definida.
```
""",
    )
    write_text(
        FAMILY / "evidence" / "README.md",
        """# Evidencias — LAB 03 MQTT

## Índice

- [Evidencias agregadas](#evidencias-agregadas)
- [Evidencias por sublaboratorio](#evidencias-por-sublaboratorio)
- [Estado](#estado)

## Evidencias agregadas

| Evidencia | Estado | Descripción |
| --- | --- | --- |
| `lab03_static_gates.txt` | CUMPLE si termina en `capture_validation result=PASS` | Gate global + gate familia LAB 03 |

## Evidencias por sublaboratorio

| Sublab | Evidencia | Estado |
| --- | --- | --- |
| LAB 03A | `../lab03a_m03_1883_plain_no_auth/evidence/lab03_m03_1883_console.log` | CUMPLE si termina en PASS |
| LAB 03B | evidencia propia futura | PENDIENTE |
| LAB 03C | evidencia propia futura | PENDIENTE |
| LAB 03D | evidencia propia futura | PENDIENTE |
| LAB 03E | evidencia propia futura | PENDIENTE |
| LAB 03F | evidencia propia futura | PENDIENTE |
| LAB 03G | evidencia propia futura | PENDIENTE |

## Estado

```text
CUMPLE:
- Evidencias agregadas separadas de evidencias de escenario.

PENDIENTE:
- Regenerar lab03_static_gates.txt tras la migración estructural.
```
""",
    )


def write_sublab_docs() -> None:
    for slug, meta in SUBLABS.items():
        sublab = FAMILY / slug
        write_text(sublab / "README.md", sublab_readme(slug, meta))
        write_text(sublab / "CHANGELOG.md", sublab_changelog(slug, meta))
        write_text(
            sublab / "docs" / "audit_evidence.md",
            f"""# Evidencias de auditoría — {meta['title']}

## Índice

- [Objetivo](#objetivo)
- [Evidencias](#evidencias)
- [Estado](#estado)

## Objetivo

Trazar las evidencias propias del escenario `{meta['scenario']}`.

## Evidencias

- Directorio de evidencias: `../evidence/`.
- No se aceptan evidencias prestadas de otro sublaboratorio.

## Estado

```text
CUMPLE:
- Documento de evidencias creado para el sublaboratorio.

NO VALIDADO:
- Ejecutar validaciones locales tras la migración.
```
""",
        )
        write_text(
            sublab / "docs" / "test_plan.md",
            f"""# Plan de pruebas — {meta['title']}

## Índice

- [Objetivo](#objetivo)
- [Pruebas mínimas](#pruebas-mínimas)
- [Estado](#estado)

## Objetivo

Definir el plan de pruebas del escenario `{meta['scenario']}`.

## Pruebas mínimas

- Comprobar que el firmware o dry-run corresponde al escenario correcto.
- Capturar logs parseables y sin secretos reales.
- Validar la clasificación de seguridad del escenario.
- Ejecutar gates antes del cierre.

## Estado

```text
PENDIENTE:
- Completar pruebas específicas del sublaboratorio cuando se implemente o se revalide.
```
""",
        )
        write_text(
            sublab / "evidence" / "README.md",
            f"""# Evidence — {meta['title']}

## Índice

- [Contenido](#contenido)
- [Estado](#estado)

## Contenido

Evidencias propias del escenario `{meta['scenario']}`.

## Estado

```text
{('CUMPLE:\n- LAB 03A conserva aquí la captura M03-1883 si el fichero fue migrado.\n\nPENDIENTE:\n- Regenerar evidencia si cambian rutas o comandos.' if slug.startswith('lab03a_') else 'PENDIENTE:\n- Sin evidencias propias todavía.')}
```
""",
        )
        for folder in ["firmware", "test", "tools"]:
            keep = sublab / folder / ".gitkeep"
            if not any((sublab / folder).iterdir()):
                write_text(keep, "")


def write_family_gates() -> None:
    write_text(
        FAMILY / "tools" / "run_static_gates.py",
        r'''#!/usr/bin/env python3
"""Gate estático agregado para la familia LAB 03 MQTT."""

from __future__ import annotations

import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_ROOT.parents[1]

REQUIRED_SUBLABS = [
    "lab03a_m03_1883_plain_no_auth",
    "lab03b_m03_1884_plain_auth",
    "lab03c_m03_8883_8886_tls_server_auth",
    "lab03d_m03_8885_tls_userpass",
    "lab03e_m03_8884_mtls_client_cert",
    "lab03f_m03_8887_expired_cert_rejection",
    "lab03g_m03_websockets",
]

REQUIRED_MARKDOWN_SECTIONS = ["## Índice", "## Objetivo", "## Estado"]
FORBIDDEN_GENERATED = ["build", "sdkconfig", "sdkconfig.old"]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def require(path: Path) -> None:
    if not path.exists():
        fail(f"missing required path: {path.relative_to(REPO_ROOT)}")


def require_sections(path: Path, sections: list[str] = REQUIRED_MARKDOWN_SECTIONS) -> None:
    text = path.read_text(encoding="utf-8")
    for section in sections:
        if section not in text:
            fail(f"{path.relative_to(REPO_ROOT)} missing section: {section}")


def main() -> int:
    if (REPO_ROOT / "labs" / "lab03_mqtt").exists():
        fail("legacy directory still present: labs/lab03_mqtt")

    require(LAB_ROOT / "README.md")
    require(LAB_ROOT / "CHANGELOG.md")
    require(LAB_ROOT / "docs" / "scenario_matrix.md")
    require(LAB_ROOT / "docs" / "family_structure.md")
    require(LAB_ROOT / "evidence" / "README.md")
    require(LAB_ROOT / "common" / "README.md")

    require_sections(LAB_ROOT / "README.md", ["## Índice", "## Objetivo", "## Matriz contractual", "## Estado"])
    require_sections(LAB_ROOT / "CHANGELOG.md")
    require_sections(LAB_ROOT / "evidence" / "README.md")

    for slug in REQUIRED_SUBLABS:
        sublab = LAB_ROOT / slug
        require(sublab)
        for child in ["README.md", "CHANGELOG.md", "docs", "evidence", "firmware", "test", "tools"]:
            require(sublab / child)
        require_sections(sublab / "README.md", ["## Índice", "## Objetivo", "## Alcance", "## Estado"])
        require_sections(sublab / "CHANGELOG.md")
        require_sections(sublab / "evidence" / "README.md")

    require(LAB_ROOT / "lab03a_m03_1883_plain_no_auth" / "firmware")
    require(LAB_ROOT / "lab03a_m03_1883_plain_no_auth" / "evidence" / "lab03_m03_1883_console.log")

    for generated in FORBIDDEN_GENERATED:
        for path in LAB_ROOT.rglob(generated):
            fail(f"forbidden generated artifact present: {path.relative_to(REPO_ROOT)}")

    print("PASS: LAB 03 MQTT family static gates completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )
    write_text(
        FAMILY / "tools" / "capture_static_gates.py",
        r'''#!/usr/bin/env python3
"""Captura evidencia de gates estáticos de la familia LAB 03 MQTT."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_ROOT.parents[1]
OUTPUT = LAB_ROOT / "evidence" / "lab03_static_gates.txt"


def run(cmd: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    commands = [
        [sys.executable, "tools/repo_quality_gates/run_static_repo_gates.py"],
        [sys.executable, "labs/lab03_mqtt/tools/run_static_gates.py"],
    ]
    lines: list[str] = ["# LAB 03 MQTT static gates evidence", ""]
    ok = True
    for cmd in commands:
        lines.append(f"$ {' '.join(cmd)}")
        rc, out = run(cmd)
        lines.append(out.rstrip())
        lines.append(f"# returncode={rc}")
        lines.append("")
        ok = ok and rc == 0

    lines.append(f"# capture_validation result={'PASS' if ok else 'FAIL'}")
    OUTPUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"{'PASS' if ok else 'FAIL'}: static gates evidence written to {OUTPUT}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
''',
    )


def update_book_chapter() -> None:
    old = ROOT / "book" / "chapters" / "03_matriz_mqtt.md"
    new = ROOT / "book" / "chapters" / "03_matriz_mqtt.md"
    move_path(old, new)
    if not new.exists():
        write_text(
            new,
            """# Capítulo 03 — Matriz MQTT contra test.mosquitto.org

## Índice

- [Propósito](#propósito)
- [Estructura](#estructura)
- [Estado](#estado)

## Propósito

Este capítulo acompaña a la familia `labs/lab03_mqtt/` y documenta la progresión desde MQTT plano hasta TLS, mTLS y WebSockets.

## Estructura

LAB 03 se divide en sublaboratorios LAB 03A–LAB 03G para evitar que una matriz completa de escenarios quede empaquetada como un único laboratorio TLS.

## Estado

```text
CUMPLE:
- LAB 03A queda definido como baseline dry-run.

PENDIENTE:
- Redactar el contenido completo de LAB 03B–LAB 03G conforme se implementen.
```
""",
        )
    else:
        text = read_text(new)
        text = text.replace("MQTT TLS", "Matriz MQTT")
        text = text.replace("lab03_mqtt", "lab03_mqtt")
        if "## Estructura por sublaboratorios" not in text:
            text += """

## Estructura por sublaboratorios

LAB 03 se organiza como familia `labs/lab03_mqtt/` con sublaboratorios independientes LAB 03A–LAB 03G. Esta estructura evita presentar como TLS escenarios que son deliberadamente MQTT plano.
"""
        write_text(new, text)


def update_root_level_docs() -> None:
    replace_all("lab03_mqtt", "lab03_mqtt")
    replace_all("LAB 03 — Matriz MQTT", "LAB 03 — Matriz MQTT")
    replace_all("03_matriz_mqtt.md", "03_matriz_mqtt.md")
    replace_all("labs\\lab03_mqtt\\firmware", "labs\\lab03_mqtt\\lab03a_m03_1883_plain_no_auth\\firmware")
    replace_all("labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/firmware", "labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/firmware")
    replace_all("labs\\lab03_mqtt\\tools\\capture_console_evidence.py", "labs\\lab03_mqtt\\lab03a_m03_1883_plain_no_auth\\tools\\capture_console_evidence.py")
    replace_all("labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/tools/capture_console_evidence.py", "labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/tools/capture_console_evidence.py")
    replace_all("labs\\lab03_mqtt\\evidence\\lab03_m03_1883_console.log", "labs\\lab03_mqtt\\lab03a_m03_1883_plain_no_auth\\evidence\\lab03_m03_1883_console.log")
    replace_all("labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/evidence/lab03_m03_1883_console.log", "labs/lab03_mqtt/lab03a_m03_1883_plain_no_auth/evidence/lab03_m03_1883_console.log")

    write_text(
        ROOT / "docs" / "repository_tree.md",
        """# Árbol contractual del repositorio

## Índice

- [Propósito](#propósito)
- [Árbol principal](#árbol-principal)
- [Detalle LAB 03](#detalle-lab-03)
- [Estado](#estado)

## Propósito

Este documento fija el árbol documental mínimo del repositorio. El árbol no es decorativo: forma parte del contrato audit-grade del proyecto.

## Árbol principal

```text
secure-embedded-labs/
├── .github/
├── book/
│   ├── chapters/
│   ├── figures/
│   └── references/
├── docs/
├── labs/
│   ├── _template/
│   ├── lab01_insecure_vs_hardened/
│   ├── lab02_device_identity/
│   ├── lab03_mqtt/
│   └── lab04...lab10/
├── standard/
└── tools/
```

## Detalle LAB 03

```text
labs/lab03_mqtt/
├── README.md
├── CHANGELOG.md
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
- LAB 03 se representa como familia MQTT con sublaboratorios independientes.

PENDIENTE:
- Mantener este árbol actualizado en cada parche estructural.
```
""",
    )

    append_once(
        ROOT / "CHANGELOG.md",
        "LAB 03 MQTT family restructure",
        """## LAB 03 MQTT family restructure

### Changed

- `labs/lab03_mqtt` pasa a `labs/lab03_mqtt`.
- LAB 03 queda organizado como familia de sublaboratorios LAB 03A–LAB 03G.
- LAB 03A conserva la evidencia dry-run M03-1883 en su propio subdirectorio.

### Status

```text
CUMPLE:
- Estructura corregida antes de continuar con LAB 03B.
```
""",
    )

    append_once(
        ROOT / "ROADMAP.md",
        "LAB 03 — Familia MQTT contra test.mosquitto.org",
        """## LAB 03 — Familia MQTT contra test.mosquitto.org

```text
CUMPLE:
- LAB 03A — M03-1883 / MQTT TCP plano sin TLS y sin autenticación / dry-run.

PENDIENTE:
- LAB 03B — M03-1884 / MQTT TCP plano con usuario/password.
- LAB 03C — M03-8883/M03-8886 / TLS servidor.
- LAB 03D — M03-8885 / TLS + usuario/password.
- LAB 03E — M03-8884 / mTLS.
- LAB 03F — M03-8887 / certificado expirado.
- LAB 03G — MQTT over WebSockets.
```
""",
    )

    append_once(
        ROOT / "docs" / "publishing_model.md",
        "Cierre transversal LAB 03 MQTT",
        """## Cierre transversal LAB 03 MQTT

Cada sublaboratorio de `labs/lab03_mqtt/` debe actualizar, como mínimo, su README, CHANGELOG, evidencias, documentación del libro, ROADMAP y changelog global antes de considerarse cerrado.
""",
    )


def update_labs_readme() -> None:
    write_text(
        LABS / "README.md",
        """# Laboratorios

## Índice

- [Propósito](#propósito)
- [Árbol](#árbol)
- [Estado](#estado)

## Propósito

Agrupar laboratorios reproducibles de ciberseguridad embebida con evidencias auditables.

## Árbol

```text
labs/
├── _template/
├── lab01_insecure_vs_hardened/
├── lab02_device_identity/
├── lab03_mqtt/
│   ├── common/
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
- LAB 01 cerrado para el alcance actual.
- LAB 02 cerrado para el alcance actual.
- LAB 03A cerrado como dry-run dentro de la familia MQTT.

PENDIENTE:
- LAB 03B y siguientes sublaboratorios MQTT.
```
""",
    )


def migrate() -> None:
    if not LABS.exists():
        raise SystemExit("FAIL: no se encuentra el directorio labs/; ejecutar desde el repo correcto")

    migrate_root_directory()
    split_lab03a()
    write_family_docs()
    write_sublab_docs()
    write_family_gates()
    update_book_chapter()
    update_root_level_docs()
    update_labs_readme()
    remove_generated_artifacts(FAMILY)

    # Última pasada para referencias antiguas que hayan quedado en ficheros generados o movidos.
    replace_all("lab03_mqtt", "lab03_mqtt")
    replace_all("03_matriz_mqtt.md", "03_matriz_mqtt.md")

    print("PASS: LAB 03 migrado a familia labs/lab03_mqtt con sublaboratorios independientes")
    print("NEXT: ejecutar gates y revisar git diff antes de continuar con LAB 03B")


if __name__ == "__main__":
    migrate()
