#!/usr/bin/env python3
"""O00 config validation helper."""
from pathlib import Path
import json

REQUIRED_CONTROLLERS = ["G00", "O00", "K00", "F00", "V00", "R00", "A00", "H00", "U00"]


def validate(registry_path: str, config_path: str) -> dict:
    gaps = []
    registry = json.loads(Path(registry_path).read_text(encoding="utf-8"))
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    registered = [c.get("controller_id") for c in registry.get("registered_controllers", [])]
    missing = [c for c in REQUIRED_CONTROLLERS if c not in registered]
    if missing:
        gaps.append({"gap_type": "missing_required_controllers", "missing": missing})
    if config.get("safe_mode") is not True:
        gaps.append({"gap_type": "safe_mode_not_true"})
    return {"status": "CONFIG_VALIDATED" if not gaps else "CONFIG_VALIDATION_FAILED", "blocking_gaps": gaps}
