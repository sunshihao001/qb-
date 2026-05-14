# Module Maturity Governance

## 用途

模块成熟度治理用于 HER / SIKK 底层系统设计，防止把“功能已经能跑”误判成“系统模块已经成熟”。

核心判断：

```text
功能做出来 ≠ 模块成熟
```

## 成熟度等级

```text
L0: missing_or_undetected
L1: functional_code_exists
L2: runtime_integrated
L3: standalone_submodule
```

## L3 标准

一个重要能力只有满足以下条件，才算 L3：

```text
1. 有独立 modules/<capability>/ 目录
2. 有 __init__.py public API
3. 有 README.md
4. 有专用 tests
5. 有 runtime anchor
6. 有 verification
7. 旧入口保留 wrapper 兼容
```

## 路由触发

当任务涉及以下表达时，必须进入 module_maturity_governance：

```text
模块成熟化
功能是不是只是做出来了
有没有形成子模块
哪些能力需要单独目录
L1/L2/L3
子模块优先级
系统能力专业化
```

## 标准流程

```text
目标护照
→ scan_module_maturity
→ 输出 module_maturity_scan.json
→ 输出 module_maturity_priority.md
→ 按 P0/P1/P2 选择 L2→L3 promotion
→ TDD 创建子模块
→ 保留旧入口 wrapper
→ verification
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

## 安全边界

```text
readonly_source_files: true
additive_outputs_only: true
paper_only: true
no_private_key: true
no_signing: true
no_broadcast: true
no_swap: true
```
