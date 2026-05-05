#!/usr/bin/env python3
"""Backup sanitized @jiegoufenxibot Hermes profile data into the SIKK repo.

This script intentionally does NOT copy secrets or binary state databases:
- no .env
- no auth.json
- no state.db / response_store.db / kanban.db
- no lock/pid files

It copies/redacts human-readable session/log/memory data only into 结构分析/jiegoufenxibot.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/root/sikk-gmgn")
SRC = Path("/root/.hermes/profiles/jiegoufenxibot")
DEST = REPO / "结构分析" / "jiegoufenxibot"

TEXT_EXTS = {".json", ".jsonl", ".md", ".txt", ".log"}
REDACTIONS = [
    (re.compile(r"\b\d{6,}:[A-Za-z0-9_-]{20,}\b"), "[REDACTED_TELEGRAM_BOT_TOKEN]"),
    (re.compile(r"\bsk-[A-Za-z0-9._-]{12,}\b"), "sk-[REDACTED]"),
    (re.compile(r"(?i)(api[_-]?key|token|secret|password|authorization|bearer)(\s*[=:]\s*)['\"]?[^'\"\s,}]+"), r"\1\2[REDACTED]"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"), "gh_[REDACTED]"),
]

INCLUDE_FILES = [
    "channel_directory.json",
    "gateway_state.json",
]
INCLUDE_DIRS = [
    "sessions",
    "memories",
]
LOG_FILES = [
    "logs/agent.log",
    "logs/gateway.log",
    "logs/errors.log",
]


def run(cmd: list[str], cwd: Path = REPO, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=check)


def redact(text: str) -> str:
    for pat, repl in REDACTIONS:
        text = pat.sub(repl, text)
    return text


def read_text_safely(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def copy_redacted_file(src: Path, dst: Path) -> dict:
    dst.parent.mkdir(parents=True, exist_ok=True)
    raw = read_text_safely(src)
    safe = redact(raw)
    dst.write_text(safe, encoding="utf-8")
    return {
        "source": str(src),
        "dest": str(dst.relative_to(REPO)),
        "bytes": dst.stat().st_size,
        "sha256": hashlib.sha256(dst.read_bytes()).hexdigest(),
    }


def copy_tree_redacted(src_dir: Path, dst_dir: Path) -> list[dict]:
    copied: list[dict] = []
    if not src_dir.exists():
        return copied
    for src in sorted(src_dir.rglob("*")):
        if not src.is_file():
            continue
        if src.suffix not in TEXT_EXTS:
            continue
        rel = src.relative_to(src_dir)
        copied.append(copy_redacted_file(src, dst_dir / rel))
    return copied


def main() -> int:
    if not REPO.exists():
        print(f"ERROR repo missing: {REPO}", file=sys.stderr)
        return 2
    if not SRC.exists():
        print(f"ERROR profile missing: {SRC}", file=sys.stderr)
        return 2

    status = run(["git", "status", "--porcelain"], check=True).stdout.splitlines()
    allowed_prefixes = {"结构分析/", "scripts/backup_jiegoufenxibot_structure_data.py"}
    blocking = []
    for line in status:
        path = line[3:] if len(line) > 3 else line
        if line.startswith("?? ") and not any(path.startswith(p) or path == p.rstrip("/") for p in allowed_prefixes):
            continue
        if not any(path.startswith(p) or path == p.rstrip("/") for p in allowed_prefixes):
            blocking.append(line)
    if blocking:
        print("ERROR tracked/unexpected changes outside backup scope:")
        print("\n".join(blocking[:80]))
        return 3

    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True, exist_ok=True)

    copied: list[dict] = []
    for rel in INCLUDE_FILES:
        src = SRC / rel
        if src.exists() and src.is_file():
            copied.append(copy_redacted_file(src, DEST / "runtime" / rel))

    for rel in INCLUDE_DIRS:
        copied.extend(copy_tree_redacted(SRC / rel, DEST / rel))

    for rel in LOG_FILES:
        src = SRC / rel
        if src.exists() and src.is_file():
            out_name = rel.replace("/", "__") + ".txt"
            copied.append(copy_redacted_file(src, DEST / "redacted_logs" / out_name))

    now = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    manifest = {
        "backup_time": now,
        "source_profile": "jiegoufenxibot",
        "source_path": str(SRC),
        "destination": str(DEST.relative_to(REPO)),
        "copied_files": copied,
        "excluded_secret_or_binary_files": [
            ".env", "auth.json", "state.db", "state.db-wal", "state.db-shm",
            "response_store.db", "kanban.db", "gateway.pid", "gateway.lock", "auth.lock",
        ],
        "redaction_enabled": True,
        "note": "Sanitized backup of readable Telegram/Hermes session, memory and log data only. No bot token/private key/API secret files are copied.",
    }
    (DEST / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (DEST / "README.md").write_text(
        "# 结构分析 / jiegoufenxibot 备份\n\n"
        f"- 更新时间：`{now}`\n"
        "- 来源：Hermes profile `jiegoufenxibot`\n"
        "- 范围：sessions、memories、channel/runtime 摘要、脱敏 logs\n"
        "- 安全边界：不备份 `.env`、`auth.json`、数据库、token、私钥、API key。文本内容已做正则脱敏。\n"
        f"- 文件数量：`{len(copied)}`\n",
        encoding="utf-8",
    )

    run(["git", "add", "结构分析", "scripts/backup_jiegoufenxibot_structure_data.py"])
    diff = run(["git", "diff", "--cached", "--stat"], check=True).stdout.strip()
    if not diff:
        print("backup_status=no_changes")
        return 0

    msg = f"chore: backup jiegoufenxibot structure data {dt.datetime.now().strftime('%Y%m%d-%H%M')}"
    run(["git", "commit", "-m", msg])
    push = run(["git", "push", "origin", "main"], check=True).stdout
    print("backup_status=committed_and_pushed")
    print(diff)
    print(push.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
