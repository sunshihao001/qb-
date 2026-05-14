#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""K00 KV extractor for machine-readable task-package facts.

Turns K00 task execution packages / wallet-structure task manifests into a
standard KV fact layer that runners can consume without manual interpretation.
The extractor is local-file, additive-only, and paper-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_SCHEMA = Path("sikk_stable_trader_os/00_knowledge_intake/kv_cache/kv_cache.schema.json")
DEFAULT_OUTPUT_ROOT = Path("sikk_stable_trader_os/00_knowledge_intake/kv_cache/runtime_extractions")
FORBIDDEN_USES = ["direct_real_trade", "private_key", "auto_broadcast", "signing", "swap"]

ASSET_CLASS_BY_FIELD = {
    "required_inputs": "field_requirement",
    "required_outputs": "output_template",
    "acceptance": "counter_evidence_rule",
    "forbidden": "counter_evidence_rule",
    "next_actions": "runner_binding",
    "tasks": "task_node",
    "automation_policy": "phase_contract",
    "safety_boundary": "phase_contract",
    "objective": "judgement_logic",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_slug(value: Any, *, max_len: int = 80) -> str:
    text = re.sub(r"[^A-Za-z0-9_\-]+", "_", str(value).strip()).strip("_").lower()
    text = re.sub(r"_+", "_", text)
    return (text or "item")[:max_len]


def read_json(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def write_json(path: Path, payload: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(path)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def infer_doc_id(payload: dict[str, Any], source_path: Path) -> str:
    for key in ("doc_id", "task_id", "package_id"):
        value = payload.get(key)
        if value:
            return str(value)
    return safe_slug(source_path.stem).upper()


def infer_phases(value: Any, fallback: list[str] | None = None) -> list[str]:
    text = json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    phases = sorted(set(re.findall(r"\b(?:K\d{2}|P\d{2}|I\d{2})\b", text)))
    return phases or (fallback or ["K00"])


def infer_planes(asset_class: str, field_name: str) -> list[str]:
    if asset_class in {"field_requirement", "output_template"}:
        return ["Data Plane", "Schema Plane"]
    if asset_class in {"runner_binding", "task_node"}:
        return ["Control Plane", "Execution Plane", "Trace Plane"]
    if asset_class == "counter_evidence_rule":
        return ["Governance Plane", "Acceptance Plane"]
    if field_name in {"automation_policy", "safety_boundary"}:
        return ["Governance Plane", "Control Plane"]
    return ["Knowledge Plane", "Control Plane"]


def normalize_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def make_item(
    *,
    doc_id: str,
    raw_path: str,
    source_hash: str,
    field_name: str,
    asset_class: str,
    value: Any,
    index: int,
    phase_hint: list[str] | None = None,
) -> dict[str, Any]:
    summary = f"{field_name} item {index}: {normalize_value(value)[:220]}"
    slug_source = value.get("task_id") if isinstance(value, dict) and value.get("task_id") else f"{field_name}_{index}"
    key = f"KV::{doc_id}::{asset_class}::{safe_slug(slug_source)}::v1"
    phases = infer_phases(value, phase_hint)
    contracts: list[str] = []
    schemas: list[str] = []
    if field_name in {"required_inputs", "required_outputs", "next_actions", "tasks"}:
        contracts.append(f"{field_name}_contract")
    if field_name.endswith("schema") or "schema" in field_name:
        schemas.append(str(field_name))
    return {
        "key": key,
        "doc_id": doc_id,
        "source_span": {
            "raw_path": raw_path,
            "section": field_name,
            "line_start": None,
            "line_end": None,
        },
        "asset_class": asset_class,
        "value": {
            "summary": summary,
            "normalized_form": normalize_value(value),
            "code_facing_interpretation": f"Runner-readable K00 fact extracted from `{field_name}`; consumers must use this item instead of manual interpretation.",
        },
        "mappings": {
            "planes": infer_planes(asset_class, field_name),
            "phases": phases,
            "contracts": contracts,
            "schemas": schemas,
        },
        "reuse_policy": {
            "cache_status": "ACTIVE",
            "dedupe_key": safe_slug(f"{doc_id}_{field_name}_{sha256_text(normalize_value(value))[:12]}"),
            "version": "v1",
        },
        "evidence": {
            "evidence_level": "EVIDENCE_A_STRONG",
            "source_doc_hash": source_hash,
        },
        "governance": {
            "allowed_consumers": ["K00", "P00", "P01", "P09", "task_package_runner"],
            "forbidden_uses": FORBIDDEN_USES,
        },
    }


def iter_task_values(field_name: str, value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    if value in (None, ""):
        return []
    return [value]


def extract_kv_from_task_package(
    *,
    task_package_path: str | Path,
    output_root: str | Path = DEFAULT_OUTPUT_ROOT,
    schema_path: str | Path = DEFAULT_SCHEMA,
    doc_id: str | None = None,
) -> dict[str, Any]:
    source_path = Path(task_package_path)
    payload = read_json(source_path)
    resolved_doc_id = doc_id or infer_doc_id(payload, source_path)
    source_hash = sha256_file(source_path)
    phase_hint = [str(p) for p in payload.get("affected_phases", [])] if isinstance(payload.get("affected_phases"), list) else None

    items: list[dict[str, Any]] = []
    for field_name, asset_class in ASSET_CLASS_BY_FIELD.items():
        for idx, value in enumerate(iter_task_values(field_name, payload.get(field_name)), 1):
            items.append(
                make_item(
                    doc_id=resolved_doc_id,
                    raw_path=str(source_path),
                    source_hash=source_hash,
                    field_name=field_name,
                    asset_class=asset_class,
                    value=value,
                    index=idx,
                    phase_hint=phase_hint,
                )
            )

    # Generic top-level fields make the package self-describing without bloating the KV layer.
    for field_name in ("artifact_type", "package_id", "status", "runtime_allowed"):
        if field_name in payload:
            items.append(
                make_item(
                    doc_id=resolved_doc_id,
                    raw_path=str(source_path),
                    source_hash=source_hash,
                    field_name=field_name,
                    asset_class="phase_contract",
                    value=payload[field_name],
                    index=1,
                    phase_hint=phase_hint,
                )
            )

    out = Path(output_root) / safe_slug(resolved_doc_id)
    items_path = out / f"kv_items_{safe_slug(resolved_doc_id)}.jsonl"
    manifest_path = out / f"kv_cache_manifest_{safe_slug(resolved_doc_id)}.json"
    facts_path = out / f"k00_facts_{safe_slug(resolved_doc_id)}.json"

    out.mkdir(parents=True, exist_ok=True)
    items_path.write_text("\n".join(json.dumps(item, ensure_ascii=False) for item in items) + ("\n" if items else ""), encoding="utf-8")
    by_asset_class = {asset_class: sum(1 for item in items if item["asset_class"] == asset_class) for asset_class in sorted({item["asset_class"] for item in items})}
    next_actions = payload.get("next_actions") if isinstance(payload.get("next_actions"), list) else []
    tasks = payload.get("tasks") if isinstance(payload.get("tasks"), list) else []
    manifest = {
        "artifact_type": "k00_kv_cache_manifest",
        "doc_id": resolved_doc_id,
        "created_at": utc_now(),
        "status": "KV_CACHE_READY" if items else "KV_CACHE_EMPTY",
        "schema": str(schema_path),
        "raw_path": str(source_path),
        "source_sha256": source_hash,
        "item_count": len(items),
        "by_asset_class": by_asset_class,
        "items_path": str(items_path),
        "items": [item["key"] for item in items],
        "runner_inputs": {
            "has_next_actions": bool(next_actions),
            "next_action_count": len(next_actions),
            "task_count": len(tasks),
        },
        "safety_boundary": {
            "paper_only": True,
            "readonly_source_files": True,
            "additive_outputs_only": True,
            "no_private_key": True,
            "no_signing": True,
            "no_broadcast": True,
            "no_swap": True,
        },
    }
    facts = {
        "artifact_type": "k00_standard_fact_package",
        "doc_id": resolved_doc_id,
        "generated_at": utc_now(),
        "source_task_package": str(source_path),
        "kv_cache_manifest": str(manifest_path),
        "kv_items": str(items_path),
        "facts": {
            "status": payload.get("status"),
            "objective": payload.get("objective"),
            "runtime_allowed": payload.get("runtime_allowed", False),
            "affected_phases": payload.get("affected_phases", phase_hint or ["K00"]),
            "next_actions": next_actions,
            "tasks": tasks,
            "acceptance": payload.get("acceptance", []),
            "automation_policy": payload.get("automation_policy", {}),
            "safety_boundary": payload.get("safety_boundary", manifest["safety_boundary"]),
        },
        "kv_summary": {
            "item_count": len(items),
            "by_asset_class": by_asset_class,
            "runner_binding_count": by_asset_class.get("runner_binding", 0),
            "task_node_count": by_asset_class.get("task_node", 0),
        },
        "acceptance_gate": {
            "status": "PASS" if items and Path(schema_path).exists() else "NEEDS_ACTION",
            "checks": {
                "kv_items_materialized": items_path.exists(),
                "kv_manifest_materialized": True,
                "schema_exists": Path(schema_path).exists(),
                "raw_source_exists": source_path.exists(),
            },
        },
    }
    write_json(manifest_path, manifest)
    write_json(facts_path, facts)
    return {
        "status": "COMPLETED",
        "doc_id": resolved_doc_id,
        "kv_cache_manifest": str(manifest_path),
        "kv_items": str(items_path),
        "k00_facts": str(facts_path),
        "item_count": len(items),
        "by_asset_class": by_asset_class,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract K00 KV facts from a task package")
    parser.add_argument("--task-package", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--schema-path", default=str(DEFAULT_SCHEMA))
    parser.add_argument("--doc-id", default="")
    args = parser.parse_args()
    result = extract_kv_from_task_package(
        task_package_path=args.task_package,
        output_root=args.output_root,
        schema_path=args.schema_path,
        doc_id=args.doc_id or None,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
