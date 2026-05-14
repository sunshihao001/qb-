from pathlib import Path

from modules.source_wallet_bot.config import SourceWalletBotConfig
from modules.source_wallet_bot.io_utils import read_json, write_json
from modules.source_wallet_bot.models import WalletTradeRecord


def test_config_paths_are_isolated_under_source_wallet_bot():
    cfg = SourceWalletBotConfig(project_root=Path('/tmp/sikk-gmgn'))
    assert str(cfg.module_dir).endswith('modules/source_wallet_bot')
    assert str(cfg.data_dir).endswith('data/source_wallet_bot')
    assert 'paper' not in str(cfg.data_dir)
    assert 'state_machine' not in str(cfg.data_dir)


def test_json_roundtrip(tmp_path):
    path = tmp_path / 'sample.json'
    payload = {'token_address': 'TOKEN', 'missing_fields': ['wallet_snapshot_time']}
    write_json(path, payload)
    assert read_json(path) == payload


def test_wallet_trade_record_to_dict_has_required_fields():
    record = WalletTradeRecord(token_address='TOKEN', wallet_address='WALLET')
    data = record.to_dict()
    assert data['token_address'] == 'TOKEN'
    assert data['wallet_address'] == 'WALLET'
    assert data['first_buy_time'] == 'missing'
    assert data['buy_count'] == 0
    assert 'PAPER_READY' not in data
    assert 'final_trade_gate' not in data
