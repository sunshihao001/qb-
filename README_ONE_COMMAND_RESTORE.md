# SIKK One-Command Restore

This repository is the GitHub source-of-truth recovery layer for SIKK backup packs.

## One command

On a new machine / new terminal:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/sunshihao001/qb-/main/restore_latest_sikk.sh)"
```

Default restore target:

```text
$PWD/sikk-quant-runner-restored
```

Custom restore target:

```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/sunshihao001/qb-/main/restore_latest_sikk.sh)" -- /absolute/path/to/sikk-quant-runner-restored
```

## What this does

1. Clones `https://github.com/sunshihao001/qb-.git` to a temporary work directory.
2. Reads `LATEST_SIKK_BACKUP.txt` if present; otherwise selects the newest `SIKK_GITHUB_RECOVERY_BACKUP_V0_1_*` directory.
3. Runs the backup pack secret scan.
4. Restores `recovery_pack` into the target directory.
5. Runs `verify_restore.sh` from the restored pack.
6. Writes `SIKK_RESTORE_SOURCE.json` in the restored target.

## Boundaries

This restore path is GitHub-source-of-truth only.

It does **not** restore secrets and must never contain:

- `.env` real values
- API tokens
- private keys / SSH keys
- wallet secrets
- signing material
- live trading credentials
- cookies / browser sessions

External secrets must be restored separately by the operator after the non-secret restore passes.

## Current backup pointer

See:

```text
LATEST_SIKK_BACKUP.txt
```

