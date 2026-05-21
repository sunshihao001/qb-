from adapters.gmgn_skill_adapter import GMGNSkillAdapter
from adapters.okx_skill_adapter import OKXSkillAdapter


def test_gmgn_logical_source_maps_to_actual_skills():
    adapter = GMGNSkillAdapter()
    assert adapter.source == "gmgn"
    assert adapter.source_type == "hermes_skill"
    assert adapter.actual_skill_for_operation("query_token") == "gmgn-token"
    assert adapter.actual_skill_for_operation("query_market") == "gmgn-market"
    assert adapter.actual_skill_for_operation("query_wallet") == "gmgn-portfolio"
    assert adapter.actual_skill_for_operation("query_track") == "gmgn-track"


def test_okx_logical_source_maps_to_actual_skills():
    adapter = OKXSkillAdapter()
    assert adapter.source == "okx"
    assert adapter.source_type == "hermes_skill"
    assert adapter.actual_skill_for_operation("query_token") == "okx-dex-token"
    assert adapter.actual_skill_for_operation("query_market") == "okx-dex-market"
    assert adapter.actual_skill_for_operation("query_security") == "okx-security"
    assert adapter.actual_skill_for_operation("query_wallet") == "okx-wallet-portfolio"


def test_detected_agent_skill_is_not_invokable_without_bridge():
    adapter = GMGNSkillAdapter()
    result = adapter.fetch("TOKEN", "solana", operation="query_token").to_dict()
    assert result["source"] == "gmgn"
    assert result["source_type"] == "hermes_skill"
    assert result["actual_skill_used"] == "gmgn-token"
    assert result["request_status"] == "capability_detected_not_invokable"
