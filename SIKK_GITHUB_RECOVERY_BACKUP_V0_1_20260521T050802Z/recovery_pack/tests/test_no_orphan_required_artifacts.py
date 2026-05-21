import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_no_orphan_required_artifacts():
    m=json.load(open(ROOT/'data/coordination/latest/artifact_consumption_matrix.json'))
    bad=[a for a in m['artifacts'] if a['is_required_for_next_stage'] and not a['actual_downstream_consumer']]
    assert bad == []
    for a in m['artifacts']:
        if not a['is_required_for_next_stage'] and a['main_chain_position'] == 'reference_only':
            assert a['repair_status'] in ['REFERENCE_ONLY','LINKED']
