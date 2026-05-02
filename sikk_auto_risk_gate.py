"""SIKK 自动交易准备框架：风险门禁。

本模块只判断是否允许进入纸面交易或人工确认阶段，不执行任何交易。
"""

from __future__ import annotations

from typing import Any, Dict, List

from sikk_auto_trade_types import RiskGateResult, TradePermission


DEFAULT_MIN_LIQUIDITY_USD = 10_000.0


def _num(data: Dict[str, Any], key: str, default: float = 0.0) -> float:
    """安全读取数字字段。"""

    value = data.get(key, default)
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _bool(data: Dict[str, Any], key: str, default: bool = False) -> bool:
    """安全读取布尔字段，兼容 yes/no 字符串。"""

    value = data.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "是"}
    return bool(value)


def evaluate_risk_gate(data: Dict[str, Any]) -> RiskGateResult:
    """评估代币是否允许进入交易准备流程。

    返回三类权限：
    - BLOCK_BUY：任何模式都禁止买入
    - PAUSE_NEED_CONFIRM：仅半自动/人工确认可继续
    - ALLOW_PAPER_TRADE：只允许纸面交易
    """

    block_reasons: List[str] = []
    pause_reasons: List[str] = []
    allow_reasons: List[str] = []
    missing_evidence: List[str] = []

    risk_level = str(data.get("security_risk_level", "UNKNOWN")).upper()
    mode = str(data.get("mode", "paper")).lower()
    min_liquidity = _num(data, "min_liquidity_usd", DEFAULT_MIN_LIQUIDITY_USD)
    liquidity = _num(data, "liquidity_usd", 0.0)
    slippage = _num(data, "slippage_pct", 0.0)
    price_impact = _num(data, "price_impact_pct", 0.0)
    clearout_ratio = _num(data, "early_wallet_clearout_ratio", 0.0)

    if risk_level == "CRITICAL":
        block_reasons.append("安全风险为 CRITICAL")
    elif risk_level == "HIGH":
        pause_reasons.append("安全风险为 HIGH，需要人工确认")
    elif risk_level in {"UNKNOWN", "", "NONE"}:
        missing_evidence.append("安全风险等级缺失")

    if _bool(data, "is_honeypot"):
        block_reasons.append("检测到 Honeypot/貔貅风险")
    if not _bool(data, "can_sell", True):
        block_reasons.append("卖出能力不可确认或无法卖出")
    if not _bool(data, "quote_available", True):
        block_reasons.append("无有效报价")
    if liquidity and liquidity < min_liquidity:
        block_reasons.append(f"流动性低于阈值 {min_liquidity:g} USD")
    if price_impact > 10:
        block_reasons.append("价格影响超过 10%")
    elif price_impact > 5:
        pause_reasons.append("价格影响 5%-10%，需要降仓或确认")
    if slippage > 20:
        block_reasons.append("预估滑点超过 20%")
    elif slippage >= 10:
        pause_reasons.append("预估滑点 10%-20%，需要人工确认")

    if _bool(data, "break_control_low"):
        block_reasons.append("跌破控盘底")
    if clearout_ratio >= 0.8:
        block_reasons.append("早期钱包集中清仓")
    elif clearout_ratio >= 0.6:
        pause_reasons.append("早期钱包清仓比例偏高")

    if _bool(data, "security_scan_failed") and mode in {"auto", "real_auto"}:
        block_reasons.append("安全扫描失败，全自动模式默认禁止买入")
    elif _bool(data, "security_scan_failed"):
        pause_reasons.append("安全扫描失败，需要人工确认")

    if _bool(data, "data_delayed"):
        pause_reasons.append("关键数据延迟")
    if _bool(data, "wallet_evidence_missing"):
        missing_evidence.append("钱包证据缺失")
        pause_reasons.append("钱包证据缺失，需要降低信号等级")

    if block_reasons:
        return RiskGateResult(TradePermission.BLOCK_BUY, "高", block_reasons, pause_reasons, allow_reasons, missing_evidence)
    if pause_reasons:
        return RiskGateResult(TradePermission.PAUSE_NEED_CONFIRM, "中", [], pause_reasons, allow_reasons, missing_evidence)

    allow_reasons.append("安全层通过")
    allow_reasons.append("流动性/报价/滑点未触发硬风险")
    return RiskGateResult(TradePermission.ALLOW_PAPER_TRADE, "低", [], [], allow_reasons, missing_evidence)
