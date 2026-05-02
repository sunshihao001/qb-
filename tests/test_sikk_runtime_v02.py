import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_module_runner_skips_existing_outputs_and_records_errors(tmp_path):
    from sikk_module_runner import run_external_modules_for_token

    token = {"token_address": "TokenRuntime111", "token_symbol": "RUN"}
    base_dir = tmp_path / "live"
    _write_json(base_dir / "wallet_structure" / token["token_address"] / "wallet_structure_decision.json", {"ok": True})
    calls = []

    def fake_script_runner(command):
        calls.append(command)
        if "quote_script.py" in command:
            raise RuntimeError("quote failed")
        return "{}"

    result = run_external_modules_for_token(
        token=token,
        config={
            "base_dir": str(base_dir),
            "modules": {
                "wallet_structure": {"enabled": True, "mode": "script", "script_path": "wallet_script.py"},
                "quote": {"enabled": True, "mode": "script", "script_path": "quote_script.py"},
                "paper_runner": {"enabled": True, "mode": "script", "script_path": "paper_script.py"},
            },
        },
        script_runner=fake_script_runner,
    )

    by_module = {row["module"]: row for row in result["module_results"]}
    assert by_module["wallet_structure"]["status"] == "SKIPPED"
    assert by_module["quote"]["status"] == "ERROR"
    assert by_module["paper_runner"]["status"] == "OK"
    flattened = " ".join(" ".join(cmd) for cmd in calls)
    assert "quote_script.py" in flattened
    assert "paper_script.py" in flattened
    assert "wallet_script.py" not in flattened


def test_trace_logger_writes_state_change_before_status_overwrite(tmp_path):
    from sikk_trace_logger import write_process_trace

    token = {"token_address": "TokenTrace111", "token_symbol": "TRC"}
    token_dir = tmp_path / "tokens" / token["token_address"]
    _write_json(
        token_dir / "token_status.json",
        {
            "current_state": "WATCHING",
            "wallet_structure": {"wallet_structure_status": "WALLET_NEUTRAL"},
            "paper": {"paper_status": "NONE"},
        },
    )

    current = {
        "current_state": "PAPER_READY",
        "latest_action": "ALLOW_PAPER",
        "latest_reason": "钱包结构支持",
        "wallet_structure": {"wallet_structure_status": "WALLET_SUPPORT"},
        "paper": {"paper_status": "READY"},
    }
    write_process_trace(token=token, current_status=current, module_result={"ok": True}, base_dir=tmp_path)

    lines = (token_dir / "process_trace.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    row = json.loads(lines[0])
    assert row["state_changed"] is True
    assert row["previous_state"] == "WATCHING"
    assert row["current_state"] == "PAPER_READY"
    assert row["previous_wallet_status"] == "WALLET_NEUTRAL"
    assert row["current_wallet_status"] == "WALLET_SUPPORT"
    assert row["module_result"] == {"ok": True}


def test_skip_policy_cools_down_blocked_and_processes_paper_open(tmp_path):
    from sikk_token_skip_policy import should_process_token

    blocked = {"token_address": "TokenBlocked111", "token_symbol": "BLK"}
    paper_open = {"token_address": "TokenOpen111", "token_symbol": "OPN"}
    _write_json(tmp_path / "tokens" / blocked["token_address"] / "token_status.json", {"current_state": "BLOCKED", "last_update": "2026-05-02T00:00:00Z"})
    _write_json(tmp_path / "tokens" / paper_open["token_address"] / "token_status.json", {"current_state": "PAPER_OPEN", "last_update": "2026-05-02T00:00:00Z"})

    process_blocked, reason_blocked = should_process_token(blocked, base_dir=tmp_path, now="2026-05-02T01:00:00Z")
    process_open, reason_open = should_process_token(paper_open, base_dir=tmp_path, now="2026-05-02T01:00:00Z")

    assert process_blocked is False
    assert "BLOCKED" in reason_blocked
    assert process_open is True
    assert "continuous" in reason_open


def test_dashboard_builder_writes_html_with_token_status_and_events(tmp_path):
    from sikk_dashboard_builder import write_dashboard

    _write_json(
        tmp_path / "live_state.json",
        {
            "last_update": "2026-05-02T00:00:00Z",
            "token_count": 1,
            "tokens": [
                {
                    "token_address": "TokenDash111",
                    "token_symbol": "DSH",
                    "current_state": "PAPER_READY",
                    "discovered_at": "2026-05-02T00:00:00Z",
                    "discovery_market_cap_usd": 12345,
                    "priority_level": "P1_PAPER_READY",
                    "wallet_structure": {"wallet_structure_status": "WALLET_SUPPORT", "wallet_structure_score": 88, "wallet_risk_score": 10, "counterparty_pressure_score": 12, "data_quality_score": 90, "wallet_decision_at": "2026-05-02T00:03:00Z"},
                    "signal": {"signal_level": "S3", "signal_gate": "PASS", "first_signal_at": "2026-05-02T00:02:00Z", "first_signal_type": "ACCUMULATION"},
                    "quote": {"quote_gate": "PASS"},
                    "security": {"security_gate": "PASS"},
                    "paper": {"paper_status": "READY", "unrealized_pnl_pct": 0},
                    "latest_action": "OPEN_PAPER_POSITION",
                    "latest_reason": "测试通过",
                }
            ],
        },
    )
    events_dir = tmp_path / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    (events_dir / "live_events.jsonl").write_text(json.dumps({"time": "2026-05-02T00:00:00Z", "event_type": "PAPER_READY", "token_symbol": "DSH", "message": "进入纸面准备"}, ensure_ascii=False) + "\n", encoding="utf-8")
    _write_json(
        tmp_path / "paper_live" / "paper_positions_open.json",
        {
            "open_positions": [
                {
                    "代币地址": "TokenDash111",
                    "代币符号": "DSH",
                    "entry_time": "2026-05-02T00:04:00Z",
                    "entry_price": 0.42,
                    "position_sol": 0.01,
                    "last_price": 0.46,
                    "当前收益率_pct": 9.5238,
                    "wallet_position_action": "EXIT_MONITOR",
                    "last_update_time": "2026-05-02T00:05:00Z",
                }
            ]
        },
    )
    (tmp_path / "paper_live" / "failure_attribution.jsonl").write_text(
        json.dumps({"事件时间": "2026-05-02T00:05:00Z", "事件类型": "EXIT_MONITOR", "代币地址": "TokenDash111", "failure_type": "WALLET_EXIT", "failure_reason": "早期钱包卖出增加"}, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    path = write_dashboard(base_dir=tmp_path)
    html = Path(path).read_text(encoding="utf-8")
    assert "SIKK-SOL Live Dashboard" in html
    assert "DSH" in html
    assert "WALLET_SUPPORT" in html
    assert "PAPER_READY" in html
    assert "id=\"token-search\"" in html
    assert "id=\"state-filter\"" in html
    assert "id=\"wallet-filter\"" in html
    assert "Priority" in html
    assert "Next" in html
    assert "discovered_at" in html
    assert "paper_entry_at" in html
    assert "current_price" in html
    assert "failure_attribution_type" in html
    assert "2026-05-02T00:04:00Z" in html
    assert "0.42" in html
    assert "WALLET_EXIT" in html
    assert "待补" in html


def test_professional_live_board_has_decision_sections_priority_and_reasons(tmp_path):
    from sikk_live_orchestrator import write_live_board

    statuses = [
        {
            "token_address": "TokenA",
            "token_symbol": "AAA",
            "current_state": "BLOCKED",
            "priority_level": "P5_BLOCKED",
            "latest_reason": "同源组同步卖出",
            "latest_action": "COOLING",
            "wallet_structure": {"wallet_structure_status": "WALLET_BLOCK", "wallet_structure_score": 20, "wallet_risk_score": 90, "counterparty_pressure_score": 80, "data_quality_score": 95},
            "signal": {"signal_level": "SX", "signal_gate": "BLOCK"},
            "quote": {"quote_gate": "PASS"},
            "security": {"security_gate": "PASS"},
            "paper": {"paper_status": "NONE"},
        },
        {
            "token_address": "TokenB",
            "token_symbol": "BBB",
            "current_state": "PAPER_READY",
            "latest_reason": "钱包结构支持，等待 paper runner",
            "wallet_structure": {"wallet_structure_status": "WALLET_SUPPORT", "wallet_structure_score": 80, "wallet_risk_score": 10, "counterparty_pressure_score": 8, "data_quality_score": 90},
            "signal": {"signal_level": "S3", "signal_gate": "PASS"},
            "quote": {"quote_gate": "PASS"},
            "security": {"security_gate": "PASS"},
            "paper": {"paper_status": "READY", "unrealized_pnl_pct": 0},
        },
        {
            "token_address": "TokenC",
            "token_symbol": "CCC",
            "current_state": "WATCHING",
            "latest_reason": "early_wallet_raw.csv missing",
            "wallet_structure": {"wallet_structure_status": "MISSING", "missing_reason": "early_wallet_raw.csv missing"},
            "signal": {"signal_level": "S1", "signal_gate": "WAIT"},
            "quote": {"quote_gate": "MISSING"},
            "security": {"security_gate": "MISSING"},
            "paper": {"paper_status": "NONE"},
        },
    ]

    path = write_live_board(statuses, base_dir=tmp_path, now="2026-05-02T00:00:00Z")
    board = Path(path).read_text(encoding="utf-8")
    for title in ["## 1. 系统总览", "## 2. 重点机会", "## 3. 钱包结构状态", "## 4. 阻断 / 暂停原因", "## 5. 当前纸面仓位", "## 6. 未入场原因 Top", "## 7. 今日纸面验证", "## 8. 最新事件"]:
        assert title in board
    assert "P1_PAPER_READY" in board
    assert "OPEN_PAPER_POSITION" in board
    assert "同源组同步卖出" in board
    assert "early_wallet_raw.csv missing" in board
    assert "wallet_structure_missing" in board
    assert "钱包结构接入率" in board
    assert board.index("BBB") < board.index("AAA")


def test_notifier_sends_only_important_events_without_secrets_in_message():
    from sikk_notifier import notify_event

    sent = []

    notify_event(
        {"time": "2026-05-02T00:00:00Z", "event_type": "DEBUG", "token_symbol": "DBG", "message": "debug"},
        {"notification": {"enabled": True, "channels": ["discord"], "discord_webhook_url": "https://discord.example/hook"}},
        post_json=lambda url, payload: sent.append((url, payload)),
    )
    assert sent == []

    notify_event(
        {"time": "2026-05-02T00:00:00Z", "event_type": "WALLET_BLOCK", "token_symbol": "BLK", "token_address": "TokenBlock", "message": "钱包结构阻断"},
        {"notification": {"enabled": True, "channels": ["discord"], "discord_webhook_url": "https://discord.example/hook"}},
        post_json=lambda url, payload: sent.append((url, payload)),
    )
    assert len(sent) == 1
    assert sent[0][0] == "https://discord.example/hook"
    assert "钱包结构阻断" in sent[0][1]["content"]


def test_live_orchestrator_once_writes_state_board_dashboard_trace_and_skip_events(tmp_path):
    from sikk_live_orchestrator import run_once

    token_new = {"token_address": "TokenNew111", "token_symbol": "NEW"}
    token_blocked = {"token_address": "TokenOldBlocked111", "token_symbol": "OLD"}
    _write_json(
        tmp_path / "tokens" / token_blocked["token_address"] / "token_status.json",
        {"token_address": token_blocked["token_address"], "token_symbol": "OLD", "current_state": "BLOCKED", "last_update": "2026-05-02T00:00:00Z", "wallet_structure": {"wallet_structure_status": "WALLET_BLOCK"}},
    )

    def fake_module_runner(token, config, force=False):
        assert token["token_address"] == token_new["token_address"]
        return {"token_address": token["token_address"], "module_results": [{"module": "wallet_structure", "status": "OK", "reason": "done"}]}

    paths = run_once(
        candidates=[token_new, token_blocked],
        base_dir=tmp_path,
        config={"base_dir": str(tmp_path)},
        module_runner=fake_module_runner,
        now="2026-05-02T01:00:00Z",
    )

    assert Path(paths["live_state_json"]).exists()
    assert Path(paths["live_board_md"]).exists()
    assert Path(paths["live_dashboard_html"]).exists()
    assert Path(paths["latest_events_md"]).exists()
    assert (tmp_path / "events" / "live_events.jsonl").exists()
    assert (tmp_path / "tokens" / token_new["token_address"] / "token_status.json").exists()
    assert (tmp_path / "tokens" / token_new["token_address"] / "process_trace.jsonl").exists()

    live_state = _read_json(Path(paths["live_state_json"]))
    by_token = {row["token_address"]: row for row in live_state["tokens"]}
    assert by_token[token_new["token_address"]]["current_state"] == "WATCHING"
    assert by_token[token_blocked["token_address"]]["current_state"] == "BLOCKED"
    events = (tmp_path / "events" / "live_events.jsonl").read_text(encoding="utf-8")
    assert "TOKEN_SKIPPED" in events
    assert "MODULES_FINISHED" in events
