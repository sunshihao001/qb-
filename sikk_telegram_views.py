#!/usr/bin/env python3
"""SIKK Telegram 中文视图函数层。

本模块只把统一索引渲染成 Telegram bot 可发送的 payload，不直接连接 Telegram，
不执行真实交易、不签名、不广播。callback_data 使用短码，用户可见内容中文化。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping

import sikk_telegram_zh as zh

DEFAULT_INDEX_DIR = Path("data/gmgn_candidates_live_run/index")
FORBIDDEN_ACTION_WORDS = {"BUY", "SELL", "SWAP", "EXECUTE", "APPROVE", "BROADCAST"}


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _index_dir(path: str | Path = DEFAULT_INDEX_DIR) -> Path:
    p = Path(path)
    if p.name != "index" and (p / "index").exists():
        return p / "index"
    return p


def _text(value: Any, default: str = "待补") -> str:
    s = str(value or "").strip()
    return s if s and s.lower() not in {"none", "null", "nan"} else default


def _num_text(value: Any, suffix: str = "") -> str:
    s = _text(value, "待补")
    return f"{s}{suffix}" if s != "待补" and suffix and not s.endswith(suffix) else s


def _button(text: str, callback_data: str) -> Dict[str, str]:
    return {"text": text, "callback_data": callback_data}


def _payload(text: str, rows: List[List[Dict[str, str]]], source: str = "") -> Dict[str, Any]:
    flat = [b for row in rows for b in row]
    return {"text": text, "buttons": rows, "buttons_flat": flat, "source": source, "boundary": zh.SAFETY_NOTE}


def _load_indexes(index_dir: str | Path) -> Dict[str, Any]:
    root = _index_dir(index_dir)
    return {
        "root": root,
        "system": _read_json(root / "system_index.json", {}),
        "tokens": _read_json(root / "token_detail_index.json", {"tokens": []}),
        "positions": _read_json(root / "position_index.json", {"open_positions": [], "closed_positions": []}),
        "open": _read_json(root / "latest_open_positions.json", {"open_positions": []}),
        "closed": _read_json(root / "latest_closed_positions.json", {"closed_positions": []}),
        "alerts": _read_json(root / "alert_index.json", {"alerts": []}),
        "callbacks": _read_json(root / "telegram_callback_index.json", {"callbacks": {}}),
        "cases": _read_json(root / "case_file_index.json", {"cases": []}),
        "reviews": _read_json(root / "auto_review_index.json", {}),
    }


def render_main_menu(index_dir: str | Path = DEFAULT_INDEX_DIR) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    sys = data["system"]
    counts = sys.get("counts") or {}
    safety = sys.get("safety") or {}
    text = "\n".join([
        "【SIKK 中文专业控制台】",
        "模式：只读观察 / paper-only",
        f"真实交易：{'开启' if safety.get('real_swap_enabled') else '关闭'}",
        f"广播交易：{'允许' if safety.get('broadcast_allowed') else '关闭'}",
        f"候选代币：{counts.get('token_count', 0)}",
        f"开放纸面仓位：{counts.get('open_position_count', 0)}",
        f"已关闭纸面仓位：{counts.get('closed_position_count', 0)}",
        f"风险提醒：{(data['alerts'].get('alert_count') or len(data['alerts'].get('alerts') or []))}",
        f"更新时间：{_text(sys.get('generated_at'))}",
        "安全边界：不执行真实 swap、不读取私钥、不签名、不广播。",
    ])
    rows = [
        [_button("开放仓位", "list:open:0"), _button("已关闭仓位", "list:closed:0")],
        [_button("风险提醒", "list:alerts:0"), _button("系统健康", "menu:health")],
        [_button("策略复盘", "menu:review"), _button("刷新数据", "refresh:main")],
    ]
    return _payload(text, rows, str(data["root"] / "system_index.json"))


def _position_label(pos: Mapping[str, Any]) -> str:
    symbol = _text(pos.get("token_symbol"), "UNKNOWN")
    pnl = _text(pos.get("paper_pnl_pct") or pos.get("当前收益率_pct") or pos.get("net_pnl_pct"), "待补")
    quality = zh.zh_status(pos.get("case_quality") or pos.get("evidence_quality") or pos.get("sample_quality") or "UNKNOWN")
    return f"{symbol}｜{pnl}%｜{quality}"


def render_open_positions(index_dir: str | Path = DEFAULT_INDEX_DIR, page: int = 0, page_size: int = 8) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    positions = list(data["open"].get("open_positions") or [])
    start = max(0, page) * page_size
    page_rows = positions[start:start + page_size]
    lines = ["【开放纸面仓位】", f"数量：{len(positions)}", "说明：仅展示 paper 仓位，不执行真实交易。"]
    rows: List[List[Dict[str, str]]] = []
    for pos in page_rows:
        code = _text(pos.get("position_short_id"), "")
        if code:
            rows.append([_button(_position_label(pos), f"pos:{code}")])
    rows.append([_button("返回主菜单", "menu:main"), _button("刷新", "refresh:main")])
    return _payload("\n".join(lines), rows, str(data["root"] / "latest_open_positions.json"))


def _find_position(data: Mapping[str, Any], short_code: str) -> Dict[str, Any]:
    code = short_code.replace("pos:", "")
    for pos in list((data["positions"].get("open_positions") or [])) + list((data["positions"].get("closed_positions") or [])):
        if _text(pos.get("position_short_id"), "") == code or _text(pos.get("position_id"), "") == code:
            return dict(pos)
    return {}


def render_position_detail(index_dir: str | Path, callback_data: str) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    pos = _find_position(data, callback_data)
    symbol = _text(pos.get("token_symbol"), "UNKNOWN")
    wallet_status = zh.zh_status(pos.get("wallet_structure_status") or pos.get("entry_wallet_structure_status"))
    action = zh.safe_action_text(pos.get("next_action") or pos.get("wallet_position_action") or pos.get("wallet_exit_action") or "观察")
    missing = _text(pos.get("evidence_missing_fields") or pos.get("missing_fields") or pos.get("case_missing_fields"), "待补")
    lines = [
        f"【{symbol} 纸面仓位详情】",
        f"仓位状态：{zh.zh_status(pos.get('position_status') or pos.get('status'))}",
        f"入场时间：{_text(pos.get('paper_entry_time') or pos.get('entry_time'))}",
        f"入场价格：{_text(pos.get('paper_entry_price') or pos.get('entry_price') or pos.get('live_entry_price'))}",
        f"仓位规模：{_num_text(pos.get('paper_size_sol') or pos.get('position_sol'), ' SOL')}",
        f"当前收益：{_num_text(pos.get('paper_pnl_pct') or pos.get('当前收益率_pct') or pos.get('net_pnl_pct'), '%')}",
        f"最大回撤：{_num_text(pos.get('max_drawdown_pct') or pos.get('最大回撤_pct'), '%')}",
        f"样本质量：{zh.zh_status(pos.get('case_quality') or pos.get('sample_quality') or pos.get('evidence_quality'))}",
        f"钱包结构：{wallet_status}",
        f"缺失证据：{missing}",
        f"下一步动作：{action}",
        "安全边界：只读复盘，不执行真实交易。",
    ]
    code = callback_data.replace("pos:", "")
    rows = [
        [_button("入场证据", f"entry:{code}"), _button("自动复盘", f"review:{code}")],
        [_button("返回开放仓位", "list:open:0"), _button("返回主菜单", "menu:main")],
    ]
    return _payload("\n".join(lines), rows, str(data["root"] / "position_index.json"))


def render_alerts(index_dir: str | Path = DEFAULT_INDEX_DIR) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    alerts = list(data["alerts"].get("alerts") or [])
    lines = ["【风险提醒】", "说明：只读提醒，不执行、不授权、不广播真实交易。", f"数量：{len(alerts)}"]
    rows: List[List[Dict[str, str]]] = []
    for alert in alerts[:10]:
        action = zh.safe_action_text(alert.get("action"))
        text = f"{_text(alert.get('severity'))}｜{_text(alert.get('title'))}｜{action}"
        aid = _text(alert.get("alert_id"), "")
        if aid:
            rows.append([_button(text, f"alert:{aid}")])
        else:
            lines.append(f"- {text}")
    rows.append([_button("返回主菜单", "menu:main"), _button("刷新", "refresh:main")])
    return _payload("\n".join(lines), rows, str(data["root"] / "alert_index.json"))


def _find_token(data: Mapping[str, Any], callback_data: str) -> Dict[str, Any]:
    code = callback_data.replace("tok:", "")
    for token in data["tokens"].get("tokens", []) or []:
        if _text(token.get("token_id"), "") == code:
            return dict(token)
    return {}


def _case_for_token(data: Mapping[str, Any], token_address: str) -> str:
    for case in data["cases"].get("cases", []) or []:
        if _text(case.get("token_address"), "") == _text(token_address, ""):
            return _text(case.get("case_short_id"), "C1")
    return "C1"


def _position_for_token(data: Mapping[str, Any], token_address: str) -> str:
    for pos in list(data["positions"].get("open_positions") or []) + list(data["positions"].get("closed_positions") or []):
        if _text(pos.get("token_address"), "") == _text(token_address, ""):
            return _text(pos.get("position_short_id"), "P1")
    return "P1"


def render_token_detail(index_dir: str | Path, callback_data: str) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    token = _find_token(data, callback_data)
    symbol = _text(token.get("token_symbol"), "UNKNOWN")
    token_addr = _text(token.get("token_address"), "")
    pos_code = _position_for_token(data, token_addr)
    case_code = _case_for_token(data, token_addr)
    lines = [
        f"【{symbol} 代币详情】",
        f"状态：{zh.zh_status(token.get('状态') or token.get('current_state'))}",
        f"信号等级：{_text(token.get('信号等级') or token.get('signal_level'))}",
        f"钱包结构：{zh.zh_status(token.get('钱包结构') or token.get('wallet_structure_status'))}",
        f"主导侧心理：{_text(token.get('主导侧心理') or token.get('operator_psychology_label'))}",
        f"观察重点：{_text(token.get('观察重点') or token.get('next_observation_focus'))}",
        "安全边界：只读详情，不执行真实交易。",
    ]
    rows = [
        [_button("入场证据", f"entry:{pos_code}"), _button("钱包结构", f"wallet:{pos_code}")],
        [_button("OKX 集群", f"okx:{pos_code}"), _button("自动复盘", f"review:{pos_code}")],
        [_button("完整档案", f"case:{case_code}"), _button("返回主菜单", "menu:main")],
    ]
    return _payload("\n".join(lines), rows, str(data["root"] / "token_detail_index.json"))


def render_case_detail(index_dir: str | Path, callback_data: str) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    code = callback_data.replace("case:", "")
    case = {}
    for item in data["cases"].get("cases", []) or []:
        if _text(item.get("case_short_id"), "") == code:
            case = dict(item); break
    path = _text(case.get("case_file_md") or case.get("case_file_json") or case.get("case_file") or case.get("path"), "待补")
    lines = [
        f"【完整档案 {code}】",
        f"代币：{_text(case.get('token_symbol'), 'UNKNOWN')}",
        f"状态：{zh.zh_status(case.get('status'))}",
        f"证据路径：{path}",
        "说明：Case File 为纸面实战档案索引，只读展示。",
    ]
    return _payload("\n".join(lines), [[_button("返回主菜单", "menu:main")]], str(data["root"] / "case_file_index.json"))


def render_review_detail(index_dir: str | Path, callback_data: str) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    code = callback_data.replace("review:", "")
    review = data["reviews"]
    status = _text(review.get("review_status"), "待补") if isinstance(review, Mapping) else "待补"
    summary = review.get("strategy_summary") if isinstance(review, Mapping) and isinstance(review.get("strategy_summary"), Mapping) else {}
    lines = [
        f"【自动复盘 {code}】",
        f"复盘状态：{status}",
        f"策略摘要：{_text(summary or review.get('scope_note') if isinstance(review, Mapping) else '')}",
        "说明：自动复盘索引聚合策略表现与样本质量，不输出真实交易建议。",
        "安全边界：只读复盘，不执行真实 swap、不签名、不广播。",
    ]
    return _payload("\n".join(lines), [[_button("返回主菜单", "menu:main")]], str(data["root"] / "auto_review_index.json"))


def _as_lines(value: Any, default: str = "待补") -> str:
    if isinstance(value, list):
        clean = [_text(v, "") for v in value]
        clean = [v for v in clean if v]
        return "、".join(clean) if clean else default
    if isinstance(value, Mapping):
        if not value:
            return default
        return "；".join(f"{k}={_text(v)}" for k, v in value.items())
    return _text(value, default)


def _find_token_by_address(data: Mapping[str, Any], token_address: str) -> Dict[str, Any]:
    wanted = _text(token_address, "")
    for token in data["tokens"].get("tokens", []) or []:
        if _text(token.get("token_address"), "") == wanted:
            return dict(token)
    return {}


def _safe_code(callback_data: str, prefix: str) -> str:
    return str(callback_data or "").replace(prefix, "", 1)


def _case_for_position(data: Mapping[str, Any], pos: Mapping[str, Any]) -> str:
    token = _text(pos.get("token_address"), "")
    pid = _text(pos.get("position_id"), "")
    for case in data["cases"].get("cases", []) or []:
        if token and _text(case.get("token_address"), "") == token:
            return _text(case.get("case_short_id"), "C1")
        if pid and _text(case.get("position_id"), "") == pid:
            return _text(case.get("case_short_id"), "C1")
    return "C1"


def render_entry_detail(index_dir: str | Path, callback_data: str) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    code = callback_data.replace("entry:", "")
    pos = _find_position(data, f"pos:{code}")
    symbol = _text(pos.get("token_symbol"), "UNKNOWN")
    case_code = _case_for_position(data, pos)
    why = _text(pos.get("entry_reason") or pos.get("main_reason") or pos.get("paper_entry_reason") or pos.get("入场原因"), "信号/钱包/报价/安全证据待复查")
    lines = [
        f"【{symbol} 入场证据 {code}】",
        f"发现时间：{_text(pos.get('candidate_discovered_at') or pos.get('discovery_time') or pos.get('发现时间'))}",
        f"发现市值：{_num_text(pos.get('discovery_market_cap_usd') or pos.get('发现市值USD'), ' USD')}",
        f"入场时间：{_text(pos.get('paper_entry_time') or pos.get('entry_time') or pos.get('入场时间'))}",
        f"入场市值：{_num_text(pos.get('paper_entry_market_cap_usd') or pos.get('entry_market_cap_usd') or pos.get('入场市值USD'), ' USD')}",
        f"买入 SOL：{_num_text(pos.get('paper_size_sol') or pos.get('paper_position_sol') or pos.get('position_sol') or pos.get('模拟仓位SOL'), ' SOL')}",
        f"估算 Token：{_text(pos.get('estimated_token_amount') or pos.get('token_amount') or pos.get('估算Token数量'))}",
        f"信号等级：{_text(pos.get('signal_level') or pos.get('信号等级'))}",
        f"钱包结构：{zh.zh_status(pos.get('wallet_structure_status') or pos.get('entry_wallet_structure_status'))}",
        f"Quote/Security：{zh.zh_status(pos.get('quote_gate'))} / {zh.zh_status(pos.get('security_gate'))}",
        f"为什么入场：{why}",
        "安全边界：入场证据只读展示；不执行真实交易、不签名、不广播。",
    ]
    rows = [
        [_button("返回仓位", f"pos:{code}"), _button("Case File", f"case:{case_code}")],
        [_button("自动复盘", f"review:{code}"), _button("返回主菜单", "menu:main")],
    ]
    return _payload("\n".join(lines), rows, str(data["root"] / "position_index.json"))


def render_wallet_structure_detail(index_dir: str | Path, callback_data: str) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    code = _safe_code(callback_data, "wallet:")
    pos = _find_position(data, f"pos:{code}")
    token = _find_token_by_address(data, pos.get("token_address"))
    symbol = _text(pos.get("token_symbol") or token.get("token_symbol"), "UNKNOWN")
    status = pos.get("wallet_structure_status") or token.get("wallet_structure_status") or pos.get("entry_wallet_structure_status")
    lines = [
        f"【{symbol} 钱包结构 {code}】",
        f"结构状态：{zh.zh_status(status)}",
        f"结构分：{_text(pos.get('wallet_structure_score') or token.get('wallet_structure_score'), '0.0')}",
        f"风险分：{_text(pos.get('wallet_risk_score') or token.get('wallet_risk_score'), '0.0')}",
        f"对手盘压力：{_text(pos.get('counterparty_pressure_score') or token.get('counterparty_pressure_score'), '0.0')}",
        f"证据等级：{_text(pos.get('wallet_evidence_level') or token.get('wallet_evidence_level'))}",
        f"结构原因：{_text(pos.get('wallet_structure_reason') or token.get('wallet_structure_reason') or token.get('wallet_missing_reason'), '钱包结构输入待补')}",
        f"缺失字段：{_as_lines(pos.get('missing_fields') or token.get('missing_fields') or token.get('evidence_missing_fields'))}",
        "安全边界：钱包结构只读展示；不执行真实交易、不签名、不广播。",
    ]
    rows = [[_button("返回代币", f"tok:{token.get('token_id', 'T1')}"), _button("返回仓位", f"pos:{code}")], [_button("返回主菜单", "menu:main")]]
    return _payload("\n".join(lines), rows, str(data["root"] / "position_index.json"))


def render_okx_cluster_detail(index_dir: str | Path, callback_data: str) -> Dict[str, Any]:
    data = _load_indexes(index_dir)
    code = _safe_code(callback_data, "okx:")
    pos = _find_position(data, f"pos:{code}")
    token = _find_token_by_address(data, pos.get("token_address"))
    symbol = _text(pos.get("token_symbol") or token.get("token_symbol"), "UNKNOWN")
    status = pos.get("okx_cluster_status") or token.get("okx_cluster_status") or "待接入 / 资金层跳过"
    lines = [
        f"【{symbol} OKX 集群 {code}】",
        f"集群状态：{_text(status)}",
        f"集群分：{_text(pos.get('okx_cluster_score') or token.get('okx_cluster_score'))}",
        f"风险分：{_text(pos.get('okx_cluster_risk_score') or token.get('okx_cluster_risk_score'))}",
        f"派发分：{_text(pos.get('okx_cluster_distribution_score') or token.get('okx_cluster_distribution_score'))}",
        f"控筹留存分：{_text(pos.get('okx_cluster_control_retention_score') or token.get('okx_cluster_control_retention_score'))}",
        f"最大集群持仓：{_num_text(pos.get('largest_cluster_holding_pct') or token.get('largest_cluster_holding_pct'), '%')}",
        f"说明：OKX 集群字段当前按统一索引只读展示；缺失时标记为资金层跳过/待复查。",
        "安全边界：OKX 集群只读展示；不执行链上查询写入、不签名、不广播。",
    ]
    rows = [[_button("钱包结构", f"wallet:{code}"), _button("完整档案", f"case:{_case_for_position(data, pos)}")], [_button("返回主菜单", "menu:main")]]
    return _payload("\n".join(lines), rows, str(data["root"] / "token_detail_index.json"))


def render_by_callback(index_dir: str | Path, callback_data: str) -> Dict[str, Any]:
    if callback_data == "menu:main" or callback_data == "refresh:main":
        return render_main_menu(index_dir)
    if callback_data.startswith("list:open"):
        return render_open_positions(index_dir)
    if callback_data.startswith("list:alerts"):
        return render_alerts(index_dir)
    if callback_data.startswith("pos:"):
        return render_position_detail(index_dir, callback_data)
    if callback_data.startswith("tok:"):
        return render_token_detail(index_dir, callback_data)
    if callback_data.startswith("case:"):
        return render_case_detail(index_dir, callback_data)
    if callback_data.startswith("review:"):
        return render_review_detail(index_dir, callback_data)
    if callback_data.startswith("entry:"):
        return render_entry_detail(index_dir, callback_data)
    if callback_data.startswith("wallet:"):
        return render_wallet_structure_detail(index_dir, callback_data)
    if callback_data.startswith("okx:"):
        return render_okx_cluster_detail(index_dir, callback_data)
    return _payload("【暂未接入】\n该按钮已保留，后续阶段接入详情页。", [[_button("返回主菜单", "menu:main")]], str(_index_dir(index_dir)))
