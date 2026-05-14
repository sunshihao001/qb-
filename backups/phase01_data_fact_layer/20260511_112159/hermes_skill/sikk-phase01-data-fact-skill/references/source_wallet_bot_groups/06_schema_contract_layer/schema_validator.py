from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable

from .config import FORBIDDEN_HANDOFF_FIELDS
from .errors import ForbiddenFieldError, SchemaValidationError

REQUIRED_DESIGN_FILES = [
    "modules/source_wallet_bot/source_registry_schema.json",
    "modules/source_wallet_bot/wallet_raw_normalized_schema.json",
    "modules/source_wallet_bot/wallet_entity_profile_schema.json",
    "modules/source_wallet_bot/current_token_behavior_schema.json",
    "modules/source_wallet_bot/same_source_group_schema.json",
    "modules/source_wallet_bot/wallet_intelligence_decision_schema.json",
    "modules/source_wallet_bot/bot2_handoff_packet_schema.json",
    "modules/source_wallet_bot/gmgn_to_sikk_field_mapping.csv",
    "modules/source_wallet_bot/wallet_role_rule_matrix.csv",
    "modules/source_wallet_bot/evidence_level_matrix.csv",
    "modules/source_wallet_bot/gmgn_note_dictionary.csv",
]


def validate_required_keys(payload: dict[str, Any], required: Iterable[str]) -> None:
    missing = [key for key in required if key not in payload]
    if missing:
        raise SchemaValidationError(f"missing required keys: {', '.join(missing)}")


def assert_no_forbidden_fields(payload: Any, forbidden: set[str] | None = None) -> None:
    forbidden = forbidden or FORBIDDEN_HANDOFF_FIELDS
    found: list[str] = []

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key in forbidden:
                    found.append(key)
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)
    if found:
        raise ForbiddenFieldError(f"forbidden handoff fields present: {', '.join(sorted(set(found)))}")


def validate_json_file(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise SchemaValidationError(f"json file missing: {p}")
    try:
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as exc:
        raise SchemaValidationError(f"invalid json {p}: {exc}") from exc


def validate_source_wallet_design_package(project_root: str | Path) -> dict[str, Any]:
    root = Path(project_root)
    missing = [rel for rel in REQUIRED_DESIGN_FILES if not (root / rel).exists()]
    json_results: dict[str, str] = {}
    for rel in REQUIRED_DESIGN_FILES:
        if rel.endswith(".json") and (root / rel).exists():
            validate_json_file(root / rel)
            json_results[rel] = "PASS"
    return {
        "ok": not missing,
        "missing_files": missing,
        "json_results": json_results,
    }


def validate_handoff_packet(payload: dict[str, Any]) -> None:
    validate_required_keys(
        payload,
        [
            "packet_id",
            "token_address",
            "created_at",
            "missing_fields_summary",
            "requires_followup_fields",
            "evidence_language_only",
        ],
    )
    assert_no_forbidden_fields(payload)


def consume_schema_contract_runtime_adapters(registry: dict[str, Any]) -> dict[str, Any]:
    groups = registry.get("adapter_groups", {}) if isinstance(registry, dict) else {}
    adapters = groups.get("schema_contract_runtime_adapter", []) or []
    return {
        "status": "PASS" if adapters else "EMPTY",
        "consumer": "modules/source_wallet_bot/schema_validator.py",
        "schema_contract_adapters": len(adapters),
        "source_files": [x.get("source_file") for x in adapters if isinstance(x, dict)],
        "validation_role": "schema_contract_validation_input",
        "write_policy": "additive_validation_index_only",
    }


def validate_runtime_adapter_registry(registry: dict[str, Any]) -> dict[str, Any]:
    required_groups = [
        "legacy_path_map_runtime_adapter",
        "legacy_manifest_runtime_adapter",
        "wallet_data_passport_runtime_adapter",
        "schema_contract_runtime_adapter",
        "interface_inventory_runtime_adapter",
    ]
    groups = registry.get("adapter_groups", {}) if isinstance(registry, dict) else {}
    targets = registry.get("integration_targets", {}) if isinstance(registry, dict) else {}
    group_status = {name: "PASS" if groups.get(name) else "MISSING" for name in required_groups}
    target_status = {name: "PASS" if targets.get(name, {}).get("target") else "MISSING" for name in required_groups}
    present_groups = [name for name in required_groups if groups.get(name)]
    ok = bool(present_groups) and all(targets.get(name, {}).get("target") for name in present_groups)
    return {
        "ok": ok,
        "total_adapters": registry.get("total_adapters", 0),
        "required_groups_status": group_status,
        "integration_target_status": target_status,
    }
