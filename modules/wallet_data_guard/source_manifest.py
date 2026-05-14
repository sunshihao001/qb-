from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from .contracts import SemanticLayer


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _layer_value(layer: SemanticLayer | str) -> str:
    return layer.value if isinstance(layer, SemanticLayer) else str(layer)


def build_source_manifest(
    *,
    source_id: str,
    source_type: str,
    token_address: str,
    raw_path: str | Path,
    normalized_path: str | Path | None = None,
    allowed_layers: Sequence[SemanticLayer | str] | None = None,
    collected_at: str | None = None,
    collector: str | None = None,
    schema_version: str = "v1",
    read_mode: str = "readonly",
    confidence: str = "raw",
    contains_inference: bool = False,
    contains_handoff: bool = False,
) -> dict[str, Any]:
    allowed = [_layer_value(layer) for layer in (allowed_layers or [SemanticLayer.RAW])]
    all_layers = [layer.value for layer in SemanticLayer]
    blocked = [layer for layer in all_layers if layer not in set(allowed)]
    return {
        "source_id": source_id,
        "source_type": source_type,
        "token_address": token_address,
        "collected_at": collected_at or _utc_now(),
        "collector": collector or source_type,
        "raw_path": str(raw_path),
        "normalized_path": str(normalized_path) if normalized_path else None,
        "schema_version": schema_version,
        "read_mode": read_mode,
        "confidence": confidence,
        "contains_inference": contains_inference,
        "contains_handoff": contains_handoff,
        "allowed_layers": allowed,
        "blocked_layers": blocked,
    }


def consume_passport_runtime_adapters(registry: Mapping[str, Any]) -> dict[str, Any]:
    groups = registry.get("adapter_groups", {}) if isinstance(registry, Mapping) else {}
    adapters = groups.get("wallet_data_passport_runtime_adapter", []) or []
    return {
        "status": "PASS" if adapters else "EMPTY",
        "consumer": "modules/wallet_data_guard/source_manifest.py",
        "passport_adapters": len(adapters),
        "source_files": [x.get("source_file") for x in adapters if isinstance(x, Mapping)],
        "semantic_layer": "manifest",
        "write_policy": "additive_manifest_index_only",
    }


def validate_source_manifest(manifest: Mapping[str, Any]) -> dict[str, Any]:
    required = [
        "source_id",
        "source_type",
        "token_address",
        "collected_at",
        "raw_path",
        "schema_version",
        "read_mode",
        "confidence",
        "allowed_layers",
        "blocked_layers",
    ]
    failures = []
    for key in required:
        value = manifest.get(key)
        if value is None or value == "" or value == []:
            failures.append(key)
    if manifest.get("read_mode") != "readonly":
        failures.append("read_mode_must_be_readonly")
    if manifest.get("contains_inference") and "facts" in manifest.get("allowed_layers", []):
        failures.append("inference_source_cannot_write_facts")
    if manifest.get("contains_handoff") and any(layer in manifest.get("allowed_layers", []) for layer in ["raw", "facts", "evidence"]):
        failures.append("handoff_source_cannot_write_lower_layers")
    return {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }
