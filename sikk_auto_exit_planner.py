"""SIKK 自动交易准备框架：退出计划生成。"""

from __future__ import annotations

from sikk_auto_trade_types import ExitPlan


def build_exit_plan(
    strategy_type: str,
    entry_price: float,
    *,
    control_low: float | None = None,
    fib_0236: float | None = None,
    fib_0382: float | None = None,
    time_stop_minutes: int = 30,
) -> ExitPlan:
    """根据策略类型生成默认退出计划。

    第一版 SIKK-B 突破回踩优先使用 0.236 作为硬止损；如果缺失则用 0.382，
    再缺失才使用控盘底。
    """

    if "SIKK-B" in strategy_type:
        hard_stop = fib_0236 or fib_0382 or control_low
        stop_label = "控盘 0.236 / 0.382 / 控盘底"
    else:
        hard_stop = fib_0382 or fib_0236 or control_low
        stop_label = "结构止损"

    take_profit_rules = [
        {"触发收益率": 50, "卖出比例": 25, "说明": "+50% 卖出 25%，回收部分风险"},
        {"触发收益率": 100, "卖出比例": 25, "说明": "+100% 再卖出 25%"},
        {"触发收益率": 200, "卖出比例": 25, "说明": "+200% 再卖出 25%，剩余跟踪"},
    ]
    trailing_stop_rule = {
        "启用条件": "首次止盈后或最大浮盈超过 100%",
        "峰值回撤_pct": 35,
        "卖出比例": "剩余仓位",
    }
    emergency_exit_rules = [
        "早期钱包集中清仓",
        "跌破控盘底",
        "跌破 POC 且放量",
        "跌破 AVWAP 且放量",
        "安全风险升级为 HIGH/CRITICAL",
        "流动性骤降或无有效报价",
    ]
    if stop_label:
        emergency_exit_rules.append(f"硬止损参考：{stop_label}")

    return ExitPlan(
        hard_stop_price=hard_stop,
        time_stop_minutes=time_stop_minutes,
        take_profit_rules=take_profit_rules,
        trailing_stop_rule=trailing_stop_rule,
        emergency_exit_rules=emergency_exit_rules,
    )
