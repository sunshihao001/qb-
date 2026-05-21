import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_boundaries():
    reg=json.load(open(ROOT/'data/coordination/latest/skill_capability_registry.json'))
    for s in reg['skills']:
        assert s['runtime_decision_permission'] is False
        text=json.dumps(s)
        assert 'strategy_contract modification' not in text
        assert 'decision_ticket modification' not in text
    combined='\n'.join(p.read_text(encoding='utf-8') for p in (ROOT/'data/coordination/latest/invocation_evidence').glob('*.json'))
    for bad in ['swap_allowed','private_key_required','signing_allowed','broadcast_allowed','live_trade']:
        assert bad not in combined
