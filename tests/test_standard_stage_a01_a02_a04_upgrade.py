import importlib.util
import json
from pathlib import Path

ROOT = Path("/root/sikk-gmgn")
MANIFEST = ROOT / "system/stable_trader_os/standard_stage_closure/manifest.json"
PHASES = [f"K{i:02d}" for i in range(0, 9)] + [f"P{i:02d}" for i in range(0, 11)] + [f"I{i:02d}" for i in range(1, 6)] + ["R00"]
FORBIDDEN = {"swap", "private_key", "signing", "broadcast", "real_trade"}


def load_manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def load_json(rel_path):
    return json.loads((ROOT / rel_path).read_text(encoding="utf-8"))


def import_runtime(phase, rel_path):
    spec = importlib.util.spec_from_file_location(f"runtime_{phase.lower()}", ROOT / rel_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_all_standard_stage_runtimes_are_business_bound_not_wrapper_only():
    manifest = load_manifest()
    for phase in PHASES:
        rel_path = manifest["phases"][phase]["runtime_entry"]
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        assert "BusinessBoundStageRuntime" in text, phase
        assert "load_stage_context" in text, phase
        assert "run_semantic_replay" in text, phase
        module = import_runtime(phase, rel_path)
        result = module.run({"run_id": "TEST_BUSINESS_BOUND", "sample_kind": "happy_path"})
        assert result["runtime_mode"] == "paper_only"
        assert result["runtime_depth"] == "BUSINESS_BOUND_RUNTIME"
        assert result["business_binding"]["binding_status"] in {"BOUND_TO_STANDARD_STAGE_CONTEXT", "BLOCKED_WITH_EXPLICIT_REASON"}
        assert result["trace_packet"]["input_hash"]
        assert result["trace_packet"]["source_artifact"]
        assert result["semantic_acceptance"]["status"] in {"SEMANTIC_REPLAY_ACCEPTED", "SEMANTIC_REPLAY_ACCEPTED_WITH_DOWNGRADE"}
        assert set(result["blocked_real_execution"]) == FORBIDDEN


def test_handoff_contracts_are_explicit_phase_chain_not_generic_bootstrap():
    manifest = load_manifest()
    chain = [f"K{i:02d}" for i in range(0, 9)] + [f"P{i:02d}" for i in range(0, 11)] + [f"I{i:02d}" for i in range(1, 6)] + ["R00"]
    for idx, phase in enumerate(chain):
        contract = load_json(manifest["phases"][phase]["contract"])
        handoff = load_json(manifest["phases"][phase]["handoff"])
        expected_upstream = "SYSTEM_BOOTSTRAP" if idx == 0 else f"{chain[idx - 1]}_STANDARD_STAGE_HANDOFF"
        expected_downstream = None if idx == len(chain) - 1 else f"{chain[idx + 1]}_STANDARD_STAGE_INPUT"
        assert contract["input_contract"]["required_upstream_handoff"] == expected_upstream, phase
        assert handoff["next_phase_refs"] == ([] if expected_downstream is None else [chain[idx + 1]]), phase
        assert handoff["downstream_input_contract"] == expected_downstream, phase
        assert handoff["handoff_chain"]["previous_handoff"] == expected_upstream, phase


def test_acceptance_gates_are_semantic_replay_acceptance_not_structure_only():
    manifest = load_manifest()
    required_checks = {
        "schema_validation_replay",
        "happy_path_sample_replay",
        "missing_field_downgrade_replay",
        "conflict_input_blocker_replay",
        "dirty_data_quality_replay",
        "forbidden_action_replay_scan",
        "handoff_contract_field_alignment",
        "trace_evidence_completeness",
    }
    for phase in PHASES:
        acceptance = load_json(manifest["phases"][phase]["acceptance"])
        checks = set(acceptance["semantic_replay_acceptance"]["required_replays"])
        assert required_checks <= checks, phase
        assert acceptance["acceptance_depth"] == "SEMANTIC_REPLAY_ACCEPTANCE", phase
        assert acceptance["status"] == "SEMANTIC_ACCEPTANCE_READY_PAPER_ONLY", phase
        assert acceptance["semantic_replay_acceptance"]["real_execution_allowed"] is False, phase
