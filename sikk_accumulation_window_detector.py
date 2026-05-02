#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIKK Accumulation Window Detector

用途：
  从代币开盘后的 K 线 CSV 中识别疑似早期吸筹窗口：T_start ~ T_end。
  第一版只做复盘/识别，不做自动交易、不下单。

输入 CSV 字段：
  timestamp, open, high, low, close, volume
可选字段：
  amount / market_cap / supply

输出：
  outputs/accumulation_window.json
  outputs/accumulation_window.csv

示例：
  python3 sikk_accumulation_window_detector.py --csv data/kline.csv --token TOKEN --output-dir outputs
  python3 sikk_accumulation_window_detector.py --csv data/kline.csv --token TOKEN --supply 1000000000
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple, Any


# -----------------------------
# 基础工具函数
# -----------------------------

def to_float(x: Any, default: Optional[float] = None) -> Optional[float]:
    """安全转 float。"""
    try:
        if x is None or x == "":
            return default
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return default
        return v
    except Exception:
        return default


def parse_timestamp(x: Any) -> int:
    """解析 timestamp，兼容秒、毫秒、ISO 字符串。"""
    if x is None:
        raise ValueError("timestamp 为空")
    s = str(x).strip()
    # 数字时间戳：GMGN K线 time 为毫秒，这里自动转秒
    try:
        v = float(s)
        if v > 10_000_000_000:  # 毫秒级
            v = v / 1000.0
        return int(v)
    except Exception:
        pass
    # ISO / 常见字符串
    s2 = s.replace("Z", "+00:00")
    try:
        return int(dt.datetime.fromisoformat(s2).timestamp())
    except Exception as e:
        raise ValueError(f"无法解析 timestamp: {x}") from e


def fmt_time(ts: Optional[int]) -> str:
    """UTC 时间字符串。"""
    if ts is None:
        return ""
    return dt.datetime.utcfromtimestamp(int(ts)).strftime("%Y-%m-%d %H:%M:%S UTC")


def sma(values: List[Optional[float]], n: int) -> List[Optional[float]]:
    """简单移动平均。"""
    out: List[Optional[float]] = []
    window: List[float] = []
    for v in values:
        if v is None:
            window.append(0.0)
        else:
            window.append(v)
        if len(window) > n:
            window.pop(0)
        if len(window) < n:
            out.append(None)
        else:
            out.append(sum(window) / n)
    return out


def rolling_sum(values: List[float], n: int) -> List[Optional[float]]:
    """滚动求和。"""
    out: List[Optional[float]] = []
    window: List[float] = []
    for v in values:
        window.append(v)
        if len(window) > n:
            window.pop(0)
        out.append(None if len(window) < n else sum(window))
    return out


def median(vals: List[float]) -> Optional[float]:
    vals = sorted([v for v in vals if v is not None])
    if not vals:
        return None
    m = len(vals) // 2
    return vals[m] if len(vals) % 2 else (vals[m - 1] + vals[m]) / 2


@dataclass
class Candle:
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    amount: Optional[float] = None
    market_cap: Optional[float] = None

    # 计算字段
    volume_ma20: Optional[float] = None
    rvol: Optional[float] = None
    obv: Optional[float] = None
    cmf20: Optional[float] = None
    mfi14: Optional[float] = None
    atr14: Optional[float] = None
    atr_pct: Optional[float] = None
    avwap: Optional[float] = None
    swing: str = ""
    structure_tag: str = ""
    accumulation_score: int = 0
    score_reasons: str = ""
    lower_wick_ratio: Optional[float] = None


# -----------------------------
# 数据读取与指标计算
# -----------------------------

def load_csv(path: str, supply: Optional[float] = None) -> List[Candle]:
    """读取 K 线 CSV。字段名兼容 timestamp/time。"""
    rows: List[Candle] = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for raw in reader:
            ts_raw = raw.get("timestamp") or raw.get("time") or raw.get("Time")
            ts = parse_timestamp(ts_raw)
            o = to_float(raw.get("open"), 0.0) or 0.0
            h = to_float(raw.get("high"), 0.0) or 0.0
            l = to_float(raw.get("low"), 0.0) or 0.0
            c = to_float(raw.get("close"), 0.0) or 0.0
            v = to_float(raw.get("volume"), 0.0) or 0.0
            amount = to_float(raw.get("amount"), None)
            mc = to_float(raw.get("market_cap"), None)
            if mc is None and supply:
                mc = c * supply
            rows.append(Candle(ts, o, h, l, c, v, amount, mc))
    rows.sort(key=lambda x: x.timestamp)
    if not rows:
        raise ValueError("CSV 没有可用 K线")
    return rows


def compute_indicators(candles: List[Candle]) -> None:
    """计算 RVOL、OBV、CMF、MFI、ATR、AVWAP、下影线比例。"""
    closes = [c.close for c in candles]
    highs = [c.high for c in candles]
    lows = [c.low for c in candles]
    vols = [c.volume for c in candles]

    vol_ma20 = sma(vols, 20)
    for i, c in enumerate(candles):
        c.volume_ma20 = vol_ma20[i]
        c.rvol = (c.volume / vol_ma20[i]) if vol_ma20[i] and vol_ma20[i] > 0 else None

    # OBV：价格涨则加量，跌则减量，平则不变
    obv = 0.0
    for i, c in enumerate(candles):
        if i == 0:
            obv = 0.0
        elif c.close > candles[i - 1].close:
            obv += c.volume
        elif c.close < candles[i - 1].close:
            obv -= c.volume
        c.obv = obv

    # CMF(20)：Chaikin Money Flow
    mfv_values = []
    for c in candles:
        rng = c.high - c.low
        mfm = 0.0 if rng == 0 else ((c.close - c.low) - (c.high - c.close)) / rng
        mfv_values.append(mfm * c.volume)
    mfv_sum20 = rolling_sum(mfv_values, 20)
    vol_sum20 = rolling_sum(vols, 20)
    for i, c in enumerate(candles):
        if mfv_sum20[i] is not None and vol_sum20[i] and vol_sum20[i] > 0:
            c.cmf20 = mfv_sum20[i] / vol_sum20[i]

    # MFI(14)：用 typical price × volume 的正负资金流
    pos_flow = [0.0]
    neg_flow = [0.0]
    typical = [(h + l + cl) / 3.0 for h, l, cl in zip(highs, lows, closes)]
    for i in range(1, len(candles)):
        flow = typical[i] * vols[i]
        if typical[i] > typical[i - 1]:
            pos_flow.append(flow); neg_flow.append(0.0)
        elif typical[i] < typical[i - 1]:
            pos_flow.append(0.0); neg_flow.append(flow)
        else:
            pos_flow.append(0.0); neg_flow.append(0.0)
    pos14 = rolling_sum(pos_flow, 14)
    neg14 = rolling_sum(neg_flow, 14)
    for i, c in enumerate(candles):
        if pos14[i] is not None and neg14[i] is not None:
            if neg14[i] == 0:
                c.mfi14 = 100.0
            else:
                mfr = pos14[i] / neg14[i]
                c.mfi14 = 100.0 - (100.0 / (1.0 + mfr))

    # ATR(14)
    tr: List[float] = []
    for i, c in enumerate(candles):
        if i == 0:
            tr.append(c.high - c.low)
        else:
            prev_close = candles[i - 1].close
            tr.append(max(c.high - c.low, abs(c.high - prev_close), abs(c.low - prev_close)))
    atr14 = sma(tr, 14)
    for i, c in enumerate(candles):
        c.atr14 = atr14[i]
        c.atr_pct = (atr14[i] / c.close) if atr14[i] and c.close else None

    # 从开盘锚定 AVWAP：用 typical price * volume / volume 累计
    cum_pv = 0.0
    cum_v = 0.0
    for c in candles:
        tp = (c.high + c.low + c.close) / 3.0
        cum_pv += tp * c.volume
        cum_v += c.volume
        c.avwap = cum_pv / cum_v if cum_v > 0 else None

    # 下影线比例：下影线 / 全 K 振幅
    for c in candles:
        rng = c.high - c.low
        lower = min(c.open, c.close) - c.low
        c.lower_wick_ratio = (lower / rng) if rng > 0 else 0.0


def detect_swings(candles: List[Candle], left: int = 2, right: int = 2) -> None:
    """识别 Swing High / Swing Low，并派生 LL/LH/HL/HH。"""
    last_high: Optional[float] = None
    last_low: Optional[float] = None
    for i in range(left, len(candles) - right):
        h = candles[i].high
        l = candles[i].low
        is_sh = all(h >= candles[j].high for j in range(i - left, i + right + 1) if j != i)
        is_sl = all(l <= candles[j].low for j in range(i - left, i + right + 1) if j != i)
        tags = []
        if is_sh:
            candles[i].swing = (candles[i].swing + ",SH").strip(",")
            if last_high is not None:
                tags.append("HH" if h > last_high else "LH")
            last_high = h
        if is_sl:
            candles[i].swing = (candles[i].swing + ",SL").strip(",")
            if last_low is not None:
                tags.append("HL" if l > last_low else "LL")
            last_low = l
        candles[i].structure_tag = ",".join(tags)


def compute_volume_profile(candles: List[Candle], bins: int = 48) -> Dict[str, Optional[float]]:
    """简化成交量分布：按价格区间把每根K线 volume 分摊到 typical price 所在价格桶。"""
    if not candles:
        return {"POC_price": None, "VAH_price": None, "VAL_price": None}
    lo = min(c.low for c in candles)
    hi = max(c.high for c in candles)
    if hi <= lo:
        px = candles[-1].close
        return {"POC_price": px, "VAH_price": px, "VAL_price": px}
    step = (hi - lo) / bins
    buckets = [0.0 for _ in range(bins)]
    prices = [lo + (i + 0.5) * step for i in range(bins)]
    for c in candles:
        tp = (c.high + c.low + c.close) / 3.0
        idx = int((tp - lo) / step)
        idx = max(0, min(bins - 1, idx))
        buckets[idx] += c.volume
    total = sum(buckets)
    poc_idx = max(range(bins), key=lambda i: buckets[i])
    # Value Area：从 POC 向两边扩展到 70% 成交量
    target = total * 0.70
    left = right = poc_idx
    acc = buckets[poc_idx]
    while acc < target and (left > 0 or right < bins - 1):
        lv = buckets[left - 1] if left > 0 else -1
        rv = buckets[right + 1] if right < bins - 1 else -1
        if rv >= lv and right < bins - 1:
            right += 1; acc += buckets[right]
        elif left > 0:
            left -= 1; acc += buckets[left]
        else:
            break
    return {"POC_price": prices[poc_idx], "VAH_price": prices[right], "VAL_price": prices[left]}


# -----------------------------
# 吸筹评分、开始/结束/失败判定
# -----------------------------

def score_accumulation(candles: List[Candle]) -> None:
    """按用户给定规则计算 accumulation_score。"""
    open_low = candles[0].low
    recent_low = open_low
    for i, c in enumerate(candles):
        score = 0
        reasons = []
        # RVOL > 1.5，加15分
        if c.rvol is not None and c.rvol > 1.5:
            score += 15; reasons.append("RVOL>1.5")
        # 当前K线没有继续大幅创新低，加15分：允许不低于最近低点 2% 或没有收在新低附近
        prior_lows = [x.low for x in candles[max(0, i - 10):i]]
        prior_min = min(prior_lows) if prior_lows else c.low
        if c.low >= prior_min * 0.98 or c.close > c.low * 1.01:
            score += 15; reasons.append("未继续大幅创新低")
        # OBV 上升或 OBV 没有跟随价格创新低，加20分
        if i >= 3:
            obv_up = c.obv is not None and candles[i - 3].obv is not None and c.obv >= candles[i - 3].obv
            price_new_low = c.low < min(x.low for x in candles[max(0, i - 10):i] or [c])
            obv_not_new_low = c.obv is not None and c.obv > min((x.obv or 0.0) for x in candles[max(0, i - 10):i+1])
            if obv_up or (price_new_low and obv_not_new_low):
                score += 20; reasons.append("OBV上升/未跟随创新低")
        # CMF(20) > 0，加15分
        if c.cmf20 is not None and c.cmf20 > 0:
            score += 15; reasons.append("CMF20>0")
        # MFI(14) 从低位抬升，加10分
        if i >= 3 and c.mfi14 is not None and candles[i - 3].mfi14 is not None:
            if candles[i - 3].mfi14 < 45 and c.mfi14 > candles[i - 3].mfi14:
                score += 10; reasons.append("MFI低位抬升")
        # 当前K线有明显下影线，加10分
        if c.lower_wick_ratio is not None and c.lower_wick_ratio >= 0.35:
            score += 10; reasons.append("明显下影线")
        # ATR 百分比开始下降或波动率收缩，加10分
        if i >= 3 and c.atr_pct is not None and candles[i - 3].atr_pct is not None:
            if c.atr_pct < candles[i - 3].atr_pct:
                score += 10; reasons.append("ATR%收缩")
        # close 接近或重新站上开盘 AVWAP，加15分
        if c.avwap is not None and c.close >= c.avwap * 0.985:
            score += 15; reasons.append("接近/站上开盘AVWAP")
        c.accumulation_score = score
        c.score_reasons = ";".join(reasons)
        recent_low = min(recent_low, c.low)


def find_t_start(candles: List[Candle]) -> Optional[int]:
    """连续3根 accumulation_score >= 60，取第一根作为 T_start。"""
    for i in range(2, len(candles)):
        if all(candles[j].accumulation_score >= 60 for j in (i - 2, i - 1, i)):
            return i - 2
    return None


def latest_lh_before(candles: List[Candle], idx: int) -> Tuple[Optional[float], Optional[int]]:
    """寻找 idx 前最近 LH 价格。若没有明确 LH，则退化为最近 swing high。"""
    for j in range(idx - 1, -1, -1):
        if "LH" in candles[j].structure_tag:
            return candles[j].high, j
    for j in range(idx - 1, -1, -1):
        if "SH" in candles[j].swing:
            return candles[j].high, j
    return None, None


def has_sequence_ll_lh_hl_hh(candles: List[Candle], start: int, end: int) -> bool:
    """简化判断是否出现 LL-LH-HL-HH 序列。"""
    seq: List[str] = []
    for c in candles[start:end + 1]:
        for tag in (c.structure_tag or "").split(","):
            if tag in ("LL", "LH", "HL", "HH"):
                seq.append(tag)
    target = ["LL", "LH", "HL", "HH"]
    pos = 0
    for tag in seq:
        if tag == target[pos]:
            pos += 1
            if pos == len(target):
                return True
    return False


def detect_window(candles: List[Candle], token: str, supply: Optional[float] = None) -> Dict[str, Any]:
    """主检测函数：输出用户指定字段，并附加辅助字段。"""
    compute_indicators(candles)
    detect_swings(candles)
    score_accumulation(candles)

    start_idx = find_t_start(candles)
    if start_idx is None:
        # 没有连续3根达标：输出 pending/invalid 的保守结论
        best_idx = max(range(len(candles)), key=lambda i: candles[i].accumulation_score)
        profile = compute_volume_profile(candles[:best_idx + 1])
        return {
            "token": token,
            "T_start": "",
            "T_end": "",
            "T_start_timestamp": None,
            "T_end_timestamp": None,
            "T_start_market_cap": None,
            "T_end_market_cap": None,
            "window_high": None,
            "window_low": None,
            "window_duration_bars": 0,
            "window_duration_minutes": 0,
            **profile,
            "AVWAP_anchor_time": fmt_time(candles[0].timestamp),
            "latest_AVWAP": candles[-1].avwap,
            "accumulation_score_avg": round(sum(c.accumulation_score for c in candles) / len(candles), 2),
            "breakout_type": "未形成连续3根吸筹评分达标",
            "window_status": "pending",
            "interpretation": "尚未出现连续3根 accumulation_score>=60，第一版不强行标记吸筹窗口；建议结合早期钱包是否集中进入继续观察。",
            "debug_best_score_time": fmt_time(candles[best_idx].timestamp),
            "debug_best_score": candles[best_idx].accumulation_score,
        }

    end_idx: Optional[int] = None
    breakout_type = ""
    invalid_reason = ""
    status = "pending"

    for i in range(start_idx + 3, len(candles)):
        current_slice = candles[start_idx:i + 1]
        window_high = max(x.high for x in current_slice[:-1])
        window_low = min(x.low for x in current_slice[:-1])
        profile = compute_volume_profile(current_slice[:-1])
        poc, vah = profile["POC_price"], profile["VAH_price"]
        c = candles[i]
        vol_ma = c.volume_ma20 or median([x.volume for x in candles[max(0, i - 20):i]]) or 0.0

        # 失败判定优先：跌破窗口低点 / POC / AVWAP / OBV+CMF 持续弱 / 无 HL HH
        if c.close < window_low:
            status = "invalid"; invalid_reason = "close跌破吸筹窗口低点"; end_idx = i; break
        if poc is not None and c.close < poc and vol_ma > 0 and c.volume > vol_ma * 1.5:
            status = "invalid"; invalid_reason = "close跌破POC且放量"; end_idx = i; break
        if c.avwap is not None and c.close < c.avwap and vol_ma > 0 and c.volume > vol_ma * 1.5:
            status = "invalid"; invalid_reason = "close跌破AVWAP且放量"; end_idx = i; break
        if i >= start_idx + 5:
            recent = candles[i - 4:i + 1]
            obv_down = all((recent[k].obv or 0) < (recent[k - 1].obv or 0) for k in range(1, len(recent)))
            cmf_neg = all((x.cmf20 is not None and x.cmf20 < 0) for x in recent)
            if obv_down and cmf_neg:
                status = "invalid"; invalid_reason = "OBV持续下跌且CMF持续小于0"; end_idx = i; break

        lh_price, lh_idx = latest_lh_before(candles, i)
        # 结束判定1：close 放量突破最近 LH，且 volume > MA20*1.8
        if lh_price is not None and c.close > lh_price and vol_ma > 0 and c.volume > vol_ma * 1.8:
            status = "valid"; breakout_type = "放量突破最近LH"; end_idx = i; break
        # 结束判定2：close 放量突破吸筹窗口上沿，且收盘站上 AVWAP
        if c.close > window_high and vol_ma > 0 and c.volume > vol_ma * 1.5 and c.avwap is not None and c.close > c.avwap:
            status = "valid"; breakout_type = "放量突破吸筹窗口上沿并站上AVWAP"; end_idx = i; break
        # 结束判定3：close 突破 VAH，且 OBV 和 CMF 同步增强
        if vah is not None and c.close > vah and i >= 3:
            obv_stronger = c.obv is not None and candles[i - 3].obv is not None and c.obv > candles[i - 3].obv
            cmf_stronger = c.cmf20 is not None and candles[i - 3].cmf20 is not None and c.cmf20 > candles[i - 3].cmf20
            if obv_stronger and cmf_stronger:
                status = "valid"; breakout_type = "突破VAH且OBV/CMF同步增强"; end_idx = i; break
        # 结束判定4：完成 LL-LH-HL-HH，并突破 LH
        if lh_price is not None and c.close > lh_price and has_sequence_ll_lh_hl_hh(candles, start_idx, i):
            status = "valid"; breakout_type = "完成LL-LH-HL-HH并突破LH"; end_idx = i; break

    if end_idx is None:
        end_idx = len(candles) - 1
        window_part = candles[start_idx:end_idx + 1]
        tags = ",".join(c.structure_tag for c in window_part)
        if "HL" not in tags or "HH" not in tags:
            status = "pending"
            breakout_type = "未完成HL/HH结构，窗口待确认"
        else:
            status = "pending"
            breakout_type = "尚未触发有效突破，窗口待确认"

    window = candles[start_idx:end_idx + 1]
    profile = compute_volume_profile(window)
    avg_score = sum(c.accumulation_score for c in window) / len(window)
    start_c = candles[start_idx]
    end_c = candles[end_idx]
    duration_min = (end_c.timestamp - start_c.timestamp) / 60.0

    if status == "valid":
        interpretation = (
            f"识别到疑似早期吸筹窗口：{fmt_time(start_c.timestamp)} 至 {fmt_time(end_c.timestamp)}。"
            f"结束信号为：{breakout_type}。该窗口可用于后续固定范围成交量分布、POC/VAH/VAL、AVWAP 与 Fib 区间锚定。"
        )
    elif status == "invalid":
        breakout_type = invalid_reason
        interpretation = (
            f"窗口从 {fmt_time(start_c.timestamp)} 开始后被失败条件破坏：{invalid_reason}。"
            "第一版标记为 invalid_window，不进入策略执行，只保留复盘证据。"
        )
    else:
        interpretation = (
            f"已出现吸筹开始候选 {fmt_time(start_c.timestamp)}，但尚未确认有效结束。"
            f"当前状态：{breakout_type}。建议叠加早期钱包集中进入/持仓变化辅助判断。"
        )

    return {
        "token": token,
        "T_start": fmt_time(start_c.timestamp),
        "T_end": fmt_time(end_c.timestamp) if status in ("valid", "invalid", "pending") else "",
        "T_start_timestamp": start_c.timestamp,
        "T_end_timestamp": end_c.timestamp,
        "T_start_market_cap": start_c.market_cap,
        "T_end_market_cap": end_c.market_cap,
        "window_high": max(c.high for c in window),
        "window_low": min(c.low for c in window),
        "window_duration_bars": len(window),
        "window_duration_minutes": round(duration_min, 2),
        **profile,
        "AVWAP_anchor_time": fmt_time(candles[0].timestamp),
        "latest_AVWAP": candles[-1].avwap,
        "accumulation_score_avg": round(avg_score, 2),
        "breakout_type": breakout_type,
        "window_status": status,
        "interpretation": interpretation,
    }


# -----------------------------
# 输出
# -----------------------------

def write_outputs(result: Dict[str, Any], candles: List[Candle], output_dir: str) -> None:
    """写 JSON / CSV，同时附带一份逐K线调试明细，方便后续接 SIKK-B。"""
    os.makedirs(output_dir, exist_ok=True)
    json_path = os.path.join(output_dir, "accumulation_window.json")
    csv_path = os.path.join(output_dir, "accumulation_window.csv")
    detail_path = os.path.join(output_dir, "accumulation_window_bars.csv")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    fields = [
        "token", "T_start", "T_end", "window_high", "window_low",
        "window_duration_bars", "window_duration_minutes", "POC_price", "VAH_price", "VAL_price",
        "AVWAP_anchor_time", "latest_AVWAP", "accumulation_score_avg", "breakout_type",
        "window_status", "interpretation", "T_start_market_cap", "T_end_market_cap",
    ]
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerow({k: result.get(k, "") for k in fields})

    detail_fields = [
        "timestamp", "time_utc", "open", "high", "low", "close", "volume", "market_cap",
        "volume_ma20", "rvol", "obv", "cmf20", "mfi14", "atr14", "atr_pct", "avwap",
        "swing", "structure_tag", "lower_wick_ratio", "accumulation_score", "score_reasons",
    ]
    with open(detail_path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=detail_fields)
        w.writeheader()
        for c in candles:
            row = asdict(c)
            row["time_utc"] = fmt_time(c.timestamp)
            w.writerow({k: row.get(k, "") for k in detail_fields})


def main() -> None:
    ap = argparse.ArgumentParser(description="SIKK Accumulation Window Detector")
    ap.add_argument("--csv", required=True, help="K线CSV路径，字段 timestamp,open,high,low,close,volume")
    ap.add_argument("--token", required=True, help="代币符号或地址")
    ap.add_argument("--output-dir", default="outputs", help="输出目录，默认 outputs")
    ap.add_argument("--supply", type=float, default=None, help="可选：供应量，用于估算市值=close*supply")
    args = ap.parse_args()

    candles = load_csv(args.csv, supply=args.supply)
    result = detect_window(candles, token=args.token, supply=args.supply)
    write_outputs(result, candles, args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
