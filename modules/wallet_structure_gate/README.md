# Wallet Structure Gate 钱包结构风险门禁 L3 子模块

## 定位

把旧好差门禁包装成 L3 结构风险门禁 API。该 gate 只能输出结构风险/支持/暂停/阻断状态，不代表交易许可。

## 旧入口

```text
sikk_wallet_structure_gate.py
```

本模块不移动、不删除旧入口，只做 additive L3 wrapper，保证旧 CLI、旧测试、旧调度继续兼容。

## 公共 API

```python
from modules.wallet_structure_gate import WalletStructureDecision
```

导出字段：

- `WalletStructureDecision`
- `evaluate_wallet_structure_gate`
- `evaluate_and_write_wallet_structure`

## HER 边界

- 只作为钱包结构分析系统内的专业子模块。
- 不执行真实交易。
- 不签名。
- 不广播。
- 不读取、写入或输出私钥。
- 不把结构门禁状态解释成买卖许可。
- 下游如需策略判断，必须继续通过 K 线、quote、流动性、安全扫描、风险收益比、时机和策略门禁。

## L3 标准

本目录提供：

- `__init__.py` public API
- `README.md` 模块边界说明
- 既有 dedicated tests 由 maturity scanner 绑定
- 旧入口兼容
