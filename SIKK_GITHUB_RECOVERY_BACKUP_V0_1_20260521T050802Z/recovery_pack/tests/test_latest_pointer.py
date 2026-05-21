from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID='bootstrap_directory_realign_v0_1'

def test_latest_pointer():
    assert (ROOT/'data/latest/latest_run_id.txt').read_text().strip()==RUN_ID
    summary=json.loads((ROOT/'data/latest/acceptance_summary.json').read_text())
    assert summary.get('latest_is_pointer_only') is True
