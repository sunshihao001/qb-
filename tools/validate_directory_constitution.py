#!/usr/bin/env python3
"""SIKK directory constitution validator.

Scope: validates presence and JSON readability of the system directory constitution
and reports obvious route skeleton issues. It does not move/delete files.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_DIRS = [
    "docs",
    "modules",
    "tests",
    "data",
    "reports",
    "research_loop",
    "imports",
    "schemas/shared",
    "contracts/shared",
    "contracts/bot_handoff",
    "tools",
    "legacy_compat/manifests",
    "legacy_compat/path_maps",
    "legacy_compat/read_fallbacks",
    "research_loop/plans",
    "research_loop/checkpoints",
    "research_loop/acceptance",
    "research_loop/blockers",
    "research_loop/state",
    "research_loop/methodology/passports",
    "research_loop/methodology/rules",
    "research_loop/methodology/counter_evidence",
    "research_loop/methodology/stat_models",
    "research_loop/methodology/audit_rules",
    "research_loop/methodology/field_maps",
    "data/source_wallet_bot/live/_TEMPLATE_TOKEN/wallet_data/raw",
    "data/source_wallet_bot/live/_TEMPLATE_TOKEN/wallet_data/normalized",
    "data/source_wallet_bot/live/_TEMPLATE_TOKEN/wallet_data/summary",
    "data/source_wallet_bot/live/_TEMPLATE_TOKEN/structure_analysis/wallet_fact",
    "data/source_wallet_bot/live/_TEMPLATE_TOKEN/structure_analysis/intelligence",
    "data/source_wallet_bot/live/_TEMPLATE_TOKEN/structure_analysis/handoff",
    "data/source_wallet_bot/live/_TEMPLATE_TOKEN/structure_analysis/reports",
    "data/source_wallet_bot/live/_TEMPLATE_TOKEN/manifest",
    "data/intel_bot/live/_TEMPLATE_TOKEN/behavior_inference",
    "data/intel_bot/live/_TEMPLATE_TOKEN/counter_evidence",
    "data/intel_bot/live/_TEMPLATE_TOKEN/quant_scores",
    "data/intel_bot/live/_TEMPLATE_TOKEN/structure_conclusion",
    "data/intel_bot/live/_TEMPLATE_TOKEN/reports",
    "data/intel_bot/live/_TEMPLATE_TOKEN/manifest",
]

REQUIRED_FILES = [
    "AGENTS.md",
    "docs/system_directory_constitution.md",
    "docs/system_directory_routes.json",
    "docs/output_directory_governance.md",
]


def validate(root: Path) -> dict:
    result = {
        "root": str(root),
        "missing_dirs": [],
        "missing_files": [],
        "routes_json_ok": False,
        "routes_version": None,
        "policy_ok": False,
        "agents_mentions_constitution": False,
        "ok": False,
    }
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            result["missing_dirs"].append(rel)
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            result["missing_files"].append(rel)

    routes_path = root / "docs/system_directory_routes.json"
    if routes_path.exists():
        routes = json.loads(routes_path.read_text(encoding="utf-8"))
        result["routes_json_ok"] = True
        result["routes_version"] = routes.get("version")
        policy = routes.get("policy", {})
        result["policy_ok"] = all(
            policy.get(k) is True
            for k in [
                "future_outputs_must_use_constitution_routes",
                "require_asset_class_before_write",
                "no_trading",
                "no_private_key",
                "no_signing",
                "no_broadcast",
                "no_swap",
            ]
        ) and policy.get("delete_old_files") is False and policy.get("move_old_files") is False

    agents_path = root / "AGENTS.md"
    if agents_path.exists():
        text = agents_path.read_text(encoding="utf-8")
        result["agents_mentions_constitution"] = "system_directory_constitution.md" in text and "system_directory_routes.json" in text

    result["ok"] = not result["missing_dirs"] and not result["missing_files"] and result["routes_json_ok"] and result["policy_ok"] and result["agents_mentions_constitution"]
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="/root/sikk-gmgn")
    args = parser.parse_args()
    result = validate(Path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
