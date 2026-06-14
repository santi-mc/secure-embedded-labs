#!/usr/bin/env python3
"""Static QA gates for secure_iot_lab01_esp32s3.

These checks do not replace `idf.py build`; they only validate repository hygiene
and source-level invariants that can be checked without ESP-IDF.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
ROOT = LAB_ROOT / "firmware"
VERSION = "0.1.0"

FORBIDDEN_PATHS = [
    "build",
    "sdkconfig",
    "sdkconfig.old",
    "dependencies.lock",
    "managed_components",
]

FORBIDDEN_SOURCE_PATTERNS = [
    "esp_flash_encryption_enabled(",
    "driver/uart.h",
    "uart_read_bytes(",
    "UART_NUM_0",
]

REQUIRED_FILES = [
    "../README.md",
    "../CHANGELOG.md",
    "../COMMIT_MESSAGE.txt",
    "../docs/architecture.md",
    "../docs/security_requirements.md",
    "../docs/threat_model.md",
    "../docs/test_plan.md",
    "../docs/audit_evidence.md",
    "../docs/known_limitations.md",
    "../docs/hardening_policy.md",

    "../tools/capture_console_evidence.py",
    "../tools/capture_console_evidence.ps1",
    "../tools/capture_static_gates.py",
    "../tools/capture_secret_scan.py",
    "../tools/apply_lab01_auto_evidence_docs_update.py",
    "../evidence/README.md",]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def display_path(path: Path) -> str:
    """Return a stable path for diagnostics from either lab or firmware roots."""
    try:
        return str(path.relative_to(LAB_ROOT))
    except ValueError:
        return str(path)


def check_required_files() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"required file missing: {rel}")


def check_forbidden_paths() -> None:
    for rel in FORBIDDEN_PATHS:
        if (ROOT / rel).exists():
            fail(f"forbidden generated artefact present: {rel}")


def source_files() -> list[Path]:
    suffixes = {".cpp", ".hpp", ".h", ".c", ".cmake", ".txt"}
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix in suffixes:
            if "build" not in path.parts:
                files.append(path)
    return files


def check_forbidden_source_patterns() -> None:
    for path in source_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for pattern in FORBIDDEN_SOURCE_PATTERNS:
            if pattern in text:
                fail(f"forbidden source pattern '{pattern}' found in {display_path(path)}")


def check_version_consistency() -> None:
    paths = [LAB_ROOT / "README.md", LAB_ROOT / "CHANGELOG.md", ROOT / "components/lab01_domain/include/lab01_domain/version.hpp"]
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        if VERSION not in text:
            fail(f"version {VERSION} not found in {display_path(path)}")


def check_docs_state_blocks() -> None:
    readme = (LAB_ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    for marker in ["CUMPLE:", "NO CUMPLE:", "NO VALIDADO:"]:
        if marker not in readme:
            fail(f"README.md missing state marker: {marker}")


def check_cmake_werror() -> None:
    cmake_files = [p for p in ROOT.rglob("CMakeLists.txt") if p.parent.name != "lab01_domain"]
    for path in cmake_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        if "idf_component_register" not in text:
            continue
        if "-Werror" not in text:
            fail(f"-Werror missing in {display_path(path)}")


def main() -> int:
    check_required_files()
    check_forbidden_paths()
    check_forbidden_source_patterns()
    check_version_consistency()
    check_docs_state_blocks()
    check_cmake_werror()
    print("PASS: LAB 01 static gates completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
