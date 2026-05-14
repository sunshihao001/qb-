from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .contracts import HANDOFF_LIKE_KEYS, INFERENCE_LIKE_KEYS, STATE_LIKE_KEYS
from .legacy_quarantine import enrich_contamination_report_with_legacy_quarantine


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _collect_keys(payload: Any) -> set[str]:
    keys: set[str] = set()
    if isinstance(payload, Mapping):
        for key, value in payload.items():
            keys.add(str(key))
            keys.update(_collect_keys(value))
    elif isinstance(payload, list):
        for item in payload:
            keys.update(_collect_keys(item))
    return keys


def _issue(code: str, path: Path, detail: str) -> dict[str, str]:
    return {"code": code, "path": str(path), "detail": detail}


def scan_wallet_data_contamination(data_root: str | Path) -> dict[str, Any]:
    root = Path(data_root)
    issues: list[dict[str, str]] = []
    files_checked = 0

    if not root.exists():
        return {
            "overall_status": "PASS",
            "checked_at": _utc_now(),
            "data_root": str(root),
            "files_checked": 0,
            "issues": [],
            "note": "data_root_missing_treated_as_empty",
        }

    for path in root.rglob("*.json"):
        files_checked += 1
        rel = path.relative_to(root).as_posix()
        payload = _load_json(path)
        if payload is None:
            continue
        keys = _collect_keys(payload)

        # Guard-wrapped artifacts should be evaluated by declared layer too.
        guard_layer = None
        if isinstance(payload, Mapping):
            guard_layer = (payload.get("guard_metadata") or {}).get("semantic_layer")
            scan_payload = payload.get("payload", payload)
            keys = _collect_keys(scan_payload)

        is_facts = "/facts/" in f"/{rel}/" or guard_layer == "facts"
        is_raw = "/raw/" in f"/{rel}/" or guard_layer == "raw"
        is_normalized = "/normalized/" in f"/{rel}/" or guard_layer == "normalized"
        is_wallet_data = "/wallet_data/" in f"/{rel}/"
        is_fallback = "/legacy_fallback/" in f"/{rel}/" or "fallback" in path.name.lower()
        is_compat = rel.startswith("sikk_sol_full_auto_workflow/") or "/sikk_sol_full_auto_workflow/" in f"/{rel}/"

        if is_facts or is_raw or is_normalized:
            bad = keys.intersection(INFERENCE_LIKE_KEYS)
            if bad:
                issues.append(_issue("INFERENCE_FIELD_IN_FACTS" if is_facts else "INFERENCE_FIELD_IN_LOWER_LAYER", path, f"inference-like keys: {sorted(bad)}"))
            bad = keys.intersection(HANDOFF_LIKE_KEYS)
            if bad:
                issues.append(_issue("HANDOFF_FIELD_IN_LOWER_LAYER", path, f"handoff-like keys: {sorted(bad)}"))
            bad = keys.intersection(STATE_LIKE_KEYS)
            if bad:
                issues.append(_issue("STATE_FIELD_IN_WALLET_DATA" if is_wallet_data else "STATE_FIELD_IN_LOWER_LAYER", path, f"state-like keys: {sorted(bad)}"))

        if is_facts and not ({"raw_ref", "raw_unit_refs"}.intersection(keys)):
            # Allow guarded facts with raw: source refs.
            refs = []
            if isinstance(payload, Mapping):
                refs = (payload.get("guard_metadata") or {}).get("source_refs") or []
            if not any(str(ref).startswith("raw:") for ref in refs):
                issues.append(_issue("FACTS_MISSING_RAW_REF", path, "facts artifact lacks raw_ref/raw_unit_refs/raw: source_refs"))

        if is_fallback:
            if "mapping_id" not in keys:
                issues.append(_issue("LEGACY_FALLBACK_MISSING_MAPPING_ID", path, "legacy fallback must include mapping_id"))
            if "read_mode" not in keys:
                issues.append(_issue("LEGACY_FALLBACK_MISSING_READ_MODE", path, "legacy fallback must include read_mode=readonly"))

        if is_compat and path.name in {"wallet_structure_decision.json", "candidate_states.validated.json"}:
            issues.append(_issue("COMPAT_ROUTE_CANONICAL_DECISION", path, "compat route must not produce canonical wallet decision artifacts"))

    report = {
        "overall_status": "PASS" if not issues else "FAIL",
        "checked_at": _utc_now(),
        "data_root": str(root),
        "files_checked": files_checked,
        "issues": issues,
    }
    return enrich_contamination_report_with_legacy_quarantine(report)
