#!/usr/bin/env python3
"""Validate HER Harness route artifacts and schemas.

Usage:
  python tools/harness/check_routes.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
ROUTES_PATH = REPO_ROOT / "docs" / "harness" / "her_harness_routes.json"
TASK_SCHEMA_PATH = REPO_ROOT / "schemas" / "harness" / "task_ticket.schema.json"
FILE_MANIFEST_SCHEMA_PATH = REPO_ROOT / "schemas" / "harness" / "file_manifest.schema.json"
ACCEPTANCE_SCHEMA_PATH = REPO_ROOT / "schemas" / "harness" / "acceptance.schema.json"


class CheckError(RuntimeError):
    pass


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CheckError(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CheckError(f"invalid json in {path}: {exc}") from exc


def ensure(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def ensure_keys(obj: dict[str, Any], keys: Iterable[str], label: str) -> None:
    missing = [key for key in keys if key not in obj]
    ensure(not missing, f"{label} missing keys: {', '.join(missing)}")


def check_schema(path: Path, required_root_keys: Iterable[str], required_props: Iterable[str]) -> None:
    schema = load_json(path)
    ensure(isinstance(schema, dict), f"{path} must be a JSON object")
    ensure_keys(schema, required_root_keys, str(path))
    props = schema.get("properties")
    ensure(isinstance(props, dict), f"{path} properties must be an object")
    ensure_keys(props, required_props, f"{path} properties")


def check_routes() -> list[str]:
    routes = load_json(ROUTES_PATH)
    ensure(isinstance(routes, dict), "routes file must be a JSON object")

    ensure(routes.get("project_root") == str(REPO_ROOT), "project_root must equal repo root")
    ensure(routes.get("canonical_root") == str(REPO_ROOT), "canonical_root must equal repo root")

    ensure_keys(routes, ["version", "name", "project_root", "canonical_root", "paths", "policy", "task_ticket", "file_manifest", "acceptance", "default_paths"], "routes")
    ensure(isinstance(routes["paths"], dict), "routes.paths must be an object")
    ensure(isinstance(routes["policy"], dict), "routes.policy must be an object")
    ensure(isinstance(routes["task_ticket"], dict), "routes.task_ticket must be an object")
    ensure(isinstance(routes["file_manifest"], dict), "routes.file_manifest must be an object")
    ensure(isinstance(routes["acceptance"], dict), "routes.acceptance must be an object")
    ensure(isinstance(routes["default_paths"], dict), "routes.default_paths must be an object")

    expected_paths = {
        "routes": "docs/harness/her_harness_routes.json",
        "task_ticket_schema": "schemas/harness/task_ticket.schema.json",
        "file_manifest_schema": "schemas/harness/file_manifest.schema.json",
        "acceptance_schema": "schemas/harness/acceptance.schema.json",
        "route_checker": "tools/harness/check_routes.py",
    }
    for key, rel in expected_paths.items():
        ensure(routes["paths"].get(key) == rel, f"routes.paths.{key} must be {rel}")

    ensure(routes["policy"].get("canonical_root_only") is True, "policy.canonical_root_only must be true")
    ensure(routes["policy"].get("legacy_workspace_is_reference_only") is True, "policy.legacy_workspace_is_reference_only must be true")
    ensure(routes["policy"].get("copy_only_legacy_migration") is True, "policy.copy_only_legacy_migration must be true")
    ensure(routes["policy"].get("no_private_key") is True, "policy.no_private_key must be true")
    ensure(routes["policy"].get("no_signing") is True, "policy.no_signing must be true")
    ensure(routes["policy"].get("no_broadcast") is True, "policy.no_broadcast must be true")
    ensure(routes["policy"].get("no_swap") is True, "policy.no_swap must be true")
    ensure(routes["policy"].get("no_real_trading") is True, "policy.no_real_trading must be true")

    expected_task_fields = [
        "task_id",
        "title",
        "bot",
        "asset_type",
        "asset_id",
        "mode",
        "input_root",
        "output_root",
        "allowed_paths",
        "forbidden_paths",
        "required_outputs",
        "phase",
        "created_at",
    ]
    ensure(routes["task_ticket"].get("schema_ref") == "schemas/harness/task_ticket.schema.json", "task_ticket.schema_ref mismatch")
    ensure(routes["task_ticket"].get("required_fields") == expected_task_fields, "task_ticket.required_fields mismatch")

    expected_manifest_fields = [
        "manifest_id",
        "asset_type",
        "asset_id",
        "bot",
        "root",
        "files",
        "generated_at",
    ]
    ensure(routes["file_manifest"].get("schema_ref") == "schemas/harness/file_manifest.schema.json", "file_manifest.schema_ref mismatch")
    ensure(routes["file_manifest"].get("required_fields") == expected_manifest_fields, "file_manifest.required_fields mismatch")

    expected_acceptance_fields = ["task_id", "status", "checks", "summary", "generated_at"]
    ensure(routes["acceptance"].get("schema_ref") == "schemas/harness/acceptance.schema.json", "acceptance.schema_ref mismatch")
    ensure(routes["acceptance"].get("required_fields") == expected_acceptance_fields, "acceptance.required_fields mismatch")

    ensure(routes["default_paths"].get("source_wallet_bot_root") == "data/source_wallet_bot/{mode}/{asset_id}/", "default_paths.source_wallet_bot_root mismatch")
    ensure(routes["default_paths"].get("intel_bot_root") == "data/intel_bot/{mode}/{asset_id}/", "default_paths.intel_bot_root mismatch")
    ensure(routes["default_paths"].get("research_acceptance") == "research_loop/acceptance/{task_name}_acceptance.md", "default_paths.research_acceptance mismatch")
    ensure(routes["default_paths"].get("research_state") == "research_loop/state/{task_id}/", "default_paths.research_state mismatch")
    ensure(routes["default_paths"].get("legacy_manifest") == "legacy_compat/manifests/{manifest_name}.json", "default_paths.legacy_manifest mismatch")

    return [
        "routes ok",
        "policy ok",
        "task_ticket contract ok",
        "file_manifest contract ok",
        "acceptance contract ok",
    ]


def main() -> int:
    try:
        checks = check_routes()
        check_schema(
            TASK_SCHEMA_PATH,
            ["$schema", "$id", "title", "type", "additionalProperties", "required", "properties"],
            [
                "task_id",
                "title",
                "bot",
                "asset_type",
                "asset_id",
                "mode",
                "input_root",
                "output_root",
                "allowed_paths",
                "forbidden_paths",
                "required_outputs",
                "phase",
                "created_at",
            ],
        )
        check_schema(
            FILE_MANIFEST_SCHEMA_PATH,
            ["$schema", "$id", "title", "type", "additionalProperties", "required", "properties"],
            ["manifest_id", "asset_type", "asset_id", "bot", "root", "generated_at", "files"],
        )
        check_schema(
            ACCEPTANCE_SCHEMA_PATH,
            ["$schema", "$id", "title", "type", "additionalProperties", "required", "properties"],
            ["task_id", "status", "summary", "generated_at", "checks"],
        )
    except CheckError as exc:
        print(f"FAIL: {exc}")
        return 1

    for line in checks:
        print(f"PASS: {line}")
    print("PASS: all HER Harness route checks succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
