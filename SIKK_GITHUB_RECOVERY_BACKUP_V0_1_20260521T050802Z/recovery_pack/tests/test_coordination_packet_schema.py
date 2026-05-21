import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_coordination_packet_schema():
    schema=json.load(open(ROOT/'contracts/coordination_task_packet_schema.json'))
    packet=json.load(open(ROOT/'data/coordination/latest/coordination_task_packet.json'))
    assert schema['additionalProperties'] is False
    assert set(schema['required']).issubset(packet)
    assert packet['mode']=='PAPER_ONLY'
