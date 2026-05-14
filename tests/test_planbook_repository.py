from __future__ import annotations

import json
from pathlib import Path
import subprocess

from modules.runtime.planbook_repository import PlanbookRepository


def test_planbook_repository_indexes_valid_planbook_and_writes_audit(tmp_path):
    planbook_dir = tmp_path / "research_loop" / "plan_books" / "active"
    planbook_dir.mkdir(parents=True)
    (planbook_dir / "valid_planbook.md").write_text(
        """# Valid Planbook

- planbook_id: `valid_planbook`
- version: `v1.0`
- status: `RUNTIME_CONSUMABLE`
- scope: `SIKK Stable Trader OS`
- owner_layer: `HER control plane`
- source_type: `planbook`
- runtime_consumption: `runtime reader consumes index`
- control_plane_refs: `docs/09_her_execution_protocol/her_total_control_execution_protocol.md`
- gap_policy: `gaps remain gaps`
- audit_policy: `write validation json`
- durable_cognition_policy: `verified stable rule only`
- safety_boundary: `paper-only / no signing / no broadcast / no real trade`
""",
        encoding="utf-8",
    )

    result = PlanbookRepository(tmp_path).validate()

    assert result["final_status"] == "PLANBOOK_REPOSITORY_READY"
    assert result["gap_register"] == []
    assert Path(result["index_path"]).exists()
    assert Path(result["audit_path"]).exists()
    index = json.loads(Path(result["index_path"]).read_text(encoding="utf-8"))
    assert index["planbooks"][0]["metadata"]["planbook_id"] == "valid_planbook"
    assert index["safety_boundary"]["real_trade_enabled"] is False


def test_planbook_repository_degrades_missing_metadata_and_blocks_forbidden_execution(tmp_path):
    active = tmp_path / "research_loop" / "plan_books" / "active"
    active.mkdir(parents=True)
    (active / "missing_metadata.md").write_text(
        """# Missing Metadata

- planbook_id: `missing_metadata`
- version: `v1.0`
- status: `DRAFT`
- safety_boundary: `paper-only / no signing / no broadcast / no real trade`
""",
        encoding="utf-8",
    )
    (active / "bad_planbook.md").write_text(
        """# Bad Planbook

- planbook_id: `bad_planbook`
- version: `v1.0`
- status: `RUNTIME_CONSUMABLE`
- scope: `SIKK Stable Trader OS`
- owner_layer: `HER control plane`
- source_type: `planbook`
- runtime_consumption: `runtime reader consumes index`
- control_plane_refs: `docs/09_her_execution_protocol/her_total_control_execution_protocol.md`
- gap_policy: `gaps remain gaps`
- audit_policy: `write validation json`
- durable_cognition_policy: `verified stable rule only`
- safety_boundary: `paper-only / no signing / no broadcast / no real trade`

signing: allowed
""",
        encoding="utf-8",
    )

    result = PlanbookRepository(tmp_path).validate()

    assert result["final_status"] == "PLANBOOK_REPOSITORY_REJECTED"
    assert any(gap["gap_id"].startswith("PLANBOOK_MISSING_METADATA_") for gap in result["gap_register"])
    assert any(gap["gap_id"] == "PLANBOOK_FORBIDDEN_EXECUTION_PATTERN" for gap in result["gap_register"])


def test_planbook_repository_cli_smoke(tmp_path):
    active = tmp_path / "research_loop" / "plan_books" / "active"
    active.mkdir(parents=True)
    (active / "valid_planbook.md").write_text(
        """# Valid Planbook

- planbook_id: `valid_planbook`
- version: `v1.0`
- status: `RUNTIME_CONSUMABLE`
- scope: `SIKK Stable Trader OS`
- owner_layer: `HER control plane`
- source_type: `planbook`
- runtime_consumption: `runtime reader consumes index`
- control_plane_refs: `docs/09_her_execution_protocol/her_total_control_execution_protocol.md`
- gap_policy: `gaps remain gaps`
- audit_policy: `write validation json`
- durable_cognition_policy: `verified stable rule only`
- safety_boundary: `paper-only / no signing / no broadcast / no real trade`
""",
        encoding="utf-8",
    )
    completed = subprocess.run(
        ["python3", "-m", "modules.runtime.planbook_repository", "--root", str(tmp_path)],
        cwd="/root/sikk-gmgn",
        text=True,
        capture_output=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["final_status"] == "PLANBOOK_REPOSITORY_READY"
    assert Path(payload["audit_path"]).exists()
