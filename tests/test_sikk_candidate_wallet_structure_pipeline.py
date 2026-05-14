import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_candidate_wallet_structure_pipeline_processes_only_paper_ready_and_writes_v1_outputs(tmp_path):
    from sikk_candidate_wallet_structure_pipeline import run_candidate_wallet_structure_pipeline

    token_support = "TokenSupport111111111111111111111111111111"
    token_block = "TokenBlock1111111111111111111111111111111"
    token_watch = "TokenWatch11111111111111111111111111111111"
    states = _write_json(
        tmp_path / "state_machine" / "candidate_states.json",
        {
            "候选状态": [
                {
                    "代币地址": token_support,
                    "代币符号": "SUP",
                    "当前状态": "PAPER_READY",
                    "信号门禁": "PASS",
                    "报价门禁": "PASS",
                    "安全门禁": "PASS",
                },
                {
                    "代币地址": token_block,
                    "代币符号": "BLK",
                    "当前状态": "PAPER_READY",
                    "信号门禁": "PASS",
                    "报价门禁": "PASS",
                    "安全门禁": "PASS",
                },
                {"代币地址": token_watch, "代币符号": "WAT", "当前状态": "WATCHING"},
            ]
        },
    )

    def fake_collector(token, symbol):
        if token == token_support:
            return [
                {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.16, "sell_ratio": 0.1, "evidence_level": "E4"},
                {"wallet_address": "P1", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.10, "sell_ratio": 0.25, "evidence_level": "E3"},
                {"wallet_address": "E1", "role": "EARLY_BUYER", "game_side": "EXECUTION_SIDE", "holding_ratio": 0.08, "sell_ratio": 0.05, "evidence_level": "E3"},
            ]
        if token == token_block:
            return [
                {"wallet_address": "B1", "role": "DISTRIBUTION_SELLER", "game_side": "DISTRIBUTION_SIDE", "sell_ratio": 0.9, "evidence_level": "E4"},
                {"wallet_address": "B2", "role": "EARLY_EXIT", "game_side": "DISTRIBUTION_SIDE", "sell_ratio": 0.82, "evidence_level": "E3"},
                {"wallet_address": "B3", "role": "EARLY_EXIT", "game_side": "DISTRIBUTION_SIDE", "sell_ratio": 0.80, "evidence_level": "E3"},
            ]
        raise AssertionError("WATCHING token should not be collected")

    paths = run_candidate_wallet_structure_pipeline(
        candidate_states_path=states,
        output_dir=tmp_path / "wallet_structure",
        wallet_collector=fake_collector,
    )

    summary = _read_json(Path(paths["summary_json"]))
    rows = summary["处理结果"]
    by_token = {row["代币地址"]: row for row in rows}
    assert summary["统计"]["处理数量"] == 2
    assert summary["统计"]["WALLET_SUPPORT"] == 1
    assert summary["统计"]["WALLET_BLOCK"] == 1
    assert by_token[token_support]["钱包结构结论"] == "WALLET_SUPPORT"
    assert by_token[token_support]["状态机建议"] == "ALLOW_PAPER_READY_IF_OTHER_GATES_PASS"
    assert by_token[token_support]["PAPER_READY允许说明"].startswith("钱包结构支持但不绕过")
    assert by_token[token_support]["wallet_structure_status"] == "WALLET_SUPPORT"
    assert "counterparty_pressure_score" in by_token[token_support]
    assert by_token[token_block]["钱包结构结论"] == "WALLET_BLOCK"

    output_paths = by_token[token_support]["钱包结构输出"]
    for key in ["decision_json", "early_wallet_raw_csv", "wallet_classification_csv", "candidate_groups_csv", "gmgn_note_table_csv"]:
        assert Path(output_paths[key]).exists()
    assert Path(by_token[token_support]["wallet_structure_snapshot_path"]).exists()
    assert Path(by_token[token_support]["wallet_structure_snapshot_path"]).name.startswith("snapshot_")
    assert "只做钱包结构门禁" in Path(paths["summary_md"]).read_text(encoding="utf-8")


def test_candidate_wallet_structure_pipeline_records_collection_failure_as_pause_with_low_data_quality(tmp_path):
    from sikk_candidate_wallet_structure_pipeline import run_candidate_wallet_structure_pipeline

    token = "TokenFail1111111111111111111111111111111111"
    states = _write_json(
        tmp_path / "candidate_states.json",
        {"候选状态": [{"代币地址": token, "代币符号": "FAIL", "当前状态": "PAPER_READY"}]},
    )

    def failing_collector(token, symbol):
        raise RuntimeError("gmgn unavailable")

    paths = run_candidate_wallet_structure_pipeline(
        candidate_states_path=states,
        output_dir=tmp_path / "wallet_structure",
        wallet_collector=failing_collector,
    )

    summary = _read_json(Path(paths["summary_json"]))
    row = summary["处理结果"][0]
    assert row["钱包结构结论"] == "WALLET_PAUSE"
    assert row["处理状态"] == "failed"
    assert row["数据质量评分"] < 50
    assert row["状态机建议"] == "PAUSE_OR_WATCHING"
    assert "gmgn unavailable" in row["状态调整原因"]


def test_candidate_wallet_structure_pipeline_does_not_turn_support_into_execution_authorization(tmp_path):
    from sikk_candidate_wallet_structure_pipeline import run_candidate_wallet_structure_pipeline

    token = "TokenSupportOnly111111111111111111111111111"
    states = _write_json(
        tmp_path / "candidate_states.json",
        {"候选状态": [{"代币地址": token, "代币符号": "SUP", "当前状态": "PAPER_READY", "信号门禁": "MISSING", "报价门禁": "MISSING", "安全门禁": "MISSING"}]},
    )

    paths = run_candidate_wallet_structure_pipeline(
        candidate_states_path=states,
        output_dir=tmp_path / "wallet_structure",
        wallet_collector=lambda token, symbol: [
            {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.2, "sell_ratio": 0.0, "evidence_level": "E4"},
            {"wallet_address": "P1", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.1, "sell_ratio": 0.1, "evidence_level": "E3"},
            {"wallet_address": "E1", "role": "EARLY_BUYER", "game_side": "EXECUTION_SIDE", "holding_ratio": 0.1, "sell_ratio": 0.0, "evidence_level": "E3"},
        ],
    )

    row = _read_json(Path(paths["summary_json"]))["处理结果"][0]
    assert row["钱包结构结论"] == "WALLET_SUPPORT"
    assert row["状态机建议"] == "ALLOW_PAPER_READY_IF_OTHER_GATES_PASS"
    assert "不绕过 K线/quote/安全扫描" in row["PAPER_READY允许说明"]


def test_wallet_structure_decision_writes_standard_time_anchors(tmp_path):
    from sikk_candidate_wallet_structure_pipeline import run_candidate_wallet_structure_pipeline

    token = "TokenTime11111111111111111111111111111111111"
    states = _write_json(
        tmp_path / "candidate_states.json",
        {"候选状态": [{"代币地址": token, "代币符号": "TIME", "当前状态": "PAPER_READY"}]},
    )

    paths = run_candidate_wallet_structure_pipeline(
        candidate_states_path=states,
        output_dir=tmp_path / "wallet_structure",
        wallet_collector=lambda token, symbol: [
            {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.2, "sell_ratio": 0.0, "evidence_level": "E4", "source_time": "2026-05-04T11:59:40Z"},
            {"wallet_address": "P1", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.1, "sell_ratio": 0.1, "evidence_level": "E3", "source_time": "2026-05-04T11:59:45Z"},
            {"wallet_address": "E1", "role": "EARLY_BUYER", "game_side": "EXECUTION_SIDE", "holding_ratio": 0.1, "sell_ratio": 0.0, "evidence_level": "E3", "source_time": "2026-05-04T11:59:50Z"},
        ],
        now="2026-05-04T12:00:00Z",
    )

    summary = _read_json(Path(paths["summary_json"]))
    row = summary["处理结果"][0]
    decision_path = Path(row["钱包结构输出"]["decision_json"])
    decision = _read_json(decision_path)
    for field in [
        "wallet_snapshot_time",
        "wallet_decision_created_at",
        "wallet_delta_time",
        "wallet_source_time",
        "wallet_refresh_started_at",
        "wallet_refresh_finished_at",
    ]:
        assert decision[field], field
        assert row[field] == decision[field]
    assert decision["wallet_snapshot_time"] == "2026-05-04T12:00:00Z"
    assert decision["wallet_decision_created_at"] == "2026-05-04T12:00:00Z"
    assert decision["wallet_delta_time"] == "2026-05-04T12:00:00Z"
    assert decision["wallet_source_time"] == "2026-05-04T11:59:50Z"



def test_candidate_wallet_structure_pipeline_default_collector_writes_canonical_source_wallet_dir(tmp_path, monkeypatch):
    import sikk_candidate_wallet_structure_pipeline as pipeline
    from sikk_candidate_wallet_structure_pipeline import run_candidate_wallet_structure_pipeline

    token = "TokenCanonical1111111111111111111111111111111"
    states = _write_json(
        tmp_path / "candidate_states.json",
        {"候选状态": [{"代币地址": token, "代币符号": "CAN", "当前状态": "PAPER_READY"}]},
    )

    def fake_collect(token_address, symbol="", *, output_root, limit=50, include_kline=False, allow_network=True):
        out = Path(output_root)
        assert str(out).endswith(f"data/source_wallet_bot/paper/{token}")
        (out / "wallet_data" / "normalized").mkdir(parents=True, exist_ok=True)
        _write_json(out / "wallet_data" / "normalized" / "wallet_structure_collector_rows.json", {"records": []})
        return [
            {"wallet_address": "H1", "role": "HIGH_RESULT_WALLET", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.2, "sell_ratio": 0.0, "evidence_level": "E4"},
            {"wallet_address": "P1", "role": "PARTIAL_HOLDER", "game_side": "STRUCTURE_SIDE", "holding_ratio": 0.1, "sell_ratio": 0.1, "evidence_level": "E3"},
            {"wallet_address": "E1", "role": "EARLY_BUYER", "game_side": "EXECUTION_SIDE", "holding_ratio": 0.1, "sell_ratio": 0.0, "evidence_level": "E3"},
        ]

    monkeypatch.setattr(pipeline, "collect_wallet_structure_rows_for_token", fake_collect)
    paths = run_candidate_wallet_structure_pipeline(
        candidate_states_path=states,
        output_dir=tmp_path / "wallet_structure",
        source_wallet_root=tmp_path / "data" / "source_wallet_bot" / "paper",
    )

    row = _read_json(Path(paths["summary_json"]))["处理结果"][0]
    canonical_dir = tmp_path / "data" / "source_wallet_bot" / "paper" / token
    assert row["wallet_structure_status"] == "WALLET_SUPPORT"
    assert row["canonical_source_wallet_dir"] == str(canonical_dir)
    assert (canonical_dir / "wallet_data" / "normalized" / "wallet_structure_collector_rows.json").exists()
    manifest_path = canonical_dir / "manifest" / "wallet_data_guard_source_manifest.json"
    assert manifest_path.exists()
    manifest = _read_json(manifest_path)
    assert manifest["source_type"] == "gmgn_okx_readonly"
    assert manifest["read_mode"] == "readonly"
    assert "inference" in manifest["blocked_layers"]

    summary = _read_json(Path(paths["summary_json"]))
    guard_path = Path(summary["wallet_data_guard"]["scan_report"])
    assert guard_path.exists()
    guard = _read_json(guard_path)
    assert guard["overall_status"] == "PASS"
    assert row["wallet_data_guard_status"] == "PASS"
