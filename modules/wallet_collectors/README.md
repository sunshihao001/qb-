# Wallet Collectors 只读采集器 L3 子模块

## 定位

把 GMGN 只读采集适配能力包装成 L3 collectors API。采集器只允许只读采集并写 Raw/Source Wallet packet，不输出交易动作。

## 旧入口

```text
modules/source_wallet_bot/gmgn_live_adapter.py
```

本模块不移动、不删除旧入口，只做 additive L3 wrapper，保证旧 CLI、旧测试、旧调度继续兼容。

## 公共 API

```python
from modules.wallet_collectors import collect_gmgn_token_wallet_rows
```

导出字段：

- `collect_gmgn_token_wallet_rows`
- `gmgn_holder_rows_to_trade_rows`
- `gmgn_holder_rows_to_profile_rows`
- `collect_and_build_source_wallet_packet`

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
