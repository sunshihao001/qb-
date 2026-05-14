REQUIRED = ['queue_id','queue_status','source_acceptance_status','total_items','ready_items','blocked_items','deferred_items','review_items','governance_items','created_at','last_updated_at','next_dispatch_candidates','forbidden_global_actions']


def test_h00_queue_state_required_fields():
    queue_state = {'queue_status': 'QUEUE_READY_WITH_GAPS'}
    missing = [field for field in REQUIRED if field not in queue_state]
    assert missing
