from __future__ import annotations

from pathlib import Path

from modules.source_wallet_bot.path_resolver import (
    READ_PRIORITY_TIERS,
    load_records_with_priority,
    resolve_field_dict,
    resolve_legacy_fallback,
    resolve_legacy_mapping,
    resolve_passport,
    resolve_standard_path,
    resolve_token_index,
    resolve_wallet_data_path,
)


def test_path_resolver_exposes_six_layer_priority():
    assert READ_PRIORITY_TIERS[:6] == [
        "new_standard_entry",
        "token_index",
        "data_passport",
        "field_dictionary",
        "legacy_path_mapping",
        "legacy_readonly_fallback",
    ]


def test_resolve_standard_path_prefers_new_standard_entry(tmp_path: Path):
    token = "TokenABC"
    path = tmp_path / "data/source_wallet_bot/legacy" / token / "wallet_data/normalized/wallet_trade_normalized.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"records": [{"wallet_address": "W1"}]}', encoding="utf-8")

    result = resolve_wallet_data_path("wallet_trade_normalized.json", token, root=tmp_path)

    assert result.source_tier == "new_standard_entry"
    assert result.is_standard is True
    assert result.is_legacy_fallback is False
    assert result.resolved_path == f"data/source_wallet_bot/legacy/{token}/wallet_data/normalized/wallet_trade_normalized.json"


def test_load_records_with_priority_returns_resolution(tmp_path: Path):
    token = "TokenABC"
    path = tmp_path / "data/source_wallet_bot/legacy" / token / "wallet_data/normalized/wallet_trade_normalized.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"records": [{"wallet_address": "W1"}]}', encoding="utf-8")

    records, result = load_records_with_priority("wallet_trade_normalized.json", token, root=tmp_path)

    assert records == [{"wallet_address": "W1"}]
    assert result.source_tier == "new_standard_entry"


def test_resolver_marks_missing_after_controlled_chain(tmp_path: Path):
    result = resolve_wallet_data_path("wallet_trade_normalized.json", "MissingToken", root=tmp_path)

    assert result.source_tier == "missing"
    assert result.resolved_path is None
    assert result.missing_reason == "not_found_after_standard_index_passport_field_dict_mapping_legacy_readonly"
    tiers = [step["tier"] for step in result.fallback_chain]
    assert "new_standard_entry" in tiers
    assert "legacy_readonly_fallback" in tiers


def test_individual_layer_functions_are_importable(tmp_path: Path):
    assert resolve_standard_path("wallet_trade_normalized.json", "T", root=tmp_path).missing_reason
    assert resolve_token_index("T", root=tmp_path).missing_reason
    assert resolve_passport("T", root=tmp_path).missing_reason
    assert resolve_field_dict("wallet_trade_normalized.json", root=tmp_path).missing_reason
    assert resolve_legacy_mapping("wallet_trade_normalized.json", "T", root=tmp_path).missing_reason
    assert resolve_legacy_fallback("wallet_trade_normalized.json", "T", root=tmp_path).missing_reason
