from pathlib import Path
import shutil
from her_pipeline_lib import write_json, trace, text_sections, infer_key_points, sha256_file, utcnow

def run(run_dir: Path, run_id: str, document: Path, goal_data: dict, repo_root: Path):
    trace(run_dir, run_id, 'K00', 'phase_started', 'STARTED')
    input_doc = run_dir/'input/raw_document.md'
    input_goal = run_dir/'input/operator_goal.json'
    input_doc.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(document, input_doc)
    write_json(input_goal, goal_data)
    text = input_doc.read_text(encoding='utf-8', errors='replace')
    doc_id = f'doc_{run_id}'
    target_phase_candidates = ['K00','F00','V00','A00','H00','U00','G00','O00']
    execution_boundary = {
      'allow_file_write': True,
      'allow_code_write': False,
      'allow_tests': True,
      'allow_runner_binding': False,
      'allowed_modes': ['SAFE_MODE_LOCAL_FILES_ONLY']
    }
    write_policy = {
      'raw_documents': 'APPEND_ONLY',
      'run_outputs': 'RUN_ID_SCOPED_WRITE',
      'trace_audit': 'APPEND_ONLY',
      'code_patch': 'PLAN_ONLY'
    }
    passport = {
      'doc_id': doc_id, 'source_name': document.name, 'source_type': 'SYSTEM_CONSTRUCTION_MATERIAL',
      'received_at': utcnow(), 'raw_path': 'input/raw_document.md', 'sha256': sha256_file(input_doc),
      'document_role': {'primary_role': 'system_building_material', 'secondary_roles': ['methodology','controller_design','function_realization','validation_or_governance']},
      'summary': {'core_intent': '让真实 GPT 研究资料 / 系统建设资料进入 HER，按主链路跑完，生成完整文件输出，保留 gap。', 'key_points': infer_key_points(text)},
      'system_mapping': {'affected_planes': ['input','K00','F00','V00','A00','H00','U00','G00','O00','trace','audit'], 'affected_controllers': target_phase_candidates, 'affected_outputs': ['system/her_document_function_system','tools','tests/her_document_function_system','data/her_document_function_system/runs']},
      'status': 'K00_READY_WITH_GAPS'
    }
    corpus = {'doc_id': doc_id, 'raw_path': 'input/raw_document.md', 'sections': text_sections(text), 'key_points': passport['summary']['key_points'], 'status': 'CORPUS_INDEX_READY_WITH_GAPS'}
    mapping = {'doc_id': doc_id, 'repo_root': str(repo_root), 'system_definition_root': 'system/her_document_function_system', 'run_output_root': 'data/her_document_function_system/runs', 'target_phase_candidates': target_phase_candidates, 'status': 'SYSTEM_MAPPING_READY_WITH_GAPS'}
    gap_detection = {
      'doc_id': doc_id,
      'status': 'GAP_DETECTION_READY_WITH_GAPS',
      'gaps': [
        {'gap_id':'gap_real_semantic_extraction_limited','gap_level':'MEDIUM_GAP','route_to':'U00','status':'OPEN','description':'K00 safe-mode writer preserves document facts but does not claim complete semantic absorption.'}
      ],
      'blocking_gaps': []
    }
    handoff = {
      'handoff_id': f'k00_handoff_{run_id}',
      'from_phase': 'K00',
      'to_phase': 'F00',
      'k00_status': 'K00_READY_WITH_GAPS',
      'status': 'K00_HANDOFF_READY_WITH_GAPS',
      'artifact_refs': {
        'document_passport':'k00/document_passport.json',
        'corpus_index':'k00/corpus_index.json',
        'system_mapping':'k00/system_mapping.json',
        'gap_detection':'k00/gap_detection.json'
      },
      'refs': {
        'document_passport':'k00/document_passport.json',
        'corpus_index':'k00/corpus_index.json',
        'system_mapping':'k00/system_mapping.json',
        'gap_detection':'k00/gap_detection.json'
      },
      'document_passport_refs': ['k00/document_passport.json'],
      'corpus_index_refs': ['k00/corpus_index.json'],
      'system_mapping_refs': ['k00/system_mapping.json'],
      'gap_detection_refs': ['k00/gap_detection.json'],
      'target_phase_candidates': target_phase_candidates,
      'execution_boundary': execution_boundary,
      'write_policy': write_policy,
      'repo_root': str(repo_root),
      'gaps': gap_detection['gaps']
    }
    write_json(run_dir/'k00/document_passport.json', passport)
    write_json(run_dir/'k00/corpus_index.json', corpus)
    write_json(run_dir/'k00/system_mapping.json', mapping)
    write_json(run_dir/'k00/gap_detection.json', gap_detection)
    write_json(run_dir/'k00/k00_handoff_packet.json', handoff)
    trace(run_dir, run_id, 'K00', 'phase_completed', 'K00_READY_WITH_GAPS')
    return handoff
