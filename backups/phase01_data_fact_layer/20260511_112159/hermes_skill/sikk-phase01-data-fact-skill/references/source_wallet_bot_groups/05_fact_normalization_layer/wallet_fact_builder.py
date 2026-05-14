from __future__ import annotations

import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io_utils import write_json
from .path_resolver import load_records_with_priority


FORBIDDEN_TERMS = [
    "trade_allowed",
    "buy_signal",
    "sell_signal",
    "execute_now",
    "PAPER_READY",
    "BLOCKED",
]


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_records(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return payload
    return payload.get("records", []) or []


def _num(value: Any) -> float:
    try:
        if value in (None, "", "missing", "unknown", [], {}):
            return 0.0
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _bool_tag(tags: list[str], *names: str) -> bool:
    tag_set = {str(t).lower() for t in tags}
    return any(name.lower() in tag_set for name in names)


def _data_quality_score(row: dict[str, Any]) -> float:
    important = [
        "first_buy_time",
        "buy_amount_usd",
        "sell_amount_usd",
        "current_balance",
        "realized_profit",
        "unrealized_profit",
        "pnl_multiple",
    ]
    present = 0
    for field in important:
        if row.get(field) not in (None, "", "missing", "unknown"):
            present += 1
    return round(present / len(important), 4)


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _assert_no_forbidden_text(obj: Any) -> None:
    text = json.dumps(obj, ensure_ascii=False)
    found = [term for term in FORBIDDEN_TERMS if term in text]
    if found:
        raise ValueError(f"wallet_fact output contains forbidden terms: {found}")


def build_wallet_fact_package(token_address: str, token_dir: str | Path, *, output_subdir: str = "wallet_data") -> dict[str, str]:
    token_path = Path(token_dir)
    out = token_path / output_subdir
    out.mkdir(parents=True, exist_ok=True)
    generated_at = _now()

    trades, trades_resolve = load_records_with_priority("wallet_trade_normalized.json", token_address)
    profiles, profiles_resolve = load_records_with_priority("wallet_entity_profile_normalized.json", token_address)
    groups, groups_resolve = load_records_with_priority("same_source_evidence_normalized.json", token_address)
    decisions, decisions_resolve = load_records_with_priority("wallet_intelligence_decision.json", token_address)
    input_resolution = {
        "wallet_trade_normalized.json": trades_resolve.to_dict(),
        "wallet_entity_profile_normalized.json": profiles_resolve.to_dict(),
        "same_source_evidence_normalized.json": groups_resolve.to_dict(),
        "wallet_intelligence_decision.json": decisions_resolve.to_dict(),
    }

    profiles_by_wallet = {p.get("wallet_address"): p for p in profiles}
    decisions_by_wallet = {d.get("wallet_address"): d for d in decisions}

    wallet_structure = []
    for t in trades:
        wallet = t.get("wallet_address")
        p = profiles_by_wallet.get(wallet, {})
        d = decisions_by_wallet.get(wallet, {})
        tags = p.get("gmgn_tags") or []
        row = {
            "token_address": token_address,
            "wallet_address": wallet,
            "snapshot_time": generated_at,
            "source_name": "GMGN readonly + Source Wallet Bot normalized",
            "retrieved_at": generated_at,
            "normalized_at": generated_at,
            "first_buy_time": t.get("first_buy_time", "missing"),
            "buy_amount_total": t.get("buy_amount_usd", 0),
            "sell_amount_total": t.get("sell_amount_usd", 0),
            "current_balance": t.get("current_balance", "missing"),
            "holding_ratio": t.get("remaining_pct", "missing"),
            "exit_ratio": t.get("sold_pct", "missing"),
            "realized_profit": t.get("realized_profit", "unknown"),
            "unrealized_profit": t.get("unrealized_profit", "unknown"),
            "pnl_multiple": t.get("pnl_multiple", "unknown"),
            "gmgn_tags": tags,
            "is_fresh_wallet": _bool_tag(tags, "fresh_wallet"),
            "is_old_wallet": not _bool_tag(tags, "fresh_wallet") if tags else "unknown",
            "is_sniper": _bool_tag(tags, "sniper"),
            "is_bundle": _bool_tag(tags, "bundler", "bundle"),
            "is_insider": _bool_tag(tags, "insider"),
            "is_whale": _bool_tag(tags, "whale", "top_holder"),
            "funding_source_address": p.get("funding_source_address", "missing"),
            "role_candidates": d.get("role_candidates", ["证据不足"]),
            "evidence_level": d.get("evidence_level", p.get("evidence_level", "E0")),
            "risk_level": d.get("risk_level", "R0"),
            "data_quality_score": _data_quality_score(t),
        }
        wallet_structure.append(row)

    role_counter = Counter()
    for row in wallet_structure:
        for role in row.get("role_candidates", []):
            role_counter[role] += 1
    balances = sorted([_num(row.get("current_balance")) for row in wallet_structure], reverse=True)
    top10_sum = sum(balances[:10])
    total_balance = sum(balances)
    summary = {
        "token_address": token_address,
        "snapshot_time": generated_at,
        "wallet_count": len(wallet_structure),
        "holder_count": len(wallet_structure),
        "total_current_balance": round(total_balance, 6),
        "full_exit_wallet_count": sum(1 for t in trades if t.get("is_full_exit") is True),
        "partial_exit_wallet_count": sum(1 for t in trades if t.get("is_partial_exit") is True),
        "same_source_group_count": len(groups),
        "same_source_group_wallet_count": sum(len(g.get("group_wallets", [])) for g in groups),
        "result_wallet_candidate_count": role_counter.get("疑似结果钱包", 0),
        "counterparty_whale_candidate_count": role_counter.get("疑似接盘鲸鱼", 0),
        "structure_wallet_candidate_count": role_counter.get("疑似结构执行钱包", 0),
        "top_wallet_balance": balances[0] if balances else 0,
        "top10_wallet_balance_sum": round(top10_sum, 6),
        "top10_wallet_balance_pct_of_tracked": round(top10_sum / total_balance * 100, 6) if total_balance else 0,
        "chip_concentration_level": "high" if total_balance and top10_sum / total_balance >= 0.5 else "medium_or_unknown",
        "chip_transfer_status": "字段缺失/需要链上补查" if not groups else "存在疑似同源/分发线索",
        "role_counter": dict(role_counter),
        "data_quality_score": round(sum(row["data_quality_score"] for row in wallet_structure) / len(wallet_structure), 4) if wallet_structure else 0,
    }

    same_source_groups = []
    for g in groups:
        same_source_groups.append({
            "token_address": token_address,
            "group_id": g.get("same_source_group_id") or g.get("group_id"),
            "source_address": g.get("shared_funding_source", "missing"),
            "member_count": len(g.get("group_wallets", [])),
            "member_addresses": g.get("group_wallets", []),
            "evidence_level": g.get("evidence_level", "E0"),
            "risk_level": g.get("risk_level", "R0"),
            "group_confidence": g.get("confidence_score", "unknown"),
            "evidence_basis": g.get("evidence_basis", ["疑似同源执行组"]),
        })

    fund_edges = []
    for row in wallet_structure:
        src = row.get("funding_source_address")
        dst = row.get("wallet_address")
        if src not in (None, "", "missing", "unknown") and dst:
            fund_edges.append({
                "token_address": token_address,
                "from_address": src,
                "to_address": dst,
                "asset": "SOL/USDC unknown",
                "amount": "unknown",
                "transfer_time": "unknown",
                "relation_type": "pre_buy_funding_candidate",
                "source_type": "GMGN native_transfer L1",
                "confidence_score": 0.6,
                "evidence_note": "疑似资金来源候选；金额/时间需要链上补查",
            })

    address_history = []
    for row in wallet_structure:
        roles = row.get("role_candidates", [])
        pnl = _num(row.get("pnl_multiple"))
        address_history.append({
            "wallet_address": row.get("wallet_address"),
            "appeared_token_count": 1,
            "appeared_tokens": [token_address],
            "role_history": roles,
            "profitable_token_count": 1 if _num(row.get("realized_profit")) + _num(row.get("unrealized_profit")) > 0 else 0,
            "losing_token_count": 1 if _num(row.get("realized_profit")) + _num(row.get("unrealized_profit")) < 0 else 0,
            "avg_roi": pnl,
            "max_roi": pnl,
            "repeated_source_addresses": [row.get("funding_source_address")] if row.get("funding_source_address") not in (None, "", "missing", "unknown") else [],
            "repeated_backflow_addresses": [],
            "current_persona": roles[0] if roles else "证据不足",
            "evidence_score": row.get("evidence_level"),
            "risk_score": row.get("risk_level"),
            "tracking_level": "watch" if row.get("evidence_level") in ("E2", "E3", "E4") else "low",
            "last_seen_time": generated_at,
        })

    manifest = {
        "token_address": token_address,
        "generated_at": generated_at,
        "module": "source_wallet_bot.wallet_fact",
        "input_files": [
            "wallet_trade_normalized.json",
            "wallet_entity_profile_normalized.json",
            "same_source_evidence_normalized.json",
            "wallet_intelligence_decision.json",
        ],
        "input_resolution": input_resolution,
        "output_files": [
            "wallet_structure_normalized.json",
            "chip_distribution_summary.json",
            "same_source_groups.json",
            "fund_flow_edges.csv",
            "address_history.json",
            "wallet_fact_report.md",
        ],
        "source_levels": ["L1", "L2"],
        "record_counts": {
            "wallet_structure": len(wallet_structure),
            "same_source_groups": len(same_source_groups),
            "fund_flow_edges": len(fund_edges),
            "address_history": len(address_history),
        },
        "safety_boundaries": ["no_state_machine", "no_paper_runner", "no_real_execution", "no_signing", "no_broadcast", "no_swap"],
    }

    report = _build_report(token_address, summary, manifest)
    payloads = [wallet_structure, summary, same_source_groups, fund_edges, address_history, manifest, report]
    _assert_no_forbidden_text(payloads)

    paths = {
        "wallet_structure_normalized": str(write_json(out / "wallet_structure_normalized.json", {"record_count": len(wallet_structure), "records": wallet_structure})),
        "chip_distribution_summary": str(write_json(out / "chip_distribution_summary.json", summary)),
        "same_source_groups": str(write_json(out / "same_source_groups.json", {"record_count": len(same_source_groups), "records": same_source_groups})),
        "fund_flow_edges": str(out / "fund_flow_edges.csv"),
        "address_history": str(write_json(out / "address_history.json", {"record_count": len(address_history), "records": address_history})),
        "wallet_fact_package_manifest": str(write_json(out / "wallet_fact_package_manifest.json", manifest)),
        "wallet_fact_report": str(out / "wallet_fact_report.md"),
    }
    _write_csv(Path(paths["fund_flow_edges"]), fund_edges)
    Path(paths["wallet_fact_report"]).write_text(report, encoding="utf-8")
    return paths


def _build_report(token_address: str, summary: dict[str, Any], manifest: dict[str, Any]) -> str:
    lines = [
        "# wallet_fact_report",
        "",
        f"token_address: `{token_address}`",
        "",
        "## 总体统计",
        f"- wallet_count: {summary['wallet_count']}",
        f"- same_source_group_count: {summary['same_source_group_count']}",
        f"- same_source_group_wallet_count: {summary['same_source_group_wallet_count']}",
        f"- total_current_balance: {summary['total_current_balance']}",
        f"- top10_wallet_balance_pct_of_tracked: {summary['top10_wallet_balance_pct_of_tracked']}",
        f"- data_quality_score: {summary['data_quality_score']}",
        "",
        "## 角色候选统计",
    ]
    for role, count in summary.get("role_counter", {}).items():
        lines.append(f"- {role}: {count}")
    lines.extend([
        "",
        "## 筹码结构摘要",
        f"- chip_concentration_level: {summary['chip_concentration_level']}",
        f"- chip_transfer_status: {summary['chip_transfer_status']}",
        f"- full_exit_wallet_count: {summary['full_exit_wallet_count']}",
        f"- partial_exit_wallet_count: {summary['partial_exit_wallet_count']}",
        "",
        "## 字段缺口 / 下一步",
        "- Class 5 Token transfer source: 需要链上补查以区分主动买入 / Token 转入 / 分发接收 / 空投接收。",
        "- Class 6 Funding source: GMGN native_transfer 可作候选，金额和时间仍需链上确认。",
        "- Class 7 Backflow: 需要从 sell tx/time 向后追踪 24h/72h 回流路径。",
        "- Class 10 Snapshot delta: 需要多快照才能计算 holder_delta。",
        "- Class 11 Quote/security: 需要 OKX quote/security scan 补充当前条件背景。",
        "",
        "## 安全边界",
    ])
    for item in manifest.get("safety_boundaries", []):
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"
