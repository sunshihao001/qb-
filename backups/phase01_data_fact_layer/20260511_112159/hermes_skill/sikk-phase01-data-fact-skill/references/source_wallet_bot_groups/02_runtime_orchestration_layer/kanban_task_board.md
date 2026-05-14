# SIKK Source Wallet Intelligence Bot Build

## Board columns
- TODO
- IN_PROGRESS
- BLOCKED
- DONE
- VERIFY

## Round cards
### round_0_import_safety — DONE
- 目标：安全导入 legacy 压缩包，生成 sha256 与文件清单，不碰正式 runtime。
- 输入：/root/sikk-gmgn/data/gmgn_candidates_live_run/orchestrator/sikk_gmgn_live_run_summary_package.zip
- 输出文件：imports/staging/<package_id>/package.sha256, imports/staging/<package_id>/package_file_list.txt
- 阻塞处理：缺包则写 blocker_report.txt；不停止后续规划。
- 验收标准：staging 导入存在，未触碰正式 runtime 目录。
- checkpoint：research_loop/checkpoints/round_0_import_safety.md
- 下一轮动作：round_1_package_passport

### round_1_package_passport — DONE
- 目标：给旧包做文件护照，区分历史样本、复盘审计、非事实源。
- 输入：imports/staging/<package_id>/package_file_list.txt
- 输出文件：modules/source_wallet_bot/package_file_passport.json, modules/source_wallet_bot/package_file_passport.md
- 阻塞处理：文件清单缺失则写 blocker_report.txt。
- 验收标准：文件护照存在且完成分类。
- checkpoint：research_loop/checkpoints/round_1_package_passport.md
- 下一轮动作：round_2_source_registry

### round_2_source_registry — DONE
- 目标：审计旧系统脚本、输出、review plan、wallet_structure 资产并映射到新 Bot。
- 输入：sikk_gmgn_token_report.py, sikk_candidate_wallet_structure_pipeline.py, 旧输出 CSV/MD/manifest
- 输出文件：modules/source_wallet_bot/legacy_mapping.md, modules/source_wallet_bot/old_system_inventory.json, modules/source_wallet_bot/codebase_inspection_report.md
- 阻塞处理：脚本缺失则做部分清单并写 blocker_report。
- 验收标准：完成旧系统能力与资产映射。
- checkpoint：research_loop/checkpoints/round_2_old_system_audit.md
- 下一轮动作：round_3_field_mapping

### round_3_field_mapping — DONE
- 目标：定义字段字典与 source manifest 合约。
- 输入：旧系统输出形态, legacy mapping
- 输出文件：modules/source_wallet_bot/field_mapping_dictionary.md, modules/source_wallet_bot/source_manifest_contract.md
- 阻塞处理：字段缺失时记录 blocker_report，不编造。
- 验收标准：字段名、来源、时间含义、fallback、用途完整。
- checkpoint：research_loop/checkpoints/round_3_field_mapping.md
- 下一轮动作：round_4_wallet_contracts

### round_4_wallet_contracts — DONE
- 目标：定义 wallet profile / trade / transfer / funding / backflow / decision 合约。
- 输入：field_mapping_dictionary.md
- 输出文件：modules/source_wallet_bot/wallet_intelligence_contracts.md
- 阻塞处理：缺字段则在合约中标记 missing / fallback / forbidden sources。
- 验收标准：钱包情报合约完整且不含交易判断。
- checkpoint：research_loop/checkpoints/round_4_wallet_contracts.md
- 下一轮动作：round_5_source_and_group_models

### round_5_source_and_group_models — DONE
- 目标：定义同源执行组证据、候选组键与 group 边界。
- 输入：wallet_intelligence_contracts.md
- 输出文件：modules/source_wallet_bot/source_and_group_models.md
- 阻塞处理：无法最终裁决时保留 candidate_group_key 与 evidence_level。
- 验收标准：同源证据模型与边界明确。
- checkpoint：research_loop/checkpoints/round_5_source_and_group_models.md
- 下一轮动作：round_6_distribution_recovery_whale

### round_6_distribution_recovery_whale — DONE
- 目标：定义分发 / 派发 / 回流 / 接盘鲸鱼 / 核心资金源候选规则。
- 输入：source_and_group_models.md
- 输出文件：modules/source_wallet_bot/distribution_recovery_whale_rules.md
- 阻塞处理：证据不足时输出候选，不输出确定性结论。
- 验收标准：角色语言保持证据化与可追溯。
- checkpoint：research_loop/checkpoints/round_6_distribution_recovery_whale.md
- 下一轮动作：round_7_evidence_note_rules

### round_7_evidence_note_rules — DONE
- 目标：定义 GMGN 备注、watchlist 与禁止语句。
- 输入：distribution_recovery_whale_rules.md
- 输出文件：modules/source_wallet_bot/evidence_note_rules.md
- 阻塞处理：禁止出现绝对化控筹语句。
- 验收标准：可用于 Telegram / GMGN 的中文证据语言已定义。
- checkpoint：research_loop/checkpoints/round_7_evidence_note_rules.md
- 下一轮动作：round_8_handoff_contract

### round_8_handoff_contract — DONE
- 目标：定义 Bot1 → Bot2 交接包结构。
- 输入：wallet_intelligence_summary, same-source evidence, GMGN notes
- 输出文件：modules/source_wallet_bot/bot2_handoff_contract.md
- 阻塞处理：缺失字段以 missing_fields 与 blocker_notes 方式交接。
- 验收标准：交接包明确不包含最终控筹结论。
- checkpoint：research_loop/checkpoints/round_8_handoff_contract.md
- 下一轮动作：round_9_final_module_package

### round_9_final_module_package — DONE
- 目标：汇总最终模块包、边界与验收说明。
- 输入：前述文档与 schema plan
- 输出文件：modules/source_wallet_bot/final_module_package.md
- 阻塞处理：若验收未过则保留 blocker_report 以便迭代。
- 验收标准：模块包可用于后续实现。
- checkpoint：research_loop/checkpoints/round_9_final_module_package.md
- 下一轮动作：final_acceptance

### final_acceptance — DONE
- 目标：验证文件、边界与导入/审计产物均已就位。
- 输入：全部文档、护照、审计报告、checkpoint
- 输出文件：research_loop/checkpoints/final_acceptance.md
- 阻塞处理：若任一验收失败，进入 blocker_report。
- 验收标准：验证通过，且不碰状态机 / paper runner / 实盘。
- checkpoint：research_loop/checkpoints/final_acceptance.md
- 下一轮动作：进入实现阶段或 Bot2 对接

## Current status
- round_0: DONE
- round_1: DONE
- round_2: DONE
- round_3: DONE
- round_4: DONE
- round_5: DONE
- round_6: DONE
- round_7: DONE
- round_8: DONE
- round_9: DONE
- final_acceptance: DONE
