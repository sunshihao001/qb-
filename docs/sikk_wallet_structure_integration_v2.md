# SIKK 钱包结构系统接入 v2.0 方法文档

## 0. 文档目的

本文档定义“上周创建的 GMGN 钱包结构采集分析系统”在 SIKK-SOL v2.0 数据架构中的正确位置、边界、输入输出关系与后续推进顺序。

本阶段只输出方法文档，不写代码，不修改状态机，不修改 paper runner，不开启实盘。

---

## 1. 核心结论

GMGN 钱包结构系统在 SIKK-SOL v2.0 中的定位是：

```text
钱包事实源 + 钱包结构分析层 + 钱包门禁输出层
```

它不是孤立报告，也不是交易执行器。它只负责把 GMGN 钱包 / holder / trade / cluster 等接口中的钱包事实，经标准化、画像、行为分析、同源/资金/筹码迁移分析、历史地址画像后，输出标准 `wallet_structure_decision.json`。

`wallet_structure_decision.json` 只能交给 `final_trade_gate` 综合消费；状态机只读取 final gate 的结果，不能直接读取 GMGN 原始钱包字段。

标准链路：

```text
GMGN 钱包 / holder / trade / cluster 接口
  ↓
wallet_source_adapter
  ↓
wallet_structure_normalized.json
  ↓
钱包实体画像
  ↓
当前 token 钱包行为分析
  ↓
同源关系 / 资金路径 / 筹码迁移分析
  ↓
历史地址画像
  ↓
wallet_structure_decision.json
  ↓
final_trade_gate
  ↓
state_machine
  ↓
paper runner / dashboard / report
```

---

## 2. GMGN 钱包结构系统原来的分层

### 2.1 数据采集层

职责：从 GMGN 相关接口读取钱包事实。

来源包括：

- GMGN 钱包接口
- GMGN holder 接口
- GMGN trade / trader 接口
- GMGN cluster / holder cluster 接口
- GMGN 标签字段，例如 bundler、sniper、fresh wallet、transfer in、top holder、top trader、KOL、smart、rat trader 等

这一层只负责采集和保留事实，不做交易判断。

输出语义：

- 原始响应
- 原始字段路径
- 来源接口名称
- 拉取时间
- 数据质量
- 缺失字段
- fallback 记录

禁止：

- 不能把 GMGN 原始字段直接交给状态机。
- 不能从 dashboard、paper、report、case file 反推钱包事实。

### 2.2 地址实体层

职责：把单个钱包地址升级为钱包实体画像。

分析对象：

- 钱包地址
- 钱包年龄
- 是否新钱包
- 是否活跃
- 是否基础设施地址
- GMGN 标签
- 当前 token 中的买卖与持仓行为
- 资金来源字段，如有
- Token 来源字段，如有
- 历史复现，如有

输出语义：

- 钱包实体画像
- 钱包画像标签
- 地址关系边
- 实体候选组
- 画像证据等级
- 缺失字段与复查项

表达边界：

- 可以说“疑似结构相关地址”。
- 可以说“实体候选组”。
- 不说“庄家钱包”。
- 不说“确认同一个人”。

### 2.3 当前 token 行为层

职责：只分析钱包在当前 token 内的行为。

核心行为：

- 首次买入时间
- 最后卖出时间
- 买入延迟
- 持仓金额
- 持仓占比
- 卖出比例
- ROI
- PnL
- 交易次数
- Holder 排名
- 是否 Token 转入
- 是否短持 / 快速卖出
- 是否高浮盈持仓
- 是否接盘或套牢

输出语义：

- 当前 token 钱包行为表
- 早期钱包原始表
- 钱包分类表
- 结构组候选表

边界：当前 token 行为层只提供证据，不直接给交易状态。

### 2.4 资金路径与同源关系层

职责：分析钱包之间是否存在资金路径、同源候选、同步行为、Token 分发或利润回收关系。

关系类型：

- 相同资金来源
- 直接资金转入
- 利润回收
- 同步买入
- 同步卖出
- 相似金额
- 相似行为
- Token 分发接收
- 跨币共现
- 基础设施边

输出语义：

- 地址关系边
- 同源候选组
- 资金路径证据
- 筹码迁移证据
- 关系强度
- 证据等级

边界：没有资金来源时，最多输出“同步候选”或“资金待查”，不能强判同源。

### 2.5 历史地址画像层

职责：把当前 token 的钱包行为放入历史地址画像库中复核。

分析内容：

- 是否多币重复出现
- 历史入场位置
- 历史退出方式
- 历史收益稳定性
- 历史风险标签
- 历史同组地址
- 历史 GMGN 备注

输出语义：

- 历史地址画像
- 历史复现证据
- 监控优先级
- 地址库更新候选

边界：历史画像只能增强或削弱证据等级，不能越过 final gate 直接交易。

### 2.6 评分与证据等级层

职责：把钱包结构证据转为可审计分数与证据等级。

评分包括：

- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- same_source_sync_buy_score
- same_source_sync_sell_score

证据等级：

- E0：无有效证据
- E1：单点记录
- E2：弱证据
- E3：当前 token 内多字段证据
- E4：多源或资金证据增强
- E5：资金 + 行为 + 历史复现一致

边界：评分是门禁输入，不是交易指令。

### 2.7 GMGN 备注输出层

职责：把钱包画像和结构角色转成 GMGN 可用备注。

输出内容：

- address
- gmgn_note
- reason
- action

备注格式建议：

```text
代币符号-角色-结果倍数-来源/标签-风险/组别
```

边界：GMGN 备注用于监控和复盘，不是买卖建议。

### 2.8 多轮快照 delta 层

职责：比较多轮钱包结构快照，观察筹码变化。

核心 delta：

- 持仓变化
- 卖出比例变化
- 同源组同步买入变化
- 同源组同步卖出变化
- 对手盘压力变化
- 筹码迁移方向
- 数据质量变化

输出语义：

- 最新 snapshot
- latest_delta
- wallet_structure_delta
- failure attribution 证据

边界：delta 层只给出结构变化，不直接触发真实买卖。

### 2.9 wallet_structure_decision 门禁层

职责：把钱包事实、画像、行为、同源、资金、历史、delta 综合为标准钱包门禁输出。

输出文件：

```text
wallet_structure_decision.json
```

它是钱包结构系统对下游唯一标准门禁产物。

边界：

- 不直接进入 `PAPER_READY`。
- 不直接触发 `BLOCKED`。
- 不直接接状态机。
- 只能供 `final_trade_gate` 综合使用。

---

## 3. 它在 SIKK-SOL v2.0 中应该放在哪里

### 3.1 事实源接口层

位置：GMGN 原始接口之后、SIKK 标准化之前。

职责：接收 GMGN 钱包 / holder / trade / cluster 数据，并保留原始事实引用。

目标：把外部事实与内部交易状态彻底解耦。

禁止：状态机直接读取 GMGN 原始钱包字段。

### 3.2 wallet normalized 层

位置：`wallet_source_adapter` 之后。

标准产物：

```text
wallet_structure_normalized.json
```

职责：把不同 GMGN 接口、不同字段命名、不同缺失情况，统一为 SIKK-SOL v2.0 钱包 normalized 合约。

这是当前第一步要建立的核心合约。

### 3.3 钱包结构分析层

位置：normalized 之后、wallet decision 之前。

组成：

- 钱包实体画像
- 当前 token 钱包行为分析
- 同源关系分析
- 资金路径分析
- 筹码迁移分析
- 历史地址画像
- 多轮 snapshot delta

职责：只读取 normalized 与历史库，不读取 dashboard / paper / report / case file 反推事实。

### 3.4 wallet gate 层

位置：钱包结构分析层之后。

标准产物：

```text
wallet_structure_decision.json
```

职责：把钱包结构分析结果转成标准钱包门禁信号。

它可以输出：

- 支持
- 观察
- 暂停
- 风险
- 数据不足

但它不直接改变状态机状态。

### 3.5 final gate 消费层

位置：wallet gate、quote/security、pattern、lifecycle、time_context 等上游门禁之后。

职责：综合消费多个门禁结论，输出最终交易前门禁结果。

状态机只读 final gate，不读钱包原始字段，不读 normalized，不读 GMGN 原始接口。

---

## 4. v2.0 正确接入架构

### 4.1 推荐目录

```text
data/gmgn_candidates_live_run/
  wallet_sources/
    <token_address>/
      gmgn_wallet_raw.json
      gmgn_holder_raw.json
      gmgn_trade_raw.json
      gmgn_cluster_raw.json
      wallet_source_adapter_log.json
  wallet_normalized/
    <token_address>/
      wallet_structure_normalized.json
      wallet_normalized_quality_report.json
  wallet_structure/
    <token_address>/
      wallet_entity_profiles.json
      current_token_wallet_behavior.json
      same_source_groups.json
      funding_paths.json
      chip_migration.json
      historical_wallet_profiles.json
      snapshots/
        snapshot_<timestamp>.json
        latest_delta.json
      wallet_structure_decision.json
  final_gate/
    <token_address>/
      final_trade_gate.json
```

### 4.2 读取方向

允许读取方向：

```text
GMGN raw → wallet_source_adapter → wallet_structure_normalized → wallet analysis → wallet_structure_decision → final_trade_gate → state_machine
```

禁止读取方向：

```text
dashboard / paper / report / case file → wallet facts
state_machine → GMGN raw wallet fields
wallet_structure_decision → 直接 PAPER_READY / BLOCKED
wallet analysis → real swap / signing / broadcast
```

### 4.3 单向证据原则

钱包事实只能从事实源进入系统，不能从展示层、复盘层、paper 层反推。

展示层可以展示钱包字段，但不能成为钱包事实来源。

---

## 5. wallet_structure_normalized 必须字段

以下字段必须进入 `wallet_structure_normalized.json`。字段定义、类型与缺失规则详见 `docs/sikk_wallet_normalized_contract.md`。

- `token_address`
- `wallet_address`
- `snapshot_time`
- `first_buy_time`
- `last_sell_time`
- `holding_amount`
- `holding_pct`
- `sold_pct`
- `roi`
- `pnl`
- `trade_count`
- `holder_rank`
- `funding_source_address`
- `cluster_id`
- `same_source_group_id`
- `source_name`
- `retrieved_at`
- `normalized_at`
- `fallback_used`

---

## 6. wallet_structure_decision 必须字段

以下字段必须进入 `wallet_structure_decision.json`：

- `wallet_structure_status`
- `wallet_structure_score`
- `wallet_risk_score`
- `counterparty_pressure_score`
- `data_quality_score`
- `same_source_sync_buy_score`
- `same_source_sync_sell_score`
- `dominant_side_status`
- `chip_transfer_status`
- `wallet_pattern_alignment`
- `decision_action`
- `reason`
- `evidence_level`
- `created_at`
- `wallet_snapshot_time`
- `expires_at`

这些字段是 final gate 消费钱包结构的最小稳定合约。

---

## 7. 禁止事项

本阶段与后续接入阶段都必须遵守：

1. 不直接改状态机。
2. 不直接进入 `PAPER_READY`。
3. 不直接触发 `BLOCKED`。
4. 不从 dashboard / paper / report / case file 反推钱包事实。
5. 不修改实盘逻辑。
6. 不开启 hard gate。
7. 不读取私钥。
8. 不签名。
9. 不广播。
10. 不让状态机直接读取 GMGN 原始钱包字段。
11. 不让钱包结构系统直接决定交易。
12. 不把钱包评分等同于买入或卖出信号。

---

## 8. final_trade_gate 与状态机边界

### 8.1 wallet gate 只输出钱包门禁

`wallet_structure_decision.json` 可以表达：

- 钱包结构支持
- 钱包结构观察
- 钱包结构暂停
- 钱包结构风险
- 数据质量不足
- 对手盘压力
- 同源组同步买入 / 卖出
- 筹码迁移状态

但不能表达：

- 直接买入
- 直接卖出
- 直接 paper ready
- 直接 blocked
- 真实交易执行

### 8.2 final_trade_gate 才能综合

`final_trade_gate` 应综合：

- 候选发现质量
- 时间上下文
- K线 / 盘型
- 钱包结构决策
- quote/security
- lifecycle / dominant side
- market cap context
- data quality

再输出状态机可读的 final gate 结果。

### 8.3 state_machine 只读 final gate

状态机只消费 final gate 的结果，不关心 GMGN 原始钱包字段，也不直接消费 normalized 钱包事实。

---

## 9. 后续推进顺序

必须按以下顺序推进，不能跳步接状态机：

1. 建立 `wallet_structure_normalized` 合约。
2. 建立 `wallet_source_adapter`。
3. 迁移旧钱包结构分析逻辑读取 normalized。
4. 输出 `wallet_structure_decision.json`。
5. `final_trade_gate` 读取 `wallet_structure_decision.json`。
6. 状态机只读 final gate。
7. paper runner 记录钱包字段。
8. `failure_attribution` 统计钱包结构失败原因。

---

## 10. 当前阶段交付物

当前只做方法文档，不写代码。

本阶段交付：

1. `docs/sikk_wallet_structure_integration_v2.md`
2. `docs/sikk_wallet_normalized_contract.md`

验收重点：

- 是否清楚说明旧 GMGN 钱包结构系统分层。
- 是否说明其在 SIKK-SOL v2.0 中的位置。
- 是否定义 normalized 与 decision 两个关键合约字段。
- 是否明确禁止状态机直连、直接交易、反推钱包事实。
- 是否给出后续推进顺序。

---

## 11. 一句话原则

```text
GMGN 钱包结构系统负责提供标准化的钱包事实和钱包门禁输出；final_trade_gate 负责综合判断；state_machine 只读 final gate；paper/dashboard/report 只记录和展示，不反向制造事实。
```
