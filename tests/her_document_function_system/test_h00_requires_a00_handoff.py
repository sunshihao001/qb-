import subprocess
from pathlib import Path

REPO = Path('/root/sikk-gmgn')


def test_h00_requires_a00_handoff(tmp_path):
    out = tmp_path / 'h00_missing'
    cmd = [
        'python3', 'tools/h00_real_queue_executor.py',
        '--a00-handoff', str(tmp_path / 'missing_a00_handoff.json'),
        '--repo-root', str(REPO),
        '--output-dir', str(out),
        '--safe-mode',
    ]
    result = subprocess.run(cmd, cwd=REPO, text=True, capture_output=True)
    assert result.returncode == 2
    assert (out / 'acceptance/h00_real_queue_acceptance.json').exists()
