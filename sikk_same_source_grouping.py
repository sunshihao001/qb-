#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-SOL same-source grouping and sync score helpers.

v1.1 目标：把钱包结构门禁从单钱包静态判断，升级为：
- 疑似同源组 / 行为同步组生成
- sync_buy_score / sync_sell_score
- CEX/路由器/公共地址降权

边界：本模块只生成结构证据，不证明“同一控制人”，不执行真实交易。
"""

from __future__ import annotations

import csv
import hashlib
import math
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, Iterable, List, Set, Tuple

CANDIDATE_GROUP_FIELDS = [
    "token_address",
    "group_id",
    "group_type",
    "group_size",
    "wallets",
    "primary_evidence",
    "source_reliability",
    "avg_entry_rank",
    "entry_time_span_sec",
    "avg_buy_amount_usd",
    "buy_amount_cv",
    "sync_buy_score",
    "sync_sell_score",
    "group_remaining_pct",
    "group_sold_pct",
    "group_risk_level",
    "group_evidence_level",
    "reason",
]

PUBLIC_SOURCE_KEYWORDS = [
    "cex",
    "okx",
    "binance",
    "bybit",
    "coinbase",
    "kraken",
    "jupiter",
    "raydium",
    "orca",
    "meteora",
    "router",
    "aggregator",
    "hot wallet",
    "exchange",
]


def _text(row: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            return str(value)
    return ""


def _num(row: Dict[str, Any], *keys: str, default: float = 0.0) -> float:
    for key in keys:
        value = row.get(key)
        if value in (None, ""):
            continue
        try:
            return float(str(value).strip().rstrip("%"))
        except (TypeError, ValueError):
            continue
    return default


def _parse_time(value: Any) -> float | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        # Treat large timestamps as ms.
        return float(value) / 1000.0 if float(value) > 10_000_000_000 else float(value)
    text = str(value).strip()
    if not text:
        return None
    try:
        if text.endswith("Z"):
            return datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp()
        return datetime.fromisoformat(text).replace(tzinfo=timezone.utc).timestamp()
    except ValueError:
        return None


def _cv(values: List[float]) -> float:
    clean = [float(v) for v in values if float(v) > 0]
    if len(clean) <= 1:
        return 0.0
    m = mean(clean)
    if m == 0:
        return 0.0
    return pstdev(clean) / m


def _source_reliability(row: Dict[str, Any]) -> str:
    source = _text(row, "funding_source_address", "资金来源")
    label = _text(row, "funding_source_label", "funding_label", "资金来源标签")
    blob = f"{source} {label}".lower()
    if not source:
        return "UNKNOWN"
    if any(keyword in blob for keyword in PUBLIC_SOURCE_KEYWORDS):
        return "LOW"
    return "HIGH"


def _funding_time_close(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    ta = _parse_time(_text(a, "first_funding_time", "funding_time"))
    tb = _parse_time(_text(b, "first_funding_time", "funding_time"))
    if ta is None or tb is None:
        return False
    return abs(ta - tb) <= 10 * 60


def _entry_time_close(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    ta = _parse_time(_text(a, "entry_time", "first_buy_time"))
    tb = _parse_time(_text(b, "entry_time", "first_buy_time"))
    if ta is None or tb is None:
        return False
    return abs(ta - tb) <= 5 * 60


def _relative_close(x: float, y: float, tolerance: float = 0.35) -> bool:
    if x <= 0 or y <= 0:
        return False
    return abs(x - y) / max((x + y) / 2.0, 1e-9) <= tolerance


def same_source_similarity_score(a: Dict[str, Any], b: Dict[str, Any]) -> int:
    """Pairwise similarity, max 100."""

    score = 0
    fa = _text(a, "funding_source_address")
    fb = _text(b, "funding_source_address")
    if fa and fb and fa == fb:
        score += 40
    if _funding_time_close(a, b):
        score += 15
    if _relative_close(_num(a, "first_funding_amount_sol"), _num(b, "first_funding_amount_sol")):
        score += 10
    if _entry_time_close(a, b):
        score += 15
    if _relative_close(_num(a, "buy_amount_usd"), _num(b, "buy_amount_usd")):
        score += 10
    sold_close = _relative_close(_num(a, "sold_pct", "sold_percentage"), _num(b, "sold_pct", "sold_percentage"), tolerance=0.5)
    remain_close = _relative_close(_num(a, "remaining_pct"), _num(b, "remaining_pct"), tolerance=0.5)
    if sold_close or remain_close:
        score += 10
    return min(score, 100)


def _connected_components(wallets: List[Dict[str, Any]]) -> List[List[int]]:
    parent = list(range(len(wallets)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(len(wallets)):
        for j in range(i + 1, len(wallets)):
            score = same_source_similarity_score(wallets[i], wallets[j])
            no_funding_pair = not _text(wallets[i], "funding_source_address") and not _text(wallets[j], "funding_source_address")
            if score >= 70 or (no_funding_pair and score >= 35):
                union(i, j)

    groups: Dict[int, List[int]] = {}
    for idx in range(len(wallets)):
        groups.setdefault(find(idx), []).append(idx)
    return [members for members in groups.values() if len(members) >= 3]


def _time_span_sec(rows: List[Dict[str, Any]], key: str) -> float:
    times = [_parse_time(_text(row, key)) for row in rows]
    clean = [t for t in times if t is not None]
    if len(clean) <= 1:
        return 0.0
    return max(clean) - min(clean)


def _entry_rank_span(rows: List[Dict[str, Any]]) -> float:
    ranks = [_num(row, "entry_rank", default=0.0) for row in rows]
    ranks = [r for r in ranks if r > 0]
    if len(ranks) <= 1:
        return 0.0
    return max(ranks) - min(ranks)


def _score_by_threshold(value: float, rules: List[Tuple[float, int]]) -> int:
    for threshold, score in rules:
        if value <= threshold:
            return score
    return 0


def _funding_group_type(rows: List[Dict[str, Any]]) -> Tuple[str, str, str]:
    reliabilities = [_source_reliability(row) for row in rows]
    sources = [_text(row, "funding_source_address") for row in rows]
    non_empty_sources = [s for s in sources if s]
    same_source = bool(non_empty_sources) and len(set(non_empty_sources)) == 1

    if same_source and all(r == "HIGH" for r in reliabilities):
        return "FUNDING_STRONG_GROUP", "HIGH", "共同非公共资金源 + 入场/行为相似"
    if same_source and any(r == "LOW" for r in reliabilities):
        return "CEX_AMBIGUOUS_GROUP", "LOW", "共同来源为 CEX/路由器/公共地址，不强判同源"
    if non_empty_sources:
        return "FUNDING_WEAK_GROUP", "MEDIUM", "资金来源相似但非强确认"
    return "BEHAVIOR_SYNC_GROUP", "UNKNOWN", "行为同步候选，资金层待查"


def compute_sync_buy_score(rows: List[Dict[str, Any]], group_type: str) -> int:
    entry_span = _time_span_sec(rows, "entry_time")
    buy_time_score = _score_by_threshold(entry_span, [(30, 30), (120, 24), (300, 16), (600, 8)])
    rank_span = _entry_rank_span(rows)
    rank_score = _score_by_threshold(rank_span, [(10, 20), (25, 15), (50, 8)])
    buy_values = [_num(row, "buy_amount_usd", default=0.0) for row in rows]
    buy_cv = _cv(buy_values)
    amount_score = _score_by_threshold(buy_cv, [(0.25, 15), (0.50, 10), (1.00, 5)])
    participation = sum(1 for value in buy_values if value > 0) / max(len(rows), 1)
    if participation >= 0.9:
        participation_score = 20
    elif participation >= 0.7:
        participation_score = 14
    elif participation >= 0.5:
        participation_score = 8
    else:
        participation_score = 0
    funding_score = {
        "FUNDING_STRONG_GROUP": 15,
        "FUNDING_WEAK_GROUP": 8,
        "BEHAVIOR_SYNC_GROUP": 3,
        "CEX_AMBIGUOUS_GROUP": 0,
        "UNKNOWN_GROUP": 0,
    }.get(group_type, 0)
    return min(100, buy_time_score + rank_score + amount_score + participation_score + funding_score)


def compute_sync_sell_score(rows: List[Dict[str, Any]]) -> int:
    sell_rows = [row for row in rows if _num(row, "sold_pct", default=0.0) >= 20]
    sell_span = _time_span_sec(sell_rows, "sell_time") if sell_rows else 10**9
    time_score = _score_by_threshold(sell_span, [(60, 30), (300, 22), (900, 12), (1800, 6)])
    participation = len(sell_rows) / max(len(rows), 1)
    if participation >= 0.9:
        participation_score = 25
    elif participation >= 0.7:
        participation_score = 18
    elif participation >= 0.5:
        participation_score = 10
    else:
        participation_score = 0
    sold_values = [_num(row, "sold_pct", default=0.0) for row in sell_rows]
    sold_cv = _cv(sold_values)
    similarity_score = _score_by_threshold(sold_cv, [(0.25, 15), (0.50, 10), (1.00, 5)]) if sell_rows else 0
    group_sold_pct = mean([_num(row, "sold_pct", default=0.0) for row in rows]) if rows else 0.0
    if group_sold_pct >= 80:
        exit_score = 20
    elif group_sold_pct >= 60:
        exit_score = 15
    elif group_sold_pct >= 40:
        exit_score = 8
    else:
        exit_score = 0
    top_bonus = 0
    for row in rows:
        if bool(row.get("is_top_holder")) and _num(row, "sold_pct", default=0.0) >= 60:
            top_bonus = 10
            break
        if bool(row.get("is_top_holder")) and _num(row, "sold_pct", default=0.0) >= 30:
            top_bonus = max(top_bonus, 5)
    return min(100, time_score + participation_score + similarity_score + exit_score + top_bonus)


def _group_id(token_symbol: str, token_address: str, rows: List[Dict[str, Any]]) -> str:
    primary_source = _text(rows[0], "funding_source_address") or "NOFUND"
    first_entry = min((_parse_time(_text(row, "entry_time")) or 0 for row in rows), default=0)
    seed = f"{token_address}|{primary_source}|{int(first_entry // 60)}"
    digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()[:6]
    safe_symbol = "".join(ch for ch in (token_symbol or "TOKEN") if ch.isalnum())[:12] or "TOKEN"
    return f"SSG_{safe_symbol}_{digest}"


def _risk_level(sync_buy_score: int, sync_sell_score: int) -> str:
    if sync_sell_score >= 70:
        return "WALLET_BLOCK"
    if sync_sell_score >= 60:
        return "WALLET_PAUSE"
    if sync_buy_score >= 70 and sync_sell_score < 40:
        return "STRUCTURE_SUPPORT"
    if sync_buy_score >= 70 and sync_sell_score >= 50:
        return "RISK_WATCH"
    return "NEUTRAL"


def _evidence_level(group_type: str, sync_buy_score: int, sync_sell_score: int) -> str:
    if group_type == "CEX_AMBIGUOUS_GROUP":
        return "E1"
    if sync_sell_score >= 70:
        return "R3"
    if group_type == "FUNDING_STRONG_GROUP" and sync_buy_score >= 80:
        return "E4"
    if sync_buy_score >= 60:
        return "E3"
    return "E2"


def _group_row(token_address: str, token_symbol: str, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    group_type, reliability, evidence = _funding_group_type(rows)
    sync_buy = compute_sync_buy_score(rows, group_type)
    sync_sell = compute_sync_sell_score(rows)
    buy_values = [_num(row, "buy_amount_usd", default=0.0) for row in rows]
    sold_values = [_num(row, "sold_pct", default=0.0) for row in rows]
    remaining_values = [_num(row, "remaining_pct", default=0.0) for row in rows]
    ranks = [_num(row, "entry_rank", default=0.0) for row in rows if _num(row, "entry_rank", default=0.0) > 0]
    wallets = [_text(row, "wallet_address", "address", "钱包地址") for row in rows]
    reason = evidence
    if group_type == "CEX_AMBIGUOUS_GROUP":
        reason += "；公共资金源降权，不强判同源"
    elif group_type == "BEHAVIOR_SYNC_GROUP":
        reason += "；行为同步，资金层待查"
    if sync_sell >= 70:
        reason += "；sync_sell_score>=70，钱包结构门禁应阻断"
    return {
        "token_address": token_address,
        "group_id": _group_id(token_symbol, token_address, rows),
        "group_type": group_type,
        "group_size": len(rows),
        "wallets": ";".join(wallets),
        "primary_evidence": evidence,
        "source_reliability": reliability,
        "avg_entry_rank": round(mean(ranks), 4) if ranks else 0,
        "entry_time_span_sec": round(_time_span_sec(rows, "entry_time"), 4),
        "avg_buy_amount_usd": round(mean([v for v in buy_values if v > 0]), 4) if any(v > 0 for v in buy_values) else 0,
        "buy_amount_cv": round(_cv(buy_values), 6),
        "sync_buy_score": sync_buy,
        "sync_sell_score": sync_sell,
        "group_remaining_pct": round(mean(remaining_values), 4) if remaining_values else 0,
        "group_sold_pct": round(mean(sold_values), 4) if sold_values else 0,
        "group_risk_level": _risk_level(sync_buy, sync_sell),
        "group_evidence_level": _evidence_level(group_type, sync_buy, sync_sell),
        "reason": reason,
    }


def build_same_source_groups(*, token_address: str, token_symbol: str = "", wallet_rows: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    wallets = [dict(row) for row in wallet_rows]
    components = _connected_components(wallets)
    groups = [_group_row(token_address, token_symbol, [wallets[idx] for idx in component]) for component in components]
    groups.sort(key=lambda row: (row["group_risk_level"] != "WALLET_BLOCK", -row["sync_buy_score"], row["group_id"]))
    return groups


def write_candidate_groups_csv(path: str | Path, groups: Iterable[Dict[str, Any]]) -> None:
    rows = list(groups)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CANDIDATE_GROUP_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in CANDIDATE_GROUP_FIELDS})
