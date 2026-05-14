# SIKK-SOL 系统索引

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
11. 专业交互系统 / 统一索引驱动

## 知识吸收与 Skill 更新规范

- Skill 文件：`knowledge/skills/sikk_hermes_long_task_absorption_skill.md`
- 用途：吸收外部文章，把文章转成系统规则、长任务拆分、上下文交接、测试验证与 skill 更新。
- 安全边界：paper-only；不真实买入；不真实卖出；不调用 swap；不签名；不广播；不读取或保存私钥。

## 专业交互系统 / 统一索引驱动

- 探究设计文档：`docs/plans/sikk_professional_interaction_investigation_design_20260503.md`
- 方法来源：按 share 方法轮执行，先侦察现状，再生成 Section Task，再更新认知，最后运行验收。
- 当前结论：`sikk_live_run.py` 仍是 canonical 单入口；现有 `sikk_query.py` / `sikkctl.py` / `sikk_telegram_open.py` 是早期只读查询层与 Telegram view 雏形。
- 下一阶段目标：新增 `sikk_unified_view_builder.py`，把 paper JSON/CSV、live_state、live_board、live_dashboard、site/dashboard_data.json、wallet daily report 汇总为 `data/gmgn_candidates_live_run/index/*.json`。
- 统一索引计划输出：`system_index.json`、`token_detail_index.json`、`position_index.json`、`latest_open_positions.json`、`latest_closed_positions.json`、`case_file_index.json`、`auto_review_index.json`、`alert_index.json`、`telegram_callback_index.json`。
- Telegram 交互原则：底层命令保留英文，用户可见中文；callback_data 使用短码，如 `tok:T1`、`pos:P1`、`case:C1`、`menu:main`，不直接塞长地址或中文。
- 安全边界：CLI / Web / Telegram / Report / Alert 全部只读展示、诊断、复盘和提醒；不新增 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST 交易按钮；真实交易默认关闭。

