# chatgpt_share_69f83af2_her_core_automation_system｜系统差异审计

## 1. 当前系统已有能力
- `sikk_live_run.py`：已存在
- `sikk_paper_live_runner.py`：已存在
- `sikk_dashboard_site_builder.py`：已存在
- `sikk_operator_psychology_engine.py`：已存在
- `sikk_paper_explanation_builder.py`：已存在
- `AGENTS.md`：已存在
- `SIKK_SYSTEM_INDEX.md`：已存在

已识别主入口与边界：`sikk_live_run.py` 是 canonical runtime；系统默认保持 paper-only；不真实买入；不真实卖出；不调用 swap；不签名；不广播；不读取或保存私钥。

## 2. 文章新增认知能力
- 建立外部文章到系统资产的固定吸收链路。
- 将“学习文章”拆成 passport、rules、system_audit、sikk_update、skill、validation_cases。
- 要求交易方法改写为主导侧行为假设、证据条件、反证条件。

## 3. 已经存在但需要增强的部分
- 已有 SIKK 方法论与 runtime 输出，但缺少统一 `knowledge/` 知识吸收资产目录。
- 已有 skill 体系，但项目内缺少可复制的知识吸收 skill 草案。
- 已有测试体系，但缺少知识吸收流程专项测试。

## 4. 当前系统缺失的部分
- `knowledge/inbox/passports/extracted_rules/system_updates/skills/audits/validation_cases` 标准目录。
- 可复用的 `sikk_knowledge_absorption.py` 工具。
- `SIKK_SYSTEM_INDEX.md` 对知识吸收 skill 的索引。
- Hindsight JSONL 知识块导出。

## 5. 文章观点与现有系统冲突的地方
无直接冲突；但任何真实交易、自动 swap、私钥、签名、广播相关内容必须被 SIKK 安全边界降级。

## 6. 应该写入 skill 的内容
知识吸收流程、目录结构、passport/rules/audit/update/skill 输出合约、TDD 验证、安全禁止行为。

## 7. 应该写入 docs 的内容
`SIKK_SYSTEM_INDEX.md` 中加入“知识吸收与 skill 更新规范”。

## 8. 应该修改代码的内容
新增只读/本地写文件工具模块 `sikk_knowledge_absorption.py` 与测试 `tests/test_sikk_knowledge_absorption.py`；不修改真实交易执行层。

## 9. 不建议修改的内容
- 不改真实交易逻辑。
- 不新增复杂后端、数据库、登录系统。
- 不删除 Runtime / dashboard / notifier / paper runner / 状态机 / 钱包结构模块。

## 10. 最小修改路径
1. 创建 knowledge 目录结构。
2. 保存 share 原文到 inbox。
3. 生成 passport/rules/audit/update/skill/index/hindsight。
4. 增加专项测试。
5. 运行 pytest 与主入口安全验证。

## 11. 专业完整修改路径
后续可把该流程扩展为 CLI：`python3 sikk_knowledge_absorption.py absorb <article>`，并接入 Hermes skill 与 Hindsight retain。

## 12. 风险与回滚方案
- 风险：文档生成覆盖已有索引。控制：追加更新，不覆盖原有段落。
- 风险：文章含敏感信息。控制：派生文档不写入私钥/API key，敏感值应替换为 `[REDACTED]`。
- 回滚：删除 `knowledge/` 本次 slug 产物与 `sikk_knowledge_absorption.py/tests/test_sikk_knowledge_absorption.py`。

## 输入规则文件
`/root/sikk-gmgn/knowledge/extracted_rules/chatgpt_share_69f83af2_her_core_automation_system.rules.md`
