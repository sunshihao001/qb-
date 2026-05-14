# -*- coding: utf-8 -*-
"""Minimal data loader for single-token personal replay.

Reads existing local artifacts first. It never fabricates unavailable facts;
missing fields are returned explicitly for downstream reports.
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA_ROOTS = [
    PROJECT_ROOT / "data" / "source_wallet_bot",
    PROJECT_ROOT / "data" / "gmgn_candidates_live_run",
    PROJECT_ROOT / "sikk_stable_trader_os" / "runtime_absorption",
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, default: Any = None) -> Any:
    if default is None:
        default = {}
    try:
        if not path.exists() or not path.is_file():
            return default
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    path.write_text(text + ("\n" if text else ""), encoding="utf-8")


def read_csv(path: Path) -> List[Dict[str, Any]]:
    if not path.exists() or not path.is_file():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def as_list(payload: Any) -> List[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ["rows", "results", "data", "tokens", "candidates", "处理结果", "候选状态", "候选结果", "wallets", "holders", "traders", "records", "list"]:
            value = payload.get(key)
            if isinstance(value, list):
                return value
        raw_payloads = payload.get("raw_payloads")
        if isinstance(raw_payloads, list):
            rows: List[Any] = []
            for item in raw_payloads:
                if isinstance(item, dict):
                    if isinstance(item.get("payload"), dict):
                        inner = item["payload"]
                        if isinstance(inner.get("list"), list):
                            rows.extend(inner["list"])
                        elif isinstance(inner.get("records"), list):
                            rows.extend(inner["records"])
                        else:
                            rows.append(inner)
                    else:
                        rows.append(item)
            if rows:
                return rows
    return []


def find_token_dirs(token: str, mode: str = "replay") -> List[Path]:
    roots = [PROJECT_ROOT / "data" / "source_wallet_bot"]
    modes = []
    for m in [mode, "live", "live_test", "paper", "replay", "ad_hoc", "backtest", "legacy"]:
        if m and m not in modes:
            modes.append(m)
    found: List[Path] = []
    for root in roots:
        for m in modes:
            candidate = root / m / token
            if candidate.exists() and candidate.is_dir():
                found.append(candidate)
    return found


def _path_matches_token(path: Path, token: str) -> bool:
    text = str(path)
    return token in text or any(part == token for part in path.parts)


def discover_existing_files(token: str, mode: str = "replay") -> List[Path]:
    candidates: List[Path] = []
    for d in find_token_dirs(token, mode):
        candidates.extend([p for p in d.rglob("*") if p.is_file() and p.suffix.lower() in {".json", ".jsonl", ".csv", ".md"}])
    # Bounded fallback for old runtime absorption only. Do not read reports/single_token_replay
    # as input, otherwise reruns contaminate facts with their own prior outputs.
    for base in [PROJECT_ROOT / "sikk_stable_trader_os" / "runtime_absorption"]:
        if base.exists():
            for p in base.rglob("*"):
                if p.is_file() and p.suffix.lower() in {".json", ".jsonl", ".csv", ".md"} and _path_matches_token(p, token):
                    candidates.append(p)
    # De-duplicate, newest first.
    uniq = {str(p): p for p in candidates}
    return sorted(uniq.values(), key=lambda p: p.stat().st_mtime if p.exists() else 0, reverse=True)


def load_records_from_file(path: Path) -> Tuple[str, Any]:
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json", read_json(path, {})
    if suffix == ".jsonl":
        rows = []
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
        except Exception:
            pass
        return "jsonl", rows
    if suffix == ".csv":
        return "csv", read_csv(path)
    if suffix == ".md":
        try:
            return "md", path.read_text(encoding="utf-8")[:20000]
        except Exception:
            return "md", ""
    return "unknown", None


def _extract_token_basic(payload: Any, token: str) -> Dict[str, Any]:
    if isinstance(payload, dict):
        out = {}
        for key in ["token_address", "address", "代币地址", "mint", "symbol", "代币符号", "name", "市值", "market_cap", "market_cap_usd", "liquidity", "liquidity_usd", "holder_count", "holders", "price", "price_usd"]:
            if key in payload and payload.get(key) not in (None, "", [], {}):
                out[key] = payload.get(key)
        for row in as_list(payload):
            if isinstance(row, dict) and str(row.get("token_address") or row.get("代币地址") or row.get("address") or row.get("mint") or "") == token:
                out.update(_extract_token_basic(row, token))
        return out
    return {}


def _looks_wallet_row(row: Dict[str, Any]) -> bool:
    keys = set(row)
    return bool(
        keys & {
            "wallet", "wallet_address", "address", "钱包地址", "holder_address", "owner",
            "gmgn_tags", "maker_token_tags", "funding_source_address", "role_candidates",
            "buy_amount_usd", "sell_amount_usd", "current_balance", "sold_pct", "remaining_pct",
            "first_buy_time", "last_buy_time", "last_sell_time", "pnl_multiple", "total_profit",
        }
    )


def _looks_kline_row(row: Dict[str, Any]) -> bool:
    keys = set(row)
    return bool(keys & {"open", "high", "low", "close", "volume", "timestamp", "time", "t"}) and not _looks_wallet_row(row)


def load_single_token_context(token: str, mode: str = "replay") -> Dict[str, Any]:
    files = discover_existing_files(token, mode)
    token_dirs = find_token_dirs(token, mode)
    context: Dict[str, Any] = {
        "token": token,
        "mode": mode,
        "loaded_at": utc_now(),
        "token_dirs": [str(p) for p in token_dirs],
        "source_files": [],
        "token_basic": {"token_address": token},
        "wallet_rows": [],
        "kline_rows": [],
        "quote_security": {},
        "paper_history": [],
        "raw_payloads": {},
        "missing_fields": [],
    }
    for path in files[:120]:
        kind, payload = load_records_from_file(path)
        rel = str(path.relative_to(PROJECT_ROOT)) if str(path).startswith(str(PROJECT_ROOT)) else str(path)
        context["source_files"].append({"path": rel, "kind": kind})
        lname = path.name.lower()
        if isinstance(payload, dict):
            context["token_basic"].update({k: v for k, v in _extract_token_basic(payload, token).items() if v not in (None, "", [], {})})
            if any(x in lname for x in ["quote", "security", "scan"]):
                if isinstance(payload, dict):
                    context["quote_security"].update(payload)
            rows = as_list(payload)
        elif kind in {"jsonl", "csv"}:
            rows = payload if isinstance(payload, list) else []
        else:
            rows = []
        if kind in {"json", "jsonl", "csv"}:
            context["raw_payloads"][rel] = payload
        for row in rows:
            if not isinstance(row, dict):
                continue
            if _looks_wallet_row(row):
                context["wallet_rows"].append(row)
            elif _looks_kline_row(row):
                context["kline_rows"].append(row)
            if any(x in lname for x in ["paper", "position", "trade", "review", "attribution"]):
                context["paper_history"].append(row)
    if not context["source_files"]:
        context["missing_fields"].append("local_token_data_files")
    if not context["wallet_rows"]:
        context["missing_fields"].append("wallet_rows")
    if not context["kline_rows"]:
        context["missing_fields"].append("kline_rows")
    if not context["quote_security"]:
        context["missing_fields"].append("quote_security")
    return context
