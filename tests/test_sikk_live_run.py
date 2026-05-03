import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _fake_pipeline_runner(**kwargs):
    root = Path(kwargs["output_root"])
    _write_json(root / "gmgn_new_token_filter" / "token_candidates.json", {"候选列表": [{"代币地址": "T1", "代币符号": "AAA"}]})
    _write_json(root / "state_machine" / "candidate_states.json", {"候选状态": [{"代币地址": "T1", "代币符号": "AAA", "当前状态": "PAPER_READY"}]})
    _write_json(root / "candidate_signal_outputs" / "candidate_signal_summary.json", {"信号结果": [{"代币地址": "T1", "代币符号": "AAA", "信号价格": 1.0, "建议纸面仓位SOL": 0.01}]})
    _write_json(root / "quote_security" / "candidate_quote_security_summary.json", {"处理结果": [{"代币地址": "T1", "交易前状态": "READY_FOR_CONFIRMATION", "最终权限": "ALLOW_CONFIRMATION_LAYER"}]})
    return {"manifest_json": str(root / "orchestrator" / "pipeline_manifest.json"), "report_md": str(root / "orchestrator" / "pipeline_report.md")}


def _fake_paper_runner(**kwargs):
    out = Path(kwargs["output_dir"])
    out.mkdir(parents=True, exist_ok=True)
    _write_json(
        out / "paper_positions_open.json",
        {
            "open_positions": [
                {
                    "代币地址": "T1",
                    "代币符号": "AAA",
                    "status": "OPEN",
                    "entry_time": "2026-05-02T00:00:00Z",
                    "entry_price": 1.23,
                    "position_sol": 0.01,
                    "last_price": 1.35,
                    "当前收益率_pct": 9.7561,
                }
            ]
        },
    )
    _write_json(out / "paper_positions_closed.json", {"closed_positions": []})
    (out / "paper_positions_closed.csv").write_text("代币地址,代币符号,status,wallet_structure_status,signal_level,最终收益率_pct,net_pnl_sol,最大浮盈_pct,最大浮亏_pct,failure_type\n", encoding="utf-8-sig")
    (out / "failure_attribution.jsonl").write_text("", encoding="utf-8")
    (out / "daily_reports").mkdir(parents=True, exist_ok=True)
    daily = out / "daily_reports" / "paper_daily_report_20260502.md"
    daily.write_text("# OKX/GMGN 纸面自动交易日报\n\n- 边界：不执行真实 swap。\n", encoding="utf-8")
    return {
        "open_positions_json": str(out / "paper_positions_open.json"),
        "closed_positions_json": str(out / "paper_positions_closed.json"),
        "paper_trades_csv": str(out / "paper_trades.csv"),
        "daily_report_md": str(daily),
        "failure_attribution_jsonl": str(out / "failure_attribution.jsonl"),
    }


def test_sikk_live_run_once_unifies_pipeline_paper_reports_and_runtime_outputs(tmp_path):
    from sikk_live_run import run_live_once

    root = tmp_path / "gmgn_candidates_live_run"
    delivered = []
    result = run_live_once(
        output_root=root,
        limit=3,
        quote_sources=("okx",),
        default_quote_amount_sol=0.01,
        pipeline_runner=_fake_pipeline_runner,
        paper_runner=_fake_paper_runner,
        now="2026-05-02T00:00:00Z",
        telegram_broadcast=True,
        message_sender=lambda *, target, message: delivered.append({"target": target, "message": message}),
    )

    assert result["output_root"] == str(root)
    assert Path(result["live_run_manifest_json"]).exists()
    assert Path(result["live_board_md"]).exists()
    assert Path(result["live_dashboard_html"]).exists()
    assert Path(result["wallet_daily_report_md"]).exists()
    assert Path(result["paper_daily_report_md"]).exists()
    assert Path(result["token_status_md"]).exists()
    assert delivered
    assert delivered[0]["target"] == "telegram"
    assert "SIKK Live Run" in delivered[0]["message"]
    assert "日报" in delivered[0]["message"]

    manifest = json.loads(Path(result["live_run_manifest_json"]).read_text(encoding="utf-8"))
    assert manifest["模式"] == "paper_runtime_once"
    assert manifest["配置"]["notification_enabled"] is True
    assert manifest["配置"]["telegram_broadcast_enabled"] is True
    assert manifest["配置"]["confirmation_enabled"] is False
    assert manifest["配置"]["real_swap_enabled"] is False
    assert manifest["阶段输出"]["pipeline"]["manifest_json"].endswith("pipeline_manifest.json")
    assert manifest["阶段输出"]["paper_live"]["open_positions_json"].endswith("paper_positions_open.json")
    assert "不执行真实 swap" in manifest["说明"]

    live_board = Path(result["live_board_md"]).read_text(encoding="utf-8")
    assert "SIKK Live Board" in live_board
    assert "PAPER_READY" in live_board
    assert "不执行真实 swap" in live_board

    live_state = json.loads(Path(result["live_state_json"]).read_text(encoding="utf-8"))
    token = live_state["tokens"][0]
    assert token["quote"]["quote_gate"] == "ALLOW_CONFIRMATION_LAYER"
    assert token["security"]["security_gate"] == "READY_FOR_CONFIRMATION"
    assert token["paper"]["paper_status"] == "OPEN"
    assert token["paper"]["paper_entry_price_mode"] == "live_or_signal_with_cost_model"
    assert token["paper"]["paper_entry_at"] == "2026-05-02T00:00:00Z"
    assert token["paper"]["paper_entry_price"] == 1.23
    assert token["paper"]["current_price"] == 1.35
    assert token["priority_level"] == "P0_ACTIVE_POSITION"
    assert token["latest_action"] == "HOLD"

    dashboard_html = Path(result["live_dashboard_html"]).read_text(encoding="utf-8")
    assert "paper_entry_price" in dashboard_html
    assert "1.23" in dashboard_html
    assert "current_price" in dashboard_html


def test_live_run_manifest_exposes_phased_improvement_flow(tmp_path):
    from sikk_live_run import run_live_once

    root = tmp_path / "gmgn_candidates_live_run"
    result = run_live_once(
        output_root=root,
        limit=3,
        quote_sources=("okx",),
        default_quote_amount_sol=0.01,
        pipeline_runner=_fake_pipeline_runner,
        paper_runner=_fake_paper_runner,
        now="2026-05-02T00:00:00Z",
    )

    manifest = json.loads(Path(result["live_run_manifest_json"]).read_text(encoding="utf-8"))
    phase_names = [phase["阶段"] for phase in manifest["分阶段流程"]]
    assert phase_names == [
        "P0_候选发现",
        "P1_K线吸筹与信号",
        "P2_钱包结构门禁",
        "P3_报价安全确认",
        "P4_live纸面交易",
        "P5_复盘校准",
        "P6_人工确认后小额实盘准备",
    ]
    assert manifest["当前不足修正"]["默认入场价"] == "live优先，缺失时降级signal并标记偏差"
    assert manifest["当前不足修正"]["钱包结构"] == "observe默认接入，soft/hard需显式启用"
    assert manifest["当前不足修正"]["真实交易"] == "默认关闭，只生成确认层，不广播"


def test_runtime_status_merges_quote_security_and_paper_position_evidence(tmp_path):
    from sikk_live_run import build_enriched_runtime_statuses

    root = tmp_path / "run"
    _write_json(root / "state_machine" / "candidate_states.json", {"候选状态": [{"代币地址": "T1", "代币符号": "AAA", "当前状态": "PAPER_READY", "discovery_market_cap_usd": 100000, "signal_market_cap_usd": 120000, "wallet_decision_market_cap_usd": 130000}]})
    _write_json(root / "quote_security" / "candidate_quote_security_summary.json", {"处理结果": [{"代币地址": "T1", "最终权限": "PAUSE_NEED_CONFIRM", "交易前状态": "PAUSE", "说明": "报价缺失", "current_market_cap_usd": 150000}]})
    _write_json(root / "paper_live" / "paper_positions_open.json", {"open_positions": [{"代币地址": "T1", "代币符号": "AAA", "entry_price_mode": "live", "entry_time": "2026-05-02T00:01:00Z", "entry_price": 2.0, "position_sol": 0.02, "last_price": 2.25, "unrealized_pnl_pct": 12.5}]})
    (root / "paper_live" / "failure_attribution.jsonl").parent.mkdir(parents=True, exist_ok=True)
    (root / "paper_live" / "failure_attribution.jsonl").write_text(json.dumps({"事件时间": "2026-05-02T00:02:00Z", "事件类型": "EXIT_MONITOR", "代币地址": "T1", "failure_type": "DATA_QUALITY_FAIL", "failure_reason": "数据质量不足"}, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_json(root / "okx_cluster" / "T1" / "okx_cluster_decision.json", {"token_address": "T1", "token_symbol": "AAA", "okx_cluster_status": "CLUSTER_CONTROL_HOLDING", "okx_cluster_score": 80, "largest_cluster_holding_pct": 14.0})

    statuses = build_enriched_runtime_statuses(root, "2026-05-02T00:00:00Z")

    assert len(statuses) == 1
    status = statuses[0]
    assert status["quote"]["quote_gate"] == "PAUSE_NEED_CONFIRM"
    assert status["security"]["security_gate"] == "PAUSE"
    assert status["paper"]["paper_status"] == "OPEN"
    assert status["paper"]["unrealized_pnl_pct"] == 12.5
    assert status["paper"]["paper_entry_at"] == "2026-05-02T00:01:00Z"
    assert status["paper"]["paper_entry_price"] == 2.0
    assert status["paper"]["paper_entry_amount_sol"] == 0.02
    assert status["paper"]["current_price"] == 2.25
    assert status["paper"]["exit_monitor_at"] == "2026-05-02T00:02:00Z"
    assert status["paper"]["failure_attribution_type"] == "DATA_QUALITY_FAIL"
    assert status["okx_cluster"]["okx_cluster_status"] == "CLUSTER_CONTROL_HOLDING"
    assert status["okx_cluster"]["largest_cluster_holding_pct"] == 14.0
    assert status["market_cap_context"]["discovery_market_cap_usd"] == 100000
    assert status["market_cap_context"]["signal_market_cap_usd"] == 120000
    assert status["market_cap_context"]["wallet_decision_market_cap_usd"] == 130000
    assert status["market_cap_context"]["current_market_cap_usd"] == 150000
    assert status["market_cap_change_from_discovery_pct"] == 50.0
    assert status["latest_action"] == "EXIT_MONITOR"
    assert "报价缺失" in status["latest_reason"]


def test_runtime_status_applies_okx_cluster_delta_failure_for_paper_action(tmp_path):
    from sikk_live_run import build_enriched_runtime_statuses

    root = tmp_path / "run"
    _write_json(root / "state_machine" / "candidate_states.json", {"候选状态": [{"代币地址": "T2", "代币符号": "BBB", "当前状态": "PAPER_READY"}]})
    _write_json(root / "quote_security" / "candidate_quote_security_summary.json", {"处理结果": [{"代币地址": "T2", "最终权限": "ALLOW_CONFIRMATION_LAYER", "交易前状态": "READY_FOR_CONFIRMATION"}]})
    _write_json(root / "paper_live" / "paper_positions_open.json", {"open_positions": [{"代币地址": "T2", "代币符号": "BBB", "entry_time": "2026-05-02T00:01:00Z", "entry_price": 1.0, "last_price": 0.8, "unrealized_pnl_pct": -20}]})
    _write_json(root / "okx_cluster" / "T2" / "okx_cluster_decision.json", {"token_address": "T2", "token_symbol": "BBB", "okx_cluster_status": "CLUSTER_DISTRIBUTION_RISK", "recommended_paper_action": "FORCE_PAPER_EXIT", "okx_cluster_failure_type": "CLUSTER_DISTRIBUTION_ACTIVE"})
    (root / "okx_cluster" / "T2" / "okx_cluster_failure_attribution.jsonl").parent.mkdir(parents=True, exist_ok=True)
    (root / "okx_cluster" / "T2" / "okx_cluster_failure_attribution.jsonl").write_text(json.dumps({"事件时间": "2026-05-02T00:03:00Z", "事件类型": "FORCE_PAPER_EXIT", "代币地址": "T2", "failure_type": "CLUSTER_DISTRIBUTION_ACTIVE", "okx_cluster_failure_type": "CLUSTER_DISTRIBUTION_ACTIVE", "recommended_paper_action": "FORCE_PAPER_EXIT", "failure_reason": "OKX集群派发风险"}, ensure_ascii=False) + "\n", encoding="utf-8")

    status = build_enriched_runtime_statuses(root, "2026-05-02T00:00:00Z")[0]

    assert status["latest_action"] == "FORCE_PAPER_EXIT"
    assert status["paper"]["failure_attribution_type"] == "CLUSTER_DISTRIBUTION_ACTIVE"
    assert status["paper"]["okx_cluster_failure_type"] == "CLUSTER_DISTRIBUTION_ACTIVE"
    assert status["paper"]["recommended_paper_action"] == "FORCE_PAPER_EXIT"
    assert "仅纸面退出/复盘" in status["latest_reason"]


def test_build_runtime_candidates_from_state_file_prefers_state_rows(tmp_path):
    from sikk_live_run import build_runtime_candidates_from_state_file

    states_path = _write_json(
        tmp_path / "state_machine" / "candidate_states.json",
        {"候选状态": [{"代币地址": "T1", "代币符号": "AAA", "当前状态": "PAPER_READY"}, {"代币地址": "T2", "代币符号": "BBB", "当前状态": "BLOCKED"}]},
    )

    rows = build_runtime_candidates_from_state_file(states_path)
    assert rows == [
        {"代币地址": "T1", "代币符号": "AAA", "当前状态": "PAPER_READY"},
        {"代币地址": "T2", "代币符号": "BBB", "当前状态": "BLOCKED"},
    ]
