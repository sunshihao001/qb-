import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from modules.shared_verification import (
    FieldCompletenessValidator,
    FreshnessValidator,
    PermissionBoundaryValidator,
    StageOutputValidator,
    validate_stage_output,
)


def _valid_stage_output(**overrides):
    payload = {
        "stage_id": "stage_02_safety_gate",
        "status": "PASS",
        "facts": {"token_address": "Token111", "chain": "solana"},
        "stats": {},
        "evidence": [{"claim": "安全扫描通过", "source": "okx-security"}],
        "inference": {},
        "counter_evidence": [],
        "inference_boundary": "安全扫描只代表当前观察窗口，不代表未来无风险。",
        "source_skill": ["okx-security"],
        "source_fields": ["riskControlLevel"],
        "evidence_refs": ["okx-security:riskControlLevel"],
        "freshness": {"observed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"), "max_age_sec": 300},
        "invalidation_condition": "riskControlLevel 转 BLOCK 或数据过期。",
        "paper_only": True,
        "live_disabled": True,
    }
    payload.update(overrides)
    return payload


def test_permission_boundary_validator_rejects_nested_secret_and_execution_fields():
    payload = _valid_stage_output(
        facts={"token_address": "Token111", "api_key": "SHOULD_NOT_EXIST"},
        inference={"execute_now": True},
    )

    result = PermissionBoundaryValidator().validate(payload)

    assert result["status"] == "FAIL"
    assert result["downgrade_to"] == "PERMISSION_FAIL"
    assert set(result["forbidden_fields"]) >= {"api_key", "execute_now"}


def test_permission_boundary_validator_passes_safe_paper_only_payload():
    result = PermissionBoundaryValidator().validate(_valid_stage_output())

    assert result["status"] == "PASS"
    assert result["forbidden_fields"] == []


def test_field_completeness_validator_returns_insufficient_data_for_missing_required_fields():
    payload = _valid_stage_output(facts={"chain": "solana"})

    result = FieldCompletenessValidator(required_fields_by_stage={"stage_02_safety_gate": ["token_address", "chain"]}).validate(payload)

    assert result["status"] == "FAIL"
    assert result["downgrade_to"] == "INSUFFICIENT_DATA"
    assert result["missing_fields"] == ["token_address"]


def test_stage_output_validator_requires_evidence_and_inference_boundary():
    payload = _valid_stage_output(evidence_refs=[], inference_boundary="")

    result = StageOutputValidator().validate(payload)

    assert result["status"] == "FAIL"
    assert "evidence_refs" in result["missing_fields"]
    assert "inference_boundary" in result["missing_fields"]


def test_freshness_validator_downgrades_stale_outputs():
    old = (datetime.now(timezone.utc) - timedelta(hours=2)).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload = _valid_stage_output(freshness={"observed_at": old, "max_age_sec": 60})

    result = FreshnessValidator(now=datetime.now(timezone.utc)).validate(payload)

    assert result["status"] == "FAIL"
    assert result["downgrade_to"] == "STALE_DATA"


def test_validate_stage_output_combines_all_validators():
    payload = _valid_stage_output()

    result = validate_stage_output(payload)

    assert result["overall_status"] == "PASS"
    assert {item["validator"] for item in result["validator_results"]} >= {
        "PermissionBoundaryValidator",
        "FieldCompletenessValidator",
        "StageOutputValidator",
        "FreshnessValidator",
    }


def test_validate_stage_output_blocks_wallet_support_as_direct_paper_signal():
    payload = _valid_stage_output(
        stage_id="stage_13_state_machine",
        status="PAPER_READY",
        inference={"wallet_structure_status": "WALLET_SUPPORT", "paper_ready_reason": "wallet only"},
        evidence_refs=["wallet:WALLET_SUPPORT"],
        source_fields=["wallet_structure_status"],
    )

    result = validate_stage_output(payload)

    assert result["overall_status"] == "FAIL"
    assert any(item["validator"] == "StateTransitionSafetyValidator" for item in result["validator_results"])
