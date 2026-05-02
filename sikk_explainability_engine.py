#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Explainability Engine v0.1.

专业解释引擎：只解释 token_status、wallet_structure_decision、状态机、quote/security、
paper positions、failure attribution、process_trace 等既有输出，不重新裁决、不采集、不报价、
不签名、不广播、不执行真实交易。
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

DEFAULT_LIVE_RUN_DIR = Path("data/gmgn_candidates_live_run")
EXPLANATION_KEYS = [
    "为什么发现",
    "为什么观察",
    "为什么支持",
    "为什么暂停",
    "为什么阻断",
    "为什么进入paper",
    "为什么退出",
    "为什么失败",
    "下一步看什么",
    "主要失效条件",
    "替代假设",
]


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__read_error__": str(exc), "__path__": str(path)}


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
            if isinstance(item, dict):
                item.setdefault("__line__", line_no)
                rows.append(item)
        except Exception:
            rows.append({"__read_error__": line[:200], "__line__": line_no})
    return rows


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _rows(payload: Any, keys: Sequence[str]) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [dict(x) for x in payload if isinstance(x, Mapping)]
    if not isinstance(payload, Mapping):
        return []
    for key in keys:
        value = payload.get(key)
        if isinstance(value, list):
            return [dict(x) for x in value if isinstance(x, Mapping)]
    return []


def _token(row: Mapping[str, Any]) -> str:
    return str(row.get("token_address") or row.get("代币地址") or row.get("token") or row.get("address") or row.get("mint") or "")


def _symbol(row: Mapping[str, Any]) -> str:
    return str(row.get("token_symbol") or row.get("代币符号") or row.get("symbol") or "")


def _index(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        t = _token(row)
        if t:
            out[t] = dict(row)
    return out


def _latest_by_token(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        t = _token(row)
        if t:
            out[t] = dict(row)
    return out


def _evidence(status: str, text: str, source: str, field: str | None = None) -> Dict[str, str]:
    return {"status": status, "text": text, "source": source, "field": field or ""}


def _present(value: Any) -> bool:
    return value not in (None, "", [], {})


def _field(row: Mapping[str, Any], *names: str) -> Any:
    for name in names:
        if _present(row.get(name)):
            return row.get(name)
    return None


def _append_if_present(items: List[Dict[str, str]], value: Any, source: str, field: str, prefix: str) -> None:
    if _present(value):
        items.append(_evidence("有证据", f"{prefix}：{value}", source, field))


def _missing(question: str, source: str) -> Dict[str, str]:
    return _evidence("证据缺失/待复查", f"{question}：未在输入中找到可引用字段，待复查；不据此新增结论。", source)


def _explain_token(
    *,
    token: str,
    status: Mapping[str, Any],
    wallet: Mapping[str, Any] | None,
    quote: Mapping[str, Any] | None,
    paper_open: Mapping[str, Any] | None,
    paper_closed: Mapping[str, Any] | None,
    failure: Mapping[str, Any] | None,
    trace: Sequence[Mapping[str, Any]],
    sources: Mapping[str, str],
) -> Dict[str, Any]:
    wallet = wallet or {}
    quote = quote or {}
    paper_open = paper_open or {}
    paper_closed = paper_closed or {}
    failure = failure or {}
    current_state = str(status.get("current_state") or status.get("当前状态") or "UNKNOWN")
    latest_action = status.get("latest_action") or status.get("下一步动作")
    latest_reason = status.get("latest_reason") or status.get("状态原因")
    wallet_status = _field(wallet, "wallet_structure_status", "钱包结构结论") or _field(status.get("wallet_structure", {}) if isinstance(status.get("wallet_structure"), Mapping) else {}, "wallet_structure_status")
    quote_gate = _field(quote, "quote_security_permission", "最终权限", "quote_gate") or _field(status.get("quote", {}) if isinstance(status.get("quote"), Mapping) else {}, "quote_gate")
    security_gate = _field(quote, "交易前状态", "pre_trade_state", "security_gate") or _field(status.get("security", {}) if isinstance(status.get("security"), Mapping) else {}, "security_gate")

    q: Dict[str, List[Dict[str, str]]] = {key: [] for key in EXPLANATION_KEYS}

    # 发现/观察：来自 token_status 与 process_trace，只解释已有状态。
    _append_if_present(q["为什么发现"], status.get("last_update") or status.get("discovered_at"), sources.get("token_status", "token_status.json"), "last_update", "token_status 出现/更新时间")
    _append_if_present(q["为什么发现"], _symbol(status), sources.get("token_status", "token_status.json"), "token_symbol", "发现对象符号")
    if not q["为什么发现"]:
        q["为什么发现"].append(_missing("为什么发现", sources.get("token_status", "token_status.json")))

    if current_state.upper() in {"WATCHING", "DISCOVERED", "ACCUMULATING"} or trace:
        _append_if_present(q["为什么观察"], current_state, sources.get("token_status", "token_status.json"), "current_state", "当前状态")
        if trace:
            last_trace = trace[-1]
            q["为什么观察"].append(_evidence("有证据", f"最近流程记录：{last_trace.get('current_state')} / {last_trace.get('latest_reason')}", sources.get("process_trace", "process_trace.jsonl"), "current_state/latest_reason"))
    if not q["为什么观察"]:
        q["为什么观察"].append(_missing("为什么观察", sources.get("process_trace", "process_trace.jsonl")))

    # 支持/暂停/阻断：引用钱包、quote/security、状态，不改变结论。
    if str(wallet_status).upper() in {"WALLET_SUPPORT", "SUPPORT", "PASS"} or str(quote_gate).upper().startswith("ALLOW"):
        _append_if_present(q["为什么支持"], wallet_status, sources.get("wallet", "wallet_structure_decision.json"), "wallet_structure_status", "钱包结构结论")
        _append_if_present(q["为什么支持"], quote_gate, sources.get("quote", "quote_security_summary.json"), "quote_security_permission", "quote/security 权限")
        _append_if_present(q["为什么支持"], _field(quote, "原因", "reason"), sources.get("quote", "quote_security_summary.json"), "原因", "quote/security 原因")
    if not q["为什么支持"]:
        q["为什么支持"].append(_missing("为什么支持", f"{sources.get('wallet', 'wallet_structure_decision.json')}；{sources.get('quote', 'quote_security_summary.json')}"))

    if "PAUSE" in str(quote_gate).upper() or "PAUSE" in str(security_gate).upper() or current_state.upper() == "PAUSED":
        _append_if_present(q["为什么暂停"], quote_gate, sources.get("quote", "quote_security_summary.json"), "quote_security_permission", "quote/security 权限")
        _append_if_present(q["为什么暂停"], security_gate, sources.get("quote", "quote_security_summary.json"), "交易前状态", "安全层状态")
        _append_if_present(q["为什么暂停"], _field(quote, "原因", "reason"), sources.get("quote", "quote_security_summary.json"), "原因", "暂停原因")
    if not q["为什么暂停"]:
        q["为什么暂停"].append(_missing("为什么暂停", sources.get("quote", "quote_security_summary.json")))

    if "BLOCK" in current_state.upper() or "BLOCK" in str(wallet_status).upper() or "BLOCK" in str(quote_gate).upper() or "BLOCK" in str(security_gate).upper():
        _append_if_present(q["为什么阻断"], current_state, sources.get("token_status", "token_status.json"), "current_state", "当前状态")
        _append_if_present(q["为什么阻断"], wallet_status, sources.get("wallet", "wallet_structure_decision.json"), "wallet_structure_status", "钱包结构结论")
        _append_if_present(q["为什么阻断"], _field(wallet, "wallet_structure_reason", "状态调整原因"), sources.get("wallet", "wallet_structure_decision.json"), "wallet_structure_reason", "钱包结构原因")
        _append_if_present(q["为什么阻断"], quote_gate, sources.get("quote", "quote_security_summary.json"), "quote_security_permission", "quote/security 权限")
    if not q["为什么阻断"]:
        q["为什么阻断"].append(_missing("为什么阻断", f"{sources.get('token_status', 'token_status.json')}；{sources.get('wallet', 'wallet_structure_decision.json')}"))

    # paper entry/exit/failure.
    if current_state.upper() in {"PAPER_READY", "PAPER_OPEN", "READY_FOR_CONFIRMATION"} or paper_open:
        _append_if_present(q["为什么进入paper"], current_state, sources.get("token_status", "token_status.json"), "current_state", "当前状态")
        _append_if_present(q["为什么进入paper"], latest_action, sources.get("token_status", "token_status.json"), "latest_action", "最新动作")
        _append_if_present(q["为什么进入paper"], latest_reason, sources.get("token_status", "token_status.json"), "latest_reason", "入场依据")
        _append_if_present(q["为什么进入paper"], paper_open.get("entry_time"), sources.get("paper_open", "paper_positions_open.json"), "entry_time", "纸面入场时间")
    if not q["为什么进入paper"]:
        q["为什么进入paper"].append(_missing("为什么进入paper", f"{sources.get('token_status', 'token_status.json')}；{sources.get('paper_open', 'paper_positions_open.json')}"))

    if paper_closed or str(current_state).upper() in {"PAPER_EXITED", "EXITED"}:
        _append_if_present(q["为什么退出"], _field(paper_closed, "exit_reason", "退出原因"), sources.get("paper_closed", "paper_positions_closed.json"), "exit_reason", "纸面退出原因")
        _append_if_present(q["为什么退出"], _field(paper_closed, "exit_time", "退出时间"), sources.get("paper_closed", "paper_positions_closed.json"), "exit_time", "纸面退出时间")
        _append_if_present(q["为什么退出"], current_state, sources.get("token_status", "token_status.json"), "current_state", "当前状态")
    if not q["为什么退出"]:
        q["为什么退出"].append(_missing("为什么退出", sources.get("paper_closed", "paper_positions_closed.json")))

    if failure or "FAIL" in current_state.upper():
        _append_if_present(q["为什么失败"], _field(failure, "failure_type", "失败类型"), sources.get("failure", "failure_attribution.jsonl"), "failure_type", "失败类型")
        _append_if_present(q["为什么失败"], _field(failure, "failure_reason", "失败原因"), sources.get("failure", "failure_attribution.jsonl"), "failure_reason", "失败原因")
        _append_if_present(q["为什么失败"], current_state, sources.get("token_status", "token_status.json"), "current_state", "当前状态")
    if not q["为什么失败"]:
        q["为什么失败"].append(_missing("为什么失败", sources.get("failure", "failure_attribution.jsonl")))

    # next, failure conditions, alternatives: evidence-based checklist.
    q["下一步看什么"].extend([
        _evidence("待复查", f"复查最新状态/动作：{current_state} / {latest_action or '证据缺失'}", sources.get("token_status", "token_status.json"), "current_state/latest_action"),
        _evidence("待复查", f"复查钱包结构是否变化：{wallet_status or '证据缺失'}", sources.get("wallet", "wallet_structure_decision.json"), "wallet_structure_status"),
        _evidence("待复查", f"复查 quote/security：{quote_gate or '证据缺失'} / {security_gate or '证据缺失'}", sources.get("quote", "quote_security_summary.json"), "quote_security_permission/交易前状态"),
        _evidence("待复查", "如有纸面持仓，复查 paper_positions_open/closed 与 failure_attribution 是否一致", f"{sources.get('paper_open', 'paper_positions_open.json')}；{sources.get('paper_closed', 'paper_positions_closed.json')}；{sources.get('failure', 'failure_attribution.jsonl')}"),
    ])
    q["主要失效条件"].extend([
        _evidence("条件", "wallet_structure_status 变为 WALLET_BLOCK 或钱包风险/对手盘压力继续恶化", sources.get("wallet", "wallet_structure_decision.json"), "wallet_structure_status/wallet_risk_score/counterparty_pressure_score"),
        _evidence("条件", "quote/security 变为 PAUSE、BLOCK、MISSING 或 ERROR", sources.get("quote", "quote_security_summary.json"), "quote_security_permission/交易前状态"),
        _evidence("条件", "paper 仓位触发止损/强制退出/failure_attribution 归因为结构走弱或执行失败", f"{sources.get('paper_closed', 'paper_positions_closed.json')}；{sources.get('failure', 'failure_attribution.jsonl')}"),
    ])
    q["替代假设"].extend([
        _evidence("待验证", "若钱包证据缺失或快照滞后，当前结构结论可能反映数据质量问题而非真实结构变化；需复查原始钱包快照。", sources.get("wallet", "wallet_structure_decision.json")),
        _evidence("待验证", "若 quote/security 缺少价格影响或报价偏离字段，暂停/支持可能受外部报价可用性影响；需复查 quote_snapshot/security_scan_report。", sources.get("quote", "quote_security_summary.json")),
        _evidence("待验证", "若 process_trace 与 paper positions 状态不一致，可能是运行周期先后导致的观测滞后；需按时间线复核。", sources.get("process_trace", "process_trace.jsonl")),
    ])

    return {
        "token_address": token,
        "token_symbol": _symbol(status) or _symbol(wallet) or _symbol(quote) or _symbol(paper_open) or _symbol(paper_closed) or _symbol(failure),
        "current_state": current_state,
        "latest_action": latest_action,
        "paper_only": True,
        "non_decision_note": "本解释仅引用既有输出，不重新裁决、不生成交易授权。",
        "source_files": dict(sources),
        "questions": q,
    }


def _collect_token_statuses(base: Path) -> tuple[Dict[str, Dict[str, Any]], Dict[str, str]]:
    statuses: Dict[str, Dict[str, Any]] = {}
    refs: Dict[str, str] = {}
    live_state = _read_json(base / "live_state.json")
    if isinstance(live_state, Mapping):
        for row in _rows(live_state, ["tokens", "候选状态"]):
            t = _token(row)
            if t:
                statuses[t] = row
                refs.setdefault(t, str(base / "live_state.json"))
    for path in sorted((base / "tokens").glob("*/token_status.json")):
        payload = _read_json(path)
        if isinstance(payload, Mapping):
            t = _token(payload) or path.parent.name
            statuses[t] = dict(payload)
            refs[t] = str(path)
    return statuses, refs


def _collect_wallet(base: Path) -> tuple[Dict[str, Dict[str, Any]], Dict[str, str]]:
    out: Dict[str, Dict[str, Any]] = {}
    refs: Dict[str, str] = {}
    summary = base / "wallet_structure" / "candidate_wallet_structure_summary.json"
    payload = _read_json(summary)
    for row in _rows(payload, ["处理结果", "wallet_structure_results", "results", "decisions"]):
        t = _token(row)
        if t:
            out[t] = row
            refs[t] = str(summary)
    for path in sorted((base / "wallet_structure").glob("*/wallet_structure_decision.json")):
        payload = _read_json(path)
        if isinstance(payload, Mapping):
            t = _token(payload) or path.parent.name
            out[t] = dict(payload)
            refs[t] = str(path)
    return out, refs


def run_explainability_engine(live_run_dir: str | Path = DEFAULT_LIVE_RUN_DIR, output_dir: str | Path | None = None) -> Dict[str, str]:
    """生成 explainability_report.json/md；paper-only，只解释已有结果。"""
    base = Path(live_run_dir)
    out_dir = Path(output_dir) if output_dir else base
    now = _utc_now_text()

    statuses, status_refs = _collect_token_statuses(base)
    wallets, wallet_refs = _collect_wallet(base)

    quote_path = base / "quote_security" / "candidate_quote_security_summary.json"
    quotes = _index(_rows(_read_json(quote_path), ["处理结果", "quote_security_results", "results"])); quote_refs = {t: str(quote_path) for t in quotes}
    open_path = base / "paper_live" / "paper_positions_open.json"
    paper_open = _index(_rows(_read_json(open_path), ["open_positions", "开放仓位", "positions"])); open_refs = {t: str(open_path) for t in paper_open}
    closed_path = base / "paper_live" / "paper_positions_closed.json"
    paper_closed = _index(_rows(_read_json(closed_path), ["closed_positions", "关闭仓位", "positions"])); closed_refs = {t: str(closed_path) for t in paper_closed}
    failure_path = base / "paper_live" / "failure_attribution.jsonl"
    failures = _latest_by_token(_read_jsonl(failure_path)); failure_refs = {t: str(failure_path) for t in failures}

    trace_by_token: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    trace_refs: Dict[str, str] = {}
    for path in sorted((base / "tokens").glob("*/process_trace.jsonl")):
        token = path.parent.name
        trace_by_token[token] = _read_jsonl(path)
        trace_refs[token] = str(path)

    all_tokens = sorted(set(statuses) | set(wallets) | set(quotes) | set(paper_open) | set(paper_closed) | set(failures) | set(trace_by_token))
    token_reports: List[Dict[str, Any]] = []
    missing_inputs: List[Dict[str, str]] = []
    required_paths = {
        "live_state/token_status": base / "live_state.json",
        "wallet_structure_summary": base / "wallet_structure" / "candidate_wallet_structure_summary.json",
        "quote_security_summary": quote_path,
        "paper_positions_open": open_path,
        "paper_positions_closed": closed_path,
        "failure_attribution": failure_path,
        "tokens_dir": base / "tokens",
    }
    for name, path in required_paths.items():
        if not path.exists():
            missing_inputs.append({"input": name, "status": "证据缺失/待复查", "path": str(path)})

    for token in all_tokens:
        status = statuses.get(token, {"token_address": token, "current_state": "UNKNOWN"})
        sources = {
            "token_status": status_refs.get(token, str(base / "tokens" / token / "token_status.json")),
            "wallet": wallet_refs.get(token, str(base / "wallet_structure" / token / "wallet_structure_decision.json")),
            "quote": quote_refs.get(token, str(quote_path)),
            "paper_open": open_refs.get(token, str(open_path)),
            "paper_closed": closed_refs.get(token, str(closed_path)),
            "failure": failure_refs.get(token, str(failure_path)),
            "process_trace": trace_refs.get(token, str(base / "tokens" / token / "process_trace.jsonl")),
        }
        token_reports.append(_explain_token(
            token=token,
            status=status,
            wallet=wallets.get(token),
            quote=quotes.get(token),
            paper_open=paper_open.get(token),
            paper_closed=paper_closed.get(token),
            failure=failures.get(token),
            trace=trace_by_token.get(token, []),
            sources=sources,
        ))

    state_counts = Counter(str(item.get("current_state") or "UNKNOWN") for item in token_reports)
    report: Dict[str, Any] = {
        "module": "SIKK Explainability Engine v0.1",
        "generated_at": now,
        "paper_only": True,
        "readonly_note": "只解释既有结果；不采集、不报价、不交易、不签名、不广播、不调用 gmgn_swap/gmgn_cooking/yolo。",
        "non_decision_note": "本报告不重新裁决 token，只保留证据链与原始文件引用；缺输入显示 证据缺失/待复查。",
        "live_run_dir": str(base),
        "token_count": len(token_reports),
        "state_counts": dict(state_counts),
        "missing_inputs": missing_inputs,
        "tokens": token_reports,
    }

    json_path = out_dir / "explainability_report.json"
    md_path = out_dir / "explainability_report.md"
    _write_json(json_path, report)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(_build_markdown(report), encoding="utf-8")
    return {"explainability_report_json": str(json_path), "explainability_report_md": str(md_path)}


def _build_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# SIKK 专业解释报告",
        "",
        f"- 生成时间：{report.get('generated_at')}",
        f"- live run：{report.get('live_run_dir')}",
        f"- token 数：{report.get('token_count')}",
        "- 安全边界：paper-only；只解释既有结果，不执行真实交易、不签名、不广播。",
        "- 非裁决说明：不重新裁决；缺输入统一标记为 证据缺失/待复查。",
        "",
        "## 状态分布",
        "",
    ]
    for state, count in sorted((report.get("state_counts") or {}).items()):
        lines.append(f"- {state}：{count}")
    lines.extend(["", "## 缺失输入", ""])
    missing = report.get("missing_inputs") or []
    if missing:
        for item in missing:
            lines.append(f"- {item.get('input')}：{item.get('status')}｜{item.get('path')}")
    else:
        lines.append("- 未发现必需输入整体缺失；逐 token 字段仍可能待复查。")
    lines.extend(["", "## Token 解释", ""])
    for item in report.get("tokens", []):
        lines.extend([
            f"### {item.get('token_symbol') or '-'} / {item.get('token_address')}",
            "",
            f"- 当前状态：{item.get('current_state')}",
            f"- 最新动作：{item.get('latest_action') or '证据缺失/待复查'}",
            "- 说明：只解释已有结果，不重新裁决。",
            "",
        ])
        questions = item.get("questions") or {}
        for key in EXPLANATION_KEYS:
            lines.append(f"#### {key}")
            for ev in questions.get(key, []):
                src = ev.get("source") or ""
                field = f"｜字段：{ev.get('field')}" if ev.get("field") else ""
                lines.append(f"- {ev.get('status')}：{ev.get('text')}｜来源：{src}{field}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK 专业解释引擎（paper-only，只解释既有结果）")
    parser.add_argument("--live-run-dir", default=str(DEFAULT_LIVE_RUN_DIR))
    parser.add_argument("--output-dir", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(run_explainability_engine(args.live_run_dir, args.output_dir), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
