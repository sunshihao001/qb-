import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_skill_call_justification_schema_exists_and_runtime_false():
    s=json.load(open(ROOT/'contracts/skill_call_justification_schema.json'))
    for k in ['skill_name','provider','call_reason','upstream_input','downstream_consumer','runtime_decision_permission','paper_only_boundary_check','actual_value_gate_status']:
        assert k in s['required']
    assert s['properties']['runtime_decision_permission']['const'] is False
