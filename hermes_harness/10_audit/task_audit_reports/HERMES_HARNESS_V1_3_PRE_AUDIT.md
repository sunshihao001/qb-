# HERMES HARNESS V1.3 APUR PRE-AUDIT

- created_at: 2026-05-09T00:57:38Z
- scope: /root/sikk-gmgn/hermes_harness/
- task: Hermes Harness V1.3 Auto Problem Understanding & Resolution Loop 补齐落地
- boundary: 只修改 hermes_harness，不修改 SIKK 业务代码，不读取/输出密钥，不触发交易，不接入外部平台。

## 现状审计

- `12_problem_loop/`: 缺失，需新增运行产物目录。
- `13_problem_loop_templates/`: 缺失，需新增 APUR 外部化判断模板。
- `01_control_plane/auto_problem_solving_policy.md`: 缺失，需新增控制面规则。
- `09_scripts/`: 已存在，需补齐 APUR dry-run/生成脚本。
- `04_memory/memory_write_queue.jsonl`: 已存在，复盘写回应写入该队列而非直接写 verified memory。
- `10_audit/task_audit_reports/`: 已存在，可写入本预审计报告。
- `08_reports/final_reports/`: 已存在，可写入最终报告。
- `06_verification/verification_reports/`: 已存在，可写入最终验证报告。
- `07_recovery/recovery_reports/`: 已存在，可在失败时写入恢复报告。

## 差距判断

既有 V1.3 已具备 manifesto/control/workflow/schema/checklist/recovery 的概念层；本轮需要把 APUR Loop 从“认知设计”补齐为“可运行脚本 + 模板 + dry-run 样本 + 验证报告”的外部化判断产物链。
