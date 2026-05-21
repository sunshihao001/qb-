import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
LATEST=ROOT/'data/coordination/latest'

def test_no_runtime_permission_and_forbidden_scope():
    reg=json.load(open(LATEST/'skill_capability_registry.json'))
    for s in reg['skills']:
        if 'gbrain' in s['skill_name'] or 'gbrain' in s['provider']:
            assert s['runtime_decision_permission'] is False
    text='\n'.join(p.read_text(encoding='utf-8') for p in [LATEST/'skill_capability_registry.json', LATEST/'real_skill_interface_activation_report.json'] + list((LATEST/'gbrain_memory_cards').glob('*.json')))
    for bad in ['live_trading_enabled','swap_allowed','private_key_required','signing_allowed','broadcast_allowed']:
        assert bad not in text
