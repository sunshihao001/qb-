#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK-SOL v0.4 OKX 前300集群关联与持仓行为分析模块。

定位：读取本地 fixture / 未来 OKX Holder Cluster 输出，生成 OKX 集群证据合约。
本模块只分析/标准化/写文件，不签名、不广播、不执行真实交易。
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any, Mapping, Sequence

DEFAULT_OUTPUT_DIR = Path("data/gmgn_candidates_live_run/okx_cluster")

SUPPORT_STATUSES = {"CLUSTER_SUPPORT", "CLUSTER_CONTROL_HOLDING", "CLUSTER_SECOND_STAGE_SUPPORT"}
RISK_STATUSES = {"CLUSTER_DISTRIBUTION_RISK", "CLUSTER_COUNTERPARTY_ABSORBING", "CLUSTER_BAGHOLDER_PRESSURE"}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def _rows(payload: Any, keys: Sequence[str]) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [dict(x) for x in payload if isinstance(x, Mapping)]
    if not isinstance(payload, Mapping):
        return []
    for key in keys:
        val = payload.get(key)
        if isinstance(val, list):
            return [dict(x) for x in val if isinstance(x, Mapping)]
    return []


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_csv(path: Path, rows: Sequence[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames or ["empty"])
        writer.writeheader()
        for row in rows:
            writer.writerow(dict(row))


@dataclass
class OkxClusterDecision:
    token_address: str
    token_symbol: str = ""
    snapshot_time: str = ""
    okx_cluster_status: str = "OKX_CLUSTER_MISSING"
    okx_cluster_score: int = 0
    okx_cluster_risk_score: int = 0
    okx_cluster_distribution_score: int = 0
    okx_cluster_control_retention_score: int = 0
    okx_cluster_reason: str = "缺 OKX 前300集群证据，降级为待补。"
    top300_wallet_count: int = 0
    cluster_count: int = 0
    linked_wallet_count: int = 0
    unlinked_wallet_count: int = 0
    largest_cluster_wallet_count: int = 0
    largest_cluster_holding_pct: float = 0.0
    top300_total_holding_pct: float = 0.0
    cluster_total_holding_pct: float = 0.0
    cluster_sync_buy_score: int = 0
    cluster_sync_sell_score: int = 0
    cluster_holding_pct_delta: float = 0.0
    cluster_sold_pct_delta: float = 0.0
    largest_cluster_holding_pct_delta: float = 0.0
    top300_total_holding_pct_delta: float = 0.0
    dominant_cluster_role: str = "UNKNOWN_CLUSTER"
    evidence_points: list[str] = field(default_factory=list)
    risk_flags: list[str] = field(default_factory=list)
    missing_fields: list[str] = field(default_factory=list)
    paper_gate_effect: str = "NO_OKX_CLUSTER_INPUT"
    scope_note: str = "OKX 集群判断只用于 paper/观察/复盘，不代表真实交易授权。"

    def to_dict(self) -> dict[str, Any]:
        return {
            "token_address": self.token_address,
            "token_symbol": self.token_symbol,
            "snapshot_time": self.snapshot_time,
            "okx_cluster_status": self.okx_cluster_status,
            "okx_cluster_score": self.okx_cluster_score,
            "okx_cluster_risk_score": self.okx_cluster_risk_score,
            "okx_cluster_distribution_score": self.okx_cluster_distribution_score,
            "okx_cluster_control_retention_score": self.okx_cluster_control_retention_score,
            "okx_cluster_reason": self.okx_cluster_reason,
            "top300_wallet_count": self.top300_wallet_count,
            "cluster_count": self.cluster_count,
            "linked_wallet_count": self.linked_wallet_count,
            "unlinked_wallet_count": self.unlinked_wallet_count,
            "largest_cluster_wallet_count": self.largest_cluster_wallet_count,
            "largest_cluster_holding_pct": round(self.largest_cluster_holding_pct, 4),
            "top300_total_holding_pct": round(self.top300_total_holding_pct, 4),
            "cluster_total_holding_pct": round(self.cluster_total_holding_pct, 4),
            "cluster_sync_buy_score": self.cluster_sync_buy_score,
            "cluster_sync_sell_score": self.cluster_sync_sell_score,
            "cluster_holding_pct_delta": round(self.cluster_holding_pct_delta, 4),
            "cluster_sold_pct_delta": round(self.cluster_sold_pct_delta, 4),
            "largest_cluster_holding_pct_delta": round(self.largest_cluster_holding_pct_delta, 4),
            "top300_total_holding_pct_delta": round(self.top300_total_holding_pct_delta, 4),
            "dominant_cluster_role": self.dominant_cluster_role,
            "evidence_points": self.evidence_points,
            "risk_flags": self.risk_flags,
            "missing_fields": self.missing_fields,
            "paper_gate_effect": self.paper_gate_effect,
            "scope_note": self.scope_note,
        }


def classify_cluster_role(row: Mapping[str, Any]) -> str:
    role = _text(row.get("cluster_role") or row.get("role"))
    if role:
        return role
    sold = _num(row.get("cluster_sold_pct"))
    remaining = _num(row.get("cluster_remaining_pct"), 100.0 - sold)
    sync_sell = _num(row.get("cluster_sync_sell_score"))
    holding = _num(row.get("cluster_holding_pct"))
    avg_roi = _num(row.get("cluster_avg_roi_pct"))
    late_buy = _num(row.get("late_cluster_buy_amount_usd_delta") or row.get("late_buy_amount_usd_delta"))
    if sync_sell >= 75 or sold >= 70:
        return "ACTIVE_DISTRIBUTION_CLUSTER"
    if sync_sell >= 55 or sold >= 35:
        return "PARTIAL_DISTRIBUTION_CLUSTER"
    if late_buy > 0 and avg_roi < 0:
        return "BAGHOLDER_CLUSTER"
    if late_buy > 0:
        return "COUNTERPARTY_ABSORBING_CLUSTER"
    if holding >= 10 and remaining >= 50:
        return "CONTROL_HOLDING_CLUSTER"
    if holding >= 5:
        return "STRUCTURE_ACCUMULATION_CLUSTER"
    return "UNKNOWN_CLUSTER"


def _status_from_metrics(*, market_pattern_type: str, second_stage_valid: bool, largest_holding: float, remaining: float, sync_sell: float, distribution: float, counterparty: float, largest_delta: float, top300_delta: float, sold_delta: float, late_buy: float, avg_roi: float) -> tuple[str, list[str], list[str]]:
    evidence: list[str] = []
    risks: list[str] = []
    if sync_sell >= 70 or sold_delta >= 20 or largest_delta <= -10 or distribution >= 75:
        risks.append("前300关联集群出现同步卖出/持仓快速下降。")
        return "CLUSTER_DISTRIBUTION_RISK", evidence, risks
    if late_buy > 0 and avg_roi < 0:
        risks.append("晚期集群买入且 ROI 偏弱，存在套牢/接盘压力。")
        return "CLUSTER_BAGHOLDER_PRESSURE", evidence, risks
    if late_buy > 0 or counterparty >= 70:
        risks.append("出现对手盘承接集群或对手盘压力升高。")
        return "CLUSTER_COUNTERPARTY_ABSORBING", evidence, risks
    if market_pattern_type == "SECOND_STAGE_EXPANSION" and second_stage_valid and sync_sell < 60 and largest_delta >= -5 and distribution < 60:
        evidence.append("二段放量时集群未明显撤退。")
        return "CLUSTER_SECOND_STAGE_SUPPORT", evidence, risks
    if market_pattern_type == "CONTROL_BOX_ACCUMULATION" and abs(top300_delta) <= 5 and sync_sell < 50:
        evidence.append("横盘控筹阶段前300/最大集群持仓相对稳定。")
        return "CLUSTER_CONTROL_HOLDING", evidence, risks
    if largest_holding >= 10 and remaining >= 50 and sync_sell < 50 and distribution < 50 and counterparty < 60:
        evidence.append("前300中存在较明显持仓集群，且未见同步派发迹象。")
        return "CLUSTER_SUPPORT", evidence, risks
    return "CLUSTER_NEUTRAL", evidence, risks


def analyze_okx_cluster_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    token = _text(payload.get("token_address") or payload.get("代币地址") or payload.get("token"))
    symbol = _text(payload.get("token_symbol") or payload.get("代币符号") or payload.get("symbol"))
    snapshot_time = _text(payload.get("snapshot_time") or payload.get("快照时间") or _utc_now())
    clusters = _rows(payload, ["clusters", "cluster_groups", "集群", "groups"])
    if not clusters:
        decision = OkxClusterDecision(token_address=token, token_symbol=symbol, snapshot_time=snapshot_time)
        decision.missing_fields = ["clusters"]
        return decision.to_dict()

    enriched = []
    for row in clusters:
        item = dict(row)
        item["cluster_role"] = classify_cluster_role(item)
        enriched.append(item)
    largest = max(enriched, key=lambda r: (_num(r.get("cluster_holding_pct")), _num(r.get("cluster_wallet_count"))))
    top300_wallet_count = int(_num(payload.get("top300_wallet_count"), sum(_num(r.get("cluster_wallet_count")) for r in enriched)))
    linked_wallet_count = int(_num(payload.get("linked_wallet_count"), sum(_num(r.get("cluster_wallet_count")) for r in enriched)))
    largest_holding = _num(payload.get("largest_cluster_holding_pct"), _num(largest.get("cluster_holding_pct")))
    top300_total = _num(payload.get("top300_total_holding_pct"), sum(_num(r.get("cluster_holding_pct")) for r in enriched))
    cluster_total = _num(payload.get("cluster_total_holding_pct"), sum(_num(r.get("cluster_holding_pct")) for r in enriched))
    sync_buy = int(round(max(_num(r.get("cluster_sync_buy_score")) for r in enriched)))
    sync_sell = int(round(max(_num(r.get("cluster_sync_sell_score")) for r in enriched)))
    sold_delta = max(_num(r.get("cluster_sold_pct_delta")) for r in enriched)
    cluster_holding_delta = sum(_num(r.get("cluster_holding_pct_delta")) for r in enriched)
    largest_delta = _num(payload.get("largest_cluster_holding_pct_delta"), _num(largest.get("cluster_holding_pct_delta")))
    top300_delta = _num(payload.get("top300_total_holding_pct_delta"), cluster_holding_delta)
    distribution = max(sync_sell, int(round(sold_delta * 3)))
    control_retention = max(0, min(100, int(round(largest_holding * 4 + max(0, 50 - sync_sell) + max(0, largest_delta)))))
    risk = max(distribution, int(round(max(0, -largest_delta) * 5)))
    counterparty = _num(payload.get("counterparty_pressure_score"), max(_num(r.get("counterparty_pressure_score")) for r in enriched))
    late_buy = max(_num(r.get("late_cluster_buy_amount_usd_delta") or r.get("late_buy_amount_usd_delta")) for r in enriched)
    avg_rois = [_num(r.get("cluster_avg_roi_pct")) for r in enriched if r.get("cluster_avg_roi_pct") not in (None, "")]
    avg_roi = mean(avg_rois) if avg_rois else 0.0
    remaining = _num(largest.get("cluster_remaining_pct"), 100 - _num(largest.get("cluster_sold_pct")))
    market_pattern_type = _text(payload.get("market_pattern_type"))
    second_stage_valid = bool(payload.get("second_stage_valid"))

    status, evidence, risks = _status_from_metrics(
        market_pattern_type=market_pattern_type,
        second_stage_valid=second_stage_valid,
        largest_holding=largest_holding,
        remaining=remaining,
        sync_sell=sync_sell,
        distribution=distribution,
        counterparty=counterparty,
        largest_delta=largest_delta,
        top300_delta=top300_delta,
        sold_delta=sold_delta,
        late_buy=late_buy,
        avg_roi=avg_roi,
    )
    if not evidence and status == "CLUSTER_NEUTRAL":
        evidence.append("OKX 前300集群未形成明确支持或风险结论。")
    reason = "；".join(evidence + risks) or "OKX 集群证据待复查。"
    score = max(0, min(100, control_retention - risk // 3 + (10 if status in SUPPORT_STATUSES else 0)))
    if status in RISK_STATUSES:
        paper_effect = "PAUSE_OR_EXIT_MONITOR_BY_OKX_CLUSTER"
    elif status in SUPPORT_STATUSES:
        paper_effect = "SUPPORT_PAPER_ONLY_IF_OTHER_GATES_PASS"
    else:
        paper_effect = "OBSERVE_ONLY"

    decision = OkxClusterDecision(
        token_address=token,
        token_symbol=symbol,
        snapshot_time=snapshot_time,
        okx_cluster_status=status,
        okx_cluster_score=score,
        okx_cluster_risk_score=risk,
        okx_cluster_distribution_score=distribution,
        okx_cluster_control_retention_score=control_retention,
        okx_cluster_reason=reason,
        top300_wallet_count=top300_wallet_count,
        cluster_count=len(enriched),
        linked_wallet_count=linked_wallet_count,
        unlinked_wallet_count=max(0, top300_wallet_count - linked_wallet_count),
        largest_cluster_wallet_count=int(_num(largest.get("cluster_wallet_count"))),
        largest_cluster_holding_pct=largest_holding,
        top300_total_holding_pct=top300_total,
        cluster_total_holding_pct=cluster_total,
        cluster_sync_buy_score=sync_buy,
        cluster_sync_sell_score=sync_sell,
        cluster_holding_pct_delta=cluster_holding_delta,
        cluster_sold_pct_delta=sold_delta,
        largest_cluster_holding_pct_delta=largest_delta,
        top300_total_holding_pct_delta=top300_delta,
        dominant_cluster_role=_text(largest.get("cluster_role"), "UNKNOWN_CLUSTER"),
        evidence_points=evidence,
        risk_flags=risks,
        paper_gate_effect=paper_effect,
    )
    out = decision.to_dict()
    out["clusters"] = enriched
    return out


def analyze_okx_cluster_file(input_path: str | Path, output_dir: str | Path = DEFAULT_OUTPUT_DIR) -> dict[str, str]:
    p = Path(input_path)
    payload: Any
    if p.suffix.lower() == ".csv":
        rows = _read_csv(p)
        payload = {"clusters": rows}
        if rows:
            payload.update({k: rows[0].get(k) for k in ["token_address", "token_symbol", "snapshot_time", "market_pattern_type"] if rows[0].get(k)})
    else:
        payload = _read_json(p)
    if not isinstance(payload, Mapping):
        raise ValueError("OKX cluster input must be JSON object or CSV rows")
    decision = analyze_okx_cluster_payload(payload)
    out_root = Path(output_dir)
    token = decision.get("token_address") or "UNKNOWN_TOKEN"
    token_dir = out_root / str(token)
    json_path = token_dir / "okx_cluster_decision.json"
    _write_json(json_path, decision)
    cluster_rows = decision.get("clusters") if isinstance(decision.get("clusters"), list) else []
    _write_csv(token_dir / "okx_cluster_groups.csv", cluster_rows)
    _write_csv(token_dir / "okx_cluster_holding_behavior.csv", cluster_rows)
    summary = {"处理结果": [decision], "生成时间": _utc_now(), "paper_only": True}
    _write_json(out_root / "okx_cluster_summary.json", summary)
    _write_csv(out_root / "okx_cluster_summary.csv", [decision])
    md = ["# OKX 集群关联与持仓行为汇总", "", "- 安全边界：paper-only；不交易、不签名、不广播。", f"- token：`{token}`", f"- 状态：{decision.get('okx_cluster_status')}", f"- 原因：{decision.get('okx_cluster_reason')}"]
    (out_root / "okx_cluster_summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    return {
        "okx_cluster_decision_json": str(json_path),
        "okx_cluster_summary_json": str(out_root / "okx_cluster_summary.json"),
        "okx_cluster_summary_csv": str(out_root / "okx_cluster_summary.csv"),
        "okx_cluster_summary_md": str(out_root / "okx_cluster_summary.md"),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="SIKK v0.4 OKX 前300集群分析，只读/paper-only")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(analyze_okx_cluster_file(args.input, args.output_dir), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
