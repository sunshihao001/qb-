# Phase 03 Chip Control Controller

## 阶段目标
读取 Phase02 结构地址证据，输出筹码控制、派发、接盘压力、主导侧和筹码迁移状态。

## 上游输入
phase_02_handoff_packet.json、wallet_structure_decision.json、wallet_classification.csv、holder_normalized.csv、token_market_context.json，可选 same_source_groups/distribution_paths/backflow_paths/kline/top_trader/wallet_trade/transfer。

## Atomic Skill
early_wallet_retention_skill、early_wallet_exit_detector_skill、same_source_group_retention_skill、chip_transfer_detector_skill、counterparty_pressure_skill、dominant_side_status_skill、distribution_pressure_skill。

## 输出
chip_control_summary.json、dominant_side_status.json、chip_transfer_status.json、counterparty_pressure.json、phase_03_handoff_packet.json、audit。

## 硬边界
不输出买卖建议，不输出确定庄家；缺失写 missing；上游 WALLET_BLOCK 必须传播硬否决。
