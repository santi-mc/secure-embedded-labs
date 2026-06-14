#!/usr/bin/env python3
"""Run LAB 02 static gates and store their output as audit evidence."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

LAB_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = LAB_ROOT.parents[1]
DEFAULT_OUTPUT = LAB_ROOT / "evidence" / "lab02_static_gates.txt"


def run_command(command: list[str]) -> tuple[int, str]:
    completed = subprocess.run(
        command,
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    return completed.returncode, completed.stdout


def main() -> int:
    output = DEFAULT_OUTPUT
    if len(sys.argv) == 3 and sys.argv[1] == "--output":
        output = Path(sys.argv[2])
    elif len(sys.argv) != 1:
        print("usage: capture_static_gates.py [--output <file>]", file=sys.stderr)
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    sections: list[str] = ["# LAB 02 static gates evidence"]
    failed = False

    commands = [
        [sys.executable, "tools/repo_quality_gates/run_static_repo_gates.py"],
        [sys.executable, "labs/lab02_device_identity/tools/run_static_gates.py"],
    ]

    for command in commands:
        sections.append(f"\n## command: {' '.join(command)}\n")
        returncode, stdout = run_command(command)
        sections.append(stdout.rstrip())
        sections.append(f"\nreturncode={returncode}")
        failed = failed or returncode != 0

    output.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8", newline="\n")

    if failed:
        print(f"FAIL: static gates evidence written to {output}")
        return 1

    print(f"PASS: static gates evidence written to {output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
