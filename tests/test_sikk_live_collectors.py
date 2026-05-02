import json
from pathlib import Path


def test_gmgn_quote_collector_builds_readonly_command_and_parses_raw_quote():
    from sikk_live_quote_security_collector import GMGNLiveQuoteCollector
    from sikk_execution_adapter_base import QuoteRequest

    collector = GMGNLiveQuoteCollector()
    request = QuoteRequest(
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        input_token="So11111111111111111111111111111111111111112",
        output_token="Token11111111111111111111111111111111111",
        amount_smallest_unit="10000000",
        slippage=0.3,
    )
    command = collector.build_command(request)
    assert command[:3] == ["gmgn-cli", "order", "quote"]
    assert "swap" not in command
    assert "execute" not in command

    raw = json.dumps({
        "code": 0,
        "data": {
            "input_token": request.input_token,
            "output_token": request.output_token,
            "input_amount": "10000000",
            "output_amount": "250000000",
            "min_output_amount": "225000000",
            "slippage": 0.3,
        },
    })
    result = collector.parse_output(raw, request)
    assert result.source == "GMGN"
    assert result.output_amount == "250000000"
    assert result.min_output_amount == "225000000"
    assert result.raw["code"] == 0


def test_okx_quote_collector_parses_price_impact_from_onchainos_quote():
    from sikk_live_quote_security_collector import OKXLiveQuoteCollector
    from sikk_execution_adapter_base import QuoteRequest

    collector = OKXLiveQuoteCollector()
    request = QuoteRequest(
        chain="solana",
        wallet_address="Wallet1111111111111111111111111111111111",
        input_token="11111111111111111111111111111111",
        output_token="Token11111111111111111111111111111111111",
        readable_amount="0.01",
    )
    command = collector.build_command(request)
    assert command[:3] == ["onchainos", "swap", "quote"]
    assert "execute" not in command

    raw = json.dumps({
        "fromTokenAmount": "0.01",
        "toTokenAmount": "23888.5",
        "minReceiveAmount": "23000",
        "priceImpact": "1.25%",
        "routerResult": {"dexRouterList": ["raydium"]},
    })
    result = collector.parse_output(raw, request)
    assert result.source == "OKX"
    assert result.input_amount == "0.01"
    assert result.output_amount == "23888.5"
    assert result.min_output_amount == "23000"
    assert result.price_impact_pct == 1.25


def test_okx_security_collector_builds_token_scan_and_extracts_triggered_labels():
    from sikk_live_quote_security_collector import OKXSecurityScanCollector
    from sikk_execution_adapter_base import TokenSide

    collector = OKXSecurityScanCollector()
    command = collector.build_command(chain_id="501", token_address="Token11111111111111111111111111111111111")
    assert command == [
        "onchainos",
        "security",
        "token-scan",
        "--tokens",
        "501:Token11111111111111111111111111111111111",
    ]

    raw = json.dumps({
        "data": [
            {
                "chainId": "501",
                "tokenAddress": "Token11111111111111111111111111111111111",
                "riskLevel": "HIGH",
                "isHoneypot": False,
                "isLowLiquidity": True,
                "isPump": True,
                "isMintable": False,
                "buyTaxes": None,
                "sellTaxes": "0",
            }
        ]
    })
    result = collector.parse_output(raw, token_address="Token11111111111111111111111111111111111", token_side=TokenSide.BUY)
    assert result.source == "OKX"
    assert result.risk_level == "HIGH"
    assert "isLowLiquidity" in result.triggered_labels
    assert "isPump" in result.triggered_labels
    assert "isHoneypot" not in result.triggered_labels


def test_live_collector_runner_injection_collects_quotes_and_scan_without_real_execution():
    from sikk_live_quote_security_collector import collect_live_pre_trade_inputs
    from sikk_execution_adapter_base import QuoteRequest

    calls = []

    def fake_runner(command):
        calls.append(command)
        joined = " ".join(command)
        if command[:3] == ["gmgn-cli", "order", "quote"]:
            return json.dumps({"data": {"input_amount": "10000000", "output_amount": "250000000", "min_output_amount": "225000000"}})
        if command[:3] == ["onchainos", "swap", "quote"]:
            return json.dumps({"fromTokenAmount": "0.01", "toTokenAmount": "249000000", "minReceiveAmount": "240000000", "priceImpact": "2.5"})
        if joined.startswith("onchainos security token-scan"):
            return json.dumps({"data": [{"tokenAddress": "Token11111111111111111111111111111111111", "riskLevel": "LOW"}]})
        raise AssertionError(f"unexpected command: {command}")

    gmgn_request = QuoteRequest(
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        input_token="So11111111111111111111111111111111111111112",
        output_token="Token11111111111111111111111111111111111",
        amount_smallest_unit="10000000",
    )
    okx_request = QuoteRequest(
        chain="solana",
        wallet_address="Wallet1111111111111111111111111111111111",
        input_token="11111111111111111111111111111111",
        output_token="Token11111111111111111111111111111111111",
        readable_amount="0.01",
    )

    quotes, scans = collect_live_pre_trade_inputs(
        gmgn_request=gmgn_request,
        okx_request=okx_request,
        okx_chain_id="501",
        scan_token_address="Token11111111111111111111111111111111111",
        runner=fake_runner,
    )
    assert [q.source for q in quotes] == ["GMGN", "OKX"]
    assert scans[0].risk_level == "LOW"
    flattened = " ".join(" ".join(c) for c in calls)
    assert "gmgn-cli swap" not in flattened
    assert "onchainos swap execute" not in flattened


def test_collect_and_write_pre_trade_review_uses_live_inputs_for_non_missing_files(tmp_path):
    from sikk_live_quote_security_collector import collect_and_write_live_pre_trade_review
    from sikk_execution_adapter_base import QuoteRequest

    def fake_runner(command):
        if command[:3] == ["gmgn-cli", "order", "quote"]:
            return json.dumps({"data": {"input_amount": "10000000", "output_amount": "250000000", "min_output_amount": "245000000"}})
        if command[:3] == ["onchainos", "swap", "quote"]:
            return json.dumps({"fromTokenAmount": "0.01", "toTokenAmount": "249000000", "minReceiveAmount": "244000000", "priceImpact": "1.5%"})
        if command[:3] == ["onchainos", "security", "token-scan"]:
            return json.dumps({"data": [{"tokenAddress": "Token11111111111111111111111111111111111", "riskLevel": "LOW"}]})
        raise AssertionError(command)

    readiness_payload = {
        "token": "Token11111111111111111111111111111111111",
        "risk_gate": {"permission": "ALLOW_PAPER_TRADE_允许纸面交易", "risk_level": "低", "block_reasons": [], "pause_reasons": [], "allow_reasons": ["安全层通过"], "missing_evidence": []},
        "signal": {"signal_level": "S4_强确认信号", "strategy_type": "SIKK-B 控盘箱体突破回踩", "signal_time": "2026-04-27 16:37:00 UTC", "signal_price": 0.00023386184, "confidence_score": 95, "evidence": ["突破控盘箱体"], "invalidation_reasons": []},
        "position_plan": {"suggested_position_sol": 0.1, "max_position_sol": 0.2, "risk_per_trade_sol": 0.025, "stop_price": 0.00018, "stop_type": "结构止损", "position_reason": "按风险计算"},
        "exit_plan": {"hard_stop_price": 0.00018, "time_stop_minutes": 30, "take_profit_rules": [], "trailing_stop_rule": {}, "emergency_exit_rules": []},
    }
    gmgn_request = QuoteRequest(chain="sol", wallet_address="Wallet1111111111111111111111111111111111", input_token="So11111111111111111111111111111111111111112", output_token="Token11111111111111111111111111111111111", amount_smallest_unit="10000000")
    okx_request = QuoteRequest(chain="solana", wallet_address="Wallet1111111111111111111111111111111111", input_token="11111111111111111111111111111111", output_token="Token11111111111111111111111111111111111", readable_amount="0.01")

    paths = collect_and_write_live_pre_trade_review(
        output_dir=tmp_path,
        readiness_payload=readiness_payload,
        chain="sol",
        wallet_address="Wallet1111111111111111111111111111111111",
        human_amount="0.01 SOL",
        gmgn_request=gmgn_request,
        okx_request=okx_request,
        okx_chain_id="501",
        scan_token_address="Token11111111111111111111111111111111111",
        snapshot_time="2026-04-30T00:00:00Z",
        runner=fake_runner,
    )

    quote_snapshot = json.loads(Path(paths["quote_snapshot_json"]).read_text(encoding="utf-8"))
    security_report = json.loads(Path(paths["security_scan_report_json"]).read_text(encoding="utf-8"))
    decision = json.loads(Path(paths["quote_security_decision_json"]).read_text(encoding="utf-8"))
    assert quote_snapshot["quote_status"] == "AVAILABLE"
    assert quote_snapshot["source_count"] == 2
    assert security_report["scan_status"] == "AVAILABLE"
    assert decision["final_permission"] == "ALLOW_CONFIRMATION_LAYER"
