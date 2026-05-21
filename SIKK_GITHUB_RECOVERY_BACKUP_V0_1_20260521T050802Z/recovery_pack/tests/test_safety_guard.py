import pytest

from core.safety_guard import assert_probe_only, assert_no_forbidden_text


def test_probe_only_metadata_passes():
    assert_probe_only({
        "mode": "paper_only",
        "live_trading_enabled": False,
        "swap_allowed": False,
        "private_key_required": False,
    })


@pytest.mark.parametrize("metadata", [
    {"mode": "live", "live_trading_enabled": False, "swap_allowed": False, "private_key_required": False},
    {"mode": "paper_only", "live_trading_enabled": True, "swap_allowed": False, "private_key_required": False},
    {"mode": "paper_only", "live_trading_enabled": False, "swap_allowed": True, "private_key_required": False},
    {"mode": "paper_only", "live_trading_enabled": False, "swap_allowed": False, "private_key_required": True},
])
def test_probe_only_metadata_rejects_unsafe(metadata):
    with pytest.raises(ValueError):
        assert_probe_only(metadata)


def test_forbidden_text_rejected():
    with pytest.raises(ValueError):
        assert_no_forbidden_text("please swap this token")
