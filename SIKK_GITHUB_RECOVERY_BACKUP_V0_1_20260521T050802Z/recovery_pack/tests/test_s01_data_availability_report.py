from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def run_id(): return (ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
def s01(): return ROOT/'data/runs'/run_id()/'s01_data_source_r02_r03'

def test_data_availability_report():
    d=json.loads((s01()/'data_availability_report.json').read_text())
    types={i['data_type'] for i in d['items']}
    for t in ['token_identity','market_pool','kline_price_volume','holder_data','smart_holder_data','trader_profit_data','wallet_profile_data','security_data','okx_quote_if_available','historical_data_foundation']:
        assert t in types
