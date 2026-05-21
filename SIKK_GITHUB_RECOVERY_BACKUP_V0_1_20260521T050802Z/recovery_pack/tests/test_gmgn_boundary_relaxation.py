from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID=(ROOT/'data/latest/gmgn_raw_field_discovery_run_id.txt').read_text().strip()
BASE=ROOT/'data/runs'/RUN_ID


def test_boundary_source_files_identified_and_relaxation_scoped():
    report=json.loads((BASE/'gmgn_raw_field_discovery_report.json').read_text())
    files=set(report['safety_boundary_source_files'])
    assert 'configs/project_boundary.yaml' in files
    assert 'configs/source_config.yaml' in files
    assert 'core/safety_guard.py' in files
    assert 'adapters/gmgn_read_only_router.py' in files
    assert 'scripts/run_gmgn_raw_field_discovery.py' in files
    assert report['relaxed_discovery_mode'] is True
    assert 'read-only' in report['relaxed_scope']


def test_hard_execution_boundary_still_forbidden():
    report=json.loads((BASE/'gmgn_raw_field_discovery_report.json').read_text())
    hard=set(report['hard_boundary_still_forbidden'])
    for term in ['gmgn-swap','gmgn-cooking','swap','execute_trade','private_key','signing','broadcast','live_trading']:
        assert term in hard
    forbidden=report['forbidden_scope_confirmed']
    assert forbidden['swap_route_signing_broadcast_used'] is False
    assert forbidden['gmgn_swap_or_cooking_used'] is False
    assert forbidden['decision_ticket_created'] is False
