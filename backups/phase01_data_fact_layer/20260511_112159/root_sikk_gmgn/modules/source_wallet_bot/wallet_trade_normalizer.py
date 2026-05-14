from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Iterable

from .models import MISSING, UNKNOWN, WalletTradeRecord

REQUIRED_TRADE_FIELDS = [
    "token_address",
    "wallet_address",
    "first_buy_time",
    "last_buy_time",
    "last_sell_time",
    "buy_count",
    "sell_count",
    "buy_amount_sol",
    "buy_amount_usd",
    "buy_token_amount",
    "sell_amount_sol",
    "sell_amount_usd",
    "sell_token_amount",
    "avg_buy_price",
    "avg_sell_price",
    "current_balance",
    "sold_pct",
    "remaining_pct",
    "realized_profit",
    "unrealized_profit",
    "total_profit",
    "pnl_multiple",
    "holding_duration_seconds",
    "is_full_exit",
    "is_partial_exit",
]


def _num(row: dict[str, Any], *keys: str) -> float:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", MISSING, UNKNOWN):
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    return 0.0


def _timestamp(row: dict[str, Any]) -> str | None:
    for key in ("timestamp", "time", "block_time", "swap_time"):
        value = row.get(key)
        if value:
            return str(value)
    return None


def _parse_ts(value: str | None) -> datetime | None:
    if not value or value == MISSING:
        return None
    text = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def _round(value: float) -> float:
    return round(value, 6)


def normalize_wallet_trades(
    rows: Iterable[dict[str, Any]],
    *,
    current_prices_usd: dict[tuple[str, str], float] | None = None,
) -> list[WalletTradeRecord]:
    current_prices_usd = current_prices_usd or {}
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    incomplete: list[dict[str, Any]] = []
    for row in rows:
        token = row.get("token_address") or row.get("token")
        wallet = row.get("wallet_address") or row.get("wallet") or row.get("address")
        if token and wallet:
            grouped[(str(token), str(wallet))].append(row)
        else:
            incomplete.append(row)

    records: list[WalletTradeRecord] = []
    for (token, wallet), group in sorted(grouped.items()):
        summary_rows = [r for r in group if str(r.get("side") or r.get("trade_type") or "").lower() == "summary"]
        if summary_rows:
            r = summary_rows[0]
            missing_fields = []
            first_time = r.get("first_buy_time") or _timestamp(r) or MISSING
            last_buy = r.get("last_buy_time") or first_time
            last_sell = r.get("last_sell_time") or MISSING
            if not first_time or first_time == MISSING:
                missing_fields.append("first_buy_time")
                first_time = MISSING
            buy_token_amount = _num(r, "buy_token_amount")
            sell_token_amount = _num(r, "sell_token_amount")
            current_balance_value = r.get("current_balance") if r.get("current_balance") not in (None, "") else (buy_token_amount - sell_token_amount if buy_token_amount else MISSING)
            start_dt = _parse_ts(first_time)
            end_dt = _parse_ts(last_sell if last_sell not in (None, "", MISSING) else last_buy)
            holding_duration = int((end_dt - start_dt).total_seconds()) if start_dt and end_dt else MISSING
            records.append(
                WalletTradeRecord(
                    token_address=token,
                    wallet_address=wallet,
                    first_buy_time=first_time,
                    last_buy_time=last_buy or MISSING,
                    last_sell_time=last_sell or MISSING,
                    buy_count=int(_num(r, "buy_count")),
                    sell_count=int(_num(r, "sell_count")),
                    buy_amount_sol=_round(_num(r, "buy_amount_sol")),
                    buy_amount_usd=_round(_num(r, "buy_amount_usd")),
                    buy_token_amount=_round(buy_token_amount) if buy_token_amount else MISSING,
                    sell_amount_sol=_round(_num(r, "sell_amount_sol")),
                    sell_amount_usd=_round(_num(r, "sell_amount_usd")),
                    sell_token_amount=_round(sell_token_amount),
                    avg_buy_price=_round(_num(r, "avg_buy_price")) if r.get("avg_buy_price") not in (None, "", MISSING, UNKNOWN) else MISSING,
                    avg_sell_price=_round(_num(r, "avg_sell_price")) if r.get("avg_sell_price") not in (None, "", MISSING, UNKNOWN) else MISSING,
                    current_balance=_round(float(current_balance_value)) if current_balance_value not in (None, "", MISSING, UNKNOWN) else MISSING,
                    sold_pct=_round(_num(r, "sold_pct")) if r.get("sold_pct") not in (None, "", MISSING, UNKNOWN) else MISSING,
                    remaining_pct=_round(_num(r, "remaining_pct")) if r.get("remaining_pct") not in (None, "", MISSING, UNKNOWN) else MISSING,
                    realized_profit=_round(_num(r, "realized_profit")) if r.get("realized_profit") not in (None, "", MISSING, UNKNOWN) else UNKNOWN,
                    unrealized_profit=_round(_num(r, "unrealized_profit")) if r.get("unrealized_profit") not in (None, "", MISSING, UNKNOWN) else UNKNOWN,
                    total_profit=_round(_num(r, "total_profit")) if r.get("total_profit") not in (None, "", MISSING, UNKNOWN) else UNKNOWN,
                    pnl_multiple=_round(_num(r, "pnl_multiple")) if r.get("pnl_multiple") not in (None, "", MISSING, UNKNOWN) else UNKNOWN,
                    holding_duration_seconds=holding_duration,
                    is_full_exit=bool(buy_token_amount and float(current_balance_value or 0) <= 0.000001) if current_balance_value not in (MISSING, UNKNOWN, None, "") else MISSING,
                    is_partial_exit=bool(sell_token_amount > 0 and current_balance_value not in (MISSING, UNKNOWN, None, "") and float(current_balance_value) > 0),
                    source_names=["GMGN token holders/traders readonly summary"],
                    missing_fields=sorted(set(missing_fields)),
                    evidence_notes=["GMGN summary row from L1 readonly holders/traders; no dashboard/paper/report backfill"],
                )
            )
            continue
        buys = [r for r in group if str(r.get("side") or r.get("trade_type") or "").lower() == "buy"]
        sells = [r for r in group if str(r.get("side") or r.get("trade_type") or "").lower() == "sell"]
        buy_times = sorted([t for t in (_timestamp(r) for r in buys) if t])
        sell_times = sorted([t for t in (_timestamp(r) for r in sells) if t])

        buy_amount_sol = sum(_num(r, "amount_sol", "sol_amount", "buy_amount_sol") for r in buys)
        buy_amount_usd = sum(_num(r, "amount_usd", "usd_amount", "buy_amount_usd") for r in buys)
        buy_token_amount = sum(_num(r, "token_amount", "buy_token_amount", "amount_token") for r in buys)
        sell_amount_sol = sum(_num(r, "amount_sol", "sol_amount", "sell_amount_sol") for r in sells)
        sell_amount_usd = sum(_num(r, "amount_usd", "usd_amount", "sell_amount_usd") for r in sells)
        sell_token_amount = sum(_num(r, "token_amount", "sell_token_amount", "amount_token") for r in sells)

        missing_fields: list[str] = []
        for r in group:
            if not _timestamp(r):
                missing_fields.append("timestamp")
        if not buy_times:
            missing_fields.append("first_buy_time")
        if buy_token_amount == 0:
            missing_fields.append("buy_token_amount")

        current_balance_value = buy_token_amount - sell_token_amount if buy_token_amount else MISSING
        sold_pct = _round((sell_token_amount / buy_token_amount) * 100) if buy_token_amount else MISSING
        remaining_pct = _round(100 - sold_pct) if isinstance(sold_pct, float) else MISSING
        avg_buy_price = _round(buy_amount_usd / buy_token_amount) if buy_token_amount else MISSING
        avg_sell_price = _round(sell_amount_usd / sell_token_amount) if sell_token_amount else MISSING

        cost_basis_sold = (buy_amount_usd / buy_token_amount * sell_token_amount) if buy_token_amount else 0.0
        realized_profit = _round(sell_amount_usd - cost_basis_sold) if sells and buy_token_amount else UNKNOWN
        price = current_prices_usd.get((token, wallet))
        requires_followup_fields: list[str] = []
        if price is None and buys:
            requires_followup_fields.append("current_price_usd")
        unrealized_profit = UNKNOWN
        if price is not None and isinstance(current_balance_value, float):
            remaining_cost = (buy_amount_usd / buy_token_amount * current_balance_value) if buy_token_amount else 0.0
            unrealized_profit = _round((current_balance_value * price) - remaining_cost)
        total_profit = UNKNOWN
        if isinstance(realized_profit, float) and isinstance(unrealized_profit, float):
            total_profit = _round(realized_profit + unrealized_profit)
        elif isinstance(realized_profit, float) and not requires_followup_fields:
            total_profit = realized_profit
        pnl_multiple = UNKNOWN
        if isinstance(total_profit, float) and buy_amount_usd:
            pnl_multiple = _round((buy_amount_usd + total_profit) / buy_amount_usd)

        first_time = buy_times[0] if buy_times else MISSING
        last_sell = sell_times[-1] if sell_times else MISSING
        start_dt = _parse_ts(first_time)
        end_dt = _parse_ts(last_sell if last_sell != MISSING else (buy_times[-1] if buy_times else None))
        holding_duration = int((end_dt - start_dt).total_seconds()) if start_dt and end_dt else MISSING
        is_full_exit = bool(buy_token_amount and current_balance_value <= 0.000001)
        is_partial_exit = bool(buy_token_amount and sell_token_amount > 0 and not is_full_exit)

        records.append(
            WalletTradeRecord(
                token_address=token,
                wallet_address=wallet,
                first_buy_time=first_time,
                last_buy_time=buy_times[-1] if buy_times else MISSING,
                last_sell_time=last_sell,
                buy_count=len(buys),
                sell_count=len(sells),
                buy_amount_sol=_round(buy_amount_sol),
                buy_amount_usd=_round(buy_amount_usd),
                buy_token_amount=_round(buy_token_amount) if buy_token_amount else MISSING,
                sell_amount_sol=_round(sell_amount_sol),
                sell_amount_usd=_round(sell_amount_usd),
                sell_token_amount=_round(sell_token_amount),
                avg_buy_price=avg_buy_price,
                avg_sell_price=avg_sell_price,
                current_balance=_round(current_balance_value) if isinstance(current_balance_value, float) else MISSING,
                sold_pct=sold_pct,
                remaining_pct=remaining_pct,
                realized_profit=realized_profit,
                unrealized_profit=unrealized_profit,
                total_profit=total_profit,
                pnl_multiple=pnl_multiple,
                holding_duration_seconds=holding_duration,
                is_full_exit=is_full_exit,
                is_partial_exit=is_partial_exit,
                source_names=["GMGN wallet trade", "GMGN trader detail", "链上 DEX swap 记录"],
                missing_fields=sorted(set(missing_fields)),
                requires_followup_fields=sorted(set(requires_followup_fields)),
                evidence_notes=["交易字段仅来自 L0/L1/L2，不使用 dashboard/paper/report 反推"],
            )
        )
    return records
