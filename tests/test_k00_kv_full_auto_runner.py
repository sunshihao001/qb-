import json
from pathlib import Path


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    return path


def test_k00_kv_extractor_materializes_runner_readable_facts(tmp_path):
    from sikk_k00_kv_extractor import extract_kv_from_task_package

    schema = tmp_path / 'sikk_stable_trader_os/00_knowledge_intake/kv_cache/kv_cache.schema.json'
    _write_json(schema, {'title': 'demo schema'})
    task_package = _write_json(
        tmp_path / 'task_execution_package_DOC-TEST-001.json',
        {
            'artifact_type': 'task_execution_package',
            'package_id': 'DOC-TEST-001',
            'status': 'READY_TO_EXECUTE',
            'runtime_allowed': True,
            'objective': '把任务包压成 runner 可消费数据单元',
            'affected_phases': ['K00', 'P00'],
            'required_inputs': ['raw document', 'schema'],
            'required_outputs': ['kv_items jsonl', 'manifest json'],
            'acceptance': ['kv manifest exists', 'facts package exists'],
            'next_actions': [
                {
                    'order': 1,
                    'priority': 'P0',
                    'source_file': 'docs/source.md',
                    'capability': 'schema_contract',
                    'action': 'create_runtime_adapter',
                    'target_module': 'modules/source_wallet_bot/',
                }
            ],
            'automation_policy': {'paper_only': True, 'delete_old_files': False},
            'safety_boundary': {'no_swap': True, 'no_broadcast': True},
        },
    )

    result = extract_kv_from_task_package(
        task_package_path=task_package,
        output_root=tmp_path / 'runtime_extractions',
        schema_path=schema,
    )

    assert result['status'] == 'COMPLETED'
    assert result['doc_id'] == 'DOC-TEST-001'
    assert result['item_count'] >= 8
    assert result['by_asset_class']['runner_binding'] == 1
    assert result['by_asset_class']['field_requirement'] == 2

    manifest = json.loads(Path(result['kv_cache_manifest']).read_text(encoding='utf-8'))
    assert manifest['status'] == 'KV_CACHE_READY'
    assert manifest['runner_inputs']['has_next_actions'] is True
    assert manifest['safety_boundary']['paper_only'] is True

    facts = json.loads(Path(result['k00_facts']).read_text(encoding='utf-8'))
    assert facts['artifact_type'] == 'k00_standard_fact_package'
    assert facts['facts']['runtime_allowed'] is True
    assert facts['facts']['next_actions'][0]['priority'] == 'P0'
    assert facts['acceptance_gate']['status'] == 'PASS'

    items = [json.loads(line) for line in Path(result['kv_items']).read_text(encoding='utf-8').splitlines()]
    assert any(item['asset_class'] == 'runner_binding' for item in items)
    assert all('direct_real_trade' in item['governance']['forbidden_uses'] for item in items)
    assert all(item['evidence']['source_doc_hash'] for item in items)


def test_full_auto_runner_executes_manifest_and_writes_closed_loop_outputs(tmp_path):
    from sikk_full_auto_task_package_runner import run_full_auto_task_package

    schema = tmp_path / 'sikk_stable_trader_os/00_knowledge_intake/kv_cache/kv_cache.schema.json'
    _write_json(schema, {'title': 'demo schema'})
    source = tmp_path / 'docs/source.md'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text('# source\nwallet path contract\n', encoding='utf-8')
    task_package = _write_json(
        tmp_path / 'task_manifest.json',
        {
            'artifact_type': 'wallet_structure_system_gap_task_manifest',
            'task_id': 'AUTO-DEMO',
            'status': 'READY_TO_EXECUTE',
            'objective': '执行 next_actions 并回写验收结果',
            'next_actions': [
                {
                    'order': 1,
                    'priority': 'P0',
                    'source_file': 'docs/source.md',
                    'capability': 'schema_contract',
                    'action': 'create_runtime_adapter',
                    'target_module': 'modules/source_wallet_bot/',
                }
            ],
            'acceptance': ['apply manifest exists', 'verification passes'],
        },
    )

    result = run_full_auto_task_package(
        project_root=tmp_path,
        task_package=task_package,
        output_root='runner_state',
        task_id='demo_run',
        max_priority='P2',
    )

    assert result['status'] == 'COMPLETED'
    assert Path(result['kv_cache_manifest']).exists()
    assert Path(result['k00_facts']).exists()
    assert Path(result['apply_manifest']).exists()
    assert Path(result['verification_json']).exists()
    assert Path(result['writeback_manifest']).exists()
    assert Path(result['next_task_manifest']).exists()

    verification = json.loads(Path(result['verification_json']).read_text(encoding='utf-8'))
    assert verification['status'] == 'PASS'
    assert all(verification['checks'].values())

    apply_manifest = json.loads(Path(result['apply_manifest']).read_text(encoding='utf-8'))
    assert apply_manifest['applied_count'] == 1
    assert apply_manifest['skipped_count'] == 0
    adapter_path = Path(apply_manifest['applied'][0]['artifact_path'])
    assert adapter_path.exists()
    adapter = json.loads(adapter_path.read_text(encoding='utf-8'))
    assert adapter['runtime_contract']['write_mode'] == 'additive_adapter_artifact_only'
    assert adapter['automation_policy']['no_swap'] is True

    next_task = json.loads(Path(result['next_task_manifest']).read_text(encoding='utf-8'))
    assert next_task['status'] == 'COMPLETED'
    assert next_task['next_actions'] == []

    writeback = json.loads(Path(result['writeback_manifest']).read_text(encoding='utf-8'))
    assert writeback['status'] == 'COMPLETED'
    assert writeback['safety_boundary']['paper_only'] is True


def test_full_auto_runner_normalizes_k00_task_package_tasks_into_actions(tmp_path):
    from sikk_full_auto_task_package_runner import run_full_auto_task_package

    schema = tmp_path / 'sikk_stable_trader_os/00_knowledge_intake/kv_cache/kv_cache.schema.json'
    _write_json(schema, {'title': 'demo schema'})
    task_package = _write_json(
        tmp_path / 'task_execution_package_DOC-K00-TASKS.json',
        {
            'artifact_type': 'task_execution_package',
            'package_id': 'DOC-K00-TASKS',
            'status': 'READY_TO_EXECUTE',
            'runtime_allowed': True,
            'objective': 'K00 tasks 自动转 next_actions',
            'tasks': [
                {
                    'task_id': 'K00-EXTRACTOR',
                    'phase': 'K00',
                    'action': 'implement extractor',
                    'output': 'sikk_k00_kv_extractor.py',
                    'acceptance': 'extracts kv items',
                }
            ],
            'acceptance': ['normalized manifest exists'],
        },
    )

    result = run_full_auto_task_package(
        project_root=tmp_path,
        task_package=task_package,
        output_root='runner_state',
        task_id='normalize_run',
        max_priority='P2',
    )

    assert result['status'] == 'COMPLETED'
    normalized = json.loads(Path(result['normalized_task_manifest']).read_text(encoding='utf-8'))
    assert normalized['artifact_type'] == 'normalized_full_auto_task_manifest'
    assert normalized['next_actions'][0]['priority'] == 'P0'
    assert normalized['next_actions'][0]['capability'] == 'k00-extractor'

    facts = json.loads(Path(result['k00_facts']).read_text(encoding='utf-8'))
    assert facts['kv_summary']['task_node_count'] == 1
    assert facts['facts']['tasks'][0]['task_id'] == 'K00-EXTRACTOR'

    verification = json.loads(Path(result['verification_json']).read_text(encoding='utf-8'))
    assert verification['status'] == 'PASS'
    next_task = json.loads(Path(result['next_task_manifest']).read_text(encoding='utf-8'))
    assert next_task['status'] == 'COMPLETED'
