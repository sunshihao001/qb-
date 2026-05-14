from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping

PHASE_ID = "phase_04_scenario_recognition_controller"
NEXT_STAGE = "phase_05_structure_position_controller"
RISK_SCENARIOS = {
    "SCENARIO_HIGH_DISTRIBUTION",
    "SCENARIO_DOWNTREND_DISTRIBUTION",
    "SCENARIO_BULL_TRAP_BOUNCE",
    "SCENARIO_EXIT_LIQUIDITY_TRAP",
    "SCENARIO_TERMINAL_PUMP_DISTRIBUTION",
    "SCENARIO_FAKE_VOLUME_BREAKOUT",
    "SCENARIO_COUNTERPARTY_WHALE_TRAP",
}
POSITIVE_SCENARIOS = {
    "SCENARIO_ACCUMULATION",
    "SCENARIO_FIRST_EXPANSION",
    "SCENARIO_SECOND_STAGE_EXPANSION_CANDIDATE",
    "SCENARIO_REACCUMULATION",
}
VALID_SCENARIO_STATUS = {
    "SCENARIO_ALLOW",
    "SCENARIO_PAUSE",
    "SCENARIO_BLOCK",
    "SCENARIO_UNKNOWN",
    "SCENARIO_REVIEW_ONLY",
    "SCENARIO_SECOND_STAGE_CANDIDATE",
    "SCENARIO_DISTRIBUTION_RISK",
    "SCENARIO_TRAP_RISK",
}


class Phase04ScenarioRecognitionController:
    """HER Phase04 controller: chip-control evidence -> scenario recognition.

    This phase is a read-only / paper-only scenario裁决 layer. It does not emit
    entries, buy/sell advice, strategy decisions, swaps, signing, or execution.
    Risk scenario detection runs before positive scenario selection.
    """

    def run(self, *, phase03_handoff_file: str | Path, output_dir: str | Path) -> Dict[str, Any]:
        handoff_file = Path(phase03_handoff_file)
        out = Path(output_dir)
        phase_dir = out / "04_scenario_recognition"
        dirs = self._ensure_dirs(phase_dir)

        phase03 = self._read_json(handoff_file)
        validation = self._validate_phase03_handoff(phase03, handoff_file.parent)
        refs = self._resolve_refs(phase03, handoff_file.parent)
        token = str(phase03.get("token_address") or "missing")
        symbol = str(phase03.get("token_symbol") or "")
        snapshot_id = str(phase03.get("snapshot_id") or "missing")
        snapshot_time = self._now()

        chip_summary = self._read_json(refs.get("chip_control_summary"))
        dominant = self._read_json(refs.get("dominant_side_status"))
        transfer = self._read_json(refs.get("chip_transfer_status"))
        counterparty = self._read_json(refs.get("counterparty_pressure"))
        distribution = self._read_json(refs.get("distribution_sell_state"))
        backflow = self._read_json(refs.get("backflow_risk_state"))
        wallet_decision = self._read_json(refs.get("wallet_structure_decision"))
        kline_rows = self._read_csv(refs.get("kline_normalized"))
        market = self._read_json(refs.get("token_market_context"))

        missing_fields = sorted(set(validation["missing_fields"] + self._data_missing_fields(kline_rows, market, chip_summary)))
        lifecycle = self._market_lifecycle_context(token, market, chip_summary)
        price = self._price_structure_state(token, kline_rows)
        volume = self._volume_quality_state(token, kline_rows, chip_summary, distribution)
        wallet_ctx = self._wallet_scenario_context(token, wallet_decision, phase03, refs)
        chip_ctx = self._chip_scenario_context(token, chip_summary, dominant, transfer, counterparty, distribution, backflow)
        mcap = self._market_cap_scenario_context(token, market, chip_summary)

        risk_scores = self._risk_scenario_scores(lifecycle, price, volume, wallet_ctx, chip_ctx, mcap, chip_summary, counterparty)
        positive_scores = self._positive_scenario_scores(lifecycle, price, volume, wallet_ctx, chip_ctx, mcap, chip_summary)
        scored = self._score_all_scenarios(risk_scores, positive_scores)
        decision = self._decide_primary(
            token=token,
            symbol=symbol,
            snapshot_id=snapshot_id,
            snapshot_time=snapshot_time,
            lifecycle=lifecycle,
            price=price,
            volume=volume,
            wallet_ctx=wallet_ctx,
            chip_ctx=chip_ctx,
            mcap=mcap,
            scores=scored,
            missing_fields=missing_fields,
            validation=validation,
        )
        counter = self._counter_evidence(decision, chip_summary, transfer, counterparty, price, volume, wallet_ctx, mcap)
        hard = self._hard_negative_checklist(decision, chip_summary, transfer, counterparty, price, volume, wallet_ctx)
        decision["counter_evidence"] = [i["reason"] for i in counter["counter_evidence_items"]]
        decision["hard_negative_triggered"] = hard["hard_negative_triggered"]
        decision["hard_negative_reasons"] = hard["hard_negative_reasons"]
        if hard["hard_negative_triggered"]:
            decision["scenario_status"] = hard["scenario_status"]
            decision["allowed_next_stage"] = "blocked" if hard["scenario_status"] == "SCENARIO_BLOCK" else "review_only"
            decision["handoff_status"] = "HANDOFF_BLOCKED"
            decision["block_reason"] = "; ".join(hard["hard_negative_reasons"])
        artifacts = self._write_outputs(
            dirs=dirs,
            token=token,
            lifecycle=lifecycle,
            price=price,
            volume=volume,
            wallet_ctx=wallet_ctx,
            chip_ctx=chip_ctx,
            mcap=mcap,
            risk_scores=risk_scores,
            positive_scores=positive_scores,
            scores=scored,
            decision=decision,
            counter=counter,
            hard=hard,
            validation=validation,
            phase03=phase03,
        )
        manifest = phase_dir / "run_manifest.json"
        manifest.write_text(json.dumps({"phase": PHASE_ID, "phase_status": decision.get("scenario_status"), "artifacts": artifacts}, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["run_manifest"] = str(manifest)
        return {"phase": PHASE_ID, "phase_status": decision.get("scenario_status"), "artifacts": artifacts}

    def _ensure_dirs(self, phase_dir: Path) -> Dict[str, Path]:
        dirs = {
            "phase": phase_dir,
            "scenario_fact": phase_dir / "scenario_fact",
            "scenario_scores": phase_dir / "scenario_scores",
            "scenario_decision": phase_dir / "scenario_decision",
            "handoff": phase_dir / "handoff",
            "reports": phase_dir / "reports",
            "audit": phase_dir / "audit",
        }
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        return dirs

    def _resolve_refs(self, packet: Mapping[str, Any], base: Path) -> Dict[str, Path]:
        refs = dict(packet.get("handoff_files", {}) or {})
        refs.update(packet.get("required_files_for_next_stage", {}) or {})
        refs.update(packet.get("optional_files_for_next_stage", {}) or {})
        out: Dict[str, Path] = {}
        for k, v in refs.items():
            if not v or v == "missing":
                continue
            p = Path(str(v))
            out[k] = p if p.is_absolute() else base / p
        return out

    def _validate_phase03_handoff(self, packet: Mapping[str, Any], base: Path) -> Dict[str, Any]:
        errors: list[str] = []
        degrade: list[str] = []
        missing: list[str] = []
        for field in ["phase", "token_address", "snapshot_id", "chip_control_status", "handoff_files"]:
            if field not in packet:
                errors.append(f"missing_handoff_field:{field}")
                missing.append(field)
        if packet.get("allowed_next_stage") not in {PHASE_ID, "phase_04_scenario_recognition_controller", NEXT_STAGE, "blocked", None}:
            degrade.append("unexpected_allowed_next_stage")
        if packet.get("handoff_status") == "HANDOFF_BLOCKED":
            degrade.append("phase03_handoff_blocked_positive_path")
        refs = packet.get("handoff_files", {}) or {}
        for name in ["chip_control_summary", "dominant_side_status", "chip_transfer_status", "counterparty_pressure"]:
            ref = refs.get(name)
            if not ref:
                errors.append(f"missing_required_ref:{name}")
                missing.append(name)
            else:
                p = Path(ref) if Path(ref).is_absolute() else base / ref
                if not p.exists():
                    errors.append(f"missing_required_file:{name}")
        for name in ["distribution_sell_state", "backflow_risk_state", "wallet_structure_decision", "kline_normalized", "token_market_context"]:
            ref = refs.get(name)
            if not ref:
                degrade.append(f"optional_or_upstream_ref_missing:{name}")
            else:
                p = Path(ref) if Path(ref).is_absolute() else base / ref
                if not p.exists():
                    degrade.append(f"optional_or_upstream_file_missing:{name}")
        return {"errors": errors, "degrade_reasons": degrade, "missing_fields": missing}

    def _read_json(self, path: Path | None) -> dict:
        if not path or not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _read_csv(self, path: Path | None) -> list[dict]:
        if not path or not path.exists() or path.suffix.lower() != ".csv":
            return []
        with path.open(newline="", encoding="utf-8-sig") as f:
            return [dict(r) for r in csv.DictReader(f)]

    def _num(self, row: Mapping[str, Any], *keys: str, default: float = 0.0) -> float:
        for k in keys:
            v = row.get(k)
            if v in (None, "", "missing"):
                continue
            try:
                return float(str(v).replace(",", ""))
            except ValueError:
                continue
        return default

    def _data_missing_fields(self, klines: list[dict], market: Mapping[str, Any], chip: Mapping[str, Any]) -> list[str]:
        missing = []
        if not klines:
            missing.append("kline_normalized")
        else:
            for field in ["close", "volume_usd"]:
                if field not in klines[-1]:
                    missing.append(f"kline.{field}")
        for field in ["discovery_market_cap_usd", "current_market_cap_usd"]:
            if field not in market:
                missing.append(f"token_market_context.{field}")
        if "chip_control_status" not in chip:
            missing.append("chip_control_summary.chip_control_status")
        return missing

    def _market_lifecycle_context(self, token: str, market: Mapping[str, Any], chip: Mapping[str, Any]) -> dict:
        age = self._num(market, "token_age_minutes", default=-1)
        change = chip.get("market_cap_context_status") or ""
        cap_pct = self._cap_pct(market)
        if age >= 0 and age <= 60:
            status = "LIFECYCLE_NEW_LAUNCH"
        elif chip.get("chip_control_status") == "RE_ACCUMULATION":
            status = "LIFECYCLE_REACTIVATION"
        elif cap_pct != "missing" and float(cap_pct) >= 400:
            status = "LIFECYCLE_DISTRIBUTION_ZONE"
        elif chip.get("chip_control_status") == "CONTROL_RETAINED" and cap_pct != "missing" and 50 <= float(cap_pct) < 400:
            status = "LIFECYCLE_SECOND_STAGE_CANDIDATE"
        elif chip.get("chip_control_status") == "CONTROL_RETAINED":
            status = "LIFECYCLE_EARLY_ACCUMULATION"
        elif "DOWNTREND" in str(change):
            status = "LIFECYCLE_DOWNTREND"
        else:
            status = "LIFECYCLE_UNKNOWN"
        return self._fact(token, "market_lifecycle_status", status, [status], [] if status != "LIFECYCLE_UNKNOWN" else ["lifecycle_evidence_insufficient"])

    def _price_structure_state(self, token: str, rows: list[dict]) -> dict:
        if len(rows) < 2:
            return self._fact(token, "price_structure_status", "PRICE_UNKNOWN", [], ["kline_insufficient"])
        closes = [self._num(r, "close", default=0) for r in rows if self._num(r, "close", default=0) > 0]
        vols = [self._num(r, "volume_usd", default=0) for r in rows]
        if len(closes) < 2:
            return self._fact(token, "price_structure_status", "PRICE_UNKNOWN", [], ["close_missing"])
        first, last, high = closes[0], closes[-1], max(closes)
        change = (last - first) / first * 100 if first else 0
        pullback_from_high = (high - last) / high * 100 if high else 0
        vol_spike = bool(vols and vols[-1] > (sum(vols[:-1]) / max(1, len(vols[:-1]))) * 1.8)
        if change >= 80 and pullback_from_high < 20:
            status = "PRICE_UPTREND_PUSH"
        elif change >= 25 and pullback_from_high <= 35:
            status = "PRICE_BREAKOUT_PULLBACK"
        elif vol_spike and pullback_from_high > 25:
            status = "PRICE_FAILED_BREAKOUT"
        elif change <= -35:
            status = "PRICE_DOWNTREND"
        elif abs(change) < 12:
            status = "PRICE_CONTROL_BOX"
        else:
            status = "PRICE_UNKNOWN"
        return self._fact(token, "price_structure_status", status, [status], [])

    def _volume_quality_state(self, token: str, rows: list[dict], chip: Mapping[str, Any], distribution: Mapping[str, Any]) -> dict:
        if not rows:
            return self._fact(token, "volume_quality_status", "VOLUME_UNKNOWN", [], ["kline_missing"])
        vols = [self._num(r, "volume_usd", default=0) for r in rows]
        avg = sum(vols[:-1]) / max(1, len(vols[:-1])) if len(vols) > 1 else vols[-1]
        spike = avg > 0 and vols[-1] >= avg * 1.8
        exit_ratio = chip.get("early_wallet_exit_ratio")
        dist_status = distribution.get("distribution_sell_status") or chip.get("distribution_sell_status")
        if spike and dist_status in {"DISTRIBUTION_ACTIVE_SELL", "DISTRIBUTION_CLUSTER_EXIT"}:
            status = "VOLUME_DISTRIBUTION_PRESSURE"
        elif spike and chip.get("chip_control_status") in {"CONTROL_RETAINED", "CONTROL_WEAKENING"}:
            status = "VOLUME_REAL_EXPANSION"
        elif exit_ratio != "missing" and self._safe_float(exit_ratio) >= 0.55:
            status = "VOLUME_DISTRIBUTION_PRESSURE"
        elif max(vols) <= 0:
            status = "VOLUME_WEAK_LIQUIDITY"
        else:
            status = "VOLUME_ACCUMULATION_SUPPORT"
        return self._fact(token, "volume_quality_status", status, [status], [])

    def _wallet_scenario_context(self, token: str, wallet: Mapping[str, Any], phase03: Mapping[str, Any], refs: Mapping[str, Path]) -> dict:
        status0 = wallet.get("phase_status") or phase03.get("wallet_structure_status")
        if status0 == "WALLET_BLOCK":
            status = "WALLET_CONTEXT_BLOCKING"
        elif not wallet and "wallet_structure_decision" not in refs:
            status = "WALLET_CONTEXT_WEAK"
        elif status0 in {"WALLET_PAUSE", "WALLET_UNKNOWN", "WALLET_DATA_WEAK"}:
            status = "WALLET_CONTEXT_MIXED"
        elif status0 in {"WALLET_COUNTERPARTY_PRESSURE", "WALLET_DISTRIBUTION_DETECTED"}:
            status = "WALLET_CONTEXT_DISTRIBUTION_RISK"
        else:
            status = "WALLET_CONTEXT_SUPPORTIVE"
        return self._fact(token, "wallet_context_status", status, [status] if "SUPPORTIVE" in status else [], [] if "SUPPORTIVE" in status else [status])

    def _chip_scenario_context(self, token: str, chip: Mapping[str, Any], dominant: Mapping[str, Any], transfer: Mapping[str, Any], counterparty: Mapping[str, Any], distribution: Mapping[str, Any], backflow: Mapping[str, Any]) -> dict:
        st = chip.get("chip_control_status")
        tr = transfer.get("chip_transfer_status") or chip.get("chip_transfer_status")
        if st == "CONTROL_RETAINED" and tr == "CHIP_RETAINED":
            status = "CHIP_CONTEXT_SUPPORTS_EXPANSION"
        elif st == "RE_ACCUMULATION":
            status = "CHIP_CONTEXT_SUPPORTS_REACCUMULATION"
        elif st in {"ACTIVE_DISTRIBUTION", "PARTIAL_DISTRIBUTION"}:
            status = "CHIP_CONTEXT_SUPPORTS_DISTRIBUTION"
        elif st == "TRANSFER_TO_COUNTERPARTY" or tr == "CHIP_TRANSFER_TO_COUNTERPARTY":
            status = "CHIP_CONTEXT_SUPPORTS_TRAP"
        elif st == "STRUCTURE_COLLAPSE":
            status = "CHIP_CONTEXT_BLOCKING"
        elif st == "UNKNOWN_CONTROL":
            status = "CHIP_CONTEXT_UNKNOWN"
        else:
            status = "CHIP_CONTEXT_SUPPORTS_ACCUMULATION"
        return self._fact(token, "chip_context_status", status, [status] if "SUPPORTS" in status else [], [] if status not in {"CHIP_CONTEXT_BLOCKING", "CHIP_CONTEXT_UNKNOWN"} else [status])

    def _market_cap_scenario_context(self, token: str, market: Mapping[str, Any], chip: Mapping[str, Any]) -> dict:
        pct = self._cap_pct(market)
        if pct == "missing":
            status = "MARKET_CONTEXT_UNKNOWN"
        elif float(pct) >= 1000:
            status = "MARKET_CONTEXT_EXIT_LIQUIDITY"
        elif float(pct) >= 400:
            status = "MARKET_CONTEXT_OVEREXTENDED"
        elif float(pct) >= 100:
            status = "MARKET_CONTEXT_EXPANDED"
        elif float(pct) >= 0:
            status = "MARKET_CONTEXT_REASONABLE"
        else:
            status = "MARKET_CONTEXT_EARLY"
        return self._fact(token, "market_cap_context_status", status, [status], [])

    def _cap_pct(self, market: Mapping[str, Any]) -> float | str:
        d = self._num(market, "discovery_market_cap_usd", default=0)
        c = self._num(market, "current_market_cap_usd", default=0)
        if d <= 0:
            return "missing"
        return round((c - d) / d * 100, 2)

    def _risk_scenario_scores(self, lifecycle: dict, price: dict, volume: dict, wallet: dict, chip: dict, mcap: dict, chip_summary: dict, counterparty: dict) -> list[dict]:
        scores = []
        def add(scenario: str, score: int, evidence: list[str], counter: list[str] | None = None):
            scores.append(self._scenario_row(scenario, score, evidence, counter or []))
        chip_status = chip_summary.get("chip_control_status")
        cp_score = self._safe_float(counterparty.get("counterparty_pressure_score"))
        add("SCENARIO_HIGH_DISTRIBUTION", 75 if chip_status == "ACTIVE_DISTRIBUTION" and "HIGH" in price.get("price_structure_status", "") else 45 if chip_status == "ACTIVE_DISTRIBUTION" else 10, [chip_status or "missing", price.get("price_structure_status")])
        add("SCENARIO_DOWNTREND_DISTRIBUTION", 80 if chip_status == "ACTIVE_DISTRIBUTION" and price.get("price_structure_status") == "PRICE_DOWNTREND" else 15, [chip_status or "missing", price.get("price_structure_status")])
        add("SCENARIO_BULL_TRAP_BOUNCE", 70 if price.get("price_structure_status") in {"PRICE_FAILED_BREAKOUT", "PRICE_DOWNTREND"} and chip_status in {"CONTROL_WEAKENING", "ACTIVE_DISTRIBUTION"} else 15, [price.get("price_structure_status"), chip_status or "missing"])
        add("SCENARIO_EXIT_LIQUIDITY_TRAP", 90 if chip_status == "TRANSFER_TO_COUNTERPARTY" or chip.get("chip_context_status") == "CHIP_CONTEXT_SUPPORTS_TRAP" else 20, [chip_status or "missing", chip.get("chip_context_status")])
        add("SCENARIO_TERMINAL_PUMP_DISTRIBUTION", 75 if mcap.get("market_cap_context_status") in {"MARKET_CONTEXT_OVEREXTENDED", "MARKET_CONTEXT_EXIT_LIQUIDITY"} and chip_status in {"ACTIVE_DISTRIBUTION", "PARTIAL_DISTRIBUTION"} else 15, [mcap.get("market_cap_context_status"), chip_status or "missing"])
        add("SCENARIO_FAKE_VOLUME_BREAKOUT", 85 if volume.get("volume_quality_status") in {"VOLUME_FAKE_BREAKOUT_RISK", "VOLUME_DISTRIBUTION_PRESSURE"} and price.get("price_structure_status") == "PRICE_FAILED_BREAKOUT" else 20, [volume.get("volume_quality_status"), price.get("price_structure_status")])
        add("SCENARIO_COUNTERPARTY_WHALE_TRAP", 85 if cp_score >= 55 or chip_status == "TRANSFER_TO_COUNTERPARTY" else 15, [f"counterparty_pressure_score={cp_score}", chip_status or "missing"])
        return scores

    def _positive_scenario_scores(self, lifecycle: dict, price: dict, volume: dict, wallet: dict, chip: dict, mcap: dict, chip_summary: dict) -> list[dict]:
        rows = []
        def add(scenario: str, score: int, evidence: list[str], counter: list[str] | None = None):
            rows.append(self._scenario_row(scenario, score, evidence, counter or []))
        chip_status = chip_summary.get("chip_control_status")
        wallet_support = wallet.get("wallet_context_status") == "WALLET_CONTEXT_SUPPORTIVE"
        chip_support = chip.get("chip_context_status") in {"CHIP_CONTEXT_SUPPORTS_EXPANSION", "CHIP_CONTEXT_SUPPORTS_ACCUMULATION"}
        add("SCENARIO_ACCUMULATION", 70 if price.get("price_structure_status") == "PRICE_CONTROL_BOX" and chip_support else 30, [price.get("price_structure_status"), chip.get("chip_context_status")])
        add("SCENARIO_FIRST_EXPANSION", 72 if price.get("price_structure_status") == "PRICE_UPTREND_PUSH" and chip_support and wallet_support else 35, [price.get("price_structure_status"), chip.get("chip_context_status"), wallet.get("wallet_context_status")])
        add("SCENARIO_SECOND_STAGE_EXPANSION_CANDIDATE", 82 if price.get("price_structure_status") == "PRICE_BREAKOUT_PULLBACK" and chip_status in {"CONTROL_RETAINED", "CONTROL_WEAKENING"} and wallet_support else 40, [price.get("price_structure_status"), chip_status or "missing", wallet.get("wallet_context_status")])
        add("SCENARIO_REACCUMULATION", 78 if chip_status == "RE_ACCUMULATION" or lifecycle.get("market_lifecycle_status") == "LIFECYCLE_REACTIVATION" else 25, [chip_status or "missing", lifecycle.get("market_lifecycle_status")])
        return rows

    def _score_all_scenarios(self, risk: list[dict], positive: list[dict]) -> list[dict]:
        return sorted(risk + positive, key=lambda r: (r["score"], r["scenario"] in RISK_SCENARIOS), reverse=True)

    def _decide_primary(self, **ctx: Any) -> dict:
        scores = ctx["scores"]
        validation = ctx["validation"]
        missing = ctx["missing_fields"]
        best = scores[0] if scores else self._scenario_row("SCENARIO_UNKNOWN", 0, [], ["no_scores"])
        second = scores[1] if len(scores) > 1 else self._scenario_row("SCENARIO_UNKNOWN", 0, [], [])
        scenario = best["scenario"]
        if validation["errors"]:
            scenario_status = "SCENARIO_BLOCK"
        elif scenario in {"SCENARIO_EXIT_LIQUIDITY_TRAP", "SCENARIO_FAKE_VOLUME_BREAKOUT", "SCENARIO_COUNTERPARTY_WHALE_TRAP", "SCENARIO_TERMINAL_PUMP_DISTRIBUTION", "SCENARIO_DOWNTREND_DISTRIBUTION"} and best["score"] >= 70:
            scenario_status = "SCENARIO_TRAP_RISK" if "TRAP" in scenario or "FAKE" in scenario or "EXIT" in scenario else "SCENARIO_DISTRIBUTION_RISK"
        elif scenario == "SCENARIO_HIGH_DISTRIBUTION" and best["score"] >= 70:
            scenario_status = "SCENARIO_DISTRIBUTION_RISK"
        elif scenario == "SCENARIO_SECOND_STAGE_EXPANSION_CANDIDATE" and best["score"] >= 70:
            scenario_status = "SCENARIO_SECOND_STAGE_CANDIDATE"
        elif scenario in POSITIVE_SCENARIOS and best["score"] >= 65:
            scenario_status = "SCENARIO_ALLOW"
        elif missing:
            scenario_status = "SCENARIO_UNKNOWN"
        else:
            scenario_status = "SCENARIO_PAUSE"
        allowed = NEXT_STAGE if scenario_status in {"SCENARIO_ALLOW", "SCENARIO_SECOND_STAGE_CANDIDATE", "SCENARIO_PAUSE", "SCENARIO_UNKNOWN"} else "blocked"
        return {
            "phase": "phase_04_scenario_recognition",
            "token_address": ctx["token"],
            "token_symbol": ctx["symbol"],
            "snapshot_id": ctx["snapshot_id"],
            "snapshot_time": ctx["snapshot_time"],
            "primary_scenario": scenario,
            "secondary_scenario": second["scenario"],
            "scenario_confidence": min(100, int(best["score"])),
            "scenario_risk_level": "R3" if scenario in RISK_SCENARIOS and best["score"] >= 70 else "R2" if scenario in RISK_SCENARIOS else "R1",
            "scenario_status": scenario_status,
            "market_lifecycle_status": ctx["lifecycle"].get("market_lifecycle_status"),
            "price_structure_status": ctx["price"].get("price_structure_status"),
            "volume_quality_status": ctx["volume"].get("volume_quality_status"),
            "wallet_context_status": ctx["wallet_ctx"].get("wallet_context_status"),
            "chip_context_status": ctx["chip_ctx"].get("chip_context_status"),
            "market_cap_context_status": ctx["mcap"].get("market_cap_context_status"),
            "positive_evidence": best["positive_evidence"] or ["scenario_score_selected"],
            "negative_evidence": best["negative_evidence"],
            "counter_evidence": [],
            "risk_scenarios_detected": [r["scenario"] for r in scores if r["scenario"] in RISK_SCENARIOS and r["score"] >= 60],
            "hard_negative_triggered": False,
            "hard_negative_reasons": [],
            "blocked_positive_scenarios": [],
            "forced_next_checks": self._forced_next_checks(scenario_status, scenario),
            "missing_fields": missing,
            "allowed_next_stage": allowed,
            "handoff_status": "HANDOFF_READY" if allowed == NEXT_STAGE else "HANDOFF_BLOCKED",
            "block_reason": "input_contract_errors:" + ",".join(validation["errors"]) if validation["errors"] else "",
            "degrade_reason": "; ".join(validation["degrade_reasons"] + (["missing_fields:" + ",".join(missing)] if missing else [])),
        }

    def _counter_evidence(self, decision: Mapping[str, Any], chip: Mapping[str, Any], transfer: Mapping[str, Any], counterparty: Mapping[str, Any], price: Mapping[str, Any], volume: Mapping[str, Any], wallet: Mapping[str, Any], mcap: Mapping[str, Any]) -> dict:
        items = []
        primary = decision.get("primary_scenario")
        positive = primary in POSITIVE_SCENARIOS
        checks = [
            (positive and chip.get("chip_control_status") == "ACTIVE_DISTRIBUTION", "phase_03", "chip_control_status", "ACTIVE_DISTRIBUTION", "conflicts_with_positive_scenario"),
            (positive and (transfer.get("chip_transfer_status") == "CHIP_TRANSFER_TO_COUNTERPARTY"), "phase_03", "chip_transfer_status", "CHIP_TRANSFER_TO_COUNTERPARTY", "conflicts_with_expansion"),
            (positive and chip.get("chip_control_status") == "STRUCTURE_COLLAPSE", "phase_03", "chip_control_status", "STRUCTURE_COLLAPSE", "blocks_positive_scenario"),
            (positive and wallet.get("wallet_context_status") == "WALLET_CONTEXT_BLOCKING", "phase_02", "wallet_context_status", "WALLET_CONTEXT_BLOCKING", "wallet_structure_not_supportive"),
            (positive and mcap.get("market_cap_context_status") in {"MARKET_CONTEXT_OVEREXTENDED", "MARKET_CONTEXT_EXIT_LIQUIDITY"}, "phase_01", "market_cap_context_status", mcap.get("market_cap_context_status"), "late_entry_or_exit_liquidity_risk"),
            (positive and volume.get("volume_quality_status") in {"VOLUME_DISTRIBUTION_PRESSURE", "VOLUME_FAKE_BREAKOUT_RISK"}, "phase_01", "volume_quality_status", volume.get("volume_quality_status"), "volume_conflicts_with_positive_scenario"),
        ]
        for ok, source, field, value, reason in checks:
            if ok:
                items.append({"evidence_type": "counter_evidence", "source_phase": source, "source_file": "runtime_context", "field": field, "value": value, "conflict_with": primary, "severity": "HIGH", "reason": reason})
        return {"phase": "phase_04_scenario_recognition", "token_address": decision.get("token_address"), "snapshot_time": decision.get("snapshot_time"), "tested_primary_scenario": primary, "counter_evidence_items": items, "hard_negative_items": [], "scenario_invalidated": any(i["severity"] == "HIGH" for i in items), "scenario_degraded": bool(items), "final_counter_evidence_level": "CE3" if items else "CE0"}

    def _hard_negative_checklist(self, decision: Mapping[str, Any], chip: Mapping[str, Any], transfer: Mapping[str, Any], counterparty: Mapping[str, Any], price: Mapping[str, Any], volume: Mapping[str, Any], wallet: Mapping[str, Any]) -> dict:
        reasons = []
        primary = decision.get("primary_scenario")
        if primary in {"SCENARIO_HIGH_DISTRIBUTION", "SCENARIO_DOWNTREND_DISTRIBUTION", "SCENARIO_EXIT_LIQUIDITY_TRAP", "SCENARIO_TERMINAL_PUMP_DISTRIBUTION", "SCENARIO_FAKE_VOLUME_BREAKOUT", "SCENARIO_COUNTERPARTY_WHALE_TRAP"} and decision.get("scenario_confidence", 0) >= 70:
            reasons.append(f"risk_primary_scenario:{primary}")
        if chip.get("chip_control_status") == "STRUCTURE_COLLAPSE":
            reasons.append("chip_control_status=STRUCTURE_COLLAPSE")
        if transfer.get("chip_transfer_status") == "CHIP_TRANSFER_TO_COUNTERPARTY" and self._safe_float(counterparty.get("counterparty_pressure_score")) >= 55:
            reasons.append("chip_transfer_to_counterparty_with_high_pressure")
        if wallet.get("wallet_context_status") == "WALLET_CONTEXT_BLOCKING":
            reasons.append("wallet_context_blocking")
        if volume.get("volume_quality_status") == "VOLUME_FAKE_BREAKOUT_RISK" and price.get("price_structure_status") == "PRICE_FAILED_BREAKOUT":
            reasons.append("fake_volume_failed_breakout")
        status = "SCENARIO_BLOCK" if reasons and any("STRUCTURE_COLLAPSE" in r or "blocking" in r for r in reasons) else "SCENARIO_REVIEW_ONLY" if reasons else decision.get("scenario_status")
        return {"phase": "phase_04_scenario_recognition", "token_address": decision.get("token_address"), "hard_negative_triggered": bool(reasons), "hard_negative_reasons": reasons, "scenario_status": status, "checked_rules": 10}

    def _write_outputs(self, **kw: Any) -> Dict[str, str]:
        dirs = kw["dirs"]
        artifacts: Dict[str, str] = {}
        json_items = {
            "market_lifecycle_context": (dirs["scenario_fact"] / "market_lifecycle_context.json", kw["lifecycle"]),
            "price_structure_state": (dirs["scenario_fact"] / "price_structure_state.json", kw["price"]),
            "volume_quality_state": (dirs["scenario_fact"] / "volume_quality_state.json", kw["volume"]),
            "wallet_scenario_context": (dirs["scenario_fact"] / "wallet_scenario_context.json", kw["wallet_ctx"]),
            "chip_scenario_context": (dirs["scenario_fact"] / "chip_scenario_context.json", kw["chip_ctx"]),
            "market_cap_scenario_context": (dirs["scenario_fact"] / "market_cap_scenario_context.json", kw["mcap"]),
            "scenario_scores": (dirs["scenario_scores"] / "scenario_scores.json", {"phase": "phase_04_scenario_recognition", "token_address": kw["token"], "scenarios": kw["scores"]}),
            "risk_scenario_scores": (dirs["scenario_scores"] / "risk_scenario_scores.json", {"phase": "phase_04_scenario_recognition", "token_address": kw["token"], "scenarios": kw["risk_scores"]}),
            "positive_scenario_scores": (dirs["scenario_scores"] / "positive_scenario_scores.json", {"phase": "phase_04_scenario_recognition", "token_address": kw["token"], "scenarios": kw["positive_scores"]}),
            "primary_scenario": (dirs["scenario_decision"] / "primary_scenario.json", kw["decision"]),
            "secondary_scenario": (dirs["scenario_decision"] / "secondary_scenario.json", {"phase": "phase_04_scenario_recognition", "token_address": kw["token"], "secondary_scenario": kw["decision"].get("secondary_scenario")}),
            "scenario_counter_evidence": (dirs["scenario_decision"] / "scenario_counter_evidence.json", kw["counter"]),
            "scenario_hard_negative_checklist": (dirs["scenario_decision"] / "scenario_hard_negative_checklist.json", kw["hard"]),
            "scenario_transition_log": (dirs["scenario_decision"] / "scenario_transition_log.json", {"phase": "phase_04_scenario_recognition", "token_address": kw["token"], "transition": [kw["decision"].get("primary_scenario"), kw["decision"].get("scenario_status")]}),
        }
        for key, (path, obj) in json_items.items():
            path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
            artifacts[key] = str(path)
        self._write_csv(dirs["scenario_fact"] / "price_structure_segments.csv", [{"segment_id": "S1", "price_structure_status": kw["price"].get("price_structure_status")}], ["segment_id", "price_structure_status"])
        artifacts["price_structure_segments"] = str(dirs["scenario_fact"] / "price_structure_segments.csv")
        self._write_csv(dirs["scenario_scores"] / "scenario_score_matrix.csv", kw["scores"], ["scenario", "score", "confidence", "risk_level", "reason"])
        artifacts["scenario_score_matrix"] = str(dirs["scenario_scores"] / "scenario_score_matrix.csv")
        report = dirs["reports"] / "scenario_report.md"
        report.write_text(self._report(kw["decision"], artifacts), encoding="utf-8")
        artifacts["scenario_report"] = str(report)
        handoff = self._build_handoff(kw["decision"], artifacts, dirs)
        hp = dirs["handoff"] / "phase_04_handoff_packet.json"
        hp.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["handoff_packet"] = str(hp)
        missing = dirs["audit"] / "missing_fields_report.md"
        missing.write_text("# Phase 04 Missing Fields\n\n" + "\n".join(f"- {m}" for m in (kw["decision"].get("missing_fields") or ["none"])), encoding="utf-8")
        artifacts["missing_fields_report"] = str(missing)
        outval = dirs["audit"] / "output_validation_report.json"
        required = list(artifacts.values())
        miss = [p for p in required if not Path(p).exists()]
        outval.write_text(json.dumps({"status": "PASS" if not miss else "FAIL", "checked_files": required, "missing_files": miss}, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["output_validation_report"] = str(outval)
        hval = dirs["audit"] / "handoff_validation_report.json"
        hmiss = [k for k, v in handoff.get("handoff_files", {}).items() if not Path(v).exists()]
        hval.write_text(json.dumps({"status": "PASS" if not hmiss and handoff.get("handoff_status") in {"HANDOFF_READY", "HANDOFF_BLOCKED"} else "FAIL", "missing_handoff_files": hmiss, "next_stage": handoff.get("allowed_next_stage")}, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["handoff_validation_report"] = str(hval)
        gaps = dirs["audit"] / "gaps.md"
        gaps.write_text(self._gaps(kw["decision"], kw["validation"]), encoding="utf-8")
        artifacts["gaps"] = str(gaps)
        audit = dirs["audit"] / "phase_04_audit_report.md"
        audit.write_text(self._audit(kw["phase03"], kw["decision"], artifacts, kw["validation"]), encoding="utf-8")
        artifacts["audit_report"] = str(audit)
        return artifacts

    def _build_handoff(self, decision: Mapping[str, Any], artifacts: Mapping[str, str], dirs: Mapping[str, Path]) -> dict:
        return {
            "phase": "phase_04_scenario_recognition",
            "token_address": decision.get("token_address"),
            "token_symbol": decision.get("token_symbol"),
            "snapshot_id": decision.get("snapshot_id"),
            "snapshot_time": decision.get("snapshot_time"),
            "scenario_status": decision.get("scenario_status"),
            "primary_scenario": decision.get("primary_scenario"),
            "secondary_scenario": decision.get("secondary_scenario"),
            "scenario_confidence": decision.get("scenario_confidence"),
            "scenario_risk_level": decision.get("scenario_risk_level"),
            "handoff_files": {
                "primary_scenario": artifacts["primary_scenario"],
                "scenario_scores": artifacts["scenario_scores"],
                "scenario_counter_evidence": artifacts["scenario_counter_evidence"],
                "scenario_hard_negative_checklist": artifacts["scenario_hard_negative_checklist"],
                "scenario_report": artifacts["scenario_report"],
            },
            "phase_05_required_context": {
                "requires_avwap_completion_check": True,
                "requires_poc_context_check": True,
                "requires_failure_test_check": True,
                "requires_fatigue_filter": True,
                "requires_position_overextension_check": True,
                "blocked_position_confirmation": decision.get("scenario_status") in {"SCENARIO_BLOCK", "SCENARIO_REVIEW_ONLY", "SCENARIO_DISTRIBUTION_RISK", "SCENARIO_TRAP_RISK"},
                "forced_position_risk_checks": decision.get("forced_next_checks", []),
            },
            "blocked_positive_scenarios": decision.get("blocked_positive_scenarios", []),
            "forced_next_checks": decision.get("forced_next_checks", []),
            "allowed_next_stage": decision.get("allowed_next_stage"),
            "handoff_status": decision.get("handoff_status"),
            "block_reason": decision.get("block_reason"),
            "degrade_reason": decision.get("degrade_reason"),
            "audit_file": str(dirs["audit"] / "phase_04_audit_report.md"),
        }

    def _scenario_row(self, scenario: str, score: int, positive: list[Any], negative: list[Any]) -> dict:
        return {"scenario": scenario, "score": max(0, min(100, int(score))), "confidence": max(0, min(100, int(score))), "risk_level": "R3" if scenario in RISK_SCENARIOS and score >= 70 else "R1", "positive_evidence": [str(x) for x in positive if x], "negative_evidence": [str(x) for x in negative if x], "counter_evidence": [str(x) for x in negative if x], "hard_negative_triggered": scenario in RISK_SCENARIOS and score >= 85, "reason": scenario}

    def _fact(self, token: str, key: str, status: str, pos: list[str], neg: list[str]) -> dict:
        return {"phase": "phase_04_scenario_recognition", "token_address": token, key: status, "positive_evidence": pos, "negative_evidence": neg, "counter_evidence": neg, "hard_negative_triggered": False, "missing_fields": []}

    def _forced_next_checks(self, scenario_status: str, scenario: str) -> list[str]:
        checks = []
        if scenario_status == "SCENARIO_SECOND_STAGE_CANDIDATE" or scenario == "SCENARIO_SECOND_STAGE_EXPANSION_CANDIDATE":
            checks += ["avwap_completion_check", "poc_context_check", "failure_test_check", "fatigue_filter"]
        if scenario in RISK_SCENARIOS:
            checks += ["block_positive_position_confirmation", "review_risk_scene_only"]
        return checks

    def _write_csv(self, path: Path, rows: list[dict], default_fields: list[str]) -> None:
        fields = []
        for r in rows:
            for k in r:
                if k not in fields:
                    fields.append(k)
        if not fields:
            fields = default_fields
        with path.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    def _report(self, s: Mapping[str, Any], artifacts: Mapping[str, str]) -> str:
        return "\n".join([
            "# Phase 04 Scenario Recognition Report",
            "",
            f"- primary_scenario: {s.get('primary_scenario')}",
            f"- secondary_scenario: {s.get('secondary_scenario')}",
            f"- scenario_status: {s.get('scenario_status')}",
            f"- scenario_confidence: {s.get('scenario_confidence')}",
            f"- hard_negative_triggered: {s.get('hard_negative_triggered')}",
            "",
            "## Positive Evidence",
            *(f"- {x}" for x in s.get("positive_evidence", [])),
            "",
            "## Counter Evidence",
            *(f"- {x}" for x in s.get("counter_evidence", [])),
            "",
            "## Missing Fields",
            *(f"- {x}" for x in (s.get("missing_fields") or ["none"])),
            "",
            "## Handoff",
            f"- next_stage: {s.get('allowed_next_stage')}",
        ]) + "\n"

    def _audit(self, phase03: Mapping[str, Any], s: Mapping[str, Any], artifacts: Mapping[str, str], validation: Mapping[str, Any]) -> str:
        lines = [
            "# Phase 04 Scenario Recognition Controller Audit",
            "",
            f"- phase: {PHASE_ID}",
            f"- upstream_chip_control_status: {phase03.get('chip_control_status')}",
            f"- primary_scenario: {s.get('primary_scenario')}",
            f"- scenario_status: {s.get('scenario_status')}",
            f"- handoff_status: {s.get('handoff_status')}",
            f"- hard_negative: {s.get('hard_negative_triggered')}",
            f"- validation_errors: {validation.get('errors')}",
            "",
            "## 已调用 Atomic Skill",
            "- market_lifecycle_classifier_skill",
            "- price_structure_classifier_skill",
            "- volume_quality_classifier_skill",
            "- wallet_scenario_context_builder_skill",
            "- chip_scenario_context_builder_skill",
            "- market_cap_scenario_context_builder_skill",
            "- risk_scenario_detector_skill",
            "- positive_scenario_detector_skill",
            "- scenario_score_engine_skill",
            "- scenario_counter_evidence_checker_skill",
            "- scenario_hard_negative_checker_skill",
            "- primary_scenario_decision_writer_skill",
            "- phase_04_handoff_writer_skill",
            "",
            "## 输出文件",
        ]
        lines += [f"- {k}: {v}" for k, v in artifacts.items()]
        lines += ["", "## Missing 字段"] + [f"- {m}" for m in (s.get("missing_fields") or ["none"])]
        lines += ["", "## 反证 / 硬否决", f"- counter_evidence: {s.get('counter_evidence')}", f"- hard_negative_reasons: {s.get('hard_negative_reasons')}", "", "## 下游交接", f"- next_stage: {NEXT_STAGE}", f"- handoff_packet: {artifacts.get('handoff_packet')}"]
        return "\n".join(lines) + "\n"

    def _gaps(self, s: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
        gaps = []
        if s.get("missing_fields"):
            gaps.append("missing_fields_require_upstream_refresh:" + ",".join(s.get("missing_fields")))
        if validation.get("degrade_reasons"):
            gaps.append("degraded_optional_inputs:" + ",".join(validation.get("degrade_reasons")))
        if s.get("scenario_status") == "SCENARIO_UNKNOWN":
            gaps.append("insufficient_scenario_evidence")
        if not gaps:
            gaps.append("none")
        return "# Phase 04 Gaps\n\n" + "\n".join(f"- {g}" for g in gaps) + "\n"

    def _safe_float(self, value: Any) -> float:
        try:
            if value in (None, "", "missing"):
                return 0.0
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
