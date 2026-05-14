# S00_unified_system_standardization Charter

- producer: S00_unified_system_standardization
- consumer: HER / SIKK Control Plane, K00/P00/R00/P01-P10, paper runtime, P09/P10 review-upgrade
- version: 0.1.0
- status: active_with_gaps
- acceptance: every judgment must trace goal → method → data → field lineage → schema/contract → runner → trace → acceptance → handoff → P08 → paper-only → P09/P10 → regression/rollback.

## Role
S00 is the unified standard control layer for HER / SIKK. It is not a document pile and not an extra trading phase.

## Hard boundaries
- No real swap.
- No private key read/write/storage.
- No signing or broadcast.
- Paper-only actions require P08 permission gate.
- P09/P10 review upgrades cannot mutate runtime rules directly.
- Legacy runtime is absorbed through maps/wrappers only; no isolated new runtime islands.
