#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEL_ROOT = ROOT / 'data' / 'gmgn_candidates_live_run' / 'intel-bot'
LOGS_ROOT = INTEL_ROOT / 'logs'
CODE_ROOT = INTEL_ROOT / 'code'

MIGRATIONS = [
    {
        'name': 'legacy_intel_bot_contracts',
        'src': ROOT / 'data' / 'gmgn_candidates_live_run' / 'intel_bot',
        'dst': LOGS_ROOT / 'legacy_intel_bot',
        'kind': 'move',
    },
    {
        'name': 'wallet_structure_runtime',
        'src': ROOT / 'data' / 'gmgn_candidates_live_run' / 'wallet_structure',
        'dst': LOGS_ROOT / 'wallet_structure',
        'kind': 'move',
    },
    {
        'name': 'legacy_wallet_intelligence_archive',
        'src': ROOT / 'data' / 'wallet_intelligence',
        'dst': LOGS_ROOT / 'legacy_wallet_intelligence',
        'kind': 'move',
    },
    {
        'name': 'orchestrator_wallet_structure_snapshot',
        'src': ROOT / 'data' / 'gmgn_candidates_live_run' / 'orchestrator' / 'sikk_gmgn_live_run_summary_package_unpacked' / 'wallet_structure',
        'dst': LOGS_ROOT / 'orchestrator_wallet_structure_snapshot',
        'kind': 'copy',
    },
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def file_inventory(root: Path):
    files = []
    if not root.exists():
        return files
    for path in sorted(p for p in root.rglob('*') if p.is_file()):
        st = path.stat()
        files.append({
            'path': str(path.relative_to(ROOT)),
            'size_bytes': st.st_size,
            'sha256': sha256_file(path),
        })
    return files


def merge_tree(src: Path, dst: Path, dry_run: bool):
    moved = []
    conflicts = []
    if not src.exists():
        return moved, conflicts
    for path in sorted(p for p in src.rglob('*') if p.is_file()):
        rel = path.relative_to(src)
        target = dst / rel
        if target.exists():
            if sha256_file(path) == sha256_file(target):
                if not dry_run:
                    path.unlink()
                moved.append({'from': str(path.relative_to(ROOT)), 'to': str(target.relative_to(ROOT)), 'action': 'dedupe_remove_source'})
                continue
            conflicts.append({'from': str(path.relative_to(ROOT)), 'to': str(target.relative_to(ROOT)), 'reason': 'different_content'})
            continue
        moved.append({'from': str(path.relative_to(ROOT)), 'to': str(target.relative_to(ROOT)), 'action': 'move'})
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))
    if not dry_run:
        # remove empty directories bottom-up, but leave src parent tree if non-empty
        for d in sorted([p for p in src.rglob('*') if p.is_dir()], reverse=True):
            try:
                d.rmdir()
            except OSError:
                pass
        try:
            src.rmdir()
        except OSError:
            pass
    return moved, conflicts


def copy_tree(src: Path, dst: Path, dry_run: bool):
    copied = []
    conflicts = []
    if not src.exists():
        return copied, conflicts
    for path in sorted(p for p in src.rglob('*') if p.is_file()):
        rel = path.relative_to(src)
        target = dst / rel
        if target.exists() and sha256_file(path) != sha256_file(target):
            conflicts.append({'from': str(path.relative_to(ROOT)), 'to': str(target.relative_to(ROOT)), 'reason': 'different_content'})
            continue
        copied.append({'from': str(path.relative_to(ROOT)), 'to': str(target.relative_to(ROOT)), 'action': 'copy' if not target.exists() else 'already_same'})
        if not dry_run and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
    return copied, conflicts


def main():
    ap = argparse.ArgumentParser(description='Migrate legacy Intel Bot data into data/gmgn_candidates_live_run/intel-bot/.')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    LOGS_ROOT.mkdir(parents=True, exist_ok=True)
    CODE_ROOT.mkdir(parents=True, exist_ok=True)
    report = {
        'schema_version': '1.0.0',
        'dry_run': args.dry_run,
        'migration_time': datetime.now(timezone.utc).isoformat(),
        'intel_bot_root': str(INTEL_ROOT.relative_to(ROOT)),
        'items': [],
        'conflicts': [],
    }

    for item in MIGRATIONS:
        src, dst = item['src'], item['dst']
        before = file_inventory(src)
        if item['kind'] == 'copy':
            actions, conflicts = copy_tree(src, dst, args.dry_run)
        else:
            actions, conflicts = merge_tree(src, dst, args.dry_run)
        after_dst = file_inventory(dst)
        report['items'].append({
            'name': item['name'],
            'kind': item['kind'],
            'source': str(src.relative_to(ROOT)),
            'destination': str(dst.relative_to(ROOT)),
            'source_exists_before': src.exists() or bool(before),
            'files_before': len(before),
            'files_at_destination_after': len(after_dst),
            'actions': actions,
        })
        report['conflicts'].extend(conflicts)

    report_path = LOGS_ROOT / 'migration_manifest.json'
    if not args.dry_run:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({
        'dry_run': args.dry_run,
        'items': [{k: v for k, v in item.items() if k != 'actions'} | {'action_count': len(item['actions'])} for item in report['items']],
        'conflict_count': len(report['conflicts']),
        'manifest': str(report_path.relative_to(ROOT)),
    }, ensure_ascii=False, indent=2))
    if report['conflicts']:
        raise SystemExit(2)

if __name__ == '__main__':
    main()
