#!/usr/bin/env python3
"""SIKK-GMGN 新币候选池筛选模块。

第一层只做 GMGN Trenches / 新币列表筛选：
- 排除明显垃圾/高风险候选；
- 输出 S0/S1/S2/S3 候选等级；
- 写出 `outputs/gmgn_new_token_filter/token_candidates.json/csv`；
- 不执行 swap，不下单，不创建策略单。

后续真实买卖必须由 SIKK 吸筹窗口、结构信号、风险门禁、仓位模块和执行状态机共同决定。
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "token_filter_config.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "outputs" / "gmgn_new_token_filter"

_FORBIDDEN_COMMAND_SNIPPETS = [
    "gmgn-cli swap",
    "gmgn-cli multi-swap",
    "gmgn-cli order",
    "order strategy create",
    "onchainos swap execute",
]

CSV_HEADERS = [
    "扫描时间",
    "来源分类",
    "代币符号",
    "代币名称",
    "代币地址",
    "创建时间戳",
    "开盘时间戳",
    "总供应量",
    "发射平台",
    "筛选等级",
    "风险动作",
    "是否进入候选池",
    "当前市值USD",
    "流动性USD",
    "24H成交额USD",
    "24H净买入USD",
    "24H交易数",
    "24H买笔数",
    "24H卖笔数",
    "Top10持仓率",
    "Dev持仓率",
    "rat异常占比",
    "bot占比",
    "鲸鱼持仓率",
    "Dev发币数",
    "Smart钱包数",
    "KOL人数",
    "新钱包比例",
    "狙击钱包数",
    "捆绑交易占比",
    "Rug风险",
    "结构加分",
    "通过条件",
    "排除原因",
    "下一步动作",
]


def _num(value: Any, default: float = 0.0) -> float:
    """把 GMGN 返回中的数字/字符串安全转成 float。"""
    try:
        if value in (None, "", [], {}):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _int(value: Any, default: int = 0) -> int:
    return int(_num(value, float(default)))


def _first(data: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """兼容 GMGN 不同接口/版本的字段别名。"""
    for key in keys:
        value = data.get(key)
        if value not in (None, "", [], {}):
            return value
    return default


def _pct_text(value: float) -> str:
    return f"{value * 100:.2f}%"


def load_filter_config(path: Optional[Path | str] = None) -> Dict[str, Any]:
    """读取 SIKK-GMGN 新币筛选配置。"""
    cfg_path = Path(path) if path else DEFAULT_CONFIG_PATH
    with cfg_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_token(raw: Dict[str, Any], source_category: str = "unknown") -> Dict[str, Any]:
    """把 GMGN Trenches token 行标准化成筛选字段。

    保留 `raw` 便于后续排错；用户输出使用中文字段。
    """
    price = _num(_first(raw, "price", "price_usd"), 0)
    supply = _num(_first(raw, "circulating_supply", "total_supply"), 0)
    inferred_market_cap = price * supply if price and supply else 0
    stat = raw.get("stat") or {}
    dev = raw.get("dev") or {}
    wallet_tags = raw.get("wallet_tags_stat") or {}

    return {
        "来源分类": source_category,
        "代币地址": _first(raw, "address", "token_address", "base_address", default=""),
        "代币符号": _first(raw, "symbol", "token_symbol", default="UNKNOWN"),
        "代币名称": _first(raw, "name", "token_name", default="未知"),
        "创建时间戳": _int(_first(raw, "created_timestamp", "creation_timestamp", default=0), 0),
        "开盘时间戳": _int(_first(raw, "open_timestamp", "open_ts", default=0), 0),
        "总供应量": _num(_first(raw, "total_supply", "circulating_supply", "supply", default=0), 0),
        "发射平台": _first(raw, "launchpad_platform", "platform", default="未知"),
        "当前市值USD": _num(_first(raw, "usd_market_cap", "market_cap", "fdv", default=inferred_market_cap), 0),
        "流动性USD": _num(_first(raw, "liquidity", "liquidity_usd", default=_first(raw.get("pool") or {}, "liquidity", default=0)), 0),
        "24H成交额USD": _num(_first(raw, "volume_24h", "volume", "volume_usd", default=0), 0),
        "24H净买入USD": _num(_first(raw, "net_buy_24h", "net_buy", "netflow_usd", "net_inflow_usd", default=0), 0),
        "24H交易数": _int(_first(raw, "swaps_24h", "swap_count_24h", "txns_24h", "trade_count_24h", default=0), 0),
        "24H买笔数": _int(_first(raw, "buys_24h", "buy_count_24h", "buy_tx_count_24h", default=0), 0),
        "24H卖笔数": _int(_first(raw, "sells_24h", "sell_count_24h", "sell_tx_count_24h", default=0), 0),
        "Top10持仓率": _num(_first(raw, "top_10_holder_rate", default=_first(stat, "top_10_holder_rate", default=0)), 0),
        "Dev持仓率": _num(_first(raw, "creator_balance_rate", "dev_hold_rate", default=_first(stat, "creator_hold_rate", default=_first(dev, "creator_balance_rate", default=0))), 0),
        "rat异常占比": _num(_first(raw, "rat_trader_amount_rate", "insider_ratio", default=_first(stat, "top_rat_trader_percentage", default=0)), 0),
        "bot占比": _num(_first(raw, "bot_degen_rate", "bot_rate", default=_first(stat, "bot_degen_rate", default=0)), 0),
        "鲸鱼持仓率": _num(_first(raw, "whale_hold_rate", "whale_holding_rate", default=0), 0),
        "Dev发币数": _int(_first(raw, "creator_created_count", "creator_open_count", default=_first(dev, "creator_open_count", default=0)), 0),
        "Smart钱包数": _int(_first(raw, "smart_degen_count", "smart_wallets", default=_first(wallet_tags, "smart_wallets", default=0)), 0),
        "KOL人数": _int(_first(raw, "renowned_count", "renowned_wallets", "kol_count", default=_first(wallet_tags, "renowned_wallets", default=0)), 0),
        "新钱包比例": _num(_first(raw, "fresh_wallet_rate", default=_first(stat, "fresh_wallet_rate", default=0)), 0),
        "狙击钱包数": _int(_first(raw, "sniper_count", "sniper_wallets", default=_first(wallet_tags, "sniper_wallets", default=0)), 0),
        "捆绑交易占比": _num(_first(raw, "bundler_trader_amount_rate", "bundler_rate", default=_first(stat, "top_bundler_trader_percentage", default=0)), 0),
        "Rug风险": _num(_first(raw, "rug_ratio", default=0), 0),
        "raw": raw,
    }


def _below_min(label: str, value: float, minimum: Optional[float], reasons: List[str]) -> None:
    if minimum is not None and value < minimum:
        reasons.append(f"{label}低于阈值：{value:g} < {minimum:g}")


def _above_max(label: str, value: float, maximum: Optional[float], reasons: List[str]) -> None:
    if maximum is not None and value > maximum:
        reasons.append(f"{label}高于阈值：{value:g} > {maximum:g}")


def classify_token(raw_token: Dict[str, Any], config: Dict[str, Any], source_category: str = "unknown") -> Dict[str, Any]:
    """按 SIKK-GMGN V1 规则给单个 GMGN 新币候选分级。"""
    token = normalize_token(raw_token, source_category)
    th = config["thresholds"]
    hard = config["hard_exclude"]
    bonus_cfg = config["structure_bonus_rules"]
    level_rules = config["level_rules"]

    exclude_reasons: List[str] = []
    soft_reasons: List[str] = []
    passed: List[str] = []

    if token["流动性USD"] < hard["min_liquidity_usd"]:
        exclude_reasons.append(f"流动性硬排除：{token['流动性USD']:g} < {hard['min_liquidity_usd']:g}")
    if token["Top10持仓率"] > hard["max_top_10_holder_rate"]:
        exclude_reasons.append(f"Top10持仓过高：{_pct_text(token['Top10持仓率'])} > {_pct_text(hard['max_top_10_holder_rate'])}")
    if token["Dev持仓率"] > hard["max_creator_balance_rate"]:
        exclude_reasons.append(f"Dev持仓过高：{_pct_text(token['Dev持仓率'])} > {_pct_text(hard['max_creator_balance_rate'])}")
    if token["rat异常占比"] > hard["max_rat_trader_amount_rate"]:
        exclude_reasons.append(f"rat异常占比硬排除：{_pct_text(token['rat异常占比'])}")
    if token["Rug风险"] > hard["max_rug_ratio"]:
        exclude_reasons.append(f"Rug风险过高：{token['Rug风险']:.2f} > {hard['max_rug_ratio']:.2f}")

    threshold_map = [
        ("市值", "当前市值USD", "market_cap"),
        ("池子/流动性", "流动性USD", "liquidity"),
        ("24H成交额", "24H成交额USD", "volume_24h"),
        ("24H净买入", "24H净买入USD", "net_buy_24h"),
        ("24H交易数", "24H交易数", "swaps_24h"),
        ("24H买笔数", "24H买笔数", "buys_24h"),
        ("24H卖笔数", "24H卖笔数", "sells_24h"),
        ("Top10持仓率", "Top10持仓率", "top_10_holder_rate"),
        ("Dev持仓率", "Dev持仓率", "creator_balance_rate"),
        ("rat异常占比", "rat异常占比", "rat_trader_amount_rate"),
        ("bot占比", "bot占比", "bot_degen_rate"),
        ("鲸鱼持仓率", "鲸鱼持仓率", "whale_hold_rate"),
        ("Dev发币数", "Dev发币数", "creator_created_count"),
        ("Rug风险", "Rug风险", "rug_ratio"),
    ]
    for label, token_key, cfg_key in threshold_map:
        rule = th.get(cfg_key, {})
        before_len = len(soft_reasons)
        _below_min(label, token[token_key], rule.get("min"), soft_reasons)
        _above_max(label, token[token_key], rule.get("max"), soft_reasons)
        if len(soft_reasons) == before_len:
            passed.append(f"{label}达标")

    bonus = 0
    if token["Smart钱包数"] >= bonus_cfg["smart_degen_count_min"]:
        bonus += 1
        passed.append("Smart钱包>=1")
    if bonus_cfg["renowned_count_min"] <= token["KOL人数"] <= bonus_cfg["renowned_count_max"]:
        bonus += 1
        passed.append("KOL人数>=1")
    if token["新钱包比例"] >= bonus_cfg["fresh_wallet_rate_min"]:
        bonus += 1
        passed.append("新钱包比例有结构痕迹")
    if token["狙击钱包数"] >= bonus_cfg["sniper_count_min"]:
        bonus += 1
        passed.append("存在狙击钱包")
    if token["捆绑交易占比"] >= bonus_cfg["bundler_trader_amount_rate_min"]:
        bonus += 1
        passed.append("存在捆绑交易痕迹")
    if bonus_cfg.get("positive_net_buy_required") and token["24H净买入USD"] > 0:
        passed.append("净流入为正")

    if exclude_reasons:
        level = "S0_排除"
        action = "BLOCK"
        in_pool = False
        next_action = "不进入 SIKK；只记录风险样本"
    elif soft_reasons:
        level = "S1_普通观察"
        action = "OBSERVE_ONLY"
        in_pool = True
        next_action = "进入低权重观察；等待下一轮 GMGN/K线确认"
    elif bonus >= level_rules["S3_min_structure_bonus"]:
        level = "S3_进入SIKK结构分析"
        action = "ALLOW_ANALYSIS"
        in_pool = True
        next_action = "拉取K线与 holders/traders；进入吸筹窗口与钱包结构分析"
    elif bonus >= level_rules["S2_min_structure_bonus"]:
        level = "S2_重点观察"
        action = "ALLOW_WATCH"
        in_pool = True
        next_action = "加入重点观察；等待结构确认"
    else:
        level = "S1_普通观察"
        action = "OBSERVE_ONLY"
        in_pool = True
        next_action = "只观察，不进入深度结构分析"

    return {
        **{k: v for k, v in token.items() if k != "raw"},
        "筛选等级": level,
        "风险动作": action,
        "是否进入候选池": in_pool,
        "结构加分": bonus,
        "通过条件": passed,
        "软性不足": soft_reasons,
        "排除原因": exclude_reasons,
        "下一步动作": next_action,
        "raw": raw_token,
    }


def build_gmgn_trenches_command(config: Dict[str, Any], limit: Optional[int] = None) -> List[str]:
    """构建只读 GMGN Trenches 新币筛选命令。"""
    query = config.get("gmgn_query", {})
    th = config["thresholds"]
    cmd = [
        "gmgn-cli",
        "market",
        "trenches",
        "--chain",
        config.get("chain", "sol"),
    ]
    for type_name in query.get("type", ["completed"]):
        cmd.extend(["--type", str(type_name)])
    cmd.extend([
        "--limit",
        str(limit or query.get("limit", 80)),
        "--sort-by",
        query.get("sort_by", "created_timestamp"),
        "--direction",
        query.get("direction", "desc"),
        "--min-marketcap",
        str(th["market_cap"]["min"]),
        "--max-marketcap",
        str(th["market_cap"]["max"]),
        "--min-liquidity",
        str(th["liquidity"]["min"]),
        "--max-liquidity",
        str(th["liquidity"]["max"]),
        "--min-volume-24h",
        str(th["volume_24h"]["min"]),
        "--min-net-buy-24h",
        str(th["net_buy_24h"]["min"]),
        "--min-swaps-24h",
        str(th["swaps_24h"]["min"]),
        "--min-buys-24h",
        str(th["buys_24h"]["min"]),
        "--min-sells-24h",
        str(th["sells_24h"]["min"]),
        "--max-top-holder-rate",
        str(th["top_10_holder_rate"]["max"]),
        "--max-creator-balance-rate",
        str(th["creator_balance_rate"]["max"]),
        "--max-rug-ratio",
        str(th["rug_ratio"]["max"]),
        "--raw",
    ])
    _assert_readonly_command(cmd)
    return cmd


def _assert_readonly_command(cmd: List[str]) -> None:
    joined = " ".join(cmd)
    for snippet in _FORBIDDEN_COMMAND_SNIPPETS:
        if snippet in joined:
            raise ValueError(f"禁止构建真实交易命令：{snippet}")
    if cmd[:3] != ["gmgn-cli", "market", "trenches"]:
        raise ValueError("GMGN 新币筛选模块只允许 market trenches 只读命令")


def default_runner(cmd: List[str]) -> Dict[str, Any]:
    """执行只读 GMGN CLI 命令并解析 JSON。"""
    _assert_readonly_command(cmd)
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=180)
    out = proc.stdout.strip()
    try:
        data = json.loads(out)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"GMGN 输出不是有效 JSON：{out[:1000]}") from exc
    if proc.returncode != 0:
        raise RuntimeError(f"GMGN 命令失败：{out[:1000]}")
    return data


def _iter_trenches_tokens(raw: Any) -> Iterable[tuple[str, Dict[str, Any]]]:
    """兼容 GMGN trenches 可能返回的几种 JSON 结构。"""
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                yield "unknown", item
        return
    if not isinstance(raw, dict):
        return
    for category in ("completed", "new_creation", "near_completion", "list", "data", "tokens"):
        items = raw.get(category)
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    yield category, item
    # 有些 CLI 可能返回 {data:{completed:[...]}}
    data = raw.get("data")
    if isinstance(data, dict):
        for category in ("completed", "new_creation", "near_completion", "list", "tokens"):
            items = data.get(category)
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        yield category, item


def _csv_value(value: Any) -> Any:
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, list):
        return "；".join(str(x) for x in value) if value else "无"
    if isinstance(value, float):
        return f"{value:.8f}".rstrip("0").rstrip(".")
    if value in (None, ""):
        return "未知"
    return value


def write_candidate_outputs(results: List[Dict[str, Any]], output_dir: Path | str, config: Dict[str, Any], raw_response: Any) -> Dict[str, Path]:
    """写出候选池 JSON 和中文 CSV。"""
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    scan_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    candidate_rows = [r for r in results if r["是否进入候选池"]]
    blocked_rows = [r for r in results if not r["是否进入候选池"]]

    json_path = outdir / "token_candidates.json"
    csv_path = outdir / "token_candidates.csv"
    raw_path = outdir / "gmgn_trenches_raw.json"

    def public_row(row: Dict[str, Any]) -> Dict[str, Any]:
        clean = {k: v for k, v in row.items() if k != "raw"}
        clean["扫描时间"] = scan_time
        return clean

    payload = {
        "模块": "SIKK-GMGN 新币筛选",
        "配置名称": config.get("template_name"),
        "扫描时间": scan_time,
        "候选统计": {
            "总扫描数": len(results),
            "进入候选池": len(candidate_rows),
            "排除数量": len(blocked_rows),
            "S3数量": sum(1 for r in results if r["筛选等级"] == "S3_进入SIKK结构分析"),
            "S2数量": sum(1 for r in results if r["筛选等级"] == "S2_重点观察"),
            "S1数量": sum(1 for r in results if r["筛选等级"] == "S1_普通观察"),
            "S0数量": sum(1 for r in results if r["筛选等级"] == "S0_排除"),
        },
        "候选列表": [public_row(r) for r in candidate_rows],
        "排除列表": [public_row(r) for r in blocked_rows],
        "说明": "GMGN 新币筛选只负责候选池入口；自动买卖由后续 SIKK 信号/风控/仓位/执行状态机决定。",
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    raw_path.write_text(json.dumps(raw_response, ensure_ascii=False, indent=2), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for row in candidate_rows:
            out = {h: _csv_value(row.get(h)) for h in CSV_HEADERS}
            out["扫描时间"] = scan_time
            writer.writerow(out)

    return {"json_path": json_path, "csv_path": csv_path, "raw_path": raw_path}


def collect_and_write_candidate_pool(
    *,
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    config: Optional[Dict[str, Any]] = None,
    runner: Callable[[List[str]], Dict[str, Any]] = default_runner,
    limit: Optional[int] = None,
) -> Dict[str, Path]:
    """采集 GMGN 新币列表、筛选候选池并写出 JSON/CSV。"""
    cfg = config or load_filter_config()
    cmd = build_gmgn_trenches_command(cfg, limit=limit)
    raw = runner(cmd)
    results = [classify_token(token, cfg, source_category=category) for category, token in _iter_trenches_tokens(raw)]
    # 进入候选池优先，再按 S3/S2/S1 和结构加分排序。
    rank = {"S3_进入SIKK结构分析": 0, "S2_重点观察": 1, "S1_普通观察": 2, "S0_排除": 3}
    results.sort(key=lambda r: (rank.get(r["筛选等级"], 9), -r["结构加分"], -r["24H净买入USD"], -r["24H成交额USD"]))
    return write_candidate_outputs(results, output_dir, cfg, raw)


def main() -> None:
    parser = argparse.ArgumentParser(description="SIKK-GMGN 新币候选池筛选")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG_PATH), help="筛选配置 JSON")
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR), help="输出目录")
    parser.add_argument("--limit", type=int, default=None, help="GMGN 每类最大返回数量")
    args = parser.parse_args()

    outputs = collect_and_write_candidate_pool(
        output_dir=args.output_dir,
        config=load_filter_config(args.config),
        limit=args.limit,
    )
    print(json.dumps({k: str(v) for k, v in outputs.items()}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
