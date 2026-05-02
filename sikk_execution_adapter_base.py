"""SIKK v0.2 执行适配器基础类型。

本文件只定义报价、安全扫描、真实执行确认所需的数据结构。
默认不执行任何真实交易。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TokenSide(str, Enum):
    """代币在交易中的方向。"""

    BUY = "buy"
    SELL = "sell"


@dataclass
class QuoteRequest:
    """统一报价请求。"""

    chain: str
    wallet_address: str
    input_token: str
    output_token: str
    amount_smallest_unit: Optional[str] = None
    readable_amount: Optional[str] = None
    slippage: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QuoteResult:
    """统一报价结果。"""

    source: str
    input_token: str
    output_token: str
    input_amount: str
    output_amount: Optional[str]
    min_output_amount: Optional[str]
    price_impact_pct: Optional[float]
    raw: Dict[str, Any]


@dataclass
class SecurityScanResult:
    """单个数据源的代币安全扫描结果。"""

    source: str
    token_address: str
    token_side: TokenSide
    risk_level: str
    triggered_labels: List[str]
    raw: Dict[str, Any]


@dataclass
class PreTradeSecurityDecision:
    """多源安全扫描聚合后的最终门禁。"""

    permission: str
    risk_level: str
    requires_user_confirmation: bool
    reasons: List[str]
    source_count: int


class ReadOnlyQuoteAdapter:
    """只读报价适配器基类。

    子类只负责构造 quote 命令，不允许构造 execute/swap 真实交易命令。
    """

    source_name = "base"

    def make_quote_request(self, **kwargs: Any) -> QuoteRequest:
        return QuoteRequest(**kwargs)

    def build_quote_command(self, request: QuoteRequest) -> List[str]:
        raise NotImplementedError
