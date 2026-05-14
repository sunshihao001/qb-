import json
import subprocess
from pathlib import Path

REPO = Path('/root/sikk-gmgn')


def test_h00_real_queue_executor_generates_required_outputs(tmp_path):
    a00 = tmp_path / 'a00_real_acceptance_to_h00_handoff.json'
    a00.write_text(json.dumps({
        'handoff_id': 'a00_to_h00_fixture',
        'from_phase': 'A00_REAL_ACCEPTANCE',
        'to_phase': 'H00_REAL_DOWNSTREAM_QUEUE',
        'final_status': 'A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS',
        'source_acceptance_run_id': 'a00_real_fixture',
        'source_pipeline_run_id': 'o00_run_fixture',
        'readiness_certificate': {
            'final_status': 'A00_REAL_ACCEPTANCE_EVIDENCE_READY_WITH_GAPS',
            'readiness_level': 'HANDOFF_READY_WITH_NON_BLOCKING_GAPS',
            'ready_for_h00': True,
            'ready_for_u00': True,
            'ready_for_g00': True,
            'ready_for_production': False,
            'open_gaps': ['policy_not_active','run_document_not_validated'],
            'accepted_risks': ['safe_dry_run_only'],
        },
        'real_evidence_bundle': {'bundle_id': 'bundle_fixture'},
        'phase_status_matrix': {'A00': 'READY_WITH_GAPS'},
        'artifact_manifest': {'artifacts': []},
        'gap_propagation_report': {'open_gaps': ['policy_not_active','run_document_not_validated']},
        'acceptance_decision': {'decision': 'ACCEPTED_WITH_GAPS'},
        'allowed_next_actions': ['generate_downstream_queue','handoff_to_u00','handoff_to_g00'],
        'forbidden_next_actions': ['live_runtime','wallet_signing','auto_deploy','production_trading','execute_real_order'],
    }, ensure_ascii=False), encoding='utf-8')
    out = tmp_path / 'h00_run'
    result = subprocess.run(['python3','tools/h00_real_queue_executor.py','--a00-handoff',str(a00),'--repo-root',str(REPO),'--output-dir',str(out),'--safe-mode'], cwd=REPO, text=True, capture_output=True)
    assert result.returncode == 10, result.stdout + result.stderr
    required = [
        'downstream_targets/downstream_target_inventory.json','capability_matrix/target_capability_matrix.json','routing/routing_decision.json','queue/downstream_queue.json','queue/queue_items.json','dependency/dependency_graph.json','priority/priority_plan.json','gap_risk/gap_risk_binding.json','handoff_packets/h00_to_u00_handoff_packet.json','handoff_packets/h00_to_g00_handoff_packet.json','handoff_packets/h00_to_o00_handoff_packet.json','queue_state/queue_state.json','acceptance/h00_real_queue_acceptance.json','reports/h00_real_queue_report.md'
    ]
    missing = [rel for rel in required if not (out / rel).exists()]
    assert not missing
    acceptance = json.loads((out/'acceptance/h00_real_queue_acceptance.json').read_text())
    assert acceptance['final_status'] == 'H00_REAL_DOWNSTREAM_QUEUE_READY_WITH_GAPS'
