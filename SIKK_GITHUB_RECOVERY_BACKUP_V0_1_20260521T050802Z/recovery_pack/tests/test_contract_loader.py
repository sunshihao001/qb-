from __future__ import annotations

from pathlib import Path

from core.contract_loader import ensure_ascii_path, load_contract


def test_load_contract_hash_and_safety():
    contract, contract_hash = load_contract("contracts/strategy_contract.json")
    assert contract["strategy_id"] == "sikk_quant_runner_v0_1"
    assert len(contract_hash) == 64
    assert contract["swap_allowed"] is False
    assert contract["live_trading_enabled"] is False


def test_ensure_ascii_path_rejects_translated_path():
    try:
        ensure_ascii_path("数据/运行/x")
    except Exception:  # noqa: BLE001
        pass
    else:
        raise AssertionError("translated path accepted")
