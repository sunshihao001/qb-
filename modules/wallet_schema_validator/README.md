# Wallet Schema Validator 钱包结构 schema/contract 校验 L3 子模块

## 定位

把 Source Wallet Bot 的 schema/contract 校验能力包装成稳定 L3 API，作为 Raw/Normalized/Wallet-Fact 进入下游前的门禁。

## 旧入口

```text
modules/source_wallet_bot/schema_validator.py
```

本模块不移动、不删除旧入口，只做 additive L3 wrapper，保证旧 CLI、旧测试、旧调度继续兼容。

## 公共 API

```python
from modules.wallet_schema_validator import validate_required_keys
```

导出字段：

- `validate_required_keys`
- `assert_no_forbidden_fields`
- `validate_json_file`
- `validate_source_wallet_design_package`
- `validate_handoff_packet`
- `consume_schema_contract_runtime_adapters`
- `validate_runtime_adapter_registry`

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
