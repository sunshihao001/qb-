#!/usr/bin/env python3
"""SIKK unified view index builder.

把 `sikk_live_run.py` 已生成的 paper/live/site/report 输出收敛成一组只读索引，供
CLI / Web / Telegram / Report / Alert 共用。该模块不采集、不报价、不交易、不签名、
不广播；只读取本地文件并写入 `data/gmgn_candidates_live_run/index/*.json`。
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

SCHEMA_VERSION = "sikk.unified_view.v1"
BOUNDARY = "SIKK 统一索引层；只读展示、诊断、复盘和提醒；不执行真实 swap，不读取私钥，不签名，不自动 broadcast。"
SAFETY_DEFAULTS = {
    "real_swap_enabled": False,
    "broadcast_allowed": False,
    "private_key_required": False,
    "confirmation_enabled": False,
}
FORBIDDEN_ALERT_WORDS = ("BUY", "SELL", "SWAP", "EXECUTE", "APPROVE", "BROADCAST")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def read_csv_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return [dict(row) for row in csv.DictReader(f)]
    except Exception:
        return []


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    s = str(value).strip()
    return s if s and s.lower() not in {"none", "null", "nan"} else default


def first_non_empty(row: Mapping[str, Any], keys: Iterable[str], default: Any = "") -> Any:
    for key in keys:
        value = row.get(key)
        if text(value):
            return value
    return default


def token_address(row: Mapping[str, Any]) -> str:
    return text(first_non_empty(row, ["token_address", "代币地址", "address", "token", "mint"]))


def token_symbol(row: Mapping[str, Any]) -> str:
    return text(first_non_empty(row, ["token_symbol", "代币符号", "symbol"], "UNKNOWN"), "UNKNOWN")


def position_id(row: Mapping[str, Any], prefix: str, idx: int) -> str:
    raw = text(first_non_empty(row, ["position_id", "paper_position_id", "case_id", "trade_id"]))
    if raw:
        return raw
    token = token_address(row)
    if token:
        return f"{prefix}_{token[:8]}_{idx + 1}"
    return f"{prefix}_{idx + 1}"


def envelope(payload: Dict[str, Any], generated_at: str) -> Dict[str, Any]:
    base = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at,
        "boundary": BOUNDARY,
        "safety": dict(SAFETY_DEFAULTS),
    }
    base.update(payload)
    return base


def latest_file(paths: Iterable[Path]) -> Optional[Path]:
    existing = [p for p in paths if p.exists()]
    if not existing:
        return None
    return max(existing, key=lambda p: p.stat().st_mtime)


def discover_wallet_daily_report(base: Path) -> Dict[str, str]:
    reports = base / "reports"
    latest_csv = latest_file(reports.glob("wallet_structure_daily_report_*.csv")) if reports.exists() else None
    latest_json = latest_file(reports.glob("wallet_structure_daily_report_*.json")) if reports.exists() else None
    latest_md = latest_file(reports.glob("wallet_structure_daily_report_*.md")) if reports.exists() else None
    return {
        "latest_csv": str(latest_csv) if latest_csv else "",
        "latest_json": str(latest_json) if latest_json else "",
        "latest_md": str(latest_md) if latest_md else "",
    }


def source_file_status(base: Path) -> Dict[str, Dict[str, Any]]:
    files = {
        "live_run_manifest": base / "live_run_manifest.json",
        "live_state": base / "live_state.json",
        "live_board": base / "live_board.md",
        "live_dashboard": base / "live_dashboard.html",
        "site_dashboard_data": base / "site" / "dashboard_data.json",
        "site_index": base / "site" / "index.html",
        "site_app": base / "site" / "app.js",
        "site_style": base / "site" / "style.css",
        "paper_open_json": base / "paper_live" / "paper_positions_open.json",
        "paper_closed_json": base / "paper_live" / "paper_positions_closed.json",
        "paper_open_csv": base / "paper_live" / "paper_positions_open.csv",
        "paper_closed_csv": base / "paper_live" / "paper_positions_closed.csv",
        "case_files_manifest": base / "paper_live" / "case_files" / "case_files_manifest.json",
    }
    return {
        key: {
            "path": str(path),
            "exists": path.exists(),
            "size_bytes": path.stat().st_size if path.exists() else 0,
        }
        for key, path in files.items()
    }


def paper_rows(base: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, str]], List[Dict[str, str]]]:
    paper = base / "paper_live"
    open_payload = read_json(paper / "paper_positions_open.json", {"open_positions": []})
    closed_payload = read_json(paper / "paper_positions_closed.json", {"closed_positions": []})
    open_rows = open_payload.get("open_positions", []) if isinstance(open_payload, Mapping) else []
    closed_rows = closed_payload.get("closed_positions", []) if isinstance(closed_payload, Mapping) else []
    if not isinstance(open_rows, list):
        open_rows = []
    if not isinstance(closed_rows, list):
        closed_rows = []
    return (
        [dict(r) for r in open_rows if isinstance(r, Mapping)],
        [dict(r) for r in closed_rows if isinstance(r, Mapping)],
        read_csv_rows(paper / "paper_positions_open.csv"),
        read_csv_rows(paper / "paper_positions_closed.csv"),
    )


def build_token_detail_index(base: Path, dashboard_data: Mapping[str, Any], generated_at: str) -> Dict[str, Any]:
    tokens = []
    for idx, row in enumerate(dashboard_data.get("tokens") or [], start=1):
        if not isinstance(row, Mapping):
            continue
        normalized = dict(row)
        normalized.update({
            "token_id": f"T{idx}",
            "token_address": token_address(row),
            "token_symbol": token_symbol(row),
            "状态": text(row.get("current_state") or row.get("paper_status"), "UNKNOWN"),
            "信号等级": text(row.get("signal_level"), "UNKNOWN"),
            "钱包结构": text(row.get("wallet_structure_status"), "MISSING"),
            "主导侧心理": text(row.get("operator_psychology_label") or row.get("operator_psychology"), "证据不足 / 待复查"),
            "纸面对齐": text(row.get("paper_trade_alignment"), "待复查"),
            "观察重点": text(row.get("next_observation_focus"), "待补"),
            "安全边界": BOUNDARY,
        })
        tokens.append(normalized)
    by_address = {r["token_address"]: r["token_id"] for r in tokens if r.get("token_address")}
    by_symbol = {r["token_symbol"]: r["token_id"] for r in tokens if r.get("token_symbol")}
    return envelope({"tokens": tokens, "by_address": by_address, "by_symbol": by_symbol, "token_count": len(tokens)}, generated_at)


def case_metric_from_row(row: Mapping[str, Any]) -> Dict[str, Any]:
    """从 paper/case row 提取 Case File 质量摘要；只做本地只读归一化。"""
    missing = row.get("evidence_missing_fields") or row.get("case_missing_fields") or row.get("missing_fields") or []
    if not isinstance(missing, list):
        missing = [missing] if text(missing) else []
    preview = row.get("case_field_sources_preview") or row.get("field_sources_preview") or []
    if not isinstance(preview, list):
        preview = [preview] if text(preview) else []
    return {
        "case_quality_level": text(row.get("case_quality_level") or row.get("case_quality"), "待补"),
        "case_completeness_score": row.get("case_completeness_score", ""),
        "case_field_source_count": row.get("case_field_source_count") or row.get("field_source_count") or 0,
        "case_field_sources_preview": preview[:8],
        "case_missing_fields": missing,
        "evidence_missing_fields": missing,
        "strategy_review_eligible": bool(row.get("strategy_review_eligible")),
    }


def enrich_rows_with_dashboard_case_metrics(rows: List[Dict[str, Any]], dashboard_rows: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    """用 site/dashboard_data.json 中已聚合的 Case File 摘要回填 paper 行。"""
    by_pos: Dict[str, Mapping[str, Any]] = {}
    by_token: Dict[str, Mapping[str, Any]] = {}
    for item in dashboard_rows:
        if not isinstance(item, Mapping):
            continue
        pid = text(first_non_empty(item, ["position_id", "paper_position_id", "case_id", "trade_id"]))
        token = token_address(item)
        if pid:
            by_pos[pid] = item
        if token:
            by_token[token] = item
    enriched: List[Dict[str, Any]] = []
    metric_keys = {
        "case_quality_level",
        "case_quality",
        "case_completeness_score",
        "case_field_source_count",
        "field_source_count",
        "case_field_sources_preview",
        "field_sources_preview",
        "case_missing_fields",
        "evidence_missing_fields",
        "missing_fields",
        "strategy_review_eligible",
        "case_file_json",
        "case_file_md",
    }
    for row in rows:
        out = dict(row)
        source = by_pos.get(text(first_non_empty(row, ["position_id", "paper_position_id", "case_id", "trade_id"]))) or by_token.get(token_address(row))
        if source:
            for key in metric_keys:
                if key in source and (not text(out.get(key)) if not isinstance(out.get(key), list) else not out.get(key)):
                    out[key] = source.get(key)
        enriched.append(out)
    return enriched


def normalize_position(row: Mapping[str, Any], status: str, idx: int) -> Dict[str, Any]:
    prefix = "P" if status == "OPEN" else "C"
    out = dict(row)
    out.update(case_metric_from_row(row))
    out.update({
        "position_id": position_id(row, prefix, idx),
        "position_short_id": f"{prefix}{idx + 1}",
        "position_status": status,
        "token_address": token_address(row),
        "token_symbol": token_symbol(row),
        "安全边界": BOUNDARY,
    })
    return out


def build_position_indexes(open_rows: List[Dict[str, Any]], closed_rows: List[Dict[str, Any]], generated_at: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    open_positions = [normalize_position(row, "OPEN", idx) for idx, row in enumerate(open_rows)]
    closed_positions = [normalize_position(row, "CLOSED", idx) for idx, row in enumerate(closed_rows)]
    position_index = envelope({
        "open_count": len(open_positions),
        "closed_count": len(closed_positions),
        "open_positions": open_positions,
        "closed_positions": closed_positions,
        "by_token_address": {p.get("token_address"): p.get("position_short_id") for p in open_positions + closed_positions if p.get("token_address")},
    }, generated_at)
    latest_open = envelope({"open_count": len(open_positions), "open_positions": open_positions}, generated_at)
    latest_closed = envelope({"closed_count": len(closed_positions), "closed_positions": closed_positions}, generated_at)
    return position_index, latest_open, latest_closed


def build_case_file_index(base: Path, open_positions: List[Dict[str, Any]], closed_positions: List[Dict[str, Any]], generated_at: str) -> Dict[str, Any]:
    manifest_path = base / "paper_live" / "case_files" / "case_files_manifest.json"
    manifest = read_json(manifest_path, {})
    cases: List[Dict[str, Any]] = []
    raw_cases = []
    if isinstance(manifest, Mapping):
        for key in ("case_files", "cases", "files"):
            value = manifest.get(key)
            if isinstance(value, list):
                raw_cases = value
                break
    for idx, item in enumerate(raw_cases):
        if not isinstance(item, Mapping):
            continue
        case = dict(item)
        case.update(case_metric_from_row(item))
        case.setdefault("case_short_id", f"C{idx + 1}")
        cases.append(case)
    if not cases:
        for idx, pos in enumerate(open_positions + closed_positions):
            ref = text(pos.get("case_file_md") or pos.get("case_md") or pos.get("case_file_json"))
            if ref:
                cases.append({"case_short_id": f"C{idx + 1}", "token_address": pos.get("token_address"), "case_file": ref})
    return envelope({"manifest_path": str(manifest_path), "case_count": len(cases), "cases": cases}, generated_at)


def build_auto_review_index(dashboard_data: Mapping[str, Any], generated_at: str) -> Dict[str, Any]:
    strategy = dashboard_data.get("strategy_panel") if isinstance(dashboard_data.get("strategy_panel"), Mapping) else {}
    return envelope({
        "review_status": "READY_FROM_STRATEGY_PANEL" if strategy else "MISSING_STRATEGY_PANEL",
        "strategy_summary": strategy.get("summary") if isinstance(strategy, Mapping) else {},
        "signal_groups": strategy.get("signal_groups") if isinstance(strategy, Mapping) else [],
        "wallet_groups": strategy.get("wallet_groups") if isinstance(strategy, Mapping) else [],
        "scope_note": "自动复盘索引只聚合策略表现与样本质量，不输出真实交易建议。",
    }, generated_at)


def sanitize_alert(alert: Dict[str, Any]) -> Dict[str, Any]:
    raw = json.dumps(alert, ensure_ascii=False)
    upper = raw.upper()
    if any(word in upper for word in FORBIDDEN_ALERT_WORDS):
        alert = dict(alert)
        alert["action"] = "复查"
        alert["安全说明"] = "提醒文本已安全降级；不包含交易执行动作。"
    return alert


def build_alert_index(dashboard_data: Mapping[str, Any], open_positions: List[Dict[str, Any]], generated_at: str) -> Dict[str, Any]:
    alerts: List[Dict[str, Any]] = []
    coverage = dashboard_data.get("coverage_diagnostics") if isinstance(dashboard_data.get("coverage_diagnostics"), Mapping) else {}
    missing_rate = coverage.get("wallet_missing_rate_pct")
    try:
        missing_rate_num = float(missing_rate)
    except Exception:
        missing_rate_num = 0.0
    if missing_rate_num >= 50:
        alerts.append({
            "alert_id": "A1",
            "type": "DATA_SYNC_FAIL",
            "severity": "HIGH",
            "title": "钱包结构覆盖缺口较高",
            "reason": f"wallet_missing_rate_pct={missing_rate_num}",
            "action": "数据补全",
        })
    for idx, pos in enumerate(open_positions, start=len(alerts) + 1):
        wallet_status = text(pos.get("wallet_structure_status") or pos.get("钱包结构状态"), "MISSING")
        pnl = text(pos.get("paper_pnl_pct") or pos.get("当前收益率_pct"), "")
        if wallet_status.upper() in {"WALLET_BLOCK", "BLOCK"}:
            alerts.append({"alert_id": f"A{idx}", "type": "WALLET_BLOCK", "severity": "HIGH", "token_address": pos.get("token_address"), "title": "开放纸面仓位钱包结构阻断", "reason": wallet_status, "action": "退出监控"})
        elif pnl.startswith("-"):
            alerts.append({"alert_id": f"A{idx}", "type": "PAPER_DRAWDOWN", "severity": "MEDIUM", "token_address": pos.get("token_address"), "title": "开放纸面仓位浮亏", "reason": f"paper_pnl_pct={pnl}", "action": "观察"})
    alerts = [sanitize_alert(a) for a in alerts]
    return envelope({"alert_count": len(alerts), "alerts": alerts, "scope_note": "Alert 只读提醒；不执行、不授权、不广播真实交易。"}, generated_at)


def build_telegram_callback_index(token_index: Mapping[str, Any], position_index: Mapping[str, Any], case_index: Mapping[str, Any], alert_index: Mapping[str, Any], generated_at: str) -> Dict[str, Any]:
    callbacks: Dict[str, Dict[str, Any]] = {
        "menu:main": {"type": "menu", "view": "main"},
        "list:open:0": {"type": "list", "view": "open_positions", "page": 0},
        "list:closed:0": {"type": "list", "view": "closed_positions", "page": 0},
        "refresh:main": {"type": "refresh", "view": "main"},
    }
    for token in token_index.get("tokens", [])[:80]:
        code = token.get("token_id")
        if code:
            callbacks[f"tok:{code}"] = {"type": "token", "token_id": code, "token_address": token.get("token_address"), "token_symbol": token.get("token_symbol")}
    for pos in (position_index.get("open_positions", []) + position_index.get("closed_positions", []))[:80]:
        code = pos.get("position_short_id")
        if code:
            callbacks[f"pos:{code}"] = {"type": "position", "position_id": pos.get("position_id"), "position_short_id": code, "token_address": pos.get("token_address")}
            callbacks[f"entry:{code}"] = {"type": "entry_evidence", "position_id": pos.get("position_id"), "position_short_id": code, "token_address": pos.get("token_address")}
    for case in case_index.get("cases", [])[:80]:
        code = case.get("case_short_id")
        if code:
            callbacks[f"case:{code}"] = {
                "type": "case",
                "case_short_id": code,
                "case_file": case.get("case_file") or case.get("case_file_md") or case.get("case_file_json") or case.get("path") or case.get("case_md"),
                "token_address": case.get("token_address"),
                "position_id": case.get("position_id"),
            }
    for pos in (position_index.get("open_positions", []) + position_index.get("closed_positions", []))[:80]:
        code = pos.get("position_short_id")
        if code:
            callbacks[f"review:{code}"] = {"type": "review", "position_short_id": code, "position_id": pos.get("position_id"), "token_address": pos.get("token_address")}
    for alert in alert_index.get("alerts", [])[:80]:
        code = alert.get("alert_id")
        if code:
            callbacks[f"alert:{code}"] = {"type": "alert", "alert_id": code, "alert_type": alert.get("type")}
    return envelope({"callbacks": callbacks, "callback_count": len(callbacks), "rule": "callback_data 使用英文短码；用户可见内容由 view 层中文化。"}, generated_at)


def build_system_index(base: Path, dashboard_data: Mapping[str, Any], open_rows: List[Dict[str, Any]], closed_rows: List[Dict[str, Any]], open_csv_rows: List[Dict[str, str]], closed_csv_rows: List[Dict[str, str]], generated_at: str) -> Dict[str, Any]:
    sources = source_file_status(base)
    wallet_report = discover_wallet_daily_report(base)
    tokens = dashboard_data.get("tokens") if isinstance(dashboard_data.get("tokens"), list) else []
    manifest = read_json(base / "live_run_manifest.json", {})
    manifest_cfg = manifest.get("配置") if isinstance(manifest, Mapping) and isinstance(manifest.get("配置"), Mapping) else {}
    safety = dict(SAFETY_DEFAULTS)
    safety.update({
        "real_swap_enabled": bool(manifest_cfg.get("real_swap_enabled", False)),
        "broadcast_allowed": bool(manifest_cfg.get("broadcast_allowed", False)),
        "confirmation_enabled": bool(manifest_cfg.get("confirmation_enabled", False)),
        "telegram_broadcast_enabled": bool(manifest_cfg.get("telegram_broadcast_enabled", False)),
        "private_key_required": False,
    })
    return envelope({
        "entrypoint": {"canonical": "sikk_live_run.py", "mode": manifest.get("模式", "unknown") if isinstance(manifest, Mapping) else "unknown"},
        "base_dir": str(base),
        "source_files": sources,
        "runtime_outputs": {
            "live_state_json": str(base / "live_state.json"),
            "live_board_md": str(base / "live_board.md"),
            "live_dashboard_html": str(base / "live_dashboard.html"),
        },
        "site_outputs": {
            "dashboard_data_json": str(base / "site" / "dashboard_data.json"),
            "index_html": str(base / "site" / "index.html"),
            "app_js": str(base / "site" / "app.js"),
            "style_css": str(base / "site" / "style.css"),
        },
        "wallet_daily_report": wallet_report,
        "paper_sync": {
            "open_json_count": len(open_rows),
            "closed_json_count": len(closed_rows),
            "open_csv_count": len(open_csv_rows),
            "closed_csv_count": len(closed_csv_rows),
            "open_csv_exists": (base / "paper_live" / "paper_positions_open.csv").exists(),
            "closed_csv_exists": (base / "paper_live" / "paper_positions_closed.csv").exists(),
            "json_csv_note": "paper JSON 与 CSV 均作为统一索引输入；数量差异需由日报/审计层解释。",
        },
        "counts": {
            "token_count": len(tokens),
            "open_position_count": len(open_rows),
            "closed_position_count": len(closed_rows),
            "opportunity_count": len(dashboard_data.get("opportunities") or []),
        },
        "system_health": dashboard_data.get("system_health") or {},
        "coverage_diagnostics": dashboard_data.get("coverage_diagnostics") or {},
        "safety": safety,
    }, generated_at)


def build_unified_indexes(base_dir: str | Path = "data/gmgn_candidates_live_run") -> Dict[str, Any]:
    base = Path(base_dir)
    generated_at = utc_now()
    dashboard_data = read_json(base / "site" / "dashboard_data.json", {})
    if not isinstance(dashboard_data, Mapping):
        dashboard_data = {}
    open_rows, closed_rows, open_csv_rows, closed_csv_rows = paper_rows(base)
    dashboard_open = ((dashboard_data.get("paper_positions") or {}).get("open") or []) if isinstance(dashboard_data.get("paper_positions"), Mapping) else []
    dashboard_closed = ((dashboard_data.get("paper_positions") or {}).get("closed") or []) if isinstance(dashboard_data.get("paper_positions"), Mapping) else []
    open_rows = enrich_rows_with_dashboard_case_metrics(open_rows, dashboard_open)
    closed_rows = enrich_rows_with_dashboard_case_metrics(closed_rows, dashboard_closed)

    token_index = build_token_detail_index(base, dashboard_data, generated_at)
    position_index, latest_open, latest_closed = build_position_indexes(open_rows, closed_rows, generated_at)
    case_index = build_case_file_index(base, position_index["open_positions"], position_index["closed_positions"], generated_at)
    auto_review_index = build_auto_review_index(dashboard_data, generated_at)
    alert_index = build_alert_index(dashboard_data, position_index["open_positions"], generated_at)
    telegram_callback_index = build_telegram_callback_index(token_index, position_index, case_index, alert_index, generated_at)
    system_index = build_system_index(base, dashboard_data, open_rows, closed_rows, open_csv_rows, closed_csv_rows, generated_at)

    index_dir = base / "index"
    payloads = {
        "system_index.json": system_index,
        "token_detail_index.json": token_index,
        "position_index.json": position_index,
        "latest_open_positions.json": latest_open,
        "latest_closed_positions.json": latest_closed,
        "case_file_index.json": case_index,
        "auto_review_index.json": auto_review_index,
        "alert_index.json": alert_index,
        "telegram_callback_index.json": telegram_callback_index,
    }
    for filename, payload in payloads.items():
        write_json(index_dir / filename, payload)

    return {
        "index_dir": str(index_dir),
        "written_files": [str(index_dir / name) for name in payloads],
        "system_index": system_index,
        "token_detail_index": token_index,
        "position_index": position_index,
        "latest_open_positions": latest_open,
        "latest_closed_positions": latest_closed,
        "case_file_index": case_index,
        "auto_review_index": auto_review_index,
        "alert_index": alert_index,
        "telegram_callback_index": telegram_callback_index,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SIKK 统一索引生成器（只读，不交易）")
    parser.add_argument("--base-dir", default="data/gmgn_candidates_live_run")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    result = build_unified_indexes(args.base_dir)
    print(json.dumps({"index_dir": result["index_dir"], "written_files": result["written_files"], "boundary": BOUNDARY}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
