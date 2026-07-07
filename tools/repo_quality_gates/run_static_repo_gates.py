#!/usr/bin/env python3
"""Static repository gates for Secure Embedded Labs.

These gates validate repository structure and documentation contracts.
Firmware build gates must be executed inside each lab when firmware exists.
"""

from __future__ import annotations

import sys
from pathlib import Path

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

FORBIDDEN_PATH_PARTS = {
    "build",
    "managed_components",
    ".pytest_cache",
    "__pycache__",
}

FORBIDDEN_FILES = {
    "sdkconfig",
    "sdkconfig.old",
    "dependencies.lock",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def check_required_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"required file missing: {rel}")


def check_lab_readmes() -> None:
    for lab in LAB_DIRS:
        readme = ROOT / "labs" / lab / "README.md"
        if not readme.is_file():
            fail(f"lab README missing: {readme.relative_to(ROOT)}")

        text = readme.read_text(encoding="utf-8")
        for section in REQUIRED_LAB_README_SECTIONS:
            if section not in text:
                fail(f"{readme.relative_to(ROOT)} missing section: {section}")


def check_forbidden_artifacts() -> None:
    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue

        rel_parts = set(path.relative_to(ROOT).parts)
        if rel_parts & FORBIDDEN_PATH_PARTS:
            fail(f"forbidden generated directory present: {path.relative_to(ROOT)}")

        if path.name in FORBIDDEN_FILES:
            fail(f"forbidden generated/config file present: {path.relative_to(ROOT)}")


def check_markdown_indices() -> None:
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts:
            continue

        text = md.read_text(encoding="utf-8")
        if "## Índice" not in text and md.name.upper() != "LICENSE.md":
            fail(f"Markdown without index: {md.relative_to(ROOT)}")


def main() -> int:
    check_required_files()
    check_lab_readmes()
    check_forbidden_artifacts()
    check_markdown_indices()

    print("PASS: static repository gates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
