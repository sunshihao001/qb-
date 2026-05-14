from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WALLET_DATA_RAW = {
    "gmgn_wallet_rows_raw.json": "wallet_data/raw/gmgn_wallet_rows_raw.json",
    "gmgn_wallet_trade_input.json": "wallet_data/raw/gmgn_wallet_trade_input.json",
    "gmgn_wallet_profile_input.json": "wallet_data/raw/gmgn_wallet_profile_input.json",
}

WALLET_DATA_NORMALIZED = {
    "wallet_trade_normalized.json": "wallet_data/normalized/wallet_trade_normalized.json",
    "wallet_entity_profile_normalized.json": "wallet_data/normalized/wallet_entity_profile_normalized.json",
    "summary_overview.json": "wallet_data/summary/summary_overview.json",
    "summary_overview.md": "wallet_data/summary/summary_overview.md",
}

STRUCTURE_INTELLIGENCE = {
    "same_source_evidence_normalized.json": "structure_analysis/intelligence/same_source_evidence_normalized.json",
    "wallet_intelligence_decision.json": "structure_analysis/intelligence/wallet_intelligence_decision.json",
    "bot2_handoff_packet.json": "structure_analysis/handoff/bot2_handoff_packet.json",
}

WALLET_FACT_FILES = {
    "wallet_fact/wallet_structure_normalized.json": "structure_analysis/wallet_fact/wallet_structure_normalized.json",
    "wallet_fact/chip_distribution_summary.json": "structure_analysis/wallet_fact/chip_distribution_summary.json",
    "wallet_fact/same_source_groups.json": "structure_analysis/wallet_fact/same_source_groups.json",
    "wallet_fact/fund_flow_edges.csv": "structure_analysis/wallet_fact/fund_flow_edges.csv",
    "wallet_fact/address_history.json": "structure_analysis/wallet_fact/address_history.json",
    "wallet_fact/wallet_fact_report.md": "structure_analysis/reports/wallet_fact_report.md",
    "wallet_fact/wallet_fact_package_manifest.json": "structure_analysis/wallet_fact/wallet_fact_package_manifest.json",
}

PLACEHOLDER_NORMALIZED = {
    "token_transfer_normalized.json": "wallet_data/normalized/token_transfer_normalized.json",
    "token_source_classification_base.json": "wallet_data/normalized/token_source_classification_base.json",
    "funding_flow_normalized.json": "wallet_data/normalized/funding_flow_normalized.json",
    "funding_source_normalized.json": "wallet_data/normalized/funding_source_normalized.json",
    "backflow_paths_normalized.json": "wallet_data/normalized/backflow_paths_normalized.json",
    "gmgn_wallet_tags_normalized.json": "wallet_data/normalized/gmgn_wallet_tags_normalized.json",
    "wallet_snapshot_delta_source.json": "wallet_data/normalized/wallet_snapshot_delta_source.json",
    "holder_delta_normalized.json": "wallet_data/normalized/holder_delta_normalized.json",
    "quote_security_normalized.json": "wallet_data/normalized/quote_security_normalized.json",
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _copy(src: Path, dst: Path) -> dict[str, Any]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.resolve() == dst.resolve():
        return {
            "old_path": str(src),
            "new_path": str(dst),
            "action": "kept_standard",
            "status": "ok",
            "bytes": dst.stat().st_size,
        }
    shutil.copy2(src, dst)
    return {
        "old_path": str(src),
        "new_path": str(dst),
        "action": "copied",
        "status": "ok",
        "bytes": dst.stat().st_size,
    }


def _first_existing_source(root: Path, old_rel: str, new_rel: str) -> Path | None:
    standard = root / new_rel
    if standard.exists():
        return standard
    legacy = root / old_rel
    if legacy.exists():
        return legacy
    return None


def _write_placeholder(token_address: str, dst: Path, class_name: str) -> dict[str, Any]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "token_address": token_address,
        "record_count": 0,
        "records": [],
        "status": "placeholder_contract_only",
        "missing_policy": "字段缺失 / 需要链上补查",
        "class_name": class_name,
        "source_level": "missing",
    }
    dst.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "old_path": "missing",
        "new_path": str(dst),
        "action": "created_placeholder",
        "status": "ok",
        "bytes": dst.stat().st_size,
    }


def apply_directory_governance(token_address: str, token_dir: str | Path) -> dict[str, str]:
    """Copy current token outputs into governed wallet_data/structure_analysis layout.

    This function never deletes or moves old files. It only copies existing files and
    creates missing contract placeholders under the new layout.
    """

    root = Path(token_dir)
    root.mkdir(parents=True, exist_ok=True)
    mappings: list[dict[str, Any]] = []
    missing_sources: list[str] = []

    mapping_specs = {}
    mapping_specs.update(WALLET_DATA_RAW)
    mapping_specs.update(WALLET_DATA_NORMALIZED)
    mapping_specs.update(STRUCTURE_INTELLIGENCE)
    mapping_specs.update(WALLET_FACT_FILES)

    for old_rel, new_rel in mapping_specs.items():
        src = _first_existing_source(root, old_rel, new_rel)
        dst = root / new_rel
        if src is not None:
            mappings.append(_copy(src, dst))
        else:
            missing_sources.append(old_rel)
            mappings.append({
                "old_path": str(root / old_rel),
                "new_path": str(dst),
                "action": "skipped_missing_source",
                "status": "missing",
            })

    for placeholder_name, new_rel in PLACEHOLDER_NORMALIZED.items():
        dst = root / new_rel
        if not dst.exists():
            mappings.append(_write_placeholder(token_address, dst, placeholder_name))

    layout_md = _build_layout_md(token_address, root, mappings, missing_sources)
    layout_path = root / "manifest" / "directory_layout.md"
    layout_path.parent.mkdir(parents=True, exist_ok=True)
    layout_path.write_text(layout_md, encoding="utf-8")

    manifest = {
        "token_address": token_address,
        "generated_at": _now(),
        "task_name": "输出目录治理",
        "root_dir": str(root),
        "target_layout": {
            "wallet_data": {
                "raw": "wallet raw/API/input data",
                "normalized": "wallet fact normalized data",
                "summary": "wallet data summaries",
            },
            "structure_analysis": {
                "wallet_fact": "legacy-style wallet_fact aggregate outputs",
                "intelligence": "same-source and role candidate evidence",
                "handoff": "Bot2/Intel Bot handoff packet",
                "reports": "human-readable structure reports",
            },
            "manifest": "path mapping and layout docs",
        },
        "policy": {
            "directory_governance_only": True,
            "rewrite_wallet_logic": False,
            "rewrite_structure_logic": False,
            "delete_old_files": False,
            "move_old_files": False,
            "copy_or_reoutput_only": True,
            "keep_old_path_compatibility": True,
            "standard_layout_as_primary_write": True,
            "legacy_root_as_primary_write": False,
            "future_outputs_must_use_new_layout": True,
            "no_trading": True,
            "no_state_machine": True,
            "no_paper_runner": True,
            "no_private_key": True,
            "no_signing": True,
            "no_broadcast": True,
            "no_swap": True,
        },
        "path_mappings": mappings,
        "missing_sources": missing_sources,
        "primary_write_layout": "standard_source_wallet_token_layout",
    }
    manifest_path = root / "manifest" / "token_output_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "manifest": str(manifest_path),
        "layout": str(layout_path),
        "wallet_data_dir": str(root / "wallet_data"),
        "structure_analysis_dir": str(root / "structure_analysis"),
        "primary_write_layout": "standard_source_wallet_token_layout",
    }


def _build_layout_md(token_address: str, root: Path, mappings: list[dict[str, Any]], missing_sources: list[str]) -> str:
    lines = [
        "# Source Wallet Bot Directory Layout",
        "",
        f"token_address: `{token_address}`",
        f"root_dir: `{root}`",
        "",
        "## Target layout",
        "",
        "```text",
        "<token>/",
        "├── wallet_data/",
        "│   ├── raw/",
        "│   ├── normalized/",
        "│   └── summary/",
        "├── structure_analysis/",
        "│   ├── wallet_fact/",
        "│   ├── intelligence/",
        "│   ├── handoff/",
        "│   └── reports/",
        "└── manifest/",
        "```",
        "",
        "## Policy",
        "",
        "- 只做目录治理。",
        "- 不重写钱包判断逻辑。",
        "- 不重写结构分析逻辑。",
        "- 不删除旧文件。",
        "- 不移动旧文件。",
        "- 只复制 / 重新输出到新目录。",
        "- 保留旧路径兼容。",
        "- 后续新输出必须写入新目录。",
        "- 不接交易 / 状态机 / paper runner。",
        "- 不读取私钥 / 不签名 / 不广播 / 不 swap。",
        "",
        "## Mapping summary",
        "",
    ]
    copied = sum(1 for m in mappings if m.get("action") == "copied")
    placeholders = sum(1 for m in mappings if m.get("action") == "created_placeholder")
    skipped = sum(1 for m in mappings if m.get("status") == "missing")
    lines.extend([
        f"- copied: {copied}",
        f"- created_placeholder: {placeholders}",
        f"- skipped_missing_source: {skipped}",
        "",
        "## Missing sources",
    ])
    if missing_sources:
        for item in missing_sources:
            lines.append(f"- {item}")
    else:
        lines.append("- none")
    return "\n".join(lines) + "\n"
