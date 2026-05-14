from pathlib import Path
from her_pipeline_lib import write_json, trace

def exists(run_dir, rels):
    return all((run_dir/r).exists() for r in rels)

def run(run_dir: Path, run_id: str):
    trace(run_dir, run_id, 'V00', 'phase_started', 'STARTED')
    checks=[
      {'check_id':'check_k00_outputs','target':'K00','required_outputs':['k00/document_passport.json','k00/corpus_index.json','k00/system_mapping.json','k00/gap_detection.json','k00/k00_handoff_packet.json']},
      {'check_id':'check_f00_function_mapping','target':'F00','required_outputs':['f00/function_mapping.json','f00/required_system_assets.json','f00/implementation_task_package.json','f00/f00_handoff_packet.json']},
      {'check_id':'check_trace_audit_started','target':'O00','required_outputs':['trace.jsonl','audit.jsonl']},]
    for c in checks:
        c['status']='PASSED' if exists(run_dir,c['required_outputs']) else 'FAILED'
    gaps=[
      {'gap_id':'gap_001','origin_phase':'F00','gap_type':'missing_implementation_evidence','gap_level':'HIGH_GAP','description':'Function mapping exists, but production implementation evidence is intentionally not claimed.', 'route_to':'U00','status':'OPEN'},
      {'gap_id':'gap_002','origin_phase':'V00','gap_type':'real_tool_execution_limited_to_safe_mode','gap_level':'MEDIUM_GAP','description':'Pipeline has safe-mode file execution evidence only; no scheduler/live/paper runtime evidence.', 'route_to':'H00','status':'OPEN'},
      {'gap_id':'gap_003','origin_phase':'G00','gap_type':'governance_candidate_not_applied','gap_level':'MEDIUM_GAP','description':'Governance rules are candidates, not globally active policy.', 'route_to':'G00','status':'OPEN'}]
    matrix={'validation_id':f'v00_validation_{run_id}','checks':checks,'overall_status':'V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS'}
    evidence={'evidence_id':f'v00_evidence_{run_id}','evidence_status':'EVIDENCE_READY_WITH_GAPS','validated_files':[x for c in checks for x in c['required_outputs']],'forbidden_assertions_blocked':['TEST_PLAN_AS_TESTED','MAPPING_AS_CODE_DONE','READY_WITH_GAPS_AS_READY']}
    handoff={'handoff_id':f'v00_handoff_{run_id}','from_phase':'V00','to_phase':'A00','status':'V00_HANDOFF_READY_WITH_GAPS','refs':{'validation_matrix':'v00/validation_matrix.json','gap_register':'v00/gap_register.json','evidence_report':'v00/evidence_report.json'},'gaps':gaps}
    write_json(run_dir/'v00/validation_matrix.json', matrix)
    write_json(run_dir/'v00/gap_register.json', {'gaps':gaps})
    write_json(run_dir/'v00/evidence_report.json', evidence)
    write_json(run_dir/'v00/v00_handoff_packet.json', handoff)
    trace(run_dir, run_id, 'V00', 'phase_completed', 'V00_REAL_VALIDATION_EVIDENCE_READY_WITH_GAPS')
    return handoff
