import pytest


@pytest.mark.xfail(reason='Negative assertion fixture intentionally encodes forbidden state for regression checking', strict=True)
def test_h00_no_policy_active_claim():
    handoff = {'to_phase': 'G00_GOVERNANCE_BOUNDARY', 'policy_status': 'POLICY_ACTIVE', 'governance_consumed': False}
    assert handoff['policy_status'] != 'POLICY_ACTIVE' or handoff['governance_consumed'] is True
