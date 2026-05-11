
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "09_scripts" / "hermes_runtime_hook_launcher.py"

def test_launcher_help_mentions_quick_command_and_json_output():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--help"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0
    help_text = result.stdout + result.stderr
    assert "--problem" in help_text
    assert "--dry-run" in help_text
    assert "--json" in help_text
    assert "quick command" in help_text.lower()

def test_launcher_dry_run_returns_runtime_metadata_json():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--dry-run", "--problem", "执行任务，全自动完成：验证 launcher 可用。", "--json"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout.strip())
    assert payload["status"] == "COMPLETED"
    assert payload["route"] == "hermes_runtime_hook_autonomous_problem_loop"
    assert payload["dry_run"] is True
    assert Path(payload["run_dir"]).exists()
    assert Path(payload["run_dir"]).joinpath("runtime_state.json").exists()
    assert Path(payload["run_dir"]).joinpath("tool_ledger.jsonl").exists()
