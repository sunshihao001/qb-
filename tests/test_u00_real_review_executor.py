import json
import subprocess
import sys
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')
EXEC = ROOT / 'tools/u00_real_review_executor.py'
O00_RUN_ID = 'o00_run_20260513_184513_393401'


def test_u00_real_safe_mode_executor_runs_ready_with_gaps():
    proc = subprocess.run(
        [sys.executable, str(EXEC), '--repo-root', str(ROOT), '--safe-mode', '--o00-run-id', O00_RUN_ID],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 10, proc.stdout + proc.stderr
    marker_line = next(line for line in proc.stdout.splitlines() if line.startswith('U00_REAL_RESULT='))
    payload = json.loads(marker_line.split('=', 1)[1])
    assert payload['status'] == 'U00_REAL_READY_WITH_GAPS'
    assert payload['review_cases'] >= 1
    assert payload['upgrade_candidates'] >= 1
