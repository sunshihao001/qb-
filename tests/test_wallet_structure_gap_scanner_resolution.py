import json
from pathlib import Path


def test_gap_scanner_treats_consumed_runtime_registry_sources_as_resolved(tmp_path):
    from modules.wallet_structure_governance.gap_scanner import scan_wallet_structure_system_gaps

    root = tmp_path
    doc = root / "docs/source_wallet_bot/directory_governance/file_level_inventory_summary.md"
    doc.parent.mkdir(parents=True)
    doc.write_text("# interface capability inventory\nGMGN OKX collector 接口能力", encoding="utf-8")
    mod = root / "modules/source_wallet_bot/system_gap_scanner.py"
    mod.parent.mkdir(parents=True)
    mod.write_text("def consume_interface_inventory_runtime_adapters(registry): return registry", encoding="utf-8")

    first = scan_wallet_structure_system_gaps(project_root=root, output_dir=tmp_path / "first")
    assert first["summary"]["total_findings"] == 1

    registry = root / "research_loop/state/integration/runtime_adapter_registry.json"
    registry.parent.mkdir(parents=True)
    registry.write_text(json.dumps({
        "adapter_groups": {
            "interface_inventory_runtime_adapter": [
                {"source_file": "docs/source_wallet_bot/directory_governance/file_level_inventory_summary.md"}
            ]
        }
    }), encoding="utf-8")
    consumption = root / "research_loop/state/consumption/runtime_registry_consumption_report.json"
    consumption.parent.mkdir(parents=True)
    consumption.write_text(json.dumps({
        "status": "PASS",
        "target_consumption": {
            "system_gap_scanner": {
                "status": "PASS",
                "source_files": ["docs/source_wallet_bot/directory_governance/file_level_inventory_summary.md"]
            }
        }
    }), encoding="utf-8")

    second = scan_wallet_structure_system_gaps(project_root=root, output_dir=tmp_path / "second")
    assert second["summary"]["total_findings"] == 0
    assert second["summary"]["resolved_by_runtime_registry_count"] == 1
