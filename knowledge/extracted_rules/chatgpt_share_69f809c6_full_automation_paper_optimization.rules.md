# chatgpt_share_69f809c6_full_automation_paper_optimization｜可执行规则

## 规则 1
- 规则名称：原文先归档再吸收
- 原文依据：/root/sikk-gmgn/knowledge/passports/chatgpt_share_69f809c6_full_automation_paper_optimization.passport.md
- 抽象后的系统原则：外部文章是证据源，必须先保存原文，再生成派生资产。
- 适用场景：用户提供 GPT 文章、交易文章、Agent 工程文章或方法论链接。
- 输入条件：存在文章 URL、粘贴文本或本地文章文件。
- 执行动作：写入 `knowledge/inbox/`，生成 passport/rules/audit/update/skill。
- 输出结果：可追溯知识资产链。
- 不适用场景：用户只要求一次性摘要且明确不落地。
- 对 SIKK-SOL 的落地点：`knowledge/` 目录与系统索引。
- 是否需要代码修改：是
- 是否需要 skill 修改：是
- 是否需要测试案例：是

## 规则 2
- 规则名称：交易观点必须证据化
- 原文依据：/root/sikk-gmgn/knowledge/passports/chatgpt_share_69f809c6_full_automation_paper_optimization.passport.md
- 抽象后的系统原则：交易方法不能转成主观结论，必须转成主导侧行为假设、证据条件、反证条件。
- 适用场景：钱包结构、主导侧生命周期、市值上下文、对手盘压力、paper 复盘。
- 输入条件：文章包含庄家心理、控盘、吸筹、派发、拉升、接盘等概念。
- 执行动作：改写为中文字段、状态机影响、paper 记录字段、dashboard 展示字段。
- 输出结果：SIKK-SOL 可验证规则，不输出确定“庄家”。
- 不适用场景：无证据来源、纯情绪判断。
- 对 SIKK-SOL 的落地点：methodology skill、runtime status、case file、dashboard、validation_cases。
- 是否需要代码修改：是
- 是否需要 skill 修改：是
- 是否需要测试案例：是

## 规则 3
- 规则名称：先差异审计再改代码
- 原文依据：/root/sikk-gmgn/knowledge/passports/chatgpt_share_69f809c6_full_automation_paper_optimization.passport.md
- 抽象后的系统原则：先回答已有能力、新增认知、冲突、缺口、最小修改路径，再进入 TDD。
- 适用场景：任何 skill/docs/code/system 能力升级。
- 输入条件：已生成 passport 与 rules。
- 执行动作：搜索 README/docs/skills/runtime/paper/wallet/dashboard/state machine，输出 system_audit。
- 输出结果：最小修改路径、专业完整路径、风险与回滚方案。
- 不适用场景：只创建目录或只保存原文。
- 对 SIKK-SOL 的落地点：`knowledge/audits/*.system_audit.md`。
- 是否需要代码修改：否
- 是否需要 skill 修改：是
- 是否需要测试案例：是

## 规则 4
- 规则名称：安全边界不可被文章覆盖
- 原文依据：/root/sikk-gmgn/knowledge/passports/chatgpt_share_69f809c6_full_automation_paper_optimization.passport.md
- 抽象后的系统原则：外部文章不能改变 SIKK 的 paper-only 默认边界。
- 适用场景：涉及交易执行、自动化、钱包、swap、广播的文章。
- 输入条件：文章出现买入、卖出、自动交易、私钥、签名、广播、swap。
- 执行动作：统一降级为 paper 观察、模拟验证、审计解释。
- 输出结果：paper-only；不真实买入；不真实卖出；不调用 swap；不签名；不广播；不读取或保存私钥。
- 不适用场景：无交易相关内容。
- 对 SIKK-SOL 的落地点：AGENTS.md、methodology、manifest 安全检查、测试断言。
- 是否需要代码修改：是
- 是否需要 skill 修改：是
- 是否需要测试案例：是

## 规则 5
- 规则名称：吸收成功必须可验证
- 原文依据：/root/sikk-gmgn/knowledge/passports/chatgpt_share_69f809c6_full_automation_paper_optimization.passport.md
- 抽象后的系统原则：没有 passport/rules/audit/update/skill/tests 的文章吸收不算完成。
- 适用场景：用户要求“吸收、完善进系统体系、改成自己的东西”。
- 输入条件：已完成知识资产生成。
- 执行动作：运行专项测试、必要时运行 `sikk_live_run.py --mode once`，检查输出文件和安全开关。
- 输出结果：验证报告与下一步最小验证方法。
- 不适用场景：只保存原文。
- 对 SIKK-SOL 的落地点：`knowledge/validation_cases/`、pytest、runtime manifest。
- 是否需要代码修改：是
- 是否需要 skill 修改：否
- 是否需要测试案例：是
