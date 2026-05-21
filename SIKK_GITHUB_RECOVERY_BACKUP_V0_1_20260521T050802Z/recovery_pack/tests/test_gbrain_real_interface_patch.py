import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')
LATEST=ROOT/'data/coordination/latest'

def test_patch_report():
    r=json.load(open(LATEST/'gbrain_real_interface_patch_report.json'))
    assert r['gbrain_patch_status'] in ['REAL_CONNECTED','FILE_PROTOCOL_BRIDGE','STUB_ONLY','NOT_AVAILABLE','FAILED']
    if r['cli_found'] or r['python_module_found'] or r['http_endpoint_found'] or r['mcp_tool_found']:
        assert r['gbrain_patch_status'] == 'REAL_CONNECTED'
        assert r['confirmed_entrypoint']
    else:
        assert r['gbrain_patch_status'] != 'REAL_CONNECTED'
