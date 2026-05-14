import json
from pathlib import Path


def test_module_maturity_governance_is_standalone_submodule(tmp_path):
    import modules.module_maturity_governance as maturity

    assert callable(maturity.scan_module_maturity)
    assert callable(maturity.evaluate_capability_maturity)
    assert callable(maturity.build_maturity_design_contract)
    assert callable(maturity.write_maturity_design_contract)

    contract = maturity.build_maturity_design_contract()
    assert contract['artifact_type'] == 'module_maturity_design_contract'
    assert contract['maturity_levels']['L1'] == 'functional_code_exists'
    assert contract['maturity_levels']['L2'] == 'runtime_integrated'
    assert contract['maturity_levels']['L3'] == 'standalone_submodule'
    assert contract['promotion_gate']['requires_public_api'] is True
    assert contract['promotion_gate']['requires_verification'] is True


def test_module_maturity_governance_scan_outputs_contract_and_priority(tmp_path):
    from modules.module_maturity_governance import scan_module_maturity

    root = tmp_path
    module = root / 'modules/sample_l3'
    module.mkdir(parents=True)
    (module / '__init__.py').write_text('def public_api(): pass\n', encoding='utf-8')
    (module / 'README.md').write_text('# Sample\n', encoding='utf-8')
    (root / 'tests').mkdir()
    (root / 'tests/test_wallet_data_guard.py').write_text('def test_x(): pass\n', encoding='utf-8')
    # create one known L2 anchor too
    (root / 'sikk_wallet_structure_auto_runner.py').write_text('def run_wallet_structure_auto_task(): pass\n', encoding='utf-8')
    (root / 'tests/test_sikk_wallet_structure_auto_runner.py').write_text('def test_auto(): pass\n', encoding='utf-8')

    result = scan_module_maturity(project_root=root, output_dir=root / 'out')

    assert result['artifact_type'] == 'wallet_structure_module_maturity_scan'
    assert result['design_contract']['artifact_type'] == 'module_maturity_design_contract'
    assert Path(result['json_path']).exists()
    assert Path(result['priority_md_path']).exists()
    assert Path(result['design_contract_path']).exists()


def test_wallet_structure_governance_maturity_scanner_is_wrapper():
    from modules.wallet_structure_governance.maturity_scanner import scan_module_maturity
    from modules.module_maturity_governance import scan_module_maturity as new_scan

    assert scan_module_maturity is new_scan
