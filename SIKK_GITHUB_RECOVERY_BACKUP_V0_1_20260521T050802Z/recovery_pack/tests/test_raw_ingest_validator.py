from pathlib import Path

from core.raw_ingest_validator import missing_external_payload, validate_external_payload


def valid_payload():
    return {
        "source": "gmgn",
        "source_type": "hermes_skill_handoff",
        "actual_skill_used": "gmgn-token",
        "operation_used": "query_token",
        "token_address": "TOKEN",
        "fetch_ts": "2026-01-01T00:00:00+00:00",
        "request_status": "success",
        "raw_response": {"price_usd": 1},
        "errors": [],
    }


def test_valid_external_payload_passes():
    ok, errors = validate_external_payload(valid_payload(), "gmgn", "TOKEN")
    assert ok is True
    assert errors == []


def test_empty_success_raw_response_invalid():
    payload = valid_payload()
    payload["raw_response"] = {}
    ok, errors = validate_external_payload(payload, "gmgn", "TOKEN")
    assert ok is False
    assert any(e["error_type"] == "empty_success_raw_response" for e in errors)


def test_forbidden_operation_invalid():
    payload = valid_payload()
    payload["operation_used"] = "swap"
    ok, errors = validate_external_payload(payload, "gmgn", "TOKEN")
    assert ok is False
    assert any(e["error_type"] == "unsafe_operation_blocked" for e in errors)


def test_missing_payload_shape():
    payload = missing_external_payload("gmgn", "TOKEN", Path("missing.json"))
    assert payload["request_status"] == "external_raw_missing"
    assert payload["source_type"] == "hermes_skill_handoff"
