# Handoff Protocol

每个 handoff packet 至少包含：

```json
{
  "phase": "",
  "token_address": "",
  "snapshot_id": "",
  "status": "",
  "handoff_files": {},
  "allowed_next_stage": "",
  "hard_negatives": [],
  "missing": [],
  "audit_refs": []
}
```

自然语言报告不能替代 handoff packet。
