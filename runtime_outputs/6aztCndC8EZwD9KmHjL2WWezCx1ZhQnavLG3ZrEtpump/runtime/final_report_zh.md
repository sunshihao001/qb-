# 固定 CA 运行报告：- / 6aztCndC8EZwD9KmHjL2WWezCx1ZhQnavLG3ZrEtpump

## 结论

- 状态机：WATCHING
- 系统动作：LIVE_RUN_SYNC
- 交易门控：BLOCK / RISK_MONITOR
- 真实交易：BLOCK_REAL_TRADE；real_trade_enabled=False
- 合约权限：BLOCK_BUY_禁止买入
- 最大实盘仓位：0.0
- 边界：不执行真实 swap，不签名，不广播。

## 主要原因

- 资金状态：资金待查
- 风险等级：HIGH
- 原因码：SECURITY_OR_LIQUIDITY_BLOCK, STRUCTURAL_PAUSE, FUNDING_PENDING
- 缺失证据：资金层跳过, funding_path_missing

## 完成审计

- overall_passed：True
- ca_consistency_passed：True
- safety_boundary_passed：True

