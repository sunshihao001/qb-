import json
from pathlib import Path


def _registry(tmp_path: Path):
    return {
        'artifact_type': 'wallet_structure_runtime_adapter_registry',
        'total_adapters': 5,
        'adapter_groups': {
            'legacy_path_map_runtime_adapter': [{'artifact_path': 'a', 'source_file': 'legacy_compat/path_maps/a.json'}],
            'legacy_manifest_runtime_adapter': [{'artifact_path': 'b', 'source_file': 'legacy_compat/manifests/b.json'}],
            'wallet_data_passport_runtime_adapter': [{'artifact_path': 'c', 'source_file': 'research_loop/methodology/passports/c.md'}],
            'schema_contract_runtime_adapter': [{'artifact_path': 'd', 'source_file': 'contracts/shared/README.md'}],
            'interface_inventory_runtime_adapter': [{'artifact_path': 'e', 'source_file': 'docs/source_wallet_bot/directory_governance/e.md'}],
        },
        'integration_targets': {
            'legacy_path_map_runtime_adapter': {'target': 'modules/source_wallet_bot/path_resolver.py'},
            'legacy_manifest_runtime_adapter': {'target': 'modules/source_wallet_bot/path_resolver.py'},
            'wallet_data_passport_runtime_adapter': {'target': 'modules/wallet_data_guard/source_manifest.py'},
            'schema_contract_runtime_adapter': {'target': 'modules/source_wallet_bot/schema_validator.py'},
            'interface_inventory_runtime_adapter': {'target': 'modules/source_wallet_bot/system_gap_scanner.py'},
        },
        'automation_policy': {'delete_old_files': False, 'paper_only': True},
    }


def test_target_modules_consume_runtime_adapter_registry(tmp_path):
    from modules.source_wallet_bot.path_resolver import consume_runtime_adapter_registry as consume_path_registry
    from modules.wallet_data_guard.source_manifest import consume_passport_runtime_adapters
    from modules.source_wallet_bot.schema_validator import consume_schema_contract_runtime_adapters
    from modules.source_wallet_bot.system_gap_scanner import consume_interface_inventory_runtime_adapters

    reg = _registry(tmp_path)
    path_result = consume_path_registry(reg)
    passport_result = consume_passport_runtime_adapters(reg)
    schema_result = consume_schema_contract_runtime_adapters(reg)
    inventory_result = consume_interface_inventory_runtime_adapters(reg)

    assert path_result['status'] == 'PASS'
    assert path_result['legacy_path_map_adapters'] == 1
    assert path_result['legacy_manifest_adapters'] == 1
    assert passport_result['status'] == 'PASS'
    assert passport_result['passport_adapters'] == 1
    assert schema_result['status'] == 'PASS'
    assert schema_result['schema_contract_adapters'] == 1
    assert inventory_result['status'] == 'PASS'
    assert inventory_result['interface_inventory_adapters'] == 1


def test_full_registry_consumption_runner_writes_report(tmp_path):
    from sikk_wallet_structure_consume_runtime_registry import consume_runtime_registry

    registry_path = tmp_path / 'runtime_adapter_registry.json'
    registry_path.write_text(json.dumps(_registry(tmp_path), ensure_ascii=False), encoding='utf-8')
    result = consume_runtime_registry(project_root=tmp_path, registry_path=registry_path, output_dir=tmp_path / 'out')

    assert result['status'] == 'PASS'
    assert Path(result['report_path']).exists()
    report = json.loads(Path(result['report_path']).read_text(encoding='utf-8'))
    assert report['target_consumption']['path_resolver']['status'] == 'PASS'
    assert report['target_consumption']['source_manifest']['status'] == 'PASS'
    assert report['target_consumption']['schema_validator']['status'] == 'PASS'
    assert report['target_consumption']['system_gap_scanner']['status'] == 'PASS'
