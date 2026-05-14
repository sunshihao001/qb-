# SIKK-GMGN Project Rules

本项目是 SIKK-SOL / SIKK-GMGN 结构智能纸面验证与观测系统。

当前阶段：Phase B-0.5：连续运行 + 纸面验证 + 专业静态可视化控制台。

## 核心边界

- 不执行真实 swap。
- 不读取、写入或保存私钥。
- 不自动签名或 broadcast。
- 不删除已有模块。
- 不新增复杂后端。
- 不新增数据库。
- 不新增登录系统。
- 不为了复杂而升级。
- `data/gmgn_candidates_live_run` 仅保留为 legacy runtime 兼容区，不再作为新 source_wallet 主写路径。
- 钱包结构分析 / 钱包数据采集 / Source Wallet Bot 的专业化主目录固定为 `/root/sikk-gmgn/`；`/root/sikk-wallet-intel/` 只作为 Wallet-Intel 协同、总控、行为推断和历史 runs 工作区，不作为新增钱包结构分析主数据/主代码/主方法论目录。

## 系统目录宪法（强制）

后续任何 Hermes / 子 agent / 脚本任务，只要要写入、生成或重排文件，必须先遵守：

- 主文档：`docs/system_directory_constitution.md`
- 机器路由：`docs/system_directory_routes.json`
- 旧输出补充规范：`docs/output_directory_governance.md`

写文件前必须先回答四个问题：

1. 这是哪个 Bot / domain？
2. 这是哪类资产：方法论、代码、数据、schema、contract、报告、token 输出、长任务状态、import、legacy compat？
3. 资产 ID 是什么：token、run、import、case、task？
4. 主写路径是否符合 `docs/system_directory_routes.json`？

如果不能回答，必须先写计划到 `research_loop/plans/`，不得直接写运行文件。

新增文件默认规则：

- 方法论 / 反证 / 统计模型：`research_loop/methodology/`
- 功能代码：`modules/<bot_or_domain>/`
- 测试：`tests/`
- schema：`modules/<bot>/schemas/` 或 `schemas/shared/`
- contract：`modules/<bot>/contracts/` 或 `contracts/`
- 运行数据：`data/<bot>/<mode>/<asset_id>/`
- 人类可读报告：`reports/<bot>/<mode>/<asset_id>/`
- 长任务状态：`research_loop/state/<task_id>/`
- 外部导入：`imports/staging/<import_id>/`
- 旧路径兼容索引：`legacy_compat/`

禁止在项目根目录散放新的 JSON / CSV / Markdown 运行输出。根目录只允许入口脚本、既有兼容文件、`README.md`、`AGENTS.md`、`SIKK_*.md` 等明确顶层文档。

不允许为了迁移而删除或移动旧文件；旧路径只能 copy-only 映射，并在 manifest 中记录 old_path -> new_path。

## 主入口

`python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode once`

## 当前可视化目标

创建本地静态网站控制台：

`data/gmgn_candidates_live_run/site/index.html`

## 禁止

- 改真实交易逻辑。
- 新增交易按钮。
- 新增自动实盘。
- 删除 Runtime / dashboard / notifier / paper runner 已有模块。
- 把 `priority_level` 当作买入信号。
