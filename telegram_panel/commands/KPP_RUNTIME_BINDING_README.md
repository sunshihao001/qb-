# KPP Telegram Runtime Binding

Status: READY_FOR_RUNTIME_REGISTRY_IMPORT

This directory contains the platform-level binding surface for KPP document uploads and query commands.

## Canonical module

```text
telegram_panel/commands/kpp_runtime_binding.py
```

## Platform-neutral functions

Use these when the deployed Telegram runtime already downloads files and sends replies itself:

```python
from telegram_panel.commands.kpp_runtime_binding import (
    dispatch_kpp_text_command,
    dispatch_kpp_uploaded_file,
)

# document/file upload path after Telegram runtime downloads it locally
reply_envelope = dispatch_kpp_uploaded_file(
    downloaded_file_path=downloaded_file,
    telegram_context={
        'chat_id': chat_id,
        'message_id': message_id,
        'user_id': user_id,
        'filename': filename,
    },
)
send_message(chat_id, reply_envelope['reply_text'])

# text command path
reply_envelope = dispatch_kpp_text_command('/kpp_status <run_id>')
if reply_envelope['handled']:
    send_message(chat_id, reply_envelope['reply_text'])
```

## Optional python-telegram-bot v20+ binding

If the runtime uses `python-telegram-bot` Application:

```python
from telegram_panel.commands.kpp_runtime_binding import build_python_telegram_bot_handlers

build_python_telegram_bot_handlers(application)
```

Registered commands:

```text
/kpp_status <run_id>
/kpp_panel <run_id>
/kpp_handoff <run_id>
/kpp_report <run_id>
/kpp_candidates <run_id>
/kpp_governance <run_id>
```

Document uploads are routed to:

```text
modules/knowledge_processing_program/upload_gateway_adapter.py
```

Command queries are routed to:

```text
modules/knowledge_processing_program/telegram_query.py
```

## Safety boundary

This binding does not allow production mutation:

```text
candidate_only: true
production_mutation_allowed: false
real_swap: false
signing: false
broadcast: false
private_key_access: false
paper/live runtime activation: false
```

Unsupported files are blocked with `BLOCKER_REPORT.json` instead of being silently processed.
