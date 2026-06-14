#!/usr/bin/env python3
"""Static gates for LAB 02.

These gates do not replace ESP-IDF build or hardware validation.
"""
from __future__ import annotations

from pathlib import Path
import sys

LAB_ROOT = Path(__file__).resolve().parents[1]
FW_ROOT = LAB_ROOT / "firmware"

REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "COMMIT_MESSAGE.txt",
    "docs/architecture.md",
    "docs/audit_evidence.md",
    "docs/bringup_checklist.md",
    "docs/concurrency_model.md",
    "docs/hardening_policy.md",
    "docs/known_limitations.md",
    "docs/references.md",
    "docs/requirements.md",
    "docs/resource_budget.md",
    "docs/risk_register.md",
    "docs/security_requirements.md",
    "docs/temporal_model.md",
    "docs/test_plan.md",
    "docs/threat_model.md",
    "docs/watchdog_policy.md",
    "evidence/README.md",
    "firmware/CMakeLists.txt",
    "firmware/main/Kconfig.projbuild",
    "firmware/main/app_main.cpp",
    "firmware/sdkconfig.defaults",
    "test/manual_lab02_commands.txt",
    "tools/check_lab02_identity_logs.py",
    "tools/capture_console_evidence.py",
    "tools/capture_static_gates.py",
]

REQUIRED_COMPONENTS = [
    "app_core",
    "board_hal",
    "command_console",
    "identity_service",
    "lab02_domain",
    "secure_log",
    "security_status",
]

FORBIDDEN_PARTS = {"build", "managed_components", "__pycache__", ".pytest_cache"}
FORBIDDEN_FILES = {"sdkconfig", "sdkconfig.old", "dependencies.lock"}


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def check_required_files() -> None:
    for rel in REQUIRED_FILES:
        if not (LAB_ROOT / rel).is_file():
            fail(f"required file missing: {rel}")


def check_components() -> None:
    for component in REQUIRED_COMPONENTS:
        component_dir = FW_ROOT / "components" / component
        if not component_dir.is_dir():
            fail(f"component missing: {component}")
        if not (component_dir / "CMakeLists.txt").is_file():
            fail(f"component CMakeLists missing: {component}")


def check_forbidden_artifacts() -> None:
    for path in LAB_ROOT.rglob("*"):
        rel_parts = set(path.relative_to(LAB_ROOT).parts)
        if rel_parts & FORBIDDEN_PARTS:
            fail(f"forbidden generated path present: {path.relative_to(LAB_ROOT)}")
        if path.name in FORBIDDEN_FILES:
            fail(f"forbidden generated/config file present: {path.relative_to(LAB_ROOT)}")


def check_markdown_indices() -> None:
    for md in LAB_ROOT.rglob("*.md"):
        text = md.read_text(encoding="utf-8")
        if "## Índice" not in text:
            fail(f"Markdown without index: {md.relative_to(LAB_ROOT)}")


def check_profile_contracts() -> None:
    kconfig = (FW_ROOT / "main" / "Kconfig.projbuild").read_text(encoding="utf-8")
    if "LAB02_PROFILE_INSECURE" not in kconfig:
        fail("missing INSECURE profile Kconfig option")
    if "LAB02_PROFILE_HARDENED" not in kconfig:
        fail("missing HARDENED profile Kconfig option")

    identity_contract = ((FW_ROOT / "components" / "identity_service" / "src" / "identity_service.cpp").read_text(encoding="utf-8") + "\n" + (FW_ROOT / "components" / "lab02_domain" / "include" / "lab02_domain" / "identity_contract.hpp").read_text(encoding="utf-8"))
    for required in [
        "hardcoded_mutable_console_value",
        "efuse_mac_sha256_truncated",
        "INSECURE_SHARED_LAB02_TOKEN",
        "identity_is_not_authentication",
    ]:
        if required not in identity_contract:
            fail(f"identity contract marker missing: {required}")


def main() -> int:
    check_required_files()
    check_components()
    check_forbidden_artifacts()
    check_markdown_indices()
    check_profile_contracts()
    print("PASS: LAB 02 static gates completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
