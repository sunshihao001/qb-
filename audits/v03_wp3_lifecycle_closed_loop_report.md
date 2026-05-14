# v0.3 WP3 审计报告：主导侧/对手盘生命周期闭环

## 1. 工作包目标

让 `sikk_dominant_lifecycle_classifier.py` 不再只是旁路生命周期分类，而是把主导侧生命周期、主导侧意图、对手盘状态作为证据输入，进入 WP1 的筹码控制权状态机。

## 2. 修改文件

- 修改：`sikk_dominant_lifecycle_classifier.py`
- 修改：`tests/test_sikk_dominant_lifecycle_classifier.py`

## 3. 新增闭环字段

生命周期输出新增：

```text
chip_control_state
chip_control_confidence
chip_control_action
chip_control_reason_codes
chip_control_invalidators
chip_control_evidence_refs
```

中文 CSV/摘要新增：

```text
筹码控制权状态
筹码控制置信度
筹码控制动作
筹码控制原因码
筹码控制失效条件
```

## 4. 闭环规则

- `ACTIVE_DISTRIBUTION` / `FINAL_DISTRIBUTION` / `STRUCTURE_COLLAPSE`：驱动 `CONTROL_LOST_TO_DISTRIBUTION` 或高风险迁移。
- `PARTIAL_DISTRIBUTION` / 高对手盘压力 / 同源同步卖出：驱动 `CONTROL_MIGRATING_TO_COUNTERPARTY`。
- `SECOND_STAGE_PREPARATION` / `REACTIVATION`：只能增强观察或 paper candidate，不直接产生真实交易授权。
- 所有 supportive 输出仍保持 `ALLOW_PAPER_READY_IF_OTHER_GATES_PASS`，必须继续通过 signal/quote/security。

## 5. 测试结果

指定测试：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_dominant_lifecycle_classifier.py tests/test_sikk_chip_control_state_machine.py
```

结果：

```text
9 passed in 0.03s
```

全量测试：

```bash
PYTHONPATH=/root/sikk-gmgn pytest -q
```

结果：

```text
133 passed in 9.63s
```

## 6. 审计结论

WP3 已完成。v0.3 当前已经形成：钱包结构 → 生命周期/对手盘 → 筹码控制权状态机 的闭环。下一步进入 WP4：系统审计、解释、dashboard/paper review 读取 v0.3 输出，并做最终提交。
