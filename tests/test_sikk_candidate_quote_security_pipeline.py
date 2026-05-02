import csv
import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def _readiness_payload(token: str) -> dict:
    return {
        "token": token,
        "risk_gate": {
            "permission": "ALLOW_PAPER_TRADE_允许纸面交易",
            "risk_level": "低",
            "block_reasons": [],
            "pause_reasons": [],
            "allow_reasons": ["纸面风险门禁通过"],
            "missing_evidence": [],
        },
        "signal": {
            "signal_level": "S4_强确认信号",
            "strategy_type": "SIKK-B 控盘箱体突破回踩",
            "signal_time": "2026-04-30 11:41:00 UTC",
            "signal_price": 0.0001,
            "confidence_score": 99,
            "evidence": ["吸筹窗口 valid", "突破 LH"],
            "invalidation_reasons": [],
        },
        "position_plan": {
            "suggested_position_sol": 0.12,
            "max_position_sol": 0.2,
            "risk_per_trade_sol": 0.025,
            "stop_price": 0.00008,
            "stop_type": "结构止损",
            "position_reason": "按 S4 风险预算计算",
        },
        "exit_plan": {
            "hard_stop_price": 0.00008,
            "time_stop_minutes": 30,
            "take_profit_rules": [],
            "trailing_stop_rule": {},
            "emergency_exit_rules": [],
        },
    }


def test_candidate_quote_security_pipeline_processes_only_paper_ready_and_maps_decisions(tmp_path):
    from sikk_candidate_quote_security_pipeline import run_candidate_quote_security_pipeline

    token_allow = "TokenAllow1111111111111111111111111111111"
    token_pause = "TokenPause1111111111111111111111111111111"
    token_block = "TokenBlock1111111111111111111111111111111"
    token_watch = "TokenWatch11111111111111111111111111111111"

    readiness_allow = _write_json(tmp_path / "signals" / token_allow / "token_readiness_result.json", _readiness_payload(token_allow))
    readiness_pause = _write_json(tmp_path / "signals" / token_pause / "token_readiness_result.json", _readiness_payload(token_pause))
    readiness_block = _write_json(tmp_path / "signals" / token_block / "token_readiness_result.json", _readiness_payload(token_block))

    states_path = _write_json(
        tmp_path / "state_machine" / "candidate_states.json",
        {
            "候选状态": [
                {"代币地址": token_allow, "代币符号": "ALLOW", "当前状态": "PAPER_READY", "建议纸面仓位SOL": 0.12},
                {"代币地址": token_pause, "代币符号": "PAUSE", "当前状态": "PAPER_READY", "建议纸面仓位SOL": 0.12},
                {"代币地址": token_block, "代币符号": "BLOCK", "当前状态": "PAPER_READY", "建议纸面仓位SOL": 0.12},
                {"代币地址": token_watch, "代币符号": "WATCH", "当前状态": "WATCHING", "建议纸面仓位SOL": 0},
            ]
        },
    )
    signal_summary_path = _write_json(
        tmp_path / "candidate_signal_summary.json",
        {
            "信号结果": [
                {"代币地址": token_allow, "自动准备输出": {"json": str(readiness_allow)}},
                {"代币地址": token_pause, "自动准备输出": {"json": str(readiness_pause)}},
                {"代币地址": token_block, "自动准备输出": {"json": str(readiness_block)}},
            ]
        },
    )

    calls = []

    def fake_runner(command):
        calls.append(command)
        joined = " ".join(command)
        if command[:3] == ["gmgn-cli", "order", "quote"]:
            token = command[command.index("--output-token") + 1]
            output = "1000"
            if token == token_pause:
                output = "1000"
            if token == token_block:
                output = "1000"
            return json.dumps({"data": {"input_amount": command[command.index("--amount") + 1], "output_amount": output, "min_output_amount": "900"}})
        if command[:3] == ["onchainos", "swap", "quote"]:
            token = command[command.index("--to") + 1]
            impact = "1.2"
            if token == token_pause:
                impact = "6.5"
            if token == token_block:
                impact = "12.5"
            return json.dumps({"fromTokenAmount": "0.12", "toTokenAmount": "995", "minReceiveAmount": "930", "priceImpact": impact})
        if command[:3] == ["onchainos", "security", "token-scan"]:
            token = command[-1].split(":", 1)[1]
            risk = "LOW"
            labels = {}
            if token == token_pause:
                risk = "HIGH"
                labels = {"isLowLiquidity": True}
            if token == token_block:
                risk = "CRITICAL"
                labels = {"isHoneypot": True}
            return json.dumps({"data": [{"tokenAddress": token, "riskLevel": risk, **labels}]})
        raise AssertionError(f"unexpected command: {command}")

    paths = run_candidate_quote_security_pipeline(
        candidate_states_path=states_path,
        signal_summary_path=signal_summary_path,
        output_dir=tmp_path / "quote_security",
        wallet_address="Wallet1111111111111111111111111111111111",
        default_amount_sol=0.12,
        runner=fake_runner,
        snapshot_time="2026-04-30T12:00:00Z",
    )

    summary = json.loads(Path(paths["summary_json"]).read_text(encoding="utf-8"))
    assert summary["处理统计"] == {
        "读取状态数": 4,
        "PAPER_READY数量": 3,
        "成功数量": 3,
        "跳过数量": 1,
        "失败数量": 0,
        "READY_FOR_CONFIRMATION": 1,
        "PAUSE": 1,
        "BLOCK": 1,
    }
    statuses = {row["代币符号"]: row["交易前状态"] for row in summary["处理结果"]}
    assert statuses == {"ALLOW": "READY_FOR_CONFIRMATION", "PAUSE": "PAUSE", "BLOCK": "BLOCK"}
    assert summary["跳过结果"][0]["代币符号"] == "WATCH"

    for row in summary["处理结果"]:
        review_dir = Path(row["审查输出目录"])
        assert (review_dir / "quote_snapshot.json").exists()
        assert (review_dir / "security_scan_report.json").exists()
        assert (review_dir / "quote_security_decision.json").exists()

    csv_rows = list(csv.DictReader(Path(paths["summary_csv"]).open(encoding="utf-8-sig")))
    assert len(csv_rows) == 3
    md = Path(paths["summary_md"]).read_text(encoding="utf-8")
    assert "不执行真实 swap" in md
    assert "READY_FOR_CONFIRMATION" in md

    flattened = " ".join(" ".join(c) for c in calls)
    assert "gmgn-cli swap" not in flattened
    assert "order strategy create" not in flattened
    assert "onchainos swap execute" not in flattened


def test_candidate_quote_security_pipeline_pauses_when_readiness_file_missing(tmp_path):
    from sikk_candidate_quote_security_pipeline import run_candidate_quote_security_pipeline

    states_path = _write_json(
        tmp_path / "candidate_states.json",
        {"候选状态": [{"代币地址": "TokenMissing111111111111111111111111111", "代币符号": "MISS", "当前状态": "PAPER_READY"}]},
    )
    signal_summary_path = _write_json(tmp_path / "candidate_signal_summary.json", {"信号结果": []})

    paths = run_candidate_quote_security_pipeline(
        candidate_states_path=states_path,
        signal_summary_path=signal_summary_path,
        output_dir=tmp_path / "quote_security",
        wallet_address="Wallet1111111111111111111111111111111111",
        runner=lambda command: (_ for _ in ()).throw(AssertionError("不应调用 CLI")),
    )

    summary = json.loads(Path(paths["summary_json"]).read_text(encoding="utf-8"))
    assert summary["处理统计"]["失败数量"] == 1
    assert summary["失败结果"][0]["交易前状态"] == "PAUSE"
    assert "缺少 readiness JSON" in summary["失败结果"][0]["原因"]
