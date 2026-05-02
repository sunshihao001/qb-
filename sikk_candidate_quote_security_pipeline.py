#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK 候选币 quote/security 决策管道 v0.6。

目标链路：
PAPER_READY → 实时报价 quote → OKX token-scan / 安全扫描
→ quote_security_decision → READY_FOR_CONFIRMATION / PAUSE / BLOCK。

安全边界：本模块只调用只读报价与 token-scan 采集器，不执行真实 swap，
不广播交易，不创建策略单。真实执行必须由后续独立权限层处理。
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional

from sikk_execution_adapter_base import QuoteRequest, TokenSide
from sikk_live_quote_security_collector import (
    GMGNLiveQuoteCollector,
    OKXLiveQuoteCollector,
    OKXSecurityScanCollector,
    run_readonly_cli,
)
from sikk_quote_security_review import build_and_write_pre_trade_review

Runner = Callable[[List[str]], str]

GMGN_SOL_TOKEN = "So11111111111111111111111111111111111111112"
OKX_SOL_TOKEN = "11111111111111111111111111111111"
DEFAULT_SLIPPAGE = 0.3


def _utc_now_text() -> str:
    """返回 UTC 时间文本。"""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: str | Path | None) -> Dict[str, Any]:
    """读取 JSON；文件不存在时返回空对象。"""

    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    """写 JSON 文件。"""

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: str | Path, rows: Iterable[Dict[str, Any]]) -> None:
    """写 CSV 文件。"""

    rows = list(rows)
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        p.write_text("", encoding="utf-8")
        return
    fieldnames: List[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with p.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _state_rows(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """兼容状态机 JSON 的候选状态列表。"""

    rows = payload.get("候选状态")
    return rows if isinstance(rows, list) else []


def _signal_index(payload: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """按代币地址索引候选信号结果。"""

    index: Dict[str, Dict[str, Any]] = {}
    for row in payload.get("信号结果", []):
        token = str(row.get("代币地址") or row.get("token") or "")
        if token:
            index[token] = row
    return index


def _to_float(value: Any, default: float = 0.0) -> float:
    """安全转 float。"""

    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _sol_to_lamports(amount_sol: float) -> str:
    """把 SOL 数量转成 lamports 字符串，供 GMGN quote 使用。"""

    return str(int(round(amount_sol * 1_000_000_000)))


def _readiness_path_for_token(token: str, signal_rows: Dict[str, Dict[str, Any]]) -> str:
    """从信号汇总中找到 token_readiness_result.json。"""

    row = signal_rows.get(token, {})
    outputs = row.get("自动准备输出") or row.get("outputs") or {}
    if isinstance(outputs, dict):
        return str(outputs.get("json") or outputs.get("readiness_json") or "")
    return ""


def _map_final_permission(final_permission: str) -> str:
    """把 quote_security_decision 权限映射为候选交易前状态。"""

    if final_permission == "ALLOW_CONFIRMATION_LAYER":
        return "READY_FOR_CONFIRMATION"
    if final_permission == "BLOCK_BUY":
        return "BLOCK"
    return "PAUSE"


def _build_requests(
    *,
    token: str,
    wallet_address: str,
    amount_sol: float,
    slippage: float,
    quote_sources: Iterable[str],
) -> tuple[Optional[QuoteRequest], Optional[QuoteRequest]]:
    """构造 GMGN/OKX 只读报价请求。

    GMGN quote 需要钱包地址；OKX quote 不依赖钱包登录。没有钱包时可仅跑 OKX。
    """

    sources = {str(source).strip().lower() for source in quote_sources}
    gmgn_request: Optional[QuoteRequest] = None
    okx_request: Optional[QuoteRequest] = None
    if "gmgn" in sources:
        if not wallet_address:
            raise ValueError("GMGN quote 需要 wallet_address；如无钱包可使用 quote_sources=('okx',)")
        gmgn_request = QuoteRequest(
            chain="sol",
            wallet_address=wallet_address,
            input_token=GMGN_SOL_TOKEN,
            output_token=token,
            amount_smallest_unit=_sol_to_lamports(amount_sol),
            slippage=slippage,
        )
    if "okx" in sources:
        okx_request = QuoteRequest(
            chain="solana",
            wallet_address=wallet_address,
            input_token=OKX_SOL_TOKEN,
            output_token=token,
            readable_amount=str(amount_sol),
        )
    return gmgn_request, okx_request


def run_candidate_quote_security_pipeline(
    *,
    candidate_states_path: str | Path,
    signal_summary_path: str | Path,
    output_dir: str | Path = "data/gmgn_candidates/quote_security",
    wallet_address: str,
    default_amount_sol: float = 0.01,
    use_position_amount: bool = False,
    slippage: float = DEFAULT_SLIPPAGE,
    runner: Runner = run_readonly_cli,
    snapshot_time: Optional[str] = None,
    quote_sources: Iterable[str] = ("gmgn", "okx"),
) -> Dict[str, str]:
    """运行 PAPER_READY 候选的只读报价 + 安全扫描 + 决策管道。

    第一版仅处理 `当前状态 == PAPER_READY` 的候选；其他状态写入跳过结果。
    输出候选级五文件目录与总汇总 JSON/CSV/Markdown。
    """

    states_payload = _read_json(candidate_states_path)
    signal_payload = _read_json(signal_summary_path)
    states = _state_rows(states_payload)
    signals = _signal_index(signal_payload)
    now = snapshot_time or _utc_now_text()

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    results: List[Dict[str, Any]] = []
    skipped: List[Dict[str, Any]] = []
    failed: List[Dict[str, Any]] = []

    for state in states:
        token = str(state.get("代币地址") or state.get("token") or "")
        symbol = str(state.get("代币符号") or "")
        current_state = str(state.get("当前状态") or "")
        if current_state != "PAPER_READY":
            skipped.append({
                "代币地址": token,
                "代币符号": symbol,
                "原状态": current_state,
                "原因": "不是 PAPER_READY，暂不进入报价/安全扫描层",
            })
            continue

        readiness_path = _readiness_path_for_token(token, signals)
        if not readiness_path or not Path(readiness_path).exists():
            failed.append({
                "代币地址": token,
                "代币符号": symbol,
                "原状态": current_state,
                "交易前状态": "PAUSE",
                "原因": "缺少 readiness JSON，无法生成确认审查五文件",
            })
            continue

        readiness_payload = _read_json(readiness_path)
        position_sol = _to_float(state.get("建议纸面仓位SOL"), 0.0)
        amount_sol = position_sol if use_position_amount and position_sol > 0 else float(default_amount_sol)
        gmgn_request, okx_request = _build_requests(
            token=token,
            wallet_address=wallet_address,
            amount_sol=amount_sol,
            slippage=slippage,
            quote_sources=quote_sources,
        )
        review_dir = out / token

        try:
            # 单源失败不让整个 token 失败：报价缺失会在 quote_security_decision 中变成 PAUSE。
            quote_results = []
            scan_results = []
            collection_errors: List[str] = []
            if gmgn_request is not None:
                try:
                    quote_results.append(GMGNLiveQuoteCollector().collect(gmgn_request, runner=runner))
                except Exception as exc:  # noqa: BLE001 - 记录单源失败，继续 OKX/安全扫描
                    collection_errors.append(f"GMGN quote 失败：{exc}")
            if okx_request is not None:
                try:
                    quote_results.append(OKXLiveQuoteCollector().collect(okx_request, runner=runner))
                except Exception as exc:  # noqa: BLE001
                    collection_errors.append(f"OKX quote 失败：{exc}")
            try:
                scan_results.append(
                    OKXSecurityScanCollector().collect(
                        chain_id="501",
                        token_address=token,
                        token_side=TokenSide.BUY,
                        runner=runner,
                    )
                )
            except Exception as exc:  # noqa: BLE001
                collection_errors.append(f"OKX token-scan 失败：{exc}")

            paths = build_and_write_pre_trade_review(
                output_dir=review_dir,
                readiness_payload=readiness_payload,
                chain="sol",
                wallet_address=wallet_address,
                human_amount=f"{amount_sol} SOL",
                quote_results=quote_results,
                security_scan_results=scan_results,
                snapshot_time=now,
            )
            decision = _read_json(paths["quote_security_decision_json"])
            final_permission = str(decision.get("final_permission") or "PAUSE_NEED_CONFIRM")
            trade_pre_state = _map_final_permission(final_permission)
            reasons = list(decision.get("reasons", [])) + collection_errors
            results.append({
                "代币地址": token,
                "代币符号": symbol,
                "原状态": current_state,
                "交易前状态": trade_pre_state,
                "quote_security_permission": final_permission,
                "报价状态": decision.get("quote_status", ""),
                "安全权限": decision.get("security_permission", ""),
                "安全风险等级": decision.get("security_risk_level", ""),
                "最大价格影响_pct": decision.get("max_price_impact_pct", ""),
                "报价偏离_pct": decision.get("quote_deviation_pct", ""),
                "原因": "；".join(reasons),
                "审查输出目录": str(review_dir),
                "quote_security_decision_json": paths["quote_security_decision_json"],
                "trade_confirmation_ticket_md": paths["trade_confirmation_ticket_md"],
            })
        except Exception as exc:  # noqa: BLE001 - 批量管道需要逐 token 记录失败
            failed.append({
                "代币地址": token,
                "代币符号": symbol,
                "原状态": current_state,
                "交易前状态": "PAUSE",
                "原因": f"报价/安全扫描审查文件生成失败：{exc}",
            })

    status_counter = Counter(row["交易前状态"] for row in results)
    stats = {
        "读取状态数": len(states),
        "PAPER_READY数量": sum(1 for row in states if str(row.get("当前状态") or "") == "PAPER_READY"),
        "成功数量": len(results),
        "跳过数量": len(skipped),
        "失败数量": len(failed),
        "READY_FOR_CONFIRMATION": status_counter.get("READY_FOR_CONFIRMATION", 0),
        "PAUSE": status_counter.get("PAUSE", 0) + len(failed),
        "BLOCK": status_counter.get("BLOCK", 0),
    }

    payload = {
        "模块": "SIKK Candidate Quote/Security Pipeline v0.6",
        "扫描时间": now,
        "输入文件": {
            "候选状态": str(candidate_states_path),
            "信号汇总": str(signal_summary_path),
        },
        "处理统计": stats,
        "处理结果": results,
        "跳过结果": skipped,
        "失败结果": failed,
        "说明": "PAPER_READY 后置只读报价与安全扫描管道；输出 READY_FOR_CONFIRMATION / PAUSE / BLOCK，不执行真实 swap。",
    }

    summary_json = out / "candidate_quote_security_summary.json"
    summary_csv = out / "candidate_quote_security_summary.csv"
    summary_md = out / "candidate_quote_security_summary.md"
    _write_json(summary_json, payload)
    _write_csv(summary_csv, results)

    md_lines = [
        "# SIKK PAPER_READY 报价与安全扫描汇总",
        "",
        f"- 扫描时间：{now}",
        "- 执行边界：只读 quote + OKX token-scan，不执行真实 swap。",
        f"- PAPER_READY 数量：{stats['PAPER_READY数量']}",
        f"- READY_FOR_CONFIRMATION：{stats['READY_FOR_CONFIRMATION']}",
        f"- PAUSE：{stats['PAUSE']}",
        f"- BLOCK：{stats['BLOCK']}",
        "",
        "## 处理结果",
        "",
    ]
    for row in results:
        md_lines.extend([
            f"- 代币：{row['代币符号']} / {row['代币地址']}",
            f"  - 交易前状态：{row['交易前状态']}",
            f"  - 权限：{row['quote_security_permission']}",
            f"  - 原因：{row['原因']}",
        ])
    if failed:
        md_lines.extend(["", "## 失败/暂停结果", ""])
        for row in failed:
            md_lines.append(f"- {row['代币符号']} / {row['代币地址']}：{row['原因']}")
    summary_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    return {
        "summary_json": str(summary_json),
        "summary_csv": str(summary_csv),
        "summary_md": str(summary_md),
    }


def parse_args() -> argparse.Namespace:
    """解析 CLI 参数。"""

    parser = argparse.ArgumentParser(description="SIKK PAPER_READY quote/security pipeline v0.6")
    parser.add_argument("--candidate-states", required=True, help="state_machine/candidate_states.json")
    parser.add_argument("--signal-summary", required=True, help="candidate_signal_summary.json")
    parser.add_argument("--output-dir", default="data/gmgn_candidates/quote_security")
    parser.add_argument("--wallet-address", default="", help="用于 GMGN 只读报价的本机/绑定钱包地址；OKX-only 可留空")
    parser.add_argument("--quote-sources", default="gmgn,okx", help="报价来源，逗号分隔：gmgn,okx；无钱包时可填 okx")
    parser.add_argument("--default-amount-sol", type=float, default=0.01, help="默认审查金额 SOL")
    parser.add_argument("--use-position-amount", action="store_true", help="使用状态机建议纸面仓位作为报价金额")
    parser.add_argument("--slippage", type=float, default=DEFAULT_SLIPPAGE, help="GMGN quote slippage，小数形式")
    return parser.parse_args()


def main() -> None:
    """CLI 入口。"""

    args = parse_args()
    result = run_candidate_quote_security_pipeline(
        candidate_states_path=args.candidate_states,
        signal_summary_path=args.signal_summary,
        output_dir=args.output_dir,
        wallet_address=args.wallet_address,
        default_amount_sol=args.default_amount_sol,
        use_position_amount=args.use_position_amount,
        slippage=args.slippage,
        quote_sources=[source.strip() for source in args.quote_sources.split(",") if source.strip()],
    )
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
