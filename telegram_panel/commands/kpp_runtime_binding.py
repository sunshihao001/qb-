from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

from modules.knowledge_processing_program.telegram_query import handle_kpp_command
from modules.knowledge_processing_program.upload_gateway_adapter import handle_telegram_upload_event

KPP_COMMANDS = {
    '/kpp_status',
    '/kpp_panel',
    '/kpp_handoff',
    '/kpp_report',
    '/kpp_candidates',
    '/kpp_governance',
}


class TelegramLikeMessage(Protocol):
    text: str | None


class TelegramLikeUpdate(Protocol):
    message: Any


def is_kpp_command(text: str | None) -> bool:
    if not text:
        return False
    first = text.strip().split(maxsplit=1)[0]
    return first in KPP_COMMANDS


def dispatch_kpp_text_command(text: str, *, search_roots: list[str | Path] | None = None) -> dict[str, Any]:
    """Dispatch a Telegram text command into the KPP query surface.

    Returns a small platform-neutral reply envelope so any Telegram runtime can
    send it with its own API (`reply_text`, `send_message`, webhook JSON, etc.).
    """
    if not is_kpp_command(text):
        return {'handled': False, 'reply_text': ''}
    reply = handle_kpp_command(text, search_roots=search_roots)
    return {
        'handled': True,
        'reply_text': reply,
        'parse_mode': None,
        'safe_to_send': True,
    }


def dispatch_kpp_uploaded_file(
    *,
    downloaded_file_path: str | Path,
    telegram_context: dict[str, Any] | None = None,
    output_root: str | Path | None = None,
    queue_path: str | Path | None = None,
    run_id: str | None = None,
    doc_id: str | None = None,
) -> dict[str, Any]:
    """Dispatch a downloaded Telegram document to the KPP upload adapter.

    This function assumes the platform-specific bot runtime has already
    downloaded the Telegram file to a local path. It does not require a token and
    does not perform network I/O, making it safe to test and reusable across
    python-telegram-bot, aiogram, or webhook runtimes.
    """
    result = handle_telegram_upload_event(
        file_path=downloaded_file_path,
        telegram_context=telegram_context or {},
        output_root=output_root,
        queue_path=queue_path,
        run_id=run_id,
        doc_id=doc_id,
    )
    if result.get('ok'):
        reply = result['telegram_reply_text']
    else:
        reply = (
            'KPP 文档处理阻塞\n'
            f"run_id: {result.get('run_id')}\n"
            f"status: {result.get('status')}\n"
            f"reason: {result.get('blocker_reason')}"
        )
    return {
        'handled': True,
        'ok': bool(result.get('ok')),
        'reply_text': reply,
        'result': result,
        'safe_to_send': True,
    }


def build_python_telegram_bot_handlers(application: Any, *, output_root: str | Path | None = None, queue_path: str | Path | None = None) -> dict[str, Any]:
    """Register handlers on a python-telegram-bot v20+ Application.

    This function imports python-telegram-bot lazily. It is optional glue for a
    deployed runtime; tests should use the platform-neutral dispatch functions.
    """
    try:
        from telegram.ext import CommandHandler, MessageHandler, filters
    except Exception as exc:  # pragma: no cover - runtime dependency optional
        raise RuntimeError('python-telegram-bot is required for direct Application binding') from exc

    async def _command(update: Any, context: Any) -> None:  # pragma: no cover - requires live telegram runtime
        text = getattr(getattr(update, 'message', None), 'text', '') or ''
        envelope = dispatch_kpp_text_command(text)
        if envelope['handled']:
            await update.message.reply_text(envelope['reply_text'])

    async def _document(update: Any, context: Any) -> None:  # pragma: no cover - requires live telegram runtime
        message = update.message
        document = message.document
        tg_file = await context.bot.get_file(document.file_id)
        download_dir = Path('/tmp/sikk_kpp_telegram_uploads')
        download_dir.mkdir(parents=True, exist_ok=True)
        target = download_dir / f"{message.chat_id}_{message.message_id}_{document.file_name or document.file_unique_id}"
        await tg_file.download_to_drive(custom_path=str(target))
        envelope = dispatch_kpp_uploaded_file(
            downloaded_file_path=target,
            telegram_context={
                'chat_id': str(message.chat_id),
                'message_id': str(message.message_id),
                'user_id': str(getattr(message.from_user, 'id', '')),
                'filename': document.file_name,
                'file_id': document.file_id,
                'file_unique_id': document.file_unique_id,
            },
            output_root=output_root,
            queue_path=queue_path,
        )
        await message.reply_text(envelope['reply_text'])

    registered = []
    for command in sorted(cmd.strip('/') for cmd in KPP_COMMANDS):
        handler = CommandHandler(command, _command)
        application.add_handler(handler)
        registered.append(command)
    doc_handler = MessageHandler(filters.Document.ALL, _document)
    application.add_handler(doc_handler)
    return {'registered_commands': registered, 'document_handler_registered': True}


def export_binding_manifest(path: str | Path) -> dict[str, Any]:
    manifest = {
        'binding': 'kpp_telegram_runtime_binding',
        'status': 'READY_FOR_RUNTIME_REGISTRY_IMPORT',
        'platform_neutral_functions': [
            'dispatch_kpp_text_command',
            'dispatch_kpp_uploaded_file',
        ],
        'optional_python_telegram_bot_entry': 'build_python_telegram_bot_handlers(application)',
        'commands': sorted(KPP_COMMANDS),
        'safety': {
            'candidate_only': True,
            'production_mutation_allowed': False,
            'real_swap': False,
            'signing': False,
            'broadcast': False,
            'private_key_access': False,
        },
    }
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    return manifest
