#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LAB = ROOT / "labs" / "lab03_mqtt_tls"
OUT = LAB / "evidence" / "lab03_static_gates.txt"


def remove_generated_artifacts() -> None:
    """Remove local ESP-IDF outputs that are forbidden by repository gates."""
    for path in [
        LAB / "firmware" / "build",
        LAB / "firmware" / "sdkconfig",
        LAB / "firmware" / "sdkconfig.old",
    ]:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def run(command: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return result.returncode, result.stdout, result.stderr


def file_has_pass(path: Path) -> bool:
    return path.exists() and "capture_validation result=PASS" in path.read_text(
        encoding="utf-8", errors="replace"
    )


def update_evidence_readme(static_ok: bool) -> None:
    evidence_readme = LAB / "evidence" / "README.md"
    console_ok = file_has_pass(LAB / "evidence" / "lab03_m03_1883_console.log")
    console_status = "CUMPLE" if console_ok else "PENDIENTE"
    static_status = "CUMPLE" if static_ok else "PENDIENTE"
    evidence_readme.write_text(
        "\n".join(
            [
                "# Evidencias LAB 03",
                "",
                "## Índice",
                "",
                "- [Propósito](#propósito)",
                "- [Evidencias de fase 03A](#evidencias-de-fase-03a)",
                "- [Pendientes](#pendientes)",
                "",
                "## Propósito",
                "",
                "Este directorio almacena evidencias de ejecución del LAB 03.",
                "",
                "No se deben versionar credenciales reales, certificados privados ni payloads sensibles.",
                "",
                "## Evidencias de fase 03A",
                "",
                "| Fichero | Estado | Descripción |",
                "| --- | --- | --- |",
                f"| `lab03_m03_1883_console.log` | {console_status} | Baseline MQTT 1883 sin TLS. |",
                f"| `lab03_static_gates.txt` | {static_status} | Gates estáticos. |",
                "",
                "## Pendientes",
                "",
                "| Evidencia | Estado |",
                "| --- | --- |",
                "| `lab03_build_esp32s3.txt` | PENDIENTE |",
                "| `lab03_real_broker_matrix.txt` | PENDIENTE |",
                "| `lab03_tls_certificate_validation.txt` | PENDIENTE |",
            ]
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    remove_generated_artifacts()

    sections = ["# LAB 03 static gates evidence", ""]
    commands = [
        [sys.executable, "tools/repo_quality_gates/run_static_repo_gates.py"],
        [sys.executable, "labs/lab03_mqtt_tls/tools/run_static_gates.py"],
    ]
    ok = True
    for command in commands:
        rc, stdout, stderr = run(command)
        ok = ok and rc == 0
        sections += [
            "## command",
            " ".join(command),
            f"returncode: {rc}",
            "stdout:",
            stdout.strip() or "<empty>",
            "stderr:",
            stderr.strip() or "<empty>",
            "",
        ]

    sections.append(f"# capture_validation result={'PASS' if ok else 'FAIL'}")
    OUT.write_text("\n".join(sections) + "\n", encoding="utf-8", newline="\n")
    update_evidence_readme(ok)
    print(f"{'PASS' if ok else 'FAIL'}: static gates evidence written to {OUT}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
