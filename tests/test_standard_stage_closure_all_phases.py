from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PHASES = [f"K{i:02d}" for i in range(0, 9)] + [f"P{i:02d}" for i in range(0, 11)] + [f"I{i:02d}" for i in range(1, 6)] + ["R00"]


def test_standard_stage_assets_exist_for_all_requested_phases():
    result = subprocess.run(
        [sys.executable, "tools/stable_trader_os/standard_stage_closure.py", "validate", "--root", str(ROOT)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "STANDARD_STAGE_CLOSURE_VALIDATION_PASS" in result.stdout

    manifest_path = ROOT / "system/stable_trader_os/standard_stage_closure/manifest.json"
    manifest = json.loads(manifest_path.read_text())
    assert manifest["safety"]["paper_only"] is True
    assert manifest["safety"]["forbidden_real_execution"] == ["swap", "private_key", "signing", "broadcast", "real_trade"]
    assert set(PHASES).issubset(set(manifest["phases"].keys()))

    for phase in PHASES:
        record = manifest["phases"][phase]
        assert record["status"] in {
            "STANDARD_STAGE_CLOSED_PAPER_ONLY",
            "BUSINESS_BOUND_STAGE_READY_PAPER_ONLY",
        }
        for key in ["controller", "schema", "contract", "trace", "acceptance", "handoff", "runtime_entry"]:
            path = ROOT / record[key]
            assert path.exists(), f"missing {phase} {key}: {path}"


def test_r00_standard_stage_contract_is_paper_only_and_no_real_execution():
    contract_path = ROOT / "contracts/stable_trader_os/r00_standard_stage/contract.json"
    contract = json.loads(contract_path.read_text())
    assert contract["phase_id"] == "R00"
    assert contract["runtime_mode"] == "paper_only"
    assert contract["permissions"]["real_execution_allowed"] is False
    assert contract["permissions"]["private_key_access_allowed"] is False
    assert contract["permissions"]["broadcast_allowed"] is False
    assert "PAPER_ONLY_RUNTIME_STAGE" in contract["allowed_outputs"]
