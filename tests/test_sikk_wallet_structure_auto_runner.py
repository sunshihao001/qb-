import json
from pathlib import Path


def test_wallet_structure_system_audit_identifies_runtime_gaps(tmp_path):
    from sikk_wallet_structure_system_audit import audit_wallet_structure_system

    report = audit_wallet_structure_system(project_root=Path('/root/sikk-gmgn'), output_dir=tmp_path)

    assert report['artifact_type'] == 'wallet_structure_system_audit'
    assert report['overall_status'] == 'PASS'
    resolved_ids = {gap['id'] for gap in report['resolved_gaps']}
    assert 'LONG_RUNNING_AUTO_RUNNER' in resolved_ids
    assert 'ACCEPTANCE_NOT_IN_PIPELINE_MANIFEST' in resolved_ids
    assert 'WALLET_GUARD_SYSTEM_WIDE_INDEX' in resolved_ids
    assert report['gaps'] == []
    assert Path(report['json_path']).exists()
    assert Path(report['md_path']).exists()
    md = Path(report['md_path']).read_text(encoding='utf-8')
    assert '钱包结构分析系统全流程审计' in md
    assert '已补全运行能力' in md


def test_wallet_structure_auto_runner_runs_multiple_cycles_with_checkpoint(tmp_path):
    from sikk_wallet_structure_auto_runner import run_wallet_structure_auto_task

    calls = []

    def fake_pipeline(**kwargs):
        calls.append(kwargs)
        out = Path(kwargs['output_root'])
        orchestrator = out / 'orchestrator'
        orchestrator.mkdir(parents=True, exist_ok=True)
        manifest = orchestrator / 'pipeline_manifest.json'
        report = orchestrator / 'pipeline_report.md'
        payload = {
            '模块': 'fake pipeline',
            '阶段统计': {
                '钱包结构门禁': {'成功数量': 1, 'wallet_data_guard': {'status': 'PASS'}},
                '状态机': {'候选数量': 1},
            },
            '输出文件': {'运行报告MD': str(report)},
            '说明': '不执行真实 swap',
        }
        manifest.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        report.write_text('# fake\n不执行真实 swap\n', encoding='utf-8')
        return {'manifest_json': str(manifest), 'report_md': str(report)}

    result = run_wallet_structure_auto_task(
        output_root=tmp_path,
        cycles=2,
        interval_seconds=0,
        pipeline_runner=fake_pipeline,
        now_sequence=['2026-05-08T01:20:00Z', '2026-05-08T01:21:00Z'],
        limit=1,
    )

    assert len(calls) == 2
    assert result['status'] == 'COMPLETED'
    assert result['cycles_completed'] == 2
    assert Path(result['checkpoint_path']).exists()
    assert Path(result['manifest_path']).exists()
    assert Path(result['audit_report_path']).exists()
    checkpoint = json.loads(Path(result['checkpoint_path']).read_text(encoding='utf-8'))
    assert checkpoint['last_completed_cycle'] == 2
    assert checkpoint['safety_boundary']['real_swap_enabled'] is False
    manifest = json.loads(Path(result['manifest_path']).read_text(encoding='utf-8'))
    assert manifest['long_running_task']['cycles_requested'] == 2
    assert manifest['cycles'][0]['wallet_structure_status'] == 'PASS'
    assert manifest['cycles'][0]['acceptance_status'] == 'PASS'
    assert Path(manifest['guard_trend_index_path']).exists()
    trend = json.loads(Path(manifest['guard_trend_index_path']).read_text(encoding='utf-8'))
    assert trend['cycles_total'] == 2
    assert trend['status_counts']['PASS'] == 2


def test_wallet_structure_auto_runner_resumes_from_checkpoint(tmp_path):
    from sikk_wallet_structure_auto_runner import run_wallet_structure_auto_task

    calls = []

    def fake_pipeline(**kwargs):
        calls.append(kwargs)
        out = Path(kwargs['output_root'])
        orchestrator = out / 'orchestrator'
        orchestrator.mkdir(parents=True, exist_ok=True)
        manifest = orchestrator / 'pipeline_manifest.json'
        report = orchestrator / 'pipeline_report.md'
        payload = {
            '阶段统计': {
                '钱包结构门禁': {'成功数量': 1, 'wallet_data_guard': {'status': 'PASS'}},
                '状态机': {'候选数量': 1},
            },
            '输出文件': {'运行报告MD': str(report)},
            '说明': '不执行真实 swap',
        }
        manifest.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        report.write_text('# fake\n不执行真实 swap\n', encoding='utf-8')
        return {'manifest_json': str(manifest), 'report_md': str(report)}

    run_wallet_structure_auto_task(
        output_root=tmp_path,
        cycles=1,
        interval_seconds=0,
        pipeline_runner=fake_pipeline,
        now_sequence=['2026-05-08T01:30:00Z'],
    )
    result = run_wallet_structure_auto_task(
        output_root=tmp_path,
        cycles=3,
        interval_seconds=0,
        pipeline_runner=fake_pipeline,
        now_sequence=['2026-05-08T01:31:00Z', '2026-05-08T01:32:00Z'],
        resume=True,
    )

    assert result['cycles_completed'] == 3
    checkpoint = json.loads(Path(result['checkpoint_path']).read_text(encoding='utf-8'))
    assert checkpoint['last_completed_cycle'] == 3
    manifest = json.loads(Path(result['manifest_path']).read_text(encoding='utf-8'))
    assert manifest['long_running_task']['resume'] is True
    assert [cycle['cycle'] for cycle in manifest['cycles']] == [1, 2, 3]
