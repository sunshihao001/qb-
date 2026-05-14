#!/usr/bin/env python3
"""SIKK 只读 Telegram bot handler 适配层。

本模块不直接连接 Telegram 网络，不发送消息，不执行交易；真实 bot glue 只需把
message/callback 传入本模块并发送返回 payload。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import sikk_telegram_views as views
import sikk_telegram_zh as zh

DEFAULT_INDEX_DIR = Path("data/gmgn_candidates_live_run/index")
READONLY_MODE = "readonly"


def _readonly(payload: Dict[str, Any], callback_data: str = "") -> Dict[str, Any]:
    out = dict(payload)
    out.setdefault("boundary", zh.SAFETY_NOTE)
    out["mode"] = READONLY_MODE
    out["readonly"] = True
    out["callback_data"] = callback_data
    return out


def handle_text_message(text: str, *, index_dir: str | Path = DEFAULT_INDEX_DIR) -> Dict[str, Any]:
    trigger = zh.resolve_trigger(text, index_dir=index_dir)
    callback_data = trigger.get("callback_data") or "menu:main"
    payload = views.render_by_callback(index_dir, callback_data)
    if trigger.get("type") == "wallet_source_token" and trigger.get("token_address"):
        token_address = str(trigger["token_address"])
        payload = dict(payload)
        payload["token_address"] = token_address
        payload["text"] = "\n".join([
            payload.get("text", ""),
            f"目标 token：{token_address}",
            f"目标目录：data/source_wallet_bot/<mode>/{token_address}/",
        ])
    return _readonly(payload, callback_data)


def handle_callback_query(callback_data: str, *, index_dir: str | Path = DEFAULT_INDEX_DIR) -> Dict[str, Any]:
    safe_callback = str(callback_data or "menu:main").strip() or "menu:main"
    return _readonly(views.render_by_callback(index_dir, safe_callback), safe_callback)
