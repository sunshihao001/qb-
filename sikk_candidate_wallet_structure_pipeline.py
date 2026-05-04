#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK 候选币钱包结构门禁 pipeline。

读取状态机中的 PAPER_READY 候选，采集/接收早期钱包分类结果，写出每个 token 的
四张核心表和全局钱包结构摘要。默认采集器保持只读 GMGN 查询；当前第一版也支持
测试/编排注入 wallet_collector。
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List

from sikk_same_source_grouping import build_same_source_groups, write_candidate_groups_csv
from sikk_wallet_structure_gate import evaluate_and_write_wallet_structure, evaluate_wallet_structure_gate
from sikk_wallet_structure_snapshot import write_snapshot_and_delta

WalletCollector = Callable[[str, str], List[Dict[str, Any]]]

_FORBIDDEN_SNIPPETS = [
    "gmgn-cli swap",
    "gmgn-cli multi-swap",
    "order strategy create",
    "onchainos swap execute",
    "swap execute",
]


def _utc_now_text() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: str | Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    rows = list(rows)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        p.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _state_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = payload.get("候选状态") or payload.get("rows") or payload.get("data") or []
    return rows if isinstance(rows, list) else []


def _assert_readonly_command(command: List[str]) -> None:
    joined = " ".join(command)
    for snippet in _FORBIDDEN_SNIPPETS:
        if snippet in joined:
            raise ValueError(f"禁止构造/执行真实交易命令：{snippet}")
    if command[:3] != ["gmgn-cli", "token", "holders"] and command[:3] != ["gmgn-cli", "token", "traders"]:
        raise ValueError(f"钱包结构采集只允许 GMGN token holders/traders 只读命令：{command}")


def _run_json_command(command: List[str], timeout: int = 90) -> Dict[str, Any]:
    _assert_readonly_command(command)
    completed = subprocess.run(command, check=True, capture_output=True, text=True, timeout=timeout)
    return json.loads((completed.stdout or "{}").strip() or "{}")


def _text(row: Dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = row.get(key)
        if value not in (None, "", [], {}):
            return str(value)
    return ""


def _num(row: Dict[str, Any], *keys: str, default: float = 0.0) -> float:
    for key in keys:
        value = row.get(key)
        if value in (None, ""):
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return default


def _latest_source_time(rows: Iterable[Dict[str, Any]]) -> str:
    values: List[str] = []
    for row in rows:
        value = _text(row, "wallet_source_time", "source_time", "snapshot_time", "updated_at", "last_seen_at", "首次买入时间", "first_buy_time")
        if value:
            values.append(value)
    return max(values) if values else ""


def _classify_gmgn_wallet(row: Dict[str, Any]) -> Dict[str, Any]:
    tags = row.get("tags") or []
    maker_tags = row.get("maker_token_tags") or []
    tag_text = ",".join(str(x) for x in tags + maker_tags)
    sell_ratio = _num(row, "sell_amount_percentage", "sell_ratio", default=0.0)
    if sell_ratio > 1:
        sell_ratio = sell_ratio / 100.0
    profit = _num(row, "profit", "total_profit", "pnl", default=0.0)
    hold_ratio = _num(row, "amount_percentage", "holding_ratio", default=0.0)
    is_transfer = bool(row.get("transfer_in")) or "transfer_in" in maker_tags
    is_new = bool(row.get("is_new")) or "fresh_wallet" in tags or "fresh_wallet" in maker_tags

    role = "普通交易钱包"
    evidence = "E1"
    status = "仍持有" if hold_ratio > 0 else "未知"
    if is_transfer and sell_ratio >= 0.6:
        role, evidence, status = "分发派发钱包", "E4", "已清仓"
    elif is_transfer:
        role, evidence = "Token接收钱包", "E3"
    elif "rat_trader" in maker_tags or row.get("is_suspicious"):
        role, evidence = "可疑中转节点", "R2"
    elif "bundler" in maker_tags and is_new:
        role, evidence = "临时执行钱包", "E3"
    elif "sniper" in maker_tags or is_new:
        role, evidence = "新钱包狙击", "E2"
    elif "smart_degen" in tags and profit > 0:
        role, evidence = "结果钱包", "E3"
    elif profit > 5000 and hold_ratio > 0:
        role, evidence = "高结果鲸鱼", "E4"
    elif sell_ratio >= 0.7:
        role, evidence, status = "接盘鲸鱼", "R2", "已清仓"

    return {
        "钱包地址": _text(row, "address", "钱包地址"),
        "当前角色": role,
        "证据等级": evidence,
        "当前状态": status,
        "收益倍数": _text(row, "profit_percentage", "roi", "pnl_rate"),
        "卖出占比": sell_ratio,
        "持仓占比": hold_ratio,
        "GMGN标签": tag_text,
        "资金来源状态": "资金待查",
        "主要原因": f"GMGN标签={tag_text or '无'}；profit={profit}；hold={hold_ratio}；sell_ratio={sell_ratio}",
        "原始证据引用": _text(row, "source", "source_list") or "gmgn_token_holder_trader",
    }


def default_gmgn_wallet_collector(token: str, symbol: str = "") -> List[Dict[str, Any]]:
    """只读采集 GMGN holders/traders 并转换成钱包结构门禁输入。"""

    commands = [
        ["gmgn-cli", "token", "holders", "--chain", "sol", "--address", token, "--limit", "30", "--order-by", "amount_percentage", "--direction", "desc", "--raw"],
        ["gmgn-cli", "token", "traders", "--chain", "sol", "--address", token, "--limit", "30", "--order-by", "profit", "--direction", "desc", "--raw"],
        ["gmgn-cli", "token", "holders", "--chain", "sol", "--address", token, "--limit", "20", "--tag", "transfer_in", "--order-by", "amount_percentage", "--direction", "desc", "--raw"],
        ["gmgn-cli", "token", "holders", "--chain", "sol", "--address", token, "--limit", "20", "--tag", "bundler", "--order-by", "amount_percentage", "--direction", "desc", "--raw"],
        ["gmgn-cli", "token", "holders", "--chain", "sol", "--address", token, "--limit", "20", "--tag", "fresh_wallet", "--order-by", "amount_percentage", "--direction", "desc", "--raw"],
    ]
    by_address: Dict[str, Dict[str, Any]] = {}
    for command in commands:
        payload = _run_json_command(command)
        source = "_".join(command[1:3])
        for row in payload.get("list", []) or []:
            address = _text(row, "address")
            if not address:
                continue
            merged = by_address.setdefault(address, dict(row))
            merged.setdefault("tags", [])
            merged.setdefault("maker_token_tags", [])
            merged["tags"] = list({*merged.get("tags", []), *row.get("tags", [])})
            merged["maker_token_tags"] = list({*merged.get("maker_token_tags", []), *row.get("maker_token_tags", [])})
            merged["source"] = source
        time.sleep(0.5)
    return [_classify_gmgn_wallet(row) for row in by_address.values()]


def run_candidate_wallet_structure_pipeline(
    *,
    candidate_states_path: str | Path,
    output_dir: str | Path = "data/gmgn_candidates/wallet_structure",
    wallet_collector: WalletCollector = default_gmgn_wallet_collector,
    now: str | None = None,
) -> Dict[str, str]:
    states_payload = _read_json(candidate_states_path)
    candidates = [row for row in _state_rows(states_payload) if row.get("当前状态") == "PAPER_READY"]
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    now = now or _utc_now_text()
    results: List[Dict[str, Any]] = []

    for row in candidates:
        token = _text(row, "代币地址", "token", "address")
        symbol = _text(row, "代币符号", "symbol")
        token_dir = out / token
        wallet_refresh_started_at = now
        try:
            wallet_rows = wallet_collector(token, symbol)
            wallet_refresh_finished_at = now
            wallet_source_time = _latest_source_time(wallet_rows) or wallet_refresh_finished_at
            time_anchors = {
                "wallet_snapshot_time": wallet_refresh_finished_at,
                "wallet_decision_created_at": wallet_refresh_finished_at,
                "wallet_delta_time": wallet_refresh_finished_at,
                "wallet_source_time": wallet_source_time,
                "wallet_refresh_started_at": wallet_refresh_started_at,
                "wallet_refresh_finished_at": wallet_refresh_finished_at,
            }
            candidate_groups = build_same_source_groups(token_address=token, token_symbol=symbol, wallet_rows=wallet_rows)
            paths = evaluate_and_write_wallet_structure(token=token, symbol=symbol, wallet_rows=wallet_rows, output_dir=token_dir, candidate_groups=candidate_groups)
            write_candidate_groups_csv(paths["candidate_groups_csv"], candidate_groups)
            decision_obj = evaluate_wallet_structure_gate(token=token, symbol=symbol, wallet_rows=wallet_rows, candidate_groups=candidate_groups)
            snapshot_result = write_snapshot_and_delta(
                token_address=token,
                token_symbol=symbol,
                decision=decision_obj,
                market_context={
                    "price": row.get("当前价格") or row.get("price"),
                    "market_cap": row.get("当前市值USD") or row.get("market_cap"),
                    "liquidity": row.get("流动性USD") or row.get("liquidity"),
                    "holder_count": row.get("持有人数") or row.get("holder_count"),
                    "top10_holder_pct": row.get("Top10持仓率") or row.get("top10_holder_pct"),
                    "top20_holder_pct": row.get("Top20持仓率") or row.get("top20_holder_pct"),
                },
                base_dir=out,
            )
            decision = _read_json(paths["wallet_structure_decision_json"])
            decision.update(time_anchors)
            _write_json(paths["wallet_structure_decision_json"], decision)
            results.append({
                "代币地址": token,
                "代币符号": symbol,
                "处理状态": "ok",
                "钱包结构结论": decision.get("钱包结构结论"),
                "钱包结构系数": decision.get("钱包结构系数"),
                "钱包结构评分": decision.get("钱包结构评分"),
                "钱包风险评分": decision.get("钱包风险评分"),
                "对手盘压力评分": decision.get("对手盘压力评分"),
                "数据质量评分": decision.get("数据质量评分"),
                "筹码控制权状态": decision.get("筹码控制权状态"),
                "钱包证据等级": decision.get("钱包证据等级"),
                "建议状态调整": decision.get("建议状态调整"),
                "状态机建议": decision.get("状态机建议"),
                "PAPER_READY允许说明": decision.get("PAPER_READY允许说明"),
                "状态调整原因": decision.get("状态调整原因"),
                "wallet_structure_status": decision.get("wallet_structure_status"),
                "wallet_structure_score": decision.get("wallet_structure_score"),
                "wallet_risk_score": decision.get("wallet_risk_score"),
                "counterparty_pressure_score": decision.get("counterparty_pressure_score"),
                "data_quality_score": decision.get("data_quality_score"),
                "wallet_structure_factor": decision.get("wallet_structure_factor"),
                "wallet_structure_reason": decision.get("wallet_structure_reason"),
                "wallet_evidence_level": decision.get("wallet_evidence_level"),
                "钱包结构快照": snapshot_result.get("snapshot_path"),
                "钱包结构Delta": snapshot_result.get("delta_path"),
                "wallet_structure_snapshot_path": snapshot_result.get("snapshot_path"),
                "wallet_structure_delta_path": snapshot_result.get("delta_path"),
                **time_anchors,
                "钱包结构输出": {
                    "decision_json": paths["wallet_structure_decision_json"],
                    "summary_md": paths["wallet_structure_summary_md"],
                    "early_wallet_raw_csv": paths["early_wallet_raw_csv"],
                    "wallet_classification_csv": paths["wallet_classification_csv"],
                    "candidate_groups_csv": paths["candidate_groups_csv"],
                    "gmgn_note_table_csv": paths["gmgn_note_table_csv"],
                },
            })
        except Exception as exc:
            wallet_refresh_finished_at = now
            time_anchors = {
                "wallet_snapshot_time": wallet_refresh_finished_at,
                "wallet_decision_created_at": wallet_refresh_finished_at,
                "wallet_delta_time": wallet_refresh_finished_at,
                "wallet_source_time": wallet_refresh_finished_at,
                "wallet_refresh_started_at": wallet_refresh_started_at,
                "wallet_refresh_finished_at": wallet_refresh_finished_at,
            }
            decision = evaluate_wallet_structure_gate(token=token, symbol=symbol, wallet_rows=[])
            failure_reason = f"钱包结构采集失败：{exc}"
            results.append({
                "代币地址": token,
                "代币符号": symbol,
                "处理状态": "failed",
                "钱包结构结论": "WALLET_PAUSE",
                "钱包结构系数": 0.3,
                "钱包结构评分": decision.wallet_structure_score,
                "钱包风险评分": max(decision.wallet_risk_score, 30),
                "对手盘压力评分": decision.counterparty_pressure_score,
                "数据质量评分": min(decision.data_quality_score, 20),
                "筹码控制权状态": decision.chip_control_state,
                "钱包证据等级": decision.wallet_evidence_level,
                "建议状态调整": "降级为 WATCHING/PAUSE，等待钱包结构补采",
                "状态机建议": "PAUSE_OR_WATCHING",
                "PAPER_READY允许说明": "钱包结构采集失败，不能放行 PAPER_READY；需补采后再进入 quote/security 确认层。",
                "状态调整原因": failure_reason,
                "wallet_structure_status": "WALLET_PAUSE",
                "wallet_structure_score": decision.wallet_structure_score,
                "wallet_risk_score": max(decision.wallet_risk_score, 30),
                "counterparty_pressure_score": decision.counterparty_pressure_score,
                "data_quality_score": min(decision.data_quality_score, 20),
                "wallet_structure_factor": 0.3,
                "wallet_structure_reason": failure_reason,
                "wallet_evidence_level": decision.wallet_evidence_level,
                **time_anchors,
                "钱包结构输出": {},
            })

    counts: Dict[str, int] = {}
    for row in results:
        status = str(row.get("钱包结构结论") or "UNKNOWN")
        counts[status] = counts.get(status, 0) + 1

    summary_json = out / "candidate_wallet_structure_summary.json"
    summary_csv = out / "candidate_wallet_structure_summary.csv"
    summary_md = out / "candidate_wallet_structure_summary.md"
    payload = {
        "模块": "SIKK 候选币钱包结构门禁 v1.0",
        "更新时间": now,
        "输入文件": str(candidate_states_path),
        "统计": {"处理数量": len(results), **counts},
        "处理结果": results,
        "说明": "只处理 PAPER_READY 候选；只做钱包结构门禁，不执行真实 swap。",
    }
    _write_json(summary_json, payload)
    _write_csv(summary_csv, results)

    md = [
        "# SIKK 候选币钱包结构门禁汇总",
        "",
        f"- 更新时间：{now}",
        f"- 处理数量：{len(results)}",
        "- 边界：只做钱包结构门禁，不执行真实 swap。",
        "",
        "## 统计",
    ]
    for key, value in counts.items():
        md.append(f"- {key}：{value}")
    md.extend(["", "## 处理结果"])
    for row in results:
        md.extend([
            f"- 代币：{row.get('代币符号')} / {row.get('代币地址')}",
            f"  - 钱包结构结论：{row.get('钱包结构结论')}",
            f"  - 建议状态调整：{row.get('建议状态调整')}",
            f"  - 原因：{row.get('状态调整原因')}",
        ])
    summary_md.write_text("\n".join(md) + "\n", encoding="utf-8")

    return {"summary_json": str(summary_json), "summary_csv": str(summary_csv), "summary_md": str(summary_md)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK 候选币钱包结构门禁 pipeline")
    parser.add_argument("--candidate-states", required=True)
    parser.add_argument("--output-dir", default="data/gmgn_candidates/wallet_structure")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_candidate_wallet_structure_pipeline(candidate_states_path=args.candidate_states, output_dir=args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
