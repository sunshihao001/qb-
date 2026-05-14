import json
from pathlib import Path


def test_pipeline_config_safe_mode_and_boundary():
    path = Path('/root/sikk-gmgn/system/her_document_function_system/config/pipeline_config.full_safe_replay.json')
    data = json.loads(path.read_text())
    assert data['safe_mode'] is True
    boundary = data.get('execution_boundary', {})
    assert boundary.get('allow_live_runtime') is False
    assert boundary.get('allow_wallet_signing') is False
    assert boundary.get('allow_auto_deploy') is False
    assert boundary.get('allow_production_trading') is False
