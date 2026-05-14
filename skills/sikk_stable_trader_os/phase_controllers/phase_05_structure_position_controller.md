# 第 5 阶段：结构位置确认层 Phase Controller

## 阶段定位

本文件是 Phase Controller，不是孤立 Skill。它规定本阶段边界、输入、Atomic Skill 调用、输出、状态码、handoff 与审计。

## 核心输出

```text
structure_position_decision.json
```

## 状态码范围

```text
COMPLETION_PASS / COMPLETION_WAIT / COMPLETION_FAIL / FATIGUE_BLOCK
```

## Atomic Skill 调用清单

- `poc_context_skill`
- `avwap_completion_gate_skill`
- `failure_test_skill`
- `fatigue_filter_skill`


## 固定执行顺序

```text
读取输入
  ↓
校验字段
  ↓
识别缺口
  ↓
调用 Atomic Skill
  ↓
汇总 positive_evidence / negative_evidence / counter_evidence
  ↓
检查 hard_negative_trigger
  ↓
生成 status_code
  ↓
写 `structure_position_decision.json`
  ↓
写 handoff packet
  ↓
写 audit report
```

## Controller 判决边界

- Atomic Skill 只输出证据包。
- 本 Controller 汇总证据后生成本阶段状态码。
- 跨阶段状态由总控 Skill 和 candidate_state_contract 管理。
- 任一硬否决触发时，不允许升级到下一阶段强通过状态。

## 验收标准

- 输入通过 contract validator。
- 输出符合 candidate_state_contract。
- 必须包含正证、反证、硬否决、missing_fields、gaps。
- 必须写 handoff 和 audit。
