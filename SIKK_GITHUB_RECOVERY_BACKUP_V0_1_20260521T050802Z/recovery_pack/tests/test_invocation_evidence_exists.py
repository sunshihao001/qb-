from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
E=ROOT/'data/coordination/latest/invocation_evidence'

def test_evidence_files_exist():
    for name in ['gbrain_preflight_request.json','gbrain_preflight_response.json','gbrain_preflight_error.json','openase_skill_ticket_request.json','openase_skill_ticket_response.json','openase_skill_ticket_error.json','openase_harness_dry_run_request.json','openase_harness_dry_run_response.json','gbrain_writeback_request.json','gbrain_writeback_response.json','invocation_log.jsonl']:
        assert (E/name).exists(), name
