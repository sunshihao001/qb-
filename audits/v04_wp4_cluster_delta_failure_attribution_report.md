# SIKK-SOL v0.4 WP4 审计报告：多轮 OKX 集群快照 delta 与 paper failure attribution

## 目标

完成 v0.4 最后一层：把 OKX 前300集群从“单轮状态”升级为“多轮快照 delta + 纸面失败归因”。

## 新增文件

```text
sikk_okx_cluster_delta.py
tests/test_sikk_okx_cluster_delta.py
```

## 修改文件

```text
sikk_live_run.py
tests/test_sikk_live_run.py
```

## 核心能力

### 1. 多轮快照 delta

`build_okx_cluster_delta(previous_snapshot, current_snapshot)` 会比较两轮 `okx_cluster_decision.json`：

```text
largest_cluster_holding_pct_delta_round
top300_total_holding_pct_delta_round
cluster_total_holding_pct_delta_round
cluster_sync_sell_score_delta_round
okx_cluster_distribution_score_delta_round
okx_cluster_control_retention_score_delta_round
okx_cluster_risk_score_delta_round
```

### 2. 集群风险 flags

当多轮快照出现以下变化时输出风险 flags：

```text
OKX_CLUSTER_STATUS_FLIPPED_FROM_SUPPORT_TO_RISK
LARGEST_CLUSTER_HOLDING_DROPPED_FAST
TOP300_HOLDING_DROPPED_FAST
CLUSTER_SYNC_SELL_SCORE_SPIKED
CLUSTER_DISTRIBUTION_SCORE_SPIKED
CLUSTER_CONTROL_RETENTION_WEAKENED
OKX_CLUSTER_RISK_SCORE_SPIKED
```

### 3. paper failure attribution

新增集群相关失败归因：

```text
CLUSTER_DISTRIBUTION_ACTIVE
COUNTERPARTY_ABSORBING
BAGHOLDER_PRESSURE
CLUSTER_STRUCTURE_WEAKENING
NO_OKX_CLUSTER_FAILURE
```

输出事件写入：

```text
okx_cluster/<token>/okx_cluster_failure_attribution.jsonl
```

事件字段包括：

```text
事件时间
事件类型
代币地址
代币符号
failure_type
failure_reason
okx_cluster_failure_type
previous_okx_cluster_status
current_okx_cluster_status
recommended_paper_action
scope_note
```

### 4. live runtime 接入

`sikk_live_run.py` 现在会只读合并：

```text
okx_cluster/<token>/okx_cluster_decision.json
okx_cluster/okx_cluster_summary.json
okx_cluster/okx_cluster_delta_summary.json
okx_cluster/<token>/okx_cluster_failure_attribution.jsonl
```

当 paper position 为 OPEN：

- `recommended_paper_action=HOLD` → 保持 HOLD。
- `recommended_paper_action=EXIT_MONITOR` → 进入 `EXIT_MONITOR`。
- `recommended_paper_action=FORCE_PAPER_EXIT` → 只触发纸面 `FORCE_PAPER_EXIT`，用于复盘，不真实卖出。

## 安全边界

```text
OKX 集群 delta != 真实卖出
FORCE_PAPER_EXIT 只表示纸面退出/复盘
不签名
不广播
不调用 gmgn_swap
不调用 gmgn_cooking
不绕过 quote/security/signal gates
```

## 指定测试

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_okx_cluster_delta.py tests/test_sikk_live_run.py tests/test_sikk_runtime_v02.py
```

结果：

```text
16 passed in 0.12s
```

## 全量回归

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q
```

结果：

```text
145 passed in 9.75s
```
