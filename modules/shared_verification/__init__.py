from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping

FORBIDDEN_FIELD_NAMES = {
    "private_key",
    "api_key",
    "secret",
    "mnemonic",
    "seed_phrase",
    "buy_signal",
    "sell_signal",
    "execute_now",
    "trade_allowed",
    "swap",
    "sign",
    "broadcast",
}

REQUIRED_STAGE_OUTPUT_FIELDS = [
    "stage_id",
    "status",
    "source_skill",
    "source_fields",
    "evidence_refs",
    "inference_boundary",
    "invalidation_condition",
]

DEFAULT_REQUIRED_FIELDS_BY_STAGE = {
    "stage_01_candidate_discovery": ["token_address", "chain", "discovered_at"],
    "stage_02_safety_gate": ["token_address", "chain"],
    "stage_03_market_gate": ["token_address", "market_cap", "liquidity_usd"],
    "stage_13_state_machine": ["token_address"],
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _walk_forbidden(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{path}.{key_text}" if path else key_text
            if key_text in FORBIDDEN_FIELD_NAMES:
                found.append(key_text)
            found.extend(_walk_forbidden(child, child_path))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            found.extend(_walk_forbidden(child, f"{path}[{idx}]"))
    return sorted(set(found))


def _field_present(payload: Mapping[str, Any], field_name: str) -> bool:
    locations = [payload, payload.get("facts", {}), payload.get("stats", {}), payload.get("inference", {})]
    for item in locations:
        if isinstance(item, Mapping) and item.get(field_name) not in (None, "", []):
            return True
    return False


def _parse_time(value: Any) -> datetime | None:
    if not value:
        return None
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


@dataclass
class PermissionBoundaryValidator:
    forbidden_fields: set[str] = field(default_factory=lambda: set(FORBIDDEN_FIELD_NAMES))

    def validate(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        found = _walk_forbidden(payload)
        return {
            "validator": self.__class__.__name__,
            "status": "FAIL" if found else "PASS",
            "failed_rules": ["FORBIDDEN_FIELD_PRESENT"] if found else [],
            "forbidden_fields": found,
            "downgrade_to": "PERMISSION_FAIL" if found else "",
            "checked_at": _utc_now(),
        }


@dataclass
class FieldCompletenessValidator:
    required_fields_by_stage: Mapping[str, list[str]] = field(default_factory=lambda: DEFAULT_REQUIRED_FIELDS_BY_STAGE)

    def validate(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        stage_id = str(payload.get("stage_id") or "")
        required = list(self.required_fields_by_stage.get(stage_id, []))
        missing = [name for name in required if not _field_present(payload, name)]
        return {
            "validator": self.__class__.__name__,
            "status": "FAIL" if missing else "PASS",
            "failed_rules": ["MISSING_REQUIRED_FIELD"] if missing else [],
            "missing_fields": missing,
            "downgrade_to": "INSUFFICIENT_DATA" if missing else "",
            "checked_at": _utc_now(),
        }


@dataclass
class StageOutputValidator:
    required_stage_fields: list[str] = field(default_factory=lambda: list(REQUIRED_STAGE_OUTPUT_FIELDS))

    def validate(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        missing: list[str] = []
        for key in self.required_stage_fields:
            if payload.get(key) in (None, "", []):
                missing.append(key)
        if str(payload.get("status") or "").upper() in {"PASS", "WARN", "PAPER_READY", "READY_FOR_CONFIRMATION"}:
            if not payload.get("evidence_refs"):
                if "evidence_refs" not in missing:
                    missing.append("evidence_refs")
            if not payload.get("inference_boundary"):
                if "inference_boundary" not in missing:
                    missing.append("inference_boundary")
        return {
            "validator": self.__class__.__name__,
            "status": "FAIL" if missing else "PASS",
            "failed_rules": ["INVALID_STAGE_OUTPUT"] if missing else [],
            "missing_fields": missing,
            "downgrade_to": "INVALID_STAGE_OUTPUT" if missing else "",
            "checked_at": _utc_now(),
        }


@dataclass
class FreshnessValidator:
    now: datetime | None = None

    def validate(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        freshness = payload.get("freshness") if isinstance(payload.get("freshness"), Mapping) else {}
        observed_at = _parse_time(freshness.get("observed_at")) if isinstance(freshness, Mapping) else None
        max_age_sec = freshness.get("max_age_sec", 0) if isinstance(freshness, Mapping) else 0
        failed: list[str] = []
        age_sec: float | None = None
        if observed_at is None:
            failed.append("MISSING_OBSERVED_AT")
        else:
            now = self.now or datetime.now(timezone.utc)
            age_sec = (now - observed_at).total_seconds()
            try:
                max_age = float(max_age_sec)
            except (TypeError, ValueError):
                max_age = 0
            if max_age > 0 and age_sec > max_age:
                failed.append("STALE_DATA")
        return {
            "validator": self.__class__.__name__,
            "status": "FAIL" if failed else "PASS",
            "failed_rules": failed,
            "age_sec": age_sec,
            "downgrade_to": "STALE_DATA" if failed else "",
            "checked_at": _utc_now(),
        }


@dataclass
class StateTransitionSafetyValidator:
    def validate(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        status = str(payload.get("status") or payload.get("final_state") or "").upper()
        inference = payload.get("inference") if isinstance(payload.get("inference"), Mapping) else {}
        wallet_status = str(inference.get("wallet_structure_status") or payload.get("wallet_structure_status") or "").upper()
        evidence_refs = [str(x) for x in payload.get("evidence_refs") or []]
        failures: list[str] = []
        if status in {"PAPER_READY", "READY_FOR_CONFIRMATION"} and wallet_status == "WALLET_SUPPORT":
            other_gate_evidence = [ref for ref in evidence_refs if not ref.upper().startswith("WALLET")]
            if not other_gate_evidence:
                failures.append("WALLET_SUPPORT_CANNOT_DIRECTLY_PROMOTE_TO_PAPER_READY")
        if payload.get("live_disabled") is False:
            failures.append("LIVE_DISABLED_MUST_REMAIN_TRUE")
        return {
            "validator": self.__class__.__name__,
            "status": "FAIL" if failures else "PASS",
            "failed_rules": failures,
            "downgrade_to": "INVALID_TRANSITION" if failures else "",
            "checked_at": _utc_now(),
        }


def validate_stage_output(payload: Mapping[str, Any], *, required_fields_by_stage: Mapping[str, list[str]] | None = None) -> dict[str, Any]:
    validators = [
        PermissionBoundaryValidator(),
        FieldCompletenessValidator(required_fields_by_stage or DEFAULT_REQUIRED_FIELDS_BY_STAGE),
        StageOutputValidator(),
        FreshnessValidator(),
        StateTransitionSafetyValidator(),
    ]
    results = [validator.validate(payload) for validator in validators]
    overall = "PASS" if all(item["status"] == "PASS" for item in results) else "FAIL"
    return {
        "overall_status": overall,
        "validator_results": results,
        "downgrade_to": next((item.get("downgrade_to") for item in results if item.get("downgrade_to")), ""),
        "checked_at": _utc_now(),
    }
