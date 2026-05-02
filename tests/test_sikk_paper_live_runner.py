import csv
import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_paper_live_runner_opens_updates_and_closes_positions_without_real_swap(tmp_path):
    from sikk_paper_live_runner import run_paper_live_cycle

    token_open = "TokenOpen11111111111111111111111111111111"
    token_stop = "TokenStop11111111111111111111111111111111"
    token_block = "TokenBlock1111111111111111111111111111111"

    states_path = _write_json(
        tmp_path / "state_machine" / "candidate_states.json",
        {
            "候选状态": [
                {
                    "代币地址": token_open,
                    "代币符号": "OPEN",
                    "当前状态": "PAPER_READY",
                    "信号等级": "S4_强确认信号",
                    "策略类型": "SIKK-B 控盘箱体突破回踩",
                    "信号时间": "2026-05-01T00:00:00Z",
                    "信号价格": 1.0,
                    "建议纸面仓位SOL": 0.1,
                },
                {
                    "代币地址": token_block,
                    "代币符号": "BLOCK",
                    "当前状态": "PAPER_READY",
                    "信号等级": "S4_强确认信号",
                    "信号价格": 1.0,
                    "建议纸面仓位SOL": 0.1,
                },
            ]
        },
    )
    signal_summary_path = _write_json(
        tmp_path / "candidate_signal_summary.json",
        {
            "信号结果": [
                {
                    "代币地址": token_open,
                    "代币符号": "OPEN",
                    "信号等级": "S4_强确认信号",
                    "策略类型": "SIKK-B 控盘箱体突破回踩",
                    "信号时间": "2026-05-01T00:00:00Z",
                    "信号价格": 1.0,
                    "建议纸面仓位SOL": 0.1,
                    "自动准备输出": {
                        "json": str(
                            _write_json(
                                tmp_path / "signals" / token_open / "token_readiness_result.json",
                                {
                                    "token": token_open,
                                    "position_plan": {"suggested_position_sol": 0.1, "stop_price": 0.8},
                                    "exit_plan": {
                                        "hard_stop_price": 0.8,
                                        "time_stop_minutes": 30,
                                        "take_profit_rules": [
                                            {"触发收益率": 50, "卖出比例": 25},
                                            {"触发收益率": 100, "卖出比例": 25},
                                        ],
                                        "trailing_stop_rule": {"峰值回撤_pct": 35},
                                        "emergency_exit_rules": [],
                                    },
                                },
                            )
                        )
                    },
                },
                {
                    "代币地址": token_block,
                    "代币符号": "BLOCK",
                    "信号等级": "S4_强确认信号",
                    "信号价格": 1.0,
                    "建议纸面仓位SOL": 0.1,
                },
            ]
        },
    )
    quote_security_summary_path = _write_json(
        tmp_path / "quote_security" / "candidate_quote_security_summary.json",
        {
            "处理结果": [
                {"代币地址": token_open, "交易前状态": "READY_FOR_CONFIRMATION", "最终权限": "ALLOW_CONFIRMATION_LAYER"},
                {"代币地址": token_block, "交易前状态": "BLOCK", "最终权限": "BLOCK_BUY"},
            ]
        },
    )
    _write_json(
        tmp_path / "paper_live" / "paper_positions_open.json",
        {
            "open_positions": [
                {
                    "position_id": "paper-existing",
                    "代币地址": token_stop,
                    "代币符号": "STOP",
                    "entry_time": "2026-05-01T00:00:00Z",
                    "entry_price": 1.0,
                    "position_sol": 0.2,
                    "remaining_pct": 100.0,
                    "stop_price": 0.8,
                    "take_profit_rules": [],
                    "triggered_tps": [],
                    "max_price": 1.0,
                    "min_price": 1.0,
                    "status": "OPEN",
                }
            ]
        },
    )

    prices = {
        token_open: {"price": 1.6, "source": "okx", "snapshot_time": "2026-05-01T00:05:00Z"},
        token_stop: {"price": 0.75, "source": "okx", "snapshot_time": "2026-05-01T00:05:00Z"},
        token_block: {"price": 2.0, "source": "okx", "snapshot_time": "2026-05-01T00:05:00Z"},
    }

    paths = run_paper_live_cycle(
        candidate_states_path=states_path,
        signal_summary_path=signal_summary_path,
        quote_security_summary_path=quote_security_summary_path,
        output_dir=tmp_path / "paper_live",
        price_provider=lambda token: prices[token],
        snapshot_time="2026-05-01T00:05:00Z",
    )

    open_payload = _read_json(Path(paths["open_positions_json"]))
    closed_payload = _read_json(Path(paths["closed_positions_json"]))
    metrics = _read_json(Path(paths["strategy_metrics_json"]))
    risk_events = Path(paths["risk_events_jsonl"]).read_text(encoding="utf-8")
    report = Path(paths["daily_report_md"]).read_text(encoding="utf-8")

    open_tokens = {row["代币地址"] for row in open_payload["open_positions"]}
    assert token_open in open_tokens
    assert token_stop not in open_tokens
    assert token_block not in open_tokens

    open_row = next(row for row in open_payload["open_positions"] if row["代币地址"] == token_open)
    assert open_row["status"] == "OPEN"
    assert open_row["entry_price_mode"] == "live"
    assert open_row["signal_entry_price"] == 1.0
    assert open_row["live_entry_price"] == 1.6
    assert open_row["entry_price"] == 1.6
    assert open_row["entry_price_diff_pct"] == 60.0
    assert open_row["cost_model"]["buy_slippage_pct"] == 3
    assert open_row["cost_buffer_pct"] == 7.25
    assert open_row["已触发止盈次数"] == 0
    assert open_row["最大浮盈_pct"] == 0.0

    closed_tokens = {row["代币地址"] for row in closed_payload["closed_positions"]}
    assert token_stop in closed_tokens
    stop_row = next(row for row in closed_payload["closed_positions"] if row["代币地址"] == token_stop)
    assert stop_row["status"] == "CLOSED"
    assert stop_row["exit_reason"] == "命中纸面止损"

    assert metrics["统计"]["新增纸面入场数"] == 1
    assert metrics["统计"]["阻断候选数"] == 1
    assert metrics["统计"]["当前开放仓位数"] == 1
    assert "BLOCK_BUY" in risk_events
    assert "OKX/GMGN 纸面自动交易日报" in report
    assert "不执行真实 swap" in report

    trades = list(csv.DictReader(Path(paths["paper_trades_csv"]).open(encoding="utf-8-sig")))
    assert {row["事件类型"] for row in trades} >= {"PAPER_ENTRY", "PAPER_EXIT"}


def test_paper_live_runner_reads_wallet_delta_and_force_exits_open_position(tmp_path):
    from sikk_paper_live_runner import run_paper_live_cycle

    token = "TokenWalletExit111111111111111111111111111"
    states_path = _write_json(tmp_path / "candidate_states.json", {"候选状态": []})
    signal_summary_path = _write_json(tmp_path / "candidate_signal_summary.json", {"信号结果": []})
    _write_json(
        tmp_path / "paper_live" / "paper_positions_open.json",
        {
            "open_positions": [
                {
                    "position_id": "paper-wallet-exit",
                    "代币地址": token,
                    "代币符号": "WEX",
                    "entry_price": 1.0,
                    "position_sol": 0.1,
                    "remaining_pct": 100.0,
                    "stop_price": 0.5,
                    "take_profit_rules": [],
                    "triggered_tps": [],
                    "max_price": 1.0,
                    "min_price": 1.0,
                    "status": "OPEN",
                }
            ]
        },
    )
    _write_json(
        tmp_path / "wallet_structure" / token / "wallet_structure_decision.json",
        {
            "wallet_structure_status": "WALLET_BLOCK",
            "counterparty_pressure_score": 90,
            "data_quality_score": 90,
            "metrics": {"same_source_sync_sell_score": 80},
        },
    )
    _write_json(
        tmp_path / "wallet_structure" / token / "snapshots" / "latest_delta.json",
        {
            "same_source_group_sold_pct_delta": 35,
            "counterparty_pressure_score_delta": 30,
            "wallet_risk_score_delta": 40,
        },
    )

    paths = run_paper_live_cycle(
        candidate_states_path=states_path,
        signal_summary_path=signal_summary_path,
        output_dir=tmp_path / "paper_live",
        wallet_structure_dir=tmp_path / "wallet_structure",
        price_provider=lambda _token: {"price": 1.1, "source": "okx", "snapshot_time": "2026-05-01T04:00:00Z"},
        snapshot_time="2026-05-01T04:00:00Z",
    )

    open_payload = _read_json(Path(paths["open_positions_json"]))
    closed_payload = _read_json(Path(paths["closed_positions_json"]))
    assert open_payload["open_positions"] == []
    closed = closed_payload["closed_positions"][0]
    assert closed["status"] == "CLOSED"
    assert closed["exit_reason"] == "钱包结构触发纸面强制退出"
    assert closed["failure_type"] == "STRUCTURE_WEAKENING"

    attribution = Path(paths["failure_attribution_jsonl"]).read_text(encoding="utf-8")
    assert "FORCE_PAPER_EXIT" in attribution
    assert "STRUCTURE_WEAKENING" in attribution
    trades = list(csv.DictReader(Path(paths["paper_trades_csv"]).open(encoding="utf-8-sig")))
    assert any(row["事件类型"] == "PAPER_FORCE_EXIT" for row in trades)


def test_paper_live_runner_pauses_on_quote_security_pause_permission(tmp_path):
    from sikk_paper_live_runner import run_paper_live_cycle

    token = "TokenPause11111111111111111111111111111111"
    states_path = _write_json(
        tmp_path / "candidate_states.json",
        {"候选状态": [{"代币地址": token, "代币符号": "PAUSE", "当前状态": "PAPER_READY", "信号价格": 1.0, "建议纸面仓位SOL": 0.1}]},
    )
    signal_summary_path = _write_json(
        tmp_path / "candidate_signal_summary.json",
        {"信号结果": [{"代币地址": token, "代币符号": "PAUSE", "信号价格": 1.0, "建议纸面仓位SOL": 0.1}]},
    )
    quote_security_summary_path = _write_json(
        tmp_path / "quote_security.json",
        {"处理结果": [{"代币地址": token, "交易前状态": "PAUSE", "quote_security_permission": "PAUSE_NEED_CONFIRM"}]},
    )
    calls = []

    paths = run_paper_live_cycle(
        candidate_states_path=states_path,
        signal_summary_path=signal_summary_path,
        quote_security_summary_path=quote_security_summary_path,
        output_dir=tmp_path / "paper_live",
        price_provider=lambda token_: calls.append(token_) or {"price": 1.1, "source": "okx", "snapshot_time": "2026-05-01T01:00:00Z"},
        snapshot_time="2026-05-01T01:00:00Z",
    )

    payload = _read_json(Path(paths["open_positions_json"]))
    metrics = _read_json(Path(paths["strategy_metrics_json"]))
    assert payload["open_positions"] == []
    assert metrics["统计"]["新增纸面入场数"] == 0
    assert calls == []


def test_decide_wallet_position_action_forces_paper_exit_on_wallet_block():
    from sikk_paper_live_runner import decide_wallet_position_action

    action = decide_wallet_position_action(
        position={"代币地址": "TokenExit111", "当前收益率_pct": -8},
        current_decision={
            "wallet_structure_status": "WALLET_BLOCK",
            "counterparty_pressure_score": 82,
            "data_quality_score": 90,
            "metrics": {"same_source_sync_sell_score": 20},
        },
        latest_delta={"wallet_risk_score_delta": 35},
        mode="paper",
    )

    assert action["action"] == "FORCE_PAPER_EXIT"
    assert action["failure_type"] == "STRUCTURE_WEAKENING"
    assert "纸面" in action["reason"]
    assert "不执行真实 swap" in action["scope_note"]


def test_decide_wallet_position_action_uses_confirmation_in_live_mode_not_auto_exit():
    from sikk_paper_live_runner import decide_wallet_position_action

    action = decide_wallet_position_action(
        position={"代币地址": "TokenLive111", "当前收益率_pct": 12},
        current_decision={
            "wallet_structure_status": "WALLET_BLOCK",
            "counterparty_pressure_score": 82,
            "data_quality_score": 90,
            "metrics": {"same_source_sync_sell_score": 80},
        },
        latest_delta={"same_source_group_sold_pct_delta": 30},
        mode="live",
    )

    assert action["action"] == "REAL_TRADE_CONFIRMATION_REQUIRED"
    assert action["failure_type"] in {"STRUCTURE_WEAKENING", "SAME_SOURCE_EXIT"}
    assert "不自动卖出" in action["scope_note"]


def test_decide_wallet_position_action_monitors_profitable_early_wallet_exit():
    from sikk_paper_live_runner import decide_wallet_position_action

    action = decide_wallet_position_action(
        position={"代币地址": "TokenMonitor111", "当前收益率_pct": 45},
        current_decision={
            "wallet_structure_status": "WALLET_SUPPORT",
            "counterparty_pressure_score": 30,
            "data_quality_score": 88,
            "metrics": {"same_source_sync_sell_score": 20},
        },
        latest_delta={"early_wallet_sold_pct_delta": 22, "wallet_risk_score_delta": 5},
        mode="paper",
    )

    assert action["action"] == "EXIT_MONITOR"
    assert action["failure_type"] == "WALLET_EXIT"


def test_okx_readonly_price_provider_parses_market_price_without_swap_command():
    from sikk_paper_live_runner import build_okx_market_price_provider

    calls = []

    def fake_runner(command):
        calls.append(command)
        return json.dumps({"data": {"price": "0.00042", "time": "2026-05-01T02:00:00Z"}})

    provider = build_okx_market_price_provider(runner=fake_runner)
    price = provider("TokenPrice111111111111111111111111111111")

    assert price["price"] == 0.00042
    assert price["source"] == "okx_market_price"
    assert price["snapshot_time"] == "2026-05-01T02:00:00Z"
    assert calls == [["onchainos", "market", "price", "--address", "TokenPrice111111111111111111111111111111", "--chain", "solana"]]
    flattened = " ".join(" ".join(c) for c in calls)
    assert "swap execute" not in flattened
    assert "gmgn-cli swap" not in flattened


def test_paper_live_runner_does_not_reenter_existing_open_position(tmp_path):
    from sikk_paper_live_runner import run_paper_live_cycle

    token = "TokenSame111111111111111111111111111111111"
    states_path = _write_json(
        tmp_path / "candidate_states.json",
        {"候选状态": [{"代币地址": token, "代币符号": "SAME", "当前状态": "PAPER_READY", "信号价格": 1.0, "建议纸面仓位SOL": 0.1}]},
    )
    signal_summary_path = _write_json(
        tmp_path / "candidate_signal_summary.json",
        {"信号结果": [{"代币地址": token, "代币符号": "SAME", "信号价格": 1.0, "建议纸面仓位SOL": 0.1}]},
    )
    quote_security_summary_path = _write_json(
        tmp_path / "quote_security.json",
        {"处理结果": [{"代币地址": token, "交易前状态": "READY_FOR_CONFIRMATION", "最终权限": "ALLOW_CONFIRMATION_LAYER"}]},
    )
    _write_json(
        tmp_path / "paper_live" / "paper_positions_open.json",
        {"open_positions": [{"position_id": "paper-existing", "代币地址": token, "代币符号": "SAME", "entry_price": 1.0, "position_sol": 0.1, "remaining_pct": 100.0, "stop_price": 0.8, "take_profit_rules": [], "triggered_tps": [], "max_price": 1.0, "min_price": 1.0, "status": "OPEN"}]},
    )

    paths = run_paper_live_cycle(
        candidate_states_path=states_path,
        signal_summary_path=signal_summary_path,
        quote_security_summary_path=quote_security_summary_path,
        output_dir=tmp_path / "paper_live",
        price_provider=lambda _token: {"price": 1.1, "source": "okx", "snapshot_time": "2026-05-01T01:00:00Z"},
        snapshot_time="2026-05-01T01:00:00Z",
    )
    payload = _read_json(Path(paths["open_positions_json"]))
    assert len(payload["open_positions"]) == 1
    metrics = _read_json(Path(paths["strategy_metrics_json"]))
    assert metrics["统计"]["新增纸面入场数"] == 0
    assert metrics["统计"]["重复持仓跳过数"] == 1


def test_paper_live_runner_logs_entry_price_failure_and_continues(tmp_path):
    from sikk_paper_live_runner import run_paper_live_cycle

    token_bad = "TokenBad1111111111111111111111111111111111"
    token_good = "TokenGood111111111111111111111111111111111"
    states_path = _write_json(
        tmp_path / "candidate_states.json",
        {
            "候选状态": [
                {"代币地址": token_bad, "代币符号": "BAD", "当前状态": "PAPER_READY", "信号价格": 1.0, "建议纸面仓位SOL": 0.1},
                {"代币地址": token_good, "代币符号": "GOOD", "当前状态": "PAPER_READY", "信号价格": 1.0, "建议纸面仓位SOL": 0.1},
            ]
        },
    )
    signal_summary_path = _write_json(
        tmp_path / "candidate_signal_summary.json",
        {
            "信号结果": [
                {"代币地址": token_bad, "代币符号": "BAD", "信号价格": 1.0, "建议纸面仓位SOL": 0.1},
                {"代币地址": token_good, "代币符号": "GOOD", "信号价格": 1.0, "建议纸面仓位SOL": 0.1},
            ]
        },
    )
    quote_security_summary_path = _write_json(
        tmp_path / "quote_security.json",
        {
            "处理结果": [
                {"代币地址": token_bad, "交易前状态": "READY_FOR_CONFIRMATION", "最终权限": "ALLOW_CONFIRMATION_LAYER"},
                {"代币地址": token_good, "交易前状态": "READY_FOR_CONFIRMATION", "最终权限": "ALLOW_CONFIRMATION_LAYER"},
            ]
        },
    )

    def flaky_price_provider(token):
        if token == token_bad:
            raise ValueError("OKX market price 未返回有效价格")
        return {"price": 1.2, "source": "okx", "snapshot_time": "2026-05-01T03:00:00Z"}

    paths = run_paper_live_cycle(
        candidate_states_path=states_path,
        signal_summary_path=signal_summary_path,
        quote_security_summary_path=quote_security_summary_path,
        output_dir=tmp_path / "paper_live",
        price_provider=flaky_price_provider,
        snapshot_time="2026-05-01T03:00:00Z",
    )

    payload = _read_json(Path(paths["open_positions_json"]))
    metrics = _read_json(Path(paths["strategy_metrics_json"]))
    risk_events = Path(paths["risk_events_jsonl"]).read_text(encoding="utf-8")

    assert [row["代币地址"] for row in payload["open_positions"]] == [token_good]
    assert metrics["统计"]["新增纸面入场数"] == 1
    assert "PAPER_ENTRY_PRICE_FAILED" in risk_events
    assert token_bad in risk_events
