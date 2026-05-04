# Phase 11｜NEXT_BACKLOG

## 下一步任务

1. GPT 链接自动处理 adapter
   - 输入: `工作流自动化 <GPT链接>`
   - 输出: 原文、passport、topic map、gap matrix、task package、final reports
   - 边界: paper-only / no secret / no broadcast

2. 报告回流增强
   - 将 Hermes 执行报告自动回流到 `sikk_loop_review_ingestor.py`
   - 生成下一轮 task package

3. Repomix context 正式接入 task package
   - 将 `sikk_repomix_context_planner.py` 的分阶段上下文计划合并进 `REPOMIX_CONTEXT_PLAN.md`

4. 移动端/TG 触发面板
   - 使用自然语言入口，不新增未注册 slash command
   - 输出中文状态卡片与产物路径

## 安全边界

- 不真实交易
- 不 swap
- 不读取私钥
- 不签名
- 不 broadcast
- 不打印 token/webhook
