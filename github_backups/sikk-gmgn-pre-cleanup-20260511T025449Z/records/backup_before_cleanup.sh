#!/usr/bin/env bash
set -euo pipefail
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_ROOT="/root/sikk-backups/sikk-gmgn-pre-clean-${STAMP}"
mkdir -p "$BACKUP_ROOT"
cd /
# 1) manifest and path list
cp -a /root/sikk-gmgn/research_loop/plans/data_cleanup_20260511 "$BACKUP_ROOT/cleanup_plan"
# 2) archive useful data/code/system assets. This is backup only, no deletion.
tar --warning=no-file-changed --ignore-failed-read -czf "$BACKUP_ROOT/sikk-gmgn-useful-assets.tar.gz" -T /root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/backup_include_paths.txt
# 3) checksum
sha256sum "$BACKUP_ROOT/sikk-gmgn-useful-assets.tar.gz" > "$BACKUP_ROOT/SHA256SUMS.txt"
# 4) quick inventory
du -h "$BACKUP_ROOT"/* > "$BACKUP_ROOT/backup_size.txt"
echo "BACKUP_DONE=$BACKUP_ROOT"
cat "$BACKUP_ROOT/SHA256SUMS.txt"
