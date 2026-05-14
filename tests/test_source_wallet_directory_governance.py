import json
from pathlib import Path

from modules.source_wallet_bot.directory_governance import apply_directory_governance


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def test_apply_directory_governance_copies_without_deleting_old_files(tmp_path):
    token = 'TOKEN'
    _write(tmp_path / 'gmgn_wallet_rows_raw.json', {'raw': True})
    _write(tmp_path / 'wallet_trade_normalized.json', {'record_count': 0, 'records': []})
    _write(tmp_path / 'wallet_intelligence_decision.json', {'record_count': 0, 'records': []})
    _write(tmp_path / 'bot2_handoff_packet.json', {'token_address': token})
    _write(tmp_path / 'wallet_fact' / 'wallet_fact_report.md', {'not': 'markdown but ok for copy'})
    result = apply_directory_governance(token, tmp_path)
    assert (tmp_path / 'gmgn_wallet_rows_raw.json').exists()
    assert (tmp_path / 'wallet_data' / 'raw' / 'gmgn_wallet_rows_raw.json').exists()
    assert (tmp_path / 'wallet_data' / 'normalized' / 'wallet_trade_normalized.json').exists()
    assert (tmp_path / 'structure_analysis' / 'intelligence' / 'wallet_intelligence_decision.json').exists()
    assert (tmp_path / 'structure_analysis' / 'handoff' / 'bot2_handoff_packet.json').exists()
    manifest = json.loads((tmp_path / 'manifest' / 'token_output_manifest.json').read_text(encoding='utf-8'))
    assert manifest['token_address'] == token
    assert manifest['policy']['delete_old_files'] is False
    assert any(m['old_path'].endswith('wallet_trade_normalized.json') for m in manifest['path_mappings'])
    assert result['manifest'].endswith('token_output_manifest.json')


def test_apply_directory_governance_accepts_standard_layout_without_root_legacy_source(tmp_path):
    token = 'TOKEN'
    _write(tmp_path / 'wallet_data/raw/gmgn_wallet_rows_raw.json', {'raw': True})
    _write(tmp_path / 'wallet_data/normalized/wallet_trade_normalized.json', {'record_count': 0, 'records': []})
    _write(tmp_path / 'structure_analysis/intelligence/wallet_intelligence_decision.json', {'record_count': 0, 'records': []})
    _write(tmp_path / 'structure_analysis/handoff/bot2_handoff_packet.json', {'token_address': token})

    result = apply_directory_governance(token, tmp_path)
    manifest = json.loads((tmp_path / 'manifest/token_output_manifest.json').read_text(encoding='utf-8'))

    assert result['primary_write_layout'] == 'standard_source_wallet_token_layout'
    assert manifest['policy']['legacy_root_as_primary_write'] is False
    assert manifest['policy']['standard_layout_as_primary_write'] is True
    assert not any(
        item == 'wallet_trade_normalized.json'
        for item in manifest['missing_sources']
    )
    assert any(
        m['new_path'].endswith('wallet_data/normalized/wallet_trade_normalized.json') and m['action'] in {'kept_standard', 'copied'}
        for m in manifest['path_mappings']
    )
