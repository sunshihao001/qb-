from __future__ import annotations

from collections import defaultdict

from .models import MISSING, SourceGroupRecord, WalletProfileRecord, WalletTradeRecord


def build_same_source_groups(
    profiles: list[WalletProfileRecord],
    trades: list[WalletTradeRecord],
    *,
    min_group_size: int = 2,
) -> list[SourceGroupRecord]:
    by_funding: dict[str, list[str]] = defaultdict(list)
    for profile in profiles:
        source = profile.funding_source_address
        if source and source != MISSING:
            by_funding[str(source)].append(profile.wallet_address)

    groups: list[SourceGroupRecord] = []
    idx = 1
    for funding_source, wallets in sorted(by_funding.items()):
        unique_wallets = sorted(set(wallets))
        if len(unique_wallets) >= min_group_size:
            groups.append(
                SourceGroupRecord(
                    same_source_group_id=f"SSG-{idx:04d}",
                    group_wallets=unique_wallets,
                    shared_funding_source=funding_source,
                    evidence_label="疑似同源执行组",
                    evidence_level="E3",
                    risk_level="R2",
                )
            )
            idx += 1
    return groups
