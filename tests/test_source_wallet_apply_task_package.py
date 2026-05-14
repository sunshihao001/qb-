import json
from pathlib import Path


def test_runtime_adapters_process_p0_actions(tmp_path):
    from modules.source_wallet_bot.system_gap_runtime_adapters import apply_gap_action

    root = tmp_path
    source = root / 'docs/source_wallet_bot/directory_governance/file_level_inventory_summary.md'
    source.parent.mkdir(parents=True)
    source.write_text('# Inventory\nfile level inventory summary\n', encoding='utf-8')

    action = {
        'order': 1,
        'priority': 'P0',
        'source_file': 'docs/source_wallet_bot/directory_governance/file_level_inventory_summary.md',
        'capability': 'interface_inventory',
        'action': 'create_runtime_adapter',
        'target_module': 'modules/source_wallet_bot/',
    }
    result = apply_gap_action(root, action, output_dir=root / 'research_loop/state/apply')

    assert result['status'] == 'APPLIED'
    assert result['priority'] == 'P0'
    assert result['artifact_path']
    artifact = Path(result['artifact_path'])
    assert artifact.exists()
    payload = json.loads(artifact.read_text(encoding='utf-8'))
    assert payload['source_file'] == action['source_file']
    assert payload['adapter_type'] == 'interface_inventory_runtime_adapter'
    assert payload['automation_policy']['delete_old_files'] is False


def test_apply_task_package_runs_only_p0_by_default(tmp_path):
    from sikk_wallet_structure_apply_task_package import apply_task_package

    root = tmp_path
    p0_source = root / 'legacy_compat/path_maps/data_path_map_20260506.json'
    p0_source.parent.mkdir(parents=True)
    p0_source.write_text('{"old": "new"}', encoding='utf-8')
    p1_source = root / 'contracts/shared/README.md'
    p1_source.parent.mkdir(parents=True)
    p1_source.write_text('# shared contract', encoding='utf-8')

    manifest = {
        'artifact_type': 'wallet_structure_system_gap_task_manifest',
        'task_id': 'demo',
        'next_actions': [
            {'order': 1, 'priority': 'P0', 'source_file': 'legacy_compat/path_maps/data_path_map_20260506.json', 'capability': 'interface_inventory', 'action': 'create_runtime_adapter', 'target_module': 'modules/wallet_data_guard/'},
            {'order': 2, 'priority': 'P1', 'source_file': 'contracts/shared/README.md', 'capability': 'schema_contract', 'action': 'add_schema_validator', 'target_module': 'modules/wallet_data_guard/'},
        ],
        'automation_policy': {'delete_old_files': False},
    }
    manifest_path = root / 'research_loop/task_packages/pending/demo/task_manifest.json'
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')

    result = apply_task_package(project_root=root, task_manifest=manifest_path, max_priority='P0', task_id='apply_demo')

    assert result['status'] == 'COMPLETED'
    assert result['applied_count'] == 1
    assert result['skipped_count'] == 1
    assert Path(result['apply_manifest']).exists()
    apply_manifest = json.loads(Path(result['apply_manifest']).read_text(encoding='utf-8'))
    assert apply_manifest['applied'][0]['source_file'].endswith('data_path_map_20260506.json')
    assert apply_manifest['skipped'][0]['priority'] == 'P1'


def test_apply_task_package_supports_only_priority_and_all(tmp_path):
    from sikk_wallet_structure_apply_task_package import apply_task_package

    root = tmp_path
    for rel in ['a/p0.md', 'a/p1.md', 'a/p2.md']:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(rel, encoding='utf-8')
    manifest = {
        'artifact_type': 'wallet_structure_system_gap_task_manifest',
        'task_id': 'demo_all',
        'next_actions': [
            {'order': 1, 'priority': 'P0', 'source_file': 'a/p0.md', 'capability': 'interface_inventory', 'action': 'create_runtime_adapter', 'target_module': 'modules/source_wallet_bot/'},
            {'order': 2, 'priority': 'P1', 'source_file': 'a/p1.md', 'capability': 'schema_contract', 'action': 'add_schema_validator', 'target_module': 'modules/wallet_data_guard/'},
            {'order': 3, 'priority': 'P2', 'source_file': 'a/p2.md', 'capability': 'legacy_fallback', 'action': 'create_legacy_path_map', 'target_module': 'modules/wallet_data_guard/'},
        ],
    }
    manifest_path = root / 'pkg/task_manifest.json'
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')

    result = apply_task_package(project_root=root, task_manifest=manifest_path, only_priority='P1', task_id='apply_p1')
    assert result['applied_count'] == 1
    p1_manifest = json.loads(Path(result['apply_manifest']).read_text(encoding='utf-8'))
    assert p1_manifest['applied'][0]['priority'] == 'P1'
    assert {s['priority'] for s in p1_manifest['skipped']} == {'P0', 'P2'}

    all_result = apply_task_package(project_root=root, task_manifest=manifest_path, max_priority='P2', task_id='apply_all')
    assert all_result['applied_count'] == 3
    all_manifest = json.loads(Path(all_result['apply_manifest']).read_text(encoding='utf-8'))
    assert all_manifest['by_priority']['P0'] == 1
    assert all_manifest['by_priority']['P1'] == 1
    assert all_manifest['by_priority']['P2'] == 1
