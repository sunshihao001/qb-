from pathlib import Path
import json

from sikk_core.run_isolation import create_run_context, write_final_report, verify_run_context
from sikk_core.skill_registry import SkillRegistry, validate_registry_file

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "docs/capability_roadmap/skill_orchestrated_backbone_v0_1/first_batch_control_mapping_baseline"


def test_run_isolation_creates_required_files(tmp_path):
    ctx = create_run_context(
        run_id="test_run_001",
        run_name="TEST_CONTROL_RUN",
        expected_backbone_node="OBN-00",
        allowed_scope=["contract_validation_only"],
        root=tmp_path,
    )
    write_final_report(ctx, "PASS_WITH_GAPS", {"control_layer_only": True})
    result = verify_run_context(ctx.run_dir)
    assert result["status"] == "PASS"
    assert result["missing"] == []
    assert result["unsafe_flags"] == []


def test_run_isolation_baseline_contract_is_closed_by_default():
    path = BASELINE / "control_layer/RUN_ISOLATION_BASELINE.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["default_permissions"]["canonical_write_allowed"] is False
    assert data["default_permissions"]["promotion_allowed"] is False
    assert data["default_permissions"]["runtime_validation_allowed"] is False
    for forbidden in ["gmgn_runtime_call", "feature_generation", "structure_signal_generation", "decision_ticket_generation", "live", "swap", "signing", "broadcast"]:
        assert forbidden in data["forbidden_scope"]


def test_skill_registry_baseline_validates():
    path = BASELINE / "control_layer/SKILL_REGISTRY_BASELINE.json"
    result = validate_registry_file(path)
    assert result["status"] == "PASS", result
    assert result["skill_count"] >= 3


def test_skill_registry_invocation_gate():
    path = BASELINE / "control_layer/SKILL_REGISTRY_BASELINE.json"
    registry = SkillRegistry.from_json_file(path)
    assert registry.invocation_allowed("skill.run_isolation", "OBN-00")["allowed"] is True
    assert registry.invocation_allowed("skill.gmgn_readonly_data_source", "OBN-01")["allowed"] is True
    assert registry.invocation_allowed("skill.gmgn_readonly_data_source", "OBN-00")["allowed"] is False
    assert registry.invocation_allowed("missing.skill", "OBN-01")["allowed"] is False


def test_control_layer_does_not_allow_runtime_forbidden_outputs():
    path = BASELINE / "control_layer/SKILL_REGISTRY_BASELINE.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    forbidden = ["BUY", "SELL", "EXECUTE", "LIVE_READY", "SWAP_READY", "PAPER_READY"]
    for skill in data["skills"]:
        outputs = " ".join(skill.get("output_artifacts", [])).upper()
        for word in forbidden:
            assert word not in outputs
