#!/usr/bin/env python3
"""SIKK read-only unified query layer.

统一查询层：把 dashboard_data.json / live_state / paper JSON / case files 聚合为
一个总览命令和一个单币详情命令。只读；不执行 swap、不签名、不广播。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional

import sikk_dashboard_site_builder as dashboard

QUERY_BOUNDARY = "只读统一查询层；不执行真实 swap，不读取私钥，不签名，不自动 broadcast。"


def _text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    s = str(value).strip()
    return s if s and s.lower() not in {"none", "null", "nan"} else default


def _token_of(row: Mapping[str, Any]) -> str:
    return _text(row.get("token_address") or row.get("代币地址") or row.get("address") or row.get("token") or row.get("mint"))


def _symbol_of(row: Mapping[str, Any]) -> str:
    return _text(row.get("token_symbol") or row.get("代币符号") or row.get("symbol"), "UNKNOWN")


def _norm_query(value: str) -> str:
    return _text(value).lower()


def _position_key(row: Mapping[str, Any]) -> str:
    return _token_of(row)


def _latest_position_for(token: str, positions: Mapping[str, Any]) -> Optional[Dict[str, Any]]:
    target = _norm_query(token)
    for row in list(positions.get("open") or []) + list(positions.get("closed") or []):
        if not isinstance(row, Mapping):
            continue
        if target in {_norm_query(_position_key(row)), _norm_query(_symbol_of(row))}:
            return dict(row)
    return None


def _stage_evidence(token_row: Mapping[str, Any], paper_position: Optional[Mapping[str, Any]]) -> List[Dict[str, str]]:
    return [
        {
            "阶段": "P0 候选发现",
            "状态": "已进入" if _token_of(token_row) else "待查",
            "证据": _text(token_row.get("discovery_market_cap_usd"), "发现市值待补"),
        },
        {
            "阶段": "P1 K线吸筹与信号",
            "状态": _text(token_row.get("signal_level"), "UNKNOWN"),
            "证据": _text(token_row.get("signal_gate"), "信号门待补"),
        },
        {
            "阶段": "P2 钱包结构门禁",
            "状态": _text(token_row.get("wallet_structure_status"), "MISSING"),
            "证据": f"结构分={_text(token_row.get('wallet_structure_score'), '0')} / 风险分={_text(token_row.get('wallet_risk_score'), '0')} / 对手盘压力={_text(token_row.get('counterparty_pressure_score'), '0')}",
        },
        {
            "阶段": "P3 报价安全确认",
            "状态": f"{_text(token_row.get('quote_gate'), 'MISSING')} / {_text(token_row.get('security_gate'), 'MISSING')}",
            "证据": _text(token_row.get("main_reason"), "待补"),
        },
        {
            "阶段": "P4 纸面买入",
            "状态": "已纸面买入" if paper_position else "未纸面买入",
            "证据": _text((paper_position or {}).get("paper_entry_time"), "纸面入场待补"),
        },
        {
            "阶段": "P5 持仓监控与退出",
            "状态": _text((paper_position or {}).get("status") or token_row.get("paper_status"), "NONE"),
            "证据": f"收益={_text((paper_position or {}).get('paper_pnl_pct') or token_row.get('paper_pnl_pct'), '0')}%",
        },
        {
            "阶段": "P6 复盘校准",
            "状态": "进入 case/daily report" if paper_position else "待形成纸面样本",
            "证据": _text((paper_position or {}).get("case_file_md"), "case file 待生成或待关联"),
        },
    ]


def build_query_index(base_dir: str | Path) -> Dict[str, Any]:
    """Build a read-only query index from the existing SIKK live output root."""
    base = Path(base_dir)
    data = dashboard.build_dashboard_data(base)
    tokens = list(data.get("tokens") or [])
    paper_positions = dict(data.get("paper_positions") or {})
    board = {
        "token_count": len(tokens),
        "paper_open_count": paper_positions.get("open_count", 0),
        "paper_closed_count": paper_positions.get("closed_count", 0),
        "wallet_missing_count": (data.get("kpi") or {}).get("wallet_missing_count", 0),
        "wallet_coverage": (data.get("kpi") or {}).get("wallet_structure_coverage", 0),
        "opportunity_count": len(data.get("opportunities") or []),
        "generated_at": (data.get("meta") or {}).get("generated_at"),
        "source_last_update": (data.get("meta") or {}).get("source_last_update"),
    }
    return {
        "boundary": QUERY_BOUNDARY,
        "base_dir": str(base),
        "board": board,
        "tokens": tokens,
        "paper_positions": paper_positions,
        "wallet_structure_summary": data.get("wallet_structure_summary") or {},
        "wallet_missing_reasons": data.get("wallet_missing_reasons") or {},
        "coverage_diagnostics": data.get("coverage_diagnostics") or {},
        "entry_block_reasons": data.get("entry_block_reasons") or {},
        "events": data.get("events") or [],
    }


def get_token_detail(index: Mapping[str, Any], query: str) -> Dict[str, Any]:
    """Return a single token detail by symbol or address, case-insensitive."""
    q = _norm_query(query)
    if not q:
        raise KeyError("empty query")
    matched: Optional[Mapping[str, Any]] = None
    for row in index.get("tokens") or []:
        if not isinstance(row, Mapping):
            continue
        if q in {_norm_query(_token_of(row)), _norm_query(_symbol_of(row))}:
            matched = row
            break
    if matched is None:
        # fallback: partial address/symbol match for mobile use
        for row in index.get("tokens") or []:
            if not isinstance(row, Mapping):
                continue
            hay = f"{_token_of(row)} {_symbol_of(row)}".lower()
            if q in hay:
                matched = row
                break
    if matched is None:
        # Some older open paper positions no longer appear in current live_state/token_status.
        # Keep the query layer useful by synthesizing a detail row from paper JSON + case file.
        pos = _latest_position_for(query, index.get("paper_positions") or {})
        if pos:
            matched = {
                "token_address": _token_of(pos),
                "token_symbol": _symbol_of(pos),
                "current_state": _text(pos.get("status") or pos.get("paper_status"), "PAPER_OPEN"),
                "paper_status": _text(pos.get("status") or pos.get("paper_status"), "OPEN"),
                "priority_level": "P0_ACTIVE_POSITION",
                "signal_level": _text(pos.get("signal_level"), "UNKNOWN"),
                "wallet_structure_status": _text(pos.get("wallet_structure_status"), "MISSING"),
                "wallet_structure_score": pos.get("wallet_structure_score", 0),
                "wallet_risk_score": pos.get("wallet_risk_score", 0),
                "counterparty_pressure_score": pos.get("counterparty_pressure_score", 0),
                "quote_gate": _text(pos.get("quote_gate"), "MISSING"),
                "security_gate": _text(pos.get("security_gate"), "MISSING"),
                "main_reason": "纸面仓位存在，但当前 token_status 未覆盖；从 paper_live 聚合。",
                "next_action": _text(pos.get("wallet_exit_action") or pos.get("wallet_position_action"), "HOLD"),
            }
    if matched is None:
        raise KeyError(f"未找到代币：{query}")
    token = _token_of(matched)
    paper_position = _latest_position_for(token, index.get("paper_positions") or {})
    detail = dict(matched)
    detail.update({
        "boundary": index.get("boundary", QUERY_BOUNDARY),
        "paper_position": paper_position,
        "stage_evidence": _stage_evidence(matched, paper_position),
        "evidence_quality": infer_evidence_quality(matched, paper_position),
    })
    return detail


def infer_evidence_quality(token_row: Mapping[str, Any], paper_position: Optional[Mapping[str, Any]]) -> str:
    missing = []
    checks = {
        "发现市值": token_row.get("discovery_market_cap_usd"),
        "钱包结构": token_row.get("wallet_structure_status") if token_row.get("wallet_structure_status") != "MISSING" else "",
        "主导侧生命周期": token_row.get("operator_lifecycle_stage") if token_row.get("operator_lifecycle_stage") != "UNKNOWN" else "",
        "对手盘压力": token_row.get("counterparty_pressure_score"),
        "纸面入场": (paper_position or {}).get("paper_entry_time"),
        "实战档案": (paper_position or {}).get("case_file_md"),
    }
    for label, value in checks.items():
        if not _text(value):
            missing.append(label)
    if not missing:
        return "E3_可复盘"
    if len(missing) <= 2:
        return "E2_部分可复盘｜待补：" + "、".join(missing)
    return "E1_记录型样本｜核心证据待补：" + "、".join(missing)


def _format_counts(obj: Mapping[str, Any]) -> str:
    if not obj:
        return "- 暂无统计"
    return "\n".join(f"- {k}: {v}" for k, v in obj.items())


def format_board(index: Mapping[str, Any]) -> str:
    b = index.get("board") or {}
    d = index.get("coverage_diagnostics") or {}
    sync = d.get("paper_json_csv_sync") or {}
    safe = d.get("safety_defaults") or {}
    return "\n".join([
        "## SIKK 统一查询层总览",
        f"- 安全边界: {index.get('boundary', QUERY_BOUNDARY)}",
        f"- 输出目录: {index.get('base_dir')}",
        f"- 生成时间: {_text(b.get('generated_at'), '待补')}",
        f"- 候选币总数: {b.get('token_count', 0)}",
        f"- 钱包结构覆盖: {b.get('wallet_coverage', 0)}/{b.get('token_count', 0)}",
        f"- 钱包结构未接入: {b.get('wallet_missing_count', 0)}",
        f"- 重点机会数: {b.get('opportunity_count', 0)}",
        f"- 当前开放纸面仓位: {b.get('paper_open_count', 0)}",
        f"- 累计关闭纸面仓位: {b.get('paper_closed_count', 0)}",
        "\n## 覆盖诊断",
        f"- 钱包缺口率: {_text(d.get('wallet_missing_rate_pct'), '0')}%",
        f"- JSON/CSV 同步: open_json={_text(sync.get('open_json_count'), '0')} / closed_json={_text(sync.get('closed_json_count'), '0')} / open_csv={sync.get('open_csv_exists')} / closed_csv={sync.get('closed_csv_exists')}",
        f"- 安全默认关闭: real_swap_enabled={safe.get('real_swap_enabled')} / broadcast_allowed={safe.get('broadcast_allowed')} / private_key_required={safe.get('private_key_required')}",
        "- 钱包结构缺口修复计划:",
        "\n".join(f"  - {x}" for x in (d.get('wallet_missing_repair_plan') or ["暂无缺口"])),
        "\n## 钱包结构分布",
        _format_counts(index.get("wallet_structure_summary") or {}),
        "\n## 未入场/阻断原因",
        _format_counts(index.get("entry_block_reasons") or {}),
        "\n## 固定入口",
        "- 总览: `python3 sikk_query.py board --base-dir data/gmgn_candidates_live_run`",
        "- 单币: `python3 sikk_query.py token <symbol_or_address> --base-dir data/gmgn_candidates_live_run`",
    ])


def _format_position(p: Optional[Mapping[str, Any]]) -> List[str]:
    if not p:
        return ["- 纸面仓位: 暂无纸面买入记录"]
    return [
        f"- 纸面仓位: {_text(p.get('status') or p.get('paper_status'), 'OPEN/CLOSED 待查')}",
        f"- 纸面买入时间: {_text(p.get('paper_entry_time'), '待补')}",
        f"- 纸面买入数量: {_text(p.get('paper_position_sol'), '待补')} SOL",
        f"- 入场价: {_text(p.get('paper_entry_price'), '待补')}",
        f"- 当前价: {_text(p.get('paper_current_price'), '待补')}",
        f"- 当前收益: {_text(p.get('paper_pnl_pct'), '0')}%",
        f"- 实战档案: {_text(p.get('case_file_md'), '待生成或待关联')}",
    ]


def format_token_detail(detail: Mapping[str, Any]) -> str:
    lines = [
        "## SIKK 单币详情",
        f"- 代币: {_symbol_of(detail)}",
        f"- 地址: {_token_of(detail)}",
        f"- 状态: {_text(detail.get('current_state'), 'UNKNOWN')}",
        f"- 优先级: {_text(detail.get('priority_level'), '待补')}",
        f"- 信号: {_text(detail.get('signal_level'), 'UNKNOWN')}",
        f"- 钱包结构: {_text(detail.get('wallet_structure_status'), 'MISSING')}｜结构分 {_text(detail.get('wallet_structure_score'), '0')}｜风险分 {_text(detail.get('wallet_risk_score'), '0')}｜对手盘压力 {_text(detail.get('counterparty_pressure_score'), '0')}",
        f"- 主导侧生命周期: {_text(detail.get('operator_lifecycle_stage'), 'UNKNOWN')}",
        f"- 主导侧心理: {_text(detail.get('operator_psychology_label'), '证据不足 / 待复查')}",
        f"- 阻断/观察原因: {_text(detail.get('main_reason'), '待补')}",
        f"- 下一步动作: {_text(detail.get('next_action'), '待补')}",
        f"- Case 质量: {_text(detail.get('case_quality'), '待补')}",
        f"- Paper 动作: {_text(detail.get('paper_action') or detail.get('next_action'), '待补')}",
        f"- 证据缺口: {', '.join(detail.get('missing_fields') or []) or '无'}",
        f"- 证据质量: {_text(detail.get('evidence_quality'), 'E1_待补')}",
        "\n## 纸面仓位",
    ]
    lines.extend(_format_position(detail.get("paper_position")))
    lines.append("\n## 阶段证据")
    for row in detail.get("stage_evidence") or []:
        lines.append(f"- {row.get('阶段')}: {row.get('状态')}｜{row.get('证据')}")
    lines.append("\n## 安全边界")
    lines.append(f"- {detail.get('boundary', QUERY_BOUNDARY)}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SIKK read-only unified query layer")
    sub = parser.add_subparsers(dest="command", required=True)
    p_board = sub.add_parser("board", help="显示 SIKK 总览")
    p_board.add_argument("--base-dir", default="data/gmgn_candidates_live_run")
    p_token = sub.add_parser("token", help="显示单币详情")
    p_token.add_argument("query", help="代币符号或地址")
    p_token.add_argument("--base-dir", default="data/gmgn_candidates_live_run")
    p_json = sub.add_parser("json", help="输出统一查询层 JSON")
    p_json.add_argument("--base-dir", default="data/gmgn_candidates_live_run")
    return parser


def run_cli(argv: Optional[List[str]] = None) -> str:
    args = build_parser().parse_args(argv)
    index = build_query_index(args.base_dir)
    if args.command == "board":
        return format_board(index)
    if args.command == "token":
        return format_token_detail(get_token_detail(index, args.query))
    if args.command == "json":
        return json.dumps(index, ensure_ascii=False, indent=2)
    raise SystemExit(f"unknown command: {args.command}")


def main(argv: Optional[List[str]] = None) -> int:
    print(run_cli(argv))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
