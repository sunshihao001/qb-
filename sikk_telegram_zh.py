#!/usr/bin/env python3
"""SIKK Telegram 中文术语与自然语言触发层。

只负责用户可见中文文案、状态翻译和输入触发映射；不连接 Telegram、不交易、不签名、不广播。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Mapping

SAFETY_NOTE = "只读观察；不执行真实 swap，不读取私钥，不签名，不广播。"

STATUS_ZH = {
    "UNKNOWN": "待补 / 证据不足",
    "MISSING": "待补 / 证据不足",
    "NONE": "无",
    "OPEN": "开放纸面仓位",
    "CLOSED": "已关闭纸面仓位",
    "PAPER_OPEN": "开放纸面仓位",
    "PAPER_CLOSED": "已关闭纸面仓位",
    "HOLD": "继续观察持有",
    "HOLD_WITH_DATA_RISK": "带数据风险持有",
    "DATA_BACKFILL_REQUIRED": "需要补齐数据",
    "WALLET_SUPPORT": "钱包结构支持",
    "WALLET_NEUTRAL": "钱包结构中性",
    "WALLET_BLOCK": "钱包结构阻断",
    "BLOCK": "阻断",
    "LOW": "低质量",
    "MEDIUM": "中等质量",
    "HIGH": "高质量",
    "EXIT_MONITOR": "退出监控",
    "FORCE_PAPER_EXIT": "强制纸面退出",
}

TRIGGERS = {
    # 注意：Telegram/Hermes 网关会优先拦截真正的 slash command。
    # 因此 SIKK 面板的稳定入口同时提供“无斜杠别名”，移动端优先让用户发送这些文本。
    "/sikk": {"type": "menu", "callback_data": "menu:main"},
    "/open": {"type": "list", "callback_data": "list:open:0"},
    "/closed": {"type": "list", "callback_data": "list:closed:0"},
    "/alerts": {"type": "list", "callback_data": "list:alerts:0"},
    "/health": {"type": "menu", "callback_data": "menu:health"},
    "/refresh": {"type": "refresh", "callback_data": "refresh:main"},
    "sikk": {"type": "menu", "callback_data": "menu:main"},
    "menu": {"type": "menu", "callback_data": "menu:main"},
    "open": {"type": "list", "callback_data": "list:open:0"},
    "closed": {"type": "list", "callback_data": "list:closed:0"},
    "alerts": {"type": "list", "callback_data": "list:alerts:0"},
    "health": {"type": "menu", "callback_data": "menu:health"},
    "refresh": {"type": "refresh", "callback_data": "refresh:main"},
    "ca": {"type": "menu", "callback_data": "menu:wallet_source"},
    "CA": {"type": "menu", "callback_data": "menu:wallet_source"},
    "字段依赖": {"type": "menu", "callback_data": "menu:data_dependency"},
    "data_dependency": {"type": "menu", "callback_data": "menu:data_dependency"},
    "dep": {"type": "menu", "callback_data": "menu:data_dependency"},
    "主菜单": {"type": "menu", "callback_data": "menu:main"},
    "菜单": {"type": "menu", "callback_data": "menu:main"},
    "交易面板": {"type": "menu", "callback_data": "menu:main"},
    "系统总览": {"type": "menu", "callback_data": "menu:main"},
    "开放仓位": {"type": "list", "callback_data": "list:open:0"},
    "当前仓位": {"type": "list", "callback_data": "list:open:0"},
    "持仓列表": {"type": "list", "callback_data": "list:open:0"},
    "已关闭仓位": {"type": "list", "callback_data": "list:closed:0"},
    "纸面统计": {"type": "menu", "callback_data": "menu:paper"},
    "策略复盘": {"type": "menu", "callback_data": "menu:review"},
    "风险提醒": {"type": "list", "callback_data": "list:alerts:0"},
    "系统健康": {"type": "menu", "callback_data": "menu:health"},
    "刷新数据": {"type": "refresh", "callback_data": "refresh:main"},
}


def zh_status(value: object, default: str = "待补 / 证据不足") -> str:
    key = str(value or "").strip().upper()
    if not key:
        return default
    return STATUS_ZH.get(key, str(value))


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _index_dir(path: str | Path) -> Path:
    p = Path(path)
    if p.name != "index" and (p / "index").exists():
        return p / "index"
    return p


def _resolve_token_symbol(symbol: str, index_dir: str | Path) -> str:
    root = _index_dir(index_dir)
    payload = _read_json(root / "token_detail_index.json", {"tokens": []})
    wanted = str(symbol or "").strip().upper()
    for row in payload.get("tokens", []) if isinstance(payload, Mapping) else []:
        if str(row.get("token_symbol") or "").strip().upper() == wanted and row.get("token_id"):
            return f"tok:{row['token_id']}"
    return "tok:T1" if wanted else "menu:main"


def _resolve_position_code(code: str) -> str:
    cleaned = str(code or "").strip().upper()
    if re.fullmatch(r"[PC]\d+", cleaned):
        return f"pos:{cleaned}"
    return "list:open:0"


def resolve_trigger(text: str, index_dir: str | Path = "data/gmgn_candidates_live_run/index") -> Dict[str, str]:
    raw = str(text or "").strip()
    normalized = re.sub(r"\s+", " ", raw)
    if raw in TRIGGERS:
        return dict(TRIGGERS[raw])
    if normalized.lower() in TRIGGERS:
        return dict(TRIGGERS[normalized.lower()])
    if normalized in TRIGGERS:
        return dict(TRIGGERS[normalized])
    ca_match = re.fullmatch(r"ca\s+([A-Za-z0-9_.$-]+)", normalized, flags=re.IGNORECASE)
    if ca_match:
        return {"type": "wallet_source_token", "callback_data": "menu:wallet_source", "token_address": ca_match.group(1)}
    depgroup_match = re.fullmatch(r"(?:字段依赖|依赖|field dependency)\s+(基础判断|资金判断|结果判断|风险判断|基础设施)", normalized, flags=re.IGNORECASE)
    if depgroup_match:
        group = depgroup_match.group(1).strip()
        return {"type": "data_dependency_group", "callback_data": f"depgroup:{group}"}
    question_match = re.fullmatch(r"(?:分析问题|问题|analysis question)\s+(.+)", normalized, flags=re.IGNORECASE)
    if question_match:
        question = question_match.group(1).strip()
        return {"type": "analysis_question", "callback_data": f"q:{question}"}
    dep_match = re.fullmatch(r"(?:字段依赖|依赖|field dependency)\s+(.+)", normalized, flags=re.IGNORECASE)
    if dep_match:
        target = dep_match.group(1).strip()
        return {"type": "data_dependency_target", "callback_data": f"dep:{target}"}
    token_match = re.fullmatch(r"(?:查看|代币|token)\s+([A-Za-z0-9_.$-]+)", normalized, flags=re.IGNORECASE)
    if token_match:
        return {"type": "token", "callback_data": _resolve_token_symbol(token_match.group(1), index_dir)}
    pos_match = re.fullmatch(r"(?:仓位|持仓|position|pos)\s+([PC]\d+)", normalized, flags=re.IGNORECASE)
    if pos_match:
        return {"type": "position", "callback_data": _resolve_position_code(pos_match.group(1))}
    return {"type": "unknown", "callback_data": "menu:main"}


def safe_action_text(value: object) -> str:
    action = str(value or "观察").strip()
    forbidden = {"BUY", "SELL", "SWAP", "EXECUTE", "APPROVE", "BROADCAST"}
    if action.upper() in forbidden:
        return "复查"
    return action or "观察"
