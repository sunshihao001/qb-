import json
import sys
from pathlib import Path

TOOLS = Path('/root/sikk-gmgn/tools')
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import k00_document_intake


def test_k00_safe_mode_writer_emits_f00_legal_handoff(tmp_path):
    doc = tmp_path / 'source.md'
    doc.write_text('# 测试文档\n\n必须通过 K00/F00/V00，并保留 READY_WITH_GAPS。\n', encoding='utf-8')
    run_dir = tmp_path / 'run'
    repo_root = Path('/root/sikk-gmgn')

    k00_document_intake.run(run_dir, 'test_run', doc, {'goal_text': 'test'}, repo_root)

    expected_files = [
        'k00/document_passport.json',
        'k00/corpus_index.json',
        'k00/system_mapping.json',
        'k00/gap_detection.json',
        'k00/k00_handoff_packet.json',
    ]
    for rel in expected_files:
        assert (run_dir / rel).exists(), rel

    handoff = json.loads((run_dir / 'k00/k00_handoff_packet.json').read_text(encoding='utf-8'))
    assert handoff['from_phase'] == 'K00'
    assert handoff['to_phase'] == 'F00'
    assert handoff['k00_status'] == 'K00_READY_WITH_GAPS'
    assert handoff['artifact_refs']['gap_detection'] == 'k00/gap_detection.json'
    assert handoff['document_passport_refs'] == ['k00/document_passport.json']
    assert handoff['corpus_index_refs'] == ['k00/corpus_index.json']
    assert handoff['system_mapping_refs'] == ['k00/system_mapping.json']
    assert handoff['gap_detection_refs'] == ['k00/gap_detection.json']
    assert handoff['target_phase_candidates']
    assert handoff['repo_root'] == str(repo_root)
    assert handoff['execution_boundary']['allow_code_write'] is False
    assert handoff['write_policy']['code_patch'] == 'PLAN_ONLY'

    gap_detection = json.loads((run_dir / 'k00/gap_detection.json').read_text(encoding='utf-8'))
    assert gap_detection['status'] == 'GAP_DETECTION_READY_WITH_GAPS'
    assert gap_detection['gaps'][0]['status'] == 'OPEN'
