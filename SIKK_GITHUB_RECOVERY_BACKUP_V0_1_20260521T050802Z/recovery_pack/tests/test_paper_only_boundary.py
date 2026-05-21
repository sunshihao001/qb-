import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_paper_only_boundary():
    latest=ROOT/'data/coordination/latest'
    forbidden_fields=['live_trading_enabled','swap_allowed','private_key_required','signing_allowed','broadcast_allowed']
    for path in latest.glob('*.json'):
        text=path.read_text(encoding='utf-8')
        for field in forbidden_fields:
            assert field not in text
    forbidden_outputs=['paper_position.json','paper_trades.csv','paper_equity_curve.csv','backtest_result.json','replay_case.json','attribution_report.json','upgrade_candidate.json']
    for name in forbidden_outputs:
        assert not (ROOT/name).exists()
        assert not (latest/name).exists()
