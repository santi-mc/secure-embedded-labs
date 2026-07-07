#!/usr/bin/env python3
"""Static gates for LAB 03 MQTT family."""
from __future__ import annotations

from pathlib import Path
import sys

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
    print(f"FAIL: {message}")
    raise SystemExit(1)


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

    for name in [
        "lab03a_m03_1883_plain_no_auth",
        "lab03b_m03_1884_plain_auth",
        "lab03c_m03_8883_8886_tls_server_auth",
        "lab03d_m03_8885_tls_userpass",
        "lab03e_m03_8884_mtls_client_cert",
        "lab03f_m03_8887_expired_cert_rejection",
        "lab03g_m03_websockets",
    ]:
        check_readme(LAB03 / name / "README.md")
        require_file(LAB03 / name / "CHANGELOG.md")

    check_markdown_indexes()
    print("PASS: LAB 03 static gates completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
