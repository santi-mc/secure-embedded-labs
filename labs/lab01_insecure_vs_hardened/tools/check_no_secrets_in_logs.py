#!/usr/bin/env python3
"""
LAB 01 log scanner.

The scanner intentionally treats INSECURE and HARDENED logs differently:

- INSECURE must demonstrate the intended training vulnerability.
- HARDENED must not expose raw MQTT password material.

Allowed in HARDENED:
- help text containing: set_mqtt_password <value>
- TX metadata containing: set_mqtt_password <redacted>
- JSON fields containing: "<redacted>"

Rejected in HARDENED:
- raw set_mqtt_password payloads
- mqtt_password values other than "<redacted>"
- command args for set_mqtt_password other than "<redacted>"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


REDACTED = "<redacted>"
HELP_PLACEHOLDER = "<value>"


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def is_redacted_or_placeholder(value: str) -> bool:
    return REDACTED in value or HELP_PLACEHOLDER in value


def parse_json_line(line: str) -> dict[str, Any] | None:
    stripped = line.strip()
    if not stripped.startswith("{"):
        return None

    try:
        value = json.loads(stripped)
    except json.JSONDecodeError:
        return None

    if isinstance(value, dict):
        return value
    return None


def contains_raw_set_password_payload(line: str) -> bool:
    """Return true only for real payloads, not help placeholders."""

    if "set_mqtt_password " not in line:
        return False

    if is_redacted_or_placeholder(line):
        return False

    return True


def check_hardened(lines: list[str]) -> int:
    saw_hardened_profile = False
    saw_redacted_password = False
    saw_set_password_command = False

    for line_number, line in enumerate(lines, start=1):
        stripped = line.strip()

        if contains_raw_set_password_payload(stripped):
            return fail(f"line {line_number}: raw set_mqtt_password payload is visible")

        obj = parse_json_line(stripped)
        if obj is None:
            continue

        profile = obj.get("profile")
        if profile == "HARDENED":
            saw_hardened_profile = True
        elif profile in {"INSECURE", "insecure"}:
            return fail(f"line {line_number}: INSECURE event found in HARDENED log")

        if obj.get("cmd") == "set_mqtt_password":
            saw_set_password_command = True
            args = obj.get("args")
            if args not in (None, REDACTED):
                return fail(f"line {line_number}: set_mqtt_password args are not redacted")

        raw = obj.get("raw")
        if isinstance(raw, str) and contains_raw_set_password_payload(raw):
            return fail(f"line {line_number}: raw command field exposes set_mqtt_password payload")

        if obj.get("field") == "mqtt_password":
            value = obj.get("value")
            if value != REDACTED:
                return fail(f"line {line_number}: mqtt_password update value is not redacted")
            saw_redacted_password = True

        if "mqtt_password" in obj:
            value = obj.get("mqtt_password")
            if value != REDACTED:
                return fail(f"line {line_number}: mqtt_password config value is not redacted")
            saw_redacted_password = True

    if not saw_hardened_profile:
        return fail("HARDENED profile was not observed")

    if not saw_set_password_command:
        return fail("set_mqtt_password command was not observed in HARDENED evidence")

    if not saw_redacted_password:
        return fail("redacted mqtt_password evidence was not observed")

    print("PASS: hardened log does not expose raw secrets")
    return 0


def check_insecure(lines: list[str]) -> int:
    saw_insecure_profile = False
    saw_disclosure = False

    for line in lines:
        stripped = line.strip()

        if contains_raw_set_password_payload(stripped):
            saw_disclosure = True

        obj = parse_json_line(stripped)
        if obj is None:
            continue

        profile = obj.get("profile")
        if profile == "INSECURE":
            saw_insecure_profile = True
        elif profile in {"HARDENED", "hardened"}:
            return fail("HARDENED event found in INSECURE log")

        raw = obj.get("raw")
        if isinstance(raw, str) and contains_raw_set_password_payload(raw):
            saw_disclosure = True

        if obj.get("field") == "mqtt_password":
            value = obj.get("value")
            if isinstance(value, str) and value != REDACTED:
                saw_disclosure = True

        if "mqtt_password" in obj:
            value = obj.get("mqtt_password")
            if isinstance(value, str) and value != REDACTED:
                saw_disclosure = True

    if not saw_insecure_profile:
        return fail("INSECURE profile was not observed")

    if not saw_disclosure:
        return fail("intended LAB 01 secret disclosure was not observed")

    print("PASS: insecure log demonstrates the intended LAB 01 secret disclosure")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file", type=Path)
    parser.add_argument("--profile", required=True, choices=("insecure", "hardened"))
    args = parser.parse_args()

    if not args.log_file.exists():
        return fail(f"log file does not exist: {args.log_file}")

    lines = args.log_file.read_text(encoding="utf-8", errors="replace").splitlines()

    if args.profile == "insecure":
        return check_insecure(lines)

    return check_hardened(lines)


if __name__ == "__main__":
    sys.exit(main())
