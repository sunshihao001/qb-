import json
from pathlib import Path


def test_wallet_structure_governance_submodule_exports_public_api():
    import modules.wallet_structure_governance as governance

    assert callable(governance.scan_wallet_structure_system_gaps)
    assert callable(governance.apply_gap_action)
    assert callable(governance.build_runtime_adapter_registry)
    assert callable(governance.integrate_runtime_adapters)
    assert callable(governance.consume_runtime_registry)
    assert callable(governance.run_governance_cycle)


def test_wallet_structure_governance_cycle_runs_scan_apply_integrate_consume(tmp_path):
    from modules.wallet_structure_governance import run_governance_cycle

    root = tmp_path
    source = root / 'legacy_compat/path_maps/data_path_map_20260506.json'
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(json.dumps({'routes': []}, ensure_ascii=False), encoding='utf-8')
    doc = root / 'docs/source_wallet_bot/directory_governance/interface_capability_inventory_v1.md'
    doc.parent.mkdir(parents=True, exist_ok=True)
    doc.write_text('# Interface Capability\nGMGN OKX collector adapter contract\n', encoding='utf-8')

    result = run_governance_cycle(
        project_root=root,
        output_root=root / 'state/governance_cycle',
        task_id='governance_cycle_test',
        max_priority='P2',
    )

    assert result['status'] in {'PASS', 'COMPLETED'}
    assert Path(result['scan_json']).exists()
    assert Path(result['apply_manifest']).exists()
    assert Path(result['registry_path']).exists()
    assert Path(result['consumption_report']).exists()
    assert result['consumption_status'] == 'PASS'


def test_old_source_wallet_bot_imports_remain_wrappers():
    from modules.source_wallet_bot.system_gap_scanner import scan_wallet_structure_system_gaps
    from modules.wallet_structure_governance.gap_scanner import scan_wallet_structure_system_gaps as new_scan
    from modules.source_wallet_bot.runtime_adapter_registry import build_runtime_adapter_registry
    from modules.wallet_structure_governance.registry import build_runtime_adapter_registry as new_registry

    assert scan_wallet_structure_system_gaps is new_scan
    assert build_runtime_adapter_registry is new_registry
