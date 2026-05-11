---
artifact_type: task_passport
status: verified
version: v1.1
valid_until: null
---
# Current Task Passport

## task_id
hermes.task.20260506.140632.hermes_harness_v11

## original_goal
把 Hermes Harness V1.1 第一优先级稳定性基础整理成 canonical 内容。

## real_intent
让 Hermes 先不乱跑，再逐步专业化扩展。

## task_type
system_design

## task_mode
new/resume capable

## expected_outputs
- startup protocol
- task passport
- risk/permission policy
- active task state
- verification report
- recovery report template/report

## risk_boundary
- 不删除旧 V1.0 文件
- 不移动大目录
- 不执行外部发布/git push/交易/密钥读取
- 写入仅限 `/root/sikk-gmgn/hermes_harness/`

## verification_method
- 文件存在验证
- 内容字段验证
- runtime state 验证
- permission checker 验证
- surface completion audit

## next_route
priority_1_stabilization
