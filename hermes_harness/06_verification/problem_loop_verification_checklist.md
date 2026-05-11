# Problem Loop Verification Checklist

- artifact_type: verification_checklist
- version: v1.3-apur

## 验证内容

1. 是否生成 problem_passport。
2. 是否生成 understanding_report。
3. 是否生成 evidence_plan。
4. 是否生成 hypothesis_set。
5. 是否生成 root_cause_report。
6. 是否生成 solution_design。
7. 是否生成 resolution_verification。
8. 失败时是否生成 failure_attribution。
9. 解决后是否生成 learning_writeback。
10. 是否把经验写入 memory_write_queue，而不是直接写 verified_memory。
11. 是否有 loop_state。
12. 是否有下一轮入口。
13. 是否所有脚本支持 `--help`。
14. 是否所有脚本支持 `--dry-run`。
15. 是否默认只写 hermes_harness/。
16. 是否没有删除文件、没有修改业务代码、没有读取密钥、没有触发交易。

## 裁决

- PASSED：全部关键产物存在，dry-run 可执行，验证报告通过，经验写入 queue。
- PARTIAL：产物不完整或未接入主路由，但不影响已有系统安全。
- FAILED：dry-run 失败、关键产物缺失、直接写长期记忆、或违反安全边界。
