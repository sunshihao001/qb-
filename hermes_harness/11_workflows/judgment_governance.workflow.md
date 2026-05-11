# Judgment Governance Workflow

Route: `hermes_judgment_governance_layer`

```text
problem intake
→ problem triage
→ evidence sufficiency matrix
→ abstention decision
→ causal graph
→ solution cost review
→ operator decision gate
→ APUR/runtime continuation decision
→ meta verification
→ anti self-deception audit
→ memory lifecycle review
→ judgment error tracking
→ governance report
```

## Runtime insertion

This workflow is invoked by V1.4 runtime hook as `judgment_governance_hook` before APUR execution is treated as allowed.

## Outputs

- `judgment_governance_state.json`
- `problem_triage.json`
- `evidence_sufficiency_matrix.json`
- `abstention_decision.md`
- `solution_cost_review.json`
- `meta_verification_report.md`
- `anti_self_deception_audit.md`
- `causal_graph.json`
- `memory_lifecycle_review.json`
- `operator_decision_gate.md`
- `judgment_governance_report.md`
