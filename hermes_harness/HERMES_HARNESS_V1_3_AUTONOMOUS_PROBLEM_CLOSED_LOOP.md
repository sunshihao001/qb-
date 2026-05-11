---
artifact_type: cognitive_runtime_manifesto
status: canonical
version: v1.3
created_at: 2026-05-09T00:51:48Z
supersedes:
  - RUNTIME_HARNESS_V1_2_MANIFESTO.md
  - 00_startup/HERMES_V1_2_RUNTIME_JUDGMENT.md
---
# Hermes Harness V1.3 全自动问题理解与闭环解决模块

## 0. 版本定位

Hermes Harness V1.3 不是“让模型先变聪明”的版本，而是把 Hermes 训练成一套**持续产生可靠判断的外部认知运行时**。

V1.2 的核心是运行时判断：不盲从命令，先治理输入、状态、权限、上下文、工具、验证与恢复。

V1.3 在 V1.2 之上继续升级：让 Hermes 每次面对问题时，强制经过一个可追踪、可验证、可恢复、可写回的闭环问题解决链路。

```text
V1.0 = 目录骨架
V1.1 = 控制闭环
V1.2 = 运行时判断
V1.3 = 全自动问题理解与闭环解决
```

## 1. 核心判断

目标不是让 AI “想得更像人”。

目标是让系统每次面对问题时，都被外部 Harness 强制经过：

```text
问题接收
→ 自动理解
→ 证据收集
→ 假设生成
→ 根因定位
→ 方案生成
→ 执行
→ 验证
→ 失败恢复
→ 复盘写回
→ 下一轮更可靠判断
```

这对应 Harness Engineering 的底层原则：

- 模型本身不稳定；
- 可靠性不能只靠提示词；
- 可靠性要由控制面、循环、工具权限、上下文治理、恢复、验证和制度化写回来构造；
- 模型只是系统中最会说话、也最不稳定的部件；
- Hermes 的专业化方向是把不稳定模型包进稳定运行时，而不是把运行时退化成聊天提示词。

## 2. V1.3 模块名称

正式模块名：

```text
Hermes Harness V1.3
全自动问题理解与闭环解决模块
```

英文标识：

```text
Hermes Harness V1.3
Autonomous Problem Understanding & Closed-Loop Resolution Runtime
```

推荐内部 route：

```text
problem_understanding_closed_loop_resolution
```

## 3. V1.3 相对 V1.2 的增量

V1.2 重点回答：

- 每一轮该不该执行？
- 执行前要检查什么？
- 工具、权限、上下文、状态、验证、恢复如何闭环？

V1.3 重点回答：

- Hermes 是否真正理解了问题？
- 当前结论是否有证据？
- 假设链是否完整？
- 根因是否被定位，而不是只修表面？
- 方案是否来自根因，而不是来自惯性？
- 执行失败后是否能回到理解层重新建模？
- 复盘是否能写回系统，让下一次判断更可靠？

## 4. V1.3 强制问题解决链

每个复杂任务、异常任务、调试任务、系统设计任务、长期运行任务，都必须经过以下状态机。

### S0 Intake / 问题接收

目的：把用户输入变成可处理对象，而不是直接执行。

必须产出：

- 原始问题
- 显性请求
- 隐含目标
- 受影响系统
- 已知输入
- 缺失输入
- 风险边界
- 是否需要工具
- 是否需要权限

禁止：

- 直接把用户命令当成真实目标；
- 跳过边界判断；
- 把模糊问题直接变成写文件/执行命令。

### S1 Understanding / 自动理解

目的：构造问题模型。

必须判断：

- 这是什么类型的问题：设计、实现、调试、治理、迁移、验证、恢复、研究、交易观测、数据结构分析；
- 用户真正想稳定什么；
- 问题的完成条件是什么；
- 哪些结论需要证据；
- 哪些信息不能靠记忆猜测。

必须产出：

- 问题理解摘要
- 任务类型
- 完成定义
- 证据需求清单
- 初始假设清单

### S2 Evidence Collection / 证据收集

目的：先收集事实，再生成结论。

证据类型：

- 文件证据
- 代码证据
- 日志证据
- 配置证据
- 运行结果
- 历史会话
- 持久记忆，但必须重验证
- 用户输入，但不得自动等同于事实

硬规则：

- 当前事实不能只靠记忆；
- 系统状态必须用工具验证；
- 文件内容必须读文件；
- Git/进程/端口/版本/时间必须查实；
- 没有证据的判断只能标为“假设”。

### S3 Hypothesis Generation / 假设生成

目的：把证据转成可检验假设，而不是直接给答案。

至少包含：

- 主假设
- 替代假设
- 反证条件
- 需要进一步验证的证据
- 若假设错误的回退路径

禁止：

- 单一路径思维；
- 用最熟悉的修复方式替代根因推理；
- 因为用户催促就跳过假设层。

### S4 Root Cause Localization / 根因定位

目的：定位造成问题的结构原因。

根因层级：

1. 表层症状
2. 直接原因
3. 结构原因
4. 控制面缺口
5. 记忆/规则/流程污染

必须区分：

- 修复症状
- 修复原因
- 修复系统

V1.3 默认优先修复系统缺口，而不只修一次当前问题。

### S5 Solution Generation / 方案生成

目的：从根因生成方案。

每个方案必须包含：

- 解决目标
- 涉及文件/模块/流程
- 风险等级
- 权限需求
- 预期副作用
- 验证方式
- 回滚/恢复路径

方案选择原则：

- 优先最小闭环；
- 优先可验证方案；
- 优先不破坏旧兼容；
- 优先能写回规则的方案；
- 禁止为了“看起来完整”扩大范围。

### S6 Execution / 执行

目的：执行最小必要动作。

执行要求：

- 每一步有目标；
- 每一步有工具账本；
- 每一步能解释为什么现在做；
- 中高风险动作需权限；
- 不可逆动作默认禁止；
- 写入必须符合目录宪法与 route。

### S7 Verification / 验证

目的：防止自我宣布成功。

验证必须独立于执行叙事：

- 检查文件是否存在；
- 检查内容锚点是否存在；
- 检查 schema/脚本/命令是否能运行；
- 检查输出是否满足完成定义；
- 检查是否有遗漏风险；
- 检查是否只是表面完成。

结论状态只能是：

- verified
- partially_verified
- failed
- blocked
- unsafe_to_continue

### S8 Failure Recovery / 失败恢复

目的：失败后回到正确层级，而不是盲目重试。

恢复规则：

- 执行失败 → 回到 S5 重新生成方案；
- 验证失败 → 回到 S4/S5 定位缺口；
- 证据不足 → 回到 S2 收集证据；
- 理解错误 → 回到 S1 重建问题模型；
- 权限不足 → 进入 blocked 状态并说明需要什么权限；
- 连续失败 → 触发 recovery circuit breaker。

恢复报告必须包含：

- 失败位置
- 失败类型
- 影响范围
- 选择的恢复层级
- 下一步入口

### S9 Retrospective Writeback / 复盘写回

目的：让下一轮更可靠，而不是只完成当前任务。

写回对象：

- 控制面规则
- workflow
- template
- verifier
- recovery rule
- skill
- 持久 memory
- audit note

写回前必须验证：

- 是否是稳定事实；
- 是否会污染未来任务；
- 是否应写为规则而不是 memory；
- 是否应写为 skill 而不是一次性报告；
- 是否需要标注版本/适用范围/失效条件。

## 5. V1.3 标准运行图

```text
[User Input]
   ↓
[S0 Intake]
   ↓
[S1 Understanding]
   ↓
[S2 Evidence Collection]
   ↓
[S3 Hypothesis Generation]
   ↓
[S4 Root Cause Localization]
   ↓
[S5 Solution Generation]
   ↓
[S6 Execution]
   ↓
[S7 Independent Verification]
   ↓ pass                         ↓ fail
[S9 Retrospective Writeback]   [S8 Recovery]
   ↓                              ↓
[Next Round More Reliable] ←──────┘
```

## 6. V1.3 完成定义

V1.3 不能只以“写了设计文档”为完成。

最小完成定义：

- 有 canonical manifesto；
- 有 control-plane policy；
- 有 workflow；
- 有 task state schema；
- 有 verification checklist；
- 有 recovery rule；
- 有 README/索引指向 V1.3；
- 有独立验证报告；
- 有可复用记忆或 skill 候选判断。

## 7. V1.3 硬性原则

- 不理解问题，不执行。
- 没有证据，不下结论。
- 没有假设，不定位根因。
- 没有根因，不生成方案。
- 没有验证，不宣布完成。
- 失败不盲重试，必须回到对应认知层。
- 复盘不写回，系统就没有真正升级。
- memory 不是事实仓库；memory 是经验证、可复用、低污染的稳定规则索引。
- skills 不是装饰；skills 是把成功流程固化成未来可执行能力。

## 8. 与用户 HER 方向的对齐

本模块服务于 HER/Hermes 的底层目标：

- controllable：受控制面约束；
- resumable：状态机可续跑；
- verifiable：验证者与执行者分离；
- auditable：工具账本与报告可审计；
- recoverable：失败有层级化恢复；
- self-improving：复盘写回形成下一轮更可靠判断。

Hermes V1.3 的核心不是“更会回答”，而是“每次回答前后都有一套可靠的外部认知闭环”。
