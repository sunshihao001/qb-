from pathlib import Path
from her_pipeline_lib import write_json, read_json, trace

def run(run_dir: Path, run_id: str):
    trace(run_dir, run_id, 'U00', 'phase_started', 'STARTED')
    gaps=read_json(run_dir/'v00/gap_register.json')['gaps']
    review=[]; roots=[]; upgrades=[]
    for i,g in enumerate(gaps,1):
        review.append({'review_case_id':f'review_{i:03d}','source_gap':g['gap_id'],'gap_level':g['gap_level'],'status':'OPEN'})
        roots.append({'root_cause_id':f'root_{i:03d}','source_gap':g['gap_id'],'root_cause':'Pipeline intentionally separates mapping/evidence/production readiness; remaining work requires later hardening.', 'status':'IDENTIFIED'})
        upgrades.append({'upgrade_item_id':f'upgrade_{i:03d}','source_gap':g['gap_id'],'target_controller':'F00' if g['origin_phase']=='F00' else g['route_to'],'upgrade_type':'FUNCTION_MAPPING_HARDENING' if g['origin_phase']=='F00' else 'PIPELINE_GAP_HARDENING','description':'Improve real-run evidence separation and downstream closure.', 'priority':'P1_HIGH' if g['gap_level']=='HIGH_GAP' else 'P2_MEDIUM','status':'QUEUED'})
    write_json(run_dir/'u00/review_cases.json', {'review_cases':review,'status':'REVIEW_CASES_READY_WITH_GAPS'})
    write_json(run_dir/'u00/root_cause_analysis.json', {'root_causes':roots,'status':'ROOT_CAUSE_READY_WITH_GAPS'})
    write_json(run_dir/'u00/upgrade_queue.json', {'upgrade_queue_id':f'u00_upgrade_queue_{run_id}','queue_status':'UPGRADE_QUEUE_READY_WITH_GAPS','items':upgrades})
    write_json(run_dir/'u00/learning_index.json', {'lessons':[{'lesson_id':'lesson_no_ready_without_evidence','statement':'mapping/task package is not implementation evidence'},{'lesson_id':'lesson_queue_not_completed','statement':'queue creation is routing evidence, not task completion'}], 'status':'LEARNING_INDEX_READY_WITH_GAPS'})
    trace(run_dir, run_id, 'U00', 'phase_completed', 'UPGRADE_QUEUE_READY_WITH_GAPS')
    return upgrades
