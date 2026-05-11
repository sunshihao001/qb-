---
artifact_type: control_policy
status: verified
version: v1.2
valid_until: null
---
# Prompt Layer Policy

## Purpose
Define prompt layering so Hermes can combine baseline governance, project constraints, task-specific rules, user overrides, and append-only post-execution requirements without losing safety or control.

## Prompt Layers
- **L0 Default Constitution**: always active; defines non-negotiable safety, verification, and recovery rules.
- **L1 Project Rules**: current repository root, directory boundaries, legacy mapping, and forbidden zones.
- **L2 Task Rules**: current task passport, phase plan, checkpoint, and runtime state.
- **L3 Temporary User Rules**: this turn's additional user instructions and preferences.
- **L4 Append Rules**: validation, recovery, and retroactive instructions generated after execution.

## Precedence
1. L0 is immutable.
2. L1 may narrow the working scope but cannot weaken L0.
3. L2 may refine execution for the current task but cannot override L0 or L1 safety boundaries.
4. L3 may add temporary preferences but cannot override safety, security, or directory boundaries.
5. L4 is append-only; it may add requirements, but may not replace lower layers.

## Hard Rules
- Task rules cannot override the default constitution.
- Temporary user rules cannot override safety boundaries.
- Append rules can only supplement; they cannot replace the baseline.
- If a lower layer conflicts with a higher layer, the higher layer wins and the conflict must be reported.

## Required Use
Every task intake should explicitly record which rules were inherited from each layer.
Every execution round should reference the active prompt layers before tool use.
Every final report should explain any layer conflicts and the resolution applied.
