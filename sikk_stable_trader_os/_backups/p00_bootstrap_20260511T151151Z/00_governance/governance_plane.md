# SIKK Stable Trader OS｜Governance Plane v2.0

## 0. 文件定位

本文件定义 SIKK Stable Trader OS 的治理平面。

治理平面是整个系统的最高约束层，用于回答：

```text
系统为什么存在？
系统当前处于什么运行模式？
系统允许做什么？
系统禁止做什么？
哪些动作必须被阻断？
哪些阶段可以启动？
哪些结果可以进入下游？
````

本文件不是交易策略。  
本文件不是阶段执行文档。  
本文件不是 Atomic Skill。  
本文件不是买卖判断规则。

本文件是所有阶段、Skill、工具、Schema、Contract、Report、Replay、Review 的上位治理约束。

---

## 1. 治理平面的系统位置

SIKK Stable Trader OS 的完整系统平面包括：

```text
治理平面 Governance Plane
领域平面 Domain Plane
数据平面 Data Plane
控制平面 Control Plane
决策平面 Decision Plane
风险平面 Risk Plane
执行平面 Execution Plane
验证平面 Verification Plane
学习平面 Learning Plane
```

治理平面位于最上层。

它的作用不是直接做判断，而是定义所有判断的边界。

```text
没有治理平面，系统会变成自由解释。
没有治理平面，HER 会不知道哪些事情允许做、哪些事情禁止做。
没有治理平面，阶段、Skill、工具和报告都会失去上位约束。
```

---

## 2. 治理平面的核心职责

治理平面负责：

```text
1. 定义系统总目标
2. 定义系统非目标
3. 定义当前运行模式
4. 定义允许事项
5. 定义禁止事项
6. 定义系统硬边界
7. 定义实盘权限边界
8. 定义自动判断边界
9. 定义阶段启动条件
10. 定义升级与规则变更边界
11. 定义 HER 执行权限
12. 定义风险不可绕过原则
```

治理平面不负责：

```text
1. 不负责直接判断买入
2. 不负责直接判断卖出
3. 不负责直接判断钱包角色
4. 不负责直接判断筹码控制
5. 不负责直接执行交易
6. 不负责直接修改策略规则
7. 不负责直接替代阶段验收
```

---

## 3. 系统总目标

SIKK Stable Trader OS 的总目标是：

```text
建立一个由 HER 调度的结构化交易研究操作系统，
通过事实校验、市场场景识别、钱包结构分析、筹码控制判断、策略门禁、风险否定、纸面验证、复盘归因和规则升级，
将 memecoin token 从候选发现到纸面验证的全过程变成可追溯、可验收、可复盘、可升级的判断链条。
```

系统目标不是：

```text
寻找最多机会
让 AI 直接喊单
让 AI 直接实盘交易
只靠钱包判断买卖
只靠 K 线判断买卖
只靠主观解释判断庄家
```

系统真正目标是：

```text
少犯错
少接盘
少进入错误场景
少被假结构欺骗
少被派发结构诱导
少让证据不足样本进入纸面验证
少让风险未确认样本进入执行层
```

---

## 4. 系统当前运行模式

当前系统默认运行模式为：

```text
SYSTEM_BUILDING
```

含义：

```text
当前处于系统体系建设阶段。
允许建立系统方法论、系统平面、阶段模型、领域对象、状态机、数据流、判断流、风险流、handoff 流、Atomic Skill 抽取原则和 HER 执行协议。
不允许直接进入实盘自动交易。
不允许直接输出买卖指令。
```

---

## 5. 系统运行模式定义

### 5.1 SYSTEM_BUILDING

```text
系统建设阶段。
允许搭建系统结构、阶段、Skill、Schema、Contract、Report、Replay、Review。
禁止实盘交易。
禁止自动买卖判断。
```

### 5.2 SYSTEM_READY

```text
系统结构完成，核心阶段和基础验证机制存在。
允许进入纸面验证准备。
仍不代表允许实盘。
```

### 5.3 SYSTEM_WITH_GAPS

```text
系统存在缺口，但缺口不一定阻断所有建设。
允许继续补充非阻断模块。
不得进入被缺口阻断的阶段。
```

### 5.4 SYSTEM_BLOCKED

```text
存在 BLOCKER 级缺口。
禁止进入下游阶段。
必须先修复阻断问题。
```

### 5.5 SYSTEM_RUNNING

```text
系统开始按阶段处理候选 token。
必须有 Runtime State、Phase State、Handoff Packet 和日志。
```

### 5.6 SYSTEM_REVIEWING

```text
系统处于复盘阶段。
允许生成 failure attribution、review report、rule adjustment candidates。
不允许直接修改实时规则。
```

### 5.7 SYSTEM_UPGRADING

```text
系统处于规则升级阶段。
允许生成 upgrade proposal、rule change log、skill update plan。
新规则不得未经审计直接生效。
```

---

## 6. 当前允许事项

在 SYSTEM_BUILDING 阶段，允许：

```text
1. 建立 system_methodology_blueprint.md
2. 建立 governance_plane.md
3. 建立 domain_plane.md
4. 建立 data_plane.md
5. 建立 control_plane.md
6. 建立 decision_plane.md
7. 建立 risk_plane.md
8. 建立 execution_plane.md
9. 建立 verification_plane.md
10. 建立 learning_plane.md
11. 建立 domain_object_registry.yaml
12. 建立 state_dictionary.yaml
13. 建立 phase_registry.yaml
14. 建立 phase_transition_map.yaml
15. 建立 system_state_machine.yaml
16. 建立 data_flow_map.md
17. 建立 decision_flow_map.md
18. 建立 risk_flow_map.md
19. 建立 handoff_flow_map.md
20. 建立 atomic_skill_extraction_policy.md
21. 建立 atomic_skill_registry.yaml
22. 建立 her_execution_protocol.md
23. 建立总控 Skill
24. 建立 P00_system_boundary 阶段包
25. 建立 P01_data_fact 阶段包
```

---

## 7. 当前禁止事项

在 SYSTEM_BUILDING 阶段，禁止：

```text
1. 禁止直接输出买入判断
2. 禁止直接输出卖出判断
3. 禁止直接实盘交易
4. 禁止创建无边界的自动交易脚本
5. 禁止跳过 P00_system_boundary
6. 禁止跳过 P01_data_fact
7. 禁止没有事实字段就进行推理
8. 禁止用 AI 推测补全事实字段
9. 禁止用 report 文字替代机器字段
10. 禁止没有 handoff_packet 就进入下游阶段
11. 禁止没有 acceptance_gate 就标记阶段完成
12. 禁止没有 replay 的判断直接进入正式系统
13. 禁止复盘结果直接污染实时规则
14. 禁止阶段直接等同于 Skill
15. 禁止无注册 Atomic Skill 被阶段调用
16. 禁止未通过风险层直接进入执行层
```

---

## 8. 系统硬边界

以下边界为全局硬边界，任何阶段、Skill、工具和 HER 任务不得绕过。

---

### 8.1 实盘边界

默认状态：

```text
LIVE_DISABLED
```

含义：

```text
系统默认不允许无人工确认的实盘交易。
```

允许实盘必须满足：

```text
1. P00 明确允许实盘模式
2. P01 数据事实层通过
3. P02-P05 判断链通过
4. P06 风险控制通过
5. P07 生成 execution_ticket
6. 已设置最大亏损、滑点、手续费、仓位限制
7. 已设置连续失败熔断
8. 已设置单 token 重复入场限制
9. 已记录人工确认
10. 已记录真实交易回填字段
```

当前阶段不满足上述条件，因此：

```text
禁止实盘自动执行
```

---

### 8.2 自动判断边界

自动判断不得直接产生：

```text
BUY
SELL
ALL_IN
MARKET_BUY
MARKET_SELL
LIVE_EXECUTE
```

自动判断只允许输出：

```text
STRATEGY_BLOCK
STRATEGY_PAUSE
STRATEGY_WATCH
PAPER_READY
READY_FOR_CONFIRMATION
```

即使输出 `PAPER_READY`，也只代表：

```text
允许进入纸面验证或人工确认准备
不代表允许实盘执行
```

---

### 8.3 AI 推理边界

AI 可以做：

```text
结构化归纳
证据链整理
反证识别
阶段状态判断
风险提示
规则候选建议
复盘归因
```

AI 不可以做：

```text
凭空补全缺失字段
将推测写成事实
跳过硬否定
无数据来源给出确定结论
用语气强度替代证据等级
把 report 当成机器判断输入
```

---

### 8.4 复盘边界

P08 复盘结果不能直接改变实时规则。

P08 只能输出：

```text
failure_attribution.json
review_report.md
rule_adjustment_candidates.json
```

P09 才能输出：

```text
upgrade_proposal.json
rule_change_log.md
skill_update_plan.md
field_update_plan.md
```

规则正式生效必须满足：

```text
1. 有 rule_change_log
2. 有版本号
3. 有变更原因
4. 有影响范围
5. 有回滚方案
6. 有人工确认或明确授权
```

---

## 9. 阶段启动治理规则

### 9.1 P00 启动条件

P00 可以在 SYSTEM_BUILDING 阶段启动。

P00 目标：

```text
确认系统边界、运行模式、禁止事项、允许事项和 P01 启动条件。
```

---

### 9.2 P01 启动条件

P01 启动必须满足：

```text
1. P00 已完成
2. P00 输出 phase_00_handoff_packet.json
3. P00 未命中 BLOCKER
4. 当前模式允许数据事实层建设
```

P01 目标：

```text
建立输入快照、字段来源映射、标准事实层和 phase_01_handoff_packet。
```

---

### 9.3 P02 启动条件

P02 启动必须满足：

```text
1. P01 = PHASE_READY
或
2. P01 = PHASE_WITH_GAPS 且 gap 不影响 P02 必需字段
```

禁止：

```text
P01 未完成时直接进入 P02 市场场景判断。
```

---

### 9.4 P03 启动条件

P03 启动必须满足：

```text
1. P01 已输出钱包相关事实字段
2. 钱包地址、交易事件、时间戳、持仓变化字段可用
3. 字段来源可追踪
```

禁止：

```text
无钱包事实字段时直接判断钱包角色。
```

---

### 9.5 P04 启动条件

P04 启动必须满足：

```text
1. P03 已输出 wallet_classification
2. P03 已输出 same_source_groups 或明确缺失
3. P03 已输出 wallet_structure_decision
```

禁止：

```text
没有钱包结构证据时直接判断筹码控制。
```

---

### 9.6 P05 启动条件

P05 启动必须满足：

```text
1. P02 市场场景结果存在
2. P03 钱包结构结果存在
3. P04 筹码控制结果存在
4. 风险硬否定未提前阻断
```

禁止：

```text
只凭 K 线或只凭钱包单项结果进入策略门禁。
```

---

### 9.7 P06 启动条件

P06 启动必须满足：

```text
1. P05 输出策略门禁状态
2. P05 未输出 STRATEGY_BLOCK
3. 需要进一步评估安全、流动性、报价、滑点和执行风险
```

禁止：

```text
策略门禁未通过时进入执行风险评估并试图放行。
```

---

### 9.8 P07 启动条件

P07 启动必须满足：

```text
1. P05 = PAPER_READY 或 READY_FOR_CONFIRMATION
2. P06 = RISK_APPROVED
3. 生成 execution_ticket
4. 明确执行模式 PAPER_ONLY 或 HUMAN_CONFIRMATION_REQUIRED
```

禁止：

```text
P05 / P06 未通过时进入执行层。
```

---

### 9.9 P08 启动条件

P08 启动必须满足：

```text
1. 已有 paper position 或 rejected sample
2. 已有阶段判断记录
3. 已有 strategy decision trace
4. 已有风险记录或交易结果
```

---

### 9.10 P09 启动条件

P09 启动必须满足：

```text
1. P08 输出 failure_attribution
2. P08 输出 rule_adjustment_candidates
3. P08 明确哪些是事实归因，哪些是解释性假设
```

禁止：

```text
没有复盘归因时直接升级系统规则。
```

---

## 10. HER 权限治理

HER 在系统中不是自由决策者，而是：

```text
系统调度器
阶段执行器
文件生成器
状态回写器
验收执行器
失败恢复器
交接包生成器
```

---

## 10.1 HER 可以做

```text
1. 读取治理平面
2. 读取运行状态
3. 读取阶段定义
4. 读取领域对象
5. 检查输入字段
6. 标记缺口
7. 生成阶段文档
8. 生成结构化输出
9. 生成 handoff_packet
10. 更新 phase_state
11. 生成 report
12. 生成 replay plan
13. 生成 rule upgrade proposal
```

---

## 10.2 HER 不可以做

```text
1. 绕过治理平面
2. 绕过阶段顺序
3. 绕过硬否定
4. 绕过风险控制
5. 绕过 handoff
6. 绕过 acceptance_gate
7. 凭空补全事实字段
8. 将推测写成事实
9. 未经授权直接实盘
10. 复盘后直接修改实时规则
```

---

## 11. 治理平面输入

治理平面应读取或引用以下文件：

```text
system_methodology_blueprint.md
system_manifest.yaml
global_building_principles.md
forbidden_action_policy.yaml
risk_boundary_policy.yaml
current_system_state.json
```

如果这些文件未全部存在，系统状态应标记为：

```text
SYSTEM_WITH_GAPS
```

如果缺失文件影响阶段边界判断，系统状态应标记为：

```text
SYSTEM_BLOCKED
```

---

## 12. 治理平面输出

治理平面应输出：

```text
governance_status.json
governance_boundary_summary.json
governance_forbidden_actions.json
governance_allowed_actions.json
governance_gap_list.json
governance_handoff_packet.json
```

---

## 13. 治理状态结构

标准治理状态结构：

```json
{
  "plane": "governance_plane",
  "system": "SIKK Stable Trader OS",
  "status": "GOVERNANCE_READY",
  "runtime_mode": "SYSTEM_BUILDING",
  "live_trading_allowed": false,
  "automated_execution_allowed": false,
  "paper_trading_allowed": true,
  "active_phase_allowed": [
    "P00_system_boundary",
    "P01_data_fact"
  ],
  "forbidden_actions": [
    "LIVE_EXECUTE",
    "AI_INFER_FACT_FIELD",
    "SKIP_ACCEPTANCE_GATE",
    "SKIP_HANDOFF_PACKET"
  ],
  "blocking_gaps": [],
  "next_required_plane": "domain_plane"
}
```

---

## 14. 治理平面验收标准

治理平面完成必须满足：

```text
1. 明确系统总目标
2. 明确系统非目标
3. 明确当前运行模式
4. 明确当前允许事项
5. 明确当前禁止事项
6. 明确实盘边界
7. 明确自动判断边界
8. 明确 AI 推理边界
9. 明确复盘升级边界
10. 明确 P00-P09 启动条件
11. 明确 HER 权限边界
12. 明确治理平面输入
13. 明确治理平面输出
14. 明确治理状态结构
15. 明确后续下游平面
```

---

## 15. 与其他系统平面的关系

### 15.1 对领域平面的约束

治理平面要求领域平面必须先定义对象，再定义判断。

```text
不得在未定义 Token、Wallet、MarketScene、ChipState、GateDecision 等对象前进入阶段判断。
```

---

### 15.2 对数据平面的约束

治理平面要求数据平面必须区分：

```text
事实字段
推理字段
状态字段
报告字段
```

事实字段不得由 AI 推测生成。

---

### 15.3 对控制平面的约束

治理平面要求控制平面必须定义：

```text
阶段顺序
阶段启动条件
阶段退出条件
handoff 条件
acceptance gate
```

---

### 15.4 对决策平面的约束

治理平面要求每个判断必须包含：

```text
decision
evidence
counter_evidence
confidence
invalidation_conditions
next_action
```

---

### 15.5 对风险平面的约束

治理平面要求风险平面必须拥有一票否定权。

硬否定命中时，任何解释不得继续放行。

---

### 15.6 对执行平面的约束

治理平面默认执行层为：

```text
LIVE_DISABLED
```

只有经过明确模式切换和多阶段验收，才允许进入人工确认或实盘准备。

---

### 15.7 对验证平面的约束

治理平面要求：

```text
无 schema 不正式
无 contract 不交接
无 replay 不稳定
无 acceptance gate 不完成
```

---

### 15.8 对学习平面的约束

治理平面要求：

```text
复盘归因不得直接污染实时规则
规则升级必须进入 proposal
proposal 必须审计后才可生效
```

---

## 16. 治理平面的下游派生文件

本文件完成后，后续应派生：

```text
forbidden_action_policy.yaml
risk_boundary_policy.yaml
system_manifest.yaml
current_system_state.json
P00_system_boundary/phase_manifest.yaml
P00_system_boundary/acceptance_gate.yaml
```

---

## 17. 治理平面总结

治理平面是 SIKK Stable Trader OS 的最高约束层。

它不负责寻找机会。  
它不负责直接判断交易。  
它不负责执行交易。

它负责确保：

```text
系统不越权
阶段不跳跃
HER 不自由发挥
AI 不补事实
风险不被解释绕过
复盘不污染实时规则
实盘不被提前打开
```

治理平面完成后，系统才允许进入领域平面设计。
