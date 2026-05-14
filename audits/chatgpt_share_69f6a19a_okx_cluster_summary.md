# ChatGPT 分享链接提取摘要：OKX 前300集群关联与 SIKK 纸面交易优化

来源：`https://chatgpt.com/share/69f6a19a-5344-83a3-af3e-b28438f886ab`

标题：`Branch · Branch · Branch · 纸面交易优化方案`

提取时间：本地会话中通过 direct HTML + React stream 提取。

## 1. 核心新增认知

该对话提出：OKX 前 300 Holder Cluster / 集群关联能力不应只是辅助信息，而应成为 SIKK-SOL 的正式判断层：

```text
集群关联 + 持仓行为 = 结构筹码验证层
```

它补充 GMGN 钱包结构的盲区，重点回答：

```text
结构侧筹码是否仍在？
结构侧是否撤退？
二段放量时是否出现派发？
横盘控筹是否仍由集群维持？
当前是否更像对手盘/接盘侧承接？
```

表达边界：输出中应使用“结构侧、主导侧、对手盘、接盘集群、疑似集群”等证据标签，避免确定性“庄家”措辞。

## 2. 建议新增模块

```text
sikk_okx_cluster_holding_analyzer.py
```

中文名：

```text
OKX 集群关联与持仓行为分析模块
```

推荐系统层级：

```text
候选发现
→ 市值上下文
→ 盘型识别
→ GMGN 钱包结构
→ OKX 前300集群关联 / 持仓行为
→ 主导侧生命周期
→ 主导侧动机
→ 状态机
→ paper
```

## 3. 输出目录与文件

新增目录：

```text
data/gmgn_candidates_live_run/okx_cluster/
```

单 token 输出：

```text
<token>/okx_top300_raw.csv
<token>/okx_cluster_groups.csv
<token>/okx_cluster_holding_behavior.csv
<token>/okx_cluster_decision.json
```

汇总输出：

```text
okx_cluster_summary.json
okx_cluster_summary.csv
okx_cluster_summary.md
```

## 4. 核心字段合约

### 4.1 前300集群基础字段

```text
token_address
snapshot_time
top300_wallet_count
cluster_count
linked_wallet_count
unlinked_wallet_count
largest_cluster_wallet_count
largest_cluster_holding_pct
top300_total_holding_pct
cluster_total_holding_pct
```

### 4.2 集群行为字段

```text
cluster_id
cluster_wallet_count
cluster_holding_pct
cluster_buy_amount_usd
cluster_sell_amount_usd
cluster_net_buy_usd
cluster_remaining_pct
cluster_sold_pct
cluster_avg_entry_time
cluster_avg_entry_market_cap_usd
cluster_avg_roi_pct
cluster_role
cluster_confidence
```

### 4.3 集群同步行为字段

```text
cluster_sync_buy_score
cluster_sync_sell_score
cluster_entry_time_span_sec
cluster_sell_time_span_sec
cluster_buy_amount_cv
cluster_sold_pct_cv
```

### 4.4 多轮快照 delta 字段

```text
cluster_holding_pct_delta
cluster_sold_pct_delta
cluster_net_buy_delta_usd
largest_cluster_holding_pct_delta
top300_total_holding_pct_delta
linked_wallet_count_delta
cluster_count_delta
```

### 4.5 集群状态字段

```text
okx_cluster_status
okx_cluster_score
okx_cluster_risk_score
okx_cluster_distribution_score
okx_cluster_control_retention_score
okx_cluster_reason
```

## 5. 集群角色枚举

```text
STRUCTURE_ACCUMULATION_CLUSTER     结构吸筹集群
CONTROL_HOLDING_CLUSTER            控筹持有集群
EXECUTION_CLUSTER                  执行集群
PARTIAL_DISTRIBUTION_CLUSTER       部分派发集群
ACTIVE_DISTRIBUTION_CLUSTER        主动派发集群
COUNTERPARTY_ABSORBING_CLUSTER     对手盘承接集群
BAGHOLDER_CLUSTER                  套牢集群
NOISE_CLUSTER                      噪音集群
UNKNOWN_CLUSTER                    未知集群
```

## 6. 集群状态规则

### 6.1 结构支持型

条件：

```text
largest_cluster_holding_pct >= 10
cluster_remaining_pct >= 50
cluster_sync_sell_score < 50
cluster_distribution_score < 50
counterparty_pressure_score < 60
```

输出：

```text
okx_cluster_status = CLUSTER_SUPPORT
```

### 6.2 控筹横盘型

条件：

```text
market_pattern_type = CONTROL_BOX_ACCUMULATION
box_duration_min >= 30
largest_cluster_holding_pct 稳定
top300_total_holding_pct_delta 绝对值较小
cluster_sync_sell_score < 50
```

输出：

```text
okx_cluster_status = CLUSTER_CONTROL_HOLDING
```

### 6.3 二段支持型

条件：

```text
market_pattern_type = SECOND_STAGE_EXPANSION
second_stage_valid = true
cluster_sync_sell_score < 60
largest_cluster_holding_pct_delta >= -5
cluster_distribution_score < 60
```

输出：

```text
okx_cluster_status = CLUSTER_SECOND_STAGE_SUPPORT
```

### 6.4 集群派发型

条件之一：

```text
cluster_sync_sell_score >= 70
cluster_sold_pct_delta >= 20
largest_cluster_holding_pct_delta <= -10
```

输出：

```text
okx_cluster_status = CLUSTER_DISTRIBUTION_RISK
```

### 6.5 接盘集群型

对话中提到应识别 late cluster buy / late absorbing 行为，归类为对手盘承接或接盘集群。具体实现应结合入场时间、市值位置、浮亏、后续推进失败等字段。

## 7. 与 v0.3 现有状态机的关系

该设计适合作为 SIKK-SOL v0.4 候选方向，而不是替代 v0.3。

当前 v0.3 已有：

```text
sikk_chip_control_state_machine.py
sikk_market_cap_context.py
sikk_dominant_lifecycle_classifier.py
sikk_system_audit.py
sikk_explainability_engine.py
```

下一阶段可加入：

```text
sikk_okx_cluster_holding_analyzer.py
```

并让其输出作为 `evaluate_chip_control_state()` 的附加证据输入，影响：

```text
chip_control_state
chip_control_confidence
chip_control_action
invalidators
evidence_points
```

但仍需保持：

```text
OKX 集群支持 != 买入
OKX 集群风险 != 真实卖出
只允许影响 paper/observe/pause/force_paper_exit_monitor 等纸面状态
```

## 8. 建议 v0.4 工作包

1. WP1：OKX 集群字段合约与 fixture analyzer
   - 新增 `sikk_okx_cluster_holding_analyzer.py`
   - 支持从本地 fixture / 未来 OKX 输出读取前300 holder cluster
   - 输出标准 JSON/CSV/MD

2. WP2：集群状态接入筹码控制权状态机
   - 将 `okx_cluster_status`、`okx_cluster_score`、`okx_cluster_distribution_score`、`okx_cluster_control_retention_score` 接入 `sikk_chip_control_state_machine.py`
   - 不绕过 signal/quote/security

3. WP3：dashboard / audit / explainability 增加 OKX 集群字段
   - 审计缺字段
   - 解释集群支持/风险/缺失
   - dashboard 显示 `okx_cluster_status` 与关键 delta

4. WP4：多轮快照 delta 与 paper failure attribution
   - 增加集群持仓 delta
   - 如果 paper 失败，可归因到 `CLUSTER_DISTRIBUTION_RISK`、`COUNTERPARTY_ABSORBING_CLUSTER`、`BAGHOLDER_CLUSTER` 等证据

## 9. 安全边界

该对话内容只能作为方法论/工程输入，不代表真实市场事实，也不授权真实交易。

保持：

```text
paper-only
不真实买入
不真实卖出
不调用 gmgn_swap
不调用 gmgn_cooking
不广播交易
不 yolo
```
