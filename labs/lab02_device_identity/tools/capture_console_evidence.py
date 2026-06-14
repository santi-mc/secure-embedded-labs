#!/usr/bin/env python3
"""Capture LAB 02 console evidence through a serial port.

The script sends a deterministic command sequence to the ESP32-S3 USB
Serial/JTAG console and stores the received NDJSON logs in an evidence file.

It is intentionally transport-only: it does not change Kconfig, build, flash or
select the firmware profile. The operator must flash the matching INSECURE or
HARDENED image before capturing each profile.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

try:
    import serial
except ImportError as exc:  # pragma: no cover - depends on host environment
    raise SystemExit(
        "pyserial is required. Install it with: python -m pip install pyserial"
    ) from exc

DEFAULT_BAUDRATE = 115200
DEFAULT_READ_WINDOW_S = 1.25
DEFAULT_BOOT_WINDOW_S = 1.50
DEFAULT_TIMEOUT_S = 0.10

INSECURE_COMMANDS = [
    "help",
    "identity_status",
    "get_identity",
    "set_device_id CLONED-DEVICE-001",
    "get_identity",
    "get_claim",
    "security_status",
]

HARDENED_COMMANDS = [
    "help",
    "identity_status",
    "get_identity",
    "get_claim",
    "set_device_id CLONED-DEVICE-001",
    "get_identity",
    "get_claim",
    "security_status",
]


def _read_available(ser: "serial.Serial", duration_s: float) -> list[str]:
    """Read complete text lines for a bounded interval."""
    deadline = time.monotonic() + duration_s
    lines: list[str] = []

    while time.monotonic() < deadline:
        raw = ser.readline()
        if not raw:
            continue

        text = raw.decode("utf-8", errors="replace").rstrip("\r\n")
        if text:
            lines.append(text)

    return lines


def _build_commands(profile: str) -> list[str]:
    if profile == "insecure":
        return list(INSECURE_COMMANDS)
    if profile == "hardened":
        return list(HARDENED_COMMANDS)
    raise ValueError(f"unsupported profile: {profile}")


def _json_events(lines: list[str]) -> list[dict[str, object]]:
    """Parse JSON log events from a mixed capture file."""
    events: list[dict[str, object]] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("{"):
            continue
        try:
            event = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def _validate_capture(lines: list[str], profile: str) -> list[str]:
    """Validate that captured evidence matches the requested profile."""
    expected_profile = profile.upper()
    events = _json_events(lines)
    errors: list[str] = []

    profile_values = [event.get("profile") for event in events if "profile" in event]
    if not profile_values:
        errors.append("no firmware profile found in captured JSON events")
    elif any(value != expected_profile for value in profile_values):
        observed = sorted({str(value) for value in profile_values})
        errors.append(
            f"firmware profile mismatch: requested {expected_profile}, observed {','.join(observed)}"
        )

    if profile == "insecure":
        if not any(event.get("event") == "identity_update_accepted" for event in events):
            errors.append("missing INSECURE identity_update_accepted evidence")
        if not any(event.get("auth_token") == "INSECURE_SHARED_LAB02_TOKEN" for event in events):
            errors.append("missing INSECURE shared-token evidence")
    elif profile == "hardened":
        if any(event.get("auth_token") == "INSECURE_SHARED_LAB02_TOKEN" for event in events):
            errors.append("HARDENED capture exposes INSECURE shared token")
        if any(event.get("raw_hardware_id") not in (None, "<redacted>") for event in events):
            errors.append("HARDENED capture exposes raw hardware identifier")
        if not any(event.get("event") == "identity_update_rejected" for event in events):
            errors.append("missing HARDENED identity_update_rejected evidence")

    return errors


def capture(
    *,
    port: str,
    baudrate: int,
    output: Path,
    profile: str,
    command_delay_s: float,
    boot_window_s: float,
) -> int:
    """Capture one profile evidence file."""
    output.parent.mkdir(parents=True, exist_ok=True)
    commands = _build_commands(profile)

    with serial.Serial(port=port, baudrate=baudrate, timeout=DEFAULT_TIMEOUT_S) as ser:
        # Keep control lines deasserted. This avoids accidental reset on boards
        # whose USB-UART bridge maps RTS/DTR to EN/BOOT. Native USB Serial/JTAG
        # normally ignores this, but keeping the policy explicit is safer.
        ser.dtr = False
        ser.rts = False
        time.sleep(0.25)
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        captured: list[str] = [
            f"# capture_start lab=LAB02 profile={profile.upper()} port={port} baudrate={baudrate}",
            "# operator_note firmware_profile_must_match_capture_profile",
        ]
        captured.extend(_read_available(ser, boot_window_s))

        for command in commands:
            captured.append(f"# tx {command}")
            ser.write((command + "\n").encode("utf-8"))
            ser.flush()
            captured.extend(_read_available(ser, command_delay_s))

        validation_errors = _validate_capture(captured, profile)
        if validation_errors:
            captured.append("# capture_validation result=FAIL")
            captured.extend(f"# capture_validation_error {error}" for error in validation_errors)
        else:
            captured.append("# capture_validation result=PASS")

        captured.append("# capture_end")

    output.write_text("\n".join(captured) + "\n", encoding="utf-8", newline="\n")
    if validation_errors:
        for error in validation_errors:
            print(f"FAIL: {error}", file=sys.stderr)
        print(f"FAIL: invalid evidence written to {output}", file=sys.stderr)
        return 1

    print(f"PASS: {profile.upper()} console evidence written to {output}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture LAB 02 console evidence")
    parser.add_argument("--port", required=True, help="Serial port, for example COM5")
    parser.add_argument("--baudrate", type=int, default=DEFAULT_BAUDRATE)
    parser.add_argument("--profile", required=True, choices=("insecure", "hardened"))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--command-delay-s", type=float, default=DEFAULT_READ_WINDOW_S)
    parser.add_argument("--boot-window-s", type=float, default=DEFAULT_BOOT_WINDOW_S)
    args = parser.parse_args()

    return capture(
        port=args.port,
        baudrate=args.baudrate,
        output=args.output,
        profile=args.profile,
        command_delay_s=args.command_delay_s,
        boot_window_s=args.boot_window_s,
    )


if __name__ == "__main__":
    sys.exit(main())
