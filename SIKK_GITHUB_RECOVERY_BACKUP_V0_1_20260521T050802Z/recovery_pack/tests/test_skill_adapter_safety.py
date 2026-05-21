import pytest

from adapters.gmgn_skill_adapter import GMGNSkillAdapter
from adapters.okx_skill_adapter import OKXSkillAdapter


@pytest.mark.parametrize("adapter", [GMGNSkillAdapter(), OKXSkillAdapter()])
@pytest.mark.parametrize("operation", ["swap", "execute_trade", "sign_transaction", "broadcast_transaction"])
def test_forbidden_operations_blocked(adapter, operation):
    result = adapter.fetch("TOKEN", "solana", operation=operation).to_dict()
    assert result["request_status"] == "unsafe_operation_blocked"
    assert result["operation_used"] == operation
    assert result["errors"]


def test_uninstalled_skill_cannot_success():
    result = GMGNSkillAdapter().fetch("TOKEN", "solana").to_dict()
    assert result["request_status"] in {"skill_not_found", "not_configured", "failed", "capability_detected_not_invokable"}
    assert result["request_status"] != "success"


def test_allowed_callable_can_success_read_only():
    adapter = GMGNSkillAdapter(skill_callable=lambda actual_skill, operation, token, chain: {"price_usd": 1, "liquidity_usd": 2})
    result = adapter.fetch("TOKEN", "solana", operation="query_token").to_dict()
    assert result["request_status"] == "success"
    assert result["source"] == "gmgn"
    assert result["source_type"] == "hermes_skill"
