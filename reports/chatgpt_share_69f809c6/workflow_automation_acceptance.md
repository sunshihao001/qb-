# 工作流自动化验收报告

- 来源：`https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426`
- Slug：`chatgpt_share_69f809c6`
- 状态：已生成
- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。

## 已生成产物
- acceptance_report：`/root/sikk-gmgn/reports/chatgpt_share_69f809c6/automation_absorption_acceptance.md`
- audit：`/root/sikk-gmgn/knowledge/audits/chatgpt_share_69f809c6.system_audit.md`
- hindsight：`/root/sikk-gmgn/knowledge/skills/sikk_hermes_long_task_absorption_skill.md.hindsight.jsonl`
- inbox：`/root/sikk-gmgn/knowledge/inbox/chatgpt_share_69f809c6.md`
- index：`/root/sikk-gmgn/SIKK_SYSTEM_INDEX.md`
- mobile_command_md：`/root/sikk-gmgn/tasks/chatgpt_share_69f809c6/workflow_automation/MOBILE_COMMAND.md`
- passport：`/root/sikk-gmgn/knowledge/passports/chatgpt_share_69f809c6.passport.md`
- rules：`/root/sikk-gmgn/knowledge/extracted_rules/chatgpt_share_69f809c6.rules.md`
- section_task_md：`/root/sikk-gmgn/tasks/chatgpt_share_69f809c6/SECTION_TASK.md`
- shell_entry：`/root/sikk-gmgn/tasks/chatgpt_share_69f809c6/workflow_automation/run_workflow_automation.sh`
- skill：`/root/sikk-gmgn/knowledge/skills/sikk_hermes_long_task_absorption_skill.md`
- system_update：`/root/sikk-gmgn/knowledge/system_updates/chatgpt_share_69f809c6.sikk_update.md`
- task_router_json：`/root/sikk-gmgn/tasks/chatgpt_share_69f809c6/TASK_ROUTER.json`
- task_router_md：`/root/sikk-gmgn/tasks/chatgpt_share_69f809c6/TASK_ROUTER.md`
- workflow_package_json：`/root/sikk-gmgn/tasks/chatgpt_share_69f809c6/workflow_automation/WORKFLOW_AUTOMATION_PACKAGE.json`
- workflow_report_md：`/root/sikk-gmgn/reports/chatgpt_share_69f809c6/workflow_automation_acceptance.md`

## 验收命令
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_her_task_router.py -q`
- `PYTHONPATH=/root/sikk-gmgn python3 sikk_her_task_router.py '<GPT链接>' --execute-absorption --workflow-package`
