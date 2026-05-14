#!/usr/bin/env python3
"""O00 pipeline orchestrator helper.

This module intentionally exposes safe design-level helpers used by tools/o00_cli.py.
It does not start live runtime, wallet signing, deploys, or production trading.
"""
from pathlib import Path
import json

FORBIDDEN_ACTIONS = ["live_runtime", "wallet_signing", "auto_deploy", "production_trading", "execute_real_order"]


def load_json(path: str):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def assert_safe_boundary(config: dict) -> list:
    boundary = config.get("execution_boundary", {})
    violations = []
    for key, action in [
        ("allow_live_runtime", "live_runtime"),
        ("allow_wallet_signing", "wallet_signing"),
        ("allow_auto_deploy", "auto_deploy"),
        ("allow_production_trading", "production_trading"),
        ("allow_execute_real_order", "execute_real_order"),
    ]:
        if boundary.get(key) is True:
            violations.append(action)
    return violations


def build_design_execution_plan(pipeline_run_id: str) -> dict:
    return {
        "pipeline_run_id": pipeline_run_id,
        "mode": "DESIGN_LEVEL_REPLAY",
        "stages": ["K00", "F00", "V00", "R00", "A00", "H00", "U00", "G00"],
        "r00_policy": "SKIP_REAL_RUNNER_BINDING",
        "forbidden_actions": FORBIDDEN_ACTIONS,
    }
