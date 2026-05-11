---
artifact_type: legacy_path_mapping_template
status: verified
version: v2.0-stage7
generated_at: 2026-05-07T08:15:59Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 旧新路径映射模板 V2.0 — 阶段 7

## 1. CSV 模板

| mapping_id | token_address | token_symbol | semantic_layer | old_path | new_path | source_type | copy_mode | checksum_old | checksum_new | mapped_at | mapped_by | compatibility_status | fallback_allowed | migration_status | missing_reason | notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| map_001 | <token> | <symbol> | facts/evidence/inference/handoff/reports/index | /old/path/file | /new/path/file | csv/json/md/raw/report | copy_only/reference_only | sha256 | sha256 | timestamp | hermes | ok/compatibility_required/trace_missing | true/false | copied/reference_only/skipped | <if skipped> | <notes> |

## 2. JSON 模板

```json
{
  "mapping_id": "map_001",
  "token_address": "",
  "token_symbol": "",
  "semantic_layer": "facts | evidence | inference | handoff | reports | index | unknown",
  "old_path": "",
  "new_path": "",
  "source_type": "csv | json | md | raw | report | unknown",
  "copy_mode": "copy_only | reference_only | no_copy",
  "checksum_old": "",
  "checksum_new": "",
  "compatibility_status": "ok | compatibility_required | trace_missing | deprecated_reference",
  "fallback_allowed": false,
  "migration_status": "copied | reference_only | skipped | pending",
  "missing_reason": "",
  "notes": ""
}
```

## 3. 必填规则

```text
old_path 必填。
new_path 在 copy_only 导入时必填。
semantic_layer 必填。
compatibility_status 必填。
fallback_allowed 必填。
copy_mode 必填。
checksum_old / checksum_new 在发生复制时必填。
```

## 4. 禁止

```text
不得只记录 new_path 不记录 old_path。
不得以“目录已整理”代替映射明细。
不得覆盖旧映射历史。
```
