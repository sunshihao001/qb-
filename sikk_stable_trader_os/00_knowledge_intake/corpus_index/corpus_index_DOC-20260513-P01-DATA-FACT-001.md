# Corpus Index｜DOC-20260513-P01-DATA-FACT-001

## Sections
- h1: P01 数据事实层专业版阶段包
- h2: `P01_data_fact_controller`｜GMGN / OKX 数据源接入与事实层总控
- h1: 0. 阶段总定位
- h2: P01 的本质定义
- h1: 1. P01 阶段核心结论
- h1: 2. P01 阶段身份文件
- h2: 2.1 `phase_01_data_fact_controller.yaml`
- h2: 2.2 `phase_01_data_fact_controller.md`
- h1: P01 数据事实层｜阶段上下文压缩包
- h1: 3. P01 专业化设计原则
- h2: 3.1 事实源优先原则
- h2: 3.2 Raw-first 原则
- h2: 3.3 缺失状态化原则
- h2: 3.4 Fail-closed 原则
- h2: 3.5 下游隔离原则
- h2: 3.6 可复盘原则
- h1: 4. P01 总目录结构
- h1: 5. P01 子阶段总表
- h1: 6. 数据源职责定义
- h2: 6.1 GMGN 职责
- h2: 6.2 OKX 职责
- h1: 7. Source Capability Matrix
- h1: 8. P01 核心数据模型
- h2: 8.1 Token Fact
- h2: 8.2 Market Fact
- h2: 8.3 Wallet Fact
- h2: 8.4 Quote Fact
- h1: 9. 数据质量门设计
- h2: 9.1 质量评分维度
- h2: 9.2 质量状态
- h2: 9.3 状态含义
- h2: 9.4 示例
- h1: 10. Downstream Handoff Packet
- h1: 11. P01 失败分类体系
- h2: 11.1 数据源失败
- h2: 11.2 数据字段失败
- h2: 11.3 下游权限失败
- h1: 12. P01 运行链路
- h1: 13. P01 模块文件设计
- h2: 13.1 控制器
- h2: 13.2 Connectors
- h2: 13.3 Normalizers
- h2: 13.4 Gates
- h2: 13.5 Contracts
- h2: 13.6 Tests
- h1: 14. P01 验收标准
- h2: 14.1 第一层验收：阶段结构成立
- h2: 14.2 第二层验收：数据源成立
- h2: 14.3 第三层验收：标准化成立
- h2: 14.4 第四层验收：质量门成立
- h2: 14.5 第五层验收：下游交接成立
- h1: 15. P01 运行命令设计
- h1: 16. P01 专业化差距审计表
- h1: 17. HER 可复制执行任务书
- h1: 18. P01 完成后的系统状态
- h1: 19. 不应继续做的事情
- h1: 20. 本次认知升级点
- h1: 21. 尚未解决问题

## Key Terms / Anchors
- `P01_data_fact_controller`
- `GMGN`
- `OKX`
- `raw snapshot`
- `data_fact_handoff_packet.json`
- `DATA_READY`
- `DATA_PARTIAL_READY`
- `DATA_PAUSE`
- `DATA_BLOCK`
- `DATA_SCHEMA_REVIEW`
- `DATA_REPLAY_ONLY`
- `field_provenance`
- `freshness`
- `source_capability_matrix.json`
- `real_execution false`

## Important Claims
- P01 未成立时不应继续推进策略、paper runner、dashboard、解释模块或真实交易门禁。
- P01 的下游唯一可信入口是 `data_fact_handoff_packet.json`。
- 所有外部数据必须 raw-first；缺失必须状态化；关键事实缺失默认阻断。
- GMGN 是 Token + Wallet + Chip + Behavior Fact Source；OKX 是 Quote + Liquidity + Execution Feasibility + Safety Cross-check Source.

## Dependencies
- K00 intake acceptance must precede P01 package/code landing.
- P01 handoff acceptance must precede P02/P03/P06 consumption.
- Connector availability and replay fixtures are required before live/paper runtime claims.
