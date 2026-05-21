from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_operating_backbone_doc_and_index():
    doc=ROOT/'docs/SIKK_QUANT_RUNNER_OPERATING_BACKBONE_V0_1.md'
    idx=ROOT/'docs/stage_maps/operating_backbone_index.json'
    assert doc.exists()
    assert idx.exists()
    text=doc.read_text()
    for term in ['Real Data Acquisition','Standard Data Objects','Feature Generation','Structure Signal','Strategy Contract','Decision Ticket','Failure Attribution','Upgrade Candidate']:
        assert term in text
    data=json.loads(idx.read_text())
    assert len(data['steps'])==10
    assert data['steps'][0]['primary_output']=='raw_snapshot_manifest'
    assert data['steps'][-1]['primary_output']=='upgrade_candidate'

def test_backbone_gate_in_core_rules():
    rules=(ROOT/'PROJECT_RULES.md').read_text()
    assert 'Operating Backbone 默认主干' in rules
    assert '不能挂到主干的任务标记' in rules
