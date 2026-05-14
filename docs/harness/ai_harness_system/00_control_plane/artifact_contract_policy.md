# Artifact Contract Policy

## 用途
定义所有关键产物的统一输出契约，确保每个文件都能回答来源、阶段、验证和有效期。

## 适用范围
适用于所有关键输出：控制面文件、目标护照、方法轮产物、执行计划、验证报告、恢复报告、审计报告、复盘报告、记忆沉淀报告及其可复用资产。

## 产物必须回答的问题
- 这个文件是谁生成的？
- 来自哪个任务？
- 对应哪个阶段？
- 输入来源是什么？
- 是否已验证？
- 能不能被后续任务调用？
- 过期条件是什么？

## 标准 frontmatter
所有关键输出应优先附带 YAML frontmatter：

```yaml
task_id: hermes.task.20260506.0001
phase_id: phase_02_control_plane
artifact_type: control_policy
status: verified
created_at: 2026-05-06T00:00:00Z
source_inputs:
  - user_goal
  - HERMES_STARTUP_CONTEXT.md
verification_report: HERMES_HARNESS_V1_VERIFICATION.md
valid_until: null
```

## 规则
1. 关键产物默认带 header。
2. verified 之前不能当长期引用源。
3. 过期产物必须标明 valid_until 或失效条件。
4. 后续任务调用前必须再次检查状态是否仍有效。
5. 无来源、无阶段、无验证的产物不能进入 canonical 目录。

## 禁止行为
- 把草稿当 verified。
- 把无 header 的临时文件当长期资产。
- 把旧产物不加状态直接复用。
- 把验证报告缺失的文件当最终产物。

## 检查标准
- 是否有 task_id。
- 是否有 phase_id。
- 是否标明 artifact_type。
- 是否标明 status 和 verification_report。
- 是否能追踪 source_inputs。
- 是否说明 valid_until 或失效条件。
