from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from modules.stable_trader_os.adapters.gmgn_source_wallet_to_phase01 import build_phase01_input_from_source_wallet_run
from modules.stable_trader_os.handoff_translator import translate_bot2_handoff_to_phase01
from modules.stable_trader_os.phase_02_wallet_structure_controller.runner import Phase02WalletStructureController


ROOT = Path('/root/sikk-gmgn')
FIXTURE_RUN = ROOT / 'data/stable_trader_os/runs/ca_system_gap_8BuGJvmz_20260509T051529Z'
TOKEN = '8BuGJvmzrtKg1Pq31pdcabFk5UVdvykAYqNqPfWGpump'


def test_real_ca_source_wallet_run_builds_phase01_input_contract(tmp_path: Path):
    output = tmp_path / 'phase01_input.json'

    payload = build_phase01_input_from_source_wallet_run(
        token_address=TOKEN,
        source_wallet_run_dir=FIXTURE_RUN / 'source_wallet_bot',
        output_file=output,
        run_id='test_real_ca_phase01_adapter',
    )

    assert output.exists()
    assert payload['run_id'] == 'test_real_ca_phase01_adapter'
    assert payload['token_address'] == TOKEN
    assert payload['chain'] == 'sol'
    assert payload['run_mode'] == 'real_ca_readonly'
    assert payload['data_snapshot_time'] != 'missing'
    assert set(['gmgn_traders', 'gmgn_holders']).issubset(payload['sources'])
    for rel_path in payload['sources'].values():
        assert (output.parent / rel_path).exists(), rel_path


def test_bot2_handoff_translates_to_stable_phase01_handoff_packet(tmp_path: Path):
    bot2 = FIXTURE_RUN / 'source_wallet_bot/structure_analysis/handoff/bot2_handoff_packet.json'
    phase01_normalized = FIXTURE_RUN / 'source_wallet_bot/wallet_data/normalized/wallet_trade_normalized.json'
    output = tmp_path / 'phase_01_handoff_packet.json'

    packet = translate_bot2_handoff_to_phase01(
        bot2_handoff_file=bot2,
        phase01_output_dir=tmp_path,
        output_file=output,
        run_id='test_translate_bot2',
        phase01_gate_status='PASS_WITH_WARNING',
        required_fact_files={'wallet_trade_source_json': str(phase01_normalized)},
    )

    assert output.exists()
    assert packet['phase'] == 'phase_01_data_fact_controller'
    assert packet['next_stage'] == 'phase_02_wallet_structure_controller'
    assert packet['allow_next_stage'] is True
    assert packet['phase_status'] == 'PASS_WITH_WARNING'
    assert packet['token_address'] == TOKEN
    assert 'wallet_trade_source_json' in packet['required_files_for_next_stage']
    assert packet['hard_negative_triggered'] is False
    assert isinstance(packet['missing_fields'], list)


def test_phase02_controller_wraps_wallet_structure_with_contract_audit_and_handoff(tmp_path: Path):
    phase01_input = build_phase01_input_from_source_wallet_run(
        token_address=TOKEN,
        source_wallet_run_dir=FIXTURE_RUN / 'source_wallet_bot',
        output_file=tmp_path / 'phase01_input.json',
        run_id='test_phase02_controller',
    )
    phase01_handoff = translate_bot2_handoff_to_phase01(
        bot2_handoff_file=FIXTURE_RUN / 'source_wallet_bot/structure_analysis/handoff/bot2_handoff_packet.json',
        phase01_output_dir=tmp_path,
        output_file=tmp_path / 'phase_01_handoff_packet.json',
        run_id='test_phase02_controller',
        phase01_gate_status='PASS_WITH_WARNING',
        required_fact_files={'gmgn_traders': str((tmp_path / phase01_input['sources']['gmgn_traders']).resolve())},
    )

    result = Phase02WalletStructureController().run(
        phase01_handoff_file=tmp_path / 'phase_01_handoff_packet.json',
        output_dir=tmp_path / 'phase02',
    )

    assert result['phase_status'] in {'WALLET_SUPPORT', 'WALLET_PAUSE', 'WALLET_BLOCK', 'WALLET_UNKNOWN', 'WALLET_DATA_WEAK'}
    assert Path(result['artifacts']['wallet_structure_decision']).exists()
    assert Path(result['artifacts']['audit_report']).exists()
    assert Path(result['artifacts']['handoff_packet']).exists()
    assert Path(result['artifacts']['handoff_validation_report']).exists()

    handoff = json.loads(Path(result['artifacts']['handoff_packet']).read_text())
    assert handoff['phase'] == 'phase_02_wallet_structure_controller'
    assert handoff['token_address'] == TOKEN
    assert 'positive_evidence' in handoff
    assert 'negative_evidence' in handoff
    assert 'missing_fields' in handoff
    assert handoff['phase_status'] == result['phase_status']

    audit = Path(result['artifacts']['audit_report']).read_text(encoding='utf-8')
    assert 'Phase 02 Wallet Structure Controller Audit' in audit
    assert 'Atomic Skill' in audit
    assert 'hard negative' in audit

    classification = Path(result['artifacts']['wallet_classification'])
    assert classification.exists()
    with classification.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    assert rows
    assert 'wallet_address' in rows[0]
