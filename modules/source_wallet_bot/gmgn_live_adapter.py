from __future__ import annotations

import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .io_utils import write_json
from .wallet_profile_normalizer import normalize_wallet_profile
from .wallet_trade_normalizer import normalize_wallet_trades
from .source_group_engine import build_same_source_groups
from .role_classifier import classify_wallet
from .handoff_exporter import build_handoff_packet
from .directory_governance import apply_directory_governance
from modules.wallet_data_guard import (
    SemanticLayer,
    build_source_manifest,
    scan_wallet_data_contamination,
    validate_source_manifest,
)


def _ts(value: Any) -> str:
    if value in (None, "", 0, "0"):
        return ""
    try:
        ts = float(value)
    except (TypeError, ValueError):
        return str(value)
    if ts > 10_000_000_000:
        ts /= 1000.0
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _num(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, "", [], {}):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _pct(value: Any) -> float:
    number = _num(value)
    if 0 <= number <= 1:
        return round(number * 100, 6)
    return round(number, 6)


def _run_gmgn_json(command: list[str], timeout: int = 90) -> dict[str, Any]:
    if command[:3] not in (["gmgn-cli", "token", "holders"], ["gmgn-cli", "token", "traders"]):
        raise ValueError(f"Source Wallet Bot GMGN adapter only allows readonly token holders/traders: {command}")
    forbidden = " ".join(command)
    for snippet in (" swap", " order", "execute", "broadcast", "sign"):
        if snippet in forbidden:
            raise ValueError(f"forbidden gmgn command snippet: {snippet}")
    completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=timeout)
    return json.loads((completed.stdout or "{}").strip() or "{}")


def collect_gmgn_token_wallet_rows(token_address: str, *, limit: int = 30, sleep_seconds: float = 0.25) -> dict[str, Any]:
    commands = [
        ["gmgn-cli", "token", "holders", "--chain", "sol", "--address", token_address, "--limit", str(limit), "--order-by", "amount_percentage", "--direction", "desc", "--raw"],
        ["gmgn-cli", "token", "traders", "--chain", "sol", "--address", token_address, "--limit", str(limit), "--order-by", "profit", "--direction", "desc", "--raw"],
        ["gmgn-cli", "token", "holders", "--chain", "sol", "--address", token_address, "--limit", str(min(limit, 20)), "--tag", "transfer_in", "--order-by", "amount_percentage", "--direction", "desc", "--raw"],
        ["gmgn-cli", "token", "holders", "--chain", "sol", "--address", token_address, "--limit", str(min(limit, 20)), "--tag", "bundler", "--order-by", "amount_percentage", "--direction", "desc", "--raw"],
        ["gmgn-cli", "token", "holders", "--chain", "sol", "--address", token_address, "--limit", str(min(limit, 20)), "--tag", "fresh_wallet", "--order-by", "amount_percentage", "--direction", "desc", "--raw"],
    ]
    raw_payloads = []
    by_address: dict[str, dict[str, Any]] = {}
    for command in commands:
        payload = _run_gmgn_json(command)
        raw_payloads.append({"command": command[:], "payload": payload})
        for row in payload.get("list", []) or []:
            address = row.get("address")
            if not address:
                continue
            merged = by_address.setdefault(str(address), dict(row))
            for key in ("tags", "maker_token_tags"):
                old_values = merged.get(key) or []
                new_values = row.get(key) or []
                merged[key] = sorted(set([*old_values, *new_values]))
            for k, v in row.items():
                if merged.get(k) in (None, "", [], {}) and v not in (None, "", [], {}):
                    merged[k] = v
        time.sleep(sleep_seconds)
    return {"raw_payloads": raw_payloads, "wallet_rows": list(by_address.values())}


def gmgn_holder_rows_to_trade_rows(token_address: str, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    trade_rows = []
    for row in rows:
        wallet = row.get("address") or row.get("wallet_address")
        if not wallet:
            continue
        buy_token_amount = _num(row.get("buy_amount_cur") or row.get("current_buy_amount") or row.get("accu_amount"))
        sell_token_amount = _num(row.get("sell_amount_cur") or row.get("current_sell_amount"))
        current_balance = _num(row.get("amount_cur") or row.get("balance"))
        buy_usd = _num(row.get("buy_volume_cur") or row.get("history_bought_cost") or row.get("cost"))
        sell_usd = _num(row.get("sell_volume_cur") or row.get("history_sold_income"))
        trade_rows.append({
            "token_address": token_address,
            "wallet_address": str(wallet),
            "side": "summary",
            "timestamp": _ts(row.get("last_active_timestamp") or row.get("start_holding_at")),
            "first_buy_time": _ts(row.get("start_holding_at")),
            "last_buy_time": _ts(row.get("start_holding_at")),
            "last_sell_time": _ts(row.get("end_holding_at")),
            "buy_count": int(_num(row.get("buy_tx_count_cur"))),
            "sell_count": int(_num(row.get("sell_tx_count_cur"))),
            "buy_amount_usd": buy_usd,
            "sell_amount_usd": sell_usd,
            "buy_token_amount": buy_token_amount,
            "sell_token_amount": sell_token_amount,
            "current_balance": current_balance,
            "sold_pct": _pct(row.get("sell_amount_percentage")),
            "remaining_pct": round(100 - _pct(row.get("sell_amount_percentage")), 6),
            "realized_profit": _num(row.get("realized_profit")),
            "unrealized_profit": _num(row.get("unrealized_profit")),
            "total_profit": _num(row.get("profit")),
            "pnl_multiple": _num(row.get("profit_change")),
            "avg_buy_price": _num(row.get("avg_cost")),
            "avg_sell_price": _num(row.get("avg_sold")),
            "source": "GMGN token holders/traders readonly",
        })
    return trade_rows


def gmgn_holder_rows_to_profile_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    profiles = []
    for row in rows:
        wallet = row.get("address") or row.get("wallet_address")
        if not wallet:
            continue
        native_transfer = row.get("native_transfer") if isinstance(row.get("native_transfer"), dict) else {}
        tags = sorted(set([*(row.get("tags") or []), *(row.get("maker_token_tags") or [])]))
        profiles.append({
            "wallet_address": str(wallet),
            "wallet_first_seen_time": _ts(row.get("created_at")),
            "wallet_last_active_time": _ts(row.get("last_active_timestamp")),
            "gmgn_tags": tags,
            "funding_source_address": native_transfer.get("from_address") or "missing",
            "total_token_count": "unknown",
            "traded_token_count": "unknown",
            "cross_token_reappearance": "unknown",
        })
    return profiles


def _write_wallet_data_guard_outputs(token_address: str, out: Path) -> dict[str, str]:
    manifest = build_source_manifest(
        source_id=f"gmgn_live_adapter:{token_address}",
        source_type="gmgn_live_adapter",
        token_address=token_address,
        raw_path=out / "wallet_data" / "raw",
        normalized_path=out / "wallet_data" / "normalized",
        allowed_layers=[SemanticLayer.RAW, SemanticLayer.NORMALIZED, SemanticLayer.FACTS],
        collector="modules.source_wallet_bot.gmgn_live_adapter",
        confidence="normalized",
    )
    manifest["validation"] = validate_source_manifest(manifest)
    manifest_path = write_json(out / "manifest" / "wallet_data_guard_source_manifest.json", manifest)
    scan_report = scan_wallet_data_contamination(out)
    scan_path = write_json(out / "verification" / "wallet_data_guard_contamination_scan.json", scan_report)
    return {
        "wallet_data_guard_manifest": str(manifest_path),
        "wallet_data_guard_scan_report": str(scan_path),
        "wallet_data_guard_status": str(scan_report.get("overall_status")),
    }


def collect_and_build_source_wallet_packet(token_address: str, output_dir: str | Path, *, limit: int = 30) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    collected = collect_gmgn_token_wallet_rows(token_address, limit=limit)
    raw_rows = collected["wallet_rows"]
    raw_path = write_json(out / "wallet_data" / "raw" / "gmgn_wallet_rows_raw.json", collected)
    trade_input = gmgn_holder_rows_to_trade_rows(token_address, raw_rows)
    profile_input = gmgn_holder_rows_to_profile_rows(raw_rows)
    trade_input_path = write_json(out / "wallet_data" / "raw" / "gmgn_wallet_trade_input.json", trade_input)
    profile_input_path = write_json(out / "wallet_data" / "raw" / "gmgn_wallet_profile_input.json", profile_input)
    trades = normalize_wallet_trades(trade_input)
    profiles = [normalize_wallet_profile(row) for row in profile_input]
    groups = build_same_source_groups(profiles, trades)
    profile_by_wallet = {p.wallet_address: p for p in profiles}
    decisions = [classify_wallet(t, profile_by_wallet.get(t.wallet_address), groups) for t in trades]
    packet = build_handoff_packet(token_address=token_address, wallet_trades=trades, wallet_profiles=profiles, source_groups=groups, decisions=decisions)
    trade_out = write_json(out / "wallet_data" / "normalized" / "wallet_trade_normalized.json", {"record_count": len(trades), "records": [t.to_dict() for t in trades]})
    profile_out = write_json(out / "wallet_data" / "normalized" / "wallet_entity_profile_normalized.json", {"record_count": len(profiles), "records": [p.to_dict() for p in profiles]})
    group_out = write_json(out / "structure_analysis" / "intelligence" / "same_source_evidence_normalized.json", {"record_count": len(groups), "records": [g.to_dict() for g in groups]})
    decision_out = write_json(out / "structure_analysis" / "intelligence" / "wallet_intelligence_decision.json", {"record_count": len(decisions), "records": [d.to_dict() for d in decisions]})
    handoff_out = write_json(out / "structure_analysis" / "handoff" / "bot2_handoff_packet.json", packet.to_dict())
    layout_paths = apply_directory_governance(token_address, out)
    guard_paths = _write_wallet_data_guard_outputs(token_address, out)
    return {
        "raw_path": str(raw_path),
        "trade_input_path": str(trade_input_path),
        "profile_input_path": str(profile_input_path),
        "wallet_trade_normalized": str(trade_out),
        "wallet_entity_profile_normalized": str(profile_out),
        "same_source_evidence_normalized": str(group_out),
        "wallet_intelligence_decision": str(decision_out),
        "bot2_handoff_packet": str(handoff_out),
        "directory_manifest": layout_paths["manifest"],
        "wallet_data_dir": layout_paths["wallet_data_dir"],
        "structure_analysis_dir": layout_paths["structure_analysis_dir"],
        "primary_write_layout": layout_paths["primary_write_layout"],
        **guard_paths,
    }
