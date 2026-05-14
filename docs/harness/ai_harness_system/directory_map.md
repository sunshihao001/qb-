# Directory Map

AI Harness V1.0 canonical root：`docs/harness/ai_harness_system/`

| 逻辑区域 | 当前落点 | 说明 |
|---|---|---|
| control_plane | `00_control_plane/` | 系统宪法、角色边界、权限、验证、恢复、记忆规则 |
| goals | `01_goals/` | 原始目标、目标护照 |
| research_loop | `02_research_loop/` | 方法轮、研究资产、任务分解 |
| context_governance | `03_context_governance/` | 上下文分层、记忆沉淀、证据索引 |
| task_plans | `04_task_plans/` | 阶段计划、任务状态机、执行包 |
| execution_runs | `05_execution_runs/` | 执行循环、run log、command log、runtime state |
| verification | `06_verification/` | 验证清单、完成定义、验证报告 |
| recovery | `07_recovery/` | 错误分类、恢复报告、重试计划 |
| audit | `08_audit/` | 表层完成审计、系统缺口审计、完成审计 |
| reports | `09_reports/` | 任务报告、复盘报告、最终报告 |
| templates | `10_templates/` | 通用模板 |
| Hermes / Bot 调用 | `11_hermes_bot_invocation/` | 受控调用格式、中文命令体系、核心工作流 |

## 映射原则

- 已有类似目录不迁移、不删除。
- SIKK 业务目录继续保留业务用途。
- AI Harness V1.0 的底层认知规则统一写入 `docs/harness/ai_harness_system/`。
