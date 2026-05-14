import json
from pathlib import Path

import sikk_live_run
import sikk_telegram_bot_handler as bot
import sikk_telegram_views as views
import sikk_telegram_zh as zh
import sikk_unified_view_builder as unified

BASE = Path("data/gmgn_candidates_live_run")


def _index_dir():
    unified.build_unified_indexes(BASE)
    return BASE / "index"


def test_readonly_bot_handler_routes_message_and_callback_without_side_effects():
    index_dir = _index_dir()

    msg_payload = bot.handle_text_message("查看 LITH", index_dir=index_dir)
    assert "只读" in msg_payload["boundary"]
    assert msg_payload["mode"] == "readonly"
    assert "真实交易" in msg_payload["text"] or "不执行真实" in msg_payload["text"]
    assert msg_payload["callback_data"].startswith("tok:T")

    cb_payload = bot.handle_callback_query("pos:P1", index_dir=index_dir)
    assert cb_payload["mode"] == "readonly"
    assert "纸面仓位详情" in cb_payload["text"]
    forbidden_text = json.dumps({"buttons": cb_payload["buttons"]}, ensure_ascii=False).upper()
    for word in ["BUY", "SELL", "SWAP", "EXECUTE", "APPROVE", "BROADCAST"]:
        assert word not in forbidden_text


def test_chinese_natural_language_triggers_token_and_position_short_codes():
    index_dir = _index_dir()

    token_trigger = zh.resolve_trigger("代币 LITH", index_dir=index_dir)
    assert token_trigger["type"] == "token"
    assert token_trigger["callback_data"].startswith("tok:T")

    view_trigger = zh.resolve_trigger("查看 LITH", index_dir=index_dir)
    assert view_trigger["type"] == "token"
    assert view_trigger["callback_data"] == token_trigger["callback_data"]

    pos_trigger = zh.resolve_trigger("仓位 P1", index_dir=index_dir)
    assert pos_trigger["type"] == "position"
    assert pos_trigger["callback_data"] == "pos:P1"


def test_token_case_and_auto_review_detail_buttons_are_rendered():
    index_dir = _index_dir()

    token_callback = zh.resolve_trigger("查看 LITH", index_dir=index_dir)["callback_data"]
    token_detail = views.render_by_callback(index_dir, token_callback)
    assert "代币详情" in token_detail["text"]
    token_button_codes = [b["callback_data"] for b in token_detail["buttons_flat"]]
    case_callback = next(code for code in token_button_codes if code.startswith("case:"))
    review_callback = next(code for code in token_button_codes if code.startswith("review:"))

    case_detail = views.render_by_callback(index_dir, case_callback)
    assert "Case File" in case_detail["text"]
    assert "证据" in case_detail["text"] or "路径" in case_detail["text"]

    review_detail = views.render_by_callback(index_dir, review_callback)
    assert "自动复盘" in review_detail["text"]
    assert "不输出真实交易建议" in review_detail["text"]


def test_lith_drilldown_renders_entry_wallet_okx_review_and_full_case_buttons():
    index_dir = _index_dir()

    menu_payload = bot.handle_text_message("/sikk", index_dir=index_dir)
    assert any(b["text"] == "开放仓位" and b["callback_data"] == "list:open:0" for b in menu_payload["buttons_flat"])

    token_callback = zh.resolve_trigger("查看 LITH", index_dir=index_dir)["callback_data"]
    token_detail = bot.handle_callback_query(token_callback, index_dir=index_dir)
    assert "【LITH 代币详情】" in token_detail["text"]
    button_map = {b["text"]: b["callback_data"] for b in token_detail["buttons_flat"]}
    for label in ["入场证据", "钱包结构", "OKX 集群", "自动复盘", "完整档案"]:
        assert label in button_map

    expected_fragments = {
        "入场证据": "入场证据",
        "钱包结构": "钱包结构",
        "OKX 集群": "OKX 集群",
        "自动复盘": "自动复盘",
        "完整档案": "完整档案",
    }
    for label, fragment in expected_fragments.items():
        payload = bot.handle_callback_query(button_map[label], index_dir=index_dir)
        assert fragment in payload["text"]
        assert payload["readonly"] is True
        forbidden_text = json.dumps({"buttons": payload["buttons"]}, ensure_ascii=False).upper()
        for word in ["BUY", "SELL", "SWAP", "EXECUTE", "APPROVE", "BROADCAST"]:
            assert word not in forbidden_text

def test_live_run_refreshes_unified_and_telegram_index_after_round(tmp_path):
    def fake_pipeline_runner(**kwargs):
        root = Path(kwargs["output_root"])
        (root / "state_machine").mkdir(parents=True, exist_ok=True)
        (root / "candidate_signal_outputs").mkdir(parents=True, exist_ok=True)
        (root / "quote_security").mkdir(parents=True, exist_ok=True)
        (root / "wallet_structure").mkdir(parents=True, exist_ok=True)
        (root / "state_machine" / "candidate_states.json").write_text(json.dumps({"候选状态": [{"token_address": "LITHADDR", "token_symbol": "LITH", "current_state": "PAPER_OPEN", "wallet_structure_status": "WALLET_SUPPORT"}]}, ensure_ascii=False), encoding="utf-8")
        (root / "candidate_signal_outputs" / "candidate_signal_summary.json").write_text(json.dumps({"处理结果": []}, ensure_ascii=False), encoding="utf-8")
        (root / "quote_security" / "candidate_quote_security_summary.json").write_text(json.dumps({"处理结果": []}, ensure_ascii=False), encoding="utf-8")
        return {"candidate_states": str(root / "state_machine" / "candidate_states.json")}

    def fake_paper_runner(**kwargs):
        out = Path(kwargs["output_dir"])
        out.mkdir(parents=True, exist_ok=True)
        open_payload = {"open_positions": [{"position_id": "paper-LITH", "token_address": "LITHADDR", "token_symbol": "LITH", "paper_pnl_pct": "12.3", "wallet_structure_status": "WALLET_SUPPORT"}]}
        closed_payload = {"closed_positions": []}
        (out / "paper_positions_open.json").write_text(json.dumps(open_payload, ensure_ascii=False), encoding="utf-8")
        (out / "paper_positions_closed.json").write_text(json.dumps(closed_payload, ensure_ascii=False), encoding="utf-8")
        (out / "failure_attribution.jsonl").write_text("", encoding="utf-8")
        return {"open_positions_json": str(out / "paper_positions_open.json"), "closed_positions_json": str(out / "paper_positions_closed.json")}

    paths = sikk_live_run.run_live_once(
        output_root=tmp_path,
        limit=1,
        now="2026-05-03T00:00:00Z",
        pipeline_runner=fake_pipeline_runner,
        paper_runner=fake_paper_runner,
    )

    assert Path(paths["unified_index_dir"]).exists()
    assert Path(paths["telegram_callback_index_json"]).exists()
    callbacks = json.loads(Path(paths["telegram_callback_index_json"]).read_text(encoding="utf-8"))["callbacks"]
    assert "tok:T1" in callbacks
    assert "pos:P1" in callbacks
    assert Path(paths["site_dashboard_data_json"]).exists()
