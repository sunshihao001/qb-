---
artifact_type: task_passport
status: active
version: v2.0
task_id: wallet_intel_harness_v2_system_write
generated_at: 2026-05-07T05:40:28Z
---
# Task Passport — Hermes Wallet-Intel Harness V2.0 系统写入

## 1. 原始任务
重建并写入 Hermes Wallet-Intel Harness V2.0 系统体系。

## 2. 真实意图
把钱包数据采集分析、钱包结构分析、旧目录导入、数据语义整合固化为 Hermes/HER Harness 的系统级运行规则，使后续 Wallet-Intel 相关任务能被自动识别、自动路由、按固定工作流执行、验证、恢复，并区分钱包事实、结构证据、行为推断和策略交接。

## 3. 任务类型
- system_design
- harness_control_plane_update
- workflow_module_write
- verification_policy_write

## 4. 本轮范围
只做系统写入：控制面、workflow、模板、验证报告、候选记忆规则。

## 5. 明确不做
- 不扫描旧数据目录
- 不复制旧数据
- 不移动旧目录
- 不删除旧目录
- 不覆盖旧文件
- 不修改业务代码
- 不触发交易
- 不读取或输出私钥、API key、token
- 不执行 git push
- 不声称完成，除非生成系统写入验证报告

## 6. 继承规则
- System First, Model Second
- Prompt 是控制面，不是临时说明
- 钱包数据整合不能按普通目录整理处理
- 语义分层优先于旧目录名分类
- 旧目录只读参考，高价值旧数据 copy-only 导入
- 完成标准是 Hermes 能按 token 理解数据，而不是文件复制完成
- 未验证规则只能写入候选记忆，不能直接写长期记忆

## 7. 输出物
- `01_control_plane/wallet_intel_harness_v2_policy.md`
- `11_workflows/wallet_intel_semantic_integration.workflow.md`
- `05_templates/wallet_intel_data_passport_template.md`
- `05_templates/wallet_intel_import_after_validation_report_template.md`
- `10_audit/wallet_intel_harness_v2_candidate_memory_rules.md`
- `08_reports/project_governance/WALLET_INTEL_HARNESS_V2_SYSTEM_WRITE_REPORT.md`
- `06_verification/project_governance/WALLET_INTEL_HARNESS_V2_SYSTEM_WRITE_VERIFICATION.md`

## 8. 验证方法
独立读取已写入文件，检查：任务路由、语义分层、禁止事项、三层隔离、导入后验证、恢复路径、候选记忆边界是否存在。
