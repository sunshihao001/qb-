from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping

PHASE = "phase_01_data_fact_controller"
NEXT_STAGE = "phase_02_wallet_structure_controller"
ALLOWED_PHASE01_STATUS = {"PASS", "PASS_WITH_WARNING", "DATA_OK", "DATA_PARTIAL"}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _rel_or_abs(path: str | Path, base: Path) -> str:
    p = Path(path)
    try:
        return str(p.resolve().relative_to(base.resolve()))
    except Exception:
        return str(p)


def translate_bot2_handoff_to_phase01(
    *,
    bot2_handoff_file: str | Path,
    phase01_output_dir: str | Path,
    output_file: str | Path,
    run_id: str,
    phase01_gate_status: str,
    required_fact_files: Mapping[str, str],
) -> Dict[str, Any]:
    bot2_path = Path(bot2_handoff_file)
    phase01_dir = Path(phase01_output_dir)
    output = Path(output_file)
    output.parent.mkdir(parents=True, exist_ok=True)
    bot2 = json.loads(bot2_path.read_text(encoding="utf-8"))

    missing_fields = bot2.get("missing_fields_summary") or []
    if isinstance(missing_fields, dict):
        missing_fields = list(missing_fields.keys())
    if not isinstance(missing_fields, list):
        missing_fields = [str(missing_fields)]

    hard_negative = phase01_gate_status not in ALLOWED_PHASE01_STATUS and phase01_gate_status not in {"PASS_WITH_WARNING", "PASS"}
    required_files = {k: _rel_or_abs(v, phase01_dir) for k, v in dict(required_fact_files).items()}
    packet: Dict[str, Any] = {
        "phase": PHASE,
        "token_address": bot2.get("token_address", "missing"),
        "snapshot_id": run_id,
        "phase_status": phase01_gate_status,
        "allow_next_stage": not hard_negative,
        "next_stage": NEXT_STAGE,
        "required_files_for_next_stage": required_files,
        "positive_evidence": [
            "bot2_handoff_packet_present",
            "source_wallet_refs_preserved",
            "fact_only_language_enforced" if bot2.get("evidence_language_only") else "fact_only_language_unknown",
        ],
        "negative_evidence": [],
        "counter_evidence": [
            "translated_from_bot2_handoff_not_native_phase01_runtime" if PHASE not in str(bot2.get("packet_id", "")) else "native_phase01_packet"
        ],
        "hard_negative_triggered": hard_negative,
        "hard_negative_reasons": [] if not hard_negative else [f"phase01_gate_status_not_allowed:{phase01_gate_status}"],
        "block_reason": "" if not hard_negative else f"phase01_gate_status_not_allowed:{phase01_gate_status}",
        "degrade_reason": "translated_from_source_wallet_bot_handoff",
        "missing_fields": missing_fields,
        "audit_file": "missing",
        "source_handoff_file": str(bot2_path),
        "created_at": _now(),
    }
    output.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    return packet
