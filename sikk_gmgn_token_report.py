#!/usr/bin/env python3
"""
SIKK-GMGN automated single-token workflow.

Usage:
  python3 /root/sikk-gmgn/sikk_gmgn_token_report.py <sol_token_address>

Output:
  /root/sikk-gmgn/reports/<symbol>_<short>_<timestamp>/
    01_analysis_depth.csv
    02_token_basic.csv
    03_structure_metrics.csv
    04_key_address_matrix.csv
    05_infrastructure_registry.csv
    06_low_weight_scope.csv
    07_review_plan.csv
    08_summary.csv
    sikk_gmgn_report.md
    <symbol>_<short>_<timestamp>.zip
"""
import csv, json, subprocess, sys, time, datetime, pathlib, re, zipfile

CHAIN = "sol"
BASE = pathlib.Path("/root/sikk-gmgn/reports")


def sh(cmd, timeout=120):
    p = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    out = p.stdout.strip()
    try:
        return json.loads(out)
    except Exception:
        return {"_error": "json_parse_failed", "_exit": p.returncode, "_raw": out[:4000]}


def fl(x, default=None):
    try:
        if x is None or x == "": return default
        return float(x)
    except Exception:
        return default


def fmt(x, n=4):
    if x is None: return ""
    try:
        v = float(x)
        if abs(v) >= 1000: return f"{v:.2f}"
        return f"{v:.{n}f}".rstrip("0").rstrip(".")
    except Exception:
        return str(x)


def pct(x):
    v = fl(x)
    return "" if v is None else f"{v*100:.3f}%"


def ts(t):
    try:
        if not t: return ""
        return datetime.datetime.utcfromtimestamp(int(float(t))).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return ""


def hm(t):
    try:
        if not t: return ""
        return datetime.datetime.utcfromtimestamp(int(float(t))).strftime("%H:%M:%S")
    except Exception:
        return ""


def tags(w):
    return ",".join((w.get("tags") or []) + (w.get("maker_token_tags") or []))


def get_any(w, *keys):
    """Return the first non-empty GMGN field among possible aliases."""
    for k in keys:
        v = w.get(k)
        if v not in (None, "", [], {}):
            return v
    return ""


def write_csv(path, headers, rows):
    """Write Excel/Google-Sheets friendly UTF-8-BOM CSV. Missing values are kept as fields."""
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(["未知" if x is None or x == "" else x for x in row])


def classify(w):
    mt = w.get("maker_token_tags") or []
    tg = w.get("tags") or []
    addr_type = w.get("addr_type")
    hold = fl(w.get("amount_percentage"),0) or 0
    sellpct = fl(w.get("sell_amount_percentage"),0) or 0
    profit = fl(get_any(w,"profit","total_profit","pnl"),0) or 0
    buy = fl(get_any(w,"buy_volume_cur","buy_volume_usd","total_buy_usd"),0) or 0
    tin = w.get("transfer_in")
    role_tags = ",".join([x for x in [",".join(tg), ",".join(mt)] if x])
    # return: 角色, 证据等级, 风险等级, 信号方向, 主动作, 辅助动作, 写入库, GMGN追踪, 复盘优先级, 备注, 角色标签
    if addr_type == 2:
        return ("LP池子","I1","无","排除","I","无","基础设施地址库,地址关系边库","否","无","LP/Pool基础设施，不进入普通钱包评分",role_tags)
    if "rat_trader" in mt:
        return ("可疑中转节点","R2","R2","风险","R","保留关系边","风险地址库,地址关系边库","否","高","rat_trader/可疑转入，保留关系边",role_tags)
    if tin and sellpct >= 0.6:
        return ("分发派发钱包","E4","R2","风险","R","A4重点追踪","地址主档库,Token来源库,风险地址库,地址关系边库","否","高","Token转入后高比例卖出，疑似分发后派发",role_tags)
    if tin:
        ev = "E4" if profit>5000 or hold>0.01 else "E3"
        act = "A4" if ev == "E4" else "A3"
        return ("分发接收钱包",ev,"无","结构",act,"观察Token去向","地址主档库,Token来源库,地址关系边库","观察","高","Token转入/接收，需追Token来源地址",role_tags)
    if "smart_degen" in tg and profit > 1000:
        return ("结果钱包","E4","无","正向","A4","复盘稳定性","地址主档库,钱包结果档案库","是","高","Smart Money高结果，需复盘稳定性",role_tags)
    if sellpct >= 0.6 and buy > 10000:
        return ("接盘鲸鱼","R2","R2","风险","R","不正向追踪","风险地址库,地址主档库","否","高","高买入且大比例卖出/结果不稳定",role_tags)
    if "bundler" in mt and profit > 5000:
        return ("结果钱包","E4","无","结构","A4","复盘资金回流","地址主档库,钱包结果档案库,地址关系边库","是","高","bundler+高结果，疑似结构执行中的结果地址",role_tags)
    if w.get("is_new") and "bundler" in mt:
        return ("新钱包狙击","E3","无","结构","A3","观察复现","地址主档库,地址关系边库","观察","中","fresh/bundler早期参与，历史稳定性待验证",role_tags)
    if "kol" in tg:
        return ("结果钱包","E3","R1","正向","A3","观察派发风险","地址主档库,钱包结果档案库","观察","中","KOL参与，注意后续派发",role_tags)
    if hold > 0.01 or "top_holder" in mt:
        return ("普通交易钱包","E2","无","中性","A2","观察持仓变化","地址主档库","观察","中","Top holder但关键结构证据不足",role_tags)
    return ("普通交易钱包","E1","无","中性","A1","无","地址主档库","否","低","低权重记录",role_tags)

def main():
    if len(sys.argv) < 2 or not re.match(r"^[1-9A-HJ-NP-Za-km-z]{32,44}$", sys.argv[1]):
        print("Usage: sikk_gmgn_token_report.py <sol_token_address>", file=sys.stderr)
        sys.exit(2)
    addr = sys.argv[1]
    now = int(time.time())

    info = sh(f"gmgn-cli token info --chain {CHAIN} --address {addr} --raw")
    sec = sh(f"gmgn-cli token security --chain {CHAIN} --address {addr} --raw")
    pool = sh(f"gmgn-cli token pool --chain {CHAIN} --address {addr} --raw")
    k1h = sh(f"gmgn-cli market kline --chain {CHAIN} --address {addr} --resolution 1m --from {now-3600} --to {now} --raw")

    specs = [
      ("holders_top","token holders","--limit 20 --order-by amount_percentage --direction desc"),
      ("traders_profit","token traders","--limit 15 --order-by profit --direction desc"),
      ("holders_smart","token holders","--limit 10 --tag smart_degen --order-by amount_percentage --direction desc"),
      ("holders_bundler","token holders","--limit 10 --tag bundler --order-by amount_percentage --direction desc"),
      ("holders_transfer","token holders","--limit 10 --tag transfer_in --order-by amount_percentage --direction desc"),
      ("holders_renowned","token holders","--limit 8 --tag renowned --order-by amount_percentage --direction desc"),
      ("holders_fresh","token holders","--limit 8 --tag fresh_wallet --order-by amount_percentage --direction desc"),
      ("holders_rat","token holders","--limit 8 --tag rat_trader --order-by amount_percentage --direction desc"),
    ]
    res = {}
    for name, sub, opt in specs:
        res[name] = sh(f"gmgn-cli {sub} --chain {CHAIN} --address {addr} {opt} --raw")
        time.sleep(1.25)

    symbol = info.get("symbol") or "UNKNOWN"
    outdir = BASE / f"{symbol}_{addr[:6]}_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    outdir.mkdir(parents=True, exist_ok=True)

    stat = info.get("stat") or {}
    wstat = info.get("wallet_tags_stat") or {}
    dev = info.get("dev") or {}
    link = info.get("link") or {}
    price = fl(info.get("price"),0) or 0
    supply = fl(info.get("circulating_supply"),0) or 0
    kl = k1h.get("list") or []
    if kl:
        op = fl(kl[0].get("open"),0) or 0
        cl = fl(kl[-1].get("close"),0) or 0
        ksum = {
          "open": op, "close": cl,
          "chg": ((cl/op-1)*100 if op else None),
          "high": max(fl(x.get("high"),0) or 0 for x in kl),
          "low": min(fl(x.get("low"),10**9) or 10**9 for x in kl),
          "volume": sum(fl(x.get("volume"),0) or 0 for x in kl)
        }
    else:
        ksum = {}

    bund_rate = fl(stat.get("top_bundler_trader_percentage"),0) or fl(sec.get("bundler_trader_amount_rate"),0) or 0
    fresh_rate = fl(stat.get("fresh_wallet_rate"),0) or 0
    sniper = int(wstat.get("sniper_wallets") or sec.get("sniper_count") or 0)
    smart = int(wstat.get("smart_wallets") or 0)
    top10 = fl(stat.get("top_10_holder_rate"),0) or fl(sec.get("top_10_holder_rate"),0) or 0
    liq = fl(info.get("liquidity"),0) or 0

    if liq < 5000:
        depth = "L0 排除"
    elif bund_rate>0.3 or sniper>20 or fresh_rate>0.1 or top10>0.2:
        depth = "L3 深度结构复盘"
    elif bund_rate>0.1 or sniper>5 or smart>=3:
        depth = "L2 早期结构全量"
    else:
        depth = "L1 快速扫描"
    depth_reason = f"bundler占比{bund_rate*100:.2f}%, fresh={fresh_rate*100:.2f}%, sniper={sniper}, smart={smart}, Top10={top10*100:.2f}%, liquidity={liq:.2f}"

    write_csv(outdir/"01_analysis_depth.csv", ["字段","值","备注"], [
      ["分析深度等级", depth, "先判断深度，不默认全量深挖"],
      ["深度原因", depth_reason, "由结构指标触发"],
      ["选定时间窗口", "W1,W2,W3,W4,W6", "优先0-30分钟，复盘派发/清仓/回流"],
      ["深挖地址范围", "0-30m早期买入,bundled,insider,sniper,fresh,transfer_in,Top Holder,Top Trader,Smart/KOL,rat_trader,核心资金源,回流节点", "只深挖关键地址"],
      ["低权重地址范围", "中后期小额普通买家,无标签,无复现,无异常来源,非Top Holder/Trader", "低权重记录"],
      ["跳过深挖原因", "不全量深挖所有散户", "降低成本并避免历史库污染"],
      ["基础设施关系边保留", "LP/Pool/Router/Aggregator/CEX/Program/native_from/token_from", "基础设施不评分但保留关系边"],
      ["下一轮复盘计划", "T+1h,T+6h,T+24h,T+72h,T+7d", "E4/R优先复盘"],
    ])

    write_csv(outdir/"02_token_basic.csv", ["字段","值","备注"], [
      ["代币符号", symbol, ""], ["代币名称", info.get("name"), ""], ["代币地址", addr, ""], ["链", CHAIN, ""],
      ["当前价格USD", fmt(price,8), ""], ["当前市值估算USD", fmt(price*supply,2), "price*circulating_supply"], ["流动性USD", fmt(liq,2), ""], ["持有人数量", info.get("持有人数量"), ""],
      ["创建时间", ts(info.get("creation_timestamp")), ""], ["开盘时间", ts(info.get("open_timestamp")), ""], ["发射平台", info.get("launchpad_platform") or info.get("发射平台"), ""],
      ["主池地址", info.get("biggest_pool_address"), ""], ["创建者地址", dev.get("创建者地址"), ""], ["创建者代币状态", dev.get("创建者代币状态"), ""],
      ["创建者开盘次数", dev.get("创建者开盘次数"), ""], ["CTO标记", dev.get("CTO标记"), ""], ["GMGN链接", link.get("gmgn"), ""], ["官网", link.get("官网"), ""], ["推特用户名", link.get("推特用户名"), ""],
    ])

    write_csv(outdir/"03_structure_metrics.csv", ["指标","值","备注"], [
      ["renounced_mint", sec.get("renounced_mint"), "安全权限"], ["renounced_freeze_account", sec.get("renounced_freeze_account"), "安全权限"], ["buy_tax", sec.get("buy_tax"), "交易税"], ["sell_tax", sec.get("sell_tax"), "交易税"], ["burn_status", sec.get("burn_status"), "LP燃烧"],
      ["top_10_holder_rate", pct(top10), "筹码集中度"], ["fresh_wallet_rate", pct(fresh_rate), "新钱包比例"], ["top_bundler_trader_percentage", pct(bund_rate), "bundler交易占比"], ["top_rat_trader_percentage", pct(stat.get("top_rat_trader_percentage")), "rat交易占比"], ["top_entrapment_trader_percentage", pct(stat.get("top_entrapment_trader_percentage")), "entrapment占比"], ["bot_degen_rate", pct(stat.get("bot_degen_rate")), "bot比例"],
      ["smart_wallets", smart, "GMGN标签"], ["renowned_wallets", wstat.get("renowned_wallets"), "KOL"], ["sniper_wallets", sniper, "狙击"], ["bundler_wallets", wstat.get("bundler_wallets"), "bundler"], ["fresh_wallets", wstat.get("fresh_wallets"), "fresh"], ["rat_trader_wallets", wstat.get("rat_trader_wallets"), "rat"],
      ["1h_open", fmt(ksum.get("open"),8), "kline"], ["1h_close", fmt(ksum.get("close"),8), "kline"], ["1h_change_pct", (fmt(ksum.get("chg"),2)+"%") if ksum.get("chg") is not None else "", "kline"], ["1h_high", fmt(ksum.get("high"),8), "kline"], ["1h_low", fmt(ksum.get("low"),8), "kline"], ["1h_volume_usd", fmt(ksum.get("volume"),2), "kline"],
    ])

    wallets = {}
    for listname, data in res.items():
        for w in (data.get("list") or []):
            a = w.get("address")
            if not a: continue
            if a not in wallets:
                wallets[a] = w.copy(); wallets[a]["source_lists"] = [listname]
            else:
                wallets[a]["source_lists"].append(listname)
                wallets[a]["tags"] = list(set((wallets[a].get("tags") or [])+(w.get("tags") or [])))
                wallets[a]["maker_token_tags"] = list(set((wallets[a].get("maker_token_tags") or [])+(w.get("maker_token_tags") or [])))
    def priority(w):
        score=0; mt=w.get("maker_token_tags") or []; tg=w.get("tags") or []
        if w.get("addr_type")==2: score+=100
        if "top_holder" in mt: score+=50
        if w.get("transfer_in"): score+=45
        if "smart_degen" in tg: score+=40
        if "bundler" in mt: score+=30
        if "kol" in tg: score+=20
        score += min((fl(w.get("profit"),0) or 0)/1000,20)
        score += min((fl(w.get("amount_percentage"),0) or 0)*100,10)
        return -score
    selected = sorted(wallets.values(), key=priority)[:25]

    addr_rows=[]
    review_rows=[]
    infra_rows=[]
    for w in selected:
        role,ev,risk_level,signal,action,secondary_action,db,track,prio,remark,role_tags = classify(w)
        tin_addr = (w.get("token_transfer_in") or {}).get("address") if isinstance(w.get("token_transfer_in"),dict) else ""
        nf = (w.get("native_transfer") or {}).get("from_address") if isinstance(w.get("native_transfer"),dict) else ""
        addr_rows.append([
            w.get("address"), CHAIN, symbol, addr, tags(w), role_tags,
            "基础设施" if w.get("addr_type")==2 else "普通钱包",
            "转入" if w.get("transfer_in") else "主动买入",
            "路由/工具节点候选" if nf else "未知源",
            hm(get_any(w,"start_holding_at","first_buy_timestamp","created_at")),
            hm(get_any(w,"last_active_timestamp","last_active_time")),
            pct(w.get("amount_percentage")), fmt(w.get("usd_value"),2),
            fmt(get_any(w,"buy_volume_cur","buy_volume_usd","total_buy_usd"),2),
            get_any(w,"buy_count","buy_times","buy_tx_count"),
            fmt(get_any(w,"sell_volume_cur","sell_volume_usd","total_sell_usd"),2),
            get_any(w,"sell_count","sell_times","sell_tx_count"),
            pct(w.get("sell_amount_percentage")),
            fmt(get_any(w,"profit","total_profit","pnl"),2),
            fmt(get_any(w,"realized_profit","realized_profit_usd"),2),
            fmt(get_any(w,"unrealized_profit","unrealized_profit_usd"),2),
            get_any(w,"profit_percentage","roi","pnl_rate"),
            tin_addr, nf, get_any(w,"token_transfer_out","token_out_address"),
            str(get_any(w,"native_transfer","funding_source","funding")),
            role, ev, risk_level, signal, action, secondary_action, db, track, prio, remark
        ])
        windows = "T+1h,T+6h,T+24h,T+72h,T+7d" if "E4" in ev else ("T+6h,T+24h,T+72h" if ev.startswith("R") or ev=="E3" else "T+24h,T+72h")
        review_rows.append([f"{symbol}_{w.get('address','')[:6]}",w.get("address"),CHAIN,symbol,addr,windows,prio,"卖出/转出/资金回流/角色升级降级","保持/升级/降级/转风险"])
    write_csv(outdir/"04_key_address_matrix.csv", ["钱包地址","链","代币符号","代币地址","GMGN标签","角色标签","地址类型","Token来源类型","资金来源类型","首次买入时间UTC","最后活动时间UTC","持仓占比","持仓价值USD","买入金额USD","买入次数","卖出金额USD","卖出次数","卖出占比","总利润USD","已实现利润USD","未实现利润USD","收益率","Token来源地址","资金来源地址","Token去向","资金来源原始字段","最终角色","证据等级","风险等级","信号方向","主动作","辅助动作","写入数据库","建议GMGN追踪","复盘优先级","SIKK备注"], addr_rows)

    infra_rows.append([pool.get("pool_address") or info.get("biggest_pool_address"),CHAIN,"LP/Pool",pool.get("exchange") or "unknown","I1","LP池子不进入普通钱包评分","中","低","是","保留交易/流动性关系边"])
    seen=set()
    for w in selected:
        nf = (w.get("native_transfer") or {}).get("from_address") if isinstance(w.get("native_transfer"),dict) else ""
        if nf and nf not in seen:
            seen.add(nf)
            infra_rows.append([nf,CHAIN,"Router/TradingTool" if nf.startswith("Axiom") else "FundingSourceCandidate","GMGN返回native_from","I3" if nf.startswith("Axiom") else "I2","资金来源/交易工具候选，不进入普通钱包评分","中","中","是","保留funding_source边，待跨币复现确认"])
    write_csv(outdir/"05_infrastructure_registry.csv", ["address","链","entity_type","entity_name","infrastructure_level","exclusion_reason","structure_relevance","risk_relevance","keep_edges","sikk_remark"], infra_rows)
    write_csv(outdir/"06_low_weight_scope.csv", ["范围","条件","动作","原因"], [
        ["中后期小额普通买家","无GMGN标签/无Top排名/无异常路径","A1记录或跳过深挖","防止历史库污染"],
        ["普通散户追涨钱包","非早期窗口且无结果表现","A1低权重","不占用深挖额度"],
        ["非Top Holder/Trader普通钱包","无transfer_in/无同源/无回流","A1或不写核心库","只在复现时升级"],
    ])
    write_csv(outdir/"07_review_plan.csv", ["review_id","address","链","代币符号","代币地址","review_window","review_priority","review_focus","expected_update_action"], review_rows)
    write_csv(outdir/"08_summary.csv", ["项目","值","备注"], [
        ["代币总体等级", "E3+R2" if depth.startswith("L3") else depth, "自动初判，待人工复核"],
        ["主要正向信号", f"smart={smart}, renounced_mint={sec.get('renounced_mint')}, renounced_freeze={sec.get('renounced_freeze_account')}", ""],
        ["主要风险信号", f"bundler={bund_rate*100:.2f}%, sniper={sniper}, bot_degen={pct(stat.get('bot_degen_rate'))}", ""],
        ["分析策略", "不全量深挖所有地址", "只深挖早期窗口和关键地址"],
        ["输出目录", str(outdir), ""],
    ])

    # Canonical Phase-1 database filenames. Keep evidence CSVs too, but DB import should use these three.
    (outdir/"sikk_gmgn_master_log.csv").write_text((outdir/"04_key_address_matrix.csv").read_text(encoding="utf-8-sig"), encoding="utf-8-sig")
    (outdir/"infrastructure_registry.csv").write_text((outdir/"05_infrastructure_registry.csv").read_text(encoding="utf-8-sig"), encoding="utf-8-sig")
    (outdir/"review_update_history.csv").write_text((outdir/"07_review_plan.csv").read_text(encoding="utf-8-sig"), encoding="utf-8-sig")

    # Human-readable Markdown summary. CSV files are the canonical database layer.
    md = []
    md.append(f"# SIKK-GMGN 单币分析报告\n")
    md.append(f"- 链: {CHAIN}\n- 代币符号: {symbol}\n- 代币地址: {addr}\n- 分析深度等级: {depth}\n- 自动交易: false\n")
    md.append("## 说明\n本报告包统一使用 CSV + Markdown；不再生成 TSV。CSV 文件可直接复制/导入 Excel、Google Sheet、SQLite。缺失字段使用 未知 / 暂无数据 / 需复查。\n")
    md.append(f"## 深度判断\n- {depth_reason}\n")
    md.append("## 核心文件\n- sikk_gmgn_master_log.csv\n- infrastructure_registry.csv\n- review_update_history.csv\n- 01_analysis_depth.csv\n- 02_token_basic.csv\n- 03_structure_metrics.csv\n- 04_key_address_matrix.csv\n")
    (outdir/"sikk_gmgn_report.md").write_text("\n".join(md), encoding="utf-8")

    # Final ZIP bundle; no TSV/XLSX generated.
    zip_path = outdir.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for f in sorted(outdir.iterdir()):
            if f.is_file() and f.suffix.lower() in {".csv", ".md", ".json"}:
                z.write(f, arcname=f.name)

    print(str(zip_path))

if __name__ == "__main__":
    main()

