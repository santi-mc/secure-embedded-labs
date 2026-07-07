#!/usr/bin/env python3
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
