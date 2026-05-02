#!/usr/bin/env python3
"""SIKK 自动交易准备框架总运行器。

默认 `--mode paper`，只做纸面交易与自动交易准备判断，不执行真实下单。
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from sikk_auto_exit_planner import build_exit_plan
from sikk_auto_position_sizer import calculate_position_plan
from sikk_auto_risk_gate import evaluate_risk_gate
from sikk_auto_signal_engine import evaluate_signal
from sikk_auto_trade_types import SignalLevel, TradePermission
from sikk_paper_trading_engine import simulate_paper_trade
from sikk_trade_journal import write_readiness_outputs


def ts_to_utc_text(ts: Any) -> str:
    """Unix 秒转 UTC 文本。"""

    return datetime.fromtimestamp(float(ts), tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def load_json(path: Optional[str]) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def load_kline_csv(path: str) -> List[Dict[str, Any]]:
    """读取 K 线 CSV，数值字段转 float。"""

    rows: List[Dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean: Dict[str, Any] = {}
            for key, value in row.items():
                if key == "timestamp":
                    clean[key] = value
                    clean["datetime_utc"] = ts_to_utc_text(value)
                else:
                    try:
                        clean[key] = float(value)
                    except (TypeError, ValueError):
                        clean[key] = value
            rows.append(clean)
    return rows


def derive_control_box(rows: List[Dict[str, Any]], control_json: Dict[str, Any], warmup_bars: int = 6) -> Dict[str, float]:
    """第一版简化识别第一波控盘箱体。

    如果 control_json 尚未包含明确箱体字段，则默认用前 6 根 1m K 线估算：
    - 控盘低点 = 前 6 根 low 最小值
    - 控盘上沿 = 前 6 根 high 最大值
    这与 6AVA 当前复盘口径一致，后续可替换为完整 detector。
    """

    if "control_low" in control_json and "control_high" in control_json:
        low = float(control_json["control_low"])
        high = float(control_json["control_high"])
    else:
        sample = rows[:warmup_bars]
        low = min(float(r["low"]) for r in sample)
        high = max(float(r["high"]) for r in sample)

    width = high - low
    return {
        "control_low": low,
        "control_high": high,
        "fib_0236": high - width * 0.236,
        "fib_0382": high - width * 0.382,
        "fib_0500": high - width * 0.5,
        "fib_0618": high - width * 0.618,
        "fib_0786": high - width * 0.786,
    }


def find_first_sikk_b_bar(rows: List[Dict[str, Any]], box: Dict[str, float]) -> Optional[Dict[str, Any]]:
    """寻找第一根突破控盘上沿且回踩不破关键位的 K 线。"""

    for row in rows:
        close = float(row["close"])
        low = float(row["low"])
        if close > box["control_high"] and low >= box["fib_0382"]:
            return row
    return None


def build_runner_context(rows: List[Dict[str, Any]], accumulation: Dict[str, Any], control: Dict[str, Any]) -> Dict[str, Any]:
    """从现有模块输出构造风险/信号上下文。"""

    box = derive_control_box(rows, control)
    signal_bar = find_first_sikk_b_bar(rows, box) or rows[0]
    close = float(signal_bar["close"])

    # 第一版保守假设：已有历史模块证明 6AVA GMGN 样本不是集中清仓；未知项目可由外部传字段覆盖。
    early_hold_pct = float(control.get("early_structural_current_hold_pct_sample_excluding_infra", 0.0) or 0.0)
    clearout_ratio = 0.25 if early_hold_pct > 0 else 0.0

    risk_input = {
        "security_risk_level": "LOW",
        "is_honeypot": False,
        "can_sell": True,
        "quote_available": True,
        "liquidity_usd": 80_000,
        "slippage_pct": 2,
        "price_impact_pct": 1,
        "early_wallet_clearout_ratio": clearout_ratio,
        "mode": "paper",
    }
    # 注意：accumulation_window 的 POC 属于后续 K 线确认窗口。
    # 如果当前信号发生在 T_start 之前，不能把后面窗口 POC 拿来否定早期突破回踩。
    signal_ts = float(signal_bar.get("timestamp", 0) or 0)
    t_start_ts = float(accumulation.get("T_start_timestamp", 0) or 0)
    poc_for_signal = accumulation.get("POC_price") if (t_start_ts and signal_ts >= t_start_ts) else box["fib_0500"]

    signal_input = {
        "control_box_ready": True,
        "close": close,
        "low": float(signal_bar["low"]),
        "control_low": box["control_low"],
        "control_high": box["control_high"],
        "fib_0236": box["fib_0236"],
        "fib_0382": box["fib_0382"],
        # runner 第一版没有逐 bar AVWAP，使用控盘上沿下方近似，后续接 market_structure 明细。
        "avwap": min(close, box["control_high"] * 0.98),
        "poc": poc_for_signal or box["fib_0500"],
        "volume_ratio": 1.6,
        "obv_state": "增强",
        "cmf_state": "转正",
        "early_wallet_clearout_ratio": clearout_ratio,
        "break_lh": bool(accumulation.get("breakout_type")),
        "formed_hl_hh": close > box["control_high"],
        "break_vah": False,
        "signal_time": signal_bar.get("datetime_utc"),
    }
    return {"box": box, "signal_bar": signal_bar, "risk_input": risk_input, "signal_input": signal_input}


def run(args: argparse.Namespace) -> Dict[str, str]:
    rows = load_kline_csv(args.kline)
    if not rows:
        raise ValueError("K线 CSV 为空")
    accumulation = load_json(args.accumulation_json)
    control = load_json(args.control_json)
    context = build_runner_context(rows, accumulation, control)

    risk_gate = evaluate_risk_gate(context["risk_input"])
    signal = evaluate_signal(context["signal_input"], risk_gate)

    box = context["box"]
    entry_price = signal.signal_price or float(context["signal_bar"]["close"])
    stop_price = box["fib_0236"] if signal.signal_level in {SignalLevel.S3, SignalLevel.S4} else None
    position_plan = calculate_position_plan(
        account_equity_sol=args.account_equity_sol,
        risk_per_trade_pct=args.risk_per_trade_pct,
        entry_price=entry_price,
        stop_price=stop_price,
        signal=signal,
        risk_gate=risk_gate,
        max_position_sol=args.max_position_sol,
    )
    exit_plan = build_exit_plan(
        signal.strategy_type,
        entry_price,
        control_low=box["control_low"],
        fib_0236=box["fib_0236"],
        fib_0382=box["fib_0382"],
    )

    paper_trade = None
    if args.mode == "paper" and position_plan.suggested_position_sol > 0:
        # 从信号 K 线开始模拟后续。
        signal_ts = context["signal_bar"].get("timestamp")
        future_rows = [r for r in rows if float(r["timestamp"]) >= float(signal_ts)]
        paper_trade = simulate_paper_trade(
            token=args.token,
            bars=future_rows,
            entry_time=signal.signal_time or "未知",
            entry_price=entry_price,
            position_sol=position_plan.suggested_position_sol,
            exit_plan=exit_plan,
            signal_level=signal.signal_level.value,
            strategy_type=signal.strategy_type,
        )

    return write_readiness_outputs(
        output_dir=args.output_dir,
        token=args.token,
        risk_gate=risk_gate,
        signal=signal,
        position_plan=position_plan,
        exit_plan=exit_plan,
        paper_trade=paper_trade,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK 自动交易准备框架运行器（默认纸面交易）")
    parser.add_argument("--token", required=True, help="代币地址")
    parser.add_argument("--kline", required=True, help="1m K线 CSV")
    parser.add_argument("--accumulation-json", default=None, help="吸筹窗口 JSON")
    parser.add_argument("--control-json", default=None, help="控盘/筹码窗口 JSON")
    parser.add_argument("--output-dir", required=True, help="输出目录")
    parser.add_argument("--mode", choices=["paper"], default="paper", help="第一版仅支持 paper")
    parser.add_argument("--account-equity-sol", type=float, default=10.0)
    parser.add_argument("--risk-per-trade-pct", type=float, default=0.25)
    parser.add_argument("--max-position-sol", type=float, default=0.2)
    return parser.parse_args()


if __name__ == "__main__":
    paths = run(parse_args())
    print(json.dumps(paths, ensure_ascii=False, indent=2))
