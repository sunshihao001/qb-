import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')

def latest_a00_run():
    runs = sorted((ROOT/'data/her_document_function_system/a00_real_acceptance_runs').glob('a00_real_*'))
    assert runs, 'no A00 real acceptance run found'
    return runs[-1]

def load(rel):
    return json.loads((latest_a00_run()/rel).read_text())

def test_a00_artifact_manifest_required_assets():
    manifest = load('artifact_manifest/artifact_manifest.json')
    required = [a for a in manifest['artifacts'] if a['required']]
    assert required
    assert all(a['exists'] for a in required)
