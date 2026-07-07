#!/usr/bin/env python3
"""Align LAB 03 documentation with repository and lab-specific gate contracts.

This maintenance helper is intentionally idempotent. It fixes only repository
hygiene/documentation contract issues found during LAB 03 bring-up:

- Remove generated ESP-IDF artifacts from labs/*/firmware.
- Ensure LAB 03 README exposes the lab-specific contractual matrix section.
- Ensure LAB 03 CHANGELOG has an index required by the global markdown gate.
- Keep the LAB 03 generator aligned so reruns do not reintroduce the same drift.
"""

from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "labs" / "lab03_mqtt_tls"
README = LAB / "README.md"
CHANGELOG = LAB / "CHANGELOG.md"
GENERATOR = ROOT / "tools" / "maintenance" / "apply_lab03_mosquitto_matrix.py"
SDKCONFIG_DEFAULTS = LAB / "firmware" / "sdkconfig.defaults"

MATRIX_BLOCK = """## Matriz contractual

| ID | Puerto | Transporte | TLS | Autenticación | Estado esperado | Estado actual |
| --- | ---: | --- | --- | --- | --- | --- |
| M03-1883 | 1883 | MQTT TCP | No | No | Conecta funcionalmente, pero `NO CUMPLE` seguridad | CUMPLE baseline dry-run |
| M03-1884 | 1884 | MQTT TCP | No | Usuario/password | Conecta, pero credenciales sin TLS: `NO CUMPLE` seguridad | PENDIENTE |
| M03-8883 | 8883 | MQTT TCP | Sí | No | Conecta validando CA mosquitto.org | PENDIENTE |
| M03-8884 | 8884 | MQTT TCP | Sí | Certificado cliente | Conecta solo con certificado cliente válido | PENDIENTE |
| M03-8885 | 8885 | MQTT TCP | Sí | Usuario/password | Conecta con TLS y autenticación | PENDIENTE |
| M03-8886 | 8886 | MQTT TCP | Sí | No | Conecta validando CA pública/Let's Encrypt | PENDIENTE |
| M03-8887 | 8887 | MQTT TCP | Sí, certificado expirado | No | El cliente debe rechazar la conexión | PENDIENTE |
| M03-8080 | 8080 | MQTT WebSocket | No | No | Conecta, pero `NO CUMPLE` seguridad | PENDIENTE |
| M03-8081 | 8081 | MQTT WebSocket | Sí | No | Conecta con WSS | PENDIENTE |
| M03-8090 | 8090 | MQTT WebSocket | No | Usuario/password | Conecta, pero credenciales sin TLS: `NO CUMPLE` seguridad | PENDIENTE |
| M03-8091 | 8091 | MQTT WebSocket | Sí | Usuario/password | Conecta con WSS y autenticación | PENDIENTE |

La matriz es contractual: cada escenario debe acabar con evidencia `CUMPLE`, `NO CUMPLE`, `NO VALIDADO` o `PENDIENTE`, sin considerar una conexión funcional como evidencia de seguridad por sí sola.
"""

CHANGELOG_INDEX = """## Índice

- [Estado actual](#estado-actual)
- [Historial](#historial)

"""

CHANGELOG_STATUS = """## Estado actual

- LAB 03A / M03-1883: baseline MQTT TCP sin TLS con evidencia de consola capturada.
- Matriz completa test.mosquitto.org: definida contractualmente y pendiente de ejecución real por fases.

"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text_if_changed(path: Path, content: str) -> bool:
    normalized = content.replace("\r\n", "\n").replace("\r", "\n")
    if path.exists() and read_text(path).replace("\r\n", "\n").replace("\r", "\n") == normalized:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(normalized, encoding="utf-8", newline="\n")
    return True


def insert_after_first_h1(content: str, block: str) -> str:
    lines = content.splitlines()
    for idx, line in enumerate(lines):
        if line.startswith("# "):
            return "\n".join(lines[: idx + 1]) + "\n\n" + block.rstrip() + "\n\n" + "\n".join(lines[idx + 1:]).lstrip("\n") + "\n"
    return block.rstrip() + "\n\n" + content.lstrip("\n")


def insert_before_anchor(content: str, block: str, anchors: list[str]) -> str:
    for anchor in anchors:
        pos = content.find("\n" + anchor)
        if pos != -1:
            return content[: pos + 1] + block.rstrip() + "\n\n" + content[pos + 1 :]
    if not content.endswith("\n"):
        content += "\n"
    return content + "\n" + block.rstrip() + "\n"


def cleanup_generated_artifacts() -> list[str]:
    removed: list[str] = []
    for firmware_dir in ROOT.glob("labs/*/firmware"):
        build_dir = firmware_dir / "build"
        if build_dir.exists():
            shutil.rmtree(build_dir)
            removed.append(str(build_dir.relative_to(ROOT)))
        for name in ("sdkconfig", "sdkconfig.old"):
            generated = firmware_dir / name
            if generated.exists():
                generated.unlink()
                removed.append(str(generated.relative_to(ROOT)))
    return removed


def ensure_lab03_readme_matrix() -> bool:
    if not README.exists():
        raise SystemExit(f"FAIL: missing {README.relative_to(ROOT)}")
    content = read_text(README)
    if "## Matriz contractual" in content:
        return False

    if "## Matriz de escenarios" in content:
        content = content.replace("## Matriz de escenarios", "## Matriz contractual", 1)
    else:
        content = insert_before_anchor(
            content,
            MATRIX_BLOCK,
            [
                "## Threat model",
                "## Modelo de amenazas",
                "## Requisitos",
                "## Plan de pruebas",
                "## Evidencias",
                "## Estado",
            ],
        )
    return write_text_if_changed(README, content)


def ensure_changelog_index() -> bool:
    if not CHANGELOG.exists():
        content = "# Changelog LAB 03\n\n" + CHANGELOG_INDEX + CHANGELOG_STATUS + "## Historial\n\n- Inicio de LAB 03A.\n"
        return write_text_if_changed(CHANGELOG, content)

    content = read_text(CHANGELOG)
    changed = False
    if "## Índice" not in content and "## Indice" not in content:
        content = insert_after_first_h1(content, CHANGELOG_INDEX)
        changed = True
    if "## Estado actual" not in content:
        insert_pos = content.find("\n## Historial")
        if insert_pos != -1:
            content = content[: insert_pos + 1] + CHANGELOG_STATUS + content[insert_pos + 1 :]
        else:
            if not content.endswith("\n"):
                content += "\n"
            content += "\n" + CHANGELOG_STATUS
        changed = True
    if "## Historial" not in content:
        if not content.endswith("\n"):
            content += "\n"
        content += "\n## Historial\n\n- Inicio de LAB 03A.\n"
        changed = True
    return write_text_if_changed(CHANGELOG, content) if changed else False


def ensure_sdkconfig_defaults() -> bool:
    if not SDKCONFIG_DEFAULTS.exists():
        return False
    content = read_text(SDKCONFIG_DEFAULTS)
    content = content.replace("CONFIG_ESP_CONSOLE_UART_NONE=y\n", "")
    content = content.replace("CONFIG_ESP_CONSOLE_NONE=y\n", "")
    if "CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y" not in content:
        content = content.rstrip() + "\nCONFIG_ESP_CONSOLE_USB_SERIAL_JTAG=y\n"
    return write_text_if_changed(SDKCONFIG_DEFAULTS, content)


def align_generator() -> bool:
    if not GENERATOR.exists():
        return False
    content = read_text(GENERATOR)
    original = content
    content = content.replace("CONFIG_ESP_CONSOLE_UART_NONE=y\\n", "")
    content = content.replace("CONFIG_ESP_CONSOLE_UART_NONE=y\n", "")
    content = content.replace("CONFIG_ESP_CONSOLE_NONE=y\\n", "")
    content = content.replace("CONFIG_ESP_CONSOLE_NONE=y\n", "")
    content = content.replace("## Matriz de escenarios", "## Matriz contractual")
    if "## Matriz contractual" not in content and "M03-1883" in content:
        # Conservative fallback: add the contractual section before the first threat-model section in the template.
        marker = "## Threat model"
        if marker in content:
            content = content.replace(marker, MATRIX_BLOCK.rstrip() + "\n\n" + marker, 1)
    return write_text_if_changed(GENERATOR, content) if content != original else False


def main() -> int:
    changed: list[str] = []
    removed = cleanup_generated_artifacts()
    if removed:
        changed.append("removed generated artifacts: " + ", ".join(removed))
    if ensure_lab03_readme_matrix():
        changed.append(str(README.relative_to(ROOT)))
    if ensure_changelog_index():
        changed.append(str(CHANGELOG.relative_to(ROOT)))
    if ensure_sdkconfig_defaults():
        changed.append(str(SDKCONFIG_DEFAULTS.relative_to(ROOT)))
    if align_generator():
        changed.append(str(GENERATOR.relative_to(ROOT)))

    if changed:
        print("PASS: LAB 03 gate contract aligned")
        for item in changed:
            print(f"- {item}")
    else:
        print("PASS: LAB 03 gate contract already aligned")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
