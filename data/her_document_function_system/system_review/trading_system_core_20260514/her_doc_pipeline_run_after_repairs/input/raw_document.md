# HER_DOC Trading System Core Task Issue Package

- package_id: `HER_DOC_TRADING_SYSTEM_CORE_ISSUE_PACKAGE_20260514`
- updated_at: `2026-05-14T09:27:30Z`
- mode: safe-mode / paper-only / no real swap

## Repair Summary
- safe_mode_pipeline: `executed`
- runtime_data_integrity: `RUNTIME_DATA_INTEGRITY_PASS_WITH_GAPS`
- p02_p03_mapping: `P02_P03_MAPPING_READY_WITH_GAPS`
- paper_only_boundary: `PAPER_ONLY_BOUNDARY_ACCEPTANCE_READY`
- remaining_open_issue_ids: `['HER-TS-002']`

## Core Chain
- 真实代币数据
- 阶段化事实采集
- 钱包结构推理
- 筹码结构推理
- 证据与反证控制
- 场景识别
- 策略门禁
- paper-only 风控
- 复盘升级

## Issues

### HER-TS-001 [HIGH]
- 问题: HER-DFAFS 系统自审计显示控制器语义资产完整，但交易系统核心链路还缺少一份把“真实代币数据→复盘升级”逐阶段绑定到具体 runtime 入口、数据文件、证据/反证、验收门槛的统一任务问题清单。
- 影响阶段: 全链路 / HER_DOC_SYSTEM_REVIEW
- 证据:
  - system/her_document_function_system/system_audit/audit_result_auto.json: gap_count=0 仅证明 HER-DFAFS 控制器资产完整
  - data/her_document_function_system/applied_runs/.../f00/implementation_task_package.json: 多个任务仍标记 TASK_REQUIRED_NOT_IMPLEMENTED_EVIDENCE
- 修复任务: 创建 trading_system_core_task_issue_package.json/md，明确问题、证据、影响阶段、修复任务、验收标准。
- 验收标准: 任务包存在且覆盖 9 段核心链路；每个问题含 issue_id、evidence、affected_stage、repair_task、acceptance。
- 状态: FIXED_BY_THIS_RUN

### HER-TS-002 [HIGH]
- 问题: safe-mode HER_DOC 管线已有执行证据，但 F00/V00/H00 仍指出没有生产实现证据或 live/paper runtime 证据闭环，不能声称生产完成。
- 影响阶段: F00/V00/H00/U00
- 证据:
  - data/her_document_function_system/applied_runs/HER_DOC_CLOSURE_TRADING_SYSTEM_20260514_071635/v00/gap_register.json: gap_001 missing_implementation_evidence
  - gap_002 real_tool_execution_limited_to_safe_mode
- 修复任务: 把 safe-mode 执行证据、runtime manifest、paper-only 运行证据纳入 V00 evidence bundle，并保持 READY_WITH_GAPS 与 ACCEPTED 分离。
- 验收标准: V00 evidence bundle 包含命令、输入、输出、退出码、runtime 文件存在性；A00 不把 safe-mode 等同生产 ACCEPTED。
- 状态: OPEN

### HER-TS-003 [HIGH]
- 问题: 核心目标要求真实代币数据阶段化事实采集，但当前审计只确认文件/控制器存在，尚未验证 token_candidates、K线、钱包、quote/security、paper positions 的字段完整性和样本可回放性。
- 影响阶段: 真实代币数据 / P01 数据事实 / P07 paper-only 风控
- 证据:
  - data/gmgn_candidates_live_run/live_run_manifest.json 存在
  - 需要继续验证 gmgn_new_token_filter、candidate_signal_outputs、wallet_structure、quote_security、paper_live 具体输出 schema 与样本
- 修复任务: 增加 runtime_data_integrity_audit.json：逐文件检查存在性、JSON 可读性、关键字段、样本数量、缺字段策略。
- 验收标准: 每个 runtime 阶段有 file_exists/json_ok/key_fields_present/sample_count/status；缺 quote/scan 不得视为安全。
- 状态: FIXED_WITH_GAPS_BY_THIS_RUN
- 修复产物:
  - runtime_data_integrity_audit.json
  - runtime_data_integrity_audit.md

### HER-TS-004 [MEDIUM]
- 问题: 钱包结构推理与筹码结构推理已有阶段控制器，但还需证明 runtime 输出与 P02/P03 的证据字段、反证字段、同源/成本区/派发进度字段一一映射。
- 影响阶段: P02 钱包结构 / P03 筹码控制
- 证据:
  - sikk_stable_trader_os/02_phase_controllers/P02_wallet_structure/phase_manifest.yaml 存在
  - P03_chip_control/phase_manifest.yaml 存在
  - data/gmgn_candidates_live_run/wallet_structure/ 输出需要字段级验收
- 修复任务: 创建 P02/P03 runtime-field mapping 与反证字段清单；缺失字段进入 H00 downstream queue。
- 验收标准: wallet_structure summary 中每个结论有 evidence_level、counter_evidence、dominant_side/cost/distribution 字段或明确 missing/degraded。
- 状态: FIXED_WITH_GAPS_BY_THIS_RUN
- 修复产物:
  - p02_p03_runtime_field_mapping.json
  - p02_p03_runtime_field_mapping.md

### HER-TS-005 [MEDIUM]
- 问题: 策略门禁、paper-only 风控、复盘升级之间还需要显式禁止“paper ready=实盘授权”的治理规则与验收检查。
- 影响阶段: P06/P07/P08/P09/G00/A00
- 证据:
  - SIKK skill 与 live manifest 均强调 OBSERVE_PAPER_ONLY
  - 需要把该边界纳入 G00/A00 可验证规则
- 修复任务: 补充 paper-only boundary acceptance：禁止 swap/sign/broadcast/private-key；PAPER_READY 仅进入 paper runner；复盘只生成升级候选不直接改实时规则。
- 验收标准: A00 检查项包含 no_real_swap/no_private_key/no_signature/no_broadcast/review_no_direct_rule_mutation。
- 状态: FIXED_BY_THIS_RUN
- 修复产物:
  - paper_only_boundary_acceptance.json
  - paper_only_boundary_acceptance.md
