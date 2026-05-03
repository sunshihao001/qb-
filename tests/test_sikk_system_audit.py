import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_system_audit_runs_on_empty_directory(tmp_path):
    from sikk_system_audit import run_system_audit

    paths = run_system_audit(live_run_dir=tmp_path)

    audit = _read_json(Path(paths["system_audit_json"]))
    md = Path(paths["system_audit_md"]).read_text(encoding="utf-8")
    assert audit["paper_only"] is True
    assert audit["candidate_count"] == 0
    assert audit["missing_files"]
    assert "只读系统审计" in audit["readonly_note"]
    assert "不采集、不交易" in md


def test_system_audit_runs_on_partial_missing_directory(tmp_path):
    from sikk_system_audit import run_system_audit

    token = "TokenPartial111111111111111111111111111111"
    _write_json(
        tmp_path / "state_machine" / "candidate_states.json",
        {
            "候选状态": [
                {
                    "代币地址": token,
                    "代币符号": "PART",
                    "当前状态": "WATCHING",
                    "状态原因": "等待信号",
                    "钱包门禁效果": "NO_WALLET_INPUT",
                    "钱包结构结论": "未接入",
                }
            ]
        },
    )
    _write_json(tmp_path / "live_state.json", {"tokens": [{"token_address": token, "token_symbol": "PART", "current_state": "WATCHING"}]})

    paths = run_system_audit(live_run_dir=tmp_path)
    audit = _read_json(Path(paths["system_audit_json"]))

    assert audit["candidate_count"] == 1
    assert audit["stuck_tokens"][0]["token"] == token
    assert audit["wallet_bypass_or_degraded"]
    assert audit["dashboard_missing_fields"]["missing_field_counts"]["discovered_at"] == 1
    assert any("补齐 live run 标准输出目录" in item for item in audit["recommendations"])


def test_system_audit_summarizes_normal_fake_outputs(tmp_path):
    from sikk_system_audit import run_system_audit

    token_open = "TokenOpenAudit1111111111111111111111111111"
    token_block = "TokenBlockAudit111111111111111111111111111"
    token_stuck = "TokenStuckAudit111111111111111111111111111"

    _write_json(
        tmp_path / "candidate_pool" / "token_candidates.json",
        {
            "候选结果": [
                {"代币地址": token_open, "代币符号": "OPEN"},
                {"代币地址": token_block, "代币符号": "BLOCK"},
                {"代币地址": token_stuck, "代币符号": "STUCK"},
            ]
        },
    )
    _write_json(
        tmp_path / "kline" / "candidate_kline_pipeline_summary.json",
        {"处理结果": [{"代币地址": token_open, "状态": "ok"}, {"代币地址": token_block, "状态": "failed"}]},
    )
    _write_json(
        tmp_path / "signals" / "candidate_signal_summary.json",
        {
            "信号结果": [{"代币地址": token_open, "状态": "ok"}],
            "跳过结果": [{"代币地址": token_stuck, "状态": "SKIPPED", "原因": "no kline"}],
        },
    )
    _write_json(
        tmp_path / "quote_security" / "candidate_quote_security_summary.json",
        {"处理结果": [{"代币地址": token_open, "状态": "ok"}, {"代币地址": token_block, "状态": "BLOCK"}]},
    )
    _write_json(
        tmp_path / "state_machine" / "candidate_states.json",
        {
            "候选状态": [
                {"代币地址": token_open, "代币符号": "OPEN", "当前状态": "BLOCKED", "状态原因": "后续风险阻断"},
                {"代币地址": token_block, "代币符号": "BLOCK", "当前状态": "BLOCKED", "状态原因": "风险阻断"},
                {"代币地址": token_stuck, "代币符号": "STUCK", "当前状态": "ACCUMULATING", "状态原因": "等待 T_end", "钱包门禁效果": "NO_WALLET_INPUT"},
            ]
        },
    )
    _write_json(
        tmp_path / "wallet_structure" / "candidate_wallet_structure_summary.json",
        {
            "处理结果": [
                {
                    "token_address": token_open,
                    "wallet_structure_status": "WALLET_SUPPORT",
                    "wallet_structure_score": 82,
                    "wallet_gate_result": "PASS",
                    "paper_gate_effect": "SUPPORT",
                    "reason_codes": ["smart_wallet_buy"],
                    "data_quality_status": "OK",
                },
                {
                    "token_address": token_stuck,
                    "wallet_structure_status": "DEGRADED",
                    "wallet_structure_score": "",
                    "wallet_gate_result": "DEGRADED",
                    "paper_gate_effect": "NO_WALLET_INPUT",
                    "reason_codes": ["missing_snapshot"],
                    "data_quality_status": "DEGRADED",
                },
            ]
        },
    )
    _write_json(
        tmp_path / "live_state.json",
        {
            "tokens": [
                {
                    "token_address": token_open,
                    "token_symbol": "OPEN",
                    "current_state": "BLOCKED",
                    "discovered_at": "2026-05-01T00:00:00Z",
                    "first_signal_at": "2026-05-01T00:01:00Z",
                    "wallet_decision_at": "2026-05-01T00:02:00Z",
                    "current_price": 1.2,
                    "wallet_structure": {"wallet_structure_status": "WALLET_SUPPORT"},
                    "signal": {"signal_level": "S4"},
                    "paper": {"paper_status": "OPEN"},
                }
            ]
        },
    )
    _write_json(
        tmp_path / "paper_live" / "paper_positions_open.json",
        {
            "open_positions": [
                {
                    "代币地址": token_open,
                    "代币符号": "OPEN",
                    "entry_time": "2026-05-01T00:03:00Z",
                    "entry_price": 1.0,
                    "status": "OPEN",
                }
            ]
        },
    )
    _write_json(
        tmp_path / "paper_live" / "paper_positions_closed.json",
        {"closed_positions": [{"代币地址": token_block, "代币符号": "BLOCK", "exit_reason": "命中纸面止损"}]},
    )
    _write_json(tmp_path / "paper_live" / "strategy_metrics.json", {"统计": {"读取候选数": 3, "新增纸面入场数": 1, "纸面退出数": 1}})
    (tmp_path / "paper_live").mkdir(exist_ok=True)
    (tmp_path / "paper_live" / "failure_attribution.jsonl").write_text(
        json.dumps({"代币地址": token_block, "failure_type": "wallet_exit", "failure_reason": "pressure"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "live_dashboard.html").write_text("<html>fake</html>", encoding="utf-8")

    paths = run_system_audit(live_run_dir=tmp_path)
    audit = _read_json(Path(paths["system_audit_json"]))
    md = Path(paths["system_audit_md"]).read_text(encoding="utf-8")

    assert audit["candidate_count"] == 3
    assert audit["module_counts"]["kline"]["failed"] == 1
    assert audit["module_counts"]["signals"]["skipped"] == 1
    assert any(item["token"] == token_stuck for item in audit["stuck_tokens"])
    assert any(item["token"] == token_stuck for item in audit["wallet_bypass_or_degraded"])
    assert any(item["conflict"] == "open_position_with_terminal_state" for item in audit["state_machine_conflicts"])
    assert audit["dashboard_missing_fields"]["missing_field_counts"]["paper_entry_market_cap_usd"] == 1
    assert audit["dashboard_missing_fields"]["missing_field_counts"]["chip_control_state"] == 1
    assert audit["dashboard_missing_fields"]["missing_field_counts"]["market_cap_context"] == 1
    assert audit["replay_unavailable_fields"]["missing_field_counts"]["paper_entry_market_cap_usd"] >= 1
    assert "状态机冲突" in md
    assert "下一步建议" in md
