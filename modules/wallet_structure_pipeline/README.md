# Wallet Structure Pipeline 候选币钱包结构 Pipeline L3 子模块

## 定位

把候选币钱包结构 pipeline 从根脚本包装成 L3 API，负责从候选 token 到钱包结构门禁产物的只读编排。

## 旧入口

```text
sikk_candidate_wallet_structure_pipeline.py
```

本模块不移动、不删除旧入口，只做 additive L3 wrapper，保证旧 CLI、旧测试、旧调度继续兼容。

## 公共 API

```python
from modules.wallet_structure_pipeline import default_gmgn_wallet_collector
```

导出字段：

- `default_gmgn_wallet_collector`
- `run_candidate_wallet_structure_pipeline`

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
