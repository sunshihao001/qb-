# Hermes Harness V1.6 Judgment Governance Layer

## 定位

V1.6 不是继续增强“自动解决问题”，而是在 V1.3 APUR 与 V1.4/V1.5 runtime hook 之上增加 **Judgment Governance System / 判断系统治理层**。

核心升级：

```text
从：让 Hermes 自动理解并闭环解决问题
到：治理 Hermes 的判断质量、停止能力、证据阈值、验证质量、记忆风险和人机边界
```

## 核心判断

Hermes 不得把“流程完整”视为“判断正确”。
Hermes 不得把“生成文档”视为“任务落地”。
Hermes 不得把“没有报错”视为“已验证”。
Hermes 不得把“记忆更多”视为“判断更可靠”。

## V1.6 必须回答的治理问题

1. 问题是否真实，还是表面噪声？
2. 是否值得现在解决，还是应观察/排队/降级？
3. 当前证据是否足够判断？
4. 是否存在反证或未知项？
5. 是否应该停止、不行动、缩小范围或交给人？
6. 方案是否过度工程化，维护成本是否可接受？
7. 验证是否能证明目标达成，还是只证明产物存在？
8. 旧规则/旧记忆是否已失效或污染判断？
9. 系统是否在把输出、解释、dry-run、流程完成当成真实成果？
10. 本次错误是否能降低下一次同类 judgment_error_rate？

## 新路由

`hermes_judgment_governance_layer`

## 新目录

`15_judgment_governance/`

## 插入点

V1.6 在 V1.4 runtime hook 中作为 `judgment_governance_hook`：

```text
router
→ problem_passport
→ judgment_governance_hook
→ APUR execution or abstention/human handoff
→ tool ledger
→ verification
→ meta verification
→ anti self-deception audit
→ recovery/writeback/completion audit
```

## 完成定义

V1.6 不能只以 runner exit 0 为完成。完成必须同时满足：

- judgment_governance_state 存在且 schema 合法；
- problem triage 已判断 worth/impact/urgency/root-vs-symptom；
- evidence sufficiency 已给出证据阈值与未知项；
- abstention gate 给出 continue/abstain/observe/human_handoff/reduce_scope；
- solution cost review 执行 complexity brake；
- meta verification 审查验证本身；
- anti self-deception audit 审查假闭环；
- memory lifecycle review 审查记忆污染风险；
- operator decision gate 记录是否需要人类裁决；
- final report 与 memory queue candidate 写入；
- 独立验证通过。
