# chatgpt_share_69f72598_sikk_paper_trade_optimization｜SIKK 系统更新方案

## 系统更新方案
将 ChatGPT/Hermes 文章吸收流程落地为 SIKK-SOL 本地知识治理层。

## 输入文件
- `knowledge/passports/chatgpt_share_69f72598_sikk_paper_trade_optimization.passport.md`
- `knowledge/extracted_rules/chatgpt_share_69f72598_sikk_paper_trade_optimization.rules.md`
- `knowledge/audits/chatgpt_share_69f72598_sikk_paper_trade_optimization.system_audit.md`

## 新增系统资产
- `sikk_knowledge_absorption.py`：生成知识护照、规则、审计、skill、索引、Hindsight JSONL。
- `tests/test_sikk_knowledge_absorption.py`：锁定吸收流程。
- `knowledge/`：外部文章系统化吸收目录。
- `SIKK_SYSTEM_INDEX.md`：系统索引入口。

## 字段 / 文件合约
- 原文：`knowledge/inbox/*.md`
- 知识护照：`knowledge/passports/*.passport.md`
- 可执行规则：`knowledge/extracted_rules/*.rules.md`
- 系统差异审计：`knowledge/audits/*.system_audit.md`
- 系统更新方案：`knowledge/system_updates/*.sikk_update.md`
- skill 草案：`knowledge/skills/*_skill.md`
- Hindsight 块：`knowledge/skills/*.hindsight.jsonl`

## 安全边界
paper-only；不真实买入；不真实卖出；不调用 swap；不签名；不广播；不读取或保存私钥。

## 验证方式
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_knowledge_absorption.py -q`
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q`
- `PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none`
