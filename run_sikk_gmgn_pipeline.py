#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-GMGN Pipeline Orchestrator v1.0

一键串联当前已完成的 GMGN→SIKK 自动准备链路：

1. GMGN 新币筛选：`sikk_gmgn_new_token_filter.py`
2. 候选币 K线 + 吸筹窗口：`sikk_candidate_kline_pipeline.py`
3. 候选币 SIKK 信号：`sikk_candidate_signal_pipeline.py`
4. 候选币生命周期状态机：`sikk_candidate_state_machine.py`
5. 可选 PAPER_READY 报价 + OKX token-scan + 确认层：`sikk_candidate_quote_security_pipeline.py`

执行边界：
- 默认 paper/readiness；
- 默认只读取 GMGN 新币/K线数据与本地文件；
- 开启 `--run-quote-security` 时只调用报价/token-scan，不广播交易；
- 不构建、不执行真实 swap；
- 后续真实交易必须另接权限、熔断、订单监控与人工确认。
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from sikk_candidate_kline_pipeline import default_runner as default_kline_runner
from sikk_candidate_kline_pipeline import run_candidate_kline_pipeline
from sikk_candidate_quote_security_pipeline import run_candidate_quote_security_pipeline
from sikk_candidate_signal_pipeline import run_candidate_signal_pipeline
from sikk_candidate_state_machine import run_candidate_state_machine
from sikk_candidate_wallet_structure_pipeline import run_candidate_wallet_structure_pipeline
from sikk_gmgn_new_token_filter import collect_and_write_candidate_pool, default_runner as default_trenches_runner, load_filter_config

DEFAULT_OUTPUT_ROOT = Path("data/gmgn_candidates")


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: str | Path | None) -> Dict[str, Any]:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_gmgn_env_value(name: str) -> str:
    """Read a simple KEY=value from ~/.config/gmgn/.env without exposing secrets."""

    env_path = Path.home() / ".config" / "gmgn" / ".env"
    if not env_path.exists():
        return ""
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith(f"{name}="):
            continue
        value = line.split("=", 1)[1].strip()
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        return value
    return ""


def _default_wallet_address() -> str:
    return os.environ.get("GMGN_WALLET_ADDRESS", "") or _read_gmgn_env_value("GMGN_WALLET_ADDRESS") or _read_gmgn_env_value("SIKK_GMGN_WALLET_ADDRESS")


def _count_state_machine_candidates(states_payload: Dict[str, Any]) -> int:
    return len(states_payload.get("候选状态", []))


def _candidate_filter_stats(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("候选统计", {"状态": "missing"})


def _kline_stats(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("处理统计", {"状态": "missing"})


def _signal_stats(payload: Dict[str, Any]) -> Dict[str, Any]:
    return payload.get("处理统计", {"状态": "missing"})


def _state_stats(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not payload:
        return {"状态": "missing"}
    stats = dict(payload.get("状态统计", {}))
    stats["候选数量"] = _count_state_machine_candidates(payload)
    return stats


def _quote_security_stats(payload: Dict[str, Any]) -> Dict[str, Any]:
    """提取报价/安全确认层统计；缺失时保持可读状态。"""

    if not payload:
        return {"状态": "missing"}
    return payload.get("处理统计", {"状态": "missing"})


def _wallet_structure_stats(payload: Dict[str, Any]) -> Dict[str, Any]:
    """提取钱包结构门禁统计；缺失时保持可读状态。"""

    if not payload:
        return {"状态": "missing"}
    return payload.get("统计", {"状态": "missing"})


def _build_markdown_report(manifest: Dict[str, Any]) -> str:
    stats = manifest.get("阶段统计", {})
    outputs = manifest.get("输出文件", {})
    lines = [
        "# SIKK-GMGN 一键管道运行报告",
        "",
        f"- 运行时间：{manifest.get('运行时间', '')}",
        f"- 模式：{manifest.get('模式', '')}",
        "- 执行边界：只做候选发现、K线吸筹识别、纸面信号、状态机，可选进入报价 + 安全扫描 + 确认层；不执行真实 swap。",
        "",
        "## 阶段统计",
        "",
    ]
    for stage, value in stats.items():
        lines.append(f"- {stage}：{json.dumps(value, ensure_ascii=False)}")
    lines.extend(["", "## 输出文件", ""])
    for name, path in outputs.items():
        lines.append(f"- {name}：{path or '未生成'}")
    lines.extend([
        "",
        "## 下一步",
        "",
        "- 若已启用报价 + 安全扫描 + 确认层，只能得到 READY_FOR_CONFIRMATION / PAUSE / BLOCK，不代表真实执行授权。",
        "- 若状态机出现 PAPER_READY 但未启用确认层，可再运行 `--run-quote-security`。",
        "- 若状态为 ACCUMULATING，继续刷新 K线与吸筹窗口。",
        "- 若 BLOCKED / FAILED，进入风险复查或数据修复。",
    ])
    return "\n".join(lines) + "\n"


def run_full_pipeline(
    *,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
    config_path: str | Path = "config/token_filter_config.json",
    trenches_runner: Callable[[List[str]], Dict[str, Any]] = default_trenches_runner,
    kline_runner: Callable[[List[str]], Dict[str, Any]] = default_kline_runner,
    limit: Optional[int] = None,
    include_s2: bool = False,
    run_accumulation: bool = True,
    run_signal: bool = True,
    run_state: bool = True,
    run_wallet_structure: bool = True,
    wallet_structure_runner: Callable[..., Dict[str, str]] = run_candidate_wallet_structure_pipeline,
    wallet_structure_mode: str = "observe",
    run_quote_security: bool = False,
    quote_security_runner: Callable[..., Dict[str, str]] = run_candidate_quote_security_pipeline,
    wallet_address: str = "",
    quote_sources: tuple[str, ...] = ("okx",),
    default_quote_amount_sol: float = 0.01,
    use_position_amount: bool = False,
    account_equity_sol: float = 10.0,
    risk_per_trade_pct: float = 0.25,
    max_position_sol: float = 0.2,
) -> Dict[str, str]:
    """执行 GMGN→SIKK 一键管道并写出 manifest/report。"""

    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    started_at = _utc_now()

    filter_dir = root / "gmgn_new_token_filter"
    kline_dir = root / "kline_pipeline"
    signal_dir = root / "candidate_signal_outputs"
    state_dir = root / "state_machine"
    wallet_structure_dir = root / "wallet_structure"
    quote_security_dir = root / "quote_security"
    orchestrator_dir = root / "orchestrator"

    # 1) GMGN 新币筛选
    filter_outputs = collect_and_write_candidate_pool(
        output_dir=filter_dir,
        config=load_filter_config(config_path),
        runner=trenches_runner,
        limit=limit,
        now=started_at,
        base_dir=root,
    )
    candidates_json = filter_outputs["json_path"]

    # 2) 候选 K线 + 吸筹窗口
    levels = ["S3_进入SIKK结构分析"]
    if include_s2:
        levels.append("S2_重点观察")
    kline_outputs = run_candidate_kline_pipeline(
        candidates_path=candidates_json,
        output_root=kline_dir,
        runner=kline_runner,
        include_levels=levels,
        run_accumulation=run_accumulation,
    )
    kline_summary = Path(kline_outputs["summary_path"])

    signal_summary_json = ""
    signal_summary_csv = ""
    if run_signal:
        signal_outputs = run_candidate_signal_pipeline(
            kline_summary,
            output_root=signal_dir,
            account_equity_sol=account_equity_sol,
            risk_per_trade_pct=risk_per_trade_pct,
            max_position_sol=max_position_sol,
        )
        signal_summary_json = signal_outputs["summary_json"]
        signal_summary_csv = signal_outputs["summary_csv"]

    states_json = ""
    states_csv = ""
    events_jsonl = ""
    state_summary_md = ""
    if run_state and run_signal:
        state_outputs = run_candidate_state_machine(
            candidates_path=candidates_json,
            kline_summary_path=kline_summary,
            signal_summary_path=signal_summary_json,
            output_dir=state_dir,
        )
        states_json = state_outputs["states_json"]
        states_csv = state_outputs["states_csv"]
        events_jsonl = state_outputs["events_jsonl"]
        state_summary_md = state_outputs["summary_md"]

    wallet_structure_summary_json = ""
    wallet_structure_summary_csv = ""
    wallet_structure_summary_md = ""
    if run_wallet_structure and run_state and run_signal and states_json:
        wallet_structure_outputs = wallet_structure_runner(
            candidate_states_path=states_json,
            output_dir=wallet_structure_dir,
        )
        wallet_structure_summary_json = wallet_structure_outputs["summary_json"]
        wallet_structure_summary_csv = wallet_structure_outputs["summary_csv"]
        wallet_structure_summary_md = wallet_structure_outputs["summary_md"]
        # 钱包结构门禁生成后，默认以 observe 旁路模式重新运行状态机：
        # 只把 wallet_gate/would_block 等字段写入候选状态，不让钱包结构卡死主流程。
        state_outputs = run_candidate_state_machine(
            candidates_path=candidates_json,
            kline_summary_path=kline_summary,
            signal_summary_path=signal_summary_json,
            wallet_structure_summary_path=wallet_structure_summary_json,
            wallet_structure_mode=wallet_structure_mode,
            output_dir=state_dir,
        )
        states_json = state_outputs["states_json"]
        states_csv = state_outputs["states_csv"]
        events_jsonl = state_outputs["events_jsonl"]
        state_summary_md = state_outputs["summary_md"]

    quote_summary_json = ""
    quote_summary_csv = ""
    quote_summary_md = ""
    if run_quote_security and run_state and run_signal:
        quote_outputs = quote_security_runner(
            candidate_states_path=states_json,
            signal_summary_path=signal_summary_json,
            output_dir=quote_security_dir,
            wallet_address=wallet_address,
            default_amount_sol=default_quote_amount_sol,
            use_position_amount=use_position_amount,
            quote_sources=quote_sources,
        )
        quote_summary_json = quote_outputs["summary_json"]
        quote_summary_csv = quote_outputs["summary_csv"]
        quote_summary_md = quote_outputs["summary_md"]

    filter_payload = _read_json(candidates_json)
    kline_payload = _read_json(kline_summary)
    signal_payload = _read_json(signal_summary_json)
    state_payload = _read_json(states_json)
    wallet_structure_payload = _read_json(wallet_structure_summary_json)
    quote_payload = _read_json(quote_summary_json)

    signal_stat = _signal_stats(signal_payload) if run_signal else {"状态": "skipped"}
    state_stat = _state_stats(state_payload) if run_state and run_signal else {"状态": "skipped"}
    wallet_structure_stat = _wallet_structure_stats(wallet_structure_payload) if run_wallet_structure and run_state and run_signal else {"状态": "skipped"}
    quote_stat = _quote_security_stats(quote_payload) if run_quote_security and run_state and run_signal else {"状态": "skipped"}

    manifest = {
        "模块": "SIKK-GMGN Pipeline Orchestrator v1.0",
        "运行时间": started_at,
        "模式": "paper/readiness",
        "参数": {
            "include_s2": include_s2,
            "run_accumulation": run_accumulation,
            "run_signal": run_signal,
            "run_state": run_state,
            "run_wallet_structure": run_wallet_structure,
            "wallet_structure_mode": wallet_structure_mode,
            "run_quote_security": run_quote_security,
            "quote_sources": list(quote_sources),
            "default_quote_amount_sol": default_quote_amount_sol,
            "use_position_amount": use_position_amount,
            "account_equity_sol": account_equity_sol,
            "risk_per_trade_pct": risk_per_trade_pct,
            "max_position_sol": max_position_sol,
        },
        "阶段统计": {
            "新币筛选": _candidate_filter_stats(filter_payload),
            "K线吸筹管道": _kline_stats(kline_payload),
            "信号管道": signal_stat,
            "状态机": state_stat,
            "钱包结构门禁": wallet_structure_stat,
            "报价安全确认层": quote_stat,
        },
        "输出文件": {
            "候选池JSON": str(candidates_json),
            "候选池CSV": str(filter_outputs["csv_path"]),
            "原始GMGN响应": str(filter_outputs["raw_path"]),
            "K线管道汇总": str(kline_summary),
            "信号汇总JSON": signal_summary_json,
            "信号汇总CSV": signal_summary_csv,
            "状态机JSON": states_json,
            "状态机CSV": states_csv,
            "状态事件JSONL": events_jsonl,
            "状态报告MD": state_summary_md,
            "钱包结构汇总JSON": wallet_structure_summary_json,
            "钱包结构汇总CSV": wallet_structure_summary_csv,
            "钱包结构报告MD": wallet_structure_summary_md,
            "报价安全汇总JSON": quote_summary_json,
            "报价安全汇总CSV": quote_summary_csv,
            "报价安全报告MD": quote_summary_md,
            "运行报告MD": str(orchestrator_dir / "pipeline_report.md"),
        },
        "说明": "本 Orchestrator 只串联 GMGN 新币筛选、K线吸筹、SIKK 纸面信号、状态机与可选报价/安全确认层，不执行真实 swap。",
    }

    manifest_path = orchestrator_dir / "pipeline_manifest.json"
    report_path = orchestrator_dir / "pipeline_report.md"
    manifest["输出文件"]["运行ManifestJSON"] = str(manifest_path)
    _write_json(manifest_path, manifest)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(_build_markdown_report(manifest), encoding="utf-8")

    return {"manifest_json": str(manifest_path), "report_md": str(report_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK-GMGN Pipeline Orchestrator v1.0")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT), help="总输出目录")
    parser.add_argument("--config", default="config/token_filter_config.json", help="GMGN 新币筛选配置")
    parser.add_argument("--limit", type=int, default=None, help="GMGN trenches 每类最大返回数量")
    parser.add_argument("--include-s2", action="store_true", help="K线管道同时处理 S2_重点观察")
    parser.add_argument("--no-accumulation", action="store_true", help="跳过吸筹窗口识别")
    parser.add_argument("--no-signal", action="store_true", help="跳过 SIKK 信号接入")
    parser.add_argument("--no-state", action="store_true", help="跳过状态机")
    parser.add_argument("--no-wallet-structure", action="store_true", help="跳过钱包结构门禁层")
    parser.add_argument("--wallet-structure-mode", choices=["off", "observe", "soft", "hard"], default="observe", help="钱包结构交易接入模式，默认 observe 只记录不阻断")
    parser.add_argument("--run-quote-security", action="store_true", help="状态机后运行只读报价 + OKX token-scan + 确认层")
    parser.add_argument("--wallet-address", default=_default_wallet_address(), help="GMGN quote 需要的钱包地址；默认读取 GMGN_WALLET_ADDRESS；OKX-only 可留空")
    parser.add_argument("--quote-sources", default="okx", help="逗号分隔：okx 或 gmgn,okx；默认 okx")
    parser.add_argument("--default-quote-amount-sol", type=float, default=0.01, help="确认层默认只读报价金额 SOL")
    parser.add_argument("--use-position-amount", action="store_true", help="确认层优先使用状态机建议纸面仓位作为报价金额")
    parser.add_argument("--account-equity-sol", type=float, default=10.0)
    parser.add_argument("--risk-per-trade-pct", type=float, default=0.25)
    parser.add_argument("--max-position-sol", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    quote_sources = tuple(source.strip() for source in args.quote_sources.split(",") if source.strip())
    result = run_full_pipeline(
        output_root=args.output_root,
        config_path=args.config,
        limit=args.limit,
        include_s2=args.include_s2,
        run_accumulation=not args.no_accumulation,
        run_signal=not args.no_signal,
        run_state=not args.no_state,
        run_wallet_structure=not args.no_wallet_structure,
        wallet_structure_mode=args.wallet_structure_mode,
        run_quote_security=args.run_quote_security,
        wallet_address=args.wallet_address,
        quote_sources=quote_sources,
        default_quote_amount_sol=args.default_quote_amount_sol,
        use_position_amount=args.use_position_amount,
        account_equity_sol=args.account_equity_sol,
        risk_per_trade_pct=args.risk_per_trade_pct,
        max_position_sol=args.max_position_sol,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
