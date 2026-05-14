from pathlib import Path

MODULE_EXPORTS = {
    'modules.wallet_path_resolver': [
        'resolve_standard_path',
        'resolve_token_index',
        'resolve_wallet_data_path',
        'load_records_with_priority',
    ],
    'modules.wallet_schema_validator': [
        'validate_required_keys',
        'validate_json_file',
        'validate_source_wallet_design_package',
        'validate_handoff_packet',
    ],
    'modules.wallet_collectors': [
        'collect_gmgn_token_wallet_rows',
        'collect_and_build_source_wallet_packet',
        'gmgn_holder_rows_to_trade_rows',
    ],
    'modules.wallet_structure_pipeline': [
        'run_candidate_wallet_structure_pipeline',
        'default_gmgn_wallet_collector',
    ],
    'modules.wallet_structure_gate': [
        'WalletStructureDecision',
        'evaluate_wallet_structure_gate',
        'evaluate_and_write_wallet_structure',
    ],
    'modules.wallet_same_source_grouping': [
        'same_source_similarity_score',
        'compute_sync_buy_score',
        'compute_sync_sell_score',
        'build_same_source_groups',
    ],
    'modules.wallet_chip_control': [
        'ChipControlDecision',
        'evaluate_chip_control_state',
    ],
    'modules.wallet_candidate_state_machine': [
        'run_candidate_state_machine',
    ],
}


def test_remaining_l2_modules_have_l3_public_api_and_docs():
    for module_name, exports in MODULE_EXPORTS.items():
        module = __import__(module_name, fromlist=['*'])
        assert hasattr(module, '__all__'), module_name
        for exported in exports:
            assert hasattr(module, exported), f'{module_name}.{exported}'
            assert exported in module.__all__, f'{module_name}.__all__ missing {exported}'
        module_dir = Path('/root/sikk-gmgn') / module_name.replace('.', '/')
        readme = module_dir / 'README.md'
        assert readme.exists(), str(readme)
        text = readme.read_text(encoding='utf-8')
        assert 'L3' in text
        assert '旧入口' in text
        assert '不执行真实交易' in text
        assert '不签名' in text
        assert '不广播' in text
