from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from modules.stable_trader_os.phase_08_review_learning_controller import Phase08ReviewLearningController


def _write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


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


def _load(path: str | Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _read_jsonl(path: str | Path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def _read_csv(path: str | Path) -> list[dict]:
    return list(csv.DictReader(Path(path).open(encoding="utf-8")))


def _phase08_package(
    tmp_path: Path,
    *,
    phase07_status: str = "PAPER_EXECUTED",
    execution_status: str = "EXECUTION_ALLOWED",
    paper_status: str = "PAPER_EXECUTED",
    pnl_pct: float | None = 18.5,
    include_prior_trace: bool = True,
    include_trades: bool = True,
    risk_event_types: list[str] | None = None,
    manual_confirmation: bool = False,
) -> Path:
    run = tmp_path / "run"
    token = "[REDACTED]"
    now = datetime.now(timezone.utc).isoformat()

    p01 = run / "01_data_fact" / "normalized"
    p02 = run / "02_wallet_structure" / "wallet_decision"
    p03 = run / "03_chip_control" / "chip_decision"
    p04 = run / "04_scenario_recognition" / "scenario_decision"
    p05 = run / "05_structure_position" / "position_decision"
    p06 = run / "06_strategy_filter" / "strategy_decision"
    p07_decision = run / "07_execution_risk" / "execution_decision"
    p07_state = run / "07_execution_risk" / "state"
    p07_handoff = run / "07_execution_risk" / "handoff"

    data_quality = {
        "phase": "phase_01_data_fact_controller",
        "token_address": token,
        "data_quality_status": "DATA_OK",
        "positive_evidence": ["gmgn_snapshot_complete"],
        "negative_evidence": [],
        "missing_fields": [],
        "evidence_level": "E4",
        "risk_level": "LOW",
    }
    wallet = {
        "phase": "phase_02_wallet_structure_controller",
        "token_address": token,
        "wallet_structure_status": "WALLET_SUPPORT",
        "candidate_roles": ["疑似同源执行组", "疑似结构钱包"],
        "positive_evidence": ["early_wallet_cluster", "same_source_group_detected"],
        "negative_evidence": [],
        "counter_evidence": [],
        "evidence_level": "E4",
        "risk_level": "MEDIUM",
    }
    chip = {
        "phase": "phase_03_chip_control_controller",
        "token_address": token,
        "chip_control_status": "CONTROL_RETAINED",
        "positive_evidence": ["early_wallet_retention_high"],
        "negative_evidence": [],
        "counter_evidence": [],
        "evidence_level": "E4",
        "risk_level": "LOW",
    }
    scenario = {
        "phase": "phase_04_scenario_recognition_controller",
        "token_address": token,
        "primary_scenario": "SCENARIO_SECOND_STAGE_CANDIDATE",
        "scenario_status": "SCENARIO_ALLOW",
        "positive_evidence": ["volume_push_with_retention"],
        "negative_evidence": [],
        "counter_evidence": [],
        "evidence_level": "E4",
        "risk_level": "MEDIUM",
    }
    position = {
        "phase": "phase_05_structure_position_controller",
        "token_address": token,
        "position_status": "COMPLETION_PASS",
        "position_quality": "P1",
        "positive_evidence": ["avwap_reclaim", "failure_test_pass"],
        "negative_evidence": [],
        "counter_evidence": [],
        "evidence_level": "E4",
        "risk_level": "LOW",
    }
    strategy = {
        "phase": "phase_06_strategy_gate_controller",
        "token_address": token,
        "strategy_gate_status": "PAPER_READY",
        "a_plus_p1_pass": True,
        "positive_evidence": ["A+ structure", "P1 position"],
        "negative_evidence": [],
        "counter_evidence": [],
        "hard_negative_triggered": False,
        "evidence_level": "E4",
        "risk_level": "LOW",
    }
    execution = {
        "phase": "phase_07_execution_risk_controller",
        "token_address": token,
        "snapshot_id": "snap-p8-test",
        "input_status": "PHASE_07_INPUT_READY",
        "execution_risk_status": execution_status,
        "paper_trade_status": paper_status,
        "real_execution_allowed": False,
        "hard_negative_triggered": execution_status in {"EXECUTION_BLOCK", "SECURITY_HIGH_RISK"},
        "hard_negative_reasons": risk_event_types or [],
        "positive_evidence": ["QUOTE_OK", "SECURITY_OK"] if execution_status == "EXECUTION_ALLOWED" else [],
        "negative_evidence": risk_event_types or [],
        "counter_evidence": risk_event_types or [],
        "missing_fields": [],
        "risk_level": "HIGH" if execution_status != "EXECUTION_ALLOWED" else "LOW",
        "evidence_level": "E3",
    }
    paper_decision = {
        "phase": "phase_07_execution_risk_controller",
        "token_address": token,
        "paper_only": True,
        "paper_trade_status": paper_status,
        "real_execution_allowed": False,
        "reason": execution_status,
        "position_id": "paper-p8-1" if paper_status == "PAPER_EXECUTED" else "",
    }
    open_positions = []
    closed_positions = []
    if pnl_pct is None and paper_status == "PAPER_EXECUTED":
        open_positions.append({"position_id": "paper-p8-1", "token_address": token, "status": "OPEN", "paper_only": True, "entry_price_usd": 0.001, "size_usd": 100})
    elif pnl_pct is not None:
        closed_positions.append({"position_id": "paper-p8-1", "token_address": token, "status": "CLOSED", "paper_only": True, "entry_price_usd": 0.001, "exit_price_usd": 0.001 * (1 + pnl_pct / 100), "size_usd": 100, "pnl_pct": pnl_pct, "pnl_usd": pnl_pct})
    trade_rows = [{"trade_id": "paper-p8-1", "token_address": token, "side": "PAPER_BUY", "price_usd": 0.001, "size_usd": 100, "paper_only": True, "timestamp": now}] if include_trades and paper_status == "PAPER_EXECUTED" else []
    equity_rows = [{"timestamp": now, "equity_usd": 1000 + (pnl_pct or 0), "token_address": token}] if pnl_pct is not None else []
    events = [{"timestamp": now, "token_address": token, "event_type": event, "phase": "phase_07_execution_risk_controller"} for event in (risk_event_types or [])]

    if include_prior_trace:
        _write_json(p01 / "data_quality_summary.json", data_quality)
        _write_json(p02 / "wallet_structure_decision.json", wallet)
        _write_json(p03 / "chip_control_summary.json", chip)
        _write_json(p04 / "primary_scenario.json", scenario)
        _write_json(p05 / "structure_position_decision.json", position)
        _write_json(p06 / "strategy_gate_decision.json", strategy)
    else:
        _write_json(p06 / "strategy_gate_decision.json", strategy)

    _write_json(p07_decision / "execution_risk_decision.json", execution)
    _write_json(p07_decision / "paper_trade_decision.json", paper_decision)
    if manual_confirmation:
        _write_json(p07_decision / "manual_confirmation_ticket.json", {"ticket_status": "READY_FOR_CONFIRMATION", "token_address": token, "real_execution_allowed": False})
    _write_json(p07_state / "paper_positions_open.json", open_positions)
    _write_json(p07_state / "paper_positions_closed.json", closed_positions)
    _write_csv(p07_state / "paper_trades.csv", trade_rows)
    _write_csv(p07_state / "paper_equity_curve.csv", equity_rows)
    _write_jsonl(p07_state / "risk_events.jsonl", events)

    required = {
        "phase_07_handoff_packet": str(p07_handoff / "phase_07_handoff_packet.json"),
        "execution_risk_decision": str(p07_decision / "execution_risk_decision.json"),
        "paper_trade_decision": str(p07_decision / "paper_trade_decision.json"),
        "paper_positions_open": str(p07_state / "paper_positions_open.json"),
        "paper_positions_closed": str(p07_state / "paper_positions_closed.json"),
        "paper_trades": str(p07_state / "paper_trades.csv"),
        "paper_equity_curve": str(p07_state / "paper_equity_curve.csv"),
        "risk_events": str(p07_state / "risk_events.jsonl"),
        "strategy_gate_decision": str(p06 / "strategy_gate_decision.json"),
        "structure_position_decision": str(p05 / "structure_position_decision.json"),
        "primary_scenario": str(p04 / "primary_scenario.json"),
        "chip_control_summary": str(p03 / "chip_control_summary.json"),
        "wallet_structure_decision": str(p02 / "wallet_structure_decision.json"),
        "data_quality_summary": str(p01 / "data_quality_summary.json"),
    }
    if manual_confirmation:
        required["manual_confirmation_ticket"] = str(p07_decision / "manual_confirmation_ticket.json")
    handoff = {
        "phase": "phase_07_execution_risk_controller",
        "token_address": token,
        "snapshot_id": "snap-p8-test",
        "phase_status": phase07_status,
        "allow_next_stage": True,
        "next_stage": "phase_08_review_learning_controller",
        "required_files_for_next_stage": required,
        "positive_evidence": execution["positive_evidence"],
        "negative_evidence": execution["negative_evidence"],
        "hard_negative_triggered": execution["hard_negative_triggered"],
        "hard_negative_reasons": execution["hard_negative_reasons"],
        "block_reason": ";".join(execution["hard_negative_reasons"]),
        "degrade_reason": "",
        "missing_fields": [],
        "audit_file": str(run / "07_execution_risk" / "audit" / "audit_report.md"),
    }
    _write_json(p07_handoff / "phase_07_handoff_packet.json", handoff)
    return p07_handoff / "phase_07_handoff_packet.json"


def test_phase08_successful_closed_paper_trade_generates_review_learning_outputs(tmp_path: Path):
    handoff = _phase08_package(tmp_path, pnl_pct=18.5)
    result = Phase08ReviewLearningController().run(phase07_handoff_file=handoff, output_dir=tmp_path / "out")
    assert result["phase"] == "phase_08_review_learning_controller"
    assert result["status"] == "REVIEW_COMPLETE"
    artifacts = result["artifacts"]
    required = [
        "paper_trade_result_snapshot",
        "paper_position_result_table",
        "review_fact_validation",
        "phase_decision_trace_json",
        "phase_decision_trace_md",
        "evidence_chain_manifest",
        "failure_attribution",
        "success_attribution",
        "address_history_update",
        "scenario_case_library",
        "strategy_performance_summary",
        "rule_update_candidates",
        "threshold_review_candidates",
        "model_recalibration_candidates",
        "review_learning_summary",
        "daily_review_report",
        "handoff_packet",
        "audit_report",
        "output_validation_report",
        "handoff_validation_report",
        "missing_fields_report",
        "gaps",
    ]
    for key in required:
        assert key in artifacts
        assert Path(artifacts[key]).exists(), key
    summary = _load(artifacts["review_learning_summary"])
    assert summary["input_status"] == "PHASE_08_INPUT_READY"
    assert summary["review_status"] == "REVIEW_COMPLETE"
    assert summary["direct_rule_change_allowed"] is False
    review_fact = _load(artifacts["review_fact_validation"])
    assert review_fact["review_fact_status"] == "REVIEW_FACT_COMPLETE"
    assert review_fact["fact_sources"]["execution_risk_decision"] is True
    assert review_fact["fact_sources"]["paper_trade_decision"] is True
    evidence_manifest = _load(artifacts["evidence_chain_manifest"])
    assert evidence_manifest["evidence_chain_status"] == "EVIDENCE_CHAIN_COMPLETE"
    assert evidence_manifest["present_phase_count"] == evidence_manifest["required_phase_count"]
    assert any(link["source_key"] == "execution_risk_decision" for link in evidence_manifest["links"])
    successes = _read_jsonl(artifacts["success_attribution"])
    assert successes
    assert successes[0]["source_phase"] in {"phase_06_strategy_gate_controller", "phase_05_structure_position_controller", "phase_04_scenario_recognition_controller"}
    assert successes[0]["evidence_refs"]
    failures = _read_jsonl(artifacts["failure_attribution"])
    assert failures == []
    handoff_out = _load(artifacts["handoff_packet"])
    assert handoff_out["next_stage"] == "phase_09_system_upgrade_controller"
    for required_key in ["paper_trade_result_snapshot", "review_fact_validation", "phase_decision_trace_json", "evidence_chain_manifest", "review_learning_summary", "failure_attribution", "success_attribution", "rule_update_candidates", "threshold_review_candidates", "scenario_case_library", "address_history_update", "strategy_performance_summary"]:
        assert Path(handoff_out["required_files_for_next_stage"][required_key]).exists()
    handoff_validation = _load(artifacts["handoff_validation_report"])
    assert handoff_validation["status"] == "PASS"
    assert handoff_validation["missing_required_handoff_keys"] == []
    assert handoff_out["evidence_chain_status"] == "EVIDENCE_CHAIN_COMPLETE"
    assert handoff_out["review_fact_status"] == "REVIEW_FACT_COMPLETE"


def test_phase08_failed_paper_trade_attributes_to_specific_phase_and_rule_candidates_have_cases(tmp_path: Path):
    handoff = _phase08_package(tmp_path, pnl_pct=-12.0)
    result = Phase08ReviewLearningController().run(phase07_handoff_file=handoff, output_dir=tmp_path / "out")
    failures = _read_jsonl(result["artifacts"]["failure_attribution"])
    assert failures
    assert all(f["source_phase"] != "unknown" for f in failures)
    assert all(f["evidence_refs"] for f in failures)
    assert not any("行情不好" in json.dumps(f, ensure_ascii=False) or "运气不好" in json.dumps(f, ensure_ascii=False) for f in failures)
    candidates = _load(result["artifacts"]["rule_update_candidates"])
    assert candidates["direct_rule_change_allowed"] is False
    assert candidates["candidates"]
    assert all(c["evidence_cases"] for c in candidates["candidates"])
    thresholds = _load(result["artifacts"]["threshold_review_candidates"])
    assert thresholds["candidates"]
    assert thresholds["phase09_only"] is True


def test_phase08_execution_block_risk_events_create_block_review_without_changing_strategy(tmp_path: Path):
    handoff = _phase08_package(
        tmp_path,
        phase07_status="EXECUTION_BLOCK",
        execution_status="EXECUTION_BLOCK",
        paper_status="PAPER_SKIPPED",
        pnl_pct=None,
        risk_event_types=["LIQUIDITY_WEAK", "SLIPPAGE_TOO_HIGH", "DUPLICATE_POSITION_BLOCK"],
    )
    result = Phase08ReviewLearningController().run(phase07_handoff_file=handoff, output_dir=tmp_path / "out")
    summary = _load(result["artifacts"]["review_learning_summary"])
    assert summary["review_status"] == "REVIEW_COMPLETE"
    assert summary["blocked_sample_count"] == 1
    failures = _read_jsonl(result["artifacts"]["failure_attribution"])
    assert {f["source_phase"] for f in failures} == {"phase_07_execution_risk_controller"}
    assert {f["failure_type"] for f in failures} >= {"LIQUIDITY_WEAK", "SLIPPAGE_TOO_HIGH", "DUPLICATE_POSITION_BLOCK"}
    rule_candidates = _load(result["artifacts"]["rule_update_candidates"])
    assert rule_candidates["direct_rule_change_allowed"] is False
    assert all(c["target_phase"] == "phase_07_execution_risk_controller" for c in rule_candidates["candidates"])


def test_phase08_ready_for_confirmation_enters_review_queue(tmp_path: Path):
    handoff = _phase08_package(
        tmp_path,
        phase07_status="READY_FOR_CONFIRMATION",
        execution_status="READY_FOR_CONFIRMATION",
        paper_status="PAPER_SKIPPED",
        pnl_pct=None,
        manual_confirmation=True,
    )
    result = Phase08ReviewLearningController().run(phase07_handoff_file=handoff, output_dir=tmp_path / "out")
    summary = _load(result["artifacts"]["review_learning_summary"])
    assert summary["manual_review_queue_count"] == 1
    assert summary["review_status"] == "REVIEW_INCOMPLETE"
    trace = _load(result["artifacts"]["phase_decision_trace_json"])
    assert trace["manual_confirmation_ticket"]["ticket_status"] == "READY_FOR_CONFIRMATION"


def test_phase08_missing_prior_evidence_chain_degrades_not_fabricates_conclusions(tmp_path: Path):
    handoff = _phase08_package(tmp_path, include_prior_trace=False, pnl_pct=-6.0)
    result = Phase08ReviewLearningController().run(phase07_handoff_file=handoff, output_dir=tmp_path / "out")
    summary = _load(result["artifacts"]["review_learning_summary"])
    assert summary["input_status"] == "PHASE_08_INPUT_DEGRADED"
    assert summary["review_status"] == "REVIEW_INCOMPLETE"
    assert summary["missing_fields"]
    failures = _read_jsonl(result["artifacts"]["failure_attribution"])
    assert failures
    assert any(f["source_phase"] == "phase_08_review_learning_controller" and f["failure_type"] == "EVIDENCE_CHAIN_DEGRADED" for f in failures)
    assert not any(f.get("absolute_conclusion") for f in failures)
    evidence_manifest = _load(result["artifacts"]["evidence_chain_manifest"])
    assert evidence_manifest["evidence_chain_status"] == "EVIDENCE_CHAIN_DEGRADED"
    assert evidence_manifest["missing_evidence_chain"]
    review_fact = _load(result["artifacts"]["review_fact_validation"])
    assert review_fact["review_fact_status"] in {"REVIEW_FACT_COMPLETE", "REVIEW_FACT_DEGRADED"}
    missing_report = Path(result["artifacts"]["missing_fields_report"]).read_text(encoding="utf-8")
    assert "data_quality_summary" in missing_report


def test_phase08_address_history_update_is_patch_mode_and_scenario_library_is_structured(tmp_path: Path):
    handoff = _phase08_package(tmp_path, pnl_pct=-9.0)
    result = Phase08ReviewLearningController().run(phase07_handoff_file=handoff, output_dir=tmp_path / "out")
    address_updates = _read_csv(result["artifacts"]["address_history_update"])
    assert address_updates
    assert all(row["update_mode"] == "patch" for row in address_updates)
    assert all(row["direct_overwrite_allowed"] == "false" for row in address_updates)
    cases = _load(result["artifacts"]["scenario_case_library"])
    assert cases["cases"]
    assert all(case["token_address"] == "[REDACTED]" for case in cases["cases"])
    assert all(case["source_phase_trace"] for case in cases["cases"])


def test_phase08_blocks_when_phase07_handoff_missing(tmp_path: Path):
    missing_handoff = tmp_path / "missing" / "phase_07_handoff_packet.json"
    result = Phase08ReviewLearningController().run(phase07_handoff_file=missing_handoff, output_dir=tmp_path / "out")
    summary = _load(result["artifacts"]["review_learning_summary"])
    assert summary["input_status"] == "PHASE_08_INPUT_BLOCKED"
    assert summary["review_status"] == "REVIEW_INCOMPLETE"
    assert "phase_07_handoff_packet_missing" in summary["block_reasons"]
    handoff = _load(result["artifacts"]["handoff_packet"])
    assert handoff["allow_next_stage"] is False
    assert handoff["next_stage"] == "phase_09_system_upgrade_controller"


def test_phase08_static_contract_schema_controller_files_exist():
    root = Path("/root/sikk-gmgn")
    required = [
        root / "research_loop/phase_08_review_learning_layer/README.md",
        root / "contracts/stable_trader_os/phase_08_review_learning/phase_08_input_contract.json",
        root / "contracts/stable_trader_os/phase_08_review_learning/phase_08_output_contract.json",
        root / "contracts/stable_trader_os/phase_08_review_learning/required_fields.md",
        root / "contracts/stable_trader_os/phase_08_review_learning/handoff_rules.md",
        root / "schemas/stable_trader_os/phase_08_review_learning/review_learning_summary.schema.json",
        root / "schemas/stable_trader_os/phase_08_review_learning/phase_08_handoff_packet.schema.json",
        root / "configs/stable_trader_os/phase_08_review_learning/phase_08_status_codes.json",
        root / "modules/stable_trader_os/phase_08_review_learning_controller/runner.py",
        root / "skills/sikk_stable_trader_os/phase_controllers/phase_08_review_learning_controller.md",
    ]
    missing = [str(p) for p in required if not p.exists() or p.stat().st_size == 0]
    assert not missing
