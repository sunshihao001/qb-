import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_artifact_consumption_matrix_shape_and_required_consumed():
    m=json.load(open(ROOT/'data/coordination/latest/artifact_consumption_matrix.json'))
    assert m['artifacts']
    required=['artifact_id','artifact_path','produced_by_stage','main_chain_position','expected_downstream_consumer','actual_downstream_consumer','is_consumed','is_required_for_next_stage','missing_reason','repair_action','repair_status']
    for a in m['artifacts']:
        for k in required:
            assert k in a
        assert 'actual_value_gate' in a
        if a['is_required_for_next_stage']:
            assert a['is_consumed'] is True
            assert a['actual_downstream_consumer']
