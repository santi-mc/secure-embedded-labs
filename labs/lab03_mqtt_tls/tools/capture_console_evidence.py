#!/usr/bin/env python3
from __future__ import annotations
import argparse
import sys
import time
from pathlib import Path
import serial
COMMANDS = ["help", "scenario_list", "select_scenario {scenario}", "scenario_status", "mqtt_connect_dry_run", "mqtt_publish_dry_run", "security_status"]
def read_available(ser: serial.Serial, duration_s: float) -> list[str]:
    deadline = time.monotonic() + duration_s
    lines: list[str] = []
    while time.monotonic() < deadline:
        raw = ser.readline()
        if not raw:
            continue
        line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
        if line:
            lines.append(line)
    return lines
def capture(port: str, baudrate: int, scenario: str, output: Path) -> int:
    output.parent.mkdir(parents=True, exist_ok=True)
    captured: list[str] = [f"# capture_start lab=LAB03 scenario={scenario} port={port} baudrate={baudrate}"]
    with serial.Serial(port=port, baudrate=baudrate, timeout=0.1) as ser:
        ser.dtr = False
        ser.rts = False
        time.sleep(0.5)
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        captured.extend(read_available(ser, 1.5))
        for template in COMMANDS:
            command = template.format(scenario=scenario)
            captured.append(f"# tx {command}")
            ser.write((command + "\n").encode("utf-8"))
            ser.flush()
            captured.extend(read_available(ser, 1.0))
    text = "\n".join(captured) + "\n"
    ok = scenario in text and "mqtt_connect_dry_run" in text and "security_status" in text
    text += f"# capture_validation result={'PASS' if ok else 'FAIL'}\n"
    output.write_text(text, encoding="utf-8", newline="\n")
    print(f"{'PASS' if ok else 'FAIL'}: LAB 03 console evidence written to {output}")
    return 0 if ok else 1
def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True)
    parser.add_argument("--baudrate", type=int, default=115200)
    parser.add_argument("--scenario", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    return capture(args.port, args.baudrate, args.scenario, args.output)
if __name__ == "__main__":
    sys.exit(main())
