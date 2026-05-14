from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

PHASE_ID = "phase_06_strategy_gate_controller"
PHASE_NAME = "phase_06_strategy_filter"
NEXT_STAGE = "phase_07_execution_risk_controller"

REQUIRED_INPUTS = [
    "phase_01_handoff_packet",
    "data_quality_summary",
    "phase_02_handoff_packet",
    "wallet_structure_decision",
    "wallet_classification",
    "phase_03_handoff_packet",
    "chip_control_summary",
    "dominant_side_status",
    "chip_transfer_status",
    "counterparty_pressure",
    "phase_04_handoff_packet",
    "primary_scenario",
    "scenario_counter_evidence",
    "scenario_hard_negative_checklist",
    "phase_05_handoff_packet",
    "structure_position_decision",
    "avwap_completion_gate",
    "failure_test_result",
    "fatigue_filter_result",
    "position_overextension_check",
    "quote_security_normalized",
    "token_market_context",
]

HARD_NEGATIVE_STATUSES = {
    "DATA_INVALID",
    "WALLET_BLOCK",
    "ACTIVE_DISTRIBUTION",
    "TRANSFER_TO_COUNTERPARTY",
    "STRUCTURE_COLLAPSE",
    "SCENARIO_BLOCK",
    "SCENARIO_TRAP_RISK",
    "SCENARIO_DISTRIBUTION_RISK",
    "COMPLETION_FAIL",
    "FATIGUE_BLOCK",
    "POSITION_OVEREXTENDED",
}

SOFT_NEGATIVE_STATUSES = {
    "DATA_WEAK",
    "DATA_PARTIAL",
    "DATA_STALE",
    "WALLET_PAUSE",
    "WALLET_UNKNOWN",
    "WALLET_DATA_WEAK",
    "CONTROL_WEAKENING",
    "PARTIAL_DISTRIBUTION",
    "UNKNOWN_CONTROL",
    "SCENARIO_PAUSE",
    "SCENARIO_UNKNOWN",
    "SCENARIO_REVIEW_ONLY",
    "COMPLETION_WAIT",
    "POSITION_UNKNOWN",
}


class Phase06StrategyGateController:
    """Stable Trader OS Phase06: strategy qualification gate.

    This is a read-only/paper-only gate. It does not generate buy points or live
    execution commands. It only decides whether upstream evidence reaches A+P1
    qualification and can be handed to Phase07 execution-risk checks.
    """

    def run(self, *, phase05_handoff_file: str | Path, output_dir: str | Path) -> Dict[str, Any]:
        handoff_file = Path(phase05_handoff_file)
        out = Path(output_dir)
        phase_dir = out / "06_strategy_filter"
        dirs = self._ensure_dirs(phase_dir)

        phase05 = self._read_json(handoff_file)
        refs = self._resolve_refs(phase05, handoff_file.parent)
        validation = self._validate_inputs(refs)
        docs = self._load_docs(refs)
        token = str(phase05.get("token_address") or docs.get("token_market_context", {}).get("token_address") or "missing")
        symbol = str(phase05.get("token_symbol") or docs.get("token_market_context", {}).get("token_symbol") or "")
        snapshot_id = str(phase05.get("snapshot_id") or docs.get("token_market_context", {}).get("snapshot_id") or "missing")
        snapshot_time = self._now()

        upstream_summary, upstream_rows = self._upstream_state_summary(phase05, docs, validation)
        hard = self._hard_negative_checklist(phase05, docs, validation, upstream_rows)
        structure = self._structure_quality_assessment(docs, hard, validation)
        position = self._position_quality_assessment(docs, hard, validation)
        template = self._strategy_template_match(docs, structure, position, hard)
        risk_reward = self._risk_reward_check(docs, structure, position, hard)
        evidence = self._evidence_chain_check(docs, validation, hard, structure, position)
        scores = self._multi_dimensional_scores(structure, position, template, risk_reward, evidence, hard)
        a_plus_p1 = self._a_plus_p1_result(structure, position, template, risk_reward, evidence, hard, validation)
        decision = self._decision(
            token=token,
            symbol=symbol,
            snapshot_id=snapshot_id,
            snapshot_time=snapshot_time,
            validation=validation,
            hard=hard,
            structure=structure,
            position=position,
            template=template,
            risk_reward=risk_reward,
            evidence=evidence,
            scores=scores,
            a_plus_p1=a_plus_p1,
        )
        artifacts = self._write_outputs(
            dirs=dirs,
            token=token,
            symbol=symbol,
            snapshot_id=snapshot_id,
            snapshot_time=snapshot_time,
            upstream_summary=upstream_summary,
            upstream_rows=upstream_rows,
            hard=hard,
            structure=structure,
            position=position,
            template=template,
            risk_reward=risk_reward,
            evidence=evidence,
            scores=scores,
            a_plus_p1=a_plus_p1,
            decision=decision,
            phase05=phase05,
            validation=validation,
        )
        manifest = phase_dir / "run_manifest.json"
        manifest.write_text(json.dumps({"phase": PHASE_ID, "phase_status": decision["strategy_gate_status"], "artifacts": artifacts}, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["run_manifest"] = str(manifest)
        return {"phase": PHASE_ID, "phase_status": decision["strategy_gate_status"], "artifacts": artifacts}

    def _ensure_dirs(self, phase_dir: Path) -> Dict[str, Path]:
        dirs = {
            "phase": phase_dir,
            "strategy_fact": phase_dir / "strategy_fact",
            "strategy_decision": phase_dir / "strategy_decision",
            "handoff": phase_dir / "handoff",
            "reports": phase_dir / "reports" / "system_audit",
            "audit": phase_dir / "audit",
        }
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        return dirs

    def _resolve_refs(self, packet: Mapping[str, Any], base: Path) -> Dict[str, Path]:
        refs = dict(packet.get("handoff_files", {}) or {})
        refs.update(packet.get("required_files_for_next_stage", {}) or {})
        refs.update(packet.get("optional_files_for_next_stage", {}) or {})
        refs.setdefault("phase_05_handoff_packet", str(base / "phase_05_handoff_packet.json"))
        out: Dict[str, Path] = {}
        for key, value in refs.items():
            if not value or value == "missing":
                continue
            p = Path(str(value))
            out[key] = p if p.is_absolute() else base / p
        return out

    def _validate_inputs(self, refs: Mapping[str, Path]) -> Dict[str, Any]:
        missing = []
        present = []
        for key in REQUIRED_INPUTS:
            path = refs.get(key)
            if path is None:
                missing.append(key)
            elif not path.exists() or path.stat().st_size == 0:
                missing.append(key)
            else:
                present.append(key)
        status = "PHASE_06_INPUT_READY"
        if missing:
            status = "PHASE_06_INPUT_BLOCKED"
        return {"input_status": status, "missing_fields": missing, "present_inputs": present}

    def _load_docs(self, refs: Mapping[str, Path]) -> Dict[str, Any]:
        docs: Dict[str, Any] = {}
        for key, path in refs.items():
            if not path.exists() or path.stat().st_size == 0:
                continue
            if path.suffix.lower() == ".csv":
                docs[key] = self._read_csv(path)
            else:
                docs[key] = self._read_json(path)
        return docs

    def _upstream_state_summary(self, phase05: Mapping[str, Any], docs: Mapping[str, Any], validation: Mapping[str, Any]) -> tuple[Dict[str, Any], list[Dict[str, Any]]]:
        rows = [
            self._phase_row("phase_01_data_fact_controller", docs.get("phase_01_handoff_packet", {}), ["phase_status", "data_quality_status", "gate_status", "handoff_status"]),
            self._phase_row("phase_02_wallet_structure_controller", docs.get("wallet_structure_decision", {}), ["phase_status", "wallet_structure_status", "handoff_status"]),
            self._phase_row("phase_03_chip_control_controller", docs.get("chip_control_summary", {}), ["phase_status", "chip_control_status", "dominant_side_status", "chip_transfer_status"]),
            self._phase_row("phase_04_scenario_recognition_controller", docs.get("primary_scenario", {}), ["phase_status", "scenario_status", "primary_scenario"]),
            self._phase_row("phase_05_structure_position_controller", docs.get("structure_position_decision", phase05), ["phase_status", "completion_status", "structure_position_status", "position_extension_status", "handoff_status"]),
        ]
        summary = {
            "phase": PHASE_ID,
            "input_status": validation["input_status"],
            "missing_fields": validation["missing_fields"],
            "upstream_phase_count": len(rows),
            "hard_negative_statuses_observed": sorted({s for row in rows for s in row.get("statuses", []) if s in HARD_NEGATIVE_STATUSES}),
            "soft_negative_statuses_observed": sorted({s for row in rows for s in row.get("statuses", []) if s in SOFT_NEGATIVE_STATUSES}),
            "rows": rows,
        }
        return summary, rows

    def _phase_row(self, phase: str, doc: Any, keys: Iterable[str]) -> Dict[str, Any]:
        if not isinstance(doc, Mapping):
            return {"phase": phase, "statuses": [], "hard_negative_triggered": False, "summary": "missing_or_unreadable"}
        statuses = []
        for key in keys:
            value = doc.get(key)
            if isinstance(value, str) and value:
                statuses.append(value)
        hard_reasons = list(doc.get("hard_negative_reasons", []) or []) if isinstance(doc.get("hard_negative_reasons", []), list) else []
        statuses.extend([x for x in hard_reasons if isinstance(x, str)])
        hard_triggered = bool(doc.get("hard_negative_triggered")) or any(s in HARD_NEGATIVE_STATUSES for s in statuses)
        return {
            "phase": phase,
            "statuses": sorted(set(statuses)),
            "hard_negative_triggered": hard_triggered,
            "positive_count": len(doc.get("positive_evidence", []) or []) if isinstance(doc.get("positive_evidence", []), list) else 0,
            "negative_count": len(doc.get("negative_evidence", []) or []) if isinstance(doc.get("negative_evidence", []), list) else 0,
            "counter_count": len(doc.get("counter_evidence", []) or []) if isinstance(doc.get("counter_evidence", []), list) else 0,
        }

    def _hard_negative_checklist(self, phase05: Mapping[str, Any], docs: Mapping[str, Any], validation: Mapping[str, Any], rows: list[Dict[str, Any]]) -> Dict[str, Any]:
        reasons: list[str] = []
        for row in rows:
            for status in row.get("statuses", []):
                if status in HARD_NEGATIVE_STATUSES:
                    reasons.append(f"{row['phase']}:{status}")
            if row.get("hard_negative_triggered"):
                for status in row.get("statuses", []):
                    if status not in reasons and status in HARD_NEGATIVE_STATUSES:
                        reasons.append(f"{row['phase']}:{status}")
        for key in ["phase_01_handoff_packet", "phase_02_handoff_packet", "phase_03_handoff_packet", "phase_04_handoff_packet", "phase_05_handoff_packet", "scenario_hard_negative_checklist", "structure_position_decision"]:
            doc = docs.get(key, phase05 if key == "phase_05_handoff_packet" else {})
            if isinstance(doc, Mapping) and doc.get("hard_negative_triggered"):
                for reason in doc.get("hard_negative_reasons", []) or []:
                    reasons.append(f"{key}:{reason}")
                block = doc.get("block_reason")
                if block:
                    reasons.append(f"{key}:{block}")
        if validation["input_status"] == "PHASE_06_INPUT_BLOCKED":
            reasons.append("PHASE_06_INPUT_BLOCKED:missing_required_inputs")
        deduped = self._dedupe(reasons)
        return {
            "phase": PHASE_ID,
            "hard_negative_triggered": bool(deduped),
            "hard_negative_reasons": deduped,
            "upstream_hard_negative_statuses": sorted({s for s in HARD_NEGATIVE_STATUSES if any(s in r for r in deduped)}),
            "rule": "上游硬否决高于策略解释权；策略层不得覆盖。",
        }

    def _structure_quality_assessment(self, docs: Mapping[str, Any], hard: Mapping[str, Any], validation: Mapping[str, Any]) -> Dict[str, Any]:
        wallet = docs.get("wallet_structure_decision", {}) if isinstance(docs.get("wallet_structure_decision", {}), Mapping) else {}
        chip = docs.get("chip_control_summary", {}) if isinstance(docs.get("chip_control_summary", {}), Mapping) else {}
        primary = docs.get("primary_scenario", {}) if isinstance(docs.get("primary_scenario", {}), Mapping) else {}
        evidence_level = str(wallet.get("evidence_level") or "missing")
        wallet_status = str(wallet.get("wallet_structure_status") or wallet.get("phase_status") or "missing")
        chip_status = str(chip.get("chip_control_status") or "missing")
        scenario_status = str(primary.get("scenario_status") or "missing")
        positive = []
        negative = []
        score = 0
        if wallet_status == "WALLET_SUPPORT":
            score += 35
            positive.append("Phase02 wallet structure supports structural interpretation")
        else:
            negative.append(f"wallet_status={wallet_status}")
        if evidence_level in {"E4", "E5"}:
            score += 20
            positive.append(f"wallet_evidence_level={evidence_level}")
        elif evidence_level in {"E2", "E3"}:
            score += 10
        else:
            negative.append(f"wallet_evidence_level={evidence_level}")
        if chip_status in {"CONTROL_RETAINED", "RE_ACCUMULATION"}:
            score += 25
            positive.append(f"chip_control_status={chip_status}")
        else:
            negative.append(f"chip_control_status={chip_status}")
        if scenario_status in {"SCENARIO_ALLOW", "SCENARIO_SECOND_STAGE_CANDIDATE"}:
            score += 20
            positive.append(f"scenario_status={scenario_status}")
        elif scenario_status:
            negative.append(f"scenario_status={scenario_status}")
        passed = score >= 75 and not hard.get("hard_negative_triggered") and validation["input_status"] == "PHASE_06_INPUT_READY"
        return {"phase": PHASE_ID, "assessment": "A_STRUCTURE_PASS" if passed else "A_STRUCTURE_FAIL", "a_plus_structure_pass": passed, "score": score, "positive_evidence": positive, "negative_evidence": negative, "evidence_level": evidence_level}

    def _position_quality_assessment(self, docs: Mapping[str, Any], hard: Mapping[str, Any], validation: Mapping[str, Any]) -> Dict[str, Any]:
        decision = docs.get("structure_position_decision", {}) if isinstance(docs.get("structure_position_decision", {}), Mapping) else {}
        gate = docs.get("avwap_completion_gate", {}) if isinstance(docs.get("avwap_completion_gate", {}), Mapping) else {}
        fatigue = docs.get("fatigue_filter_result", {}) if isinstance(docs.get("fatigue_filter_result", {}), Mapping) else {}
        extension = docs.get("position_overextension_check", {}) if isinstance(docs.get("position_overextension_check", {}), Mapping) else {}
        position_status = str(decision.get("structure_position_status") or "missing")
        completion_status = str(decision.get("completion_status") or gate.get("completion_status") or "missing")
        fatigue_status = str(decision.get("fatigue_status") or fatigue.get("fatigue_status") or "missing")
        extension_status = str(decision.get("position_extension_status") or extension.get("position_extension_status") or "missing")
        passed_count = int(gate.get("completion_passed_count") or decision.get("completion_passed_count") or 0)
        positive = []
        negative = []
        score = 0
        if position_status == "POSITION_VALID":
            score += 30
            positive.append("structure_position_status=POSITION_VALID")
        else:
            negative.append(f"structure_position_status={position_status}")
        if completion_status == "COMPLETION_PASS":
            score += 30
            positive.append("completion_status=COMPLETION_PASS")
        else:
            negative.append(f"completion_status={completion_status}")
        if passed_count >= 2:
            score += 15
            positive.append(f"completion_passed_count={passed_count}")
        if fatigue_status != "FATIGUE_BLOCK":
            score += 10
            positive.append(f"fatigue_status={fatigue_status}")
        else:
            negative.append("fatigue_status=FATIGUE_BLOCK")
        if extension_status != "POSITION_OVEREXTENDED":
            score += 15
            positive.append(f"position_extension_status={extension_status}")
        else:
            negative.append("position_extension_status=POSITION_OVEREXTENDED")
        passed = score >= 80 and not hard.get("hard_negative_triggered") and validation["input_status"] == "PHASE_06_INPUT_READY"
        return {"phase": PHASE_ID, "assessment": "P1_POSITION_PASS" if passed else "P1_POSITION_FAIL", "p1_position_pass": passed, "score": score, "positive_evidence": positive, "negative_evidence": negative}

    def _strategy_template_match(self, docs: Mapping[str, Any], structure: Mapping[str, Any], position: Mapping[str, Any], hard: Mapping[str, Any]) -> Dict[str, Any]:
        primary = docs.get("primary_scenario", {}) if isinstance(docs.get("primary_scenario", {}), Mapping) else {}
        scenario_status = str(primary.get("scenario_status") or "missing")
        matched = bool(structure.get("a_plus_structure_pass") and position.get("p1_position_pass") and scenario_status in {"SCENARIO_ALLOW", "SCENARIO_SECOND_STAGE_CANDIDATE"} and not hard.get("hard_negative_triggered"))
        return {"phase": PHASE_ID, "template": "A_PLUS_P1_SECOND_STAGE" if matched else "NO_STRATEGY_TEMPLATE", "template_match_pass": matched, "scenario_status": scenario_status, "negative_evidence": [] if matched else ["template requires A structure + P1 position + allowed scenario"]}

    def _risk_reward_check(self, docs: Mapping[str, Any], structure: Mapping[str, Any], position: Mapping[str, Any], hard: Mapping[str, Any]) -> Dict[str, Any]:
        market = docs.get("token_market_context", {}) if isinstance(docs.get("token_market_context", {}), Mapping) else {}
        quote = docs.get("quote_security_normalized", {}) if isinstance(docs.get("quote_security_normalized", {}), Mapping) else {}
        current_mc = self._to_float(market.get("current_market_cap_usd"))
        discovery_mc = self._to_float(market.get("discovery_market_cap_usd"))
        extension_ratio = current_mc / discovery_mc if current_mc and discovery_mc else None
        liquidity = self._to_float(quote.get("liquidity_usd"))
        security_status = str(quote.get("security_status") or "missing")
        negative = []
        score = 50
        if extension_ratio is not None and extension_ratio <= 5:
            score += 20
        elif extension_ratio is not None:
            negative.append(f"market_cap_extension_ratio={extension_ratio:.2f}")
        if liquidity is not None and liquidity >= 30000:
            score += 15
        else:
            negative.append(f"liquidity_usd={liquidity}")
        if security_status in {"SECURITY_OK", "LOW_RISK", "missing"}:
            score += 15
        else:
            negative.append(f"security_status={security_status}")
        passed = score >= 75 and bool(structure.get("a_plus_structure_pass")) and bool(position.get("p1_position_pass")) and not hard.get("hard_negative_triggered")
        return {"phase": PHASE_ID, "risk_reward_pass": passed, "score": score, "market_cap_extension_ratio": extension_ratio, "liquidity_usd": liquidity, "security_status": security_status, "negative_evidence": negative}

    def _evidence_chain_check(self, docs: Mapping[str, Any], validation: Mapping[str, Any], hard: Mapping[str, Any], structure: Mapping[str, Any], position: Mapping[str, Any]) -> Dict[str, Any]:
        missing = list(validation.get("missing_fields", []))
        positive_count = 0
        negative_count = 0
        for doc in docs.values():
            if isinstance(doc, Mapping):
                positive_count += len(doc.get("positive_evidence", []) or []) if isinstance(doc.get("positive_evidence", []), list) else 0
                negative_count += len(doc.get("negative_evidence", []) or []) if isinstance(doc.get("negative_evidence", []), list) else 0
                negative_count += len(doc.get("counter_evidence", []) or []) if isinstance(doc.get("counter_evidence", []), list) else 0
        passed = not missing and positive_count >= 3 and not hard.get("hard_negative_triggered") and bool(structure.get("a_plus_structure_pass")) and bool(position.get("p1_position_pass"))
        return {"phase": PHASE_ID, "evidence_chain_pass": passed, "positive_evidence_count": positive_count, "negative_or_counter_evidence_count": negative_count, "missing_fields": missing, "negative_evidence": [] if passed else ["evidence chain incomplete or hard negative exists"]}

    def _multi_dimensional_scores(self, structure: Mapping[str, Any], position: Mapping[str, Any], template: Mapping[str, Any], risk_reward: Mapping[str, Any], evidence: Mapping[str, Any], hard: Mapping[str, Any]) -> Dict[str, Any]:
        score = 0
        score += int(structure.get("score") or 0) * 0.30
        score += int(position.get("score") or 0) * 0.30
        score += (100 if template.get("template_match_pass") else 0) * 0.15
        score += int(risk_reward.get("score") or 0) * 0.15
        score += (100 if evidence.get("evidence_chain_pass") else 0) * 0.10
        if hard.get("hard_negative_triggered"):
            score = min(score, 20)
        return {"phase": PHASE_ID, "strategy_score": round(score, 2), "score_components": {"structure": structure.get("score"), "position": position.get("score"), "template": template.get("template_match_pass"), "risk_reward": risk_reward.get("score"), "evidence_chain": evidence.get("evidence_chain_pass")}}

    def _a_plus_p1_result(self, structure: Mapping[str, Any], position: Mapping[str, Any], template: Mapping[str, Any], risk_reward: Mapping[str, Any], evidence: Mapping[str, Any], hard: Mapping[str, Any], validation: Mapping[str, Any]) -> Dict[str, Any]:
        passed = all([
            structure.get("a_plus_structure_pass"),
            position.get("p1_position_pass"),
            template.get("template_match_pass"),
            risk_reward.get("risk_reward_pass"),
            evidence.get("evidence_chain_pass"),
            not hard.get("hard_negative_triggered"),
            validation["input_status"] == "PHASE_06_INPUT_READY",
        ])
        return {"phase": PHASE_ID, "a_plus_p1_pass": passed, "a_plus_structure_pass": bool(structure.get("a_plus_structure_pass")), "p1_position_pass": bool(position.get("p1_position_pass")), "hard_negative_triggered": bool(hard.get("hard_negative_triggered")), "result_status": "A_PLUS_P1_PASS" if passed else "A_PLUS_P1_FAIL"}

    def _decision(self, *, token: str, symbol: str, snapshot_id: str, snapshot_time: str, validation: Mapping[str, Any], hard: Mapping[str, Any], structure: Mapping[str, Any], position: Mapping[str, Any], template: Mapping[str, Any], risk_reward: Mapping[str, Any], evidence: Mapping[str, Any], scores: Mapping[str, Any], a_plus_p1: Mapping[str, Any]) -> Dict[str, Any]:
        hard_reasons = list(hard.get("hard_negative_reasons", []) or [])
        missing = list(validation.get("missing_fields", []) or [])
        status = "PAPER_READY" if a_plus_p1.get("a_plus_p1_pass") else "STRATEGY_PAUSE"
        allowed_next_stage = NEXT_STAGE if a_plus_p1.get("a_plus_p1_pass") else "review_only"
        block_reason = ""
        if missing:
            status = "STRATEGY_BLOCK"
            allowed_next_stage = "blocked"
            block_reason = "missing_required_inputs"
        elif hard.get("hard_negative_triggered"):
            if any("POSITION_OVEREXTENDED" in r or "SCENARIO_TRAP_RISK" in r for r in hard_reasons):
                status = "REVIEW_ONLY"
                allowed_next_stage = "review_only"
            else:
                status = "STRATEGY_BLOCK"
                allowed_next_stage = "blocked"
            block_reason = ";".join(hard_reasons) or "upstream_hard_negative"
        elif not structure.get("a_plus_structure_pass") or not position.get("p1_position_pass"):
            status = "STRATEGY_PAUSE"
            allowed_next_stage = "review_only"
            block_reason = "A structure or P1 position not passed"
        invalidation = [
            "上游任一阶段出现硬否决状态",
            "Phase05 结构位置从 COMPLETION_PASS/POSITION_VALID 退化",
            "筹码侧转为 ACTIVE_DISTRIBUTION / TRANSFER_TO_COUNTERPARTY / STRUCTURE_COLLAPSE",
            "场景转为 SCENARIO_BLOCK / TRAP_RISK / DISTRIBUTION_RISK",
        ]
        execution_checks = [
            "Phase07 quote consistency check",
            "Phase07 liquidity check",
            "Phase07 slippage check",
            "Phase07 security gate",
            "Phase07 duplicate position and risk limit check",
        ]
        return {
            "phase": PHASE_ID,
            "token_address": token,
            "token_symbol": symbol,
            "snapshot_id": snapshot_id,
            "snapshot_time": snapshot_time,
            "input_status": validation["input_status"],
            "strategy_gate_status": status,
            "a_plus_structure_pass": bool(structure.get("a_plus_structure_pass")),
            "p1_position_pass": bool(position.get("p1_position_pass")),
            "a_plus_p1_pass": bool(a_plus_p1.get("a_plus_p1_pass")),
            "hard_negative_triggered": bool(hard.get("hard_negative_triggered")),
            "hard_negative_reasons": hard_reasons,
            "missing_fields": missing,
            "positive_evidence": self._dedupe((structure.get("positive_evidence", []) or []) + (position.get("positive_evidence", []) or [])),
            "negative_evidence": self._dedupe((structure.get("negative_evidence", []) or []) + (position.get("negative_evidence", []) or []) + (risk_reward.get("negative_evidence", []) or []) + (evidence.get("negative_evidence", []) or [])),
            "counter_evidence": [],
            "strategy_score": scores.get("strategy_score"),
            "invalidation_conditions": invalidation,
            "required_execution_checks": execution_checks,
            "allowed_next_stage": allowed_next_stage,
            "block_reason": block_reason,
            "boundary": "paper qualification only; no buy point; no live execution",
        }

    def _write_outputs(self, **kwargs: Any) -> Dict[str, str]:
        dirs: Mapping[str, Path] = kwargs["dirs"]
        decision = kwargs["decision"]
        phase05 = kwargs["phase05"]
        validation = kwargs["validation"]
        artifacts: Dict[str, str] = {}

        artifacts["upstream_state_summary"] = self._write_json(dirs["strategy_fact"] / "upstream_state_summary.json", kwargs["upstream_summary"])
        artifacts["upstream_state_matrix"] = self._write_csv(dirs["strategy_fact"] / "upstream_state_matrix.csv", kwargs["upstream_rows"])
        for key in ["hard", "structure", "position", "template", "risk_reward", "evidence", "scores", "a_plus_p1"]:
            name_map = {
                "hard": "hard_negative_checklist",
                "structure": "structure_quality_assessment",
                "position": "position_quality_assessment",
                "template": "strategy_template_match",
                "risk_reward": "risk_reward_check",
                "evidence": "evidence_chain_check",
                "scores": "multi_dimensional_strategy_scores",
                "a_plus_p1": "a_plus_p1_result",
            }
            artifacts[name_map[key]] = self._write_json(dirs["strategy_decision"] / f"{name_map[key]}.json", kwargs[key])
        artifacts["strategy_gate_decision"] = self._write_json(dirs["strategy_decision"] / "strategy_gate_decision.json", decision)

        handoff = self._handoff_packet(decision, phase05, artifacts, kwargs["snapshot_time"])
        artifacts["handoff_packet"] = self._write_json(dirs["handoff"] / "phase_06_handoff_packet.json", handoff)
        artifacts["missing_fields_report"] = self._write_missing_report(dirs["audit"] / "missing_fields_report.md", validation)
        artifacts["audit_report"] = self._write_audit_report(dirs["reports"] / "phase_06_strategy_gate_audit.md", decision, artifacts, validation, kwargs)
        return artifacts

    def _handoff_packet(self, decision: Mapping[str, Any], phase05: Mapping[str, Any], artifacts: Mapping[str, str], snapshot_time: str) -> Dict[str, Any]:
        allow = decision["strategy_gate_status"] in {"PAPER_READY", "READY_FOR_CONFIRMATION", "A_PLUS_P1_PASS"}
        required = {
            "phase_06_handoff_packet": artifacts.get("handoff_packet", "self"),
            "strategy_gate_decision": artifacts.get("strategy_gate_decision", "missing"),
            "hard_negative_checklist": artifacts.get("hard_negative_checklist", "missing"),
            "a_plus_p1_result": artifacts.get("a_plus_p1_result", "missing"),
            "risk_reward_check": artifacts.get("risk_reward_check", "missing"),
        }
        inherited = phase05.get("handoff_files", {}) if isinstance(phase05.get("handoff_files", {}), Mapping) else {}
        for key in ["quote_security_normalized", "token_market_context"]:
            if key in inherited:
                required[key] = inherited[key]
        return {
            "phase": PHASE_ID,
            "token_address": decision.get("token_address", "missing"),
            "token_symbol": decision.get("token_symbol", ""),
            "snapshot_id": decision.get("snapshot_id", "missing"),
            "snapshot_time": snapshot_time,
            "phase_status": decision["strategy_gate_status"],
            "allow_next_stage": allow,
            "next_stage": NEXT_STAGE,
            "required_files_for_next_stage": required,
            "positive_evidence": decision.get("positive_evidence", []),
            "negative_evidence": decision.get("negative_evidence", []),
            "hard_negative_triggered": decision.get("hard_negative_triggered", False),
            "hard_negative_reasons": decision.get("hard_negative_reasons", []),
            "block_reason": decision.get("block_reason", ""),
            "degrade_reason": "" if allow else decision.get("block_reason", "not_ready"),
            "missing_fields": decision.get("missing_fields", []),
            "audit_file": artifacts.get("audit_report", "missing"),
        }

    def _write_audit_report(self, path: Path, decision: Mapping[str, Any], artifacts: Mapping[str, str], validation: Mapping[str, Any], ctx: Mapping[str, Any]) -> str:
        lines = [
            "# Phase06 Strategy Gate Audit",
            "",
            f"- phase: {PHASE_ID}",
            f"- status: {decision['strategy_gate_status']}",
            f"- input_status: {validation['input_status']}",
            f"- missing_fields: {', '.join(validation.get('missing_fields', [])) or 'none'}",
            f"- hard_negative_triggered: {decision['hard_negative_triggered']}",
            f"- block_reason: {decision.get('block_reason') or 'none'}",
            f"- allowed_next_stage: {decision['allowed_next_stage']}",
            "",
            "## Artifacts",
        ]
        for key, value in artifacts.items():
            lines.append(f"- {key}: {value}")
        lines.extend([
            "",
            "## Boundary",
            "- Phase06 仅输出纸面资格/策略门禁，不输出买点、不执行实盘。",
            "- 上游硬否决不能被策略层覆盖。",
        ])
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(path)

    def _write_missing_report(self, path: Path, validation: Mapping[str, Any]) -> str:
        lines = ["# Phase06 Missing Fields Report", ""]
        missing = validation.get("missing_fields", []) or []
        if missing:
            for item in missing:
                lines.append(f"- missing: {item}")
        else:
            lines.append("- missing: none")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return str(path)

    def _read_json(self, path: str | Path | None) -> Dict[str, Any]:
        if not path:
            return {}
        p = Path(path)
        if not p.exists() or p.stat().st_size == 0:
            return {}
        return json.loads(p.read_text(encoding="utf-8"))

    def _read_csv(self, path: str | Path | None) -> list[Dict[str, str]]:
        if not path:
            return []
        p = Path(path)
        if not p.exists() or p.stat().st_size == 0:
            return []
        with p.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def _write_json(self, path: Path, data: Mapping[str, Any]) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(path)

    def _write_csv(self, path: Path, rows: list[Mapping[str, Any]]) -> str:
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = ["phase", "statuses", "hard_negative_triggered", "positive_count", "negative_count", "counter_count"]
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for row in rows:
                writer.writerow({
                    "phase": row.get("phase", ""),
                    "statuses": ";".join(row.get("statuses", []) or []),
                    "hard_negative_triggered": row.get("hard_negative_triggered", False),
                    "positive_count": row.get("positive_count", 0),
                    "negative_count": row.get("negative_count", 0),
                    "counter_count": row.get("counter_count", 0),
                })
        return str(path)

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def _dedupe(self, items: Iterable[Any]) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for item in items:
            text = str(item)
            if text and text not in seen:
                seen.add(text)
                out.append(text)
        return out

    def _to_float(self, value: Any) -> float | None:
        try:
            if value is None or value == "":
                return None
            return float(value)
        except (TypeError, ValueError):
            return None
