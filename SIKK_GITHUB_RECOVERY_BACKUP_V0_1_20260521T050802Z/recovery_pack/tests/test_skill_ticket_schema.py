import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_skill_ticket_schema():
    schema=json.load(open(ROOT/'contracts/skill_ticket_schema.json'))
    tickets=json.load(open(ROOT/'data/coordination/latest/openase_skill_ticket.json'))['tickets']
    assert schema['additionalProperties'] is False
    forbidden={'gmgn-swap','gmgn-cooking','live execution','private key','signing','broadcast'}
    for t in tickets:
        assert set(schema['required']).issubset(t)
        assert t['skill_name'] not in forbidden
        assert t['purpose'] and t['downstream_consumer']
