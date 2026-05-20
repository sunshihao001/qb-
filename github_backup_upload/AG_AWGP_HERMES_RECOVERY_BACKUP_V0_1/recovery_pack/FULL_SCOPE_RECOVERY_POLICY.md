# FULL_SCOPE_RECOVERY_POLICY.md

## Purpose
This policy upgrades the portable recovery pack from protocol-only recovery to full workflow recovery coverage.

The goal is to preserve everything required to restore AG-AWGP/Hermes/GBrain/OpenASE/SIKK workflow operation after machine migration, while still excluding secrets and live execution credentials.

## Backup tiers

### Tier A — GitHub source-of-truth
Store in private GitHub:
- source code
- docs and protocols
- AG-AWGP rehydration pack
- operating profiles
- workflow definitions
- templates
- restore/verify scripts
- lightweight manifests
- example configs only

### Tier B — Full non-secret recovery artifact snapshot
Store as tar.zst/tar.gz in private release/object storage/offsite backup:
- data/operating_backbone run records
- docs/protocols
- recovery packs
- configs/templates
- scripts
- tests
- non-secret indexes
- non-secret artifact registries
- selected non-secret data needed for workflow continuity

### Tier C — External secret restoration
Never store secrets in GitHub or recovery pack. Restore secrets through a secret manager or manual local `.env` creation from templates.

## Must include for full workflow recovery
- AG-AWGP doctrine and trigger prompt
- Document Intake Mode
- Hermes/GBrain/OpenASE/GPT operating profiles
- Workflow definitions
- Operational Brief / Intake Gate / Artifact Contract / Handoff templates
- Regression cases
- restore_snapshot.sh / verify_restore.sh
- full artifact manifest
- checksum file
- run_manifest/audit/final reports
- operating_backbone directory structure
- artifact indexes and latest pointers if non-secret
- non-secret config templates

## Must exclude
- .env real values
- API tokens
- private keys
- wallet secrets
- signing material
- live trading credentials
- cookies
- browser sessions
- SSH keys
- node_modules / venv / cache unless explicitly needed and non-secret

## Recovery acceptance
A recovery is only accepted if:
- verify_restore.sh passes
- full snapshot checksum passes
- AG-AWGP trigger prompt can rehydrate a new agent
- Hermes/GBrain/OpenASE boundaries are present
- operating_backbone run records are restored
- no secret-like files are present in GitHub or snapshot
