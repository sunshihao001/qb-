# HER 任务启动器

- 来源：`https://chatgpt.com/share/69f83af2-a380-83a7-a429-200c72d43279`
- 任务类型：`chatgpt_share`
- Slug：`chatgpt_share_69f83af2`
- 安全边界：paper-only；不执行真实 swap；不读取私钥；不签名；不广播。

## 推荐 Skills
- `conversation-transcript-ingestion`
- `sikk-sol-core-methodology`
- `test-driven-development`

## 任务棱镜
- 任务棱镜 1：读取与证据保存：存在可追溯输入文件；不可读时明确声明。
- 任务棱镜 2：问题识别与断点发现：输出问题诊断、缺口清单和约束报告。
- 任务棱镜 3：系统映射与工具选择：每个结论都落到文件、字段、命令、测试或验收标准。
- 任务棱镜 4：分阶段执行：阶段产物可追溯，测试通过。
- 任务棱镜 5：审计验收与沉淀：安全断言通过，生成中文验收报告。

## 工具路由
- 链接读取：`browser/readability` — 读取链接或明确声明不可读。
- 知识吸收：`sikk_knowledge_absorption.py` — 生成 passport/rules/audit/update/skill/Hindsight。
- SIKK 运行落地：`sikk_live_run.py` — 保持 canonical 单入口与 paper-only runtime 验证。
- 测试验收：`pytest` — 专项测试、全量测试、防回归。
- 结构深度审计：`Super Hermes prism 思维` — 生成任务棱镜、盲点与约束报告。
- 跨模型上下文：`repomix` — 需要跨 LLM 提供代码库上下文时打包，必须先排除 secrets。
- 多代理长任务：`DeerFlow/delegate_task` — 研究、审计、实现、验收可拆分为独立子代理。

## 预期产物
- `tasks/chatgpt_share_69f83af2/TASK_ROUTER.json`
- `tasks/chatgpt_share_69f83af2/TASK_ROUTER.md`
- `tasks/chatgpt_share_69f83af2/SECTION_TASK.md`
- `reports/<slug>/acceptance.md`
- `knowledge/inbox/chatgpt_share_69f83af2.md`
- `knowledge/passports/chatgpt_share_69f83af2.passport.md`
- `knowledge/extracted_rules/chatgpt_share_69f83af2.rules.md`
- `knowledge/audits/chatgpt_share_69f83af2.system_audit.md`
- `knowledge/system_updates/chatgpt_share_69f83af2.sikk_update.md`

## 验收命令
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_her_task_router.py -q`
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q`
- `PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none`
- `检查 live_run_manifest.json 中 real_swap_enabled=false 且 confirmation_enabled=false`

## 下一步
先执行任务棱镜 1：读取与证据保存；不要直接改核心代码。
