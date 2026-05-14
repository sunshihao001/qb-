def test_g00_policy_candidate_is_not_policy_active():
    governance = {
        'evidence_policy_candidate_ref': 'candidate/generated.json',
        'active_policy_bundle': None,
        'status': 'G00_READY_WITH_GAPS',
    }
    assert governance['status'] != 'POLICY_ACTIVE'
    assert governance['active_policy_bundle'] is None
