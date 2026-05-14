import json
from pathlib import Path

from tools.validate_directory_constitution import validate_project_constitution, route_source_wallet_asset


def test_route_source_wallet_asset_returns_constitution_path():
    path = route_source_wallet_asset('live', 'TOKEN', 'wallet_trade_normalized.json')
    assert path == Path('data/source_wallet_bot/live/TOKEN/wallet_data/normalized/wallet_trade_normalized.json')


def test_validate_project_constitution_accepts_current_project():
    result = validate_project_constitution(Path('/root/sikk-gmgn'))
    assert result['status'] == 'PASS'
    assert result['constitution_exists'] is True
    assert result['routes_exists'] is True
    assert result['source_wallet_layout_ok'] is True
    assert result['manifest_json_ok'] is True
