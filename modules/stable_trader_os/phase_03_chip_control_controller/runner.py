from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

PHASE_ID = "phase_03_chip_control_controller"
NEXT_STAGE = "phase_04_scenario_recognition_controller"
VALID_STATUS = {
    "CONTROL_RETAINED",
    "CONTROL_WEAKENING",
    "PARTIAL_DISTRIBUTION",
    "ACTIVE_DISTRIBUTION",
    "TRANSFER_TO_COUNTERPARTY",
    "STRUCTURE_COLLAPSE",
    "RE_ACCUMULATION",
    "UNKNOWN_CONTROL",
}
HANDOFF_STATUS = {"HANDOFF_READY", "HANDOFF_BLOCKED"}
UPSTREAM_BLOCKING = {"WALLET_BLOCK"}
UPSTREAM_DEGRADED = {"WALLET_PAUSE", "WALLET_UNKNOWN", "WALLET_DATA_WEAK", "WALLET_COUNTERPARTY_PRESSURE"}


class Phase03ChipControlController:
    """HER Phase03 controller: structure-address evidence -> chip-control state.

    The controller owns contracts, missing/degrade/block handling, hard-negative
    propagation, standard outputs, handoff, and audit. It deliberately avoids
    buy/sell advice and absolute wallet identity claims.
    """

    def run(self, *, phase02_handoff_file: str | Path, output_dir: str | Path) -> Dict[str, Any]:
        handoff_file = Path(phase02_handoff_file)
        out = Path(output_dir)
        phase_dir = out / "03_chip_control"
        dirs = self._ensure_dirs(phase_dir)

        phase02 = json.loads(handoff_file.read_text(encoding="utf-8"))
        validation = self._validate_phase02_handoff(phase02, handoff_file.parent)
        refs = self._resolve_refs(phase02, handoff_file.parent)
        token_address = phase02.get("token_address", "missing")
        token_symbol = phase02.get("token_symbol", "")
        snapshot_id = phase02.get("snapshot_id", "missing")

        wallet_rows = self._read_csv(refs.get("wallet_classification"))
        same_source_rows = self._read_csv(refs.get("same_source_groups"))
        distribution_rows = self._read_csv(refs.get("distribution_paths"))
        backflow_rows = self._read_csv(refs.get("backflow_paths"))
        holder_rows = self._read_csv(refs.get("holder_normalized"))
        top_trader_rows = self._read_csv(refs.get("top_trader_normalized"))
        wallet_trade_rows = self._read_csv(refs.get("wallet_trade_normalized"))
        kline_rows = self._read_csv(refs.get("kline_normalized"))
        market_context = self._read_json(refs.get("token_market_context"))
        decision = self._read_json(refs.get("wallet_structure_decision"))

        sets = self._build_structure_wallet_sets(token_address, wallet_rows, same_source_rows, distribution_rows, backflow_rows)
        early = self._early_chip_state(token_address, sets, wallet_rows, holder_rows, wallet_trade_rows)
        early_exit = self._early_exit_detection(token_address, early)
        group_rows, group_summary = self._same_source_group_state(token_address, same_source_rows, holder_rows, wallet_trade_rows)
        distribution_state, distribution_events = self._distribution_sell_state(token_address, distribution_rows, wallet_trade_rows, holder_rows)
        backflow_state, backflow_events = self._backflow_risk_state(token_address, backflow_rows)
        counterparty = self._counterparty_pressure(token_address, wallet_rows, holder_rows, top_trader_rows)
        top_holder_change, top_holder_delta = self._top_holder_change(token_address, wallet_rows, holder_rows)
        market_cap_context = self._market_cap_context(token_address, market_context)
        volume_context = self._volume_context(token_address, kline_rows, wallet_trade_rows, early, distribution_state)

        status, positive, negative, hard_reasons = self._classify_status(
            phase02=phase02,
            validation=validation,
            early=early,
            early_exit=early_exit,
            group_summary=group_summary,
            distribution_state=distribution_state,
            backflow_state=backflow_state,
            counterparty=counterparty,
            top_holder_change=top_holder_change,
            market_cap_context=market_cap_context,
            volume_context=volume_context,
        )
        dominant = self._dominant_side_status(token_address, status, early, group_summary, hard_reasons)
        transfer = self._chip_transfer_status(token_address, status, distribution_state, counterparty, top_holder_change)
        missing_fields = sorted(set(validation["missing_fields"] + self._data_missing_fields(refs, holder_rows, market_context)))
        degrade_reason = "; ".join(validation["degrade_reasons"] + (["missing_fields:" + ",".join(missing_fields)] if missing_fields and status != "STRUCTURE_COLLAPSE" else []))
        hard_negative = bool(hard_reasons) or status in {"ACTIVE_DISTRIBUTION", "TRANSFER_TO_COUNTERPARTY", "STRUCTURE_COLLAPSE"}
        allow_next = status != "STRUCTURE_COLLAPSE" and not (phase02.get("phase_status") in UPSTREAM_BLOCKING)
        handoff_status = "HANDOFF_READY" if allow_next else "HANDOFF_BLOCKED"

        summary = {
            "phase": "phase_03_chip_control",
            "token_address": token_address,
            "token_symbol": token_symbol,
            "snapshot_id": snapshot_id,
            "snapshot_time": self._now(),
            "chip_control_status": status,
            "dominant_side_status": dominant["dominant_side_status"],
            "chip_transfer_status": transfer["chip_transfer_status"],
            "chip_control_score": self._score_control(early, group_summary, distribution_state, backflow_state, counterparty),
            "distribution_risk_score": distribution_state["distribution_risk_score"],
            "counterparty_pressure_score": counterparty["counterparty_pressure_score"],
            "structure_retention_score": self._score_retention(early, group_summary),
            "early_wallet_count": early["early_wallet_count"],
            "early_wallet_retention_ratio": early["early_wallet_retention_ratio"],
            "early_wallet_exit_ratio": early["early_wallet_exit_ratio"],
            "early_exit_status": early_exit["early_exit_status"],
            "same_source_group_count": group_summary["same_source_group_count"],
            "same_source_group_retention_ratio": group_summary["same_source_group_retention_ratio"],
            "same_source_group_sell_sync_score": group_summary["same_source_group_sell_sync_score"],
            "same_source_group_status": group_summary["same_source_group_status"],
            "distribution_receiver_count": distribution_state["distribution_receiver_count"],
            "distribution_seller_count": distribution_state["distribution_seller_count"],
            "distribution_receiver_sell_ratio": distribution_state["distribution_receiver_sell_ratio"],
            "distribution_sell_status": distribution_state["distribution_sell_status"],
            "backflow_detected": backflow_state["backflow_detected"],
            "backflow_risk_status": backflow_state["backflow_risk_status"],
            "backflow_node_count": backflow_state["backflow_node_count"],
            "counterparty_whale_count": counterparty["counterparty_whale_count"],
            "trapped_wallet_count": counterparty["trapped_wallet_count"],
            "counterparty_pressure_status": counterparty["counterparty_pressure_status"],
            "top_holder_change_status": top_holder_change["top_holder_change_status"],
            "market_cap_context_status": market_cap_context["market_cap_context_status"],
            "volume_chip_status": volume_context["volume_chip_status"],
            "positive_evidence": positive,
            "negative_evidence": negative,
            "counter_evidence": negative,
            "hard_negative_triggered": hard_negative,
            "hard_negative_reasons": hard_reasons,
            "missing_fields": missing_fields,
            "degrade_reason": degrade_reason,
            "block_reason": "; ".join(hard_reasons) if not allow_next else "",
            "allowed_next_stage": NEXT_STAGE if allow_next else "blocked",
            "handoff_status": handoff_status,
        }

        artifacts = self._write_outputs(
            dirs=dirs,
            token_address=token_address,
            sets=sets,
            early=early,
            early_exit=early_exit,
            group_rows=group_rows,
            group_summary=group_summary,
            distribution_state=distribution_state,
            distribution_events=distribution_events,
            backflow_state=backflow_state,
            backflow_events=backflow_events,
            counterparty=counterparty,
            top_holder_change=top_holder_change,
            top_holder_delta=top_holder_delta,
            market_cap_context=market_cap_context,
            volume_context=volume_context,
            dominant=dominant,
            transfer=transfer,
            summary=summary,
            phase02_handoff=phase02,
            validation=validation,
        )
        manifest = phase_dir / "run_manifest.json"
        manifest.write_text(json.dumps({"phase": PHASE_ID, "phase_status": status, "artifacts": artifacts}, ensure_ascii=False, indent=2), encoding="utf-8")
        artifacts["run_manifest"] = str(manifest)
        return {"phase": PHASE_ID, "phase_status": status, "artifacts": artifacts}

    def _ensure_dirs(self, phase_dir: Path) -> Dict[str, Path]:
        dirs = {"phase": phase_dir, "chip_fact": phase_dir / "chip_fact", "chip_control": phase_dir / "chip_control", "handoff": phase_dir / "handoff", "reports": phase_dir / "reports", "audit": phase_dir / "audit"}
        for d in dirs.values():
            d.mkdir(parents=True, exist_ok=True)
        return dirs

    def _resolve_refs(self, packet: Mapping[str, Any], base: Path) -> Dict[str, Path]:
        refs = dict(packet.get("required_files_for_next_stage", {}) or {})
        refs.update(packet.get("optional_files_for_next_stage", {}) or {})
        out: Dict[str, Path] = {}
        for k, v in refs.items():
            if not v or v == "missing":
                continue
            p = Path(str(v))
            out[k] = p if p.is_absolute() else base / p
        return out

    def _validate_phase02_handoff(self, packet: Mapping[str, Any], base: Path) -> Dict[str, Any]:
        errors: list[str] = []
        degrade: list[str] = []
        missing_fields: list[str] = []
        for field in ["phase", "token_address", "snapshot_id", "phase_status", "next_stage", "required_files_for_next_stage"]:
            if field not in packet:
                errors.append(f"missing_handoff_field:{field}")
                missing_fields.append(field)
        if packet.get("next_stage") != PHASE_ID:
            errors.append("next_stage_not_phase03_chip_control_controller")
        if packet.get("phase_status") in UPSTREAM_BLOCKING or packet.get("hard_negative_triggered"):
            errors.append("upstream_wallet_block_or_hard_negative")
        if packet.get("phase_status") in UPSTREAM_DEGRADED or packet.get("allow_next_stage") is False:
            degrade.append("upstream_wallet_structure_degraded_or_disallowed")
        refs = packet.get("required_files_for_next_stage", {}) or {}
        for name in ["wallet_structure_decision", "wallet_classification"]:
            ref = refs.get(name)
            if not ref:
                errors.append(f"missing_required_ref:{name}")
            else:
                p = Path(ref) if Path(ref).is_absolute() else base / ref
                if not p.exists():
                    errors.append(f"missing_required_file:{name}")
        for name in ["same_source_groups", "distribution_paths", "backflow_paths"]:
            ref = refs.get(name)
            if not ref:
                degrade.append(f"optional_phase02_ref_missing:{name}")
            else:
                p = Path(ref) if Path(ref).is_absolute() else base / ref
                if not p.exists():
                    degrade.append(f"optional_phase02_file_missing:{name}")
        return {"errors": errors, "degrade_reasons": degrade, "missing_fields": missing_fields, "hard_negative_triggered": bool(errors and any("block" in e or "hard_negative" in e for e in errors))}

    def _read_csv(self, path: Path | None) -> list[dict]:
        if not path or not path.exists() or path.suffix.lower() != ".csv":
            return []
        with path.open(newline="", encoding="utf-8-sig") as f:
            return [dict(r) for r in csv.DictReader(f)]

    def _read_json(self, path: Path | None) -> dict:
        if not path or not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}

    def _addr(self, row: Mapping[str, Any]) -> str:
        return str(row.get("wallet_address") or row.get("address") or row.get("holder_address") or row.get("owner") or "").strip()

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

    def _role_text(self, row: Mapping[str, Any]) -> str:
        return " ".join(str(row.get(k, "")) for k in ["primary_role", "role_name", "wallet_role", "sikk_role", "gmgn_tags", "note", "sikk_remark"]).lower()

    def _build_structure_wallet_sets(self, token: str, wallet_rows: list[dict], groups: list[dict], distributions: list[dict], backflows: list[dict]) -> dict:
        early, counterparty, trapped, noise, core = set(), set(), set(), set(), set()
        for r in wallet_rows:
            a = self._addr(r)
            text = self._role_text(r)
            first = self._num(r, "first_buy_seconds", "first_seen_seconds", default=999999)
            if not a:
                continue
            if first <= 300 or any(k in text for k in ["structure", "same-source", "同源", "new wallet", "sniper", "executor", "结构"]):
                early.add(a)
            if any(k in text for k in ["counterparty", "whale", "接盘", "trapped", "套牢"]):
                counterparty.add(a)
            if any(k in text for k in ["trapped", "套牢"]):
                trapped.add(a)
            if any(k in text for k in ["cex", "router", "lp", "pool", "program", "infra"]):
                noise.add(a)
            if any(k in text for k in ["core", "funding", "source", "核心", "资金源"]):
                core.add(a)
        group_wallets = {self._addr(r) for r in groups if self._addr(r)} | {str(r.get("member_wallet", "")).strip() for r in groups if r.get("member_wallet")}
        receivers = {str(r.get("receiver") or r.get("to_address") or self._addr(r)).strip() for r in distributions if str(r.get("receiver") or r.get("to_address") or self._addr(r)).strip()}
        sellers = {str(r.get("seller") or r.get("from_address") or self._addr(r)).strip() for r in distributions if str(r.get("seller") or r.get("from_address") or self._addr(r)).strip()}
        backflow_wallets = {self._addr(r) or str(r.get("from_address") or r.get("to_address") or "").strip() for r in backflows}
        return {"token_address": token, "snapshot_time": self._now(), "early_structure_wallets": sorted(early), "same_source_group_wallets": sorted(w for w in group_wallets if w), "distribution_receivers": sorted(receivers), "distribution_sellers": sorted(sellers), "backflow_wallets": sorted(w for w in backflow_wallets if w), "core_source_candidates": sorted(core), "counterparty_whales": sorted(counterparty), "trapped_wallets": sorted(trapped), "excluded_noise_wallets": sorted(noise)}

    def _early_chip_state(self, token: str, sets: Mapping[str, Any], wallet_rows: list[dict], holder_rows: list[dict], trade_rows: list[dict]) -> dict:
        early = set(sets.get("early_structure_wallets") or [])
        holder_by_addr = {self._addr(r): r for r in holder_rows if self._addr(r)}
        trade_by_addr = {self._addr(r): r for r in trade_rows if self._addr(r)}
        initial = current = sold = realized = unrealized = 0.0
        for a in early:
            h = holder_by_addr.get(a, {})
            t = trade_by_addr.get(a, {})
            got = self._num(t, "buy_token_amount", "token_bought", "initial_token_amount", default=0) or self._num(h, "initial_token_amount", default=0)
            bal = self._num(h, "current_token_balance", "balance", "amount", default=0)
            s = self._num(t, "sell_token_amount", "token_sold", default=0)
            if not got and (bal or s):
                got = bal + s
            initial += got
            current += bal
            sold += s
            realized += self._num(t, "realized_profit_usd", "profit", "profit_usd", default=0)
            unrealized += self._num(h, "unrealized_profit_usd", "unrealized_pnl_usd", default=0)
        retention = "missing" if initial <= 0 else round(current / initial, 6)
        exit_ratio = "missing" if initial <= 0 else round(max(sold, initial-current) / initial, 6)
        if retention == "missing": state = "EARLY_CHIP_UNKNOWN"
        elif retention >= 0.65: state = "EARLY_CHIP_RETAINED"
        elif retention >= 0.25: state = "EARLY_CHIP_PARTIAL_EXIT"
        else: state = "EARLY_CHIP_MOSTLY_EXITED"
        return {"token_address": token, "early_wallet_count": len(early), "early_wallet_initial_token_amount": initial, "early_wallet_current_token_balance": current, "early_wallet_retention_ratio": retention, "early_wallet_exit_ratio": exit_ratio, "early_wallet_realized_profit_usd": realized, "early_wallet_unrealized_profit_usd": unrealized, "early_chip_state": state, "evidence_level": "E3" if retention != "missing" else "E0", "risk_level": "R1" if state == "EARLY_CHIP_RETAINED" else "R2", "reason": state}

    def _early_exit_detection(self, token: str, early: Mapping[str, Any]) -> dict:
        er = early.get("early_wallet_exit_ratio")
        if er == "missing": status = "UNKNOWN_EARLY_EXIT"
        elif er >= 0.85: status = "FULL_EARLY_EXIT"
        elif er >= 0.6: status = "CLUSTER_EARLY_EXIT"
        elif er >= 0.3: status = "PARTIAL_EARLY_EXIT"
        else: status = "NO_EARLY_CLUSTER_EXIT"
        return {"token_address": token, "early_exit_status": status, "early_wallet_exit_ratio": er, "hard_risk": status in {"FULL_EARLY_EXIT", "CLUSTER_EARLY_EXIT"}, "reason": status}

    def _same_source_group_state(self, token: str, groups: list[dict], holder_rows: list[dict], trade_rows: list[dict]) -> tuple[list[dict], dict]:
        holder = {self._addr(r): r for r in holder_rows if self._addr(r)}
        trade = {self._addr(r): r for r in trade_rows if self._addr(r)}
        by_group: dict[str, list[str]] = {}
        for r in groups:
            gid = str(r.get("group_id") or r.get("same_source_group_id") or "G0")
            a = self._addr(r) or str(r.get("member_wallet") or "").strip()
            if a:
                by_group.setdefault(gid, []).append(a)
        rows=[]; ratios=[]; sync_scores=[]; statuses=[]
        for gid, members in by_group.items():
            init=cur=sold=0.0
            for a in members:
                h=holder.get(a,{}) ; t=trade.get(a,{})
                got=self._num(t,"buy_token_amount","initial_token_amount",default=0) or self._num(h,"initial_token_amount",default=0)
                bal=self._num(h,"current_token_balance","balance","amount",default=0)
                s=self._num(t,"sell_token_amount",default=0)
                if not got and (bal or s): got=bal+s
                init+=got; cur+=bal; sold+=s
            retention="missing" if init<=0 else round(cur/init,6)
            exit_ratio="missing" if init<=0 else round(max(sold,init-cur)/init,6)
            sync=0 if exit_ratio=="missing" else round(float(exit_ratio)*100,2)
            if retention=="missing": state="GROUP_UNKNOWN"
            elif retention>=0.65: state="GROUP_HOLDING"
            elif retention>=0.35: state="GROUP_ROTATING"
            elif sync>=75: state="GROUP_SYNC_EXIT"
            else: state="GROUP_SELLING"
            rows.append({"group_id":gid,"member_count":len(members),"group_initial_token_amount":init,"group_current_token_balance":cur,"group_retention_ratio":retention,"group_exit_ratio":exit_ratio,"group_sell_sync_score":sync,"group_backflow_detected":False,"group_chip_state":state,"group_risk_level":"R3" if state=="GROUP_SYNC_EXIT" else "R2" if state=="GROUP_SELLING" else "R1","reason":state})
            if retention!="missing": ratios.append(float(retention)); sync_scores.append(sync)
            statuses.append(state)
        summary={"token_address":token,"same_source_group_count":len(by_group),"same_source_group_retention_ratio":"missing" if not ratios else round(sum(ratios)/len(ratios),6),"same_source_group_sell_sync_score":"missing" if not sync_scores else round(sum(sync_scores)/len(sync_scores),2),"same_source_group_status":"GROUP_UNKNOWN" if not statuses else ("GROUP_SYNC_EXIT" if "GROUP_SYNC_EXIT" in statuses else "GROUP_SELLING" if "GROUP_SELLING" in statuses else "GROUP_ROTATING" if "GROUP_ROTATING" in statuses else "GROUP_HOLDING")}
        return rows, summary

    def _distribution_sell_state(self, token: str, dist: list[dict], trades: list[dict], holders: list[dict]) -> tuple[dict, list[dict]]:
        receivers={str(r.get("receiver") or r.get("to_address") or self._addr(r)).strip() for r in dist if str(r.get("receiver") or r.get("to_address") or self._addr(r)).strip()}
        trade={self._addr(r):r for r in trades if self._addr(r)}
        sellers=[]
        for a in receivers:
            t=trade.get(a,{})
            sell_usd=self._num(t,"sell_amount_usd","total_sell_usd",default=0)
            if sell_usd>0: sellers.append({"wallet_address":a,"sell_amount_usd":sell_usd})
        ratio="missing" if not receivers else round(len(sellers)/len(receivers),6)
        if ratio=="missing": status="DISTRIBUTION_UNKNOWN"
        elif ratio>=0.66: status="DISTRIBUTION_CLUSTER_EXIT"
        elif ratio>=0.35: status="DISTRIBUTION_ACTIVE_SELL"
        elif ratio>0: status="DISTRIBUTION_PARTIAL_SELL"
        else: status="DISTRIBUTION_INACTIVE"
        risk_score=0 if ratio=="missing" else round(float(ratio)*100,2)
        return {"token_address":token,"distribution_receiver_count":len(receivers),"distribution_seller_count":len(sellers),"distribution_receiver_sell_ratio":ratio,"distribution_full_exit_count":0,"distribution_cluster_sell_score":risk_score,"distribution_risk_score":risk_score,"distribution_risk_level":"R3" if risk_score>=66 else "R2" if risk_score>=35 else "R1","distribution_sell_status":status}, sellers

    def _backflow_risk_state(self, token: str, rows: list[dict]) -> tuple[dict, list[dict]]:
        count=len(rows); nodes={str(r.get("to_address") or r.get("receiver") or self._addr(r)).strip() for r in rows if str(r.get("to_address") or r.get("receiver") or self._addr(r)).strip()}
        amount=sum(self._num(r,"amount_usd","value_usd","backflow_amount_usd",default=0) for r in rows)
        if count==0: status="NO_BACKFLOW"
        elif count>=3 or len(nodes)<=1: status="CORE_NODE_BACKFLOW"
        elif count>=2: status="MULTI_WALLET_BACKFLOW"
        else: status="WEAK_BACKFLOW"
        return {"token_address":token,"backflow_detected":count>0,"backflow_wallet_count":count,"backflow_total_amount_usd":amount,"backflow_node_count":len(nodes),"core_backflow_node_count":1 if status=="CORE_NODE_BACKFLOW" else 0,"multi_wallet_backflow_score":min(100,count*30),"repeated_backflow_score":min(100,count*25),"backflow_risk_status":status}, rows

    def _counterparty_pressure(self, token: str, wallets: list[dict], holders: list[dict], traders: list[dict]) -> dict:
        cp=[r for r in wallets if any(k in self._role_text(r) for k in ["counterparty","whale","接盘","trapped","套牢"])]
        trapped=[r for r in wallets if any(k in self._role_text(r) for k in ["trapped","套牢"])]
        buy=sum(self._num(r,"buy_amount_usd","total_buy_usd",default=0) for r in cp+traders)
        cur=sum(self._num(r,"current_value_usd","value_usd",default=0) for r in holders if self._addr(r) in {self._addr(x) for x in cp})
        pressure=min(100, len(cp)*25 + len(trapped)*20 + (20 if buy>10000 else 0))
        status="COUNTERPARTY_PRESSURE_EXTREME" if pressure>=80 else "COUNTERPARTY_PRESSURE_HIGH" if pressure>=55 else "COUNTERPARTY_PRESSURE_MEDIUM" if pressure>=25 else "COUNTERPARTY_PRESSURE_LOW"
        return {"token_address":token,"counterparty_whale_count":len(cp),"late_large_buyer_count":len(traders),"trapped_wallet_count":len(trapped),"counterparty_buy_amount_usd":buy,"counterparty_current_value_usd":cur,"counterparty_unrealized_pnl_usd":0,"counterparty_pressure_score":pressure,"counterparty_pressure_status":status,"reason":status}

    def _top_holder_change(self, token: str, wallets: list[dict], holders: list[dict]) -> tuple[dict, list[dict]]:
        total=sum(self._num(r,"current_token_balance","balance","amount",default=0) for r in holders)
        structure={self._addr(r) for r in wallets if any(k in self._role_text(r) for k in ["structure","同源","sniper","executor","new wallet"])}
        counter={self._addr(r) for r in wallets if any(k in self._role_text(r) for k in ["counterparty","whale","接盘","trapped"])}
        s_bal=sum(self._num(r,"current_token_balance","balance","amount",default=0) for r in holders if self._addr(r) in structure)
        c_bal=sum(self._num(r,"current_token_balance","balance","amount",default=0) for r in holders if self._addr(r) in counter)
        if total<=0: status="HOLDER_UNKNOWN"
        elif c_bal> s_bal and c_bal/total>0.25: status="HOLDER_TRANSFER_TO_COUNTERPARTY"
        elif s_bal/total>0.35: status="HOLDER_STRUCTURE_STABLE"
        else: status="HOLDER_STRUCTURE_DISTRIBUTING"
        return {"token_address":token,"top_holder_change_status":status,"structure_wallet_top_holder_ratio":"missing" if total<=0 else round(s_bal/total,6),"counterparty_wallet_top_holder_ratio":"missing" if total<=0 else round(c_bal/total,6),"reason":status}, holders[:50]

    def _market_cap_context(self, token: str, ctx: Mapping[str, Any]) -> dict:
        d=self._num(ctx,"discovery_market_cap_usd",default=0); c=self._num(ctx,"current_market_cap_usd",default=0)
        pct="missing" if d<=0 else round((c-d)/d*100,2)
        if pct=="missing": status="MARKET_CAP_UNKNOWN"
        elif pct>=1000: status="MARKET_CAP_EXIT_LIQUIDITY_RISK"
        elif pct>=400: status="MARKET_CAP_OVEREXTENDED"
        elif pct>=100: status="MARKET_CAP_EXPANDED"
        elif pct>=0: status="MARKET_CAP_NORMAL"
        else: status="MARKET_CAP_EARLY"
        return {"token_address":token,"discovery_market_cap_usd":d,"current_market_cap_usd":c,"market_cap_change_from_discovery_pct":pct,"market_cap_context_status":status,"late_entry_risk":status in {"MARKET_CAP_OVEREXTENDED","MARKET_CAP_EXIT_LIQUIDITY_RISK"},"exit_liquidity_risk":status=="MARKET_CAP_EXIT_LIQUIDITY_RISK","reason":status}

    def _volume_context(self, token: str, klines: list[dict], trades: list[dict], early: Mapping[str, Any], dist: Mapping[str, Any]) -> dict:
        vol=sum(self._num(r,"volume_usd",default=0) for r in klines[-10:])
        er=early.get("early_wallet_exit_ratio")
        if not klines: status="VOLUME_UNKNOWN"
        elif er!="missing" and float(er)>0.5: status="VOLUME_SUPPORTS_DISTRIBUTION"
        elif dist.get("distribution_sell_status") in {"DISTRIBUTION_ACTIVE_SELL","DISTRIBUTION_CLUSTER_EXIT"}: status="VOLUME_FAKE_PUSH_RISK"
        elif vol>0 and early.get("early_chip_state")=="EARLY_CHIP_RETAINED": status="VOLUME_SUPPORTS_CONTROL"
        else: status="VOLUME_WEAK_CONFIRMATION"
        return {"token_address":token,"volume_usd_recent":vol,"volume_chip_status":status,"reason":status}

    def _classify_status(self, **ctx: Any) -> tuple[str, list[str], list[str], list[str]]:
        phase02=ctx["phase02"]; validation=ctx["validation"]; early=ctx["early"]; early_exit=ctx["early_exit"]; group=ctx["group_summary"]; dist=ctx["distribution_state"]; back=ctx["backflow_state"]; cp=ctx["counterparty"]; top=ctx["top_holder_change"]; mcap=ctx["market_cap_context"]; vol=ctx["volume_context"]
        pos=[]; neg=[]; hard=[]
        if phase02.get("phase_status") in UPSTREAM_BLOCKING or phase02.get("hard_negative_triggered"):
            hard.append("phase_02_wallet_block_or_hard_negative")
        if early.get("early_chip_state")=="EARLY_CHIP_RETAINED": pos.append("early_structure_wallet_retention_supported")
        if group.get("same_source_group_status")=="GROUP_HOLDING": pos.append("same_source_group_holding_supported")
        if dist.get("distribution_sell_status")=="DISTRIBUTION_INACTIVE": pos.append("distribution_receivers_not_selling")
        if back.get("backflow_risk_status")=="NO_BACKFLOW": pos.append("no_backflow_detected")
        if cp.get("counterparty_pressure_status")=="COUNTERPARTY_PRESSURE_LOW": pos.append("counterparty_pressure_low")
        if early_exit.get("early_exit_status") in {"CLUSTER_EARLY_EXIT","FULL_EARLY_EXIT"}: hard.append("early_structure_wallet_cluster_exit")
        if group.get("same_source_group_status")=="GROUP_SYNC_EXIT": hard.append("same_source_group_core_sync_exit")
        if dist.get("distribution_sell_status")=="DISTRIBUTION_CLUSTER_EXIT": hard.append("distribution_receivers_cluster_sell")
        if back.get("backflow_risk_status") in {"CORE_NODE_BACKFLOW","MULTI_WALLET_BACKFLOW"}: hard.append("sell_funds_backflow_to_core_node")
        if cp.get("counterparty_pressure_status") in {"COUNTERPARTY_PRESSURE_HIGH","COUNTERPARTY_PRESSURE_EXTREME"}: neg.append("counterparty_pressure_high")
        if top.get("top_holder_change_status")=="HOLDER_TRANSFER_TO_COUNTERPARTY": hard.append("top_holder_transfer_to_counterparty")
        if vol.get("volume_chip_status") in {"VOLUME_SUPPORTS_DISTRIBUTION","VOLUME_FAKE_PUSH_RISK"}: neg.append(vol["volume_chip_status"])
        if mcap.get("exit_liquidity_risk"): neg.append("market_cap_exit_liquidity_risk")
        neg.extend(validation["errors"] + validation["degrade_reasons"])
        if "phase_02_wallet_block_or_hard_negative" in hard: return "STRUCTURE_COLLAPSE", pos, neg, hard
        if "top_holder_transfer_to_counterparty" in hard or cp.get("counterparty_pressure_status")=="COUNTERPARTY_PRESSURE_EXTREME": return "TRANSFER_TO_COUNTERPARTY", pos, neg, hard or ["counterparty_pressure_extreme"]
        if hard: return "ACTIVE_DISTRIBUTION", pos, neg, hard
        if dist.get("distribution_sell_status") in {"DISTRIBUTION_ACTIVE_SELL","DISTRIBUTION_PARTIAL_SELL"}: return "PARTIAL_DISTRIBUTION", pos, neg, []
        if early.get("early_chip_state")=="EARLY_CHIP_PARTIAL_EXIT" or group.get("same_source_group_status")=="GROUP_ROTATING" or cp.get("counterparty_pressure_status")=="COUNTERPARTY_PRESSURE_MEDIUM": return "CONTROL_WEAKENING", pos, neg, []
        if early.get("early_chip_state")=="EARLY_CHIP_RETAINED" and (pos or not neg): return "CONTROL_RETAINED", pos, neg, []
        return "UNKNOWN_CONTROL", pos, neg or ["insufficient_chip_control_evidence"], []

    def _dominant_side_status(self, token: str, status: str, early: Mapping[str, Any], group: Mapping[str, Any], hard: list[str]) -> dict:
        mapping={"CONTROL_RETAINED":"DOMINANT_SIDE_RETAINED","CONTROL_WEAKENING":"DOMINANT_SIDE_WEAKENING","PARTIAL_DISTRIBUTION":"DOMINANT_SIDE_DISTRIBUTING","ACTIVE_DISTRIBUTION":"DOMINANT_SIDE_DISTRIBUTING","TRANSFER_TO_COUNTERPARTY":"DOMINANT_SIDE_EXITED","STRUCTURE_COLLAPSE":"DOMINANT_SIDE_EXITED","RE_ACCUMULATION":"DOMINANT_SIDE_ROTATING","UNKNOWN_CONTROL":"DOMINANT_SIDE_UNKNOWN"}
        return {"token_address":token,"dominant_side_status":mapping.get(status,"DOMINANT_SIDE_UNKNOWN"),"reason":"; ".join(hard) if hard else status}

    def _chip_transfer_status(self, token: str, status: str, dist: Mapping[str, Any], cp: Mapping[str, Any], top: Mapping[str, Any]) -> dict:
        mapping={"CONTROL_RETAINED":"CHIP_RETAINED","CONTROL_WEAKENING":"CHIP_PARTIAL_TRANSFER","PARTIAL_DISTRIBUTION":"CHIP_DISTRIBUTION_ACTIVE","ACTIVE_DISTRIBUTION":"CHIP_DISTRIBUTION_ACTIVE","TRANSFER_TO_COUNTERPARTY":"CHIP_TRANSFER_TO_COUNTERPARTY","STRUCTURE_COLLAPSE":"CHIP_COLLAPSE","RE_ACCUMULATION":"CHIP_RE_ACCUMULATION","UNKNOWN_CONTROL":"CHIP_UNKNOWN"}
        return {"token_address":token,"chip_transfer_status":mapping.get(status,"CHIP_UNKNOWN"),"reason":status}

    def _score_retention(self, early: Mapping[str, Any], group: Mapping[str, Any]) -> int:
        vals=[]
        for v in [early.get("early_wallet_retention_ratio"), group.get("same_source_group_retention_ratio")]:
            if v != "missing": vals.append(float(v)*100)
        return round(sum(vals)/len(vals)) if vals else 0

    def _score_control(self, early: Mapping[str, Any], group: Mapping[str, Any], dist: Mapping[str, Any], back: Mapping[str, Any], cp: Mapping[str, Any]) -> int:
        score=self._score_retention(early, group)
        score-= int(float(dist.get("distribution_risk_score") or 0)*0.3)
        score-= int(float(cp.get("counterparty_pressure_score") or 0)*0.3)
        if back.get("backflow_detected"): score-=25
        return max(0,min(100,score))

    def _data_missing_fields(self, refs: Mapping[str, Path], holders: list[dict], market: Mapping[str, Any]) -> list[str]:
        missing=[]
        for req in ["holder_normalized","token_market_context"]:
            if req not in refs or not refs[req].exists(): missing.append(req)
        if not holders: missing.append("holder_rows")
        if not market: missing.append("token_market_context_fields")
        return missing

    def _write_csv(self, path: Path, rows: list[dict], default_fields: list[str]) -> None:
        fields=[]
        for r in rows:
            for k in r:
                if k not in fields: fields.append(k)
        if not fields: fields=default_fields
        with path.open("w", newline="", encoding="utf-8") as f:
            w=csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

    def _write_outputs(self, **kw: Any) -> Dict[str, str]:
        dirs=kw["dirs"]; artifacts={}
        json_items={
            "structure_wallet_sets": (dirs["chip_fact"] / "structure_wallet_sets.json", kw["sets"]),
            "early_chip_state": (dirs["chip_control"] / "early_chip_state.json", kw["early"]),
            "early_exit_detection": (dirs["chip_control"] / "early_exit_detection.json", kw["early_exit"]),
            "distribution_sell_state": (dirs["chip_control"] / "distribution_sell_state.json", kw["distribution_state"]),
            "backflow_risk_state": (dirs["chip_control"] / "backflow_risk_state.json", kw["backflow_state"]),
            "counterparty_pressure": (dirs["chip_control"] / "counterparty_pressure.json", kw["counterparty"]),
            "same_source_group_summary": (dirs["chip_control"] / "same_source_group_summary.json", kw["group_summary"]),
            "top_holder_change": (dirs["chip_control"] / "top_holder_change.json", kw["top_holder_change"]),
            "market_cap_context_for_chip": (dirs["chip_control"] / "market_cap_context_for_chip.json", kw["market_cap_context"]),
            "volume_chip_context": (dirs["chip_control"] / "volume_chip_context.json", kw["volume_context"]),
            "dominant_side_status": (dirs["chip_control"] / "dominant_side_status.json", kw["dominant"]),
            "chip_transfer_status": (dirs["chip_control"] / "chip_transfer_status.json", kw["transfer"]),
            "chip_control_summary": (dirs["chip_control"] / "chip_control_summary.json", kw["summary"]),
        }
        for k,(p,obj) in json_items.items():
            p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"); artifacts[k]=str(p)
        self._write_csv(dirs["chip_fact"] / "structure_wallet_sets.csv", [{"set_name":k,"wallet_address":a} for k,v in kw["sets"].items() if isinstance(v,list) for a in v], ["set_name","wallet_address"]); artifacts["structure_wallet_sets_csv"]=str(dirs["chip_fact"] / "structure_wallet_sets.csv")
        self._write_csv(dirs["chip_fact"] / "early_wallet_retention.csv", [kw["early"]], list(kw["early"].keys())); artifacts["early_wallet_retention"]=str(dirs["chip_fact"] / "early_wallet_retention.csv")
        self._write_csv(dirs["chip_fact"] / "early_wallet_exit_events.csv", [kw["early_exit"]], list(kw["early_exit"].keys())); artifacts["early_wallet_exit_events"]=str(dirs["chip_fact"] / "early_wallet_exit_events.csv")
        self._write_csv(dirs["chip_control"] / "same_source_group_chip_state.csv", kw["group_rows"], ["group_id","group_chip_state","group_risk_level"]); artifacts["same_source_group_chip_state"]=str(dirs["chip_control"] / "same_source_group_chip_state.csv")
        self._write_csv(dirs["chip_fact"] / "distribution_receiver_sell_events.csv", kw["distribution_events"], ["wallet_address","sell_amount_usd"]); artifacts["distribution_receiver_sell_events"]=str(dirs["chip_fact"] / "distribution_receiver_sell_events.csv")
        self._write_csv(dirs["chip_fact"] / "backflow_cluster_events.csv", kw["backflow_events"], ["from_address","to_address","amount_usd"]); artifacts["backflow_cluster_events"]=str(dirs["chip_fact"] / "backflow_cluster_events.csv")
        self._write_csv(dirs["chip_fact"] / "counterparty_wallets.csv", [], ["wallet_address","counterparty_type","amount_usd"]); artifacts["counterparty_wallets"]=str(dirs["chip_fact"] / "counterparty_wallets.csv")
        self._write_csv(dirs["chip_fact"] / "top_holder_delta.csv", kw["top_holder_delta"], ["wallet_address","current_token_balance"]); artifacts["top_holder_delta"]=str(dirs["chip_fact"] / "top_holder_delta.csv")
        handoff=self._build_handoff(kw["summary"], artifacts, dirs)
        hp=dirs["handoff"] / "phase_03_handoff_packet.json"; hp.write_text(json.dumps(handoff, ensure_ascii=False, indent=2), encoding="utf-8"); artifacts["handoff_packet"]=str(hp)
        report=dirs["reports"] / "chip_control_report.md"; report.write_text(self._report(kw["summary"], artifacts), encoding="utf-8"); artifacts["chip_control_report"]=str(report)
        missing=dirs["audit"] / "missing_fields_report.md"; missing.write_text("# Phase 03 Missing Fields\n\n" + "\n".join(f"- {m}" for m in (kw["summary"].get("missing_fields") or ["none"])), encoding="utf-8"); artifacts["missing_fields_report"]=str(missing)
        outval=dirs["audit"] / "output_validation_report.json"; required=list(artifacts.values()); miss=[p for p in required if not Path(p).exists()]; outval.write_text(json.dumps({"status":"PASS" if not miss else "FAIL","checked_files":required,"missing_files":miss}, ensure_ascii=False, indent=2), encoding="utf-8"); artifacts["output_validation_report"]=str(outval)
        hval=dirs["audit"] / "handoff_validation_report.json"; hmiss=[k for k,v in handoff.get("handoff_files",{}).items() if not Path(v).exists()]; hval.write_text(json.dumps({"status":"PASS" if not hmiss and handoff.get("handoff_status") in HANDOFF_STATUS else "FAIL","missing_handoff_files":hmiss}, ensure_ascii=False, indent=2), encoding="utf-8"); artifacts["handoff_validation_report"]=str(hval)
        gaps=dirs["audit"] / "gaps.md"; gaps.write_text(self._gaps(kw["summary"], kw["validation"]), encoding="utf-8"); artifacts["gaps"]=str(gaps)
        audit=dirs["audit"] / "phase_03_audit_report.md"; audit.write_text(self._audit(kw["phase02_handoff"], kw["summary"], artifacts, kw["validation"]), encoding="utf-8"); artifacts["audit_report"]=str(audit)
        return artifacts

    def _build_handoff(self, summary: Mapping[str, Any], artifacts: Mapping[str, str], dirs: Mapping[str, Path]) -> dict:
        return {"phase":"phase_03_chip_control","token_address":summary.get("token_address"),"token_symbol":summary.get("token_symbol"),"snapshot_id":summary.get("snapshot_id"),"snapshot_time":summary.get("snapshot_time"),"chip_control_status":summary.get("chip_control_status"),"dominant_side_status":summary.get("dominant_side_status"),"chip_transfer_status":summary.get("chip_transfer_status"),"handoff_files":{"chip_control_summary":artifacts["chip_control_summary"],"dominant_side_status":artifacts["dominant_side_status"],"chip_transfer_status":artifacts["chip_transfer_status"],"counterparty_pressure":artifacts["counterparty_pressure"],"distribution_sell_state":artifacts["distribution_sell_state"],"backflow_risk_state":artifacts["backflow_risk_state"]},"phase_04_required_context":{"early_wallet_retention_ratio":summary.get("early_wallet_retention_ratio"),"early_wallet_exit_ratio":summary.get("early_wallet_exit_ratio"),"same_source_group_sell_sync_score":summary.get("same_source_group_sell_sync_score"),"distribution_receiver_sell_ratio":summary.get("distribution_receiver_sell_ratio"),"counterparty_pressure_score":summary.get("counterparty_pressure_score"),"distribution_risk_score":summary.get("distribution_risk_score"),"structure_retention_score":summary.get("structure_retention_score"),"market_cap_context_status":summary.get("market_cap_context_status"),"volume_chip_status":summary.get("volume_chip_status")},"forced_scenario_checks":self._forced_checks(summary),"blocked_positive_scenarios":["positive_expansion"] if summary.get("chip_control_status")=="STRUCTURE_COLLAPSE" else [],"allowed_next_stage":summary.get("allowed_next_stage"),"handoff_status":summary.get("handoff_status"),"block_reason":summary.get("block_reason"),"degrade_reason":summary.get("degrade_reason"),"audit_file":str(dirs["audit"] / "phase_03_audit_report.md")}

    def _forced_checks(self, summary: Mapping[str, Any]) -> list[str]:
        st=summary.get("chip_control_status")
        if st=="ACTIVE_DISTRIBUTION": return ["distribution_scene_detector","downtrend_distribution_check"]
        if st=="TRANSFER_TO_COUNTERPARTY": return ["trap_detector","exit_liquidity_trap_check"]
        if st=="PARTIAL_DISTRIBUTION": return ["distribution_counter_evidence_check"]
        if st=="RE_ACCUMULATION": return ["re_accumulation_scenario_check"]
        return []

    def _report(self, s: Mapping[str, Any], artifacts: Mapping[str, str]) -> str:
        return "\n".join(["# Phase 03 Chip Control Report","",f"- chip_control_status: {s.get('chip_control_status')}",f"- dominant_side_status: {s.get('dominant_side_status')}",f"- chip_transfer_status: {s.get('chip_transfer_status')}",f"- hard_negative_triggered: {s.get('hard_negative_triggered')}","","## Positive Evidence",*(f"- {x}" for x in s.get('positive_evidence',[])),"","## Counter Evidence",*(f"- {x}" for x in s.get('counter_evidence',[])),"","## Missing Fields",*(f"- {x}" for x in (s.get('missing_fields') or ['none'])),"","## Handoff",f"- next_stage: {s.get('allowed_next_stage')}"]) + "\n"

    def _audit(self, phase02: Mapping[str, Any], s: Mapping[str, Any], artifacts: Mapping[str, str], validation: Mapping[str, Any]) -> str:
        lines=["# Phase 03 Chip Control Controller Audit","",f"- phase: {PHASE_ID}",f"- upstream_phase_status: {phase02.get('phase_status')}",f"- phase_status: {s.get('chip_control_status')}",f"- handoff_status: {s.get('handoff_status')}",f"- hard_negative: {s.get('hard_negative_triggered')}",f"- validation_errors: {validation.get('errors')}","","## 已调用 Atomic Skill","- early_wallet_retention_skill","- early_wallet_exit_detector_skill","- same_source_group_retention_skill","- distribution_pressure_skill","- backflow_path_detector_skill","- counterparty_pressure_skill","- dominant_side_status_skill","- chip_transfer_detector_skill","","## 输出文件"]
        lines += [f"- {k}: {v}" for k,v in artifacts.items()]
        lines += ["","## Missing 字段"] + [f"- {m}" for m in (s.get('missing_fields') or ['none'])]
        lines += ["","## 反证 / 硬否决",f"- negative_evidence: {s.get('negative_evidence')}",f"- hard_negative_reasons: {s.get('hard_negative_reasons')}","","## 下游交接",f"- next_stage: {NEXT_STAGE}",f"- handoff_packet: {artifacts.get('handoff_packet')}"]
        return "\n".join(lines)+"\n"

    def _gaps(self, s: Mapping[str, Any], validation: Mapping[str, Any]) -> str:
        gaps=[]
        if s.get("missing_fields"): gaps.append("missing_fields_require_upstream_refresh:"+",".join(s.get("missing_fields")))
        if validation.get("degrade_reasons"): gaps.append("degraded_optional_inputs:"+",".join(validation.get("degrade_reasons")))
        if s.get("chip_control_status")=="UNKNOWN_CONTROL": gaps.append("insufficient_chip_control_evidence")
        if not gaps: gaps.append("none")
        return "# Phase 03 Gaps\n\n" + "\n".join(f"- {g}" for g in gaps) + "\n"

    def _now(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
