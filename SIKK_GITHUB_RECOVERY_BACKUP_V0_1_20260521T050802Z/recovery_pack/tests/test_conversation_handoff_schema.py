import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_conversation_handoff_schema():
    schema=json.load(open(ROOT/'contracts/conversation_handoff_schema.json'))
    path=ROOT/'data/coordination/history/conversation_handoff.jsonl'
    assert path.exists()
    lines=[json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
    assert lines
    latest=lines[-1]
    assert set(schema['required']).issubset(latest)
    assert latest['acceptance_status'] in ['PASS','PASS_WITH_GAPS','PATCH_REQUIRED','FAIL']
