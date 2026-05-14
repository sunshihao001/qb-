from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

PHASE = "phase_08_review_learning_controller"
NEXT_PHASE = "phase_09_system_upgrade_controller"
EVIDENCE_CHAIN_KEYS = [
    "data_quality_summary",
    "wallet_structure_decision",
    "chip_control_summary",
    "primary_scenario",
    "structure_position_decision",
    "strategy_gate_decision",
    "execution_risk_decision",
]
EXECUTION_BLOCK_STATUSES = {"EXECUTION_BLOCK", "SECURITY_HIGH_RISK", "QUOTE_INVALID", "LIQUIDITY_WEAK", "SLIPPAGE_TOO_HIGH", "DUPLICATE_POSITION_BLOCK", "RISK_LIMIT_BLOCK"}


@dataclass
class ArtifactPaths:
    base: Path

    @property
    def review_fact(self) -> Path: return self.base / "review_fact"
    @property
    def review_trace(self) -> Path: return self.base / "review_trace"
    @property
    def attribution(self) -> Path: return self.base / "attribution"
    @property
    def learning(self) -> Path: return self.base / "learning"
    @property
    def handoff(self) -> Path: return self.base / "handoff"
    @property
    def audit(self) -> Path: return self.base / "audit"


class Phase08ReviewLearningController:
    """Phase08 复盘学习控制器：只生成可审计回灌建议，不直接改规则。"""

    def run(self, *, phase07_handoff_file: str | Path, output_dir: str | Path) -> Dict[str, Any]:
        output = Path(output_dir)
        paths = ArtifactPaths(output)
        for d in [paths.review_fact, paths.review_trace, paths.attribution, paths.learning, paths.handoff, paths.audit]:
            d.mkdir(parents=True, exist_ok=True)

        handoff_path = Path(phase07_handoff_file)
        phase07_handoff = self._read_json(handoff_path, default={}) if handoff_path.exists() else {}
        required_files = phase07_handoff.get("required_files_for_next_stage", {}) if isinstance(phase07_handoff, dict) else {}
        loaded, missing_files = self._load_required(required_files)

        if not handoff_path.exists():
            missing_files.append("phase_07_handoff_packet")
        execution = loaded.get("execution_risk_decision", {}) if isinstance(loaded.get("execution_risk_decision"), dict) else {}
        paper = loaded.get("paper_trade_decision", {}) if isinstance(loaded.get("paper_trade_decision"), dict) else {}
        open_positions = loaded.get("paper_positions_open", []) if isinstance(loaded.get("paper_positions_open"), list) else []
        closed_positions = loaded.get("paper_positions_closed", []) if isinstance(loaded.get("paper_positions_closed"), list) else []
        paper_trades = loaded.get("paper_trades", []) if isinstance(loaded.get("paper_trades"), list) else []
        equity_curve = loaded.get("paper_equity_curve", []) if isinstance(loaded.get("paper_equity_curve"), list) else []
        risk_events = loaded.get("risk_events", []) if isinstance(loaded.get("risk_events"), list) else []
        manual_ticket = loaded.get("manual_confirmation_ticket", {}) if isinstance(loaded.get("manual_confirmation_ticket"), dict) else {}

        token = phase07_handoff.get("token_address") or execution.get("token_address") or paper.get("token_address") or self._first_token(closed_positions + open_positions + paper_trades + risk_events) or "missing"
        snapshot_id = phase07_handoff.get("snapshot_id") or execution.get("snapshot_id") or "missing"
        block_reasons: List[str] = []
        if not handoff_path.exists(): block_reasons.append("phase_07_handoff_packet_missing")
        if token == "missing": block_reasons.append("token_address_missing")
        if not execution and not paper and not paper_trades and not risk_events: block_reasons.append("review_fact_missing")

        missing_fields = self._dedupe(missing_files)
        evidence_missing = [k for k in EVIDENCE_CHAIN_KEYS if k not in loaded]
        critical_missing = [k for k in ["execution_risk_decision", "paper_trade_decision"] if k not in loaded]
        no_trade_and_no_events = "paper_trades" in missing_fields and not risk_events
        if no_trade_and_no_events:
            critical_missing.append("paper_trades_or_risk_events")
        if all(k not in loaded for k in EVIDENCE_CHAIN_KEYS):
            block_reasons.append("prior_evidence_chain_all_missing")
        elif evidence_missing:
            # 证据链缺失降级，不伪造上游判断
            pass

        if block_reasons:
            input_status = "PHASE_08_INPUT_BLOCKED"
        elif evidence_missing or critical_missing:
            input_status = "PHASE_08_INPUT_DEGRADED"
        else:
            input_status = "PHASE_08_INPUT_READY"

        trace = self._build_trace(token, snapshot_id, loaded, phase07_handoff, execution, paper, manual_ticket, evidence_missing)
        evidence_chain_manifest = self._evidence_chain_manifest(token, snapshot_id, phase07_handoff, loaded, trace, evidence_missing, missing_fields)
        snapshot = {
            "phase": PHASE,
            "token_address": token,
            "snapshot_id": snapshot_id,
            "input_status": input_status,
            "phase07_status": phase07_handoff.get("phase_status", execution.get("execution_risk_status", "missing")),
            "execution_risk_status": execution.get("execution_risk_status", "missing"),
            "paper_trade_status": paper.get("paper_trade_status", execution.get("paper_trade_status", "missing")),
            "open_position_count": len(open_positions),
            "closed_position_count": len(closed_positions),
            "paper_trade_count": len(paper_trades),
            "risk_event_count": len(risk_events),
            "manual_confirmation_ticket_present": bool(manual_ticket),
            "direct_rule_change_allowed": False,
        }
        position_rows = self._position_rows(token, open_positions, closed_positions, paper_trades)
        review_fact_validation = self._review_fact_validation(
            token,
            snapshot_id,
            execution,
            paper,
            open_positions,
            closed_positions,
            paper_trades,
            equity_curve,
            risk_events,
            evidence_chain_manifest,
            input_status,
            block_reasons,
        )

        failures, successes = self._attribute(token, input_status, execution, paper, open_positions, closed_positions, paper_trades, risk_events, loaded, evidence_missing, block_reasons)
        blocked_sample_count = 1 if (execution.get("execution_risk_status") in EXECUTION_BLOCK_STATUSES or risk_events) and paper.get("paper_trade_status") != "PAPER_EXECUTED" else 0
        manual_review_queue_count = 1 if execution.get("execution_risk_status") == "READY_FOR_CONFIRMATION" or manual_ticket else 0
        review_complete = input_status == "PHASE_08_INPUT_READY" and manual_review_queue_count == 0 and not block_reasons
        review_status = "REVIEW_COMPLETE" if review_complete else "REVIEW_INCOMPLETE"

        address_updates = self._address_history_updates(token, failures, successes, loaded)
        scenario_library = self._scenario_case_library(token, trace, failures, successes, loaded)
        performance = self._strategy_performance(token, closed_positions, open_positions, paper_trades, risk_events, failures, successes)
        rule_candidates = self._rule_candidates(failures, successes)
        threshold_candidates = self._threshold_candidates(failures, risk_events)
        model_candidates = self._model_candidates(failures, successes, trace)
        summary = {
            "phase": PHASE,
            "token_address": token,
            "snapshot_id": snapshot_id,
            "input_status": input_status,
            "review_status": review_status,
            "failure_count": len(failures),
            "success_count": len(successes),
            "blocked_sample_count": blocked_sample_count,
            "manual_review_queue_count": manual_review_queue_count,
            "rule_update_candidate_count": len(rule_candidates["candidates"]),
            "threshold_review_candidate_count": len(threshold_candidates["candidates"]),
            "model_recalibration_candidate_count": len(model_candidates["candidates"]),
            "direct_rule_change_allowed": False,
            "missing_fields": missing_fields + [f"evidence_chain:{k}" for k in evidence_missing],
            "block_reasons": block_reasons,
            "allowed_next_stage": NEXT_PHASE,
        }

        artifacts: Dict[str, str] = {}
        artifacts["paper_trade_result_snapshot"] = str(self._write_json(paths.review_fact / "paper_trade_result_snapshot.json", snapshot))
        artifacts["paper_position_result_table"] = str(self._write_csv(paths.review_fact / "paper_position_result_table.csv", position_rows))
        artifacts["review_fact_validation"] = str(self._write_json(paths.review_fact / "review_fact_validation.json", review_fact_validation))
        artifacts["phase_decision_trace_json"] = str(self._write_json(paths.review_trace / "phase_decision_trace.json", trace))
        artifacts["phase_decision_trace_md"] = str(self._write_text(paths.review_trace / "phase_decision_trace.md", self._trace_md(trace)))
        artifacts["evidence_chain_manifest"] = str(self._write_json(paths.review_trace / "evidence_chain_manifest.json", evidence_chain_manifest))
        artifacts["failure_attribution"] = str(self._write_jsonl(paths.attribution / "failure_attribution.jsonl", failures))
        artifacts["success_attribution"] = str(self._write_jsonl(paths.attribution / "success_attribution.jsonl", successes))
        artifacts["address_history_update"] = str(self._write_csv(paths.learning / "address_history_update.csv", address_updates))
        artifacts["scenario_case_library"] = str(self._write_json(paths.learning / "scenario_case_library.json", scenario_library))
        artifacts["strategy_performance_summary"] = str(self._write_json(paths.learning / "strategy_performance_summary.json", performance))
        artifacts["rule_update_candidates"] = str(self._write_json(paths.learning / "rule_update_candidates.json", rule_candidates))
        artifacts["threshold_review_candidates"] = str(self._write_json(paths.learning / "threshold_review_candidates.json", threshold_candidates))
        artifacts["model_recalibration_candidates"] = str(self._write_json(paths.learning / "model_recalibration_candidates.json", model_candidates))
        artifacts["review_learning_summary"] = str(self._write_json(paths.learning / "review_learning_summary.json", summary))
        artifacts["daily_review_report"] = str(self._write_text(paths.learning / "daily_review_report.md", self._daily_report(summary, failures, successes)))

        handoff = {
            "phase": PHASE,
            "token_address": token,
            "snapshot_id": snapshot_id,
            "phase_status": review_status,
            "allow_next_stage": input_status != "PHASE_08_INPUT_BLOCKED",
            "next_stage": NEXT_PHASE,
            "required_files_for_next_stage": {
                "phase_08_handoff_packet": str(paths.handoff / "phase_08_handoff_packet.json"),
                "paper_trade_result_snapshot": artifacts["paper_trade_result_snapshot"],
                "review_fact_validation": artifacts["review_fact_validation"],
                "phase_decision_trace_json": artifacts["phase_decision_trace_json"],
                "evidence_chain_manifest": artifacts["evidence_chain_manifest"],
                "review_learning_summary": artifacts["review_learning_summary"],
                "failure_attribution": artifacts["failure_attribution"],
                "success_attribution": artifacts["success_attribution"],
                "rule_update_candidates": artifacts["rule_update_candidates"],
                "threshold_review_candidates": artifacts["threshold_review_candidates"],
                "model_recalibration_candidates": artifacts["model_recalibration_candidates"],
                "scenario_case_library": artifacts["scenario_case_library"],
                "address_history_update": artifacts["address_history_update"],
                "strategy_performance_summary": artifacts["strategy_performance_summary"],
            },
            "positive_evidence": [s["success_type"] for s in successes],
            "negative_evidence": [f["failure_type"] for f in failures],
            "evidence_chain_status": evidence_chain_manifest["evidence_chain_status"],
            "review_fact_status": review_fact_validation["review_fact_status"],
            "hard_negative_triggered": bool(block_reasons),
            "hard_negative_reasons": block_reasons,
            "block_reason": ";".join(block_reasons),
            "degrade_reason": ";".join(summary["missing_fields"]),
            "missing_fields": summary["missing_fields"],
            "audit_file": str(paths.audit / "audit_report.md"),
        }
        artifacts["handoff_packet"] = str(self._write_json(paths.handoff / "phase_08_handoff_packet.json", handoff))
        validation = {"status": "PASS", "checked_files": artifacts, "missing_outputs": [k for k, v in artifacts.items() if not Path(v).exists()]}
        handoff_validation = self._handoff_validation(handoff)
        artifacts["output_validation_report"] = str(self._write_json(paths.audit / "output_validation_report.json", validation))
        artifacts["handoff_validation_report"] = str(self._write_json(paths.audit / "handoff_validation_report.json", handoff_validation))
        artifacts["missing_fields_report"] = str(self._write_text(paths.audit / "missing_fields_report.md", self._missing_md(summary["missing_fields"])))
        artifacts["gaps"] = str(self._write_text(paths.audit / "gaps.md", "# Gaps\n\n- Phase08 当前输出规则/阈值/模型候选，由 Phase09 决定是否应用。\n"))
        artifacts["audit_report"] = str(self._write_text(paths.audit / "audit_report.md", self._audit_md(summary, artifacts)))
        return {"phase": PHASE, "status": review_status, "artifacts": artifacts, "summary": summary}

    def _load_required(self, required_files: Dict[str, str]) -> Tuple[Dict[str, Any], List[str]]:
        loaded: Dict[str, Any] = {}
        missing: List[str] = []
        for key, raw in required_files.items():
            if not raw:
                missing.append(key); continue
            p = Path(raw)
            if not p.exists():
                missing.append(key); continue
            try:
                if p.suffix == ".jsonl":
                    loaded[key] = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
                elif p.suffix == ".json":
                    loaded[key] = self._read_json(p, default={})
                elif p.suffix == ".csv":
                    loaded[key] = list(csv.DictReader(p.open(encoding="utf-8")))
                else:
                    loaded[key] = p.read_text(encoding="utf-8")
            except Exception:
                missing.append(key)
        return loaded, self._dedupe(missing)

    def _evidence_chain_manifest(self, token: str, snapshot_id: str, handoff: Dict[str, Any], loaded: Dict[str, Any], trace: Dict[str, Any], evidence_missing: List[str], missing_fields: List[str]) -> Dict[str, Any]:
        links: List[Dict[str, Any]] = []
        required_files = handoff.get("required_files_for_next_stage", {}) if isinstance(handoff, dict) else {}
        for phase in trace.get("phases", []):
            key = phase.get("source_key", "missing")
            source_path = required_files.get(key, "missing") if isinstance(required_files, dict) else "missing"
            links.append({
                "phase": phase.get("phase", "missing"),
                "source_key": key,
                "source_path": source_path,
                "present": bool(phase.get("present")),
                "status": phase.get("status", "missing"),
                "positive_evidence_count": len(phase.get("positive_evidence") or []),
                "negative_evidence_count": len(phase.get("negative_evidence") or []),
                "counter_evidence_count": len(phase.get("counter_evidence") or []),
                "evidence_level": phase.get("evidence_level", "missing"),
                "risk_level": phase.get("risk_level", "missing"),
            })
        status = "EVIDENCE_CHAIN_COMPLETE" if not evidence_missing else "EVIDENCE_CHAIN_DEGRADED"
        if all(not item.get("present") for item in links):
            status = "EVIDENCE_CHAIN_BLOCKED"
        return {
            "phase": PHASE,
            "token_address": token,
            "snapshot_id": snapshot_id,
            "evidence_chain_status": status,
            "required_phase_count": len(links),
            "present_phase_count": sum(1 for item in links if item.get("present")),
            "missing_evidence_chain": evidence_missing,
            "missing_fields": missing_fields,
            "links": links,
            "absolute_conclusion_allowed": False,
        }

    def _review_fact_validation(self, token: str, snapshot_id: str, execution: Dict[str, Any], paper: Dict[str, Any], open_positions: List[Dict[str, Any]], closed_positions: List[Dict[str, Any]], paper_trades: List[Dict[str, Any]], equity_curve: List[Dict[str, Any]], risk_events: List[Dict[str, Any]], evidence_chain_manifest: Dict[str, Any], input_status: str, block_reasons: List[str]) -> Dict[str, Any]:
        fact_sources = {
            "execution_risk_decision": bool(execution),
            "paper_trade_decision": bool(paper),
            "paper_positions_open": bool(open_positions),
            "paper_positions_closed": bool(closed_positions),
            "paper_trades": bool(paper_trades),
            "paper_equity_curve": bool(equity_curve),
            "risk_events": bool(risk_events),
        }
        missing_core = [key for key in ["execution_risk_decision", "paper_trade_decision"] if not fact_sources[key]]
        has_outcome_fact = any(fact_sources[key] for key in ["paper_positions_open", "paper_positions_closed", "paper_trades", "risk_events"])
        if block_reasons:
            status = "REVIEW_FACT_BLOCKED"
        elif missing_core or not has_outcome_fact:
            status = "REVIEW_FACT_DEGRADED"
        else:
            status = "REVIEW_FACT_COMPLETE"
        return {
            "phase": PHASE,
            "token_address": token,
            "snapshot_id": snapshot_id,
            "review_fact_status": status,
            "input_status": input_status,
            "fact_sources": fact_sources,
            "missing_core_facts": missing_core,
            "has_outcome_fact": has_outcome_fact,
            "evidence_chain_status": evidence_chain_manifest.get("evidence_chain_status"),
            "block_reasons": block_reasons,
            "paper_only_review": True,
            "direct_rule_change_allowed": False,
        }

    def _build_trace(self, token: str, snapshot_id: str, loaded: Dict[str, Any], handoff: Dict[str, Any], execution: Dict[str, Any], paper: Dict[str, Any], manual_ticket: Dict[str, Any], evidence_missing: List[str]) -> Dict[str, Any]:
        phases = []
        mapping = [
            ("phase_01_data_fact_controller", "data_quality_summary"),
            ("phase_02_wallet_structure_controller", "wallet_structure_decision"),
            ("phase_03_chip_control_controller", "chip_control_summary"),
            ("phase_04_scenario_recognition_controller", "primary_scenario"),
            ("phase_05_structure_position_controller", "structure_position_decision"),
            ("phase_06_strategy_gate_controller", "strategy_gate_decision"),
            ("phase_07_execution_risk_controller", "execution_risk_decision"),
        ]
        for phase, key in mapping:
            item = loaded.get(key, {}) if key != "execution_risk_decision" else execution
            phases.append({
                "phase": phase,
                "source_key": key,
                "present": bool(item),
                "status": self._status_of(item),
                "positive_evidence": item.get("positive_evidence", []) if isinstance(item, dict) else [],
                "negative_evidence": item.get("negative_evidence", []) if isinstance(item, dict) else [],
                "counter_evidence": item.get("counter_evidence", []) if isinstance(item, dict) else [],
                "evidence_level": item.get("evidence_level", "missing") if isinstance(item, dict) else "missing",
                "risk_level": item.get("risk_level", "missing") if isinstance(item, dict) else "missing",
            })
        return {"phase": PHASE, "token_address": token, "snapshot_id": snapshot_id, "phase07_handoff_status": handoff.get("phase_status", "missing"), "paper_trade_status": paper.get("paper_trade_status", execution.get("paper_trade_status", "missing")), "phases": phases, "manual_confirmation_ticket": manual_ticket, "missing_evidence_chain": evidence_missing}

    def _attribute(self, token: str, input_status: str, execution: Dict[str, Any], paper: Dict[str, Any], open_positions: List[Dict[str, Any]], closed_positions: List[Dict[str, Any]], paper_trades: List[Dict[str, Any]], risk_events: List[Dict[str, Any]], loaded: Dict[str, Any], evidence_missing: List[str], block_reasons: List[str]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        failures: List[Dict[str, Any]] = []
        successes: List[Dict[str, Any]] = []
        now = self._now()
        if input_status == "PHASE_08_INPUT_BLOCKED":
            for reason in block_reasons:
                failures.append(self._failure(token, "phase_08_review_learning_controller", reason, ["phase_07_handoff_packet"], "input_block", now))
            return failures, successes
        if evidence_missing:
            failures.append(self._failure(token, PHASE, "EVIDENCE_CHAIN_DEGRADED", [f"missing:{m}" for m in evidence_missing], "degraded_review", now))
        exec_status = execution.get("execution_risk_status", "missing")
        if exec_status in EXECUTION_BLOCK_STATUSES or risk_events:
            event_types = self._dedupe([str(e.get("event_type") or exec_status) for e in risk_events] or [exec_status])
            for event in event_types:
                failures.append(self._failure(token, "phase_07_execution_risk_controller", event, ["risk_events.jsonl", "execution_risk_decision.json"], "execution_block_review", now))
        for pos in closed_positions:
            if str(pos.get("token_address")) != token:
                continue
            pnl = self._float(pos.get("pnl_pct"), 0.0)
            if pnl < 0:
                source = self._infer_failure_phase(loaded)
                failures.append(self._failure(token, source, "PAPER_TRADE_LOSS", ["paper_positions_closed.json", "phase_decision_trace.json"], "paper_trade_result", now, pnl_pct=pnl))
            elif pnl > 0:
                source = self._infer_success_phase(loaded)
                successes.append({"timestamp": now, "token_address": token, "source_phase": source, "success_type": "PAPER_TRADE_PROFIT", "pnl_pct": pnl, "evidence_refs": ["paper_positions_closed.json", "strategy_gate_decision.json", "structure_position_decision.json"], "rule_effective": True, "absolute_conclusion": False})
        if open_positions and paper.get("paper_trade_status") == "PAPER_EXECUTED" and not closed_positions:
            successes.append({"timestamp": now, "token_address": token, "source_phase": "phase_07_execution_risk_controller", "success_type": "PAPER_POSITION_OPENED_FOR_TRACKING", "pnl_pct": None, "evidence_refs": ["paper_positions_open.json", "paper_trades.csv"], "rule_effective": True, "absolute_conclusion": False})
        return failures, successes

    def _failure(self, token: str, source_phase: str, failure_type: str, refs: List[str], category: str, ts: str, pnl_pct: float | None = None) -> Dict[str, Any]:
        return {"timestamp": ts, "token_address": token, "source_phase": source_phase, "failure_type": failure_type, "failure_category": category, "pnl_pct": pnl_pct, "evidence_refs": refs, "suggested_followup": f"review_{failure_type}", "absolute_conclusion": False}

    def _infer_failure_phase(self, loaded: Dict[str, Any]) -> str:
        scenario = loaded.get("primary_scenario", {})
        position = loaded.get("structure_position_decision", {})
        strategy = loaded.get("strategy_gate_decision", {})
        if scenario.get("risk_level") in {"HIGH", "MEDIUM"}:
            return "phase_04_scenario_recognition_controller"
        if position.get("position_status") not in {"COMPLETION_PASS", "POSITION_VALID"}:
            return "phase_05_structure_position_controller"
        if strategy.get("strategy_gate_status") in {"PAPER_READY", "READY_FOR_CONFIRMATION"}:
            return "phase_06_strategy_gate_controller"
        return "phase_08_review_learning_controller"

    def _infer_success_phase(self, loaded: Dict[str, Any]) -> str:
        if loaded.get("strategy_gate_decision", {}).get("a_plus_p1_pass") is True:
            return "phase_06_strategy_gate_controller"
        if loaded.get("structure_position_decision", {}).get("position_quality") == "P1":
            return "phase_05_structure_position_controller"
        return "phase_04_scenario_recognition_controller"

    def _position_rows(self, token: str, open_positions: List[Dict[str, Any]], closed_positions: List[Dict[str, Any]], trades: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for p in open_positions + closed_positions:
            rows.append({"token_address": p.get("token_address", token), "position_id": p.get("position_id", "missing"), "status": p.get("status", "missing"), "paper_only": str(bool(p.get("paper_only", True))).lower(), "pnl_pct": p.get("pnl_pct", "missing"), "source": "paper_position"})
        if not rows:
            for t in trades:
                rows.append({"token_address": t.get("token_address", token), "position_id": t.get("trade_id", "missing"), "status": "TRADE_ONLY", "paper_only": str(bool(t.get("paper_only", True))).lower(), "pnl_pct": "missing", "source": "paper_trade"})
        return rows

    def _address_history_updates(self, token: str, failures: List[Dict[str, Any]], successes: List[Dict[str, Any]], loaded: Dict[str, Any]) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        wallet = loaded.get("wallet_structure_decision", {})
        roles = wallet.get("candidate_roles", []) if isinstance(wallet, dict) else []
        if failures or successes or roles:
            rows.append({"token_address": token, "address": token, "update_mode": "patch", "direct_overwrite_allowed": "false", "evidence_level": wallet.get("evidence_level", "missing") if isinstance(wallet, dict) else "missing", "roles_observed": ";".join(map(str, roles)), "failure_count": str(len(failures)), "success_count": str(len(successes)), "source_phase": PHASE})
        return rows

    def _scenario_case_library(self, token: str, trace: Dict[str, Any], failures: List[Dict[str, Any]], successes: List[Dict[str, Any]], loaded: Dict[str, Any]) -> Dict[str, Any]:
        scenario = loaded.get("primary_scenario", {}) if isinstance(loaded.get("primary_scenario"), dict) else {}
        return {"phase": PHASE, "direct_rule_change_allowed": False, "cases": [{"token_address": token, "scenario": scenario.get("primary_scenario", scenario.get("scenario_status", "missing")), "outcome": "failure" if failures else ("success" if successes else "review_only"), "source_phase_trace": [p["phase"] for p in trace.get("phases", [])], "failure_types": [f["failure_type"] for f in failures], "success_types": [s["success_type"] for s in successes], "evidence_refs": ["phase_decision_trace.json", "paper_trade_result_snapshot.json"]}]}

    def _strategy_performance(self, token: str, closed: List[Dict[str, Any]], open_pos: List[Dict[str, Any]], trades: List[Dict[str, Any]], events: List[Dict[str, Any]], failures: List[Dict[str, Any]], successes: List[Dict[str, Any]]) -> Dict[str, Any]:
        pnls = [self._float(p.get("pnl_pct"), 0.0) for p in closed if str(p.get("token_address")) == token and p.get("pnl_pct") not in (None, "")]
        return {"phase": PHASE, "token_address": token, "closed_position_count": len(pnls), "open_position_count": len(open_pos), "paper_trade_count": len(trades), "risk_event_count": len(events), "win_count": sum(1 for p in pnls if p > 0), "loss_count": sum(1 for p in pnls if p < 0), "avg_pnl_pct": round(sum(pnls) / len(pnls), 6) if pnls else 0.0, "failure_count": len(failures), "success_count": len(successes)}

    def _rule_candidates(self, failures: List[Dict[str, Any]], successes: List[Dict[str, Any]]) -> Dict[str, Any]:
        candidates = []
        for f in failures:
            target = f["source_phase"]
            candidates.append({"candidate_id": f"rule-{len(candidates)+1}", "target_phase": target, "candidate_type": "tighten_or_review_rule", "reason": f["failure_type"], "evidence_cases": [f["token_address"]], "evidence_refs": f["evidence_refs"], "phase09_only": True})
        return {"phase": PHASE, "direct_rule_change_allowed": False, "candidates": candidates}

    def _threshold_candidates(self, failures: List[Dict[str, Any]], events: List[Dict[str, Any]]) -> Dict[str, Any]:
        candidates = []
        for f in failures:
            if f["failure_type"] in {"SLIPPAGE_TOO_HIGH", "LIQUIDITY_WEAK", "PAPER_TRADE_LOSS", "EVIDENCE_CHAIN_DEGRADED"}:
                candidates.append({"candidate_id": f"threshold-{len(candidates)+1}", "target_phase": f["source_phase"], "metric": f["failure_type"], "review_reason": f["failure_type"], "evidence_cases": [f["token_address"]], "phase09_only": True})
        return {"phase": PHASE, "phase09_only": True, "candidates": candidates}

    def _model_candidates(self, failures: List[Dict[str, Any]], successes: List[Dict[str, Any]], trace: Dict[str, Any]) -> Dict[str, Any]:
        candidates = []
        if failures:
            candidates.append({"candidate_id": "model-1", "target_phase": failures[0]["source_phase"], "review_reason": "failure_pattern_detected", "evidence_cases": [f["token_address"] for f in failures], "phase09_only": True})
        return {"phase": PHASE, "phase09_only": True, "candidates": candidates}

    def _status_of(self, item: Any) -> str:
        if not isinstance(item, dict): return "missing"
        for key in ["data_quality_status", "wallet_structure_status", "chip_control_status", "scenario_status", "position_status", "strategy_gate_status", "execution_risk_status", "phase_status"]:
            if item.get(key): return str(item[key])
        return "present"

    def _handoff_validation(self, handoff: Dict[str, Any]) -> Dict[str, Any]:
        required = handoff.get("required_files_for_next_stage", {}) or {}
        missing = [key for key, raw in required.items() if not raw or raw == "missing" or not Path(str(raw)).exists()]
        required_keys = [
            "phase_08_handoff_packet",
            "paper_trade_result_snapshot",
            "review_fact_validation",
            "phase_decision_trace_json",
            "evidence_chain_manifest",
            "review_learning_summary",
            "failure_attribution",
            "success_attribution",
            "rule_update_candidates",
            "threshold_review_candidates",
            "model_recalibration_candidates",
            "scenario_case_library",
            "address_history_update",
            "strategy_performance_summary",
        ]
        absent_keys = [key for key in required_keys if key not in required]
        ok = handoff.get("next_stage") == NEXT_PHASE and not missing and not absent_keys and handoff.get("review_fact_status") in {"REVIEW_FACT_COMPLETE", "REVIEW_FACT_DEGRADED", "REVIEW_FACT_BLOCKED"} and handoff.get("evidence_chain_status") in {"EVIDENCE_CHAIN_COMPLETE", "EVIDENCE_CHAIN_DEGRADED", "EVIDENCE_CHAIN_BLOCKED"}
        return {
            "status": "PASS" if ok else "FAIL",
            "next_stage": NEXT_PHASE,
            "allow_next_stage": handoff.get("allow_next_stage"),
            "direct_rule_change_allowed": False,
            "missing_required_files_for_next_stage": missing,
            "missing_required_handoff_keys": absent_keys,
            "evidence_chain_status": handoff.get("evidence_chain_status"),
            "review_fact_status": handoff.get("review_fact_status"),
        }

    def _read_json(self, path: Path, default: Any) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return default

    def _write_json(self, path: Path, data: Any) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return path

    def _write_jsonl(self, path: Path, rows: Iterable[Dict[str, Any]]) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        return path

    def _write_csv(self, path: Path, rows: List[Dict[str, Any]]) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        fields: List[str] = []
        for row in rows:
            for k in row:
                if k not in fields: fields.append(k)
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields or ["empty"])
            writer.writeheader()
            if rows: writer.writerows(rows)
        return path

    def _write_text(self, path: Path, text: str) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def _trace_md(self, trace: Dict[str, Any]) -> str:
        lines = ["# Phase08 Phase Decision Trace", "", f"- token_address: {trace.get('token_address')}", f"- snapshot_id: {trace.get('snapshot_id')}", "", "## Phases"]
        for p in trace.get("phases", []):
            lines.append(f"- {p['phase']}: present={str(p['present']).lower()}, status={p['status']}, evidence_level={p['evidence_level']}, risk_level={p['risk_level']}")
        return "\n".join(lines) + "\n"

    def _daily_report(self, summary: Dict[str, Any], failures: List[Dict[str, Any]], successes: List[Dict[str, Any]]) -> str:
        return "\n".join(["# Phase08 Daily Review Report", "", f"- review_status: {summary['review_status']}", f"- input_status: {summary['input_status']}", f"- failure_count: {len(failures)}", f"- success_count: {len(successes)}", "- direct_rule_change_allowed: false", "", "## Boundary", "- 本报告是归因与回灌建议，不直接修改规则。", ""])

    def _audit_md(self, summary: Dict[str, Any], artifacts: Dict[str, str]) -> str:
        return "\n".join(["# Phase08 Review Learning Audit", "", f"- phase: {PHASE}", f"- input_status: {summary['input_status']}", f"- review_status: {summary['review_status']}", f"- direct_rule_change_allowed: {str(summary['direct_rule_change_allowed']).lower()}", f"- missing_fields: {', '.join(summary['missing_fields']) if summary['missing_fields'] else 'none'}", f"- block_reasons: {', '.join(summary['block_reasons']) if summary['block_reasons'] else 'none'}", "", "## Outputs", *[f"- {k}: {v}" for k, v in sorted(artifacts.items()) if k != "audit_report"], "", "## Phase09 下一步", "- 读取 Phase08 handoff 与候选文件，由 Phase09 决定是否进入规则/阈值/模型升级。", ""])

    def _missing_md(self, missing: List[str]) -> str:
        return "# Missing Fields\n\n" + ("\n".join(f"- {m}" for m in missing) if missing else "- none\n")

    def _first_token(self, rows: Iterable[Dict[str, Any]]) -> str | None:
        for row in rows:
            if isinstance(row, dict) and row.get("token_address"):
                return str(row["token_address"])
        return None

    def _float(self, value: Any, default: float) -> float:
        try:
            return float(value)
        except Exception:
            return default

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _dedupe(self, items: Iterable[str]) -> List[str]:
        out: List[str] = []
        for item in items:
            if item and item not in out:
                out.append(str(item))
        return out
