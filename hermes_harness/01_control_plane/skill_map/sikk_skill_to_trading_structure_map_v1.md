# SIKK Skill 能力地图与交易结构阶段映射 V1

本文件是 HER/Harness 控制面索引，机器可读数据以 research_loop/state/sikk_skill_to_trading_structure_map_v1/*.json 为准。

## 状态枚举

- EXCLUDE
- RECORD
- RISK_MONITOR
- WATCHING
- PAPER_READY
- HUMAN_CONFIRM_REQUIRED

## 边界

`PAPER_READY` 只表示纸面候选准备，不表示真实交易许可。真实执行、签名、广播、私钥读取全部禁止。

## 阶段

- `S0_SYSTEM_BASELINE`：系统基线与安全边界 → skills: hermes_harness_control
- `S1_CANDIDATE_DISCOVERY`：候选发现 → skills: source_wallet_bot
- `S2_RAW_INTAKE`：Raw 只读接入 → skills: source_wallet_bot
- `S3_NORMALIZATION`：字段标准化 → skills: source_wallet_bot
- `S4_DATA_QUALITY_POLLUTION`：质量与污染门禁 → skills: wallet_data_guard
- `S5_WALLET_FACT_LAYER`：钱包事实层 → skills: wallet_structure_l3_professionalization
- `S6_STRUCTURE_RELATION`：结构关系层 → skills: same_source_grouping, chip_control
- `S7_BEHAVIOR_INFERENCE`：行为推断层 → skills: chip_control
- `S8_STRUCTURE_GATE`：结构门禁交接 → skills: wallet_structure_l3_professionalization
- `S9_MARKET_CONTEXT`：市值/K线/流动性上下文 → skills: quote_security_pipeline, time_context_gate
- `S10_SECURITY_RISK`：安全风险扫描 → skills: quote_security_pipeline
- `S11_STRATEGY_HANDOFF`：策略交接状态 → skills: candidate_state_machine
- `S12_PAPER_VERIFICATION`：纸面验证 → skills: paper_live_runner
- `S13_REVIEW_AUDIT`：复盘审计 → skills: hermes_harness_control
- `S14_AUTO_GAP_DISCOVERY`：自动缺口发现 → skills: hermes_harness_control
- `S15_MEMORY_SKILL_FEEDBACK`：memory/skill 沉淀 → skills: hermes_harness_control