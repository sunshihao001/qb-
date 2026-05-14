# SIKK Lessons Learned

## 001: 不要让 AI 删除已实现模块

Runtime / dashboard / notifier / confirmation ticket / paper runner 等已有模块即使当前默认关闭，也应保留为可选模块，不应删除。

## 002: Markdown 面板不适合高频观察

`live_board.md` 适合记录和 Telegram 摘要，但不适合快速筛选、聚合和定位阻断原因。Phase B-0.5 需要本地静态 HTML 控制台。

## 003: 钱包结构未接入必须可解释

`未接入` 不应默认视为系统错误或安全。需要区分：

- `WAIT_SIGNAL`：尚未进入信号阶段。
- `WAIT_ACCUMULATION`：尚未进入吸筹/结构阶段。
- `BLOCKED_BEFORE_WALLET`：上游已阻断，未进入钱包阶段。
- `NO_WALLET_INPUT`：应进入钱包阶段但缺钱包输出，需要复查。

## 004: paper JSON/CSV 必须同步

日报、dashboard、复盘可能读取 CSV，而 paper runner 主要写 JSON。若 JSON 与 CSV 不同步，会导致统计断链。后续应优先修复 open/closed JSON↔CSV 一致性。

## 005: site dashboard 先数据层，后 UI

不要一上来做复杂页面。先稳定生成 `site/dashboard_data.json`，再让 `index.html/app.js/style.css` 只读该 JSON。

## 006: `priority_level` 只用于面板排序

`priority_level` 不是买入信号，不得绕过 signal、wallet、quote、security、paper gates。
