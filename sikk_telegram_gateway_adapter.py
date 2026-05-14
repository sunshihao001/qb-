#!/usr/bin/env python3
"""Telegram Gateway 只读适配器。

把真实 Telegram update 形状转换为 sendMessage/editMessageText payload。
本模块不调用 Telegram API、不联网、不交易、不签名、不广播；外层 gateway 只负责发送返回值。
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Mapping

import sikk_telegram_bot_handler as bot
import sikk_telegram_zh as zh

DEFAULT_INDEX_DIR = Path("data/gmgn_candidates_live_run/index")


def _inline_keyboard(buttons: Any) -> Dict[str, List[List[Dict[str, str]]]]:
    rows: List[List[Dict[str, str]]] = []
    for row in buttons or []:
        if not isinstance(row, list):
            continue
        safe_row: List[Dict[str, str]] = []
        for item in row:
            if not isinstance(item, Mapping):
                continue
            safe_row.append({"text": str(item.get("text") or "详情"), "callback_data": str(item.get("callback_data") or "menu:main")})
        if safe_row:
            rows.append(safe_row)
    return {"inline_keyboard": rows}


def _telegram_payload(payload: Mapping[str, Any], method: str) -> Dict[str, Any]:
    return {
        "method": method,
        "text": str(payload.get("text") or ""),
        "parse_mode": "HTML",
        "reply_markup": _inline_keyboard(payload.get("buttons")),
        "readonly": True,
        "mode": "readonly",
        "boundary": payload.get("boundary") or zh.SAFETY_NOTE,
        "source": payload.get("source", ""),
    }


def handle_telegram_update(update: Mapping[str, Any], *, index_dir: str | Path = DEFAULT_INDEX_DIR) -> Dict[str, Any]:
    if not isinstance(update, Mapping):
        update = {}
    if isinstance(update.get("callback_query"), Mapping):
        callback_data = str(update["callback_query"].get("data") or "menu:main")
        payload = bot.handle_callback_query(callback_data, index_dir=index_dir)
        out = _telegram_payload(payload, "editMessageText")
        out["answer_callback_query"] = {"text": "只读详情已刷新", "show_alert": False}
        return out
    message = update.get("message") if isinstance(update.get("message"), Mapping) else {}
    text = str(message.get("text") or "/start")
    payload = bot.handle_text_message(text, index_dir=index_dir)
    return _telegram_payload(payload, "sendMessage")
