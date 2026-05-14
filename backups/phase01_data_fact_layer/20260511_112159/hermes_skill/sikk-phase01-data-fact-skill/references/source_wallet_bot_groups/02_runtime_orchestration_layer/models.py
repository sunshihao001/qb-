from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

MISSING = "missing"
UNKNOWN = "unknown"


@dataclass
class SerializableRecord:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class WalletTradeRecord(SerializableRecord):
    token_address: str
    wallet_address: str
    first_buy_time: str | None = MISSING
    last_buy_time: str | None = MISSING
    last_sell_time: str | None = MISSING
    buy_count: int = 0
    sell_count: int = 0
    buy_amount_sol: float | str = MISSING
    buy_amount_usd: float | str = MISSING
    buy_token_amount: float | str = MISSING
    sell_amount_sol: float | str = MISSING
    sell_amount_usd: float | str = MISSING
    sell_token_amount: float | str = MISSING
    avg_buy_price: float | str = MISSING
    avg_sell_price: float | str = MISSING
    current_balance: float | str = MISSING
    sold_pct: float | str = MISSING
    remaining_pct: float | str = MISSING
    realized_profit: float | str = UNKNOWN
    unrealized_profit: float | str = UNKNOWN
    total_profit: float | str = UNKNOWN
    pnl_multiple: float | str = UNKNOWN
    holding_duration_seconds: int | str = MISSING
    is_full_exit: bool | str = MISSING
    is_partial_exit: bool | str = MISSING
    source_level: str = "L2"
    source_names: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    requires_followup_fields: list[str] = field(default_factory=list)
    evidence_notes: list[str] = field(default_factory=list)


@dataclass
class WalletProfileRecord(SerializableRecord):
    wallet_address: str
    wallet_first_seen_time: str | None = MISSING
    wallet_last_active_time: str | None = MISSING
    wallet_age_days: float | str = UNKNOWN
    total_token_count: int | str = UNKNOWN
    traded_token_count: int | str = UNKNOWN
    gmgn_tags: list[str] = field(default_factory=list)
    funding_source_address: str | None = MISSING
    cross_token_reappearance: bool | str | dict[str, Any] = UNKNOWN
    evidence_level: str = "E0"
    missing_fields: list[str] = field(default_factory=list)


@dataclass
class SourceGroupRecord(SerializableRecord):
    same_source_group_id: str
    group_wallets: list[str]
    shared_funding_source: str | None = None
    shared_token_source: str | None = None
    evidence_label: str = "疑似同源执行组"
    evidence_level: str = "E2"
    risk_level: str = "R2"
    missing_fields: list[str] = field(default_factory=list)


@dataclass
class WalletDecision(SerializableRecord):
    wallet_address: str
    token_address: str
    role_candidates: list[str] = field(default_factory=list)
    evidence_level: str = "E0"
    risk_level: str = "R0"
    reason_codes: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    need_onchain_followup: bool = False
    gmgn_note_suggestion: str = "证据不足"
    watchlist_action: str = "observe"


@dataclass
class Bot2HandoffPacket(SerializableRecord):
    packet_id: str
    token_address: str
    created_at: str
    source_manifest_refs: list[str] = field(default_factory=list)
    wallet_trade_refs: list[str] = field(default_factory=list)
    wallet_profile_refs: list[str] = field(default_factory=list)
    funding_flow_refs: list[str] = field(default_factory=list)
    token_source_refs: list[str] = field(default_factory=list)
    same_source_evidence_refs: list[str] = field(default_factory=list)
    backflow_path_refs: list[str] = field(default_factory=list)
    wallet_intelligence_decision_refs: list[str] = field(default_factory=list)
    missing_fields_summary: dict[str, list[str]] = field(default_factory=dict)
    requires_followup_fields: list[str] = field(default_factory=list)
    evidence_language_only: bool = True
    forbidden_decision_fields: list[str] = field(default_factory=list)
