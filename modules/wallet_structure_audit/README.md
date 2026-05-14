# Wallet Structure Audit L3 子模块

## 定位

本模块是钱包结构分析系统的 L3 系统审计层。

它把旧入口：

```text
sikk_wallet_structure_system_audit.py
```

包装为稳定公共 API：

```python
from modules.wallet_structure_audit import audit_wallet_structure_system
```

## 审计范围

每次自动任务或系统完善后，审计层检查：

- canonical route 是否存在。
- runtime artifacts 是否存在。
- auto runner 是否接入 checkpoint / manifest。
- acceptance 是否进入 pipeline manifest。
- wallet data guard 是否有趋势索引。
- safety boundary 是否仍为只读、无签名、无广播、无真实交易。

## 边界

- 只做审计。
- 不采集真实交易数据。
- 不执行交易。
- 不签名。
- 不广播。
- 不读取私钥。
- 不修改旧 runtime 输出。

## 标准输出

- `wallet_structure_system_audit.json`
- `wallet_structure_system_audit.md`

## 兼容策略

当前不移动旧根脚本，L3 模块只做 additive wrapper，保证旧测试、旧 CLI、旧调度入口继续可用。
