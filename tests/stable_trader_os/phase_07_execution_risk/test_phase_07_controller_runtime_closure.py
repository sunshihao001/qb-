from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from modules.stable_trader_os.phase_07_execution_risk_controller import Phase07ExecutionRiskController


def _write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields or ["empty"])
        writer.writeheader()
        if rows:
            writer.writerows(rows)


def _phase07_package(
    tmp_path: Path,
    *,
    strategy_status: str = "PAPER_READY",
    a_plus_p1_status: str = "A_PLUS_P1_PASS",
    hard_negative: bool = False,
    quote_valid: bool = True,
    quote_age_seconds: int = 30,
    security_status: str = "SECURITY_OK",
    liquidity_usd: float = 120000,
    slippage_bps: int = 120,
    open_position: bool = False,
    daily_loss_pct: float = 0.0,
    allow_paper_trade: bool = True,
) -> Path:
    run = tmp_path / "run"
    p06 = run / "06_strategy_filter"
    p06_decision = p06 / "strategy_decision"
    p06_handoff = p06 / "handoff"
    p01 = run / "01_data_fact" / "normalized"
    p07_state = run / "07_execution_risk" / "state"
    token = "[REDACTED]"
    now = datetime.now(timezone.utc)

    strategy_decision = {
        "phase": "phase_06_strategy_gate_controller",
        "token_address": token,
        "token_symbol": "TST",
        "snapshot_id": "snap-p7-test",
        "snapshot_time": now.isoformat(),
        "input_status": "PHASE_06_INPUT_READY",
        "strategy_gate_status": strategy_status,
        "a_plus_structure_pass": a_plus_p1_status == "A_PLUS_P1_PASS",
        "p1_position_pass": a_plus_p1_status == "A_PLUS_P1_PASS",
        "a_plus_p1_pass": a_plus_p1_status == "A_PLUS_P1_PASS",
        "hard_negative_triggered": hard_negative,
        "hard_negative_reasons": ["upstream_hard_negative"] if hard_negative else [],
        "required_execution_checks": ["quote", "security", "liquidity", "slippage", "duplicate", "risk_limit"],
        "allowed_next_stage": "phase_07_execution_risk_controller" if strategy_status in {"PAPER_READY", "READY_FOR_CONFIRMATION"} else "blocked",
        "block_reason": "upstream_hard_negative" if hard_negative else "",
    }
    a_plus_p1 = {
        "phase": "phase_06_strategy_gate_controller",
        "result_status": a_plus_p1_status,
        "a_plus_p1_pass": a_plus_p1_status == "A_PLUS_P1_PASS",
        "hard_negative_triggered": hard_negative,
    }
    hard = {"hard_negative_triggered": hard_negative, "hard_negative_reasons": strategy_decision["hard_negative_reasons"]}
    rr = {"risk_reward_pass": True, "risk_reward_status": "RR_OK", "score": 85}
    quote_time = now - timedelta(seconds=quote_age_seconds)
    quote_security = {
        "token_address": token,
        "quote_valid": quote_valid,
        "quote_timestamp": quote_time.isoformat(),
        "quote_age_seconds": quote_age_seconds,
        "price_usd": 0.0012,
        "security_status": security_status,
        "security_risk_level": "LOW" if security_status in {"SECURITY_OK", "LOW_RISK"} else "HIGH",
        "honeypot_risk": security_status == "SECURITY_HIGH_RISK",
        "liquidity_usd": liquidity_usd,
        "estimated_price_impact_bps": 80,
        "slippage_bps_estimate": slippage_bps,
    }
    risk_config = {
        "allow_paper_trade": allow_paper_trade,
        "allow_real_execution": False,
        "max_quote_age_seconds": 90,
        "min_liquidity_usd": 30000,
        "max_slippage_bps": 300,
        "max_price_impact_bps": 250,
        "max_open_positions_per_token": 1,
        "max_daily_loss_pct": 5.0,
        "paper_position_size_usd": 100.0,
        "manual_confirmation_required_for": ["READY_FOR_CONFIRMATION"],
    }
    open_positions = []
    if open_position:
        open_positions.append({"token_address": token, "position_id": "paper-existing", "status": "OPEN", "paper_only": True})
    closed_positions = [{"token_address": "OTHER", "position_id": "paper-old", "status": "CLOSED", "pnl_pct": -1.0}]
    risk_events = [
        {"event_type": "daily_loss", "loss_pct": daily_loss_pct, "token_address": "OTHER", "timestamp": now.isoformat()}
    ] if daily_loss_pct else []

    _write_json(p06_decision / "strategy_gate_decision.json", strategy_decision)
    _write_json(p06_decision / "a_plus_p1_result.json", a_plus_p1)
    _write_json(p06_decision / "hard_negative_checklist.json", hard)
    _write_json(p06_decision / "risk_reward_check.json", rr)
    _write_json(p01 / "quote_security_normalized.json", quote_security)
    _write_json(p01 / "token_market_context.json", {"token_address": token, "token_symbol": "TST", "snapshot_id": "snap-p7-test"})
    _write_json(p07_state / "risk_config.json", risk_config)
    _write_json(p07_state / "paper_positions_open.json", open_positions)
    _write_json(p07_state / "paper_positions_closed.json", closed_positions)
    risk_events_path = p07_state / "risk_events.jsonl"
    risk_events_path.parent.mkdir(parents=True, exist_ok=True)
    risk_events_path.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in risk_events), encoding="utf-8")

    required = {
        "phase_06_handoff_packet": str(p06_handoff / "phase_06_handoff_packet.json"),
        "strategy_gate_decision": str(p06_decision / "strategy_gate_decision.json"),
        "hard_negative_checklist": str(p06_decision / "hard_negative_checklist.json"),
        "a_plus_p1_result": str(p06_decision / "a_plus_p1_result.json"),
        "risk_reward_check": str(p06_decision / "risk_reward_check.json"),
        "quote_security_normalized": str(p01 / "quote_security_normalized.json"),
        "token_market_context": str(p01 / "token_market_context.json"),
        "risk_config": str(p07_state / "risk_config.json"),
        "paper_positions_open": str(p07_state / "paper_positions_open.json"),
        "paper_positions_closed": str(p07_state / "paper_positions_closed.json"),
        "risk_events": str(risk_events_path),
    }
    handoff = {
        "phase": "phase_06_strategy_gate_controller",
        "token_address": token,
        "token_symbol": "TST",
        "snapshot_id": "snap-p7-test",
        "snapshot_time": now.isoformat(),
        "phase_status": strategy_status,
        "allow_next_stage": strategy_status in {"PAPER_READY", "READY_FOR_CONFIRMATION"} and not hard_negative,
        "next_stage": "phase_07_execution_risk_controller",
        "required_files_for_next_stage": required,
        "hard_negative_triggered": hard_negative,
        "hard_negative_reasons": strategy_decision["hard_negative_reasons"],
        "block_reason": "upstream_hard_negative" if hard_negative else "",
        "missing_fields": [],
    }
    _write_json(p06_handoff / "phase_06_handoff_packet.json", handoff)
    return p06_handoff / "phase_06_handoff_packet.json"


def _load(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def test_phase07_paper_ready_executes_paper_only_and_writes_handoff(tmp_path: Path):
    handoff = _phase07_package(tmp_path)
    result = Phase07ExecutionRiskController().run(phase06_handoff_file=handoff, output_dir=tmp_path / "out")
    assert result["phase"] == "phase_07_execution_risk_controller"
    artifacts = result["artifacts"]
    required = [
        "strategy_execution_context",
        "signal_freshness_check",
        "quote_check_result",
        "security_check_result",
        "liquidity_check_result",
        "slippage_check_result",
        "duplicate_entry_check",
        "risk_limit_check_result",
        "execution_risk_decision",
        "paper_trade_decision",
        "paper_positions_open",
        "paper_trades",
        "risk_events",
        "handoff_packet",
        "audit_report",
    ]
    for key in required:
        assert key in artifacts
        assert Path(artifacts[key]).exists(), key
    decision = _load(artifacts["execution_risk_decision"])
    assert decision["execution_risk_status"] == "EXECUTION_ALLOWED"
    assert decision["paper_trade_status"] == "PAPER_EXECUTED"
    assert decision["real_execution_allowed"] is False
    assert "REAL_ORDER_EXECUTED" not in json.dumps(decision, ensure_ascii=False)
    paper = _load(artifacts["paper_trade_decision"])
    assert paper["paper_only"] is True
    assert paper["paper_trade_status"] == "PAPER_EXECUTED"
    positions = json.loads(Path(artifacts["paper_positions_open"]).read_text(encoding="utf-8"))
    assert len(positions) == 1
    assert positions[0]["paper_only"] is True
    handoff_out = _load(artifacts["handoff_packet"])
    assert handoff_out["phase"] == "phase_07_execution_risk_controller"
    assert handoff_out["next_stage"] == "phase_08_review_learning_controller"
    assert handoff_out["required_files_for_next_stage"]["execution_risk_decision"] == artifacts["execution_risk_decision"]


def test_phase07_upstream_strategy_block_prevents_execution(tmp_path: Path):
    handoff = _phase07_package(tmp_path, strategy_status="STRATEGY_BLOCK", hard_negative=True)
    result = Phase07ExecutionRiskController().run(phase06_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = _load(result["artifacts"]["execution_risk_decision"])
    assert decision["input_status"] == "PHASE_07_INPUT_BLOCKED"
    assert decision["execution_risk_status"] == "EXECUTION_BLOCK"
    assert decision["paper_trade_status"] == "PAPER_SKIPPED"
    assert decision["real_execution_allowed"] is False


def test_phase07_quote_stale_or_invalid_blocks_with_risk_event(tmp_path: Path):
    handoff = _phase07_package(tmp_path, quote_valid=False, quote_age_seconds=600)
    result = Phase07ExecutionRiskController().run(phase06_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = _load(result["artifacts"]["execution_risk_decision"])
    quote = _load(result["artifacts"]["quote_check_result"])
    assert quote["quote_status"] == "QUOTE_INVALID"
    assert decision["execution_risk_status"] == "EXECUTION_BLOCK"
    assert decision["paper_trade_status"] == "PAPER_SKIPPED"
    events = Path(result["artifacts"]["risk_events"]).read_text(encoding="utf-8")
    assert "QUOTE_INVALID" in events


def test_phase07_security_high_risk_hard_blocks(tmp_path: Path):
    handoff = _phase07_package(tmp_path, security_status="SECURITY_HIGH_RISK")
    result = Phase07ExecutionRiskController().run(phase06_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = _load(result["artifacts"]["execution_risk_decision"])
    sec = _load(result["artifacts"]["security_check_result"])
    assert sec["security_status"] == "SECURITY_HIGH_RISK"
    assert decision["execution_risk_status"] == "SECURITY_HIGH_RISK"
    assert decision["paper_trade_status"] == "PAPER_SKIPPED"


def test_phase07_liquidity_slippage_duplicate_and_risk_limit_block(tmp_path: Path):
    handoff = _phase07_package(tmp_path, liquidity_usd=1000, slippage_bps=900, open_position=True, daily_loss_pct=9.5)
    result = Phase07ExecutionRiskController().run(phase06_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = _load(result["artifacts"]["execution_risk_decision"])
    assert decision["paper_trade_status"] == "PAPER_SKIPPED"
    assert set(decision["hard_negative_reasons"]) >= {"LIQUIDITY_WEAK", "SLIPPAGE_TOO_HIGH", "DUPLICATE_POSITION_BLOCK", "RISK_LIMIT_BLOCK"}
    assert _load(result["artifacts"]["liquidity_check_result"])["liquidity_status"] == "LIQUIDITY_WEAK"
    assert _load(result["artifacts"]["slippage_check_result"])["slippage_status"] == "SLIPPAGE_TOO_HIGH"
    assert _load(result["artifacts"]["duplicate_entry_check"])["duplicate_status"] == "DUPLICATE_POSITION_BLOCK"
    assert _load(result["artifacts"]["risk_limit_check_result"])["risk_limit_status"] == "RISK_LIMIT_BLOCK"


def test_phase07_ready_for_confirmation_generates_manual_ticket_without_paper_execution(tmp_path: Path):
    handoff = _phase07_package(tmp_path, strategy_status="READY_FOR_CONFIRMATION")
    result = Phase07ExecutionRiskController().run(phase06_handoff_file=handoff, output_dir=tmp_path / "out")
    decision = _load(result["artifacts"]["execution_risk_decision"])
    assert decision["execution_risk_status"] == "READY_FOR_CONFIRMATION"
    assert decision["paper_trade_status"] == "PAPER_SKIPPED"
    assert "manual_confirmation_ticket" in result["artifacts"]
    assert "confirmation_ticket" in result["artifacts"]
    ticket = _load(result["artifacts"]["manual_confirmation_ticket"])
    assert ticket["ticket_status"] == "READY_FOR_CONFIRMATION"
    assert ticket["real_execution_allowed"] is False


def test_phase07_static_contract_schema_controller_files_exist():
    root = Path("/root/sikk-gmgn")
    required = [
        root / "research_loop/phase_07_execution_risk_layer/README.md",
        root / "contracts/stable_trader_os/phase_07_execution_risk/phase_07_input_contract.json",
        root / "contracts/stable_trader_os/phase_07_execution_risk/phase_07_output_contract.json",
        root / "contracts/stable_trader_os/phase_07_execution_risk/required_fields.md",
        root / "contracts/stable_trader_os/phase_07_execution_risk/handoff_rules.md",
        root / "schemas/stable_trader_os/phase_07_execution_risk/execution_risk_decision.schema.json",
        root / "schemas/stable_trader_os/phase_07_execution_risk/phase_07_handoff_packet.schema.json",
        root / "configs/stable_trader_os/phase_07_execution_risk/phase_07_status_codes.json",
        root / "modules/stable_trader_os/phase_07_execution_risk_controller/runner.py",
        root / "skills/sikk_stable_trader_os/phase_controllers/phase_07_execution_risk_controller.md",
    ]
    missing = [str(p) for p in required if not p.exists() or p.stat().st_size == 0]
    assert not missing
