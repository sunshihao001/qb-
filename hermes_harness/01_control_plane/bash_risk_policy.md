---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Bash Risk Policy

## Purpose
Bash is a risk amplifier. It is not an ordinary tool. Bash can touch files, processes, network, Git, configuration, redirection, secrets, and runtime state.

Hermes must classify Bash commands before execution.

## Bash Risk Classes
- **B0 Read-only query**: `pwd`, `ls`, `cat`, `grep`, `find`, `wc`, `sha256sum`, read-only inspection.
- **B1 Low-risk creation**: `mkdir`, `touch` for new files/directories within allowed scope.
- **B2 Document write**: writing markdown/json/report files inside the task scope.
- **B3 Script execution**: `python`, `bash`, `node`, package scripts, tests, validators.
- **B4 System/project modification**: `mv`, `cp`, `sed -i`, config edits, service restart, broad overwrite.
- **B5 Destructive high-risk**: `rm`, `git reset`, `git clean`, `docker prune`, destructive migrations.
- **B6 External/secrets**: external `curl`/network actions, `env`, reading key/token/private-key material, broadcast/trade/signing.

## Default Permissions
- **B0/B1**: auto-allow inside project boundary.
- **B2**: allowed only inside task scope and must be logged.
- **B3**: allowed only when stdout/stderr are recorded or summarized.
- **B4**: ask before execution.
- **B5/B6**: deny by default.

## Required Logging
Every Bash command must record:
- command
- cwd
- bash_risk_class
- permission
- stdout/stderr policy
- expected effect
- actual result
- exit code

## Hard Rules
- Do not classify Bash as a generic tool call.
- Do not run B4 without explicit approval.
- Do not run B5/B6 unless a higher-level policy explicitly permits and the user confirms.
- Do not print secrets even during classification.
- If a command contains redirection, pipe, env access, network access, Git mutation, Docker prune, or deletion, classify upward.
