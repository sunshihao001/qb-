from pathlib import Path
import json

ROOT = Path('/root/sikk-quant-runner')
LATEST = ROOT / 'data/latest/task_package_application_report.json'


def load_bundle():
    assert LATEST.exists()
    ptr = json.loads(LATEST.read_text(encoding='utf-8'))
    report = json.loads((ROOT / ptr['canonical_path']).read_text(encoding='utf-8'))
    return ptr, report


def test_task_package_application_outputs_exist():
    ptr, report = load_bundle()
    assert ptr['pointer_only'] is True
    assert (ROOT / ptr['canonical_path']).exists()
    assert (ROOT / ptr['markdown_path']).exists()
    assert report['artifact_type'] == 'sikk_task_package_application_scenario_brief'
    assert report['task_package_files']
    assert report['acceptance_status'] in {'PASS', 'PASS_WITH_GAPS'}


def test_task_package_application_safe_boundaries():
    _, report = load_bundle()
    forbidden = report['forbidden_scope_confirmed']
    assert forbidden['paper_position_created'] is False
    assert forbidden['paper_trade_created'] is False
    assert forbidden['swap_or_order_quote_called'] is False
    assert forbidden['private_key_signing_broadcast_used'] is False
    assert forbidden['live_trading_used'] is False
    assert forbidden['strategy_contract_modified'] is False
    assert forbidden['canonical_promotion_performed'] is False
    assert forbidden['openase_gbrain_runtime_decision'] is False


def test_task_package_application_has_operational_brief_and_gate_status():
    _, report = load_bundle()
    brief = report['operator_brief_for_real_use']
    app = report['application_state']
    assert brief['professional_term'] == 'Operating Backbone Control-Plane Application Scenario'
    assert brief['s_stage_position']
    assert brief['r_pipeline_position']
    assert 'DecisionTicket' in brief['data_objects']
    assert app['application_status'] in {
        'APPLICATION_APPLIED_AS_CONTROL_PLANE_BLOCKED_FOR_RUNTIME',
        'APPLICATION_READY_FOR_PAPER_ONLY_VALIDATION_WITH_PROMOTION_BLOCKED',
        'APPLICATION_READY_FOR_CONTROLLED_PROMOTION_REVIEW',
    }
    assert set(app['gate_statuses']).issuperset({'wiring_gate', 'semantic_gate', 'runtime_gate', 'promotion_gate', 'overall'})
    if app['runtime_validation_allowed'] is False:
        assert app['decision_state'] != 'PAPER_READY_CANDIDATE'
