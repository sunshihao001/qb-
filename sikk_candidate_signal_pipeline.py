#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK 候选币自动信号接入模块。

本模块接在 `sikk_candidate_kline_pipeline.py` 之后：

GMGN 候选池 → K线接入 → 吸筹窗口识别 → 本模块生成 SIKK 自动交易准备信号。

重要边界：
- 第一版只输出 paper / readiness 结果；
- 不执行真实 swap；
- 不构建 GMGN/OKX 实盘交易命令；
- S3/S4 代表进入策略准备/强确认观察，不代表直接下单。
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict, Iterable, List, Optional

from sikk_auto_readiness_runner import run as run_readiness


DEFAULT_ACCOUNT_EQUITY_SOL = 10.0
DEFAULT_RISK_PER_TRADE_PCT = 0.25
DEFAULT_MAX_POSITION_SOL = 0.2


def _utc_now_text() -> str:
    """返回 UTC ISO 时间。"""

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json(path: str | Path) -> Dict[str, Any]:
    """读取 JSON 文件。"""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    """写入中文 JSON。"""

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    """写入中文 CSV。"""

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


def _safe_token_dir_name(token: str) -> str:
    """生成安全目录名。"""

    return "".join(ch for ch in str(token) if ch.isalnum() or ch in {"_", "-"})[:96] or "unknown_token"


def _extract_kline_path(item: Dict[str, Any]) -> str:
    """从候选 K线管道结果中提取 1m K线文件路径。"""

    kline_files = item.get("K线文件") or {}
    if isinstance(kline_files, dict):
        return str(kline_files.get("1m") or kline_files.get("1min") or kline_files.get("kline_1m") or "")
    return ""


def _load_readiness_result(path_map: Dict[str, str]) -> Dict[str, Any]:
    """读取 readiness runner 输出的主 JSON。"""

    json_path = path_map.get("json")
    if not json_path:
        return {}
    p = Path(json_path)
    if not p.exists():
        return {}
    return _read_json(p)


def _flatten_signal_row(item: Dict[str, Any], readiness_paths: Dict[str, str], readiness_payload: Dict[str, Any]) -> Dict[str, Any]:
    """把 readiness JSON 压缩成候选池汇总行。"""

    risk_gate = readiness_payload.get("risk_gate") or {}
    signal = readiness_payload.get("signal") or {}
    position_plan = readiness_payload.get("position_plan") or {}
    exit_plan = readiness_payload.get("exit_plan") or {}
    paper_trade = readiness_payload.get("paper_trade") or {}

    return {
        "代币地址": item.get("代币地址", ""),
        "代币符号": item.get("代币符号", ""),
        "候选筛选等级": item.get("筛选等级", ""),
        "模式": "paper",
        "风险门禁": risk_gate.get("permission", ""),
        "风险等级": risk_gate.get("risk_level", ""),
        "信号等级": signal.get("signal_level", ""),
        "策略类型": signal.get("strategy_type", ""),
        "信号时间": signal.get("signal_time", ""),
        "信号价格": signal.get("signal_price", ""),
        "信号置信分": signal.get("confidence_score", ""),
        "建议纸面仓位SOL": position_plan.get("suggested_position_sol", ""),
        "止损价格": position_plan.get("stop_price") or exit_plan.get("hard_stop_price", ""),
        "最大浮盈_pct": paper_trade.get("最大浮盈_pct", ""),
        "最终收益率_pct": paper_trade.get("最终收益率_pct", ""),
        "自动准备输出": readiness_paths,
        "状态": "ok",
        "说明": "纸面交易/自动准备信号，不执行真实 swap",
    }


def _make_runner_args(
    *,
    token: str,
    kline_path: str,
    accumulation_path: str,
    output_dir: Path,
    account_equity_sol: float,
    risk_per_trade_pct: float,
    max_position_sol: float,
) -> SimpleNamespace:
    """构造 sikk_auto_readiness_runner.run 所需参数。"""

    return SimpleNamespace(
        token=token,
        kline=kline_path,
        accumulation_json=accumulation_path,
        control_json=None,
        output_dir=str(output_dir),
        mode="paper",
        account_equity_sol=account_equity_sol,
        risk_per_trade_pct=risk_per_trade_pct,
        max_position_sol=max_position_sol,
    )


def run_candidate_signal_pipeline(
    kline_summary_path: str | Path,
    *,
    output_root: str | Path | None = None,
    account_equity_sol: float = DEFAULT_ACCOUNT_EQUITY_SOL,
    risk_per_trade_pct: float = DEFAULT_RISK_PER_TRADE_PCT,
    max_position_sol: float = DEFAULT_MAX_POSITION_SOL,
) -> Dict[str, str]:
    """批量读取 K线管道结果，并生成候选币 SIKK 自动信号。

    参数：
    - kline_summary_path：`candidate_kline_pipeline_summary.json`
    - output_root：信号输出根目录；为空时写在 summary 同目录 `candidate_signal_outputs/`
    """

    summary_path = Path(kline_summary_path)
    source_summary = _read_json(summary_path)
    output_root_path = Path(output_root) if output_root else summary_path.parent / "candidate_signal_outputs"
    output_root_path.mkdir(parents=True, exist_ok=True)

    signal_rows: List[Dict[str, Any]] = []
    skipped_rows: List[Dict[str, Any]] = []

    for item in source_summary.get("处理结果", []):
        token = str(item.get("代币地址") or "")
        if item.get("状态") != "ok":
            skipped_rows.append({
                "代币地址": token,
                "代币符号": item.get("代币符号", ""),
                "状态": "skipped",
                "原因": item.get("错误") or "上游 K线管道未成功",
            })
            continue

        kline_path = _extract_kline_path(item)
        accumulation_path = str(item.get("吸筹窗口输出") or "")
        missing = []
        if not kline_path or not Path(kline_path).exists():
            missing.append("1m K线文件缺失")
        if not accumulation_path or not Path(accumulation_path).exists():
            missing.append("吸筹窗口 JSON 缺失")
        if missing:
            skipped_rows.append({
                "代币地址": token,
                "代币符号": item.get("代币符号", ""),
                "状态": "skipped",
                "原因": "；".join(missing),
            })
            continue

        token_output_dir = output_root_path / _safe_token_dir_name(token) / "signal_outputs"
        runner_args = _make_runner_args(
            token=token,
            kline_path=kline_path,
            accumulation_path=accumulation_path,
            output_dir=token_output_dir,
            account_equity_sol=account_equity_sol,
            risk_per_trade_pct=risk_per_trade_pct,
            max_position_sol=max_position_sol,
        )
        readiness_paths = run_readiness(runner_args)
        readiness_payload = _load_readiness_result(readiness_paths)
        signal_rows.append(_flatten_signal_row(item, readiness_paths, readiness_payload))

    summary_payload = {
        "模块": "SIKK 候选币自动信号接入模块",
        "扫描时间": _utc_now_text(),
        "K线管道来源": str(summary_path),
        "模式": "paper",
        "处理统计": {
            "读取候选数": len(source_summary.get("处理结果", [])),
            "成功数量": len(signal_rows),
            "跳过数量": len(skipped_rows),
            "失败数量": 0,
        },
        "信号结果": signal_rows,
        "跳过结果": skipped_rows,
        "说明": "本模块只生成 SIKK 自动交易准备/纸面信号，不执行真实 swap。",
    }

    summary_json = output_root_path / "candidate_signal_summary.json"
    summary_csv = output_root_path / "candidate_signal_summary.csv"
    _write_json(summary_json, summary_payload)
    _write_csv(summary_csv, signal_rows)

    return {"summary_json": str(summary_json), "summary_csv": str(summary_csv)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK 候选币自动信号接入模块（paper/readiness only）")
    parser.add_argument("--kline-summary", required=True, help="candidate_kline_pipeline_summary.json 路径")
    parser.add_argument("--output-root", default=None, help="候选币信号输出根目录")
    parser.add_argument("--account-equity-sol", type=float, default=DEFAULT_ACCOUNT_EQUITY_SOL)
    parser.add_argument("--risk-per-trade-pct", type=float, default=DEFAULT_RISK_PER_TRADE_PCT)
    parser.add_argument("--max-position-sol", type=float, default=DEFAULT_MAX_POSITION_SOL)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_candidate_signal_pipeline(
        args.kline_summary,
        output_root=args.output_root,
        account_equity_sol=args.account_equity_sol,
        risk_per_trade_pct=args.risk_per_trade_pct,
        max_position_sol=args.max_position_sol,
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
