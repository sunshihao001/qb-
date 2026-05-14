from __future__ import annotations

"""User-facing Phase01 token data display panel.

This module reads the governed Phase01 fact-store index and standard fact assets,
then renders a human-readable token data panel. It deliberately stays inside
Phase01 boundaries: facts, candidate evidence, quality/missing fields, and
handoff readiness only. It must not emit trading/state-machine decisions.
"""

import json
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .phase01_fact_store_router import build_fact_store_index

FORBIDDEN_PANEL_TERMS = [
    "PAPER_READY",
    "BLOCKED",
    "buy_signal",
    "sell_signal",
    "trade_allowed",
    "execute_now",
    "真实交易",
    "建议买入",
    "确定庄家",
    "确定内幕",
]


@dataclass
class TokenDataPanel:
    artifact_type: str
    token_address: str
    mode: str
    generated_at: str
    quality_status: str
    recommended_action: str
    contamination_status: str
    panel: dict[str, Any]
    output_paths: dict[str, str]
    forbidden_term_scan: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_type": self.artifact_type,
            "token_address": self.token_address,
            "mode": self.mode,
            "generated_at": self.generated_at,
            "quality_status": self.quality_status,
            "recommended_action": self.recommended_action,
            "contamination_status": self.contamination_status,
            "panel": self.panel,
            "output_paths": self.output_paths,
            "forbidden_term_scan": self.forbidden_term_scan,
        }


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_json(path: Path | None) -> Any:
    if not path or not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _selected_path(index: dict[str, Any], root: Path, asset_key: str) -> Path | None:
    asset = (index.get("fact_assets") or {}).get(asset_key) or {}
    selected = asset.get("selected_path")
    if not selected:
        return None
    p = Path(selected)
    return p if p.is_absolute() else root / selected


def _records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return [x for x in payload["records"] if isinstance(x, dict)]
    return []


def _counter(records: list[dict[str, Any]], field: str) -> dict[str, int]:
    c: Counter[str] = Counter()
    for row in records:
        value = row.get(field)
        if isinstance(value, list):
            for item in value:
                c[str(item or "missing")] += 1
        else:
            c[str(value or "missing")] += 1
    return dict(c.most_common())


def _sum_followup_fields(records: list[dict[str, Any]]) -> dict[str, int]:
    c: Counter[str] = Counter()
    wallets = 0
    for row in records:
        fields = row.get("requires_followup_fields") or row.get("missing_fields") or []
        if fields:
            wallets += 1
        if isinstance(fields, list):
            for f in fields:
                c[str(f)] += 1
    return {"wallets_with_followup_fields": wallets, "field_distribution": dict(c.most_common())}


def _top_wallets(trades: list[dict[str, Any]], decisions: list[dict[str, Any]], limit: int = 8) -> list[dict[str, Any]]:
    decision_by_wallet = {d.get("wallet_address"): d for d in decisions if d.get("wallet_address")}

    def score(row: dict[str, Any]) -> float:
        for k in ("buy_amount_usd", "realized_profit", "total_profit", "buy_amount_sol"):
            v = row.get(k)
            if isinstance(v, (int, float)):
                return float(v)
        return 0.0

    out: list[dict[str, Any]] = []
    for row in sorted(trades, key=score, reverse=True)[:limit]:
        wallet = row.get("wallet_address")
        dec = decision_by_wallet.get(wallet, {})
        out.append({
            "wallet_address": wallet,
            "buy_amount_usd": row.get("buy_amount_usd"),
            "buy_amount_sol": row.get("buy_amount_sol"),
            "sell_amount_usd": row.get("sell_amount_usd"),
            "remaining_pct": row.get("remaining_pct"),
            "sold_pct": row.get("sold_pct"),
            "pnl_multiple": row.get("pnl_multiple"),
            "evidence_level": dec.get("evidence_level"),
            "risk_level": dec.get("risk_level"),
            "role_candidates": dec.get("role_candidates") or [],
            "need_onchain_followup": dec.get("need_onchain_followup"),
        })
    return out


def _market_summary(stage_payload: Any) -> dict[str, Any]:
    if not isinstance(stage_payload, dict):
        return {}
    field_summary = stage_payload.get("field_summary") or {}
    stages = stage_payload.get("stage_outputs") or []
    stage_status = {}
    if isinstance(stages, list):
        for stage in stages:
            if isinstance(stage, dict):
                stage_status[stage.get("stage_id", "unknown_stage")] = stage.get("status")
    return {
        "symbol": field_summary.get("symbol"),
        "price_usd": field_summary.get("price_usd"),
        "market_cap": field_summary.get("market_cap"),
        "liquidity_usd": field_summary.get("liquidity_usd"),
        "top10_holder_rate": field_summary.get("top10_holder_rate"),
        "rug_ratio": field_summary.get("rug_ratio"),
        "risk_level_source_value": field_summary.get("risk_level"),
        "holders_count": field_summary.get("holders_count"),
        "traders_count": field_summary.get("traders_count"),
        "okx_top_trader_count": field_summary.get("okx_top_trader_count"),
        "okx_cluster_count": field_summary.get("okx_cluster_count"),
        "required_failures_count": field_summary.get("required_failures_count"),
        "stage_status": stage_status,
    }


def _missing_assets_summary(index: dict[str, Any]) -> dict[str, Any]:
    return {
        "missing_required_assets_count": len(index.get("missing_required_assets") or []),
        "missing_optional_assets_count": len(index.get("missing_optional_assets") or []),
        "missing_required_assets": index.get("missing_required_assets") or [],
        "missing_optional_assets": index.get("missing_optional_assets") or [],
    }


def _same_source_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "candidate_group_count": len(records),
        "groups": [
            {
                "same_source_group_id": r.get("same_source_group_id"),
                "wallet_count": len(r.get("group_wallets") or []),
                "evidence_level": r.get("evidence_level"),
                "risk_level": r.get("risk_level"),
                "evidence_label": r.get("evidence_label"),
                "shared_funding_source": r.get("shared_funding_source"),
                "shared_token_source": r.get("shared_token_source"),
                "missing_fields": r.get("missing_fields") or [],
            }
            for r in records
        ],
        "evidence_level_distribution": _counter(records, "evidence_level"),
        "risk_level_distribution": _counter(records, "risk_level"),
    }


def _scan_forbidden(text: str) -> dict[str, Any]:
    hits = [term for term in FORBIDDEN_PANEL_TERMS if term in text]
    return {"status": "PASS" if not hits else "FAIL", "hits": hits}


def _render_markdown(panel_dict: dict[str, Any]) -> str:
    panel = panel_dict["panel"]
    market = panel["market_fact"]
    records = panel["record_counts"]
    wallet = panel["wallet_fact_summary"]
    same = panel["same_source_candidate_summary"]
    quality = panel["quality_and_missing"]
    lines = [
        "# Phase01 代币数据展示面板",
        "",
        f"- token_address: `{panel_dict['token_address']}`",
        f"- mode: `{panel_dict['mode']}`",
        f"- generated_at: `{panel_dict['generated_at']}`",
        f"- quality_status: `{panel_dict['quality_status']}`",
        f"- recommended_action: `{panel_dict['recommended_action']}`",
        f"- contamination_status: `{panel_dict['contamination_status']}`",
        "",
        "## 1. 基础行情事实",
        f"- symbol: `{market.get('symbol')}`",
        f"- price_usd: `{market.get('price_usd')}`",
        f"- market_cap: `{market.get('market_cap')}`",
        f"- liquidity_usd: `{market.get('liquidity_usd')}`",
        f"- top10_holder_rate: `{market.get('top10_holder_rate')}`",
        f"- holders_count: `{market.get('holders_count')}`",
        f"- traders_count: `{market.get('traders_count')}`",
        f"- okx_cluster_count: `{market.get('okx_cluster_count')}`",
        "",
        "## 2. 标准事实记录量",
        f"- wallet_trade_records: `{records.get('wallet_trade_records')}`",
        f"- wallet_profile_records: `{records.get('wallet_profile_records')}`",
        f"- wallet_intelligence_records: `{records.get('wallet_intelligence_records')}`",
        f"- same_source_candidate_groups: `{records.get('same_source_candidate_groups')}`",
        "",
        "## 3. 钱包候选证据分布",
        f"- evidence_level_distribution: `{wallet.get('evidence_level_distribution')}`",
        f"- risk_level_distribution: `{wallet.get('risk_level_distribution')}`",
        f"- role_candidate_distribution: `{wallet.get('role_candidate_distribution')}`",
        "",
        "## 4. 疑似同源候选组",
        f"- candidate_group_count: `{same.get('candidate_group_count')}`",
    ]
    for group in same.get("groups", []):
        lines.append(
            f"- {group.get('same_source_group_id')}: wallet_count=`{group.get('wallet_count')}`, "
            f"evidence_level=`{group.get('evidence_level')}`, risk_level=`{group.get('risk_level')}`, "
            f"label=`{group.get('evidence_label')}`"
        )
    lines.extend([
        "",
        "## 5. 缺失与待补查",
        f"- missing_required_assets_count: `{quality.get('missing_required_assets_count')}`",
        f"- missing_optional_assets_count: `{quality.get('missing_optional_assets_count')}`",
        f"- requires_followup_fields: `{quality.get('requires_followup_fields')}`",
        f"- wallets_with_followup_fields: `{quality.get('wallets_with_followup_fields')}`",
        "",
        "## 6. 边界声明",
        "- 本面板只展示 Phase01 事实、候选证据、缺失字段和质量状态。",
        "- 不输出确定性内幕/主控结论，不输出买卖建议，不输出策略状态机或交易执行字段。",
    ])
    return "\n".join(lines) + "\n"


def build_token_data_panel(
    token_address: str,
    *,
    mode: str = "live",
    root: Path | str = "/root/sikk-gmgn",
    write: bool = True,
) -> TokenDataPanel:
    root = Path(root)
    index_obj = build_fact_store_index(token_address, mode=mode, root=root, write=True)
    index = index_obj.to_dict()
    token_root = Path(index["token_root"])

    stage = _load_json(_selected_path(index, root, "token_stage_summary"))
    trades = _records(_load_json(_selected_path(index, root, "wallet_trade_normalized")))
    profiles = _records(_load_json(_selected_path(index, root, "wallet_entity_profile_normalized")))
    decisions = _records(_load_json(_selected_path(index, root, "wallet_intelligence_decision")))
    same_source = _records(_load_json(_selected_path(index, root, "same_source_evidence_normalized")))
    handoff = _load_json(_selected_path(index, root, "bot2_handoff_packet")) or {}
    contamination = _load_json(_selected_path(index, root, "contamination_scan")) or {}

    followup = _sum_followup_fields(trades)
    handoff_followup = handoff.get("requires_followup_fields") if isinstance(handoff, dict) else []
    if isinstance(handoff_followup, list):
        for f in handoff_followup:
            followup["field_distribution"][str(f)] = max(followup["field_distribution"].get(str(f), 0), 1)
    missing_summary = handoff.get("missing_fields_summary") if isinstance(handoff, dict) else None
    if isinstance(missing_summary, dict):
        # Handoff is the authoritative downstream contract for per-wallet missing fields.
        # Some trade rows may not carry the missing fields directly, so do not report 0
        # wallets when the handoff packet explicitly lists affected wallet addresses.
        followup["wallets_with_followup_fields"] = max(
            followup["wallets_with_followup_fields"],
            len([wallet for wallet, fields in missing_summary.items() if fields]),
        )

    panel = {
        "market_fact": _market_summary(stage),
        "record_counts": {
            "wallet_trade_records": len(trades),
            "wallet_profile_records": len(profiles),
            "wallet_intelligence_records": len(decisions),
            "same_source_candidate_groups": len(same_source),
        },
        "wallet_fact_summary": {
            "evidence_level_distribution": _counter(decisions, "evidence_level"),
            "risk_level_distribution": _counter(decisions, "risk_level"),
            "role_candidate_distribution": _counter(decisions, "role_candidates"),
            "top_wallets_by_observed_buy_amount": _top_wallets(trades, decisions),
        },
        "same_source_candidate_summary": _same_source_summary(same_source),
        "quality_and_missing": {
            **_missing_assets_summary(index),
            "requires_followup_fields": sorted(followup["field_distribution"].keys()),
            "followup_field_distribution": followup["field_distribution"],
            "wallets_with_followup_fields": followup["wallets_with_followup_fields"],
            "handoff_missing_fields_summary": handoff.get("missing_fields_summary") if isinstance(handoff, dict) else None,
        },
        "source_files": {
            key: asset.get("selected_path")
            for key, asset in (index.get("fact_assets") or {}).items()
            if asset.get("status") == "FOUND" and asset.get("fact_source", True)
        },
        "phase01_boundary": {
            "allowed": ["事实字段", "候选证据", "证据等级", "风险等级", "缺失字段", "质量状态", "交接状态"],
            "forbidden_summary": ["确定性内幕/主控结论", "买卖建议", "策略状态机字段", "实盘签名/广播/swap"],
        },
    }

    contamination_status = contamination.get("overall_status") or "NOT_AVAILABLE"
    out = TokenDataPanel(
        artifact_type="phase01_token_data_display_panel",
        token_address=token_address,
        mode=mode,
        generated_at=_now(),
        quality_status=index.get("quality_status"),
        recommended_action=index.get("recommended_action"),
        contamination_status=contamination_status,
        panel=panel,
        output_paths={},
        forbidden_term_scan={"status": "NOT_RUN", "hits": []},
    )
    out_dict = out.to_dict()
    md = _render_markdown(out_dict)
    out_dict["forbidden_term_scan"] = _scan_forbidden(json.dumps(out_dict, ensure_ascii=False) + "\n" + md)
    out.forbidden_term_scan = out_dict["forbidden_term_scan"]

    if write:
        report_dir = token_root / "source_wallet_packet" / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        json_path = report_dir / "phase01_token_data_display_panel.json"
        md_path = report_dir / "phase01_token_data_display_panel.md"
        out.output_paths = {
            "json": str(json_path),
            "markdown": str(md_path),
        }
        final_dict = out.to_dict()
        final_dict["forbidden_term_scan"] = _scan_forbidden(json.dumps(final_dict, ensure_ascii=False) + "\n" + md)
        json_path.write_text(json.dumps(final_dict, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        md_path.write_text(md, encoding="utf-8")
        out.forbidden_term_scan = final_dict["forbidden_term_scan"]
    return out
