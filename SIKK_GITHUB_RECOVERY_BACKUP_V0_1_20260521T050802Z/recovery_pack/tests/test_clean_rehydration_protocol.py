import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC_DIR = ROOT / "docs/operating_backbone/clean_rehydration_v0_1"
POINTER = ROOT / "data/operating_backbone/canonical/current/CURRENT_STATE_POINTER.json"
REQUIRED_DOCS = ["CLEAN_START_PROTOCOL.md","CURRENT_STATE_POINTER_CONTRACT.json","READ_ALLOWLIST_POLICY.json","LEGACY_QUARANTINE_POLICY.json","CONTAMINATION_CHECKLIST.json","ACCEPTANCE_CHECKLIST.json"]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def test_clean_rehydration_pack_files_exist():
    for name in REQUIRED_DOCS:
        assert (DOC_DIR / name).exists(), name
    assert POINTER.exists()

def test_current_state_pointer_contract_required_fields():
    contract = load(DOC_DIR / "CURRENT_STATE_POINTER_CONTRACT.json")
    required = set(contract["required_fields"])
    for field in ["artifact_type", "version", "status", "approved_at_utc", "contract_registry", "skill_registry", "storage_policy", "latest_approved_runs", "forbidden_default_reads"]:
        assert field in required
    forbidden = "\n".join(contract["forbidden_fields"])
    for term in ["private_key", "signature", "swap_payload", "broadcast_payload", "feature_values", "structure_score"]:
        assert term in forbidden

def test_current_pointer_references_approved_paths_and_explicit_runs():
    pointer = load(POINTER)
    assert pointer["status"] == "APPROVED_CURRENT"
    for key in ["clean_rehydration_protocol", "contract_registry", "skill_registry", "storage_policy"]:
        path = ROOT / pointer[key]["path"]
        assert path.exists(), (key, path)
    assert pointer["latest_approved_runs"]
    for run in pointer["latest_approved_runs"]:
        assert "run_id" in run
        assert "path" in run
        assert "mtime" not in json.dumps(run).lower()
    forbidden = "\n".join(pointer["forbidden_default_reads"])
    assert "runs/*" in forbidden
    assert "quarantine" in forbidden
    assert "archive" in forbidden
    assert "mtime" in forbidden

def test_read_allowlist_blocks_old_data_pollution_patterns():
    policy = load(DOC_DIR / "READ_ALLOWLIST_POLICY.json")
    forbidden = "\n".join(policy["forbidden_default_reads"])
    for phrase in ["runs/*", "quarantine", "archive", "mtime", "old decision_ticket", "old feature_artifact", "old raw_evidence"]:
        assert phrase in forbidden
    conditional = json.dumps(policy["conditional_reads"])
    assert "CURRENT_STATE_POINTER" in conditional
    assert "explicit task packet" in conditional

def test_legacy_policy_quarantines_unknown_lineage_and_blocks_runtime_use():
    policy = load(DOC_DIR / "LEGACY_QUARANTINE_POLICY.json")
    text = json.dumps(policy, ensure_ascii=False)
    for term in ["UNKNOWN_LINEAGE", "DEPRECATED", "quarantine", "do_not_consume_as_current", "BLOCKED"]:
        assert term in text
    forbidden = "\n".join(policy["forbidden_uses_of_legacy_data"])
    for term in ["current truth", "runtime input", "feature input", "decision_ticket approval", "paper readiness"]:
        assert term in forbidden

def test_contamination_checklist_blocks_bypass_and_runtime_scope():
    checklist = load(DOC_DIR / "CONTAMINATION_CHECKLIST.json")
    text = json.dumps(checklist, ensure_ascii=False)
    for term in ["runs/* glob", "quarantine", "archive", "mtime", "GMGN acquisition", "Operational Brief", "live/swap/private_key/signing/broadcast"]:
        assert term in text
    assert "does not authorize GMGN call" in checklist["forbidden_interpretation"]

def test_acceptance_checklist_covers_control_pack_and_forbidden_actions():
    checklist = load(DOC_DIR / "ACCEPTANCE_CHECKLIST.json")
    text = "\n".join(checklist["checklist"])
    for name in REQUIRED_DOCS:
        assert name in text
    forbidden = "\n".join(checklist["forbidden_actions"])
    for term in ["GMGN call", "raw evidence acquisition", "feature_generation", "decision_ticket_generation", "paper_validation", "live/swap/private_key/signing/broadcast"]:
        assert term in forbidden
