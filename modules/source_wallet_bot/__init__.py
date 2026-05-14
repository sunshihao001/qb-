"""SIKK Source & Wallet Intelligence Bot implementation package.

This package is evidence-only. It does not modify state machines, paper runners,
private keys, signing, broadcasting, or swap execution.
"""

from .config import SourceWalletBotConfig
from .models import (
    Bot2HandoffPacket,
    SourceGroupRecord,
    WalletDecision,
    WalletProfileRecord,
    WalletTradeRecord,
)

from .phase01_fact_store_router import build_fact_store_index

__all__ = [
    "SourceWalletBotConfig",
    "WalletTradeRecord",
    "WalletProfileRecord",
    "SourceGroupRecord",
    "WalletDecision",
    "Bot2HandoffPacket",
    "build_fact_store_index",
]
