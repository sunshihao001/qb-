# Module Maturity Governance

模块成熟度治理小模块，用于 HER / SIKK 底层系统设计。

## 核心认知

```text
功能做出来 ≠ 模块成熟
```

重要能力需要从 scattered functional code 升级成 named submodule。

## 成熟度等级

```text
L0: missing_or_undetected
L1: functional_code_exists
L2: runtime_integrated
L3: standalone_submodule
```

## L3 Promotion Gate

```text
standalone module directory
__init__.py public API
README.md
专用 tests
运行锚点
verification
backward-compatible wrappers
```

## Public API

```python
from modules.module_maturity_governance import (
    scan_module_maturity,
    evaluate_capability_maturity,
    build_maturity_design_contract,
    write_maturity_design_contract,
)
```

## 用途

- 扫描哪些能力只是 L1/L2。
- 按 P0/P1/P2 排列模块化补全优先级。
- 生成 module_maturity_design_contract，可被 HER 底层逻辑系统设计引用。
- 防止“功能能跑”被误判成“系统模块完成”。

## 安全边界

```text
readonly_source_files: true
additive_outputs_only: true
paper_only: true
no_private_key/signing/broadcast/swap
```
