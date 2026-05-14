from pathlib import Path
import json

import pytest

from modules.wallet_data_guard.contracts import (
    CANONICAL_WALLET_ROUTE,
    COMPATIBILITY_ROUTES,
    SemanticLayer,
    ProducerType,
)
from modules.wallet_data_guard.write_gate import validate_write_contract, write_controlled_artifact, WriteGateError
from modules.wallet_data_guard.source_manifest import build_source_manifest, validate_source_manifest
from modules.wallet_data_guard.contamination_scan import scan_wallet_data_contamination


def test_wallet_data_guard_declares_canonical_and_compat_routes():
    assert CANONICAL_WALLET_ROUTE[:3] == [
        "modules/source_wallet_bot",
        "sikk_candidate_wallet_structure_pipeline.py",
        "sikk_wallet_structure_gate.py",
    ]
    assert COMPATIBILITY_ROUTES["sikk_sol_full_auto_workflow.py"] == "legacy_compat_one_shot"


def test_write_gate_rejects_inference_written_to_facts(tmp_path):
    target = tmp_path / "wallet_data" / "facts" / "wallet_facts.json"
    with pytest.raises(WriteGateError) as exc:
        validate_write_contract(
            path=target,
            layer=SemanticLayer.FACTS,
            producer=ProducerType.ANALYZER,
            payload={"wallet_address": "W1", "dominant_lifecycle": "accumulation"},
            source_refs=["raw:gmgn_holders"],
            task_passport="passport.md",
        )
    assert "inference-like field" in str(exc.value)


def test_write_gate_allows_collector_raw_with_source_refs(tmp_path):
    target = tmp_path / "wallet_data" / "raw" / "gmgn_holders.json"
    result = write_controlled_artifact(
        path=target,
        layer=SemanticLayer.RAW,
        producer=ProducerType.COLLECTOR,
        payload={"rows": [{"wallet_address": "W1"}]},
        source_refs=["gmgn:holders"],
        task_passport="passport.md",
    )
    assert Path(result["path"]).exists()
    stored = json.loads(Path(result["path"]).read_text(encoding="utf-8"))
    assert stored["guard_metadata"]["semantic_layer"] == "raw"
    assert stored["guard_metadata"]["backwrite_allowed"] is False


def test_source_manifest_validates_required_fields():
    manifest = build_source_manifest(
        source_id="gmgn_holders_001",
        source_type="gmgn",
        token_address="Token111",
        raw_path="wallet_data/raw/gmgn_holders.json",
        normalized_path="wallet_data/normalized/gmgn_holders.normalized.json",
        allowed_layers=[SemanticLayer.RAW, SemanticLayer.FACTS],
    )
    validation = validate_source_manifest(manifest)
    assert validation["status"] == "PASS"
    assert "inference" in manifest["blocked_layers"]


def test_contamination_scan_flags_cross_layer_pollution(tmp_path):
    token_root = tmp_path / "data" / "source_wallet_bot" / "paper" / "Token111"
    facts_dir = token_root / "wallet_data" / "facts"
    facts_dir.mkdir(parents=True)
    (facts_dir / "polluted_facts.json").write_text(json.dumps({
        "wallet_address": "W1",
        "inference": "疑似控筹",
        "final_state": "WATCHING",
    }, ensure_ascii=False), encoding="utf-8")

    legacy_fb = token_root / "wallet_data" / "legacy_fallback"
    legacy_fb.mkdir(parents=True)
    (legacy_fb / "fallback.json").write_text(json.dumps({
        "fallback_source": "old_path",
        "read_mode": "readonly",
    }, ensure_ascii=False), encoding="utf-8")

    compat = tmp_path / "data" / "sikk_sol_full_auto_workflow" / "run1" / "state_machine"
    compat.mkdir(parents=True)
    (compat / "wallet_structure_decision.json").write_text(json.dumps({"final_state": "PAPER_READY"}), encoding="utf-8")

    report = scan_wallet_data_contamination(tmp_path / "data")
    issue_codes = {issue["code"] for issue in report["issues"]}
    assert "INFERENCE_FIELD_IN_FACTS" in issue_codes
    assert "STATE_FIELD_IN_WALLET_DATA" in issue_codes
    assert "LEGACY_FALLBACK_MISSING_MAPPING_ID" in issue_codes
    assert "COMPAT_ROUTE_CANONICAL_DECISION" in issue_codes
    assert report["overall_status"] == "FAIL"


def test_contamination_scan_passes_clean_guarded_artifacts(tmp_path):
    token_root = tmp_path / "data" / "source_wallet_bot" / "paper" / "Token222"
    write_controlled_artifact(
        path=token_root / "wallet_data" / "raw" / "gmgn.json",
        layer=SemanticLayer.RAW,
        producer=ProducerType.COLLECTOR,
        payload={"rows": []},
        source_refs=["gmgn:holders"],
        task_passport="passport.md",
    )
    write_controlled_artifact(
        path=token_root / "structure_analysis" / "handoff" / "wallet_handoff.json",
        layer=SemanticLayer.HANDOFF,
        producer=ProducerType.GATE,
        payload={"wallet_structure_status": "WALLET_SUPPORT", "evidence_refs": ["facts:1"]},
        source_refs=["evidence:wallet_structure"],
        task_passport="passport.md",
    )
    report = scan_wallet_data_contamination(tmp_path / "data")
    assert report["overall_status"] == "PASS"
    assert report["issues"] == []
