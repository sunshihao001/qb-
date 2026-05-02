# 工作包1审计报告：wallet_structure_decision.json 标准合约 + 钱包门控接入

生成时间: 2026-05-02T23:33Z
项目路径: /root/sikk-gmgn
分支: sikk-paper-audit-20260502

## 修改文件

- `sikk_wallet_structure_gate.py`
- `sikk_wallet_trade_adapter.py`

## 完成内容

- 扩展 `WalletStructureDecision` 标准字段：
  - `data_quality_status`
  - `decision_at`
  - `action_code`
  - `wallet_gate_result`
  - `paper_gate_effect`
  - `risk_level`
  - `reason_codes`
  - `missing_fields`
  - `source_files`
  - `valid_until`
- 增加缺字段检测：空钱包行输出 `MISSING`，关键字段缺失或低质量输出 `DEGRADED`。
- 增加稳定机器原因码 `_reason_codes`：用于审计、状态机和解释引擎后续读取。
- 保留 paper-only 边界：`WALLET_SUPPORT` 的 `paper_gate_effect=REQUIRES_SIGNAL_QUOTE_SECURITY`，不绕过 signal/quote/security。
- `sikk_wallet_trade_adapter.py` 已增强读取新合约字段的兼容性。

## 测试结果

- 指定测试：
  - 命令: `PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_wallet_structure_gate.py tests/test_sikk_wallet_trade_adapter.py`
  - 结果: `17 passed in 0.03s`
- 全量回归：
  - 命令: `PYTHONPATH=/root/sikk-gmgn pytest -q`
  - 结果: `118 passed in 9.48s`

## 审计结论

- 是否执行真实交易: 否。
- 是否触碰 swap/gmgn_cooking/广播: 否。
- 是否保持 paper-only: 是。
- 是否可回滚: 是，当前分支已有基线提交，修改尚未提交，可通过 git diff 审阅。

## 后续建议

- 工作包2的 `sikk_system_audit.py` 应读取本次新增字段，主动检查 `missing_fields`、`data_quality_status`、`paper_gate_effect`。
- 工作包3解释引擎应把 `reason_codes` 转成中文证据链，不重新裁决。
