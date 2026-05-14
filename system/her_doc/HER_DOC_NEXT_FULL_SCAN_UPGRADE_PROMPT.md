# HER_DOC Evidence-Level Full System Scan Prompt

Use this prompt only after the HER_DOC project constitution, protocol, schemas, skill, and validator exist and pass project validation.

```text
任务名称：
HER_DOC Evidence-Level Full Trading System Scan

加载：
必须加载 `her-doc` skill。
必须读取 `/root/sikk-gmgn/system/her_doc/HER_DOC_PROJECT_CONSTITUTION.md`。
必须读取 `/root/sikk-gmgn/system/her_doc/HER_DOC_EXECUTION_PROTOCOL.md`。
必须读取 `/root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR_SPEC.md`。

前置验收门禁：
必须先运行：
python /root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR.py project
只有 status=PASS 且 issue_count=0 才能开始 full trading system deep scan。
否则停止，输出 BLOCKED_VALIDATOR_PROJECT_GATE，不得继续扫描业务系统。

执行级别：
evidence-level，不是 artifact-level。
不得只生成报告、不得只检查文件存在、不得只做关键词覆盖。

执行顺序：
HER_DOC-PRE Validator Project Gate
→ HER_DOC-00
→ HER_DOC-01
→ HER_DOC-02
→ HER_DOC-03
→ HER_DOC-04
→ HER_DOC-05
→ HER_DOC-06
→ HER_DOC-07
→ HER_DOC-POST Validator Bundle Gate

不得跳步，不得先写最终报告。

强制规则：
没有 evidence_path 不得声明 PRESENT。
没有 proof_method 不得声明 READY。
没有 R00 safe dry-run/import/binding proof 不得声明 R00_READY。
没有 P09 replay proof 不得声明 REVIEW_READY。
没有 P10 governance proof 不得声明 UPGRADE_READY。
旧脚本/旧数据/旧报告/旧 GPT 研究必须进入 legacy absorption 矩阵，不能只在报告中提到。
validator project gate 未 PASS，不得开始 deep scan。
validator bundle gate 未 PASS，不得声明 full scan completed。

允许：
read-only scan、file read、YAML/JSON parse、static scan、import check、schema validation、dry-run、paper-only inert fixture、replay-only。

禁止：
真实交易、wallet signing、private key、broadcast、auto order、auto deploy、生产策略激活。

输出目录：
/root/sikk-gmgn/reports/her_doc_full_system_gap_scan/

必须输出：
1. document_passport_matrix.yaml
2. functional_object_registry.yaml
3. system_mapping_matrix.yaml
4. phase_file_evidence_matrix.yaml
5. evidence_coverage_report.yaml
6. runtime_binding_verification_matrix.yaml
7. legacy_script_absorption_matrix.yaml
8. legacy_data_replay_matrix.yaml
9. legacy_research_assetization_matrix.yaml
10. total_goal_gap_matrix.yaml
11. phase_goal_gap_matrix.yaml
12. method_loop_gap_matrix.yaml
13. gpt_research_queue.yaml
14. her_build_queue.yaml
15. r00_runtime_blocker_matrix.yaml
16. full_trading_system_gap_scan_report.md
17. next_research_batch_prompt.md
18. next_her_build_task_packet.md
19. validator_project_gate_result.json
20. validator_bundle_gate_result.json

后置验收门禁：
写完输出包后，必须运行：
python /root/sikk-gmgn/system/her_doc/HER_DOC_VALIDATOR.py bundle /root/sikk-gmgn/reports/her_doc_full_system_gap_scan/
并把结果写入：
/root/sikk-gmgn/reports/her_doc_full_system_gap_scan/validator_bundle_gate_result.json

验收：
如果 validator project gate 未 PASS：BLOCKED_VALIDATOR_PROJECT_GATE。
如果 validator bundle gate 未 PASS：BLOCKED_VALIDATOR_BUNDLE_GATE 或 HER_DOC_SCAN_OUTPUT_INCOMPLETE。
如果 evidence coverage < 80%，即使 bundle gate PASS，也不得声明 full scan completed；只能声明 `HER_DOC_ASSET_SCAN_COMPLETED_WITH_DEEP_SCAN_GAPS` 或更低。
最终报告必须列出 claims_not_made。
```
