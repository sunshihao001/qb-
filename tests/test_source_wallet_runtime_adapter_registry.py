import json
from pathlib import Path


def _write_adapter(path: Path, adapter_type: str, source_file: str, priority: str = 'P1'):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        'artifact_type': 'wallet_structure_gap_runtime_adapter',
        'adapter_type': adapter_type,
        'source_file': source_file,
        'priority': priority,
        'runtime_contract': {'read_mode': 'readonly'},
        'automation_policy': {'delete_old_files': False, 'paper_only': True},
    }, ensure_ascii=False), encoding='utf-8')


def test_runtime_adapter_registry_builds_index_and_validates_targets(tmp_path):
    from modules.source_wallet_bot.runtime_adapter_registry import build_runtime_adapter_registry

    root = tmp_path
    adapter_root = root / 'research_loop/state/apply/runtime_adapters'
    _write_adapter(adapter_root / 'legacy_path_map_runtime_adapter/a.json', 'legacy_path_map_runtime_adapter', 'legacy_compat/path_maps/a.json', 'P0')
    _write_adapter(adapter_root / 'schema_contract_runtime_adapter/b.json', 'schema_contract_runtime_adapter', 'contracts/shared/README.md', 'P1')
    _write_adapter(adapter_root / 'wallet_data_passport_runtime_adapter/c.json', 'wallet_data_passport_runtime_adapter', 'research_loop/methodology/passports/x.md', 'P2')

    result = build_runtime_adapter_registry(project_root=root, adapter_state_dir=root / 'research_loop/state/apply', output_dir=root / 'research_loop/state/integration')

    assert result['status'] == 'PASS'
    assert result['total_adapters'] == 3
    assert result['by_adapter_type']['legacy_path_map_runtime_adapter'] == 1
    assert result['integration_targets']['legacy_path_map_runtime_adapter']['target'] == 'modules/source_wallet_bot/path_resolver.py'
    assert Path(result['registry_path']).exists()
    registry = json.loads(Path(result['registry_path']).read_text(encoding='utf-8'))
    assert registry['automation_policy']['delete_old_files'] is False
    assert registry['adapter_groups']['schema_contract_runtime_adapter'][0]['source_file'] == 'contracts/shared/README.md'


def test_schema_validator_includes_runtime_adapter_registry(tmp_path):
    from modules.source_wallet_bot.schema_validator import validate_runtime_adapter_registry

    registry = {
        'artifact_type': 'wallet_structure_runtime_adapter_registry',
        'total_adapters': 2,
        'adapter_groups': {
            'legacy_path_map_runtime_adapter': [{'artifact_path': 'a', 'source_file': 'legacy_compat/path_maps/a.json'}],
            'schema_contract_runtime_adapter': [{'artifact_path': 'b', 'source_file': 'contracts/shared/README.md'}],
        },
        'integration_targets': {
            'legacy_path_map_runtime_adapter': {'target': 'modules/source_wallet_bot/path_resolver.py'},
            'schema_contract_runtime_adapter': {'target': 'modules/source_wallet_bot/schema_validator.py'},
        },
    }
    result = validate_runtime_adapter_registry(registry)
    assert result['ok'] is True
    assert result['total_adapters'] == 2
    assert result['required_groups_status']['legacy_path_map_runtime_adapter'] == 'PASS'
    assert result['required_groups_status']['schema_contract_runtime_adapter'] == 'PASS'
