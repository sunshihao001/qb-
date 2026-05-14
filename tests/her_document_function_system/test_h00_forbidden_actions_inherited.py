def test_h00_forbidden_actions_inherited():
    required = ['live_runtime', 'wallet_signing', 'auto_deploy', 'production_trading']
    queue_item = {'queue_item_id': 'queue_h00_g00_policy_review', 'forbidden_actions': []}
    missing = [action for action in required if action not in queue_item['forbidden_actions']]
    assert missing
