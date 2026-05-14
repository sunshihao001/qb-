"""SIKK 自动交易准备框架：日志与报告输出。"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from sikk_auto_trade_types import readiness_to_dict


def _ensure_dir(output_dir: str | Path) -> Path:
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    """写入 UTF-8 JSON。"""

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    """写入 CSV；rows 为空时创建空文件。"""

    rows = list(rows)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        Path(path).write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with Path(path).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_readiness_outputs(
    *,
    output_dir: str | Path,
    token: str,
    risk_gate: Any,
    signal: Any,
    position_plan: Any,
    exit_plan: Any,
    paper_trade: Dict[str, Any] | None,
) -> Dict[str, str]:
    """统一写出自动交易准备框架结果。"""

    out = _ensure_dir(output_dir)
    payload = readiness_to_dict(
        token=token,
        risk_gate=risk_gate,
        signal=signal,
        position_plan=position_plan,
        exit_plan=exit_plan,
        paper_trade=paper_trade or {},
        scope_note="第一版为纸面交易/自动交易准备框架，不执行真实 swap。",
    )

    json_path = out / "token_readiness_result.json"
    risk_path = out / "risk_gate_report.json"
    signal_path = out / "signal_events.csv"
    paper_path = out / "paper_trades.csv"
    exit_path = out / "exit_plan.json"
    md_path = out / "auto_readiness_review.md"

    write_json(json_path, payload)
    write_json(risk_path, readiness_to_dict(risk_gate=risk_gate))
    write_json(exit_path, readiness_to_dict(exit_plan=exit_plan))
    write_csv(signal_path, [readiness_to_dict(signal=signal)["signal"]])
    write_csv(paper_path, [paper_trade] if paper_trade else [])

    md = [
        "# SIKK 自动交易准备框架结果",
        "",
        f"- 代币地址：{token}",
        f"- 风险门禁：{risk_gate.permission.value}",
        f"- 风险等级：{risk_gate.risk_level}",
        f"- 信号等级：{signal.signal_level.value}",
        f"- 策略类型：{signal.strategy_type}",
        f"- 信号时间：{signal.signal_time}",
        f"- 信号价格：{signal.signal_price}",
        f"- 建议纸面仓位SOL：{position_plan.suggested_position_sol}",
        f"- 硬止损价：{exit_plan.hard_stop_price}",
        "",
        "## 重要边界",
        "",
        "本结果只用于纸面交易、半自动确认前置和复盘，不代表自动实盘买入。",
    ]
    if paper_trade:
        md.extend([
            "",
            "## 纸面交易结果",
            "",
            f"- 最大浮盈：{paper_trade.get('最大浮盈_pct')}%",
            f"- 最大浮亏：{paper_trade.get('最大浮亏_pct')}%",
            f"- 最终收益率：{paper_trade.get('最终收益率_pct')}%",
            f"- 最终R倍数：{paper_trade.get('最终R倍数')}",
            f"- 出场原因：{paper_trade.get('出场原因')}",
        ])
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    return {
        "json": str(json_path),
        "risk": str(risk_path),
        "signal": str(signal_path),
        "paper": str(paper_path),
        "exit": str(exit_path),
        "review": str(md_path),
    }
