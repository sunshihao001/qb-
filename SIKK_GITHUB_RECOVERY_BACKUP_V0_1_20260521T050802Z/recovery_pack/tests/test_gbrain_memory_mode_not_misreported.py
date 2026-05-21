import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
LATEST=ROOT/'data/coordination/latest'

def test_memory_mode_not_misreported():
    act=json.load(open(LATEST/'real_skill_interface_activation_report.json'))
    if act['gbrain_memory_mode']=='GBRAIN_FILE_PROTOCOL_BRIDGE':
        assert act['real_gbrain_available'] is False
        assert act['gbrain_patch_status'] != 'REAL_CONNECTED'
    if act['gbrain_memory_mode']=='REAL_CLI':
        assert act['real_gbrain_available'] is True
        assert act['gbrain_patch_status'] == 'REAL_CONNECTED'
        assert act['gbrain_real_call_status'] == 'REAL_CALLED'
