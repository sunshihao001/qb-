import json
from pathlib import Path

import sikk_telegram_views as views
import sikk_unified_view_builder as unified
import sikk_telegram_gateway_adapter as gateway

BASE = Path("data/gmgn_candidates_live_run")


def _index_dir():
    unified.build_unified_indexes(BASE)
    return BASE / "index"


def test_entry_callback_renders_entry_evidence_detail_with_case_and_review_links():
    index_dir = _index_dir()
    payload = views.render_by_callback(index_dir, "entry:P1")

    assert "入场证据" in payload["text"]
    for label in ["发现时间", "发现市值", "入场时间", "入场市值", "买入 SOL", "估算 Token", "为什么入场", "安全边界"]:
        assert label in payload["text"]
    codes = [b["callback_data"] for b in payload["buttons_flat"]]
    assert "pos:P1" in codes
    assert any(code.startswith("case:") for code in codes)
    assert "review:P1" in codes
    assert not any("\u4e00" <= ch <= "\u9fff" for code in codes for ch in code)


def test_gateway_adapter_converts_readonly_payload_to_telegram_message_shape():
    index_dir = _index_dir()
    outgoing = gateway.handle_telegram_update({"message": {"text": "仓位 P1"}}, index_dir=index_dir)

    assert outgoing["method"] == "sendMessage"
    assert outgoing["readonly"] is True
    assert "reply_markup" in outgoing
    assert "inline_keyboard" in outgoing["reply_markup"]
    assert "纸面仓位详情" in outgoing["text"]
    serialized = json.dumps(outgoing, ensure_ascii=False).upper()
    for word in ["BUY", "SELL", "SWAP", "EXECUTE", "APPROVE", "BROADCAST"]:
        assert word not in serialized.replace("不执行真实 SWAP", "")


def test_gateway_adapter_converts_callback_query_to_edit_message_shape():
    index_dir = _index_dir()
    outgoing = gateway.handle_telegram_update({"callback_query": {"data": "entry:P1"}}, index_dir=index_dir)

    assert outgoing["method"] == "editMessageText"
    assert outgoing["readonly"] is True
    assert "入场证据" in outgoing["text"]
    assert outgoing["answer_callback_query"]["text"] == "只读详情已刷新"
