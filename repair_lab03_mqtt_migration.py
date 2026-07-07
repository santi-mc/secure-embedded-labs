#!/usr/bin/env python3
"""Repair LAB 03 MQTT family migration.

Run from the repository root:
    python repair_lab03_mqtt_migration.py

Scope:
- Keeps LAB 03 as labs/lab03_mqtt.
- Removes the legacy labs/lab03_mqtt_tls directory if it still exists.
- Normalizes README contracts for LAB 03 family/sub-labs.
- Ensures Markdown files under LAB 03 have an index.
- Rewrites the LAB 03 family static gate so CHANGELOG.md is not treated as README.md.
- Updates the global gate path from lab03_mqtt_tls to lab03_mqtt if needed.
- Removes temporary repair scripts created during the migration attempt.
"""

from __future__ import annotations

import re
import shutil
import sys
import unicodedata
from pathlib import Path

ROOT = Path.cwd().resolve()
LAB03 = ROOT / "labs" / "lab03_mqtt"
LEGACY_LAB03 = ROOT / "labs" / "lab03_mqtt_tls"
LAB03_GATE = LAB03 / "tools" / "run_static_gates.py"
GLOBAL_GATE = ROOT / "tools" / "repo_quality_gates" / "run_static_repo_gates.py"

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
    "lab03a_m03_1883_plain_no_auth",
    "lab03b_m03_1884_plain_auth",
    "lab03c_m03_8883_8886_tls_server_auth",
    "lab03d_m03_8885_tls_userpass",
    "lab03e_m03_8884_mtls_client_cert",
    "lab03f_m03_8887_expired_cert_rejection",
    "lab03g_m03_websockets",
]

REQUIRED_DIRS = ["common", "docs", "evidence", "tools", *SUBLABS]

DEFAULT_SECTION_BODY = {
    "## Objetivo": """Definir y validar el escenario de seguridad embebida cubierto por este laboratorio, manteniendo separación entre funcionalidad, riesgo, mitigación y evidencia.""",
    "## Objetivos de aprendizaje": """- Entender el riesgo de seguridad tratado por el laboratorio.
- Distinguir entre comportamiento funcional y cumplimiento de seguridad.
- Generar evidencias reproducibles antes de declarar cierre.""",
    "## Prerrequisitos": """- Repositorio limpio de artefactos generados.
- Python 3 disponible.
- ESP-IDF disponible cuando el laboratorio incluya firmware.
- Lectura previa de la documentación raíz y del roadmap.""",
    "## Alcance": """Este documento cubre el alcance documental y técnico del laboratorio dentro del repositorio `secure-embedded-labs`.

El cierre requiere documentación, evidencias y gates en PASS.""",
    "## Fuera de alcance": """- Uso de secretos reales.
- Declarar producción sin evidencia.
- Conexiones reales no documentadas.
- Omitir gates globales o específicos.""",
    "## Hardware requerido": """- Placa ESP32-S3 compatible.
- Cable USB para alimentación, flasheo y consola.
- Para fases dry-run no se requiere conectividad Wi-Fi real.""",
    "## Software requerido": """- Git.
- Python 3.
- ESP-IDF compatible con ESP32-S3.
- PowerShell o terminal equivalente.
- Herramientas del repositorio bajo `tools/`.""",
    "## Arquitectura prevista": """La arquitectura prevista separa documentación, firmware, pruebas, herramientas y evidencias.

En LAB 03, `lab03_mqtt/` actúa como familia MQTT y cada sublaboratorio `lab03a`...`lab03g` debe cerrarse de forma independiente.""",
    "## Modelo temporal": """Las fases dry-run usan interacción por consola y no ejecutan tareas de red reales.

Cuando se introduzca conexión real, cada tarea, timeout, retry y deadline deberá quedar documentado en el sublaboratorio correspondiente.""",
    "## Threat model": """El threat model mínimo considera:

- exposición de credenciales;
- ausencia de confidencialidad;
- validación incorrecta de certificados;
- uso de broker público;
- publicación accidental de secretos;
- confusión entre autenticación y cifrado.""",
    "## Requisitos": """- Logs sin secretos.
- Evidencias reproducibles.
- Gates globales y específicos en PASS.
- Separación clara entre dry-run y conexión real.
- Estado explícito `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` y `PENDIENTE`.""",
    "## Cómo compilar": """Cuando el sublaboratorio incluya firmware:

```powershell
cd labs\\lab03_mqtt\\lab03a_m03_1883_plain_no_auth\\firmware
idf.py set-target esp32s3
idf.py build
```

La ruta debe ajustarse al sublaboratorio correspondiente.""",
    "## Cómo flashear": """Cuando el sublaboratorio incluya firmware:

```powershell
idf.py -p COMx flash monitor
```

Debe sustituirse `COMx` por el puerto real.""",
    "## Cómo probar": """Ejecutar primero gates directos:

```powershell
python tools\\repo_quality_gates\\run_static_repo_gates.py
python labs\\lab03_mqtt\\tools\\run_static_gates.py
```

Después capturar evidencia estática cuando aplique.""",
    "## Evidencias esperadas": """- Evidencia de consola cuando aplique.
- Evidencia de gates estáticos.
- Evidencia de build si se declara compilación validada.
- Evidencia de conexión real solo cuando exista prueba de red documentada.""",
    "## Errores comunes": """- Confundir autenticación con confidencialidad.
- Declarar seguro un escenario sin TLS.
- Versionar `build/`, `sdkconfig` o `sdkconfig.old`.
- Reutilizar evidencias de otro laboratorio.
- Mantener rutas legacy tras una migración.""",
    "## Ejercicios": """- Identificar qué activo protege cada mitigación.
- Clasificar el escenario como funcional, inseguro, mitigado o no validado.
- Revisar si los logs contienen secretos.""",
    "## Preguntas de repaso": """- ¿Qué diferencia hay entre autenticación y cifrado?
- ¿Qué evidencia demuestra que el escenario fue probado?
- ¿Qué condición impide declarar `CUMPLE`?
- ¿Qué parte queda fuera de alcance en dry-run?""",
    "## Fuentes": """- Documentación del repositorio.
- Documentación oficial de ESP-IDF cuando aplique.
- Documentación pública de `test.mosquitto.org` para LAB 03.
- Estándar interno audit-grade del proyecto.""",
    "## Estado": """```text
CUMPLE:
- Documento alineado con contrato mínimo del repositorio.

NO VALIDADO:
- Gates tras cada modificación.

PENDIENTE:
- Actualizar este estado con la evidencia real del laboratorio o sublaboratorio.
```""",
}

FAMILY_OVERRIDES = {
    "## Objetivo": """Organizar LAB 03 como una familia de sublaboratorios MQTT contra `test.mosquitto.org`, separando MQTT plano, autenticación, TLS, mTLS, certificado expirado y WebSockets.""",
    "## Objetivos de aprendizaje": """- Construir una matriz MQTT audit-grade contra `test.mosquitto.org`.
- Separar MQTT plano, autenticación, TLS, mTLS, certificados expirados y WebSockets.
- Evitar mezclar autenticación, confidencialidad y validación de certificados.
- Mantener cada escenario como sublaboratorio auditable de forma independiente.""",
    "## Arquitectura prevista": """LAB 03 se estructura como familia MQTT:

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

La carpeta superior contiene contrato común, documentación de matriz, gates agregados y evidencias transversales. Cada sublaboratorio mantiene su propio cierre documental y técnico.""",
    "## Estado": """```text
CUMPLE:
- LAB 03 queda modelado como familia MQTT.
- LAB 03A queda aislado como sublaboratorio para M03-1883.

NO VALIDADO:
- LAB 03B y posteriores no están cerrados.
- Conexión MQTT real todavía no forma parte del cierre dry-run.

PENDIENTE:
- Pasar gates tras la migración.
- Capturar evidencia estática.
- Continuar posteriormente con LAB 03B.
```""",
}

LAB03_GATE_TEXT = '''from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAB03 = ROOT / "labs" / "lab03_mqtt"
LEGACY = ROOT / "labs" / "lab03_mqtt_tls"

REQUIRED_DIRS = [
    "common",
    "docs",
    "evidence",
    "tools",
    "lab03a_m03_1883_plain_no_auth",
    "lab03b_m03_1884_plain_auth",
    "lab03c_m03_8883_8886_tls_server_auth",
    "lab03d_m03_8885_tls_userpass",
    "lab03e_m03_8884_mtls_client_cert",
    "lab03f_m03_8887_expired_cert_rejection",
    "lab03g_m03_websockets",
]

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


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")


def require_dir(path: Path) -> None:
    if not path.is_dir():
        fail(f"missing directory: {path.relative_to(ROOT)}")


def check_readme(path: Path) -> None:
    require_file(path)
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_LAB_README_SECTIONS:
        if section not in text:
            fail(f"{path.relative_to(ROOT)} missing section: {section}")


def check_markdown_indexes() -> None:
    for md in LAB03.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if "## Índice" not in text:
            fail(f"Markdown without index: {md.relative_to(ROOT)}")


def main() -> int:
    if LEGACY.exists():
        fail("legacy directory still present: labs/lab03_mqtt_tls")

    require_dir(LAB03)
    check_readme(LAB03 / "README.md")
    require_file(LAB03 / "CHANGELOG.md")

    for rel in REQUIRED_DIRS:
        require_dir(LAB03 / rel)

    for sublab in sorted(LAB03.glob("lab03*_m03_*")):
        check_readme(sublab / "README.md")

    check_markdown_indexes()

    print("PASS: LAB 03 static gates completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

TEMP_FILES = [
    ROOT / "fix_lab03_mqtt_migration_contract.ps1",
    ROOT / "tools" / "maintenance" / "fix_lab03_mqtt_family_gates.py",
    ROOT / "tools" / "maintenance" / "normalize_lab03_mqtt_migration_contract.py",
    ROOT / "tools" / "maintenance" / "normalize_lab03_readme_contract_from_gate.py",
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def normalize_newlines(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.splitlines()) + "\n"


def slug(title: str) -> str:
    value = title.strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^\w\s-]", "", value)
    value = re.sub(r"\s+", "-", value.strip())
    return value


def ensure_section(text: str, section: str, body: str) -> str:
    if re.search(rf"^{re.escape(section)}\s*$", text, flags=re.MULTILINE):
        return text
    if not text.endswith("\n"):
        text += "\n"
    return text + f"\n{section}\n\n{body.rstrip()}\n"


def rebuild_index(text: str) -> str:
    headings = [
        h.strip()
        for h in re.findall(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE)
        if h.strip() != "Índice"
    ]

    index = "## Índice\n\n"
    if headings:
        index += "\n".join(f"- [{h}](#{slug(h)})" for h in headings) + "\n"
    else:
        index += "- [Estado](#estado)\n"
        if "## Estado" not in text:
            text += "\n## Estado\n\nPendiente de completar.\n"

    pattern = re.compile(r"^## Índice\s*\n.*?(?=^## |\Z)", flags=re.MULTILINE | re.DOTALL)
    if pattern.search(text):
        return pattern.sub(index + "\n", text)

    lines = text.splitlines()
    insert_at = 1
    while insert_at < len(lines) and (lines[insert_at].startswith("**") or lines[insert_at].strip() == ""):
        insert_at += 1
    lines = lines[:insert_at] + ["", index.rstrip(), ""] + lines[insert_at:]
    return "\n".join(lines) + "\n"


def fix_readme(path: Path, *, family: bool = False) -> None:
    if not path.is_file():
        raise SystemExit(f"FAIL: README missing: {rel(path)}")

    text = path.read_text(encoding="utf-8")
    original = text

    for section in REQUIRED_LAB_README_SECTIONS:
        if section == "## Índice":
            continue
        body = FAMILY_OVERRIDES.get(section, DEFAULT_SECTION_BODY.get(section, "Pendiente de completar.")) if family else DEFAULT_SECTION_BODY.get(section, "Pendiente de completar.")
        text = ensure_section(text, section, body)

    text = rebuild_index(text)
    text = normalize_newlines(text)
    path.write_text(text, encoding="utf-8", newline="\n")

    if text != original:
        print(f"fixed README: {rel(path)}")
    else:
        print(f"unchanged README: {rel(path)}")


def ensure_markdown_index(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    original = text
    if "## Índice" not in text:
        text = rebuild_index(text)
    text = normalize_newlines(text)
    path.write_text(text, encoding="utf-8", newline="\n")
    if text != original:
        print(f"fixed markdown index: {rel(path)}")


def fix_global_gate_route() -> None:
    if not GLOBAL_GATE.is_file():
        print(f"skip missing global gate: {rel(GLOBAL_GATE)}")
        return
    text = GLOBAL_GATE.read_text(encoding="utf-8")
    fixed = text.replace("lab03_mqtt_tls", "lab03_mqtt")
    fixed = normalize_newlines(fixed)
    GLOBAL_GATE.write_text(fixed, encoding="utf-8", newline="\n")
    if fixed != text:
        print(f"fixed global gate route: {rel(GLOBAL_GATE)}")
    else:
        print(f"unchanged global gate route: {rel(GLOBAL_GATE)}")


def write_lab03_gate() -> None:
    LAB03_GATE.parent.mkdir(parents=True, exist_ok=True)
    LAB03_GATE.write_text(LAB03_GATE_TEXT, encoding="utf-8", newline="\n")
    print(f"rewrote LAB 03 gate: {rel(LAB03_GATE)}")


def remove_temp_files() -> None:
    for path in TEMP_FILES:
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
            print(f"removed temporary file: {rel(path)}")


def main() -> int:
    if not LAB03.is_dir():
        raise SystemExit("FAIL: labs/lab03_mqtt does not exist. Run the LAB 03 migration first.")

    if LEGACY_LAB03.exists():
        shutil.rmtree(LEGACY_LAB03)
        print(f"removed legacy directory: {rel(LEGACY_LAB03)}")
    else:
        print(f"legacy directory absent: {rel(LEGACY_LAB03)}")

    for directory in REQUIRED_DIRS:
        target = LAB03 / directory
        target.mkdir(parents=True, exist_ok=True)
        print(f"ensured directory: {rel(target)}")

    remove_temp_files()
    fix_global_gate_route()
    write_lab03_gate()

    fix_readme(LAB03 / "README.md", family=True)
    for sublab_name in SUBLABS:
        sublab_readme = LAB03 / sublab_name / "README.md"
        if not sublab_readme.exists():
            sublab_readme.write_text(f"# {sublab_name}\n", encoding="utf-8", newline="\n")
            print(f"created README: {rel(sublab_readme)}")
        fix_readme(sublab_readme)

    for md in LAB03.rglob("*.md"):
        ensure_markdown_index(md)

    print("PASS: LAB 03 MQTT migration repair completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
