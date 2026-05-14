# AI-Driven Trading Structure Control System

## 0. 定位

本文件把 SIKK 钱包结构分析从“单个钱包分析模块”升级为 AI 驱动的交易结构系统总控工程。

核心链路：

```text
Skill 能力地图
→ 目标系统映射
→ 自动发现缺口
→ 自动补全实现
→ 验证闭环
```

本系统遵循 Harness Engineering：模型不能只靠“聪明”，必须具备控制面、循环、权限、恢复、验证和多代理分工。Skill 不能被当成提示词，而必须被当成可验证、可审计、可复用的工作流模块。

---

## 1. 系统本质

新代币出现后，系统不是为了“找庄家买币”，而是为了判定：

1. token 是否先通过安全与市场硬门槛。
2. 早期结构资金是否真实存在。
3. 结构资金是否还没完全派发。
4. 当前走势是否仍受结构侧控制。
5. 当前参与是否具备风险收益比。
6. 用户是否会成为结构资金出货的流动性。

完整流程：

```text
新代币出现
→ 调用各 skill 拉取可用数据
→ 排除安全硬风险
→ 排除市场硬风险
→ 建立早期钱包事实
→ 识别疑似结构钱包 / 同源执行组
→ 识别第一波控盘箱体
→ 判断早期结构资金是否派发完成
→ 判断是否仍有二次拉升 / 二段扩张动机
→ 结合 K 线、动量、成本区、策略方法、钱包持仓、生命周期
→ 输出：排除 / 记录 / 风险监控 / 观察 / 纸面入场 / 实盘候选
```

---

## 2. 系统根目录分工

### 2.1 钱包结构与数据事实主目录

```text
/root/sikk-gmgn/
```

负责：

- 数据采集
- 安全/市场事实接入
- GMGN / OKX / holder / trade / cluster 原始数据
- 钱包事实标准化
- 钱包结构识别
- 同源组/资金路径/筹码事实
- 结构证据包
- bot2 handoff
- Skill 能力地图与目标系统映射的主工程落地

### 2.2 协同与行为推断工作区

```text
/root/sikk-wallet-intel/
```

负责：

- 协同制度
- 总控任务票
- 行为推断
- AI Harness
- 长任务状态
- 验收 runs

不作为新增钱包结构主数据目录。

---

## 3. Skill 能力地图

Skill 在本系统中不是提示词，而是可验证工作流模块。每个 Skill 必须具备：

```text
能力名称
输入合同
输出合同
依赖数据
允许权限
禁止权限
验证方法
失败恢复
下游消费者
```

### 3.1 数据接入类 Skill

能力：

- GMGN token info
- GMGN wallet rows
- GMGN holders
- GMGN traders
- GMGN wallet tags
- OKX cluster
- quote/security
- K 线/价格/成交量

输出位置：

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token>/wallet_data/raw/
```

必须输出：

```text
source
capture_time
token_address
raw_payload
endpoint_or_adapter
fetch_status
error_reason
```

### 3.2 安全硬风险 Skill

目标：先排除不能碰的 token。

检查：

- mint 权限
- freeze 权限
- blacklist/whitelist 风险
- tax 风险
- honeypot 风险
- liquidity lock/burn
- top holder 过度集中
- contract / pool 异常

输出：

```text
security_hard_gate.json
```

状态：

```text
SECURITY_PASS
SECURITY_BLOCK
SECURITY_WARN
INSUFFICIENT_DATA
```

### 3.3 市场硬风险 Skill

目标：排除市场结构上不能分析或风险过硬的 token。

检查：

- liquidity 太低
- volume 太低或异常
- market cap 异常
- spread/滑点异常
- 池子太新且数据不足
- 价格过度瞬时拉升
- 持续砸盘结构

输出：

```text
market_hard_gate.json
```

状态：

```text
MARKET_PASS
MARKET_BLOCK
MARKET_WARN
INSUFFICIENT_DATA
```

### 3.4 钱包事实 Skill

目标：建立早期钱包事实。

输出：

```text
wallet_structure_normalized.json
chip_distribution_summary.json
same_source_groups.json
fund_flow_edges.csv
address_history.json
```

目录：

```text
structure_analysis/wallet_fact/
```

### 3.5 结构识别 Skill

目标：识别疑似结构钱包 / 同源执行组 / 早期资金。

输出：

```text
wallet_role_classification.json
same_source_evidence_normalized.json
structure_evidence_pack.json
wallet_intelligence_decision.json
```

目录：

```text
structure_analysis/intelligence/
```

### 3.6 箱体与成本区 Skill

目标：识别第一波控盘箱体、成本区与筹码控制区。

输入：

- K 线
- 早期钱包成本
- holder 变化
- 成交量
- 结构钱包持仓变化

输出：

```text
control_box_detection.json
cost_zone_analysis.json
```

### 3.7 派发进度 Skill

目标：判断早期结构资金是否已经派发完成。

输入：

- 早期钱包持仓
- 同源组持仓变化
- 大额卖出
- 接盘钱包
- 回流路径
- price/volume 变化

输出：

```text
distribution_progress.json
chip_control_retention.json
```

### 3.8 二段扩张动机 Skill

目标：判断是否仍存在二次拉升 / 二段扩张动机。

输入：

- 控盘箱体
- 成本区
- 派发进度
- 筹码保留
- 反证
- 市场动量

输出：

```text
second_leg_motivation_hypothesis.json
```

必须包含：

```text
evidence_level
confidence_score
supporting_evidence
counter_evidence
downgrade_reason
```

### 3.9 策略门禁 Skill

目标：把事实、结构、行为、市场、安全转成观察/排除/纸面候选状态。

输出：

```text
structure_strategy_gate.json
```

允许状态：

```text
EXCLUDE
RECORD_ONLY
RISK_MONITOR
OBSERVE
PAPER_CANDIDATE
LIVE_CANDIDATE_REQUIRES_HUMAN_CONFIRMATION
```

禁止直接输出：

```text
BUY_NOW
SELL_NOW
AUTO_TRADE
```

---

## 4. 目标系统映射

系统目标不是单点分析，而是把每个分析问题映射到 Skill、数据、产物和验收。

| 目标问题 | 上游 Skill | 核心产物 | 下游消费 |
|---|---|---|---|
| token 是否安全 | 安全硬风险 | security_hard_gate.json | 策略门禁 |
| 市场是否可分析 | 市场硬风险 | market_hard_gate.json | 策略门禁 |
| 早期结构资金是否存在 | 钱包事实 + 结构识别 | structure_evidence_pack.json | 行为推断 |
| 是否同源执行组 | 同源分析 | same_source_groups.json | 结构识别 |
| 第一波控盘箱体在哪 | 箱体与成本区 | control_box_detection.json | 二段动机 |
| 是否派发完成 | 派发进度 | distribution_progress.json | 策略门禁 |
| 是否仍有二段动机 | 二段扩张动机 | second_leg_motivation_hypothesis.json | 策略门禁 |
| 是否会成为出货流动性 | 策略门禁 + 反证 | structure_strategy_gate.json | 人类决策 |

说明：Markdown 表格只用于文档展示，机器合同应以 JSON schema 固定。

---

## 5. 自动发现缺口

总控必须自动检查：

### 5.1 能力缺口

```text
需要某项判断，但没有对应 Skill。
```

输出：

```text
skill_gap_report.json
```

### 5.2 数据缺口

```text
Skill 存在，但上游数据缺失或不可用。
```

输出：

```text
data_gap_report.json
missing_source_blockers.json
```

### 5.3 合同缺口

```text
有脚本输出，但没有 schema / handoff contract。
```

输出：

```text
contract_gap_report.json
```

### 5.4 验证缺口

```text
有实现，但没有测试、验收或回归样本。
```

输出：

```text
verification_gap_report.json
```

### 5.5 权限缺口

```text
某 Skill 需要越权读取或写入。
```

输出：

```text
permission_gap_report.json
```

---

## 6. 自动补全实现

自动补全必须走 HER 长任务闭环，而不是随手写脚本。

顺序：

```text
发现缺口
→ 判断缺口类型
→ 生成任务票
→ 确认目录归属
→ 写最小合同 / schema
→ 写最小实现
→ 写测试或验收脚本
→ 运行验证
→ 写 acceptance_report
→ 更新能力地图
```

禁止：

- 无 schema 直接扩实现
- 无测试直接宣布完成
- 为了通过而伪造字段
- 让行为推断层倒逼事实层造数据
- 越权接入交易执行

---

## 7. 控制面

总控工程必须有控制面，而不是让模型自由发挥。

控制面包括：

```text
skill_registry.json
system_target_map.json
gap_reports/
task_tickets/
run_state/
acceptance/
recovery/
permission_policy.json
```

建议目录：

```text
/root/sikk-gmgn/docs/harness/trading_structure_control/
/root/sikk-gmgn/research_loop/state/trading_structure_control/
/root/sikk-gmgn/contracts/shared/trading_structure_control/
```

---

## 8. 多代理分工

### 8.1 Controller / Orchestrator

负责：

- 读取目标系统映射
- 选择 Skill
- 发现缺口
- 生成任务票
- 检查验收
- 不直接做业务判断

### 8.2 Data Skill Worker

负责：

- 拉取数据
- 标准化事实
- 输出 source 和质量报告

### 8.3 Structure Worker

负责：

- 同源组
- 钱包结构
- 资金路径
- 筹码分布
- 角色分类

### 8.4 Behavior Worker

负责：

- 生命周期假设
- 派发进度
- 二段扩张动机
- 反证与降级

### 8.5 Gate Worker

负责：

- 安全硬门槛
- 市场硬门槛
- 策略状态归类
- 风险收益比结构化输出

### 8.6 Auditor / Judge

负责：

- 检查产物齐全
- 检查字段来源
- 检查禁止事项
- 检查下游是否只读上游标准产物
- 检查缺字段是否降级

---

## 9. 状态输出分层

最终输出不是买卖指令，而是分层状态。

允许状态：

```text
EXCLUDE                  # 安全/市场/结构硬排除
RECORD_ONLY              # 记录但不跟踪
RISK_MONITOR             # 风险监控
OBSERVE                  # 观察
PAPER_CANDIDATE          # 纸面候选，仍不等于实盘
LIVE_CANDIDATE_REQUIRES_HUMAN_CONFIRMATION
```

禁止状态：

```text
BUY_NOW
SELL_NOW
AUTO_TRADE
GUARANTEED_PROFIT
CONFIRMED_DEALER
```

---

## 10. 验证闭环

每次完整运行必须验证：

1. Skill 是否来自 registry。
2. 输入是否满足合同。
3. 输出是否满足 schema。
4. 缺字段是否进入 downgrade。
5. 禁止事项是否没有出现。
6. 下游是否只读取允许产物。
7. gate 状态是否有证据链。
8. 是否生成 acceptance_report。
9. 是否更新 gap report。
10. 是否保留 recovery 信息。

验收输出：

```text
acceptance_report.json
acceptance_report.md
```

验收状态：

```text
PASS
PASS_WITH_DOWNGRADE
FAIL_BLOCKED
FAIL_CONTRACT_VIOLATION
FAIL_PERMISSION_VIOLATION
```

---

## 11. 权限边界

允许：

- 只读数据采集
- 文件写入标准数据目录
- schema / contract / report / acceptance 生成
- copy-only legacy 兼容
- 多代理分工
- 自动补全缺失 workflow 模块

禁止：

- 私钥读取
- 签名
- broadcast
- swap
- 自动实盘
- 绕过人工确认进入 LIVE
- 输出保证收益
- 输出确定内幕/确定庄家
- 缺字段硬推断

---

## 12. 与钱包结构分析主目录的关系

钱包结构分析仍然是本总控工程的事实与结构底座：

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token>/
```

但总控工程覆盖更高一层：

```text
Skill 能力地图
目标系统映射
缺口发现
自动补全
验证闭环
权限控制
多代理分工
```

因此：

- 钱包结构分析是子系统。
- Skill registry 是能力控制层。
- Gate 是状态归类层。
- Auditor 是闭环保障层。
- Orchestrator 是调度控制层。

---

## 13. 下一步落地优先级

### P0：制度固定

- `skill_registry.schema.json`
- `system_target_map.schema.json`
- `gap_report.schema.json`
- `acceptance_report.schema.json`
- `permission_policy.json`

### P1：能力盘点

- 扫描现有 modules / scripts / skills
- 生成 `skill_capability_inventory.json`
- 标注 implemented / missing / partial

### P2：目标映射

- 建立 `system_target_map.json`
- 每个目标问题绑定 skill、输入、输出、验收

### P3：缺口扫描器

- 自动输出能力缺口、数据缺口、合同缺口、验证缺口、权限缺口

### P4：自动补全 runner

- 根据缺口生成任务票
- 最小实现
- 测试
- 验收
- 回写 registry

### P5：E2E 样本验证

- 用一个 token 跑完整链路
- 输出 PASS / PASS_WITH_DOWNGRADE / FAIL
