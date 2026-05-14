from pathlib import Path
import yaml

from modules.integration_program.i05_auto_closure_runner import run


def test_i05_auto_closure_runner_writes_task_package():
    result = run('/root/sikk-gmgn', 'dry-run')
    assert result['p0_open'] == 0
    assert result['status'] == 'I05_AUTOMATION_READY_WITH_GAPS'
    base = Path('/root/sikk-gmgn/data/integration_program/I05_review_upgrade_closed_loop')
    required = [
        base/'automation_task_packages/i05_full_automation_task_packet.yaml',
        base/'automation_task_packages/i05_automated_issue_list_package.yaml',
        base/'priority_routing/i05_priority_routing.yaml',
        base/'runtime_state/i05_runtime_state.yaml',
        base/'handoff/i05_to_next_iteration_handoff_packet.yaml',
        base/'acceptance/i05_closed_loop_acceptance_result.yaml',
    ]
    for path in required:
        assert path.exists(), path
        with path.open() as f:
            yaml.safe_load(f)


def test_i05_safety_boundaries_remain_false():
    run('/root/sikk-gmgn', 'dry-run')
    p = Path('/root/sikk-gmgn/data/integration_program/I05_review_upgrade_closed_loop/runtime_state/i05_runtime_state.yaml')
    data = yaml.safe_load(p.read_text())
    restrictions = data['i05_runtime_state']['restrictions']
    assert restrictions['live_execution_allowed'] is False
    assert restrictions['wallet_signing_allowed'] is False
    assert restrictions['auto_deploy_allowed'] is False
    assert restrictions['direct_rule_mutation_allowed'] is False
    assert restrictions['paper_runtime_mutation_allowed'] is False
