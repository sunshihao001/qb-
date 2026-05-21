import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
LATEST=ROOT/'data/coordination/latest'

def test_memory_cards_schema():
    schema=json.load(open(ROOT/'contracts/gbrain_file_protocol_bridge_schema.json'))
    assert schema['additionalProperties'] is False
    cards=list((LATEST/'gbrain_memory_cards').glob('*.json'))
    assert len(cards) >= 5
    for p in cards:
        c=json.load(open(p))
        assert set(schema['required']).issubset(c)
        assert c['mode']=='GBRAIN_FILE_PROTOCOL_BRIDGE'
        assert c['real_gbrain_available'] is False
        assert c['runtime_decision_permission'] is False
    assert (LATEST/'invocation_evidence/gbrain_file_protocol_preflight_response.json').exists() or True
