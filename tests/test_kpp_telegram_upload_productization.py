import json
import zipfile
from pathlib import Path

import pytest

ROOT = Path('/root/sikk-gmgn')
FIXTURE = ROOT / 'tests/fixtures/kpp/sample_system_design_doc.md'
OUT = ROOT / 'data/knowledge_processing_program/telegram_upload_productization/test_runs'
QUEUE = ROOT / 'hermes_harness/03_task_runtime/input_governance_queue.jsonl'


def test_telegram_upload_adapter_saves_file_runs_kpp_and_returns_panel_summary(tmp_path):
    from modules.knowledge_processing_program.upload_gateway_adapter import handle_telegram_upload_event

    result = handle_telegram_upload_event(
        file_path=FIXTURE,
        telegram_context={
            'chat_id': 'TEST_CHAT',
            'message_id': 'MSG001',
            'user_id': 'USER001',
            'filename': 'sample_system_design_doc.md',
        },
        output_root=OUT,
        queue_path=QUEUE,
        run_id='TEST-KPP-TELEGRAM-UPLOAD',
        doc_id='TEST-KPP-TELEGRAM-DOC',
    )

    assert result['ok'] is True
    assert result['run_id'] == 'TEST-KPP-TELEGRAM-UPLOAD'
    assert result['overall_status'] == 'KPP_READY_FOR_GOVERNANCE_QUEUE_WITH_CANDIDATES'
    assert result['telegram_reply_text'].startswith('KPP 文档处理完成')
    run_root = OUT / 'TEST-KPP-TELEGRAM-UPLOAD'
    assert (run_root / 'K00/raw_source_manifest.json').exists()
    assert (run_root / 'K00/normalized_text.md').exists()
    assert (run_root / 'K08/telegram_status_panel.json').exists()
    manifest = json.loads((run_root / 'K00/raw_source_manifest.json').read_text())
    assert manifest['source_type'] == 'telegram_upload'
    assert manifest['telegram_context']['chat_id'] == 'TEST_CHAT'
    assert manifest['normalized_text_path'].endswith('K00/normalized_text.md')


def test_kpp_telegram_query_commands_return_status_panel_and_handoff():
    from modules.knowledge_processing_program.telegram_query import handle_kpp_command

    status = handle_kpp_command('/kpp_status TEST-KPP-TELEGRAM-UPLOAD', search_roots=[OUT])
    panel = handle_kpp_command('/kpp_panel TEST-KPP-TELEGRAM-UPLOAD', search_roots=[OUT])
    handoff = handle_kpp_command('/kpp_handoff TEST-KPP-TELEGRAM-UPLOAD', search_roots=[OUT])

    assert 'KPP_READY_FOR_GOVERNANCE_QUEUE_WITH_CANDIDATES' in status
    assert 'current_stage: K08' in status
    assert 'candidate_count:' in panel
    assert 'handoff_packet.json' in handoff
    assert 'manual_governance_or_P00_review_required' in handoff


def test_zip_source_adapter_extracts_text_and_runs(tmp_path):
    from modules.knowledge_processing_program.upload_gateway_adapter import handle_telegram_upload_event

    zip_path = tmp_path / 'docs.zip'
    with zipfile.ZipFile(zip_path, 'w') as zf:
        zf.writestr('a.md', '# Zip KPP Doc\n\nKPP candidate-only governance document.')
        zf.writestr('nested/b.txt', 'second text file')

    result = handle_telegram_upload_event(
        file_path=zip_path,
        telegram_context={'chat_id': 'TEST_CHAT', 'message_id': 'MSGZIP'},
        output_root=OUT,
        queue_path=QUEUE,
        run_id='TEST-KPP-ZIP-UPLOAD',
        doc_id='TEST-KPP-ZIP-DOC',
    )

    assert result['ok'] is True
    normalized = (OUT / 'TEST-KPP-ZIP-UPLOAD/K00/normalized_text.md').read_text()
    assert 'Zip KPP Doc' in normalized
    assert 'second text file' in normalized


def test_unsupported_image_upload_writes_blocker_without_running_kpp(tmp_path):
    from modules.knowledge_processing_program.upload_gateway_adapter import handle_telegram_upload_event

    image = tmp_path / 'scan.png'
    image.write_bytes(b'not-a-real-image')

    result = handle_telegram_upload_event(
        file_path=image,
        telegram_context={'chat_id': 'TEST_CHAT', 'message_id': 'MSGIMG'},
        output_root=OUT,
        queue_path=QUEUE,
        run_id='TEST-KPP-IMAGE-UPLOAD',
        doc_id='TEST-KPP-IMAGE-DOC',
    )

    assert result['ok'] is False
    assert result['status'] == 'BLOCKED_SOURCE_ADAPTER_REQUIRED'
    assert 'OCR' in result['blocker_reason']
    assert (OUT / 'TEST-KPP-IMAGE-UPLOAD/BLOCKER_REPORT.json').exists()
