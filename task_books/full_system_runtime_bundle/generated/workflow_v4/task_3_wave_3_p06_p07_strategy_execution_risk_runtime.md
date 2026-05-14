# Task 3：Wave 3｜P06-P07 策略与执行风控运行

- workflow_version: `full_system_workflow_v4`
- task_id: `task_3_wave_3_p06_p07_strategy_execution_risk_runtime`
- wave_id: `wave_03_p06_p07`
- mode: `plan-only`

## 目标
运行 P06-P07 策略门控与执行风控；只输出候选/风险/禁止项，不执行交易。

## 边界
P06/P07 只能给出 paper decision 与 risk gate；禁止 swap、sign、broadcast。
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
p06, p07

## handoff
- READY：进入 `task_4_wave_4_p08_p09_review_upgrade_runtime`
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
