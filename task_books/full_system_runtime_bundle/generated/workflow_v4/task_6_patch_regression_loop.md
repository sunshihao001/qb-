# Task 6：Patch + Regression 修复回归循环

- workflow_version: `full_system_workflow_v4`
- task_id: `task_6_patch_regression_loop`
- wave_id: `patch_and_regression`
- mode: `plan-only`

## 目标
专门修复失败项、阻断项与降级项，并回归到失败 wave 或 E2E。

## 边界
只修复已登记 issue；禁止绕过验收、删除旧数据或跳过审计。
真实交易：禁止。签名：禁止。广播：禁止。密钥读取：禁止。

## 输入
- full_system_runtime_bundle 总控文件
- 对应 P01-P09 stage_data / code_landing / acceptance_check 任务书
- runtime_task_state.json / wave_state.json / checkpoint_state.json
- missing_gap_register 与 workflow_v4_gap_register

## 输出
- 阶段任务书
- 代码骨架任务书
- 验收任务书
- pytest/replay/handoff/audit 结果引用
- runtime state 与 gap register 回填

## phases
not_applicable

## handoff
- READY：进入 `route_back_to_failed_wave_or_e2e`
- READY_WITH_GAPS：允许继续但必须继承 gap register
- REJECTED：停止当前 Wave，进入 `task_6_patch_regression_loop`

## 状态码
- READY
- READY_WITH_GAPS
- REJECTED

## missing
缺失字段、缺失文件、缺失证据必须写为 `missing`，不得写空值或系统猜测值。

## 阻断
- required control file missing
- JSON/state 不可解析
- 出现真实交易、签名、广播或密钥读取动作
- 删除/移动旧数据

## 降级
- mock replay / paper-only evidence
- phase taskbook 缺项
- profile/gateway/live collector 未接入

## 验收
- 任务书生成完整
- 状态码可路由
- pytest/replay/handoff/audit 引用存在或明确写 missing
- gap register 已回填
- paper-only 安全边界未破坏

## 审计
审计写入 `reports/system_audit/full_system_workflow_v4_audit.md` 与 JSON 结果。

## 当前 gap register
- none
