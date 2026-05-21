from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID=(ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
BASE=ROOT/'data/runs'/RUN_ID/'source_to_canonical'


def test_gmgn_source_to_canonical_artifacts_exist():
    for name in ['sikk_canonical_domain_model_minimal.json','gmgn_source_to_sikk_canonical_mapping.json','gmgn_mapping_coverage_report.json','gmgn_source_to_canonical_gate.json']:
        assert (BASE/name).exists(), name


def test_canonical_model_has_required_objects():
    model=json.loads((BASE/'sikk_canonical_domain_model_minimal.json').read_text())
    objects=model['objects']
    for name in ['Token','Pool','Kline','Holder','Wallet','TraderProfit','SecurityRaw','RawSnapshot']:
        assert name in objects
        assert objects[name]['fields']
        assert objects[name]['downstream_consumer']
    assert model['stage_metadata']['sr_physical_split_allowed'] is False


def test_mapping_rows_have_owner_downstream_and_missing_reason():
    mapping=json.loads((BASE/'gmgn_source_to_sikk_canonical_mapping.json').read_text())
    rows=mapping['mapping_rows']
    assert len(rows) >= 20
    route_ids={r['route_id'] for r in rows}
    assert {'token_info','market_pool','security_read_if_safe'}.issubset(route_ids)
    for row in rows:
        assert row['transformation_owner']=='GMGN_SOURCE_TO_SIKK_CANONICAL_MAPPING_RUN'
        assert row['downstream_consumer']
        assert row['canonical_domain_object']
        assert row['canonical_field']
        assert row['stage_metadata']['s_stage']=='S02'
        assert row['stage_metadata']['r_stage']==['R04']
        if row['mapping_type']=='missing_source':
            assert row['missing_reason']


def test_gate_blocks_paper_and_allows_feature_engineering_next():
    gate=json.loads((BASE/'gmgn_source_to_canonical_gate.json').read_text())
    assert gate['gmgn_router_plan_exists'] is True
    assert gate['source_to_canonical_mapping_exists'] is True
    assert gate['all_rows_have_downstream_consumer'] is True
    assert gate['all_rows_have_missing_reason_when_source_missing'] is True
    assert gate['paper_readiness_allowed'] is False
    assert gate['paper_runner_allowed'] is False
    assert gate['allowed_next_stage']=='S02_FEATURE_ENGINEERING_FROM_CANONICAL_MAPPING_RUN'
