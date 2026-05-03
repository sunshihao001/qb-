# v0.3 WP1 审计报告：独立筹码控制权状态机

## 1. 工作包目标

将 v0.2 中散落在 `sikk_wallet_structure_gate.py` 的 `chip_control_state` 判断抽离为独立模块：

```text
sikk_chip_control_state_machine.py
```

目标不是给出交易授权，而是输出 paper/观察/复盘层可消费的筹码控制状态、置信度、证据、失效条件。

## 2. 修改文件

- 新增：`sikk_chip_control_state_machine.py`
- 新增：`tests/test_sikk_chip_control_state_machine.py`
- 修改：`sikk_wallet_structure_gate.py`

## 3. 新增状态机输出

核心输出字段：

```text
chip_control_state
chip_control_confidence
chip_control_action
chip_control_reason_codes
chip_control_evidence_refs
chip_control_invalidators
missing_fields
evaluated_at
```

状态枚举：

```text
CONTROL_RETAINED_BY_STRUCTURE_SIDE
CONTROL_MIGRATING_TO_COUNTERPARTY
CONTROL_LOST_TO_DISTRIBUTION
CONTROL_UNCLEAR
DATA_QUALITY_FAIL
```

动作边界：

```text
CONTROL_RETAINED_BY_STRUCTURE_SIDE -> ALLOW_PAPER_READY_IF_OTHER_GATES_PASS
CONTROL_MIGRATING_TO_COUNTERPARTY -> PAUSE_OR_EXIT_MONITOR
CONTROL_LOST_TO_DISTRIBUTION -> BLOCK_OR_FORCE_PAPER_EXIT
CONTROL_UNCLEAR -> OBSERVE_ONLY
DATA_QUALITY_FAIL -> OBSERVE_DATA_REPAIR
```

## 4. 接入方式

`evaluate_wallet_structure_gate()` 仍负责钱包结构评分与门禁判断；在生成 `WalletStructureDecision` 前调用：

```python
evaluate_chip_control_state(wallet_decision={...})
```

然后把 `chip_control_state` 回填到原 `WalletStructureDecision`，保持旧调用方兼容。

## 5. 安全边界

- `CONTROL_RETAINED_BY_STRUCTURE_SIDE` 不等于买入。
- `chip_control_action=ALLOW_PAPER_READY_IF_OTHER_GATES_PASS` 明确要求 signal / quote / security 继续通过。
- 模块不导入 swap、cooking、broadcast、交易签名或链上发送能力。
- 只输出状态、证据、失效条件，服务 paper-only 复盘。

## 6. 测试结果

指定测试：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_chip_control_state_machine.py tests/test_sikk_wallet_structure_gate.py
```

结果：

```text
12 passed in 0.03s
```

全量测试：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q
```

结果：

```text
129 passed in 9.50s
```

## 7. 审计结论

WP1 已完成。当前 v0.3 已具备独立筹码控制权状态机，且保持 v0.2 钱包门控兼容。下一步进入 WP2：市值上下文全链路贯穿。
