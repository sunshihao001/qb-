"""SIKK 自动交易准备框架：纸面交易引擎。

只使用历史/后续 K 线模拟，不广播交易，不调用 swap。
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

from sikk_auto_trade_types import ExitPlan


def _bar_price(bar: Dict[str, Any], key: str, default: float = 0.0) -> float:
    try:
        return float(bar.get(key, default))
    except (TypeError, ValueError):
        return default


def simulate_paper_trade(
    *,
    token: str,
    bars: Iterable[Dict[str, Any]],
    entry_time: str,
    entry_price: float,
    position_sol: float,
    exit_plan: ExitPlan,
    signal_level: str,
    strategy_type: str,
) -> Dict[str, Any]:
    """模拟一笔纸面交易。

    简化假设：
    - 入场价使用信号价/指定价；
    - K 线 high 命中止盈，low 命中止损；
    - 分批止盈后仍按最终 close 计算剩余仓位；
    - R 倍数用最终收益率 / 初始风险率估算。
    """

    rows: List[Dict[str, Any]] = list(bars)
    if not rows:
        raise ValueError("bars 不能为空")
    if entry_price <= 0:
        raise ValueError("entry_price 必须大于 0")

    hard_stop = exit_plan.hard_stop_price
    initial_risk_pct = ((entry_price - hard_stop) / entry_price * 100.0) if hard_stop and hard_stop < entry_price else 100.0

    max_high = entry_price
    min_low = entry_price
    hit_stop = False
    hit_tp = False
    exit_reason = "数据结束"
    exit_price = _bar_price(rows[-1], "close", entry_price)
    realized_pct = 0.0
    remaining_pct = 100.0
    triggered_tps: List[Dict[str, Any]] = []

    for bar in rows:
        high = _bar_price(bar, "high", entry_price)
        low = _bar_price(bar, "low", entry_price)
        close = _bar_price(bar, "close", entry_price)
        max_high = max(max_high, high)
        min_low = min(min_low, low)

        if hard_stop and low <= hard_stop:
            hit_stop = True
            exit_price = hard_stop
            exit_reason = "命中硬止损"
            # 剩余仓位按止损收益率结算。
            realized_pct += remaining_pct / 100.0 * ((exit_price - entry_price) / entry_price * 100.0)
            remaining_pct = 0.0
            break

        for rule in exit_plan.take_profit_rules:
            trigger = float(rule["触发收益率"])
            if any(done["触发收益率"] == trigger for done in triggered_tps):
                continue
            target_price = entry_price * (1 + trigger / 100.0)
            if high >= target_price:
                sell_ratio = min(float(rule["卖出比例"]), remaining_pct)
                realized_pct += sell_ratio / 100.0 * trigger
                remaining_pct -= sell_ratio
                triggered_tps.append(rule)
                hit_tp = True
                exit_reason = "命中分批止盈"

        exit_price = close

    if remaining_pct > 0:
        final_pct = (exit_price - entry_price) / entry_price * 100.0
        realized_pct += remaining_pct / 100.0 * final_pct

    max_profit_pct = (max_high - entry_price) / entry_price * 100.0
    max_drawdown_pct = (min_low - entry_price) / entry_price * 100.0
    r_multiple = realized_pct / initial_risk_pct if initial_risk_pct else 0.0

    return {
        "代币地址": token,
        "信号时间": entry_time,
        "策略类型": strategy_type,
        "信号等级": signal_level,
        "模拟入场价": entry_price,
        "模拟仓位SOL": position_sol,
        "止损价": hard_stop,
        "最大浮盈_pct": round(max_profit_pct, 4),
        "最大浮亏_pct": round(max_drawdown_pct, 4),
        "最终出场价": exit_price,
        "最终收益率_pct": round(realized_pct, 4),
        "最终R倍数": round(r_multiple, 4),
        "出场原因": exit_reason,
        "是否命中止损": hit_stop,
        "是否命中止盈": hit_tp,
        "已触发止盈次数": len(triggered_tps),
    }
