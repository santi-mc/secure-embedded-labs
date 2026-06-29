#!/usr/bin/env python3
from __future__ import annotations
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "labs" / "lab03_mqtt_tls" / "evidence" / "lab03_static_gates.txt"
def run(command: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return result.returncode, result.stdout, result.stderr
def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    sections = ["# LAB 03 static gates evidence", ""]
    commands = [[sys.executable, "tools/repo_quality_gates/run_static_repo_gates.py"], [sys.executable, "labs/lab03_mqtt_tls/tools/run_static_gates.py"]]
    ok = True
    for command in commands:
        rc, stdout, stderr = run(command)
        ok = ok and rc == 0
        sections += ["## command", " ".join(command), f"returncode: {rc}", "stdout:", stdout.strip() or "<empty>", "stderr:", stderr.strip() or "<empty>", ""]
    sections.append(f"# capture_validation result={'PASS' if ok else 'FAIL'}")
    OUT.write_text("\n".join(sections) + "\n", encoding="utf-8", newline="\n")
    print(f"{'PASS' if ok else 'FAIL'}: static gates evidence written to {OUT}")
    return 0 if ok else 1
if __name__ == "__main__":
    sys.exit(main())
