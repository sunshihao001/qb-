# Wallet Structure Main Directory Bottom Rule Verification

artifact_type: verification_artifact
verification_status: PASS
generated_at: 2026-05-08
scope: HER bottom control-plane update for wallet-structure main-directory cognition

## Verified bottom rule

SIKK 钱包结构分析专业化必须固定一个主目录和一个新主写数据路径：

```text
main_project: /root/sikk-gmgn/
new_primary_data_root: /root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

`/root/sikk-wallet-intel/` 仅作为 Wallet-Intel 协同 / 总控 / 行为推断工作区，不作为新钱包结构分析主事实目录、主采集目录或 Source Wallet Bot canonical 数据目录。

`data/gmgn_candidates_live_run/` 仅保留 legacy runtime / dashboard / paper 兼容，不作为新的 Source Wallet Bot 钱包结构主写路径。

## Allowed semantic layers under new_primary_data_root

```text
wallet_data/raw
wallet_data/normalized
wallet_data/summary
structure_analysis/wallet_fact
structure_analysis/intelligence
structure_analysis/handoff
structure_analysis/reports
manifest
```

## Forbidden content under new_primary_data_root

```text
trading_state_machine
paper_runner_output
dashboard_primary_output
private_key_or_signing_or_broadcast_or_swap
research_notes
task_tickets
wallet_intel_collaboration_logs
```

## Modified control-plane files

- `/root/sikk-gmgn/hermes_harness/01_control_plane/hermes_constitution.md`
- `/root/sikk-gmgn/hermes_harness/01_control_plane/task_routing_policy.md`
- `/root/sikk-gmgn/hermes_harness/01_control_plane/wallet_intel_task_routing_rule_v2.md`

## Verification flags

```text
bottom_rule_persisted: true
memory_updated: true
canonical_wallet_route_enforced: true
single_main_directory_enforced: true
new_primary_data_root_enforced: true
wallet_intel_workspace_demoted_from_primary_data_root: true
gmgn_candidates_live_run_demoted_to_legacy_runtime: true
legacy_full_auto_demoted_to_compat: true
```

## Anchor strings to verify

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
/root/sikk-wallet-intel/ 仅作为 Wallet-Intel 协同
new_primary_data_root
wallet_intel_collaboration_logs
data/gmgn_candidates_live_run/` 仅保留 legacy runtime
```
