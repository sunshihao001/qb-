import json
from pathlib import Path

from modules.source_wallet_bot.wallet_fact_builder import build_wallet_fact_package


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def test_build_wallet_fact_package_creates_wallet_data_outputs(tmp_path):
    token = 'TOKEN'
    _write(tmp_path / 'wallet_trade_normalized.json', {'record_count': 1, 'records': [{
        'token_address': token,
        'wallet_address': 'W1',
        'first_buy_time': '2026-05-01T00:00:00Z',
        'buy_amount_usd': 100,
        'sell_amount_usd': 200,
        'current_balance': 10,
        'sold_pct': 50,
        'remaining_pct': 50,
        'realized_profit': 80,
        'unrealized_profit': 20,
        'total_profit': 100,
        'pnl_multiple': 2,
        'is_full_exit': False,
        'is_partial_exit': True,
    }]})
    _write(tmp_path / 'wallet_entity_profile_normalized.json', {'record_count': 1, 'records': [{
        'wallet_address': 'W1',
        'wallet_first_seen_time': '2026-04-01T00:00:00Z',
        'wallet_last_active_time': '2026-05-01T00:00:00Z',
        'gmgn_tags': ['bundler', 'fresh_wallet'],
        'funding_source_address': 'FUND',
        'evidence_level': 'E2',
    }]})
    _write(tmp_path / 'same_source_evidence_normalized.json', {'record_count': 0, 'records': []})
    _write(tmp_path / 'wallet_intelligence_decision.json', {'record_count': 1, 'records': [{
        'token_address': token,
        'wallet_address': 'W1',
        'role_candidates': ['疑似结构执行钱包'],
        'evidence_level': 'E2',
        'risk_level': 'R1',
    }]})
    result = build_wallet_fact_package(token, tmp_path)
    assert Path(result['wallet_structure_normalized']).exists()
    assert Path(result['chip_distribution_summary']).exists()
    assert Path(result['fund_flow_edges']).exists()
    summary = json.loads((tmp_path / 'wallet_data' / 'chip_distribution_summary.json').read_text(encoding='utf-8'))
    assert summary['wallet_count'] == 1
    assert summary['structure_wallet_candidate_count'] == 1
