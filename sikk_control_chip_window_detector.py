#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIKK Control Chip Window Detector

定位：
  这是对 K线版 Accumulation Window Detector 的补充模块。
  它按“从创建/开盘第一秒开始”的思路，把 GMGN traders/holders 钱包行为与 K线结合，
  估算早期结构地址从什么时候开始拿筹码、拿到多少当前可见筹码、什么时候进入拉盘/派发阶段。

边界：
  - 只做复盘与结构识别，不下单、不自动交易。
  - 不强判同源；输出“疑似早期结构/控筹候选”。
  - GMGN top traders/holders 是样本口径，不等于全量链上持仓。

输入：
  --info-json      GMGN token info raw JSON
  --wallet-json    可重复传入：GMGN token traders/holders raw JSON
  --kline-csv      1m K线CSV，字段 timestamp/open/high/low/close/volume/market_cap
  --output-dir     输出目录

输出：
  control_chip_window.json
  control_chip_window.csv
  control_chip_phase_summary.csv
"""

from __future__ import annotations

import argparse, csv, json, os, datetime as dt, statistics
from collections import defaultdict
from typing import Any, Dict, List, Optional


def fl(x: Any, default: float = 0.0) -> float:
    try:
        if x is None or x == "": return default
        return float(x)
    except Exception:
        return default


def ts(t: Optional[int]) -> str:
    if not t: return ""
    return dt.datetime.utcfromtimestamp(int(t)).strftime("%Y-%m-%d %H:%M:%S UTC")


def short(a: str) -> str:
    return a[:4] + "..." + a[-4:] if a else ""


def tags(w: Dict[str, Any]) -> str:
    return ",".join((w.get("tags") or []) + (w.get("maker_token_tags") or []))


def load_wallets(paths: List[str]) -> List[Dict[str, Any]]:
    """合并多个 GMGN wallets JSON，按 address 去重。"""
    seen: Dict[str, Dict[str, Any]] = {}
    for p in paths:
        obj = json.load(open(p, encoding="utf-8"))
        for w in obj.get("list", []) if isinstance(obj, dict) else []:
            a = w.get("address")
            if not a: continue
            # 多来源同地址时，保留字段更完整的一份
            if a not in seen or len(json.dumps(w, ensure_ascii=False)) > len(json.dumps(seen[a], ensure_ascii=False)):
                seen[a] = w
    return list(seen.values())


def load_kline(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            rows.append({
                "timestamp": int(float(r.get("timestamp") or r.get("time") or 0)),
                "open": fl(r.get("open")),
                "high": fl(r.get("high")),
                "low": fl(r.get("low")),
                "close": fl(r.get("close")),
                "volume": fl(r.get("volume")),
                "market_cap": fl(r.get("market_cap")),
            })
    rows.sort(key=lambda x: x["timestamp"])
    return rows


def wallet_role(w: Dict[str, Any]) -> str:
    tg = tags(w)
    roles = []
    if w.get("addr_type") == 2 or w.get("exchange"): roles.append("基础设施")
    if "dev_team" in tg or "creator" in tg: roles.append("Dev相关")
    if "bundler" in tg: roles.append("捆绑")
    if "sniper" in tg: roles.append("新狙")
    if w.get("is_new") or "fresh_wallet" in tg: roles.append("新钱")
    if w.get("transfer_in") or "transfer_in" in tg: roles.append("Token转入")
    if "top_holder" in tg or str(w.get("wallet_tag_v2", "")).startswith("TOP"): roles.append("Top持仓/交易")
    if "kol" in tg or "renowned" in tg: roles.append("KOL")
    if "smart_degen" in tg: roles.append("Smart")
    return "+".join(roles) if roles else "普通/待查"


def phase_name(t: int, creation: int, open_ts: int, k_tstart: Optional[int], k_tend: Optional[int]) -> str:
    if not t: return "未知"
    if t < open_ts: return "A 创建/曲线阶段"
    if t < open_ts + 60: return "B 开放后0-60秒"
    if t < open_ts + 5*60: return "C 开放后1-5分钟"
    if k_tstart and t < k_tstart: return "D 开放后5分钟-拉盘确认前"
    if k_tstart and k_tend and t <= k_tend: return "E 拉盘确认窗口"
    return "F 窗口后/后续交易"


def detect_pull_start(kline: List[Dict[str, Any]], open_ts: int) -> Optional[int]:
    """识别初始拉盘点：价格相对近低点抬升、成交量不弱、连续收高。"""
    if len(kline) < 5: return None
    vols = [r["volume"] for r in kline[:20] if r["volume"] > 0]
    base_vol = statistics.median(vols) if vols else 0
    for i in range(3, min(len(kline), 80)):
        prior_low = min(r["low"] for r in kline[max(0, i-6):i])
        prior_high = max(r["high"] for r in kline[max(0, i-6):i])
        r = kline[i]
        close_up = r["close"] > prior_low * 1.45 or r["close"] > prior_high * 1.05
        vol_ok = (base_vol == 0) or r["volume"] >= base_vol * 0.45
        consecutive = r["close"] > kline[i-1]["close"] and kline[i-1]["close"] >= kline[i-2]["close"]
        if r["timestamp"] >= open_ts and close_up and vol_ok and consecutive:
            return r["timestamp"]
    return kline[0]["timestamp"] if kline else None


def find_kline_at(kline: List[Dict[str, Any]], t: Optional[int]) -> Dict[str, Any]:
    if not kline or not t: return {}
    return min(kline, key=lambda r: abs(r["timestamp"] - t))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--info-json", required=True)
    ap.add_argument("--wallet-json", action="append", required=True)
    ap.add_argument("--kline-csv", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--k-tstart", type=int, default=None, help="可选：K线吸筹确认开始时间戳")
    ap.add_argument("--k-tend", type=int, default=None, help="可选：K线吸筹/突破确认结束时间戳")
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    info = json.load(open(args.info_json, encoding="utf-8"))
    wallets = load_wallets(args.wallet_json)
    kline = load_kline(args.kline_csv)
    creation = int(info.get("creation_timestamp") or info.get("open_timestamp"))
    open_ts = int(info.get("open_timestamp") or creation)
    supply = fl(info.get("circulating_supply") or info.get("total_supply"))
    token = info.get("address")
    symbol = info.get("symbol", "")

    pull_start = detect_pull_start(kline, open_ts)
    pull_k = find_kline_at(kline, pull_start)
    k_tend = args.k_tend
    tend_k = find_kline_at(kline, k_tend)

    # 结构相关地址：包含早期标签、Top、转入、或早期大额买入。基础设施池子单独排除出筹码估算。
    phase = defaultdict(lambda: defaultdict(float))
    phase_rows = []
    structural_rows = []
    for w in wallets:
        st = int(w.get("start_holding_at") or 0)
        role = wallet_role(w)
        tg = tags(w)
        buy = fl(w.get("buy_volume_cur") or w.get("history_bought_cost"))
        sell = fl(w.get("sell_volume_cur") or w.get("history_sold_income"))
        hold_pct = fl(w.get("amount_percentage")) * 100
        profit = fl(w.get("profit"))
        is_infra = w.get("addr_type") == 2 or bool(w.get("exchange"))
        is_structural = (
            ("捆绑" in role) or ("新狙" in role) or ("新钱" in role) or ("Token转入" in role)
            or ("Dev相关" in role) or ("KOL" in role) or ("Top持仓" in role) or (st and st <= (args.k_tend or open_ts + 1800) and buy >= 1000)
        )
        ph = phase_name(st, creation, open_ts, args.k_tstart, args.k_tend)
        d = phase[ph]
        d["地址数"] += 1
        d["买入USD"] += buy
        d["卖出USD"] += sell
        d["利润USD"] += profit
        d["当前持仓%_含基础设施"] += hold_pct
        if not is_infra:
            d["当前持仓%_排除基础设施"] += hold_pct
        for key, label in [("bundler", "捆绑数"), ("sniper", "新狙数"), ("fresh_wallet", "新钱数"), ("transfer_in", "Token转入数"), ("top_holder", "Top数"), ("kol", "KOL数")]:
            if key in tg: d[label] += 1
        rec = {
            "短地址": short(w.get("address", "")), "钱包地址": w.get("address", ""),
            "首次时间": ts(st), "距创建秒": st-creation if st else "", "距开放秒": st-open_ts if st else "",
            "阶段": ph, "买入USD": buy, "卖出USD": sell, "当前持仓%": hold_pct,
            "利润USD": profit, "估算均买市值": fl(w.get("avg_cost"))*supply,
            "候选角色": role, "GMGN标签": tg, "是否基础设施": is_infra,
        }
        phase_rows.append(rec)
        if is_structural:
            structural_rows.append(rec)

    # 早期可见筹码：从创建到拉盘确认/原K线T_end之间，排除池子/基础设施。
    early_cut = args.k_tend or pull_start or open_ts + 1800
    early_struct = [r for r in structural_rows if r["距创建秒"] != "" and creation <= creation + int(r["距创建秒"]) <= early_cut and not r["是否基础设施"]]
    early_hold_pct = sum(r["当前持仓%"] for r in early_struct)
    early_buy = sum(r["买入USD"] for r in early_struct)
    early_sell = sum(r["卖出USD"] for r in early_struct)

    result = {
        "token": token,
        "symbol": symbol,
        "creation_time": ts(creation),
        "open_market_time": ts(open_ts),
        "chip_accumulation_start": ts(creation),
        "initial_pull_start": ts(pull_start),
        "initial_pull_start_market_cap": pull_k.get("market_cap"),
        "kline_confirm_start": ts(args.k_tstart) if args.k_tstart else "",
        "kline_confirm_end": ts(args.k_tend) if args.k_tend else "",
        "kline_confirm_end_market_cap": tend_k.get("market_cap"),
        "early_structural_wallet_count_sample": len(early_struct),
        "early_structural_buy_usd_sample": early_buy,
        "early_structural_sell_usd_sample": early_sell,
        "early_structural_current_hold_pct_sample_excluding_infra": early_hold_pct,
        "sample_scope_note": "GMGN top traders/holders/tagged wallets 样本口径，非全量链上筹码；用于疑似结构强度估算，不强判同源。",
        "interpretation": "从创建第一秒开始计算，早期结构相关地址先在创建/曲线阶段与开放后0-5分钟拿筹码，随后进入拉盘确认与派发/兑现窗口。",
    }

    # 输出 JSON / CSV
    with open(os.path.join(args.output_dir, "control_chip_window.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    with open(os.path.join(args.output_dir, "control_chip_window.csv"), "w", encoding="utf-8-sig", newline="") as f:
        fields = list(result.keys())
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerow(result)
    with open(os.path.join(args.output_dir, "control_chip_phase_summary.csv"), "w", encoding="utf-8-sig", newline="") as f:
        fields = ["阶段","地址数","买入USD","卖出USD","利润USD","当前持仓%_含基础设施","当前持仓%_排除基础设施","捆绑数","新狙数","新钱数","Token转入数","Top数","KOL数"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for ph in sorted(phase):
            row = {"阶段": ph}; row.update(phase[ph]); w.writerow({k: row.get(k, 0) for k in fields})
    with open(os.path.join(args.output_dir, "control_chip_structural_wallets.csv"), "w", encoding="utf-8-sig", newline="") as f:
        fields = ["短地址","钱包地址","首次时间","距创建秒","距开放秒","阶段","买入USD","卖出USD","当前持仓%","利润USD","估算均买市值","候选角色","GMGN标签","是否基础设施"]
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for r in sorted(structural_rows, key=lambda x: (999999 if x["距创建秒"] == "" else x["距创建秒"], -x["买入USD"])):
            w.writerow({k: r.get(k, "") for k in fields})
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
