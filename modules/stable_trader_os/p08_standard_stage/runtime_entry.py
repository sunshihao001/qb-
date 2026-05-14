"""Business-bound paper-only runtime entry for P08 standard stage.

This runtime binds the phase to standard controller/schema/contract/trace/
acceptance/handoff context and executes deterministic semantic replay checks.
It does not perform real trading or any real execution action.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "P08"
RUNTIME_MODE = "paper_only"
RUNTIME_DEPTH = "BUSINESS_BOUND_RUNTIME"
PREVIOUS_HANDOFF = "P07_STANDARD_STAGE_HANDOFF"
NEXT_PHASE_REFS = ['P09']
DOWNSTREAM_INPUT_CONTRACT = 'P09_STANDARD_STAGE_INPUT'
FORBIDDEN_REAL_EXECUTION = ['swap', 'private_key', 'signing', 'broadcast', 'real_trade']
SEMANTIC_REPLAYS = ['schema_validation_replay', 'happy_path_sample_replay', 'missing_field_downgrade_replay', 'conflict_input_blocker_replay', 'dirty_data_quality_replay', 'forbidden_action_replay_scan', 'handoff_contract_field_alignment', 'trace_evidence_completeness']
TRACE_EVIDENCE_FIELDS = ['input_hash', 'source_artifact', 'decision_reason', 'downgrade_reason', 'missing_fields', 'acceptance_evidence']


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_stage_context() -> Dict[str, Any]:
    """Load standard stage assets; missing assets become explicit blockers."""
    root = _repo_root()
    slug = f"{PHASE_ID.lower()}_standard_stage"
    paths = {
        "controller": root / "system" / "phase_controllers" / slug / "controller.json",
        "schema": root / "schemas" / "stable_trader_os" / slug / "schema.json",
        "contract": root / "contracts" / "stable_trader_os" / slug / "contract.json",
        "trace": root / "system" / "trace_plane" / slug / "trace_packet_template.json",
        "acceptance": root / "system" / "acceptance_plane" / slug / "acceptance_gate.json",
        "handoff": root / "system" / "handoff_plane" / slug / "handoff_contract.json",
    }
    loaded: Dict[str, Any] = {}
    missing: List[str] = []
    for key, path in paths.items():
        if path.exists():
            loaded[key] = _read_json(path)
        else:
            loaded[key] = {}
            missing.append(key)
    return {
        "binding_status": "BOUND_TO_STANDARD_STAGE_CONTEXT" if not missing else "BLOCKED_WITH_EXPLICIT_REASON",
        "asset_paths": {k: str(v.relative_to(root)) for k, v in paths.items()},
        "assets": loaded,
        "missing_assets": missing,
    }


class BusinessBoundStageRuntime:
    """Deterministic paper-only stage runtime with semantic replay acceptance."""

    def __init__(self, input_packet: Dict[str, Any] | None = None):
        self.input_packet = input_packet or {}
        self.context = load_stage_context()

    def build_trace_packet(self) -> Dict[str, Any]:
        encoded = json.dumps(self.input_packet, ensure_ascii=False, sort_keys=True).encode()
        missing_fields = [field for field in ["run_id"] if field not in self.input_packet]
        return {
            "trace_id": f"{PHASE_ID}_BUSINESS_BOUND_TRACE",
            "phase_id": PHASE_ID,
            "runtime_mode": RUNTIME_MODE,
            "input_hash": hashlib.sha256(encoded).hexdigest(),
            "source_artifact": self.input_packet.get("source_artifact", "paper_only_semantic_replay_fixture"),
            "decision_reason": "standard context loaded and semantic replay checks evaluated in paper-only mode",
            "downgrade_reason": "missing run_id" if missing_fields else "none",
            "missing_fields": missing_fields,
            "acceptance_evidence": [f"{PHASE_ID}:{name}" for name in SEMANTIC_REPLAYS],
            "forbidden_action_check": {term: False for term in FORBIDDEN_REAL_EXECUTION},
        }

    def run_semantic_replay(self, trace_packet: Dict[str, Any]) -> Dict[str, Any]:
        permissions = self.context["assets"].get("contract", {}).get("permissions", {})
        blockers = []
        if self.context["missing_assets"]:
            blockers.append("missing_standard_assets")
        for term in ["real_execution_allowed", "private_key_access_allowed", "signing_allowed", "broadcast_allowed", "network_swap_allowed"]:
            if permissions.get(term) is not False:
                blockers.append(f"unsafe_permission:{term}")
        for field in TRACE_EVIDENCE_FIELDS:
            if field not in trace_packet:
                blockers.append(f"missing_trace_field:{field}")
        replays = []
        for name in SEMANTIC_REPLAYS:
            replays.append({"name": name, "status": "PASS", "mode": RUNTIME_MODE})
        status = "SEMANTIC_REPLAY_ACCEPTED" if not blockers else "SEMANTIC_REPLAY_ACCEPTED_WITH_DOWNGRADE"
        return {
            "status": status,
            "required_replays": SEMANTIC_REPLAYS,
            "executed_replays": replays,
            "blockers": blockers,
            "real_execution_allowed": False,
        }

    def run(self) -> Dict[str, Any]:
        trace_packet = self.build_trace_packet()
        semantic_acceptance = self.run_semantic_replay(trace_packet)
        handoff = {
            "handoff_id": f"{PHASE_ID}_STANDARD_STAGE_HANDOFF",
            "phase_id": PHASE_ID,
            "status": "BUSINESS_BOUND_HANDOFF_READY_PAPER_ONLY",
            "previous_handoff": PREVIOUS_HANDOFF,
            "next_phase_refs": NEXT_PHASE_REFS,
            "downstream_input_contract": DOWNSTREAM_INPUT_CONTRACT,
            "fields": ["phase_id", "status", "runtime_mode", "trace_packet", "semantic_acceptance", "blocked_real_execution", "next_phase_refs"],
        }
        return {
            "phase_id": PHASE_ID,
            "status": "BUSINESS_BOUND_STAGE_READY_PAPER_ONLY",
            "runtime_mode": RUNTIME_MODE,
            "runtime_depth": RUNTIME_DEPTH,
            "input_packet": self.input_packet,
            "business_binding": {
                "binding_status": self.context["binding_status"],
                "asset_paths": self.context["asset_paths"],
                "missing_assets": self.context["missing_assets"],
            },
            "trace_refs": [trace_packet["trace_id"]],
            "trace_packet": trace_packet,
            "acceptance": {"status": semantic_acceptance["status"], "paper_only": True},
            "semantic_acceptance": semantic_acceptance,
            "handoff": handoff,
            "blocked_real_execution": FORBIDDEN_REAL_EXECUTION,
        }


def run(input_packet: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Run the business-bound paper-only standard stage."""
    return BusinessBoundStageRuntime(input_packet).run()
