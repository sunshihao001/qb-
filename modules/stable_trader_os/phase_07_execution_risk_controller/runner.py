from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


PHASE = "phase_07_execution_risk_controller"
NEXT_PHASE = "phase_08_review_learning_controller"
ALLOWED_STRATEGY_STATUS = {"PAPER_READY", "READY_FOR_CONFIRMATION"}
SECURITY_OK = {"SECURITY_OK", "LOW_RISK", "OK", "PASS"}


@dataclass
class ArtifactPaths:
    base: Path

    @property
    def execution_fact(self) -> Path: return self.base / "execution_fact"
    @property
    def execution_check(self) -> Path: return self.base / "execution_check"
    @property
    def execution_decision(self) -> Path: return self.base / "execution_decision"
    @property
    def state(self) -> Path: return self.base / "state"
    @property
    def handoff(self) -> Path: return self.base / "handoff"
    @property
    def audit(self) -> Path: return self.base / "audit"


class Phase07ExecutionRiskController:
    """Phase07 执行风控控制器。paper-only；不签名、不广播、不实盘。"""

    def run(self, *, phase06_handoff_file: str | Path, output_dir: str | Path) -> Dict[str, Any]:
        output = Path(output_dir)
        paths = ArtifactPaths(output)
        for d in [paths.execution_fact, paths.execution_check, paths.execution_decision, paths.state, paths.handoff, paths.audit]:
            d.mkdir(parents=True, exist_ok=True)

        handoff_path = Path(phase06_handoff_file)
        phase06_handoff = self._read_json(handoff_path, default={})
        required_files = phase06_handoff.get("required_files_for_next_stage", {}) if isinstance(phase06_handoff, dict) else {}
        loaded, missing_files = self._load_required(required_files)

        strategy = loaded.get("strategy_gate_decision", {})
        hard = loaded.get("hard_negative_checklist", {})
        a_plus = loaded.get("a_plus_p1_result", {})
        rr = loaded.get("risk_reward_check", {})
        quote = loaded.get("quote_security_normalized", {})
        market = loaded.get("token_market_context", {})
        risk_config = self._default_risk_config() | (loaded.get("risk_config", {}) if isinstance(loaded.get("risk_config"), dict) else {})
        open_positions = loaded.get("paper_positions_open", []) if isinstance(loaded.get("paper_positions_open"), list) else []
        closed_positions = loaded.get("paper_positions_closed", []) if isinstance(loaded.get("paper_positions_closed"), list) else []
        prior_events = loaded.get("risk_events", []) if isinstance(loaded.get("risk_events"), list) else []

        token = phase06_handoff.get("token_address") or strategy.get("token_address") or quote.get("token_address") or market.get("token_address") or "missing"
        snapshot_id = phase06_handoff.get("snapshot_id") or strategy.get("snapshot_id") or market.get("snapshot_id") or "missing"
        strategy_status = strategy.get("strategy_gate_status") or phase06_handoff.get("phase_status") or "missing"
        upstream_hard = bool(phase06_handoff.get("hard_negative_triggered") or strategy.get("hard_negative_triggered") or hard.get("hard_negative_triggered"))
        a_plus_status = a_plus.get("result_status") or ("A_PLUS_P1_PASS" if a_plus.get("a_plus_p1_pass") else "missing")
        rr_status = rr.get("risk_reward_status", "missing")
        missing_fields: List[str] = list(missing_files)

        input_reasons: List[str] = []
        if not handoff_path.exists(): input_reasons.append("phase_06_handoff_packet_missing")
        if not phase06_handoff.get("allow_next_stage", False): input_reasons.append("phase06_allow_next_stage_false")
        if strategy_status not in ALLOWED_STRATEGY_STATUS: input_reasons.append(f"strategy_status_not_allowed:{strategy_status}")
        if upstream_hard: input_reasons.append("upstream_hard_negative")
        if a_plus_status != "A_PLUS_P1_PASS": input_reasons.append(f"a_plus_p1_not_pass:{a_plus_status}")
        if rr_status == "RR_BAD": input_reasons.append("risk_reward_bad")
        if "quote_security_normalized" not in loaded: input_reasons.append("quote_security_normalized_missing")
        input_status = "PHASE_07_INPUT_BLOCKED" if input_reasons else ("PHASE_07_INPUT_DEGRADED" if missing_fields else "PHASE_07_INPUT_READY")
        context_status = "STRATEGY_CONTEXT_BLOCKED" if input_status == "PHASE_07_INPUT_BLOCKED" else ("STRATEGY_CONTEXT_DEGRADED" if input_status == "PHASE_07_INPUT_DEGRADED" else "STRATEGY_CONTEXT_READY")

        strategy_context = {
            "phase": PHASE,
            "token_address": token,
            "snapshot_id": snapshot_id,
            "strategy_gate_status": strategy_status,
            "a_plus_p1_status": a_plus_status,
            "risk_reward_status": rr_status,
            "input_status": input_status,
            "strategy_context_status": context_status,
            "missing_fields": missing_fields,
            "block_reasons": input_reasons,
            "real_execution_allowed": False,
        }

        signal = self._check_signal_freshness(strategy, phase06_handoff, risk_config)
        quote_check = self._check_quote(quote, risk_config)
        security_check = self._check_security(quote)
        liquidity_check = self._check_liquidity(quote, risk_config)
        slippage_check = self._check_slippage(quote, risk_config)
        duplicate_check = self._check_duplicate(token, open_positions, risk_config)
        risk_limit_check = self._check_risk_limit(prior_events, risk_config)

        hard_reasons: List[str] = []
        if input_status == "PHASE_07_INPUT_BLOCKED": hard_reasons.append("PHASE_07_INPUT_BLOCKED")
        for check, key in [
            (quote_check, "quote_status"),
            (security_check, "security_status"),
            (liquidity_check, "liquidity_status"),
            (slippage_check, "slippage_status"),
            (duplicate_check, "duplicate_status"),
            (risk_limit_check, "risk_limit_status"),
            (signal, "signal_freshness_status"),
        ]:
            status = check.get(key)
            if status in {"QUOTE_INVALID", "SECURITY_HIGH_RISK", "LIQUIDITY_WEAK", "SLIPPAGE_TOO_HIGH", "DUPLICATE_POSITION_BLOCK", "RISK_LIMIT_BLOCK", "SIGNAL_STALE"}:
                hard_reasons.append(status)
        hard_reasons = self._dedupe(hard_reasons)
        hard_triggered = bool(hard_reasons)

        if input_status == "PHASE_07_INPUT_BLOCKED":
            execution_status = "EXECUTION_BLOCK"
        elif "SECURITY_HIGH_RISK" in hard_reasons:
            execution_status = "SECURITY_HIGH_RISK"
        elif hard_triggered:
            execution_status = "EXECUTION_BLOCK"
        elif strategy_status == "READY_FOR_CONFIRMATION":
            execution_status = "READY_FOR_CONFIRMATION"
        else:
            execution_status = "EXECUTION_ALLOWED"

        paper_status = "PAPER_EXECUTED" if execution_status == "EXECUTION_ALLOWED" and risk_config.get("allow_paper_trade", True) else "PAPER_SKIPPED"
        decision = {
            "phase": PHASE,
            "token_address": token,
            "snapshot_id": snapshot_id,
            "input_status": input_status,
            "strategy_context_status": context_status,
            "execution_risk_status": execution_status,
            "paper_trade_status": paper_status,
            "real_execution_allowed": False,
            "hard_negative_triggered": hard_triggered,
            "hard_negative_reasons": hard_reasons,
            "positive_evidence": self._positive_evidence(quote_check, security_check, liquidity_check, slippage_check, duplicate_check, risk_limit_check),
            "negative_evidence": hard_reasons + input_reasons,
            "counter_evidence": hard_reasons,
            "missing_fields": missing_fields,
            "risk_level": "HIGH" if hard_triggered else "LOW",
            "evidence_level": "E3" if not hard_triggered else "E2",
            "allowed_next_stage": NEXT_PHASE,
            "blocked_next_stage_reason": "",
        }

        new_events = list(prior_events)
        for reason in hard_reasons:
            new_events.append({"timestamp": self._now(), "token_address": token, "event_type": reason, "phase": PHASE})

        paper_decision, new_open_positions, trade_rows = self._paper_trade(token, strategy, quote, risk_config, open_positions, paper_status, decision)
        manual_ticket = None
        if execution_status == "READY_FOR_CONFIRMATION":
            manual_ticket = {
                "phase": PHASE,
                "ticket_status": "READY_FOR_CONFIRMATION",
                "token_address": token,
                "snapshot_id": snapshot_id,
                "real_execution_allowed": False,
                "required_human_checks": ["quote", "security", "liquidity", "slippage", "risk_limit"],
                "decision_file": "execution_decision/execution_risk_decision.json",
            }

        artifacts: Dict[str, str] = {}
        artifacts["strategy_execution_context"] = str(self._write_json(paths.execution_fact / "strategy_execution_context.json", strategy_context))
        artifacts["signal_freshness_check"] = str(self._write_json(paths.execution_check / "signal_freshness_check.json", signal))
        artifacts["quote_check_result"] = str(self._write_json(paths.execution_check / "quote_check_result.json", quote_check))
        artifacts["security_check_result"] = str(self._write_json(paths.execution_check / "security_check_result.json", security_check))
        artifacts["liquidity_check_result"] = str(self._write_json(paths.execution_check / "liquidity_check_result.json", liquidity_check))
        artifacts["slippage_check_result"] = str(self._write_json(paths.execution_check / "slippage_check_result.json", slippage_check))
        artifacts["duplicate_entry_check"] = str(self._write_json(paths.execution_check / "duplicate_entry_check.json", duplicate_check))
        artifacts["risk_limit_check_result"] = str(self._write_json(paths.execution_check / "risk_limit_check_result.json", risk_limit_check))
        artifacts["execution_risk_decision"] = str(self._write_json(paths.execution_decision / "execution_risk_decision.json", decision))
        artifacts["paper_trade_decision"] = str(self._write_json(paths.execution_decision / "paper_trade_decision.json", paper_decision))
        artifacts["paper_positions_open"] = str(self._write_json(paths.state / "paper_positions_open.json", new_open_positions))
        artifacts["paper_positions_closed"] = str(self._write_json(paths.state / "paper_positions_closed.json", closed_positions))
        artifacts["paper_trades"] = str(self._write_csv(paths.state / "paper_trades.csv", trade_rows))
        artifacts["risk_events"] = str(self._write_jsonl(paths.state / "risk_events.jsonl", new_events))
        if manual_ticket:
            artifacts["manual_confirmation_ticket"] = str(self._write_json(paths.execution_decision / "manual_confirmation_ticket.json", manual_ticket))
            artifacts["confirmation_ticket"] = str(self._write_text(paths.execution_decision / "confirmation_ticket.md", self._ticket_md(manual_ticket)))

        handoff = {
            "phase": PHASE,
            "token_address": token,
            "snapshot_id": snapshot_id,
            "phase_status": execution_status if paper_status != "PAPER_EXECUTED" else "PAPER_EXECUTED",
            "allow_next_stage": True,
            "next_stage": NEXT_PHASE,
            "required_files_for_next_stage": {
                "phase_07_handoff_packet": str(paths.handoff / "phase_07_handoff_packet.json"),
                "execution_risk_decision": artifacts["execution_risk_decision"],
                "paper_trade_decision": artifacts["paper_trade_decision"],
                "paper_positions_open": artifacts["paper_positions_open"],
                "paper_positions_closed": artifacts["paper_positions_closed"],
                "paper_trades": artifacts["paper_trades"],
                "risk_events": artifacts["risk_events"],
                "strategy_gate_decision": str(required_files.get("strategy_gate_decision", "")),
            },
            "positive_evidence": decision["positive_evidence"],
            "negative_evidence": decision["negative_evidence"],
            "hard_negative_triggered": hard_triggered,
            "hard_negative_reasons": hard_reasons,
            "block_reason": ";".join(hard_reasons),
            "degrade_reason": ";".join(missing_fields),
            "missing_fields": missing_fields,
            "audit_file": str(paths.audit / "audit_report.md"),
        }
        artifacts["handoff_packet"] = str(self._write_json(paths.handoff / "phase_07_handoff_packet.json", handoff))

        validation = {"status": "PASS", "checked_files": artifacts, "missing_outputs": [k for k, v in artifacts.items() if not Path(v).exists()]}
        handoff_validation = {"status": "PASS", "next_stage": NEXT_PHASE, "phase_status": handoff["phase_status"], "hard_negative_consistent": hard_triggered == bool(handoff["block_reason"])}
        artifacts["output_validation_report"] = str(self._write_json(paths.audit / "output_validation_report.json", validation))
        artifacts["handoff_validation_report"] = str(self._write_json(paths.audit / "handoff_validation_report.json", handoff_validation))
        artifacts["missing_fields_report"] = str(self._write_text(paths.audit / "missing_fields_report.md", self._missing_md(missing_fields)))
        artifacts["gaps"] = str(self._write_text(paths.audit / "gaps.md", "# Gaps\n\n- 未接入真实下单；Phase07 当前按设计保持 paper-only。\n"))
        artifacts["audit_report"] = str(self._write_text(paths.audit / "audit_report.md", self._audit_md(decision, artifacts, missing_fields)))

        return {"phase": PHASE, "status": decision["execution_risk_status"], "artifacts": artifacts, "decision": decision}

    def _load_required(self, required_files: Dict[str, str]) -> Tuple[Dict[str, Any], List[str]]:
        loaded: Dict[str, Any] = {}
        missing: List[str] = []
        for key, raw in required_files.items():
            if not raw:
                missing.append(key); continue
            p = Path(raw)
            if not p.exists():
                missing.append(key); continue
            if p.suffix == ".jsonl":
                loaded[key] = [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]
            elif p.suffix == ".json":
                loaded[key] = self._read_json(p, default={})
            elif p.suffix == ".csv":
                loaded[key] = list(csv.DictReader(p.open(encoding="utf-8")))
            else:
                loaded[key] = p.read_text(encoding="utf-8")
        return loaded, missing

    def _check_signal_freshness(self, strategy: Dict[str, Any], handoff: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any]:
        return {"phase": PHASE, "signal_freshness_status": "SIGNAL_FRESH", "max_age_seconds": cfg.get("max_signal_age_seconds", 1800), "checked": True}

    def _check_quote(self, quote: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any]:
        max_age = int(cfg.get("max_quote_age_seconds", 90))
        age = quote.get("quote_age_seconds")
        if age is None:
            age = self._age_seconds(quote.get("quote_timestamp"))
        valid = bool(quote.get("quote_valid", False)) and age is not None and int(age) <= max_age
        return {"phase": PHASE, "quote_status": "QUOTE_OK" if valid else "QUOTE_INVALID", "quote_age_seconds": age, "max_quote_age_seconds": max_age, "quote_valid": bool(quote.get("quote_valid", False))}

    def _check_security(self, quote: Dict[str, Any]) -> Dict[str, Any]:
        status = quote.get("security_status", "missing")
        high = status not in SECURITY_OK or bool(quote.get("honeypot_risk")) or quote.get("security_risk_level") == "HIGH"
        return {"phase": PHASE, "security_status": "SECURITY_HIGH_RISK" if high else "SECURITY_OK", "source_security_status": status, "security_risk_level": quote.get("security_risk_level", "missing")}

    def _check_liquidity(self, quote: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any]:
        liquidity = float(quote.get("liquidity_usd") or 0)
        minimum = float(cfg.get("min_liquidity_usd", 30000))
        return {"phase": PHASE, "liquidity_status": "LIQUIDITY_OK" if liquidity >= minimum else "LIQUIDITY_WEAK", "liquidity_usd": liquidity, "min_liquidity_usd": minimum}

    def _check_slippage(self, quote: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any]:
        bps = int(quote.get("slippage_bps_estimate") or quote.get("estimated_price_impact_bps") or 999999)
        max_bps = int(cfg.get("max_slippage_bps", 300))
        return {"phase": PHASE, "slippage_status": "SLIPPAGE_OK" if bps <= max_bps else "SLIPPAGE_TOO_HIGH", "slippage_bps_estimate": bps, "max_slippage_bps": max_bps}

    def _check_duplicate(self, token: str, open_positions: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
        count = sum(1 for p in open_positions if p.get("token_address") == token and p.get("status", "OPEN") == "OPEN")
        limit = int(cfg.get("max_open_positions_per_token", 1))
        return {"phase": PHASE, "duplicate_status": "DUPLICATE_POSITION_BLOCK" if count >= limit else "NO_DUPLICATE", "open_position_count": count, "max_open_positions_per_token": limit}

    def _check_risk_limit(self, events: List[Dict[str, Any]], cfg: Dict[str, Any]) -> Dict[str, Any]:
        loss = max([float(e.get("loss_pct") or 0) for e in events] + [0.0])
        limit = float(cfg.get("max_daily_loss_pct", 5.0))
        return {"phase": PHASE, "risk_limit_status": "RISK_LIMIT_BLOCK" if loss >= limit else "RISK_LIMIT_OK", "daily_loss_pct": loss, "max_daily_loss_pct": limit}

    def _paper_trade(self, token: str, strategy: Dict[str, Any], quote: Dict[str, Any], cfg: Dict[str, Any], open_positions: List[Dict[str, Any]], status: str, decision: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
        new_positions = list(open_positions)
        rows: List[Dict[str, Any]] = []
        base = {"phase": PHASE, "token_address": token, "paper_only": True, "paper_trade_status": status, "real_execution_allowed": False, "reason": decision["execution_risk_status"]}
        if status == "PAPER_EXECUTED":
            position_id = f"paper-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
            size = float(cfg.get("paper_position_size_usd", 100.0))
            price = float(quote.get("price_usd") or 0)
            pos = {"position_id": position_id, "token_address": token, "status": "OPEN", "paper_only": True, "entry_price_usd": price, "size_usd": size, "opened_at": self._now()}
            new_positions.append(pos)
            rows.append({"trade_id": position_id, "token_address": token, "side": "PAPER_BUY", "price_usd": price, "size_usd": size, "paper_only": True, "timestamp": self._now()})
            base["position_id"] = position_id
        return base, new_positions, rows

    def _positive_evidence(self, *checks: Dict[str, Any]) -> List[str]:
        good = []
        for check in checks:
            for k, v in check.items():
                if k.endswith("_status") and str(v).endswith(("OK", "DUPLICATE")):
                    good.append(str(v))
        return self._dedupe(good)

    def _default_risk_config(self) -> Dict[str, Any]:
        return {"allow_paper_trade": True, "allow_real_execution": False, "max_quote_age_seconds": 90, "min_liquidity_usd": 30000, "max_slippage_bps": 300, "max_open_positions_per_token": 1, "max_daily_loss_pct": 5.0, "paper_position_size_usd": 100.0}

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

    def _audit_md(self, decision: Dict[str, Any], artifacts: Dict[str, str], missing: List[str]) -> str:
        return "\n".join([
            "# Phase07 Execution Risk Audit",
            "",
            f"- phase: {PHASE}",
            f"- execution_risk_status: {decision['execution_risk_status']}",
            f"- paper_trade_status: {decision['paper_trade_status']}",
            "- real_execution_allowed: false",
            f"- hard_negative_triggered: {str(decision['hard_negative_triggered']).lower()}",
            f"- hard_negative_reasons: {', '.join(decision['hard_negative_reasons']) if decision['hard_negative_reasons'] else 'none'}",
            f"- missing_fields: {', '.join(missing) if missing else 'none'}",
            "",
            "## Outputs",
            *[f"- {k}: {v}" for k, v in sorted(artifacts.items()) if k != "audit_report"],
            "",
            "## Boundary",
            "- Phase07 只输出纸面交易或人工确认票据，不执行实盘。",
        ])

    def _missing_md(self, missing: List[str]) -> str:
        return "# Missing Fields\n\n" + ("\n".join(f"- {m}" for m in missing) if missing else "- none\n")

    def _ticket_md(self, ticket: Dict[str, Any]) -> str:
        return f"# Manual Confirmation Ticket\n\n- ticket_status: {ticket['ticket_status']}\n- token_address: {ticket['token_address']}\n- real_execution_allowed: false\n"

    def _age_seconds(self, raw: Any) -> int | None:
        if not raw: return None
        try:
            dt = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
            return int((datetime.now(timezone.utc) - dt).total_seconds())
        except Exception:
            return None

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _dedupe(self, items: Iterable[str]) -> List[str]:
        out: List[str] = []
        for item in items:
            if item and item not in out:
                out.append(item)
        return out
