# Wallet Path Resolver 受控路径解析 L3 子模块

## 定位

把 Source Wallet Bot 里的路径解析能力包装成稳定 L3 API，用于统一 token、passport、field dict、legacy fallback 等路径路由。

## 旧入口

```text
modules/source_wallet_bot/path_resolver.py
```

本模块不移动、不删除旧入口，只做 additive L3 wrapper，保证旧 CLI、旧测试、旧调度继续兼容。

## 公共 API

```python
from modules.wallet_path_resolver import ResolvedWalletPath
```

导出字段：

- `ResolvedWalletPath`
- `resolve_standard_path`
- `resolve_token_index`
- `resolve_passport`
- `resolve_field_dict`
- `resolve_legacy_mapping`
- `resolve_legacy_fallback`
- `resolve_wallet_data_path`
- `consume_runtime_adapter_registry`
- `load_records_with_priority`

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
