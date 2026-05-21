import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "docs/operating_backbone/storage_topology_v0_1"

REQUIRED_FILES = [
    "README.md",
    "VERSION.json",
    "STORAGE_TOPOLOGY_CONTRACT.json",
    "ARTIFACT_CLASSIFICATION_MATRIX.json",
    "RUN_DIRECTORY_CONTRACT.json",
    "CANONICAL_PROMOTION_POLICY.json",
    "ARTIFACT_INDEX_POLICY.json",
    "CONTAMINATION_PREVENTION_RULES.json",
    "ACCEPTANCE_CHECKLIST.json",
]


def load(name):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def test_storage_topology_pack_exists():
    for name in REQUIRED_FILES:
        assert (BASE / name).exists(), name


def test_runs_are_evidence_not_truth_and_canonical_is_gated():
    storage = load("STORAGE_TOPOLOGY_CONTRACT.json")
    principles = "\n".join(storage["principles"])
    assert "new operational artifacts first write to runs/<run_id>" in principles
    assert "canonical/current receives only promotion-gated" in principles
    assert "never glob latest files" in principles
    assert storage["topology"]["runs/<run_id>"] == "isolated run evidence and candidates"
    assert "scratch files" in load("CANONICAL_PROMOTION_POLICY.json")["canonical_current_forbidden_content"]


def test_artifact_classes_preserve_layer_boundaries():
    matrix = load("ARTIFACT_CLASSIFICATION_MATRIX.json")
    classes = {item["class"]: item for item in matrix["artifact_classes"]}
    assert "raw_evidence" in classes
    assert classes["raw_evidence"]["allowed_consumers"] == ["source_to_canonical_mapping"]
    assert "feature_artifact" in classes["raw_evidence"]["forbidden_outputs"]
    assert "structure_signal" in classes["feature_artifact"]["allowed_consumers"] or classes["feature_artifact"]["allowed_consumers"] == ["structure_signal_generation"]
    assert "strategy_behavior" in classes["feature_artifact"]["forbidden_outputs"]
    assert "trade_action" in classes["structure_signal"]["forbidden_outputs"]
    assert "runner_permission_without_ticket" in classes["strategy_contract"]["forbidden_outputs"]


def test_run_directory_contract_requires_run_class_and_manifest_outputs():
    contract = load("RUN_DIRECTORY_CONTRACT.json")
    required = contract["required_manifest_fields"]
    for field in ["run_id", "run_class", "expected_backbone_node", "status", "outputs", "promotion_allowed", "canonical_write_allowed"]:
        assert field in required
    assert "control_plane" in contract["run_classes"]
    assert "data_acquisition" in contract["run_classes"]
    assert "feature_engineering" in contract["run_classes"]
    assert "Consumers must read only paths declared in run_manifest outputs or artifact_index" in contract["read_rule"]
    assert contract["status_rule"]["PATCH_REQUIRED"] == "not promotable"
    assert contract["status_rule"]["BLOCKED"].startswith("not promotable")


def test_promotion_policy_blocks_patch_required_blocked_and_mixed_layers():
    policy = load("CANONICAL_PROMOTION_POLICY.json")
    denied = "\n".join(policy["promotion_denied_if"])
    assert "status PATCH_REQUIRED or BLOCKED" in denied
    assert "lineage missing" in denied
    assert "consumer missing" in denied
    assert "artifact mixes raw/canonical/feature/structure/strategy/paper layers" in denied
    assert "paper result claims live readiness" in denied
    assert "private keys" in policy["canonical_current_forbidden_content"]
    assert "swap/broadcast payloads" in policy["canonical_current_forbidden_content"]


def test_index_policy_forbids_glob_latest_truth():
    policy = load("ARTIFACT_INDEX_POLICY.json")
    forbidden = "\n".join(policy["forbidden_read_patterns"])
    assert "runs/*/outputs/**/*.json as truth" in forbidden
    assert "latest file by mtime as approved artifact" in forbidden
    assert "blocked/PATCH_REQUIRED artifacts as canonical input" in forbidden
    assert "latest_approved_pointers.json" in policy["indexes"]


def test_contamination_rules_cover_core_failure_modes():
    rules = load("CONTAMINATION_PREVENTION_RULES.json")
    text = "\n".join(rule["rule"] for rule in rules["hard_rules"])
    assert "raw evidence cannot be consumed by feature_engineering directly" in text
    assert "feature_artifact cannot contain structure judgment labels" in text
    assert "structure_signal cannot become strategy behavior without strategy_contract" in text
    assert "replay/backtest/paper-only cannot run without valid strategy_contract and decision_ticket" in text
    assert "PATCH_REQUIRED or BLOCKED runs cannot be promoted" in text
    assert "control_plane runs cannot produce GMGN response" in text
    assert "downstream modules cannot glob runs/* as truth" in text
    assert "live/swap/private_key/signing/broadcast artifacts are forbidden" in text
    assert "forbidden_scope" in rules["boundary_terms"]["allowed_as_guardrail_field"]
