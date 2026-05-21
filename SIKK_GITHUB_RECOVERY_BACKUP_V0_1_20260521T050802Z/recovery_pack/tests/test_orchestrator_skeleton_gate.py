from pathlib import Path
import json

from sikk_core.run_isolation import create_run_context, write_final_report
from sikk_core.skill_registry import SkillRegistry
from sikk_core.orchestrator_skeleton import (
    build_invocation_envelope,
    evaluate_orchestrator_gate,
    write_gate_artifacts,
)

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs/capability_roadmap/skill_orchestrated_backbone_v0_1/first_batch_control_mapping_baseline/control_layer"
REGISTRY_PATH = BASELINE / "SKILL_REGISTRY_BASELINE.json"
ORCH_BASELINE = BASELINE / "ORCHESTRATOR_SKELETON_GATE.json"


def load_registry():
    return SkillRegistry.from_json_file(REGISTRY_PATH)


def test_orchestrator_baseline_contract_exists_and_forbids_runtime():
    data = json.loads(ORCH_BASELINE.read_text(encoding="utf-8"))
    assert data["artifact_type"] == "orchestrator_skeleton_gate_baseline"
    for field in ["run_id", "skill_id", "expected_backbone_node", "input_artifacts", "output_artifacts", "downstream_consumers"]:
        assert field in data["input_contract"]
    for forbidden in ["GMGN runtime call", "feature generation", "structure_signal generation", "decision_ticket generation", "live trading", "swap", "signing", "broadcast"]:
        assert forbidden in data["forbidden_actions"]


def test_orchestrator_gate_passes_registered_control_skill(tmp_path):
    ctx = create_run_context(
        run_id="orch_pass_001",
        run_name="ORCH_PASS",
        expected_backbone_node="OBN-00",
        allowed_scope=["control_layer_initialization", "artifact_validation"],
        root=tmp_path,
    )
    registry = load_registry()
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.run_isolation",
        expected_backbone_node="OBN-00",
        allowed_scope=["control_layer_initialization", "artifact_validation"],
        forbidden_scope=["gmgn_runtime_call", "feature_generation", "live", "swap", "signing", "broadcast"],
        input_artifacts=["operational_brief", "allowed_scope", "forbidden_scope"],
        output_artifacts=["run_manifest.yaml", "audit_log.jsonl", "final_run_report.yaml"],
        downstream_consumers=["orchestrator_skeleton"],
        invocation_context="control_layer_initialization",
        artifact_class="control_plane",
        target_paths=["control/run_manifest.yaml", "control/audit_log.jsonl", "reports/final_run_report.yaml"],
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=registry, envelope=envelope)
    paths = write_gate_artifacts(ctx, envelope, result)
    write_final_report(ctx, "PASS", {"orchestrator_gate_passed": result["status"] == "PASS"}, outputs=list(paths.values()))
    assert result["status"] == "PASS", result
    assert result["runtime_action_executed"] is False
    assert result["gmgn_called"] is False
    assert Path(paths["invocation_envelope"]).exists()
    assert Path(paths["orchestrator_gate_result"]).exists()


def test_orchestrator_gate_patch_required_for_missing_contracts(tmp_path):
    ctx = create_run_context(
        run_id="orch_patch_001",
        run_name="ORCH_PATCH",
        expected_backbone_node="OBN-00",
        allowed_scope=["contract_lookup"],
        root=tmp_path,
    )
    registry = load_registry()
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.skill_registry",
        expected_backbone_node="OBN-00",
        allowed_scope=["contract_lookup"],
        forbidden_scope=["gmgn_runtime_call", "feature_generation", "live", "swap"],
        input_artifacts=[],
        output_artifacts=["registry_validation_report"],
        downstream_consumers=[],
        invocation_context="preflight_gate",
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=registry, envelope=envelope)
    assert result["status"] == "PATCH_REQUIRED", result
    assert "input_artifacts" in result["envelope_check"]["empty_required_fields"]
    assert "downstream_consumers" in result["envelope_check"]["empty_required_fields"]
    assert result["runtime_action_executed"] is False


def test_orchestrator_gate_blocks_unregistered_skill(tmp_path):
    ctx = create_run_context(
        run_id="orch_block_missing_001",
        run_name="ORCH_BLOCK_MISSING",
        expected_backbone_node="OBN-00",
        allowed_scope=["contract_lookup"],
        root=tmp_path,
    )
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.not_registered",
        expected_backbone_node="OBN-00",
        allowed_scope=["contract_lookup"],
        forbidden_scope=["live", "swap", "signing", "broadcast"],
        input_artifacts=["x"],
        output_artifacts=["y"],
        downstream_consumers=["z"],
        invocation_context="preflight_gate",
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "BLOCKED", result
    assert "skill_not_registered" in result["block_reasons"]


def test_orchestrator_gate_blocks_backbone_mismatch_and_live_scope(tmp_path):
    ctx = create_run_context(
        run_id="orch_block_live_001",
        run_name="ORCH_BLOCK_LIVE",
        expected_backbone_node="OBN-00",
        allowed_scope=["contract_lookup"],
        root=tmp_path,
    )
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.gmgn_readonly_data_source",
        expected_backbone_node="OBN-00",
        allowed_scope=["live", "swap", "gmgn_runtime_call"],
        forbidden_scope=["live", "swap", "signing", "broadcast"],
        input_artifacts=["approved_run_context", "source_query_spec"],
        output_artifacts=["raw_request_evidence", "raw_response_evidence"],
        downstream_consumers=["source_to_canonical_mapping_skill"],
        invocation_context="preflight_gate",
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "BLOCKED", result
    assert "backbone_node_mismatch" in result["block_reasons"]
    assert "hard_forbidden_scope_detected" in result["block_reasons"]
    assert "live" in result["hard_forbidden_hits"]
    assert result["gmgn_called"] is False
    assert result["feature_generated"] is False
    assert result["paper_validation_executed"] is False
