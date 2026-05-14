import json
from pathlib import Path


def test_o00_sample_replay_expected_ready_with_gaps_status():
    run = Path('/root/sikk-gmgn/data/her_document_function_system/o00_runs/o00_run_20260513_183923_827542/state/pipeline_state.json')
    data = json.loads(run.read_text())
    assert data['final_status'] == 'PIPELINE_READY_WITH_GAPS'
    assert data['system_status_code'] == 'O00_CLI_SAMPLE_REPLAY_READY_WITH_GAPS'
    assert 'TESTED' in data['forbidden_claims_blocked']
