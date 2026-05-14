# P01 Data Fact Controller Detection Report

- doc_id: `DOC-20260513-P01-DATA-FACT-001`
- detected_at_utc: `2026-05-13T04:35:02.771501+00:00`
- overall_status: `P01_RUNTIME_NOT_READY`
- result_json: `/root/sikk-gmgn/sikk_stable_trader_os/00_knowledge_intake/intake_reports/p01_data_fact_detection_result_DOC-20260513-P01-DATA-FACT-001.json`

## Counts
- controller: 0/1
- connectors: 0/2
- normalizers: 0/4
- gates: 0/4
- contracts: 0/6
- tests: 0/7
- runtime_dirs: 0/13

## Blocking Issues
- controller_missing_1_of_1
- connectors_missing_2_of_2
- contracts_missing_6_of_6
- tests_missing_7_of_7

## Degraded Issues
- runtime_dirs_incomplete_0_of_13
- possible_raw_or_legacy_direct_read_risk_detected

## Expected Path Status
### controller
- MISSING: `controllers/p01_data_fact_controller.py`
### connectors
- MISSING: `connectors/gmgn_connector.py`
- MISSING: `connectors/okx_connector.py`
### normalizers
- MISSING: `normalizers/p01_token_fact_normalizer.py`
- MISSING: `normalizers/p01_market_fact_normalizer.py`
- MISSING: `normalizers/p01_wallet_fact_normalizer.py`
- MISSING: `normalizers/p01_quote_fact_normalizer.py`
### gates
- MISSING: `gates/p01_data_quality_gate.py`
- MISSING: `gates/p01_freshness_gate.py`
- MISSING: `gates/p01_schema_contract_gate.py`
- MISSING: `gates/p01_cross_source_consistency_gate.py`
### contracts
- MISSING: `contracts/p01/normalized_token_fact.schema.json`
- MISSING: `contracts/p01/normalized_market_fact.schema.json`
- MISSING: `contracts/p01/normalized_wallet_fact.schema.json`
- MISSING: `contracts/p01/normalized_quote_fact.schema.json`
- MISSING: `contracts/p01/data_quality_decision.schema.json`
- MISSING: `contracts/p01/data_fact_handoff_packet.schema.json`
### tests
- MISSING: `tests/p01/test_gmgn_connector.py`
- MISSING: `tests/p01/test_okx_connector.py`
- MISSING: `tests/p01/test_p01_data_fact_controller.py`
- MISSING: `tests/p01/test_p01_normalizers.py`
- MISSING: `tests/p01/test_p01_quality_gate.py`
- MISSING: `tests/p01/test_p01_handoff_packet.py`
- MISSING: `tests/p01/test_p01_replay_fixture.py`
### runtime_dirs
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/phase_identity`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/source_registry`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/connectivity`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/candidate_universe`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/raw/gmgn`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/raw/okx`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/normalized`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/quality`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/handoff`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/replay_fixture`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/audit`
- MISSING: `data/gmgn_candidates_live_run/p01_data_fact/reports`

## Risk Scan Summary
- direct_raw_reads: 10 files
  - `modules/wallet_data_guard/README.md`
    - L57: `path="data/source_wallet_bot/paper/<token>/wallet_data/raw/gmgn.json",`
  - `modules/source_wallet_bot/directory_governance.py`
    - L11: `"gmgn_wallet_rows_raw.json": "wallet_data/raw/gmgn_wallet_rows_raw.json",`
  - `modules/source_wallet_bot/path_resolver.py`
    - L24: `"gmgn_wallet_rows_raw.json": "wallet_data/raw/gmgn_wallet_rows_raw.json",`
  - `tests/test_source_wallet_gmgn_live_adapter.py`
    - L83: `assert (tmp_path / 'wallet_data/raw/gmgn_wallet_rows_raw.json').exists()`
  - `tests/test_wallet_data_guard.py`
    - L61: `raw_path="wallet_data/raw/gmgn_holders.json",`
  - `tests/test_source_wallet_directory_governance.py`
    - L34: `_write(tmp_path / 'wallet_data/raw/gmgn_wallet_rows_raw.json', {'raw': True})`
  - `sikk_stable_trader_os/00_knowledge_intake/system_mapping/system_mapping_DOC-20260513-P01-DATA-FACT-001.json`
    - L8: `"raw/gmgn",`
  - `sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260513-002_p01_data_fact_controller_professional.md`
    - L385: `│   │       ├── token_profile_raw.json`
  - `sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260513-P01-DATA-FACT-001_p01_data_fact_controller_professional_phase_pack.md`
    - L385: `│   │       ├── token_profile_raw.json`
  - `sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260512-002_p02_source_data_fact_controller_v3.md`
    - L411: `token_profile_raw_available: boolean`
- legacy_gmgn_live_run_reads: 15 files
  - `modules/wallet_structure/constants.py`
    - L8: `INTEL_BOT_ROOT = 'data/gmgn_candidates_live_run/intel-bot'`
  - `modules/wallet_structure/implementation_plan.md`
    - L86: `python3 -m json.tool data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token>/wallet_structure_decision.json`
  - `modules/wallet_structure/README.md`
    - L84: `python3 -m modules.wallet_structure.run   --input data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_structure_input.json   --output-dir data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<to`
  - `modules/wallet_structure/module_contract.md`
    - L86: `python3 -m modules.wallet_structure.run   --input data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_structure_input.json   --output-dir data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<to`
  - `modules/wallet_structure/decision_builder.py`
    - L521: `out_dir = Path(output_dir) if output_dir else Path('data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure') / request.get('token_address', 'unknown')`
  - `modules/source_wallet_bot/package_file_passport.json`
    - L4: `"source_archive": "/root/sikk-gmgn/data/gmgn_candidates_live_run/orchestrator/sikk_gmgn_live_run_summary_package.zip",`
  - `modules/source_wallet_bot/kanban_task_board.md`
    - L13: `- 输入：/root/sikk-gmgn/data/gmgn_candidates_live_run/orchestrator/sikk_gmgn_live_run_summary_package.zip`
  - `modules/source_wallet_bot/package_file_passport.md`
    - L5: `- Source archive: `/root/sikk-gmgn/data/gmgn_candidates_live_run/orchestrator/sikk_gmgn_live_run_summary_package.zip``
  - `sikk_stable_trader_os/00_knowledge_intake/raw_inputs/DOC-20260511-021_governance_plane_v2_institutional_design.md`
    - L1009: `- data/gmgn_candidates_live_run/`
  - `sikk_stable_trader_os/00_knowledge_intake/raw_inputs/I02_directory_contract_index_unification_v1_0.md`
    - L164: `/root/sikk-gmgn/data/gmgn_candidates_live_run/`
- direct_okx_quote_security: 51 files
  - `modules/stable_trader_os/phase_01_data_fact/runner.py`
    - L136: `required = [raw_manifest, token_fact_path, token_basic_path, token_market_context_path, wallet_path, trade_path, holder_path, kline_path, quote_path, security_path, wallet_normalized_path, holder_normalized_path, kline_n`
  - `modules/source_wallet_bot/legacy_mapping.md`
    - L38: `- `candidate_quote_security_summary.json``
  - `modules/source_wallet_bot/field_mapping_dictionary.md`
    - L78: `- liquidity_usd: current or snapshot liquidity; source GMGN/OKX/quote/security; required for quote/security; fallback from market snapshot with mark; used by liquidity gate handoff.`
  - `modules/source_wallet_bot/gmgn_okx_readonly_adapter.py`
    - L160: `CollectorCommand("okx", "security_token_scan", ["onchainos", "security", "token-scan", "--tokens", f"501:{token_address}"], False),`
  - `modules/source_wallet_bot/wallet_fact_schema_index.json`
    - L40: `"status": "contract_placeholder_OKX_quote_scan_allowed"`
  - `modules/source_wallet_bot/wallet_fact_output_contract.md`
    - L13: `- L1 OKX quote / scan，只用于 quote/security/liquidity 类`
  - `modules/source_wallet_bot/package_file_passport.json`
    - L82: `"file_path": "quote_security/candidate_quote_security_summary.json",`
  - `modules/source_wallet_bot/phase01_fact_store_router.py`
    - L33: `"description": "GMGN/OKX stage outputs, token quote/security/holder/trader overview.",`
  - `modules/source_wallet_bot/package_file_passport.md`
    - L31: `- `quote_security/candidate_quote_security_summary.json` → **HISTORY_SAMPLE**：历史钱包情报样本，可用于复盘、归档、模式参考，不可反推当前实时事实。`
  - `modules/source_wallet_bot/wallet_fact_builder.py`
    - L309: `"- Class 11 Quote/security: 需要 OKX quote/security scan 补充当前条件背景。",`
- handoff_mentions: 36 files
  - `src/phase_01_data_fact/phase_01_auditor.py`
    - L6: `p.write_text('\n'.join(['# phase_01_data_fact audit','',f'- task: phase_01_data_fact_code_skeleton_landing',f'- phase: phase_01_data_fact',f'- data_quality_status: {result.get("data_quality_status")}',f'- handoff_status:`
  - `src/phase_01_data_fact/phase_01_runner.py`
    - L25: `def run_phase_01(mode,token,chain,raw_input_dir,output_root,shared_handoff_root,snapshot_time=None,legacy_input_dir=None,strict=False):`
  - `src/phase_01_data_fact/handoff_writer.py`
    - L5: `def write_handoff(run_dir, shared_handoff_root, token, chain, snapshot_manifest, token_basic, quality, time_validity):`
  - `modules/stable_trader_os/phase_01_data_fact/runner.py`
    - L40: `shared_handoff_dir = output_dir / "shared_handoff" / str(payload.get("token_address", "missing"))`
  - `modules/stable_trader_os/phase_06_strategy_gate_controller/runner.py`
    - L14: `"phase_01_handoff_packet",`
  - `modules/runtime/phase_runner.py`
    - L181: `shared_handoff = self.root / "shared_handoff" / canonical_phase / token / handoff_name`
  - `modules/runtime/full_system_runner.py`
    - L63: `reusable_handoff = self._shared_handoff_path(phase, token)`
  - `modules/runtime/wave3_p06_p07_runner.py`
    - L134: `("phase_01_handoff_packet", refs.get("phase01_handoff_packet") or refs.get("phase_01_handoff")),`
  - `modules/runtime/full_system_workflow_v4.py`
    - L132: `return self.root / "shared_handoff" / "full_system_workflow_v4"`
  - `modules/runtime/wave1_p01_p03_runner.py`
    - L137: `"phase_01_handoff_packet": artifacts["phase01_handoff"],`
- real_execution_flags: 60 files
  - `src/phase_01_data_fact/phase_01_auditor.py`
    - L6: `p.write_text('\n'.join(['# phase_01_data_fact audit','',f'- task: phase_01_data_fact_code_skeleton_landing',f'- phase: phase_01_data_fact',f'- data_quality_status: {result.get("data_quality_status")}',f'- handoff_status:`
  - `src/phase_01_data_fact/phase_01_runner.py`
    - L37: `write_json(run_dir/'summary'/'phase_01_analysis_scope.json',{'phase':'phase_01_data_fact','scope':'data facts only','forbidden':['wallet_structure_status','WALLET_SUPPORT','CONTROL_RETAINED','SCENARIO_ALLOW','PAPER_READY`
  - `src/phase_01_data_fact/transfer_normalizer.py`
    - L9: `for i,r in enumerate(listify(data)): rows.append({'source_file':'raw_transfer.json','row_id':i,'from_address':get_any(r,['from_address','from']),'to_address':get_any(r,['to_address','to']),'amount_token':get_any(r,['amou`
  - `src/phase_01_data_fact/wallet_trade_normalizer.py`
    - L7: `row={'source_file':'raw_wallet_trade.json','row_id':i,'wallet_address':get_any(r,['wallet_address','address','maker']),'tx_hash':get_any(r,['tx_hash','hash','signature']),'side':get_any(r,['side','type']),'amount_token':`
  - `modules/wallet_data_guard/README.md`
    - L46: `handoff ≠ trade signal`
  - `modules/stable_trader_os/phase_04_scenario_recognition_controller/runner.py`
    - L42: `entries, buy/sell advice, strategy decisions, swaps, signing, or execution.`
  - `modules/stable_trader_os/phase_01_data_fact/validator.py`
    - L8: `"buy_signal",`
  - `modules/stable_trader_os/phase_01_data_fact/runner.py`
    - L20: `deliberately read-only with respect to trading execution: it never signs,`
  - `modules/stable_trader_os/adapters/gmgn_source_wallet_to_phase01.py`
    - L49: `It does not classify wallets, infer scenarios, sign, broadcast, or trade.`
  - `modules/stable_trader_os/phase_09_system_upgrade_controller/runner.py`
    - L396: `"broadcast_allowed": False,`

## P01 Related Files Sample
- `contracts/phase_01_data_fact/README.md`
- `contracts/phase_01_data_fact/handoff_rules.md`
- `contracts/phase_01_data_fact/input_contract.json`
- `contracts/phase_01_data_fact/output_contract.json`
- `contracts/phase_01_data_fact/required_fields.md`
- `contracts/stable_trader_os/phase_01_candidate_intake/index.yaml`
- `contracts/stable_trader_os/phase_01_candidate_intake/input_contract.json`
- `contracts/stable_trader_os/phase_01_candidate_intake/output_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/input_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/output_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_acceptance_matrix.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_forbidden_judgement_contract.md`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_goal_passport.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_input_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_output_contract.json`
- `contracts/stable_trader_os/phase_01_data_fact/phase_01_to_phase_02_contract.json`
- `contracts/stable_trader_os/phase_02_source_data_fact/index.yaml`
- `contracts/stable_trader_os/phase_02_source_data_fact/input_contract.json`
- `contracts/stable_trader_os/phase_02_source_data_fact/output_contract.json`

## Verdict
K00 已完成，但当前仓库未达到 P01 data_fact_controller runtime ready。需要先补齐 controller/connectors/contracts/tests 或迁移现有 Phase01 实现到本次 P01 专业版契约。

## Safety
- paper_runtime_allowed: false
- live_execution_allowed: false
- real_execution_allowed: false