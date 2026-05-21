import json
from pathlib import Path

from sikk_core.run_isolation import create_run_context
from sikk_core.skill_registry import SkillRegistry
from sikk_core.orchestrator_skeleton import evaluate_orchestrator_gate

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/operating_backbone/invocation_contracts_v0_1"
REGISTRY_PATH = ROOT / "docs/capability_roadmap/skill_orchestrated_backbone_v0_1/first_batch_control_mapping_baseline/control_layer/SKILL_REGISTRY_BASELINE.json"

REQUIRED_FILES = [
    "INVOCATION_ENVELOPE_CONTRACT.json",
    "ORCHESTRATOR_GATE_RESULT_CONTRACT.json",
    "STORAGE_POLICY_GATE_RESULT_CONTRACT.json",
    "GMGN_READONLY_DRY_RUN_ENVELOPE_EXAMPLE.json",
    "ACCEPTANCE_CHECKLIST.json",
]


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def test_requested_invocation_contract_files_exist():
    for name in REQUIRED_FILES:
        assert (BASE / name).exists(), name


def test_invocation_envelope_contract_requires_storage_fields_and_non_runtime_flags():
    contract = load("INVOCATION_ENVELOPE_CONTRACT.json")
    required = set(contract["required_fields"])
    for field in ["artifact_class", "target_paths", "read_paths", "promotion_requested", "canonical_write_requested", "execution_requested", "runtime_action_allowed"]:
        assert field in required
    assert contract["field_contract"]["promotion_requested"]["required_value"] is False
    assert contract["field_contract"]["canonical_write_requested"]["required_value"] is False
    assert contract["field_contract"]["execution_requested"]["required_value"] is False
    assert contract["field_contract"]["runtime_action_allowed"]["required_value"] is False
    forbidden = "\n".join(contract["forbidden"])
    for term in ["GMGN call", "feature_generation", "PAPER_READY", "live", "swap", "signing", "broadcast"]:
        assert term in forbidden


def test_orchestrator_gate_result_contract_requires_non_runtime_evidence():
    contract = load("ORCHESTRATOR_GATE_RESULT_CONTRACT.json")
    required = set(contract["required_fields"])
    for field in ["registry_check", "invocation_check", "envelope_check", "storage_policy_check", "patch_reasons", "block_reasons"]:
        assert field in required
    for flag in ["runtime_action_executed", "gmgn_called", "feature_generated", "structure_signal_generated", "decision_ticket_generated", "paper_validation_executed", "canonical_promoted"]:
        assert flag in contract["non_runtime_flags_required_false"]
    assert "PASS" in contract["status_allowed_values"]
    assert "PATCH_REQUIRED" in contract["status_allowed_values"]
    assert "BLOCKED" in contract["status_allowed_values"]
    assert "not target skill execution" in contract["forbidden_interpretation"]


def test_storage_policy_gate_result_contract_covers_storage_contamination_modes():
    contract = load("STORAGE_POLICY_GATE_RESULT_CONTRACT.json")
    required = set(contract["required_fields"])
    for field in ["artifact_class", "bad_target_paths", "bad_consumers", "forbidden_output_hits", "forbidden_read_patterns", "patch_reasons", "block_reasons"]:
        assert field in required
    blocked = "\n".join(contract["blocked_conditions"])
    for phrase in ["artifact_class not registered", "target path not allowed", "consumer not allowed", "forbidden output requested", "promotion/canonical write requested", "forbidden read pattern detected"]:
        assert phrase in blocked
    forbidden_reads = "\n".join(contract["forbidden_read_patterns"])
    assert "runs/* as truth" in forbidden_reads
    assert "latest file by mtime" in forbidden_reads


def test_gmgn_readonly_dry_run_example_is_safe_and_gate_passes(tmp_path):
    example = load("GMGN_READONLY_DRY_RUN_ENVELOPE_EXAMPLE.json")
    assert example["skill_id"] == "skill.gmgn_readonly_data_source"
    assert example["expected_backbone_node"] == "OBN-01"
    assert example["artifact_class"] == "raw_evidence"
    assert example["downstream_consumers"] == ["source_to_canonical_mapping"]
    assert example["promotion_requested"] is False
    assert example["canonical_write_requested"] is False
    assert example["execution_requested"] is False
    assert example["runtime_action_allowed"] is False
    assert example["metadata"]["dry_run_only"] is True
    assert example["metadata"]["real_data_acquisition_allowed"] is False
    for path in example["target_paths"]:
        assert path.startswith("evidence/")
    ctx = create_run_context(
        run_id="gmgn_readonly_dry_run_contract_test",
        run_name="GMGN_READONLY_DRY_RUN_CONTRACT_TEST",
        expected_backbone_node="OBN-01",
        allowed_scope=example["allowed_scope"],
        root=tmp_path,
    )
    result = evaluate_orchestrator_gate(
        ctx=ctx,
        registry=SkillRegistry.from_json_file(REGISTRY_PATH),
        envelope=example,
    )
    assert result["status"] == "PASS", result
    assert result["gmgn_called"] is False
    assert result["runtime_action_executed"] is False
    assert result["canonical_promoted"] is False
    assert result["storage_policy_check"]["status"] == "PASS"


def test_acceptance_checklist_covers_requested_contract_pack():
    checklist = load("ACCEPTANCE_CHECKLIST.json")
    text = "\n".join(checklist["checklist"])
    for name in REQUIRED_FILES:
        assert name in text
    forbidden = "\n".join(checklist["forbidden_actions"])
    for term in ["GMGN call", "raw evidence acquisition", "canonical/current promotion", "feature_generation", "structure_signal_generation", "decision_ticket_generation", "live/swap/private_key/signing/broadcast"]:
        assert term in forbidden
