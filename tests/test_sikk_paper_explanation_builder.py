import json
from pathlib import Path


def test_build_case_file_payload_contains_required_sections(tmp_path):
    from sikk_paper_explanation_builder import build_case_file_payload

    position = {
        "position_id": "paper-ABC-20260503T122002Z",
        "token_symbol": "ABC",
        "token_address": "TokenABC111",
        "status": "CLOSED",
        "strategy_name": "SIKK-B 控盘箱体突破回踩",
        "signal_level": "S4_强确认信号",
        "candidate_discovered_at": "2026-05-03T12:01:22Z",
        "discovery_market_cap_usd": 82000,
        "signal_time": "2026-05-03T12:18:40Z",
        "signal_market_cap_usd": 118000,
        "wallet_decision_time": "2026-05-03T12:19:10Z",
        "wallet_structure_status": "WALLET_SUPPORT",
        "wallet_structure_score": 72,
        "wallet_risk_score": 28,
        "counterparty_pressure_score": 32,
        "data_quality_score": 81,
        "paper_entry_time": "2026-05-03T12:20:02Z",
        "entry_market_cap_usd": 126000,
        "market_cap_context_status": "NORMAL_ENTRY",
        "paper_size_sol": 0.01,
        "paper_size_usd": 1.65,
        "estimated_token_amount": 30800,
        "entry_raw_quote_price": 0.000052,
        "entry_simulated_price": 0.00005356,
        "entry_slippage_pct": 3,
        "entry_fee_sol": 0.0005,
        "exit_time": "2026-05-03T13:02:12Z",
        "exit_price": 0.000069,
        "exit_market_cap_usd": 162000,
        "exit_trigger": "WALLET_STRUCTURE",
        "exit_reason_code": "STRUCTURE_WEAKENING",
        "net_pnl_pct": 28.7,
        "failure_type": None,
    }
    journal = [{"time": "2026-05-03T12:35:00Z", "current_price": 0.00006, "unrealized_pnl_pct": 18.2, "paper_action": "HOLD"}]
    payload = build_case_file_payload(position, holding_journal=journal)

    for key in ["basic", "discovery", "pattern", "signal", "wallet_entry", "quote_security", "entry", "holding_journal", "exit", "review", "adjustment"]:
        assert key in payload
    assert payload["entry"]["paper_entry_time"] == "2026-05-03T12:20:02Z"
    assert payload["entry"]["market_cap_context_status"] == "NORMAL_ENTRY"
    assert "为什么" not in payload["entry"]["entry_explanation"]
    assert "入场" in payload["entry"]["entry_explanation"]
    assert payload["holding_journal"][0]["paper_action"] == "HOLD"
    quality = payload["case_quality"]
    assert quality["case_quality_level"] == "E3_可复盘"
    assert quality["missing_core_fields"] == []
    assert quality["case_completeness_score"] == 100.0
    assert quality["strategy_review_eligible"] is True
    assert payload["entry"]["paper_entry_snapshot"]["entry_market_cap_usd"] == 126000


def test_build_case_files_writes_json_and_markdown(tmp_path):
    from sikk_paper_explanation_builder import build_case_files

    paper_dir = tmp_path / "paper_live"
    paper_dir.mkdir(parents=True)
    (paper_dir / "paper_positions_open.json").write_text(json.dumps({"open_positions": [{
        "position_id": "paper-open-1",
        "token_address": "TokenOpen111",
        "token_symbol": "OPEN",
        "status": "OPEN",
        "paper_entry_time": "2026-05-03T12:20:02Z",
        "paper_size_sol": 0.01,
        "estimated_token_amount": 1000,
        "entry_market_cap_usd": 126000,
        "market_cap_context_status": "NORMAL_ENTRY",
    }]}, ensure_ascii=False), encoding="utf-8")
    (paper_dir / "paper_positions_closed.json").write_text(json.dumps({"closed_positions": []}, ensure_ascii=False), encoding="utf-8")
    journal_dir = paper_dir / "position_journal"
    journal_dir.mkdir()
    (journal_dir / "paper-open-1.jsonl").write_text(json.dumps({"time": "2026-05-03T12:30:00Z", "paper_action": "HOLD"}, ensure_ascii=False)+"\n", encoding="utf-8")

    paths = build_case_files(paper_dir=paper_dir, base_dir=tmp_path, output_dir=paper_dir / "case_files")
    assert paths["case_json_count"] == 1
    assert paths["case_md_count"] == 1
    case_json = next(p for p in (paper_dir / "case_files").glob("*.json") if p.name != "case_files_manifest.json")
    case_md = next(p for p in (paper_dir / "case_files").glob("*.md"))
    payload = json.loads(case_json.read_text(encoding="utf-8"))
    assert payload["basic"]["position_id"] == "paper-open-1"
    md = case_md.read_text(encoding="utf-8")
    for section in ["基础信息", "候选发现", "盘型判断", "入场信号", "钱包结构门禁", "纸面入场", "持仓过程", "退出", "策略复盘", "策略调整建议", "字段来源追踪", "仍然缺失的字段清单"]:
        assert section in md
    assert "不执行真实 swap" in md



def test_case_file_payload_contains_operator_psychology_section():
    from sikk_paper_explanation_builder import build_case_file_payload

    position = {
        "position_id": "pos-psy-1",
        "token_address": "T1",
        "token_symbol": "AAA",
        "status": "OPEN",
        "dominant_side_lifecycle": "ACTIVE_DISTRIBUTION",
        "dominant_side_intent": "ACTIVE_DISTRIBUTION",
        "counterparty_state": "EXIT_LIQUIDITY_FORMING",
        "chip_control_state": "CONTROL_LOST_TO_DISTRIBUTION_SIDE",
        "operator_psychology": "DISTRIBUTE_INTO_DEMAND",
        "operator_psychology_label": "借需求派发 / 高位兑现",
        "paper_trade_alignment": "LATE_IN_DISTRIBUTION",
        "psychology_evidence_level": "E4",
        "psychology_reason": "主导侧心理解释：生命周期进入派发/兑现侧。",
        "next_observation_focus": "观察同步卖出和对手盘承接。",
        "invalidation_conditions": ["同源卖出停止"],
    }

    payload = build_case_file_payload(position)

    assert "operator_psychology" in payload
    section = payload["operator_psychology"]
    assert section["operator_psychology"] == "DISTRIBUTE_INTO_DEMAND"
    assert section["paper_trade_alignment"] == "LATE_IN_DISTRIBUTION"
    assert "主导侧心理解释" in section["psychology_explanation"]


def test_case_file_markdown_displays_operator_psychology_section():
    from sikk_paper_explanation_builder import build_case_file_payload, render_case_markdown

    payload = build_case_file_payload({
        "position_id": "pos-psy-2",
        "token_address": "T2",
        "token_symbol": "BBB",
        "operator_psychology": "DEFEND_STRUCTURE_LEVEL",
        "operator_psychology_label": "防守结构位 / 箱体控筹",
        "operator_lifecycle_stage": "CONTROL_BOX_ACCUMULATION",
        "paper_trade_alignment": "ALIGNED_WITH_ACCUMULATION_OR_CONTROL",
        "psychology_reason": "主导侧心理解释：箱体/再控筹阶段更像结构侧维护价格区间。",
    })
    md = render_case_markdown(payload)

    assert "## 8. 主导侧心理与生命周期" in md
    assert "防守结构位 / 箱体控筹" in md
    assert "ALIGNED_WITH_ACCUMULATION_OR_CONTROL" in md


def test_case_file_quality_marks_missing_snapshot_as_record_only():
    from sikk_paper_explanation_builder import build_case_file_payload, render_case_markdown

    payload = build_case_file_payload({
        "position_id": "pos-low-quality",
        "token_address": "T3",
        "token_symbol": "MISS",
        "status": "OPEN",
    })

    assert payload["case_quality"]["case_quality_level"] == "E1_记录型样本"
    assert "发现时市值" in payload["case_quality"]["missing_core_fields"]
    assert "paper entry snapshot" in payload["case_quality"]["repair_suggestions"][0]
    md = render_case_markdown(payload)
    assert "Case File 质量" in md
    assert "E1_记录型样本" in md
