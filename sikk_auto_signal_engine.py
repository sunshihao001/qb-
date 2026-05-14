"""SIKK 自动交易准备框架：S0-S4 / SX 信号引擎。"""

from __future__ import annotations

from typing import Any, Dict, List

from sikk_auto_trade_types import RiskGateResult, SignalLevel, SignalResult, TradePermission


def _num(data: Dict[str, Any], key: str, default: float = 0.0) -> float:
    value = data.get(key, default)
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _bool(data: Dict[str, Any], key: str, default: bool = False) -> bool:
    value = data.get(key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "是"}
    return bool(value)


def evaluate_signal(data: Dict[str, Any], risk_gate: RiskGateResult) -> SignalResult:
    """把结构证据转换为 SIKK 自动交易前置信号。

    注意：信号结果只用于纸面交易/人工确认，不代表自动实盘执行。
    """

    evidence: List[str] = []
    invalidation: List[str] = []

    close = _num(data, "close")
    low = _num(data, "low", close)
    control_low = _num(data, "control_low")
    control_high = _num(data, "control_high")
    fib_0236 = _num(data, "fib_0236")
    fib_0382 = _num(data, "fib_0382")
    avwap = _num(data, "avwap")
    poc = _num(data, "poc")
    volume_ratio = _num(data, "volume_ratio", 1.0)
    clearout_ratio = _num(data, "early_wallet_clearout_ratio", 0.0)
    obv_state = str(data.get("obv_state", "未知"))
    cmf_state = str(data.get("cmf_state", "未知"))

    # 先判断失效：SX 优先级最高。
    if control_low and close < control_low:
        invalidation.append("跌破控盘底")
    if poc and close < poc and volume_ratio >= 1.5:
        invalidation.append("跌破 POC 且放量")
    if avwap and close < avwap and volume_ratio >= 1.5:
        invalidation.append("跌破 AVWAP 且放量")
    if "持续下降" in obv_state:
        invalidation.append("OBV 持续下降")
    if "持续小于0" in cmf_state or "持续小于 0" in cmf_state:
        invalidation.append("CMF 持续小于0")
    if clearout_ratio >= 0.8:
        invalidation.append("早期钱包集中清仓")
    if risk_gate.permission == TradePermission.BLOCK_BUY:
        invalidation.extend(risk_gate.block_reasons)

    if invalidation:
        return SignalResult(SignalLevel.SX, "风险监控", data.get("signal_time"), close or None, 0.0, evidence, invalidation)

    if not _bool(data, "control_box_ready"):
        return SignalResult(SignalLevel.S0, "无策略", data.get("signal_time"), close or None, 0.0, [], [])

    evidence.append("第一波控盘箱体明确")
    score = 20.0

    breakout = bool(control_high and close > control_high)
    if breakout:
        evidence.append("收盘突破控盘箱体上沿")
        score += 15

    retest_not_broken = False
    if fib_0236 and low >= fib_0236:
        retest_not_broken = True
        evidence.append("回踩不破 0.236 强控位")
        score += 12
    elif fib_0382 and low >= fib_0382:
        retest_not_broken = True
        evidence.append("回踩不破 0.382 上中轴")
        score += 8
    elif control_high and low <= control_high <= close:
        retest_not_broken = True
        evidence.append("回踩控盘上沿后收回")
        score += 8

    if avwap and close >= avwap:
        evidence.append("收盘站上 AVWAP")
        score += 12
    if any(word in obv_state for word in ["增强", "上升", "不弱"]):
        evidence.append("OBV 不弱或增强")
        score += 8
    if any(word in cmf_state for word in ["转正", "大于0", "增强", ">0"]):
        evidence.append("CMF 改善或转正")
        score += 8
    if clearout_ratio < 0.6:
        evidence.append("早期钱包未集中清仓")
        score += 8
    if _bool(data, "break_lh"):
        evidence.append("突破最近 LH")
        score += 8
    if _bool(data, "formed_hl_hh"):
        evidence.append("形成 HL → HH")
        score += 8
    if _bool(data, "break_vah"):
        evidence.append("突破 VAH")
        score += 6

    if breakout and retest_not_broken and avwap and close >= avwap and clearout_ratio < 0.6:
        level = SignalLevel.S4 if (_bool(data, "break_lh") and _bool(data, "formed_hl_hh")) else SignalLevel.S3
        strategy = "SIKK-B 控盘箱体突破回踩"
    elif control_high and close >= control_high * 0.95:
        level = SignalLevel.S2
        strategy = "SIKK-B 预备观察"
    else:
        level = SignalLevel.S1
        strategy = "控盘箱体观察"

    if risk_gate.permission == TradePermission.PAUSE_NEED_CONFIRM and level in {SignalLevel.S3, SignalLevel.S4}:
        evidence.append("风险门禁为 PAUSE，信号仅作人工确认观察")
        score = min(score, 65)

    return SignalResult(level, strategy, data.get("signal_time"), close or None, min(score, 100.0), evidence, [])
