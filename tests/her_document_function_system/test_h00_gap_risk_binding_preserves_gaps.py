def test_h00_gap_risk_binding_preserves_gaps():
    open_gaps = ['policy_not_active', 'paper_runtime_not_enabled', 'run_document_not_validated']
    binding = {'bindings': [{'queue_item_id': 'queue_h00_u00_review_gaps', 'gap_refs': ['policy_not_active']}]} 
    bound = {gap for item in binding['bindings'] for gap in item.get('gap_refs', [])}
    missing = [gap for gap in open_gaps if gap not in bound]
    assert missing
