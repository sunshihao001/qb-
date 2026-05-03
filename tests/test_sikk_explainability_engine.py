import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_explainability_engine_explains_existing_results_without_redeciding(tmp_path):
    from sikk_explainability_engine import run_explainability_engine

    token = "TokenExplain111111111111111111111111111111"
    _write_json(
        tmp_path / "tokens" / token / "token_status.json",
        {
            "token_address": token,
            "token_symbol": "EXPL",
            "current_state": "PAPER_READY",
            "latest_action": "OPEN_PAPER_POSITION",
            "latest_reason": "吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0",
            "last_update": "2026-05-02T00:00:00Z",
            "wallet_structure": {"wallet_structure_status": "WALLET_SUPPORT"},
            "quote": {"quote_gate": "ALLOW_CONFIRMATION_LAYER"},
            "security": {"security_gate": "READY_FOR_CONFIRMATION"},
            "paper": {"paper_status": "NONE"},
            "chip_control": {
                "chip_control_state": "CONTROL_RETAINED_BY_STRUCTURE_SIDE",
                "chip_control_action": "ALLOW_PAPER_READY_IF_OTHER_GATES_PASS",
                "evidence_points": ["钱包结构支持且其他门控通过"],
            },
            "market_cap_context": {
                "discovery_market_cap_usd": 100000,
                "signal_market_cap_usd": 120000,
                "paper_entry_market_cap_usd": 135000,
                "market_cap_context_quality": "PARTIAL",
            },
            "lifecycle": {
                "dominant_side_lifecycle": "ACCUMULATION_CONTROL",
                "dominant_side_intent": "STRUCTURE_MAINTAINING",
                "counterparty_state": "LOW_PRESSURE",
            },
            "okx_cluster": {
                "okx_cluster_status": "CLUSTER_CONTROL_HOLDING",
                "okx_cluster_score": 82,
                "okx_cluster_risk_score": 12,
                "okx_cluster_distribution_score": 18,
                "okx_cluster_control_retention_score": 78,
                "okx_cluster_reason": "横盘控筹阶段前300/最大集群持仓相对稳定。",
            },
        },
    )
    (tmp_path / "tokens" / token / "process_trace.jsonl").write_text(
        json.dumps({"time": "2026-05-02T00:00:00Z", "current_state": "PAPER_READY", "latest_reason": "已有状态机输出"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _write_json(
        tmp_path / "wallet_structure" / token / "wallet_structure_decision.json",
        {
            "代币地址": token,
            "代币符号": "EXPL",
            "wallet_structure_status": "WALLET_SUPPORT",
            "wallet_structure_reason": "发现聪明钱包持续承接",
            "wallet_structure_score": 82,
        },
    )
    _write_json(
        tmp_path / "quote_security" / "candidate_quote_security_summary.json",
        {
            "处理结果": [
                {
                    "代币地址": token,
                    "代币符号": "EXPL",
                    "交易前状态": "READY_FOR_CONFIRMATION",
                    "quote_security_permission": "ALLOW_CONFIRMATION_LAYER",
                    "原因": "报价与安全扫描未触发硬阻断，可进入人工确认层",
                }
            ]
        },
    )
    _write_json(
        tmp_path / "paper_live" / "paper_positions_open.json",
        {"open_positions": [{"代币地址": token, "代币符号": "EXPL", "entry_time": "2026-05-02 00:01:00 UTC", "status": "OPEN"}]},
    )
    _write_json(tmp_path / "paper_live" / "paper_positions_closed.json", {"closed_positions": []})
    (tmp_path / "paper_live" / "failure_attribution.jsonl").write_text("", encoding="utf-8")

    paths = run_explainability_engine(live_run_dir=tmp_path)
    report = _read_json(Path(paths["explainability_report_json"]))
    md = Path(paths["explainability_report_md"]).read_text(encoding="utf-8")

    assert report["paper_only"] is True
    assert "不重新裁决" in report["non_decision_note"]
    assert report["tokens"][0]["current_state"] == "PAPER_READY"
    questions = report["tokens"][0]["questions"]
    assert "报价与安全扫描未触发硬阻断" in json.dumps(questions["为什么支持"], ensure_ascii=False)
    assert "吸筹窗口 valid" in json.dumps(questions["为什么进入paper"], ensure_ascii=False)
    assert "CONTROL_RETAINED_BY_STRUCTURE_SIDE" in json.dumps(questions["为什么支持"], ensure_ascii=False)
    assert "paper_entry_market_cap_usd" in json.dumps(questions["为什么进入paper"], ensure_ascii=False)
    assert "STRUCTURE_MAINTAINING" in json.dumps(questions["下一步看什么"], ensure_ascii=False)
    assert "CLUSTER_CONTROL_HOLDING" in json.dumps(questions["为什么支持"], ensure_ascii=False)
    assert "OKX 前300集群" in json.dumps(questions["下一步看什么"], ensure_ascii=False)
    assert "证据缺失/待复查" in json.dumps(questions["为什么失败"], ensure_ascii=False)
    assert "来源" in md
    assert str(tmp_path / "tokens" / token / "token_status.json") in md


def test_explainability_engine_marks_missing_inputs_and_does_not_invent(tmp_path):
    from sikk_explainability_engine import EXPLANATION_KEYS, run_explainability_engine

    token = "TokenMissingExplain1111111111111111111111111"
    _write_json(
        tmp_path / "live_state.json",
        {"tokens": [{"token_address": token, "token_symbol": "MISS", "current_state": "WATCHING", "latest_action": "WAIT_SIGNAL"}]},
    )

    paths = run_explainability_engine(live_run_dir=tmp_path)
    report = _read_json(Path(paths["explainability_report_json"]))
    token_report = report["tokens"][0]

    assert report["missing_inputs"]
    assert token_report["current_state"] == "WATCHING"
    assert set(EXPLANATION_KEYS) == set(token_report["questions"].keys())
    assert "证据缺失/待复查" in json.dumps(token_report["questions"]["为什么支持"], ensure_ascii=False)
    assert "证据缺失/待复查" in json.dumps(token_report["questions"]["为什么阻断"], ensure_ascii=False)
    assert "不重新裁决" in token_report["non_decision_note"]


def test_explainability_engine_explains_pause_block_exit_failure(tmp_path):
    from sikk_explainability_engine import run_explainability_engine

    token = "TokenFailExplain111111111111111111111111111"
    _write_json(
        tmp_path / "tokens" / token / "token_status.json",
        {
            "token_address": token,
            "token_symbol": "FAILX",
            "current_state": "BLOCKED",
            "latest_action": "STOP_PAPER",
            "latest_reason": "钱包结构变为 WALLET_BLOCK",
            "last_update": "2026-05-02T01:00:00Z",
        },
    )
    _write_json(
        tmp_path / "wallet_structure" / "candidate_wallet_structure_summary.json",
        {"处理结果": [{"代币地址": token, "代币符号": "FAILX", "wallet_structure_status": "WALLET_BLOCK", "wallet_structure_reason": "对手盘压力高"}]},
    )
    _write_json(
        tmp_path / "quote_security" / "candidate_quote_security_summary.json",
        {"处理结果": [{"代币地址": token, "代币符号": "FAILX", "交易前状态": "PAUSE", "quote_security_permission": "PAUSE_NEED_CONFIRM", "原因": "OKX 中等风险"}]},
    )
    _write_json(tmp_path / "paper_live" / "paper_positions_open.json", {"open_positions": []})
    _write_json(
        tmp_path / "paper_live" / "paper_positions_closed.json",
        {"closed_positions": [{"代币地址": token, "代币符号": "FAILX", "exit_time": "2026-05-02T01:02:00Z", "exit_reason": "命中纸面止损"}]},
    )
    (tmp_path / "paper_live" / "failure_attribution.jsonl").write_text(
        json.dumps({"事件时间": "2026-05-02T01:02:00Z", "代币地址": token, "代币符号": "FAILX", "failure_type": "STRUCTURE_WEAKENING", "failure_reason": "钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    paths = run_explainability_engine(live_run_dir=tmp_path)
    token_report = _read_json(Path(paths["explainability_report_json"]))["tokens"][0]
    questions_text = json.dumps(token_report["questions"], ensure_ascii=False)

    assert "PAUSE_NEED_CONFIRM" in questions_text
    assert "WALLET_BLOCK" in questions_text
    assert "命中纸面止损" in questions_text
    assert "STRUCTURE_WEAKENING" in questions_text
    assert "对手盘压力高" in questions_text
