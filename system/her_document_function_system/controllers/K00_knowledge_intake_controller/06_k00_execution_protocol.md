# K00 Execution Protocol

1. Preserve raw material or source ref before interpretation.
2. Create registry/passport/index/mapping/gap refs.
3. Bind execution boundary, write policy, repo root.
4. Produce K00 handoff packet.
5. Validate handoff against `09_k00_handoff_packet.schema.json`.
6. Only then allow F00 preflight.

## F00 gating

F00 may start only when:

- `k00_handoff_packet` exists.
- passport/index/mapping/gap refs are non-empty or explicitly gap-coded.
- repo_root/write_policy/execution_boundary are present.

Otherwise F00 must return `F00_BLOCKED` or `DESIGN_ONLY` according to F00 input contract.
