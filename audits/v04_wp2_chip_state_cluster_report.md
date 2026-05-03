# SIKK-SOL v0.4 WP2 审计报告：OKX 集群状态接入筹码控制权状态机

## 目标

把 WP1 生成的 `okx_cluster_decision.json` 作为 v0.3 `sikk_chip_control_state_machine.py` 的新增证据输入。

## 修改文件

```text
sikk_chip_control_state_machine.py
tests/test_sikk_chip_control_state_machine.py
```

## 接入方式

`evaluate_chip_control_state()` 新增参数：

```python
okx_cluster_decision: Mapping[str, Any] | None = None
```

缺 OKX 集群数据时：

```text
missing_fields += okx_cluster_decision
refs += okx_cluster_decision_missing
```

不阻断主流程，不把缺 OKX 数据当成交易风险。

## 状态影响规则

### 支持类

```text
CLUSTER_SUPPORT
CLUSTER_CONTROL_HOLDING
CLUSTER_SECOND_STAGE_SUPPORT
```

影响：

```text
增强 CONTROL_RETAINED_BY_STRUCTURE_SIDE 的证据与置信度
输出 OKX_CLUSTER_<status> reason_code
仍只允许 ALLOW_PAPER_READY_IF_OTHER_GATES_PASS
不得绕过 signal/quote/security gates
```

### 派发风险类

```text
CLUSTER_DISTRIBUTION_RISK
okx_cluster_distribution_score >= 75
cluster_sync_sell_score >= 70
largest_cluster_holding_pct_delta <= -10
```

影响：

```text
CONTROL_LOST_TO_DISTRIBUTION
BLOCK_OR_FORCE_PAPER_EXIT
risk_level=HIGH
```

### 对手盘/套牢压力类

```text
CLUSTER_COUNTERPARTY_ABSORBING
CLUSTER_BAGHOLDER_PRESSURE
okx_cluster_risk_score >= 70
```

影响：

```text
CONTROL_MIGRATING_TO_COUNTERPARTY
PAUSE_OR_EXIT_MONITOR
```

## 安全边界

- OKX 集群支持不等于买入。
- OKX 集群风险不等于真实卖出。
- 所有输出仍为 paper/观察/复盘状态。
- `ALLOW_PAPER_READY_IF_OTHER_GATES_PASS` 仍要求其他 gates 通过。

## 测试结果

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_chip_control_state_machine.py tests/test_sikk_okx_cluster_holding_analyzer.py
```

结果：

```text
12 passed in 0.04s
```
