from __future__ import annotations

"""Phase 01 fact-store router for SIKK Source Wallet Bot.

This module is the runtime bridge between the Hermes skill
`sikk-phase01-data-fact-skill` and per-token fact artifacts under
`data/source_wallet_bot/<mode>/<token_address>/`.

It does not collect network data and does not infer trading decisions. It only
locates, indexes, and quality-checks existing Phase 01 fact artifacts so HER can
read the correct standard files instead of guessing paths from chat/history.
"""

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path("/root/sikk-gmgn")
ALLOWED_MODES = {"live", "live_test", "ad_hoc", "archive", "legacy"}

# Canonical files HER should prefer when producing token data analysis.
# `primary_rel` is the governed standard path when available.
# `fallback_rels` preserves compatibility with existing duplicated package roots.
PHASE01_FACT_ASSETS: dict[str, dict[str, Any]] = {
    "token_stage_summary": {
        "group": "market_fact",
        "required": False,
        "primary_rel": "wallet_data/normalized/gmgn_okx_raw_stage_outputs.json",
        "fallback_rels": ["structure_analysis/intelligence/stage_outputs.jsonl"],
        "description": "GMGN/OKX stage outputs, token quote/security/holder/trader overview.",
    },
    "raw_source_manifest": {
        "group": "manifest",
        "required": True,
        "primary_rel": "source_wallet_packet/manifest/wallet_data_guard_source_manifest.json",
        "fallback_rels": ["manifest/token_output_manifest.json", "source_wallet_packet/manifest/token_output_manifest.json"],
        "description": "Source provenance and token package manifest.",
    },
    "wallet_trade_normalized": {
        "group": "wallet_fact",
        "required": True,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/wallet_trade_normalized.json",
        "fallback_rels": ["wallet_data/normalized/wallet_trade_normalized.json"],
        "description": "Normalized wallet trade facts.",
    },
    "wallet_entity_profile_normalized": {
        "group": "wallet_fact",
        "required": True,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/wallet_entity_profile_normalized.json",
        "fallback_rels": ["wallet_data/normalized/wallet_entity_profile_normalized.json"],
        "description": "Normalized wallet profile/entity/tag facts.",
    },
    "gmgn_wallet_tags_normalized": {
        "group": "wallet_fact",
        "required": False,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/gmgn_wallet_tags_normalized.json",
        "fallback_rels": ["wallet_data/normalized/gmgn_wallet_tags_normalized.json"],
        "description": "Normalized GMGN tag hints; candidate evidence only.",
    },
    "token_transfer_normalized": {
        "group": "transfer_fact",
        "required": False,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/token_transfer_normalized.json",
        "fallback_rels": ["wallet_data/normalized/token_transfer_normalized.json"],
        "description": "Token transfer facts; separates active trades from transfers.",
    },
    "funding_flow_normalized": {
        "group": "funding_fact",
        "required": False,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/funding_flow_normalized.json",
        "fallback_rels": ["wallet_data/normalized/funding_flow_normalized.json"],
        "description": "Funding flow facts.",
    },
    "funding_source_normalized": {
        "group": "funding_fact",
        "required": False,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/funding_source_normalized.json",
        "fallback_rels": ["wallet_data/normalized/funding_source_normalized.json"],
        "description": "Funding source facts for candidate same-source evidence.",
    },
    "backflow_paths_normalized": {
        "group": "backflow_fact",
        "required": False,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/backflow_paths_normalized.json",
        "fallback_rels": ["wallet_data/normalized/backflow_paths_normalized.json"],
        "description": "Post-sell/profit backflow path facts.",
    },
    "wallet_snapshot_delta_source": {
        "group": "snapshot_delta_fact",
        "required": False,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/wallet_snapshot_delta_source.json",
        "fallback_rels": ["wallet_data/normalized/wallet_snapshot_delta_source.json"],
        "description": "Wallet snapshot delta facts.",
    },
    "holder_delta_normalized": {
        "group": "snapshot_delta_fact",
        "required": False,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/holder_delta_normalized.json",
        "fallback_rels": ["wallet_data/normalized/holder_delta_normalized.json"],
        "description": "Holder delta facts.",
    },
    "quote_security_normalized": {
        "group": "quote_security_fact",
        "required": False,
        "primary_rel": "source_wallet_packet/wallet_data/normalized/quote_security_normalized.json",
        "fallback_rels": ["wallet_data/normalized/quote_security_normalized.json"],
        "description": "Quote/security normalized context.",
    },
    "same_source_evidence_normalized": {
        "group": "same_source_evidence",
        "required": True,
        "primary_rel": "source_wallet_packet/structure_analysis/intelligence/same_source_evidence_normalized.json",
        "fallback_rels": ["structure_analysis/intelligence/same_source_evidence_normalized.json"],
        "description": "Candidate same-source evidence; not deterministic same-source claim.",
    },
    "wallet_intelligence_decision": {
        "group": "wallet_intelligence_evidence",
        "required": True,
        "primary_rel": "source_wallet_packet/structure_analysis/intelligence/wallet_intelligence_decision.json",
        "fallback_rels": ["structure_analysis/intelligence/wallet_intelligence_decision.json"],
        "description": "Wallet role candidates/evidence levels/risk levels; evidence-only.",
    },
    "bot2_handoff_packet": {
        "group": "handoff",
        "required": True,
        "primary_rel": "source_wallet_packet/structure_analysis/handoff/bot2_handoff_packet.json",
        "fallback_rels": ["structure_analysis/handoff/bot2_handoff_packet.json"],
        "description": "Phase01/Source Bot to Bot2 handoff packet with missing/restricted fields.",
    },
    "contamination_scan": {
        "group": "verification",
        "required": False,
        "primary_rel": "source_wallet_packet/verification/wallet_data_guard_contamination_scan.json",
        "fallback_rels": [],
        "description": "Anti-pollution / forbidden output scan evidence.",
    },
    "token_analysis_result_summary": {
        "group": "report",
        "required": False,
        "primary_rel": "token_analysis_result_summary.json",
        "fallback_rels": ["reports/token_analysis_result_summary.json"],
        "description": "Human-facing token analysis result; not an upstream fact source.",
        "fact_source": False,
    },
}

FORBIDDEN_OUTPUT_FIELDS = [
    "buy_signal",
    "sell_signal",
    "trade_allowed",
    "execute_now",
    "PAPER_READY",
    "real_execution",
    "swap",
    "signing",
    "broadcast",
]


@dataclass
class FactAssetStatus:
    asset_key: str
    group: str
    required: bool
    status: str
    selected_path: str | None
    selected_tier: str
    record_count: int | None = None
    bytes: int | None = None
    mtime_utc: str | None = None
    description: str = ""
    all_candidates: list[dict[str, Any]] = field(default_factory=list)
    fact_source: bool = True


@dataclass
class FactStoreIndex:
    artifact_type: str
    token_address: str
    mode: str
    token_root: str
    generated_at: str
    skill_binding: dict[str, Any]
    quality_status: str
    recommended_action: str
    missing_required_assets: list[str]
    missing_optional_assets: list[str]
    fact_assets: dict[str, dict[str, Any]]
    group_summary: dict[str, dict[str, int]]
    downstream_read_policy: dict[str, Any]
    forbidden_output_fields: list[str]
    index_path: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _load_json_light(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _record_count(path: Path) -> int | None:
    if path.suffix == ".jsonl":
        try:
            return sum(1 for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip())
        except Exception:
            return None
    if path.suffix != ".json":
        return None
    payload = _load_json_light(path)
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict):
        for key in ("record_count", "records_count", "count", "total"):
            value = payload.get(key)
            if isinstance(value, int):
                return value
        records = payload.get("records")
        if isinstance(records, list):
            return len(records)
        items = payload.get("items")
        if isinstance(items, list):
            return len(items)
    return None


def _file_meta(path: Path, root: Path) -> dict[str, Any]:
    stat = path.stat()
    return {
        "path": _rel(path, root),
        "exists": True,
        "bytes": stat.st_size,
        "mtime_utc": datetime.fromtimestamp(stat.st_mtime, timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    }


def resolve_token_root(token_address: str, *, mode: str = "live", root: Path = PROJECT_ROOT) -> Path:
    if mode not in ALLOWED_MODES:
        raise ValueError(f"unsupported mode={mode!r}; allowed={sorted(ALLOWED_MODES)}")
    return root / "data" / "source_wallet_bot" / mode / token_address


def _candidate_paths(token_root: Path, spec: dict[str, Any]) -> Iterable[tuple[str, Path]]:
    yield "primary", token_root / str(spec["primary_rel"])
    for rel in spec.get("fallback_rels", []) or []:
        yield "fallback", token_root / str(rel)


def resolve_fact_asset(token_root: Path, asset_key: str, spec: dict[str, Any], *, root: Path = PROJECT_ROOT) -> FactAssetStatus:
    candidates: list[dict[str, Any]] = []
    selected: tuple[str, Path] | None = None
    for tier, candidate in _candidate_paths(token_root, spec):
        item = {"tier": tier, "path": _rel(candidate, root), "exists": candidate.exists()}
        if candidate.exists():
            item.update(_file_meta(candidate, root))
            if selected is None:
                selected = (tier, candidate)
        candidates.append(item)

    if selected is None:
        return FactAssetStatus(
            asset_key=asset_key,
            group=str(spec["group"]),
            required=bool(spec.get("required", False)),
            status="missing_required" if spec.get("required", False) else "missing_optional",
            selected_path=None,
            selected_tier="missing",
            description=str(spec.get("description", "")),
            all_candidates=candidates,
            fact_source=bool(spec.get("fact_source", True)),
        )

    tier, path = selected
    meta = _file_meta(path, root)
    return FactAssetStatus(
        asset_key=asset_key,
        group=str(spec["group"]),
        required=bool(spec.get("required", False)),
        status="present",
        selected_path=meta["path"],
        selected_tier=tier,
        record_count=_record_count(path),
        bytes=meta["bytes"],
        mtime_utc=meta["mtime_utc"],
        description=str(spec.get("description", "")),
        all_candidates=candidates,
        fact_source=bool(spec.get("fact_source", True)),
    )


def build_fact_store_index(
    token_address: str,
    *,
    mode: str = "live",
    root: Path = PROJECT_ROOT,
    write: bool = True,
) -> FactStoreIndex:
    token_root = resolve_token_root(token_address, mode=mode, root=root)
    assets: dict[str, FactAssetStatus] = {
        key: resolve_fact_asset(token_root, key, spec, root=root)
        for key, spec in PHASE01_FACT_ASSETS.items()
    }
    missing_required = [key for key, value in assets.items() if value.status == "missing_required"]
    missing_optional = [key for key, value in assets.items() if value.status == "missing_optional"]

    if not token_root.exists():
        quality_status = "BLOCK"
        recommended_action = "run_source_wallet_bot_collection_or_check_token_root"
    elif missing_required:
        quality_status = "PAUSE"
        recommended_action = "complete_missing_required_phase01_fact_assets_before_analysis"
    elif missing_optional:
        quality_status = "PASS_WITH_WARNING"
        recommended_action = "analysis_allowed_with_missing_optional_fields_explicitly_reported"
    else:
        quality_status = "PASS"
        recommended_action = "analysis_allowed_read_standard_fact_assets"

    group_summary: dict[str, dict[str, int]] = {}
    for asset in assets.values():
        bucket = group_summary.setdefault(asset.group, {"present": 0, "missing_required": 0, "missing_optional": 0, "total": 0})
        bucket[asset.status] = bucket.get(asset.status, 0) + 1
        bucket["total"] += 1

    index = FactStoreIndex(
        artifact_type="phase01_fact_store_index",
        token_address=token_address,
        mode=mode,
        token_root=_rel(token_root, root),
        generated_at=_now(),
        skill_binding={
            "skill_name": "sikk-phase01-data-fact-skill",
            "skill_role": "governs allowed reads, quality gates, handoff rules, and anti-pollution boundaries",
            "runtime_code_root": "modules/source_wallet_bot",
            "fact_store_root": f"data/source_wallet_bot/{mode}/{token_address}",
        },
        quality_status=quality_status,
        recommended_action=recommended_action,
        missing_required_assets=missing_required,
        missing_optional_assets=missing_optional,
        fact_assets={key: asdict(value) for key, value in assets.items()},
        group_summary=group_summary,
        downstream_read_policy={
            "phase01_analysis_should_read": [
                "present assets with fact_source=true",
                "bot2_handoff_packet",
                "raw_source_manifest/token manifest",
                "missing_required_assets and missing_optional_assets",
            ],
            "reports_are_human_facing_not_upstream_fact_source": True,
            "forbidden_bypass": [
                "Telegram/chat interpretation as fact source",
                "paper runner/state machine outputs as fact source",
                "old reports as live facts unless imported under legacy read-only mode",
            ],
            "missing_behavior": "explicit missing/restricted/downgrade; do not fabricate fields",
        },
        forbidden_output_fields=FORBIDDEN_OUTPUT_FIELDS,
    )

    if write:
        manifest_dir = token_root / "manifest"
        manifest_dir.mkdir(parents=True, exist_ok=True)
        index_path = manifest_dir / "phase01_fact_store_index.json"
        index.index_path = _rel(index_path, root)
        index_path.write_text(json.dumps(index.to_dict(), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")

    return index


def cmd_index(args: argparse.Namespace) -> int:
    index = build_fact_store_index(args.token, mode=args.mode, root=Path(args.root), write=not args.no_write)
    print(json.dumps(index.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if index.quality_status in {"PASS", "PASS_WITH_WARNING"} else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Phase01 fact-store router for Source Wallet Bot")
    parser.add_argument("--token", required=True, help="Token address")
    parser.add_argument("--mode", default="live", choices=sorted(ALLOWED_MODES))
    parser.add_argument("--root", default=str(PROJECT_ROOT))
    parser.add_argument("--no-write", action="store_true", help="Print index without writing manifest/phase01_fact_store_index.json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return cmd_index(args)


if __name__ == "__main__":
    raise SystemExit(main())
