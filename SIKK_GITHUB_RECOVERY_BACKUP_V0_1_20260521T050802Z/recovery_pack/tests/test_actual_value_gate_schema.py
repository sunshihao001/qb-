import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_actual_value_gate_schema_exists_and_requires_core_fields():
    s=json.load(open(ROOT/'contracts/actual_value_gate_schema.json'))
    for k in ['main_chain_position','upstream_input','downstream_consumer','decision_value','current_stage_relevance','skip_if','acceptance_evidence']:
        assert k in s['required']
    assert 'not_now' in s['properties']['main_chain_position']['enum']
