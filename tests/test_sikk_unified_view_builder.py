import json
from pathlib import Path

import sikk_unified_view_builder as unified


BASE = Path("data/gmgn_candidates_live_run")


def test_build_unified_indexes_writes_required_index_files(tmp_path):
    result = unified.build_unified_indexes(BASE)

    index_dir = BASE / "index"
    required = [
        "system_index.json",
        "token_detail_index.json",
        "position_index.json",
        "latest_open_positions.json",
        "latest_closed_positions.json",
        "case_file_index.json",
        "auto_review_index.json",
        "alert_index.json",
        "telegram_callback_index.json",
    ]
    assert result["index_dir"] == str(index_dir)
    for name in required:
        path = index_dir / name
        assert path.exists(), name
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["schema_version"].startswith("sikk.unified_view.")
        assert "只读" in payload["boundary"]
        assert payload["safety"]["real_swap_enabled"] is False
        assert payload["safety"]["broadcast_allowed"] is False
        assert payload["safety"]["private_key_required"] is False


def test_system_index_summarizes_single_entry_outputs_and_paper_sync():
    system = unified.build_unified_indexes(BASE)["system_index"]

    assert system["entrypoint"]["canonical"] == "sikk_live_run.py"
    assert system["paper_sync"]["open_json_count"] >= 0
    assert system["paper_sync"]["closed_json_count"] >= 0
    assert system["paper_sync"]["open_csv_exists"] is True
    assert system["paper_sync"]["closed_csv_exists"] is True
    assert system["site_outputs"]["dashboard_data_json"].endswith("site/dashboard_data.json")
    assert system["runtime_outputs"]["live_state_json"].endswith("live_state.json")
    assert system["wallet_daily_report"]["latest_csv"].endswith(".csv")
    assert system["counts"]["token_count"] > 0
    assert system["counts"]["open_position_count"] == system["paper_sync"]["open_json_count"]
    assert system["counts"]["closed_position_count"] == system["paper_sync"]["closed_json_count"]


def test_token_and_position_indexes_are_query_friendly_and_chinese_labeled():
    result = unified.build_unified_indexes(BASE)
    token_index = result["token_detail_index"]
    position_index = result["position_index"]

    assert token_index["tokens"]
    first = token_index["tokens"][0]
    for key in ["token_id", "token_address", "token_symbol", "状态", "信号等级", "钱包结构", "主导侧心理", "安全边界"]:
        assert key in first
    assert "不执行真实 swap" in first["安全边界"]

    assert "open_positions" in position_index
    assert "closed_positions" in position_index
    assert position_index["open_count"] == len(position_index["open_positions"])
    assert position_index["closed_count"] == len(position_index["closed_positions"])


def test_telegram_callback_index_uses_short_codes_not_long_addresses_or_chinese_callbacks():
    cb = unified.build_unified_indexes(BASE)["telegram_callback_index"]

    assert cb["callbacks"]
    assert "menu:main" in cb["callbacks"]
    for code, target in cb["callbacks"].items():
        assert len(code.encode("utf-8")) <= 32
        assert not any("\u4e00" <= ch <= "\u9fff" for ch in code)
        assert ":" in code
        assert target["type"] in {"menu", "token", "position", "entry_evidence", "case", "review", "alert", "list", "refresh"}


def test_unified_indexes_expose_case_quality_and_missing_evidence(tmp_path):
    base = tmp_path / "run"
    paper = base / "paper_live"
    case_dir = paper / "case_files"
    case_dir.mkdir(parents=True)
    (base / "site").mkdir(parents=True)
    position = {
        "position_id": "paper-case-quality-1",
        "token_address": "TokenQuality111",
        "token_symbol": "QUAL",
        "case_quality_level": "E2_REVIEWABLE",
        "case_completeness_score": 78.5,
        "case_field_source_count": 9,
        "case_field_sources_preview": ["paper_live/paper_positions_open.json", "live_state.json"],
        "evidence_missing_fields": ["exit_reason", "funding_path"],
        "strategy_review_eligible": False,
    }
    (base / "site" / "dashboard_data.json").write_text(json.dumps({"tokens": [], "paper_positions": {"open": [position], "closed": []}}, ensure_ascii=False), encoding="utf-8")
    (paper / "paper_positions_open.json").write_text(json.dumps({"open_positions": [position]}, ensure_ascii=False), encoding="utf-8")
    (paper / "paper_positions_closed.json").write_text(json.dumps({"closed_positions": []}, ensure_ascii=False), encoding="utf-8")
    (case_dir / "case_files_manifest.json").write_text(json.dumps({"case_files": [dict(position, case_file_json="case.json", case_file_md="case.md")]}, ensure_ascii=False), encoding="utf-8")

    result = unified.build_unified_indexes(base)
    pos = result["position_index"]["open_positions"][0]
    case = result["case_file_index"]["cases"][0]

    for item in (pos, case):
        assert item["case_quality_level"] == "E2_REVIEWABLE"
        assert item["case_completeness_score"] == 78.5
        assert item["case_field_source_count"] == 9
        assert item["evidence_missing_fields"] == ["exit_reason", "funding_path"]
    assert pos["安全边界"].startswith("SIKK 统一索引层")

def test_alert_index_is_readonly_and_has_no_trade_actions():
    alerts = unified.build_unified_indexes(BASE)["alert_index"]

    forbidden = {"BUY", "SELL", "SWAP", "EXECUTE", "APPROVE", "BROADCAST"}
    alert_text = json.dumps(alerts["alerts"], ensure_ascii=False).upper()
    for word in forbidden:
        assert word not in alert_text
    assert alerts["alert_count"] == len(alerts["alerts"])
    for alert in alerts["alerts"]:
        assert alert["action"] in {"记录", "观察", "复查", "暂停纸面入场", "退出监控", "数据补全"}
