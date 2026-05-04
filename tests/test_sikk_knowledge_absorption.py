import json
from pathlib import Path

from sikk_knowledge_absorption import (
    KNOWLEDGE_SUBDIRS,
    build_knowledge_passport,
    build_system_audit,
    ensure_knowledge_workspace,
    extract_executable_rules,
    generate_absorption_skill,
    generate_hindsight_blocks,
    generate_system_update,
    update_system_index,
)


SAMPLE_ARTICLE = """# Hermes 长任务吸收流程

文章认为外部文章不能只总结，必须先保存原文，再生成知识护照、提炼规则、执行系统差异审计，最后沉淀成 skill、测试与工程更新。
对 SIKK-SOL 来说，交易方法文章要改写成主导侧行为假设、证据条件、反证条件，不能写成确定庄家。
代码修改前必须列文件清单，修改后必须运行测试；涉及交易执行必须保持 paper-only，不调用 swap、不签名、不广播。
"""


def test_ensure_knowledge_workspace_creates_expected_dirs(tmp_path):
    root = tmp_path / "sikk"

    paths = ensure_knowledge_workspace(root)

    assert [p.name for p in paths] == KNOWLEDGE_SUBDIRS
    for subdir in KNOWLEDGE_SUBDIRS:
        assert (root / "knowledge" / subdir).is_dir()


def test_build_knowledge_passport_preserves_article_and_outputs_required_sections(tmp_path):
    root = tmp_path / "sikk"
    article_path = root / "knowledge" / "inbox" / "hermes_harness_engineering.md"
    article_path.parent.mkdir(parents=True)
    article_path.write_text(SAMPLE_ARTICLE, encoding="utf-8")

    passport_path = build_knowledge_passport(root, article_path)
    passport = passport_path.read_text(encoding="utf-8")

    assert article_path.read_text(encoding="utf-8") == SAMPLE_ARTICLE
    assert passport_path == root / "knowledge" / "passports" / "hermes_harness_engineering.passport.md"
    for section in [
        "文章标题",
        "原始主题",
        "适用领域",
        "核心观点",
        "关键机制",
        "可转化为系统能力的部分",
        "不适合纳入系统的部分",
        "对 SIKK-SOL 的潜在价值",
        "与当前 SIKK-SOL 系统的关系",
        "需要进一步验证的地方",
    ]:
        assert section in passport
    assert "paper-only" in passport
    assert "不调用 swap" in passport


def test_extract_rules_audit_update_skill_index_and_hindsight_are_generated(tmp_path):
    root = tmp_path / "sikk"
    root.mkdir(parents=True)
    (root / "sikk_live_run.py").write_text("# canonical runtime\nPAPER_READY = True\n", encoding="utf-8")
    (root / "sikk_paper_live_runner.py").write_text("# paper runner\n", encoding="utf-8")
    (root / "sikk_dashboard_site_builder.py").write_text("# dashboard\n", encoding="utf-8")
    article_path = root / "knowledge" / "inbox" / "hermes_harness_engineering.md"
    article_path.parent.mkdir(parents=True)
    article_path.write_text(SAMPLE_ARTICLE, encoding="utf-8")

    passport_path = build_knowledge_passport(root, article_path)
    rules_path = extract_executable_rules(root, passport_path)
    audit_path = build_system_audit(root, rules_path)
    update_path = generate_system_update(root, passport_path, rules_path, audit_path)
    skill_path = generate_absorption_skill(root, passport_path, rules_path, audit_path)
    index_path = update_system_index(root, skill_path)
    hindsight_path = generate_hindsight_blocks(root, skill_path)

    rules = rules_path.read_text(encoding="utf-8")
    assert "## 规则 1" in rules
    assert "对 SIKK-SOL 的落地点" in rules
    assert "是否需要代码修改：是" in rules
    assert "是否需要 skill 修改：是" in rules
    assert "是否需要测试案例：是" in rules
    assert "主导侧行为假设" in rules

    audit = audit_path.read_text(encoding="utf-8")
    for section in [
        "当前系统已有能力",
        "文章新增认知能力",
        "当前系统缺失的部分",
        "应该写入 skill 的内容",
        "应该修改代码的内容",
        "风险与回滚方案",
    ]:
        assert section in audit
    assert "sikk_live_run.py" in audit
    assert "paper-only" in audit

    update = update_path.read_text(encoding="utf-8")
    assert "系统更新方案" in update
    assert "knowledge/passports" in update
    assert "knowledge/extracted_rules" in update

    skill = skill_path.read_text(encoding="utf-8")
    assert "Skill 名称" in skill
    assert "工作流" in skill
    assert "禁止行为" in skill
    assert "SIKK-SOL" in skill

    index = index_path.read_text(encoding="utf-8")
    assert "SIKK-SOL 系统索引" in index
    assert "sikk_hermes_long_task_absorption_skill.md" in index

    blocks = [json.loads(line) for line in hindsight_path.read_text(encoding="utf-8").splitlines()]
    assert blocks
    assert {"title", "content", "keywords", "use_case"} <= set(blocks[0])
    assert "知识吸收" in blocks[0]["keywords"]


def test_her_core_automation_share_is_absorbed_as_task_lens_and_tool_router(tmp_path):
    from sikk_knowledge_absorption import absorb_article

    root = tmp_path / "sikk"
    root.mkdir(parents=True)
    (root / "sikk_live_run.py").write_text("# canonical runtime\n", encoding="utf-8")
    article_path = tmp_path / "chatgpt_share_69f83af2_her_core_automation_system.md"
    article_path.write_text(
        "# HER 核心运用手法与自动化体系重构\n\n"
        "GPT 链接默认不是总结，而是进入任务棱镜、系统审计、工具选择、分阶段实现、测试验收。\n"
        "Super Hermes 提供 prism-scan/prism-reflect 约束报告，Repomix 提供代码库上下文打包，DeerFlow 提供多代理运行时。\n"
        "AI 可以自己跑流程，但必须保持 paper-only、不真实 swap、不签名、不广播。\n",
        encoding="utf-8",
    )

    outputs = absorb_article(root, article_path)

    passport = Path(outputs["passport"]).read_text(encoding="utf-8")
    rules = Path(outputs["rules"]).read_text(encoding="utf-8")
    audit = Path(outputs["audit"]).read_text(encoding="utf-8")
    update = Path(outputs["system_update"]).read_text(encoding="utf-8")

    assert "HER 核心运用手法与自动化体系重构" in passport
    assert "原文先归档再吸收" in rules
    assert "系统差异审计" in audit
    assert "paper-only" in update
    assert "swap" in update
