from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path("/root/sikk-gmgn")

READ_PRIORITY_TIERS = [
    "new_standard_entry",
    "token_index",
    "data_passport",
    "field_dictionary",
    "legacy_path_mapping",
    "legacy_readonly_fallback",
    "missing",
]

# Canonical asset routes for Source Wallet Bot token packages. Keep this in sync
# with docs/system_directory_routes.json and directory_governance.py.
SOURCE_WALLET_ASSET_ROUTES: dict[str, str] = {
    "gmgn_wallet_rows_raw.json": "wallet_data/raw/gmgn_wallet_rows_raw.json",
    "gmgn_wallet_trade_input.json": "wallet_data/raw/gmgn_wallet_trade_input.json",
    "gmgn_wallet_profile_input.json": "wallet_data/raw/gmgn_wallet_profile_input.json",
    "wallet_trade_normalized.json": "wallet_data/normalized/wallet_trade_normalized.json",
    "wallet_entity_profile_normalized.json": "wallet_data/normalized/wallet_entity_profile_normalized.json",
    "token_transfer_normalized.json": "wallet_data/normalized/token_transfer_normalized.json",
    "funding_flow_normalized.json": "wallet_data/normalized/funding_flow_normalized.json",
    "funding_source_normalized.json": "wallet_data/normalized/funding_source_normalized.json",
    "backflow_paths_normalized.json": "wallet_data/normalized/backflow_paths_normalized.json",
    "same_source_evidence_normalized.json": "structure_analysis/intelligence/same_source_evidence_normalized.json",
    "wallet_intelligence_decision.json": "structure_analysis/intelligence/wallet_intelligence_decision.json",
    "bot2_handoff_packet.json": "structure_analysis/handoff/bot2_handoff_packet.json",
    "wallet_structure_normalized.json": "structure_analysis/wallet_fact/wallet_structure_normalized.json",
    "chip_distribution_summary.json": "structure_analysis/wallet_fact/chip_distribution_summary.json",
    "same_source_groups.json": "structure_analysis/wallet_fact/same_source_groups.json",
    "fund_flow_edges.csv": "structure_analysis/wallet_fact/fund_flow_edges.csv",
    "address_history.json": "structure_analysis/wallet_fact/address_history.json",
    "wallet_fact_package_manifest.json": "structure_analysis/wallet_fact/wallet_fact_package_manifest.json",
    "wallet_fact_report.md": "structure_analysis/reports/wallet_fact_report.md",
    "token_output_manifest.json": "manifest/token_output_manifest.json",
    "directory_layout.md": "manifest/directory_layout.md",
}

PASSPORT_FILENAMES = [
    "token_output_manifest.json",
    "copy_manifest_v7.json",
    "directory_layout.md",
    "token_output_manifest.md",
]

FIELD_DICTIONARY_PATHS = [
    "modules/source_wallet_bot/field_dictionary.csv",
    "modules/source_wallet_bot/gmgn_to_sikk_field_mapping.csv",
    "modules/source_wallet_bot/wallet_trade_contract.md",
    "modules/source_wallet_bot/wallet_intelligence_contracts.md",
    "modules/source_wallet_bot/bot2_handoff_contract.md",
    "modules/source_wallet_bot/quantitative_structure_field_addendum.md",
    "modules/source_wallet_bot/wallet_intel_behavior_handoff_addendum.md",
]

LEGACY_MAPPING_PATHS = [
    "legacy_compat/path_maps/wallet_data_token_index_v1.json",
    "legacy_compat/path_maps/legacy_to_new_semantic_mapping_v6.json",
    "legacy_compat/path_maps/wallet_data_old_to_standard_map_v1.json",
]

LEGACY_READONLY_ROOTS = [
    "data/source_wallet_bot/live",
    "data/source_wallet_bot/ad_hoc",
    "data/gmgn_candidates_live_run",
]


@dataclass
class ResolvedWalletPath:
    asset_name: str
    token_address: str | None
    resolved_path: str | None = None
    source_tier: str = "missing"
    fallback_chain: list[dict[str, Any]] = field(default_factory=list)
    missing_reason: str = ""
    is_standard: bool = False
    is_legacy_fallback: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _extract_records_from_manifest(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, dict):
        for key in ("items", "selected_copy", "file_mappings", "path_mappings", "records"):
            value = payload.get(key)
            if isinstance(value, list):
                return [x for x in value if isinstance(x, dict)]
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    return []


def resolve_standard_path(
    asset_name: str,
    token_address: str,
    *,
    mode: str = "legacy",
    root: Path = PROJECT_ROOT,
) -> ResolvedWalletPath:
    chain: list[dict[str, Any]] = []
    rel_route = SOURCE_WALLET_ASSET_ROUTES.get(asset_name, asset_name)
    candidates = [root / "data" / "source_wallet_bot" / mode / token_address / rel_route]
    # Some copy-only legacy packages used hash-prefixed filenames to avoid collisions.
    parent = candidates[0].parent
    if parent.is_dir():
        candidates.extend(sorted(parent.glob(f"*__{asset_name}")))
        candidates.extend(sorted(parent.glob(asset_name)))
    for candidate in candidates:
        chain.append({"tier": "new_standard_entry", "path": _rel(candidate, root), "exists": candidate.exists()})
        if candidate.exists():
            return ResolvedWalletPath(
                asset_name=asset_name,
                token_address=token_address,
                resolved_path=_rel(candidate, root),
                source_tier="new_standard_entry",
                fallback_chain=chain,
                is_standard=True,
            )
    return ResolvedWalletPath(
        asset_name=asset_name,
        token_address=token_address,
        fallback_chain=chain,
        missing_reason="new_standard_entry_missing",
    )


def resolve_token_index(token_address: str, *, root: Path = PROJECT_ROOT) -> ResolvedWalletPath:
    chain: list[dict[str, Any]] = []
    for relp in LEGACY_MAPPING_PATHS:
        path = root / relp
        exists = path.exists()
        chain.append({"tier": "token_index", "path": relp, "exists": exists})
        if not exists:
            continue
        payload = _load_json(path)
        text_hit = token_address in path.read_text(encoding="utf-8", errors="ignore")
        if text_hit:
            return ResolvedWalletPath(
                asset_name="token_index",
                token_address=token_address,
                resolved_path=relp,
                source_tier="token_index",
                fallback_chain=chain,
                is_standard=False,
            )
    return ResolvedWalletPath(asset_name="token_index", token_address=token_address, fallback_chain=chain, missing_reason="token_index_missing")


def resolve_passport(token_address: str, *, mode: str = "legacy", root: Path = PROJECT_ROOT) -> ResolvedWalletPath:
    chain: list[dict[str, Any]] = []
    manifest_dir = root / "data" / "source_wallet_bot" / mode / token_address / "manifest"
    for name in PASSPORT_FILENAMES:
        path = manifest_dir / name
        chain.append({"tier": "data_passport", "path": _rel(path, root), "exists": path.exists()})
        if path.exists():
            return ResolvedWalletPath(
                asset_name=name,
                token_address=token_address,
                resolved_path=_rel(path, root),
                source_tier="data_passport",
                fallback_chain=chain,
                is_standard=True,
            )
    return ResolvedWalletPath(asset_name="data_passport", token_address=token_address, fallback_chain=chain, missing_reason="data_passport_missing")


def resolve_field_dict(field_or_asset: str = "", *, root: Path = PROJECT_ROOT) -> ResolvedWalletPath:
    chain: list[dict[str, Any]] = []
    needles = {field_or_asset, Path(field_or_asset).stem} if field_or_asset else set()
    for relp in FIELD_DICTIONARY_PATHS:
        path = root / relp
        exists = path.exists()
        hit = False
        if exists and needles:
            text = path.read_text(encoding="utf-8", errors="ignore")
            hit = any(n and n in text for n in needles)
        chain.append({"tier": "field_dictionary", "path": relp, "exists": exists, "hit": hit})
        if exists and (not needles or hit):
            return ResolvedWalletPath(
                asset_name=field_or_asset or "field_dictionary",
                token_address=None,
                resolved_path=relp,
                source_tier="field_dictionary",
                fallback_chain=chain,
            )
    return ResolvedWalletPath(asset_name=field_or_asset or "field_dictionary", token_address=None, fallback_chain=chain, missing_reason="field_dictionary_missing")


def resolve_legacy_mapping(asset_name: str, token_address: str | None, *, root: Path = PROJECT_ROOT) -> ResolvedWalletPath:
    chain: list[dict[str, Any]] = []
    for relp in LEGACY_MAPPING_PATHS:
        path = root / relp
        exists = path.exists()
        chain.append({"tier": "legacy_path_mapping", "path": relp, "exists": exists})
        if not exists:
            continue
        payload = _load_json(path)
        for rec in _extract_records_from_manifest(payload):
            old_path = str(rec.get("old_path") or rec.get("old_dir") or "")
            new_path = str(rec.get("new_path") or rec.get("copy_target") or rec.get("new_standard_read_position") or "")
            rec_token = rec.get("token_address")
            if asset_name not in old_path and asset_name not in new_path:
                continue
            if token_address and rec_token not in (None, token_address) and token_address not in old_path and token_address not in new_path:
                continue
            chosen = new_path or old_path
            return ResolvedWalletPath(
                asset_name=asset_name,
                token_address=token_address,
                resolved_path=chosen,
                source_tier="legacy_path_mapping",
                fallback_chain=chain,
                is_standard=bool(new_path),
                is_legacy_fallback=not bool(new_path),
            )
    return ResolvedWalletPath(asset_name=asset_name, token_address=token_address, fallback_chain=chain, missing_reason="legacy_mapping_missing")


def resolve_legacy_fallback(asset_name: str, token_address: str | None, *, root: Path = PROJECT_ROOT) -> ResolvedWalletPath:
    chain: list[dict[str, Any]] = []
    if not token_address:
        return ResolvedWalletPath(asset_name=asset_name, token_address=token_address, missing_reason="token_required_for_legacy_fallback")
    for relroot in LEGACY_READONLY_ROOTS:
        base = root / relroot
        exists = base.exists()
        chain.append({"tier": "legacy_readonly_fallback", "path": relroot, "exists": exists, "scope": "mapped_readonly"})
        if not exists:
            continue
        # Scoped token search only; never full-repo blind search.
        candidates = list(base.glob(f"**/{token_address}/**/{asset_name}"))[:20]
        candidates.extend(list(base.glob(f"**/{token_address}/{asset_name}"))[:20])
        for candidate in candidates:
            if candidate.exists():
                return ResolvedWalletPath(
                    asset_name=asset_name,
                    token_address=token_address,
                    resolved_path=_rel(candidate, root),
                    source_tier="legacy_readonly_fallback",
                    fallback_chain=chain,
                    is_legacy_fallback=True,
                )
    return ResolvedWalletPath(asset_name=asset_name, token_address=token_address, fallback_chain=chain, missing_reason="legacy_readonly_fallback_missing")


def resolve_wallet_data_path(
    asset_name: str,
    token_address: str,
    *,
    mode: str = "legacy",
    root: Path = PROJECT_ROOT,
    allow_legacy_fallback: bool = True,
) -> ResolvedWalletPath:
    """Resolve wallet data with the enforced Hermes six-layer priority.

    Priority:
    1. new_standard_entry
    2. token_index
    3. data_passport
    4. field_dictionary
    5. legacy_path_mapping
    6. legacy_readonly_fallback
    7. missing
    """
    full_chain: list[dict[str, Any]] = []

    standard = resolve_standard_path(asset_name, token_address, mode=mode, root=root)
    full_chain.extend(standard.fallback_chain)
    if standard.resolved_path:
        standard.fallback_chain = full_chain
        return standard

    token_index = resolve_token_index(token_address, root=root)
    full_chain.extend(token_index.fallback_chain)

    passport = resolve_passport(token_address, mode=mode, root=root)
    full_chain.extend(passport.fallback_chain)

    field_dict = resolve_field_dict(asset_name, root=root)
    full_chain.extend(field_dict.fallback_chain)

    mapping = resolve_legacy_mapping(asset_name, token_address, root=root)
    full_chain.extend(mapping.fallback_chain)
    if mapping.resolved_path:
        candidate = root / mapping.resolved_path
        if candidate.exists():
            mapping.fallback_chain = full_chain
            return mapping

    if allow_legacy_fallback:
        legacy = resolve_legacy_fallback(asset_name, token_address, root=root)
        full_chain.extend(legacy.fallback_chain)
        if legacy.resolved_path:
            legacy.fallback_chain = full_chain
            return legacy

    return ResolvedWalletPath(
        asset_name=asset_name,
        token_address=token_address,
        source_tier="missing",
        fallback_chain=full_chain,
        missing_reason="not_found_after_standard_index_passport_field_dict_mapping_legacy_readonly",
    )


def consume_runtime_adapter_registry(registry: dict[str, Any]) -> dict[str, Any]:
    """Consume runtime adapter registry entries relevant to controlled path resolution.

    Additive/read-only: converts registry groups into resolver-readable counts and
    source file lists without mutating legacy path maps.
    """
    groups = registry.get("adapter_groups", {}) if isinstance(registry, dict) else {}
    path_maps = groups.get("legacy_path_map_runtime_adapter", []) or []
    manifests = groups.get("legacy_manifest_runtime_adapter", []) or []
    return {
        "status": "PASS" if path_maps or manifests else "EMPTY",
        "consumer": "modules/source_wallet_bot/path_resolver.py",
        "legacy_path_map_adapters": len(path_maps),
        "legacy_manifest_adapters": len(manifests),
        "source_files": [x.get("source_file") for x in path_maps + manifests if isinstance(x, dict)],
        "read_policy": "controlled_read_resolver_input",
        "write_policy": "additive_index_only",
    }


def load_records_with_priority(
    asset_name: str,
    token_address: str,
    *,
    mode: str = "legacy",
    root: Path = PROJECT_ROOT,
    allow_legacy_fallback: bool = True,
) -> tuple[list[dict[str, Any]], ResolvedWalletPath]:
    result = resolve_wallet_data_path(asset_name, token_address, mode=mode, root=root, allow_legacy_fallback=allow_legacy_fallback)
    if not result.resolved_path:
        return [], result
    path = root / result.resolved_path
    payload = _load_json(path)
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)], result
    if isinstance(payload, dict):
        records = payload.get("records")
        if isinstance(records, list):
            return [x for x in records if isinstance(x, dict)], result
        return [payload], result
    return [], result
