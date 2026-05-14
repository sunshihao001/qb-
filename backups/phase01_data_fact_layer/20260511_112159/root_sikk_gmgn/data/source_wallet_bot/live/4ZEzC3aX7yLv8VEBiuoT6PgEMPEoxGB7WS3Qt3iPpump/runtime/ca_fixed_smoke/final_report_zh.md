# 固定 CA 运行报告：AGI / 4ZEzC3aX7yLv8VEBiuoT6PgEMPEoxGB7WS3Qt3iPpump

## 结论

- 状态机：WATCHING
- 系统动作：STRUCTURE_OBSERVE
- 交易门控：OBSERVE_ONLY / OBSERVE
- 真实交易：BLOCK_REAL_TRADE；real_trade_enabled=False
- 合约权限：PAUSE_NEED_CONFIRM_需要人工确认
- 最大实盘仓位：0.0
- 边界：不执行真实 swap，不签名，不广播。

## 主要原因

- 资金状态：资金待查
- 风险等级：MEDIUM_HIGH
- 原因码：STRUCTURAL_PAUSE, FUNDING_PENDING
- 缺失证据：资金层跳过, funding_path_missing

## 完成审计

- overall_passed：True
- ca_consistency_passed：True
- safety_boundary_passed：True

