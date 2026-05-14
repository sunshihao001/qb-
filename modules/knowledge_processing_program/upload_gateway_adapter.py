from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .kpp_total_runner import DEFAULT_QUEUE, ROOT, run_chain

TEXT_SUFFIXES = {'.md', '.txt', '.json', '.yaml', '.yml', '.csv', '.log'}
DOCX_SUFFIXES = {'.docx'}
PDF_SUFFIXES = {'.pdf'}
IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff'}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n')


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def _safe_name(name: str) -> str:
    return ''.join(ch if ch.isalnum() or ch in '._-' else '_' for ch in name)[:160] or 'upload'


def normalize_source_to_markdown(source_path: Path, output_path: Path) -> dict[str, Any]:
    """Convert an uploaded source file into KPP-readable markdown text.

    This is intentionally conservative: native text and zip text bundles are supported;
    PDF/DOCX/OCR hooks are declared as blockers unless the runtime dependency is present.
    """
    suffix = source_path.suffix.lower()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if suffix in TEXT_SUFFIXES:
        text = source_path.read_text(errors='replace')
        output_path.write_text(text)
        return {'ok': True, 'adapter': 'plain_text', 'normalized_text_path': str(output_path), 'source_files': [str(source_path)]}

    if suffix == '.zip':
        parts: list[str] = []
        source_files: list[str] = []
        with zipfile.ZipFile(source_path) as zf:
            for info in sorted(zf.infolist(), key=lambda item: item.filename):
                if info.is_dir():
                    continue
                inner = Path(info.filename)
                if inner.suffix.lower() not in TEXT_SUFFIXES:
                    continue
                data = zf.read(info.filename).decode('utf-8', errors='replace')
                parts.append(f"\n\n# ZIP_FILE: {info.filename}\n\n{data}")
                source_files.append(info.filename)
        if not parts:
            return {'ok': False, 'status': 'BLOCKED_SOURCE_ADAPTER_REQUIRED', 'blocker_reason': 'ZIP contains no supported text/markdown/json/yaml/csv/log files.'}
        output_path.write_text('\n'.join(parts).strip() + '\n')
        return {'ok': True, 'adapter': 'zip_text_bundle', 'normalized_text_path': str(output_path), 'source_files': source_files}

    if suffix in PDF_SUFFIXES:
        return {'ok': False, 'status': 'BLOCKED_SOURCE_ADAPTER_REQUIRED', 'blocker_reason': 'PDF adapter/OCR extraction is required before KPP can process this upload.'}

    if suffix in DOCX_SUFFIXES:
        return {'ok': False, 'status': 'BLOCKED_SOURCE_ADAPTER_REQUIRED', 'blocker_reason': 'DOCX adapter is required before KPP can process this upload.'}

    if suffix in IMAGE_SUFFIXES:
        return {'ok': False, 'status': 'BLOCKED_SOURCE_ADAPTER_REQUIRED', 'blocker_reason': 'OCR adapter is required before KPP can process image uploads.'}

    return {'ok': False, 'status': 'BLOCKED_SOURCE_ADAPTER_REQUIRED', 'blocker_reason': f'Unsupported upload suffix: {suffix or "<none>"}'}


def _telegram_reply(panel: dict[str, Any]) -> str:
    return (
        'KPP 文档处理完成\n'
        f"run_id: {panel.get('run_id')}\n"
        f"doc_id: {panel.get('doc_id')}\n"
        f"status: {panel.get('overall_status')}\n"
        f"current_stage: {panel.get('current_stage')}\n"
        f"governance: {panel.get('governance_queue_status')}\n"
        f"next: {panel.get('next_action')}\n"
        f"commands: {' / '.join(panel.get('query_commands', []))}"
    )


def handle_telegram_upload_event(
    *,
    file_path: str | Path,
    telegram_context: dict[str, Any] | None = None,
    output_root: str | Path | None = None,
    queue_path: str | Path | None = None,
    run_id: str | None = None,
    doc_id: str | None = None,
    input_classification: str = 'system_building_material',
) -> dict[str, Any]:
    source_path = Path(file_path)
    if not source_path.exists():
        raise FileNotFoundError(source_path)

    digest = _sha256_file(source_path)[:12]
    run_id = run_id or f'KPP-TG-{digest}'
    doc_id = doc_id or f'DOC-TG-{digest}'
    output_root = Path(output_root or (ROOT / 'data/knowledge_processing_program/telegram_upload_productization/runs'))
    queue_path = Path(queue_path or DEFAULT_QUEUE)
    run_root = output_root / run_id
    k00 = run_root / 'K00'
    upload_dir = k00 / 'uploaded_source'
    upload_dir.mkdir(parents=True, exist_ok=True)
    staged_source = upload_dir / f'{doc_id}_{digest}_{_safe_name(source_path.name)}'
    if not staged_source.exists():
        shutil.copy2(source_path, staged_source)

    normalized_path = k00 / 'normalized_text.md'
    normalized = normalize_source_to_markdown(staged_source, normalized_path)
    if not normalized.get('ok'):
        blocker = {
            'run_id': run_id,
            'doc_id': doc_id,
            'status': normalized.get('status', 'BLOCKED_SOURCE_ADAPTER_REQUIRED'),
            'blocker_reason': normalized.get('blocker_reason'),
            'source_path': str(source_path),
            'staged_source': str(staged_source),
            'telegram_context': telegram_context or {},
            'created_at': _now(),
            'candidate_only': True,
            'production_mutation_allowed': False,
        }
        _write_json(run_root / 'BLOCKER_REPORT.json', blocker)
        return {'ok': False, **blocker}

    request = {
        'run_id': run_id,
        'doc_id': doc_id,
        'source_type': 'telegram_upload',
        'source_path': str(normalized_path),
        'original_source_path': str(source_path),
        'staged_source_path': str(staged_source),
        'normalized_source_adapter': normalized.get('adapter'),
        'normalized_source_files': normalized.get('source_files', []),
        'telegram_context': telegram_context or {},
        'input_classification': input_classification,
        'output_root': str(output_root),
        'queue_path': str(queue_path),
        'telegram_panel': True,
        'candidate_only': True,
    }
    request_path = k00 / 'telegram_run_request.json'
    _write_json(request_path, request)
    result = run_chain(request)
    panel_path = Path(result['run_root']) / 'K08' / 'telegram_status_panel.json'
    panel = json.loads(panel_path.read_text())

    # Enrich K00 manifest after runner writes it, preserving validator-required fields.
    manifest_path = Path(result['run_root']) / 'K00' / 'raw_source_manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest.update({
        'source_type': 'telegram_upload',
        'original_source_path': str(source_path),
        'staged_source_path': str(staged_source),
        'normalized_text_path': str(normalized_path),
        'normalized_source_adapter': normalized.get('adapter'),
        'telegram_context': telegram_context or {},
    })
    _write_json(manifest_path, manifest)

    reply = _telegram_reply(panel)
    return {
        'ok': True,
        'run_id': result['run_id'],
        'doc_id': doc_id,
        'run_root': result['run_root'],
        'queue_entry_id': result['queue_entry_id'],
        'overall_status': panel.get('overall_status'),
        'telegram_panel_path': str(panel_path),
        'telegram_reply_text': reply,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--chat-id', default='')
    parser.add_argument('--message-id', default='')
    parser.add_argument('--run-id')
    parser.add_argument('--doc-id')
    parser.add_argument('--output-root')
    parser.add_argument('--queue-path')
    args = parser.parse_args(argv)
    result = handle_telegram_upload_event(
        file_path=args.file,
        telegram_context={'chat_id': args.chat_id, 'message_id': args.message_id},
        output_root=args.output_root,
        queue_path=args.queue_path,
        run_id=args.run_id,
        doc_id=args.doc_id,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get('ok') else 1


if __name__ == '__main__':
    raise SystemExit(main())
