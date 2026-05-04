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
- 所有运行输出统一在 `data/gmgn_candidates_live_run` 下。

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
