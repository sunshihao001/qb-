from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

FORBIDDEN_KEYS = {
    "buy_signal",
    "sell_signal",
    "trade_allowed",
    "execute_now",
    "certain_dealer_judgement",
    "private_key",
    "seed_phrase",
    "signed_transaction",
    "swap_execution",
}

REQUIRED_CONFIG = ["run_id", "token_address", "chain", "run_mode", "data_snapshot_time"]


class Phase01Validator:
    """Contract and hard-negative validator for Phase 01 data-fact runtime.

    The validator intentionally checks only facts/control contracts. It does not
    infer wallet roles, market scenarios, entries, or trading permission.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def validate_input(self, input_file: str | Path) -> Dict[str, Any]:
        input_file = Path(input_file)
        verdict: Dict[str, Any] = {
            "allowed": True,
            "gate_status": "PASS",
            "missing_fields": [],
            "hard_negative_reasons": [],
            "positive_evidence": [],
            "negative_evidence": [],
            "counter_evidence": [],
            "input_file": str(input_file),
        }
        try:
            payload = json.loads(input_file.read_text())
        except Exception as exc:  # noqa: BLE001
            verdict.update({
                "allowed": False,
                "gate_status": "BLOCK",
                "hard_negative_reasons": ["invalid_json"],
                "negative_evidence": [f"input_json_parse_failed:{exc.__class__.__name__}"],
            })
            return verdict

        missing = [key for key in REQUIRED_CONFIG if payload.get(key) in (None, "")]
        if missing:
            verdict["missing_fields"].extend(missing)
            verdict["negative_evidence"].append(f"required_config_missing:{','.join(missing)}")

        forbidden = sorted(k for k in FORBIDDEN_KEYS if k in payload)
        if forbidden:
            verdict["allowed"] = False
            verdict["gate_status"] = "BLOCK"
            verdict["hard_negative_reasons"].append("forbidden_judgement_leakage")
            verdict["negative_evidence"].append(f"forbidden_keys_present:{','.join(forbidden)}")
            verdict["counter_evidence"].append("Phase 01 input contains judgement/execution fields; data fact layer must block.")
            return verdict

        if missing:
            verdict["gate_status"] = "PAUSE" if len(missing) >= 2 else "PASS_WITH_WARNING"
            verdict["allowed"] = verdict["gate_status"] != "PAUSE"
        else:
            verdict["positive_evidence"].append("required_config_present")

        sources = payload.get("sources", {})
        if not isinstance(sources, dict) or not sources:
            verdict["missing_fields"].append("sources")
            verdict["negative_evidence"].append("sources_missing_or_empty")
            if verdict["gate_status"] == "PASS":
                verdict["gate_status"] = "PASS_WITH_WARNING"

        if payload.get("contains_mock_data") is True:
            verdict["counter_evidence"].append("mock_data_detected: not eligible for live decision claims")
            if verdict["gate_status"] == "PASS":
                verdict["gate_status"] = "PASS_WITH_WARNING"

        return verdict
