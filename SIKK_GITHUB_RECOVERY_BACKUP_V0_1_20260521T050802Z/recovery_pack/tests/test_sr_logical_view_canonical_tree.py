from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_sr_logical_view_doc_exists_and_forbids_physical_split():
    p=ROOT/'docs/SR_LOGICAL_VIEW_CANONICAL_ARTIFACT_TREE.md'
    assert p.exists()
    text=p.read_text()
    assert 'S/R 是两套运行视图，不是两套数据目录' in text
    assert 'S00-S10 = Operating Lifecycle View' in text
    assert 'R00-R13 = Research-to-Execution Validation Pipeline View' in text
    for forbidden in ['Do not copy raw', 'Do not copy feature', 'Do not create two `decision_ticket`']:
        assert forbidden in text

def test_s_to_r_map_has_canonical_tree_rule_and_all_s_stages():
    text=(ROOT/'docs/stage_maps/s_to_r_pipeline_map.yaml').read_text()
    assert 'canonical_artifact_tree_rule:' in text
    assert 'sr_physical_split_allowed' in text
    for i in range(11):
        assert f'S{i:02d}:' in text
    assert 'duplicate_decision_ticket_under_s_and_r' in text

def test_core_docs_reference_sr_logical_rule():
    for rel in ['PROJECT_RULES.md','docs/METHODOLOGY_KERNEL.md','docs/SIKK_QUANT_RUNNER_OPERATING_BACKBONE_V0_1.md']:
        text=(ROOT/rel).read_text()
        assert 'S/R Logical View + Canonical Artifact Tree' in text
        assert '禁止复制 raw、feature、decision_ticket' in text
