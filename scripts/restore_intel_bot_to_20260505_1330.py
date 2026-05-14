#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CUTOVER_COMMIT = 'e91828c'
CUTOVER_BJ = '2026-05-05T13:30:00+08:00'
TARGETS = [
    Path('结构分析/jiegoufenxibot'),
    Path('data/gmgn_candidates_live_run/intel-bot'),
    Path('data/gmgn_candidates_live_run/intel_bot'),
    Path('data/gmgn_candidates_live_run/wallet_structure'),
    Path('data/wallet_intelligence'),
]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=check)


def list_tree(commit: str, rel: Path) -> set[str]:
    cp = run(['git', 'ls-tree', '-r', '--name-only', commit, '--', str(rel)])
    return {line for line in cp.stdout.splitlines() if line.strip()}


def working_files(rel: Path) -> set[str]:
    p = ROOT / rel
    if not p.exists():
        return set()
    return {str(x.relative_to(ROOT)) for x in p.rglob('*') if x.is_file()}


def remove_path(rel: Path, dry_run: bool, actions: list[dict]):
    p = ROOT / rel
    if not p.exists():
        return
    files = [x for x in p.rglob('*') if x.is_file()] if p.is_dir() else [p]
    actions.append({'action': 'remove_working_path', 'path': str(rel), 'files': len(files)})
    if not dry_run:
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()


def checkout_from_commit(rel: Path, dry_run: bool, actions: list[dict]):
    files = list_tree(CUTOVER_COMMIT, rel)
    if not files:
        actions.append({'action': 'no_commit_snapshot', 'path': str(rel), 'commit': CUTOVER_COMMIT})
        return
    actions.append({'action': 'restore_from_commit', 'path': str(rel), 'commit': CUTOVER_COMMIT, 'files': len(files)})
    if not dry_run:
        run(['git', 'checkout', CUTOVER_COMMIT, '--', str(rel)])


def main():
    ap = argparse.ArgumentParser(description='Restore Intel/jiegoufenxibot data to BJ 2026-05-05 13:30 cutover.')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    actions=[]
    for rel in TARGETS:
        before_working = working_files(rel)
        commit_files = list_tree(CUTOVER_COMMIT, rel)
        # Remove every working file/dir first so files created after cutover disappear.
        remove_path(rel, args.dry_run, actions)
        # Restore only paths that existed at the cutover commit.
        checkout_from_commit(rel, args.dry_run, actions)
        actions.append({
            'action': 'summary',
            'path': str(rel),
            'working_files_before': len(before_working),
            'commit_files': len(commit_files),
        })

    report = {
        'schema_version': '1.0.0',
        'dry_run': args.dry_run,
        'cutover_bj': CUTOVER_BJ,
        'cutover_commit': CUTOVER_COMMIT,
        'run_time_utc': datetime.now(timezone.utc).isoformat(),
        'targets': [str(x) for x in TARGETS],
        'actions': actions,
    }
    report_path = ROOT / 'restore_intel_bot_to_20260505_1330_report.json'
    if not args.dry_run:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        'dry_run': args.dry_run,
        'cutover_bj': CUTOVER_BJ,
        'cutover_commit': CUTOVER_COMMIT,
        'report': str(report_path.relative_to(ROOT)),
        'actions': actions,
    }, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
