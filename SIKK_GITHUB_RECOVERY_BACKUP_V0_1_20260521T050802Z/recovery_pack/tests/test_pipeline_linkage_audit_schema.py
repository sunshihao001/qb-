import json
from pathlib import Path
ROOT=Path('/root/sikk-quant-runner')

def test_pipeline_linkage_audit_schema_and_report():
    schema=json.load(open(ROOT/'contracts/pipeline_linkage_audit_schema.json'))
    report=json.load(open(ROOT/'data/coordination/latest/pipeline_linkage_audit_report.json'))
    for k in schema['required']:
        assert k in report
    assert report['repair_status'] in ['REPAIRED','PASS','PATCH_REQUIRED']
    assert not [x for x in report['broken_links'] if x.get('priority')=='P0']
