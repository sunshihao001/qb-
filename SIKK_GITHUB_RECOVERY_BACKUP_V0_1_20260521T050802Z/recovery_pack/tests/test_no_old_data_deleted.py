from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID='bootstrap_directory_realign_v0_1'

def test_no_old_data_deleted():
    assert (ROOT/'data/gmgn_read_only/latest').exists()
    compat=json.loads((ROOT/'data/runs'/RUN_ID/'compatibility_mapping.json').read_text())
    assert compat['delete_old_data'] is False
    assert compat['compatibility_status']=='ACTIVE'
