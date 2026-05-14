# 17 System Integration & Cognition Update Protocol

- task_id: `task_0_full_system_runtime_bundle_setup`
- generated_at: `2026-05-10T07:00:00+00:00`
- status_scope: `FULL_SYSTEM_BUNDLE_READY_WITH_GAPS` candidate until validation
- control_mode: HER phase generator / contract checker / state-flow controller / audit executor
- boundary: this file is documentation-first, but it must be wired into the runtime control plane, audit flow, and durable cognition update path.

## Purpose

This protocol exists to prevent the bundle from becoming a static document set.
It defines how the P01-P09 bundle is consumed by the system, how verified rules are promoted into runtime governance, and how cognition is updated after validation.

## System integration requirements

The bundle is considered system-integrated only when all of the following exist:

- control-plane docs reference this bundle as an active route
- runtime state can point to the next allowed task
- gap register is readable by the progression gate
- audit reports are written back into the bundle ledger
- wave runners can consume the taskbooks without manual reconstruction
- verified rules are available to downstream governance or skill layers

## Cognition update requirements

Documentation alone is not enough.
The system must also update its durable cognition surface after validation:

- verified control rules may be promoted into reusable governance artifacts
- stable execution patterns may be promoted into skills or runtime helpers
- temporary gaps must remain in gap registers, not in durable memory
- unresolved issues must not be rewritten as facts
- READY_WITH_GAPS may update process memory, but not erase the gaps

## Integration gates

Before declaring the bundle ready, confirm:

- `manifest` exists and matches the runtime state
- `execution order` resolves to the correct wave chain
- `runtime state` has explicit `next_allowed_task`
- `stop condition` can reject unsafe progression
- `acceptance` can distinguish document-ready from live-ready
- `gap-aware progression` is linked into every downstream decision
- `audit` and `validation` reflect the same final status candidate

## Acceptance language

Use the following distinction:

- `document-ready`: the bundle is structurally complete and system-linkable
- `system-ready-with-gaps`: the bundle is integrated into routing and audit, but some waves are still intentionally deferred
- `system-rejected`: required control files, gates, or audit links are missing

## Update rule

If a verified rule is stable across runs, it should be written into the appropriate durable system layer.
If it is still conditional, it stays in the bundle docs and gap register only.

## Final note

This protocol is the bridge between:

- documents
- runtime
- audit
- durable cognition

Without this bridge, the bundle is only readable text.
With it, the bundle becomes an executable control surface.
