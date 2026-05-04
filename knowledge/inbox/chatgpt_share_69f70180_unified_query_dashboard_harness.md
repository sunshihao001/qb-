# ChatGPT Share 69f70180｜SIKK 统一查询层、专业面板与 Harness 长任务工程

来源：https://chatgpt.com/share/69f70180-4b3c-83a9-99a3-63fb91e044e9

## 提取说明

本文件由 ChatGPT share 页面内嵌 React stream 提取并筛选，保留与 SIKK-SOL 工程相关的可复用内容：统一查询层、Token 详情入口、专业静态面板、钱包结构接入诊断、纸面仓位 case file 质量、Harness 多 Agent 长任务工作流。

安全处理：如原始内容含凭据形态字段，已替换为 `[REDACTED]`。本文件只作为方法论和工程设计输入，不构成真实交易授权。

## 核心吸收主题

1. SIKK 当前不应再让用户通过多个文件/命令中转才能看到一个代币的纸面仓位详情；应新增统一查询层。
2. 查询入口应支持总览与单币详情：`sikk board` / `sikk token <symbol_or_address>`，以及静态站点中的 Token Detail Drawer / 单币详情抽屉。
3. Dashboard 不是复杂交易后台，而是本地静态专业控制台：读取现有 JSON/CSV/MD，生成 `site/dashboard_data.json/index.html/app.js/style.css`。
4. 面板必须回答：系统是否运行、哪些 token 值得看、为什么没有入场、钱包结构接入率、纸面仓位表现、下一步动作。
5. 当前最大诊断重点之一是钱包结构接入率：例如 48 个 token 里 41 个未接入时，优先修 wallet_structure 链路，而不是盲目放宽 paper entry。
6. LITH 这类 case file 已证明档案方向正确，但如果市值、钱包结构、生命周期、对手盘压力等字段仍是 `待补/UNKNOWN`，不能视作高质量复盘样本。
7. 长任务工程应采用 Harness 模式：Coordinator / Planner / Builder / Verifier / Auditor 通过文件传递状态，避免上下文爆窗和重复造轮子。
8. 所有改造继续保持 paper-only：不真实 swap、不签名、不广播、不读取私钥。

## 筛选后的正文证据

你这个问题问到核心了：**现在流程确实不应该这么麻烦。**

你不应该为了看一个纸面仓位，连续查：

```text
paper_positions_open.json
paper_positions_closed.json
paper_trades.csv
token_status.json
wallet_structure_decision.json
signal_summary.json
quote_security_summary.json
case_file.md
daily_report.md
```

这说明系统缺了一个东西：

# SIKK 统一查询层

也就是：

```text
原始数据很多
  ↓
统一聚合
  ↓
一个页面 / 一个命令 / 一个 token 详情入口
```

现在你遇到的问题不是数据没有，而是：

> **数据分散在太多文件里，没有统一入口。**

---

# 九、给 OpenClaw / Hermes 的精确修复指令

直接复制：

```text
任务：修复 SIKK Paper Case File 的数据质量分层与开放仓位 HOLD 语义问题，以 LITH 为典型样本。

当前问题：
LITH 纸面仓位已经生成 Case File，但大量关键字段缺失：
- discovery_market_cap_usd 缺失
- entry_market_cap_usd 缺失
- wallet_structure_status 缺失
- wallet_structure_score 缺失
- wallet_risk_score 缺失
- counterparty_pressure_score 缺失
- lifecycle_phase UNKNOWN
- dominant_side_intent DATA_INSUFFICIENT

同时该仓位当前仍为 OPEN，paper_action = HOLD，但该 HOLD 并不是强证据支持下的 HOLD，而是因为证据不足尚未触发退出。

目标：
1. 增加 Case Quality Gate。
2. 将关键字段缺失的开放仓位标记为 HOLD_WITH_DATA_RISK。
3. 对最大回撤超过 -20% 且数据质量不足的仓位触发 DATA_RISK_MONITOR。
4. 不允许这类 LOW quality case 进入核心策略统计。
5. 不因为数据缺失直接 FORCE_PAPER_EXIT。

允许修改：
- sikk_paper_lifecycle_recorder.py
- sikk_paper_explanation_builder.py
- sikk_paper_auto_reviewer.py
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/app.js
- tests/test_sikk_paper_auto_reviewer.py
- tests/test_sikk_paper_lifecycle_recorder.py

禁止：
- 不执行真实 swap
- 不新增交易按钮
- 不删除已有模块
- 不改变真实交易逻辑

一、新增 case_quality 字段

允许值：
- HIGH
- MEDIUM
- LOW
- INVALID

规则：
HIGH：
- discovery_market_cap_usd 存在
- entry_market_cap_usd 存在
- signal_market_cap_usd 存在
- entry_wallet_structure_status 存在
- entry_wallet_structure_score 存在
- quote_gate 存在
- paper_entry_time 存在

MEDIUM：
- paper_entry_time 存在
- entry_market_cap_usd 存在
- entry_wallet_structure_status 存在
- 但部分辅助字段缺失

LOW：
- paper_entry_time 存在
- 但 discovery_market_cap_usd 或 entry_market_cap_usd 或 entry_wallet_structure_status 缺失

INVALID：
- paper_entry_time 缺失
- 或 token_address 缺失
- 或 position_id 缺失

二、新增 strategy_review_eligible 字段

规则：
- HIGH：true
- MEDIUM：true，但标记 limited_confidence
- LOW：false
- INVALID：false

三、新增 evidence_missing_fields 字段

记录缺失字段列表，例如：
[
  "discovery_market_cap_usd",
  "entry_market_cap_usd",
  "entry_wallet_structure_status",
  "entry_wallet_structure_score",
  "entry_wallet_risk_score",
  "entry_counterparty_pressure_score"
]

四、修正开放仓位 action

如果仓位 OPEN，且 case_quality = LOW，并且 max_drawdown_pct <= -20：
- paper_action = HOLD_WITH_DATA_RISK
- review_status = DATA_BACKFILL_REQUIRED
- monitor_status = DATA_RISK_MONITOR
- next_action = BACKFILL_WALLET_AND_MARKET_CAP

如果仓位 OPEN，且 case_quality = LOW，但 max_drawdown_pct > -20：
- paper_action = HOLD_WITH_DATA_RISK
- review_status = DATA_BACKFILL_REQUIRED
- monitor_status = NORMAL_MONITOR

五、自然语言解释

Case File 中必须加入：

“当前 HOLD 动作不是强结构支持下的主动持有，而是由于关键证据缺失，系统尚未触发退出条件。该仓位应被标记为 HOLD_WITH_DATA_RISK，并进入数据补齐观察。”

六、自动复盘规则

如果 case_quality = LOW：
- strategy_fit_result = INCONCLUSIVE
- entry_quality_review = 数据不足，无法判断入场质量
- wallet_gate_review = 钱包结构证据缺失
- risk_management_review = 如果出现较深回撤，应进入 DATA_RISK_MONITOR
- strategy_adjustment_suggestion = 补齐发现市值、入场市值、钱包结构和生命周期字段后再评估

七、Dashboard 展示

Visual Console 中：
1. Token Detail Drawer 显示 case_quality。
2. Paper Lab 显示 LOW quality cases 数量。
3. 开放仓位表中，LOW quality + drawdown <= -20 的仓位高亮。
4. 增加 “Data Missing” 标签。
5. LITH 这种样本不能显示为普通 HOLD，必须显示 HOLD_WITH_DATA_RISK。

八、验收命令

cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_paper_lifecycle_recorder.py \
  sikk_paper_explanation_builder.py \
  sikk_paper_auto_reviewer.py \
  sikk_paper_live_runner.py \
  sikk_dashboard_site_builder.py

python3 sikk_paper_auto_reviewer.py \
  --paper-dir data/gmgn_candidates_live_run/paper_live \
  --case-dir data/gmgn_candidates_live_run/paper_live/case_files \
  --output-dir data/gmgn_candidates_live_run/paper_live/auto_reviews

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 - <<'PY'
import json
from pathlib import Path

case_dir = Path("data/gmgn_candidates_live_run/paper_live/case_files")
matches = []
for p in case_dir.glob("*.json"):
    d = json.loads(p.read_text())
    if d.get("token_symbol") == "LITH" or "LITH" in p.name:
        matches.append((p, d))

print("LITH cases:", len(matches))
assert matches, "no LITH case found"

for p, d in matches:
    print("case:", p)
    print("case_quality:", d.get("case_quality"))
    print("strategy_review_eligible:", d.get("strategy_review_eligible"))
    print("evidence_missing_fields:", d.get("evidence_missing_fields"))
    print("paper_action:", d.get("paper_action"))
    print("review_status:", d.get("review_status"))
    print("monitor_status:", d.get("monitor_status"))

    assert d.get("case_quality") in {"LOW", "INVALID", "MEDIUM", "HIGH"}
    assert "evidence_missing_fields" in d

print("LITH quality gate OK")
PY

九、验收标准：
1. LITH 不再显示为普通 HOLD。
2. LITH 如果关键字段缺失，应显示 HOLD_WITH_DATA_RISK。
3. LITH case_quality 应为 LOW 或更低。
4. LITH strategy_review_eligible 应为 false。
5. LITH 的缺失字段必须明确列出。
6. Dashboard 能显示 LITH 的 Data Missing 状态。
7. 不允许因为数据缺失直接 FORCE_PAPER_EXIT。
```

---

可以。现在这个问题要从“面板简陋”进一步细化到：

# Token 不能点击进入详情的问题

这不是小问题。  
专业面板里，**Token 总表不能点进去查看详情**，就会导致你只能看一堆表格，无法判断：

```text
这个 token 为什么 WATCHING？
钱包结构为什么 MISSING？
为什么 BLOCKED？
为什么没有 paper entry？
纸面仓位当前风险是什么？
```

所以 v2 里必须补：

> **Token Detail Drawer / 单币详情抽屉**

不是跳转新页面，第一版建议做右侧抽屉，点击表格里的 token 后，右侧弹出详情。

---

可以。你现在应该在 OpenClaw 里创建的是：

# SIKK-SOL 本地静态可视化网站控制台

不是复杂网站，不是交易后台，不是实盘控制台。

定位：

```text
读取现有 SIKK 输出数据
→ 生成 dashboard_data.json
→ 生成 site/index.html
→ 浏览器打开查看
```

核心目标：

```text
一眼看到：
1. 系统是否正常运行
2. 当前有没有机会
3. 哪些 token PAPER_OPEN / PAPER_READY
4. 哪些 token 被钱包结构阻断
5. 为什么没有新增 paper entry
6. 钱包结构未接入原因
7. 当前纸面仓位盈亏
```

---

# 十二、把 tmux 纳入 SIKK Harness

你的完整 Harness 应该是：

```text
tmux session 隔离
  ↓
Hermes session 隔离
  ↓
/branch 任务分支
  ↓
/kanban 任务拆解
  ↓
delegate_task 子 Agent
  ↓
文件输出报告
  ↓
Verifier 测试
  ↓
Auditor 审计
  ↓
CHANGELOG / LESSONS 更新
```

这样才是专业运用。

---

这笔 LITH 档案已经说明：**Case File 方向是对的，但现在还没达到“可复盘样本”的质量。**

LITH 当前不能用来判断 SIKK-B 是否有效，也不能用来判断钱包结构退出是否正确。它现在只能说明：

```text
纸面仓位记录已生成
持仓 journal 已记录
但核心证据链缺失
所以复盘结论可信度低
```

---

可以实现，而且这应该成为你纸面系统的核心升级之一。

你现在要做的不是单纯“记录交易”，而是建立：

# SIKK Paper Lifecycle Recorder  
# 纸面仓位全生命周期记录与自动复盘系统

目标是：

```text
从代币被发现开始
→ 进入观察
→ 盘型识别
→ 信号触发
→ 钱包结构判断
→ quote/security 检查
→ 纸面入场
→ 持仓更新
→ 风险变化
→ 退出
→ 自动复盘
→ 策略调整建议
```

每一个阶段都用：

```text
结构化数据 + 自然语言解释 + 复盘判断
```

同时保存下来。

---

# 一、你现在需要新增一个核心概念

建议命名为：

```text
Paper Position Case File
纸面仓位实战档案
```

每一笔纸面仓位生成一个独立文件：

```text
data/gmgn_candidates_live_run/paper_live/case_files/<position_id>.json
data/gmgn_candidates_live_run/paper_live/case_files/<position_id>.md
```

JSON 给系统统计用。  
MD 给你人类复盘看。

---

## 第 2 层：长期目标层

目的：让 Hermes 始终知道 SIKK 的边界。

用：

```text
/goal
```

你应该设置成：

```text
/goal

SIKK-SOL 当前长期目标：
把候选发现、K线信号、钱包结构门禁、quote/security、paper runner、日报、事件日志整合成一个可运行、可观察、可复盘的纸面验证系统。

当前重点：
创建本地静态可视化网站控制台，用于观察系统运行、token 状态、钱包结构、未入场原因、纸面仓位和复盘数据。

边界：
- 不执行真实 swap
- 不接自动实盘
- 不删除已有模块
- 不新增复杂后端
- 不使用数据库
- 不做大型 React 项目
- 只做可观察、可筛选、可复盘的专业面板
```

这条 `/goal` 是你的长期约束，避免 AI 乱扩展。

---

这套命令说明：**你现在已经不是“没有系统”，而是系统已经有了运行链路，只是需要做一次命令体系收敛和输出一致性检查。**

当前可以判断为：

```text
SIKK-SOL 已进入：Phase B-0.5
连续运行 + 纸面验证 + 专业面板优化阶段
```

不是概念阶段了。

---

# 一、LITH 当前真实状态判断

## 1. 价格路径

入场价：

```text
0.000021063508
```

最低记录价：

```text
0.00001643109064634298
```

最大记录浮亏：

```text
-21.9926%
```

最新价格：

```text
0.000018142653087750394
```

最新浮亏：

```text
-13.8669%
```

这说明它不是持续恶化，而是：

```text
先从入场价下跌到约 -22%
随后反弹修复到约 -13.87%
```

从最低点到最新点大约修复了：

```text
+10.42%
```

所以当前不能简单说它失败，也不能简单说它该退出。它处于：

```text
浮亏修复中，但结构证据不足
```

---

# 三、LITH 应该被重新标记

我建议 LITH 当前状态改成：

```text
position_status: OPEN
paper_action: HOLD_WITH_DATA_RISK
review_status: DATA_BACKFILL_REQUIRED
case_quality: LOW
evidence_level: E1
strategy_review_eligible: false
```

解释：

```text
仓位仍然开放，但由于市值、钱包结构、生命周期和主导侧证据缺失，该仓位不能纳入高质量策略复盘样本。
当前动作不是强制退出，而是继续观察并要求补齐数据。
```

---

# 四、LITH 应该触发的系统动作

不要直接 FORCE_EXIT。  
但也不能普通 HOLD。  
应该进入：

```text
DATA_RISK_MONITOR
```

触发条件：

```text
data_quality_score 缺失或 < 40
并且 max_drawdown_pct <= -20%
```

LITH 已经出现过：

```text
max_drawdown_pct = -21.9926%
```

所以应该触发：

```text
EXIT_MONITOR_DATA_INSUFFICIENT
```

含义：

```text
不是因为钱包结构恶化退出
而是因为持仓已经出现较深回撤，但关键结构证据缺失，需要提高监控级别
```

---

# 五、LITH 当前复盘应该怎么写

可以这样写进 Case File：

```text
LITH 当前仍为开放纸面仓位。该仓位入场价为 0.000021063508，最近价格为 0.000018142653087750394，当前浮亏约 -13.87%。

持仓过程中最大记录浮亏达到 -21.99%，随后价格从低点有所修复，说明当前并非单边持续恶化状态。但由于发现时市值、入场市值、钱包结构、对手盘压力、生命周期和主导侧心理字段均缺失，本次持仓无法判断是否属于有效 SIKK-B 入场样本。

当前 HOLD 动作应被解释为“证据不足下的继续观察”，而不是强结构支持下的主动持有。该仓位应进入 DATA_RISK_MONITOR，等待补齐钱包结构和市值路径后再进行正式复盘。

当前不能将 LITH 计入高质量策略统计样本。
```

---

# 六、系统需要新增一个 Case Quality Gate

以后每笔 Case File 都要有质量等级。

## Case Quality 分级

| 等级 | 含义 | 是否进入策略统计 |
|---|---|---|
| `HIGH` | 市值、信号、钱包、quote、entry、exit 基本完整 | 可以 |
| `MEDIUM` | 少量字段缺失，但核心入场/退出证据完整 | 可以，但标注 |
| `LOW` | 钱包或市值路径缺失 | 不进入核心统计 |
| `INVALID` | 入场/退出基础字段缺失 | 不进入统计 |

LITH 当前属于：

```text
LOW
```

原因：

```text
市值路径缺失
钱包结构缺失
生命周期缺失
主导侧心理缺失
```

---

# 八、LITH 需要补齐的最小字段

优先补这些，不要一次补全部。

## P0 必补

```text
discovery_market_cap_usd
signal_market_cap_usd
entry_market_cap_usd
current_market_cap_usd
entry_market_cap_change_from_discovery_pct
market_cap_context_status
entry_wallet_structure_status
entry_wallet_structure_score
entry_wallet_risk_score
entry_counterparty_pressure_score
```

## P1 再补

```text
pattern_type
lifecycle_phase
dominant_side_status
dominant_side_intent
chip_transfer_status
quote_gate
security_gate
price_deviation_pct
```

## P2 后补

```text
control_box_high
control_box_low
avwap_price
poc_price
ema20
ema50
volume_state
volatility_state
```

---

# 十、LITH 当前最终定性

现在 LITH 应该这样写：

```text
LITH 当前不是高质量复盘样本。

它是一个开放纸面仓位，当前浮亏 -13.87%，最大记录浮亏约 -21.99%，最近有一定修复。但由于市值路径、钱包结构、生命周期和主导侧心理字段缺失，当前无法判断它是否符合 SIKK-B 高质量入场标准。

当前动作应从 HOLD 修正为 HOLD_WITH_DATA_RISK。
该仓位需要进入 DATA_BACKFILL_REQUIRED，不应纳入核心策略胜率和收益统计。
```

---

# 十一、下一步最重要的不是继续看 LITH PnL

而是修系统：

```text
1. 给每个 case 增加 case_quality
2. 给每个 open position 增加 evidence_missing_fields
3. HOLD 改成 HOLD / HOLD_WITH_DATA_RISK 两种
4. LOW quality case 不进入核心统计
5. Dashboard 高亮数据不足的开放仓位
```

这样你以后不会再被“有记录但没证据”的仓位误导。

---

已读取该纸面实战档案。

LITH 纸面仓位摘要

- 代币：LITH
- 地址：
    GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump
  
- 状态：OPEN
- 策略：SIKK-B 控盘箱体突破回踩
- 信号等级：S4_强确认信号
- 入场时间：2026-04-28 17:46:00 UTC
- 纸面仓位：0.085319 SOL
- 模拟入场价：0.000021063508
- 当前净收益：-13.8669%

当前持仓过程

已记录 5 条 journal。

最近一次：

- 时间：2026-05-03T07:55:27Z
- 当前价格：0.000018142653087750394
- 浮动收益：-13.87%
- 动作：HOLD

持仓变化：

- 2026-05-03T05:58:32Z
  - 价格：0.000017363255431351204
  - 浮盈：-17.5671%
  - 动作：HOLD

- 2026-05-03T06:26:08Z
  - 价格：0.000017455960463229563
  - 浮盈：-17.127%
  - 动作：HOLD

- 2026-05-03T06:54:45Z
  - 价格：0.00001643109064634298
  - 浮盈：-21.9926%
  - 动作：HOLD

- 2026-05-03T07:47:41Z
  - 价格：0.000017836180479
  - 浮盈：-15.3219%
  - 动作：HOLD

- 2026-05-03T07:55:27Z
  - 价格：0.000018142653087750394
  - 浮盈：-13.8669%
  - 动作：HOLD

当前判断

- 仓位仍然 OPEN，尚未退出。
- 当前属于浮亏持仓，但最近两轮从 -21.99% 修复到 -13.87%。
- 系统动作仍为 HOLD，没有触发 EXIT_MONITOR 或 FORCE_PAPER_EXIT。
- 钱包结构、市值上下文、生命周期字段目前大量是 待补 / UNKNOWN，所以这笔仓位的解释质量偏低。

主导侧心理与生命周期

- 主导侧生命周期：UNKNOWN
- 主导侧心理：证据不足 / 待复查
- 筹码控制权：CONTROL_UNCLEAR
- 纸面入场匹配度：DATA_INSUFFICIENT
- 证据等级：E1

解释：

主导侧心理证据不足，不能把盘型直接解释为明确控筹或派发。


复盘结论

当前系统给出的策略复盘：

- 当前结果：LOSS
- 失败归因：UNCLASSIFIED
- 需要复查：
  - 入场是否追高
  - 钱包结构是否误判
  - quote/security 是否延迟
  - 退出是否过慢
  - 入场市值分桶是否需要调整

关键问题

这笔 LITH 档案目前最大问题不是 PnL，而是字段缺失：

- 发现时市值：待补
- 入场市值：待补
- 钱包结构状态：待补
- 钱包结构分：待补
- 钱包风险分：待补
- 对手盘压力：待补
- 生命周期：UNKNOWN
- 主导侧心理：DATA_INSUFFICIENT

所以它现在只能作为纸面持仓记录，不能作为高质量策略复盘样本。

---

# 一、正确目标

以后你要做到：

## 看总览

```bash
sikk board
```

或者直接打开网站。

## 看某个代币

```bash
sikk token AALIEN
```

## 看某个纸面仓位

```bash
sikk position PAPER_AALIEN_20260503_120102
```

## 看最新开放仓位

```bash
sikk open
```

## 看某个 token 的完整复盘

```bash
sikk case AALIEN
```

而不是现在这样东找西找。

---

# 二、系统应该新增一个“统一索引文件”

所有纸面仓位、token、case file、钱包结构、信号状态，都统一写进一个索引：

```text
data/gmgn_candidates_live_run/index/
  token_index.json
  position_index.json
  latest_open_positions.json
  latest_closed_positions.json
  token_detail_index.json
```

这样网站和 CLI 都只读这些索引，不再到处扫文件。

---

# 三、最关键的两个文件

## 1. `position_index.json`

每一笔仓位都在这里能查到。

```json
{
  "PAPER_AALIEN_20260503_120102": {
    "position_id": "PAPER_AALIEN_20260503_120102",
    "token_symbol": "AALIEN",
    "token_address": "...",
    "status": "CLOSED",
    "paper_entry_time": "2026-05-03T12:01:02Z",
    "exit_time": "2026-05-03T13:20:44Z",
    "paper_size_sol": 0.01,
    "entry_price": 0.00004822,
    "exit_price": 0.00037582,
    "entry_market_cap_usd": 126000,
    "exit_market_cap_usd": 980000,
    "net_pnl_pct": 679.39,
    "wallet_structure_status": "WALLET_SUPPORT",
    "exit_trigger": "WALLET_STRUCTURE",
    "exit_reason_code": "STRUCTURE_WEAKENING",
    "case_file_md": "paper_live/case_files/PAPER_AALIEN_20260503_120102.md",
    "case_file_json": "paper_live/case_files/PAPER_AALIEN_20260503_120102.json"
  }
}
```

---

## 2. 看某个 token

```bash
python3 sikkctl.py token AALIEN
```

输出：

```text
$AALIEN 纸面交易档案

当前市值：1.2M
总纸面记录：34
开放仓位：0
已关闭仓位：34
累计收益：+1184.20%
最大单笔收益：+679.39%
最差单笔：-xx%

最新钱包状态：WALLET_BLOCK
最新退出原因：STRUCTURE_WEAKENING

最近仓位：
- PAPER_AALIEN_20260503_120102
  入场时间：12:01:02
  入场市值：126K
  退出时间：13:20:44
  退出市值：980K
  收益：+679.39%
  Case File：paper_live/case_files/xxx.md
```

---

## 4. 打开 case file

```bash
python3 sikkctl.py case AALIEN
```

直接输出最新 case file 路径：

```text
最新 Case File：
data/gmgn_candidates_live_run/paper_live/case_files/PAPER_AALIEN_20260503_120102.md
```

也可以直接：

```bash
sed -n '1,220p' data/gmgn_candidates_live_run/paper_live/case_files/PAPER_AALIEN_20260503_120102.md
```

---

# 五、网站也必须用这个统一索引

Visual Console 现在不要自己到处拼字段。

它应该只读：

```text
site/dashboard_data.json
index/position_index.json
index/token_detail_index.json
```

点击 token 后直接展示：

```text
token_detail_index[token]
```

点击 position 后直接展示：

```text
position_index[position_id]
```

这样页面才不会乱。

---

# 六、你现在真正需要新增的模块

不是再加一堆分析逻辑，而是加：

# `sikk_unified_view_builder.py`

作用：

```text
把分散数据统一成可查询索引
```

输入：

```text
paper_positions_open.json
paper_positions_closed.json
paper_trades.csv
token_status.json
wallet_structure_decision.json
case_files/*.json
events/live_events.jsonl
```

输出：

```text
index/token_index.json
index/position_index.json
index/token_detail_index.json
index/latest_open_positions.json
index/latest_closed_positions.json
```

然后：

# `sikkctl.py`

作用：

```text
一个命令查看所有关键信息
```

---

# 七、你可以直接复制给 OpenClaw / Hermes

```text
任务：为 SIKK-SOL 增加统一查看层，解决查看纸面仓位需要中转多个命令的问题。

当前问题：
现在用户要查看一个纸面仓位，需要分别查看：
- paper_positions_open.json
- paper_positions_closed.json
- paper_trades.csv
- token_status.json
- wallet_structure_decision.json
- signal_summary.json
- quote_security_summary.json
- case_files
- daily_report

这导致查询一个 token 或 position 非常麻烦。

目标：
新增统一索引层和统一 CLI 查询工具，让用户可以通过一个命令或一个页面查看完整信息。

新增文件：
- sikk_unified_view_builder.py
- sikkctl.py
- tests/test_sikk_unified_view_builder.py
- tests/test_sikkctl.py

输出目录：
data/gmgn_candidates_live_run/index/

输出文件：
- token_index.json
- position_index.json
- token_detail_index.json
- latest_open_positions.json
- latest_closed_positions.json

严格边界：
1. 不执行真实 swap。
2. 不新增交易按钮。
3. 不修改真实交易逻辑。
4. 不删除已有模块。
5. 只做数据聚合和查看。

一、sikk_unified_view_builder.py 功能

读取：
- data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
- data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
- data/gmgn_candidates_live_run/paper_live/paper_trades.csv
- data/gmgn_candidates_live_run/tokens/*/token_status.json
- data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json
- data/gmgn_candidates_live_run/paper_live/case_files/*.json
- data/gmgn_candidates_live_run/events/live_events.jsonl

输出：
data/gmgn_candidates_live_run/index/position_index.json
data/gmgn_candidates_live_run/index/token_index.json
data/gmgn_candidates_live_run/index/token_detail_index.json
data/gmgn_candidates_live_run/index/latest_open_positions.json
data/gmgn_candidates_live_run/index/latest_closed_positions.json

二、position_index.json 每个 position 必须包含：

- position_id
- token_symbol
- token_address
- status
- candidate_discovered_at
- discovery_market_cap_usd
- signal_time
- signal_level
- signal_type
- signal_market_cap_usd
- paper_entry_time
- entry_price
- entry_market_cap_usd
- paper_size_sol
- paper_size_usd
- estimated_token_amount
- exit_time
- exit_price
- exit_market_cap_usd
- current_price
- current_market_cap_usd
- net_pnl_pct
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- entry_wallet_structure_status
- exit_wallet_structure_status
- wallet_structure_status
- exit_trigger
- exit_reason_code
- trade_result_type
- failure_type
- main_reason
- next_action
- case_file_json
- case_file_md

三、token_detail_index.json 每个 token 必须包含：

- token_symbol
- token_address
- current_state
- current_market_cap_usd
- latest_wallet_structure_status
- latest_signal_level
- total_positions
- open_positions
- closed_positions
- total_pnl_pct
- avg_pnl_pct
- median_pnl_pct
- best_trade_pct
- worst_trade_pct
- win_rate
- latest_position_id
- latest_case_file_md
- positions
- recent_events

四、sikkctl.py 支持命令：

1. 查看开放仓位：
python3 sikkctl.py open

2. 查看关闭仓位：
python3 sikkctl.py closed --limit 20

3. 查看某个 token：
python3 sikkctl.py token AALIEN

支持 token_symbol 或 token_address。

4. 查看某个 position：
python3 sikkctl.py position PAPER_AALIEN_20260503_120102

5. 查看最新 case file：
python3 sikkctl.py case AALIEN

6. 重建索引：
python3 sikkctl.py rebuild-index

五、sikkctl.py 输出要求：

命令：
python3 sikkctl.py open

必须显示：
- 当前开放仓位数量
- token
- entry_time
- entry_market_cap_usd
- current_market_cap_usd
- paper_size_sol
- unrealized_pnl_pct
- wallet_structure_status
- next_action
- position_id

命令：
python3 sikkctl.py token AALIEN

必须显示：
- 当前市值
- 总仓位数
- 开放仓位数
- 关闭仓位数
- 累计收益
- 胜率
- 最大单笔收益
- 最大单笔亏损
- 最新钱包状态
- 最近 position 列表
- case file 路径

命令：
python3 sikkctl.py position <position_id>

必须显示：
- 发现时间 / 发现市值
- 信号时间 / 信号市值
- 入场时间 / 入场市值
- 入场价格
- 买入规模 SOL
- 估算 token 数量
- 当前市值或退出市值
- 收益
- 入场钱包状态
- 退出钱包状态
- exit_trigger
- exit_reason_code
- trade_result_type
- failure_type
- main_reason
- next_action
- case file 路径

六、Visual Console 集成：

sikk_dashboard_site_builder.py 应该读取：
data/gmgn_candidates_live_run/index/token_detail_index.json
data/gmgn_candidates_live_run/index/position_index.json

Token Detail Drawer 点击 token 时直接显示 token_detail_index 数据。
Position Detail 点击 position 时直接显示 position_index 数据。

七、验收命令：

cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_unified_view_builder.py \
  sikkctl.py

python3 sikk_unified_view_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/index

python3 sikkctl.py open
python3 sikkctl.py closed --limit 10
python3 sikkctl.py token AALIEN

python3 - <<'PY'
import json
from pathlib import Path

base = Path("data/gmgn_candidates_live_run/index")
for name in [
    "position_index.json",
    "token_index.json",
    "token_detail_index.json",
    "latest_open_positions.json",
    "latest_closed_positions.json"
]:
    p = base / name
    print(name, p.exists())
    assert p.exists(), name

pos = json.loads((base / "position_index.json").read_text())
tok = json.loads((base / "token_detail_index.json").read_text())
print("positions:", len(pos))
print("tokens:", len(tok))
print("unified index OK")
PY

八、最终验收标准：
1. 查看开放仓位只需要一个命令：python3 sikkctl.py open。
2. 查看某个 token 只需要一个命令：python3 sikkctl.py token SYMBOL。
3. 查看某个仓位只需要一个命令：python3 sikkctl.py position POSITION_ID。
4. 不需要人工到多个 JSON / CSV 文件里查。
5. Visual Console 点击 token 后能直接显示完整 token 信息。
6. 不允许真实交易。
```

---

# 一、可以实现到什么程度

可以实现成三层：

## 第 1 层：结构化记录

给机器统计用。

例如：

```json
{
  "stage": "PAPER_ENTRY",
  "time": "2026-05-03T12:20:02Z",
  "entry_market_cap_usd": 126000,
  "entry_price": 0.00005356,
  "paper_size_sol": 0.01,
  "wallet_structure_status": "WALLET_SUPPORT",
  "signal_level": "S4"
}
```

---

## S4：钱包结构门禁

回答：

```text
钱包结构是支持、暂停、阻断，还是数据缺失？
早期钱包有没有跑？
同源组有没有同步卖？
对手盘压力多少？
```

字段：

```text
wallet_decision_time
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
early_wallet_remaining_pct
early_wallet_sold_pct
same_source_group_count
same_source_sync_sell_score
high_result_wallet_remaining_pct
late_large_buyer_count
wallet_support_signals
wallet_risk_signals
wallet_reason
```

自然语言：

```text
钱包结构在 {{wallet_decision_time}} 给出 {{wallet_structure_status}}。
结构分为 {{wallet_structure_score}}，风险分为 {{wallet_risk_score}}，对手盘压力为 {{counterparty_pressure_score}}，数据质量为 {{data_quality_score}}。
支持证据包括：{{wallet_support_signals}}。
风险证据包括：{{wallet_risk_signals}}。
综合判断：{{wallet_reason}}。
```

---

## S6：入场决策

回答：

```text
为什么允许入场？
为什么不入场？
如果入场，具体依据是什么？
```

字段：

```text
entry_decision_time
entry_decision
entry_decision_reason
entry_evidence_chain
entry_block_reasons
entry_invalid_conditions
next_action
```

自然语言：

```text
系统在 {{entry_decision_time}} 做出入场决策：{{entry_decision}}。
主要依据是：{{entry_evidence_chain}}。
当前阻断或风险原因是：{{entry_block_reasons}}。
若进入纸面仓位，主要失效条件为：{{entry_invalid_conditions}}。
下一步动作为：{{next_action}}。
```

---

## S7：纸面入场

回答你最关心的问题：

```text
什么时候买？
买了多少？
什么价格买？
什么市值买？
是否追高？
```

字段：

```text
paper_entry_time
entry_price_mode
entry_quote_source
entry_raw_quote_price
entry_simulated_price
entry_slippage_pct
entry_fee_sol
entry_market_cap_usd
entry_liquidity_usd
entry_holder_count
paper_size_sol
paper_size_usd
estimated_token_amount
entry_delay_from_discovery_sec
entry_delay_from_signal_sec
entry_market_cap_change_from_discovery_pct
entry_market_cap_change_from_signal_pct
market_cap_context_status
entry_reason_summary
```

自然语言：

```text
纸面仓位在 {{paper_entry_time}} 入场。
入场价格模式为 {{entry_price_mode}}，quote 来源为 {{entry_quote_source}}。
原始 quote 价格为 {{entry_raw_quote_price}}，加入 {{entry_slippage_pct}}% 模拟滑点后，入场价格为 {{entry_simulated_price}}。
入场时市值约 {{entry_market_cap_usd}} USD，流动性约 {{entry_liquidity_usd}} USD。

本次纸面买入规模为 {{paper_size_sol}} SOL，约 {{paper_size_usd}} USD，估算获得 {{estimated_token_amount}} 个 token。

从发现到入场经过 {{entry_delay_from_discovery_sec}} 秒，从信号触发到入场经过 {{entry_delay_from_signal_sec}} 秒。
入场市值相对发现时变化 {{entry_market_cap_change_from_discovery_pct}}%，入场上下文被标记为 {{market_cap_context_status}}。

入场总结：{{entry_reason_summary}}。
```

---

## S8：持仓监控

回答：

```text
持仓期间发生了什么？
价格、市值、钱包、风险如何变化？
```

每次更新写一行 JSONL：

```text
position_journal/<position_id>.jsonl
```

字段：

```text
time
current_price
current_market_cap_usd
unrealized_pnl_pct
unrealized_pnl_sol
max_floating_profit_pct
max_drawdown_pct
wallet_structure_status
wallet_risk_score
counterparty_pressure_score
price_structure_status
paper_action
monitor_reason
```

自然语言：

```text
{{time}}，仓位当前浮动收益为 {{unrealized_pnl_pct}}%，当前市值约 {{current_market_cap_usd}} USD。
最大浮盈为 {{max_floating_profit_pct}}%，最大回撤为 {{max_drawdown_pct}}%。
钱包结构状态为 {{wallet_structure_status}}，钱包风险分为 {{wallet_risk_score}}，对手盘压力为 {{counterparty_pressure_score}}。
当前动作：{{paper_action}}。
监控原因：{{monitor_reason}}。
```

---

## S11：纸面退出

回答：

```text
什么时候退出？
什么价格退出？
退出时市值多少？
最终收益多少？
```

字段：

```text
exit_time
exit_price
exit_market_cap_usd
exit_liquidity_usd
exit_slippage_pct
exit_fee_sol
net_pnl_pct
net_pnl_sol
trade_result_type
failure_type
exit_wallet_structure_status
exit_wallet_structure_score
exit_wallet_risk_score
exit_counterparty_pressure_score
```

自然语言：

```text
纸面仓位在 {{exit_time}} 退出。
退出价格为 {{exit_price}}，退出时市值约 {{exit_market_cap_usd}} USD，流动性约 {{exit_liquidity_usd}} USD。
本次净收益为 {{net_pnl_pct}}%，约 {{net_pnl_sol}} SOL。
交易结果类型为 {{trade_result_type}}。
失败归因为 {{failure_type}}。
退出时钱包结构状态为 {{exit_wallet_structure_status}}，风险分为 {{exit_wallet_risk_score}}，对手盘压力为 {{exit_counterparty_pressure_score}}。
```

---

# 六、Visual Console 里怎么展示

单币详情里新增：

```text
Lifecycle Timeline
```

显示：

```text
发现 → 初筛 → 盘型 → 信号 → 钱包 → Quote → 入场 → 持仓 → 风险 → 退出 → 复盘
```

每个阶段可点击展开。

例如：

```text
S7 纸面入场
时间：2026-05-03 12:20:02 UTC
入场市值：126K
买入规模：0.01 SOL
入场原因：S4 + WALLET_SUPPORT + quote/security pass
入场上下文：NORMAL_ENTRY
```

还要有：

```text
Open Full Case File
Open Auto Review
```

---

# 七、给 OpenClaw / Hermes 的专业任务书

下面这段可以直接复制。

```text
任务：实现 SIKK Paper Lifecycle Recorder + Auto Review，用于记录每笔纸面仓位从发现到退出的全生命周期数据，并生成自然语言复盘。

当前问题：
当前纸面仓位记录只显示收益、退出原因、钱包状态等结果信息，缺少从代币发现到最终退出的完整阶段性记录。
用户无法系统复盘：
- 什么时间发现
- 发现时市值多少
- 为什么进入观察
- 什么时候识别盘型
- 为什么触发信号
- 钱包结构当时是否支持
- quote/security 是否通过
- 什么时候纸面入场
- 入场时市值多少
- 买了多少 SOL
- 估算获得多少 token
- 入场位置相对箱体 / AVWAP / POC 在哪里
- 持仓过程中风险如何变化
- 什么时候退出
- 退出时市值多少
- 为什么退出
- 这笔交易暴露了策略什么问题
- 下一次应该怎么调整

目标：
为每一笔 paper position 建立完整生命周期记录：
S0_DISCOVERY
S1_INITIAL_FILTER
S2_PATTERN_CLASSIFICATION
S3_SIGNAL_TRIGGER
S4_WALLET_GATE
S5_QUOTE_SECURITY
S6_ENTRY_DECISION
S7_PAPER_ENTRY
S8_POSITION_MONITOR
S9_RISK_CHANGE
S10_EXIT_DECISION
S11_PAPER_EXIT
S12_AUTO_REVIEW

每个阶段必须同时保存：
1. 结构化数据
2. 自然语言解释
3. 风险点
4. 下一步动作
5. 后续复盘依据

允许新增文件：
- sikk_paper_lifecycle_recorder.py
- sikk_paper_explanation_builder.py
- sikk_paper_auto_reviewer.py
- tests/test_sikk_paper_lifecycle_recorder.py
- tests/test_sikk_paper_explanation_builder.py
- tests/test_sikk_paper_auto_reviewer.py

允许修改：
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css

输出目录：
data/gmgn_candidates_live_run/paper_live/case_files/
data/gmgn_candidates_live_run/paper_live/position_journal/
data/gmgn_candidates_live_run/paper_live/auto_reviews/

每笔仓位输出：
- paper_live/case_files/<position_id>.json
- paper_live/case_files/<position_id>.md
- paper_live/position_journal/<position_id>.jsonl
- paper_live/auto_reviews/<position_id>_review.json
- paper_live/auto_reviews/<position_id>_review.md

严格边界：
1. 不执行真实 swap。
2. 不接自动实盘。
3. 不新增交易按钮。
4. 不读取私钥。
5. 不写入私钥。
6. 不删除已有模块。
7. 不改变真实交易逻辑。
8. 只增强 paper 记录、自然语言解释、自动复盘和 dashboard 展示。

一、Lifecycle Record 结构

每笔仓位的 case_files/<position_id>.json 必须包含：

{
  "position_id": "...",
  "token_symbol": "...",
  "token_address": "...",
  "strategy_name": "...",
  "strategy_version": "...",
  "stages": {
    "S0_DISCOVERY": {},
    "S1_INITIAL_FILTER": {},
    "S2_PATTERN_CLASSIFICATION": {},
    "S3_SIGNAL_TRIGGER": {},
    "S4_WALLET_GATE": {},
    "S5_QUOTE_SECURITY": {},
    "S6_ENTRY_DECISION": {},
    "S7_PAPER_ENTRY": {},
    "S8_POSITION_MONITOR": {},
    "S9_RISK_CHANGE": {},
    "S10_EXIT_DECISION": {},
    "S11_PAPER_EXIT": {},
    "S12_AUTO_REVIEW": {}
  },
  "summary": {},
  "review": {},
  "adjustment": {}
}

二、每个 stage 的统一字段

每个阶段必须包含：
- stage_name
- stage_time
- stage_status
- data
- natural_language_summary
- risk_points
- decision
- next_action
- evidence
- missing_fields

三、S0_DISCOVERY 必须记录：
- candidate_discovered_at
- discovery_source
- discovery_price
- discovery_market_cap_usd
- discovery_liquidity_usd
- discovery_holder_count
- discovery_age_minutes
- discovery_volume_5m
- discovery_volume_1h
- discovery_reason
- natural_language_summary

四、S1_INITIAL_FILTER 必须记录：
- initial_filter_time
- initial_filter_result
- min_liquidity_pass
- min_holder_pass
- age_filter_pass
- risk_filter_pass
- initial_filter_reason
- natural_language_summary

五、S2_PATTERN_CLASSIFICATION 必须记录：
- pattern_time
- pattern_type
- lifecycle_phase
- control_box_high
- control_box_low
- control_box_mid
- poc_price
- avwap_price
- ema20
- ema50
- volume_state
- volatility_state
- price_structure_status
- pattern_confidence
- pattern_reason
- natural_language_summary

六、S3_SIGNAL_TRIGGER 必须记录：
- signal_time
- signal_level
- signal_type
- signal_gate
- signal_price
- signal_market_cap_usd
- signal_liquidity_usd
- signal_kline_interval
- signal_reason
- confirmation_conditions
- invalid_level
- invalid_conditions
- natural_language_summary

七、S4_WALLET_GATE 必须记录：
- wallet_decision_time
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- early_wallet_remaining_pct
- early_wallet_sold_pct
- same_source_group_count
- same_source_sync_sell_score
- high_result_wallet_remaining_pct
- late_large_buyer_count
- wallet_support_signals
- wallet_risk_signals
- wallet_reason
- natural_language_summary

八、S5_QUOTE_SECURITY 必须记录：
- quote_check_time
- quote_source
- quote_price
- gmgn_price
- okx_price
- kline_close_price
- price_deviation_pct
- quote_gate
- quote_reason
- security_check_time
- security_gate
- security_risk_level
- security_flags
- security_reason
- natural_language_summary

九、S6_ENTRY_DECISION 必须记录：
- entry_decision_time
- entry_decision
- entry_decision_reason
- entry_evidence_chain
- entry_block_reasons
- entry_invalid_conditions
- next_action
- natural_language_summary

十、S7_PAPER_ENTRY 必须记录：
- paper_entry_time
- entry_price_mode
- entry_quote_source
- entry_raw_quote_price
- entry_simulated_price
- entry_slippage_pct
- entry_fee_sol
- entry_market_cap_usd
- entry_liquidity_usd
- entry_holder_count
- paper_size_sol
- paper_size_usd
- estimated_token_amount
- entry_delay_from_discovery_sec
- entry_delay_from_signal_sec
- entry_market_cap_change_from_discovery_pct
- entry_market_cap_change_from_signal_pct
- market_cap_context_status
- entry_reason_summary
- natural_language_summary

十一、S8_POSITION_MONITOR 必须记录：
- position_journal_path
- first_update_time
- max_profit_time
- max_drawdown_time
- max_floating_profit_pct
- max_drawdown_pct
- current_price
- current_market_cap_usd
- current_wallet_structure_status
- current_wallet_risk_score
- current_counterparty_pressure_score
- natural_language_summary

十二、position_journal/<position_id>.jsonl 每次更新写一行：
- time
- current_price
- current_market_cap_usd
- unrealized_pnl_pct
- unrealized_pnl_sol
- max_floating_profit_pct
- max_drawdown_pct
- wallet_structure_status
- wallet_risk_score
- counterparty_pressure_score
- price_structure_status
- paper_action
- monitor_reason
- natural_language_summary

十三、S9_RISK_CHANGE 必须记录：
- risk_events
每个 risk event 包含：
  - risk_event_time
  - risk_event_type
  - risk_event_level
  - risk_source
  - risk_reason
  - wallet_risk_score_before
  - wallet_risk_score_after
  - counterparty_pressure_before
  - counterparty_pressure_after
  - price_structure_before
  - price_structure_after
  - risk_action
  - natural_language_summary

十四、S10_EXIT_DECISION 必须记录：
- exit_decision_time
- exit_action
- exit_trigger
- exit_reason_code
- exit_reason
- exit_evidence_chain
- wallet_exit_action
- wallet_exit_confidence
- wallet_exit_reason_code
- wallet_exit_evidence
- market_confirmation
- pattern_conflict
- natural_language_summary

十五、S11_PAPER_EXIT 必须记录：
- exit_time
- exit_price
- exit_market_cap_usd
- exit_liquidity_usd
- exit_slippage_pct
- exit_fee_sol
- net_pnl_pct
- net_pnl_sol
- trade_result_type
- failure_type
- exit_wallet_structure_status
- exit_wallet_structure_score
- exit_wallet_risk_score
- exit_counterparty_pressure_score
- natural_language_summary

十六、S12_AUTO_REVIEW 必须记录：
- review_time
- strategy_fit_result
- entry_quality_review
- wallet_gate_review
- exit_quality_review
- risk_management_review
- main_success_factors
- main_failure_factors
- missed_opportunity
- false_exit_flag
- strategy_adjustment_suggestion
- open_questions
- natural_language_summary

十七、自动复盘规则

实现规则版 auto review：

1. 如果 market_cap_context_status = CHASE_ENTRY：
   - 标记 entry_quality_review = 入场偏晚
   - strategy_adjustment_suggestion 增加：限制发现后市值涨幅或提高早期入场条件

2. 如果 market_cap_context_status = LATE_ENTRY 且 net_pnl_pct < 0：
   - 标记 entry_quality_review = 入场滞后导致亏损风险增加

3. 如果 net_pnl_pct < -80：
   - risk_management_review = 风控严重滞后
   - suggestion = 增加最大亏损硬止损或快速下跌保护

4. 如果 FORCE_PAPER_EXIT 后 shadow_hold 60m 继续上涨 > 30：
   - false_exit_flag = true
   - exit_quality_review = 钱包退出可能过早
   - suggestion = 将类似场景从 FORCE_EXIT 降级为 EXIT_MONITOR

5. 如果 S4 信号入场后最大浮盈 < 10 且最大回撤 < -40：
   - strategy_fit_result = S4 信号质量不足
   - suggestion = 增加 quote/security 和钱包确认过滤

6. 如果 entry_wallet_structure_status = WALLET_BLOCK：
   - wallet_gate_review = 入场门禁异常
   - suggestion = 修复状态机，禁止 WALLET_BLOCK 进入 paper entry

7. 如果 entry_wallet_structure_status = MISSING：
   - wallet_gate_review = 钱包数据缺失
   - suggestion = 不允许 MISSING 直接 PAPER_READY，或降低仓位 / 仅观察

8. 如果 net_pnl_pct > 100：
   - trade_result_type = BIG_WIN
   - review 中标记：右尾赢家，需检查是否可复现

9. 如果 net_pnl_pct > 0 但 failure_type 非空：
   - 清空 failure_type
   - 记录 warning：failure_type should not be set for profitable trade

十八、Markdown Case File

case_files/<position_id>.md 必须包含：

# Paper Case File: $TOKEN

1. 基础信息
2. 候选发现
3. 初筛判断
4. 盘型识别
5. 入场信号
6. 钱包结构门禁
7. Quote / Security
8. 入场决策
9. 纸面入场
10. 持仓过程
11. 风险变化
12. 退出决策
13. 纸面退出
14. 自动复盘
15. 策略调整建议
16. 仍需观察的问题

每个章节必须包含：
- 关键结构化数据表
- 自然语言解释
- 风险点
- 下一步动作或复盘结论

十九、Visual Console 集成

Token Detail Drawer 增加：
- Lifecycle Timeline
- Stage Detail
- Open Case File
- Open Auto Review

Paper Lab 增加：
- Recent Case Files
- Strategy Weakness Summary
- Adjustment Suggestions

dashboard_data.json 增加：
- case_files
- auto_reviews
- lifecycle_summary

二十、验收命令

cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_paper_lifecycle_recorder.py \
  sikk_paper_explanation_builder.py \
  sikk_paper_auto_reviewer.py \
  sikk_paper_live_runner.py \
  sikk_dashboard_site_builder.py

python3 sikk_paper_live_runner.py \
  --candidate-states data/gmgn_candidates_live_run/state_machine/candidate_states.json \
  --signal-summary data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json \
  --quote-security-summary data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json \
  --output-dir data/gmgn_candidates_live_run/paper_live

python3 sikk_paper_explanation_builder.py \
  --paper-dir data/gmgn_candidates_live_run/paper_live \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/paper_live/case_files

python3 sikk_paper_auto_reviewer.py \
  --paper-dir data/gmgn_candidates_live_run/paper_live \
  --case-dir data/gmgn_candidates_live_run/paper_live/case_files \
  --output-dir data/gmgn_candidates_live_run/paper_live/auto_reviews

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 - <<'PY'
import json
from pathlib import Path

case_dir = Path("data/gmgn_candidates_live_run/paper_live/case_files")
review_dir = Path("data/gmgn_candidates_live_run/paper_live/auto_reviews")

case_json = list(case_dir.glob("*.json"))
case_md = list(case_dir.glob("*.md"))
review_json = list(review_dir.glob("*_review.json"))
review_md = list(review_dir.glob("*_review.md"))

print("case json:", len(case_json))
print("case md:", len(case_md))
print("review json:", len(review_json))
print("review md:", len(review_md))

assert case_json, "no case json"
assert case_md, "no case md"
assert review_json, "no review json"
assert review_md, "no review md"

sample = json.loads(case_json[0].read_text())
assert "stages" in sample
for s in [
    "S0_DISCOVERY",
    "S1_INITIAL_FILTER",
    "S2_PATTERN_CLASSIFICATION",
    "S3_SIGNAL_TRIGGER",
    "S4_WALLET_GATE",
    "S5_QUOTE_SECURITY",
    "S6_ENTRY_DECISION",
    "S7_PAPER_ENTRY",
    "S8_POSITION_MONITOR",
    "S9_RISK_CHANGE",
    "S10_EXIT_DECISION",
    "S11_PAPER_EXIT",
    "S12_AUTO_REVIEW"
]:
    assert s in sample["stages"], s
    assert "natural_language_summary" in sample["stages"][s], s

md = case_md[0].read_text()
for section in ["候选发现","盘型识别","入场信号","钱包结构门禁","纸面入场","持仓过程","纸面退出","自动复盘","策略调整建议"]:
    assert section in md, section

print("lifecycle recorder and auto review OK")
PY

二十一、最终验收标准：
1. 每笔 paper position 都有 case json。
2. 每笔 paper position 都有 case markdown。
3. 每个 case 包含 S0-S12 全阶段。
4. 每个阶段有自然语言解释。
5. 每笔记录能回答什么时候发现、什么时候入场、入场市值、买了多少、为什么入场、为什么退出。
6. 自动复盘能指出策略不足和调整建议。
7. Visual Console 能打开 Case File。
8. 不允许真实交易。
```

---

对，这才是纸面交易真正应该做的事。

你现在的纸面仓位不能只是：

```text
Token
Entry Price
Exit Price
PnL
Exit Reason
```

这太粗。  
真正有复盘价值的纸面仓位，必须变成：

> **单币实战档案 + 策略执行日志 + 入场证据链 + 出场证据链 + 失败归因 + 调整建议。**

也就是说，每一笔纸面仓位都要能回答：

```text
我为什么发现它？
我什么时候决定观察？
我什么时候入场？
入场时市值多少？
入场位置在哪里？
当时 K线、成交量、钱包结构、quote/security 是什么？
我为什么认为这个位置值得进？
我买了多少？
买入后发生了什么？
什么时候退出？
退出时市值多少？
为什么退出？
如果亏了，亏在哪里？
如果赚了，赚的原因是否符合预期？
下一次策略应该怎么调整？
```

---

## 阶段 4：钱包结构门禁

这是你的核心，必须详细记录。

字段：

```text
wallet_decision_time
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
early_wallet_remaining_pct
early_wallet_sold_pct
same_source_group_count
same_source_sync_sell_score
high_result_wallet_remaining_pct
late_large_buyer_count
wallet_reason
wallet_support_signals
wallet_risk_signals
```

自然语言解释示例：

```text
钱包结构在 2026-05-03 12:19:10 UTC 给出 WALLET_SUPPORT。
结构分 72，风险分 28，对手盘压力 32，数据质量 81。
支持原因是：早期钱包仍保留部分筹码，高结果钱包没有集中退出，同源组没有出现同步卖出。
风险点是：个别早期钱包已有部分止盈，但当前没有形成群体同步派发。
因此钱包结构在入场前不是买入信号，而是“允许纸面验证”的门禁条件。
```

---

## 阶段 6：纸面入场

这是你现在最缺的部分。必须详细。

字段：

```text
paper_entry_time
entry_decision_time
entry_price_mode
entry_quote_source
entry_raw_quote_price
entry_simulated_price
entry_slippage_pct
entry_fee_sol
entry_market_cap_usd
entry_liquidity_usd
entry_holder_count
paper_size_sol
paper_size_usd
estimated_token_amount
entry_position_type
entry_reason_summary
entry_evidence_chain
entry_invalid_conditions
```

自然语言解释必须写成这种：

```text
纸面仓位在 2026-05-03 12:20:02 UTC 入场。
入场模式为 live quote，不使用历史信号价。
原始 quote 价格为 0.000052，加入 3% 模拟滑点后，纸面入场价为 0.00005356。
入场时市值约 126,000 USD，流动性约 33,000 USD。

本次纸面买入规模为 0.01 SOL，按当时 SOL/USD 估算约 1.65 USD，预计获得 30,800 个 token。

入场原因：
1. 盘型符合 SIKK-B 控盘箱体突破回踩。
2. S4 强确认信号触发。
3. 价格回踩未破关键结构位。
4. 钱包结构为 WALLET_SUPPORT，早期钱包没有集中清仓。
5. Quote 与 security 均通过。
6. 入场市值相对发现时上涨 53.6%，属于 NORMAL_ENTRY，不属于严重追高。

失效条件：
1. 跌破 control_box_low。
2. 跌破 AVWAP 后无法收回。
3. 钱包结构从 SUPPORT 转为明确同源组同步退出。
4. 对手盘压力快速升至 75 以上。
```

---

## 阶段 7：持仓过程

纸面仓位不能只记录最终结果，要记录过程。

建议每次更新都写入：

```text
paper_live/position_journal/<position_id>.jsonl
```

每一行记录：

```text
time
current_price
current_market_cap_usd
unrealized_pnl_pct
max_floating_profit_pct
max_drawdown_pct
wallet_structure_status
wallet_risk_score
counterparty_pressure_score
price_structure_status
paper_action
monitor_reason
```

自然语言示例：

```text
2026-05-03 12:35:00 UTC，仓位浮盈达到 +18.2%。
价格仍位于 AVWAP 上方，未跌破控盘箱体中轴。
钱包结构保持 WALLET_SUPPORT，但早期钱包卖出比例小幅上升。
当前动作维持 HOLD，不触发退出。
```

如果进入 EXIT_MONITOR：

```text
2026-05-03 12:48:00 UTC，钱包风险分从 28 上升到 54，对手盘压力从 32 上升到 58。
由于该变化只出现一轮快照，且价格仍未跌破结构位，因此不执行 FORCE_EXIT，而是进入 EXIT_MONITOR。
后续需要观察下一轮钱包 delta 是否继续恶化。
```

---

## 阶段 8：退出与复盘

退出时必须记录：

```text
exit_time
exit_price
exit_market_cap_usd
exit_liquidity_usd
exit_trigger
exit_reason_code
exit_reason
exit_wallet_structure_status
exit_wallet_structure_score
exit_wallet_risk_score
exit_counterparty_pressure_score
net_pnl_pct
net_pnl_sol
trade_result_type
failure_type
exit_evidence_chain
post_exit_review
strategy_adjustment_suggestion
```

自然语言示例：

```text
纸面仓位在 2026-05-03 13:02:12 UTC 退出。
退出价格为 0.000069，退出时市值约 162,000 USD。
本次净收益为 +28.7%。

退出触发来自 WALLET_STRUCTURE。
具体原因是钱包结构风险上升，早期钱包卖出比例持续增加，同源组卖出同步性增强。
但由于退出时价格仍未跌破关键结构位，本次退出被标记为 EXIT_MONITOR_REQUIRED_REVIEW，需要后续 shadow hold 判断是否过早退出。

本次交易结果为 WIN。
failure_type 为空，因为这是盈利交易，不应标记为失败归因。

复盘结论：
本次入场逻辑基本符合 SIKK-B 策略预期。
需要继续验证的问题是：钱包结构退出是否过早。如果退出后 60 分钟价格继续上涨超过 30%，则该笔退出应标记为 FALSE_EXIT。
```

---

# 三、必须新增自然语言解释模块

建议新增文件：

```text
sikk_paper_explanation_builder.py
```

作用：

```text
把结构化字段转换成自然语言解释
```

输入：

```text
paper position json
token_status.json
wallet_structure_decision.json
signal_summary
quote/security summary
position_journal
```

输出：

```text
case_files/<position_id>.md
```

这个模块不做交易判断，只做解释。

---

# 四、单笔 Case File 的完整 Markdown 模板

你要让系统每一笔都生成这种文件：

```markdown
# Paper Case File: $ABC

## 1. 基础信息

| 字段 | 数值 |
|---|---|
| Position ID | PAPER_ABC_20260503_122002 |
| Token | ABC |
| Address | xxx |
| 状态 | CLOSED |
| 策略 | SIKK-B 控盘箱体突破回踩 |
| 信号等级 | S4_强确认信号 |
| 入场时间 | 2026-05-03 12:20:02 UTC |
| 退出时间 | 2026-05-03 13:02:12 UTC |
| 纸面仓位 | 0.01 SOL |
| 入场市值 | 126,000 USD |
| 退出市值 | 162,000 USD |
| 净收益 | +28.7% |

---

## 5. 钱包结构门禁

钱包判断时间：{{wallet_decision_time}}

| 指标 | 数值 |
|---|---:|
| wallet_structure_status | {{wallet_structure_status}} |
| wallet_structure_score | {{wallet_structure_score}} |
| wallet_risk_score | {{wallet_risk_score}} |
| counterparty_pressure_score | {{counterparty_pressure_score}} |
| data_quality_score | {{data_quality_score}} |

钱包结构解释：

{{wallet_explanation}}

支持证据：

{{wallet_support_signals}}

风险证据：

{{wallet_risk_signals}}

---

## F. 钱包证据字段

```text
entry_wallet_structure_status
entry_wallet_structure_score
entry_wallet_risk_score
entry_counterparty_pressure_score
exit_wallet_structure_status
exit_wallet_structure_score
exit_wallet_risk_score
exit_counterparty_pressure_score
wallet_support_signals
wallet_risk_signals
```

---

# 七、Visual Console 必须增加一个 “Case File” 入口

Token Detail Drawer 里必须有：

```text
Open Case File
```

点击后可以打开：

```text
paper_live/case_files/<position_id>.md
```

或者在详情抽屉里直接展示：

```text
Strategy Narrative
```

分区：

```text
1. Timeline
2. Entry Evidence
3. Wallet Evidence
4. Position Progress
5. Exit Evidence
6. Review
7. Adjustment Suggestion
```

---

# 八、给 OpenClaw / Hermes 的完整任务书

你可以直接复制下面这段。

```text
任务：升级 SIKK 纸面交易系统，新增 Paper Position Case File 和自然语言策略复盘解释。

当前问题：
当前 paper report 只能看到总体收益、胜率、退出原因和 token 贡献，但缺少单笔实战细节。
用户无法明确知道：
- 一个代币当前市值多少
- 什么时间进去
- 入场时市值多少
- 买了多少 SOL
- 估算买了多少 token
- 什么价格进
- 什么时候退出
- 退出时市值多少
- 为什么进场
- 为什么退出
- 进场时指标和钱包结构是否支持
- 持仓过程中发生了什么
- 策略到底哪里不足
- 哪个位置需要调整

目标：
把每一笔 paper position 升级成完整 Paper Position Case File。
每笔仓位必须记录发现、盘型、信号、钱包结构、quote/security、入场、持仓过程、退出、复盘和策略调整建议。
同时生成 JSON 结构化文件和 Markdown 自然语言报告。

允许修改：
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- sikk_paper_explanation_builder.py
- sikk_wallet_structure_daily_report.py
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- tests/test_sikk_paper_live_runner.py
- tests/test_sikk_dashboard_site_builder.py
- tests/test_sikk_paper_explanation_builder.py

新增文件：
- sikk_paper_explanation_builder.py
- tests/test_sikk_paper_explanation_builder.py

输出目录：
data/gmgn_candidates_live_run/paper_live/case_files/

每笔仓位输出：
- case_files/<position_id>.json
- case_files/<position_id>.md

严格边界：
1. 不执行真实 swap。
2. 不接自动实盘。
3. 不新增交易按钮。
4. 不读取私钥。
5. 不写入私钥。
6. 不删除已有模块。
7. 不改变真实交易逻辑。
8. 只增强 paper 记录、解释、复盘和展示。
9. 可以增强 paper runner 的字段记录。
10. 可以增强 dashboard 展示。

一、每笔 paper position 必须新增完整时间路径：

- candidate_discovered_at
- signal_time
- wallet_decision_time
- quote_check_time
- paper_entry_time
- first_update_time
- max_profit_time
- max_drawdown_time
- exit_time

二、每笔 paper position 必须新增完整市值路径：

- discovery_market_cap_usd
- signal_market_cap_usd
- wallet_decision_market_cap_usd
- entry_market_cap_usd
- current_market_cap_usd
- exit_market_cap_usd
- entry_market_cap_change_from_discovery_pct
- entry_market_cap_change_from_signal_pct
- exit_market_cap_change_from_entry_pct
- market_cap_context_status

market_cap_context_status 规则：
- EARLY_ENTRY：entry_market_cap_change_from_discovery_pct < 50
- NORMAL_ENTRY：50 <= change < 150
- LATE_ENTRY：150 <= change < 300
- CHASE_ENTRY：change >= 300
- UNKNOWN_ENTRY：缺少 discovery_market_cap_usd 或 entry_market_cap_usd

三、每笔 paper position 必须新增完整价格路径：

- discovery_price
- signal_price
- entry_raw_quote_price
- entry_simulated_price
- current_price
- exit_price
- price_change_from_entry_pct
- max_price_after_entry
- min_price_after_entry

四、每笔 paper position 必须新增仓位规模字段：

- paper_size_sol
- paper_size_usd
- estimated_token_amount
- entry_slippage_pct
- entry_fee_sol
- exit_slippage_pct
- exit_fee_sol
- net_pnl_pct
- net_pnl_sol

五、每笔 paper position 必须新增策略字段：

- strategy_name
- strategy_version
- signal_level
- signal_type
- signal_gate
- pattern_type
- lifecycle_phase
- control_box_high
- control_box_low
- control_box_mid
- poc_price
- avwap_price
- ema20
- ema50
- volume_state
- volatility_state
- price_structure_status
- invalid_level
- entry_reason_summary
- entry_evidence_chain
- invalid_conditions

六、每笔 paper position 必须新增钱包结构字段：

入场时：
- entry_wallet_structure_status
- entry_wallet_structure_score
- entry_wallet_risk_score
- entry_counterparty_pressure_score
- entry_data_quality_score
- entry_early_wallet_remaining_pct
- entry_early_wallet_sold_pct
- entry_same_source_sync_sell_score
- entry_high_result_wallet_remaining_pct
- entry_wallet_support_signals
- entry_wallet_risk_signals
- entry_wallet_reason

退出时：
- exit_wallet_structure_status
- exit_wallet_structure_score
- exit_wallet_risk_score
- exit_counterparty_pressure_score
- exit_data_quality_score
- exit_early_wallet_remaining_pct
- exit_early_wallet_sold_pct
- exit_same_source_sync_sell_score
- exit_high_result_wallet_remaining_pct
- exit_wallet_reason

七、每笔 paper position 必须新增 quote/security 字段：

- quote_gate
- quote_source
- quote_price
- gmgn_price
- okx_price
- kline_close_price
- price_deviation_pct
- quote_reason
- security_gate
- security_risk_level
- security_flags
- security_reason

八、每笔 paper position 必须新增退出字段：

- exit_trigger
- exit_reason
- exit_reason_code
- trade_result_type
- failure_type
- wallet_exit_action
- wallet_exit_confidence
- wallet_exit_reason_code
- wallet_exit_evidence
- false_exit_flag
- avoided_drawdown_pct
- missed_profit_pct

字段语义规则：
1. exit_trigger 表示谁触发退出，例如 WALLET_STRUCTURE / STOP_LOSS / TAKE_PROFIT / TIME_STOP。
2. exit_reason_code 表示具体信号码，例如 STRUCTURE_WEAKENING / SAME_SOURCE_SYNC_EXIT。
3. failure_type 只用于亏损或无效交易，盈利交易不要写 failure_type。
4. 盈利交易如果由钱包结构退出，应记录：
   exit_trigger = WALLET_STRUCTURE
   exit_reason_code = STRUCTURE_WEAKENING
   trade_result_type = BIG_WIN / WIN
   failure_type = null

九、每笔仓位必须新增 position_journal：

路径：
data/gmgn_candidates_live_run/paper_live/position_journal/<position_id>.jsonl

每次更新写一行：
- time
- current_price
- current_market_cap_usd
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- wallet_structure_status
- wallet_risk_score
- counterparty_pressure_score
- price_structure_status
- paper_action
- monitor_reason

十、生成 Paper Case File JSON：

路径：
data/gmgn_candidates_live_run/paper_live/case_files/<position_id>.json

结构必须包含：
- basic
- discovery
- pattern
- signal
- wallet_entry
- quote_security
- entry
- holding_journal
- exit
- review
- adjustment

十一、生成 Paper Case File Markdown：

路径：
data/gmgn_candidates_live_run/paper_live/case_files/<position_id>.md

Markdown 必须包含以下章节：

1. 基础信息
2. 候选发现
3. 盘型判断
4. 入场信号
5. 钱包结构门禁
6. Quote / Security
7. 纸面入场
8. 持仓过程
9. 退出
10. 策略复盘
11. 策略调整建议
12. 需要继续观察的问题

十二、自然语言解释字段必须生成：

- discovery_explanation
- pattern_explanation
- signal_explanation
- wallet_explanation
- quote_security_explanation
- entry_explanation
- holding_explanation
- exit_explanation
- post_trade_review
- strategy_adjustment_suggestion
- open_questions

解释要求：
1. 必须使用自然语言。
2. 不能只堆字段。
3. 必须说明为什么入场。
4. 必须说明入场时位置在哪里。
5. 必须说明入场时市值多少。
6. 必须说明入场是否追高。
7. 必须说明钱包结构是否支持。
8. 必须说明指标上的具体依据。
9. 必须说明退出原因。
10. 必须说明策略哪里可能不足。
11. 必须给出下一步调整建议。

十三、Visual Console 增强：

Token Detail Drawer 和 Paper Lab 必须显示：
- paper_entry_time
- paper_size_sol
- estimated_token_amount
- discovery_market_cap_usd
- signal_market_cap_usd
- entry_market_cap_usd
- current_market_cap_usd
- exit_market_cap_usd
- market_cap_context_status
- entry_reason_summary
- entry_evidence_chain
- exit_reason
- strategy_adjustment_suggestion
- case_file_path

Token Detail Drawer 增加按钮 / 链接：
Open Case File

十四、日报增强：

paper_daily_report 必须新增：
1. Case File Summary
2. Entry Market Cap Context
3. Entry Delay Analysis
4. Strategy Weakness Summary
5. Wallet Exit Effectiveness
6. Right Tail Dependency
7. Token Level Statistics
8. Adjustment Suggestions

十五、验收命令：

cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_paper_live_runner.py \
  sikk_paper_explanation_builder.py \
  sikk_dashboard_site_builder.py

python3 sikk_paper_live_runner.py \
  --candidate-states data/gmgn_candidates_live_run/state_machine/candidate_states.json \
  --signal-summary data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json \
  --quote-security-summary data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json \
  --output-dir data/gmgn_candidates_live_run/paper_live

python3 sikk_paper_explanation_builder.py \
  --paper-dir data/gmgn_candidates_live_run/paper_live \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/paper_live/case_files

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 - <<'PY'
import json
from pathlib import Path

case_dir = Path("data/gmgn_candidates_live_run/paper_live/case_files")
json_files = list(case_dir.glob("*.json"))
md_files = list(case_dir.glob("*.md"))

print("case json:", len(json_files))
print("case md:", len(md_files))

assert json_files, "no case json files"
assert md_files, "no case md files"

sample = json.loads(json_files[0].read_text())
for k in ["basic","discovery","pattern","signal","wallet_entry","quote_security","entry","holding_journal","exit","review","adjustment"]:
    assert k in sample, k

entry = sample["entry"]
required_entry = [
    "paper_entry_time",
    "paper_size_sol",
    "estimated_token_amount",
    "entry_market_cap_usd",
    "market_cap_context_status",
    "entry_explanation"
]
for k in required_entry:
    assert k in entry, k

md = md_files[0].read_text()
for section in ["基础信息","候选发现","盘型判断","入场信号","钱包结构门禁","纸面入场","持仓过程","退出","策略复盘","策略调整建议"]:
    assert section in md, section

print("paper case file OK")
PY

十六、验收标准：
1. 每笔 paper position 都能看到什么时候买。
2. 每笔 paper position 都能看到买了多少 SOL。
3. 每笔 paper position 都能看到估算 token 数量。
4. 每笔 paper position 都能看到发现时市值、信号时市值、入场时市值、当前市值、退出市值。
5. 每笔 paper position 都能看到为什么进场。
6. 每笔 paper position 都能看到进场时指标依据。
7. 每笔 paper position 都能看到钱包结构依据。
8. 每笔 paper position 都能看到为什么退出。
9. 每笔 paper position 都能看到策略复盘。
10. 每笔 paper position 都能看到策略调整建议。
11. Visual Console 能打开对应 Case File。
12. 不允许真实交易。
```

---

# 最短结论

你的判断完全正确：

> **纸面仓位的目标不是展示赚钱，而是暴露策略哪里不足。**

所以每笔仓位必须从“盈亏记录”升级成：

```text
实战档案
+ 策略证据链
+ 入场位置解释
+ 钱包结构解释
+ 市值路径
+ 持仓过程
+ 出场原因
+ 复盘结论
+ 调整建议
```

没有这些细节，纸面测试没有办法真正优化 SIKK。

---

## 2. 当前样本不是 116 个独立样本

报告显示：

```text
总纸面记录：119
涉及代币总数：17
AALIEN 次数：34
WOLVERINE 次数：16
```

这说明你的纸面仓位不是 119 个独立 token 样本，而是：

```text
17 个 token 上重复产生了 119 条仓位记录
```

这会造成一个问题：

> **单个 token 的多次记录会严重放大统计权重。**

例如 AALIEN 34 次，如果它表现好，就会把系统整体收益拉高；WOLVERINE 16 次，如果表现差，也会放大拖累。

所以必须把日报拆成两套统计：

```text
按仓位统计
按 token 统计
```

当前报告主要是按仓位统计，不足够。

---

## 问题 2：钱包结构状态可能被当前状态覆盖

报告里：

```text
钱包结构状态统计：WALLET_BLOCK 112
```

这可能是“退出时状态”，不一定是“入场时状态”。

你必须拆开：

```text
entry_wallet_structure_status
exit_wallet_structure_status
current_wallet_structure_status
```

否则你无法判断：

```text
入场时钱包结构支持，后来恶化？
还是入场时就已经 WALLET_BLOCK，但系统仍然开仓？
```

这是非常关键的数据审计点。

---

## 5. 入场钱包状态 vs 出场钱包状态

新增：

```text
entry_wallet_structure_status
entry_wallet_structure_score
entry_wallet_risk_score
entry_counterparty_pressure_score

exit_wallet_structure_status
exit_wallet_structure_score
exit_wallet_risk_score
exit_counterparty_pressure_score
```

这个是钱包结构审计的核心。

---

# 五、钱包结构接入方式需要改成“三层制”

现在：

```text
wallet_structure → FORCE_PAPER_EXIT
```

应该改成：

```text
wallet_structure_signal
  ↓
wallet_exit_policy
  ↓
paper_action
```

## 第一层：钱包结构信号

只判断事实：

```text
早期钱包是否卖出
同源组是否同步卖出
高结果钱包是否退出
对手盘压力是否上升
数据质量是否足够
```

输出：

```text
wallet_risk_signal
wallet_risk_score
wallet_evidence
```

---

## 第三层：paper runner 执行动作

```text
HOLD → 继续持仓
EXIT_MONITOR → 不退出，提高监控，记录风险
FORCE_PAPER_EXIT → 关闭纸面仓位，并创建 shadow hold
```

---

# 六、FORCE_EXIT 规则需要收紧

当前 96 次 FORCE_EXIT 太多。

建议立刻修改：

```text
默认钱包风险 → EXIT_MONITOR
强证据钱包风险 → FORCE_PAPER_EXIT
```

允许 FORCE_EXIT 的条件：

```text
1. data_quality_score >= 65
2. wallet_exit_confidence >= 80
3. hard_exit_code 命中
4. 至少 2 轮 delta 确认，或同源组同步退出非常明确
5. 市场结构确认恶化
```

hard_exit_code 只允许：

```text
SAME_SOURCE_SYNC_EXIT
ACTIVE_DISTRIBUTION
HIGH_RESULT_GROUP_EXIT
COUNTERPARTY_ABSORBING
WALLET_RISK_WITH_PRICE_BREAKDOWN
```

不允许 FORCE_EXIT：

```text
wallet_structure_status = MISSING
单个钱包卖出
单轮 early_wallet_sold_pct 上升
高 ROI 钱包部分止盈
data_quality_score < 65
长横盘控盘箱体正常换手
二段启动前筹码轮换
```

---

# 八、给 OpenClaw / Hermes 的修复任务书

直接复制：

```text
任务：审计并升级 SIKK 纸面交易统计和钱包结构退出机制。

当前纸面报告显示：
- 总纸面记录：119
- 已关闭仓位：116
- 涉及 token：17
- 胜率：29.31%
- 平均单笔收益：+9.5195%
- 中位数收益：-0.0493%
- 最大单笔收益：+679.3995%
- 钱包结构强制退出：96 / 116
- WALLET_BLOCK：112
- STRUCTURE_WEAKENING：96
- 所有样本都是 S4_强确认信号 + SIKK-B 控盘箱体突破回踩

当前问题：
1. 样本被少数 token 主导，AALIEN 和 lolcat 贡献过大。
2. 119 条仓位记录只涉及 17 个 token，样本不是独立样本。
3. 钱包结构强制退出占比过高，FORCE_PAPER_EXIT 可能过度主导。
4. STRUCTURE_WEAKENING 被同时当作退出原因和失败归因，字段语义混乱。
5. 缺少 paper entry snapshot，无法知道什么时候买、买了多少、什么市值进去。
6. 缺少 entry_wallet_status 和 exit_wallet_status，无法判断入场时是否已风险。
7. 缺少 shadow hold tracking，无法判断 FORCE_EXIT 是否误杀。
8. 当前统计只覆盖 S4 + SIKK-B，不能推导整个系统有效。

目标：
升级纸面交易统计、钱包结构退出策略和 Visual Console Paper Lab，使系统能够判断：
- 收益是否过度依赖少数右尾 token
- 钱包结构强制退出是否有效
- 入场是不是太晚
- 钱包结构在入场时和退出时分别是什么状态
- FORCE_EXIT 是否规避风险还是卖飞
- SIKK-B S4 是否真的具备稳定性

允许修改：
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- sikk_wallet_structure_gate.py
- sikk_wallet_structure_snapshot.py
- sikk_wallet_structure_daily_report.py
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- tests/test_sikk_paper_live_runner.py
- tests/test_sikk_dashboard_site_builder.py
- tests/test_sikk_wallet_structure_gate.py

禁止：
- 不执行真实 swap
- 不修改真实交易逻辑
- 不新增交易按钮
- 不删除已有模块
- 不使用数据库
- 不新增复杂后端

一、修正字段语义

新增并拆分：
- exit_trigger
- exit_reason
- exit_reason_code
- trade_result_type
- failure_type

规则：
1. exit_trigger 表示谁触发退出，例如 WALLET_STRUCTURE / STOP_LOSS / TAKE_PROFIT / TIME_STOP。
2. exit_reason_code 表示具体信号码，例如 STRUCTURE_WEAKENING / SAME_SOURCE_SYNC_EXIT。
3. failure_type 只用于亏损或无效交易，不要把盈利交易标记为 failure。
4. 盈利交易如果由钱包结构退出，应记录：
   exit_trigger = WALLET_STRUCTURE
   exit_reason_code = STRUCTURE_WEAKENING
   trade_result_type = BIG_WIN / WIN
   failure_type = null

二、新增 paper entry snapshot

每笔 paper position 必须记录：
- candidate_discovered_at
- discovery_price
- discovery_market_cap_usd
- discovery_liquidity_usd
- discovery_holder_count
- signal_time
- signal_level
- signal_type
- signal_price
- signal_market_cap_usd
- wallet_decision_time
- entry_wallet_structure_status
- entry_wallet_structure_score
- entry_wallet_risk_score
- entry_counterparty_pressure_score
- paper_entry_time
- entry_price_mode
- entry_quote_source
- entry_raw_quote_price
- entry_simulated_price
- entry_market_cap_usd
- entry_liquidity_usd
- paper_size_sol
- paper_size_usd
- estimated_token_amount
- entry_delay_from_discovery_sec
- entry_delay_from_signal_sec
- entry_market_cap_change_from_discovery_pct
- entry_market_cap_change_from_signal_pct
- market_cap_context_status

market_cap_context_status：
- EARLY_ENTRY：涨幅 < 50%
- NORMAL_ENTRY：50%-150%
- LATE_ENTRY：150%-300%
- CHASE_ENTRY：>=300%
- UNKNOWN_ENTRY：缺少数据

三、新增 exit wallet snapshot

关闭仓位时记录：
- exit_time
- exit_price
- exit_market_cap_usd
- exit_wallet_structure_status
- exit_wallet_structure_score
- exit_wallet_risk_score
- exit_counterparty_pressure_score
- exit_reason
- exit_reason_code
- exit_trigger
- net_pnl_pct
- trade_result_type
- failure_type

四、钱包结构退出改为三层

当前不要让 wallet_structure 直接触发 FORCE_PAPER_EXIT。

新增 wallet_exit_policy：
输入：
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- same_source_sync_sell_score
- early_wallet_sold_pct_delta
- high_result_remaining_pct_delta
- pattern_type
- lifecycle_phase
- price_structure_status
- latest_delta
- current paper position

输出：
- wallet_exit_action：HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
- wallet_exit_confidence
- wallet_exit_reason_code
- wallet_exit_reason
- wallet_exit_evidence

规则：
1. wallet_structure_status = MISSING 不允许 FORCE_PAPER_EXIT。
2. data_quality_score < 65 不允许 FORCE_PAPER_EXIT。
3. 单轮钱包风险默认 EXIT_MONITOR。
4. 长横盘控盘箱体 / 二段启动 / 再吸筹盘型下，早期钱包部分卖出默认 EXIT_MONITOR。
5. 只有 hard_exit_code 才允许 FORCE_PAPER_EXIT：
   - SAME_SOURCE_SYNC_EXIT
   - ACTIVE_DISTRIBUTION
   - HIGH_RESULT_GROUP_EXIT
   - COUNTERPARTY_ABSORBING
   - WALLET_RISK_WITH_PRICE_BREAKDOWN
6. FORCE_PAPER_EXIT 需要：
   - wallet_exit_confidence >= 80
   - data_quality_score >= 65
   - hard_exit_code 命中
   - market_confirmation = true
   - pattern_conflict = true

五、新增 shadow hold tracking

每次 FORCE_PAPER_EXIT 后，创建 shadow hold：
- wallet_exit_trigger_time
- wallet_exit_trigger_type
- force_exit_price
- shadow_tracking_until
- shadow_hold_price_15m
- shadow_hold_price_30m
- shadow_hold_price_60m
- shadow_hold_max_profit_after_exit
- shadow_hold_max_drawdown_after_exit
- false_exit_flag
- avoided_drawdown_pct
- missed_profit_pct

判断：
1. 如果 FORCE_EXIT 后 60m 内继续上涨超过 30%，且没有更大回撤，标记 false_exit_flag = true。
2. 如果 FORCE_EXIT 后出现更大下跌，记录 avoided_drawdown_pct。
3. 每日统计 false_exit_rate。

六、新增样本独立性统计

日报增加：
- position_count
- token_count
- avg_positions_per_token
- max_positions_per_token
- top_1_token_contribution_pct
- top_3_token_contribution_pct
- total_pnl_excluding_top_1_token
- total_pnl_excluding_top_2_tokens
- token_level_win_rate
- token_level_avg_pnl
- token_level_median_pnl

七、新增按市值和入场上下文统计

日报和 dashboard 增加：
按 entry_market_cap_usd 分桶：
- <50K
- 50K-100K
- 100K-200K
- 200K-500K
- 500K-1M
- >1M

每个桶统计：
- trades
- win_rate
- avg_pnl
- median_pnl
- max_drawdown

按 market_cap_context_status 统计：
- EARLY_ENTRY
- NORMAL_ENTRY
- LATE_ENTRY
- CHASE_ENTRY
- UNKNOWN_ENTRY

统计：
- trades
- win_rate
- avg_pnl
- median_pnl

八、Visual Console Paper Lab 升级

Paper Lab 必须展示：
1. 当前开放仓位：
- Token
- Entry Time
- Entry MC
- Current MC
- MC Change %
- Entry Price
- Current Price
- Size SOL
- Token Amount
- PnL %
- Max Profit %
- Max Drawdown %
- Entry Wallet
- Exit Policy
- Market Cap Context

2. 已关闭仓位：
- Token
- Entry Time
- Exit Time
- Entry MC
- Exit MC
- Size SOL
- Net PnL %
- Exit Trigger
- Exit Reason Code
- Trade Result Type
- Failure Type
- Entry Wallet
- Exit Wallet
- Market Cap Context

3. Wallet Exit Effectiveness：
- wallet_force_exit_count
- exit_monitor_count
- true_positive_exit_count
- false_positive_exit_count
- false_exit_rate
- avg_avoided_drawdown_pct
- avg_missed_profit_pct

4. Right Tail Dependency：
- total_pnl
- total_pnl_excluding_top_1_token
- total_pnl_excluding_top_2_tokens
- top_1_token_contribution_pct
- top_3_token_contribution_pct

九、验收命令

cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_paper_live_runner.py \
  sikk_dashboard_site_builder.py \
  sikk_wallet_structure_gate.py \
  sikk_wallet_structure_snapshot.py \
  sikk_wallet_structure_daily_report.py

python3 sikk_paper_live_runner.py \
  --candidate-states data/gmgn_candidates_live_run/state_machine/candidate_states.json \
  --signal-summary data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json \
  --quote-security-summary data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json \
  --output-dir data/gmgn_candidates_live_run/paper_live

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 - <<'PY'
import json
from pathlib import Path

open_p = Path("data/gmgn_candidates_live_run/paper_live/paper_positions_open.json")
closed_p = Path("data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json")
site_p = Path("data/gmgn_candidates_live_run/site/dashboard_data.json")

for p in [open_p, closed_p, site_p]:
    print(p, p.exists())

def rows(path):
    if not path.exists():
        return []
    d = json.loads(path.read_text())
    return d if isinstance(d, list) else d.get("positions", [])

all_rows = rows(open_p) + rows(closed_p)
print("positions:", len(all_rows))

if all_rows:
    r = all_rows[0]
    required = [
        "paper_entry_time",
        "paper_size_sol",
        "entry_market_cap_usd",
        "discovery_market_cap_usd",
        "signal_market_cap_usd",
        "entry_wallet_structure_status",
        "market_cap_context_status",
        "exit_trigger",
        "exit_reason_code",
        "trade_result_type"
    ]
    for k in required:
        print(k, "=", r.get(k))
        assert k in r, k

d = json.loads(site_p.read_text())
assert "paper_metrics" in d
assert "paper_positions" in d
assert "tokens" in d
print("dashboard paper fields OK")
PY

十、验收标准：
1. paper 报告能显示每笔什么时候买。
2. paper 报告能显示每笔买了多少 SOL。
3. paper 报告能显示入场时市值。
4. paper 报告能显示发现时市值、信号时市值、入场时市值。
5. paper 报告能显示入场是不是 EARLY / NORMAL / LATE / CHASE。
6. paper 报告能按 token 聚合统计。
7. paper 报告能剔除 Top 1 / Top 2 贡献后统计。
8. FORCE_EXIT 不再由 wallet_structure 直接触发。
9. MISSING wallet 不再 FORCE_EXIT。
10. 每个 FORCE_EXIT 都有 shadow hold tracking。
11. Visual Console Paper Lab 展示这些字段。
12. 不允许真实交易。
```

---

纸面仓位总览

数据更新时间：2026-05-03T05:27:54Z

- 总纸面记录：119
- 当前开放仓位：3
- 已关闭仓位：116
- 涉及代币总数：17
- 已关闭代币数：16

已关闭仓位表现

- 已关闭记录数：116
- 总收益率累计：+1104.26%
- 平均单笔收益率：+9.5195%
- 中位数收益率：-0.0493%
- 最大单笔收益：+679.3995%
- 最大单笔亏损：-98.3146%

胜负结构

- 盈利笔数：34
- 亏损笔数：58
- 持平笔数：24
- 胜率：29.31%

解读：胜率不高，但靠少数大幅盈利仓位拉高了总收益。中位数接近 0，说明大部分仓位结果偏小幅波动或小亏，小部分极端大盈对总结果贡献很大。

当前开放仓位表现

- 开放仓位：3
- 当前浮动总收益率：-21.5976%
- 平均浮动收益率：-7.1992%
- 中位数浮动收益率：0.0%
- 当前盈利仓位：0
- 当前亏损仓位：1
- 当前持平仓位：2

解读：当前开放仓位整体轻微偏弱，主要由一个浮亏仓位拖累。

仓位规模统计

- 平均仓位：0.1728 SOL
- 中位仓位：0.1857 SOL
- 最小仓位：0.042 SOL
- 最大仓位：0.2 SOL
- 总记录仓位规模累计：20.5664 SOL

注意：这里是纸面记录的仓位规模累计，不代表真实资金投入，也不代表当前净敞口。

止盈触发情况

- 有止盈统计的记录：99
- 总触发止盈次数：18
- 平均每笔触发止盈：0.1818 次
- 最大单笔触发止盈：3 次
- 触发过止盈的记录：8
- 未触发止盈的记录：91

解读：大多数纸面仓位没有走到止盈区，少数强势币贡献了主要收益。

退出原因统计

- 钱包结构触发纸面强制退出：96
- 命中纸面止损：20

钱包动作统计

- FORCE_PAPER_EXIT：96
- 未标记：20

失败归因统计

- STRUCTURE_WEAKENING：96
- 未标记：20

钱包结构状态统计

- WALLET_BLOCK：112
- 未标记：4

解读：当前纸面系统主要是被钱包结构恶化触发退出，而不是传统价格止损触发退出。也就是说，系统现在的风险控制核心已经偏向“钱包结构门禁”，而不是单纯价格线。

信号和策略分布

所有记录都是：

- 信号等级：S4_强确认信号
- 策略类型：SIKK-B 控盘箱体突破回踩

这说明当前纸面样本还比较单一，主要验证的是强确认突破回踩模型，没有覆盖 S3、S2、SX 等更多状态。

贡献最大的代币

正贡献 Top

1. AALIEN
   - 次数：34
   - 总收益率：+1184.2034%
   - 平均收益：+34.8295%
   - 胜率：44.12%
   - 最大单次：+679.3995%

2. lolcat
   - 次数：8
   - 总收益率：+462.6269%
   - 平均收益：+57.8284%
   - 胜率：50.0%
   - 最大单次：+343.0812%

3. UNIPUMP
   - 次数：8
   - 总收益率：+42.9981%
   - 平均收益：+5.3748%
   - 胜率：37.5%

4. CHARITYDROP
   - 次数：5
   - 总收益率：+2.6248%
   - 平均收益：+0.525%
   - 胜率：60.0%

拖累最大的代币

1. HDD
   - 次数：6
   - 总收益率：-108.7725%
   - 平均收益：-18.1288%
   - 胜率：0%

2. GRUMP
   - 次数：1
   - 总收益率：-98.3146%

3. GOBLIEN
   - 次数：1
   - 总收益率：-97.2723%

4. NYAN
   - 次数：1
   - 总收益率：-92.6342%

5. FINE
   - 次数：3
   - 总收益率：-70.1676%

6. WOLVERINE
   - 次数：16
   - 总收益率：-68.4914%
   - 平均收益：-4.2807%
   - 胜率：18.75%

最好和最差单笔

最好单笔

- 代币：AALIEN
- 最终收益率：+679.3995%
- 入场价：0.000048220098
- 退出价：0.00037582719343021165
- 退出原因：钱包结构触发纸面强制退出
- 失败归因：STRUCTURE_WEAKENING

最差单笔

- 代币：GRUMP
- 最终收益率：-98.3146%
- 入场价：0.00024935266
- 退出价：0.0000042025141525633655
- 退出原因：钱包结构触发纸面强制退出
- 失败归因：STRUCTURE_WEAKENING

核心结论

1. 纸面系统整体累计是正的
   - 已关闭累计：+1104.26%
   - 但主要靠 AALIEN、lolcat 这类大波动赢家贡献。

2. 胜率偏低
   - 胜率只有 29.31%
   - 中位数 -0.0493%
   - 说明多数仓位不是稳定盈利，而是靠少数右尾大赚拉起来。

3. 钱包结构退出是主导机制
   - 96 / 116 个关闭仓位来自钱包结构强制退出。
   - 这说明当前系统已经在执行“钱包结构恶化优先退出”的逻辑。

4. 样本信号过于集中
   - 全部是 S4_强确认信号
   - 全部是 SIKK-B 控盘箱体突破回踩
   - 后面需要按 S3/S4、钱包结构状态、失败归因继续拆分，否则不知道到底是哪一层真正有效。

5. 风险点
   - GRUMP、GOBLIEN、NYAN 这类接近归零亏损说明：即使是 S4，也不能单独作为入场充分条件。
   - 钱包结构虽然能触发退出，但有些 token 已经大幅下跌后才退出，说明钱包结构检测和退出时机还需要提前。

---

## 2. EXIT_MONITOR

风险出现，但证据不够强。

动作：

```text
不立刻退出
提高监控频率
禁止加仓
缩短时间止损
观察下一轮钱包 delta
记录风险事件
```

适合：

```text
早期钱包部分卖出
高结果钱包减仓
counterparty_pressure 中等上升
wallet_structure_score 小幅下降
data_quality 不够高
```

---

# 五、哪些情况不应该直接 FORCE_EXIT

这些应该先进入 `EXIT_MONITOR`。

```text
1. 单个早期钱包卖出
2. 早期钱包部分减仓但同源组没同步出货
3. 高 ROI 钱包部分止盈
4. 钱包结构 MISSING
5. data_quality_score < 60
6. 长横盘控盘箱体中的正常换手
7. 二段启动前的筹码轮换
8. price 仍在结构位上方
9. quote/security 没恶化
10. 只有一轮快照出现风险
```

特别注意：

```text
wallet_structure_status = MISSING
```

不能强制退出。  
只能：

```text
EXIT_MONITOR / FIX_DATA_SOURCE
```

---

# 六、你现在应该新增一个退出策略层

叫：

```text
wallet_exit_policy
```

不要让 `wallet_structure_gate` 直接决定退出。

结构应该是：

```text
wallet_structure_decision
  ↓
wallet_exit_policy
  ↓
paper_runner action
```

也就是：

```text
钱包结构判断：风险是什么
退出策略层：该不该退出
paper runner：执行 HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
```

---

# 十、你现在应该怎么修

当前优先修 4 件事。

## 1. 不要让 wallet_structure 直接触发 FORCE_EXIT

改成：

```text
wallet_structure_signal
  ↓
wallet_exit_policy
  ↓
action
```

---

# 十一、给 OpenClaw / Hermes 的修复指令

直接复制：

```text
任务：审计并修正 SIKK-SOL 钱包结构触发 FORCE_PAPER_EXIT 的逻辑。

当前问题：
很多 paper positions 因钱包结构风险直接触发 FORCE_PAPER_EXIT。需要检查这种接入方式是否过于激进。钱包结构不应该默认直接控制退出，而应该通过 wallet_exit_policy 分层判断。

目标：
1. 钱包结构作为风险证据，不直接等于强制退出。
2. 新增 wallet_exit_policy 层。
3. 默认钱包风险触发 EXIT_MONITOR。
4. 只有强证据、多轮 delta、盘型冲突、市场确认时才 FORCE_PAPER_EXIT。
5. 所有 FORCE_EXIT 必须进入后续影子持仓复盘，判断是否误杀。

允许修改：
- sikk_paper_live_runner.py
- sikk_wallet_structure_gate.py
- sikk_wallet_structure_snapshot.py
- sikk_dashboard_site_builder.py
- tests/test_sikk_paper_live_runner.py
- tests/test_sikk_wallet_structure_gate.py

禁止：
- 不执行真实 swap
- 不修改真实交易逻辑
- 不删除已有模块
- 不新增复杂后端

新增 wallet_exit_policy：

输入：
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- same_source_sync_sell_score
- early_wallet_sold_pct_delta
- high_result_remaining_pct_delta
- same_source_group_sold_pct_delta
- pattern_type
- lifecycle_phase
- price_structure_status
- latest_delta
- current paper position

输出：
- wallet_exit_action: HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
- wallet_exit_confidence
- wallet_exit_reason_code
- wallet_exit_reason
- wallet_exit_evidence

规则：
1. data_quality_score < 65 时，不允许 FORCE_PAPER_EXIT，只能 EXIT_MONITOR。
2. 单轮钱包风险不允许 FORCE_PAPER_EXIT，至少需要 2 轮 delta 或明确 hard_exit_code。
3. pattern_type 为 LONG_CONTROL_BOX / SECOND_STAGE_EXPANSION / REACCUMULATION 时，早期钱包部分卖出默认 EXIT_MONITOR，不直接 FORCE_EXIT。
4. 只有以下 hard_exit_code 允许 FORCE_PAPER_EXIT：
   - SAME_SOURCE_SYNC_EXIT
   - ACTIVE_DISTRIBUTION
   - HIGH_RESULT_GROUP_EXIT
   - COUNTERPARTY_ABSORBING
   - WALLET_RISK_WITH_PRICE_BREAKDOWN

FORCE_PAPER_EXIT 条件：
- wallet_exit_confidence >= 80
- data_quality_score >= 65
- hard_exit_code 命中
- pattern_conflict = true
- market_confirmation = true

EXIT_MONITOR 条件：
- early_wallet_sold_pct_delta >= 10
- counterparty_pressure_score >= 55
- high_result_remaining_pct_delta <= -15
- wallet_risk_score_delta >= 15
- data_quality_score 不足
- 只有单轮快照风险

Paper runner 修改：
1. wallet_exit_action = HOLD → 继续持仓
2. wallet_exit_action = EXIT_MONITOR → 不关闭仓位，标记 exit_monitor=true，提高监控频率
3. wallet_exit_action = FORCE_PAPER_EXIT → 关闭纸面仓位，但创建 shadow_hold_tracking

新增 shadow_hold_tracking 字段：
- wallet_exit_trigger_time
- wallet_exit_trigger_type
- force_exit_price
- shadow_tracking_until
- shadow_hold_price_15m
- shadow_hold_price_30m
- shadow_hold_price_60m
- shadow_hold_max_profit_after_exit
- shadow_hold_max_drawdown_after_exit
- false_exit_flag
- avoided_drawdown_pct
- missed_profit_pct

Daily report 增加：
Wallet Exit Effectiveness
- wallet_force_exit_count
- exit_monitor_count
- true_positive_exit_count
- false_positive_exit_count
- false_exit_rate
- avg_avoided_drawdown_pct
- avg_missed_profit_pct
- avg_price_change_after_exit_30m
- avg_price_change_after_exit_60m

Visual Console 增加：
1. Paper Lab 显示 FORCE_EXIT / EXIT_MONITOR 数量
2. 显示 false_exit_rate
3. 单币详情显示 wallet_exit_policy 结果
4. 显示 shadow hold tracking

验收：
1. 钱包结构 MISSING 不再触发 FORCE_PAPER_EXIT。
2. 单轮 early wallet sell 不再触发 FORCE_PAPER_EXIT。
3. LONG_CONTROL_BOX / SECOND_STAGE_EXPANSION 盘型下，部分早期钱包卖出进入 EXIT_MONITOR。
4. SAME_SOURCE_SYNC_EXIT + market confirmation 才 FORCE_PAPER_EXIT。
5. 每次 FORCE_PAPER_EXIT 都有 wallet_exit_reason_code 和 evidence。
6. 每次 FORCE_PAPER_EXIT 都创建 shadow hold tracking。
7. Daily report 能统计 false_exit_rate。
8. 不允许真实交易。
```

---

# 二、paper position 必须新增字段

每一笔纸面仓位必须至少有这些字段。

## 1. 基础信息

```json
{
  "position_id": "PAPER_SOL_ABC_20260503_120102",
  "token_address": "...",
  "token_symbol": "ABC",
  "status": "OPEN",
  "created_at": "2026-05-03T12:01:02Z",
  "updated_at": "2026-05-03T12:05:00Z"
}
```

---

## 4. 钱包结构门禁时信息

```json
{
  "wallet_decision_time": "2026-05-03T11:59:20Z",
  "wallet_structure_status": "WALLET_SUPPORT",
  "wallet_structure_score": 72,
  "wallet_risk_score": 28,
  "counterparty_pressure_score": 32,
  "data_quality_score": 81,
  "wallet_decision_market_cap_usd": 121000,
  "wallet_reason": "早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出"
}
```

这个用于判断：

```text
入场前钱包结构是否真的支持
还是只是价格信号通过
```

---

# 六、dashboard_data.json 必须补字段

每个 paper position 必须变成这样：

```json
{
  "position_id": "PAPER_ABC_001",
  "token_symbol": "ABC",
  "token_address": "...",

  "candidate_discovered_at": "2026-05-03T11:42:10Z",
  "discovery_market_cap_usd": 82000,

  "signal_time": "2026-05-03T11:58:30Z",
  "signal_market_cap_usd": 118000,
  "signal_level": "S3",
  "signal_type": "CONTROL_BOX_BREAKOUT_PULLBACK",

  "wallet_decision_time": "2026-05-03T11:59:20Z",
  "wallet_structure_status": "WALLET_SUPPORT",
  "wallet_structure_score": 72,
  "wallet_risk_score": 28,
  "counterparty_pressure_score": 32,

  "paper_entry_time": "2026-05-03T12:01:02Z",
  "entry_price": 0.000001875,
  "entry_market_cap_usd": 126000,
  "entry_liquidity_usd": 33000,
  "paper_size_sol": 0.01,
  "paper_size_usd": 1.65,
  "estimated_token_amount": 879123.12,

  "entry_delay_from_discovery_sec": 1132,
  "entry_delay_from_signal_sec": 152,
  "entry_market_cap_change_from_discovery_pct": 53.65,
  "entry_market_cap_change_from_signal_pct": 6.78,
  "market_cap_context_status": "NORMAL_ENTRY",

  "current_price": 0.00000210,
  "current_market_cap_usd": 145000,
  "unrealized_pnl_pct": 12.0,
  "max_floating_profit_pct": 28.5,
  "max_drawdown_pct": -7.4,

  "next_action": "HOLD"
}
```

---

# 七、给 OpenClaw / Hermes 的专业任务书

直接复制下面这段。

```text
任务：升级 SIKK Paper Lab 和 paper runner 记录字段，补齐纸面交易入场证据链。

当前问题：
Visual Console 里只能看到纸面仓位盈亏，但看不到：
- 什么时候买的
- 买了多少
- 用什么价格买的
- 当时市值是多少
- 从发现到入场涨了多少
- 从信号到入场涨了多少
- 入场时钱包结构是什么
- 入场时 quote/security 是否通过

这导致纸面测试无法判断是否真的有效，也无法判断是不是追高。

目标：
为每一笔 paper position 增加完整 Paper Entry Snapshot。
纸面仓位必须记录发现时、信号时、钱包门禁时、入场时、当前、出场时的关键数据。

允许修改：
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- tests/test_sikk_paper_live_runner.py
- tests/test_sikk_dashboard_site_builder.py

禁止：
- 不执行真实 swap
- 不修改真实交易逻辑
- 不新增真实交易按钮
- 不删除已有模块
- 不新增复杂后端
- 不使用数据库

一、paper position 必须新增字段：

基础：
- position_id
- token_address
- token_symbol
- status
- created_at
- updated_at

候选发现：
- candidate_discovered_at
- discovery_price
- discovery_market_cap_usd
- discovery_liquidity_usd
- discovery_holder_count
- discovery_source

信号：
- signal_time
- signal_level
- signal_type
- signal_gate
- signal_price
- signal_market_cap_usd
- signal_liquidity_usd
- signal_reason

钱包结构：
- wallet_decision_time
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- wallet_decision_market_cap_usd
- wallet_reason

入场：
- paper_entry_time
- entry_price_mode
- entry_quote_source
- entry_raw_quote_price
- entry_simulated_price
- entry_slippage_pct
- entry_fee_sol
- entry_market_cap_usd
- entry_liquidity_usd
- entry_holder_count
- paper_size_sol
- paper_size_usd
- estimated_token_amount

入场上下文：
- entry_delay_from_discovery_sec
- entry_delay_from_signal_sec
- entry_market_cap_change_from_discovery_pct
- entry_market_cap_change_from_signal_pct
- market_cap_context_status

当前：
- current_price
- current_market_cap_usd
- current_liquidity_usd
- unrealized_pnl_pct
- unrealized_pnl_sol
- max_floating_profit_pct
- max_drawdown_pct

出场：
- exit_time
- exit_reason
- exit_price
- exit_market_cap_usd
- exit_liquidity_usd
- exit_slippage_pct
- exit_fee_sol
- net_pnl_pct
- net_pnl_sol
- failure_type

二、market_cap_context_status 规则：
- EARLY_ENTRY：entry_market_cap_change_from_discovery_pct < 50
- NORMAL_ENTRY：50 <= change < 150
- LATE_ENTRY：150 <= change < 300
- CHASE_ENTRY：change >= 300
- UNKNOWN_ENTRY：缺少 discovery_market_cap_usd 或 entry_market_cap_usd

三、paper_trades.csv 必须新增字段：
- trade_id
- position_id
- token_address
- token_symbol
- side
- event_type
- trade_time
- price
- market_cap_usd
- liquidity_usd
- size_sol
- size_usd
- token_amount
- slippage_pct
- fee_sol
- quote_source
- reason

四、输出文件必须同时支持 JSON 和 CSV：
- paper_positions_open.json
- paper_positions_open.csv
- paper_positions_closed.json
- paper_positions_closed.csv
- paper_trades.csv

五、dashboard_data.json 的 paper_positions 必须包含上述字段。
Visual Console 的 Paper Lab 必须展示：

开放仓位表字段：
- Token
- Entry Time
- Entry MC
- Current MC
- MC Change %
- Entry Price
- Current Price
- Size SOL
- Token Amount
- PnL %
- Max Profit %
- Max Drawdown %
- Wallet Status
- Signal Level
- Market Cap Context
- Next Action

关闭仓位表字段：
- Token
- Entry Time
- Exit Time
- Entry MC
- Exit MC
- Size SOL
- Net PnL %
- Exit Reason
- Failure Type
- Wallet Status
- Market Cap Context

六、Paper Lab 新增统计：
- 按 entry_market_cap_usd 分桶统计胜率和收益：
  <50K
  50K-100K
  100K-200K
  200K-500K
  500K-1M
  >1M

- 按 market_cap_context_status 统计：
  EARLY_ENTRY
  NORMAL_ENTRY
  LATE_ENTRY
  CHASE_ENTRY
  UNKNOWN_ENTRY

- 统计：
  avg_entry_delay_from_discovery_sec
  avg_entry_delay_from_signal_sec
  avg_entry_market_cap_change_from_discovery_pct
  avg_entry_market_cap_change_from_signal_pct

七、单币详情 Drawer 的 Paper 区必须展示：
- paper_entry_time
- paper_size_sol
- estimated_token_amount
- entry_market_cap_usd
- discovery_market_cap_usd
- signal_market_cap_usd
- entry_market_cap_change_from_discovery_pct
- market_cap_context_status
- entry_price_mode
- entry_quote_source
- entry_slippage_pct
- entry_fee_sol

八、验收命令：
cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_paper_live_runner.py \
  sikk_dashboard_site_builder.py

python3 sikk_paper_live_runner.py \
  --candidate-states data/gmgn_candidates_live_run/state_machine/candidate_states.json \
  --signal-summary data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json \
  --quote-security-summary data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json \
  --output-dir data/gmgn_candidates_live_run/paper_live

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 - <<'PY'
import json
from pathlib import Path

p = Path("data/gmgn_candidates_live_run/paper_live/paper_positions_open.json")
if p.exists():
    d = json.loads(p.read_text())
    rows = d if isinstance(d, list) else d.get("positions", [])
    print("open positions:", len(rows))
    if rows:
        r = rows[0]
        required = [
            "paper_entry_time",
            "paper_size_sol",
            "entry_market_cap_usd",
            "discovery_market_cap_usd",
            "signal_market_cap_usd",
            "entry_market_cap_change_from_discovery_pct",
            "market_cap_context_status",
            "estimated_token_amount"
        ]
        for k in required:
            print(k, "=", r.get(k))
            assert k in r, k

p2 = Path("data/gmgn_candidates_live_run/site/dashboard_data.json")
d2 = json.loads(p2.read_text())
pp = d2.get("paper_positions", [])
print("dashboard paper positions:", len(pp))
if pp:
    r = pp[0]
    assert "paper_entry_time" in r
    assert "entry_market_cap_usd" in r
    assert "market_cap_context_status" in r

print("paper entry snapshot OK")
PY

九、验收标准：
1. 每笔 open paper position 能看到什么时候买。
2. 每笔 open paper position 能看到买了多少 SOL。
3. 每笔 open paper position 能看到估算 token 数量。
4. 每笔 open paper position 能看到入场时市值。
5. 每笔 position 能看到发现时市值、信号时市值、入场时市值。
6. 能计算从发现到入场市值涨幅。
7. 能判断 EARLY_ENTRY / NORMAL_ENTRY / LATE_ENTRY / CHASE_ENTRY。
8. Visual Console Paper Lab 能展示这些字段。
9. Token Detail Drawer 能展示单币 paper entry snapshot。
10. 不允许真实交易。
```

---

可以。下面给你一套**可直接复制给 OpenClaw / Hermes 的专业级任务书**。  
不是“第一版简单网站”，而是按多阶段实现一个完整的：

# SIKK-SOL Visual Console Pro

定位：

```text
SIKK-SOL 专业可视化决策控制台
用于展示候选发现、K线信号、钱包结构、quote/security、paper runner、未入场原因、纸面仓位、失败归因、系统健康和复盘结果。
```

核心原则：

```text
可以复杂，但必须分阶段实现。
每一阶段有明确文件、目标、验收命令。
不删除已有模块。
不修改真实交易逻辑。
不接真实 swap。
不做自动实盘。
```

---

# 复制给 Hermes / OpenClaw 的总任务书

```text
任务名称：
SIKK-SOL Visual Console Pro 多阶段建设任务

项目目录：
/root/sikk-gmgn

当前数据目录：
data/gmgn_candidates_live_run

目标：
为 SIKK-SOL 创建一个专业级可视化网站控制台，用于查看系统运行、候选 token、K线信号、钱包结构、quote/security、paper runner、未入场原因、纸面仓位、失败归因和系统健康。

核心定位：
这个网站是观察、筛选、诊断、复盘控制台，不是交易执行后台。

严格边界：
1. 不执行真实 swap。
2. 不新增自动实盘。
3. 不新增交易按钮。
4. 不读取私钥。
5. 不写入私钥。
6. 不删除已有模块。
7. 不破坏 sikk_live_run.py 主入口。
8. 不破坏 paper runner 当前逻辑。
9. 不影响 Telegram 广播。
10. 所有输出统一放在 data/gmgn_candidates_live_run/site/。
11. 可以重构 dashboard 前端，但不能重构交易核心逻辑。
12. 可以新增 builder / frontend / schema / tests。
13. 复杂功能必须分阶段实现，不允许一次性大爆改。

当前允许新增 / 修改文件：
- sikk_dashboard_site_builder.py
- sikk_dashboard_schema.py
- sikk_dashboard_quality_check.py
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- data/gmgn_candidates_live_run/site/dashboard_data.json
- data/gmgn_candidates_live_run/site/AGENTS.md
- tests/test_sikk_dashboard_site_builder.py
- tests/test_sikk_dashboard_schema.py

禁止修改：
- 真实交易执行逻辑
- swap / broadcast 相关代码
- 私钥 / API key / webhook 配置逻辑
- paper runner 的交易判定逻辑，除非只是增加读取展示字段
```

---

# 阶段 0：项目侦察与数据源盘点

```text
阶段 0：Dashboard Readiness Inspection

目标：
先检查当前 SIKK 项目已有输出，不写 UI，不改业务代码。

需要检查的数据源：
1. data/gmgn_candidates_live_run/live_state.json
2. data/gmgn_candidates_live_run/live_board.md
3. data/gmgn_candidates_live_run/tokens/*/token_status.json
4. data/gmgn_candidates_live_run/state_machine/candidate_states.json
5. data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json
6. data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json
7. data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json
8. data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
9. data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
10. data/gmgn_candidates_live_run/paper_live/paper_positions_open.csv
11. data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv
12. data/gmgn_candidates_live_run/paper_live/paper_trades.csv
13. data/gmgn_candidates_live_run/paper_live/strategy_metrics.json
14. data/gmgn_candidates_live_run/paper_live/risk_events.jsonl
15. data/gmgn_candidates_live_run/events/live_events.jsonl
16. data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_*.md
17. data/gmgn_candidates_live_run/paper_live/daily_reports/paper_daily_report_*.md

输出：
- SIKK_DASHBOARD_READINESS_REPORT.md

报告必须包含：
1. 已存在文件
2. 缺失文件
3. 每个 JSON 的字段样本
4. dashboard_data.json 需要合并哪些字段
5. 当前无法展示的原因
6. 当前最影响面板专业性的缺口
7. 不允许修改任何业务代码

验收命令：
cd /root/sikk-gmgn
ls data/gmgn_candidates_live_run
find data/gmgn_candidates_live_run -maxdepth 3 -type f | head -n 100
```

---

# 阶段 1：统一 Dashboard 数据模型

```text
阶段 1：Dashboard Data Schema

目标：
先定义统一 dashboard_data.json 数据模型，解决当前面板散乱的问题。

新增文件：
- sikk_dashboard_schema.py

要求：
定义 dashboard_data.json 的标准结构：

{
  "meta": {},
  "kpi": {},
  "funnel": {},
  "tokens": [],
  "opportunities": [],
  "paper_positions": [],
  "paper_metrics": {},
  "wallet_structure_summary": {},
  "wallet_missing_reasons": [],
  "entry_block_reasons": [],
  "failure_attribution": [],
  "system_health": {},
  "events": []
}

一、meta 字段：
- generated_at
- base_dir
- runtime_status
- data_version
- dashboard_version
- source_files
- stale_warnings

二、kpi 字段：
- token_count
- watching_count
- pause_count
- blocked_count
- paper_ready_count
- paper_open_count
- wallet_support_count
- wallet_pause_count
- wallet_block_count
- wallet_missing_count
- wallet_coverage_count
- wallet_coverage_rate
- open_positions
- closed_positions
- closed_win_rate
- avg_closed_pnl_pct
- max_drawdown_pct
- new_paper_entries_today
- paper_exits_today

三、funnel 字段：
- candidates
- signal_ready
- wallet_support
- wallet_not_missing
- quote_security_pass
- paper_ready
- paper_open
- paper_closed

四、tokens 每个 token 必须包含：
- token_symbol
- token_address
- current_state
- priority_level
- signal_level
- signal_gate
- signal_type
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- quote_gate
- security_gate
- paper_status
- paper_pnl_pct
- main_reason
- next_action
- last_update
- market
- signal
- wallet_structure
- quote
- security
- paper
- recent_events

五、priority_level 规则：
- P0_ACTIVE_POSITION：paper_status 为 OPEN / PAPER_OPEN
- P1_PAPER_READY：current_state 为 PAPER_READY
- P2_STRUCTURE_SUPPORT：wallet_structure_status 为 WALLET_SUPPORT
- P3_WATCHING：current_state 为 WATCHING
- P4_PAUSE：current_state 为 PAUSE
- P5_BLOCKED：current_state 为 BLOCKED 或 wallet_structure_status 为 WALLET_BLOCK
- P6_DATA_MISSING：wallet_structure_status 为 MISSING
- P7_ERROR：current_state 为 ERROR

六、main_reason 规则：
main_reason 不允许为空。
优先级：
1. BLOCKED reason
2. WALLET_BLOCK reason
3. wallet MISSING reason
4. WATCHING watching_reason
5. quote reason
6. security reason
7. paper reason
8. 默认：等待下一轮信号确认

七、next_action 允许值：
- HOLD
- WAIT_SIGNAL
- WAIT_WALLET
- WAIT_QUOTE
- WAIT_SECURITY
- READY_FOR_PAPER
- OPEN_PAPER_POSITION
- EXIT_MONITOR
- FORCE_PAPER_EXIT
- COOLING
- FIX_DATA_SOURCE
- IGNORE

八、next_action 规则：
- PAPER_OPEN → HOLD
- PAPER_READY → OPEN_PAPER_POSITION
- WALLET_SUPPORT 但 signal 未通过 → WAIT_SIGNAL
- wallet MISSING → FIX_DATA_SOURCE
- WALLET_BLOCK / BLOCKED → COOLING
- quote 失败 → WAIT_QUOTE
- security 失败 → WAIT_SECURITY
- PAUSE → WAIT_WALLET
- ERROR → FIX_DATA_SOURCE

验收：
新增 tests/test_sikk_dashboard_schema.py，测试：
1. priority_level 不为空
2. main_reason 不为空
3. next_action 不为空
4. MISSING token 的 next_action = FIX_DATA_SOURCE
5. BLOCKED token 的 next_action = COOLING
6. PAPER_OPEN token 的 next_action = HOLD
```

---

# 阶段 2：Dashboard 数据构建器

```text
阶段 2：Dashboard Site Builder

目标：
实现 sikk_dashboard_site_builder.py，读取现有 SIKK 输出，生成 dashboard_data.json。

新增 / 修改：
- sikk_dashboard_site_builder.py
- tests/test_sikk_dashboard_site_builder.py

运行命令：
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

功能要求：

1. 读取 token_status
从：
data/gmgn_candidates_live_run/tokens/*/token_status.json

2. 读取状态机
从：
data/gmgn_candidates_live_run/state_machine/candidate_states.json

3. 读取信号
从：
data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json

4. 读取 quote/security
从：
data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json

5. 读取钱包结构
从：
data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json

6. 读取 paper open
从：
data/gmgn_candidates_live_run/paper_live/paper_positions_open.json

7. 读取 paper closed
从：
data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
若 json 不存在但 csv 存在，则兼容读取 csv。

8. 读取 strategy_metrics
从：
data/gmgn_candidates_live_run/paper_live/strategy_metrics.json

9. 读取 events
从：
data/gmgn_candidates_live_run/events/live_events.jsonl

10. 读取 risk_events
从：
data/gmgn_candidates_live_run/paper_live/risk_events.jsonl

输出：
data/gmgn_candidates_live_run/site/dashboard_data.json

dashboard_data.json 必须包含：
- meta
- kpi
- funnel
- tokens
- opportunities
- paper_positions
- paper_metrics
- wallet_structure_summary
- wallet_missing_reasons
- entry_block_reasons
- failure_attribution
- system_health
- events

排序规则：
tokens 按以下顺序：
1. PAPER_OPEN
2. PAPER_READY
3. WALLET_SUPPORT
4. PAUSE
5. WATCHING
6. BLOCKED
7. MISSING
8. ERROR

同级内：
1. wallet_structure_score 高的靠前
2. counterparty_pressure_score 低的靠前
3. data_quality_score 高的靠前
4. paper_pnl_pct 高的靠前

opportunities 只包含：
- PAPER_OPEN
- PAPER_READY
- WALLET_SUPPORT
- S3 / S4 signal
- quote/security pass

system_health 必须包含：
- live_state_exists
- token_status_count
- wallet_decision_count
- paper_open_exists
- paper_closed_exists
- strategy_metrics_exists
- events_exists
- dashboard_data_generated_at
- stale_data_warnings

entry_block_reasons 必须统计：
- wallet_structure_missing
- wallet_block
- signal_not_ready
- quote_not_ready
- security_not_ready
- paper_runner_not_called
- state_not_ready
- data_quality_low

验收命令：
cd /root/sikk-gmgn

python3 -m py_compile sikk_dashboard_schema.py sikk_dashboard_site_builder.py

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 160

python3 - <<'PY'
import json
from pathlib import Path
p = Path("data/gmgn_candidates_live_run/site/dashboard_data.json")
d = json.loads(p.read_text())
for k in ["meta","kpi","funnel","tokens","opportunities","paper_positions","entry_block_reasons","system_health","events"]:
    assert k in d, k
print("dashboard_data schema OK")
print("tokens:", len(d["tokens"]))
PY
```

---

# 阶段 3：Visual Console 页面骨架

```text
阶段 3：Visual Console Layout

目标：
实现完整的静态页面骨架，不接后端，不用 React。

新增 / 修改：
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css

页面布局：

一、左侧 Sidebar
导航：
- Command Center
- Opportunities
- Token Explorer
- Paper Lab
- Wallet Structure
- System Health
- Events

二、顶部 Header
显示：
- SIKK-SOL Visual Console Pro
- generated_at
- runtime_status
- auto refresh 状态
- dashboard_version

三、Command Center
包含：
- KPI cards
- Pipeline funnel
- Entry Block Reasons
- System warning banner

四、Opportunities
只显示重点机会：
- PAPER_OPEN
- PAPER_READY
- WALLET_SUPPORT
- S3/S4 signal
- quote/security pass

五、Token Explorer
包含：
- Token 总表
- 搜索框
- current_state 筛选
- wallet_structure_status 筛选
- paper_status 筛选
- reason 搜索
- priority 排序

六、Paper Lab
包含：
- 当前开放仓位
- 已关闭统计
- 胜率
- 平均收益
- 最大回撤
- 失败原因 Top
- paper_positions 表

七、Wallet Structure
包含：
- 钱包结构状态分布
- WALLET_SUPPORT / PAUSE / BLOCK / MISSING 统计
- wallet_missing_reasons
- counterparty_pressure 高风险 token

八、System Health
包含：
- 各数据源是否存在
- token_status 数量
- wallet_decision 数量
- paper files 状态
- events 状态
- stale warning

九、Events
显示最近 live_events.jsonl。

视觉要求：
- 深色专业风格。
- 表格紧凑。
- 卡片化。
- 状态 badge。
- 保持金融终端风格，不要花哨。
- 不加入任何交易按钮。

颜色规则：
- PAPER_OPEN / PAPER_READY：绿色
- WALLET_SUPPORT：青绿色
- WATCHING / PAUSE：黄色
- BLOCKED / WALLET_BLOCK：红色
- MISSING / DATA_QUALITY_LOW：灰色
- ERROR：紫红色
- POSITIVE PNL：绿色
- NEGATIVE PNL：红色

验收：
打开 index.html 后必须看到：
1. 顶部 KPI
2. 漏斗
3. 重点机会
4. Token 总表
5. Paper Lab
6. System Health
7. Events
```

---

# 阶段 4：Token 点击详情 Drawer

```text
阶段 4：Token Detail Drawer

目标：
修复当前 Token 不能点击进去的问题。实现右侧单币详情抽屉。

允许修改：
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- sikk_dashboard_site_builder.py

一、index.html 必须增加：
- detailOverlay
- tokenDetailDrawer
- drawerTokenTitle
- drawerTokenAddress
- drawerCloseBtn
- drawerContent

二、Token 表格要求：
每个 tr 必须有：
class="token-row"
data-token-address="..."

三、app.js 必须实现：
- loadDashboardData()
- renderDashboard()
- renderTokenTable()
- bindTokenClicks()
- openTokenDrawer(tokenAddress)
- closeTokenDrawer()
- renderTokenDetail(token)
- renderSection(title, fields)
- renderField(label, value)
- renderEvents(events)

四、点击行为：
- 点击 token 行打开右侧 drawer
- 点击遮罩关闭 drawer
- 点击 X 关闭 drawer
- 按 Escape 关闭 drawer
- 找不到 token 时显示 Token not found
- 浏览器控制台不能有 JS 报错

五、详情抽屉必须显示：
1. Decision
- current_state
- priority_level
- main_reason
- next_action
- last_update

2. Market
- price
- market_cap
- liquidity
- holder_count
- pool_address

3. Signal
- signal_level
- signal_gate
- signal_type
- invalid_level
- reason

4. Wallet Structure
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- dominant_side_status
- chip_transfer_status
- reason
- support_signals
- risk_signals

5. Quote / Security
- quote_gate
- price_deviation_pct
- quote reason
- security_gate
- risk_level
- security reason

6. Paper
- paper_status
- entry_price
- current_price
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- exit_reason
- failure_type

7. Recent Events
- time
- event_type
- message

验收：
1. Token 总表每一行可点击。
2. 点击后右侧 drawer 打开。
3. Drawer 内容完整。
4. 关闭按钮有效。
5. 遮罩关闭有效。
6. Escape 关闭有效。
7. dashboard_data.json 每个 token 有 market/signal/wallet_structure/quote/security/paper/recent_events。
```

---

# 阶段 5：筛选、排序、搜索、自动刷新

```text
阶段 5：Interactive Controls

目标：
让网站真正可用，而不是只展示数据。

必须实现：

一、Token 搜索
搜索范围：
- token_symbol
- token_address

二、状态筛选
- current_state
- wallet_structure_status
- paper_status
- priority_level

三、Reason 搜索
搜索：
- main_reason
- next_action
- wallet_structure.reason
- quote.reason
- security.reason

四、快速筛选按钮
- Only PAPER_OPEN
- Only PAPER_READY
- Only WALLET_SUPPORT
- Only BLOCKED
- Only MISSING
- Only HIGH COUNTERPARTY

五、排序
支持：
- priority_level
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- paper_pnl_pct
- last_update

六、自动刷新
- 默认每 60 秒重新拉取 dashboard_data.json
- Header 显示 last refresh
- 手动 Refresh 按钮
- 加 ?ts=Date.now() 防止缓存

七、空状态提示
当没有 opportunities 时显示：
当前无 PAPER_READY / PAPER_OPEN / WALLET_SUPPORT token。

当没有 paper positions 时显示：
当前无开放纸面仓位。

验收：
1. 搜索 token 有效。
2. State 筛选有效。
3. Wallet 筛选有效。
4. Paper 筛选有效。
5. Reason 搜索有效。
6. 点击快速筛选有效。
7. 自动刷新不报错。
8. refresh 后点击详情仍然可用。
```

---

# 阶段 6：Paper Lab 专业化

```text
阶段 6：Paper Lab Pro

目标：
让纸面验证区真正能评估策略有效性。

数据来源：
- paper_positions_open.json
- paper_positions_closed.json
- paper_trades.csv
- paper_equity_curve.csv
- strategy_metrics.json
- risk_events.jsonl
- failure_attribution.jsonl

Paper Lab 必须展示：

一、顶部纸面指标：
- open_positions
- closed_positions
- win_rate
- avg_pnl_pct
- median_pnl_pct
- best_trade_pct
- worst_trade_pct
- max_drawdown_pct
- avg_hold_time
- sample_confidence

二、样本可信度规则：
- 0-9 closed：LOW
- 10-19 closed：EARLY
- 20-49 closed：OBSERVABLE
- 50+ closed：MORE_RELIABLE

三、开放仓位表：
- token_symbol
- entry_time
- entry_price
- current_price
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- wallet_structure_status
- next_action

四、关闭仓位表：
- token_symbol
- entry_price
- exit_price
- net_pnl_pct
- exit_reason
- failure_type
- wallet_structure_status

五、失败原因 Top：
- STRUCTURE_FAIL
- LIQUIDITY_FAIL
- QUOTE_FAIL
- SECURITY_FAIL
- MOMENTUM_FAIL
- WALLET_EXIT
- STOP_LOSS
- TIME_STOP
- COUNTERPARTY_ABSORBING

六、按 wallet_structure_status 分组统计：
- WALLET_SUPPORT 胜率
- WALLET_PAUSE 胜率
- WALLET_BLOCK 后续表现
- MISSING 样本表现

验收：
打开 Paper Lab 后，必须能回答：
1. 当前开放仓位是什么
2. 当前盈亏多少
3. 最大回撤多少
4. 关闭样本是否足够
5. 失败主要集中在哪些原因
6. WALLET_SUPPORT 是否表现更好
```

---

# 阶段 7：System Health 与数据质量诊断

```text
阶段 7：System Health

目标：
面板不只看 token，还要诊断系统本身哪里坏了。

System Health 必须显示：

一、文件状态：
- live_state.json exists
- token_status count
- wallet_structure_decision count
- candidate count
- signal summary exists
- quote/security summary exists
- paper open exists
- paper closed exists
- strategy metrics exists
- events exists

二、覆盖率：
- wallet_structure coverage = wallet_decision_count / token_count
- token_status coverage
- quote/security coverage
- signal coverage
- paper output health

三、stale data warning：
如果 dashboard_data generated_at 超过 10 分钟，显示 STALE。
如果 live_state last_update 超过 10 分钟，显示 RUNTIME STALE。
如果 wallet_structure coverage < 80%，显示 WALLET COVERAGE LOW。
如果 paper output 缺失，显示 PAPER OUTPUT MISSING。

四、错误事件：
从 events/live_events.jsonl 读取 ERROR / EXCEPTION / FAILED 类型事件。

五、修复建议：
根据异常输出 next_system_action：
- FIX_WALLET_STRUCTURE_PIPELINE
- FIX_TOKEN_STATUS_BUILDER
- FIX_QUOTE_SECURITY_OUTPUT
- FIX_PAPER_OUTPUT
- CHECK_RUNTIME_LOOP
- CHECK_EVENT_LOG

验收：
System Health 页面必须明确告诉用户：
1. 当前系统是否正常
2. 哪些数据源缺失
3. 哪个模块覆盖率低
4. 下一步修什么
```