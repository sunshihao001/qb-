# Intel Bot 钱包结构研究工作流 2小时升级版

## Bot 2：Intel Bot

### 定位

Intel Bot 是结构情报与筹码分析 Bot。

代币集群分析、钱包结构、筹码结构、主导侧行为、主导侧行为动机推断，都归入 Intel Bot；专业表达中不使用“庄家心理”，统一称为“主导侧行为动机推断”。

### 负责范围

1. 代币 holder 集群分析
2. 钱包地址画像
3. 当前 token 钱包行为分析
4. 早期钱包识别
5. 同源执行组识别
6. 资金路径识别
7. 历史地址画像
8. 筹码集中 / 筹码迁移 / 筹码派发判断
9. 对手盘压力分析
10. 主导侧生命周期判断
11. 主导侧行为动机推断
12. 钱包 × 盘型匹配

### 代币集群分析归属

以下全部属于 Intel Bot：

- `holder_cluster`
- `same_source_group`
- `funding_source`
- `top_holder_concentration`
- `early_wallet_group`
- `distribution_receiver`
- `bagholder_whale`
- `counterparty_wallet`

### 主导侧行为动机推断枚举

- `ACCUMULATE`：`疑似吸筹`
- `CONTROL`：`疑似控盘`
- `WASHOUT`：`疑似洗盘`
- `BREAKOUT_TEST`：`疑似测试突破`
- `MARKUP`：`疑似推进拉升`
- `PARTIAL_DISTRIBUTION`：`疑似部分派发`
- `ACTIVE_DISTRIBUTION`：`疑似主动派发`
- `REACCUMULATION`：`疑似再吸筹`
- `REACTIVATION`：`疑似再激活`
- `ABANDONMENT`：`疑似放弃维护`

### 标准输出

- `shared/decisions/wallet_structure/<token>/wallet_structure_decision.json`
- `shared/decisions/chip/<token>/chip_transfer_decision.json`
- `shared/decisions/lifecycle/<token>/dominant_lifecycle_decision.json`
- `shared/decisions/intent/<token>/dominant_intent_decision.json`
- `shared/reports/wallet/<token>/wallet_report.md`

### 禁止事项

Intel Bot 不能：

- 直接交易
- 直接 `PAPER_READY`
- 直接 `BLOCKED`
- 开仓
- 止损
- 止盈
- 修改状态机

## 任务定位

本任务只研究 **Intel Bot 钱包结构分析子系统**，不改交易代码，不接入状态机，不开启 paper，不开启实盘，不执行 swap，不读取私钥，不签名，不广播。

## Intel Bot 的唯一职责

- wallet_structure_decision
- dominant_lifecycle_decision
- dominant_intent_decision
- chip_transfer_decision
- gmgn_note_table
- wallet_report

## 不允许做的事

- 直接 PAPER_READY
- 直接 BLOCKED
- 修改状态机
- 修改 paper runner
- 执行交易
- 读取私钥
- 签名
- 广播
- swap

## 资料边界

本次接收的是 `SIKK-GMGN 保留数据包：截止 2026-04-30 10:22 +08:00` 的 legacy 钱包情报快照。
它只作为历史钱包分析数据包、历史地址库种子、旧钱包结构报告归档来处理。

## 方法原则

1. 不直接判断“庄家”。
2. 只输出“疑似结构角色”。
3. 所有判断必须有字段证据、规则依据、证据等级、风险等级。
4. 单个字段不能决定角色。
5. GMGN 标签只能作为辅助证据。
6. 当前 token 行为、资金来源、同源关系、历史复现必须分层判断。
7. wallet_structure_decision 是交易侧唯一交接文件。
8. final_trade_gate 才能决定是否进入交易流程。

## 交付目录

Intel Bot 现在使用单独目录记录数据，避免和其他 Bot / 状态机 / 交易侧文件混放：

- `data/gmgn_candidates_live_run/intel-bot/`
  - `code/`：Intel Bot 相关代码索引、schema 合同副本、生成脚本索引、只读分析模块说明。
  - `logs/`：Intel Bot 每轮运行、每个 token 的结构分析输出、钱包画像结果、筹码结构报告、同源 / 分发 / 接盘 / 结果钱包判断日志。

历史研究文档仍保留在：

- `docs/intel_bot/`

迁移过来的历史数据也必须进入 Intel Bot 专属目录，禁止再散放到旧目录：

- 禁止：`data/gmgn_candidates_live_run/intel_bot/`
- 禁止：`data/gmgn_candidates_live_run/wallet_structure/`
- 统一：`data/gmgn_candidates_live_run/intel-bot/logs/`

## 本阶段交付原则

- 只做研究、护照、分层复原、缺口扫描、模块设计、命令镜头、后续任务包。
- 不进入任何交易执行路径。
