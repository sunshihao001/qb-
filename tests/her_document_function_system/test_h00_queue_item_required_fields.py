REQUIRED_FIELDS = ['queue_item_id','source_phase','target_controller','task_type','priority','status','required_inputs','expected_outputs','allowed_actions','forbidden_actions','gap_refs','risk_refs','evidence_refs','handoff_packet_ref','acceptance_requirements','created_at']


def test_h00_queue_item_required_fields():
    item = {
        'queue_item_id': 'queue_h00_u00_review_gaps',
        'target_controller': 'U00',
    }
    missing = [field for field in REQUIRED_FIELDS if field not in item]
    assert missing
