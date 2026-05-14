# AI Harness System V1.0

## 系统目标
建立一套用于调试、调度、约束、验证和复盘 AI 工作流的基础系统。该系统不是业务系统本身，而是管理 AI 如何理解目标、拆解任务、执行、验证、恢复、写入记忆和生成复盘的底层工作体系。

## 总架构

```text
AI 调节设计系统 V1.0 =
控制面
+ 目标护照
+ 方法轮
+ 上下文治理
+ 执行循环
+ 工具权限
+ 验证审计
+ 错误恢复
+ 记忆沉淀
+ 复盘报告
+ Hermes 调用规范
```

它的核心不是“让 AI 更像人”，而是：

```text
让 AI 像一个受约束的工程系统一样工作。
```

## 目录架构

```text
AI 调节设计系统 V1.0
├── 00_control_plane
├── 01_goals
├── 02_research_loop
├── 03_context_governance
├── 04_task_plans
├── 05_execution_runs
├── 06_verification
├── 07_recovery
├── 08_audit
├── 09_reports
├── 10_templates
└── 11_hermes_bot_invocation
```

## 目录说明
详见 `directory_map.md` 与 `directory_purpose_table.md`。

## 角色体系
- 总控协调者
- 研究分析者
- 工程执行者
- 独立验证者
- 审计复盘者

## 状态机
```text
RECEIVED → SCOUTING → PLANNING → READY_TO_EXECUTE → EXECUTING → VERIFYING
验证通过 → DONE → ARCHIVED
验证失败 → RECOVERING → PLANNING
高风险 → BLOCKED
```

## 工作流
1. 自然语言目标 → 专业任务
2. 文章 / 书籍 → 方法轮
3. 系统混乱 → 治理
4. Hermes 长任务

## 命令建议
- /目标登记
- /系统侦察
- /目录检查
- /上下文整理
- /任务拆解
- /方法轮执行
- /执行一轮
- /验证结果
- /错误恢复
- /写入记忆
- /生成复盘
- /审计系统

## 验证方式
- 文件存在验证
- 内容完整验证
- 目录用途验证
- 命令/流程验证
- 审计问题检查

## V1.0 验收标准

这个系统第一版完成后，必须能做到：

```text
1. 用户随便说一个复杂目标，AI 能先生成目标护照。
2. AI 不会直接开始乱做，而会先拆阶段。
3. 每个阶段有输入、输出、验证。
4. 方法轮有独立目录，不和代码混放。
5. 控制面有独立目录，不和任务报告混放。
6. 记忆有写入规则，不会乱写。
7. Hermes 跑长任务时，每一轮都能留下状态。
8. 失败时有 recovery，而不是直接停。
9. 任务完成时有 verification，而不是模型自称完成。
10. 后续可以把这套系统应用到 SIKK、Wallet-Intel、Telegram 面板、Hermes 多 Agent。
```

## 后续升级路线
- 增加机器可读 JSON schema。
- 增加命令路由器。
- 增加自动 verification runner。
- 增加 Telegram 命令映射。
- 增加多 Bot 角色拆分。
