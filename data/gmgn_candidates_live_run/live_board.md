# SIKK Live Board

- 更新时间：2026-05-04T12:40:24Z
- 运行状态：正常生成
- 边界：只做持续监控、分析、quote/security、纸面流程和复盘，不执行真实 swap。

## 1. 系统总览
- 本轮 Token 数：5
- WATCHING：2
- PAUSE：0
- BLOCKED：2
- PAPER_READY：0
- PAPER_OPEN：0
- 钱包结构接入率：5 / 5
- 当前开放仓位：0
- 样本可信度：低（以关闭仓位统计为准）

## 2. 重点机会
- 当前无 PAPER_READY / WALLET_SUPPORT token。

## 3. 钱包结构状态
- WALLET_SUPPORT：0
- WALLET_PAUSE：0
- WALLET_BLOCK：1
- WALLET_NEUTRAL：0
- MISSING：0

### 钱包结构未接入原因
- 无

## 4. 阻断 / 暂停原因
- jestin  / D5GpuB8FAWAc6Qex1p3B1vT9DJKvjPNuBzQgX5y3bonk
  - Priority：P3_WATCHING
  - State：WATCHING
  - Signal：UNKNOWN / UNKNOWN
  - Wallet：未接入 / score=None / risk=None / counterparty=None / data=None
  - Quote/Security：MISSING / MISSING
  - Paper：NONE / PnL=-
  - 主原因：候选筛选等级为观察层，等待更多 K线/结构证据
  - Next：LIVE_RUN_SYNC
- trolls / 7CR3CBpivSMzBEet3cvUckjeSLdbCKaxRB1yNNm6pump
  - Priority：P3_WATCHING
  - State：WATCHING
  - Signal：S1_观察信号 / UNKNOWN
  - Wallet：未接入 / score=None / risk=None / counterparty=None / data=None
  - Quote/Security：MISSING / MISSING
  - Paper：NONE / PnL=-
  - 主原因：SIKK 信号仍为观察/预备层
  - Next：LIVE_RUN_SYNC
- CARDS / ziffq43QSCC95DUjVc7cULKYttEHyA1pops25gDpump
  - Priority：P5_BLOCKED
  - State：BLOCKED
  - Signal：UNKNOWN / UNKNOWN
  - Wallet：未接入 / score=None / risk=None / counterparty=None / data=None
  - Quote/Security：MISSING / MISSING
  - Paper：NONE / PnL=-
  - 主原因：吸筹窗口 invalid，进入风险阻断观察
  - Next：LIVE_RUN_SYNC
- trollina / Y4vtfnvGSTe2exSm94SXUq3684MGWwWEhXzASkupump
  - Priority：P5_BLOCKED
  - State：BLOCKED
  - Signal：UNKNOWN / UNKNOWN
  - Wallet：未接入 / score=None / risk=None / counterparty=None / data=None
  - Quote/Security：MISSING / MISSING
  - Paper：NONE / PnL=-
  - 主原因：吸筹窗口 invalid，进入风险阻断观察
  - Next：LIVE_RUN_SYNC
- TROLLIEN / ECgweD7xkMj4bm8CcM9rusxKjyQGgdosCvVmhGUupump
  - Priority：P5_BLOCKED
  - State：PAPER_EXITED
  - Signal：S4_强确认信号 / UNKNOWN
  - Wallet：WALLET_BLOCK / score=None / risk=100.0 / counterparty=72.0 / data=100.0
  - Quote/Security：ALLOW_CONFIRMATION_LAYER / READY_FOR_CONFIRMATION
  - Paper：CLOSED / PnL=-
  - 主原因：吸筹窗口 valid + SIKK S3/S4 + 允许纸面交易 + 仓位大于0
  - Next：LIVE_RUN_SYNC

## 5. 当前纸面仓位
- 当前无纸面仓位。

## 6. 未入场原因 Top
- wallet_structure_missing：0
- wallet_block：1
- signal_not_ready：5
- quote_not_ready：4
- security_not_ready：4
- paper_runner_not_called：0
- state_not_ready：5

## 7. 今日纸面验证
- 当前开放仓位：0
- 累计关闭仓位：0
- 已关闭胜率：样本不足
- 已关闭平均收益：样本不足
- 样本可信度：低

## 8. 最新事件
- 事件详见 events/live_events.jsonl
