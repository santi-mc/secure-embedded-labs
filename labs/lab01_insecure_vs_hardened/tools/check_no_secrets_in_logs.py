#!/usr/bin/env python3
"""Check LAB 01 logs for forbidden secret disclosure patterns."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SECRET_WORDS = re.compile(r"(private_key|BEGIN PRIVATE KEY|token=|password=)", re.IGNORECASE)
RAW_SECRET_COMMAND = re.compile(r"set_mqtt_password\s+\S+", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", type=Path)
    parser.add_argument("--profile", choices=["insecure", "hardened"], required=True)
    return parser.parse_args()


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def check_hardened_line(line: str, line_no: int) -> None:
    if RAW_SECRET_COMMAND.search(line):
        fail(f"line {line_no}: raw set_mqtt_password payload is visible")

    if SECRET_WORDS.search(line):
        fail(f"line {line_no}: generic secret marker found")

    start = line.find("{")
    if start < 0:
        return

    try:
        obj = json.loads(line[start:])
    except json.JSONDecodeError:
        return

    if obj.get("mqtt_password") not in (None, "<redacted>"):
        fail(f"line {line_no}: mqtt_password is not redacted")

    if obj.get("field") == "mqtt_password" and obj.get("value") not in (None, "<redacted>"):
        fail(f"line {line_no}: mqtt_password update value is not redacted")

    if obj.get("raw", "").lower().startswith("set_mqtt_password"):
        fail(f"line {line_no}: raw sensitive command found in JSON")


def main() -> int:
    args = parse_args()
    if not args.logfile.is_file():
        fail(f"log file not found: {args.logfile}")

    text = args.logfile.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    if args.profile == "hardened":
        for index, line in enumerate(lines, start=1):
            check_hardened_line(line, index)
        print("PASS: hardened log contains no forbidden secret disclosure")
        return 0

    # In INSECURE mode the leak is intentional; this script reports whether the
    # evidence actually contains a demonstrable disclosure.
    leak_found = any(RAW_SECRET_COMMAND.search(line) or "INSECURE_DEFAULT_PASSWORD" in line for line in lines)
    if not leak_found:
        fail("insecure profile evidence does not demonstrate the expected leak")
    print("PASS: insecure log demonstrates the intended LAB 01 secret disclosure")
    return 0


if __name__ == "__main__":
    sys.exit(main())
