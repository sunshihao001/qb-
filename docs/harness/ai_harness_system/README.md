# AI Harness System 目录总说明

这是通用 AI 调节系统的目录与调解规则根目录。

## 1. 定位

- 这是 HER / Hermes 的底层思考、判断、调度、验证、恢复、复盘系统。
- 这里放的是系统规则、任务结构、认知边界和运行治理，不是 SIKK 业务代码本身。
- 这套目录的目标，是让 Hermes 知道每类东西应该去哪，不再把代码、方法、运行数据、复盘报告混在一起。

## 2. 总体分层原则

必须保持以下逻辑分层：

- 控制面单独放
- 方法轮单独放
- 上下文治理单独放
- 任务计划单独放
- 执行日志单独放
- 验证单独放
- 恢复单独放
- 审计单独放
- 报告单独放
- 模板单独放

## 3. 目录结构总览

```text
ai_harness_system/
├── 00_control_plane/      # 系统宪法、角色边界、权限、验证、恢复
├── 01_goals/              # 原始目标、goal passport
├── 02_research_loop/      # 方法轮、研究资产、gap 与 synthesis
├── 03_context_governance/  # 记忆层、证据索引、过期记忆审查
├── 04_task_plans/         # 阶段计划、执行包、交接合同
├── 05_execution_runs/     # run logs、command logs、outputs、state
├── 06_verification/       # 检查清单、验证报告、失败验证
├── 07_recovery/           # 错误日志、恢复报告、重试计划
├── 08_audit/              # 表层审计、系统缺口审计、完成审计
├── 09_reports/            # 日报、任务报告、最终报告
├── 10_templates/          # task、method wheel、verification、recovery 模板
└── 11_hermes_bot_invocation/ # Hermes / Bot 受控调用入口与中文命令体系
```

## 4. 各层职责

### 00_control_plane
系统最高规则层。

职责：
- 定义系统宪法
- 定义角色边界
- 定义权限规则
- 定义验证标准
- 定义错误恢复
- 定义记忆写入边界
- 定义禁止行为

### 01_goals
任务入口层。

职责：
- 接收用户原始目标
- 生成 goal passport
- 防止目标在执行中漂移

### 02_research_loop
方法论资产层。

职责：
- 记录 intake
- 记录 passports
- 记录 theme maps
- 记录 method lenses
- 记录 gap detection
- 记录 synthesis

### 03_context_governance
上下文治理层。

职责：
- 管理 system memory
- 管理 project memory
- 管理 session memory
- 管理 evidence index
- 审查 stale memory

### 04_task_plans
任务计划层。

职责：
- 生成 phase plans
- 生成 execution packets
- 生成 handoff contracts

### 05_execution_runs
执行运行层。

职责：
- 记录 run logs
- 记录 command logs
- 记录 outputs
- 记录 runtime state

### 06_verification
验证层。

职责：
- 写 checklists
- 写 verification reports
- 写 failed verification 记录

### 07_recovery
恢复层。

职责：
- 记录 error logs
- 记录 recovery reports
- 记录 retry plans

### 08_audit
审计层。

职责：
- 审查表面工作
- 审查系统缺口
- 审查完成质量

### 09_reports
报告层。

职责：
- 输出 daily reports
- 输出 task reports
- 输出 final reports

### 10_templates
模板层。

职责：
- 提供固定骨架
- 但模板不是运行结果

### 11_hermes_bot_invocation
Hermes / Bot 调用层。

职责：
- 定义 Hermes 调用总格式
- 定义 Telegram / Hermes 中文命令体系
- 让 Bot 通过受控工作流接收任务
- 防止直接对 AI 说“帮我做一个系统”后进入无控制执行

## 5. 核心认知

这套目录体系的核心不是“名字必须一模一样”，而是“功能必须分离”。

Hermes 需要明确：
- 哪些是控制面
- 哪些是目标
- 哪些是方法
- 哪些是上下文
- 哪些是执行过程
- 哪些是验证
- 哪些是恢复
- 哪些是审计
- 哪些是报告
- 哪些是模板

## 6. 系统宪法优先级

该系统的认知优先级高于旧的临时上下文、旧习惯和旧默认 prompt 模式。

当临时聊天内容、旧任务习惯、旧目录习惯与系统宪法冲突时，以本目录体系和控制面规则为准。

## 7. 入口

- 先读 `00_control_plane/system_constitution.md`
- 再读对应层目录下的 README 或规则文件
- 再决定读取、写入、验证与回流动作
