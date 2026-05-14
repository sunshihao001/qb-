import json
from pathlib import Path


def test_system_gap_scanner_finds_document_only_wallet_files(tmp_path):
    from modules.source_wallet_bot.system_gap_scanner import scan_wallet_structure_system_gaps

    root = tmp_path
    (root / 'docs/source_wallet_bot/directory_governance').mkdir(parents=True)
    (root / 'docs/source_wallet_bot/directory_governance/data_dependency_map_v1.md').write_text(
        '# Data Dependency\n需要 runner acceptance contract scanner\n', encoding='utf-8'
    )
    (root / 'modules/source_wallet_bot').mkdir(parents=True)
    (root / 'docs/system_directory_routes.json').parent.mkdir(parents=True, exist_ok=True)
    (root / 'docs/system_directory_routes.json').write_text(json.dumps({'bots': {'source_wallet_bot': {}}}), encoding='utf-8')

    report = scan_wallet_structure_system_gaps(project_root=root, output_dir=root / 'research_loop/state/gap_scan')

    assert report['artifact_type'] == 'wallet_structure_system_gap_scan'
    assert report['summary']['total_findings'] >= 1
    finding = report['findings'][0]
    assert finding['file_path'].endswith('data_dependency_map_v1.md')
    assert finding['gap_type'] == 'document_only_without_runtime_anchor'
    assert finding['priority'] in {'P0', 'P1'}
    assert finding['recommended_action']['action'] in {'create_runtime_adapter', 'connect_to_existing_runner'}
    assert Path(report['json_path']).exists()
    assert Path(report['priority_md_path']).exists()


def test_system_gap_auto_runner_writes_task_package(tmp_path):
    from sikk_wallet_structure_system_gap_auto_runner import run_system_gap_auto_flow

    root = tmp_path
    (root / 'docs/source_wallet_bot/directory_governance').mkdir(parents=True)
    (root / 'docs/source_wallet_bot/directory_governance/interface_capability_inventory_v1.md').write_text(
        '# Interface Capability\nGMGN OKX collector adapter contract\n', encoding='utf-8'
    )
    (root / 'modules/source_wallet_bot').mkdir(parents=True)
    (root / 'docs/system_directory_routes.json').parent.mkdir(parents=True, exist_ok=True)
    (root / 'docs/system_directory_routes.json').write_text(json.dumps({'bots': {'source_wallet_bot': {}}}), encoding='utf-8')

    result = run_system_gap_auto_flow(project_root=root, task_id='gap_test')

    assert result['status'] in {'COMPLETED', 'NEEDS_ACTION'}
    assert Path(result['scan_json']).exists()
    assert Path(result['priority_md']).exists()
    assert Path(result['task_package_dir']).exists()
    manifest = json.loads(Path(result['task_manifest']).read_text(encoding='utf-8'))
    assert manifest['artifact_type'] == 'wallet_structure_system_gap_task_manifest'
    assert manifest['automation_policy']['delete_old_files'] is False
    assert manifest['next_actions']
    assert len(manifest['next_actions']) == manifest['summary']['total_findings']
