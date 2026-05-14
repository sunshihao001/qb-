# Wallet Structure Governance

独立钱包结构治理子模块。

## 定位

本模块不直接做交易、不直接做钱包角色判断，而是治理钱包结构分析系统自身：

```text
scan -> task package/apply -> runtime adapters -> registry -> integration -> consumption
```

## Public API

```python
from modules.wallet_structure_governance import (
    scan_wallet_structure_system_gaps,
    apply_gap_action,
    build_runtime_adapter_registry,
    integrate_runtime_adapters,
    consume_runtime_registry,
    run_governance_cycle,
)
```

## 一键周期

```python
from modules.wallet_structure_governance import run_governance_cycle

run_governance_cycle(
    project_root='/root/sikk-gmgn',
    output_root='/root/sikk-gmgn/research_loop/state/<task_id>',
    max_priority='P2',
)
```

## 安全边界

```text
readonly_source_files: true
additive_outputs_only: true
paper_only: true
no_private_key/signing/broadcast/swap
```
