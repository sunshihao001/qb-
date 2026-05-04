import json
from pathlib import Path

import sikk_unified_view_builder as unified
import sikk_telegram_zh as zh
import sikk_telegram_views as views

BASE = Path("data/gmgn_candidates_live_run")


def _ensure_index():
    unified.build_unified_indexes(BASE)
    return BASE / "index"


def test_zh_layer_translates_states_and_routes_chinese_triggers():
    assert zh.zh_status("HOLD_WITH_DATA_RISK") == "带数据风险持有"
    assert zh.zh_status("UNKNOWN") == "待补 / 证据不足"
    assert zh.zh_status("WALLET_BLOCK") == "钱包结构阻断"
    assert zh.resolve_trigger("系统总览")["callback_data"] == "menu:main"
    assert zh.resolve_trigger("开放仓位")["callback_data"] == "list:open:0"
    assert zh.resolve_trigger("open")["callback_data"] == "list:open:0"
    assert zh.resolve_trigger("OPEN")["callback_data"] == "list:open:0"
    assert zh.resolve_trigger("交易面板")["callback_data"] == "menu:main"
    assert zh.resolve_trigger("pos P1")["callback_data"] == "pos:P1"
    assert zh.resolve_trigger("token LITH", index_dir=BASE / "index")["callback_data"].startswith("tok:T")
    assert zh.resolve_trigger("风险提醒")["callback_data"] == "list:alerts:0"


def test_main_menu_is_chinese_readonly_and_uses_short_callbacks():
    index_dir = _ensure_index()
    payload = views.render_main_menu(index_dir)

    assert "SIKK 中文专业控制台" in payload["text"]
    assert "只读观察" in payload["text"]
    assert "真实交易：关闭" in payload["text"]
    button_text = json.dumps(payload["buttons"], ensure_ascii=False)
    assert "开放仓位" in button_text
    assert "风险提醒" in button_text
    assert "刷新数据" in button_text
    for button in payload["buttons_flat"]:
        assert len(button["callback_data"].encode("utf-8")) <= 32
        assert not any("\u4e00" <= ch <= "\u9fff" for ch in button["callback_data"])
        assert button["callback_data"].upper() not in {"BUY", "SELL", "SWAP", "EXECUTE", "APPROVE", "BROADCAST"}


def test_open_positions_list_can_click_into_position_detail():
    index_dir = _ensure_index()
    payload = views.render_open_positions(index_dir)

    assert "开放纸面仓位" in payload["text"]
    assert "真实交易" not in json.dumps(payload["buttons"], ensure_ascii=False)
    assert payload["buttons_flat"]
    pos_buttons = [b for b in payload["buttons_flat"] if b["callback_data"].startswith("pos:")]
    assert pos_buttons

    detail = views.render_by_callback(index_dir, pos_buttons[0]["callback_data"])
    assert "纸面仓位详情" in detail["text"]
    for label in ["入场时间", "入场价格", "仓位规模", "当前收益", "最大回撤", "样本质量", "缺失证据", "下一步动作"]:
        assert label in detail["text"]
    detail_buttons = json.dumps(detail["buttons"], ensure_ascii=False)
    assert "入场证据" in detail_buttons
    assert "自动复盘" in detail_buttons


def test_alerts_view_is_readonly_and_action_safe():
    index_dir = _ensure_index()
    payload = views.render_alerts(index_dir)
    actionable = json.dumps({"text": payload["text"], "buttons": payload["buttons"]}, ensure_ascii=False).upper()
    for word in ["BUY", "SELL", "EXECUTE", "APPROVE", "BROADCAST"]:
        assert word not in actionable
    assert "风险提醒" in payload["text"]
    assert "只读提醒" in payload["text"]
    assert "已降级" not in payload["text"]
    assert any(b["callback_data"].startswith("alert:") for b in payload["buttons_flat"])
