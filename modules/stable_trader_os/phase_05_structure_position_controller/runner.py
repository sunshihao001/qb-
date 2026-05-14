from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping

PHASE_ID = "phase_05_structure_position_controller"
PHASE_NAME = "phase_05_structure_position"
NEXT_STAGE = "phase_06_strategy_gate_controller"
UPSTREAM_BLOCK_STATUSES = {"SCENARIO_BLOCK", "SCENARIO_REVIEW_ONLY", "SCENARIO_DISTRIBUTION_RISK", "SCENARIO_TRAP_RISK"}


class Phase05StructurePositionController:
    """HER Phase05 controller: scenario handoff -> structure position confirmation.

    Paper-only/read-only layer. It checks AVWAP/POC/Failure Test/Fatigue and
    cannot repair upstream scenario hard negatives.
    """

    def run(self, *, phase04_handoff_file: str | Path, output_dir: str | Path) -> Dict[str, Any]:
        handoff_file = Path(phase04_handoff_file)
        out = Path(output_dir)
        phase_dir = out / "05_structure_position"
        dirs = self._ensure_dirs(phase_dir)

        phase04 = self._read_json(handoff_file)
        validation = self._validate_phase04_handoff(phase04, handoff_file.parent)
        refs = self._resolve_refs(phase04, handoff_file.parent)
        token = str(phase04.get("token_address") or "missing")
        symbol = str(phase04.get("token_symbol") or "")
        snapshot_id = str(phase04.get("snapshot_id") or "missing")
        snapshot_time = self._now()

        primary = self._read_json(refs.get("primary_scenario"))
        scenario_counter = self._read_json(refs.get("scenario_counter_evidence"))
        scenario_hard = self._read_json(refs.get("scenario_hard_negative_checklist"))
        market = self._read_json(refs.get("token_market_context"))
        chip = self._read_json(refs.get("chip_control_summary"))
        wallet = self._read_json(refs.get("wallet_structure_decision"))
        klines = self._read_csv(refs.get("kline_normalized"))

        missing_fields = sorted(set(validation["missing_fields"] + self._data_missing_fields(klines, market)))
        constraints = self._scenario_position_constraints(token, phase04, primary, scenario_hard)
        profile_rows, poc = self._poc_context(token, klines)
        anchor = self._avwap_anchor_context(token, klines, market)
        avwap = self._avwap_acceptance(token, klines, anchor)
        retracement = self._retracement_context(token, klines)
        volume = self._position_volume_confirmation(token, klines)
        adx = self._adx_noise_filter(token, klines, volume)
        failure = self._failure_test_result(token, klines, anchor, poc, adx)
        fatigue = self._fatigue_filter_result(token, klines, volume, chip)
        overextension = self._position_overextension_check(token, klines, market, anchor)
        gate = self._avwap_completion_gate(token, avwap, failure, poc, volume, adx, fatigue, overextension, constraints)
        hard = self._hard_negative_checklist(phase04, primary, scenario_hard, gate, fatigue, overextension, validation, missing_fields)
        decision = self._decision(
            token=token,
            symbol=symbol,
            snapshot_id=snapshot_id,
            snapshot_time=snapshot_time,
            phase04=phase04,
            primary=primary,
            counter=scenario_counter,
            hard=hard,
            constraints=constraints,
            poc=poc,
            avwap=avwap,
            failure=failure,
            gate=gate,
            fatigue=fatigue,
            overextension=overextension,
            missing_fields=missing_fields,
            validation=validation,
        )
        artifacts = self._write_outputs(
            dirs=dirs,
            token=token,
            constraints=constraints,
            profile_rows=profile_rows,
            poc=poc,
            anchor=anchor,
            avwap=avwap,
            retracement=retracement,
            volume=volume,
            adx=adx,
            failure=failure,
            gate=gate,
            fatigue=fatigue,
            overextension=overextension,
            hard=hard,
            decision=decision,
            phase04=phase04,
            validation=validation,
        )
        manifest = phase_dir / "run_manifest.json"
        manifest.write_text(json.dumps({"phase": PHASE_ID, "phase_status": decision.get("completion_status"), "artifacts": artifacts}, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["run_manifest"] = str(manifest)
        return {"phase": PHASE_ID, "phase_status": decision.get("completion_status"), "artifacts": artifacts}

    def _ensure_dirs(self, phase_dir: Path) -> Dict[str, Path]:
        dirs = {"phase": phase_dir, "position_fact": phase_dir / "position_fact", "position_decision": phase_dir / "position_decision", "handoff": phase_dir / "handoff", "reports": phase_dir / "reports", "audit": phase_dir / "audit"}
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

    def _validate_phase04_handoff(self, packet: Mapping[str, Any], base: Path) -> Dict[str, Any]:
        errors: list[str] = []
        degrade: list[str] = []
        missing: list[str] = []
        for field in ["phase", "token_address", "snapshot_id", "scenario_status", "primary_scenario", "handoff_files"]:
            if field not in packet:
                errors.append(f"missing_handoff_field:{field}")
                missing.append(field)
        if packet.get("allowed_next_stage") not in {PHASE_ID, "phase_05_structure_position_controller", NEXT_STAGE, "blocked", "review_only", None}:
            degrade.append("unexpected_allowed_next_stage")
        refs = packet.get("handoff_files", {}) or {}
        for name in ["primary_scenario", "scenario_counter_evidence", "scenario_hard_negative_checklist", "kline_normalized", "token_market_context"]:
            ref = refs.get(name)
            if not ref:
                errors.append(f"missing_required_ref:{name}")
                missing.append(name)
            else:
                p = Path(ref) if Path(ref).is_absolute() else base / ref
                if not p.exists():
                    errors.append(f"missing_required_file:{name}")
                    missing.append(name)
        for name in ["scenario_scores", "chip_control_summary", "wallet_structure_decision"]:
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
            except (TypeError, ValueError):
                continue
        return default

    def _data_missing_fields(self, klines: list[dict], market: Mapping[str, Any]) -> list[str]:
        missing = []
        if not klines:
            missing.append("kline_normalized")
        else:
            last = klines[-1]
            for field in ["close", "high", "low", "volume_usd"]:
                if field not in last:
                    missing.append(f"kline.{field}")
        for field in ["discovery_market_cap_usd", "current_market_cap_usd"]:
            if field not in market:
                missing.append(f"token_market_context.{field}")
        return missing

    def _scenario_position_constraints(self, token: str, phase04: Mapping[str, Any], primary: Mapping[str, Any], hard: Mapping[str, Any]) -> dict:
        status = phase04.get("scenario_status") or primary.get("scenario_status")
        upstream_blocked = status in UPSTREAM_BLOCK_STATUSES or phase04.get("handoff_status") == "HANDOFF_BLOCKED" or bool(hard.get("hard_negative_triggered"))
        return {"phase": PHASE_NAME, "token_address": token, "scenario_status": status, "primary_scenario": phase04.get("primary_scenario") or primary.get("primary_scenario"), "upstream_position_blocked": upstream_blocked, "required_checks": phase04.get("phase_05_required_context", {}), "positive_evidence": ["phase04_handoff_loaded"] if phase04 else [], "counter_evidence": ["upstream_scenario_blocks_position"] if upstream_blocked else [], "hard_negative_triggered": upstream_blocked, "missing_fields": []}

    def _prices(self, klines: list[dict]) -> list[float]:
        return [self._num(r, "close") for r in klines if self._num(r, "close") > 0]

    def _poc_context(self, token: str, klines: list[dict]) -> tuple[list[dict], dict]:
        rows = []
        for idx, row in enumerate(klines):
            close = self._num(row, "close")
            vol = self._num(row, "volume_usd")
            rows.append({"bucket_id": idx + 1, "price": close, "volume_usd": vol})
        poc_price = max(rows, key=lambda r: r["volume_usd"], default={"price": 0}).get("price", 0)
        current = rows[-1]["price"] if rows else 0
        support = bool(poc_price and current >= poc_price * 0.92)
        return rows, {"phase": PHASE_NAME, "token_address": token, "poc_price": poc_price, "current_price": current, "poc_support_status": "POC_SUPPORT" if support else "POC_LOST_OR_UNKNOWN", "positive_evidence": ["current_price_near_or_above_poc"] if support else [], "counter_evidence": [] if support else ["current_price_below_poc_band"], "hard_negative_triggered": False, "missing_fields": [] if rows else ["kline_normalized"]}

    def _avwap_anchor_context(self, token: str, klines: list[dict], market: Mapping[str, Any]) -> dict:
        prices = self._prices(klines)
        anchor = prices[0] if prices else 0
        avwap = sum(prices) / len(prices) if prices else 0
        return {"phase": PHASE_NAME, "token_address": token, "anchor_type": "launch_or_local_base", "anchor_price": anchor, "avwap_value": avwap, "market_cap_context": market.get("current_market_cap_usd", "missing"), "missing_fields": [] if prices else ["kline.close"]}

    def _avwap_acceptance(self, token: str, klines: list[dict], anchor: Mapping[str, Any]) -> dict:
        prices = self._prices(klines)
        avwap = self._num(anchor, "avwap_value")
        current = prices[-1] if prices else 0
        recent = prices[-3:] if len(prices) >= 3 else prices
        accepted = bool(recent and avwap and sum(1 for p in recent if p >= avwap * 0.96) >= max(1, len(recent) - 1) and current >= avwap * 0.98)
        return {"phase": PHASE_NAME, "token_address": token, "avwap_value": avwap, "current_price": current, "avwap_acceptance_status": "AVWAP_ACCEPTED" if accepted else "AVWAP_NOT_ACCEPTED", "avwap_acceptance_pass": accepted, "positive_evidence": ["recent_closes_accept_avwap"] if accepted else [], "counter_evidence": [] if accepted else ["recent_closes_do_not_accept_avwap"], "missing_fields": [] if prices else ["kline.close"]}

    def _retracement_context(self, token: str, klines: list[dict]) -> dict:
        prices = self._prices(klines)
        if not prices:
            return {"phase": PHASE_NAME, "token_address": token, "retracement_status": "RETRACEMENT_UNKNOWN", "retracement_pct": "missing", "missing_fields": ["kline.close"]}
        high = max(prices)
        low_after = min(prices[prices.index(high):]) if high in prices else min(prices)
        pct = ((high - low_after) / high * 100) if high else 0
        return {"phase": PHASE_NAME, "token_address": token, "swing_high": high, "post_high_low": low_after, "retracement_pct": round(pct, 2), "retracement_status": "RETRACEMENT_HEALTHY" if 15 <= pct <= 45 else "RETRACEMENT_SHALLOW_OR_EXTREME", "missing_fields": []}

    def _position_volume_confirmation(self, token: str, klines: list[dict]) -> dict:
        vols = [self._num(r, "volume_usd") for r in klines]
        if len(vols) < 3:
            return {"phase": PHASE_NAME, "token_address": token, "volume_confirmation_status": "VOLUME_UNKNOWN", "volume_confirmation_pass": False, "missing_fields": ["kline.volume_usd"]}
        prev = sum(vols[:-2]) / max(1, len(vols[:-2]))
        recent = sum(vols[-2:]) / 2
        passed = recent >= prev * 1.05
        return {"phase": PHASE_NAME, "token_address": token, "recent_volume_avg": round(recent, 4), "prior_volume_avg": round(prev, 4), "volume_confirmation_status": "VOLUME_CONFIRMED" if passed else "VOLUME_NOT_CONFIRMED", "volume_confirmation_pass": passed, "positive_evidence": ["recent_volume_confirms_position"] if passed else [], "counter_evidence": [] if passed else ["recent_volume_not_confirming"], "missing_fields": []}

    def _adx_noise_filter(self, token: str, klines: list[dict], volume: Mapping[str, Any]) -> dict:
        prices = self._prices(klines)
        if len(prices) < 4:
            return {"phase": PHASE_NAME, "token_address": token, "adx_noise_status": "ADX_UNKNOWN", "adx_noise_rejected": False, "missing_fields": ["kline.close"]}
        changes = [abs(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices)) if prices[i-1]]
        direction = abs(prices[-1] - prices[0]) / prices[0] if prices[0] else 0
        churn = sum(changes) / max(direction, 0.01)
        # Phase05 不能把“ADX/成交量很强”单独当作 Completion。若价格来回扫动、
        # 净方向不足，即使近期成交放大，也属于趋势噪声/诱导确认，必须交给
        # AVWAP + Failure Test 去否定。
        directional_close = direction >= 0.14
        rejected = churn >= 2.6 and not directional_close
        return {"phase": PHASE_NAME, "token_address": token, "noise_churn_ratio": round(churn, 4), "directional_close_ratio": round(direction, 4), "adx_noise_status": "ADX_NOISE_REJECTED" if rejected else "ADX_NOISE_ACCEPTABLE", "adx_noise_rejected": rejected, "positive_evidence": [] if rejected else ["noise_filter_not_blocking"], "counter_evidence": ["high_churn_low_direction_noise"] if rejected else [], "missing_fields": []}

    def _failure_test_result(self, token: str, klines: list[dict], anchor: Mapping[str, Any], poc: Mapping[str, Any], adx: Mapping[str, Any]) -> dict:
        prices = self._prices(klines)
        lows = [self._num(r, "low") for r in klines if self._num(r, "low") > 0]
        if len(prices) < 3:
            passed = False
            reason = "insufficient_kline"
        else:
            avwap = self._num(anchor, "avwap_value")
            recent_low = min(lows[-3:]) if lows else min(prices[-3:])
            current = prices[-1]
            passed = bool(avwap and recent_low <= avwap * 1.05 and current >= avwap * 1.03 and not adx.get("adx_noise_rejected"))
            reason = "sweep_recovery_above_avwap" if passed else "no_recovery_or_noise_rejected"
        return {"phase": PHASE_NAME, "token_address": token, "failure_test_status": "FAILURE_TEST_PASS" if passed else "FAILURE_TEST_FAIL", "failure_test_pass": passed, "reason": reason, "positive_evidence": [reason] if passed else [], "counter_evidence": [] if passed else [reason], "missing_fields": [] if prices else ["kline.close"]}

    def _fatigue_filter_result(self, token: str, klines: list[dict], volume: Mapping[str, Any], chip: Mapping[str, Any]) -> dict:
        prices = self._prices(klines)
        vols = [self._num(r, "volume_usd") for r in klines]
        fatigue = False
        reasons: list[str] = []
        if len(prices) >= 5:
            flat = abs(prices[-1] - prices[-4]) / prices[-4] < 0.04 if prices[-4] else False
            vol_down = vols[-1] < (sum(vols[-4:-1]) / 3) * 0.75 if len(vols) >= 4 else False
            if flat and vol_down:
                fatigue = True
                reasons.append("flat_price_with_declining_volume")
        if chip.get("chip_control_status") in {"ACTIVE_DISTRIBUTION", "STRUCTURE_COLLAPSE"}:
            fatigue = True
            reasons.append("chip_control_conflicts_with_position")
        return {"phase": PHASE_NAME, "token_address": token, "fatigue_status": "FATIGUE_BLOCK" if fatigue else "FATIGUE_CLEAR", "fatigue_block": fatigue, "hard_negative_triggered": fatigue, "positive_evidence": [] if fatigue else ["fatigue_filter_clear"], "counter_evidence": reasons, "hard_negative_reasons": reasons, "missing_fields": []}

    def _position_overextension_check(self, token: str, klines: list[dict], market: Mapping[str, Any], anchor: Mapping[str, Any]) -> dict:
        prices = self._prices(klines)
        current = prices[-1] if prices else 0
        avwap = self._num(anchor, "avwap_value")
        discovery = self._num(market, "discovery_market_cap_usd")
        current_cap = self._num(market, "current_market_cap_usd")
        price_ext = (current / avwap) if avwap else 0
        cap_ext = (current_cap / discovery) if discovery else 0
        swing_high = max(prices) if prices else 0
        swing_low = min(prices) if prices else 0
        swing_ext = (current / swing_low) if swing_low else 0
        late_vertical_ext = 0.0
        if len(prices) >= 3 and prices[-3] > 0:
            late_vertical_ext = current / prices[-3]
        # Phase05 过度延伸不仅看 current/AVWAP；强拉离开最近回调低点、
        # late vertical expansion 也会把“位置确认”降级为追高风险。
        over = price_ext >= 1.75 or cap_ext >= 7.0 or swing_ext >= 2.2 or late_vertical_ext >= 2.2
        chasing = not over and (price_ext >= 1.55 or swing_ext >= 1.9 or late_vertical_ext >= 1.9)
        status = "POSITION_OVEREXTENDED" if over else "POSITION_CHASING_RISK" if chasing else "POSITION_VALID_RANGE"
        return {"phase": PHASE_NAME, "token_address": token, "position_extension_status": status, "position_overextended": over or chasing, "current_to_avwap_ratio": round(price_ext, 4), "market_cap_extension_ratio": round(cap_ext, 4), "current_to_swing_low_ratio": round(swing_ext, 4), "late_vertical_extension_ratio": round(late_vertical_ext, 4), "positive_evidence": [] if over or chasing else ["position_not_overextended"], "counter_evidence": ["price_or_market_cap_overextended"] if over else ["position_chasing_risk"] if chasing else [], "hard_negative_triggered": over or chasing, "missing_fields": [] if prices else ["kline.close"]}

    def _avwap_completion_gate(self, token: str, avwap: Mapping[str, Any], failure: Mapping[str, Any], poc: Mapping[str, Any], volume: Mapping[str, Any], adx: Mapping[str, Any], fatigue: Mapping[str, Any], over: Mapping[str, Any], constraints: Mapping[str, Any]) -> dict:
        checks = {
            "avwap_acceptance_pass": bool(avwap.get("avwap_acceptance_pass")),
            "failure_test_pass": bool(failure.get("failure_test_pass")),
            "poc_support_pass": poc.get("poc_support_status") == "POC_SUPPORT",
            "volume_confirmation_pass": bool(volume.get("volume_confirmation_pass")),
        }
        passed_count = sum(1 for v in checks.values() if v)
        blocked = constraints.get("upstream_position_blocked") or adx.get("adx_noise_rejected") or fatigue.get("fatigue_block") or over.get("position_overextended")
        completion = "COMPLETION_PASS" if passed_count >= 2 and not blocked else "COMPLETION_BLOCKED" if constraints.get("upstream_position_blocked") else "FATIGUE_BLOCK" if fatigue.get("fatigue_block") else "COMPLETION_FAIL" if over.get("position_overextended") else "COMPLETION_WAIT"
        return {"phase": PHASE_NAME, "token_address": token, "completion_status": completion, "completion_passed_count": passed_count, **checks, "adx_noise_rejected": bool(adx.get("adx_noise_rejected")), "blocked_by_upstream": bool(constraints.get("upstream_position_blocked")), "positive_evidence": [k for k, v in checks.items() if v], "counter_evidence": [k for k, v in checks.items() if not v] + (["adx_noise_rejected"] if adx.get("adx_noise_rejected") else []), "missing_fields": []}

    def _hard_negative_checklist(self, phase04: Mapping[str, Any], primary: Mapping[str, Any], scenario_hard: Mapping[str, Any], gate: Mapping[str, Any], fatigue: Mapping[str, Any], over: Mapping[str, Any], validation: Mapping[str, Any], missing: list[str]) -> dict:
        reasons: list[str] = []
        status = phase04.get("scenario_status") or primary.get("scenario_status")
        if status in UPSTREAM_BLOCK_STATUSES or phase04.get("handoff_status") == "HANDOFF_BLOCKED":
            reasons.append(f"phase04_upstream_block:{status}")
        if scenario_hard.get("hard_negative_triggered"):
            reasons.extend([f"phase04_hard_negative:{r}" for r in scenario_hard.get("hard_negative_reasons", [])] or ["phase04_hard_negative"])
        if validation.get("errors"):
            reasons.append("input_contract_errors:" + ",".join(validation.get("errors", [])))
        if fatigue.get("fatigue_block"):
            reasons.extend(fatigue.get("hard_negative_reasons", []) or ["fatigue_block"])
        if over.get("position_overextended"):
            reasons.append("position_overextended")
        if "kline_normalized" in missing:
            reasons.append("missing_required_kline")
        return {"phase": PHASE_NAME, "hard_negative_triggered": bool(reasons), "hard_negative_reasons": reasons, "checked_rules": 8}

    def _decision(self, **kw: Any) -> dict:
        gate = kw["gate"]
        hard = kw["hard"]
        over = kw["overextension"]
        completion = "COMPLETION_BLOCKED" if hard.get("hard_negative_triggered") and gate.get("blocked_by_upstream") else gate.get("completion_status")
        if hard.get("hard_negative_triggered") and over.get("position_overextended"):
            completion = "COMPLETION_FAIL"
        if completion == "COMPLETION_PASS":
            position_status = "POSITION_VALID"
            allowed = NEXT_STAGE
        elif over.get("position_overextended"):
            position_status = "POSITION_OVEREXTENDED"
            allowed = "blocked"
        elif completion in {"COMPLETION_BLOCKED", "COMPLETION_FAIL", "FATIGUE_BLOCK"}:
            position_status = "POSITION_UNKNOWN" if completion == "COMPLETION_BLOCKED" else "POSITION_CHASING_RISK"
            allowed = "blocked"
        else:
            position_status = "POSITION_UNKNOWN"
            allowed = "review_only"
        return {"phase": PHASE_NAME, "token_address": kw["token"], "token_symbol": kw["symbol"], "snapshot_id": kw["snapshot_id"], "snapshot_time": kw["snapshot_time"], "upstream_scenario_status": kw["phase04"].get("scenario_status"), "primary_scenario": kw["phase04"].get("primary_scenario") or kw["primary"].get("primary_scenario"), "completion_status": completion, "structure_position_status": position_status, "position_extension_status": over.get("position_extension_status"), "completion_passed_count": gate.get("completion_passed_count"), "positive_evidence": gate.get("positive_evidence", []) + kw["poc"].get("positive_evidence", []) + kw["avwap"].get("positive_evidence", []) + kw["failure"].get("positive_evidence", []), "negative_evidence": gate.get("counter_evidence", []), "counter_evidence": gate.get("counter_evidence", []) + kw["counter"].get("counter_evidence_items", []), "hard_negative_triggered": hard.get("hard_negative_triggered"), "hard_negative_reasons": hard.get("hard_negative_reasons", []), "missing_fields": kw["missing_fields"], "confidence_level": "E4" if completion == "COMPLETION_PASS" else "E2", "risk_level": "R1" if completion == "COMPLETION_PASS" else "R3", "allowed_next_stage": allowed, "handoff_status": "HANDOFF_READY" if allowed == NEXT_STAGE else "HANDOFF_BLOCKED", "block_reason": "; ".join(hard.get("hard_negative_reasons", [])) if allowed != NEXT_STAGE else "", "degrade_reason": "; ".join(kw["validation"].get("degrade_reasons", []) + (["missing_fields:" + ",".join(kw["missing_fields"])] if kw["missing_fields"] else []))}

    def _write_outputs(self, **kw: Any) -> Dict[str, str]:
        dirs = kw["dirs"]
        artifacts: Dict[str, str] = {}
        json_items = {
            "scenario_position_constraints": (dirs["position_fact"] / "scenario_position_constraints.json", kw["constraints"]),
            "poc_context": (dirs["position_fact"] / "poc_context.json", kw["poc"]),
            "avwap_anchor_context": (dirs["position_fact"] / "avwap_anchor_context.json", kw["anchor"]),
            "avwap_acceptance": (dirs["position_fact"] / "avwap_acceptance.json", kw["avwap"]),
            "retracement_context": (dirs["position_fact"] / "retracement_context.json", kw["retracement"]),
            "position_volume_confirmation": (dirs["position_fact"] / "position_volume_confirmation.json", kw["volume"]),
            "adx_noise_filter": (dirs["position_fact"] / "adx_noise_filter.json", kw["adx"]),
            "failure_test_result": (dirs["position_fact"] / "failure_test_result.json", kw["failure"]),
            "avwap_completion_gate": (dirs["position_decision"] / "avwap_completion_gate.json", kw["gate"]),
            "fatigue_filter_result": (dirs["position_decision"] / "fatigue_filter_result.json", kw["fatigue"]),
            "position_overextension_check": (dirs["position_decision"] / "position_overextension_check.json", kw["overextension"]),
            "structure_position_hard_negative_checklist": (dirs["position_decision"] / "structure_position_hard_negative_checklist.json", kw["hard"]),
            "structure_position_decision": (dirs["position_decision"] / "structure_position_decision.json", kw["decision"]),
        }
        for key, (path, obj) in json_items.items():
            path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
            artifacts[key] = str(path)
        self._write_csv(dirs["position_fact"] / "fixed_range_volume_profile.csv", kw["profile_rows"], ["bucket_id", "price", "volume_usd"])
        artifacts["fixed_range_volume_profile"] = str(dirs["position_fact"] / "fixed_range_volume_profile.csv")
        report = dirs["reports"] / "structure_position_report.md"
        report.write_text(self._report(kw["decision"]), encoding="utf-8")
        artifacts["structure_position_report"] = str(report)
        handoff = self._build_handoff(kw["decision"], artifacts, dirs)
        hp = dirs["handoff"] / "phase_05_handoff_packet.json"
        hp.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["handoff_packet"] = str(hp)
        missing = dirs["audit"] / "missing_fields_report.md"
        missing.write_text("# Phase 05 Missing Fields\n\n" + "\n".join(f"- {m}" for m in (kw["decision"].get("missing_fields") or ["none"])), encoding="utf-8")
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
        audit = dirs["audit"] / "phase_05_audit_report.md"
        audit.write_text(self._audit(kw["phase04"], kw["decision"], artifacts, kw["validation"]), encoding="utf-8")
        artifacts["audit_report"] = str(audit)
        return artifacts

    def _build_handoff(self, decision: Mapping[str, Any], artifacts: Mapping[str, str], dirs: Mapping[str, Path]) -> dict:
        return {"phase": PHASE_NAME, "token_address": decision.get("token_address"), "token_symbol": decision.get("token_symbol"), "snapshot_id": decision.get("snapshot_id"), "snapshot_time": decision.get("snapshot_time"), "completion_status": decision.get("completion_status"), "structure_position_status": decision.get("structure_position_status"), "position_extension_status": decision.get("position_extension_status"), "handoff_files": {"structure_position_decision": artifacts["structure_position_decision"], "avwap_completion_gate": artifacts["avwap_completion_gate"], "failure_test_result": artifacts["failure_test_result"], "fatigue_filter_result": artifacts["fatigue_filter_result"], "position_overextension_check": artifacts["position_overextension_check"], "structure_position_report": artifacts["structure_position_report"]}, "phase_06_required_context": {"completion_status": decision.get("completion_status"), "structure_position_status": decision.get("structure_position_status"), "position_extension_status": decision.get("position_extension_status"), "hard_negative_triggered": decision.get("hard_negative_triggered"), "required_strategy_checks": ["a_plus_structure_quality", "p1_position_quality", "hard_negative_checklist"]}, "positive_evidence": decision.get("positive_evidence", []), "counter_evidence": decision.get("counter_evidence", []), "hard_negative_triggered": decision.get("hard_negative_triggered"), "hard_negative_reasons": decision.get("hard_negative_reasons", []), "missing_fields": decision.get("missing_fields", []), "allowed_next_stage": decision.get("allowed_next_stage"), "handoff_status": decision.get("handoff_status"), "block_reason": decision.get("block_reason"), "degrade_reason": decision.get("degrade_reason"), "audit_file": str(dirs["audit"] / "phase_05_audit_report.md")}

    def _write_csv(self, path: Path, rows: list[dict], default_fields: list[str]) -> None:
        fields: list[str] = []
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

    def _report(self, d: Mapping[str, Any]) -> str:
        return "\n".join(["# Phase 05 Structure Position Report", "", f"- completion_status: {d.get('completion_status')}", f"- structure_position_status: {d.get('structure_position_status')}", f"- allowed_next_stage: {d.get('allowed_next_stage')}", f"- hard_negative_triggered: {d.get('hard_negative_triggered')}", "", "## Positive Evidence", *(f"- {x}" for x in d.get("positive_evidence", [])), "", "## Counter Evidence", *(f"- {x}" for x in d.get("counter_evidence", [])), "", "## Missing Fields", *(f"- {x}" for x in (d.get("missing_fields") or ["none"]))]) + "\n"

    def _audit(self, phase04: Mapping[str, Any], d: Mapping[str, Any], artifacts: Mapping[str, str], validation: Mapping[str, Any]) -> str:
        lines = ["# Phase 05 Structure Position Controller Audit", "", f"- phase: {PHASE_ID}", f"- upstream_scenario_status: {phase04.get('scenario_status')}", f"- completion_status: {d.get('completion_status')}", f"- handoff_status: {d.get('handoff_status')}", f"- hard_negative: {d.get('hard_negative_triggered')}", f"- validation_errors: {validation.get('errors')}", "", "## 已调用 Atomic Skill", "- poc_context_skill", "- avwap_anchor_skill", "- avwap_completion_gate_skill", "- failure_test_skill", "- adx_noise_rejection_skill", "- fatigue_filter_skill", "- position_quality_skill", "- phase_05_handoff_writer_skill", "", "## 输出文件"]
        lines += [f"- {k}: {v}" for k, v in artifacts.items()]
        lines += ["", "## Missing 字段"] + [f"- {m}" for m in (d.get("missing_fields") or ["none"])]
        lines += ["", "## 反证 / 硬否决", f"- counter_evidence: {d.get('counter_evidence')}", f"- hard_negative_reasons: {d.get('hard_negative_reasons')}", "", "## 下游交接", f"- next_stage: {NEXT_STAGE}", f"- allowed_next_stage: {d.get('allowed_next_stage')}"]
        return "\n".join(lines) + "\n"

    def _gaps(self, d: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
        gaps: list[str] = []
        if d.get("missing_fields"):
            gaps.append("missing_fields_require_upstream_refresh:" + ",".join(d.get("missing_fields")))
        if validation.get("degrade_reasons"):
            gaps.append("degraded_optional_inputs:" + ",".join(validation.get("degrade_reasons")))
        if d.get("completion_status") in {"COMPLETION_WAIT", "POSITION_UNKNOWN"}:
            gaps.append("insufficient_position_completion_evidence")
        if not gaps:
            gaps.append("none")
        return "# Phase 05 Gaps\n\n" + "\n".join(f"- {g}" for g in gaps) + "\n"

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
