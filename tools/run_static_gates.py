#!/usr/bin/env python3
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
runpy.run_path(str(ROOT / "tools" / "repo_quality_gates" / "run_static_repo_gates.py"), run_name="__main__")
