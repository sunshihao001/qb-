
from pathlib import Path
import json, csv
from src.phase_01_data_fact.phase_01_runner import run_phase_01

ROOT=Path('/root/sikk-gmgn')
FIX=ROOT/'tests/fixtures/phase_01_data_fact'
TOKEN='MockToken1111111111111111111111111111111111'
CHAIN='solana'

def run_case(tmp_path, fixture, mode='replay'):
    return run_phase_01(mode, TOKEN, CHAIN, FIX/fixture, tmp_path/'out', tmp_path/'shared_handoff', snapshot_time='2026-05-09T15:00:00Z')

def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def test_valid_raw_ready_generates_required_outputs(tmp_path):
    res=run_case(tmp_path,'valid_raw')
    assert res['data_quality_status'] == 'DATA_OK'
    assert res['handoff_status'] == 'HANDOFF_READY'
    run_dir=Path(res['run_dir'])
    for rel in ['raw/copied_raw_files','normalized','summary','handoff','reports','audit','manifest']:
        assert (run_dir/rel).exists()
    for rel in ['summary/data_quality_summary.json','summary/time_validity_report.json','handoff/phase_01_handoff_packet.json','normalized/token_basic_normalized.json','normalized/token_market_context.json','normalized/wallet_trade_normalized.csv','normalized/holder_normalized.csv']:
        assert (run_dir/rel).exists()
    assert Path(res['shared_handoff']).exists()
    assert load_json(run_dir/'handoff/phase_01_handoff_packet.json') == load_json(res['shared_handoff'])
    packet=load_json(res['local_handoff'])
    assert packet['allowed_next_stage'] == 'phase_02_wallet_structure'
    assert packet['handoff_status'] == 'HANDOFF_READY'

def test_missing_optional_degrades_not_blocks(tmp_path):
    res=run_case(tmp_path,'missing_optional_raw')
    assert res['data_quality_status'] == 'DATA_PARTIAL'
    assert res['handoff_status'] == 'HANDOFF_DEGRADED'
    packet=load_json(res['local_handoff'])
    assert 'raw_transfer.json' in packet['missing_fields']
    assert 'transfer_missing_no_distribution_inference' in packet['degrade_reason']

def test_missing_transfer_degrades_and_keeps_inference_guard(tmp_path):
    res=run_case(tmp_path,'missing_transfer')
    assert res['data_quality_status'] == 'DATA_PARTIAL'
    run_dir=Path(res['run_dir'])
    rows=list(csv.DictReader((run_dir/'normalized'/'transfer_normalized.csv').open(encoding='utf-8')))
    assert rows[0]['inference_guard'] == 'missing_transfer_no_distribution_or_backflow_judgement'


def test_missing_wallet_address_blocks(tmp_path):
    res=run_case(tmp_path,'missing_wallet_address')
    assert res['data_quality_status'] == 'DATA_INVALID'
    assert res['handoff_status'] == 'HANDOFF_BLOCKED'
    packet=load_json(res['local_handoff'])
    assert packet['hard_negative_triggered'] is True
    assert any('wallet_address' in x for x in packet['hard_negative_reasons'])


def test_missing_kline_blocks(tmp_path):
    res=run_case(tmp_path,'missing_kline')
    assert res['data_quality_status'] == 'DATA_INVALID'
    assert res['handoff_status'] == 'HANDOFF_BLOCKED'
    assert any('raw_kline.json' in x for x in res['blocking_issues'])


def test_stale_quote_refresh_required(tmp_path):
    res=run_case(tmp_path,'stale_quote')
    assert res['data_quality_status'] == 'DATA_STALE'
    assert res['handoff_status'] == 'HANDOFF_REFRESH_REQUIRED'


def test_missing_quote_security_blocks(tmp_path):
    res=run_case(tmp_path,'missing_quote_security')
    assert res['data_quality_status'] == 'DATA_INVALID'
    assert any('raw_quote_security.json' in x for x in res['blocking_issues'])


def test_no_forbidden_downstream_statuses_in_outputs(tmp_path):
    res=run_case(tmp_path,'valid_raw')
    forbidden={'WALLET_SUPPORT','CONTROL_RETAINED','SCENARIO_ALLOW','PAPER_READY'}
    text='\n'.join(p.read_text(encoding='utf-8', errors='ignore') for p in Path(res['run_dir']).rglob('*') if p.is_file())
    # allowed only inside explicit forbidden scope report, not as status fields
    for s in forbidden:
        assert f'"{s}"' not in load_json(Path(res['run_dir'])/'handoff'/'phase_01_handoff_packet.json').get('phase_status','')
