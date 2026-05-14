from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from .config import FORBIDDEN_HANDOFF_FIELDS
from .models import Bot2HandoffPacket, SourceGroupRecord, WalletDecision, WalletProfileRecord, WalletTradeRecord
from .schema_validator import assert_no_forbidden_fields


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_handoff_packet(
    *,
    token_address: str,
    wallet_trades: list[WalletTradeRecord],
    wallet_profiles: list[WalletProfileRecord],
    source_groups: list[SourceGroupRecord],
    decisions: list[WalletDecision],
    packet_id: str | None = None,
) -> Bot2HandoffPacket:
    packet_id = packet_id or f"source-wallet-{token_address}-{_now_iso()}"
    missing_summary: dict[str, list[str]] = {}
    followup: set[str] = set()
    for trade in wallet_trades:
        if trade.missing_fields:
            missing_summary[trade.wallet_address] = sorted(set(trade.missing_fields))
        followup.update(trade.requires_followup_fields)
    for decision in decisions:
        if decision.missing_fields:
            missing_summary.setdefault(decision.wallet_address, [])
            missing_summary[decision.wallet_address] = sorted(set(missing_summary[decision.wallet_address] + decision.missing_fields))
        if decision.need_onchain_followup:
            followup.update(decision.missing_fields)

    forbidden_found: list[str] = []
    payload_probe = {
        "decisions": [d.to_dict() for d in decisions],
        "trades": [t.to_dict() for t in wallet_trades],
    }
    try:
        assert_no_forbidden_fields(payload_probe)
    except Exception:
        forbidden_found = sorted(FORBIDDEN_HANDOFF_FIELDS.intersection(str(payload_probe).split()))

    return Bot2HandoffPacket(
        packet_id=packet_id,
        token_address=token_address,
        created_at=_now_iso(),
        source_manifest_refs=["modules/source_wallet_bot/source_registry.md"],
        wallet_trade_refs=["data/source_wallet_bot/wallet_trade_normalized.json"] if wallet_trades else [],
        wallet_profile_refs=["data/source_wallet_bot/wallet_entity_profile_normalized.json"] if wallet_profiles else [],
        same_source_evidence_refs=["data/source_wallet_bot/same_source_evidence_normalized.json"] if source_groups else [],
        wallet_intelligence_decision_refs=["data/source_wallet_bot/wallet_intelligence_decision.json"] if decisions else [],
        missing_fields_summary=missing_summary,
        requires_followup_fields=sorted(followup),
        evidence_language_only=True,
        forbidden_decision_fields=forbidden_found,
    )
