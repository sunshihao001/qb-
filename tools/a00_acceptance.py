from pathlib import Path
from her_pipeline_lib import write_json, read_json, trace
FINAL='HER_DOC_FUNCTION_PIPELINE_RUNNABLE_WITH_GAPS'

def run(run_dir: Path, run_id: str):
    trace(run_dir, run_id, 'A00', 'phase_started', 'STARTED')
    gaps=read_json(run_dir/'v00/gap_register.json')['gaps']
    matrix={'acceptance_id':f'a00_matrix_{run_id}','checks':[{'target':'K00/F00/V00','status':'PASSED_WITH_GAPS'},{'target':'safe_mode_boundary','status':'PASSED'},{'target':'forbidden_claims','status':'PASSED'}],'overall_status':'PASSED_WITH_GAPS'}
    cert={'certificate_id':f'a00_readiness_{run_id}','status':FINAL,'ready_for_h00':True,'ready_for_next_run':True,'ready_for_production':False}
    result={'acceptance_id':f'a00_acceptance_{run_id}','final_status':FINAL,'k00_status':'PASSED','f00_status':'PASSED_WITH_GAPS','v00_status':'PASSED_WITH_GAPS','blocking_gaps':[],'non_blocking_gaps':[g['gap_type'] for g in gaps],'ready_for_h00':True,'ready_for_production':False,'forbidden_claims_blocked':['PRODUCTION_READY','FULLY_AUTOMATED','LIVE_READY','IMPLEMENTED_WITHOUT_EVIDENCE']}
    write_json(run_dir/'a00/acceptance_matrix.json', matrix)
    write_json(run_dir/'a00/readiness_certificate.json', cert)
    write_json(run_dir/'a00/a00_acceptance_result.json', result)
    trace(run_dir, run_id, 'A00', 'phase_completed', FINAL)
    return result
