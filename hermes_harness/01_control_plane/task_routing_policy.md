---
artifact_type: control_policy
status: verified
version: v2.0
valid_until: null
---
# Task Routing Policy

Complex tasks without a task passport cannot execute.

## Standard routes

- `document_research` → `method_wheel`
- `directory_governance` → `directory_scouting`
- `code_change` → `engineering_execution`
- `system_design` → `architecture_design`
- `debug_recovery` → `error_diagnosis`
- `long_task` → `segmented_loop`
- `memory_cleanup` → `memory_audit`

## Wallet-Intel route

When the task involves wallet data collection analysis, wallet structure analysis, Wallet-Intel, source wallet data, old directory import, semantic data integration, data passport, field dictionary, handoff packets, facts/evidence/inference/conclusion separation, token-level understanding, or import-after validation, route to:

```text
wallet_intel_semantic_integration
```

Authoritative detailed rule file:

```text
01_control_plane/wallet_intel_task_routing_rule_v2.md
```

Route test samples:

```text
06_verification/project_governance/wallet_intel_route_test_samples_v2.md
```

Route failure recovery:

```text
01_control_plane/wallet_intel_route_failure_recovery_rule_v2.md
```

This route must be used before ordinary directory governance because Wallet-Intel data integration is semantic data governance, not simple file organization.

Hard boundary: this route does not authorize scanning, copying, moving, deleting, or overwriting legacy data unless a separate task passport explicitly grants that scope.

## Mandatory execution order for Wallet-Intel / wallet-structure work

For any SIKK wallet structure, Wallet-Intel, source_wallet_bot, token data passport, field dictionary, old-path mapping, handoff, chip/cluster/same-source evidence, or wallet-analysis task, the execution order is mandatory:

```text
1. Read this routing policy and wallet_intel_task_routing_rule_v2.md
2. Set route_decision = wallet_intel_semantic_integration
3. Generate or update task_passport
4. Read 11_workflows/wallet_intel_semantic_integration.workflow.md
5. Confirm canonical_route before code/data changes
6. Execute only inside the existing canonical wallet structure system
7. Verify and write recovery note if route drift occurs
```

Canonical wallet structure route:

```text
modules/source_wallet_bot
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
→ sikk_candidate_state_machine.py / sikk_live_run.py
```

Canonical wallet structure main project directory:

```text
/root/sikk-gmgn/
```

Canonical new wallet data write root:

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

The canonical token directory may contain only wallet collection data, normalized wallet facts, structural evidence, structural inference, handoff packets, report copies, and manifest/passport artifacts. It must not contain trading state machine outputs, paper runner outputs, dashboard primary outputs, private-key/sign/broadcast/swap artifacts, research notes, task tickets, or Wallet-Intel collaboration logs.

`/root/sikk-wallet-intel/` is a Wallet-Intel collaboration / orchestration / behavior-inference workspace only. It must not be used as the new primary Source Wallet Bot fact store, raw collection root, or canonical wallet structure data directory.

Compatibility-only route:

```text
sikk_sol_full_auto_workflow.py = legacy_compat_one_shot
```

`legacy_compat_one_shot` may preserve old commands, old task packages, readiness checks, or sample/smoke runs, but it must not become the primary wallet-analysis entry or a second parallel wallet structure system.
