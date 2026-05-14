#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEL_ROOT = ROOT / 'data' / 'gmgn_candidates_live_run' / 'intel-bot'
LOGS_ROOT = INTEL_ROOT / 'logs'
CODE_ROOT = INTEL_ROOT / 'code'
DEFAULT_WALLET_STRUCTURE_COMMIT = '4c05677'
LEGACY_PATHS = [
    (ROOT / 'data/gmgn_candidates_live_run/intel_bot', LOGS_ROOT / 'legacy_intel_bot'),
    (ROOT / 'data/gmgn_candidates_live_run/wallet_structure', LOGS_ROOT / 'wallet_structure'),
    (ROOT / 'data/wallet_intelligence', LOGS_ROOT / 'legacy_wallet_intelligence'),
]


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def inventory(path: Path):
    if not path.exists():
        return []
    return [{'path': str(p.relative_to(ROOT)), 'size_bytes': p.stat().st_size, 'sha256': sha256_file(p)} for p in sorted(path.rglob('*')) if p.is_file()]


def merge_move(src: Path, dst: Path, actions: list, dry_run: bool):
    if not src.exists():
        actions.append({'action':'source_missing','source':str(src.relative_to(ROOT))})
        return
    for p in sorted(src.rglob('*')):
        if not p.is_file():
            continue
        target=dst/p.relative_to(src)
        if target.exists() and sha256_file(target)==sha256_file(p):
            actions.append({'action':'dedupe_remove_source','from':str(p.relative_to(ROOT)),'to':str(target.relative_to(ROOT))})
            if not dry_run: p.unlink()
            continue
        if target.exists():
            target=target.with_name(target.name+'.migrated_duplicate')
        actions.append({'action':'move','from':str(p.relative_to(ROOT)),'to':str(target.relative_to(ROOT))})
        if not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(target))
    if not dry_run:
        shutil.rmtree(src, ignore_errors=True)


def restore_wallet_structure_from_commit(commit: str, dry_run: bool, actions: list):
    dst=LOGS_ROOT/'wallet_structure'
    if dst.exists() and any(dst.rglob('*')):
        actions.append({'action':'wallet_structure_destination_exists_skip_archive_restore','destination':str(dst.relative_to(ROOT)), 'files': len(inventory(dst))})
        return
    names=subprocess.run(['git','ls-tree','-r','--name-only',commit,'--','data/gmgn_candidates_live_run/wallet_structure'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.splitlines()
    if not names:
        actions.append({'action':'wallet_structure_no_commit_snapshot','commit':commit})
        return
    actions.append({'action':'restore_wallet_structure_archive','commit':commit,'files':len(names),'destination':str(dst.relative_to(ROOT))})
    if dry_run:
        return
    with tempfile.TemporaryDirectory(prefix='sikk_wallet_structure_restore_') as td:
        tar_path=Path(td)/'wallet_structure.tar'
        with tar_path.open('wb') as out:
            subprocess.run(['git','archive',commit,'data/gmgn_candidates_live_run/wallet_structure'],cwd=ROOT,stdout=out,check=True)
        with tarfile.open(tar_path) as tf:
            tf.extractall(td)
        src=Path(td)/'data/gmgn_candidates_live_run/wallet_structure'
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))


def ensure_readmes():
    INTEL_ROOT.mkdir(parents=True, exist_ok=True)
    CODE_ROOT.mkdir(parents=True, exist_ok=True)
    LOGS_ROOT.mkdir(parents=True, exist_ok=True)


def main():
    ap=argparse.ArgumentParser(description='Ensure all Intel Bot migrated data lives under intel-bot/code and intel-bot/logs.')
    ap.add_argument('--dry-run',action='store_true')
    ap.add_argument('--wallet-structure-commit',default=DEFAULT_WALLET_STRUCTURE_COMMIT)
    args=ap.parse_args()
    ensure_readmes()
    actions=[]
    for src,dst in LEGACY_PATHS:
        merge_move(src,dst,actions,args.dry_run)
    restore_wallet_structure_from_commit(args.wallet_structure_commit,args.dry_run,actions)
    report={
        'schema_version':'1.0.0',
        'dry_run':args.dry_run,
        'run_time_utc':datetime.now(timezone.utc).isoformat(),
        'intel_root':str(INTEL_ROOT.relative_to(ROOT)),
        'rule':'All Intel Bot migrated/runtime data must live under intel-bot/code or intel-bot/logs.',
        'actions':actions,
        'final_inventory':{
            'code_files':len(inventory(CODE_ROOT)),
            'logs_files':len(inventory(LOGS_ROOT)),
            'wallet_structure_files':len(inventory(LOGS_ROOT/'wallet_structure')),
        },
    }
    report_path=LOGS_ROOT/'intel_bot_data_consolidation_manifest.json'
    if not args.dry_run:
        report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'dry_run':args.dry_run,'report':str(report_path.relative_to(ROOT)),'final_inventory':report['final_inventory'],'actions':actions[:20],'action_count':len(actions)},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
