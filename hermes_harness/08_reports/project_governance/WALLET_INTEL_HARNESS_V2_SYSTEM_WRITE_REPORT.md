# Hermes Wallet-Intel Harness V2.0 系统写入报告

- 任务 ID：wallet_intel_harness_v2_system_write
- 生成时间：2026-05-07T05:40:28Z
- 范围：只做系统写入，不做实际数据迁移

## 1. 写入目标
将钱包数据采集分析、钱包结构分析、旧目录导入、数据语义整合写入 Hermes/HER Harness 系统体系，使后续 Wallet-Intel 任务可以：

- 自动识别
- 自动路由
- 按固定 workflow 执行
- 自动验证
- 自动恢复
- 区分钱包事实、结构证据、行为推断、结论判断和策略交接

## 2. 已写入系统资产

### 控制面
- `01_control_plane/wallet_intel_harness_v2_policy.md`

作用：定义 Wallet-Intel Harness V2.0 的路由、语义分层、旧目录治理、导入后验证、恢复与候选记忆规则。

### Workflow
- `11_workflows/wallet_intel_semantic_integration.workflow.md`

作用：定义 Wallet-Intel 语义整合任务的适用条件、输入契约、允许工具、禁止事项、执行阶段、输出物、验证标准和失败处理。

### 模板
- `05_templates/wallet_intel_data_passport_template.md`
- `05_templates/wallet_intel_import_after_validation_report_template.md`
- `05_templates/wallet_intel_legacy_path_map_template.md`

作用：提供数据护照、旧路径映射和导入后理解验证报告的标准格式。

### 候选记忆
- `10_audit/wallet_intel_harness_v2_candidate_memory_rules.md`

作用：只记录候选长期规则，不直接写入长期记忆。

### 验证报告
- `06_verification/project_governance/WALLET_INTEL_HARNESS_V2_SYSTEM_WRITE_VERIFICATION.md`

作用：独立检查本次系统写入是否具备必备锚点。

## 3. 已固化原则

```text
System First, Model Second。
Prompt 是控制面，不是临时说明。
钱包数据整合不能按普通目录整理处理。
数据必须按语义分层，而不是按旧目录名分类。
事实层、证据层、推断层、交接层必须分开。
旧目录默认保留，只读参考。
高价值旧数据只能复制导入，不能移动。
所有旧新路径必须可追溯。
完成标准是 Hermes 能按 token 理解数据，而不是文件复制完成。
验证必须独立，不允许系统自己说完成。
未验证规则只能写入候选记忆，不能直接写长期记忆。
```

## 4. 本轮明确未做

- 未扫描旧数据目录
- 未复制旧数据
- 未移动旧目录
- 未删除旧目录
- 未覆盖旧文件
- 未修改业务代码
- 未触发交易
- 未读取或输出私钥、API key、token
- 未执行 git push

## 5. 后续任务入口
后续如果用户要求实际整理/导入 Wallet-Intel 数据，必须新开任务护照并明确是否允许：

- 只读审计
- copy-only 导入
- token 抽样验证
- legacy path fallback

未经新授权，不得把本系统写入任务扩展为真实数据迁移任务。

## 6. 当前结论
本轮完成的是 Harness 系统写入，不是数据迁移完成。最终完成性以独立系统写入验证报告为准。
