---
artifact_type: conflict_handling_template
status: verified
version: v2.0-stage9
generated_at: 2026-05-07T09:01:56Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel Conflict Handling Template V2.0 — 阶段 9

## 1. 冲突类型模板

```text
conflict_id:
conflict_type: token_source_conflict | new_path_name_conflict | field_undocumented | unknown_file | unresolved_token
conflict_subject:
conflict_sources:
conflict_paths:
conflict_refs:
current_state_markers:
resolution_status: open | under_review | resolved | blocked
required_next_action:
required_validation:
owner_module:
notes:
```

## 2. 填写规则

```text
- conflict_sources 必须保留全部来源。
- conflict_paths 必须列出每条冲突路径。
- current_state_markers 必须记录 not_found / unknown / unresolved_token_candidates / source_conflict / conflict_candidates / undocumented_field / compatibility_required。
- resolution_status 为 open 或 under_review 时，不得进入完成声明。
- required_next_action 必须是恢复或验证动作，不得是删除动作。
```

## 3. 冲突处理输出

```text
- conflict ledger entry
- traceable candidate record
- recovery or verification ticket
- no overwrite confirmation
```
