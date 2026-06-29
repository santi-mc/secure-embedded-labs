#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("log_file", type=Path)
    parser.add_argument("--scenario", required=True)
    args = parser.parse_args()
    if not args.log_file.exists():
        return fail(f"log file does not exist: {args.log_file}")
    saw_scenario = saw_connect = saw_publish = saw_validation = saw_no_cumple = False
    for line in args.log_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip() == "# capture_validation result=PASS":
            saw_validation = True
        if not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("scenario_id") == args.scenario:
            saw_scenario = True
        if obj.get("event") == "mqtt_connect_dry_run":
            saw_connect = True
            if obj.get("security_result") == "NO_CUMPLE_EXPECTED":
                saw_no_cumple = True
        if obj.get("event") == "mqtt_publish_dry_run":
            saw_publish = True
    if not saw_validation: return fail("capture validation PASS not found")
    if not saw_scenario: return fail(f"scenario {args.scenario} not found")
    if not saw_connect: return fail("mqtt_connect_dry_run not found")
    if not saw_publish: return fail("mqtt_publish_dry_run not found")
    if args.scenario == "M03-1883" and not saw_no_cumple: return fail("M03-1883 did not report NO_CUMPLE_EXPECTED")
    print(f"PASS: LAB 03 scenario log checks for {args.scenario}")
    return 0
if __name__ == "__main__":
    sys.exit(main())
