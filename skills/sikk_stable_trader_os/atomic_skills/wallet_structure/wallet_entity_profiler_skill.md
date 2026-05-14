# wallet_entity_profiler_skill

## 类型

Atomic Skill 规格文件。

## 职责边界

本能力只输出证据包，不直接决定最终跨阶段状态，不私自创建状态码，不绕过 Phase Controller。

## 标准输入

- 上游 candidate_state
- 阶段 controller 指定的标准化输入
- 统一 contracts / schemas / status_codes

## 标准输出

```json
{
  "skill_name": "wallet_entity_profiler_skill",
  "positive_evidence": [],
  "negative_evidence": [],
  "counter_evidence": [],
  "hard_negative_trigger": null,
  "missing_fields": [],
  "gaps": [],
  "source_refs": [],
  "audit_notes": []
}
```

## 验收标准

- 输出字段完整。
- 缺失写 missing_fields。
- 不确定写 gaps。
- 自动补全标记为 系统推导。
- 不输出最终 PAPER_READY / BLOCK 等跨阶段最终状态。
