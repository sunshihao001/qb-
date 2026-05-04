# SIKK Hermes 长任务知识吸收 Skill

## 1. Skill 名称
SIKK Hermes 长任务知识吸收与系统改造规范

## 2. 适用任务
用户提供 GPT 文章、交易方法论、Agent 工程文章，并要求“吸收、完善进系统体系、改成自己的东西”。

## 3. 不适用任务
一次性摘要、无落地要求的阅读、明确不修改系统的临时问答。

## 4. 工作流
1. 原文保存到 `knowledge/inbox/`。
2. 生成文章知识护照到 `knowledge/passports/`。
3. 提炼可执行规则到 `knowledge/extracted_rules/`。
4. 做系统差异审计到 `knowledge/audits/`。
5. 生成系统更新方案到 `knowledge/system_updates/`。
6. 必要时更新 skill/docs/code。
7. 使用 TDD 添加测试并运行验证。
8. 输出中文报告与下一步最小验证方法。

## 5. 输入格式
文章 URL、Markdown、纯文本、截图 OCR 后文本或本地文件路径。

## 6. 输出格式
passport、rules、system_audit、sikk_update、skill、hindsight JSONL、validation cases。

## 7. Hermes 调用方式
优先使用 `read_file/search_files/write_file/patch/terminal/skill_manage`；涉及 Hermes Agent 自身配置时加载 `hermes-agent` skill。

## 8. 长任务拆分方式
按“读取 → 审计 → 设计 → TDD 修改 → 测试 → 复盘”拆分，不在未审计前直接改核心代码。

## 9. 上下文重置方式
每个阶段将状态写入 `knowledge/system_updates/` 或 `SIKK_PROJECT_STATE.md`，避免上下文压缩后丢失。

## 10. 进度记录方式
使用 todo，并在产物中记录输入、输出、验证命令、未完成项。

## 11. 文件写入规范
追加优先，不覆盖已有系统索引；原文不改写；派生文件必须可追溯到原文。

## 12. 测试验证规范
新增行为先写失败测试；通过后运行专项测试、全量测试和必要的 `sikk_live_run.py --mode once`。

## 13. 禁止行为
paper-only；不真实买入；不真实卖出；不调用 swap；不签名；不广播；不读取或保存私钥。 不输出确定“庄家”；不把文章主观判断直接变成交易动作。

## 14. 与 SIKK-SOL 系统的结合方式
把文章内容落到 SIKK-SOL 的数据层、钱包结构层、盘型识别层、主导侧生命周期层、市值上下文层、状态机层、paper 层、dashboard 层和复盘层。

## 来源资产
- `/root/sikk-gmgn/knowledge/passports/chatgpt_share_69f868b8.passport.md`
- `/root/sikk-gmgn/knowledge/extracted_rules/chatgpt_share_69f868b8.rules.md`
- `/root/sikk-gmgn/knowledge/audits/chatgpt_share_69f868b8.system_audit.md`
