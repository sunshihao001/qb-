#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK Full Auto Orchestrator 兼容入口。

重要：本文件是用户命令兼容 wrapper，不创建新的并行主循环，不替代 canonical
`sikk_live_run.py`。实际运行仍委托给 `sikk_live_run.run_live_once()`。

安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不 broadcast。
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

from run_sikk_gmgn_pipeline import _default_wallet_address
from sikk_live_run import run_live_once

SAFETY_BOUNDARY: Dict[str, Any] = {
    "paper_only": True,
    "real_swap_enabled": False,
    "private_key_required": False,
    "signing_enabled": False,
    "broadcast_enabled": False,
    "canonical_entrypoint": "sikk_live_run.py",
    "scope_note": "sikk_full_auto_orchestrator.py 只是兼容入口；不创建新的并行主循环。",
}

FULL_AUTOMATION_LAYERS: List[Dict[str, str]] = [
    {"name": "Runtime Orchestrator", "职责": "定时调度 canonical sikk_live_run.py，不创建并行真实主循环。"},
    {"name": "Data Source Layer", "职责": "接入 GMGN、OKX、K线、Paper、Wallet、Cluster 数据。"},
    {"name": "Structure Intelligence Layer", "职责": "融合 GMGN 钱包结构、OKX Top300 集群、K线盘型、市值路径。"},
    {"name": "State Machine Layer", "职责": "推进 DISCOVERED/WATCHING/PAPER_READY/PAPER_OPEN/PAPER_CLOSED/BLOCKED/EXPIRED。"},
    {"name": "Paper Trading Layer", "职责": "纸面入场、持仓更新、退出、止损止盈、结构退出、失败归因。"},
    {"name": "Case File Layer", "职责": "为每笔 paper position 生成完整实战档案。"},
    {"name": "Review Layer", "职责": "自动复盘、策略问题定位、右尾依赖、误杀与样本质量分层。"},
    {"name": "Interaction Layer", "职责": "CLI / TG / Web 三端统一查询。"},
    {"name": "Audit Layer", "职责": "字段覆盖率、模板应用、runtime 接入、数据质量、安全边界审计。"},
    {"name": "Reporting Layer", "职责": "日报、风险提醒、系统健康、下一步 backlog。"},
]

REQUIRED_ARTIFACTS: List[Dict[str, str]] = [
    {"key": "candidate_discovery", "path": "gmgn_new_token_filter/token_candidates.*", "说明": "候选发现"},
    {"key": "signal_analysis", "path": "candidate_signal_outputs/candidate_signal_summary.json", "说明": "信号分析"},
    {"key": "wallet_structure", "path": "wallet_structure/", "说明": "钱包结构"},
    {"key": "okx_cluster", "path": "okx_cluster/ 或统一索引 okx_cluster 字段", "说明": "OKX cluster"},
    {"key": "quote_security", "path": "quote_security/candidate_quote_security_summary.json", "说明": "quote/security"},
    {"key": "state_machine", "path": "state_machine/candidate_states.json", "说明": "状态机"},
    {"key": "paper_runner", "path": "paper_live/paper_positions_open.json", "说明": "paper runner"},
    {"key": "case_backfill", "path": "paper_live/case_files/", "说明": "case backfill"},
    {"key": "auto_review", "path": "paper_live/daily_reports/ + reports/", "说明": "auto review"},
    {"key": "unified_index", "path": "index/system_index.json", "说明": "unified index"},
    {"key": "dashboard", "path": "site/dashboard_data.json + site/index.html", "说明": "dashboard"},
    {"key": "telegram_callback_index", "path": "index/telegram_callback_index.json", "说明": "telegram callback index"},
    {"key": "reports", "path": "reports/*.md", "说明": "reports"},
    {"key": "events", "path": "events/live_events.jsonl", "说明": "events"},
]


def build_full_automation_contract() -> Dict[str, Any]:
    return {
        "version": "SIKK Full Automation System v1.0",
        "canonical_entrypoint": "sikk_live_run.py",
        "compatibility_entrypoint": "sikk_full_auto_orchestrator.py",
        "定位": "不是新脚本；是一套围绕 canonical runtime 的 paper-only 全流程自动化体系。",
        "layers": FULL_AUTOMATION_LAYERS,
        "required_artifacts": REQUIRED_ARTIFACTS,
        "safety_boundary": SAFETY_BOUNDARY,
        "loop_acceptance": {
            "target_runtime_hours": 5,
            "interval_sec": 600,
            "paper_update_sec": 180,
            "health_check_sec": 300,
            "real_trade_allowed": False,
        },
    }


def loop_config_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "mode": args.mode,
        "interval_sec": args.interval_sec,
        "paper_update_sec": args.paper_update_sec,
        "health_check_sec": args.health_check_sec,
    }


def _quote_sources(value: str) -> Tuple[str, ...]:
    sources = tuple(item.strip() for item in str(value or "").split(",") if item.strip())
    return sources or ("okx",)


def build_mapped_args(args: argparse.Namespace) -> Dict[str, Any]:
    return {
        "output_root": str(Path(args.base_dir)),
        "config_path": args.config,
        "limit": args.limit,
        "include_s2": args.include_s2,
        "quote_sources": list(_quote_sources(args.quote_sources)),
        "default_quote_amount_sol": args.default_quote_amount_sol,
        "wallet_address": args.wallet_address,
        "use_position_amount": args.use_position_amount,
        "force": args.force,
        "telegram_broadcast": False,
        "telegram_target": "",
    }


def run_once_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    mapped = build_mapped_args(args)
    if not args.paper_only:
        raise SystemExit("安全拒绝：必须显式传入 --paper-only。")
    if args.dry_run:
        return {
            "dry_run": True,
            "canonical_entrypoint": "sikk_live_run.py",
            "mapped_args": mapped,
            "safety_boundary": SAFETY_BOUNDARY,
            "说明": "dry-run 只展示参数映射，不运行 pipeline。",
        }
    result = run_live_once(
        output_root=mapped["output_root"],
        config_path=mapped["config_path"],
        limit=mapped["limit"],
        include_s2=mapped["include_s2"],
        quote_sources=tuple(mapped["quote_sources"]),
        default_quote_amount_sol=mapped["default_quote_amount_sol"],
        wallet_address=mapped["wallet_address"],
        use_position_amount=mapped["use_position_amount"],
        force=mapped["force"],
        telegram_broadcast=False,
        telegram_target="",
    )
    return {
        "canonical_entrypoint": "sikk_live_run.py",
        "compatibility_entrypoint": "sikk_full_auto_orchestrator.py",
        "mapped_args": mapped,
        "safety_boundary": SAFETY_BOUNDARY,
        "result": result,
    }


def _write_json(path: Path, payload: Dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def build_health_report(
    *,
    args: argparse.Namespace,
    loop_summary: Dict[str, Any],
    iterations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "version": "SIKK Full Automation System v1.0",
        "canonical_entrypoint": "sikk_live_run.py",
        "compatibility_entrypoint": "sikk_full_auto_orchestrator.py",
        "loop_config": loop_config_from_args(args),
        "loop_summary": {
            "target_runtime_hours": 5,
            **loop_summary,
        },
        "full_automation_contract": build_full_automation_contract(),
        "safety_boundary": SAFETY_BOUNDARY,
        "iterations": iterations,
        "说明": "loop 健康报告只审计 paper-only runtime；不读取私钥、不签名、不广播、不执行真实交易。",
    }


def run_loop_from_args(args: argparse.Namespace) -> Dict[str, Any]:
    if not args.paper_only:
        raise SystemExit("安全拒绝：loop 模式必须显式传入 --paper-only。")
    iterations: List[Dict[str, Any]] = []
    max_loops = getattr(args, "max_loops", None)
    completed_iterations = 0
    started_at = time.time()

    while True:
        iteration_started_at = time.time()
        payload = run_once_from_args(args)
        completed_iterations += 1
        iterations.append({
            "iteration": completed_iterations,
            "started_at_epoch": iteration_started_at,
            "finished_at_epoch": time.time(),
            "canonical_entrypoint": payload.get("canonical_entrypoint"),
            "live_run_manifest_json": (payload.get("result") or {}).get("live_run_manifest_json"),
            "safety_boundary": payload.get("safety_boundary"),
        })
        if max_loops and completed_iterations >= max_loops:
            break
        time.sleep(args.interval_sec)

    loop_summary = {
        "completed_iterations": completed_iterations,
        "elapsed_sec": round(time.time() - started_at, 3),
        "status": "COMPLETED_FOR_MAX_LOOPS" if max_loops else "STOPPED",
    }
    report = build_health_report(args=args, loop_summary=loop_summary, iterations=iterations)
    report_path = _write_json(Path(args.base_dir) / "full_automation" / "FULL_AUTOMATION_V1_HEALTH.json", report)
    return {**report, "health_report_json": report_path}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK 全自动兼容入口（委托 sikk_live_run.py，paper-only）")
    parser.add_argument("--base-dir", default="data/gmgn_candidates_live_run", help="兼容旧命令；映射到 sikk_live_run.py --output-root")
    parser.add_argument("--mode", choices=["once", "loop"], default="once")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--quote-sources", default="okx")
    parser.add_argument("--default-quote-amount-sol", type=float, default=0.01)
    parser.add_argument("--paper-only", action="store_true", help="必填安全确认；仍然只运行纸面/只读流程")
    parser.add_argument("--config", default="config/token_filter_config.json")
    parser.add_argument("--include-s2", action="store_true")
    parser.add_argument("--wallet-address", default=_default_wallet_address())
    parser.add_argument("--use-position-amount", action="store_true")
    parser.add_argument("--interval-sec", type=int, default=600)
    parser.add_argument("--paper-update-sec", type=int, default=180, help="loop 模式纸面持仓更新节奏说明；当前每轮仍由 canonical runtime 完整刷新")
    parser.add_argument("--health-check-sec", type=int, default=300, help="loop 模式健康检查节奏说明；写入 v1 健康报告")
    parser.add_argument("--max-loops", type=int, default=None, help="测试/演练用：达到指定轮数后退出；生产 5 小时运行不传")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="只输出参数映射，不运行 pipeline")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.dry_run:
        mapped = build_mapped_args(args)
        payload = {
            "dry_run": True,
            "canonical_entrypoint": "sikk_live_run.py",
            "compatibility_entrypoint": "sikk_full_auto_orchestrator.py",
            "mapped_args": mapped,
            "loop_config": loop_config_from_args(args),
            "full_automation_contract": build_full_automation_contract(),
            "safety_boundary": SAFETY_BOUNDARY,
            "说明": "dry-run 只展示 v1.0 合同、参数映射与安全边界，不运行 pipeline。",
        }
    elif args.mode == "loop":
        payload = run_loop_from_args(args)
    else:
        payload = run_once_from_args(args)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
