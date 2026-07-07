#!/usr/bin/env python3
"""Capture LAB 03 static gate evidence."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "labs" / "lab03_mqtt" / "evidence" / "lab03_static_gates.txt"

COMMANDS = [
    ("static_repository_gates", ROOT / "tools" / "repo_quality_gates" / "run_static_repo_gates.py"),
    ("lab03_static_gates", ROOT / "labs" / "lab03_mqtt" / "tools" / "run_static_gates.py"),
]


def run_command(script: Path) -> tuple[int, str, str]:
    completed = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def main() -> int:
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = [
        "# LAB 03 static gates evidence",
        "",
        "```text",
    ]

    overall_ok = True

    for name, script in COMMANDS:
        if not script.exists():
            overall_ok = False
            lines.extend([
                f"command: {name}",
                f"script: {script.relative_to(ROOT)}",
                "returncode: MISSING",
                "stderr:",
                f"missing script: {script.relative_to(ROOT)}",
                "",
            ])
            continue

        returncode, stdout, stderr = run_command(script)
        if returncode != 0:
            overall_ok = False

        lines.extend([
            f"command: {name}",
            f"script: {script.relative_to(ROOT)}",
            f"returncode: {returncode}",
            "stdout:",
            stdout.rstrip() if stdout.strip() else "<empty>",
            "stderr:",
            stderr.rstrip() if stderr.strip() else "<empty>",
            "",
        ])

    lines.extend([
        "```",
        "",
        f"# capture_validation result={'PASS' if overall_ok else 'FAIL'}",
        "",
    ])

    EVIDENCE.write_text("\n".join(lines), encoding="utf-8", newline="\n")

    if not overall_ok:
        print(f"FAIL: static gates evidence written to {EVIDENCE}")
        return 1

    print(f"PASS: static gates evidence written to {EVIDENCE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
