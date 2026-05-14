# Wallet Chip Control 筹码控制状态机 L3 子模块

## 定位

把筹码控制状态机包装成 L3 API，用于结构库存、派发进度、成本区、对手盘压力等事实后的状态判断。

## 旧入口

```text
sikk_chip_control_state_machine.py
```

本模块不移动、不删除旧入口，只做 additive L3 wrapper，保证旧 CLI、旧测试、旧调度继续兼容。

## 公共 API

```python
from modules.wallet_chip_control import ChipControlDecision
```

导出字段：

- `ChipControlDecision`
- `evaluate_chip_control_state`

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
