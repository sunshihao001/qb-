# SIKK 大系统 GitHub 备份分级目录说明

> 目的：把当前大型交易系统/HER 方法体系/控制面/领域平面/钱包分析项目整体备份到 GitHub，同时避免继续在同一个运行主线里扩大设计，降低认知冲突、目录冲突、字段冲突、执行优先级冲突。

## 当前备份定位

- 备份对象：`/root/sikk-gmgn/` 当前大型系统体系。
- 备份用途：归档、审计、回溯、未来拆分参考。
- 当前运行主线：个人版轻量系统优先，不在此备份任务中继续扩展大型 Control Plane。
- 真实交易：不启用；不上传私钥；不上传本地 `.env`；不上传大体量生成报告。

## 分级目录

### L0 根目录：主系统入口与历史脚本

包含：
- `sikk_*.py`
- `run_sikk_gmgn_pipeline.py`
- `sikkctl.py`
- `README.md`
- `SIKK_*` 系统状态/审计/计划文档

定位：历史主系统、交易/回放/候选分析脚本集合。

### L1 个人轻量运行层

包含：
- `sikk/`
- `scripts/run_single_token_analysis.py`

定位：当前优先恢复的个人版单 token 结构分析与 paper-only 验证闭环。

阶段压缩：
- S01 数据读取与事实面板：覆盖旧 P01/P02
- S02 钱包结构 + 筹码结构判断：覆盖旧 P03/P04
- S03 证据/反证 + 场景识别：覆盖旧 P05/P06
- S04 策略门禁 + paper-only 决策：覆盖旧 P07/P08
- S05 复盘归因 + 规则升级候选：覆盖旧 P09/P10

### L2 旧钱包分析核心模块

包含：
- `modules/source_wallet_bot/`
- `modules/wallet_structure/`
- `modules/wallet_structure_*`
- `modules/wallet_collectors/`
- `modules/wallet_data_guard/`
- `standard_wallet_data/`
- 相关 `sikk_wallet_structure_*.py`

定位：旧钱包结构采集/分析项目，不删除，作为主系统核心模块保留。

### L3 阶段/合约/schema 体系

包含：
- `contracts/`
- `schemas/`
- `docs/01_stage_definitions/`
- `docs/02_phase_layer_step_maps/`
- `docs/03_handoff_flow/`
- `docs/08_schema_index/`
- `docs/09_her_execution_protocol/`

定位：P01-P10、handoff、contract、schema、阶段定义的历史设计备份。当前冻结，不继续扩展。

### L4 HER/Control Plane/方法轮体系

包含：
- `hermes_harness/`
- `system/full_control_plane/`
- `system/her_doc/`
- `system/her_document_function_system/`
- `system/knowledge_processing_program/`
- `system/phase_controllers/`
- `system/trace_plane/`
- `system/unified_standardization/`
- `sikk_stable_trader_os/00_control/`
- `sikk_stable_trader_os/00_methodology/`
- `sikk_stable_trader_os/00_domain/`
- `sikk_stable_trader_os/02_phase_controllers/`
- `sikk_stable_trader_os/06_phase_controllers/`

定位：大型系统治理、HER_DOC、方法轮、控制面、领域平面、知识处理程序、阶段控制器。当前只备份，不作为短期运行主线。

### L5 数据/运行/审计产物

包含部分轻量文本状态、manifest、审计结果；默认排除大体量运行输出：
- `reports/` 默认忽略
- `research_loop/` 默认忽略
- `knowledge/` 默认忽略
- `ai_context/` 默认忽略
- `logs/` 默认忽略
- `__pycache__/` 默认忽略

定位：GitHub 只保留必要结构、规则、代码、轻量示例；大体量 runtime/report 另行本地或 release artifact 备份。

## 冲突隔离原则

1. 大型 HER 体系只作为备份/归档，不继续驱动当前个人版运行。
2. 个人版运行只读必要事实数据，不反向污染旧 reports。
3. 钱包分析继续作为主系统核心模块，不再独立扩成新总控系统。
4. P01-P10 保留为历史阶段解释；运行时压缩成 S01-S05。
5. 所有真实交易相关能力默认关闭，paper-only 优先。

## GitHub 备份策略

- 使用单独备份分支：`backup/full-system-YYYYMMDD-HHMMSS`
- 提交内容：代码、方法论、控制面、领域平面、schema/contract/docs、轻量配置。
- 排除内容：密钥、环境变量、大体量报告、cache、日志、私钥、压缩包。
- 如果需要完整 runtime 数据，另建 release artifact 或本地 tar，不混入主分支源码树。
