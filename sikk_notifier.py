#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Runtime Discord/Telegram notifier."""

from __future__ import annotations

import json
import urllib.request
from typing import Any, Callable, Dict, Mapping

IMPORTANT_EVENTS = {
    "WALLET_SUPPORT",
    "WALLET_BLOCK",
    "PAPER_READY",
    "PAPER_OPENED",
    "PAPER_FORCE_EXIT",
    "ERROR",
    "DAILY_REPORT_READY",
}


def should_notify(event: Mapping[str, Any]) -> bool:
    return str(event.get("event_type") or "") in IMPORTANT_EVENTS


def format_event_message(event: Mapping[str, Any]) -> str:
    return (
        f"[{event.get('time', '')}] {event.get('event_type', '')}\n"
        f"Token: {event.get('token_symbol', '-') }\n"
        f"Address: {event.get('token_address', '-') }\n"
        f"{event.get('message', '')}"
    )


def default_post_json(url: str, payload: Dict[str, Any]) -> None:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    urllib.request.urlopen(req, timeout=10)


def notify_event(
    event: Mapping[str, Any],
    config: Mapping[str, Any],
    *,
    post_json: Callable[[str, Dict[str, Any]], None] = default_post_json,
) -> None:
    notification = config.get("notification", {}) if isinstance(config.get("notification", {}), Mapping) else {}
    if not notification.get("enabled", False):
        return
    if not should_notify(event):
        return
    text = format_event_message(event)
    channels = notification.get("channels", []) or []
    if "discord" in channels:
        url = str(notification.get("discord_webhook_url") or "")
        if url:
            post_json(url, {"content": text})
    if "telegram" in channels:
        bot_token = str(notification.get("telegram_bot_token") or "")
        chat_id = str(notification.get("telegram_chat_id") or "")
        if bot_token and chat_id:
            post_json(f"https://api.telegram.org/bot{bot_token}/sendMessage", {"chat_id": chat_id, "text": text, "disable_web_page_preview": True})
