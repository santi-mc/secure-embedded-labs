#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAB_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
FIRMWARE_ROOT="${LAB_ROOT}/firmware"

echo "[LAB01] Running static gates..."
python3 "${SCRIPT_DIR}/run_static_gates.py"

echo "[LAB01] Running ESP-IDF build..."
cd "${FIRMWARE_ROOT}"
idf.py set-target esp32s3
idf.py build

echo "[LAB01] Quality gates completed."
