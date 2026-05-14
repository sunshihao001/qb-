import json
from pathlib import Path


def test_module_maturity_scanner_classifies_l1_l2_l3_and_priorities(tmp_path):
    from modules.wallet_structure_governance.maturity_scanner import scan_module_maturity

    root = tmp_path
    # L3: standalone submodule
    l3 = root / 'modules/wallet_data_guard'
    l3.mkdir(parents=True)
    (l3 / '__init__.py').write_text('def public_api(): pass\n', encoding='utf-8')
    (l3 / 'README.md').write_text('# Wallet Data Guard\n', encoding='utf-8')
    (root / 'tests').mkdir()
    (root / 'tests/test_wallet_data_guard.py').write_text('def test_guard(): pass\n', encoding='utf-8')

    # L2: runtime integrated but no standalone submodule
    (root / 'sikk_wallet_structure_auto_runner.py').write_text('def run_wallet_structure_auto_task(): pass\n', encoding='utf-8')
    (root / 'tests/test_sikk_wallet_structure_auto_runner.py').write_text('def test_auto(): pass\n', encoding='utf-8')

    # L1: functional code only
    (root / 'sikk_wallet_structure_system_audit.py').write_text('def run_audit(): pass\n', encoding='utf-8')

    result = scan_module_maturity(project_root=root, output_dir=root / 'out')

    assert result['artifact_type'] == 'wallet_structure_module_maturity_scan'
    assert result['summary']['total_capabilities'] >= 3
    by_name = {item['capability']: item for item in result['capabilities']}
    assert by_name['wallet_data_guard']['maturity_level'] == 'L3'
    assert by_name['auto_runner']['maturity_level'] == 'L2'
    assert by_name['system_audit']['maturity_level'] == 'L1'
    assert by_name['system_audit']['priority'] in {'P0', 'P1'}
    assert Path(result['json_path']).exists()
    assert Path(result['priority_md_path']).exists()


def test_governance_public_api_exports_maturity_scanner():
    import modules.wallet_structure_governance as governance

    assert callable(governance.scan_module_maturity)
