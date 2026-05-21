from __future__ import annotations

from core.field_mapper import field_value, percent_change, unix_to_iso, ensure_ascii_path


def test_field_value_missing_does_not_default_zero():
    value = field_value(None, source="gmgn", source_path="data/runs/t/r/raw/gmgn.json", missing_reason="missing")
    assert value["value"] is None
    assert value["missing"] is True
    assert value["missing_reason"] == "missing"
    assert value["confidence"] == 0.0


def test_percent_change():
    assert percent_change("110", "100") == 0.1
    assert percent_change("100", "0") is None


def test_unix_to_iso_ms():
    assert unix_to_iso("1779148677233").startswith("2026-")


def test_ensure_ascii_path_rejects_translated_path():
    try:
        ensure_ascii_path("数据/运行/x")
    except Exception as exc:  # noqa: BLE001
        assert "forbidden translated path" in str(exc) or isinstance(exc, UnicodeEncodeError)
    else:
        raise AssertionError("translated path was accepted")
