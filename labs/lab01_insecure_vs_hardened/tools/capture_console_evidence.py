#!/usr/bin/env python3
"""Capture LAB 01 console evidence over a serial port.

The script sends a deterministic command sequence to the ESP32-S3 console and
stores the received NDJSON-style firmware logs in an evidence file. It validates
that the firmware profile observed in the log matches the requested profile.

Do not use real credentials or production secrets in lab commands. The passwords
used here are fixed laboratory strings.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

try:
    import serial
except ImportError as exc:  # pragma: no cover - depends on host environment
    raise SystemExit("FAIL: pyserial is required. Install with: python -m pip install pyserial") from exc


@dataclass(frozen=True)
class CaptureProfile:
    """Command sequence and validation metadata for a LAB 01 profile."""

    name: str
    expected_profile: str
    commands: tuple[str, ...]


PROFILES: dict[str, CaptureProfile] = {
    "insecure": CaptureProfile(
        name="insecure",
        expected_profile="INSECURE",
        commands=(
            "help",
            "status",
            "get_config",
            "set_period 25s",
            "set_period 0",
            "set_mqtt_password LAB01_INSECURE_TEST_PASSWORD",
            "get_config",
            "factory_reset",
            "security_status",
        ),
    ),
    "hardened": CaptureProfile(
        name="hardened",
        expected_profile="HARDENED",
        commands=(
            "help",
            "status",
            "get_config",
            "set_period 25s",
            "set_period 0",
            "set_period 60",
            "set_mqtt_password LAB01_HARDENED_TEST_PASSWORD",
            "get_config",
            "factory_reset",
            "security_status",
        ),
    ),
}


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True, help="Serial port, e.g. COM5")
    parser.add_argument("--baudrate", type=int, default=115200)
    parser.add_argument("--profile", choices=sorted(PROFILES), required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--startup-wait-s", type=float, default=2.0)
    parser.add_argument("--command-wait-s", type=float, default=1.2)
    return parser.parse_args()


def decode_line(raw: bytes) -> str:
    """Decode one serial line safely for evidence storage."""

    return raw.decode("utf-8", errors="replace").rstrip("\r\n")


def read_available(ser: serial.Serial, duration_s: float) -> list[str]:
    """Read all available serial lines for a bounded amount of time."""

    deadline = time.monotonic() + duration_s
    lines: list[str] = []
    while time.monotonic() < deadline:
        raw = ser.readline()
        if not raw:
            continue
        line = decode_line(raw)
        if line:
            lines.append(line)
    return lines


def tx_label(command: str) -> str:
    """Return a non-sensitive transmission label for evidence comments."""

    if command.startswith("set_mqtt_password"):
        return "<sensitive_command_redacted>"
    return command


def extract_json_objects(lines: list[str]) -> list[dict[str, object]]:
    """Extract JSON objects from captured lines, ignoring comments/noise."""

    objects: list[dict[str, object]] = []
    for line in lines:
        start = line.find("{")
        if start < 0:
            continue
        try:
            parsed = json.loads(line[start:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            objects.append(parsed)
    return objects


def validate_capture(lines: list[str], profile: CaptureProfile) -> tuple[bool, str]:
    """Validate profile consistency and obvious hardened-secret leakage."""

    objects = extract_json_objects(lines)
    observed_profiles = {
        str(obj.get("profile"))
        for obj in objects
        if obj.get("profile") is not None
    }

    if profile.expected_profile not in observed_profiles:
        return False, f"expected profile {profile.expected_profile} not observed; observed={sorted(observed_profiles)}"

    wrong_profiles = observed_profiles - {profile.expected_profile}
    if wrong_profiles:
        return False, f"unexpected profiles observed: {sorted(wrong_profiles)}"

    if profile.name == "hardened":
        forbidden = "LAB01_HARDENED_TEST_PASSWORD"
        for line in lines:
            if forbidden in line:
                return False, "hardened evidence leaked the test password literal"

    return True, "profile_consistent"


def capture(args: argparse.Namespace) -> int:
    """Capture evidence and write the output file even on validation failure."""

    profile = PROFILES[args.profile]
    args.output.parent.mkdir(parents=True, exist_ok=True)

    captured: list[str] = [
        f"# capture_start lab=LAB01 requested_profile={profile.expected_profile} port={args.port} baudrate={args.baudrate}",
        "# note Do not edit this file manually. Regenerate it with capture_console_evidence.py.",
    ]

    with serial.Serial(port=args.port, baudrate=args.baudrate, timeout=0.1) as ser:
        # Keep control lines stable to avoid accidental reset on many boards.
        ser.dtr = False
        ser.rts = False
        time.sleep(0.5)
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        captured.extend(read_available(ser, args.startup_wait_s))

        for command in profile.commands:
            captured.append(f"# tx {tx_label(command)}")
            ser.write((command + "\n").encode("utf-8"))
            ser.flush()
            captured.extend(read_available(ser, args.command_wait_s))

    ok, reason = validate_capture(captured, profile)
    result = "PASS" if ok else "FAIL"
    captured.append(f"# capture_validation result={result} reason={reason}")
    captured.append("# capture_end")
    args.output.write_text("\n".join(captured) + "\n", encoding="utf-8", newline="\n")

    if not ok:
        print(f"FAIL: {profile.expected_profile} console evidence validation failed: {reason}")
        print(f"Evidence written to {args.output}")
        return 1

    print(f"PASS: {profile.expected_profile} console evidence written to {args.output}")
    return 0


def main() -> int:
    """CLI entry point."""

    return capture(parse_args())


if __name__ == "__main__":
    sys.exit(main())
