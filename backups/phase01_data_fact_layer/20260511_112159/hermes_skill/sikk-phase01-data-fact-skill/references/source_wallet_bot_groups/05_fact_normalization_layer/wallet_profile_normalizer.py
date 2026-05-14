from __future__ import annotations

from typing import Any

from .models import MISSING, UNKNOWN, WalletProfileRecord

PROFILE_REQUIRED_HINTS = [
    "wallet_first_seen_time",
    "wallet_last_active_time",
    "funding_source_address",
]


def normalize_wallet_profile(row: dict[str, Any]) -> WalletProfileRecord:
    wallet = str(row.get("wallet_address") or row.get("wallet") or row.get("address") or MISSING)
    tags_raw = row.get("gmgn_tags") or row.get("tags") or []
    if isinstance(tags_raw, str):
        tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]
    else:
        tags = [str(tag) for tag in tags_raw]

    missing_fields = [field for field in PROFILE_REQUIRED_HINTS if row.get(field) in (None, "", MISSING)]
    if wallet == MISSING:
        missing_fields.append("wallet_address")

    evidence_level = "E0"
    if tags and row.get("funding_source_address"):
        evidence_level = "E2"
    elif tags or row.get("funding_source_address"):
        evidence_level = "E1"

    return WalletProfileRecord(
        wallet_address=wallet,
        wallet_first_seen_time=row.get("wallet_first_seen_time") or MISSING,
        wallet_last_active_time=row.get("wallet_last_active_time") or MISSING,
        wallet_age_days=row.get("wallet_age_days", UNKNOWN),
        total_token_count=row.get("total_token_count", UNKNOWN),
        traded_token_count=row.get("traded_token_count", UNKNOWN),
        gmgn_tags=tags,
        funding_source_address=row.get("funding_source_address") or MISSING,
        cross_token_reappearance=row.get("cross_token_reappearance", UNKNOWN),
        evidence_level=evidence_level,
        missing_fields=sorted(set(missing_fields)),
    )
