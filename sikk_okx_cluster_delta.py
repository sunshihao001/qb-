#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-SOL v0.4 OKX 前300集群快照 delta 与 paper failure attribution。

定位：只读比较多轮 OKX cluster decision/snapshot，输出 delta 与纸面失败归因候选。
本模块不签名、不广播、不执行真实交易；只为 token_status、dashboard、audit、复盘提供证据。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

DEFAULT_OUTPUT_DIR = Path("data/gmgn_candidates_live_run/okx_cluster")


SUPPORT_STATUSES = {"CLUSTER_SUPPORT", "CLUSTER_CONTROL_HOLDING", "CLUSTER_SECOND_STAGE_SUPPORT"}
RISK_STATUSES = {"CLUSTER_DISTRIBUTION_RISK", "CLUSTER_COUNTERPARTY_ABSORBING", "CLUSTER_BAGHOLDER_PRESSURE"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _read_json(path: str | Path) -> Any:
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_json(path: str | Path, payload: Mapping[str, Any]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(p)


def _write_jsonl(path: str | Path, rows: Iterable[Mapping[str, Any]]) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(dict(row), ensure_ascii=False) + "\n")
    return str(p)


def _num(v: Any, default: float = 0.0) -> float:
    if v in (None, "", [], {}):
        return default
    try:
        return float(v)
    except Exception:
        return default


def _text(v: Any, default: str = "") -> str:
    if v in (None, ""):
        return default
    return str(v)


def _extract_decision(payload: Any) -> dict[str, Any]:
    if isinstance(payload, Mapping):
        if isinstance(payload.get("处理结果"), list) and payload["处理结果"]:
            first = payload["处理结果"][0]
            return dict(first) if isinstance(first, Mapping) else {}
        if isinstance(payload.get("decisions"), list) and payload["decisions"]:
            first = payload["decisions"][0]
            return dict(first) if isinstance(first, Mapping) else {}
        return dict(payload)
    return {}


def _load_snapshot(snapshot: str | Path | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(snapshot, Mapping):
        return _extract_decision(snapshot)
    return _extract_decision(_read_json(snapshot))


def _delta(now: Mapping[str, Any], prev: Mapping[str, Any], key: str) -> float:
    return round(_num(now.get(key)) - _num(prev.get(key)), 4)


def build_okx_cluster_delta(
    previous_snapshot: str | Path | Mapping[str, Any],
    current_snapshot: str | Path | Mapping[str, Any],
    *,
    observed_at: str | None = None,
) -> dict[str, Any]:
    """比较两轮 OKX 集群快照，生成可复盘 delta。"""

    prev = _load_snapshot(previous_snapshot)
    cur = _load_snapshot(current_snapshot)
    token = _text(cur.get("token_address") or prev.get("token_address"))
    symbol = _text(cur.get("token_symbol") or prev.get("token_symbol"))
    prev_status = _text(prev.get("okx_cluster_status"), "OKX_CLUSTER_MISSING")
    cur_status = _text(cur.get("okx_cluster_status"), "OKX_CLUSTER_MISSING")

    largest_delta = _delta(cur, prev, "largest_cluster_holding_pct")
    top300_delta = _delta(cur, prev, "top300_total_holding_pct")
    cluster_total_delta = _delta(cur, prev, "cluster_total_holding_pct")
    sync_sell_delta = _delta(cur, prev, "cluster_sync_sell_score")
    distribution_delta = _delta(cur, prev, "okx_cluster_distribution_score")
    retention_delta = _delta(cur, prev, "okx_cluster_control_retention_score")
    risk_delta = _delta(cur, prev, "okx_cluster_risk_score")

    risk_flags: list[str] = []
    evidence_points: list[str] = []
    if prev_status in SUPPORT_STATUSES and cur_status in RISK_STATUSES:
        risk_flags.append("OKX_CLUSTER_STATUS_FLIPPED_FROM_SUPPORT_TO_RISK")
    if largest_delta <= -8:
        risk_flags.append("LARGEST_CLUSTER_HOLDING_DROPPED_FAST")
    if top300_delta <= -10:
        risk_flags.append("TOP300_HOLDING_DROPPED_FAST")
    if sync_sell_delta >= 25:
        risk_flags.append("CLUSTER_SYNC_SELL_SCORE_SPIKED")
    if distribution_delta >= 25:
        risk_flags.append("CLUSTER_DISTRIBUTION_SCORE_SPIKED")
    if retention_delta <= -25:
        risk_flags.append("CLUSTER_CONTROL_RETENTION_WEAKENED")
    if risk_delta >= 25:
        risk_flags.append("OKX_CLUSTER_RISK_SCORE_SPIKED")

    if not risk_flags:
        evidence_points.append("OKX 前300集群多轮快照未出现明显风险 delta。")
    else:
        evidence_points.append("OKX 前300集群多轮快照出现结构弱化/派发风险 delta。")

    failure_type = infer_okx_cluster_failure_type(
        current_status=cur_status,
        delta_flags=risk_flags,
        largest_delta=largest_delta,
        sync_sell_delta=sync_sell_delta,
        distribution_delta=distribution_delta,
        retention_delta=retention_delta,
    )
    recommended_action = "EXIT_MONITOR" if failure_type != "NO_OKX_CLUSTER_FAILURE" else "HOLD"
    if failure_type in {"CLUSTER_DISTRIBUTION_ACTIVE", "CLUSTER_STRUCTURE_WEAKENING"} and cur_status == "CLUSTER_DISTRIBUTION_RISK":
        recommended_action = "FORCE_PAPER_EXIT"

    return {
        "token_address": token,
        "token_symbol": symbol,
        "observed_at": observed_at or _utc_now(),
        "previous_snapshot_time": prev.get("snapshot_time"),
        "current_snapshot_time": cur.get("snapshot_time"),
        "previous_okx_cluster_status": prev_status,
        "current_okx_cluster_status": cur_status,
        "largest_cluster_holding_pct_delta_round": largest_delta,
        "top300_total_holding_pct_delta_round": top300_delta,
        "cluster_total_holding_pct_delta_round": cluster_total_delta,
        "cluster_sync_sell_score_delta_round": sync_sell_delta,
        "okx_cluster_distribution_score_delta_round": distribution_delta,
        "okx_cluster_control_retention_score_delta_round": retention_delta,
        "okx_cluster_risk_score_delta_round": risk_delta,
        "okx_cluster_delta_flags": risk_flags,
        "evidence_points": evidence_points,
        "okx_cluster_failure_type": failure_type,
        "recommended_paper_action": recommended_action,
        "scope_note": "OKX 集群 delta 只用于 paper failure attribution / EXIT_MONITOR / 复盘，不执行真实交易。",
    }


def infer_okx_cluster_failure_type(
    *,
    current_status: str,
    delta_flags: Sequence[str],
    largest_delta: float,
    sync_sell_delta: float,
    distribution_delta: float,
    retention_delta: float,
) -> str:
    flags = set(delta_flags)
    if current_status == "CLUSTER_DISTRIBUTION_RISK" or "CLUSTER_DISTRIBUTION_SCORE_SPIKED" in flags or sync_sell_delta >= 25:
        return "CLUSTER_DISTRIBUTION_ACTIVE"
    if current_status == "CLUSTER_COUNTERPARTY_ABSORBING":
        return "COUNTERPARTY_ABSORBING"
    if current_status == "CLUSTER_BAGHOLDER_PRESSURE":
        return "BAGHOLDER_PRESSURE"
    if largest_delta <= -8 or retention_delta <= -25 or "CLUSTER_CONTROL_RETENTION_WEAKENED" in flags:
        return "CLUSTER_STRUCTURE_WEAKENING"
    return "NO_OKX_CLUSTER_FAILURE"


def build_okx_cluster_failure_attribution_event(
    delta: Mapping[str, Any],
    *,
    event_time: str | None = None,
    paper_status: str = "OPEN",
    prior_failure_type: str | None = None,
) -> dict[str, Any]:
    """把 OKX cluster delta 转为 paper failure attribution 事件。"""

    failure_type = _text(delta.get("okx_cluster_failure_type"), "NO_OKX_CLUSTER_FAILURE")
    event_type = _text(delta.get("recommended_paper_action"), "HOLD")
    if prior_failure_type and failure_type == "NO_OKX_CLUSTER_FAILURE":
        failure_type = prior_failure_type
    reason = "；".join(delta.get("okx_cluster_delta_flags") or delta.get("evidence_points") or [])
    if not reason:
        reason = "OKX 集群 delta 未形成明确失败归因。"
    return {
        "事件时间": event_time or _text(delta.get("observed_at")) or _utc_now(),
        "事件类型": event_type,
        "代币地址": delta.get("token_address"),
        "代币符号": delta.get("token_symbol"),
        "paper_status": paper_status,
        "failure_type": failure_type,
        "failure_reason": reason,
        "okx_cluster_failure_type": failure_type,
        "previous_okx_cluster_status": delta.get("previous_okx_cluster_status"),
        "current_okx_cluster_status": delta.get("current_okx_cluster_status"),
        "largest_cluster_holding_pct_delta_round": delta.get("largest_cluster_holding_pct_delta_round"),
        "cluster_sync_sell_score_delta_round": delta.get("cluster_sync_sell_score_delta_round"),
        "okx_cluster_distribution_score_delta_round": delta.get("okx_cluster_distribution_score_delta_round"),
        "recommended_paper_action": event_type,
        "scope_note": "只记录纸面失败归因，不触发真实卖出。",
    }


def write_okx_cluster_delta_outputs(
    previous_snapshot: str | Path | Mapping[str, Any],
    current_snapshot: str | Path | Mapping[str, Any],
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    *,
    observed_at: str | None = None,
) -> dict[str, str]:
    delta = build_okx_cluster_delta(previous_snapshot, current_snapshot, observed_at=observed_at)
    event = build_okx_cluster_failure_attribution_event(delta, event_time=delta.get("observed_at"))
    out_root = Path(output_dir)
    token = _text(delta.get("token_address"), "UNKNOWN_TOKEN")
    token_dir = out_root / token
    delta_path = token_dir / "okx_cluster_delta.json"
    event_path = token_dir / "okx_cluster_failure_attribution.jsonl"
    _write_json(delta_path, delta)
    _write_jsonl(event_path, [event])
    summary = {"处理结果": [delta], "failure_attribution_events": [event], "生成时间": _utc_now(), "paper_only": True}
    summary_path = out_root / "okx_cluster_delta_summary.json"
    _write_json(summary_path, summary)
    md_path = out_root / "okx_cluster_delta_summary.md"
    md_path.write_text(
        "\n".join(
            [
                "# OKX 集群多轮快照 delta 汇总",
                "",
                "- 安全边界：paper-only；不真实卖出、不签名、不广播。",
                f"- token：`{token}`",
                f"- 上轮状态：{delta.get('previous_okx_cluster_status')}",
                f"- 本轮状态：{delta.get('current_okx_cluster_status')}",
                f"- failure_type：{event.get('failure_type')}",
                f"- recommended_paper_action：{event.get('recommended_paper_action')}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return {
        "okx_cluster_delta_json": str(delta_path),
        "okx_cluster_failure_attribution_jsonl": str(event_path),
        "okx_cluster_delta_summary_json": str(summary_path),
        "okx_cluster_delta_summary_md": str(md_path),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK v0.4 OKX 集群多轮快照 delta 与 paper failure attribution，只读/paper-only")
    parser.add_argument("--previous", required=True)
    parser.add_argument("--current", required=True)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--observed-at", default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(write_okx_cluster_delta_outputs(args.previous, args.current, args.output_dir, observed_at=args.observed_at), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
