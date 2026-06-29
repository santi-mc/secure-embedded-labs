#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = ["README.md", "CHANGELOG.md", "COMMIT_MESSAGE.txt", "docs/scenario_matrix.md", "docs/threat_model.md", "docs/test_plan.md", "docs/audit_evidence.md", "docs/certificate_policy.md", "docs/risk_register.md", "docs/references.md", "evidence/README.md", "test/manual_lab03_commands.txt", "tools/capture_console_evidence.py", "tools/check_mqtt_scenario_logs.py", "tools/capture_static_gates.py", "firmware/CMakeLists.txt", "firmware/sdkconfig.defaults"]
REQUIRED_README_SECTIONS = ["## Índice", "## Objetivo", "## Matriz contractual", "## Cómo compilar", "## Evidencias esperadas", "## Estado"]
def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1
def main() -> int:
    if (ROOT / "firmware/build").exists():
        return fail("forbidden generated directory present: firmware/build")
    for filename in REQUIRED_FILES:
        if not (ROOT / filename).exists():
            return fail(f"missing required file: {filename}")
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    for section in REQUIRED_README_SECTIONS:
        if section not in readme:
            return fail(f"README.md missing section: {section}")
    matrix = (ROOT / "docs/scenario_matrix.md").read_text(encoding="utf-8", errors="replace")
    for scenario in ["M03-1883", "M03-1884", "M03-8883", "M03-8884", "M03-8885", "M03-8886", "M03-8887", "M03-8080", "M03-8081", "M03-8090", "M03-8091"]:
        if scenario not in matrix:
            return fail(f"scenario matrix missing {scenario}")
    print("PASS: LAB 03 static gates completed successfully")
    return 0
if __name__ == "__main__":
    sys.exit(main())
