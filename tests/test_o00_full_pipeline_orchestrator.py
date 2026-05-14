import json
from pathlib import Path

REPO_ROOT = Path('/root/sikk-gmgn')
SYSTEM_ROOT = REPO_ROOT / 'system/her_document_function_system'
DATA_ROOT = REPO_ROOT / 'data/her_document_function_system'
O00_ROOT = SYSTEM_ROOT / 'controllers/O00_full_pipeline_orchestrator'
O00_RUN_ROOT = DATA_ROOT / 'o00_runs'
CANONICAL_ROUTE = SYSTEM_ROOT / 'CANONICAL_ROUTE.json'
RUNTIME_INDEX = DATA_ROOT / 'runtime_index/her_dfafs_runtime_index.json'

EXPECTED_FILES = [
    '01_o00_manifest.yaml',
    '02_o00_context_pack.md',
    '03_o00_objective_tree.yaml',
    '04_o00_input_contract.json',
    '05_o00_output_contract.json',
    '06_o00_execution_protocol.md',
    '07_o00_acceptance_gate.yaml',
    '08_o00_state.json',
    '09_o00_handoff_packet.schema.json',
    '10_pipeline_run.schema.json',
    '11_pipeline_state.schema.json',
    '12_stage_dependency_graph.schema.json',
    '13_stage_transition_rule.schema.json',
    '14_pipeline_queue.schema.json',
    '15_pipeline_execution_plan.schema.json',
    '16_pipeline_recovery_policy.schema.json',
    '17_pipeline_trace_audit_spec.yaml',
    '18_pipeline_acceptance_matrix.schema.json',
    '19_pipeline_report_template.md',
    '20_controller_registry.schema.json',
    '21_pipeline_config.schema.json',
    '22_pipeline_policy_binding.schema.json',
    '23_pipeline_gap_propagation.schema.json',
    '24_pipeline_failure_evidence.schema.json',
    '25_pipeline_final_handoff.schema.json',
]


def load_json(path: Path):
    return json.loads(path.read_text())


def test_o00_controller_has_required_file_pack_and_run_root():
    assert O00_ROOT.exists()
    assert O00_RUN_ROOT.exists()
    actual = sorted(p.name for p in O00_ROOT.iterdir() if p.is_file())
    assert actual == sorted(EXPECTED_FILES)


def test_o00_input_output_contracts_enforce_master_entry_requirements():
    input_contract = load_json(O00_ROOT / '04_o00_input_contract.json')
    required = set(input_contract['required'])
    for key in [
        'source_document_or_document_refs',
        'operator_goal',
        'governance_policy_bundle',
        'controller_registry',
        'execution_boundary',
        'pipeline_config',
        'repo_root',
        'write_policy',
        'safe_mode',
    ]:
        assert key in required
    assert input_contract['properties']['safe_mode']['const'] is True
    boundary = input_contract['properties']['execution_boundary']['properties']
    assert boundary['allow_live_runtime']['const'] is False
    assert boundary['allow_wallet_signing']['const'] is False
    assert boundary['allow_auto_deploy']['const'] is False
    assert boundary['allow_production_trading']['const'] is False

    output_contract = load_json(O00_ROOT / '05_o00_output_contract.json')
    for key in [
        'preflight_result',
        'pipeline_run',
        'pipeline_execution_plan',
        'stage_dependency_graph',
        'pipeline_state',
        'stage_state_matrix',
        'pipeline_queue',
        'pipeline_gap_register',
        'gap_propagation_matrix',
        'pipeline_acceptance_matrix',
        'recovery_report',
        'trace_log',
        'audit_log',
        'final_handoff',
        'final_report',
    ]:
        assert key in output_contract['required']


def test_o00_registry_dependency_transition_and_recovery_schemas_cover_full_chain():
    registry = load_json(O00_ROOT / '20_controller_registry.schema.json')
    registered = registry['properties']['registered_controllers']['items']['properties']['controller_id']['enum']
    assert registered == ['G00', 'K00', 'F00', 'V00', 'R00', 'A00', 'H00', 'U00']

    graph = load_json(O00_ROOT / '12_stage_dependency_graph.schema.json')
    edge_types = graph['properties']['edges']['items']['properties']['dependency_type']['enum']
    for dep in [
        'REQUIRES_K00_HANDOFF',
        'REQUIRES_F00_HANDOFF',
        'REQUIRES_V00_HANDOFF',
        'REQUIRES_A00_READINESS_CERTIFICATE',
        'REQUIRES_G00_POLICY',
    ]:
        assert dep in edge_types

    transition = load_json(O00_ROOT / '13_stage_transition_rule.schema.json')
    blocked_reasons = transition['properties']['blocked_by']['items']['enum']
    for reason in ['missing_handoff', 'missing_evidence', 'missing_acceptance', 'blocking_gap', 'policy_violation']:
        assert reason in blocked_reasons

    queue = load_json(O00_ROOT / '14_pipeline_queue.schema.json')
    statuses = queue['properties']['queue_items']['items']['properties']['status']['enum']
    for status in ['QUEUED', 'RUNNING', 'COMPLETED', 'BLOCKED', 'FAILED', 'RETRY_PENDING']:
        assert status in statuses

    recovery = load_json(O00_ROOT / '16_pipeline_recovery_policy.schema.json')
    for stage in ['K00', 'F00', 'V00', 'R00', 'A00', 'H00', 'U00', 'G00']:
        assert stage in recovery['properties']['stage_failure_policies']['properties']


def test_o00_protocol_acceptance_gap_and_trace_rules_prevent_false_closure():
    protocol = (O00_ROOT / '06_o00_execution_protocol.md').read_text()
    for idx in range(19):
        assert f'O00.{idx}' in protocol
    for phrase in [
        'No G00 active policy bundle, no pipeline start',
        'No controller registry, no stage dispatch',
        'No K00 handoff, no F00',
        'No F00 handoff, no V00',
        'No V00 handoff, no R00',
        'No A00 readiness certificate, no H00',
        'DESIGN_ONLY is not IMPLEMENTED',
        'test_plan is not TESTED',
        'binding_plan is not RUNNER_BOUND',
        'live_runtime',
        'wallet_signing',
        'auto_deploy',
        'production_trading',
    ]:
        assert phrase in protocol

    gate = (O00_ROOT / '07_o00_acceptance_gate.yaml').read_text()
    for phrase in [
        'g00_policy_bundle_required',
        'controller_registry_required',
        'pipeline_run_id_required',
        'ready_with_gaps_must_carry_gap_refs',
        'forbidden_actions_must_be_inherited',
        'design_only_must_not_be_marked_implemented',
        'final_report_must_output_true_pipeline_status',
    ]:
        assert phrase in gate

    gap = load_json(O00_ROOT / '23_pipeline_gap_propagation.schema.json')
    assert 'gap_id' in gap['required']
    assert gap['properties']['status']['enum'] == ['OPEN', 'RESOLVED', 'ACCEPTED_RISK', 'DEFERRED', 'INVALIDATED', 'SUPERSEDED']
    assert gap['properties']['blocking']['type'] == 'boolean'

    acceptance = load_json(O00_ROOT / '18_pipeline_acceptance_matrix.schema.json')
    final_statuses = acceptance['properties']['final_pipeline_status']['enum']
    for status in ['PIPELINE_ACCEPTED', 'PIPELINE_READY_WITH_GAPS', 'PIPELINE_BLOCKED', 'PIPELINE_REJECTED', 'PIPELINE_DESIGN_ONLY', 'PIPELINE_VALIDATED_NOT_BOUND']:
        assert status in final_statuses

    trace = (O00_ROOT / '17_pipeline_trace_audit_spec.yaml').read_text()
    for event in ['stage_dispatched', 'stage_failed', 'gap_propagated', 'recovery_decided', 'pipeline_acceptance_built', 'final_handoff_written']:
        assert event in trace


def test_canonical_route_and_runtime_index_include_o00_master_orchestrator():
    route = load_json(CANONICAL_ROUTE)
    runtime_index = load_json(RUNTIME_INDEX)

    assert route['canonical_o00_controller'] == str(O00_ROOT)
    assert route['canonical_o00_run_root'] == str(O00_RUN_ROOT)
    assert 'O00' in route['controller_chain']

    assert 'O00' in runtime_index['phases']
    o00 = runtime_index['phases']['O00']
    assert o00['controller_root'] == str(O00_ROOT)
    assert o00['run_root'] == str(O00_RUN_ROOT)
    assert o00['status'] in {'DESIGN_BLUEPRINT_READY', 'O00_ACCEPTED', 'O00_READY_WITH_GAPS'}
    assert o00['primary_refs']
