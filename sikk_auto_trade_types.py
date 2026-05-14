"""SIKK 自动交易准备框架：共享数据类型。

第一版只服务于纸面交易与自动交易前置判断，不包含任何真实下单逻辑。
所有字段尽量保持中文可读，方便后续报告直接展示。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class SignalLevel(str, Enum):
    """SIKK 自动交易前置信号等级。"""

    S0 = "S0_无信号"
    S1 = "S1_观察信号"
    S2 = "S2_预备信号"
    S3 = "S3_策略观察信号"
    S4 = "S4_强确认信号"
    SX = "SX_失效信号"


class TradePermission(str, Enum):
    """交易权限门禁结果。"""

    BLOCK_BUY = "BLOCK_BUY_禁止买入"
    PAUSE_NEED_CONFIRM = "PAUSE_NEED_CONFIRM_需要人工确认"
    ALLOW_PAPER_TRADE = "ALLOW_PAPER_TRADE_允许纸面交易"
    ALLOW_SMALL_REAL_WITH_CONFIRM = "ALLOW_SMALL_REAL_WITH_CONFIRM_极小仓实盘需确认"


@dataclass
class RiskGateResult:
    """风险门禁输出。"""

    permission: TradePermission
    risk_level: str
    block_reasons: List[str]
    pause_reasons: List[str]
    allow_reasons: List[str]
    missing_evidence: List[str]


@dataclass
class SignalResult:
    """策略信号输出。"""

    signal_level: SignalLevel
    strategy_type: str
    signal_time: Optional[str]
    signal_price: Optional[float]
    confidence_score: float
    evidence: List[str]
    invalidation_reasons: List[str]


@dataclass
class PositionPlan:
    """仓位建议输出。"""

    suggested_position_sol: float
    max_position_sol: float
    risk_per_trade_sol: float
    stop_price: Optional[float]
    stop_type: str
    position_reason: str


@dataclass
class ExitPlan:
    """退出计划输出。"""

    hard_stop_price: Optional[float]
    time_stop_minutes: int
    take_profit_rules: List[Dict[str, Any]]
    trailing_stop_rule: Dict[str, Any]
    emergency_exit_rules: List[str]


def _serialize(value: Any) -> Any:
    """把 dataclass / Enum 递归转换为 JSON 可写对象。"""

    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return {k: _serialize(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {k: _serialize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_serialize(v) for v in value]
    return value


def readiness_to_dict(**sections: Any) -> Dict[str, Any]:
    """统一生成 readiness JSON 结构。"""

    return {name: _serialize(value) for name, value in sections.items()}
