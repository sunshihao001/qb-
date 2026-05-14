from __future__ import annotations

from .models import MISSING, UNKNOWN, SourceGroupRecord, WalletDecision, WalletProfileRecord, WalletTradeRecord


def _as_float(value: object, default: float = 0.0) -> float:
    if value in (None, "", MISSING, UNKNOWN):
        return default
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return default


def classify_wallet(
    trade: WalletTradeRecord,
    profile: WalletProfileRecord | None,
    groups: list[SourceGroupRecord],
) -> WalletDecision:
    roles: list[str] = []
    reasons: list[str] = []
    risk = "R0"
    evidence = "E0"
    followup = False

    group_hit = any(trade.wallet_address in group.group_wallets for group in groups)
    if group_hit:
        roles.append("疑似同源执行组")
        reasons.append("same_source_group_candidate")
        evidence = "E3"
        risk = "R2"

    pnl_multiple = _as_float(trade.pnl_multiple)
    if pnl_multiple >= 2.0:
        roles.append("疑似结果钱包")
        reasons.append("high_pnl_multiple")
        evidence = max(evidence, "E3")
        risk = max(risk, "R2")

    current_balance = _as_float(trade.current_balance)
    buy_amount_usd = _as_float(trade.buy_amount_usd)
    sold_pct = _as_float(trade.sold_pct, -1.0)
    if current_balance >= 1000 and buy_amount_usd >= 50 and 0 <= sold_pct <= 30:
        roles.append("疑似接盘鲸鱼")
        reasons.append("large_remaining_balance_low_sell_pct")
        evidence = max(evidence, "E2")
        risk = max(risk, "R2")

    if profile and profile.gmgn_tags and profile.funding_source_address not in (None, MISSING):
        roles.append("疑似结构执行钱包")
        reasons.append("gmgn_tag_plus_funding_evidence")
        evidence = max(evidence, "E2")
        risk = max(risk, "R1")

    missing_fields = sorted(set(trade.missing_fields + (profile.missing_fields if profile else [])))
    if not roles:
        roles.append("证据不足")
        followup = True
    if missing_fields:
        followup = True

    note = roles[0]
    return WalletDecision(
        wallet_address=trade.wallet_address,
        token_address=trade.token_address,
        role_candidates=sorted(set(roles), key=roles.index),
        evidence_level=evidence,
        risk_level=risk,
        reason_codes=sorted(set(reasons)),
        missing_fields=missing_fields,
        need_onchain_followup=followup,
        gmgn_note_suggestion=note,
        watchlist_action="track" if roles != ["证据不足"] else "observe",
    )
