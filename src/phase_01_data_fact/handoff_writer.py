
from pathlib import Path
from .utils import write_json,utc_now

def write_handoff(run_dir, shared_handoff_root, token, chain, snapshot_manifest, token_basic, quality, time_validity):
    run=Path(run_dir)
    required_files={
        'phase_01_handoff_packet': run/'handoff'/'phase_01_handoff_packet.json',
        'data_quality_summary': run/'summary'/'data_quality_summary.json',
        'token_basic_normalized': run/'normalized'/'token_basic_normalized.json',
        'token_market_context': run/'normalized'/'token_market_context.json',
        'wallet_trade_normalized': run/'normalized'/'wallet_trade_normalized.csv',
        'holder_normalized': run/'normalized'/'holder_normalized.csv',
    }
    optional_files={
        'time_validity_report': run/'summary'/'time_validity_report.json',
        'kline_normalized': run/'normalized'/'kline_normalized.csv',
        'quote_security_normalized': run/'normalized'/'quote_security_normalized.json',
        'top_trader_normalized': run/'normalized'/'top_trader_normalized.csv',
        'transfer_normalized': run/'normalized'/'transfer_normalized.csv',
    }
    required_paths={k:str(v) for k,v in required_files.items()}
    optional_paths={k:str(v) for k,v in optional_files.items()}
    allow_next=quality['handoff_status'] in {'HANDOFF_READY','HANDOFF_DEGRADED'}
    packet={
        'phase':'phase_01_data_fact',
        'token_address':token,
        'token_symbol':token_basic.get('token_symbol','missing'),
        'chain':chain,
        'snapshot_id':snapshot_manifest.get('snapshot_id','missing'),
        'snapshot_time':snapshot_manifest.get('snapshot_time','missing'),
        'phase_status':quality['phase_status'],
        'primary_status':quality['primary_status'],
        'data_quality_status':quality['data_quality_status'],
        'time_validity_status':time_validity.get('time_validity_status','missing'),
        'handoff_status':quality['handoff_status'],
        'allow_next_stage':allow_next,
        'allowed_next_stage':'phase_02_wallet_structure' if allow_next else 'blocked',
        'next_stage':'phase_02_wallet_structure' if allow_next else 'blocked',
        'required_files_for_next_stage':required_paths,
        'optional_files_for_next_stage':optional_paths,
        'handoff_files':{**required_paths, **optional_paths},
        'required_context_for_next_stage':{
            'data_quality_status':quality['data_quality_status'],
            'time_validity_status':time_validity.get('time_validity_status','missing'),
            'required_normalized_files_available':all(Path(v).exists() for k,v in required_paths.items() if k!='phase_01_handoff_packet'),
            'p01_scope':'data_fact_only_no_wallet_structure_judgement'
        },
        'positive_evidence':['P01 normalized outputs generated','P01 data_quality_summary generated','P01 handoff packet generated'],
        'negative_evidence':quality.get('degraded_fields',[]),
        'counter_evidence':quality.get('blocked_fields',[]),
        'missing_fields':quality.get('critical_missing_fields',[])+quality.get('optional_missing_fields',[])+quality.get('missing_required_raw',[])+quality.get('missing_optional_raw',[]),
        'degrade_reason':'; '.join(quality.get('degraded_fields',[])),
        'block_reason':'; '.join(quality.get('blocked_fields',[])),
        'hard_negative_triggered':quality.get('hard_negative_triggered',False),
        'hard_negative_reasons':quality.get('hard_negative_reasons',[]),
        'audit_file':str(run/'audit'/'phase_01_audit_report.md'),
        'created_at':utc_now()
    }
    local=run/'handoff'/'phase_01_handoff_packet.json'
    shared=Path(shared_handoff_root)/'data_fact'/token/'phase_01_handoff_packet.json'
    write_json(local,packet); write_json(shared,packet)
    return packet,local,shared
