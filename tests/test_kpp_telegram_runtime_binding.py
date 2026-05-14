import json
from pathlib import Path

ROOT = Path('/root/sikk-gmgn')
FIXTURE = ROOT / 'tests/fixtures/kpp/sample_system_design_doc.md'
OUT = ROOT / 'data/knowledge_processing_program/telegram_runtime_binding/test_runs'
QUEUE = ROOT / 'hermes_harness/03_task_runtime/input_governance_queue.jsonl'


def test_kpp_runtime_binding_dispatches_uploaded_file_and_query_command():
    from telegram_panel.commands.kpp_runtime_binding import dispatch_kpp_text_command, dispatch_kpp_uploaded_file

    upload = dispatch_kpp_uploaded_file(
        downloaded_file_path=FIXTURE,
        telegram_context={'chat_id': 'BIND_CHAT', 'message_id': 'BIND_MSG', 'user_id': 'BIND_USER'},
        output_root=OUT,
        queue_path=QUEUE,
        run_id='TEST-KPP-RUNTIME-BINDING',
        doc_id='TEST-KPP-RUNTIME-DOC',
    )

    assert upload['handled'] is True
    assert upload['ok'] is True
    assert 'KPP 文档处理完成' in upload['reply_text']
    assert 'TEST-KPP-RUNTIME-BINDING' in upload['reply_text']

    status = dispatch_kpp_text_command('/kpp_status TEST-KPP-RUNTIME-BINDING', search_roots=[OUT])
    assert status['handled'] is True
    assert 'KPP_READY_FOR_GOVERNANCE_QUEUE_WITH_CANDIDATES' in status['reply_text']


def test_kpp_runtime_binding_ignores_non_kpp_command_and_exports_manifest(tmp_path):
    from telegram_panel.commands.kpp_runtime_binding import dispatch_kpp_text_command, export_binding_manifest, is_kpp_command

    assert is_kpp_command('/kpp_panel RUN') is True
    assert is_kpp_command('/start') is False
    ignored = dispatch_kpp_text_command('/start')
    assert ignored['handled'] is False

    manifest_path = tmp_path / 'binding_manifest.json'
    manifest = export_binding_manifest(manifest_path)
    assert manifest['status'] == 'READY_FOR_RUNTIME_REGISTRY_IMPORT'
    assert '/kpp_status' in manifest['commands']
    saved = json.loads(manifest_path.read_text())
    assert saved['safety']['production_mutation_allowed'] is False
