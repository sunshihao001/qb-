"""SIKK-SOL knowledge absorption utilities.

把外部文章从“原文”转成 SIKK 可复用系统资产：知识护照、可执行规则、系统差异审计、系统更新方案、skill 草案、索引与 Hindsight 知识块。
本模块只写本地知识文件，不触发交易、不签名、不广播。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


KNOWLEDGE_SUBDIRS = [
    "inbox",
    "passports",
    "extracted_rules",
    "system_updates",
    "skills",
    "audits",
    "validation_cases",
]

SAFETY_BOUNDARY = "paper-only；不真实买入；不真实卖出；不调用 swap；不签名；不广播；不读取或保存私钥。"


def ensure_knowledge_workspace(root: str | Path) -> list[Path]:
    """Create the canonical SIKK knowledge absorption workspace."""
    root = Path(root)
    paths: list[Path] = []
    for subdir in KNOWLEDGE_SUBDIRS:
        path = root / "knowledge" / subdir
        path.mkdir(parents=True, exist_ok=True)
        paths.append(path)
    return paths


def _slug_from_path(path: Path) -> str:
    return path.stem.replace(" ", "_").replace("-", "_")


def _read(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")


def _write(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def _title_from_article(article: str, fallback: str) -> str:
    for line in article.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip() or fallback
    return fallback.replace("_", " ")


def _contains_any(text: str, terms: Iterable[str]) -> bool:
    lower = text.lower()
    return any(term.lower() in lower for term in terms)


def _domain(article: str) -> str:
    if _contains_any(article, ["钱包", "主导侧", "市值", "庄家", "交易", "paper", "swap"]):
        return "SIKK-SOL 交易结构方法论 / Hermes 长任务工程"
    if _contains_any(article, ["Hermes", "Harness", "Agent", "长任务", "上下文"]):
        return "Hermes Agent 长任务运行规范"
    return "SIKK-SOL 外部知识吸收"


def build_knowledge_passport(root: str | Path, article_path: str | Path) -> Path:
    """Generate a passport without modifying the source article."""
    root = Path(root)
    article_path = Path(article_path)
    ensure_knowledge_workspace(root)
    article = _read(article_path)
    slug = _slug_from_path(article_path)
    title = _title_from_article(article, slug)
    domain = _domain(article)
    passport = f"""# {title}｜文章知识护照

## 1. 文章标题
{title}

## 2. 原始主题
外部文章如何被 Hermes / SIKK-SOL 吸收为可验证的系统能力，而不是停留在摘要。

## 3. 适用领域
{domain}

## 4. 核心观点 5-10 条
1. 原文必须先完整保存到 `knowledge/inbox/`，避免二次转述丢失证据。
2. 每篇文章必须生成知识护照，先理解再改系统。
3. 文章观点必须提炼为可执行规则，包含输入、动作、输出、禁用场景与验证方式。
4. 修改 skill/docs/代码前必须先做系统差异审计。
5. 涉及交易方法时，不能输出确定“庄家”，必须改写为主导侧行为假设、证据条件与反证条件。
6. 涉及交易执行时必须保持 {SAFETY_BOUNDARY}
7. 任何新增能力必须落到字段、模块、流程、状态机、paper 记录、面板或测试之一。
8. 修改代码后必须运行专项测试与全量/主入口验证。

## 5. 关键机制
`文章 → 知识护照 → 方法论提炼 → 系统差异审计 → Skill 更新 → 代码/规则/面板字段更新 → 测试验证 → 记忆沉淀`。

## 6. 可转化为系统能力的部分
- 固定知识目录结构：`knowledge/inbox/passports/extracted_rules/system_updates/skills/audits/validation_cases`。
- 固定文档合约：passport、rules、system_audit、sikk_update、skill、hindsight JSONL。
- 固定安全边界：{SAFETY_BOUNDARY}
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
- 输入文件：`{article_path}`
- 原文长度：{len(article)} 字符
"""
    return _write(root / "knowledge" / "passports" / f"{slug}.passport.md", passport)


def extract_executable_rules(root: str | Path, passport_path: str | Path) -> Path:
    root = Path(root)
    passport_path = Path(passport_path)
    ensure_knowledge_workspace(root)
    slug = passport_path.name.replace(".passport.md", "")
    passport = _read(passport_path)
    rules = f"""# {slug}｜可执行规则

## 规则 1
- 规则名称：原文先归档再吸收
- 原文依据：{passport_path}
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
- 原文依据：{passport_path}
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
- 原文依据：{passport_path}
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
- 原文依据：{passport_path}
- 抽象后的系统原则：外部文章不能改变 SIKK 的 paper-only 默认边界。
- 适用场景：涉及交易执行、自动化、钱包、swap、广播的文章。
- 输入条件：文章出现买入、卖出、自动交易、私钥、签名、广播、swap。
- 执行动作：统一降级为 paper 观察、模拟验证、审计解释。
- 输出结果：{SAFETY_BOUNDARY}
- 不适用场景：无交易相关内容。
- 对 SIKK-SOL 的落地点：AGENTS.md、methodology、manifest 安全检查、测试断言。
- 是否需要代码修改：是
- 是否需要 skill 修改：是
- 是否需要测试案例：是

## 规则 5
- 规则名称：吸收成功必须可验证
- 原文依据：{passport_path}
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
"""
    return _write(root / "knowledge" / "extracted_rules" / f"{slug}.rules.md", rules)


def _file_exists(root: Path, name: str) -> str:
    return "已存在" if (root / name).exists() else "未发现"


def build_system_audit(root: str | Path, rules_path: str | Path) -> Path:
    root = Path(root)
    rules_path = Path(rules_path)
    ensure_knowledge_workspace(root)
    slug = rules_path.name.replace(".rules.md", "")
    candidate_files = [
        "sikk_live_run.py",
        "sikk_paper_live_runner.py",
        "sikk_dashboard_site_builder.py",
        "sikk_operator_psychology_engine.py",
        "sikk_paper_explanation_builder.py",
        "AGENTS.md",
        "SIKK_SYSTEM_INDEX.md",
    ]
    inventory = "\n".join(f"- `{name}`：{_file_exists(root, name)}" for name in candidate_files)
    audit = f"""# {slug}｜系统差异审计

## 1. 当前系统已有能力
{inventory}

已识别主入口与边界：`sikk_live_run.py` 是 canonical runtime；系统默认保持 {SAFETY_BOUNDARY}

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
`{rules_path}`
"""
    return _write(root / "knowledge" / "audits" / f"{slug}.system_audit.md", audit)


def generate_system_update(root: str | Path, passport_path: str | Path, rules_path: str | Path, audit_path: str | Path) -> Path:
    root = Path(root)
    ensure_knowledge_workspace(root)
    slug = Path(passport_path).name.replace(".passport.md", "")
    content = f"""# {slug}｜SIKK 系统更新方案

## 系统更新方案
将 ChatGPT/Hermes 文章吸收流程落地为 SIKK-SOL 本地知识治理层。

## 输入文件
- `knowledge/passports/{Path(passport_path).name}`
- `knowledge/extracted_rules/{Path(rules_path).name}`
- `knowledge/audits/{Path(audit_path).name}`

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
{SAFETY_BOUNDARY}

## 验证方式
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest tests/test_sikk_knowledge_absorption.py -q`
- `PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q`
- `PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none`
"""
    return _write(root / "knowledge" / "system_updates" / f"{slug}.sikk_update.md", content)


def generate_absorption_skill(root: str | Path, passport_path: str | Path, rules_path: str | Path, audit_path: str | Path) -> Path:
    root = Path(root)
    ensure_knowledge_workspace(root)
    content = f"""# SIKK Hermes 长任务知识吸收 Skill

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
{SAFETY_BOUNDARY} 不输出确定“庄家”；不把文章主观判断直接变成交易动作。

## 14. 与 SIKK-SOL 系统的结合方式
把文章内容落到 SIKK-SOL 的数据层、钱包结构层、盘型识别层、主导侧生命周期层、市值上下文层、状态机层、paper 层、dashboard 层和复盘层。

## 来源资产
- `{passport_path}`
- `{rules_path}`
- `{audit_path}`
"""
    return _write(root / "knowledge" / "skills" / "sikk_hermes_long_task_absorption_skill.md", content)


def update_system_index(root: str | Path, skill_path: str | Path) -> Path:
    root = Path(root)
    skill_path = Path(skill_path)
    index_path = root / "SIKK_SYSTEM_INDEX.md"
    block = f"""\n## 知识吸收与 Skill 更新规范

- Skill 文件：`{skill_path.relative_to(root) if skill_path.is_relative_to(root) else skill_path}`
- 用途：吸收外部文章，把文章转成系统规则、长任务拆分、上下文交接、测试验证与 skill 更新。
- 安全边界：{SAFETY_BOUNDARY}
"""
    if index_path.exists():
        current = _read(index_path)
        if "sikk_hermes_long_task_absorption_skill.md" not in current:
            return _write(index_path, current.rstrip() + "\n" + block)
        return index_path
    content = f"""# SIKK-SOL 系统索引

1. 核心方法论
2. 钱包结构分析
3. 盘型识别
4. 主导侧生命周期
5. 主导侧意图推断
6. 市值上下文判断
7. 纸面交易记录
8. 自动复盘系统
9. Hermes 长任务执行规范
10. 知识吸收与 skill 更新规范
{block}
"""
    return _write(index_path, content)


def generate_hindsight_blocks(root: str | Path, skill_path: str | Path) -> Path:
    root = Path(root)
    skill_path = Path(skill_path)
    ensure_knowledge_workspace(root)
    blocks = [
        {
            "title": "SIKK 知识吸收固定流程",
            "content": "外部文章必须按 原文保存→知识护照→可执行规则→系统差异审计→系统更新方案→skill/docs/code→测试验证 的链路进入 SIKK-SOL。",
            "keywords": ["SIKK-SOL", "知识吸收", "Hermes", "skill", "系统差异审计"],
            "use_case": "用户提供 GPT/交易/工程文章并要求吸收进系统体系时使用。",
        },
        {
            "title": "SIKK 文章吸收安全边界",
            "content": SAFETY_BOUNDARY + " 涉及庄家心理必须改写成主导侧行为假设、证据条件、反证条件。",
            "keywords": ["paper-only", "安全边界", "不调用 swap", "主导侧行为假设"],
            "use_case": "吸收交易方法论或自动交易文章时防止越界。",
        },
    ]
    path = skill_path.with_suffix(skill_path.suffix + ".hindsight.jsonl")
    content = "\n".join(json.dumps(block, ensure_ascii=False) for block in blocks) + "\n"
    return _write(path, content)


def absorb_article(root: str | Path, source_path: str | Path) -> dict[str, str]:
    """Run the full local absorption chain for an existing article file."""
    root = Path(root)
    ensure_knowledge_workspace(root)
    source_path = Path(source_path)
    inbox_path = root / "knowledge" / "inbox" / source_path.name
    if source_path.resolve() != inbox_path.resolve():
        _write(inbox_path, _read(source_path))
    passport = build_knowledge_passport(root, inbox_path)
    rules = extract_executable_rules(root, passport)
    audit = build_system_audit(root, rules)
    update = generate_system_update(root, passport, rules, audit)
    skill = generate_absorption_skill(root, passport, rules, audit)
    index = update_system_index(root, skill)
    hindsight = generate_hindsight_blocks(root, skill)
    return {
        "inbox": str(inbox_path),
        "passport": str(passport),
        "rules": str(rules),
        "audit": str(audit),
        "system_update": str(update),
        "skill": str(skill),
        "index": str(index),
        "hindsight": str(hindsight),
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SIKK knowledge absorption utility")
    parser.add_argument("article", help="Path to source article markdown/text")
    parser.add_argument("--root", default="/root/sikk-gmgn")
    args = parser.parse_args()
    result = absorb_article(args.root, args.article)
    print(json.dumps(result, ensure_ascii=False, indent=2))
