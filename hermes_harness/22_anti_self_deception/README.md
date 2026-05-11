# 22_anti_self_deception — Anti Self-Deception Audits

## 定位

防止 HER/Hermes 把“计划、dry-run、文档生成、自我评分”误判为真实完成。

## 主要审计

- `fake_completion_audit.md`：假完成审计。
- `dry_run_vs_real_run_audit.md`：dry-run 与真实运行边界。
- `document_only_audit.md`：只有文档、没有实现的边界。
- `plan_vs_execution_audit.md`：计划和执行混淆审计。
- `self_scoring_audit.md`：自评分审计。

## 硬规则

没有外部证据、文件存在、测试结果、运行产物或独立验证，不得宣称完成。
