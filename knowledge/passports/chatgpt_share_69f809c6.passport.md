# chatgpt_share_69f809c6｜文章知识护照

## 1. 文章标题
chatgpt_share_69f809c6

## 2. 原始主题
外部文章如何被 Hermes / SIKK-SOL 吸收为可验证的系统能力，而不是停留在摘要。

## 3. 适用领域
SIKK-SOL 外部知识吸收

## 4. 核心观点 5-10 条
1. 原文必须先完整保存到 `knowledge/inbox/`，避免二次转述丢失证据。
2. 每篇文章必须生成知识护照，先理解再改系统。
3. 文章观点必须提炼为可执行规则，包含输入、动作、输出、禁用场景与验证方式。
4. 修改 skill/docs/代码前必须先做系统差异审计。
5. 涉及交易方法时，不能输出确定“庄家”，必须改写为主导侧行为假设、证据条件与反证条件。
6. 涉及交易执行时必须保持 paper-only；不真实买入；不真实卖出；不调用 swap；不签名；不广播；不读取或保存私钥。
7. 任何新增能力必须落到字段、模块、流程、状态机、paper 记录、面板或测试之一。
8. 修改代码后必须运行专项测试与全量/主入口验证。

## 5. 关键机制
`文章 → 知识护照 → 方法论提炼 → 系统差异审计 → Skill 更新 → 代码/规则/面板字段更新 → 测试验证 → 记忆沉淀`。

## 6. 可转化为系统能力的部分
- 固定知识目录结构：`knowledge/inbox/passports/extracted_rules/system_updates/skills/audits/validation_cases`。
- 固定文档合约：passport、rules、system_audit、sikk_update、skill、hindsight JSONL。
- 固定安全边界：paper-only；不真实买入；不真实卖出；不调用 swap；不签名；不广播；不读取或保存私钥。
- 固定工程纪律：先审计，再 TDD 修改，再验证。

## 7. 不适合纳入系统的部分
- 原文中的主观化、不可验证判断。
- 将“庄家心理”直接写成确定结论的表达。
- 绕过 paper-only 的真实交易、签名、广播、swap 操作。
- 没有测试、没有输出文件、没有回滚方案的复杂升级。

## 8. 对 SIKK-SOL 的潜在价值
让 SIKK-SOL 能持续吸收 GPT 文章、交易方法论、Agent 工程文章，并把它们转为中文变量、判断条件、状态机影响、paper 字段、dashboard 字段和复盘规则。

## 9. 与当前 SIKK-SOL 系统的关系
当前 SIKK-SOL 已有单入口 `sikk_live_run.py`、paper runner、dashboard、wallet/lifecycle/psychology 等模块；本文章补充的是“外部知识进入系统”的治理层与文件资产链路。

## 10. 需要进一步验证的地方
- 目录与文件是否自动生成。
- rules/audit/update/skill/index/hindsight 是否稳定输出。
- 新增能力是否进入项目索引与测试。
- 运行主入口后安全开关是否仍为关闭真实交易。

## 原文证据引用
- 输入文件：`/root/sikk-gmgn/knowledge/inbox/chatgpt_share_69f809c6.md`
- 原文长度：107 字符
