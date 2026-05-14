# Corpus Index — DOC-20260513-P01-DATA-FACT-CONTROLLER-002

## Identity
- Title: Phase 01 数据事实层控制器 v1.0
- Canonical file: `/root/sikk-gmgn/docs/stable_trader_os/phases/phase_01_data_fact_controller.md`
- Raw source: `/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260513-P01-DATA-FACT-CONTROLLER-002_phase_01_data_fact_controller_v1.md`

## Key anchors
- Phase定位: 事实地基层，不是分析阶段。
- 禁止项: 不判断吸筹、派发、二段扩张、庄家、买卖点、交易信号。
- 输出目录: `data/stable_trader_os/runs/<run_id>/01_data_fact/`.
- 输出资产: raw / normalized / audit / handoff / `phase_01_data_fact_report.md`.
- 质量门禁: `phase_01_quality_gate.json` with PASS / PASS_WITH_WARNING / PAUSE / BLOCK.
- 交接文件: `phase_01_handoff_to_phase_02.json`.
- 工程任务: mock 数据测试、`tests/test_phase_01_data_fact_controller.py`、缺失/无效地址/重复/时间冲突/金额异常/quality_score/handoff 覆盖。

## Downstream constraints
- P02 can consume only standardized P01 fact outputs.
- Strategy/Paper/Live remain blocked from this document alone.
- Security/quote/transfer missing must be carried as warning/degrade, not invented.
