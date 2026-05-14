from pathlib import Path
from her_pipeline_lib import write_json, read_json, trace

def run(run_dir: Path, run_id: str):
    trace(run_dir, run_id, 'H00', 'phase_started', 'STARTED')
    gaps=read_json(run_dir/'v00/gap_register.json')['gaps']
    items=[]
    for i,g in enumerate(gaps,1):
        if g['gap_level'] in ['HIGH_GAP','CRITICAL_GAP','MEDIUM_GAP']:
            items.append({'queue_item_id':f'queue_item_{i:03d}','source_gap':g['gap_id'],'target_controller':g['route_to'],'task_type':'REVIEW_AND_UPGRADE' if g['route_to']=='U00' else 'ROUTED_GAP_REVIEW','priority':'P1_HIGH' if g['gap_level']=='HIGH_GAP' else 'P2_MEDIUM','status':'QUEUED'})
    queue={'queue_id':f'h00_queue_{run_id}','queue_status':'QUEUE_READY_WITH_GAPS','items':items}
    routing={'routing_id':f'h00_routing_{run_id}','routing_status':'ROUTING_READY_WITH_GAPS','decisions':[{'source_gap':it['source_gap'],'target_controller':it['target_controller'],'decision':'QUEUE_NOT_EXECUTE'} for it in items]}
    packets={'handoff_packets':[{'handoff_id':f"h00_to_{it['target_controller']}_{it['queue_item_id']}", 'from_phase':'H00','to_phase':it['target_controller'],'status':'HANDOFF_READY_WITH_GAPS','refs':{'queue':'h00/downstream_queue.json'}} for it in items]}
    write_json(run_dir/'h00/downstream_queue.json', queue)
    write_json(run_dir/'h00/routing_decision.json', routing)
    write_json(run_dir/'h00/h00_handoff_packets.json', packets)
    trace(run_dir, run_id, 'H00', 'phase_completed', 'QUEUE_READY_WITH_GAPS')
    return queue
