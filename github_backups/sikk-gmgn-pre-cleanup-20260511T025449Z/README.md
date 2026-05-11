# SIKK-GMGN Pre-cleanup GitHub Backup

- Backup stamp: 20260511T025449Z
- Root: /root/sikk-gmgn
- Purpose: preserve the pre-cleanup plan records and selected useful assets before shrinking the workspace.

## Contents

- `records/` — copied planning and audit documents for the cleanup task
- `archives/` — split archive parts of selected useful assets, plus SHA256 checksums
- `BACKUP_INCLUDE_RELATIVE_PATHS.txt` — repository-relative file list used to build the archive

## Restore hint

If you need to restore, clone the repo and reassemble the archive parts:

```bash
cat archives/sikk-gmgn-useful-assets-20260511T025449Z.tar.gz.part-* > sikk-gmgn-useful-assets.tar.gz
sha256sum -c archives/SHA256SUMS_FULL_ARCHIVE.txt
```

Then extract the tarball into the repo root.
