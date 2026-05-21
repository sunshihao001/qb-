from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID=(ROOT/'data/latest/gmgn_raw_field_discovery_run_id.txt').read_text().strip()
BASE=ROOT/'data/runs'/RUN_ID


def test_raw_field_discovery_core_artifacts_exist():
    for rel in [
        'field_inventory/gmgn_source_capability_discovery.json',
        'field_inventory/gmgn_raw_field_inventory.json',
        'source_to_canonical/gmgn_raw_field_to_canonical_mapping.json',
        'gmgn_raw_field_discovery_report.json',
        'gmgn_raw_field_discovery_gate.json',
    ]:
        assert (BASE/rel).exists(), rel


def test_request_response_error_saved_for_routes():
    cap=json.loads((BASE/'field_inventory/gmgn_source_capability_discovery.json').read_text())
    assert len(cap['capabilities']) >= 8
    for c in cap['capabilities']:
        assert (ROOT/c['request_path']).exists()
        assert (ROOT/c['response_path']).exists()
        assert (ROOT/c['error_path']).exists()
        assert c['read_only'] is True
        assert c['downstream_consumer']
    assert 'security_read_if_safe' in {c['route_id'] for c in cap['capabilities']}
    security=[c for c in cap['capabilities'] if c['route_id']=='security_read_if_safe'][0]
    assert (ROOT/security['request_path']).exists()
    req=json.loads((ROOT/security['request_path']).read_text())
    assert req['read_only'] is True
    assert req.get('relaxed_discovery_mode') is True


def test_inventory_and_mapping_are_raw_only_no_feature():
    inv=json.loads((BASE/'field_inventory/gmgn_raw_field_inventory.json').read_text())
    mapping=json.loads((BASE/'source_to_canonical/gmgn_raw_field_to_canonical_mapping.json').read_text())
    assert 'fields' in inv
    assert mapping['mapping_rows']
    for row in mapping['mapping_rows']:
        assert row['transformation_owner']=='GMGN_RAW_FIELD_DISCOVERY_RUN'
        assert row['downstream_consumer']
        assert row['mapping_type'] in {'raw_field_discovered_unmapped','missing_source'}
        if row['mapping_type']=='missing_source':
            assert row['missing_reason']
    assert inv['stage_metadata']['s_stage']=='S01'
    assert inv['stage_metadata']['r_stage']==['R02','R03']


def test_gate_blocks_downstream_execution():
    gate=json.loads((BASE/'gmgn_raw_field_discovery_gate.json').read_text())
    assert gate['fresh_call_attempted'] is True
    assert gate['request_response_error_saved'] is True
    assert gate['feature_computed'] is False
    assert gate['decision_ticket_created'] is False
    assert gate['paper_readiness_allowed'] is False
    assert gate['forbidden_scope_used'] is False
