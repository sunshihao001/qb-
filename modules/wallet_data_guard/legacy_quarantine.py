from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_legacy_issue(issue: Mapping[str, Any], data_root: str | Path | None = None) -> bool:
    path = str(issue.get("path") or "")
    normalized = path.replace("\\", "/")
    return "/source_wallet_bot/legacy/" in normalized or "/legacy/" in normalized or normalized.startswith("legacy/")


def split_legacy_and_active_issues(issues: list[Mapping[str, Any]], data_root: str | Path | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    legacy: list[dict[str, Any]] = []
    active: list[dict[str, Any]] = []
    for issue in issues:
        row = dict(issue)
        if is_legacy_issue(row, data_root):
            row["quarantine_status"] = "LEGACY_QUARANTINED_READONLY"
            row["contaminated_source"] = True
            legacy.append(row)
        else:
            active.append(row)
    return legacy, active


def enrich_contamination_report_with_legacy_quarantine(report: Mapping[str, Any]) -> dict[str, Any]:
    enriched = dict(report)
    issues = [dict(item) for item in enriched.get("issues", []) or []]
    legacy, active = split_legacy_and_active_issues(issues, enriched.get("data_root"))
    enriched["legacy_quarantine"] = {
        "status": "ACTIVE_QUARANTINE" if legacy else "EMPTY",
        "legacy_issues_count": len(legacy),
        "policy": {
            "read_mode": "readonly",
            "delete_old_files": False,
            "move_old_files": False,
            "contaminated_source_required": True,
            "raw_fact_direct_use_allowed": False,
        },
        "issues": legacy,
    }
    enriched["active_issues_count"] = len(active)
    enriched["legacy_issues_count"] = len(legacy)
    enriched["active_issues"] = active
    if active:
        enriched["overall_status"] = "FAIL"
    elif legacy:
        enriched["overall_status"] = "PASS_WITH_LEGACY_QUARANTINE"
    else:
        enriched["overall_status"] = "PASS"
    return enriched


def build_legacy_quarantine_index(
    data_root: str | Path,
    *,
    report: Mapping[str, Any] | None = None,
    output_dir: str | Path | None = None,
) -> dict[str, Any]:
    from .contamination_scan import scan_wallet_data_contamination

    data_root_path = Path(data_root)
    enriched = enrich_contamination_report_with_legacy_quarantine(report or scan_wallet_data_contamination(data_root_path))
    legacy_issues = enriched.get("legacy_quarantine", {}).get("issues", []) or []
    active_issues = enriched.get("active_issues", []) or []
    out_dir = Path(output_dir) if output_dir else data_root_path / "verification"
    out_dir.mkdir(parents=True, exist_ok=True)
    index = {
        "artifact_type": "legacy_contamination_quarantine_index",
        "generated_at": _utc_now(),
        "data_root": str(data_root_path),
        "status": "ACTIVE_QUARANTINE" if legacy_issues else "EMPTY",
        "legacy_issues_count": len(legacy_issues),
        "active_issues_count": len(active_issues),
        "policy": {
            "read_mode": "readonly",
            "delete_old_files": False,
            "move_old_files": False,
            "copy_only": True,
            "contaminated_source_required": True,
            "raw_fact_direct_use_allowed": False,
            "fallback_allowed_with_warning": True,
        },
        "legacy_issues": legacy_issues,
        "active_issues": active_issues,
    }
    json_path = out_dir / "legacy_contamination_quarantine_index.json"
    json_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    index["json_path"] = str(json_path)
    json_path.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return index
