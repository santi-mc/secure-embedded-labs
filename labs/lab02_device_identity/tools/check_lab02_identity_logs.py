#!/usr/bin/env python3
"""Check LAB 02 identity logs for expected insecure/hardened behavior."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

INSECURE_TOKEN = "INSECURE_SHARED_LAB02_TOKEN"


def load_events(path: Path) -> list[dict[str, object]]:
    events: list[dict[str, object]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or not stripped.startswith("{"):
            continue
        try:
            event = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON at line {line_no}: {exc}") from exc
        events.append(event)
    return events


def has_event(events: list[dict[str, object]], name: str) -> bool:
    return any(event.get("event") == name for event in events)


def check_insecure(events: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    if not any(event.get("profile") == "INSECURE" for event in events):
        errors.append("missing INSECURE profile events")
    if not any(event.get("device_id") == "LAB02-DEVICE-0001" for event in events):
        errors.append("missing default cloneable device_id")
    if not any(event.get("auth_token") == INSECURE_TOKEN for event in events):
        errors.append("missing intentional insecure shared token evidence")
    if not has_event(events, "identity_update_accepted"):
        errors.append("missing accepted identity update evidence")
    return errors


def check_hardened(events: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    if not any(event.get("profile") == "HARDENED" for event in events):
        errors.append("missing HARDENED profile events")
    if any(event.get("auth_token") == INSECURE_TOKEN for event in events):
        errors.append("HARDENED log exposes insecure shared token")
    if any(event.get("raw_hardware_id") not in (None, "<redacted>") for event in events):
        errors.append("HARDENED log exposes raw hardware identifier")
    if not has_event(events, "identity_update_rejected"):
        errors.append("missing rejected identity update evidence")
    if not any(str(event.get("device_id", "")).startswith("lab02-") for event in events):
        errors.append("missing derived lab02 device_id")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log", type=Path)
    parser.add_argument("--profile", choices=("insecure", "hardened"), required=True)
    args = parser.parse_args()

    events = load_events(args.log)
    errors = check_insecure(events) if args.profile == "insecure" else check_hardened(events)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: LAB 02 {args.profile} log checks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
