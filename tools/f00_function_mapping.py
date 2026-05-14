from pathlib import Path
from her_pipeline_lib import write_json, read_json, trace, utcnow

def run(run_dir: Path, run_id: str, repo_root: Path):
    trace(run_dir, run_id, 'F00', 'phase_started', 'STARTED')
    passport=read_json(run_dir/'k00/document_passport.json')
    funcs=[
      ('func_001','K00 document intake','K00','Save raw document and generate passport/index/mapping/handoff',['document','operator_goal'],['document_passport','corpus_index','system_mapping','k00_handoff_packet'],['tools/k00_document_intake.py']),
      ('func_002','F00 function realization mapping','F00','Convert explanatory document into functional items/assets/task package',['k00_handoff_packet','document_passport_refs','corpus_index_refs','system_mapping_refs','gap_detection_refs'],['function_mapping','required_system_assets','implementation_task_package','f00_handoff_packet'],['tools/f00_function_mapping.py']),
      ('func_003','V00 validation evidence','V00','Validate required outputs and preserve gaps',['k00_outputs','f00_outputs'],['validation_matrix','gap_register','evidence_report','v00_handoff_packet'],['tools/v00_validation_evidence.py']),
      ('func_004','A00 acceptance decision','A00','Decide READY_WITH_GAPS vs BLOCKED and block false claims',['validation_matrix','gap_register'],['acceptance_matrix','readiness_certificate','a00_acceptance_result'],['tools/a00_acceptance.py']),
      ('func_005','H00 downstream queue','H00','Route gaps and task refinements to downstream queue',['acceptance_result','gap_register','function_mapping'],['downstream_queue','routing_decision','h00_handoff_packets'],['tools/h00_downstream_queue.py']),
      ('func_006','U00 review upgrade','U00','Turn gaps into review cases/root causes/upgrade queue/learning index',['gap_register','downstream_queue'],['review_cases','root_cause_analysis','upgrade_queue','learning_index'],['tools/u00_review_upgrade.py']),
      ('func_007','G00 governance candidates','G00','Extract status/process/forbidden action governance candidates',['gap_register','acceptance_result'],['governance_candidates','policy_rules_update'],['tools/g00_governance_update.py']),
      ('func_008','O00 orchestration report','O00','Orchestrate full safe-mode manual run and write final report',['document','goal','safe_mode'],['run_summary','final_report','trace','audit'],['tools/o00_run_document_main.py','tools/her_pipeline_status.py'])]
    mapped=[]
    for fid,name,ctrl,desc,inputs,outputs,files in funcs:
        mapped.append({'function_id':fid,'function_name':name,'description':desc,'target_controller':ctrl,'required_inputs':inputs,'required_outputs':outputs,'required_fields':['status','refs','gap_policy','evidence_path'],'required_files':files,'required_tools':files,'validation_needed':True,'implementation_status':'TASK_REQUIRED'})
    mapping={'mapping_id':f'f00_mapping_{run_id}','source_doc_id':passport['doc_id'],'functional_intent':'real_document_to_function_pipeline','mapped_functions':mapped,'unmapped_items':['scheduler manual enable paused','operator confirmation packet paused','one-shot trial paused','paper/live runtime paused'], 'status':'F00_FUNCTION_MAPPING_READY_WITH_GAPS'}
    assets={'assets':[]}
    i=1
    for fn in mapped:
        for p in fn['required_files']:
            assets['assets'].append({'asset_id':f'asset_{i:03d}','asset_type':'tool' if p.startswith('tools/') else 'schema','path':p,'purpose':fn['description'],'required_by':fn['function_id'],'status':'CREATED_OR_UPDATED_WITH_GAPS'}); i+=1
    tasks={'task_package_id':f'f00_task_package_{run_id}','source_mapping':'f00/function_mapping.json','tasks':[{'task_id':f"task_{fn['function_id']}", 'target_controller':fn['target_controller'], 'required_outputs':fn['required_outputs'], 'status':'TASK_REQUIRED_NOT_IMPLEMENTED_EVIDENCE'} for fn in mapped], 'status':'IMPLEMENTATION_TASK_PACKAGE_READY_WITH_GAPS'}
    handoff={'handoff_id':f'f00_handoff_{run_id}','from_phase':'F00','to_phase':'V00','status':'F00_HANDOFF_READY_WITH_GAPS','refs':{'function_mapping':'f00/function_mapping.json','required_system_assets':'f00/required_system_assets.json','implementation_task_package':'f00/implementation_task_package.json'},'gaps':[{'gap_id':'gap_mapping_not_production_implementation','gap_level':'HIGH_GAP','route_to':'V00','status':'OPEN'}]}
    write_json(run_dir/'f00/function_mapping.json', mapping)
    write_json(run_dir/'f00/required_system_assets.json', assets)
    write_json(run_dir/'f00/implementation_task_package.json', tasks)
    write_json(run_dir/'f00/f00_handoff_packet.json', handoff)
    trace(run_dir, run_id, 'F00', 'function_mapping_written', 'WRITTEN', output='f00/function_mapping.json')
    trace(run_dir, run_id, 'F00', 'phase_completed', 'F00_FUNCTION_MAPPING_READY_WITH_GAPS')
    return handoff
