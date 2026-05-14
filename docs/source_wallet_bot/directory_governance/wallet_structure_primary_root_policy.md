# Wallet Structure Primary Root Policy

## 0. HER 底层认知更新

本文件用于把 HER 对钱包结构分析项目的底层认知固定为可执行的目录规则，而不是临时聊天判断。

从本文件生效后，HER 在处理任何“钱包结构分析 / 钱包数据采集 / Source Wallet Bot / GMGN 钱包行数据 / holder-trade-cluster 标准化 / 同源组 / 资金路径 / 筹码事实 / bot2 handoff”任务时，必须先按本策略判断主目录、职责边界和禁止事项。

---

## 1. 唯一专业主目录

钱包结构分析专业主目录固定为：

```text
/root/sikk-gmgn/
```

钱包结构分析专业主数据目录固定为：

```text
/root/sikk-gmgn/data/source_wallet_bot/
```

钱包结构分析主代码目录固定为：

```text
/root/sikk-gmgn/modules/source_wallet_bot/
/root/sikk-gmgn/modules/wallet_structure/
```

标准 token 级主写路径固定为：

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

标准两层固定为：

```text
wallet_data/
structure_analysis/
```

---

## 2. 新增结构分析任务的默认落点

凡是新加入的钱包结构分析相关产物，默认写入：

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

新 token 分析优先使用：

```text
/root/sikk-gmgn/data/source_wallet_bot/live/<token_address>/
```

临时样本使用：

```text
/root/sikk-gmgn/data/source_wallet_bot/ad_hoc/<token_address>/
```

历史样本只读使用：

```text
/root/sikk-gmgn/data/source_wallet_bot/legacy/<token_address>/
```

---

## 3. 标准目录职责

### 3.1 `wallet_data/raw/`

只放原始或近原始事实输入：

- GMGN wallet rows
- GMGN holders
- GMGN traders
- GMGN wallet tags
- OKX cluster / holder / trader 原始响应
- token quote/security 只读响应
- 外部压缩包导入后的原始数据副本

不放行为推断、交易建议、状态机动作。

### 3.2 `wallet_data/normalized/`

只放标准化事实：

- `wallet_trade_normalized.json`
- `wallet_entity_profile_normalized.json`
- `token_transfer_normalized.json`
- `funding_flow_normalized.json`
- `funding_source_normalized.json`
- `backflow_paths_normalized.json`
- `gmgn_wallet_tags_normalized.json`
- `holder_delta_normalized.json`
- `quote_security_normalized.json`

### 3.3 `structure_analysis/wallet_fact/`

只放钱包事实与结构事实标准输出：

- `wallet_structure_normalized.json`
- `chip_distribution_summary.json`
- `same_source_groups.json`
- `fund_flow_edges.csv`
- `address_history.json`
- `wallet_fact_report.md`

### 3.4 `structure_analysis/intelligence/`

只放结构证据、角色分类、同源证据和 GMGN 备注字段：

- `same_source_evidence_normalized.json`
- `wallet_intelligence_decision.json`
- `wallet_role_classification.json`
- `structure_evidence_pack.json`
- `gmgn_note_fields.json`

允许使用“疑似 / 候选 / 高优先级观察 / 证据支持 / 证据不足降级”。

禁止使用“确定庄家 / 确定内幕 / 必拉 / 必买 / 稳赢 / 可买”。

### 3.5 `structure_analysis/handoff/`

只放给下游协同或行为推断模块读取的标准交接物：

- `bot2_handoff_packet.json`
- `wallet_fact_handoff.json`
- `structure_evidence_handoff.json`
- `missing_fields_report.json`

---

## 4. 主目录明确不做什么

`/root/sikk-gmgn/` 的钱包结构分析专业域不做以下事项：

1. 不做真实交易执行。
2. 不读取私钥。
3. 不签名。
4. 不广播。
5. 不 swap。
6. 不做 paper runner。
7. 不输出 paper 仓位、paper pnl、模拟买卖记录作为结构分析主产物。
8. 不直接输出 `PAPER_READY`、`BUY_READY`、`SELL`、`TAKE_PROFIT`、`STOP_LOSS` 等状态机动作。
9. 不做策略门禁最终结论。
10. 不输出“可以买 / 不能买 / 马上买 / 开仓 / 清仓”等交易建议。
11. 不做主导侧强行为终局断言。
12. 不说“确定庄家 / 确定内幕 / 确认同伙 / 老鼠仓实锤”。

钱包结构分析只输出事实、结构证据、候选分类、缺字段、降级理由和标准交接物。

---

## 5. 禁止新写入路径

以下路径只允许兼容读取或登记映射，禁止作为新任务主写路径：

```text
/root/sikk-wallet-intel/wallet_fact/data/
/root/sikk-wallet-intel/research_loop/structure_analysis/runs/
/root/sikk-gmgn/data/source_wallet_bot/*.json
/root/sikk-gmgn/data/source_wallet_bot/live/<token_address>/wallet_fact/
/root/sikk/source-bot/
```

说明：

- `/root/sikk-wallet-intel/` 是协同/总控/行为推断工作区，不是新增钱包结构分析主数据目录。
- `/root/sikk-gmgn/data/source_wallet_bot/*.json` 是历史根部漂移文件，只读兼容，不再新增。
- `live/<token>/wallet_fact/` 是历史顶层漂移路径，标准路径必须是 `structure_analysis/wallet_fact/`。
- `/root/sikk/source-bot/` 是旧 Source Bot 旁支/遗留目录，不作为当前主线主写路径。

---

## 6. 与 Wallet-Intel 的关系

`/root/sikk-wallet-intel/` 的定位固定为：

```text
协同 / 总控 / 行为推断 / AI Harness / 历史 runs 工作区
```

它可以读取 `/root/sikk-gmgn/` 的标准交接物：

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/structure_analysis/handoff/
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/structure_analysis/wallet_fact/
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/structure_analysis/intelligence/
```

但它不再承接新增钱包结构分析主数据。

Wallet-Intel 可以输出：任务票、行为推断结果、验收文件、降级报告、协同运行记录、AI Harness 制度文件。

Wallet-Intel 不应替代 `/root/sikk-gmgn/data/source_wallet_bot/` 保存 GMGN 原始钱包数据、标准化钱包事实或结构分析主产物。

---

## 7. HER 执行入口规则

HER 收到以下任务时，必须优先进入 `/root/sikk-gmgn/`：

- 钱包结构分析
- 钱包数据采集
- GMGN 钱包行数据
- holder / trade / cluster 原始接口标准化
- Source Wallet Bot `ca <token>` 触发分析
- wallet_structure_normalized 生成
- 同源组 / 资金路径 / 筹码事实
- bot2 handoff packet 生成
- GMGN note / watchlist 基础字段生成

HER 收到以下任务时，才进入 `/root/sikk-wallet-intel/`：

- Wallet-Intel 协同制度
- 总控任务票
- 行为推断模块
- AI Harness
- 协同 run 验收
- 长任务状态协议

---

## 8. 兼容与迁移原则

1. 不删除旧文件。
2. 不移动旧 runtime 输出。
3. 不覆盖旧报告。
4. 旧路径只读兼容。
5. 需要复用旧文件时，优先登记 path map 或 copy-only 到标准路径。
6. 任何轻迁移必须产生 manifest、source_path、target_path、copy_time、hash 或 size 记录。
7. 任何新写入必须走标准 token layout。

---

## 9. 验收标准

一次新的钱包结构分析任务合格，必须满足：

- 主目录在 `/root/sikk-gmgn/`。
- 主数据在 `data/source_wallet_bot/<mode>/<token_address>/`。
- 原始输入在 `wallet_data/raw/`。
- 标准事实在 `wallet_data/normalized/`。
- 钱包事实在 `structure_analysis/wallet_fact/`。
- 结构证据在 `structure_analysis/intelligence/`。
- 下游交接在 `structure_analysis/handoff/`。
- 不向 Wallet-Intel 写入钱包结构主数据。
- 不输出交易执行、paper runner、状态机动作或强行为终局断言。
