from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from .contracts import (
    HANDOFF_LIKE_KEYS,
    INFERENCE_LIKE_KEYS,
    PRODUCER_ALLOWED_LAYERS,
    STATE_LIKE_KEYS,
    ProducerType,
    SemanticLayer,
)


class WriteGateError(ValueError):
    """Raised when an artifact would contaminate another semantic layer."""


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _coerce_layer(layer: SemanticLayer | str) -> SemanticLayer:
    return layer if isinstance(layer, SemanticLayer) else SemanticLayer(str(layer))


def _coerce_producer(producer: ProducerType | str) -> ProducerType:
    return producer if isinstance(producer, ProducerType) else ProducerType(str(producer))


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


def validate_write_contract(
    *,
    path: str | Path,
    layer: SemanticLayer | str,
    producer: ProducerType | str,
    payload: Any,
    source_refs: Sequence[str] | None = None,
    task_passport: str | None = None,
    allow_overwrite: bool = False,
) -> dict[str, Any]:
    layer = _coerce_layer(layer)
    producer = _coerce_producer(producer)
    target = Path(path)
    source_refs = list(source_refs or [])

    keys = _collect_keys(payload)
    if layer in {SemanticLayer.RAW, SemanticLayer.NORMALIZED, SemanticLayer.FACTS}:
        bad_inference = sorted(keys.intersection(INFERENCE_LIKE_KEYS))
        if bad_inference:
            raise WriteGateError(f"inference-like field cannot be written to {layer.value}: {bad_inference}")
        bad_handoff = sorted(keys.intersection(HANDOFF_LIKE_KEYS))
        if bad_handoff:
            raise WriteGateError(f"handoff-like field cannot be written to {layer.value}: {bad_handoff}")
        bad_state = sorted(keys.intersection(STATE_LIKE_KEYS))
        if bad_state:
            raise WriteGateError(f"state-like field cannot be written to {layer.value}: {bad_state}")

    allowed_layers = PRODUCER_ALLOWED_LAYERS.get(producer, set())
    if layer not in allowed_layers:
        raise WriteGateError(f"producer {producer.value} cannot write semantic layer {layer.value}")

    if target.exists() and not allow_overwrite:
        raise WriteGateError(f"refuse overwrite without allow_overwrite: {target}")

    if layer not in {SemanticLayer.REPORT, SemanticLayer.MANIFEST, SemanticLayer.QUARANTINE} and not source_refs:
        raise WriteGateError(f"semantic layer {layer.value} requires source_refs")

    if layer not in {SemanticLayer.QUARANTINE} and not task_passport:
        raise WriteGateError(f"semantic layer {layer.value} requires task_passport")

    if layer == SemanticLayer.FACTS and "raw_ref" not in keys and "raw_unit_refs" not in keys and not any(str(ref).startswith("raw:") for ref in source_refs):
        raise WriteGateError("facts layer requires raw_ref/raw_unit_refs or raw: source_refs")

    if layer == SemanticLayer.EVIDENCE and not ({"evidence_level", "fact_refs", "raw_unit_refs"}.intersection(keys)):
        raise WriteGateError("evidence layer requires evidence_level, fact_refs, or raw_unit_refs")

    if layer == SemanticLayer.INFERENCE and not ({"uncertainty", "counter_evidence", "invalidation_condition", "evidence_refs"}.intersection(keys)):
        raise WriteGateError("inference layer requires uncertainty/counter_evidence/invalidation_condition/evidence_refs")

    return {
        "status": "PASS",
        "path": str(target),
        "semantic_layer": layer.value,
        "producer": producer.value,
        "source_refs": source_refs,
        "task_passport": task_passport,
        "backwrite_allowed": False,
    }


def write_controlled_artifact(
    *,
    path: str | Path,
    layer: SemanticLayer | str,
    producer: ProducerType | str,
    payload: Any,
    source_refs: Sequence[str] | None = None,
    task_passport: str | None = None,
    allow_overwrite: bool = False,
) -> dict[str, Any]:
    contract = validate_write_contract(
        path=path,
        layer=layer,
        producer=producer,
        payload=payload,
        source_refs=source_refs,
        task_passport=task_passport,
        allow_overwrite=allow_overwrite,
    )
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    wrapped = {
        "guard_metadata": {
            **contract,
            "written_at": _utc_now(),
        },
        "payload": payload,
    }
    target.write_text(json.dumps(wrapped, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {**contract, "bytes_written": target.stat().st_size}
