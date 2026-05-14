#!/usr/bin/env python3
from pathlib import Path
import json, sys, re

ROOT = Path('/root/sikk-gmgn/system/her_document_function_system/controllers/H00_handoff_downstream_queue_controller')
REQUIRED_FILES = [
 '01_h00_manifest.yaml','02_h00_context_pack.md','03_h00_objective_tree.yaml','04_h00_input_contract.json','05_h00_output_contract.json','06_h00_execution_protocol.md','07_h00_acceptance_gate.yaml','08_h00_state.json','09_h00_handoff_packet.schema.json','10_downstream_target.schema.json','11_downstream_queue.schema.json','12_queue_item.schema.json','13_dependency_graph.schema.json','14_priority_model.schema.json','15_routing_decision.schema.json','16_handoff_bundle.schema.json','17_queue_state.schema.json','18_retry_recovery.schema.json','19_trace_audit_spec.yaml','20_h00_final_report_template.md']
FORBIDDEN = ['live_runtime','wallet_signing','auto_deploy','production_trading']

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def assert_true(cond, msg):
    if not cond:
        raise AssertionError(msg)

def main():
    results=[]
    for name in REQUIRED_FILES:
        p=ROOT/name
        assert_true(p.exists(), f'missing required file: {name}')
        assert_true(p.stat().st_size>0, f'empty required file: {name}')
        results.append({'check':'file_exists','file':name,'status':'PASSED'})
    for name in REQUIRED_FILES:
        if name.endswith('.json'):
            obj=load_json(ROOT/name)
            results.append({'check':'json_parse','file':name,'status':'PASSED','top_type':type(obj).__name__})
    protocol=(ROOT/'06_h00_execution_protocol.md').read_text(encoding='utf-8')
    for i in range(16):
        assert_true(f'H00.{i}' in protocol, f'execution protocol missing H00.{i}')
    for guard in ['No A00 handoff','No readiness certificate','Queue created is not task executed','A00_BLOCKED','A00_READY_WITH_GAPS']:
        assert_true(guard in protocol, f'execution protocol missing guard: {guard}')
    input_contract=load_json(ROOT/'04_h00_input_contract.json')
    for req in ['a00_handoff_packet','readiness_certificate','evidence_bundle','forbidden_next_actions','execution_boundary']:
        assert_true(req in input_contract.get('required',[]), f'input_contract missing required: {req}')
    eb=input_contract['properties']['execution_boundary']['properties']
    for key in ['allow_live_runtime','allow_wallet_signing','allow_auto_deploy','allow_production_trading']:
        assert_true(eb[key].get('const') is False, f'execution_boundary {key} must be const false')
    output_contract=load_json(ROOT/'05_h00_output_contract.json')
    outs=output_contract['required_outputs']
    for req in ['downstream_queue','queue_items','dependency_graph','handoff_packets','recovery_report','trace_log','audit_log']:
        assert_true(req in outs, f'output_contract missing {req}')
    q=load_json(ROOT/'12_queue_item.schema.json')
    qreq=set(q['required'])
    for req in ['target_phase','required_inputs','expected_outputs','allowed_actions','forbidden_actions','gap_refs']:
        assert_true(req in qreq, f'queue_item schema missing {req}')
    route=load_json(ROOT/'15_routing_decision.schema.json')
    enum=route['properties']['routing_decision']['enum']
    for v in ['ROUTE_TO_PXX','ROUTE_TO_IXX','ROUTE_TO_RUNNER','ROUTE_TO_U00','ROUTE_TO_G00','ROUTE_TO_RECOVERY','ROUTE_TO_BACKLOG','ROUTE_TO_ARCHIVE','BLOCK_ROUTE']:
        assert_true(v in enum, f'routing_decision missing {v}')
    state=load_json(ROOT/'17_queue_state.schema.json')
    se=state['properties']['queue_status']['enum']
    for v in ['ITEM_QUEUED','ITEM_BLOCKED','ITEM_DISPATCHED','ITEM_ACCEPTED_BY_TARGET','ITEM_FAILED']:
        assert_true(v in se, f'queue_state missing {v}')
    trace=(ROOT/'19_trace_audit_spec.yaml').read_text(encoding='utf-8')
    for e in ['h00_started','a00_handoff_loaded','routing_decision_made','queue_item_created','handoff_packet_written','queue_state_written','h00_completed','h00_blocked']:
        assert_true(e in trace, f'trace spec missing {e}')
    gate=(ROOT/'07_h00_acceptance_gate.yaml').read_text(encoding='utf-8')
    for g in ['ready_with_gaps_must_retain_gaps','queue_created_is_not_task_executed','forbidden_actions_must_not_be_removed','missing_trace_audit_blocks_accepted']:
        assert_true(g in gate, f'acceptance gate missing {g}')
    manifest=(ROOT/'01_h00_manifest.yaml').read_text(encoding='utf-8')
    for f in ['start_live_runtime','wallet_signing','auto_deploy','production_trading','treat_queue_created_as_task_executed']:
        assert_true(f in manifest, f'manifest missing forbidden action {f}')
    print(json.dumps({'status':'PASSED','checked_files':len(REQUIRED_FILES),'checks':results}, ensure_ascii=False, indent=2))
if __name__=='__main__':
    main()
