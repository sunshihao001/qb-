#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WALLET_DATA_FILES = {
    "wallet_trade_normalized.json",
    "wallet_entity_profile_normalized.json",
    "same_source_evidence_normalized.json",
    "wallet_intelligence_decision.json",
    "wallet_structure_normalized.json",
    "chip_distribution_summary.json",
    "same_source_groups.json",
    "fund_flow_edges.csv",
    "address_history.json",
    "wallet_fact_report.md",
    "wallet_fact_package_manifest.json",
}

STRUCTURE_ANALYSIS_FILES = {
    "early_wallet_raw.csv",
    "wallet_classification.csv",
    "candidate_groups.csv",
    "gmgn_note_table.csv",
    "wallet_structure_decision.json",
    "wallet_structure_summary.md",
}

SAFETY_BOUNDARIES = [
    "directory_governance_only",
    "no_wallet_logic_rewrite",
    "no_structure_logic_rewrite",
    "no_delete_old_files",
    "no_move_old_files",
    "copy_only",
    "legacy_paths_preserved",
    "no_trading",
    "no_state_machine",
    "no_paper_runner",
    "no_private_key_read",
    "no_signing",
    "no_broadcast",
    "no_swap",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_file(old_path: Path, new_path: Path, root: Path, token_address: str, category: str, dry_run: bool) -> dict[str, Any]:
    size = old_path.stat().st_size
    digest = sha256_file(old_path)
    if not dry_run:
        new_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(old_path, new_path)
    return {
        "token_address": token_address,
        "category": category,
        "old_path": str(old_path.relative_to(root)),
        "new_path": str(new_path.relative_to(root)),
        "action": "would_copy" if dry_run else "copied",
        "sha256": digest,
        "size_bytes": size,
    }


def token_dirs_from_root_scattered(output_root: Path) -> list[Path]:
    dirs: list[Path] = []
    for child in sorted(output_root.iterdir() if output_root.exists() else []):
        if not child.is_dir():
            continue
        names = {p.name for p in child.iterdir() if p.is_file()}
        if names & (WALLET_DATA_FILES | STRUCTURE_ANALYSIS_FILES):
            dirs.append(child)
    return dirs


def token_dirs_from_intel_structure(output_root: Path) -> list[Path]:
    base = output_root / "intel-bot" / "logs" / "wallet_structure"
    if not base.exists():
        return []
    return [p for p in sorted(base.iterdir()) if p.is_dir()]


def govern(output_root: Path, *, dry_run: bool = False) -> dict[str, Any]:
    output_root = output_root.resolve()
    generated_at = now_utc()
    mappings: list[dict[str, Any]] = []
    scanned_dirs: list[str] = []

    for token_dir in token_dirs_from_root_scattered(output_root):
        token = token_dir.name
        scanned_dirs.append(str(token_dir.relative_to(output_root)))
        for old_path in sorted(token_dir.iterdir()):
            if not old_path.is_file():
                continue
            if old_path.name in WALLET_DATA_FILES:
                new_path = token_dir / "wallet_data" / old_path.name
                mappings.append(copy_file(old_path, new_path, output_root, token, "wallet_data", dry_run))
            elif old_path.name in STRUCTURE_ANALYSIS_FILES:
                new_path = token_dir / "structure_analysis" / old_path.name
                mappings.append(copy_file(old_path, new_path, output_root, token, "structure_analysis", dry_run))

        legacy_wallet_fact = token_dir / "wallet_fact"
        if legacy_wallet_fact.exists() and legacy_wallet_fact.is_dir():
            for old_path in sorted(legacy_wallet_fact.rglob("*")):
                if old_path.is_file():
                    new_path = token_dir / "wallet_data" / old_path.relative_to(legacy_wallet_fact)
                    mappings.append(copy_file(old_path, new_path, output_root, token, "wallet_data", dry_run))

    for token_dir in token_dirs_from_intel_structure(output_root):
        token = token_dir.name
        scanned_dirs.append(str(token_dir.relative_to(output_root)))
        for old_path in sorted(token_dir.iterdir()):
            if old_path.is_file() and old_path.name in STRUCTURE_ANALYSIS_FILES:
                new_path = token_dir / "structure_analysis" / old_path.name
                mappings.append(copy_file(old_path, new_path, output_root, token, "structure_analysis", dry_run))
        snapshots = token_dir / "snapshots"
        if snapshots.exists():
            for old_path in sorted(snapshots.rglob("*.json")):
                if old_path.is_file():
                    new_path = token_dir / "structure_analysis" / "snapshots" / old_path.relative_to(snapshots)
                    mappings.append(copy_file(old_path, new_path, output_root, token, "structure_analysis", dry_run))

    manifest = {
        "task_name": "输出目录治理",
        "generated_at": generated_at,
        "mode": "dry_run" if dry_run else "copy_only",
        "output_root": str(output_root),
        "safety_boundaries": SAFETY_BOUNDARIES,
        "new_directory_templates": {
            "wallet_data": "<token_dir>/wallet_data/",
            "structure_analysis": "<token_dir>/structure_analysis/",
        },
        "scanned_token_dirs": scanned_dirs,
        "mapping_count": len(mappings),
        "mappings": mappings,
        "legacy_compatibility": {
            "old_paths_preserved": True,
            "old_paths_deleted": False,
            "old_paths_moved": False,
            "future_output_policy": "new outputs should write wallet facts to wallet_data/ and structure results to structure_analysis/; legacy readers may fallback to old paths",
        },
    }
    if not dry_run:
        manifest_path = output_root / "directory_governance_manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description="SIKK 输出目录治理：只复制旧输出到 wallet_data/ 和 structure_analysis/，保留旧路径兼容。")
    parser.add_argument("--output-root", default="data/gmgn_candidates_live_run")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest = govern(Path(args.output_root), dry_run=args.dry_run)
    print(json.dumps({
        "task_name": manifest["task_name"],
        "mode": manifest["mode"],
        "mapping_count": manifest["mapping_count"],
        "manifest_path": None if args.dry_run else str(Path(args.output_root) / "directory_governance_manifest.json"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
