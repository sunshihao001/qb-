from pathlib import Path


def test_wallet_structure_auto_runner_l3_public_api_and_docs():
    import modules.wallet_structure_auto_runner as auto_runner

    assert callable(auto_runner.run_wallet_structure_auto_task)
    assert callable(auto_runner.build_guard_trend_index)
    assert hasattr(auto_runner, '__all__')
    module_dir = Path('/root/sikk-gmgn/modules/wallet_structure_auto_runner')
    assert (module_dir / 'README.md').exists()
    readme = (module_dir / 'README.md').read_text(encoding='utf-8')
    assert 'L3' in readme
    assert '只读' in readme
    assert '交易' in readme


def test_wallet_structure_audit_l3_public_api_and_docs(tmp_path):
    import modules.wallet_structure_audit as audit

    assert callable(audit.audit_wallet_structure_system)
    assert hasattr(audit, '__all__')
    module_dir = Path('/root/sikk-gmgn/modules/wallet_structure_audit')
    assert (module_dir / 'README.md').exists()
    readme = (module_dir / 'README.md').read_text(encoding='utf-8')
    assert 'L3' in readme
    assert '审计' in readme
    report = audit.audit_wallet_structure_system(project_root=Path('/root/sikk-gmgn'), output_dir=tmp_path)
    assert report['artifact_type'] == 'wallet_structure_system_audit'
    assert Path(report['json_path']).exists()
