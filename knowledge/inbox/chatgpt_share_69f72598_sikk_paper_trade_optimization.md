# ChatGPT Share 69f72598 摘要：SIKK 纸面交易优化、专业交互、Visual Console 与 Harness

来源链接：`https://chatgpt.com/share/69f72598-cd54-83ab-aa79-699405bda4c4`

## 一句话结论

这份 shared chat 的核心不是单个功能点，而是把 SIKK 从“文件很多、命令很多、广播很多”的状态，升级为：

```text
统一交互入口
统一状态语言
统一索引层
统一 token / position / case file 详情
统一 paper 生命周期复盘
统一 Web / Telegram / CLI 展示协议
统一 Hermes/tmux/Harness 工程执行方式
```

所有内容仍必须保持 SIKK 安全边界：paper-only、不真实 swap、不签名、不广播、不读私钥。

## 关键设计资产

### 1. SIKK-SOL 专业交互系统

SIKK 交互层不是普通 dashboard，而是：

```text
策略验证控制台
+ 纸面仓位复盘系统
+ 钱包结构解释系统
+ 数据质量诊断系统
+ 策略调整反馈系统
```

它必须回答：

```text
当前发生了什么？
为什么系统这么判断？
证据够不够？
这笔纸面交易暴露什么策略问题？
下一步应该修数据、修策略、继续观察，还是退出？
```

### 2. 对象层统一

系统对象应固定为：

```text
System：整个系统
Token：一个代币
Position：一笔纸面仓位
Case File：一笔仓位的实战档案
Review：自动复盘结果
Alert：系统提醒 / 风险事件
```

建议入口：

```text
System：sikkctl status / Telegram /sikk / Web Command Center
Token：sikkctl token <symbol> / 点击 Token / Token Detail
Position：sikkctl position <id> / 点击 Position / Position Detail
Case File：sikkctl case <symbol> / 查看 Case File / Open Case File
Review：sikkctl review / 自动复盘 / Review Lab
Alert：sikkctl alerts / 风险提醒 / Alert Center
```

### 3. 统一索引层

交互入口不能直接读一堆原始文件，应先由统一构建器生成 index：

```text
sikk_unified_view_builder.py
```

建议输出：

```text
data/gmgn_candidates_live_run/index/
  system_index.json
  token_detail_index.json
  position_index.json
  case_file_index.json
  auto_review_index.json
  alert_index.json
```

原则：

```text
原始模块负责产生数据
统一索引负责聚合数据
Web / Telegram / CLI 只读取统一索引
```

### 4. 统一状态语言

仓位状态：

```text
OPEN
CLOSED
PAUSED
EXPIRED
ERROR
```

行为动作：

```text
HOLD
HOLD_WITH_DATA_RISK
EXIT_MONITOR
FORCE_PAPER_EXIT
WAIT_SIGNAL
WAIT_WALLET
WAIT_QUOTE
WAIT_SECURITY
BACKFILL_WALLET_AND_MARKET_CAP
COOLING
IGNORE
```

Case 质量：

```text
HIGH
MEDIUM
LOW
INVALID
```

入场上下文：

```text
EARLY_ENTRY
NORMAL_ENTRY
LATE_ENTRY
CHASE_ENTRY
UNKNOWN_ENTRY
```

复盘结论：

```text
STRATEGY_VALIDATED
PARTIAL_VALIDATION
INCONCLUSIVE
STRATEGY_FAILED
DATA_INSUFFICIENT
```

这些状态必须贯穿 CLI、Telegram、Web badge、日报、case file、auto review。

### 5. Paper Lifecycle Recorder

纸面仓位不能只是 Entry / Exit / PnL，而应成为：

```text
单币实战档案
+ 策略执行日志
+ 入场证据链
+ 出场证据链
+ 失败归因
+ 调整建议
```

生命周期应覆盖：

```text
发现 → 观察 → 盘型识别 → 信号触发 → 钱包结构判断 → quote/security → paper 入场 → 持仓更新 → 退出监控 → paper 退出 → 复盘归因
```

### 6. Paper Entry Snapshot

纸面入场必须记录入场当时证据，而不是事后从当前状态倒推。

关键字段：

```text
paper_entry_at
paper_entry_price
paper_entry_market_cap_usd
paper_entry_amount_sol
paper_entry_amount_usd
paper_token_amount
entry_signal_type
entry_signal_level
wallet_structure_status
wallet_structure_score
quote_check_result
security_check_result
entry_reason
raw_evidence_refs
```

如果这些字段缺失，该 case file 质量应降级，不能用于判断策略有效性。

### 7. Visual Console Pro / v2

网站不是复杂交易后台，也不是实盘控制台，而是：

```text
本地 / VPS 静态专业控制台
读取现有 SIKK 输出数据
展示系统状态、机会、阻断原因、纸面仓位、钱包结构、未入场原因
不执行交易
不接真实 swap
不新增复杂后端
```

页面/分区建议：

```text
Command Center：系统总览
Token Table：候选代币总表
Token Detail：单币详情抽屉/页面
Paper Lab：纸面验证区
Review Lab：复盘实验室
Alert Center：风险与数据质量提醒
```

Token 总表必须可点击进入详情，不能只显示静态表格。

### 8. Telegram 从广播升级为交互面板

Telegram 当前问题是“广播文本”，目标应升级为：

```text
点击 Token → 查看该 token 状态与阻断原因
点击 Position → 查看入场时间、市值、仓位大小、收益、复盘
点击 Case File → 打开完整纸面实战档案
点击 Review → 查看失败归因和策略调整建议
```

### 9. Hermes / tmux / Harness 工程模式

认知模型：

```text
tmux = 进程隔离层
Hermes session = Agent 上下文与任务调度层
项目文件 = 长期记忆层
SIKK_PROJECT_STATE.md = 项目状态记忆
```

不要让一个 AI 在一个超长上下文硬撑。应采用：

```text
主 Agent 调度
子 Agent 独立执行
文件传递上下文
失败后重规划
目录级规则动态注入
审计 → 工作包 → 测试 → 报告 → 提交/回滚
```

建议项目状态文件：

```text
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
SIKK_LESSONS_LEARNED.md
SIKK_CHANGELOG.md
```

### 10. 落地指挥原则

不要再只让 AI 输出方案，要改成闭环命令：

```text
先审计当前文件
列出已有脚本输入/输出
找出缺口
提出最小修改路径
写代码
跑测试
生成样例输出
检查页面是否显示
输出审计报告
```

防表面化提示词核心：

```text
不要只输出概念方案。必须说明：代码写入哪里、读取哪些文件、生成哪些字段、命令怎么跑、输出样例是什么、测试如何证明、页面是否真的显示。保持 paper-only，不接真实 swap。
```

## 可转化为当前系统下一步的 P0/P1

### P0：统一索引与查询层

```text
sikk_unified_view_builder.py
sikk_query.py status/token/position/case/review/alerts
index/*.json
```

目标：Web / Telegram / CLI 不再各自乱读文件。

### P1：Paper Entry Snapshot 与 Case File 质量

```text
paper_entry_snapshot.json
case_files/*.json / *.md
case_quality = HIGH/MEDIUM/LOW/INVALID
```

目标：每笔纸面仓位可复盘，不再只有 PnL。

### P2：Visual Console v2

```text
site/dashboard_data.json
site/index.html
site/app.js
site/style.css
Token Detail Drawer
Paper Lab
Review Lab
Alert Center
```

目标：从“能打开”升级为“能解释”。

### P3：Telegram 交互层

```text
/sikk
Token 按钮
Position 按钮
Case File 按钮
Review 按钮
```

目标：Telegram 不只是广播，而是移动端查询入口。

### P4：Harness 工程治理

```text
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
audits/*.md
tests/*
```

目标：多小时任务可以拆包、验收、回滚。

## 与现有 SIKK 技能/记忆的关系

这份 share 与当前已落地认知高度一致：

```text
sikk_live_run.py 单入口
paper JSON/CSV 同步
wallet daily report 使用新 CSV
live_state/live_board/live_dashboard
site/dashboard_data.json
site/index.html/app.js/style.css
safety 默认关闭真实交易
```

它主要补强的是：

```text
统一索引层
统一交互对象层
Token/Position/Case/Review/Alert 入口
Paper Entry Snapshot
Case File 质量等级
Telegram 交互面板
Hermes/tmux/Harness 工程执行规范
```

## 安全边界

本 share 中所有“交易系统 / 自动化 / 控制台”内容，在 SIKK 当前阶段只能解释为：

```text
paper-only
模拟验证
复盘
观察
风险审计
```

不得解释为：

```text
真实买入
真实卖出
自动跟单
调用 gmgn_swap
签名
广播交易
读取私钥
```
