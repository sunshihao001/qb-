
from __future__ import annotations
import argparse,json
from pathlib import Path
if __package__ in (None,''):
    import sys; sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from src.phase_01_data_fact.utils import ensure_dirs,token_from_raw,write_json,utc_now
from src.phase_01_data_fact.input_loader import load_raw_inputs
from src.phase_01_data_fact.raw_snapshot_manager import create_raw_snapshot
from src.phase_01_data_fact.field_mapper import write_field_mapping
from src.phase_01_data_fact.token_basic_normalizer import normalize_token_basic
from src.phase_01_data_fact.token_market_context_builder import build_token_market_context
from src.phase_01_data_fact.wallet_trade_normalizer import normalize_wallet_trades
from src.phase_01_data_fact.holder_normalizer import normalize_holders
from src.phase_01_data_fact.top_trader_normalizer import normalize_top_traders
from src.phase_01_data_fact.transfer_normalizer import normalize_transfers
from src.phase_01_data_fact.kline_normalizer import normalize_kline
from src.phase_01_data_fact.quote_security_normalizer import normalize_quote_security
from src.phase_01_data_fact.time_validity_checker import check_time_validity
from src.phase_01_data_fact.data_quality_evaluator import evaluate_data_quality
from src.phase_01_data_fact.missing_fields_reporter import write_missing_fields_report
from src.phase_01_data_fact.handoff_writer import write_handoff
from src.phase_01_data_fact.phase_01_auditor import write_phase_audit

def run_phase_01(mode,token,chain,raw_input_dir,output_root,shared_handoff_root,snapshot_time=None,legacy_input_dir=None,strict=False):
    snapshot_time=snapshot_time or utc_now(); load=load_raw_inputs(raw_input_dir); raw=load['raw']; token_addr=token_from_raw(raw,token)
    run_dir=Path(output_root)/mode/token_addr/'phase_01_data_fact'; ensure_dirs(run_dir)
    snapshot=create_raw_snapshot(raw_input_dir,run_dir,snapshot_time); write_field_mapping(run_dir)
    tb,tb_missing=normalize_token_basic(raw,token_addr,chain,run_dir); mc,mc_missing=build_token_market_context(raw,run_dir)
    wt,wt_missing=normalize_wallet_trades(raw,run_dir); holders,holder_missing=normalize_holders(raw,run_dir); tt,tt_missing=normalize_top_traders(raw,run_dir)
    tr,tr_missing,tr_warnings=normalize_transfers(raw,run_dir); kl,kline_missing=normalize_kline(raw,run_dir); qs,qs_missing=normalize_quote_security(raw,run_dir)
    time_report=check_time_validity(snapshot_time,qs,run_dir)
    critical=list(wt_missing)+list(holder_missing)+list(kline_missing); optional=list(tb_missing)+list(mc_missing)+list(tt_missing)+list(tr_missing)+list(qs_missing)
    if qs.get('quote_time')=='missing': critical.append('quote_security.quote_time')
    quality=evaluate_data_quality(run_dir,load['missing_required_raw'],load['missing_optional_raw'],critical,optional,time_report,tr_warnings)
    missing_report=write_missing_fields_report(run_dir,quality)
    write_json(run_dir/'summary'/'phase_01_analysis_scope.json',{'phase':'phase_01_data_fact','scope':'data facts only','forbidden':['wallet_structure_status','WALLET_SUPPORT','CONTROL_RETAINED','SCENARIO_ALLOW','PAPER_READY','buy_signal']})
    packet,local,shared=write_handoff(run_dir,shared_handoff_root,token_addr,chain,snapshot,tb,quality,time_report)
    result={'task':'phase_01_data_fact_code_skeleton_landing','run_dir':str(run_dir),'token_address':token_addr,'data_quality_status':quality['data_quality_status'],'handoff_status':quality['handoff_status'],'local_handoff':str(local),'shared_handoff':str(shared),'blocking_issues':quality.get('blocked_fields',[]),'degraded_issues':quality.get('degraded_fields',[]),'missing_fields_report':str(missing_report)}
    audit=write_phase_audit(run_dir,result); packet['audit_file']=str(audit); write_json(local,packet); write_json(shared,packet)
    write_json(run_dir/'manifest'/'run_manifest.json',{**result,'snapshot_time':snapshot_time,'mode':mode,'chain':chain})
    write_json(run_dir/'manifest'/'manifest.json',{**result,'snapshot_time':snapshot_time,'mode':mode,'chain':chain,'handoff_packet':packet})
    (run_dir/'reports'/'audit_report.md').write_text((run_dir/'audit'/'phase_01_audit_report.md').read_text(encoding='utf-8'),encoding='utf-8')
    (run_dir/'reports'/'phase_01_data_fact_report.md').write_text(f"# P01 Data Fact Report\n\n- status: {quality['data_quality_status']}\n- handoff: {quality['handoff_status']}\n- P01 fact-only; no trading signal.\n",encoding='utf-8')
    return result

def main():
    p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['live','replay','backtest','paper','review','shadow'],required=True); p.add_argument('--token',required=True); p.add_argument('--chain',required=True); p.add_argument('--raw-input-dir',required=True); p.add_argument('--output-root',required=True); p.add_argument('--shared-handoff-root',required=True); p.add_argument('--snapshot-time'); p.add_argument('--legacy-input-dir'); p.add_argument('--strict',action='store_true')
    a=p.parse_args(); print(json.dumps(run_phase_01(a.mode,a.token,a.chain,a.raw_input_dir,a.output_root,a.shared_handoff_root,a.snapshot_time,a.legacy_input_dir,a.strict),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
