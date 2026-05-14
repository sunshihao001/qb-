import json
from pathlib import Path


def test_legacy_quarantine_index_tracks_issues_without_failing_scan(tmp_path):
    from modules.wallet_data_guard import scan_wallet_data_contamination
    from modules.wallet_data_guard.legacy_quarantine import build_legacy_quarantine_index

    root = tmp_path / "source_wallet_bot"
    legacy_raw = root / "legacy" / "TOKEN1" / "wallet_data" / "raw" / "bad.json"
    legacy_raw.parent.mkdir(parents=True)
    legacy_raw.write_text(json.dumps({"wallet_structure_status": "WALLET_BLOCK", "raw_value": 1}), encoding="utf-8")
    paper_raw = root / "paper" / "TOKEN2" / "wallet_data" / "raw" / "ok.json"
    paper_raw.parent.mkdir(parents=True)
    paper_raw.write_text(json.dumps({"raw_value": 2}), encoding="utf-8")

    report = scan_wallet_data_contamination(root)

    assert report["overall_status"] == "PASS_WITH_LEGACY_QUARANTINE"
    assert report["legacy_quarantine"]["legacy_issues_count"] == 1
    assert report["active_issues_count"] == 0

    index = build_legacy_quarantine_index(root, report=report, output_dir=tmp_path / "out")
    assert index["artifact_type"] == "legacy_contamination_quarantine_index"
    assert index["status"] == "ACTIVE_QUARANTINE"
    assert index["policy"]["delete_old_files"] is False
    assert index["policy"]["move_old_files"] is False
    assert index["legacy_issues_count"] == 1
    assert index["active_issues_count"] == 0
    assert Path(index["json_path"]).exists()


def test_active_lower_layer_contamination_still_fails(tmp_path):
    from modules.wallet_data_guard import scan_wallet_data_contamination

    root = tmp_path / "source_wallet_bot"
    active_raw = root / "paper" / "TOKEN1" / "wallet_data" / "raw" / "bad.json"
    active_raw.parent.mkdir(parents=True)
    active_raw.write_text(json.dumps({"wallet_structure_status": "WALLET_BLOCK"}), encoding="utf-8")

    report = scan_wallet_data_contamination(root)

    assert report["overall_status"] == "FAIL"
    assert report["active_issues_count"] == 1
    assert report["legacy_quarantine"]["legacy_issues_count"] == 0
