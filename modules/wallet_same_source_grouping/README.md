# Wallet Same Source Grouping 同源钱包分组 L3 子模块

## 定位

把同源钱包分组能力包装成 L3 API，用于同步买入、同步卖出、相似度、候选组输出。

## 旧入口

```text
sikk_same_source_grouping.py
```

本模块不移动、不删除旧入口，只做 additive L3 wrapper，保证旧 CLI、旧测试、旧调度继续兼容。

## 公共 API

```python
from modules.wallet_same_source_grouping import same_source_similarity_score
```

导出字段：

- `same_source_similarity_score`
- `compute_sync_buy_score`
- `compute_sync_sell_score`
- `build_same_source_groups`
- `write_candidate_groups_csv`

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
