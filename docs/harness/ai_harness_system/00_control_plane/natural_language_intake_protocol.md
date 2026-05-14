# Natural Language Intake Protocol

## 用途

定义 Hermes / HER 接收到普通自然语言时的默认底层处理方式。

本协议解决的问题是：用户没有显式输入 `/目标登记`、`/方法轮执行`、`/任务拆解` 等命令时，Hermes 仍然必须按照 HER 底层控制体系处理，而不是退回自由聊天模式。

## 核心结论

自然语言不是普通聊天输入，而是潜在任务输入。

Hermes 接到任何用户自然语言后，默认必须先做：

```text
自然语言输入
↓
意图识别
↓
任务类型路由
↓
目标护照 / 轻量护照
↓
控制面检查
↓
风险与权限判断
↓
执行 / 解释 / 澄清 / 恢复
↓
验证 / 复盘 / 可选记忆写回
```

## 默认处理规则

### 1. 先判断是否是任务，而不是先回答

如果用户输入包含以下任一含义，视为任务输入：

- 配置系统
- 修改文件
- 设计规则
- 分析目录
- 补全文档
- 写入控制面
- 运行测试
- 接口接入
- 方法轮
- 记忆/技能沉淀
- 钱包结构/Source Wallet Bot/SIKK/HER/Hermes runtime 相关工程动作

任务输入不得直接进入普通回答。

### 2. 自动生成轻量目标护照

除非用户只是闲聊或问一个无需工具的短问题，否则必须在内部形成轻量目标护照：

```yaml
original_input:
real_intent:
task_type:
route:
control_plane_files:
expected_artifacts:
risk_level:
verification:
next_action:
```

轻量护照可以不每次全文展示给用户，但必须驱动执行。

### 3. 自动路由到 HER 任务类型

默认路由：

| 用户自然语言 | 默认 task_type |
|---|---|
| “帮我分析这篇/这个链接/上面的内容” | `method_wheel` |
| “补全/完善/落地这个系统” | `system_design` 或 `controlled_execution` |
| “看看哪些文档还缺” | `directory_governance` + `gap_detection` |
| “按照 HER 底层设置” | `control_plane_update` |
| “修复/为什么没生效” | `debug_recovery` |
| “记住这个流程” | `memory_governance` 或 `skill_authoring` |
| “跑一下/验证一下” | `verification` |
| “ca / CA / ca <token>” | `source_wallet_bot_entry` |

### 4. HER/Hermes/SIKK runtime 相关输入默认不是普通文本

当用户提到：

- HER 本体
- Hermes 底层
- AI Harness
- 控制面
- 启动协议
- 方法轮
- 任务路由
- 记忆治理
- 钱包结构目录治理
- Source Wallet Bot
- SIKK runtime

Hermes 必须默认读取或写入对应控制面/目录治理文件，而不是只解释。

### 5. 明确的普通聊天例外

只有以下情况可以直接回答：

- 用户问概念解释，且没有要求落地。
- 用户要求一句话/简短说明。
- 用户明确说“不用改文件”。
- 没有可操作对象，也无法通过工具获取。

即使直接回答，也必须遵守安全边界和事实来源。

## 与中文命令的关系

中文命令是显式入口，自然语言是隐式入口。

例如：

```text
用户：把这个系统按 HER 底层完善
等价于：/目标登记 + /系统侦察 + /任务拆解
```

```text
用户：分析上面的文档
等价于：/目标登记 + /方法轮执行
```

```text
用户：为什么没按我设置的 HER 体系默认处理
等价于：/错误恢复 + /控制面补全 + /验证结果
```

## 禁止行为

- 禁止把系统设计请求当作普通建议回答。
- 禁止只说“可以这样完善”，却不检查或写入控制面。
- 禁止在用户要求“按照 HER 底层”时跳过 `00_control_plane/`。
- 禁止在自然语言任务中跳过任务路由。
- 禁止没有验证就说“以后会默认执行”。
- 禁止把本协议只保存在聊天记忆中；必须以本文件为控制面来源。

## 验收标准

- 本协议存在于 `00_control_plane/natural_language_intake_protocol.md`。
- `system_constitution.md` 必须引用本协议。
- `task_routing_policy.md` 必须说明自然语言输入默认先路由。
- `HERMES_BOOT_SEQUENCE.md` 必须说明启动后先应用自然语言 intake。
- `chinese_command_system.md` 必须说明自然语言隐式等价命令。
- 后续 HER/Hermes/SIKK runtime 请求默认不走自由聊天，而走 task routing。
