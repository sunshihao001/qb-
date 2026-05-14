#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GMGN/SIKK structural-intel → trading-system gate adapter.

目标：把代币结构扫描结果转换成交易系统可消费的数据契约。
边界：只生成观察/纸面交易/风控门控数据；不签名、不广播、不执行真实 swap。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping

INFRA_TAGS = {"pool", "lp", "amm", "router", "cex", "program", "pump_amm"}


def _num(data: Mapping[str, Any], key: str, default: float = 0.0) -> float:
    value = data.get(key, default)
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _bool(data: Mapping[str, Any], key: str, default: bool = False) -> bool:
    value = data.get(key, default)
    if isinstance(value, bool):
        return value
    if value is None or value == "":
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "是", "burn", "burned"}
    return bool(value)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _role_for_wallet(wallet: Mapping[str, Any]) -> str:
    tags = {str(t).lower() for t in wallet.get("tags", [])}
    if tags & INFRA_TAGS:
        return "INFRA_EXCLUDED"
    if "transfer_in" in tags:
        return "TOKEN_RECEIVER_FUNDING_PENDING"
    if "bundler" in tags and _num(wallet, "pnl_usd") > 0 and _num(wallet, "sold_usd") <= 0:
        return "HIGH_FLOATING_PROFIT_HOLDER"
    if "bundler" in tags and (_num(wallet, "pnl_usd") < 0 or _num(wallet, "unrealized_profit_usd") < 0):
        return "BAGHOLDER_OR_HIGH_ENTRY_CANDIDATE"
    if "sniper" in tags:
        return "EARLY_EXECUTION_CANDIDATE"
    if "bundler" in tags:
        return "STRUCTURE_EXECUTION_CANDIDATE"
    return "NORMAL_OR_UNCLASSIFIED"


def _wallet_profiles(sample_wallets: Iterable[Mapping[str, Any]]) -> list[Dict[str, Any]]:
    profiles = []
    for wallet in sample_wallets:
        role = _role_for_wallet(wallet)
        profiles.append({
            "address": str(wallet.get("address", "")),
            "role": role,
            "action_code": "I" if role == "INFRA_EXCLUDED" else ("R" if "BAGHOLDER" in role else "A2"),
            "keep_edges": role == "INFRA_EXCLUDED" or role.endswith("PENDING"),
            "tags": list(wallet.get("tags", [])),
            "holder_pct": _num(wallet, "holder_pct"),
            "pnl_usd": _num(wallet, "pnl_usd"),
            "reason": "基础设施排除普通钱包评分" if role == "INFRA_EXCLUDED" else "结构角色候选，需证据复查",
        })
    return profiles


def _score(snapshot: Mapping[str, Any]) -> Dict[str, Any]:
    holder_count = max(_num(snapshot, "holder_count"), 1.0)
    bundler = _num(snapshot, "bundler_wallet_count")
    sniper = _num(snapshot, "sniper_wallet_count")
    fresh = _num(snapshot, "fresh_wallet_count")
    smart = _num(snapshot, "smart_wallet_count")
    kol = _num(snapshot, "kol_wallet_count")
    top_bundler_pct = _num(snapshot, "top_bundler_trader_percentage_pct")
    entrapment_pct = _num(snapshot, "top_entrapment_trader_percentage_pct")
    bot_rate = _num(snapshot, "bot_degen_rate_pct")
    fresh_rate = _num(snapshot, "fresh_wallet_rate_pct", fresh / holder_count * 100.0)

    activity = min(100.0, 20 + min(25, bundler / holder_count * 100) + min(20, sniper / holder_count * 100)
                   + min(15, fresh / holder_count * 10) + min(10, smart / 5) + min(10, kol))
    early_strength_score = min(100.0, min(35, top_bundler_pct) + min(20, sniper / max(holder_count, 1) * 100)
                               + min(20, bundler / max(holder_count, 1) * 100) + min(15, bot_rate / 2) + 10)
    chase_risk = min(100.0, min(35, top_bundler_pct) + min(25, entrapment_pct * 2) + min(20, bot_rate / 2) + min(20, fresh_rate))

    return {
        "structure_activity_score": round(activity, 2),
        "early_execution_score": round(early_strength_score, 2),
        "chase_risk_score": round(chase_risk, 2),
        "early_execution_strength": "STRONG" if early_strength_score >= 55 else ("MEDIUM" if early_strength_score >= 35 else "LOW"),
        "chase_risk_level": "HIGH" if chase_risk >= 65 else ("MEDIUM" if chase_risk >= 40 else "LOW"),
    }


def convert_structural_snapshot(snapshot: Mapping[str, Any]) -> Dict[str, Any]:
    token = str(snapshot.get("token_address", ""))
    symbol = str(snapshot.get("token_symbol", ""))
    generated_at = str(snapshot.get("generated_at") or _now())
    scores = _score(snapshot)
    wallet_profiles = _wallet_profiles(snapshot.get("sample_wallets", []) or [])

    security_clean = (
        _bool(snapshot, "mint_renounced")
        and _bool(snapshot, "freeze_renounced")
        and _num(snapshot, "buy_tax_pct") == 0
        and _num(snapshot, "sell_tax_pct") == 0
        and _bool(snapshot, "lp_burned")
    )
    funding_traced = _bool(snapshot, "funding_traced")
    missing = [] if funding_traced else ["资金层跳过", "funding_path_missing"]

    hard_block = not security_clean or _num(snapshot, "liquidity_usd") < 10_000
    structural_pause = scores["chase_risk_level"] in {"MEDIUM", "HIGH"} or not funding_traced
    if hard_block:
        decision = "BLOCK"
        final_status = "RISK_MONITOR"
        signal_level = "SX"
        contract_permission = "BLOCK_BUY_禁止买入"
        wallet_status = "WALLET_BLOCK"
    elif structural_pause:
        decision = "OBSERVE_ONLY"
        final_status = "OBSERVE"
        signal_level = "S1"
        contract_permission = "PAUSE_NEED_CONFIRM_需要人工确认"
        wallet_status = "WALLET_PAUSE"
    else:
        decision = "PAPER_READY"
        final_status = "PAPER_CANDIDATE"
        signal_level = "S3"
        contract_permission = "ALLOW_PAPER_TRADE_允许纸面交易"
        wallet_status = "WALLET_SUPPORT"

    permission = "BLOCK_REAL_TRADE"
    token_intake = {
        "token_address": token,
        "token_symbol": symbol,
        "chain": snapshot.get("chain", "sol"),
        "source": "gmgn_sikk_structural_snapshot",
        "intake_time": generated_at,
    }
    structural_intel = {
        "token_address": token,
        "token_symbol": symbol,
        **scores,
        "bundler_pressure": _num(snapshot, "top_bundler_trader_percentage_pct"),
        "sniper_density": round(_num(snapshot, "sniper_wallet_count") / max(_num(snapshot, "holder_count"), 1.0) * 100, 4),
        "fresh_wallet_rate": _num(snapshot, "fresh_wallet_rate_pct"),
        "smart_kol_count": int(_num(snapshot, "smart_wallet_count") + _num(snapshot, "kol_wallet_count")),
        "holder_concentration": _num(snapshot, "top10_holder_rate_pct"),
        "wallet_profiles": wallet_profiles,
    }
    evidence_bundle = {
        "token_address": token,
        "security_permission_layer": "CLEAN" if security_clean else "RISK_OR_INCOMPLETE",
        "funding_status": "资金已追踪" if funding_traced else "资金待查",
        "missing_evidence": missing,
        "positive_evidence": ["权限层偏干净"] if security_clean else [],
        "negative_evidence": ["早期结构参与密集"] if scores["early_execution_strength"] == "STRONG" else [],
        "risk_evidence": [f"追高风险={scores['chase_risk_level']}", f"chase_risk_score={scores['chase_risk_score']}"],
    }
    trade_gate_decision = {
        "token_address": token,
        "final_status": final_status,
        "signal_level": signal_level,
        "decision": decision,
        "permission": permission,
        "contract_permission": contract_permission,
        "allowed_modes": ["observe", "paper"] if decision != "BLOCK" else ["observe"],
        "forbidden_modes": ["real_auto", "buy_now", "auto_trade", "sell_now"],
        "block_reasons": ["SECURITY_OR_LIQUIDITY_BLOCK"] if hard_block else [],
        "pause_reasons": ["STRUCTURAL_PAUSE", "FUNDING_PENDING"] if structural_pause else [],
        "allow_reasons": ["paper-only candidate"] if decision == "PAPER_READY" else [],
        "reason_codes": (["SECURITY_OR_LIQUIDITY_BLOCK"] if hard_block else []) + (["STRUCTURAL_PAUSE", "FUNDING_PENDING"] if structural_pause else []),
        "human_confirmation_required": decision != "BLOCK",
        "real_trade_enabled": False,
    }
    risk_control_profile = {
        "token_address": token,
        "risk_level": "HIGH" if hard_block else ("MEDIUM_HIGH" if structural_pause else "MEDIUM"),
        "real_trade_allowed": False,
        "max_position_sol": 0.0 if decision != "PAPER_READY" else 0.05,
        "kill_switch": True,
        "risk_notes": evidence_bundle["risk_evidence"] + missing,
    }
    execution_intent = {
        "token_address": token,
        "mode": "paper_only",
        "action": "OBSERVE" if decision != "PAPER_READY" else "PAPER_SIMULATE",
        "real_order": False,
        "broadcast_transaction": False,
    }
    review_writeback = {
        "token_address": token,
        "review_required": True,
        "review_windows": ["W1_0_60s", "W2_1_5m", "W3_5_30m", "W4_30m_2h"],
        "writeback_targets": ["trade_journal", "wallet_structure_decision", "planbook_gap_register"],
    }
    wallet_decision = {
        "token_address": token,
        "token_symbol": symbol,
        "wallet_structure_status": wallet_status,
        "wallet_structure_score": scores["structure_activity_score"],
        "wallet_risk_score": scores["chase_risk_score"],
        "counterparty_pressure_score": max(_num(snapshot, "top_entrapment_trader_percentage_pct") * 5, scores["chase_risk_score"] * 0.6),
        "data_quality_score": 65 if funding_traced else 45,
        "wallet_structure_factor": 1.0 if wallet_status == "WALLET_SUPPORT" else 0.75,
        "reason": "结构活跃但追高/资金证据不足，进入观察/纸面门控" if wallet_status != "WALLET_SUPPORT" else "结构证据暂可进入纸面模拟",
        "is_stale": False,
    }
    return {
        "token_intake": token_intake,
        "structural_intel": structural_intel,
        "evidence_bundle": evidence_bundle,
        "trade_gate_decision": trade_gate_decision,
        "risk_control_profile": risk_control_profile,
        "execution_intent": execution_intent,
        "review_writeback": review_writeback,
        "wallet_decision": wallet_decision,
    }


def write_runtime_outputs(result: Mapping[str, Any], output_dir: str | Path) -> Dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    mapping = {
        "token_intake": "token_intake.json",
        "structural_intel": "structural_intel_result.json",
        "evidence_bundle": "evidence_bundle.json",
        "trade_gate_decision": "trade_gate_decision.json",
        "risk_control_profile": "risk_control_profile.json",
        "execution_intent": "execution_intent.json",
        "review_writeback": "review_writeback.json",
        "wallet_decision": "wallet_structure_decision.json",
    }
    paths: Dict[str, str] = {}
    for key, filename in mapping.items():
        path = out / filename
        path.write_text(json.dumps(result[key], ensure_ascii=False, indent=2), encoding="utf-8")
        paths[key] = str(path)
    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert GMGN/SIKK structural snapshot to trade-gate runtime files")
    parser.add_argument("--input", required=True, help="structural snapshot JSON")
    parser.add_argument("--output-dir", required=True, help="runtime output directory")
    args = parser.parse_args()
    snapshot = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = convert_structural_snapshot(snapshot)
    paths = write_runtime_outputs(result, args.output_dir)
    print(json.dumps(paths, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
