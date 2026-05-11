#!/usr/bin/env bash
set -euo pipefail
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
QUAR="/root/sikk-gmgn/_cleanup_quarantine_${STAMP}"
mkdir -p "$QUAR"
# This script does NOT rm -rf. It only moves cache/known disposable paths into quarantine.
while IFS= read -r p; do
  [ -z "$p" ] && continue
  if [ -e "$p" ]; then
    dest="$QUAR${p#/root/sikk-gmgn}"
    mkdir -p "$(dirname "$dest")"
    mv "$p" "$dest"
    echo "MOVED_TO_QUARANTINE $p -> $dest"
  fi
done < /root/sikk-gmgn/research_loop/plans/data_cleanup_20260511/safe_delete_after_backup_paths.txt
echo "QUARANTINE=$QUAR"
