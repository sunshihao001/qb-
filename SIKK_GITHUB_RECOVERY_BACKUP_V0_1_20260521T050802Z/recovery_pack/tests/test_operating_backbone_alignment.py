from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]

def test_operating_backbone_alignment_report_gate():
    report=ROOT/'data/coordination/latest/artifact_pack/SIKK_OPERATING_BACKBONE_ALIGNMENT_RUN/operating_backbone_alignment_report.json'
    gate=ROOT/'data/coordination/latest/artifact_pack/SIKK_OPERATING_BACKBONE_ALIGNMENT_RUN/operating_backbone_alignment_gate.json'
    assert report.exists()
    assert gate.exists()
    r=json.loads(report.read_text())
    g=json.loads(gate.read_text())
    assert r['current_backbone_status']=='PASS_WITH_GAPS'
    assert r['next_operational_run']=='GMGN_SOURCE_TO_SIKK_CANONICAL_MAPPING_RUN'
    assert r['paper_readiness_allowed'] is False
    assert g['paper_runner_allowed'] is False
    assert 'source-to-canonical' in ' '.join(r['missing_backbone_links']) or r['gmgn_raw_response_mapped_to_sikk_canonical_model'].startswith('PARTIAL')
