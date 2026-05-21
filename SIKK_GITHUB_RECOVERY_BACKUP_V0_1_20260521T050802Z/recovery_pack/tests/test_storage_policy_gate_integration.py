from pathlib import Path

from sikk_core.run_isolation import create_run_context
from sikk_core.skill_registry import SkillRegistry
from sikk_core.orchestrator_skeleton import (
    build_invocation_envelope,
    evaluate_orchestrator_gate,
    evaluate_storage_policy_gate,
    load_storage_policy_contracts,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "docs/capability_roadmap/skill_orchestrated_backbone_v0_1/first_batch_control_mapping_baseline/control_layer/SKILL_REGISTRY_BASELINE.json"


def load_registry():
    return SkillRegistry.from_json_file(REGISTRY_PATH)


def make_ctx(tmp_path, run_id="storage_gate_001"):
    return create_run_context(
        run_id=run_id,
        run_name="STORAGE_POLICY_GATE_TEST",
        expected_backbone_node="OBN-00",
        allowed_scope=["control_layer_initialization"],
        root=tmp_path,
    )


def test_storage_policy_gate_passes_control_plane_envelope(tmp_path):
    ctx = make_ctx(tmp_path, "storage_gate_pass_001")
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.run_isolation",
        expected_backbone_node="OBN-00",
        allowed_scope=["control_layer_initialization"],
        forbidden_scope=["gmgn_runtime_call", "feature_generation", "live", "swap", "signing", "broadcast"],
        input_artifacts=["operational_brief"],
        output_artifacts=["run_manifest.yaml", "audit_log.jsonl", "final_run_report.yaml"],
        downstream_consumers=["orchestrator_skeleton"],
        artifact_class="control_plane",
        target_paths=["control/run_manifest.yaml", "reports/final_run_report.yaml"],
        read_paths=[],
        invocation_context="control_layer_initialization",
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "PASS", result
    assert result["storage_policy_enforced"] is True
    assert result["storage_policy_check"]["status"] == "PASS"
    assert result["canonical_promoted"] is False


def test_storage_policy_gate_patch_required_when_artifact_class_missing(tmp_path):
    ctx = make_ctx(tmp_path, "storage_gate_patch_001")
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.skill_registry",
        expected_backbone_node="OBN-00",
        allowed_scope=["contract_lookup"],
        forbidden_scope=["live", "swap", "signing", "broadcast"],
        input_artifacts=["skill_contract_record"],
        output_artifacts=["registry_validation_report"],
        downstream_consumers=["orchestrator_skeleton"],
        target_paths=["control/registry_validation_report.json"],
        invocation_context="preflight_gate",
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "PATCH_REQUIRED", result
    assert "storage_policy_patch_required" in result["patch_reasons"]
    assert "artifact_class_missing" in result["storage_policy_check"]["patch_reasons"]


def test_storage_policy_gate_blocks_unknown_artifact_class(tmp_path):
    ctx = make_ctx(tmp_path, "storage_gate_unknown_class_001")
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.run_isolation",
        expected_backbone_node="OBN-00",
        allowed_scope=["control_layer_initialization"],
        forbidden_scope=["live", "swap"],
        input_artifacts=["x"],
        output_artifacts=["y"],
        downstream_consumers=["orchestrator_skeleton"],
        artifact_class="made_up_artifact",
        target_paths=["control/x.json"],
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "BLOCKED", result
    assert "storage_policy_blocked" in result["block_reasons"]
    assert "artifact_class_not_registered" in result["storage_policy_check"]["block_reasons"]


def test_storage_policy_gate_blocks_wrong_target_path_for_raw_evidence(tmp_path):
    ctx = make_ctx(tmp_path, "storage_gate_bad_path_001")
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.gmgn_readonly_data_source",
        expected_backbone_node="OBN-01",
        allowed_scope=["future_obn_01_read_only_raw_evidence_run"],
        forbidden_scope=["swap", "signing", "broadcast"],
        input_artifacts=["approved_run_context", "source_query_spec"],
        output_artifacts=["raw_request_evidence", "raw_response_evidence"],
        downstream_consumers=["source_to_canonical_mapping"],
        artifact_class="raw_evidence",
        target_paths=["features/raw_response.json"],
        invocation_context="future_obn_01_read_only_raw_evidence_run",
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "BLOCKED", result
    assert "target_path_not_allowed_for_artifact_class" in result["storage_policy_check"]["block_reasons"]
    assert "features/raw_response.json" in result["storage_policy_check"]["bad_target_paths"]
    assert result["gmgn_called"] is False


def test_storage_policy_gate_blocks_bad_consumer_for_raw_evidence(tmp_path):
    ctx = make_ctx(tmp_path, "storage_gate_bad_consumer_001")
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.gmgn_readonly_data_source",
        expected_backbone_node="OBN-01",
        allowed_scope=["future_obn_01_read_only_raw_evidence_run"],
        forbidden_scope=["swap", "signing", "broadcast"],
        input_artifacts=["approved_run_context", "source_query_spec"],
        output_artifacts=["raw_response_evidence"],
        downstream_consumers=["feature_engineering"],
        artifact_class="raw_evidence",
        target_paths=["evidence/response/gmgn_response.json"],
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "BLOCKED", result
    assert "downstream_consumer_not_allowed_for_artifact_class" in result["storage_policy_check"]["block_reasons"]
    assert "feature_engineering" in result["storage_policy_check"]["bad_consumers"]


def test_storage_policy_gate_blocks_forbidden_control_plane_outputs(tmp_path):
    ctx = make_ctx(tmp_path, "storage_gate_forbidden_output_001")
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.run_isolation",
        expected_backbone_node="OBN-00",
        allowed_scope=["control_layer_initialization"],
        forbidden_scope=["live", "swap"],
        input_artifacts=["operational_brief"],
        output_artifacts=["feature_artifact"],
        downstream_consumers=["orchestrator_skeleton"],
        artifact_class="control_plane",
        target_paths=["control/feature_artifact.json"],
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "BLOCKED", result
    assert "forbidden_output_for_artifact_class" in result["storage_policy_check"]["block_reasons"]
    assert "feature_artifact" in result["storage_policy_check"]["forbidden_output_hits"]


def test_storage_policy_gate_blocks_promotion_and_canonical_write_request(tmp_path):
    ctx = make_ctx(tmp_path, "storage_gate_promotion_001")
    envelope = build_invocation_envelope(
        run_id=ctx.run_id,
        skill_id="skill.run_isolation",
        expected_backbone_node="OBN-00",
        allowed_scope=["control_layer_initialization"],
        forbidden_scope=["live", "swap"],
        input_artifacts=["operational_brief"],
        output_artifacts=["run_manifest.yaml"],
        downstream_consumers=["orchestrator_skeleton"],
        artifact_class="control_plane",
        target_paths=["control/run_manifest.yaml"],
        promotion_requested=True,
        canonical_write_requested=True,
    )
    result = evaluate_orchestrator_gate(ctx=ctx, registry=load_registry(), envelope=envelope)
    assert result["status"] == "BLOCKED", result
    assert "promotion_or_canonical_write_requested_without_promotion_gate" in result["storage_policy_check"]["block_reasons"]
    assert result["canonical_promoted"] is False


def test_storage_policy_gate_blocks_forbidden_read_patterns():
    envelope = build_invocation_envelope(
        run_id="read_policy_001",
        skill_id="skill.skill_registry",
        expected_backbone_node="OBN-00",
        allowed_scope=["contract_lookup"],
        forbidden_scope=["live", "swap"],
        input_artifacts=["artifact_index"],
        output_artifacts=["registry_validation_report"],
        downstream_consumers=["orchestrator_skeleton"],
        artifact_class="control_plane",
        target_paths=["control/registry_validation_report.json"],
        read_paths=["data/operating_backbone/runs/*/outputs/**/*.json", "latest_file_by_mtime.json"],
    )
    check = evaluate_storage_policy_gate(envelope, load_storage_policy_contracts())
    assert check["status"] == "BLOCKED", check
    assert "forbidden_read_pattern_detected" in check["block_reasons"]
    assert "data/operating_backbone/runs/*/outputs/**/*.json" in check["forbidden_read_patterns"]
