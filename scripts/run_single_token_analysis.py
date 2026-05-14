#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run one-token SIKK personal structure analysis and paper-only replay.

Intentionally lightweight: no new plane, no complex phase controller, no real
trade path. It compresses P01-P10 into one runnable command.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sikk.data_loader import load_single_token_context, write_json, write_jsonl, utc_now
from sikk.wallet_structure_gate import evaluate_wallet_structure
from sikk.scenario_classifier import classify_scenario
from sikk.strategy_gate import decide_strategy
from sikk.paper_runner import run_paper_decision, render_paper_report
from sikk.review_attribution import build_issue_registry, build_review_attribution


def safe_token_path(token: str) -> str:
    return "".join(ch if ch.isalnum() or ch in "_-" else "_" for ch in token)[:120] or "UNKNOWN_TOKEN"


def render_token_report(context: Dict[str, Any], wallet_eval: Dict[str, Any], scenario: Dict[str, Any], decision: Dict[str, Any], review: Dict[str, Any]) -> str:
    token_basic = context.get("token_basic") or {}
    lines: List[str] = [
        "# SIKK 单 Token 结构分析报告",
        "",
        f"- token: `{context.get('token')}`",
        f"- mode: `{context.get('mode')}`",
        f"- generated_at: `{utc_now()}`",
        f"- final_status: `{decision.get('final_status')}`",
        f"- decision: `{decision.get('decision')}`",
        f"- paper_only: `{decision.get('paper_only')}`",
        f"- real_trade_allowed: `{decision.get('real_trade_allowed')}`",
        "",
        "## S01 数据读取与事实面板",
        "- 覆盖旧 P01/P02：token 基础信息、GMGN/OKX/quote/security、K线、钱包/筹码事实。",
        f"- source_files_count: {len(context.get('source_files') or [])}",
        f"- token_basic: `{json.dumps(token_basic, ensure_ascii=False)[:1000]}`",
        f"- wallet_rows_count: {len(context.get('wallet_rows') or [])}",
        f"- kline_rows_count: {len(context.get('kline_rows') or [])}",
        f"- missing_fields: `{', '.join(decision.get('missing_fields') or []) or '无'}`",
        "",
        "## S02 钱包结构 + 筹码结构判断",
        "- 覆盖旧 P03/P04：同源、同步买卖、早期控盘、结构方撤退、接盘压力、集中/派发/清仓/再吸筹。",
        f"- role_counts: `{json.dumps(wallet_eval.get('role_counts') or {}, ensure_ascii=False)}`",
        f"- top_holder_concentration_estimate: `{wallet_eval.get('top_holder_concentration_estimate')}`",
        f"- same_source_hint: `{wallet_eval.get('same_source_hint')}`",
        f"- sync_buy_sell_hint: `{wallet_eval.get('sync_buy_sell_hint')}`",
        f"- early_control_hint: `{wallet_eval.get('early_control_hint')}`",
        f"- structure_retreat_hint: `{wallet_eval.get('structure_retreat_hint')}`",
        f"- buyer_whale_pressure_hint: `{wallet_eval.get('buyer_whale_pressure_hint')}`",
        f"- chip_concentrated: `{wallet_eval.get('chip_concentrated')}`",
        f"- chip_distribution_hint: `{wallet_eval.get('chip_distribution_hint')}`",
        f"- chip_cleared_hint: `{wallet_eval.get('chip_cleared_hint')}`",
        f"- second_accumulation_hint: `{wallet_eval.get('second_accumulation_hint')}`",
        f"- exit_liquidity_risk: `{wallet_eval.get('exit_liquidity_risk')}`",
        "",
        "## S03 证据/反证 + 场景识别",
        "- 覆盖旧 P05/P06：列出支持/否定证据，并识别吸筹、派发、陷阱、再吸筹等场景。",
        "### 支持进入观察/纸面的证据",
    ]
    lines.extend([f"- {x}" for x in decision.get("evidence", [])] or ["- 无明确正证据"])
    lines.append("### 否定进入/限制判断的反证")
    lines.extend([f"- {x}" for x in decision.get("counter_evidence", [])] or ["- 无明确反证"])
    lines += [
        f"- scenario: `{scenario.get('scenario')}`",
        f"- confidence: `{scenario.get('confidence')}`",
        "",
        "## S04 策略门禁 + paper-only 决策",
        "- 覆盖旧 P07/P08：只输出 EXCLUDE/WATCH/RISK_MONITOR/PAPER_READY/READY_FOR_CONFIRMATION；只允许 paper-only。",
        f"- allowed_decisions: `{', '.join(decision.get('allowed_decisions') or [])}`",
        f"- decision: `{decision.get('decision')}`",
        f"- reason: {decision.get('reason')}",
        f"- support_score: `{decision.get('support_score')}`",
        f"- risk_score: `{decision.get('risk_score')}`",
        "- 只允许模拟，不允许实盘。",
        "- 不读取/写入私钥，不签名，不广播，不构造swap。",
        "",
        "## S05 复盘归因 + 规则升级候选",
        "- 覆盖旧 P09/P10：记录 paper 归因，规则只生成建议，不自动修改实时规则。",
        f"- has_existing_paper_result: `{review.get('has_existing_paper_result')}`",
        f"- attribution: {review.get('attribution')}",
        "- issue_registry.md 只记录缺口/建议，不改实时规则。",
    ]
    return "\n".join(lines) + "\n"


def build_evidence_trace(context: Dict[str, Any], wallet_eval: Dict[str, Any], scenario: Dict[str, Any], decision: Dict[str, Any], paper: Dict[str, Any], review: Dict[str, Any]) -> List[Dict[str, Any]]:
    token = context.get("token")
    now = utc_now()
    return [
        {
            "stage": "S01",
            "token": token,
            "time": now,
            "summary": "数据读取与事实面板",
            "covers_old_steps": ["P01", "P02"],
            "source_files": context.get("source_files", [])[:50],
            "wallet_rows_count": len(context.get("wallet_rows") or []),
            "kline_rows_count": len(context.get("kline_rows") or []),
            "missing_fields": context.get("missing_fields", []),
        },
        {
            "stage": "S02",
            "token": token,
            "time": now,
            "summary": "钱包结构 + 筹码结构判断",
            "covers_old_steps": ["P03", "P04"],
            "wallet_structure": {k: wallet_eval.get(k) for k in ["status", "same_source_hint", "sync_buy_sell_hint", "early_control_hint", "structure_retreat_hint", "buyer_whale_pressure_hint"]},
            "chip": {k: wallet_eval.get(k) for k in ["chip_concentrated", "chip_distribution_hint", "chip_cleared_hint", "second_accumulation_hint", "exit_liquidity_risk"]},
        },
        {
            "stage": "S03",
            "token": token,
            "time": now,
            "summary": "证据/反证 + 场景识别",
            "covers_old_steps": ["P05", "P06"],
            "evidence": decision.get("evidence"),
            "counter_evidence": decision.get("counter_evidence"),
            "scenario": scenario,
        },
        {
            "stage": "S04",
            "token": token,
            "time": now,
            "summary": "策略门禁 + paper-only 决策",
            "covers_old_steps": ["P07", "P08"],
            "decision": decision,
            "paper": paper,
        },
        {
            "stage": "S05",
            "token": token,
            "time": now,
            "summary": "复盘归因 + 规则升级候选",
            "covers_old_steps": ["P09", "P10"],
            "review": review,
            "note": "仅写入issue_registry.md，不自动修改实时规则",
        },
    ]

def run(token: str, mode: str, output_root: Path) -> Dict[str, Any]:
    out_dir = output_root / safe_token_path(token)
    out_dir.mkdir(parents=True, exist_ok=True)
    context = load_single_token_context(token, mode=mode)
    wallet_eval = evaluate_wallet_structure(context)
    scenario = classify_scenario(context, wallet_eval)
    decision = decide_strategy(context, wallet_eval, scenario)
    paper = run_paper_decision(context, decision)
    review = build_review_attribution(context, paper, decision)

    token_decision = {
        "token": token,
        "mode": mode,
        "generated_at": utc_now(),
        "final_status": decision.get("final_status"),
        "decision": decision.get("decision"),
        "paper_only": True,
        "real_trade_allowed": False,
        "reason": decision.get("reason"),
        "scenario": scenario,
        "wallet_structure": {k: v for k, v in wallet_eval.items() if k != "classified_wallets"},
        "classified_wallets_sample": wallet_eval.get("classified_wallets", [])[:20],
        "paper": paper,
        "review_attribution": review,
        "missing_fields": decision.get("missing_fields", []),
    }
    write_json(out_dir / "token_decision.json", token_decision)
    write_jsonl(out_dir / "evidence_trace.jsonl", build_evidence_trace(context, wallet_eval, scenario, decision, paper, review))
    (out_dir / "token_analysis_report.md").write_text(render_token_report(context, wallet_eval, scenario, decision, review), encoding="utf-8")
    (out_dir / "paper_decision_report.md").write_text(render_paper_report(paper), encoding="utf-8")
    (out_dir / "issue_registry.md").write_text(build_issue_registry(context, wallet_eval, scenario, decision), encoding="utf-8")
    return {"output_dir": str(out_dir), "token_decision": token_decision}


def main() -> None:
    parser = argparse.ArgumentParser(description="SIKK personal single-token paper-only replay")
    parser.add_argument("--token", required=True, help="Solana token address or GMGN candidate token")
    parser.add_argument("--mode", default="replay", help="Data mode hint: replay/live/live_test/paper")
    parser.add_argument("--output-root", default=str(PROJECT_ROOT / "reports" / "single_token_replay"))
    args = parser.parse_args()
    result = run(args.token, args.mode, Path(args.output_root))
    print(json.dumps({
        "status": result["token_decision"].get("final_status"),
        "decision": result["token_decision"].get("decision"),
        "output_dir": result["output_dir"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
