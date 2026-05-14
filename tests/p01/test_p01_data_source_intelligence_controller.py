import json
import subprocess
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')
CTRL = ROOT / 'controllers/p01_data_source_intelligence_controller.py'

def run_ctrl(tmp_path, mode='all'):
    out = subprocess.check_output(['python3', str(CTRL), '--repo-root', str(ROOT), '--run-dir', str(tmp_path), '--mode', mode], text=True)
    return json.loads(out)

def test_p01_controller_all_creates_handoff_and_manifest(tmp_path):
    res = run_ctrl(tmp_path, 'all')
    assert res['status'] == 'P01_DSIC_MIN_AUTOMATION_SCAFFOLD_READY_WITH_GAPS'
    p01 = Path(res['p01_dir'])
    handoff = p01 / 'handoff/SYSTEM_ARCHIVE/data_fact_handoff_packet.json'
    manifest = p01 / 'manifest/p01_dsic_manifest.json'
    assert handoff.exists()
    assert manifest.exists()
    packet = json.loads(handoff.read_text())
    assert packet['handoff_constraints']['real_execution_allowed'] is False
    assert packet['handoff_constraints']['paper_runtime_allowed'] is False
    assert packet['handoff_constraints']['live_execution_allowed'] is False
    assert packet['handoff_constraints']['raw_direct_access_allowed'] is False
    assert packet['data_fact_status'] == 'DATA_REPLAY_ONLY'
    assert packet['downstream_permissions']['P06_paper_trading_controller'] == 'PAUSE'

def test_p01_controller_init_phase_has_identity(tmp_path):
    res = run_ctrl(tmp_path, 'init-phase')
    p01 = Path(res['p01_dir'])
    assert (p01 / 'phase_identity/phase_01_data_source_intelligence_controller.yaml').exists()
    text = (p01 / 'phase_identity/phase_01_data_source_intelligence_controller.yaml').read_text()
    assert 'real_execution_allowed: false' in text
    assert 'raw_direct_access_allowed: false' in text

def test_p01_outputs_do_not_contain_secret_like_strings(tmp_path):
    res = run_ctrl(tmp_path, 'all')
    p01 = Path(res['p01_dir'])
    bad = ['api_key', 'private_key', 'secret=', 'password=', 'bearer ']
    for path in p01.rglob('*'):
        if path.is_file() and path.suffix in {'.json', '.md', '.yaml', '.jsonl'}:
            text = path.read_text(errors='ignore').lower()
            assert not any(b in text for b in bad), f'secret-like marker in {path}'
