from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
RUN_ID=(ROOT/'data/latest/s01_fresh_run_id.txt').read_text().strip()
BASE=ROOT/'data/runs'/RUN_ID/'features'


def test_s02_feature_artifacts_exist():
    for name in ['feature_snapshot_from_canonical_mapping.json','feature_lineage_from_canonical_mapping.json','missing_feature_report_from_canonical_mapping.json','s02_feature_engineering_report.json','s02_feature_engineering_gate.json']:
        assert (BASE/name).exists(), name


def test_feature_snapshot_is_from_mapping_and_no_manual_fill():
    snap=json.loads((BASE/'feature_snapshot_from_canonical_mapping.json').read_text())
    assert snap['input_mapping'].endswith('gmgn_source_to_sikk_canonical_mapping.json')
    assert snap['manual_fill_used'] is False
    assert snap['feature_count'] >= 10
    for feature in snap['features']:
        assert feature['manual_fill_used'] is False
        assert feature['downstream_consumer']
        assert feature['transformation_owner']=='S02_FEATURE_ENGINEERING_FROM_CANONICAL_MAPPING_RUN'
        if feature['status']=='MISSING':
            assert feature['missing_reason']
            assert feature['value'] is None
    assert snap['stage_metadata']['s_stage']=='S02'
    assert snap['stage_metadata']['r_stage']==['R04']
    assert snap['stage_metadata']['sr_physical_split_allowed'] is False


def test_feature_lineage_preserves_mapping_missing_reason():
    lineage=json.loads((BASE/'feature_lineage_from_canonical_mapping.json').read_text())
    assert lineage['input_mapping'].endswith('gmgn_source_to_sikk_canonical_mapping.json')
    for item in lineage['lineage']:
        assert item['manual_fill_used'] is False
        assert item['downstream_consumer']
        for row in item['mapping_rows_used']:
            if row['mapping_type']=='missing_source':
                assert row['missing_reason']


def test_s02_gate_blocks_paper_and_allows_structure_next():
    gate=json.loads((BASE/'s02_feature_engineering_gate.json').read_text())
    assert gate['input_mapping_exists'] is True
    assert gate['feature_snapshot_from_mapping'] is True
    assert gate['manual_fill_used'] is False
    assert gate['all_missing_features_have_reason'] is True
    assert gate['paper_readiness_allowed'] is False
    assert gate['paper_runner_allowed'] is False
    assert gate['allowed_next_stage']=='S04_STRUCTURE_SIGNAL_FROM_FEATURE_SNAPSHOT_RUN'
