import json
import subprocess
import sys


def test_runner_validate_package_command_passes():
    result = subprocess.run(
        [sys.executable, '-m', 'modules.source_wallet_bot.runner', 'validate-package', '--root', '/root/sikk-gmgn'],
        cwd='/root/sikk-gmgn',
        env={'PYTHONPATH': '/root/sikk-gmgn'},
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert 'SOURCE_WALLET_BOT_IMPLEMENTATION_PACKAGE_OK' in result.stdout


def test_runner_normalize_wallet_trade_writes_output(tmp_path):
    input_path = tmp_path / 'raw.json'
    output_path = tmp_path / 'wallet_trade_normalized.json'
    input_path.write_text(json.dumps([
        {'token_address': 'TOKEN', 'wallet_address': 'W1', 'side': 'buy', 'timestamp': '2026-05-01T00:00:00Z', 'amount_usd': 100, 'token_amount': 1000}
    ]), encoding='utf-8')
    result = subprocess.run(
        [sys.executable, '-m', 'modules.source_wallet_bot.runner', 'normalize-wallet-trade', '--input', str(input_path), '--output', str(output_path)],
        cwd='/root/sikk-gmgn',
        env={'PYTHONPATH': '/root/sikk-gmgn'},
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(output_path.read_text(encoding='utf-8'))
    assert payload['record_count'] == 1
    assert payload['records'][0]['token_address'] == 'TOKEN'
