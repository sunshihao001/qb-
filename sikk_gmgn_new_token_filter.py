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


def _utc_text(value: Optional[str] = None) -> str:
    if value:
        return value
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _batch_id(now_text: str) -> str:
    dt = datetime.fromisoformat(now_text.replace("Z", "+00:00"))
    return dt.strftime("RUN_%Y%m%d_%H%M%S")


def _timestamp_to_utc(value: Any) -> str:
    if value in (None, "", [], {}, 0, "0"):
        return ""
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return ""
        if "T" in text:
            return text.replace("+00:00", "Z")
        try:
            value = float(text)
        except ValueError:
            return text
    try:
        ts = float(value)
    except (TypeError, ValueError):
        return ""
    if ts > 10_000_000_000:
        ts = ts / 1000.0
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _time_anchor_from_raw(raw: Dict[str, Any], *keys: str) -> str:
    pool = raw.get("pool") or {}
    pairs = raw.get("pairs") or []
    for key in keys:
        value = _first(raw, key, default=None)
        if value not in (None, "", [], {}, 0, "0"):
            return _timestamp_to_utc(value)
        if isinstance(pool, dict):
            value = _first(pool, key, default=None)
            if value not in (None, "", [], {}, 0, "0"):
                return _timestamp_to_utc(value)
        if isinstance(pairs, list):
            for pair in pairs:
                if isinstance(pair, dict):
                    value = _first(pair, key, default=None)
                    if value not in (None, "", [], {}, 0, "0"):
                        return _timestamp_to_utc(value)
    return ""


def _registry_path(output_dir: Path, base_dir: Path | str | None = None) -> Path:
    if base_dir is not None:
        return Path(base_dir) / "time_context" / "token_first_seen_registry.json"
    if output_dir.name == "gmgn_new_token_filter":
        return output_dir.parent / "time_context" / "token_first_seen_registry.json"
    return output_dir / "time_context" / "token_first_seen_registry.json"


def _load_first_seen_registry(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _write_first_seen_registry(path: Path, registry: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")


def _registry_tokens(registry: Dict[str, Any]) -> Dict[str, Any]:
    """兼容旧版扁平 registry，并统一返回 tokens 包裹层。"""
    tokens = registry.get("tokens") if isinstance(registry, dict) else {}
    if isinstance(tokens, dict):
        return tokens
    return registry


def _first_from_nested(raw: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """从 token/pool/pairs/stat 等常见 GMGN 结构里取第一个非空字段。"""
    value = _first(raw, *keys, default=None)
    if value not in (None, "", [], {}):
        return value
    for container_key in ("pool", "pair", "market", "quote", "stat"):
        container = raw.get(container_key)
        if isinstance(container, dict):
            value = _first(container, *keys, default=None)
            if value not in (None, "", [], {}):
                return value
    pairs = raw.get("pairs") or []
    if isinstance(pairs, list):
        for pair in pairs:
            if isinstance(pair, dict):
                value = _first(pair, *keys, default=None)
                if value not in (None, "", [], {}):
                    return value
    return default


def _source_bot_candidate_row(row: Dict[str, Any], registry_entry: Dict[str, Any], scan_time: str, candidate_batch_id: str) -> Dict[str, Any]:
    raw = row.get("raw") if isinstance(row.get("raw"), dict) else {}
    token_address = str(row.get("token_address") or row.get("代币地址") or "")
    token_symbol = str(row.get("token_symbol") or row.get("代币符号") or "")
    candidate_source = row.get("candidate_source") or f"gmgn_trenches:{row.get('来源分类') or 'unknown'}"
    token_open_time = row.get("token_open_time") or _timestamp_to_utc(row.get("开盘时间戳"))
    pool_created_at = row.get("pool_created_at") or _timestamp_to_utc(row.get("创建时间戳"))
    pool_address = _first_from_nested(raw, "pool_address", "biggest_pool_address", "pair_address", "address", default="")
    # 避免把 token address 误当成 pool address。
    if pool_address == token_address:
        pool_address = _first_from_nested(raw, "biggest_pool_address", "pair_address", default="") or ""
    normalized = {
        "token_address": token_address,
        "token_symbol": token_symbol,
        "chain": str(_first_from_nested(raw, "chain", "network", default="sol") or "sol"),
        "pool_address": pool_address,
        "token_open_time": token_open_time,
        "pool_created_at": pool_created_at,
        "discovered_at": row.get("discovered_at") or scan_time,
        "first_seen_at": registry_entry.get("first_seen_at") or row.get("first_seen_at") or scan_time,
        "last_seen_at": row.get("last_seen_at") or scan_time,
        "candidate_snapshot_at": row.get("candidate_snapshot_at") or scan_time,
        "candidate_batch_id": candidate_batch_id,
        "candidate_source": candidate_source,
        "market_cap_usd": _num(row.get("当前市值USD"), 0),
        "liquidity_usd": _num(row.get("流动性USD"), 0),
        "holder_count": _int(_first_from_nested(raw, "holder_count", "holders", "holder_num", default=row.get("持有人数") or row.get("holder_count") or 0), 0),
        "volume_1m": _num(_first_from_nested(raw, "volume_1m", "volume_m1", "volume_1min", default=0), 0),
        "volume_5m": _num(_first_from_nested(raw, "volume_5m", "volume_m5", "volume_5min", default=0), 0),
        "volume_15m": _num(_first_from_nested(raw, "volume_15m", "volume_m15", "volume_15min", default=0), 0),
        "price_usd": _num(_first_from_nested(raw, "price_usd", "price", "usd_price", default=0), 0),
    }
    missing = [key for key in (
        "token_address", "token_symbol", "chain", "pool_address", "token_open_time", "pool_created_at",
        "discovered_at", "first_seen_at", "last_seen_at", "candidate_snapshot_at", "candidate_batch_id",
        "candidate_source", "market_cap_usd", "liquidity_usd", "holder_count", "volume_1m",
        "volume_5m", "volume_15m", "price_usd",
    ) if normalized.get(key) in (None, "", [], {})]
    normalized["source_trace"] = {
        "gmgn_new_pool": candidate_source,
        "gmgn_token_info": "raw.gmgn_trenches",
        "gmgn_pool_info": "raw.pool|raw.pairs",
        "okx_or_gmgn_market_data": "gmgn_trenches.market_fields",
        "first_seen_registry": "time_context/token_first_seen_registry.json",
    }
    normalized["field_quality"] = {
        "missing_required_fields": missing,
        "time_anchor_status": "时间锚点完整" if not any(k in missing for k in ("token_open_time", "pool_created_at", "first_seen_at")) else "时间锚点缺失",
        "market_snapshot_status": "市场快照完整" if not any(k in missing for k in ("market_cap_usd", "liquidity_usd", "price_usd")) else "市场快照缺失",
    }
    return normalized


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
        "token_open_time": _time_anchor_from_raw(raw, "token_open_time", "open_time", "open_timestamp", "open_ts", "launch_time", "launch_timestamp"),
        "pool_created_at": _time_anchor_from_raw(raw, "pool_created_at", "pool_creation_time", "pool_created_time", "pool_created_timestamp", "created_timestamp", "creation_timestamp"),
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


def write_candidate_outputs(
    results: List[Dict[str, Any]],
    output_dir: Path | str,
    config: Dict[str, Any],
    raw_response: Any,
    *,
    now: Optional[str] = None,
    base_dir: Path | str | None = None,
) -> Dict[str, Path]:
    """写出候选池 JSON 和中文 CSV。"""
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    scan_time = _utc_text(now)
    candidate_batch_id = _batch_id(scan_time)
    registry_file = _registry_path(outdir, base_dir=base_dir)
    registry = _load_first_seen_registry(registry_file)

    candidate_rows = [r for r in results if r["是否进入候选池"]]
    blocked_rows = [r for r in results if not r["是否进入候选池"]]

    json_path = outdir / "token_candidates.json"
    csv_path = outdir / "token_candidates.csv"
    raw_path = outdir / "gmgn_trenches_raw.json"
    candidates_normalized_path = outdir / "candidates_normalized.json"
    token_market_snapshot_path = outdir / "token_market_snapshot.json"

    registry_tokens = _registry_tokens(registry)

    def public_row(row: Dict[str, Any]) -> Dict[str, Any]:
        clean = {k: v for k, v in row.items() if k != "raw"}
        token_address = str(clean.get("代币地址") or "")
        token_symbol = str(clean.get("代币符号") or "")
        raw = row.get("raw") if isinstance(row.get("raw"), dict) else {}
        entry = registry_tokens.setdefault(token_address, {}) if token_address else {}
        candidate_source = f"gmgn_trenches:{clean.get('来源分类') or 'unknown'}"
        token_open_time = clean.get("token_open_time") or _timestamp_to_utc(clean.get("开盘时间戳"))
        pool_created_at = clean.get("pool_created_at") or _timestamp_to_utc(clean.get("创建时间戳"))
        pool_address = _first_from_nested(raw, "pool_address", "biggest_pool_address", "pair_address", default="")
        if entry is not None and token_address:
            entry.setdefault("token_address", token_address)
            entry.setdefault("token_symbol", token_symbol)
            entry.setdefault("chain", str(_first_from_nested(raw, "chain", "network", default="sol") or "sol"))
            entry.setdefault("pool_address", pool_address)
            entry.setdefault("token_open_time", token_open_time)
            entry.setdefault("pool_created_at", pool_created_at)
            entry.setdefault("first_seen_at", scan_time)
            entry.setdefault("first_candidate_batch_id", candidate_batch_id)
            entry.setdefault("first_candidate_source", candidate_source)
            entry["last_seen_at"] = scan_time
            entry["last_candidate_batch_id"] = candidate_batch_id
            entry["last_candidate_source"] = candidate_source
            # 旧兼容字段。
            entry["candidate_source"] = candidate_source
        first_seen_at = entry.get("first_seen_at") if isinstance(entry, dict) else scan_time
        clean.update({
            "扫描时间": scan_time,
            "token_address": token_address,
            "token_symbol": token_symbol,
            "chain": str(_first_from_nested(raw, "chain", "network", default="sol") or "sol"),
            "pool_address": pool_address,
            "market_cap_usd": _num(clean.get("当前市值USD"), 0),
            "liquidity_usd": _num(clean.get("流动性USD"), 0),
            "holder_count": _int(_first_from_nested(raw, "holder_count", "holders", "holder_num", default=0), 0),
            "volume_1m": _num(_first_from_nested(raw, "volume_1m", "volume_m1", "volume_1min", default=0), 0),
            "volume_5m": _num(_first_from_nested(raw, "volume_5m", "volume_m5", "volume_5min", default=0), 0),
            "volume_15m": _num(_first_from_nested(raw, "volume_15m", "volume_m15", "volume_15min", default=0), 0),
            "price_usd": _num(_first_from_nested(raw, "price_usd", "price", "usd_price", default=0), 0),
            "token_open_time": token_open_time,
            "pool_created_at": pool_created_at,
            "discovered_at": scan_time,
            "first_seen_at": first_seen_at,
            "last_seen_at": scan_time,
            "candidate_snapshot_at": scan_time,
            "candidate_batch_id": candidate_batch_id,
            "candidate_source": candidate_source,
        })
        return clean

    public_candidates = [public_row(r) for r in candidate_rows]
    public_blocked = [public_row(r) for r in blocked_rows]
    normalized_candidates = [_source_bot_candidate_row(row, registry_tokens.get(row.get("token_address") or row.get("代币地址") or "", {}), scan_time, candidate_batch_id) for row in public_candidates]

    payload = {
        "模块": "SIKK-GMGN 新币筛选",
        "配置名称": config.get("template_name"),
        "扫描时间": scan_time,
        "candidate_snapshot_at": scan_time,
        "candidate_batch_id": candidate_batch_id,
        "candidate_source": "gmgn_trenches",
        "first_seen_registry": str(registry_file),
        "候选统计": {
            "总扫描数": len(results),
            "进入候选池": len(candidate_rows),
            "排除数量": len(blocked_rows),
            "S3数量": sum(1 for r in results if r["筛选等级"] == "S3_进入SIKK结构分析"),
            "S2数量": sum(1 for r in results if r["筛选等级"] == "S2_重点观察"),
            "S1数量": sum(1 for r in results if r["筛选等级"] == "S1_普通观察"),
            "S0数量": sum(1 for r in results if r["筛选等级"] == "S0_排除"),
        },
        "候选列表": public_candidates,
        "排除列表": public_blocked,
        "说明": "GMGN 新币筛选只负责候选池入口；自动买卖由后续 SIKK 信号/风控/仓位/执行状态机决定。",
    }
    market_snapshot = {
        "generated_at": scan_time,
        "candidate_batch_id": candidate_batch_id,
        "tokens": [
            {
                "token_address": row.get("token_address"),
                "token_symbol": row.get("token_symbol"),
                "chain": row.get("chain"),
                "pool_address": row.get("pool_address"),
                "snapshot_at": scan_time,
                "market_cap_usd": row.get("market_cap_usd"),
                "liquidity_usd": row.get("liquidity_usd"),
                "holder_count": row.get("holder_count"),
                "volume_1m": row.get("volume_1m"),
                "volume_5m": row.get("volume_5m"),
                "volume_15m": row.get("volume_15m"),
                "price_usd": row.get("price_usd"),
                "source": row.get("candidate_source"),
            }
            for row in normalized_candidates
        ],
    }
    registry_payload = {
        "generated_at": scan_time,
        "tokens": registry_tokens,
    }
    _write_first_seen_registry(registry_file, registry_payload)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    candidates_normalized_path.write_text(json.dumps(normalized_candidates, ensure_ascii=False, indent=2), encoding="utf-8")
    token_market_snapshot_path.write_text(json.dumps(market_snapshot, ensure_ascii=False, indent=2), encoding="utf-8")
    raw_path.write_text(json.dumps(raw_response, ensure_ascii=False, indent=2), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        for row in candidate_rows:
            out = {h: _csv_value(row.get(h)) for h in CSV_HEADERS}
            out["扫描时间"] = scan_time
            writer.writerow(out)

    return {
        "json_path": json_path,
        "csv_path": csv_path,
        "raw_path": raw_path,
        "candidates_normalized_path": candidates_normalized_path,
        "token_market_snapshot_path": token_market_snapshot_path,
        "token_first_seen_registry_path": registry_file,
    }


def collect_and_write_candidate_pool(
    *,
    output_dir: Path | str = DEFAULT_OUTPUT_DIR,
    config: Optional[Dict[str, Any]] = None,
    runner: Callable[[List[str]], Dict[str, Any]] = default_runner,
    limit: Optional[int] = None,
    now: Optional[str] = None,
    base_dir: Path | str | None = None,
) -> Dict[str, Path]:
    """采集 GMGN 新币列表、筛选候选池并写出 JSON/CSV。"""
    cfg = config or load_filter_config()
    cmd = build_gmgn_trenches_command(cfg, limit=limit)
    raw = runner(cmd)
    results = [classify_token(token, cfg, source_category=category) for category, token in _iter_trenches_tokens(raw)]
    # 进入候选池优先，再按 S3/S2/S1 和结构加分排序。
    rank = {"S3_进入SIKK结构分析": 0, "S2_重点观察": 1, "S1_普通观察": 2, "S0_排除": 3}
    results.sort(key=lambda r: (rank.get(r["筛选等级"], 9), -r["结构加分"], -r["24H净买入USD"], -r["24H成交额USD"]))
    return write_candidate_outputs(results, output_dir, cfg, raw, now=now, base_dir=base_dir)


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
