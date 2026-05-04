# ChatGPT Share 69f7026b 纸面交易优化方案 - 提取正文

来源: https://chatgpt.com/share/69f7026b-9164-83a9-8702-19d4e95c8d73

标题: Branch · Branch · Branch · Branch · 纸面交易优化方案

说明: 本文件为从 ChatGPT share HTML stream 中提取的项目相关正文节选；已过滤 UI 文案、明显重复短片段和英文内部摘要。用于 SIKK knowledge absorption。


---

## 片段 1 / stream_idx=560 / len=9348


你这个感觉是对的。  
现在问题不是“想法不够”，而是很多内容停在了：

```text
任务书
字段表
概念设计
面板要求
```

但没有落到：

```text
代码实际写入哪里
数据从哪里来
字段如何生成
命令怎么跑
输出样例长什么样
测试如何证明
面板是否真的显示
```

所以你在 Hermes 里要改变使用方式：**不要再让 AI 只输出方案，要强制它每一轮交付可运行结果。**

---

# 一、你现在应该用“落地闭环”来指挥 Hermes

以后每个需求都必须走这个闭环：

```text
需求
  ↓
定位已有文件
  ↓
确认数据来源
  ↓
定义字段 schema
  ↓
修改指定代码
  ↓
生成真实输出
  ↓
跑验收命令
  ↓
展示样例结果
  ↓
修复失败
  ↓
写入 changelog / lessons
```

你不要再问：

```text
这个系统应该怎么设计？
```

要改成问：

```text
请在当前项目中实现这个功能，指出修改哪些文件，运行哪些命令，生成哪些输出，给出真实样例，并通过测试。
```

---

# 二、每个需求必须压成 5 个落地点

以后你给 Hermes 的任务，必须要求它回答并执行这 5 个东西：

```text
1. 要改哪些文件
2. 要新增哪些字段
3. 字段从哪些现有文件读取
4. 跑什么命令能生成结果
5. 用什么测试证明功能真的生效
```

如果缺其中任何一个，就还是“表面”。

---

# 三、针对你现在的 SIKK，最重要的落地原则

## 1. 不要只说“新增字段”

必须要求：

```text
字段必须进入 paper_positions_open.json
字段必须进入 paper_positions_closed.json
字段必须进入 dashboard_data.json
字段必须进入 case_files/<position_id>.json
字段必须进入 case_files/<position_id>.md
字段必须在 Visual Console 显示
```

否则字段只是设计，没有用。

---

## 2. 不要只说“自然语言复盘”

必须要求生成真实文件：

```text
data/gmgn_candidates_live_run/paper_live/case_files/<position_id>.md
```

并且验收：

```bash
sed -n '1,220p' data/gmgn_candidates_live_run/paper_live/case_files/<position_id>.md
```

你要看真实文本，不要看 AI 口头说“已支持”。

---

## 3. 不要只说“面板支持点击”

必须要求：

```text
index.html 有 drawer 容器
app.js 有 openTokenDrawer()
style.css 有 drawer 样式
dashboard_data.json 每个 token 有 detail 字段
浏览器控制台无 JS 报错
```

---

## 4. 不要只说“自动复盘”

必须要求：

```text
auto_reviews/<position_id>_review.json
auto_reviews/<position_id>_review.md
```

并且里面有：

```text
entry_quality_review
wallet_gate_review
exit_quality_review
risk_management_review
strategy_adjustment_suggestion
open_questions
```

---

# 四、你在 Hermes 中要用的标准命令顺序

以后每个具体任务都按这个顺序跑。

## 第 1 步：侦察，不许改代码

```text
/codebase_inspection

任务：只检查，不修改。

检查当前 SIKK 项目中与【这里填需求】相关的文件、字段、输出路径和测试文件。

必须输出：
1. 现有文件有哪些
2. 缺失文件有哪些
3. 当前字段在哪里生成
4. 当前字段在哪里被读取
5. 需要修改哪些文件
6. 最小可落地方案
7. 验收命令

不要写代码。
```

这一轮的作用是防止 AI 乱改。

---

## 第 2 步：让它写实现计划，但必须文件级

```text
/kanban

为【这里填需求】创建任务板。

每个任务必须包含：
1. 修改文件
2. 新增字段
3. 输入数据来源
4. 输出文件
5. 验收命令
6. 测试文件

禁止输出泛泛建议。
禁止新增无关功能。
```

---

## 第 3 步：让 Codex 只改指定文件

```text
/codex

执行任务：【这里填具体小任务】

只允许修改以下文件：
- 文件 1
- 文件 2
- 文件 3

禁止修改：
- 真实交易逻辑
- swap / broadcast 代码
- 私钥 / API key / webhook 逻辑
- 与本任务无关的模块

完成后必须：
1. 说明每个文件改了什么
2. 跑 py_compile
3. 跑指定测试
4. 生成真实输出文件
5. 打印一段真实输出样例
```

---

## 第 4 步：Verifier 必须跑命令

```text
/dogfood

验证刚才实现的功能。

必须执行：
1. py_compile
2. pytest
3. 运行主命令生成输出
4. 检查输出文件存在
5. 抽样打印真实内容
6. 检查字段是否真的存在
7. 检查 dashboard 是否读取到了字段

如果失败：
- 先说明失败原因
- 只修失败点
- 不允许重构整个系统
```

---

## 第 5 步：审计，不许加功能

```text
/codebase_inspection

审计本次修改。

检查：
1. 是否删除已有模块
2. 是否新增真实交易
3. 是否修改 paper runner 核心交易逻辑
4. 是否破坏主入口
5. 是否输出真实文件
6. 是否有测试
7. 是否有样例结果
8. 是否更新 CHANGELOG / LESSONS

输出审计报告，不新增功能。
```

---

# 五、给 Hermes 的“防表面化”总提示词

你可以固定复制这一段到 Hermes：

```text
从现在开始，所有 SIKK 任务必须按“可运行交付”执行。

禁止只输出方案、字段表、建议、架构描述。
每个任务必须落到：
1. 修改文件
2. 输入文件
3. 输出文件
4. 运行命令
5. 测试命令
6. 真实样例输出
7. 验收结果

如果无法实现，必须说明卡在哪个文件、哪个字段、哪个命令，而不是继续扩展设计。

当前边界：
- 不执行真实 swap
- 不新增交易按钮
- 不删除已有模块
- 不改真实交易逻辑
- 不新增无关后端
- 所有结果必须落到 data/gmgn_candidates_live_run 下

当前优先级：
先让纸面仓位可以一键查看完整实战档案：
- 什么时候发现
- 发现时市值
- 什么时候入场
- 入场时市值
- 买了多少 SOL
- 估算多少 token
- 为什么入场
- 持仓过程
- 为什么退出
- 自动复盘
- 策略调整建议
```

---

# 六、把你的需求拆成真正可执行的 6 个 Hermes 小任务

不要一次让它做“完整纸面复盘系统”。  
分成 6 个硬任务。

---

## 任务 1：统一索引层

目标：解决你说的“要中转好多命令”。

复制给 Hermes：

```text
/codex

任务 1：实现 SIKK 统一查看索引层。

新增：
- sikk_unified_view_builder.py
- sikkctl.py

输出：
data/gmgn_candidates_live_run/index/position_index.json
data/gmgn_candidates_live_run/index/token_detail_index.json
data/gmgn_candidates_live_run/index/latest_open_positions.json
data/gmgn_candidates_live_run/index/latest_closed_positions.json

要求：
1. 读取 paper open / closed、case files、token_status、wallet_structure、events。
2. position_index 中每个仓位必须有 entry_time、entry_market_cap、paper_size_sol、estimated_token_amount、current/exit pnl、case_file 路径。
3. sikkctl.py 支持：
   - python3 sikkctl.py open
   - python3 sikkctl.py token LITH
   - python3 sikkctl.py position <position_id>
   - python3 sikkctl.py case LITH

验收：
python3 -m py_compile sikk_unified_view_builder.py sikkctl.py
python3 sikk_unified_view_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/index
python3 sikkctl.py open
python3 sikkctl.py token LITH
```

验收标准：

```text
你能用一条命令看到 LITH 的完整信息。
```

---

## 任务 2：Paper Entry Snapshot

目标：每笔仓位记录什么时候买、买了多少、什么市值买。

```text
/codex

任务 2：补齐 paper position 的 Paper Entry Snapshot。

修改：
- sikk_paper_live_runner.py
- tests/test_sikk_paper_live_runner.py

每笔 paper position 必须新增：
- candidate_discovered_at
- discovery_market_cap_usd
- signal_time
- signal_market_cap_usd
- wallet_decision_time
- paper_entry_time
- entry_price
- entry_market_cap_usd
- paper_size_sol
- paper_size_usd
- estimated_token_amount
- entry_market_cap_change_from_discovery_pct
- market_cap_context_status

输出文件：
- paper_positions_open.json
- paper_positions_closed.json
- paper_positions_open.csv
- paper_positions_closed.csv
- paper_trades.csv

验收：
运行 paper runner 后，抽样打印一个 open position，必须看到以上字段。
```

---

## 任务 3：生命周期 Case File

目标：从发现到退出，每阶段自然语言记录。

```text
/codex

任务 3：实现 Paper Lifecycle Case File。

新增：
- sikk_paper_lifecycle_recorder.py
- sikk_paper_explanation_builder.py
- tests/test_sikk_paper_lifecycle_recorder.py
- tests/test_sikk_paper_explanation_builder.py

输出：
data/gmgn_candidates_live_run/paper_live/case_files/<position_id>.json
data/gmgn_candidates_live_run/paper_live/case_files/<position_id>.md

每个 case 必须包含 S0-S12：
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

每个阶段必须有：
- structured data
- natural_language_summary
- risk_points
- next_action
- missing_fields

验收：
生成至少一个 LITH case file，并用 sed 打印前 220 行。
```

---

## 任务 4：自动复盘

目标：不要只记录，要自动指出问题。

```text
/codex

任务 4：实现规则版自动复盘。

新增：
- sikk_paper_auto_reviewer.py
- tests/test_sikk_paper_auto_reviewer.py

输出：
data/gmgn_candidates_live_run/paper_live/auto_reviews/<position_id>_review.json
data/gmgn_candidates_live_run/paper_live/auto_reviews/<position_id>_review.md

复盘必须包含：
- strategy_fit_result
- entry_quality_review
- wallet_gate_review
- exit_quality_review
- risk_management_review
- main_success_factors
- main_failure_factors
- strategy_adjustment_suggestion
- open_questions

规则：
- CHASE_ENTRY → 入场偏晚
- net_pnl < -80 → 风控严重滞后
- wallet missing → 钱包证据不足
- FORCE_EXIT 后继续涨 → 可能误杀
- BIG_WIN → 标记右尾赢家，检查可复现性

验收：
对 LITH 生成 auto review。
```

---

## 任务 5：Case Quality Gate

目标：区分高质量样本和低质量样本。

```text
/codex

任务 5：实现 Case Quality Gate。

修改：
- sikk_paper_auto_reviewer.py
- sikk_dashboard_site_builder.py
- sikkctl.py

新增字段：
- case_quality
- strategy_review_eligible
- evidence_missing_fields
- review_status
- monitor_status

规则：
HIGH：市值、钱包、entry、quote 基本完整
MEDIUM：核心字段完整但辅助字段缺失
LOW：缺市值路径或钱包结构
INVALID：缺 position_id / token_address / paper_entry_time

如果 OPEN + LOW + max_drawdown <= -20：
paper_action = HOLD_WITH_DATA_RISK
monitor_status = DATA_RISK_MONITOR
next_action = BACKFILL_WALLET_AND_MARKET_CAP

验收：
python3 sikkctl.py token LITH
必须显示 LITH 的 case_quality、缺失字段、HOLD_WITH_DATA_RISK。
```

---

## 任务 6：Visual Console 接入统一索引和 Case File

目标：网站点击就能看，不再查命令。

```text
/claude_design

任务 6：升级 Visual Console，接入统一索引和 Case File。

修改：
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- data/gmgn_candidates_live_run/site/index.html

要求：
1. Dashboard 读取 index/token_detail_index.json 和 index/position_index.json。
2. Token Detail Drawer 显示：
   - positions
   - latest case file
   - case_quality
   - evidence_missing_fields
   - lifecycle timeline
3. Position Detail Drawer 显示：
   - discovery → signal → wallet → entry → monitor → exit → review
4. 增加 Open Case File 链接。
5. LOW quality case 高亮。
6. HOLD_WITH_DATA_RISK 高亮。

验收：
打开网站，点击 LITH，必须直接看到：
- 入场时间
- 入场价格
- 当前浮亏
- case_quality
- 缺失字段
- Open Case File
- 自动复盘摘要
```

---

# 七、你要用“验收样例”逼它落地

以后每个任务都必须让 Hermes 给你贴这种结果：

```text
验收样例：

命令：
python3 sikkctl.py token LITH

输出：
Token=[REDACTED]
Status: OPEN
Entry Time: 2026-04-28 17:46:00 UTC
Entry Price: 0.000021063508
Entry Market Cap: UNKNOWN
Size: 0.085319 SOL
Current PnL: -13.8669%
Case Quality: LOW
Missing Fields:
- discovery_market_cap_usd
- entry_market_cap_usd
- entry_wallet_structure_status
Paper Action: HOLD_WITH_DATA_RISK
Next Action: BACKFILL_WALLET_AND_MARKET_CAP
Case File: data/.../case_files/<id>.md
```

如果它不能给你这个，就是没落地。

---

# 八、Hermes 中要避免的错误用法

不要再这样说：

```text
帮我完善系统
帮我优化面板
帮我加入复盘
帮我做专业化
```

这种太大，容易变成表面。

要这样说：

```text
实现 sikkctl.py token LITH，必须能一条命令输出 LITH 的入场时间、入场价格、仓位大小、当前收益、case_quality、缺失字段、case file 路径。
完成后运行命令并贴出真实输出。
```

越具体越能落地。

---

# 九、你现在最应该先做哪一步

优先级不要错。

现在先做：

```text
P0：sikk_unified_view_builder.py + sikkctl.py
```

因为你现在最大痛点是：

```text
看一个 token 要翻很多文件
```

先解决这个，后面 Case File、自动复盘、Visual Console 都能接同一套索引。

---

# 十、最终操作原则

你以后在 Hermes 里每次都用这句话结尾：

```text
完成后不要只说明方案，必须：
1. 贴出修改文件列表
2. 贴出运行命令
3. 贴出真实输出样例
4. 贴出失败项
5. 如果验收不通过，只修失败点，不允许扩展新功能
```

这句话非常关键。

---

# 最短结论

你现在感觉“很多只是建立了表面”，原因是：

```text
任务没有被强制绑定到文件、命令、输出、测试、样例。
```

在 Hermes 里要改成：

```text
每个需求 = 一个可运行小任务
每个小任务 = 指定文件 + 指定命令 + 指定输出 + 指定测试 + 真实样例
```

当前第一步直接让 Hermes 做：

```text
sikk_unified_view_builder.py
sikkctl.py
```

做到：

```bash
python3 sikkctl.py token LITH
```

一条命令就能看到 LITH 的完整纸面实战信息。


---

## 片段 2 / stream_idx=729 / len=8347


这笔 LITH 档案已经说明：**Case File 方向是对的，但现在还没达到“可复盘样本”的质量。**

LITH 当前不能用来判断 SIKK-B 是否有效，也不能用来判断钱包结构退出是否正确。它现在只能说明：

```text
纸面仓位记录已生成
持仓 journal 已记录
但核心证据链缺失
所以复盘结论可信度低
```

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

# 二、当前最大问题不是亏损，而是“盲持”

系统现在动作仍然是：

```text
HOLD
```

但同时这些字段是缺失的：

```text
发现时市值：待补
入场市值：待补
钱包结构状态：待补
钱包结构分：待补
钱包风险分：待补
对手盘压力：待补
生命周期：UNKNOWN
主导侧心理：DATA_INSUFFICIENT
```

这意味着当前 HOLD 不是基于完整证据链，而是：

```text
因为没有足够证据触发退出，所以默认继续持有
```

这在纸面系统里可以接受，但必须明确标记为：

```text
HOLD_WITH_DATA_RISK
```

而不是普通 `HOLD`。

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

# 七、必须新增两个动作

现在只有 HOLD / EXIT_MONITOR / FORCE_EXIT 还不够。

要新增：

```text
DATA_BACKFILL_REQUIRED
HOLD_WITH_DATA_RISK
```

## 1. `DATA_BACKFILL_REQUIRED`

用于：

```text
case file 生成了，但关键字段缺失
```

## 2. `HOLD_WITH_DATA_RISK`

用于：

```text
仓位继续开放，但持有依据不完整
```

这比普通 HOLD 更准确。

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

## 片段 3 / stream_idx=788 / len=1399


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

## 片段 4 / stream_idx=885 / len=10920


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

## 2. `token_detail_index.json`

每个 token 汇总到一处。

```json
{
  "AALIEN": {
    "token_symbol": "AALIEN",
    "token_address": "...",
    "current_state": "CLOSED",
    "current_market_cap_usd": 1200000,
    "positions": [
      "PAPER_AALIEN_20260503_120102",
      "PAPER_AALIEN_20260503_121500"
    ],
    "total_positions": 34,
    "open_positions": 0,
    "closed_positions": 34,
    "total_pnl_pct": 1184.2,
    "best_trade_pct": 679.39,
    "worst_trade_pct": -12.4,
    "latest_wallet_status": "WALLET_BLOCK",
    "latest_case_file": "paper_live/case_files/PAPER_AALIEN_latest.md"
  }
}
```

这样你查 token 时不用自己拼文件。

---

# 四、再新增一个统一查看命令

建议新增：

```text
sikk_view.py
```

或者更专业一点：

```text
sikkctl.py
```

先不要做复杂命令系统，只做几个实用命令。

---

## 1. 看开放仓位

```bash
python3 sikkctl.py open
```

输出：

```text
当前开放仓位：3

1. $ABC
   入场时间：2026-05-03 12:20:02
   入场市值：126K
   当前市值：145K
   仓位：0.01 SOL
   浮盈：+12.0%
   钱包状态：WALLET_SUPPORT
   下一步：HOLD
   查看详情：python3 sikkctl.py token ABC

2. $XYZ
   入场时间：...
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

## 3. 看某个仓位

```bash
python3 sikkctl.py position PAPER_AALIEN_20260503_120102
```

输出：

```text
仓位：PAPER_AALIEN_20260503_120102
Token：AALIEN
状态：CLOSED

发现时间：2026-05-03 11:42:10
发现市值：82K

信号时间：2026-05-03 11:58:30
信号市值：118K
信号等级：S4
策略：SIKK-B 控盘箱体突破回踩

入场时间：2026-05-03 12:01:02
入场市值：126K
入场价格：0.00004822
买入规模：0.01 SOL
估算 token 数量：xxx

退出时间：2026-05-03 13:20:44
退出市值：980K
退出价格：0.00037582
收益：+679.39%

入场原因：
- S4 强确认
- 控盘箱体突破回踩
- 钱包结构允许
- quote/security 通过

退出原因：
- 钱包结构触发
- 结构风险上升

复盘：
- 这是一笔右尾大赢家
- 需要检查是否可复现
- 退出后是否卖飞需要 shadow hold 验证
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

# 八、再加一个最实用命令：`sikkctl.py latest`

你每天最常用应该是：

```bash
python3 sikkctl.py latest
```

输出：

```text
SIKK 最新状态

开放仓位：3
最新入场：ABC，12:20，入场市值 126K，当前浮盈 +12%
最新退出：AALIEN，收益 +679%，退出原因 WALLET_STRUCTURE
最大风险：XYZ，浮亏 -21%，钱包状态 EXIT_MONITOR
当前最值得看：DEF，PAPER_READY，WALLET_SUPPORT
```

这个比看完整报告更方便。

---

# 九、为什么以前会这么麻烦

因为现在系统是工程模块优先：

```text
候选模块
信号模块
钱包模块
quote 模块
paper 模块
日报模块
dashboard 模块
```

但你缺的是用户视角：

```text
我要看这个 token 到底发生了什么
我要看这个仓位什么时候买的
我要看这笔为什么赚 / 亏
```

所以必须新增：

```text
统一查看层
```

这不是多余功能，而是必要功能。

---

# 十、最终结构应该变成这样

```text
原始模块输出
  ↓
sikk_unified_view_builder.py
  ↓
index/
  token_detail_index.json
  position_index.json
  latest_open_positions.json
  ↓
两个入口：
  1. sikkctl.py 命令行查看
  2. Visual Console 点击查看
```

---

# 最短结论

你现在不应该再接受“查一个仓位要看好几个文件”。

下一步直接做：

```text
sikk_unified_view_builder.py
+
sikkctl.py
```

以后你只需要：

```bash
python3 sikkctl.py open
python3 sikkctl.py token AALIEN
python3 sikkctl.py position <position_id>
```

网站也读同一套索引。  
这样系统才真正从“模块堆叠”变成“可用产品”。


---

## 片段 5 / stream_idx=1144 / len=23657


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

## 第 2 层：自然语言记录

给你人类复盘看。

例如：

```text
系统在 2026-05-03 12:20:02 UTC 进行纸面入场。
入场时市值约 126,000 USD，模拟入场价格为 0.00005356。
本次入场基于 SIKK-B 控盘箱体突破回踩模型，信号等级为 S4。
钱包结构为 WALLET_SUPPORT，说明当前早期结构侧暂未出现集中撤退。
```

---

## 第 3 层：自动复盘

给策略优化用。

例如：

```text
本次交易的主要问题是入场市值相对发现市值已经上涨 230%，属于 LATE_ENTRY。
虽然信号等级为 S4，但入场已经偏晚，且后续最大回撤达到 -41%。
建议后续对 SIKK-B 模型增加 entry_market_cap_change_from_discovery_pct 上限，避免在二段末端追入。
```

这三层结合，才是真正的纸面测试系统。

---

# 二、从开始到结束应该记录哪些阶段

建议统一成 12 个阶段。

```text
S0_DISCOVERY              候选发现
S1_INITIAL_FILTER          初筛判断
S2_PATTERN_CLASSIFICATION  盘型识别
S3_SIGNAL_TRIGGER          信号触发
S4_WALLET_GATE             钱包结构门禁
S5_QUOTE_SECURITY          Quote / Security 检查
S6_ENTRY_DECISION          入场决策
S7_PAPER_ENTRY             纸面入场
S8_POSITION_MONITOR        持仓监控
S9_RISK_CHANGE             风险变化
S10_EXIT_DECISION          退出决策
S11_PAPER_EXIT             纸面退出
S12_AUTO_REVIEW            自动复盘
```

每个阶段都要记录：

```text
时间
阶段名
输入数据
判断结果
自然语言解释
风险点
下一步动作
```

---

# 三、每个阶段具体记录什么

## S0：候选发现

回答：

```text
这个代币什么时候被系统发现？
发现时市值多少？
流动性多少？
为什么进入观察池？
```

字段：

```text
token_symbol
token_address
candidate_discovered_at
discovery_source
discovery_price
discovery_market_cap_usd
discovery_liquidity_usd
discovery_holder_count
discovery_age_minutes
discovery_volume_5m
discovery_volume_1h
discovery_reason
```

自然语言：

```text
系统在 {{candidate_discovered_at}} 发现 ${{token_symbol}}。
发现来源为 {{discovery_source}}。
发现时市值约 {{discovery_market_cap_usd}} USD，流动性约 {{discovery_liquidity_usd}} USD，持有人数量为 {{discovery_holder_count}}。
该代币进入观察池的原因是：{{discovery_reason}}。
```

---

## S1：初筛判断

回答：

```text
它为什么没有被立即过滤？
基础风险是否合格？
```

字段：

```text
initial_filter_time
initial_filter_result
min_liquidity_pass
min_holder_pass
age_filter_pass
risk_filter_pass
initial_filter_reason
```

自然语言：

```text
初筛阶段，该 token 通过基础条件检查。
流动性、持有人数量和开盘时间未触发硬性过滤。
因此系统允许其进入后续 K线结构和钱包结构分析。
```

如果失败：

```text
该 token 在初筛阶段被阻断，原因是 {{initial_filter_reason}}。
因此不进入纸面交易流程。
```

---

## S2：盘型识别

回答：

```text
它现在是什么盘？
是控盘箱体？长横盘二段？拉高派发？还是噪音盘？
```

字段：

```text
pattern_time
pattern_type
lifecycle_phase
control_box_high
control_box_low
control_box_mid
poc_price
avwap_price
ema20
ema50
volume_state
volatility_state
price_structure_status
pattern_confidence
pattern_reason
```

自然语言：

```text
盘型识别结果为 {{pattern_type}}。
当前生命周期阶段为 {{lifecycle_phase}}。
价格结构显示，代币在 {{control_box_low}} 到 {{control_box_high}} 区间内形成控制箱体。
当前价格相对 AVWAP / POC 的位置为 {{price_structure_status}}。
系统暂时判断该结构具备 {{pattern_confidence}} 的策略适配度。
```

---

## S3：信号触发

回答：

```text
为什么触发 S3 / S4？
信号触发时价格和市值是多少？
失效条件是什么？
```

字段：

```text
signal_time
signal_level
signal_type
signal_gate
signal_price
signal_market_cap_usd
signal_liquidity_usd
signal_kline_interval
signal_reason
confirmation_conditions
invalid_level
invalid_conditions
```

自然语言：

```text
系统在 {{signal_time}} 触发 {{signal_level}} 信号。
信号类型为 {{signal_type}}。
触发时价格为 {{signal_price}}，市值约 {{signal_market_cap_usd}} USD。
触发原因是：{{signal_reason}}。
该信号的主要确认条件包括：{{confirmation_conditions}}。
失效条件为：{{invalid_conditions}}。
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

## S5：Quote / Security 检查

回答：

```text
现在价格可执行吗？
quote 偏差大不大？
security 有没有风险？
```

字段：

```text
quote_check_time
quote_source
quote_price
gmgn_price
okx_price
kline_close_price
price_deviation_pct
quote_gate
quote_reason
security_check_time
security_gate
security_risk_level
security_flags
security_reason
```

自然语言：

```text
Quote 检查在 {{quote_check_time}} 完成，来源为 {{quote_source}}。
当前 quote 价格为 {{quote_price}}，与 K线收盘价偏差为 {{price_deviation_pct}}%。
Quote 门禁结果为 {{quote_gate}}。
Security 检查结果为 {{security_gate}}，风险等级为 {{security_risk_level}}。
综合判断：{{quote_reason}} {{security_reason}}。
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

## S9：风险变化

回答：

```text
什么风险开始变坏？
是价格风险、钱包风险、quote 风险还是结构风险？
```

字段：

```text
risk_event_time
risk_event_type
risk_event_level
risk_source
risk_reason
wallet_risk_score_before
wallet_risk_score_after
counterparty_pressure_before
counterparty_pressure_after
price_structure_before
price_structure_after
risk_action
```

自然语言：

```text
系统在 {{risk_event_time}} 记录风险事件：{{risk_event_type}}。
风险来源为 {{risk_source}}，等级为 {{risk_event_level}}。
风险原因是：{{risk_reason}}。
钱包风险分从 {{wallet_risk_score_before}} 变化到 {{wallet_risk_score_after}}，对手盘压力从 {{counterparty_pressure_before}} 变化到 {{counterparty_pressure_after}}。
当前策略动作调整为：{{risk_action}}。
```

---

## S10：退出决策

回答：

```text
为什么决定退出？
是止损、止盈、钱包结构、时间止损还是强制退出？
```

字段：

```text
exit_decision_time
exit_action
exit_trigger
exit_reason_code
exit_reason
exit_evidence_chain
wallet_exit_action
wallet_exit_confidence
wallet_exit_reason_code
wallet_exit_evidence
market_confirmation
pattern_conflict
```

自然语言：

```text
系统在 {{exit_decision_time}} 做出退出决策：{{exit_action}}。
退出触发来源为 {{exit_trigger}}，原因码为 {{exit_reason_code}}。
退出证据链包括：{{exit_evidence_chain}}。
钱包退出策略给出的动作为 {{wallet_exit_action}}，置信度为 {{wallet_exit_confidence}}。
市场确认状态为 {{market_confirmation}}，盘型冲突状态为 {{pattern_conflict}}。
综合解释：{{exit_reason}}。
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

## S12：自动复盘

回答：

```text
这笔交易验证了什么？
问题在哪里？
下次怎么调？
```

字段：

```text
review_time
strategy_fit_result
entry_quality_review
wallet_gate_review
exit_quality_review
risk_management_review
main_success_factors
main_failure_factors
missed_opportunity
false_exit_flag
strategy_adjustment_suggestion
open_questions
```

自然语言：

```text
自动复盘结论：

本次交易对 {{strategy_name}} 的验证结果为：{{strategy_fit_result}}。

入场质量评价：
{{entry_quality_review}}

钱包结构门禁评价：
{{wallet_gate_review}}

退出质量评价：
{{exit_quality_review}}

风险控制评价：
{{risk_management_review}}

主要成功因素：
{{main_success_factors}}

主要失败因素：
{{main_failure_factors}}

策略调整建议：
{{strategy_adjustment_suggestion}}

仍需继续观察的问题：
{{open_questions}}
```

---

# 四、自动复盘如何实现

可以实现，不需要 LLM 也能先做规则版自动复盘。

## 自动复盘规则示例

### 1. 判断是否追高

```text
如果 market_cap_context_status = CHASE_ENTRY
→ 复盘提示：入场可能过晚，需要限制发现后市值涨幅。
```

自然语言：

```text
本次入场被标记为 CHASE_ENTRY。入场市值相对发现时已经上涨超过 300%，说明系统可能在趋势末端才触发入场。后续需要检查 SIKK-B 信号是否过于滞后，或者是否需要增加 entry_market_cap_change_from_discovery_pct 上限。
```

---

### 2. 判断钱包退出是否过早

```text
如果 FORCE_EXIT 后 shadow_hold 60m 继续上涨 > 30%
→ 标记 FALSE_EXIT
```

自然语言：

```text
本次退出可能过早。FORCE_PAPER_EXIT 后 60 分钟内价格继续上涨超过 30%，且未出现明显更大回撤，说明钱包结构退出信号可能过于敏感。建议将类似场景从 FORCE_EXIT 降级为 EXIT_MONITOR。
```

---

### 3. 判断入场信号是否有效

```text
如果 S4 入场后最大浮盈 > 50%
→ S4 信号有效
如果 S4 入场后直接 -50%
→ S4 需要增加过滤条件
```

自然语言：

```text
本次 S4 信号未能提供有效保护。入场后最大回撤快速扩大，且未产生明显浮盈，说明单独依赖 S4 强确认不足。需要结合钱包结构、入场市值和 quote 偏差进一步过滤。
```

---

### 4. 判断止损是否太晚

```text
如果 net_pnl_pct < -80%
→ 风控严重滞后
```

自然语言：

```text
本次亏损接近归零，说明退出机制严重滞后。无论退出触发来自钱包结构还是价格止损，系统都未能在损失扩大前退出。建议增加最大亏损硬阈值和快速下跌保护。
```

---

### 5. 判断右尾依赖

```text
如果 token 总收益主要靠一个大赢家
→ 提示右尾集中
```

自然语言：

```text
当前策略收益高度依赖少数右尾样本。虽然累计收益为正，但中位数收益接近 0，说明大多数交易并没有稳定优势。后续应继续扩大样本，并分别观察剔除 Top 1 / Top 2 赢家后的策略表现。
```

---

# 五、需要新增的文件结构

建议新增：

```text
data/gmgn_candidates_live_run/paper_live/
  case_files/
    <position_id>.json
    <position_id>.md

  position_journal/
    <position_id>.jsonl

  auto_reviews/
    <position_id>_review.json
    <position_id>_review.md
```

核心脚本：

```text
sikk_paper_lifecycle_recorder.py
sikk_paper_explanation_builder.py
sikk_paper_auto_reviewer.py
```

三个模块分工：

| 模块 | 作用 |
|---|---|
| `sikk_paper_lifecycle_recorder.py` | 记录每个阶段的结构化数据 |
| `sikk_paper_explanation_builder.py` | 把阶段数据转成自然语言 case file |
| `sikk_paper_auto_reviewer.py` | 自动复盘并输出调整建议 |

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

# 八、最终判断

可以实现，而且这是你系统应该做的关键升级。

现在你的纸面交易要从：

```text
收益统计系统
```

升级成：

```text
策略实战复盘系统
```

它的核心不是“这个币赚了多少”，而是：

```text
这个币为什么进？
进的时候对不对？
钱包结构有没有支持？
进场是不是追高？
持仓过程中哪里开始变坏？
退出对不对？
如果错了，策略应该怎么改？
```

这才是纸面测试真正的价值。


---

## 片段 6 / stream_idx=1333 / len=20471


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

# 二、每一笔仓位必须分 8 个阶段记录

## 阶段 1：候选发现

记录这个 token 是怎么进入系统视野的。

必须记录：

```text
token_symbol
token_address
candidate_discovered_at
discovery_source
discovery_price
discovery_market_cap_usd
discovery_liquidity_usd
discovery_holder_count
discovery_volume_5m
discovery_volume_1h
discovery_age_minutes
discovery_reason
```

自然语言解释示例：

```text
系统在 2026-05-03 12:01:22 UTC 发现 $ABC。
发现来源为 GMGN 新币过滤器。
发现时市值约 82,000 USD，流动性约 26,000 USD，持有人 412。
该 token 被纳入观察的原因是：市值仍处于早期区间，流动性满足最低观察条件，并且后续 K线进入控盘箱体候选结构。
```

---

## 阶段 2：盘型识别

必须记录它是什么盘，而不是只说 SIKK-B。

字段：

```text
pattern_type
lifecycle_phase
control_box_high
control_box_low
control_box_mid
poc_price
avwap_price
ema20
ema50
volume_state
volatility_state
price_structure_status
```

自然语言解释示例：

```text
当前盘型被识别为 SIKK-B 控盘箱体突破回踩。
价格此前在 0.000041 到 0.000049 区间内形成横盘控制箱体。
回踩阶段没有有效跌破箱体下沿，成交量没有出现恐慌放大，因此暂时判断为结构性回踩，而不是单边派发。
```

---

## 阶段 3：信号触发

记录为什么变成 S3 / S4。

字段：

```text
signal_time
signal_level
signal_type
signal_gate
signal_price
signal_market_cap_usd
signal_liquidity_usd
signal_kline_interval
signal_reason
invalid_level
confirmation_conditions
```

自然语言解释示例：

```text
系统在 2026-05-03 12:18:40 UTC 触发 S4_强确认信号。
触发原因是：价格突破控盘箱体后回踩未跌破箱体中轴，随后重新站回 AVWAP 上方，1m / 5m 成交量没有明显失控放大，说明短线抛压暂时被吸收。
当时价格为 0.000052，市值约 118,000 USD。
该信号的失效条件是：价格重新跌破 control_box_low 或跌破 AVWAP 后无法快速收回。
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

## 阶段 5：Quote / Security 检查

记录是否具备可执行性。

字段：

```text
quote_check_time
quote_source
quote_price
gmgn_price
okx_price
kline_close_price
price_deviation_pct
quote_gate
quote_reason
security_check_time
security_gate
security_risk_level
security_flags
```

自然语言解释示例：

```text
Quote 检查在 2026-05-03 12:19:30 UTC 通过。
OKX quote 与 K线收盘价偏差为 0.8%，未超过暂停阈值。
Security 扫描未发现高风险标记，因此该 token 允许进入纸面交易模拟。
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

## 2. 候选发现

系统在 {{candidate_discovered_at}} 发现该 token。  
发现时市值为 {{discovery_market_cap_usd}}，流动性为 {{discovery_liquidity_usd}}，持有人数量为 {{discovery_holder_count}}。

发现原因：

{{discovery_reason}}

---

## 3. 盘型判断

当前识别盘型：

- pattern_type：{{pattern_type}}
- lifecycle_phase：{{lifecycle_phase}}
- control_box_low：{{control_box_low}}
- control_box_high：{{control_box_high}}
- AVWAP：{{avwap_price}}
- POC：{{poc_price}}

自然语言解释：

{{pattern_explanation}}

---

## 4. 入场信号

信号触发时间：{{signal_time}}  
信号等级：{{signal_level}}  
信号类型：{{signal_type}}  
信号触发时市值：{{signal_market_cap_usd}}

入场信号解释：

{{signal_explanation}}

失效条件：

{{invalid_conditions}}

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

## 6. Quote / Security

Quote 检查时间：{{quote_check_time}}  
Quote 来源：{{entry_quote_source}}  
价格偏差：{{price_deviation_pct}}  
Security 状态：{{security_gate}}

解释：

{{quote_security_explanation}}

---

## 7. 纸面入场

纸面入场时间：{{paper_entry_time}}  
入场价格模式：{{entry_price_mode}}  
原始报价价格：{{entry_raw_quote_price}}  
模拟入场价格：{{entry_simulated_price}}  
滑点：{{entry_slippage_pct}}%  
手续费：{{entry_fee_sol}} SOL  

| 项目 | 数值 |
|---|---:|
| 入场市值 | {{entry_market_cap_usd}} |
| 发现时市值 | {{discovery_market_cap_usd}} |
| 信号时市值 | {{signal_market_cap_usd}} |
| 从发现到入场市值变化 | {{entry_market_cap_change_from_discovery_pct}}% |
| 从信号到入场市值变化 | {{entry_market_cap_change_from_signal_pct}}% |
| 入场上下文 | {{market_cap_context_status}} |
| 买入规模 | {{paper_size_sol}} SOL |
| 估算 token 数量 | {{estimated_token_amount}} |

入场自然语言解释：

{{entry_explanation}}

---

## 8. 持仓过程

{{position_journal_summary}}

关键变化：

| 时间 | 价格 | 市值 | 浮盈 | 钱包状态 | 动作 | 原因 |
|---|---:|---:|---:|---|---|---|
{{journal_rows}}

---

## 9. 退出

退出时间：{{exit_time}}  
退出价格：{{exit_price}}  
退出市值：{{exit_market_cap_usd}}  
退出触发：{{exit_trigger}}  
退出原因码：{{exit_reason_code}}  
最终收益：{{net_pnl_pct}}%

退出解释：

{{exit_explanation}}

---

## 10. 策略复盘

本次交易结果：{{trade_result_type}}  
失败归因：{{failure_type}}  

复盘判断：

{{post_trade_review}}

---

## 11. 策略调整建议

{{strategy_adjustment_suggestion}}

---

## 12. 需要继续观察的问题

{{open_questions}}
```

---

# 五、策略每一步必须自然语言化

你现在需要在系统里定义这些解释字段：

## 1. `discovery_explanation`

回答：

```text
为什么这个 token 被发现？
发现时是否早？
市值是否合适？
流动性是否合适？
```

---

## 2. `pattern_explanation`

回答：

```text
这是什么盘？
为什么不是垃圾直线盘？
为什么符合 SIKK-B？
有没有可能是高位派发？
```

---

## 3. `signal_explanation`

回答：

```text
为什么触发 S4？
哪些指标支持？
哪些条件是失效点？
```

---

## 4. `wallet_explanation`

回答：

```text
钱包结构支持还是风险？
早期钱包有没有跑？
同源组有没有同步卖？
高结果钱包还在不在？
是不是正在转给接盘方？
```

---

## 5. `entry_explanation`

回答：

```text
为什么这个位置进？
进场位置相对箱体在哪里？
进场时是否追高？
进场市值相对发现时涨了多少？
为什么允许纸面买？
```

---

## 6. `holding_explanation`

回答：

```text
持仓过程中结构是否保持？
浮盈回撤是否正常？
钱包结构是否恶化？
有没有进入 EXIT_MONITOR？
```

---

## 7. `exit_explanation`

回答：

```text
为什么退出？
退出是价格触发，还是钱包触发？
退出是否过早？
退出时市值是多少？
钱包结构是否真的恶化？
```

---

## 8. `post_trade_review`

回答：

```text
这笔交易验证了什么？
亏在哪里？
赚在哪里？
是策略有效，还是右尾偶然？
```

---

## 9. `strategy_adjustment_suggestion`

回答：

```text
下次应该调哪里？
入场太晚？
止损太宽？
钱包退出太敏感？
quote 检查太慢？
市值区间不适合？
```

---

# 六、需要新增的字段分组

## A. 市值路径字段

```text
discovery_market_cap_usd
signal_market_cap_usd
wallet_decision_market_cap_usd
entry_market_cap_usd
current_market_cap_usd
exit_market_cap_usd
```

面板上显示为：

```text
发现市值 → 信号市值 → 入场市值 → 退出市值
```

这是判断是否追高的核心。

---

## B. 时间路径字段

```text
candidate_discovered_at
signal_time
wallet_decision_time
quote_check_time
paper_entry_time
exit_time
```

面板上显示为：

```text
发现 → 信号 → 钱包确认 → Quote → 入场 → 退出
```

---

## C. 价格路径字段

```text
discovery_price
signal_price
entry_raw_quote_price
entry_simulated_price
current_price
exit_price
```

---

## D. 仓位规模字段

```text
paper_size_sol
paper_size_usd
estimated_token_amount
entry_slippage_pct
entry_fee_sol
exit_fee_sol
```

---

## E. 策略证据字段

```text
strategy_name
signal_level
signal_type
pattern_type
lifecycle_phase
entry_reason_summary
entry_evidence_chain
invalid_conditions
exit_evidence_chain
```

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

# 九、你最终要的效果

以后你打开某个 token 的 case file，应该能直接看出：

```text
这个 token 是什么时候发现的
发现时市值多少
信号触发时市值多少
什么时候入场
入场时市值多少
买了多少 SOL
估计买了多少 token
入场位置是不是箱体回踩
是不是站上 AVWAP
钱包结构是不是支持
quote/security 有没有问题
入场是否追高
持仓过程中哪里变坏
为什么退出
退出是不是太早
亏损原因是什么
策略哪里需要调
```

这才叫纸面测试。

---

# 十、当前优先级

先做：

```text
P0：每笔仓位的 entry snapshot
P0：每笔仓位的 case file
P0：自然语言入场解释
P0：自然语言退出解释
P0：策略调整建议
```

再做：

```text
P1：Visual Console 展示 case file
P1：Paper Lab 分桶统计
P1：退出有效性统计
```

最后做：

```text
P2：更复杂图表和多日趋势
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

## 片段 7 / stream_idx=1390 / len=206


我需要更加详细的细节信息，一个代币是当前市值多少，什么时间进去市值多少，什么时候退出，时间市值，以及具体的策略方方面面的信息，策略的每一个步骤都要用自然语言表达出来，比如说，在什么位置进场，原因有那些，进厂时候，指标上的具体操作，或者是思维上的逻辑思考，等等都要表达出来，反正具体的目标就是纸面仓位搞这个就是在测试我的策略在哪里有不足，在什么地方，什么位置需要做调整，所以，代币具体的实战信息要记录的比较详细才行


---

## 片段 8 / stream_idx=1550 / len=16640


这份纸面报告非常有价值。它已经明确暴露出一个核心问题：

> **当前系统不是在验证“SIKK-B 控盘箱体突破回踩是否有效”，而是在验证“钱包结构强制退出机制是否过度主导”。**

现在不能只看累计收益是正的。  
这份报告说明：**系统确实能抓到右尾大收益，但退出逻辑、样本独立性、入场记录、钱包结构接入方式都有明显偏差。**

---

# 一、这份报告的真实结论

## 1. 累计收益为正，但稳定性不强

数据：

```text
已关闭累计收益：+1104.26%
平均单笔收益：+9.5195%
中位数收益：-0.0493%
胜率：29.31%
```

这说明：

```text
系统收益来自少数极端赢家
大部分交易接近小亏 / 小波动 / 持平
```

这不是坏事。meme 策略本来就可能是右尾收益模型。

但问题是：

> **你现在还不能判断系统真的稳定有效，因为 AALIEN 和 lolcat 对结果贡献过大。**

AALIEN 一项贡献：

```text
+1184.2034%
```

总收益：

```text
+1104.26%
```

这意味着：**如果去掉 AALIEN，整体收益可能完全变样。**

所以现在必须新增：

```text
剔除最大赢家后的收益
剔除 Top 1 token 后收益
剔除 Top 2 token 后收益
按 token 聚合后的收益
```

否则容易被极端右尾误导。

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

## 3. 钱包结构强制退出占比过高

核心数据：

```text
钱包结构触发纸面强制退出：96 / 116
FORCE_PAPER_EXIT：96
STRUCTURE_WEAKENING：96
WALLET_BLOCK：112
```

这说明当前系统几乎变成：

```text
钱包结构退出系统
```

而不是：

```text
K线结构 + 钱包结构 + quote/security + paper runner 的综合验证系统
```

这个问题非常严重。

钱包结构当然重要，但现在它已经过度主导退出。尤其你前面担心“很多刚因为钱包结构触发就强制退出”，这份数据已经验证了这个担心。

---

## 4. `STRUCTURE_WEAKENING` 被误用为失败归因

最好单笔：

```text
AALIEN
最终收益：+679.3995%
退出原因：钱包结构触发纸面强制退出
失败归因：STRUCTURE_WEAKENING
```

这里逻辑不对。

如果一笔交易盈利 +679%，它不应该被简单归为：

```text
失败归因：STRUCTURE_WEAKENING
```

更准确应该分开：

```text
exit_trigger = WALLET_STRUCTURE_EXIT
exit_reason_code = STRUCTURE_WEAKENING
trade_result = BIG_WIN
failure_type = null
```

现在你的系统把“退出触发原因”和“失败归因”混在一起了。

必须拆开：

```text
exit_reason        退出原因
exit_trigger       谁触发退出
exit_reason_code   退出信号码
trade_result_type  交易结果类型
failure_type       只有亏损或无效交易才写失败归因
```

否则日报会误导你。

---

## 5. S4 信号样本过于单一

报告显示：

```text
所有记录都是 S4_强确认信号
所有策略都是 SIKK-B 控盘箱体突破回踩
```

这说明当前纸面验证只覆盖了一个子策略：

```text
SIKK-B + S4
```

不能推导到整个 SIKK 系统。

当前只能说：

> **你正在验证 SIKK-B 强确认突破回踩模型。**

不能说：

```text
SIKK 整体策略有效
钱包结构系统整体有效
```

后续必须拆：

```text
S3 vs S4
WALLET_SUPPORT vs WALLET_BLOCK
EARLY_ENTRY vs LATE_ENTRY
EXIT_MONITOR vs FORCE_EXIT
不同市值区间
不同 token 生命周期
不同盘型
```

---

# 二、当前最关键的 6 个问题

## 问题 1：重复入场 / 多记录是否合理

AALIEN 34 次，WOLVERINE 16 次。

你需要确认：

```text
这是同一 token 多次独立入场？
还是 paper runner 重复开仓？
是否违反“单 token 只允许一笔实盘”的原则？
```

如果未来实盘原则是：

```text
一个 token 只允许一笔实盘
```

那纸面也应该至少增加一个统计：

```text
single_token_first_entry_only_result
```

否则纸面表现和未来实盘不一致。

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

## 问题 3：强制退出没有验证对错

96 次 FORCE_PAPER_EXIT，现在你不知道：

```text
它们是真的规避了后续下跌？
还是误杀了后续上涨？
```

所以必须加：

```text
shadow_hold_tracking
```

每次 FORCE_EXIT 后继续追踪：

```text
退出后 15m / 30m / 60m 的价格
退出后最大涨幅
退出后最大回撤
是否误杀
是否规避下跌
```

否则无法评估钱包退出机制是否正确。

---

## 问题 4：入场市值上下文缺失

你已经指出了：

```text
什么时候买
买了多少
什么市值进去
```

这份报告也说明这个字段必须补。

没有这些字段，就无法判断：

```text
AALIEN 是早期吃到右尾？
还是已经高位追进但继续冲？
GRUMP 是高位追进？
还是早期失败？
```

必须新增：

```text
discovery_market_cap_usd
signal_market_cap_usd
entry_market_cap_usd
exit_market_cap_usd
entry_market_cap_change_from_discovery_pct
market_cap_context_status
```

---

## 问题 5：收益统计方式需要升级

当前：

```text
总收益率累计：+1104.26%
```

这是把每笔百分比直接相加。

这可以看方向，但不能代表真实账户曲线。

必须新增：

```text
position_size_weighted_pnl
equity_curve_return
max_equity_drawdown
token_weighted_return
capital_weighted_return
```

否则 0.042 SOL 的仓位和 0.2 SOL 的仓位被同等看待，会失真。

---

## 问题 6：退出时机可能滞后

报告里说：

```text
GRUMP、GOBLIEN、NYAN 接近归零亏损
但退出原因仍然是钱包结构强制退出
```

这说明：

```text
钱包结构退出不是太早，而是某些情况下太晚
```

所以问题不是简单把 FORCE_EXIT 全部降级。

更准确是：

```text
钱包结构退出需要分层：
- 提前预警：EXIT_MONITOR
- 市场确认：REDUCE_RISK / TIGHT_STOP
- 强证据：FORCE_EXIT
```

当前只有 FORCE_EXIT，缺中间层。

---

# 三、当前系统应该如何重新定性

现在的系统阶段不是简单“纸面验证表现很好”。

更准确：

```text
Phase B-1A：右尾收益型纸面样本已出现，但退出机制和样本统计口径需要审计
```

当前不能进入实盘。

原因：

```text
1. 样本被少数 token 主导
2. 钱包结构强制退出过度主导
3. 入场快照缺失
4. 退出对错没有 shadow hold 验证
5. 失败归因字段混乱
6. 按 token 独立统计不足
```

---

# 四、现在必须新增的核心指标

## 1. 剔除极端赢家后的表现

日报新增：

```text
total_pnl_excluding_top_1_token
total_pnl_excluding_top_2_tokens
median_token_pnl
token_level_win_rate
position_level_win_rate
```

用途：

```text
判断系统是否只靠 AALIEN / lolcat 撑起来
```

---

## 2. 单 token 聚合统计

新增：

```text
token_count
position_count_per_token
token_total_pnl_pct
token_avg_pnl_pct
token_median_pnl_pct
token_win_rate
token_best_trade
token_worst_trade
```

同时展示：

```text
Top token contribution concentration
```

例如：

```text
AALIEN 贡献 / 总收益
Top 3 token 贡献 / 总收益
```

---

## 3. 入场上下文统计

新增：

```text
entry_market_cap_usd
entry_market_cap_bucket
entry_delay_from_discovery_sec
entry_delay_from_signal_sec
market_cap_context_status
```

市值分桶：

```text
<50K
50K-100K
100K-200K
200K-500K
500K-1M
>1M
```

---

## 4. 钱包退出有效性

新增：

```text
force_exit_count
exit_monitor_count
true_positive_exit_count
false_positive_exit_count
false_exit_rate
avg_avoided_drawdown_pct
avg_missed_profit_pct
price_change_after_exit_15m
price_change_after_exit_30m
price_change_after_exit_60m
```

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

## 第二层：退出策略判断

结合：

```text
盘型
生命周期
K线结构
quote/security
多轮 delta
paper 当前盈亏
```

输出：

```text
HOLD
EXIT_MONITOR
FORCE_PAPER_EXIT
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

# 七、这份日报下一版应该变成这样

## 新增一：样本独立性

```text
样本独立性
- 总仓位记录：119
- 涉及 token：17
- 平均每 token 仓位数：7.0
- 最高重复 token：AALIEN 34 次
- Top 1 token 贡献占比：xxx%
- 剔除 Top 1 token 后总收益：xxx%
- 剔除 Top 2 token 后总收益：xxx%
```

---

## 新增二：钱包退出有效性

```text
钱包退出有效性
- FORCE_EXIT 次数：96
- EXIT_MONITOR 次数：x
- 退出后 30m 平均价格变化：x%
- 退出后 60m 平均价格变化：x%
- 误杀次数：x
- 误杀率：x%
- 平均规避回撤：x%
- 平均错过收益：x%
```

---

## 新增三：入场市值上下文

```text
入场市值上下文
- EARLY_ENTRY：x 笔，平均收益 x%
- NORMAL_ENTRY：x 笔，平均收益 x%
- LATE_ENTRY：x 笔，平均收益 x%
- CHASE_ENTRY：x 笔，平均收益 x%
```

---

## 新增四：入场钱包状态 vs 出场钱包状态

```text
钱包结构迁移
- ENTRY WALLET_SUPPORT → EXIT WALLET_BLOCK：x 笔
- ENTRY WALLET_NEUTRAL → EXIT WALLET_BLOCK：x 笔
- ENTRY MISSING → EXIT WALLET_BLOCK：x 笔
```

这个能告诉你：

```text
是入场后结构恶化
还是入场时就不该进
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

# 九、现在的执行优先级

## P0：先修统计口径

```text
1. 拆分 exit_trigger / exit_reason_code / failure_type
2. 增加 entry_wallet_status / exit_wallet_status
3. 增加 paper entry snapshot
4. 增加按 token 聚合统计
```

## P1：再修钱包退出策略

```text
5. wallet_exit_policy
6. EXIT_MONITOR
7. FORCE_EXIT 收紧
8. shadow hold tracking
```

## P2：最后改面板展示

```text
9. Paper Lab Pro
10. Right Tail Dependency
11. Entry MC Bucket
12. Wallet Exit Effectiveness
```

不要反过来。  
先数据，后策略，再面板。

---

# 十、最终判断

这份报告说明：

```text
SIKK-B S4 当前确实能抓到大右尾
但系统稳定性还没证明
钱包结构退出机制过度主导
样本被少数 token 高度影响
纸面记录缺少入场证据链
```

所以现在最重要的不是继续增加 token，也不是马上调 dashboard，而是：

> **把 paper 统计从“收益表”升级成“交易证据链 + 退出有效性审计表”。**

这一步完成后，你才能真正判断：

```text
钱包结构接入方式是否正确
FORCE_EXIT 是否误杀
SIKK-B 是否靠少数右尾维持
入场是不是太晚
哪些市值区间更有效
哪些钱包状态真的有价值
```


---

## 片段 9 / stream_idx=1630 / len=2518


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

## 片段 10 / stream_idx=1752 / len=8949


对，你现在这个担心是对的。

如果现在出现很多：

```text
因为钱包结构触发 → FORCE_PAPER_EXIT
```

那说明系统可能已经从：

```text
钱包结构作为风险证据
```

过度变成了：

```text
钱包结构直接控制退出
```

这不一定正确。

---

# 一句话判断

> **钱包筹码结构不应该默认直接强制退出。它应该先作为“风险监控层”和“失败归因层”，只有在强证据、多快照、与盘型冲突时，才允许 FORCE_PAPER_EXIT。**

现在你要重点检查：

```text
这些强制退出是真的规避了风险？
还是把正常洗盘 / 换手 / 横盘二段前的筹码轮换误判成出货？
```

---

# 一、钱包结构在系统里的正确位置

钱包结构不应该是单独的买卖按钮。

它应该有 4 个作用：

```text
1. 入场前门禁
2. 持仓中风险监控
3. 异常时退出观察
4. 失败后归因
```

不是：

```text
看到早期钱包卖出 → 立刻退出
看到钱包结构变差 → 立刻退出
看到 WALLET_BLOCK → 立刻平仓
```

正确逻辑应该是：

```text
钱包结构变化
  ↓
判断是不是与当前盘型冲突
  ↓
判断是不是多轮快照确认
  ↓
判断是不是价格/成交/quote 同步恶化
  ↓
再决定 HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
```

---

# 二、现在最可能的问题

你现在很多强制退出，可能来自这几种误判。

## 1. 把正常换手当成出货

尤其是这种盘：

```text
长时间横盘
控盘箱体
二段放量前
早期钱包部分减仓
新钱包承接
```

这不一定是坏事。

可能是：

```text
结构侧部分换手
利润钱包释放浮盈
新承接方接力
二段前清理不稳定筹码
```

不能直接 FORCE_EXIT。

---

## 2. 单次快照触发太敏感

如果只看一轮：

```text
early_wallet_sold_pct 增加
same_source_sync_sell_score 上升
counterparty_pressure_score 上升
```

就强制退出，会有很多误杀。

正确做法：

```text
至少需要 2 轮快照 delta 确认
```

比如：

```text
snapshot_1：早期钱包卖出增加
snapshot_2：继续卖出 + 价格承压 + 对手盘压力上升
```

这才更接近真实结构恶化。

---

## 3. 没有结合盘型

不同盘型下，同一个钱包行为意义不同。

| 盘型 | 钱包卖出含义 |
|---|---|
| 爆拉后高位放量 | 大概率派发风险 |
| 长横盘控盘箱体 | 可能是换手 |
| 二段启动前 | 可能是清筹 |
| 下跌破位 | 大概率结构失败 |
| 横盘缩量 | 需要等 delta，不应马上退出 |

所以你的钱包结构门禁必须是：

```text
pattern-aware wallet gate
```

不能是：

```text
wallet-only exit gate
```

---

# 三、正确退出动作应该分 3 档

不要只有 `FORCE_PAPER_EXIT`。

应该改成：

```text
HOLD
EXIT_MONITOR
FORCE_PAPER_EXIT
```

## 1. HOLD

结构没有明显恶化。

```text
继续持有
继续观察钱包 delta
```

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

## 3. FORCE_PAPER_EXIT

只用于强证据。

必须同时满足：

```text
数据质量足够
钱包结构明确恶化
多轮 delta 确认
与当前盘型冲突
价格/成交/quote 同步支持风险判断
```

---

# 四、什么时候才允许 FORCE_PAPER_EXIT

建议只有这些情况允许强制退出。

## A. 同源组同步出货

```text
same_source_sync_sell_score >= 80
并且 group_sold_pct_delta >= 20
并且 group_remaining_pct 明显下降
```

结论：

```text
FORCE_PAPER_EXIT
```

---

## B. 价格上涨中早期钱包集中派发

```text
price_change_pct > 0
early_wallet_sold_pct_delta >= 25
late_large_buyer_count 增加
counterparty_pressure_score >= 75
```

这说明可能是：

```text
拉升过程中把筹码转给对手盘
```

结论：

```text
FORCE_PAPER_EXIT
```

---

## C. 高结果钱包集体退出

```text
high_result_remaining_pct_delta <= -30
wallet_risk_score_delta >= 20
same_source_sell 同时上升
```

结论：

```text
FORCE_PAPER_EXIT
```

---

## D. 钱包恶化 + K线破位

```text
wallet_risk_score >= 75
并且 price 跌破 control_box_low / POC / AVWAP
并且 volume 放大
```

结论：

```text
FORCE_PAPER_EXIT
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

# 七、建议配置

你可以让系统默认变成保守一点：

```json
{
  "wallet_exit_policy": {
    "enabled": true,
    "default_action": "EXIT_MONITOR",
    "force_exit_min_confidence": 80,
    "min_data_quality_score": 65,
    "require_delta_snapshots": 2,
    "require_pattern_conflict": true,
    "require_market_confirmation": true,
    "shadow_hold_tracking": true,
    "hard_exit_codes": [
      "SAME_SOURCE_SYNC_EXIT",
      "ACTIVE_DISTRIBUTION",
      "HIGH_RESULT_GROUP_EXIT",
      "COUNTERPARTY_ABSORBING",
      "WALLET_RISK_WITH_PRICE_BREAKDOWN"
    ]
  }
}
```

核心是：

```text
默认 EXIT_MONITOR
强证据才 FORCE_EXIT
```

---

# 八、必须加 Shadow Hold Tracking

这是关键。

现在如果系统 FORCE_EXIT 了，你不知道它是对是错。

所以每次触发强制退出后，还要继续模拟一个“如果不退出”的影子仓位。

新增字段：

```text
wallet_exit_trigger_time
wallet_exit_trigger_type
wallet_exit_trigger_score
wallet_exit_action
force_exit_price
shadow_hold_price_15m
shadow_hold_price_30m
shadow_hold_price_60m
shadow_hold_max_profit_after_exit
shadow_hold_max_drawdown_after_exit
false_exit_flag
avoided_drawdown_pct
missed_profit_pct
```

这样你才能知道：

```text
这次强制退出到底是规避了亏损
还是卖飞了后面的上涨
```

---

# 九、日报必须统计 FORCE_EXIT 是否有效

Paper 日报加一段：

```text
Wallet Exit Effectiveness
```

字段：

```text
wallet_force_exit_count
true_positive_exit_count
false_positive_exit_count
false_exit_rate
avg_avoided_drawdown_pct
avg_missed_profit_pct
avg_price_change_after_exit_30m
avg_price_change_after_exit_60m
```

判断：

```text
如果 false_exit_rate 很高
说明钱包退出规则过严
```

例如：

```text
force exit 后 60 分钟价格上涨 > 30%
并且没有触发更深回撤
```

标记：

```text
FALSE_EXIT
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

## 2. 默认从 FORCE_EXIT 降级为 EXIT_MONITOR

除非满足强证据。

```text
单轮钱包风险 → EXIT_MONITOR
多轮确认 + 盘型冲突 + 市场确认 → FORCE_EXIT
```

---

## 3. 加 pattern-aware 判断

必须把当前盘型传进去：

```text
pattern_type
lifecycle_phase
control_box_status
second_stage_candidate
price_structure_status
```

如果是：

```text
LONG_CONTROL_BOX
SECOND_STAGE_EXPANSION
REACCUMULATION
```

则部分钱包卖出不直接退出。

---

## 4. 加 force exit 复盘统计

否则你永远不知道规则对不对。

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

# 十二、当前结论

你现在的怀疑是正确的。

如果很多仓位刚因为钱包结构就被强制退出，说明现在系统可能过于激进。

正确方向不是取消钱包结构，而是：

```text
钱包结构继续保留
但从“直接退出器”
改成“风险证据 + 退出策略层 + 复盘验证层”
```

最终目标：

```text
不是让钱包结构少触发
而是让每一次触发都能回答：
为什么触发？
证据够不够？
是否与盘型冲突？
退出后是否证明正确？
有没有卖飞？
```

这样你的 SIKK 才会从“规则驱动退出”升级成“证据驱动退出”。


---

## 片段 11 / stream_idx=1929 / len=13739


对，这个缺口很关键。现在问题已经不是“面板不够好看”，而是：

> **纸面交易缺少入场证据链。**

如果你不知道：

```text
什么时候买的
买了多少
按什么价格买的
当时市值是多少
当时信号是什么
当时钱包结构是什么
当时 quote/security 是否通过
```

那这个纸面测试就没有复盘价值。

---

# 一、必须新增：Paper Entry Snapshot

当前 `paper_positions_open.json / closed.json` 不能只记录仓位盈亏，必须在入场瞬间保存一份不可变快照。

也就是：

```text
发现时状态
信号触发时状态
钱包门禁时状态
纸面入场时状态
```

全部要保存下来。

核心原则：

> **入场时的数据必须在入场瞬间写入，不能事后用 current price / current market cap 反推。**

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

## 2. 候选发现时信息

```json
{
  "candidate_discovered_at": "2026-05-03T11:42:10Z",
  "discovery_price": 0.00000123,
  "discovery_market_cap_usd": 82000,
  "discovery_liquidity_usd": 26000,
  "discovery_holder_count": 412,
  "discovery_source": "gmgn_new_token_filter"
}
```

这个用于判断：

```text
系统是不是发现得早
还是发现时已经高位
```

---

## 3. 信号触发时信息

```json
{
  "signal_time": "2026-05-03T11:58:30Z",
  "signal_level": "S3",
  "signal_type": "CONTROL_BOX_BREAKOUT_PULLBACK",
  "signal_price": 0.00000175,
  "signal_market_cap_usd": 118000,
  "signal_liquidity_usd": 31000,
  "signal_reason": "控盘箱体突破后回踩未破"
}
```

这个用于判断：

```text
信号出现时，市值已经涨了多少
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

## 5. 纸面入场时信息

这是最重要的。

```json
{
  "paper_entry_time": "2026-05-03T12:01:02Z",
  "entry_price_mode": "live",
  "entry_quote_source": "okx",
  "entry_raw_quote_price": 0.00000182,
  "entry_simulated_price": 0.000001875,
  "entry_slippage_pct": 3.0,
  "entry_fee_sol": 0.0005,
  "entry_market_cap_usd": 126000,
  "entry_liquidity_usd": 33000,
  "entry_holder_count": 438,

  "paper_size_sol": 0.01,
  "paper_size_usd": 1.65,
  "estimated_token_amount": 879123.12
}
```

这里必须回答你说的：

```text
什么时候买？
买了多少？
什么市值买？
什么价格买？
```

---

## 6. 当前状态

```json
{
  "current_price": 0.00000210,
  "current_market_cap_usd": 145000,
  "current_liquidity_usd": 35000,
  "unrealized_pnl_pct": 12.0,
  "unrealized_pnl_sol": 0.0012,
  "max_floating_profit_pct": 28.5,
  "max_drawdown_pct": -7.4
}
```

---

## 7. 出场信息

关闭仓位必须有：

```json
{
  "exit_time": "2026-05-03T13:20:44Z",
  "exit_reason": "TAKE_PROFIT_TRAIL",
  "exit_price": 0.00000290,
  "exit_market_cap_usd": 202000,
  "exit_liquidity_usd": 41000,
  "exit_slippage_pct": 3.0,
  "exit_fee_sol": 0.0005,
  "net_pnl_pct": 52.3,
  "net_pnl_sol": 0.00523,
  "failure_type": null
}
```

---

# 三、必须区分两个文件：仓位表和交易流水

你现在需要两层数据。

## 1. `paper_positions_open/closed`

这是仓位汇总。

记录：

```text
一笔仓位当前是什么状态
什么时候进的
现在盈亏多少
为什么进
为什么出
```

---

## 2. `paper_trades.csv`

这是交易流水。

每一次买入、卖出、强制退出、止损、止盈都要记录一行。

字段建议：

```csv
trade_id,position_id,token_address,token_symbol,side,event_type,trade_time,price,market_cap_usd,liquidity_usd,size_sol,size_usd,token_amount,slippage_pct,fee_sol,quote_source,reason
```

示例：

```csv
TRD_001,PAPER_ABC_001,xxx,ABC,BUY,PAPER_ENTRY,2026-05-03T12:01:02Z,0.000001875,126000,33000,0.01,1.65,879123,3.0,0.0005,okx,WALLET_SUPPORT+S3+QUOTE_OK
```

这样你才能复盘：

```text
每次什么时候入场
当时市值多少
买了多少 SOL
买到了多少 token
当时滑点多少
为什么买
```

---

# 四、面板 Paper Lab 必须升级

现在 Paper Lab 不能只显示：

```text
OPEN
PNL
WIN RATE
```

必须加 4 个表。

---

## 1. 当前开放仓位表

字段：

```text
Token
Entry Time
Entry MC
Current MC
MC Change
Entry Price
Current Price
Size SOL
Token Amount
PnL %
Max Profit
Max Drawdown
Wallet Status
Signal
Next Action
```

示例：

| Token | Entry Time | Entry MC | Current MC | MC Change | Size | PnL | Wallet | Next |
|---|---|---:|---:|---:|---:|---:|---|---|
| ABC | 12:01:02 | 126K | 145K | +15.1% | 0.01 SOL | +12.0% | SUPPORT | HOLD |

---

## 2. 已关闭仓位表

字段：

```text
Token
Entry Time
Exit Time
Entry MC
Exit MC
Size SOL
Net PnL %
Exit Reason
Failure Type
Wallet Status
```

---

## 3. 入场质量统计

新增：

```text
Entry Market Cap Bucket
```

市值分桶：

```text
<50K
50K-100K
100K-200K
200K-500K
500K-1M
>1M
```

统计：

```text
不同市值入场的胜率
不同市值入场的平均收益
不同市值入场的最大回撤
```

这样你才能判断：

```text
我到底是不是买晚了？
哪个市值区间更适合 SIKK？
```

---

## 4. 发现到入场延迟

必须统计：

```text
entry_delay_from_discovery_sec
entry_delay_from_signal_sec
entry_market_cap_change_from_discovery_pct
entry_market_cap_change_from_signal_pct
```

这非常关键。

如果一个 token：

```text
发现市值 50K
入场市值 300K
```

那说明你不是早期入场，而是在追高。

---

# 五、必须新增的计算字段

在 paper runner 里计算：

```python
entry_market_cap_change_from_discovery_pct =
    (entry_market_cap_usd - discovery_market_cap_usd) / discovery_market_cap_usd * 100
```

```python
entry_market_cap_change_from_signal_pct =
    (entry_market_cap_usd - signal_market_cap_usd) / signal_market_cap_usd * 100
```

新增状态：

```text
EARLY_ENTRY
NORMAL_ENTRY
LATE_ENTRY
CHASE_ENTRY
```

规则建议：

| 状态 | 条件 |
|---|---|
| `EARLY_ENTRY` | 入场市值相对发现市值上涨 < 50% |
| `NORMAL_ENTRY` | 上涨 50%-150% |
| `LATE_ENTRY` | 上涨 150%-300% |
| `CHASE_ENTRY` | 上涨 > 300% |

这个字段叫：

```text
market_cap_context_status
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

# 八、面板里 Paper Lab 应该改成这样

你要让它最终显示成这种结构。

## 当前开放仓位

| Token | Entry Time | Entry MC | Current MC | MC Change | Size | Token Amt | PnL | Max DD | Wallet | Context |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| ABC | 12:01 | 126K | 145K | +15% | 0.01 SOL | 879K | +12% | -7% | SUPPORT | NORMAL |

---

## 市值入场分布

| Entry MC Bucket | Trades | Win Rate | Avg PnL | Max DD |
|---|---:|---:|---:|---:|
| <50K | 3 | 66% | +40% | -18% |
| 50K-100K | 5 | 60% | +25% | -22% |
| 100K-200K | 9 | 44% | +8% | -31% |
| >500K | 2 | 0% | -25% | -40% |

---

## 入场是否追高

| Context | Count | Win Rate | Avg PnL |
|---|---:|---:|---:|
| EARLY_ENTRY | 4 | 75% | +42% |
| NORMAL_ENTRY | 8 | 50% | +18% |
| LATE_ENTRY | 5 | 20% | -6% |
| CHASE_ENTRY | 3 | 0% | -21% |

这才会回答你的核心问题：

> 我到底是在早期进入，还是已经在给别人提供退出流动性？

---

# 九、关键结论

你指出的问题非常重要。  
现在必须把 Paper Lab 从：

```text
只看盈亏
```

升级为：

```text
入场证据链 + 市值上下文 + 仓位快照 + 复盘统计
```

否则纸面测试无法判断：

```text
策略有效
还是只是碰巧赚钱
买得早
还是追高
钱包结构真的有用
还是价格已经走完
```

下一步优先修：

```text
paper_entry_time
paper_size_sol
entry_market_cap_usd
discovery_market_cap_usd
signal_market_cap_usd
entry_market_cap_change_from_discovery_pct
market_cap_context_status
```

这几个字段加上后，面板才真正有交易系统的复盘价值。


---

## 片段 12 / stream_idx=2075 / len=21762


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

---

# 阶段 8：安全与部署

```text
阶段 8：Deployment and Safety

目标：
网站可访问，但不能裸奔暴露敏感信息。

一、当前 http://VPS_IP:8080 只适合临时测试。
二、推荐默认使用 SSH 隧道：
ssh -L 8080:127.0.0.1:8080 root@VPS_IP

三、如需公网访问，后续用 Nginx + Basic Auth。
本阶段不强制实现 Nginx，但必须在 README 里写明风险。

四、页面禁止显示：
- private key
- api key
- bot token
- webhook url
- 真实交易签名
- 私密配置

五、增加安全检查命令：
grep -R "private key\|api_key *= *['\"][^'\"]\+\|bot_token *= *['\"][^'\"]\+\|webhook_url *= *['\"][^'\"]\+" \
  data/gmgn_candidates_live_run/site sikk_dashboard_site_builder.py | cat

六、页面禁止任何：
- swap button
- execute button
- broadcast button
- approve real trade button

验收：
1. 页面无交易按钮。
2. dashboard_data.json 不含私钥。
3. site/ 目录不含 webhook url。
4. 安全 grep 无真实密钥。
```

---

# 阶段 9：接入主流程自动刷新

```text
阶段 9：Runtime Integration

目标：
每轮 sikk_live_run.py 完成后，自动刷新 Visual Console。

要求：
1. sikk_live_run.py 每轮结束后调用：
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

2. dashboard builder 失败不能中断主流程。
3. 失败只写入 events/live_events.jsonl。
4. 不影响 paper runner。
5. 不影响 daily report。
6. 不影响 Telegram 广播。
7. 不影响真实交易边界。

事件类型：
- DASHBOARD_BUILD_STARTED
- DASHBOARD_BUILD_FINISHED
- DASHBOARD_BUILD_FAILED

验收：
运行：
python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode once

完成后检查：
ls -lh data/gmgn_candidates_live_run/site
tail -n 50 data/gmgn_candidates_live_run/events/live_events.jsonl
```

---

# 阶段 10：测试与审计

```text
阶段 10：Testing and Audit

新增测试：
- tests/test_sikk_dashboard_schema.py
- tests/test_sikk_dashboard_site_builder.py

测试内容：
1. dashboard_data.json schema 完整
2. tokens 不为空时，每个 token main_reason 不为空
3. next_action 不为空
4. priority_level 不为空
5. MISSING token next_action = FIX_DATA_SOURCE
6. BLOCKED token next_action = COOLING
7. PAPER_OPEN token next_action = HOLD
8. system_health 存在
9. entry_block_reasons 存在
10. paper_metrics 存在

验收命令：
cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_dashboard_schema.py \
  sikk_dashboard_site_builder.py

python3 -m pytest \
  tests/test_sikk_dashboard_schema.py \
  tests/test_sikk_dashboard_site_builder.py -q

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 160

安全检查：
grep -R "gmgn-cli swap\|gmgn-cli multi-swap\|order strategy create\|onchainos swap execute\|swap execute" \
  sikk_dashboard_site_builder.py data/gmgn_candidates_live_run/site/*.js data/gmgn_candidates_live_run/site/*.html | cat

审计报告：
输出 SIKK_DASHBOARD_AUDIT_REPORT.md，必须说明：
1. 是否新增真实交易功能
2. 是否删除已有模块
3. 是否破坏主入口
4. 是否只读现有输出
5. 是否没有交易按钮
6. 是否没有私钥泄露
```

---

# Hermes / OpenClaw 分阶段执行命令

## 第一次：只做数据层

```text
/codex

执行阶段 1 和阶段 2：
1. 创建 sikk_dashboard_schema.py
2. 创建 sikk_dashboard_site_builder.py
3. 创建 tests/test_sikk_dashboard_schema.py
4. 创建 tests/test_sikk_dashboard_site_builder.py
5. 只生成 dashboard_data.json，不做 UI

严格遵守总任务书边界。
完成后运行验收命令。
输出 SIKK_DASHBOARD_PHASE_1_2_REPORT.md。
```

---

## 第二次：做页面骨架

```text
/claude_design

执行阶段 3：
创建 Visual Console 页面骨架。

修改：
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css

必须实现：
- Sidebar
- Header
- Command Center
- KPI Cards
- Funnel
- Opportunities
- Token Explorer
- Paper Lab
- Wallet Structure
- System Health
- Events

不实现真实交易。
不新增后端。
不使用 React。
输出 SIKK_DASHBOARD_PHASE_3_REPORT.md。
```

---

## 第三次：修 Token 点击详情

```text
/codex

执行阶段 4：
实现 Token Detail Drawer。

必须实现：
- 点击 token 行打开右侧 drawer
- 显示 Decision / Market / Signal / Wallet / Quote / Security / Paper / Events
- 点击遮罩关闭
- 点击 X 关闭
- Escape 关闭
- 找不到 token 时显示 Token not found
- 浏览器控制台无 JS 报错

输出 SIKK_DASHBOARD_PHASE_4_REPORT.md。
```

---

## 第四次：做筛选排序自动刷新

```text
/codex

执行阶段 5：
实现交互控制。

必须实现：
- token 搜索
- state 筛选
- wallet 筛选
- paper 筛选
- reason 搜索
- 快速筛选按钮
- 排序
- 60 秒自动刷新
- 手动刷新按钮

输出 SIKK_DASHBOARD_PHASE_5_REPORT.md。
```

---

## 第五次：做 Paper Lab 和 System Health

```text
/codex

执行阶段 6 和阶段 7：
强化 Paper Lab 和 System Health。

必须实现：
- paper metrics
- open positions
- closed positions
- failure reasons
- wallet status performance
- system health
- stale warning
- next_system_action

输出 SIKK_DASHBOARD_PHASE_6_7_REPORT.md。
```

---

## 第六次：接入主流程与审计

```text
/codex

执行阶段 8、阶段 9、阶段 10：
1. 增加安全说明
2. 检查 site 不泄露密钥
3. 接入 sikk_live_run.py 每轮结束刷新 dashboard
4. dashboard build 失败不能中断主流程
5. 增加测试
6. 输出审计报告

输出 SIKK_DASHBOARD_FINAL_AUDIT_REPORT.md。
```

---

# 最终验收总命令

```bash
cd /root/sikk-gmgn

python3 -m py_compile \
  sikk_dashboard_schema.py \
  sikk_dashboard_site_builder.py

python3 -m pytest \
  tests/test_sikk_dashboard_schema.py \
  tests/test_sikk_dashboard_site_builder.py -q

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 160

ls -lh data/gmgn_candidates_live_run/site

python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site
```

浏览器检查：

```text
http://96.126.130.99:8080/
```

更安全方式：

```bash
ssh -L 8080:127.0.0.1:8080 root@96.126.130.99
```

本地打开：

```text
http://127.0.0.1:8080
```

---

# 最终成品必须达到的效果

打开网站后必须一眼看到：

```text
1. 系统是否正常运行
2. 当前有没有 PAPER_READY / PAPER_OPEN
3. 钱包结构接入率是多少
4. 为什么没有新增 paper entry
5. 哪些 token 被 WALLET_BLOCK
6. 哪些 token 是 MISSING，原因是什么
7. 当前开放纸面仓位盈亏
8. 每个 token 的 main_reason
9. 每个 token 的 next_action
10. 点击 token 后能看到完整单币详情
11. Paper Lab 能判断策略样本是否足够
12. System Health 能告诉你下一步修哪个模块
```

---

# 本次认知升级点

现在不是“做一个简单网站”，而是要做：

```text
SIKK-SOL Visual Console Pro
```

它的核心不是 UI，而是：

```text
数据模型统一
状态解释统一
原因字段统一
下一步动作统一
Token 可点击详情
纸面验证可评估
系统健康可诊断
```

---

# 尚未解决问题

下一步真正要执行的是：

```text
1. 先跑阶段 1-2：dashboard_data.json 数据层
2. 再跑阶段 3：页面骨架
3. 再跑阶段 4：Token Detail Drawer
4. 再跑阶段 5：筛选排序自动刷新
5. 再跑阶段 6-7：Paper Lab + System Health
6. 最后跑阶段 8-10：安全、集成、测试、审计
```


---

## 片段 13 / stream_idx=2233 / len=17726


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

# 一、你现在“不能点击进去”的常见原因

一般是这几种：

```text
1. 表格 token 没有绑定 onclick
2. app.js 没有正确加载
3. dashboard_data.json 没有 token_address
4. token 行没有 data-token-address
5. CSS 盖层挡住点击
6. href 指向 token_status.md，但浏览器找不到相对路径
7. JS 报错导致后续点击事件失效
8. dashboard_data.json 里 tokens 是空数组
```

所以不要只改 UI，要同时检查：

```text
HTML 结构
app.js 点击逻辑
dashboard_data.json 字段
CSS 抽屉层
浏览器控制台错误
```

---

# 二、正确交互设计

Token 表格应该这样：

```text
点击 Token 行
  ↓
根据 token_address 从 dashboard_data.tokens 找到完整对象
  ↓
打开右侧 Detail Drawer
  ↓
展示 market / signal / wallet / quote / security / paper / events
```

不要第一版做复杂路由。

不建议现在做：

```text
/token/xxxx 单独页面
复杂前端路由
React Router
后端 API
```

先做：

```text
右侧详情抽屉
```

---

# 三、Token 总表必须有这些字段

每一行必须至少有：

```html
<tr class="token-row" data-token-address="TOKEN_ADDRESS">
```

Token 名称这一列：

```html
<td>
  <button class="token-link" data-token-address="TOKEN_ADDRESS">
    $TOKEN
  </button>
</td>
```

不要只写纯文本：

```html
<td>ABC</td>
```

否则当然不能点。

---

# 四、`dashboard_data.json` 必须包含 detail 所需字段

每个 token 对象至少要有：

```json
{
  "token_symbol": "ABC",
  "token_address": "...",
  "current_state": "WATCHING",
  "priority_level": "P3_WATCHING",
  "main_reason": "wallet_structure_missing",
  "next_action": "FIX_DATA_SOURCE",

  "market": {
    "price": null,
    "market_cap": null,
    "liquidity": null,
    "holder_count": null
  },

  "signal": {
    "signal_level": "S2",
    "signal_gate": "WAIT",
    "signal_type": "CONTROL_BOX"
  },

  "wallet_structure": {
    "wallet_structure_status": "MISSING",
    "wallet_structure_score": 0,
    "wallet_risk_score": 0,
    "counterparty_pressure_score": 0,
    "data_quality_score": 0,
    "dominant_side_status": null,
    "chip_transfer_status": null,
    "reason": "early_wallet_raw.csv missing",
    "support_signals": [],
    "risk_signals": []
  },

  "quote": {
    "quote_gate": "NOT_RUN",
    "price_deviation_pct": null,
    "reason": null
  },

  "security": {
    "security_gate": "NOT_RUN",
    "risk_level": null,
    "reason": null
  },

  "paper": {
    "paper_status": "NONE",
    "entry_price": null,
    "current_price": null,
    "unrealized_pnl_pct": null,
    "max_floating_profit_pct": null,
    "max_drawdown_pct": null,
    "exit_reason": null,
    "failure_type": null
  },

  "recent_events": []
}
```

如果 builder 只给 token 表字段，没有嵌套 detail 字段，点击后也显示不出专业详情。

---

# 五、`index.html` 要加 Detail Drawer 容器

让 OpenClaw / Hermes 改 `index.html`，加入这个结构：

```html
<div id="detailOverlay" class="detail-overlay hidden"></div>

<aside id="tokenDetailDrawer" class="token-detail-drawer hidden">
  <div class="drawer-header">
    <div>
      <div class="drawer-kicker">Token Detail</div>
      <h2 id="drawerTokenTitle">-</h2>
      <div id="drawerTokenAddress" class="muted mono">-</div>
    </div>
    <button id="drawerCloseBtn" class="drawer-close">×</button>
  </div>

  <div id="drawerContent" class="drawer-content">
    <!-- app.js 注入详情 -->
  </div>
</aside>
```

---

# 六、`style.css` 要有抽屉样式

加入：

```css
.detail-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: 80;
}

.detail-overlay.hidden {
  display: none;
}

.token-detail-drawer {
  position: fixed;
  top: 0;
  right: 0;
  width: min(720px, 92vw);
  height: 100vh;
  background: #111827;
  border-left: 1px solid #273244;
  box-shadow: -20px 0 60px rgba(0, 0, 0, 0.45);
  z-index: 90;
  overflow-y: auto;
  transform: translateX(0);
  transition: transform 160ms ease;
}

.token-detail-drawer.hidden {
  transform: translateX(105%);
}

.drawer-header {
  position: sticky;
  top: 0;
  background: #111827;
  border-bottom: 1px solid #273244;
  padding: 18px 20px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  z-index: 2;
}

.drawer-kicker {
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.drawer-header h2 {
  margin: 4px 0;
  font-size: 22px;
}

.drawer-close {
  background: #1f2937;
  color: #e5e7eb;
  border: 1px solid #374151;
  border-radius: 10px;
  width: 36px;
  height: 36px;
  cursor: pointer;
  font-size: 22px;
}

.drawer-content {
  padding: 18px 20px 40px;
}

.detail-section {
  background: #0b1220;
  border: 1px solid #1f2937;
  border-radius: 14px;
  padding: 14px;
  margin-bottom: 14px;
}

.detail-section h3 {
  margin: 0 0 10px;
  font-size: 15px;
  color: #e5e7eb;
}

.detail-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px 14px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.detail-label {
  font-size: 11px;
  color: #94a3b8;
}

.detail-value {
  font-size: 13px;
  color: #e5e7eb;
  word-break: break-word;
}

.token-link {
  background: transparent;
  border: none;
  color: #93c5fd;
  cursor: pointer;
  font-weight: 700;
  padding: 0;
}

.token-link:hover {
  text-decoration: underline;
}

.token-row {
  cursor: pointer;
}

.token-row:hover {
  background: rgba(59, 130, 246, 0.08);
}
```

---

# 七、`app.js` 要加点击逻辑

核心逻辑如下：

```javascript
let dashboardData = null;
let tokenIndex = new Map();

async function loadDashboardData() {
  const response = await fetch("./dashboard_data.json?ts=" + Date.now());
  dashboardData = await response.json();

  tokenIndex = new Map(
    (dashboardData.tokens || []).map(t => [String(t.token_address), t])
  );

  renderDashboard(dashboardData);
  bindDrawerEvents();
}

function bindDrawerEvents() {
  const closeBtn = document.getElementById("drawerCloseBtn");
  const overlay = document.getElementById("detailOverlay");

  if (closeBtn) closeBtn.addEventListener("click", closeTokenDrawer);
  if (overlay) overlay.addEventListener("click", closeTokenDrawer);

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeTokenDrawer();
  });
}

function bindTokenClicks() {
  document.querySelectorAll("[data-token-address]").forEach(el => {
    el.addEventListener("click", (e) => {
      const tokenAddress = e.currentTarget.getAttribute("data-token-address");
      if (!tokenAddress) return;
      openTokenDrawer(tokenAddress);
    });
  });
}

function openTokenDrawer(tokenAddress) {
  const token=[REDACTED]

  if (!token) {
    console.warn("Token not found:", tokenAddress);
    return;
  }

  document.getElementById("drawerTokenTitle").textContent =
    `$${token.token_symbol || "UNKNOWN"} | ${token.current_state || "-"}`;

  document.getElementById("drawerTokenAddress").textContent =
    token.token_address || "-";

  document.getElementById("drawerContent").innerHTML = renderTokenDetail(token);

  document.getElementById("detailOverlay").classList.remove("hidden");
  document.getElementById("tokenDetailDrawer").classList.remove("hidden");
}

function closeTokenDrawer() {
  document.getElementById("detailOverlay").classList.add("hidden");
  document.getElementById("tokenDetailDrawer").classList.add("hidden");
}

function val(x) {
  if (x === null || x === undefined || x === "") return "-";
  return String(x);
}

function esc(x) {
  return val(x)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderField(label, value) {
  return `
    <div class="detail-item">
      <div class="detail-label">${esc(label)}</div>
      <div class="detail-value">${esc(value)}</div>
    </div>
  `;
}

function renderSection(title, fields) {
  return `
    <section class="detail-section">
      <h3>${esc(title)}</h3>
      <div class="detail-grid">
        ${fields.map(([label, value]) => renderField(label, value)).join("")}
      </div>
    </section>
  `;
}

function renderTokenDetail(t) {
  const market = t.market || {};
  const signal = t.signal || {};
  const wallet = t.wallet_structure || {};
  const quote = t.quote || {};
  const security = t.security || {};
  const paper = t.paper || {};

  return `
    ${renderSection("Decision", [
      ["Current State", t.current_state],
      ["Priority", t.priority_level],
      ["Main Reason", t.main_reason],
      ["Next Action", t.next_action],
      ["Last Update", t.last_update],
    ])}

    ${renderSection("Market", [
      ["Price", market.price],
      ["Market Cap", market.market_cap],
      ["Liquidity", market.liquidity],
      ["Holders", market.holder_count],
      ["Pool", market.pool_address],
    ])}

    ${renderSection("Signal", [
      ["Signal Level", signal.signal_level || t.signal_level],
      ["Signal Gate", signal.signal_gate || t.signal_gate],
      ["Signal Type", signal.signal_type],
      ["Invalid Level", signal.invalid_level],
      ["Reason", signal.reason],
    ])}

    ${renderSection("Wallet Structure", [
      ["Status", wallet.wallet_structure_status || t.wallet_structure_status],
      ["Structure Score", wallet.wallet_structure_score || t.wallet_structure_score],
      ["Risk Score", wallet.wallet_risk_score || t.wallet_risk_score],
      ["Counterparty Pressure", wallet.counterparty_pressure_score || t.counterparty_pressure_score],
      ["Data Quality", wallet.data_quality_score || t.data_quality_score],
      ["Dominant Side", wallet.dominant_side_status],
      ["Chip Transfer", wallet.chip_transfer_status],
      ["Reason", wallet.reason],
    ])}

    ${renderSection("Quote / Security", [
      ["Quote Gate", quote.quote_gate || t.quote_gate],
      ["Price Deviation", quote.price_deviation_pct],
      ["Quote Reason", quote.reason],
      ["Security Gate", security.security_gate || t.security_gate],
      ["Risk Level", security.risk_level],
      ["Security Reason", security.reason],
    ])}

    ${renderSection("Paper", [
      ["Paper Status", paper.paper_status || t.paper_status],
      ["Entry Price", paper.entry_price],
      ["Current Price", paper.current_price],
      ["Unrealized PnL %", paper.unrealized_pnl_pct || t.paper_pnl_pct],
      ["Max Floating Profit %", paper.max_floating_profit_pct],
      ["Max Drawdown %", paper.max_drawdown_pct],
      ["Exit Reason", paper.exit_reason],
      ["Failure Type", paper.failure_type],
    ])}

    ${renderEvents(t.recent_events || [])}
  `;
}

function renderEvents(events) {
  if (!events.length) {
    return `
      <section class="detail-section">
        <h3>Recent Events</h3>
        <div class="muted">No recent events.</div>
      </section>
    `;
  }

  return `
    <section class="detail-section">
      <h3>Recent Events</h3>
      <div class="event-list">
        ${events.map(e => `
          <div class="event-item">
            <div class="muted">${esc(e.time)}</div>
            <div><strong>${esc(e.event_type)}</strong> ${esc(e.message)}</div>
          </div>
        `).join("")}
      </div>
    </section>
  `;
}
```

重点：渲染完 Token 表后必须调用：

```javascript
bindTokenClicks();
```

比如：

```javascript
function renderTokenTable(tokens) {
  const tbody = document.getElementById("tokenTableBody");

  tbody.innerHTML = tokens.map(t => `
    <tr class="token-row" data-token-address="${esc(t.token_address)}">
      <td>
        <button class="token-link" data-token-address="${esc(t.token_address)}">
          $${esc(t.token_symbol)}
        </button>
      </td>
      <td>${esc(t.current_state)}</td>
      <td>${esc(t.wallet_structure_status)}</td>
      <td>${esc(t.wallet_structure_score)}</td>
      <td>${esc(t.wallet_risk_score)}</td>
      <td>${esc(t.counterparty_pressure_score)}</td>
      <td>${esc(t.paper_status)}</td>
      <td>${esc(t.paper_pnl_pct)}</td>
      <td>${esc(t.main_reason)}</td>
      <td>${esc(t.next_action)}</td>
    </tr>
  `).join("");

  bindTokenClicks();
}
```

---

# 八、注意一个常见 bug：按钮和行同时绑定会触发两次

如果 `<tr>` 和 `<button>` 都有 `data-token-address`，点击按钮可能触发两次。  
可以这样避免：

```javascript
function bindTokenClicks() {
  document.querySelectorAll(".token-row").forEach(row => {
    row.addEventListener("click", (e) => {
      const tokenAddress = row.getAttribute("data-token-address");
      openTokenDrawer(tokenAddress);
    });
  });
}
```

然后 token button 不单独绑定，保留样式即可：

```html
<button class="token-link" type="button">$ABC</button>
```

---

# 九、必须增加空数据提示

如果点击后没有详情，不要空白，要显示：

```text
Token detail missing
```

代码：

```javascript
function openTokenDrawer(tokenAddress) {
  const token=[REDACTED]

  if (!token) {
    document.getElementById("drawerTokenTitle").textContent = "Token not found";
    document.getElementById("drawerTokenAddress").textContent = tokenAddress || "-";
    document.getElementById("drawerContent").innerHTML = `
      <section class="detail-section">
        <h3>Missing Detail</h3>
        <div class="detail-value">dashboard_data.json 中没有找到该 token 的详情。</div>
      </section>
    `;
    document.getElementById("detailOverlay").classList.remove("hidden");
    document.getElementById("tokenDetailDrawer").classList.remove("hidden");
    return;
  }

  ...
}
```

---

# 十、给 OpenClaw / Hermes 的精确修复指令

直接复制这段：

```text
任务：修复 SIKK Visual Console v2 中 Token 不能点击进入详情的问题。

当前问题：
网站能打开，但 Token 总表不能点击查看单币详情，导致无法查看每个 token 的 market、signal、wallet_structure、quote/security、paper、reason、next_action 和 recent_events。

要求：
1. 不新增后端。
2. 不使用数据库。
3. 不使用 React。
4. 不接真实 swap。
5. 不改变 paper runner 交易逻辑。
6. 不删除已有模块。
7. 只修改静态网站相关文件和 dashboard_data 构建逻辑。

允许修改：
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css

必须实现：

一、dashboard_data.json
每个 token 必须包含完整 detail 字段：
- token_symbol
- token_address
- current_state
- priority_level
- main_reason
- next_action
- market
- signal
- wallet_structure
- quote
- security
- paper
- recent_events

二、index.html
增加右侧 Token Detail Drawer：
- detailOverlay
- tokenDetailDrawer
- drawerTokenTitle
- drawerTokenAddress
- drawerContent
- drawerCloseBtn

三、Token 表格
每个 tr 必须有：
data-token-address="..."

每一行 class="token-row"。
点击任意 token 行，打开对应详情抽屉。

四、app.js
实现：
- tokenIndex = new Map(tokens.map(t => [token_address, t]))
- bindTokenClicks()
- openTokenDrawer(tokenAddress)
- closeTokenDrawer()
- renderTokenDetail(token)
- renderSection()
- renderField()
- renderEvents()

要求：
- 点击 token 行打开 drawer。
- 点击遮罩关闭 drawer。
- 点击 X 关闭 drawer。
- 按 Escape 关闭 drawer。
- 找不到 token 时显示 Token not found。
- main_reason 和 next_action 不能为空。
- 每次重新渲染表格后重新 bindTokenClicks()。

五、style.css
增加：
- detail-overlay
- token-detail-drawer
- drawer-header
- drawer-content
- detail-section
- detail-grid
- token-row:hover
- token-link

六、验收命令：
cd /root/sikk-gmgn

python3 -m py_compile sikk_dashboard_site_builder.py

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 160

python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

验收标准：
1. 打开网站后，Token 总表里的每一行都可以点击。
2. 点击后右侧打开详情抽屉。
3. 详情抽屉显示：
   - Decision
   - Market
   - Signal
   - Wallet Structure
   - Quote / Security
   - Paper
   - Recent Events
4. 关闭按钮有效。
5. 点击遮罩有效。
6. Escape 关闭有效。
7. 浏览器控制台无 JS 报错。
```

---

# 十一、你自己在 VPS 上怎么检查

## 1. 重新生成网站

```bash
cd /root/sikk-gmgn

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site
```

## 2. 检查 dashboard_data 是否有 token detail

```bash
python3 - <<'PY'
import json
from pathlib import Path

p = Path("data/gmgn_candidates_live_run/site/dashboard_data.json")
d = json.loads(p.read_text())

tokens = d.get("tokens", [])
print("tokens:", len(tokens))

if tokens:
    t = tokens[0]
    print("sample keys:", sorted(t.keys()))
    print("token=[REDACTED] t.get("token_symbol"), t.get("token_address"))
    print("has market:", "market" in t)
    print("has signal:", "signal" in t)
    print("has wallet_structure:", "wallet_structure" in t)
    print("has quote:", "quote" in t)
    print("has security:", "security" in t)
    print("has paper:", "paper" in t)
    print("main_reason:", t.get("main_reason"))
    print("next_action:", t.get("next_action"))
PY
```

应该看到：

```text
has market: True
has signal: True
has wallet_structure: True
has quote: True
has security: True
has paper: True
```

---

## 3. 检查 HTML 有没有 drawer

```bash
grep -n "tokenDetailDrawer\|detailOverlay\|drawerContent" data/gmgn_candidates_live_run/site/index.html
```

应该能看到对应节点。

---

## 4. 检查 JS 有没有点击函数

```bash
grep -n "openTokenDrawer\|bindTokenClicks\|renderTokenDetail" data/gmgn_candidates_live_run/site/app.js
```

应该能看到函数。

---

## 5. 检查 CSS 有没有 drawer 样式

```bash
grep -n "token-detail-drawer\|detail-overlay\|detail-section" data/gmgn_candidates_live_run/site/style.css
```

---

# 十二、如果还是不能点击，按这个排查

## 1. 浏览器控制台是否有 JS 错误

最常见：

```text
Cannot read properties of null
Unexpected token
dashboard_data.json 404
```

修法：

```text
先修 JS 报错，任何一个 JS 报错都可能导致点击事件不绑定。
```

---

## 2. dashboard_data.json 是否加载成功

浏览器直接打开：

```text
http://96.126.130.99:8080/dashboard_data.json
```

必须能看到 JSON。

---

## 3. app.js 是否加载成功

打开：

```text
http://96.126.130.99:8080/app.js
```

如果 404，说明路径错了。

---

## 4. token 行是否真的有 data-token-address

在浏览器检查元素，看 `<tr>` 有没有：

```html
data-token-address="..."
```

没有就说明表格渲染逻辑没写对。

---

## 5. 是否有透明层挡住表格

CSS 里检查有没有：

```css
pointer-events: none;
z-index 很高的 overlay;
```

如果 overlay 没隐藏，会挡住点击。

---

# 最短结论

你现在要修的不是“点击链接跳转”，而是做：

```text
Token Detail Drawer
```

最小闭环是：

```text
dashboard_data.json 每个 token 有完整详情
→ Token 表格行带 data-token-address
→ app.js 绑定 click
→ 右侧 drawer 展示详情
→ 可关闭
```

这个补完后，面板才从“列表展示”变成“可分析控制台”。


---

## 片段 14 / stream_idx=2462 / len=8339


对，现在这个网站只是“能打开”，还不是专业面板。  
你现在需要做的不是继续小修样式，而是升级成：

# SIKK-SOL Visual Console v2

定位：

```text
本地 / VPS 静态专业控制台
读取现有 SIKK 输出
展示系统状态、机会、阻断原因、纸面仓位、钱包结构、未入场原因
不执行交易
不接真实 swap
不新增复杂后端
```

我这边没有稳定拉取到你这个 IP 页面内容，所以不能逐项点评页面代码；但根据你描述“太简陋、功能不完善”，现在应该直接按 v2 标准重做信息架构。

---

# 一、为什么现在看起来简陋

大概率是因为当前页面只是：

```text
KPI + 简单表格 + 一些事件
```

但专业控制台需要的是：

```text
分层导航
状态优先级
漏斗诊断
机会池
风险池
单币详情
纸面仓位
未入场原因
系统健康
自动刷新
```

所以问题不是“颜色不好看”，而是：

> **数据没有被组织成决策视图。**

---

# 二、v2 网站必须改成 6 个页面 / 分区

## 1. Command Center｜总控台

一打开先看到：

```text
系统是否正常
本轮发现多少 token
PAPER_OPEN 有几个
PAPER_READY 有几个
WALLET_BLOCK 有几个
钱包结构接入率
新增纸面入场数
未入场主因
```

顶部 KPI 卡片：

```text
Token Count
Wallet Coverage
PAPER_READY
PAPER_OPEN
WALLET_BLOCK
Open Positions
Closed Win Rate
Avg Closed PnL
```

---

## 2. Funnel｜流程漏斗

必须可视化这条链：

```text
Candidates
 → Signal Ready
 → Wallet Support
 → Quote/Security Pass
 → PAPER_READY
 → PAPER_OPEN
```

你现在最需要看到：

```text
到底卡在钱包结构？
卡在 K线？
卡在 quote/security？
还是 paper runner 没入场？
```

这比单纯表格重要。

---

## 3. Opportunities｜重点机会

只显示最值得看的 token：

```text
PAPER_OPEN
PAPER_READY
WALLET_SUPPORT
S3 / S4
quote/security 通过
```

字段：

```text
Token
Priority
State
Signal
Wallet
Structure Score
Risk Score
Counterparty
Paper PnL
Next Action
Reason
```

这个区域不能被 48 个普通 WATCHING 淹没。

---

## 4. Token Explorer｜Token 总表

必须支持：

```text
搜索 token
按 current_state 筛选
按 wallet_structure_status 筛选
按 paper_status 筛选
按 reason 搜索
按 priority 排序
```

字段必须有：

```text
token_symbol
current_state
priority_level
signal_gate
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
quote_gate
security_gate
paper_status
paper_pnl_pct
main_reason
next_action
last_update
```

点击某个 token 后，右侧弹出详情面板。

---

## 5. Token Detail｜单币详情抽屉

点击 token 后展示：

```text
市场数据
K线信号
钱包结构
quote/security
paper 状态
阻断原因
下一步动作
最近事件
```

这是你现在最缺的。  
否则你只能在表格里猜。

---

## 6. Paper Lab｜纸面验证区

展示：

```text
当前开放仓位
已关闭仓位
胜率
平均收益
最大回撤
失败原因 Top
不同 wallet status 的表现
```

当前最需要看：

```text
WALLET_SUPPORT 的 paper 表现
WALLET_BLOCK 后是否真的规避失败
EXIT_MONITOR 是否有效
```

---

# 三、v2 页面交互必须补齐

第一版至少要有这些功能：

```text
1. 自动刷新 dashboard_data.json
2. 刷新时间显示
3. Token 搜索
4. State 筛选
5. Wallet 筛选
6. Paper 筛选
7. Reason 搜索
8. Token 点击详情
9. Priority 排序
10. Missing / Error 高亮
```

不要先做复杂图表。  
先把“看得懂”做好。

---

# 四、视觉布局建议

页面结构：

```text
左侧 Sidebar
  - Command Center
  - Opportunities
  - Token Explorer
  - Paper Lab
  - System Health
  - Events

顶部 Header
  - SIKK-SOL Visual Console
  - Last Update
  - Runtime Status
  - Auto Refresh 状态

主体区域
  - KPI Cards
  - Funnel
  - Tables
  - Detail Drawer
```

颜色规则：

| 状态 | 颜色 |
|---|---|
| PAPER_OPEN / PAPER_READY | 绿色 |
| WALLET_SUPPORT | 青绿色 |
| WATCHING / PAUSE | 黄色 |
| BLOCKED / WALLET_BLOCK | 红色 |
| MISSING | 灰色 |
| ERROR | 紫红色 |

---

# 五、必须补的数据字段

你现在页面简陋，通常不是 UI 问题，而是 `dashboard_data.json` 不够完整。

v2 的 `dashboard_data.json` 应该长这样：

```json
{
  "meta": {
    "generated_at": "...",
    "base_dir": "data/gmgn_candidates_live_run",
    "runtime_status": "OK"
  },
  "kpi": {},
  "funnel": {},
  "tokens": [],
  "opportunities": [],
  "paper_positions": [],
  "wallet_structure_summary": {},
  "wallet_missing_reasons": [],
  "entry_block_reasons": [],
  "events": [],
  "system_health": {}
}
```

每个 token 至少要有：

```json
{
  "token_symbol": "ABC",
  "token_address": "...",
  "current_state": "WATCHING",
  "priority_level": "P3_WATCHING",
  "signal_level": "S2",
  "signal_gate": "WAIT",
  "wallet_structure_status": "MISSING",
  "wallet_structure_score": 0,
  "wallet_risk_score": 0,
  "counterparty_pressure_score": 0,
  "data_quality_score": 0,
  "quote_gate": "NOT_RUN",
  "security_gate": "NOT_RUN",
  "paper_status": "NONE",
  "paper_pnl_pct": null,
  "main_reason": "wallet_structure_missing: early_wallet_raw.csv missing",
  "next_action": "FIX_DATA_SOURCE",
  "last_update": "..."
}
```

关键是：

```text
main_reason 不能为空
next_action 不能为空
priority_level 不能为空
```

---

# 六、现在公网 8080 也要注意

你现在是：

```text
http://96.126.130.99:8080/
```

这意味着很可能是公网直接暴露。

建议你至少做一个安全处理：

```text
第一阶段：只用 SSH 隧道访问
第二阶段：Nginx + Basic Auth
第三阶段：再考虑域名 / HTTPS
```

当前如果面板里有 token、仓位、日志、webhook 配置、路径信息，不建议长期裸奔公网 8080。

更安全的方式：

```bash
ssh -L 8080:127.0.0.1:8080 root@96.126.130.99
```

然后本地访问：

```text
http://127.0.0.1:8080
```

---

# 七、给 OpenClaw / Hermes 的 v2 重做指令

直接复制：

```text
任务：升级 SIKK-SOL 静态可视化网站为 Visual Console v2。

当前问题：
现有 http://96.126.130.99:8080 页面太简陋，信息散乱，无法专业表达系统状态、机会、风险、纸面仓位和未入场原因。

目标：
重做 data/gmgn_candidates_live_run/site/ 下的静态网站控制台。
只做前端静态控制台，不新增后端，不使用数据库，不接真实交易，不加入 swap 按钮。

允许修改 / 新增：
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- data/gmgn_candidates_live_run/site/dashboard_data.json

禁止：
- 不删除已有模块
- 不改 sikk_live_run.py 主交易逻辑
- 不改 paper runner 交易逻辑
- 不执行真实 swap
- 不新增 FastAPI / React / 数据库
- 不新增登录系统
- 不新增 Telegram 功能

页面结构必须包含：

1. Sidebar 导航
- Command Center
- Opportunities
- Token Explorer
- Paper Lab
- System Health
- Events

2. 顶部 Header
- SIKK-SOL Visual Console
- generated_at
- runtime_status
- auto refresh 状态

3. Command Center
- KPI cards:
  token_count
  wallet_coverage
  paper_ready_count
  paper_open_count
  wallet_block_count
  wallet_missing_count
  open_positions
  closed_win_rate
  avg_closed_pnl

4. Pipeline Funnel
展示：
- candidates
- signal_ready
- wallet_support
- quote_security_pass
- paper_ready
- paper_open

5. Opportunities
只展示：
- PAPER_OPEN
- PAPER_READY
- WALLET_SUPPORT
- S3/S4 signal
- quote/security pass

6. Token Explorer
字段：
- token_symbol
- current_state
- priority_level
- signal_gate
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

功能：
- token 搜索
- state 筛选
- wallet 筛选
- paper 筛选
- reason 搜索
- priority 排序
- 点击 token 打开详情面板

7. Token Detail Drawer
点击 token 后显示：
- market
- signal
- wallet_structure
- quote
- security
- paper
- main_reason
- next_action
- recent_events

8. Paper Lab
显示：
- 当前开放仓位
- 已关闭仓位统计
- 胜率
- 平均收益
- 最大回撤
- 失败原因 Top
- paper_positions 表

9. Entry Block Reasons
显示：
- wallet_structure_missing
- wallet_block
- signal_not_ready
- quote_not_ready
- security_not_ready
- paper_runner_not_called
- state_not_ready
- data_quality_low

10. System Health
显示：
- live_state 是否存在
- token_status 数量
- wallet_structure_decision 数量
- paper files 是否存在
- events 是否存在
- dashboard_data generated_at
- stale data warning

视觉要求：
- 深色专业风格
- 卡片化布局
- 表格紧凑
- 状态 badge
- PAPER_OPEN/PAPER_READY 绿色
- WALLET_SUPPORT 青绿色
- WATCHING/PAUSE 黄色
- BLOCKED/WALLET_BLOCK 红色
- MISSING 灰色
- ERROR 紫红色
- Reason 和 Next Action 不允许为空

数据要求：
dashboard_data.json 必须包含：
- meta
- kpi
- funnel
- tokens
- opportunities
- wallet_structure_summary
- wallet_missing_reasons
- entry_block_reasons
- paper_positions
- paper_metrics
- events
- system_health

验收命令：
cd /root/sikk-gmgn

python3 -m py_compile sikk_dashboard_site_builder.py

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120

ls -lh data/gmgn_candidates_live_run/site

python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

验收标准：
打开网站后必须一眼看到：
1. 系统是否正常
2. 当前有没有 PAPER_READY / PAPER_OPEN
3. 钱包结构接入率
4. 为什么没有新增 paper entry
5. 哪些 token 被 BLOCK
6. 当前纸面仓位盈亏
7. 每个 token 的 reason 和 next_action
8. 哪些数据源缺失
```

---

# 八、开发顺序，不要一步到位

让 Hermes 分 3 次做。

## Round 1：只重做 `dashboard_data.json`

目标：

```text
数据完整，不管 UI
```

验收：

```bash
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120
```

必须看到：

```text
kpi
funnel
tokens
entry_block_reasons
paper_positions
system_health
```

---

## Round 2：重做 UI

目标：

```text
index.html + app.js + style.css
```

先实现：

```text
KPI
漏斗
Token 表
筛选
详情抽屉
纸面仓位
事件
```

---

## Round 3：接入主流程刷新

每轮 `sikk_live_run.py` 结束后自动刷新 site：

```bash
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site
```

失败不能中断主系统，只写事件。

---

# 九、最短判断

你现在这个网站不是“修修样式”就行。  
应该升级为：

```text
SIKK-SOL Visual Console v2
```

核心不是更炫，而是：

```text
信息分层
机会优先
原因解释
筛选排序
单币详情
纸面表现
系统健康
```

这样你才会从“看一堆散乱数据”变成“看专业决策控制台”。


---

## 片段 15 / stream_idx=2740 / len=5419


这段内容可以直接升级你对 Hermes 的理解：

> **Hermes 是 Agent 调度层，tmux 是进程隔离层，项目文件是长期记忆层。**

你现在如果要专业化运行 SIKK，不应该只靠 Hermes 的 `/branch`、`/background`、`/agents`。这些解决的是 **Hermes 内部任务管理**。  
而 tmux 解决的是更底层的问题：

```text
不同 Hermes 会话之间互不干扰
SSH 断开后任务继续运行
主系统 loop、网站服务、开发 Agent、测试 Agent 分开管理
每个会话有自己的工作目录和上下文
```

---

# 一、SIKK 应该怎么用 tmux 隔离

你的 SIKK 项目建议固定 6 个 tmux 会话：

| tmux 会话 | 作用 | 里面跑什么 |
|---|---|---|
| `sikk-live` | 主系统运行 | `sikk_live_run.py --mode loop` |
| `sikk-dashboard` | 可视化网站 | `http.server 8080` + dashboard builder |
| `sikk-builder` | Hermes 开发 | `/branch`、`/codex`、`/claude_design` |
| `sikk-verifier` | 测试验证 | `pytest`、`py_compile`、安全 grep |
| `sikk-logs` | 查看输出 | `tail events`、看日报、看面板 |
| `sikk-telegram` | 广播/网关 | Telegram 广播任务或状态检查 |

这样分开后：

```text
主运行不会被开发打断
网站服务不会被测试影响
开发 Agent 不会污染运行 Agent 上下文
日志观察不会误操作代码
```

---

# 二、标准创建命令

进入项目：

```bash
cd /root/sikk-gmgn
```

创建主运行会话：

```bash
tmux new -s sikk-live -c /root/sikk-gmgn
```

运行：

```bash
python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode loop \
  --interval-sec 600
```

退出但不中断：

```text
Ctrl+b，然后按 d
```

查看所有会话：

```bash
tmux ls
```

回到会话：

```bash
tmux attach -t sikk-live
```

---

# 三、给 SIKK 创建一键 tmux 脚本

在项目里创建：

```bash
nano /root/sikk-gmgn/start_sikk_tmux.sh
```

写入：

```bash
#!/usr/bin/env bash
set -e

PROJECT_DIR="/root/sikk-gmgn"

create_session() {
  local name="$1"
  local cmd="$2"

  if tmux has-session -t "$name" 2>/dev/null; then
    echo "[exists] $name"
  else
    tmux new-session -d -s "$name" -c "$PROJECT_DIR" "$cmd"
    echo "[created] $name"
  fi
}

create_session "sikk-live" "bash"
create_session "sikk-dashboard" "bash"
create_session "sikk-builder" "bash"
create_session "sikk-verifier" "bash"
create_session "sikk-logs" "bash"
create_session "sikk-telegram" "bash"

tmux ls
```

授权：

```bash
chmod +x /root/sikk-gmgn/start_sikk_tmux.sh
```

运行：

```bash
cd /root/sikk-gmgn
./start_sikk_tmux.sh
```

---

# 四、每个会话的固定职责

## 1. `sikk-live`

只跑主系统：

```bash
python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode loop \
  --interval-sec 600
```

规则：

```text
不在这里改代码
不在这里跑 Hermes 开发任务
不在这里测试新功能
```

---

## 2. `sikk-dashboard`

只跑网站面板：

```bash
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site
```

启动网站：

```bash
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site
```

更安全访问方式：

```bash
ssh -L 8080:127.0.0.1:8080 root@你的VPS_IP
```

本地打开：

```text
http://127.0.0.1:8080
```

---

## 3. `sikk-builder`

只给 Hermes / OpenClaw / Codex 开发：

```text
/branch
/kanban
/codebase_inspection
/codex
/claude_design
/dogfood
```

当前最适合跑：

```text
SIKK Dashboard Site Builder
wallet_structure_missing 修复
paper report 输出一致性修复
```

---

## 4. `sikk-verifier`

只跑验证：

```bash
python3 -m py_compile \
  sikk_live_run.py \
  sikk_dashboard_site_builder.py \
  sikk_paper_live_runner.py \
  sikk_live_orchestrator.py
```

测试：

```bash
python3 -m pytest tests/test_sikk_live_run.py tests/test_sikk_runtime_v02.py -q
```

安全边界：

```bash
grep -R "gmgn-cli swap\|gmgn-cli multi-swap\|order strategy create\|onchainos swap execute\|swap execute" \
  sikk_*.py run_sikk_gmgn_pipeline.py tests/*.py | cat
```

---

## 5. `sikk-logs`

只看状态：

```bash
sed -n '1,220p' data/gmgn_candidates_live_run/live_board.md
```

```bash
tail -n 80 data/gmgn_candidates_live_run/events/live_events.jsonl
```

```bash
ls -lh data/gmgn_candidates_live_run/paper_live/daily_reports/
```

```bash
sed -n '1,200p' data/gmgn_candidates_live_run/state_machine/state_summary.md
```

---

# 五、tmux + Hermes 的分工

你要记住这张关系：

```text
tmux = 外层隔离
Hermes = 内层调度
/branch = 任务分支
/background = Hermes 内部后台任务
/agents = Hermes 内部 Agent 状态
/rollback = 文件级安全回滚
```

所以：

```bash
tmux ls
```

看的是终端会话。

```text
/agents
```

看的是 Hermes 内部 Agent 任务。

两者不是一回事。

---

# 六、专业化使用规则

你后面应该固定这些规则：

```text
1. 一个项目一个 tmux 会话组
2. 一个长期任务一个 tmux session
3. 一个 Hermes 开发任务一个独立 session
4. 主运行 session 不改代码
5. Builder session 不跑主 loop
6. Verifier session 不写业务逻辑
7. Logs session 只观察
8. 重大改动前先 git status
9. 改坏用 /rollback 或 git restore
10. 多 Agent 同时改代码时再用 git worktree
```

---

# 七、进一步专业化：tmux + git worktree

tmux 只隔离进程，不隔离文件。  
如果两个 Agent 同时改 `/root/sikk-gmgn`，仍然可能冲突。

多 Agent 并行改代码时，用：

```bash
cd /root/sikk-gmgn
git worktree add /root/sikk-gmgn-dashboard dashboard-site
git worktree add /root/sikk-gmgn-walletfix wallet-missing-fix
```

然后：

```bash
tmux new -s sikk-dashboard-dev -c /root/sikk-gmgn-dashboard
tmux new -s sikk-walletfix-dev -c /root/sikk-gmgn-walletfix
```

这才是真正的代码层隔离。

当前阶段可以先不用 worktree；等你同时让多个 Agent 改代码时再上。

---

# 八、你的最终专业结构

```text
VPS
├── tmux:sikk-live        → 主系统 loop
├── tmux:sikk-dashboard   → 静态网站服务
├── tmux:sikk-builder     → Hermes 开发任务
├── tmux:sikk-verifier    → 测试 / 编译 / 安全检查
├── tmux:sikk-logs        → 日志与日报观察
└── tmux:sikk-telegram    → Telegram 广播观察
```

这套结构就能做到：

```text
运行不中断
开发不干扰
面板独立看
测试独立跑
Agent 上下文不串
SSH 断开不影响任务
文件改坏可回滚
```

---

# 最短结论

你这段话对 SIKK 的实际意义是：

> **Hermes 解决 Agent 调度，tmux 解决本地进程隔离。两者结合，才是专业本地 Agent 工作台。**

你现在最应该做的是：

```bash
cd /root/sikk-gmgn
./start_sikk_tmux.sh
tmux ls
```

然后固定：

```text
sikk-live 跑系统
sikk-dashboard 看网站
sikk-builder 用 Hermes 开发
sikk-verifier 跑测试
sikk-logs 看结果
```

这样你的 SIKK 才不会继续“散乱”。


---

## 片段 16 / stream_idx=2794 / len=309


所以这里给出所有运行 Hermes Agent 或任何本地 Agent 的用户都应该知道的答案：tmux 是隔离层。它是防止 Agent 上下文相互干扰的最便宜、最简单、最可靠的方法。我并行运行很多 Hermes 会话。每个项目一个会话，每个活跃模型一个会话，有时两者兼有。每个会话都有自己的工作目录、内存上下文和对话线程。工作会话、个人会话和客户端会话互不干扰。在我的主服务器上，通常每天都会运行 6 到 10 个 Hermes 会话。一个会话用于编码项目，另一个会话用于研究，还有一个会话用于撰写内容，第四个会话用于 Telegram 网关路由请求，第五个会话用于模型基准测试。切换会话零开销，上下文干扰风险为零。


---

## 片段 17 / stream_idx=2974 / len=8213


这段话的核心可以直接迁移到你的 SIKK 项目：

> **tmux 负责进程隔离，Hermes 负责 Agent 调度，项目状态文件负责长期记忆。**

你现在要把它理解成一套专业工作台：

```text
tmux = 物理隔离层
Hermes session = Agent 上下文层
SIKK_PROJECT_STATE.md = 项目记忆层
git / 文件检查点 = 回滚层
```

---

# 一、tmux 对你有什么用

你现在的问题不是只缺 AI，而是多个任务会互相干扰：

```text
1. SIKK 主运行 loop
2. Telegram 广播
3. dashboard 网站构建
4. paper runner 测试
5. wallet structure 修复
6. Hermes / OpenClaw 开发任务
7. 日志查看
```

这些如果都在一个终端、一个 Hermes 会话里做，就会乱。

tmux 的作用是：

```text
每个任务一个独立终端环境
每个 Hermes 会话互不影响
断开 SSH 后任务继续跑
随时 attach 回去查看
```

---

# 二、SIKK 项目推荐 tmux 会话规划

你可以固定 6 个 tmux session。

| tmux 会话 | 作用 | 是否长期运行 |
|---|---|---|
| `sikk-live` | SIKK 主运行 loop | 是 |
| `sikk-telegram` | Telegram 广播 / 定时任务观察 | 是 |
| `sikk-dashboard` | 可视化网站生成与 http server | 是 |
| `sikk-builder` | Hermes / Codex 写代码 | 否 |
| `sikk-verifier` | 测试、编译、安全检查 | 否 |
| `sikk-logs` | 看 live_board、events、paper 日报 | 是 |

不要把所有事情塞进一个 session。

---

# 三、最基础 tmux 命令

## 创建会话

```bash
tmux new -s sikk-live -c /root/sikk-gmgn
```

## 退出但不停止

按：

```text
Ctrl + b
然后按 d
```

这叫 detach。进程还在跑。

## 查看所有会话

```bash
tmux ls
```

## 回到某个会话

```bash
tmux attach -t sikk-live
```

## 杀掉某个会话

```bash
tmux kill-session -t sikk-live
```

---

# 四、你的 SIKK tmux 标准启动方式

## 1. 主运行会话：`sikk-live`

```bash
tmux new -s sikk-live -c /root/sikk-gmgn
```

进入后运行：

```bash
python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode loop \
  --interval-sec 600
```

这个 session 只负责主运行，不做开发。

---

## 2. Dashboard 网站会话：`sikk-dashboard`

```bash
tmux new -s sikk-dashboard -c /root/sikk-gmgn
```

先生成网站：

```bash
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site
```

再启动本地服务：

```bash
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site
```

然后浏览器访问：

```text
http://你的VPS_IP:8080
```

更安全方式是 SSH 隧道：

```bash
ssh -L 8080:127.0.0.1:8080 root@你的VPS_IP
```

本地浏览器打开：

```text
http://127.0.0.1:8080
```

---

## 3. Hermes 开发会话：`sikk-builder`

```bash
tmux new -s sikk-builder -c /root/sikk-gmgn
```

这个会话专门给 Hermes / OpenClaw / Codex 改代码。

进入后可以用：

```text
/status
/goal
/branch
/kanban
/codebase_inspection
/codex
/claude_design
/dogfood
```

规则：

```text
sikk-builder 只能开发，不跑主 loop。
```

---

## 4. 测试验证会话：`sikk-verifier`

```bash
tmux new -s sikk-verifier -c /root/sikk-gmgn
```

专门跑：

```bash
python3 -m py_compile \
  sikk_live_run.py \
  sikk_dashboard_site_builder.py \
  sikk_paper_live_runner.py \
  sikk_live_orchestrator.py
```

以及：

```bash
python3 -m pytest tests/test_sikk_live_run.py tests/test_sikk_runtime_v02.py -q
```

安全检查：

```bash
grep -R "gmgn-cli swap\|gmgn-cli multi-swap\|order strategy create\|onchainos swap execute\|swap execute" \
  sikk_*.py run_sikk_gmgn_pipeline.py tests/*.py | cat
```

---

## 5. 日志观察会话：`sikk-logs`

```bash
tmux new -s sikk-logs -c /root/sikk-gmgn
```

常用查看：

```bash
sed -n '1,220p' data/gmgn_candidates_live_run/live_board.md
```

```bash
tail -n 80 data/gmgn_candidates_live_run/events/live_events.jsonl
```

```bash
ls -lh data/gmgn_candidates_live_run/paper_live/daily_reports/
```

```bash
sed -n '1,200p' data/gmgn_candidates_live_run/state_machine/state_summary.md
```

这个 session 不写代码，只看状态。

---

# 五、推荐一键创建所有 tmux 会话

你可以创建脚本：

```bash
nano /root/sikk-gmgn/start_sikk_tmux.sh
```

内容：

```bash
#!/usr/bin/env bash
set -e

PROJECT_DIR="/root/sikk-gmgn"

create_session() {
  local name="$1"
  local cmd="$2"

  if tmux has-session -t "$name" 2>/dev/null; then
    echo "[exists] $name"
  else
    tmux new-session -d -s "$name" -c "$PROJECT_DIR" "$cmd"
    echo "[created] $name"
  fi
}

create_session "sikk-live" "bash"
create_session "sikk-dashboard" "bash"
create_session "sikk-builder" "bash"
create_session "sikk-verifier" "bash"
create_session "sikk-logs" "bash"

tmux ls
```

保存后：

```bash
chmod +x /root/sikk-gmgn/start_sikk_tmux.sh
```

运行：

```bash
cd /root/sikk-gmgn
./start_sikk_tmux.sh
```

---

# 六、专业化命名规则

不要随便叫 session。

建议统一：

```text
sikk-live
sikk-dashboard
sikk-builder
sikk-verifier
sikk-logs
sikk-telegram
sikk-research
```

如果你开多个实验分支：

```text
sikk-exp-dashboard-v1
sikk-exp-wallet-missing-fix
sikk-exp-paper-report
```

命名规则：

```text
项目-用途-任务
```

这样 `/agents`、tmux、日志都不会混乱。

---

# 七、tmux + Hermes 的正确组合

你的 Hermes 不要直接裸跑长任务。  
应该放进对应 tmux session。

## 开发任务

进入：

```bash
tmux attach -t sikk-builder
```

然后在 Hermes 里：

```text
/branch

创建 SIKK Dashboard Site 分支。
只做本地静态可视化网站，不改交易逻辑。
```

---

## 后台任务

在 Hermes 中用：

```text
/background
```

但外层也有 tmux。  
两层关系是：

```text
tmux：保护整个 Hermes 进程
/background：保护 Hermes 内部子任务
```

也就是：

```text
tmux session
  └── Hermes
        └── background task / delegate_task
```

---

## 查看任务

外层看：

```bash
tmux ls
```

Hermes 内部看：

```text
/agents
```

两者不是一回事：

```text
tmux ls = 看终端进程
/agents = 看 Hermes 内部 Agent 任务
```

---

# 八、tmux 不能解决什么

这里要清楚：

```text
tmux 隔离的是终端进程，不隔离文件系统。
```

也就是说：

```text
sikk-builder 和 sikk-live 如果同时改 /root/sikk-gmgn 同一个文件，仍然会冲突。
```

所以你还需要规则：

```text
1. sikk-live 只运行，不改代码
2. sikk-builder 才能改代码
3. sikk-verifier 只测试，不改业务逻辑
4. 修改前先 git status
5. 修改后跑测试
6. 改坏用 /rollback 或 git restore
```

---

# 九、如果要更专业：配合 git worktree

当你真的要多个 Agent 同时改代码，单靠 tmux 不够。  
需要：

```text
tmux + git worktree
```

例如：

```bash
cd /root/sikk-gmgn
git worktree add /root/sikk-gmgn-dashboard dashboard-site
git worktree add /root/sikk-gmgn-walletfix wallet-missing-fix
```

然后：

```bash
tmux new -s sikk-dashboard-dev -c /root/sikk-gmgn-dashboard
tmux new -s sikk-walletfix-dev -c /root/sikk-gmgn-walletfix
```

这样两个 Agent 不会改同一份工作目录。

当前阶段你可以先不用 worktree，但以后多 Agent 并行改代码时必须考虑。

---

# 十、SIKK 推荐工作流

## 每天启动

```bash
cd /root/sikk-gmgn
./start_sikk_tmux.sh
```

查看：

```bash
tmux ls
```

---

## 跑主系统

```bash
tmux attach -t sikk-live
```

运行：

```bash
python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode loop \
  --interval-sec 600
```

Detach：

```text
Ctrl+b，然后 d
```

---

## 看面板

```bash
tmux attach -t sikk-dashboard
```

运行：

```bash
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site
```

---

## 开发新功能

```bash
tmux attach -t sikk-builder
```

让 Hermes 执行：

```text
/branch
/title SIKK Dashboard Site Builder
/codebase_inspection
/codex
/claude_design
/dogfood
```

---

## 验证

```bash
tmux attach -t sikk-verifier
```

运行：

```bash
python3 -m py_compile sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120
```

---

# 十一、tmux 状态检查命令

查看所有 session：

```bash
tmux ls
```

查看某个 session 当前在干什么：

```bash
tmux capture-pane -t sikk-live -p | tail -n 40
```

杀掉失控 session：

```bash
tmux kill-session -t sikk-builder
```

重建：

```bash
tmux new -s sikk-builder -c /root/sikk-gmgn
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

# 十三、你现在最该执行的设置

现在先做 3 件事：

## 1. 创建 tmux 会话

```bash
cd /root/sikk-gmgn
./start_sikk_tmux.sh
```

没有脚本就先手动：

```bash
tmux new -s sikk-live -c /root/sikk-gmgn
```

---

## 2. 固定主运行会话

`sikk-live` 只跑：

```bash
python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode loop \
  --interval-sec 600
```

---

## 3. 固定开发会话

`sikk-builder` 只给 Hermes 做：

```text
SIKK Dashboard Site
wallet_structure_missing 修复
paper report 修复
```

不要在 `sikk-live` 里让 AI 改代码。

---

# 最终结论

这段话对你最重要的启发是：

> **tmux 是 SIKK 的外层隔离器，Hermes 是内层调度器。**

你的专业结构应该是：

```text
sikk-live       → 主系统运行
sikk-dashboard  → 网站控制台
sikk-builder    → AI 开发
sikk-verifier   → 测试验证
sikk-logs       → 运行观察
```

这样你才能做到：

```text
运行不中断
开发不干扰
面板独立看
测试独立跑
Agent 上下文不串
文件改坏能回滚
```

这才是 Hermes + tmux 在 SIKK 项目里的专业用法。


---

## 片段 18 / stream_idx=3037 / len=405


所以这里给出所有运行 Hermes Agent 或任何本地 Agent 的用户都应该知道的答案：tmux 是隔离层。它是防止 Agent 上下文相互干扰的最便宜、最简单、最可靠的方法。我并行运行很多 Hermes 会话。每个项目一个会话，每个活跃模型一个会话，有时两者兼有。每个会话都有自己的工作目录、内存上下文和对话线程。工作会话、个人会话和客户端会话互不干扰。在我的主服务器上，通常每天都会运行 6 到 10 个 Hermes 会话。一个会话用于编码项目，另一个会话用于研究，还有一个会话用于撰写内容，第四个会话用于 Telegram 网关路由请求，第五个会话用于模型基准测试。切换会话零开销，上下文干扰风险为零。你不需要 Docker、第二台机器或复杂的流程工具。tmux 加上清晰的命名约定，再加上每个会话一个 Hermes 会话，就构成了完整的设置。这些工具一直都在那里，只是大多数人没有将它们连接起


---

## 片段 19 / stream_idx=3298 / len=9768


我打开了你给的 X 链接，但页面没有返回可读取正文，所以不能逐字确认原文内容。下面基于你前面贴出的“Harness / Hermes 多 Agent”内容、截图里的 Hermes 命令，以及 Anthropic 关于 long-running agent harness 的官方工程思路来深化。Anthropic 的核心观点是：长任务不能只靠一个长上下文硬撑，需要用 harness 管理上下文、任务拆分、执行与评估；其后续文章也强调多 Agent harness 对长时间应用开发和前端设计质量有明显作用。citeturn108638view0turn142476search0turn142476search1

# 你的 Hermes 专业化目标

你现在不能把 Hermes 当“聊天机器人”用。  
要把它变成：

```text
SIKK 项目调度器
+ 子任务执行器
+ 代码审计器
+ 面板构建器
+ 测试验证器
+ 经验沉淀器
```

核心不是让 Hermes 一次干很多，而是让它：

```text
拆任务
开分支
派子 Agent
后台执行
检查结果
失败重规划
写入经验库
保留回滚点
```

---

# 一、Hermes 在你项目里的 5 层用法

## 第 1 层：会话控制层

目的：防止上下文爆炸、任务混乱。

常用命令：

```text
/status
/usage
/new
/branch
/title
/compress
/resume
/rollback
```

你的使用规则：

| 场景 | 命令 |
|---|---|
| 开始新任务 | `/new` |
| 做一个实验方向 | `/branch` |
| 当前会话太长 | `/compress` |
| 恢复之前命名会话 | `/resume` |
| 改坏文件 | `/rollback` |
| 查看 token / 会话状态 | `/status`、`/usage` |

对 SIKK 来说，最重要的是：

```text
/branch
/rollback
/status
/usage
```

因为你现在系统已经复杂，不能在主线里乱试。

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

## 第 3 层：任务板层

目的：把大任务拆成可执行任务。

用：

```text
/kanban
```

针对你当前的可视化网站，任务板应该是：

```text
/kanban

创建 SIKK Dashboard Site 任务板：

任务 1：项目侦察
- 检查已有 live_board.md、live_dashboard.html、token_status.json、paper_live 输出、events。
- 输出 SIKK_DASHBOARD_READINESS_REPORT.md。
- 不修改代码。

任务 2：数据层
- 创建 sikk_dashboard_site_builder.py。
- 读取现有输出。
- 生成 site/dashboard_data.json。

任务 3：静态 UI
- 创建 site/index.html、app.js、style.css。
- 显示 KPI、漏斗、重点机会、Token 表格、筛选、纸面仓位、最新事件。

任务 4：验证
- py_compile。
- 运行 builder。
- 检查 dashboard_data.json。
- 启动 http.server 验证页面。

任务 5：审计
- 检查是否新增真实交易。
- 检查是否删除已有模块。
- 检查是否引入后端 / 数据库。
- 检查是否只读现有输出。
```

这样 Hermes 不会“一口气重构项目”。

---

## 第 4 层：子 Agent 执行层

目的：用不同 Agent 做不同任务，减少上下文污染。

对应命令：

```text
/background
/agents
/stop
/steer
/queue
/codex
/claude_code
/claude_design
/dogfood
/codebase_inspection
```

你的 Agent 分工应该是：

| Agent | Hermes 命令 | 职责 |
|---|---|---|
| 侦察 Agent | `/codebase_inspection` | 只检查文件，不改代码 |
| 数据 Builder | `/codex` 或 `/claude_code` | 写 `sikk_dashboard_site_builder.py` |
| UI Builder | `/claude_design` | 写 `index.html/app.js/style.css` |
| 验证 Agent | `/dogfood` | 测试网站是否可用 |
| 审计 Agent | `/codebase_inspection` 或普通任务 | 查边界、查真实交易风险 |

---

## 第 5 层：经验沉淀层

目的：让 Hermes 不重复犯错。

你必须建立这些文件：

```text
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
SIKK_LESSONS_LEARNED.md
SIKK_CHANGELOG.md
SIKK_DASHBOARD_READINESS_REPORT.md
SIKK_VERIFY_REPORT.md
SIKK_AUDIT_REPORT.md
```

其中最重要的是：

```text
SIKK_LESSONS_LEARNED.md
```

内容示例：

```markdown
# SIKK Lessons Learned

## 001：不要删除已实现模块
Runtime、dashboard、notifier、confirmation ticket、paper runner 已经实现，后续只允许配置关闭，不允许删除。

## 002：不要把静态网站做成复杂后端
当前阶段只需要读取现有 JSON/CSV，生成本地静态 HTML。

## 003：钱包结构缺失必须可解释
wallet_structure 未接入不能静默跳过，必须写 MISSING 和具体原因。

## 004：paper closed 输出必须 CSV/JSON 一致
日报读取 CSV，runner 只输出 JSON 会导致统计断链。

## 005：面板必须有 Reason 和 Next Action
只显示 WATCHING / BLOCKED 没有决策价值。
```

每次踩坑，都让 Hermes 更新这个文件。

---

# 二、针对 SIKK 可视化网站的 Hermes 实战流程

你现在应该按 5 轮执行。

---

## Round 1：创建项目控制文件

发给 Hermes：

```text
/branch

创建 SIKK Dashboard Site 分支。

第一步只创建项目控制文件，不写业务代码。

请在 /root/sikk-gmgn 创建或更新：
- SIKK_PROJECT_STATE.md
- SIKK_NEXT_TASK.md
- SIKK_LESSONS_LEARNED.md
- SIKK_CHANGELOG.md

当前阶段：
Phase B-0.5：连续运行 + 专业可视化面板优化阶段。

当前任务：
创建本地静态可视化网站控制台。

边界：
- 不删除已有模块
- 不新增后端
- 不使用数据库
- 不接真实 swap
- 不改 paper runner 交易逻辑
- 不改自动实盘
- 只读取 data/gmgn_candidates_live_run 下已有输出
```

---

## Round 2：侦察项目状态

发给 Hermes：

```text
/codebase_inspection

检查 /root/sikk-gmgn 中与 SIKK 可视化网站相关的文件和数据。

检查范围：
1. sikk_live_run.py
2. sikk_live_orchestrator.py
3. live_board.md
4. live_dashboard.html
5. data/gmgn_candidates_live_run/live_state.json
6. data/gmgn_candidates_live_run/tokens/*/token_status.json
7. data/gmgn_candidates_live_run/paper_live/strategy_metrics.json
8. data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
9. data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
10. data/gmgn_candidates_live_run/events/live_events.jsonl
11. data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json

输出：
SIKK_DASHBOARD_READINESS_REPORT.md

要求：
- 只检查，不修改。
- 列出已有文件。
- 列出缺失文件。
- 列出 dashboard_data.json 需要读取的字段。
- 列出影响面板显示的风险。
```

这一轮用来避免 AI 盲写。

---

## Round 3：只做数据层

发给 Hermes：

```text
/codex

任务：创建 SIKK Dashboard 数据构建器。

新增文件：
/root/sikk-gmgn/sikk_dashboard_site_builder.py

只做数据层，不做 UI。

输入目录：
data/gmgn_candidates_live_run

读取：
- live_state.json
- tokens/*/token_status.json
- paper_live/strategy_metrics.json
- paper_live/paper_positions_open.json
- paper_live/paper_positions_closed.json
- events/live_events.jsonl
- wallet_structure/*/wallet_structure_decision.json

输出：
data/gmgn_candidates_live_run/site/dashboard_data.json

dashboard_data.json 必须包含：
- kpi
- funnel
- tokens
- opportunities
- wallet_structure_summary
- wallet_missing_reasons
- entry_block_reasons
- paper_positions
- events

边界：
- 不删除已有模块
- 不改 paper runner
- 不接真实 swap
- 不新增后端
- 不使用数据库
- 只读现有输出文件

验收命令：
cd /root/sikk-gmgn
python3 -m py_compile sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120

完成后更新：
SIKK_CHANGELOG.md
SIKK_BUILD_REPORT.md
```

这一轮只让它生成 `dashboard_data.json`。  
不让它碰页面，防止任务过大。

---

## Round 4：做静态页面

发给 Hermes：

```text
/claude_design

任务：基于 dashboard_data.json 创建 SIKK 静态可视化网站。

新增/修改：
data/gmgn_candidates_live_run/site/index.html
data/gmgn_candidates_live_run/site/app.js
data/gmgn_candidates_live_run/site/style.css

页面结构：
1. 顶部 KPI 卡片
2. Pipeline 漏斗
3. 重点机会区
4. Token 总表
5. 搜索与筛选
6. 未入场原因统计
7. 当前纸面仓位
8. 最新事件

Token 表字段：
- token_symbol
- current_state
- priority_level
- signal_gate
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- quote_gate
- security_gate
- paper_status
- paper_pnl_pct
- main_reason
- next_action

筛选：
- token 搜索
- current_state 筛选
- wallet_structure_status 筛选
- paper_status 筛选
- reason 搜索

视觉：
- 深色专业风格
- PAPER_OPEN / PAPER_READY：绿色
- WALLET_SUPPORT：蓝绿色
- WATCHING / PAUSE：黄色
- BLOCKED / WALLET_BLOCK：红色
- MISSING：灰色
- ERROR：红色或紫色

禁止：
- 不使用 React
- 不新增后端
- 不使用数据库
- 不加入交易按钮
- 不接真实 swap
```

---

## Round 5：测试和审计

先测试：

```text
/dogfood

测试 SIKK 静态网站控制台。

执行：
cd /root/sikk-gmgn
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

检查：
1. index.html 是否加载
2. dashboard_data.json 是否加载
3. KPI 是否显示
4. Token 表格是否显示
5. 搜索是否有效
6. current_state 筛选是否有效
7. wallet_structure_status 筛选是否有效
8. paper_status 筛选是否有效
9. paper 仓位是否显示
10. entry block reasons 是否显示
11. 页面没有交易按钮
12. 页面没有真实 swap 调用

输出：
SIKK_DASHBOARD_DOGFOOD_REPORT.md
```

再审计：

```text
/codebase_inspection

审计本次 SIKK 可视化网站修改。

检查：
1. 是否删除已有模块
2. 是否新增真实交易功能
3. 是否新增后端服务
4. 是否新增数据库依赖
5. 是否修改 paper runner 交易逻辑
6. 是否修改 swap / broadcast 路径
7. 是否只读取现有输出文件
8. 是否输出到 data/gmgn_candidates_live_run/site/
9. 是否保留 live_board.md 和已有 live_dashboard.html
10. 是否符合“静态观察控制台”目标

输出：
SIKK_AUDIT_REPORT.md
```

---

# 三、Hermes 命令组合：你每天该怎么用

## 开始前

```text
/status
/usage
/profile
```

看会话是否健康。

---

## 做新功能

```text
/branch
/title SIKK Dashboard Site
/kanban
```

先开分支，再拆任务。

---

## 跑长任务

```text
/background
/agents
```

后台跑，随时检查。

---

## 发现方向错了

```text
/steer
```

例如：

```text
/steer

不要新增后端，不要使用 React，不要改 paper runner。
当前任务只允许生成静态网站文件。
```

---

## Agent 失控

```text
/stop
```

---

## 文件改坏

```text
/rollback
```

---

## 任务太长

```text
/compress
```

但更推荐：

```text
/new
```

然后让它读：

```text
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
SIKK_LESSONS_LEARNED.md
```

---

# 四、你截图里这些命令的 SIKK 用法

| 命令 | SIKK 用法 |
|---|---|
| `/new` | 新开任务，不带旧上下文 |
| `/branch` | 开实验分支，比如 dashboard site |
| `/compress` | 压缩长会话 |
| `/rollback` | 改坏代码后回滚 |
| `/background` | 后台跑 builder / dogfood |
| `/agents` | 看后台任务 |
| `/stop` | 停止失控任务 |
| `/queue` | 当前任务结束后继续执行下一步 |
| `/steer` | 中途纠偏 |
| `/goal` | 设置 SIKK 长期目标 |
| `/kanban` | 做任务板 |
| `/codebase_inspection` | 侦察项目 |
| `/codex` | 具体写 Python / 修代码 |
| `/claude_design` | 做静态 HTML 页面 |
| `/dogfood` | 测试网站 |
| `/architecture_diagram` | 画 SIKK 架构图 |
| `/github_code_review` | 后续 review 改动 |
| `/reload_skills` | 新 skill 加入后刷新 |
| `/curator` | 后台维护 skills |

谨慎：

| 命令 | 原因 |
|---|---|
| `/yolo` | 会跳过危险命令审批 |
| `/approve` | 只在明确安全时批准 |
| `/gmgn_swap` | 涉及金融执行，当前阶段不用 |
| `/gmgn_cooking` | 涉及发行/执行类能力，当前阶段不用 |

---

# 五、用 Hermes 实现专业化的关键规则

你要固定 10 条规则：

```text
1. 每次只做一个任务
2. 每个任务先侦察，再开发
3. 子 Agent 只拿文件路径，不塞大段上下文
4. Builder 只改指定文件
5. Verifier 只测试，不加功能
6. Auditor 只审计，不重构
7. 每轮必须有验收命令
8. 每轮必须更新 CHANGELOG
9. 踩坑必须更新 LESSONS_LEARNED
10. 不允许自动实盘和真实 swap
```

---

# 六、你现在最应该执行的第一条 Hermes 指令

直接发这个：

```text
/branch

创建 SIKK Dashboard Site 分支。

目标：
为 /root/sikk-gmgn 创建本地静态可视化网站控制台。

边界：
- 不删除已有模块
- 不新增后端
- 不使用数据库
- 不接真实 swap
- 不改 paper runner 交易逻辑
- 只读取现有输出文件
- 输出到 data/gmgn_candidates_live_run/site/

第一步：
使用 /codebase_inspection 检查当前项目和 dashboard 所需数据是否齐全。
输出 SIKK_DASHBOARD_READINESS_REPORT.md。
不要修改任何代码。
```

然后按顺序：

```text
/codebase_inspection → /codex → /claude_design → /dogfood → /codebase_inspection 审计
```

---

# 最终结论

你现在要把 Hermes 用成：

```text
任务调度系统
```

而不是：

```text
一个会写代码的聊天窗口
```

对 SIKK 当前阶段，最专业的 Hermes 运用路线就是：

```text
/goal 固定长期目标
/branch 开 dashboard 分支
/kanban 拆任务
/codebase_inspection 侦察
/codex 做 dashboard_data.json
/claude_design 做静态 UI
/dogfood 测试网站
/rollback 保底
/steer 纠偏
/agents 监控后台任务
```

这套流程能让你把 SIKK 可视化网站做出来，同时不破坏已有运行链路。


---

## 片段 20 / stream_idx=3660 / len=10085


你现在要把 Hermes 用成：

> **项目调度系统，不是普通聊天助手。**

结合你截图里的命令，专业用法应该分 4 层：

```text
第 1 层：会话治理
第 2 层：任务调度
第 3 层：工程执行
第 4 层：复盘与长期维护
```

你的目标是：**让 Hermes 帮你把 SIKK-SOL 做成可运行、可观察、可复盘的专业系统**，而不是每次都靠一个大 Prompt 让 AI 乱改。

---

# 一、你截图里最重要的命令怎么用

## 1. 会话治理类

这些是控制上下文的：

| 命令 | 用法 |
|---|---|
| `/new` | 开新干净会话，适合新任务 |
| `/branch` | 从当前会话分叉，适合试验方案 |
| `/compress` | 压缩上下文，适合长对话快爆时 |
| `/status` | 看当前 session 状态 |
| `/usage` | 看 token 使用情况 |
| `/model` | 切换模型 |
| `/rollback` | 回滚文件检查点 |
| `/retry` | 重试上一条 |
| `/undo` | 撤销上一轮 user/assistant 交换 |

你的 SIKK 项目里，最常用：

```text
/status
/usage
/branch
/compress
/rollback
```

---

## 2. 执行治理类

这些是控制 Agent 执行的：

| 命令 | 用法 |
|---|---|
| `/background` | 后台跑一个任务 |
| `/agents` | 查看当前运行 Agent / 后台任务 |
| `/stop` | 停止所有后台进程 |
| `/queue` | 把提示排到下一轮，不打断当前任务 |
| `/steer` | 在下一次工具调用后插入指令 |
| `/approve` | 批准危险命令 |
| `/deny` | 拒绝危险命令 |
| `/yolo` | 跳过危险命令审批，不建议长期打开 |

你的系统里重点：

```text
/background
/agents
/stop
/queue
/steer
/approve
/deny
```

不要长期打开：

```text
/yolo
```

尤其你项目涉及 GMGN、swap、quote、安全扫描，长期 YOLO 很危险。

---

## 3. 项目管理类

这些适合做 Harness 工程：

| 命令 | 用法 |
|---|---|
| `/goal` | 设置长期目标 |
| `/kanban` | 多 profile 协作任务板 |
| `/curator` | 后台 skill 维护 |
| `/reload_skills` | 重新扫描 skill |
| `/profile` | 查看当前 profile / home |
| `/sethome` | 设置 home channel |
| `/resume` | 恢复命名 session |
| `/title` | 设置 session 名称 |

你的 SIKK 最应该用：

```text
/goal
/kanban
/resume
/title
/reload_skills
```

---

## 4. 工程 Skill 类

你截图里对 SIKK 有价值的：

| Skill | 用法 |
|---|---|
| `/codebase_inspection` | 检查代码结构、文件、复杂度 |
| `/codex` | 交给 Codex CLI 写代码 |
| `/claude_code` | 交给 Claude Code 写代码 |
| `/claude_design` | 设计一次性 HTML 页面 |
| `/dogfood` | 做 Web App 探索测试 |
| `/github_code_review` | Review PR / diff |
| `/github_issues` | 创建/管理 issue |
| `/architecture_diagram` | 生成架构图 |
| `/excalidraw` | 生成手绘结构图 |

跟你当前“可视化网站控制台”最相关的是：

```text
/codebase_inspection
/codex
/claude_design
/dogfood
/architecture_diagram
```

谨慎使用：

```text
/gmgn_swap
/gmgn_cooking
```

这些带 `[FINANCIAL EXECUTION]`，你当前阶段不要用于真实执行。

---

# 二、SIKK 项目的专业 Hermes 操作模式

你应该固定成这个流程：

```text
1. /status 检查当前会话
2. /goal 设置长期目标
3. /branch 开一个专门任务分支
4. /kanban 拆任务
5. /background 跑长任务
6. /agents 观察执行状态
7. /steer 纠偏
8. /rollback 回滚错误改动
9. /codex 或 /claude_code 执行具体代码
10. /dogfood 或测试命令验证网站
```

---

# 三、你的当前目标：创建 SIKK 可视化网站

当前任务不要说“做网站”，要定义成：

```text
创建 SIKK-SOL 本地静态可视化控制台。
只读取现有输出文件。
不新增后端。
不接真实交易。
不删除已有模块。
不改变 paper runner 交易逻辑。
```

目标文件：

```text
sikk_dashboard_site_builder.py

data/gmgn_candidates_live_run/site/
  index.html
  app.js
  style.css
  dashboard_data.json
```

---

# 四、推荐你在 Hermes 里这样操作

## 第 1 步：设置长期目标

在 Hermes 里发：

```text
/goal

SIKK-SOL 当前长期目标：
把现有连续运行、钱包结构、quote/security、paper runner、日报和事件日志，整合成一个本地静态可视化网站控制台。

边界：
- 不执行真实 swap
- 不接自动实盘
- 不删除已实现模块
- 不新增复杂后端
- 不使用数据库
- 当前只做可观察、可筛选、可复盘的专业面板
```

---

## 第 2 步：开专门分支

```text
/branch

创建 SIKK dashboard site 分支。
目标：只做 data/gmgn_candidates_live_run/site 静态控制台。
不要影响主运行链路。
```

---

## 第 3 步：先用 codebase_inspection 侦察

```text
/codebase_inspection

检查 /root/sikk-gmgn 项目中和 dashboard / runtime / paper / wallet_structure 相关的文件。

重点检查：
1. 是否已有 sikk_dashboard_site_builder.py
2. 是否已有 live_dashboard.html
3. live_state.json 是否存在
4. tokens/*/token_status.json 是否存在
5. paper_live/strategy_metrics.json 是否存在
6. paper_positions_open/closed json/csv 是否存在
7. events/live_events.jsonl 是否存在
8. 当前 live_board.md 的结构
9. 当前 dashboard 可用性问题

只输出检查报告，不修改文件。
```

输出文件建议：

```text
SIKK_DASHBOARD_READINESS_REPORT.md
```

---

## 第 4 步：用 kanban 拆任务

```text
/kanban

创建 SIKK Dashboard Site 任务板，拆成 4 个任务：

任务 1：Dashboard 数据层
- 创建 sikk_dashboard_site_builder.py
- 读取现有输出
- 生成 dashboard_data.json

任务 2：静态 UI
- 创建 index.html
- 创建 app.js
- 创建 style.css
- 显示 KPI、Token 表格、筛选、纸面仓位、事件

任务 3：验证
- py_compile
- 运行 builder
- 检查 dashboard_data.json 字段
- 启动 http.server

任务 4：审计
- 检查是否引入真实交易
- 检查是否删除已有模块
- 检查是否修改 paper runner 逻辑
```

---

# 五、最专业的执行方式：分 3 轮，不要一口气做完

## Round 1：只做数据层

发给 Hermes：

```text
/codex

任务：在 /root/sikk-gmgn 创建 sikk_dashboard_site_builder.py。

只做数据层，不做 UI。

输入：
data/gmgn_candidates_live_run/

读取：
- live_state.json
- tokens/*/token_status.json
- paper_live/strategy_metrics.json
- paper_live/paper_positions_open.json
- paper_live/paper_positions_closed.json
- events/live_events.jsonl
- wallet_structure/*/wallet_structure_decision.json

输出：
data/gmgn_candidates_live_run/site/dashboard_data.json

dashboard_data.json 必须包含：
- kpi
- funnel
- tokens
- opportunities
- wallet_structure_summary
- wallet_missing_reasons
- entry_block_reasons
- paper_positions
- events

边界：
- 不删除已有模块
- 不改 paper runner
- 不接真实 swap
- 不新增后端
- 不使用数据库

验收命令：
cd /root/sikk-gmgn
python3 -m py_compile sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120
```

---

## Round 2：做静态页面

```text
/claude_design

任务：基于 data/gmgn_candidates_live_run/site/dashboard_data.json 创建静态专业控制台。

新增：
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css

页面必须包含：
1. 顶部 KPI 卡片
2. Pipeline 漏斗
3. 重点机会区
4. Token 总表
5. Token 搜索
6. State 筛选
7. Wallet 筛选
8. Paper 筛选
9. 未入场原因统计
10. 当前纸面仓位
11. 最新事件

视觉：
- 深色专业风格
- PAPER_OPEN / PAPER_READY 绿色
- WALLET_SUPPORT 蓝绿色
- WATCHING / PAUSE 黄色
- BLOCKED / WALLET_BLOCK 红色
- MISSING 灰色
- ERROR 红色或紫色

禁止：
- 不使用 React
- 不新增后端
- 不新增数据库
- 不加入交易按钮
- 不接真实 swap
```

---

## Round 3：测试网站

```text
/dogfood

测试本地静态网站控制台。

执行：
cd /root/sikk-gmgn
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

检查：
1. index.html 是否加载
2. dashboard_data.json 是否加载
3. KPI 是否显示
4. Token 表格是否显示
5. 搜索是否有效
6. 状态筛选是否有效
7. 钱包筛选是否有效
8. paper 仓位是否显示
9. entry block reasons 是否显示
10. 没有交易按钮
11. 没有真实 swap 调用

输出 SIKK_DASHBOARD_DOGFOOD_REPORT.md。
```

---

# 六、Hermes 多 Agent 深水区怎么具体用到你项目

## 技巧 1：Stateless 子 Agent 并行侦察

用法：

```text
/background

使用 delegate_task 并行执行 4 个无状态子任务，skip_memory=True，skip_context_files=True。

task 1：
检查 /root/sikk-gmgn dashboard 相关文件是否存在。

task 2：
检查 data/gmgn_candidates_live_run 下 dashboard 所需数据是否齐全。

task 3：
检查 paper_live 输出文件结构。

task 4：
检查是否存在真实 swap / private key / api key / broadcast 风险。

最终汇总成 SIKK_DASHBOARD_READINESS_REPORT.md。
```

作用：

```text
避免一个 Agent 同时读全项目导致上下文爆炸。
```

---

## 技巧 2：失败后 Replan

比如 builder 运行失败，你不要直接“再试一次”。

应该发：

```text
/steer

如果 dashboard builder 失败，不要盲目重跑。
请先读取错误堆栈，判断失败属于：
1. 输入文件缺失
2. JSON 格式不一致
3. 字段名不一致
4. 输出目录不存在
5. 代码语法错误

然后只修对应问题，不要重构整个文件。
```

这就是 LLM-driven replan。

---

## 技巧 3：Subdirectory Hints

你应该在项目里放 AGENTS.md，让 Hermes 子 Agent 进入目录后自动读规则。

### `/root/sikk-gmgn/AGENTS.md`

```markdown
# SIKK-GMGN Project Rules

本项目是 SIKK-SOL 结构智能纸面验证系统。

当前阶段：
Phase B-0.5：连续运行 + 专业可视化面板优化阶段。

核心边界：
- 不执行真实 swap
- 不读取私钥
- 不写入私钥
- 不自动 broadcast
- 不删除已有模块
- 不新增复杂后端
- 不新增数据库
- 不为了复杂而升级
- 所有输出统一在 data/gmgn_candidates_live_run 下

主入口：
python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode once

当前可视化目标：
创建本地静态网站控制台：
data/gmgn_candidates_live_run/site/index.html
```

### `/root/sikk-gmgn/data/gmgn_candidates_live_run/site/AGENTS.md`

```markdown
# SIKK Dashboard Site Rules

本目录只放静态可视化网站文件。

允许文件：
- index.html
- app.js
- style.css
- dashboard_data.json

规则：
- 只读取 dashboard_data.json
- 不调用交易接口
- 不写入交易数据
- 不需要后端
- 不使用数据库
- 不使用大型前端框架
- 不创建登录系统
- 页面只用于观察、筛选、复盘
```

---

# 七、Hermes 命令组合：日常专业工作流

## 1. 开始任务前

```text
/status
/usage
/profile
```

目的：

```text
确认当前会话是否干净，token 是否够，profile 是否对。
```

---

## 2. 新任务开分支

```text
/branch
/title SIKK Dashboard Site Builder
```

目的：

```text
避免污染主线。
```

---

## 3. 长任务后台跑

```text
/background

执行 SIKK dashboard readiness inspection。
```

然后：

```text
/agents
```

查看运行中任务。

---

## 4. 出问题立刻停

```text
/stop
```

适合：

```text
Agent 进入循环
开始乱改文件
跑危险命令
上下文明显失控
```

---

## 5. 文件改坏了回滚

```text
/rollback
```

适合：

```text
恢复文件检查点
撤销不合格改动
```

---

## 6. 长上下文压缩

```text
/compress
```

适合：

```text
讨论太长，但还想保留当前会话
```

但真正专业做法是：

```text
/new
```

然后让 AI 读 `SIKK_PROJECT_STATE.md`。

---

# 八、你当前最实用的 Hermes 命令优先级

## P0：每天都会用

```text
/status
/usage
/background
/agents
/stop
/rollback
/branch
```

## P1：工程任务用

```text
/kanban
/codex
/claude_code
/claude_design
/codebase_inspection
/dogfood
```

## P2：维护用

```text
/compress
/resume
/reload_skills
/curator
```

## 谨慎用

```text
/yolo
/approve
/gmgn_swap
/gmgn_cooking
```

---

# 九、你现在可以直接执行的 Hermes 任务模板

复制给 Hermes：

```text
/branch

创建 SIKK Dashboard Site 分支。目标是为 /root/sikk-gmgn 创建本地静态可视化网站控制台。

边界：
- 不删除已有模块
- 不新增后端
- 不使用数据库
- 不接真实 swap
- 不改 paper runner 交易逻辑
- 只读取现有输出文件
- 输出到 data/gmgn_candidates_live_run/site/

请先用 codebase_inspection 检查当前项目，输出 SIKK_DASHBOARD_READINESS_REPORT.md。
不要修改任何代码。
```

然后第二步：

```text
/codex

根据 SIKK_DASHBOARD_READINESS_REPORT.md，实现第一阶段：
创建 sikk_dashboard_site_builder.py，只生成 dashboard_data.json，不做 UI。

验收：
python3 -m py_compile sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120
```

第三步：

```text
/claude_design

基于 dashboard_data.json 创建静态页面：
index.html
app.js
style.css

页面必须包含 KPI、漏斗、重点机会、Token 表、筛选、未入场原因、纸面仓位、最新事件。
```

第四步：

```text
/dogfood

测试 data/gmgn_candidates_live_run/site/index.html。
确认页面可打开，筛选可用，没有交易按钮，没有真实 swap 调用。
```

---

# 十、最终专业化标准

你用 Hermes 做 SIKK，不是看它能不能“写很多代码”，而是看它能不能做到：

```text
1. 每次只做一个明确任务
2. 每次有边界
3. 每次有验收
4. 每次有回滚
5. 每次有审计
6. 不删除已有模块
7. 不乱加功能
8. 不接真实交易
9. 能把失败原因写清楚
10. 能把成果接入现有运行链路
```

---

# 结论

你现在应该这样用 Hermes：

```text
Hermes = 调度系统
Codex / Claude Code = 子执行单元
AGENTS.md = 局部规则注入
/kanban = 任务板
/background + /agents = 长任务管理
/rollback = 安全回滚
/dogfood = 面板验收
```

对当前 SIKK 项目，最专业的路径就是：

```text
侦察项目
→ 生成 dashboard_data.json
→ 生成静态网站
→ 测试网站
→ 审计边界
→ 接入 sikk_live_run.py
```

不要让一个 Agent 从头到尾自由发挥。  
用 Hermes 把 AI 当“函数”和“工人”，你做调度。


---

## 片段 21 / stream_idx=3862 / len=7489


这篇内容对你现在的 SIKK 项目非常关键。它说明你在 Hermes / OpenClaw 里不要再用：

```text
一个大 Prompt
一个 AI 从头干到尾
一个上下文里塞所有系统设计
```

而应该升级成：

```text
主 Agent 调度
子 Agent 独立执行
文件传递上下文
失败后重规划
目录级规则动态注入
```

这正好适合你现在要做的 **SIKK 可视化网站控制台**。

---

# 一、这套 Hermes 思路怎么用于你的 SIKK 项目

你的项目现在已经不是简单脚本，而是多个模块：

```text
候选发现
K线信号
钱包结构门禁
quote/security
paper runner
日报
live board
dashboard site
Telegram 广播
测试与安全边界
```

如果让一个 AI 一次性改完，必然容易乱：

```text
上下文爆
忘记边界
重复造轮子
删除已实现模块
乱改 paper runner
把静态网站做成复杂后端
```

所以你应该把 Hermes 用成：

```text
Coordinator 主控
  ↓
Planner 规划
  ↓
Builder 开发
  ↓
Verifier 测试
  ↓
Auditor 审计
```

而不是让一个 Agent 全干。

---

# 二、SIKK-Hermes 多 Agent 分工

## 1. Coordinator：主调度 Agent

职责：

```text
只调度
不写代码
不改文件
不做实现
只拆任务、派发、汇总结果
```

它只看：

```text
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
SIKK_LESSONS_LEARNED.md
SIKK_CHANGELOG.md
```

---

## 2. Planner：规划 Agent

职责：

```text
明确这次要改什么
明确新增哪些文件
明确禁止碰哪些文件
明确验收命令
```

当前任务就是：

```text
为 SIKK 创建本地静态可视化网站控制台
```

---

## 3. Builder：开发 Agent

职责：

```text
只写代码
只改指定文件
不自作主张扩展
不改真实交易逻辑
```

当前允许改：

```text
sikk_dashboard_site_builder.py
data/gmgn_candidates_live_run/site/index.html
data/gmgn_candidates_live_run/site/app.js
data/gmgn_candidates_live_run/site/style.css
```

---

## 4. Verifier：测试 Agent

职责：

```text
跑命令
检查输出
检查 JSON 结构
检查 HTML 是否生成
检查不报错
```

---

## 5. Auditor：审计 Agent

职责：

```text
检查是否违反边界
检查是否引入真实交易
检查是否删除已有模块
检查是否过度设计
```

---

# 三、在 Hermes 里最适合你的调用方式

你现在可以直接使用 Hermes 的 `delegate_task` 思路，把任务拆成并发子任务。

## 第一轮：并行侦察当前项目状态

可以给 Hermes 发：

```text
使用 delegate_task 并行执行以下 4 个任务。所有子任务都使用 skip_memory=True 和 skip_context_files=True，toolsets 使用 terminal,file。

task 1：
检查 /root/sikk-gmgn 当前与 dashboard/site 相关的文件：
- live_board.md
- live_dashboard.html
- sikk_dashboard_builder.py
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/
输出已有文件、缺失文件、不要修改任何文件。

task 2：
检查 data/gmgn_candidates_live_run 下现有数据源：
- live_state.json
- tokens/*/token_status.json
- paper_live/strategy_metrics.json
- paper_live/paper_positions_open.json
- paper_live/paper_positions_closed.json
- events/live_events.jsonl
输出这些文件是否存在、字段结构示例、缺失项。

task 3：
检查 paper_live 输出是否一致：
- paper_positions_open.json
- paper_positions_closed.json
- paper_positions_open.csv
- paper_positions_closed.csv
- strategy_metrics.json
- daily_reports/
输出缺失项和可能影响 dashboard 的问题。

task 4：
检查安全边界：
搜索是否存在真实 swap、private key、api key、broadcast 相关危险路径。
只报告，不修改。

最终由父 Agent 汇总成 SIKK_DASHBOARD_READINESS_REPORT.md。
```

这一轮的目标不是写代码，而是先看清楚项目。

---

# 四、第二轮：创建网站数据层，不做 UI

你应该先让 Hermes 只做 `dashboard_data.json`，不要一上来做页面。

发给 Hermes：

```text
使用 delegate_task 创建一个 Builder 子任务。

任务：
在 /root/sikk-gmgn 创建 sikk_dashboard_site_builder.py。

边界：
1. 不删除任何已有文件。
2. 不改真实交易逻辑。
3. 不改 paper runner。
4. 不接 swap。
5. 不新增后端。
6. 不使用数据库。
7. 只读取现有输出，生成 dashboard_data.json。

输入目录：
data/gmgn_candidates_live_run

读取：
- live_state.json
- tokens/*/token_status.json
- paper_live/strategy_metrics.json
- paper_live/paper_positions_open.json
- paper_live/paper_positions_closed.json
- events/live_events.jsonl
- wallet_structure/*/wallet_structure_decision.json

输出：
data/gmgn_candidates_live_run/site/dashboard_data.json

dashboard_data.json 必须包含：
- kpi
- funnel
- tokens
- opportunities
- wallet_structure_summary
- wallet_missing_reasons
- entry_block_reasons
- paper_positions
- events

验收命令：
cd /root/sikk-gmgn
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 80

完成后写 SIKK_BUILD_REPORT.md。
```

---

# 五、第三轮：创建静态网站 UI

等 `dashboard_data.json` 成功，再做页面。

```text
使用 delegate_task 创建 Builder 子任务。

任务：
基于 data/gmgn_candidates_live_run/site/dashboard_data.json 创建静态网站控制台。

新增/修改：
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css

要求：
1. 纯静态页面。
2. 不使用 React。
3. 不新增后端。
4. 不接真实交易。
5. 页面只做观察、筛选、复盘。

页面包含：
1. 顶部 KPI 卡片
2. Pipeline 漏斗
3. 重点机会区
4. Token 总表
5. 搜索与筛选
6. 未入场原因统计
7. 当前纸面仓位
8. 最新事件

视觉：
- 深色专业风格
- PAPER_OPEN / PAPER_READY 绿色
- WALLET_SUPPORT 蓝绿色
- WATCHING / PAUSE 黄色
- BLOCKED / WALLET_BLOCK 红色
- MISSING 灰色
- ERROR 紫色或红色

验收：
cd /root/sikk-gmgn
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

确认 index.html、app.js、style.css、dashboard_data.json 都存在。
```

---

# 六、第四轮：Verifier 测试

```text
使用 delegate_task 创建 Verifier 子任务。

任务：
验证 SIKK 静态网站控制台是否可运行。

执行：
cd /root/sikk-gmgn

python3 -m py_compile sikk_dashboard_site_builder.py

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

ls -lh data/gmgn_candidates_live_run/site

python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 120

检查：
1. dashboard_data.json 是否存在
2. index.html 是否存在
3. app.js 是否存在
4. style.css 是否存在
5. dashboard_data.json 是否包含 kpi、tokens、opportunities、entry_block_reasons、paper_positions、events
6. 不允许发现真实 swap 路径
7. 不允许修改 paper runner 逻辑

输出 SIKK_VERIFY_REPORT.md。
```

---

# 七、第五轮：Auditor 审计

```text
使用 delegate_task 创建 Auditor 子任务。

任务：
审计本次 SIKK 可视化网站改造是否符合边界。

检查：
1. 是否删除已有模块
2. 是否新增真实交易功能
3. 是否新增后端服务
4. 是否新增数据库依赖
5. 是否修改 paper runner 的交易逻辑
6. 是否修改真实 swap / broadcast 路径
7. 是否只读取现有输出文件
8. 是否输出到 data/gmgn_candidates_live_run/site/
9. 是否保留 live_board.md 和 live_dashboard.html
10. 是否符合“只做静态观察控制台”的目标

输出 SIKK_AUDIT_REPORT.md。
```

---

# 八、Hermes 的 `Subdirectory Hints` 可以怎么用

你可以在项目目录里放 `AGENTS.md`，让子 Agent 进入对应目录后自动读取局部规则。

建议创建：

```text
/root/sikk-gmgn/AGENTS.md
/root/sikk-gmgn/data/gmgn_candidates_live_run/site/AGENTS.md
```

---

## `/root/sikk-gmgn/AGENTS.md`

内容：

```markdown
# SIKK-GMGN Project Rules

本项目是 SIKK-SOL 结构智能纸面验证系统。

当前阶段：
Phase B-0.5：连续运行 + 专业可视化面板优化阶段。

核心边界：
- 不执行真实 swap
- 不读取私钥
- 不写入私钥
- 不自动 broadcast
- 不删除已有模块
- 不新增复杂后端
- 不新增数据库
- 不为了复杂而升级
- 所有输出统一在 data/gmgn_candidates_live_run 下

主入口：
python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode once

当前可视化目标：
创建本地静态网站控制台：
data/gmgn_candidates_live_run/site/index.html

禁止：
- 改真实交易逻辑
- 新增交易按钮
- 新增自动实盘
- 删除 Runtime / dashboard / notifier / paper runner 已有模块
```

---

## `/root/sikk-gmgn/data/gmgn_candidates_live_run/site/AGENTS.md`

内容：

```markdown
# SIKK Dashboard Site Rules

本目录只放静态可视化网站文件。

允许文件：
- index.html
- app.js
- style.css
- dashboard_data.json

规则：
- 只读取 dashboard_data.json
- 不调用交易接口
- 不写入交易数据
- 不需要后端
- 不使用数据库
- 不使用大型前端框架
- 不创建登录系统
- 页面只用于观察、筛选、复盘

页面必须包含：
- KPI 卡片
- Pipeline 漏斗
- 重点机会
- Token 总表
- 搜索和筛选
- 未入场原因
- 纸面仓位
- 最新事件
```

---

# 九、Hermes 万能调度提示词：适配 SIKK

你可以保存成一个固定模板：

```text
你是 SIKK-SOL 项目的 Coordinator。

本轮任务必须遵守 Harness 工程方式：
1. 主 Agent 只调度，不写代码。
2. 子 Agent 使用 delegate_task。
3. 每个子 Agent 是一次性无状态执行单元。
4. 子 Agent 之间只通过文件路径交流，不传大段代码。
5. 每轮任务必须有验收命令。
6. 每次失败必须分析 status / exit_reason / tool_trace 后再决定是否重试。
7. 不允许无限循环。
8. 不允许删除已有模块。
9. 不允许新增真实 swap。
10. 不允许为了复杂而升级。

当前项目：
/root/sikk-gmgn

当前任务：
{{这里填具体任务}}

请先把任务拆成：
- Planner
- Builder
- Verifier
- Auditor

然后用 delegate_task 派发。
最终汇总：
- 修改文件
- 验收命令
- 验收结果
- 风险点
- 下一步
```

---

# 十、当前你最应该在 Hermes 执行的命令思路

不是直接让 Hermes “做网站”，而是这样：

```text
第一轮：并行读取项目状态
第二轮：生成 dashboard_data.json
第三轮：生成静态页面
第四轮：测试
第五轮：审计
```

这就是你要的 Harness 工程。

---

# 最短结论

这篇 Hermes 多 Agent 内容，对你的 SIKK 项目的用法是：

```text
不要让一个 AI 长上下文硬做完网站。
用 Hermes delegate_task 把它拆成：
侦察 → 数据层 → UI 层 → 测试 → 审计。
```

现在最合适的第一步是：

```text
先用 Hermes 并行检查当前 SIKK 项目输出文件是否齐全。
再做 dashboard_data.json。
最后才做静态网站 UI。
```

这样才不会乱改、不会爆上下文、不会把系统带偏。


---

## 片段 22 / stream_idx=3936 / len=2070


Hermes 多 Agent 深水区：三个高级实战技巧   90% 的人用 Hermes，还停留在助手阶段：把所有需求塞进一个 Prompt，然后看着它串行执行。  这种用法在多 Agent 并发场景下有三个隐性代价：        •Token 浪费：子 Agent 继承冗余历史信息。        •指令稀释：长上下文中关键指令权重衰减。        •控制循环失控：缺乏显式执行预算，容易进入低效循环。  今天直接进深水区，教你用 Hermes 三个核心机制，把单体 Agent 升级为工程级调度系统。  技巧 1：用 Stateless Ephemeral Unit 实现真并行  每次调用 delegate_task，Hermes 都会实例化一个新的 AIAgent。通过 skip_memory=True 和 skip_context_files=True，子 Agent 拥有完全独立的上下文，互不干扰。本质：每个子 Agent = 一次性无状态执行单元。  实测命令（并行读取本地日志并汇总，可以根据自己需要更改）：  hermes chat -q "使用 delegate_task 工具并行执行以下 3 个任务（toolsets 均为 terminal,file）：  task 1: 尝试读取 /var/log/syslog（若无权限或不存在则跳过并说明原因）  task 2: 读取 /var/log/auth.log 的最后 10 行并总结  task 3: 读取 /var/log/dpkg.log 的最后 10 行并总结  最终汇总为一份系统运行状态报告，包含每个任务的执行耗时" --toolsets delegation,terminal,file --yolo  技巧 2：触发 LLM-Driven Replan 处理故障  Hermes 的故障处理在两个不同层级运作：        •Layer 1（Infra 层，自动）：在 LLM API 调用层处理 HTTP 503/429/timeout，自动重试，对上层完全透明。        •Layer 2（编排层，LLM 驱动）：子 Agent 失败时，返回包含 status、exit_reason、tool_trace 的结构体。  高级玩法：利用 Layer 2 返回的 status 和 tool_trace，引导父 Agent 自主判断是否调整策略，而不是盲目重跑。  实测命令：  hermes chat -q "使用 delegate_task 执行：读取目录 /tmp/non_existent_path 下的文件。  收到结果后：  - 如果 status 表示失败（如 failed 或 error），分析失败原因  - 重新发起 delegate_task，改为读取当前用户家目录（~）下的文件  - 最终告诉我：第一次失败的原因、第二次成功获取的文件列表、重试次数" --toolsets delegation,terminal,file --yolo  (注：为防止控制循环失控，Hermes 设置了递归深度硬性上限 MAX_DEPTH=2 和单 Agent 迭代轮次上限 50。)  技巧 3：利用 Tool-Result 层实现动态上下文注入  这是 Hermes 里最隐蔽、也最实用的机制：Subdirectory Hints。  Hermes 会在子 Agent 进入特定目录时，自动将该目录下的 AGENTS.md 或 .cursorrules 注入到工具返回结果中。  这种方式使得上下文可以在“局部工具调用阶段”被动态扩展，而不依赖全局 Prompt 重构，从而降低静态 Prompt 膨胀的风险。  实操方式：        1.在项目的不同子目录下放置各自的 AGENTS.md（例如 frontend/AGENTS.md）。        2. 让子 Agent 进入该目录并执行 ls 或读取文件等操作。  （注意：hints 只在子 Agent 进入该目录时的工具调用结果中出现，不会持续存在于后续对话中。）        3. 执行 ls 或文件操作后，规则会随工具结果自动注入，子 Agent 随后会按照该目录的特定规则行事。  总结        •技巧 1 → Context 层（解决浪费）        •技巧 2 → Execution 层（实现自愈）        •技巧 3 → Context Management 层（按需扩展）  万能公式：delegate_task + task 数组 + 自定义 Goal = 你的专属 Agent 团队。你可以根据自己的项目结构，把这些命令里的路径和任务描述替换掉，直接在你的终端起飞。  本质区别只有一个：你是在堆 Agent，还是在做调度系统。一旦你把 Agent 当“函数”而不是“角色”，整个系统的扩展性会完全不同。


---

## 片段 23 / stream_idx=4127 / len=8147


这段内容本质上说的是：

> **不要让一个 AI 在一个超长上下文里硬撑，而是用“工程化运行框架”让 AI 分工、重启、交接、校验、复盘。**

这个思路和你现在的 SIKK-SOL 很匹配，但要注意：你不能直接照搬“10 小时连续编码”的模式。你应该把它改造成：

# SIKK 的 Harness 工程模式

也就是：

```text
主 AI 不写代码，只调度
子 AI 分别负责：规划、实现、测试、审计、复盘
所有上下文通过文件传递
每一轮完成后写进项目状态文件
下一轮 AI 先读状态文件，再继续
```

Anthropic 官方工程文章确实强调了 long-running agent 的关键问题：单靠上下文压缩不够，长任务需要 initializer / coding agent 这类跨上下文的 harness 设计，并让 agent 每轮做增量进展、留下清晰 artifact 给下一轮继续。citeturn144168search1 另一篇 Anthropic 文章也把“harness design”定义为推动长时间应用开发表现的关键工程层，而不只是提示词技巧。citeturn144168search0

---

# 一、这套方法对你现在有什么用

你现在的问题不是 AI 不够聪明，而是项目已经变成：

```text
SIKK 运行层
钱包结构层
纸面交易层
面板层
日报层
安全边界
测试体系
```

如果你每次都把所有历史讨论、所有模块、所有命令一次性塞给 AI，AI 一定会：

```text
漏掉已有模块
重复造轮子
改错主入口
删除已实现功能
把重点带偏
过度扩展 dashboard / bot / 实盘
```

所以你需要的不是“让 AI 连续聊 10 小时”，而是：

> **让 AI 每次只处理一个明确工程任务，并且通过文件继承项目状态。**

---

# 二、SIKK 项目应该怎么套 Harness 模式

你可以把 OpenClaw / Hermes 里的 AI 分成 5 个角色。

## 1. 主控 Agent：Coordinator

职责：

```text
只做调度
不写代码
不改文件
不重构
只拆任务、检查输出、决定下一步
```

主控 Agent 永远只读这些文件：

```text
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
SIKK_CHANGELOG.md
SIKK_LESSONS_LEARNED.md
```

它不应该直接读全项目所有代码。

---

## 2. 规划 Agent：Planner

职责：

```text
把需求拆成小任务
明确要改哪些文件
明确验收命令
明确不能碰哪些模块
```

输出：

```text
SIKK_TASK_PLAN.md
```

---

## 3. 开发 Agent：Builder

职责：

```text
只按计划改代码
只改指定文件
不自作主张新增功能
不删除已有模块
```

输入：

```text
SIKK_TASK_PLAN.md
相关文件路径
```

输出：

```text
SIKK_BUILD_REPORT.md
```

---

## 4. 测试 Agent：Verifier

职责：

```text
跑测试
跑 py_compile
跑安全 grep
检查输出文件
检查 live_board / site 是否生成
```

输出：

```text
SIKK_VERIFY_REPORT.md
```

---

## 5. 审计 Agent：Auditor

职责：

```text
检查有没有过度扩展
检查是否破坏安全边界
检查是否绕开 paper only
检查是否删除已实现模块
检查面板是否真能解释状态
```

输出：

```text
SIKK_AUDIT_REPORT.md
```

---

# 三、你要建立 4 个长期文件

这个是 Harness 的核心。不是靠 AI 记忆，而是靠文件。

## 1. `SIKK_PROJECT_STATE.md`

记录当前项目状态。

内容：

```markdown
# SIKK Project State

## 当前阶段
Phase B-0.5：连续运行 + 专业可视化面板优化阶段

## 主入口
python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode once

## 当前核心目标
创建本地静态可视化网站控制台：
data/gmgn_candidates_live_run/site/index.html

## 已实现模块
- sikk_live_run.py
- sikk_paper_live_runner.py
- sikk_live_orchestrator.py
- sikk_wallet_structure_gate.py
- sikk_candidate_wallet_structure_pipeline.py
- sikk_wallet_structure_daily_report.py
- live_board.md
- live_dashboard.html
- Telegram 定时广播
- paper daily report
- wallet structure daily report

## 当前不允许做
- 不执行真实 swap
- 不新增复杂后端
- 不删除已实现模块
- 不做自动实盘
- 不做大型 React 项目
- 不接数据库
```

---

## 2. `SIKK_NEXT_TASK.md`

只记录当前这一轮要做什么。

例如：

```markdown
# SIKK Next Task

## 任务
创建本地静态网站控制台。

## 新增文件
- sikk_dashboard_site_builder.py
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/app.js
- data/gmgn_candidates_live_run/site/style.css
- data/gmgn_candidates_live_run/site/dashboard_data.json

## 数据来源
- live_state.json
- tokens/*/token_status.json
- paper_live/strategy_metrics.json
- paper_live/paper_positions_open.json
- paper_live/paper_positions_closed.json
- events/live_events.jsonl

## 验收命令
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
ls -lh data/gmgn_candidates_live_run/site
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

## 禁止
- 不改交易逻辑
- 不接真实 swap
- 不新增后端
```

---

## 3. `SIKK_LESSONS_LEARNED.md`

记录踩坑。

例如：

```markdown
# SIKK Lessons Learned

## 001: 不要让 AI 删除已实现模块
之前 Runtime / dashboard / notifier / confirmation ticket 已经实现，后续只允许配置关闭，不允许删除。

## 002: Markdown 面板不适合高频观察
live_board.md 适合记录，但不适合直观观察。应生成静态 HTML 控制台。

## 003: 钱包结构缺失必须写 MISSING decision
不能让 token 静默未接入，必须写 wallet_structure_status=MISSING 和具体原因。

## 004: paper_positions_closed.csv 与 json 必须同时输出
日报读取 CSV，runner 输出 JSON 会导致统计断链。
```

---

## 4. `SIKK_CHANGELOG.md`

记录每轮改了什么。

```markdown
# SIKK Changelog

## 2026-05-03
- 新增本地静态网站控制台 builder
- 输出 dashboard_data.json
- 生成 site/index.html / app.js / style.css
- 保留 live_board.md，不删除
```

---

# 四、你在 OpenClaw 里应该怎么调用

你可以固定使用这个流程。

## 第一步：让主控 Agent 读状态

复制：

```text
你是 SIKK-SOL 项目的 Coordinator，只负责调度，不写代码。

先读取这些文件：
- SIKK_PROJECT_STATE.md
- SIKK_NEXT_TASK.md
- SIKK_LESSONS_LEARNED.md
- SIKK_CHANGELOG.md

然后输出：
1. 当前任务是否明确
2. 需要交给 Builder 修改哪些文件
3. 验收命令
4. 风险点
不要改代码。
```

---

## 第二步：让 Builder 只改指定文件

复制：

```text
你是 SIKK-SOL 项目的 Builder。

只执行 SIKK_NEXT_TASK.md 中定义的任务。
只允许新增/修改指定文件。
禁止删除任何已实现模块。
禁止新增真实交易功能。
禁止接 swap。
禁止改 paper runner 的交易逻辑。

完成后输出：
- 修改了哪些文件
- 每个文件作用
- 如何运行
- 是否有未完成项
```

---

## 第三步：让 Verifier 跑测试

复制：

```text
你是 SIKK-SOL 项目的 Verifier。

请执行：
1. py_compile 检查新增/修改文件
2. 运行 dashboard builder
3. 检查 site/index.html、app.js、style.css、dashboard_data.json 是否生成
4. 检查 dashboard_data.json 是否包含：
   - kpi
   - tokens
   - opportunities
   - entry_block_reasons
   - paper_positions
   - events
5. 不要修改业务逻辑，除非是修复明显运行错误。

输出 SIKK_VERIFY_REPORT.md。
```

---

## 第四步：让 Auditor 审计

复制：

```text
你是 SIKK-SOL 项目的 Auditor。

检查本次修改是否违反边界：
1. 是否删除已有模块
2. 是否引入真实交易
3. 是否新增复杂后端
4. 是否改变 paper runner 交易逻辑
5. 是否破坏主入口 sikk_live_run.py
6. 是否让 dashboard 只做观察，不做执行
7. 是否所有输出路径仍在 data/gmgn_candidates_live_run 下

输出 SIKK_AUDIT_REPORT.md。
```

---

# 五、把 “Lessons Learned” 用到你的可视化网站任务

你当前要给 OpenClaw 的任务，不要再开大任务。应该拆成 3 轮。

## Round 1：只生成数据

任务：

```text
创建 sikk_dashboard_site_builder.py，只生成 dashboard_data.json，不做 UI。
```

验收：

```bash
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 80
```

dashboard_data.json 必须包含：

```text
kpi
tokens
opportunities
entry_block_reasons
wallet_structure_summary
paper_positions
events
```

---

## Round 2：生成静态页面

任务：

```text
基于 dashboard_data.json 生成 index.html、app.js、style.css。
```

验收：

```bash
ls -lh data/gmgn_candidates_live_run/site
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site
```

---

## Round 3：接入主流程

任务：

```text
在 sikk_live_run.py 每轮结束后调用 dashboard builder。
失败不能中断主流程，只写事件。
```

验收：

```bash
python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode once
ls -lh data/gmgn_candidates_live_run/site
```

---

# 六、你这个系统里 Harness 的关键规则

以后你在 OpenClaw 上跑 SIKK，不要让 AI “自由发挥”。

固定规则：

```text
1. 每轮只做一个任务
2. 每轮必须有验收命令
3. 每轮必须更新 CHANGELOG
4. 每轮踩坑必须更新 LESSONS_LEARNED
5. 主 Agent 不写代码
6. Builder 不做规划
7. Verifier 不新增功能
8. Auditor 不修代码，只审计
9. 所有上下文通过文件传递
10. 不允许依赖聊天历史作为项目记忆
```

---

# 七、针对你当前项目的 Harness 总提示词

你可以保存成：

```text
SIKK_HARNESS_SYSTEM_PROMPT.md
```

内容如下：

```text
你正在参与 SIKK-SOL 项目开发。

SIKK-SOL 是 Solana meme token 的结构智能纸面验证系统，不是自动实盘交易系统。

当前阶段：
Phase B-0.5：连续运行 + 专业可视化面板优化阶段。

系统目标：
- 候选发现
- K线信号
- 钱包结构门禁
- quote/security
- 状态机
- paper runner
- daily report
- 可视化面板

核心边界：
- 不执行真实 swap
- 不读取或写入私钥
- 不新增自动实盘 broadcast
- 不删除已实现模块
- 不为了复杂而升级
- 优先实用、可运行、可观察、可复盘

工作方式：
- Coordinator 只调度，不写代码
- Planner 只拆任务，不改代码
- Builder 只按任务改指定文件
- Verifier 只测试和修运行错误
- Auditor 只审计边界和一致性

必须读取：
- SIKK_PROJECT_STATE.md
- SIKK_NEXT_TASK.md
- SIKK_LESSONS_LEARNED.md
- SIKK_CHANGELOG.md

每次任务必须输出：
- 修改文件
- 运行命令
- 验收结果
- 未完成项
- 是否更新 lessons learned
```

---

# 八、你现在最应该做的下一步

不是让 AI 连续工作 10 小时。  
而是让它做 **第一轮 Harness 任务**：

```text
创建 SIKK_PROJECT_STATE.md
创建 SIKK_NEXT_TASK.md
创建 SIKK_LESSONS_LEARNED.md
创建 SIKK_CHANGELOG.md
然后只做 dashboard_data.json builder。
```

直接发给 OpenClaw：

```text
请按照 Harness 工程方式工作。

第一步不要写业务代码，先创建以下 4 个项目控制文件：
1. SIKK_PROJECT_STATE.md
2. SIKK_NEXT_TASK.md
3. SIKK_LESSONS_LEARNED.md
4. SIKK_CHANGELOG.md

然后把当前任务定义为：
创建本地静态可视化网站控制台的第一阶段：只实现 sikk_dashboard_site_builder.py，并生成 dashboard_data.json。

不要先做 UI。
不要改交易逻辑。
不要删除已有模块。
不要接真实 swap。
```

---

# 九、这段内容对你的最大启发

你现在不应该追求：

```text
让一个 AI 连续干 10 小时
```

而应该追求：

```text
让 10 个干净上下文的 AI，每次只做一件小事，并且通过文件交接
```

这才是适合 SIKK 的 Harness 工程。

---

# 本次认知升级点

> SIKK 后续开发应该从“长对话驱动”升级为“文件驱动的 Harness 工程”。

核心不是 AI 记住多少，而是：

```text
项目状态文件
任务文件
经验库
变更日志
测试报告
审计报告
```

让 AI 每一轮都从文件恢复上下文，而不是靠聊天历史。

---

# 尚未解决问题

下一步要落地：

```text
1. 创建 SIKK_PROJECT_STATE.md
2. 创建 SIKK_NEXT_TASK.md
3. 创建 SIKK_LESSONS_LEARNED.md
4. 创建 SIKK_CHANGELOG.md
5. 第一轮只实现 dashboard_data.json builder
6. 第二轮再做静态 HTML 控制台
7. 第三轮接入 sikk_live_run.py
```


---

## 片段 24 / stream_idx=4210 / len=884


让AI连续工作10小时不崩溃？揭秘Anthropic官方推崇的“Harness工程”！ 很多人用Claude Code跑长任务，跑着跑着AI就变傻、甚至罢工。 原因很简单：上下文窗口爆了。 今天分享一套让AI“无限续航”的系统级方案（Harness Engineering），不仅能让AI干活，还能让它自我进化。 1⃣ 核心原理：重置上下文 AI的记性有限。官方Anthropic的思路是：把大任务拆碎，每次只让AI在一个全新的、干净的上下文里干一件小事。 ❌ 错误做法：把所有需求一次性塞给AI。 ✅ 正确做法：拆解任务 -> 独立会话执行 -> 记录进度 -> 下一个循环。 2⃣ 方案对比：Ralph vs 多智能体 方案A（Ralph循环）： 用Bash脚本写个while循环，强制重启新会话。简单粗暴，适合极客。 方案B（多智能体协同 - 推荐）： 我在用的方案。更灵活，更像真实团队。 主Agent（Coordinator）： 只负责调度，绝不写代码（保持上下文极其干净）。 子Agent（Workers）： 计划、开发、测试（布局/美观/动画）。各司其职，独立上下文。 3⃣ 工作流设计（关键！） 我的实战工作流： 主Agent 接收需求 -> 丢给 计划Agent 出排期。 主Agent 拿到计划 -> 派给 开发Agent 写代码（只传文件路径，不传大段代码！）。 开发完 -> 派给 测试Agent 找Bug。 Bug修复闭环： 测试挂了？用 resume 参数唤醒同一个开发Agent修Bug（保留现场上下文），而不是开新号！ 4⃣ 让AI自我进化的Secret Sauce Lessons Learned： 建一个经验库文件。每次踩坑，强制AI把错误写进去。下一次开发，先读这个文件，避免重复犯错。 文件通信： Agent之间只传文件路径（Path），不传具体内容。主Agent的上下文永远只有几行字，永不爆窗。 这套系统我跑了一个通宵，生成了20多页PPT，质量极高。 真正的Harness不是让AI更聪明，而是设计一套不依赖AI记性的流程


---

## 片段 25 / stream_idx=4289 / len=7806


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

# 一、在 OpenClaw 里不要这样说

不要说：

```text
帮我做一个网站
帮我做一个 dashboard
帮我做一个后台系统
帮我做一个交易控制台
```

这样它容易给你做复杂架构。

应该说：

```text
在现有项目基础上，创建一个本地静态可视化面板，只读取现有输出文件，不新增后端，不接真实交易，不改变交易逻辑。
```

---

# 二、最终文件结构

让 OpenClaw 创建这些文件：

```text
/root/sikk-gmgn/
  sikk_dashboard_site_builder.py

data/gmgn_candidates_live_run/
  site/
    index.html
    app.js
    style.css
    dashboard_data.json
```

数据来源：

```text
data/gmgn_candidates_live_run/live_state.json
data/gmgn_candidates_live_run/live_board.md
data/gmgn_candidates_live_run/tokens/*/token_status.json
data/gmgn_candidates_live_run/paper_live/strategy_metrics.json
data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
data/gmgn_candidates_live_run/events/live_events.jsonl
data/gmgn_candidates_live_run/state_machine/candidate_states.json
data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json
```

---

# 三、你给 OpenClaw 的第一段任务

直接复制这一段给 OpenClaw：

```text
任务：为 SIKK-SOL 项目创建一个本地静态可视化网站控制台。

重要边界：
1. 不删除任何已有模块。
2. 不改真实交易逻辑。
3. 不接真实 swap。
4. 不新增复杂后端。
5. 不使用数据库。
6. 不做登录系统。
7. 不做 Telegram / Discord 新功能。
8. 只读取现有输出文件，生成静态网站。
9. 网站只用于观察、筛选、复盘，不用于执行交易。

当前项目目录：
/root/sikk-gmgn

当前数据目录：
data/gmgn_candidates_live_run

请新增：
1. sikk_dashboard_site_builder.py
2. data/gmgn_candidates_live_run/site/index.html
3. data/gmgn_candidates_live_run/site/app.js
4. data/gmgn_candidates_live_run/site/style.css
5. data/gmgn_candidates_live_run/site/dashboard_data.json

运行方式：
cd /root/sikk-gmgn
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

查看方式：
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

目标：
打开浏览器后，能像专业交易控制台一样看到：
- 系统总览
- 机会漏斗
- 重点机会
- Token 总表
- 当前纸面仓位
- 钱包结构状态
- 未入场原因统计
- 最新事件

不要新增无关功能。先保证可运行、清晰、可维护。
```

---

# 四、让 OpenClaw 创建的网站页面结构

继续发第二段：

```text
网站页面必须包含 8 个区域：

1. 顶部 KPI 卡片
显示：
- token_count
- WATCHING 数
- BLOCKED 数
- PAUSE 数
- PAPER_READY 数
- PAPER_OPEN 数
- wallet_structure_coverage
- wallet_missing_count
- open_positions
- closed_positions
- closed_win_rate
- avg_closed_pnl

2. Pipeline 漏斗
显示：
- candidates
- signal_ready
- wallet_support
- quote_security_pass
- paper_ready
- paper_open

3. 重点机会区
只显示：
- PAPER_OPEN
- PAPER_READY
- WALLET_SUPPORT
- S3 / S4 信号
- quote/security 通过的 token

4. Token 总表
字段：
- token_symbol
- token_address
- current_state
- priority_level
- signal_level
- signal_gate
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

5. 筛选功能
必须支持：
- token 搜索
- current_state 筛选
- wallet_structure_status 筛选
- paper_status 筛选
- reason 搜索

6. 未入场原因统计
统计：
- wallet_structure_missing
- wallet_block
- signal_not_ready
- quote_not_ready
- security_not_ready
- paper_runner_not_called
- state_not_ready
- data_quality_low

7. 当前纸面仓位
字段：
- token_symbol
- status
- entry_price
- current_price
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- wallet_structure_status
- next_action
- exit_reason
- failure_type

8. 最新事件
读取：
data/gmgn_candidates_live_run/events/live_events.jsonl

显示：
- time
- event_type
- token_symbol
- message
```

---

# 五、排序规则

发第三段：

```text
Token 排序规则必须专业化，不要按发现顺序。

排序优先级：

1. PAPER_OPEN
2. PAPER_READY
3. WALLET_SUPPORT
4. PAUSE
5. WATCHING
6. BLOCKED
7. MISSING
8. ERROR

同级内部排序：
1. wallet_structure_score 高的靠前
2. counterparty_pressure_score 低的靠前
3. data_quality_score 高的靠前
4. paper_pnl_pct 高的靠前

新增 priority_level 字段：

- P0_ACTIVE_POSITION：已有纸面仓位
- P1_PAPER_READY：准备纸面入场
- P2_STRUCTURE_SUPPORT：钱包结构支持
- P3_WATCHING：普通观察
- P4_PAUSE：暂停
- P5_BLOCKED：阻断
- P6_DATA_MISSING：数据缺失
- P7_ERROR：错误

priority_level 只用于面板排序，不作为买入信号。
```

---

# 六、Reason 和 Next Action 规则

发第四段：

```text
面板里 Reason 和 Next Action 不能为空。

main_reason 生成规则：
1. 如果 current_state = BLOCKED，优先显示 block reason。
2. 如果 wallet_structure_status = WALLET_BLOCK，显示钱包结构阻断原因。
3. 如果 wallet_structure_status = MISSING，显示 missing reason。
4. 如果 current_state = WATCHING，显示 watching_reason。
5. 如果 quote_gate != ALLOW，显示 quote reason。
6. 如果 security_gate != ALLOW，显示 security reason。
7. 如果 paper_status = OPEN，显示 paper reason 或持仓状态。
8. 如果都没有，显示 "等待下一轮信号确认"。

next_action 允许值：
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

next_action 生成规则：
- PAPER_OPEN → HOLD 或 EXIT_MONITOR
- PAPER_READY → OPEN_PAPER_POSITION
- WALLET_SUPPORT 但 signal 未通过 → WAIT_SIGNAL
- wallet MISSING → FIX_DATA_SOURCE
- WALLET_BLOCK / BLOCKED → COOLING
- quote 失败 → WAIT_QUOTE
- security 失败 → WAIT_SECURITY
- PAUSE → WAIT_WALLET
- ERROR → FIX_DATA_SOURCE
```

---

# 七、视觉规则

发第五段：

```text
视觉要求：
1. 使用深色专业风格。
2. 顶部 KPI 卡片要清晰。
3. Token 表格要紧凑。
4. 状态用颜色区分：
   - PAPER_OPEN / PAPER_READY：绿色
   - WALLET_SUPPORT：蓝绿色
   - WATCHING / PAUSE：黄色
   - BLOCKED / WALLET_BLOCK：红色
   - MISSING / DATA_QUALITY_LOW：灰色
   - ERROR：紫色或红色
5. 表格支持搜索和筛选。
6. 页面不需要复杂图表，第一版可以只用卡片、表格、简单漏斗条。
7. 不要引入大型前端框架。
8. index.html、app.js、style.css 必须可以直接用浏览器打开。
```

---

# 八、数据生成逻辑

发第六段：

```text
sikk_dashboard_site_builder.py 的职责：

1. 读取 base-dir 下的现有输出文件。
2. 合并 token_status.json。
3. 合并 paper open / closed positions。
4. 合并 strategy_metrics.json。
5. 合并 latest events。
6. 统计 wallet_structure coverage。
7. 统计未入场原因 Top。
8. 生成 dashboard_data.json。
9. 复制或生成 index.html、app.js、style.css。

不要改变原始数据。
不要覆盖 paper runner 输出。
不要修改交易逻辑。
```

---

# 九、验收命令

让 OpenClaw 完成后，你这样跑：

```bash
cd /root/sikk-gmgn

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site
```

检查输出：

```bash
ls -lh data/gmgn_candidates_live_run/site
```

应该看到：

```text
index.html
app.js
style.css
dashboard_data.json
```

本地启动：

```bash
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site
```

浏览器访问：

```text
http://你的VPS_IP:8080
```

更安全的方式是 SSH 隧道：

```bash
ssh -L 8080:127.0.0.1:8080 root@你的VPS_IP
```

然后本地浏览器打开：

```text
http://127.0.0.1:8080
```

---

# 十、让主流程自动生成网站

等网站 builder 跑通后，再让 OpenClaw 把它接到主流程最后。

发这段：

```text
在 sikk_live_run.py 的每轮运行结束后，调用：

python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

要求：
1. dashboard 生成失败不能中断主流程。
2. 失败只写入事件日志。
3. 不影响 paper runner。
4. 不影响 daily_report。
5. 不影响真实交易边界。
```

---

# 十一、不要让 OpenClaw 做过头

明确告诉它：

```text
本阶段不要做：
1. 登录系统
2. 数据库
3. FastAPI 后端
4. React 项目
5. 自动交易按钮
6. 真实 swap
7. Telegram 新功能
8. 多用户权限
9. 复杂 K线图
10. 钱包图谱可视化

只做静态专业控制台。
```

---

# 十二、第一版网站做到什么程度就够

第一版只要能做到：

```text
1. 一眼看系统状态
2. 一眼看 PAPER_OPEN / PAPER_READY
3. 一眼看 wallet_structure_missing 数量
4. 一眼看为什么没有 paper entry
5. 一眼看当前纸面仓位盈亏
6. 可以搜索 token
7. 可以按状态筛选
```

就够了。

不要追求“像交易所一样复杂”。  
你当前要的是：

```text
可观察
可诊断
可复盘
可决策
```

---

# 十三、推荐你在 OpenClaw 里分 3 次提交

## 第一次：只做 builder 和 dashboard_data

```text
先实现 sikk_dashboard_site_builder.py，生成 dashboard_data.json。
不要先写复杂 UI。
```

## 第二次：做 index.html / app.js / style.css

```text
基于 dashboard_data.json 做静态页面。
```

## 第三次：接入 sikk_live_run.py

```text
每轮结束后自动刷新 site。
```

这样最稳。

---

# 最短结论

你在 OpenClaw 上应该这样做：

```text
创建一个本地静态网站控制台：
sikk_dashboard_site_builder.py
读取现有 SIKK 输出
生成 data/gmgn_candidates_live_run/site/index.html
浏览器打开看
```

重点不是“做网站”，而是把系统变成：

```text
专业可视化决策控制台
```

它必须帮你直观看到：

```text
有没有机会
卡在哪一步
为什么没入场
钱包结构是否接入
纸面仓位是否有效
下一步该修什么
```


---

## 片段 26 / stream_idx=4484 / len=6280


对，你现在应该做一个**网站式面板**，但不要做复杂网站。

准确说：

> **不是新建一个完整 Web 系统，而是把现有 `live_dashboard.html` 升级成“本地静态专业控制台”。**

这样最适合你当前阶段。

---

# 一、为什么现在 `live_board.md` 会显得乱

`live_board.md` 的问题不是内容少，而是：

```text
1. 信息是线性排列的
2. 不能筛选
3. 不能按状态聚合
4. 不能点进单个 token
5. 阻断原因、纸面仓位、钱包结构混在一起
6. 没有视觉优先级
```

所以你会感觉：

```text
数据都有
但看不出重点
```

这就是 Markdown 面板的天然限制。

---

# 二、现在应该做什么类型的网站

不要做：

```text
React 大项目
FastAPI 后端
数据库后台
登录系统
复杂图表系统
```

现在只做：

```text
静态 HTML 控制台
```

也就是：

```text
Python 读取现有 JSON / CSV / MD
→ 生成一个 index.html
→ 浏览器打开看
```

路径建议：

```text
data/gmgn_candidates_live_run/site/index.html
```

运行：

```bash
cd /root/sikk-gmgn
python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site
```

然后查看：

```bash
cd /root/sikk-gmgn
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site
```

浏览器打开：

```text
http://你的服务器IP:8080
```

如果是在 VPS 上，先不要公网暴露，最好先用 SSH 隧道或本地查看。

---

# 三、网站面板应该分成 7 个页面区域

## 1. 顶部总览卡片

一打开就看到：

```text
Runtime 状态
本轮 token 数
PAPER_READY 数
PAPER_OPEN 数
WALLET_BLOCK 数
钱包结构接入率
当前开放仓位
今日收益
```

例如：

```text
Token=[REDACTED]
Watching: 39
Blocked: 9
Wallet Coverage: 7/48
Paper Open: 2
Closed Win Rate: 100%
Avg PnL: 284.45%
```

---

## 2. 漏斗图 / 流程图

这个很重要，能直观看出卡在哪一步。

```text
候选发现 48
  ↓
K线通过 x
  ↓
钱包结构通过 x
  ↓
Quote/Security 通过 x
  ↓
PAPER_READY x
  ↓
PAPER_OPEN 2
```

你现在最大问题会一眼显示：

```text
钱包结构未接入 41
```

---

## 3. 重点机会区

只显示最值得看的 token：

```text
PAPER_OPEN
PAPER_READY
WALLET_SUPPORT
S3/S4 信号
Quote/Security 通过
```

这个区应该在最上方，不要让 48 个 token 淹没重点。

---

## 4. Token 总表

支持：

```text
搜索 token
按状态筛选
按钱包状态筛选
按 paper 状态筛选
按 reason 搜索
```

表格字段：

```text
Token
State
Priority
Signal
Wallet
Structure Score
Risk Score
Counterparty
Quote
Security
Paper
PnL
Reason
Next Action
```

排序规则：

```text
PAPER_OPEN
PAPER_READY
WALLET_SUPPORT
PAUSE
WATCHING
BLOCKED
MISSING
ERROR
```

---

## 5. 单币详情面板

点击 token 后右侧展示：

```text
市场信息
K线信号
钱包结构
quote/security
paper 仓位
阻断原因
下一步动作
最近事件
```

这样你不用一个个打开 `token_status.md`。

---

## 6. 未入场原因统计

这一块必须图形化。

例如柱状图：

```text
wallet_structure_missing: 41
wallet_block: 7
signal_not_ready: 35
quote_not_ready: 12
security_not_ready: 3
```

这样你能直接知道：

```text
下一步应该修钱包结构接入，而不是调策略参数
```

---

## 7. 当前纸面仓位区

专门显示：

```text
当前开放仓位
浮盈
最大浮盈
最大回撤
钱包状态变化
是否进入 EXIT_MONITOR
```

这是你每天最该看的地方。

---

# 四、网站不是为了好看，而是为了解决 4 个问题

你现在创建网站的目的应该是：

## 1. 快速判断有没有机会

```text
当前有没有 PAPER_READY？
有没有 WALLET_SUPPORT？
有没有 PAPER_OPEN？
```

## 2. 快速判断系统卡在哪里

```text
钱包结构没接入？
K线没信号？
Quote 失败？
Security 失败？
Paper runner 没开仓？
```

## 3. 快速判断 token 为什么没进场

```text
Reason / Next Action 必须可见
```

## 4. 快速判断纸面验证是否有效

```text
胜率
平均收益
最大回撤
失败原因
不同 wallet status 的表现
```

---

# 五、推荐网站文件结构

```text
data/gmgn_candidates_live_run/site/
  index.html
  app.js
  style.css
  dashboard_data.json
```

其中：

```text
dashboard_data.json
```

由 Python 生成，整合这些来源：

```text
live_state.json
tokens/*/token_status.json
paper_live/strategy_metrics.json
paper_live/paper_positions_open.json
paper_live/paper_positions_closed.json
events/live_events.jsonl
reports/wallet_structure_daily_report_YYYYMMDD.md
```

---

# 六、最小网站版本就够了

第一版只做这些：

```text
1. 顶部 KPI 卡片
2. Token 表格
3. 状态筛选
4. Token 搜索
5. 未入场原因统计
6. 当前纸面仓位
7. 最新事件
```

不要先做：

```text
登录
数据库
复杂曲线
多用户
权限
实时 websocket
自动交易按钮
```

---

# 七、你现在应该让 Codex 做的任务

可以直接发：

```text
任务：把 SIKK 当前 live_dashboard.html 升级为本地静态专业控制台，不新增后端，不接真实交易，不删除已有模块。

目标：
创建 data/gmgn_candidates_live_run/site/index.html，用浏览器查看系统状态。

数据来源：
- data/gmgn_candidates_live_run/live_state.json
- data/gmgn_candidates_live_run/tokens/*/token_status.json
- data/gmgn_candidates_live_run/paper_live/strategy_metrics.json
- data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
- data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
- data/gmgn_candidates_live_run/events/live_events.jsonl

新增脚本：
- sikk_dashboard_site_builder.py

输出：
- data/gmgn_candidates_live_run/site/index.html
- data/gmgn_candidates_live_run/site/dashboard_data.json
- data/gmgn_candidates_live_run/site/style.css
- data/gmgn_candidates_live_run/site/app.js

页面结构：
1. 顶部 KPI 卡片
   - token_count
   - WATCHING
   - BLOCKED
   - PAPER_READY
   - PAPER_OPEN
   - wallet_structure_coverage
   - open_positions
   - closed_win_rate
   - avg_pnl

2. Pipeline 漏斗
   - candidates
   - signal_pass
   - wallet_support
   - quote_security_pass
   - paper_ready
   - paper_open

3. 重点机会区
   - PAPER_OPEN
   - PAPER_READY
   - WALLET_SUPPORT
   - S3/S4 signal

4. Token 总表
   字段：
   - token_symbol
   - current_state
   - priority_level
   - signal_gate
   - wallet_structure_status
   - wallet_structure_score
   - wallet_risk_score
   - counterparty_pressure_score
   - quote_gate
   - security_gate
   - paper_status
   - paper_pnl_pct
   - main_reason
   - next_action

5. 筛选功能
   - token 搜索
   - current_state 筛选
   - wallet_structure_status 筛选
   - paper_status 筛选

6. 未入场原因统计
   - wallet_structure_missing
   - wallet_block
   - signal_not_ready
   - quote_not_ready
   - security_not_ready
   - paper_runner_not_called
   - state_not_ready

7. 当前纸面仓位
   - token
   - entry_price
   - current_price
   - unrealized_pnl_pct
   - max_floating_profit_pct
   - max_drawdown_pct
   - wallet_structure_status
   - next_action

8. 最新事件
   - time
   - event_type
   - token
   - message

排序规则：
- PAPER_OPEN
- PAPER_READY
- WALLET_SUPPORT
- PAUSE
- WATCHING
- BLOCKED
- MISSING
- ERROR

视觉要求：
- PAPER_OPEN / PAPER_READY 用绿色
- WALLET_SUPPORT 用蓝绿色
- WATCHING / PAUSE 用黄色
- BLOCKED / WALLET_BLOCK 用红色
- MISSING 用灰色
- Reason 不允许为空
- Next Action 不允许为空

验收：
运行：
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site

然后：
python3 -m http.server 8080 -d data/gmgn_candidates_live_run/site

浏览器打开后，必须一眼看到：
- 系统是否正常运行
- 当前有没有机会
- 为什么没有新增 paper entry
- 哪些 token 被钱包结构阻断
- 钱包结构未接入原因
- 当前 paper 仓位盈亏
```

---

# 八、你现在是否应该创建网站？

结论：

```text
应该。
```

但只做：

```text
本地静态网站控制台
```

不要做：

```text
复杂 Web 平台
```

因为你现在需要的是：

```text
直观
聚合
筛选
排序
原因解释
纸面表现展示
```

不是新架构。

---

# 九、最终判断

你现在的感觉是对的：

> Markdown 面板已经不够用了。

下一步最合理的是：

```text
把 live_board.md / live_dashboard.html 升级成一个本地静态网站控制台。
```

它会让你从：

```text
看一堆文本
```

变成：

```text
看系统决策面板
```

重点不是美观，而是让你一眼判断：

```text
有没有机会
卡在哪一步
为什么没入场
钱包结构是否接入
纸面验证是否有效
```

这一步值得做，而且符合当前实用优先级。


---

## 片段 27 / stream_idx=4641 / len=6198


这套命令说明：**你现在已经不是“没有系统”，而是系统已经有了运行链路，只是需要做一次命令体系收敛和输出一致性检查。**

当前可以判断为：

```text
SIKK-SOL 已进入：Phase B-0.5
连续运行 + 纸面验证 + 专业面板优化阶段
```

不是概念阶段了。

---

# 一、你现在已经具备的能力

从你贴的命令看，系统已经有这些部分：

| 模块 | 状态 |
|---|---|
| `sikk_live_run.py` 主入口 | 已有 |
| `sikk_paper_live_runner.py` 纸面 runner | 已有 |
| `sikk_live_orchestrator.py` Runtime 观测层 | 已有 |
| `live_board.md` 主面板 | 已有 |
| `live_dashboard.html` HTML 面板 | 已有 |
| `paper_daily_report_YYYYMMDD.md` 纸面日报 | 已有 |
| `wallet_structure_daily_report` 钱包结构日报 | 已有 |
| `events/live_events.jsonl` 事件记录 | 已有 |
| 测试文件 | 已有 |
| 安全边界 grep 检查 | 已有 |

所以现在重点不是继续加模块，而是：

```text
让现有命令更稳定、更清晰、更统一、更适合专业面板展示。
```

---

# 二、现在命令体系里有 3 个需要修正的点

## 1. `paper_positions_closed.json` 和 `paper_positions_closed.csv` 不一致

你前面纸面 runner 输出写的是：

```text
paper_positions_open.json
paper_positions_closed.json
paper_trades.csv
paper_equity_curve.csv
strategy_metrics.json
risk_events.jsonl
```

但钱包结构日报命令用的是：

```bash
--closed-positions data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv
```

这里有冲突。

### 修法二选一

推荐保留 CSV，因为日报统计更方便：

```text
paper_positions_closed.csv
```

让 `sikk_paper_live_runner.py` 同时输出：

```text
paper_positions_closed.json
paper_positions_closed.csv
paper_positions_open.json
paper_positions_open.csv
```

否则 `sikk_wallet_structure_daily_report.py` 会读不到关闭仓位。

---

## 2. `sikk_live_run.py` 和 `sikk_live_orchestrator.py` 入口要明确主次

你现在有两个入口：

```bash
python3 sikk_live_run.py ...
```

和：

```bash
python3 sikk_live_orchestrator.py --mode once ...
```

这两个都存在可以，但必须定义：

```text
sikk_live_run.py = 主运行入口
sikk_live_orchestrator.py = 观测层 / 面板层 / 状态汇总层
```

不要让两个脚本都各自跑一套完整 pipeline，否则会出现：

```text
重复处理 token
状态文件覆盖
paper runner 重复开仓
事件日志重复
```

### 建议定义

```text
常规运行只用 sikk_live_run.py
sikk_live_orchestrator.py 只用于重建面板、状态汇总、事件观测
```

---

## 3. 安全 grep 会误报配置字段

你现在 grep 包含：

```bash
bot_token
webhook_url
api key
```

如果代码里有配置字段名，比如：

```python
telegram_bot_token=[REDACTED]
discord_webhook_url = ""
```

也会被 grep 出来。

这不一定是风险，真正风险是：

```text
真实密钥值
私钥
自动 swap 执行
真实交易 broadcast
```

### 建议把安全检查分成两类

#### A. 禁止真实交易路径

```bash
grep -R "gmgn-cli swap\|gmgn-cli multi-swap\|order strategy create\|onchainos swap execute\|swap execute" \
  sikk_*.py run_sikk_gmgn_pipeline.py tests/*.py | cat
```

#### B. 检查敏感配置是否泄露

```bash
grep -R "private key\|api_key *= *['\"][^'\"]\+\|bot_token *= *['\"][^'\"]\+\|webhook_url *= *['\"][^'\"]\+" \
  sikk_*.py run_sikk_gmgn_pipeline.py config/*.json tests/*.py | cat
```

这样不会因为字段名存在就误判。

---

# 三、现在最常用 3 条命令可以保留

你最后总结的 3 条是对的。

## 1. 正常跑一轮

```bash
cd /root/sikk-gmgn
python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode once
```

## 2. 连续跑

```bash
cd /root/sikk-gmgn
python3 sikk_live_run.py \
  --output-root data/gmgn_candidates_live_run \
  --limit 50 \
  --quote-sources okx \
  --default-quote-amount-sol 0.01 \
  --mode loop \
  --interval-sec 600
```

## 3. 看面板

```bash
cd /root/sikk-gmgn
sed -n '1,220p' data/gmgn_candidates_live_run/live_board.md
```

这 3 条就是当前最实用的主操作。

---

# 四、建议你把命令体系重新分成 5 类

## A. 主运行命令

只保留：

```bash
python3 sikk_live_run.py ...
```

用于：

```text
候选发现
结构分析
quote/security
状态机
纸面交易
日报
面板
```

---

## B. 单独纸面更新命令

保留：

```bash
python3 sikk_paper_live_runner.py ...
```

用于单独调试纸面仓位，不作为日常主入口。

---

## C. 报告命令

保留：

```bash
python3 sikk_wallet_structure_daily_report.py ...
```

用于重建钱包结构日报。

---

## D. 查看命令

保留：

```bash
sed -n '1,220p' data/gmgn_candidates_live_run/live_board.md
realpath data/gmgn_candidates_live_run/live_dashboard.html
tail -n 50 data/gmgn_candidates_live_run/events/live_events.jsonl
sed -n '1,200p' data/gmgn_candidates_live_run/state_machine/state_summary.md
ls data/gmgn_candidates_live_run/paper_live/daily_reports/
```

---

## E. 安全 / 测试命令

保留：

```bash
python3 -m pytest ...
python3 -m py_compile ...
grep ...
```

这一类只在修改代码后跑，不需要每轮都跑。

---

# 五、下一步最该做的不是加功能，而是统一输出

你现在最需要检查这些文件是否稳定生成：

```text
data/gmgn_candidates_live_run/live_board.md
data/gmgn_candidates_live_run/live_dashboard.html
data/gmgn_candidates_live_run/events/live_events.jsonl
data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
data/gmgn_candidates_live_run/paper_live/paper_trades.csv
data/gmgn_candidates_live_run/paper_live/strategy_metrics.json
data/gmgn_candidates_live_run/paper_live/daily_reports/paper_daily_report_YYYYMMDD.md
data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_YYYYMMDD.md
```

尤其要确认：

```text
paper_positions_closed.csv 是否存在
```

因为钱包结构日报正在读它。

---

# 六、现在阶段的准确判断

你当前不是“还没搭起来”。

更准确是：

```text
运行链路已搭建
纸面交易已运行
Telegram 广播已运行
面板已存在
日报已存在
但专业面板和数据一致性还需要收敛
```

现在属于：

```text
Phase B-0.5：连续运行 + 专业面板收敛阶段
```

下一阶段才是：

```text
Phase B-1：连续纸面样本积累阶段
```

进入 Phase B-1 的条件：

```text
1. 连续运行 24 小时不中断
2. live_board.md 清晰显示机会、阻断、未入场原因
3. wallet_structure 未接入数量明显下降，或每个 MISSING 都有原因
4. paper_positions_closed.csv/json 输出一致
5. paper_daily_report 能解释为什么没有新增入场
6. 至少开始稳定积累 paper 样本
```

---

# 七、给 Codex / OpenClaw 的整理指令

你可以直接发：

```text
当前 SIKK-SOL 已有完整运行命令体系，不要删除已实现模块，不要新增无关功能。现在只做命令与输出一致性收敛。

目标：
1. 明确 sikk_live_run.py 是主入口。
2. sikk_live_orchestrator.py 只作为观测层 / 面板层 / 状态汇总层，不重复执行完整 pipeline。
3. 修复 paper_positions_closed.json 与 paper_positions_closed.csv 不一致问题。
4. sikk_paper_live_runner.py 必须同时输出：
   - paper_positions_open.json
   - paper_positions_open.csv
   - paper_positions_closed.json
   - paper_positions_closed.csv
   - paper_trades.csv
   - paper_equity_curve.csv
   - strategy_metrics.json
   - risk_events.jsonl
   - daily_reports/paper_daily_report_YYYYMMDD.md
5. sikk_wallet_structure_daily_report.py 默认读取：
   data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv
   如果 CSV 不存在，但 JSON 存在，则自动兼容读取 JSON。
6. live_board.md 要继续优化成专业面板结构：
   - 系统总览
   - 重点机会
   - 钱包结构状态
   - 阻断 / 暂停原因
   - 当前纸面仓位
   - 未入场原因 Top
   - 今日纸面验证
   - 最新事件
7. 修正安全 grep，避免只因为配置字段名 bot_token / webhook_url 存在就误报。
8. 保留测试命令和 py_compile 检查。
9. 不接真实 swap，不执行真实交易，不启用 broadcast。
```

---

# 最短结论

你这套命令现在已经能支撑系统运行。  
当前要修的是：

```text
1. 输出文件格式一致
2. 主入口和观测入口分工清楚
3. live_board 专业化
4. paper closed CSV/JSON 对齐
5. 钱包结构日报能稳定读取纸面结果
```

先把这些收敛好，再继续看下一轮 Telegram 广播结果。


---

## 片段 28 / stream_idx=4697 / len=4044


cd /root/sikk-gmgn
python3 sikk_paper_live_runner.py \
  --candidate-states data/gmgn_candidates_live_run/state_machine/candidate_states.json \
  --signal-summary data/gmgn_candidates_live_run/candidate_signal_outputs/candidate_signal_summary.json \
  --quote-security-summary data/gmgn_candidates_live_run/quote_security/candidate_quote_security_summary.json \
  --output-dir data/gmgn_candidates_live_run/paper_live

输出：

- paper_positions_open.json
- paper_positions_closed.json
- paper_trades.csv
- paper_equity_curve.csv
- strategy_metrics.json
- risk_events.jsonl
- daily_reports/paper_daily_report_YYYYMMDD.md

---

9. 钱包结构纸面日报

cd /root/sikk-gmgn
python3 sikk_wallet_structure_daily_report.py \
  --closed-positions data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv \
  --failure-attribution data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl \
  --output-dir data/gmgn_candidates_live_run/reports \
  --report-date 20260502

---

10. Runtime 观测层

cd /root/sikk-gmgn
python3 sikk_live_orchestrator.py \
  --mode once \
  --candidates data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json \
  --base-dir data/gmgn_candidates_live_run

循环：

python3 sikk_live_orchestrator.py \
  --mode loop \
  --candidates data/gmgn_candidates_live_run/gmgn_new_token_filter/token_candidates.json \
  --base-dir data/gmgn_candidates_live_run \
  --interval-sec 600

---

D. 输出查看命令

看主面板

cd /root/sikk-gmgn
sed -n '1,220p' data/gmgn_candidates_live_run/live_board.md

看HTML 面板路径

cd /root/sikk-gmgn
realpath data/gmgn_candidates_live_run/live_dashboard.html

看最新事件

cd /root/sikk-gmgn
tail -n 50 data/gmgn_candidates_live_run/events/live_events.jsonl

看状态机结果

cd /root/sikk-gmgn
sed -n '1,200p' data/gmgn_candidates_live_run/state_machine/state_summary.md

看纸面日报

cd /root/sikk-gmgn
ls data/gmgn_candidates_live_run/paper_live/daily_reports/

---

E. 安全边界命令/ 检查命令

跑测试

cd /root/sikk-gmgn
python3 -m pytest tests/test_sikk_live_run.py tests/test_sikk_runtime_v02.py -q

跑完整相关测试

cd /root/sikk-gmgn
python3 -m pytest \
  tests/test_sikk_live_run.py \
  tests/test_sikk_wallet_structure_daily_report.py \
  tests/test_sikk_runtime_v02.py \
  tests/test_sikk_wallet_structure_snapshot.py \
  tests/test_sikk_same_source_grouping.py \
  tests/test_sikk_wallet_structure_gate.py \
  tests/test_sikk_candidate_wallet_structure_pipeline.py \
  tests/test_sikk_state_wallet_structure_integration.py \
  tests/test_sikk_orchestrator_wallet_structure_integration.py \
  tests/test_sikk_paper_wallet_structure_integration.py \
  tests/test_sikk_candidate_state_machine.py \
  tests/test_run_sikk_gmgn_pipeline.py \
  tests/test_sikk_paper_live_runner.py \
  tests/test_sikk_candidate_quote_security_pipeline.py -q

编译检查

cd /root/sikk-gmgn
python3 -m py_compile \
  sikk_live_run.py \
  sikk_wallet_structure_daily_report.py \
  sikk_module_runner.py \
  sikk_trace_logger.py \
  sikk_token_skip_policy.py \
  sikk_dashboard_builder.py \
  sikk_notifier.py \
  sikk_live_orchestrator.py \
  sikk_wallet_structure_snapshot.py \
  sikk_same_source_grouping.py \
  sikk_wallet_structure_gate.py \
  sikk_candidate_wallet_structure_pipeline.py \
  sikk_candidate_state_machine.py \
  run_sikk_gmgn_pipeline.py \
  sikk_paper_live_runner.py \
  sikk_candidate_quote_security_pipeline.py

禁止真实交易路径检查

cd /root/sikk-gmgn
grep -R "gmgn-cli swap\|gmgn-cli multi-swap\|order strategy create\|onchainos swap execute\|swap execute\|private key\|api key\|bot_token\|webhook_url" \
  sikk_*.py run_sikk_gmgn_pipeline.py tests/*.py | cat

---

当前最常用的3 条

如果你只记3 条，就是这三个：

1. 正常跑一轮

cd /root/sikk-gmgn
python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode once

2. 连续跑
（3/4）
cd /root/sikk-gmgn
python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode loop --interval-sec 600
3看面板
cd /root/sikk-gmgn
sed -n '1,220p' data/gmgn_candidates_live_run/live_board.md


---

## 片段 29 / stream_idx=4817 / len=10647


可以。现在可以进入：

# SIKK 专业面板优化阶段

但这个阶段不是做炫酷界面，而是把面板升级成：

```text
决策控制台
+ 风险解释台
+ 纸面验证台
+ 系统诊断台
```

它必须围绕你的系统策略服务：

> **判断筹码控制权是否还在结构侧，是否正在转移给对手盘，当前 token 是否允许进入纸面验证。**

---

# 一、当前阶段定位

现在阶段可以定义为：

```text
Phase B-0.5：专业可观测面板优化阶段
```

不是：

```text
自动实盘阶段
复杂 dashboard 阶段
纯 UI 美化阶段
```

而是：

```text
让系统输出更像专业交易控制台
让每个 token 的状态、风险、原因、下一步动作都一眼可见
```

---

# 二、专业面板必须服务 8 个核心问题

你的面板打开后，必须直接回答：

```text
1. 系统有没有正常运行？
2. 本轮发现了哪些 token？
3. 哪些 token 最值得看？
4. 哪些 token 被阻断，为什么？
5. 钱包结构是否接入完整？
6. 有没有进入 PAPER_READY / PAPER_OPEN？
7. 当前纸面仓位表现如何？
8. 下一步应该修系统，还是继续观察 token？
```

如果面板回答不了这些，就不专业。

---

# 三、建议面板结构：8 个区域

## 1. 系统运行状态区

放最上面。

显示：

```text
最近运行时间
运行状态
本轮 token 数
候选发现是否正常
钱包结构接入率
quote/security 是否正常
paper runner 是否正常
日报是否生成
```

示例：

```markdown
## 1. 系统状态

| 指标 | 状态 |
|---|---|
| 最近运行 | 2026-05-02 10:26 UTC |
| Runtime | 正常 |
| Telegram 广播 | 正常 |
| 候选发现 | 48 |
| 钱包结构接入率 | 7 / 48 |
| Paper Runner | 正常 |
| 当前开放仓位 | 2 |
| 今日日报 | 已生成 |
```

这里最关键的是：

```text
钱包结构接入率
```

因为这是你当前最大的短板。

---

## 2. 核心机会区

这里不要放全部 token，只放最值得看的。

进入条件：

```text
PAPER_OPEN
PAPER_READY
WALLET_SUPPORT
S3 / S4 信号
quote/security 通过
```

示例：

```markdown
## 2. 重点机会

| Token | 当前状态 | 信号 | 钱包结构 | Quote | Security | Paper | 下一步 |
|---|---|---|---|---|---|---|---|
| ABC | PAPER_OPEN | S3 | SUPPORT 72 | OK | OK | +8.2% | HOLD |
| DEF | PAPER_READY | S4 | SUPPORT 68 | OK | OK | 未开仓 | 等 paper runner |
```

如果没有机会，也要明确写：

```text
当前无 PAPER_READY / WALLET_SUPPORT token。
```

不要空白。

---

## 3. 钱包结构控制权区

这是你系统的核心特色。  
不要只显示 WALLET_BLOCK 数量，要显示结构状态分布。

```markdown
## 3. 钱包结构状态

| 状态 | 数量 | 解释 |
|---|---:|---|
| WALLET_SUPPORT | 0 | 结构侧仍有支持 |
| WALLET_PAUSE | 0 | 结构不清晰或风险偏高 |
| WALLET_BLOCK | 7 | 钱包结构阻断 |
| WALLET_NEUTRAL | 0 | 中性 |
| MISSING | 41 | 钱包结构未接入 |
```

还要加：

```markdown
### 钱包结构未接入原因

| 原因 | 数量 |
|---|---:|
| early_wallet_raw.csv missing | 28 |
| gmgn report missing | 8 |
| field mapping failed | 5 |
```

这能直接告诉你下一步修什么。

---

## 4. 阻断 / 暂停原因区

专业面板必须解释“为什么不入场”。

```markdown
## 4. 阻断 / 暂停原因

| Token | 状态 | 主原因 | 关键证据 | 下一步 |
|---|---|---|---|---|
| AAA | BLOCKED | 同源组同步卖出 | sync_sell_score=76 | 冷却后重检 |
| BBB | WATCHING | 钱包结构缺失 | early_wallet_raw.csv missing | 修 GMGN 钱包报告 |
| CCC | PAUSE | 对手盘压力偏高 | counterparty=58 | 等下一轮 delta |
```

这个区域比“最新事件”更重要。

---

## 5. 当前纸面仓位区

这是判断系统有没有价值的核心。

```markdown
## 5. 当前纸面仓位

| Token | 状态 | 入场价 | 当前价 | 浮盈 | 最大浮盈 | 最大回撤 | 钱包结构 | 动作 |
|---|---|---:|---:|---:|---:|---:|---|---|
| XXX | OPEN | 0.00012 | 0.00015 | +25% | +40% | -8% | HOLDING | HOLD |
| YYY | OPEN | 0.00008 | 0.00007 | -12% | +5% | -18% | WEAKENING | EXIT_MONITOR |
```

重点字段：

```text
unrealized_pnl_pct
max_floating_profit_pct
max_drawdown_pct
wallet_structure_status
failure_candidate
next_action
```

---

## 6. 未入场原因统计区

这一区是系统优化最有用的地方。

```markdown
## 6. 未入场原因 Top

| 原因 | 数量 |
|---|---:|
| wallet_structure_missing | 41 |
| wallet_block | 7 |
| signal_not_ready | 35 |
| quote_not_ready | 12 |
| security_not_ready | 3 |
| state_not_ready | 9 |
| paper_runner_not_called | 0 |
```

这能告诉你：

```text
现在是策略没机会？
还是模块没接入？
还是 quote/security 卡住？
还是 paper runner 没跑？
```

---

## 7. 纸面验证统计区

这一块不要只写胜率，要写样本是否足够。

```markdown
## 7. 纸面验证统计

| 指标 | 数值 |
|---|---:|
| 当前开放仓位 | 2 |
| 累计关闭仓位 | 3 |
| 胜率 | 100.00% |
| 平均收益 | 284.45% |
| 样本可信度 | 低 |
| 最低目标样本 | 20 个关闭仓位 |
```

这里要明确：

```text
3 个关闭仓位不能证明策略有效
```

所以面板上要加：

```text
样本可信度：低 / 中 / 高
```

建议规则：

| 关闭仓位数 | 样本可信度 |
|---:|---|
| 0-9 | 低 |
| 10-19 | 初步 |
| 20-49 | 可观察 |
| 50+ | 较可靠 |

---

## 8. 最新事件区

这个区域放最后，不要放最前面。

```markdown
## 8. 最新事件

| 时间 | 事件 | 说明 |
|---|---|---|
| 10:26:10 | LIVE_RUN_STARTED | 开始运行 |
| 10:26:10 | LIVE_RUN_FINISHED | 完成一轮 |
```

事件日志是追踪用，不是主要决策区。

---

# 四、Token 表格必须增加这些字段

专业面板的 token 表格建议统一字段：

```text
token_symbol
token_address
current_state
priority_level
signal_level
signal_gate
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
quote_gate
security_gate
paper_status
paper_pnl_pct
main_reason
next_action
last_update
```

---

# 五、排序规则必须专业化

不要按发现顺序展示。  
按决策优先级排序。

推荐排序：

```text
1. PAPER_OPEN
2. PAPER_READY
3. WALLET_SUPPORT
4. PAUSE
5. WATCHING
6. BLOCKED
7. MISSING
8. ERROR
```

同状态内再按：

```text
wallet_structure_score 高 → 低
counterparty_pressure_score 低 → 高
data_quality_score 高 → 低
```

这样你打开面板，最重要的 token 永远在上面。

---

# 六、增加 priority_level，不等于买入信号

建议新增一个展示用字段：

```text
priority_level
```

取值：

```text
P0_ACTIVE_POSITION
P1_PAPER_READY
P2_STRUCTURE_SUPPORT
P3_WATCHING
P4_PAUSE
P5_BLOCKED
P6_DATA_MISSING
```

解释：

| 等级 | 含义 |
|---|---|
| P0 | 已有纸面仓位，必须跟踪 |
| P1 | 已准备进入纸面 |
| P2 | 钱包结构支持，但其他门禁未全过 |
| P3 | 普通观察 |
| P4 | 暂停 |
| P5 | 阻断 |
| P6 | 数据缺失 |

注意：

```text
priority_level 只是面板排序，不是买入信号。
```

---

# 七、Next Action 必须标准化

专业面板要有“下一步动作”。

建议枚举：

```text
HOLD
WAIT_SIGNAL
WAIT_WALLET
WAIT_QUOTE
WAIT_SECURITY
READY_FOR_PAPER
OPEN_PAPER_POSITION
EXIT_MONITOR
FORCE_PAPER_EXIT
COOLING
FIX_DATA_SOURCE
IGNORE
```

示例：

| 状态 | next_action |
|---|---|
| PAPER_OPEN | HOLD / EXIT_MONITOR |
| PAPER_READY | OPEN_PAPER_POSITION |
| WALLET_SUPPORT 但 signal 未过 | WAIT_SIGNAL |
| wallet missing | FIX_DATA_SOURCE |
| WALLET_BLOCK | COOLING |
| quote 失败 | WAIT_QUOTE |
| security 失败 | WAIT_SECURITY |

---

# 八、颜色规则

如果有 HTML 面板，颜色不要花。只用 5 类。

| 状态 | 颜色 |
|---|---|
| PAPER_OPEN / PAPER_READY | 绿色 |
| WALLET_SUPPORT | 蓝绿色 |
| WATCHING / PAUSE | 黄色 |
| BLOCKED / WALLET_BLOCK | 红色 |
| MISSING / DATA_QUALITY_LOW | 灰色 |

这就够了。

---

# 九、专业面板的核心输出文件

当前不需要复杂数据库。  
只需要把这些文件做清楚：

```text
live_board.md
live_dashboard.html
tokens/<token>/token_status.md
paper_live/daily_reports/paper_daily_report_YYYYMMDD.md
reports/wallet_structure_daily_report_YYYYMMDD.md
events/live_events.jsonl
```

其中最重要的是：

```text
live_board.md
token_status.md
daily_report.md
```

---

# 十、建议新的 `live_board.md` 完整模板

```markdown
# SIKK-SOL Live Board

更新时间：{{time}}  
运行状态：{{runtime_status}}  
边界：只做候选发现、结构分析、quote/security、纸面交易和复盘，不执行真实 swap。

---

## 1. 系统总览

| 指标 | 数值 |
|---|---:|
| 本轮 Token 数 | {{token_count}} |
| WATCHING | {{watching_count}} |
| PAUSE | {{pause_count}} |
| BLOCKED | {{blocked_count}} |
| PAPER_READY | {{paper_ready_count}} |
| PAPER_OPEN | {{paper_open_count}} |
| 钱包结构接入率 | {{wallet_coverage}} |
| 当前开放仓位 | {{open_positions}} |
| 今日关闭仓位 | {{closed_positions_today}} |
| 已关闭胜率 | {{win_rate}} |
| 平均收益 | {{avg_pnl}} |
| 样本可信度 | {{sample_confidence}} |

---

## 2. 重点机会

| Token | Priority | State | Signal | Wallet | Quote | Security | Paper | PnL | Next |
|---|---|---|---|---|---|---|---|---:|---|
{{opportunity_rows}}

---

## 3. 钱包结构状态

| 状态 | 数量 |
|---|---:|
| WALLET_SUPPORT | {{wallet_support_count}} |
| WALLET_PAUSE | {{wallet_pause_count}} |
| WALLET_BLOCK | {{wallet_block_count}} |
| WALLET_NEUTRAL | {{wallet_neutral_count}} |
| MISSING | {{wallet_missing_count}} |

### 钱包结构未接入原因

| 原因 | 数量 |
|---|---:|
{{wallet_missing_reason_rows}}

---

## 4. 阻断 / 暂停原因

| Token | State | 主原因 | 关键证据 | Next |
|---|---|---|---|---|
{{blocked_pause_rows}}

---

## 5. 当前纸面仓位

| Token | 状态 | 入场价 | 当前价 | 浮盈 | 最大浮盈 | 最大回撤 | 钱包状态 | 动作 |
|---|---|---:|---:|---:|---:|---:|---|---|
{{paper_position_rows}}

---

## 6. 未入场原因 Top

| 原因 | 数量 |
|---|---:|
{{entry_block_reason_rows}}

---

## 7. 今日纸面验证

| 指标 | 数值 |
|---|---:|
| 新增纸面入场 | {{new_entries}} |
| 纸面退出 | {{paper_exits}} |
| 当前开放仓位 | {{open_positions}} |
| 累计关闭仓位 | {{total_closed}} |
| 已关闭胜率 | {{closed_win_rate}} |
| 已关闭平均收益 | {{closed_avg_pnl}} |
| 最大回撤 | {{max_drawdown}} |

---

## 8. 最新事件

| 时间 | 事件 | 说明 |
|---|---|---|
{{event_rows}}
```

---

# 十一、系统策略对应的面板字段

根据你的 SIKK 策略，面板必须覆盖这些维度：

## 1. 筹码控制权

字段：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
dominant_side_status
chip_transfer_status
```

目的：

```text
判断结构侧是否仍在
```

---

## 2. 对手盘压力

字段：

```text
counterparty_pressure_score
late_large_buyer_count
bagholder_whale_count
early_wallet_sold_pct_delta
```

目的：

```text
判断是否正在成为退出流动性
```

---

## 3. 数据质量

字段：

```text
data_quality_score
wallet_missing_reason
wallet_coverage_rate
```

目的：

```text
判断这次分析可信不可信
```

---

## 4. K线结构

字段：

```text
signal_level
signal_type
signal_gate
invalid_level
```

目的：

```text
判断有没有可交易结构
```

---

## 5. 成交可执行性

字段：

```text
quote_gate
price_deviation_pct
security_gate
liquidity
```

目的：

```text
判断能不能按合理价格纸面模拟
```

---

## 6. 纸面验证

字段：

```text
paper_status
entry_price
current_price
unrealized_pnl_pct
max_floating_profit_pct
max_drawdown_pct
failure_type
```

目的：

```text
判断系统规则是否有效
```

---

# 十二、不要做成什么样

不要做成：

```text
一大堆日志
一大堆 token 平铺
只显示 WATCHING / BLOCKED
没有原因
没有下一步动作
没有优先级
没有未入场原因统计
```

那种面板看起来像系统在跑，但没有决策价值。

---

# 十三、当前最应该实施的面板改造

优先级：

```text
P0：
1. live_board.md 分区
2. token 排序
3. Reason 不允许为空
4. Next Action 标准化
5. 未入场原因 Top
6. 钱包结构接入率

P1：
7. HTML 搜索
8. 状态筛选
9. 颜色标记
10. 纸面仓位区优化

P2：
11. PnL 曲线
12. 失败原因图表
13. 多日趋势
14. Telegram 高级播报
```

现在只做 P0 + 少量 P1。

---

# 十四、直接给 Codex / OpenClaw 的面板优化指令

```text
任务：优化 SIKK-SOL 专业面板，不新增无关功能，不删除已有功能。

目标：
把当前 live_board.md / live_dashboard.html 从“运行日志型面板”改成“专业决策控制台”。

系统策略：
SIKK-SOL 是筹码控制权状态机，不是简单价格机器人。面板必须突出：
- 钱包结构状态
- 筹码控制权
- 对手盘压力
- K线信号
- quote/security
- 纸面仓位
- 未入场原因
- 下一步动作

一、live_board.md 必须改成 8 个分区：
1. 系统总览
2. 重点机会
3. 钱包结构状态
4. 阻断 / 暂停原因
5. 当前纸面仓位
6. 未入场原因 Top
7. 今日纸面验证
8. 最新事件

二、Token 表格必须包含字段：
- token_symbol
- current_state
- priority_level
- signal_level
- signal_gate
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

三、排序规则：
1. PAPER_OPEN
2. PAPER_READY
3. WALLET_SUPPORT
4. PAUSE
5. WATCHING
6. BLOCKED
7. MISSING
8. ERROR

四、Reason 规则：
- Reason 不允许为空。
- WATCHING 必须显示 watching_reason。
- BLOCKED 必须显示 block reason。
- MISSING 必须显示 missing reason。
- PAUSE 必须显示 pause reason。

五、Next Action 标准化：
允许值：
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

六、未入场原因统计：
必须统计：
- wallet_structure_missing
- wallet_block
- signal_not_ready
- quote_not_ready
- security_not_ready
- paper_runner_not_called
- state_not_ready

七、钱包结构接入率：
必须显示：
wallet_structure_decision.json 覆盖数量 / candidate 数量。
如果有 MISSING，必须统计 MISSING 原因。

八、HTML 面板只做轻量优化：
- 顶部状态卡片
- 状态颜色
- Token 搜索
- State 筛选
- Wallet 筛选
不要新增复杂图表，不要新建数据库，不要改实盘逻辑。

验收：
打开 live_board.md 后，必须一眼看到：
1. 系统是否正常
2. 当前有没有机会
3. 为什么没有 paper entry
4. 哪些 token 被钱包结构阻断
5. 钱包结构未接入原因
6. 当前 paper 仓位盈亏
7. 下一步该修数据、等信号，还是继续观察
```

---

# 结论

你现在进入的是：

> **专业面板优化阶段，但不是复杂 UI 阶段。**

核心不是“做得漂亮”，而是让它具备专业系统的决策表达能力：

```text
状态清楚
优先级清楚
风险清楚
原因清楚
下一步动作清楚
```

面板优化完成后，你才能真正用它来观察：

```text
SIKK 钱包结构门禁到底有没有用
哪些 token 被正确拦截
为什么没有新增纸面入场
哪些模块还在拖后腿
当前纸面仓位是否值得继续验证
```


---

## 片段 30 / stream_idx=4937 / len=5453


对，这个感觉是正常的。  
现在你的面板更像是：

```text
运行日志 + 数据堆叠
```

还不是专业系统那种：

```text
决策看板 + 状态总览 + 风险解释 + 下一步动作
```

现在不要做复杂 dashboard，但需要把现有面板重新排版成“交易系统控制台”。

---

# 一、专业面板的核心不是好看，而是清楚回答 5 个问题

你的面板必须一眼回答：

```text
1. 现在系统有没有正常跑？
2. 今天发现了哪些 token？
3. 哪些 token 值得看？
4. 为什么没入场？
5. 当前纸面仓位表现如何？
```

如果面板不能回答这 5 个问题，就算做成网页也不专业。

---

# 二、你现在面板不清晰的原因

大概率是这几个问题：

## 1. 状态太散

现在可能只显示：

```text
WATCHING
BLOCKED
WALLET_BLOCK
未接入
```

但没有告诉你：

```text
为什么 WATCHING？
下一步看什么？
哪个 token 更重要？
```

---

## 2. 没有优先级

48 个 token 全部堆在一起，视觉上会很乱。

应该分成：

```text
重点机会
观察中
已阻断
数据异常
纸面持仓
```

而不是一张大表全塞进去。

---

## 3. 没有“下一步动作”

专业面板一定要有：

```text
Next Action
```

例如：

```text
等待回踩
等待钱包结构接入
quote 过期，需刷新
security 未通过
纸面持仓继续观察
```

---

## 4. 缺少风险解释

只显示：

```text
WALLET_BLOCK
```

不够。

应该显示：

```text
WALLET_BLOCK｜同源组同步卖出 76｜早期钱包剩余 12%
```

---

## 5. 缺少分区

专业面板一定有分区：

```text
系统状态
机会池
阻断池
纸面仓位
风险事件
日报统计
```

---

# 三、建议改成 5 块面板

不要复杂化。就改成这 5 块。

---

## 1. 顶部总览卡片

```text
SIKK Live Board

更新时间：2026-05-02 10:26 UTC
运行状态：正常
本轮 token：48
BLOCKED：9
WATCHING：39
PAPER_READY：0
PAPER_OPEN：2
今日关闭胜率：100%
平均收益：284.45%
```

这个是系统健康状态。

---

## 2. 重点机会区

只显示最值得看的 token。

条件：

```text
WALLET_SUPPORT
PAPER_READY
PAPER_OPEN
S3 / S4 信号
quote/security 通过
```

表格：

| Token | 状态 | 信号 | 钱包结构 | Quote | Security | Paper | 下一步 |
|---|---|---|---|---|---|---|---|
| ABC | PAPER_OPEN | S3 | SUPPORT 72 | OK | OK | +8.2% | 继续观察 |
| DEF | PAPER_READY | S4 | SUPPORT 68 | OK | OK | 未开仓 | 等待 paper runner |

---

## 3. 阻断 / 暂停原因区

这里专门解释为什么没有入场。

| Token | 状态 | 主要阻断原因 | 细节 | 下一步 |
|---|---|---|---|---|
| AAA | BLOCKED | 钱包结构阻断 | 同源组同步卖出 74 | 6h 后重检 |
| BBB | WATCHING | 钱包结构缺失 | early_wallet_raw.csv missing | 修 GMGN 报告 |
| CCC | PAUSE | 对手盘压力偏高 | counterparty_pressure=58 | 等下一轮 delta |

---

## 4. 纸面仓位区

这个你每天必须看。

| Token | 状态 | 入场价 | 当前价 | 浮盈 | 最大浮盈 | 最大回撤 | 钱包状态 | 动作 |
|---|---|---:|---:|---:|---:|---:|---|---|
| XXX | OPEN | 0.00012 | 0.00015 | +25% | +40% | -8% | HOLDING | HOLD |
| YYY | OPEN | 0.00008 | 0.00007 | -12% | +5% | -18% | WEAKENING | EXIT_MONITOR |

---

## 5. 未入场原因统计

这一块最实用。

```text
本轮未入场原因 Top

wallet_structure_missing：41
wallet_block：7
signal_not_ready：35
quote_not_ready：12
security_not_ready：3
paper_runner_not_called：0
```

这会直接告诉你下一步修哪里。

---

# 四、推荐新的 `live_board.md` 模板

你可以让系统把 `live_board.md` 改成这个结构：

```markdown
# SIKK-SOL Live Board

更新时间：2026-05-02 10:26 UTC  
运行状态：正常  
边界：只做候选发现、结构分析、quote/security、纸面交易和复盘，不执行真实 swap。

---

## 1. 系统总览

| 指标 | 数值 |
|---|---:|
| 本轮 Token 数 | 48 |
| WATCHING | 39 |
| BLOCKED | 9 |
| PAPER_READY | 0 |
| PAPER_OPEN | 2 |
| 今日关闭仓位 | 3 |
| 已关闭胜率 | 100.00% |
| 已关闭平均收益 | 284.45% |

---

## 2. 钱包结构概览

| 钱包结构状态 | 数量 |
|---|---:|
| WALLET_SUPPORT | 0 |
| WALLET_PAUSE | 0 |
| WALLET_BLOCK | 7 |
| WALLET_NEUTRAL | 0 |
| MISSING / 未接入 | 41 |

---

## 3. 重点机会

| Token | 当前状态 | 信号 | 钱包结构 | Quote | Security | Paper | 下一步 |
|---|---|---|---|---|---|---|---|
| - | - | - | - | - | - | - | 当前无 PAPER_READY |

---

## 4. 当前纸面仓位

| Token | 状态 | 入场价 | 当前价 | 浮盈 | 最大浮盈 | 最大回撤 | 钱包结构 | 动作 |
|---|---|---:|---:|---:|---:|---:|---|---|
| XXX | OPEN | - | - | - | - | - | - | HOLD |
| YYY | OPEN | - | - | - | - | - | - | HOLD |

---

## 5. 阻断 / 暂停原因

| Token | 状态 | 主原因 | 细节 | 下一步 |
|---|---|---|---|---|
| AAA | BLOCKED | WALLET_BLOCK | 同源组同步卖出 / 早期钱包退出 | 冷却后重检 |
| BBB | WATCHING | wallet_structure_missing | early_wallet_raw.csv missing | 修钱包报告接入 |

---

## 6. 未入场原因统计

| 原因 | 数量 |
|---|---:|
| wallet_structure_missing | 41 |
| wallet_block | 7 |
| signal_not_ready | - |
| quote_not_ready | - |
| security_not_ready | - |

---

## 7. 最新事件

| 时间 | 事件 | 说明 |
|---|---|---|
| 10:26:10 | LIVE_RUN_STARTED | 开始运行 |
| 10:26:10 | LIVE_RUN_FINISHED | 完成一轮 |
```

---

# 五、如果保留 HTML 面板，也只做轻量专业化

现在 HTML 不要做复杂功能。  
只加 4 个实用点：

```text
1. 顶部卡片
2. 状态颜色
3. Token 搜索
4. 状态筛选
```

颜色建议：

| 状态 | 颜色含义 |
|---|---|
| PAPER_OPEN / PAPER_READY | 绿色 |
| WATCHING / PAUSE | 黄色 |
| BLOCKED / ERROR | 红色 |
| MISSING | 灰色 |
| WALLET_SUPPORT | 绿色 |
| WALLET_BLOCK | 红色 |

---

# 六、最应该改的不是样式，而是“排序”

专业面板一定要排序。

推荐排序：

```text
1. PAPER_OPEN
2. PAPER_READY
3. WALLET_SUPPORT
4. PAUSE
5. WATCHING
6. BLOCKED
7. MISSING
```

这样你打开面板先看到有价值的 token，而不是被 48 个候选淹没。

---

# 七、下一步修复重点

当前面板专业化不要扩展功能，只改这 4 件事：

```text
1. live_board.md 分区
2. Token 表格增加 Reason / Next Action
3. 按状态优先级排序
4. 增加未入场原因 Top
```

这就会清楚很多。

---

# 八、直接发给 Codex / OpenClaw 的修改指令

```text
当前 live_board.md / live_dashboard.html 不够清晰。不要新增复杂功能，不要做大型 dashboard，不要接新机器人。

只优化现有面板的专业可读性。

要求：

1. live_board.md 改成分区结构：
- 系统总览
- 钱包结构概览
- 重点机会
- 当前纸面仓位
- 阻断 / 暂停原因
- 未入场原因统计
- 最新事件

2. Token 表格必须包含：
- token_symbol
- current_state
- signal_gate
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- quote_gate
- security_gate
- paper_status
- pnl
- reason
- next_action

3. 排序规则：
- PAPER_OPEN 第一
- PAPER_READY 第二
- WALLET_SUPPORT 第三
- PAUSE 第四
- WATCHING 第五
- BLOCKED 第六
- MISSING 最后

4. Reason 不能空。
如果 WATCHING，必须显示 watching_reason。
如果 MISSING，必须显示 missing reason。
如果 BLOCKED，必须显示 block reason。

5. 增加未入场原因统计：
- wallet_structure_missing
- wallet_block
- signal_not_ready
- quote_not_ready
- security_not_ready
- paper_runner_not_called
- state_not_ready

6. live_dashboard.html 只做轻量优化：
- 顶部状态卡片
- 搜索框
- 状态筛选
- 钱包状态筛选
- 状态颜色标记

不要新增复杂图表，不要新建数据库，不要改实盘逻辑。
```

---

# 结论

你现在感觉“不专业”，不是因为缺复杂功能，而是因为缺：

```text
分区
优先级
原因解释
下一步动作
视觉状态
```

先把 `live_board.md` 改成专业决策看板。  
它应该让你一眼知道：

```text
现在有没有机会？
为什么没入场？
哪个 token 最值得看？
哪个模块卡住了？
纸面仓位表现如何？
```

这才是当前最实用的面板升级。


---

## 片段 31 / stream_idx=5116 / len=13948


要修复，先不要动新功能。只修这条链路：

```text
候选 token
→ 单币钱包报告
→ early_wallet_raw.csv
→ wallet_structure_decision.json
→ token_status.md
→ live_board.md
→ paper entry reason
```

你现在的问题主要是：

```text
48 个 token 里 41 个 wallet_structure 未接入
```

所以第一目标不是让它马上多开 paper，而是让每个 token 至少有一个明确钱包结构结果：

```text
WALLET_SUPPORT / WALLET_PAUSE / WALLET_BLOCK / WALLET_NEUTRAL / MISSING
```

---

# 一、先定位到底卡在哪一步

先在项目根目录执行：

```bash
ls data/gmgn_candidates_live_run
```

看有没有这些目录：

```text
candidates.json
wallet_structure/
tokens/
live_board.md
paper_live/
reports/
```

然后检查候选数量：

```bash
python - <<'PY'
import json
from pathlib import Path

p = Path("data/gmgn_candidates_live_run/candidates.json")
data = json.loads(p.read_text(encoding="utf-8"))

if isinstance(data, dict):
    rows = data.get("candidates", [])
else:
    rows = data

print("candidates:", len(rows))
for r in rows[:10]:
    print(r.get("token_symbol") or r.get("symbol"), r.get("token_address") or r.get("address") or r.get("mint"))
PY
```

再检查哪些 token 没有钱包结构决策文件：

```bash
python - <<'PY'
import json
from pathlib import Path

base = Path("data/gmgn_candidates_live_run")
p = base / "candidates.json"
data = json.loads(p.read_text(encoding="utf-8"))

rows = data.get("candidates", data) if isinstance(data, dict) else data

missing = []
ok = []

for r in rows:
    token=[REDACTED] or r.get("address") or r.get("mint")
    symbol = r.get("token_symbol") or r.get("symbol") or "UNKNOWN"
    decision = base / "wallet_structure" / token / "wallet_structure_decision.json"

    if decision.exists():
        ok.append((symbol, token))
    else:
        missing.append((symbol, token))

print("wallet_structure ok:", len(ok))
print("wallet_structure missing:", len(missing))
print("\nMissing examples:")
for x in missing[:30]:
    print(x)
PY
```

这一步先确认：

```text
是文件没生成
还是路径不一致
还是 token_address 字段不一致
```

---

# 二、最常见原因和对应修法

## 原因 1：路径不一致

你的模块可能输出到了：

```text
data/gmgn_candidates_live_run/wallet_structure/<token>/
```

但 Runtime 读取的是：

```text
data/gmgn_candidates_live_run/wallet_structures/<token>/
```

或输出到了旧目录：

```text
data/gmgn_reports/
data/reports/
data/gmgn_token_reports/
```

修法：

统一只读写这里：

```text
data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json
```

所有模块都用这个目录。

---

## 原因 2：字段名不一致

候选里可能是：

```text
address
mint
ca
token
```

但钱包结构模块只认：

```text
token_address
```

修法：在候选加载时统一字段。

加入一个函数：

```python
def normalize_token(row):
    return {
        "token_address": row.get("token_address") or row.get("address") or row.get("mint") or row.get("ca") or row.get("token"),
        "token_symbol": row.get("token_symbol") or row.get("symbol") or row.get("ticker") or "UNKNOWN",
        "raw": row,
    }
```

只要 `token_address` 为空，这个 token 就不能进入钱包结构分析。

---

## 原因 3：`sikk_gmgn_token_report.py` 没有被调用

钱包结构模块需要先有：

```text
early_wallet_raw.csv
```

如果没有，就会无法生成：

```text
wallet_structure_decision.json
```

修法：

在钱包结构 pipeline 里增加 fallback：

```text
如果 early_wallet_raw.csv 不存在
→ 尝试调用 sikk_gmgn_token_report.py
→ 再读取 early_wallet_raw.csv
→ 仍失败则写 MISSING decision
```

---

## 原因 4：没有写 MISSING 结果

现在很多 token 显示“未接入”，但你不知道原因。  
这是不合格的。

修法：

即使钱包数据失败，也必须生成：

```text
wallet_structure_decision.json
```

内容是：

```json
{
  "wallet_structure_status": "MISSING",
  "decision_action": "PAUSE",
  "reason": "early_wallet_raw.csv missing",
  "data_quality_score": 0
}
```

这样 live_board 才能显示原因。

---

# 三、最实用修复：先加 MISSING fallback

这是最应该先改的。  
即使钱包结构没跑通，也要让系统“说清楚为什么没跑通”。

在钱包结构 pipeline 里加这个函数：

```python
from pathlib import Path
import json
from datetime import datetime, timezone

def write_missing_wallet_decision(token_address, token_symbol, reason, base_dir="data/gmgn_candidates_live_run"):
    out_dir = Path(base_dir) / "wallet_structure" / token_address
    out_dir.mkdir(parents=True, exist_ok=True)

    data = {
        "token_address": token_address,
        "token_symbol": token_symbol,
        "module": "wallet_structure",
        "status": "MISSING",
        "gate": "PAUSE",
        "wallet_structure_status": "MISSING",
        "wallet_structure_score": 0,
        "wallet_risk_score": 0,
        "counterparty_pressure_score": 0,
        "data_quality_score": 0,
        "wallet_structure_factor": 0.0,
        "decision_action": "PAUSE",
        "reason": reason,
        "support_signals": [],
        "risk_signals": ["WALLET_STRUCTURE_MISSING"],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "stale_after_sec": 600,
        "metrics": {}
    }

    path = out_dir / "wallet_structure_decision.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path
```

然后在处理单个 token 时这样用：

```python
try:
    # 原来的钱包结构分析逻辑
    process_wallet_structure_for_token(token)

except FileNotFoundError as e:
    write_missing_wallet_decision(
        token_address=token_address,
        token_symbol=token_symbol,
        reason=f"wallet input missing: {e}",
    )

except Exception as e:
    write_missing_wallet_decision(
        token_address=token_address,
        token_symbol=token_symbol,
        reason=f"wallet pipeline error: {e}",
    )
```

这样下一轮广播不会只说“未接入 41”，而是能说：

```text
未接入原因：
- early_wallet_raw.csv missing: 28
- gmgn token report missing: 8
- field mapping failed: 5
```

---

# 四、修 wallet_structure pipeline 的读取逻辑

钱包结构 pipeline 应该按这个顺序找数据：

```text
1. wallet_structure/<token>/early_wallet_raw.csv
2. wallet_structure/<token>/wallet_classification.csv
3. sikk_gmgn_token_report.py 输出目录
4. 自动调用 sikk_gmgn_token_report.py
5. 失败则写 MISSING decision
```

建议函数：

```python
from pathlib import Path
import csv
import subprocess

BASE_DIR = Path("data/gmgn_candidates_live_run")

def read_csv(path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def find_wallet_input(token_address):
    candidates = [
        BASE_DIR / "wallet_structure" / token_address / "early_wallet_raw.csv",
        BASE_DIR / "wallet_structure" / token_address / "wallet_classification.csv",
        Path("data/gmgn_token_reports") / token_address / "early_wallet_raw.csv",
        Path("data/gmgn_reports") / token_address / "early_wallet_raw.csv",
    ]

    for p in candidates:
        if p.exists():
            return p

    return None

def load_or_generate_wallet_rows(token_address, token_symbol):
    path = find_wallet_input(token_address)

    if path:
        return read_csv(path)

    # 尝试调用单币报告
    script = Path("sikk_gmgn_token_report.py")
    if script.exists():
        out_dir = BASE_DIR / "wallet_structure" / token_address
        out_dir.mkdir(parents=True, exist_ok=True)

        subprocess.run([
            "python",
            str(script),
            "--token", token_address,
            "--symbol", token_symbol,
            "--output-dir", str(out_dir),
        ], check=True)

        path = find_wallet_input(token_address)
        if path:
            return read_csv(path)

    raise FileNotFoundError("early_wallet_raw.csv not found and token report generation failed")
```

---

# 五、修 `token_status.md`：必须显示未接入原因

现在 live_board 只显示数量，不够。

`token_status.json` 里必须有：

```json
{
  "wallet_structure": {
    "wallet_structure_status": "MISSING",
    "reason": "early_wallet_raw.csv missing"
  },
  "watching_reason": [
    "wallet_structure_missing",
    "signal_not_ready",
    "quote_not_run"
  ]
}
```

状态合并逻辑应该是：

```python
def build_watching_reasons(signal, wallet, quote, security, paper):
    reasons = []

    if wallet.get("wallet_structure_status") in {"MISSING", None}:
        reasons.append("wallet_structure_missing")

    if signal.get("signal_gate") not in {"ALLOW"}:
        reasons.append(f"signal_not_ready:{signal.get('signal_gate', 'MISSING')}")

    if quote.get("quote_gate") not in {"ALLOW"}:
        reasons.append(f"quote_not_ready:{quote.get('quote_gate', 'MISSING')}")

    if security.get("security_gate") not in {"ALLOW"}:
        reasons.append(f"security_not_ready:{security.get('security_gate', 'MISSING')}")

    if paper.get("paper_status") in {None, "", "NONE"}:
        reasons.append("paper_not_open")

    return reasons
```

然后 `token_status.md` 输出：

```markdown
## 当前未入场原因

- wallet_structure_missing
- signal_not_ready:MISSING
- quote_not_ready:MISSING
- security_not_ready:MISSING
```

---

# 六、修 `live_board.md`：Reason 不能空

live_board 表格增加这些列：

```text
Token | State | Wallet | Signal | Quote | Security | Paper | Reason
```

如果 Wallet 是 MISSING，就显示：

```text
wallet_structure missing: early_wallet_raw.csv not found
```

不要只显示：

```text
WATCHING
```

因为 WATCHING 没有意义，必须知道为什么 WATCHING。

---

# 七、修 daily_report：增加未入场原因统计

现在新增 paper entry = 0，但不知道原因。  
日报必须统计：

```text
PAPER_ENTRY_BLOCKED_REASON_TOP
```

实现逻辑：

```python
from collections import Counter
import json
from pathlib import Path

def collect_blocked_reasons():
    base = Path("data/gmgn_candidates_live_run/tokens")
    counter = Counter()

    for status_path in base.glob("*/token_status.json"):
        data = json.loads(status_path.read_text(encoding="utf-8"))

        state = data.get("current_state")
        if state in {"PAPER_OPEN", "PAPER_READY"}:
            continue

        reasons = data.get("watching_reason") or []

        if not reasons:
            latest_reason = data.get("latest_reason") or "unknown"
            counter[latest_reason] += 1
        else:
            for r in reasons:
                counter[r] += 1

    return counter
```

日报输出：

```markdown
## 未入场原因 Top

- wallet_structure_missing: 41
- wallet_block: 7
- signal_not_ready: 39
- quote_not_ready: 39
- security_not_ready: 39
```

这样你就能知道下一步修哪里。

---

# 八、修复顺序

按这个顺序来，不要乱改。

## 第 1 步：先让所有 token 都有 wallet decision

目标：

```text
没有 wallet_structure_decision.json 的 token=[REDACTED]
```

即使失败也生成 MISSING。

验收命令：

```bash
python - <<'PY'
import json
from pathlib import Path

base = Path("data/gmgn_candidates_live_run")
data = json.loads((base / "candidates.json").read_text(encoding="utf-8"))
rows = data.get("candidates", data) if isinstance(data, dict) else data

missing = []
for r in rows:
    token=[REDACTED] or r.get("address") or r.get("mint")
    p = base / "wallet_structure" / token / "wallet_structure_decision.json"
    if not p.exists():
        missing.append(token)

print("missing decision:", len(missing))
for x in missing[:20]:
    print(x)
PY
```

目标结果：

```text
missing decision: 0
```

---

## 第 2 步：统计 MISSING 原因

```bash
python - <<'PY'
import json
from pathlib import Path
from collections import Counter

base = Path("data/gmgn_candidates_live_run/wallet_structure")
counter = Counter()

for p in base.glob("*/wallet_structure_decision.json"):
    d = json.loads(p.read_text(encoding="utf-8"))
    status = d.get("wallet_structure_status")
    if status == "MISSING":
        counter[d.get("reason", "unknown")] += 1

print(counter)
PY
```

这会告诉你真实问题。

---

## 第 3 步：修最高频的 MISSING 原因

如果最高频是：

```text
early_wallet_raw.csv missing
```

就修 `sikk_gmgn_token_report.py` 调用。

如果是：

```text
field mapping failed
```

就修字段映射。

如果是：

```text
gmgn token report generation failed
```

就修 GMGN 数据抓取。

如果是：

```text
token_address missing
```

就修 candidates.json 字段标准化。

---

## 第 4 步：让 WATCHING 有原因

检查：

```bash
grep -R "watching_reason" data/gmgn_candidates_live_run/tokens | head
```

如果没有，就说明 `token_status` 还没补好。

---

## 第 5 步：日报增加未入场原因

检查：

```bash
grep -n "未入场原因" data/gmgn_candidates_live_run/paper_live/daily_reports/paper_daily_report_20260502.md
```

如果没有，就补 `PAPER_ENTRY_BLOCKED_REASON_TOP`。

---

# 九、下一轮广播应该变成什么样

修完后，Telegram 广播应该显示：

```text
钱包结构
- WALLET_BLOCK：7
- WALLET_SUPPORT：x
- WALLET_PAUSE：x
- WALLET_NEUTRAL：x
- MISSING：x

钱包结构未接入原因
- early_wallet_raw.csv missing：x
- field mapping failed：x
- gmgn report error：x

纸面交易
- 新增纸面入场数：0

未入场原因 Top
- wallet_structure_missing：x
- wallet_block：7
- signal_not_ready：x
- quote_not_ready：x
```

这个才是可操作的。

---

# 十、直接发给 Codex / OpenClaw 的修复指令

```text
当前 SIKK Live Run 已经能定时运行并 Telegram 广播，但 wallet_structure 未接入数量过高：48 个 token 中 41 个未接入。本次不要新增任何新功能，不要做 dashboard、机器人、实盘、confirmation ticket。只修复可用性。

目标：
1. 所有候选 token 都必须生成 wallet_structure_decision.json。
2. 即使钱包结构分析失败，也要生成 MISSING 类型的 wallet_structure_decision.json。
3. token_status.md 必须显示为什么 WATCHING / BLOCKED / PAUSE。
4. daily_report 必须统计为什么没有新增 paper entry。

具体修改：

一、在钱包结构 pipeline 中增加 fallback：
- 如果 early_wallet_raw.csv 不存在，尝试调用 sikk_gmgn_token_report.py。
- 如果仍失败，不要静默跳过，调用 write_missing_wallet_decision()。
- 输出路径统一：
  data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json

MISSING decision 格式：
{
  "token_address": "...",
  "token_symbol": "...",
  "module": "wallet_structure",
  "status": "MISSING",
  "gate": "PAUSE",
  "wallet_structure_status": "MISSING",
  "wallet_structure_score": 0,
  "wallet_risk_score": 0,
  "counterparty_pressure_score": 0,
  "data_quality_score": 0,
  "wallet_structure_factor": 0,
  "decision_action": "PAUSE",
  "reason": "具体失败原因",
  "risk_signals": ["WALLET_STRUCTURE_MISSING"]
}

二、修 token_status_builder：
- 读取 wallet_structure_decision.json。
- 如果缺失，wallet_structure_status = MISSING。
- 增加 watching_reason 数组。
- WATCHING token 必须显示：
  signal_gate
  wallet_structure_status
  quote_gate
  security_gate
  paper_gate
  watching_reason

三、修 live_board.md：
- Reason 字段必须显示真实原因。
- 不允许只显示 WATCHING。
- 如果 wallet MISSING，Reason 显示具体 missing 原因。

四、修 paper daily report：
增加 PAPER_ENTRY_BLOCKED_REASON_TOP。
统计：
- wallet_structure_missing
- wallet_block
- signal_not_ready
- quote_failed
- security_failed
- state_not_ready
- paper_runner_not_called

五、验收：
运行一轮后：
- candidates 数量 = 48 时，wallet_structure_decision.json 数量也应该接近 48。
- 没有成功分析的钱包结构必须显示 MISSING 和具体原因。
- live_board.md 能解释每个 token 为什么 WATCHING。
- daily_report.md 能解释新增 paper entry 为 0 的原因。
```

---

# 最短修复路线

现在最短路径就是：

```text
1. 所有 token 都写 wallet_structure_decision.json
2. 失败也写 MISSING
3. token_status 显示 watching_reason
4. live_board 显示具体原因
5. daily_report 统计未入场原因
```

先修这 5 个，系统就能从“会跑但看不懂”变成“会跑、能解释、能定位问题”。


---

## 片段 32 / stream_idx=5182 / len=5331


这条广播说明：**系统已经开始自己定时运行，并且 Telegram 播报已经接上了。**  
这一步已经比之前前进了一大截。

但从结果看，当前还不是“成熟纸面验证阶段”，而是：

# 当前阶段：Phase B-0｜连续运行已启动，但核心接入不完整

也就是：

```text
系统已经会跑、会播报、会生成看板和日报
但钱包结构层大面积未接入，纸面入场也没有新增
```

---

# 一、这轮结果怎么解读

## 1. 定时运行已经成功

这几项是好结果：

```text
状态：已完成最新一轮
输出目录：data/gmgn_candidates_live_run
最近事件有 LIVE_RUN_STARTED / LIVE_RUN_FINISHED
Telegram 广播正常
```

说明：

```text
Runtime / 定时任务 / 播报 / 报告路径 已经接通
```

这一层不用再扩展，先保持现状。

---

## 2. Token 数量正常

```text
令牌数量：48
已屏蔽：9
观看人数：39
```

这里的“观看人数”大概率是翻译问题，实际应该是：

```text
WATCHING：39
```

说明这轮发现了 48 个 token，其中：

```text
9 个被 BLOCK
39 个还在 WATCHING
```

目前没有进入 PAPER_READY 的新增 token。

---

## 3. 最大问题：钱包结构未接入太多

```text
WALLET_BLOCK：7
未接入：41
```

这是当前最关键的问题。

意思是：

```text
48 个 token 里，只有 7 个真正跑出了钱包结构阻断结果
剩下 41 个没有成功生成 / 读取 wallet_structure_decision.json
```

所以现在系统虽然在跑，但大部分 token 还没有真正经过你的核心优势：

```text
早期钱包
同源组
高结果钱包
分发钱包
对手盘压力
```

这说明下一步重点不是增加功能，而是修：

```text
钱包结构模块接入率
```

目标应该是：

```text
未接入 41 → 降到 0 或接近 0
```

至少先做到：

```text
48 个 token 里，80% 以上能生成 wallet_structure_decision.json
```

---

## 4. 纸面交易没有新增入场

```text
新增纸面入场数：0
纸面退出数：0
当前开放仓位数：2
累计关闭仓位数：3
```

这说明本轮没有新的 token 进入 paper。

可能原因有 4 个：

```text
1. 绝大多数 token 钱包结构未接入，无法进入 PAPER_READY
2. quote/security 没通过
3. K线信号没有达到 S3/S4
4. paper runner 入场条件过严或没有被正确调用
```

现在不要急着放宽规则。  
应该先查清楚：

```text
为什么 48 个 token 没有一个新增 paper entry？
```

需要在 live_board 或 token_status 里看到每个 token 的阻断原因。

---

## 5. 已关闭胜率 100%、平均收益 284.45% 不要过度相信

```text
累计关闭仓位数：3
已关闭胜率：100.00%
已关闭平均收益率：284.45%
```

这只是 3 个样本，不能说明策略已经有效。

现在只能说：

```text
纸面 runner 有历史关闭样本
但样本数太少，不能进入实盘判断
```

最低门槛仍然应该是：

```text
至少 100 个候选样本
至少 20 个关闭仓位
至少连续 3 天日报
live entry price 模式下仍然表现稳定
```

---

# 二、当前最重要的 3 个问题

## 问题 1：钱包结构未接入 41 个

这是最高优先级。

需要检查：

```text
data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json
```

为什么没有生成。

常见原因：

```text
1. sikk_gmgn_token_report.py 没有被调用
2. early_wallet_raw.csv 没有生成
3. pipeline 找不到 token 数据
4. wallet_structure_decision.json 路径不统一
5. 字段映射失败
6. GMGN 数据源没有返回
```

当前要修的是：

```text
candidate → wallet_structure_pipeline → wallet_structure_decision.json
```

这条链路。

---

## 问题 2：WATCHING 39 个没有解释

现在广播只说：

```text
WATCHING：39
```

但你真正需要知道：

```text
为什么 WATCHING？
是 K线不够？
是钱包未接入？
是 quote 失败？
是 security 暂停？
还是 paper runner 没开？
```

所以 `token_status.md` 里必须有：

```text
current_state: WATCHING
watching_reason:
  - signal_gate = WAIT
  - wallet_structure = MISSING
  - quote_gate = NOT_RUN
  - security_gate = NOT_RUN
```

否则你只能看到数量，看不到问题。

---

## 问题 3：paper 新增入场为 0

这不是坏事，但必须能解释。

日报应该新增一段：

```text
PAPER_READY 未入场原因统计：
- wallet_missing: 41
- wallet_block: 7
- signal_not_ready: x
- quote_failed: x
- security_failed: x
- paper_runner_not_called: x
```

这比单纯显示“新增纸面入场数 0”有用得多。

---

# 三、现在不要做什么

现在不要继续加：

```text
新 dashboard
新播报
新 confirmation ticket
新机器人
新实盘 gate
更复杂角色分类
```

因为当前真正堵点是：

```text
钱包结构接入率低
PAPER_READY 原因不可见
paper 入场为 0 的原因不可见
```

---

# 四、下一步最实用修复顺序

## P0-1：修钱包结构未接入

目标：

```text
WALLET 未接入 41 → 尽量降到 0
```

检查每个 token 是否生成：

```text
wallet_structure/<token>/wallet_structure_decision.json
```

如果没有，必须在 token_status 里写明：

```text
wallet_structure_status: MISSING
wallet_structure_reason: early_wallet_raw.csv not found / gmgn report missing / field mapping failed
```

---

## P0-2：给 WATCHING 加原因

`token_status.md` 必须显示：

```text
为什么还在 WATCHING
```

例如：

```text
WATCHING_REASON:
- signal_gate: WAIT_PULLBACK
- wallet_structure: MISSING
- quote_gate: NOT_RUN
- security_gate: NOT_RUN
```

---

## P0-3：给 paper 未入场加原因

日报里增加：

```text
未入场原因统计
```

例如：

```text
PAPER_READY / PAPER_ENTRY_BLOCKED 原因：
- wallet_structure_missing: 41
- wallet_block: 7
- signal_not_ready: 0
- quote_failed: 0
- security_failed: 0
```

---

# 五、当前状态判断

现在可以这样定性：

```text
SIKK Live Runtime 已经跑起来
Telegram 广播已接通
纸面统计已能输出
但钱包结构主能力还没有完全接入候选池
当前不能判断策略有效性
下一步重点是提高结构门禁覆盖率和入场原因可解释性
```

---

# 六、这轮广播的核心结论

```text
好消息：
系统已经会自动运行、会播报、会生成日报。

主要问题：
48 个 token 里 41 个钱包结构未接入。
本轮没有新增 paper entry。
现有 paper 收益样本太少，不能作为策略有效依据。

下一步：
不要加新功能。
先修 wallet_structure_decision.json 覆盖率。
再修 WATCHING / 未入场原因统计。
```

---

# 七、可以直接发给 Codex / OpenClaw 的修复指令

```text
当前 SIKK Live Run 已能定时运行并 Telegram 广播，但本轮 48 个 token 中 wallet_structure 未接入 41 个，新增 paper entry 为 0。

现在不要新增 dashboard、机器人、confirmation ticket 或实盘功能。

请只修三个实用问题：

1. 修复 wallet_structure 覆盖率
- 对每个候选 token 检查是否生成：
  data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json
- 如果没有生成，必须记录明确原因：
  early_wallet_raw.csv missing
  gmgn token report missing
  field mapping failed
  wallet pipeline error
  no wallet data
- token_status.json / token_status.md 必须显示 wallet_structure_status = MISSING 以及具体原因。

2. 增加 WATCHING 原因
- 每个 WATCHING token 必须写出为什么还在 WATCHING：
  signal_gate
  wallet_structure_status
  quote_gate
  security_gate
  paper_gate
  watching_reason
- live_board.md 中增加 Reason 字段，不允许只显示 WATCHING。

3. 增加 paper 未入场原因统计
- paper daily report 增加：
  PAPER_ENTRY_BLOCKED_REASON_TOP
- 统计：
  wallet_structure_missing
  wallet_block
  signal_not_ready
  quote_failed
  security_failed
  paper_runner_not_called
  state_not_ready
- 当前本轮新增 paper entry 为 0，必须能解释 0 的来源。

验收标准：
- 下一轮 Telegram 广播中，wallet_structure 未接入数量明显下降，或至少每个未接入 token 有明确原因。
- live_board.md 能看出每个 token 为什么 WATCHING / BLOCKED / PAUSE。
- daily_report.md 能解释为什么没有新增 paper entry。
```

---

# 当前一句话判断

> 系统已经开始运行了，但还没有进入真正有效的连续纸面验证；下一步要修“钱包结构覆盖率”和“未入场原因可解释性”。


---

## 片段 33 / stream_idx=5254 / len=947


定时任务响应：SIKK 直播运行 Telegram 广播
（job_id：48ad1770798d）
-------------

SIKK Live Run 广播
- 时间：2026-05-02T10:26:10Z
- 状态：已完成最新一轮
- 输出目录：data/gmgn_candidates_live_run
- 边界：只做候选发现、结构分析、quote/security、纸面交易和复盘，不执行真实swap。

状态概览
- 令牌数量：48
- 已屏蔽：9
观看人数：39

钱包结构
- WALLET_BLOCK：7
- 未接入：41

纸面交易
- 新增纸面入场数：0
- 纸面退出数：0
- 当前开放仓位数：2
- 累计关闭仓位数：3
- 已关闭胜率：100.00%
- 已关闭平均收益率：284.45%

最近事件
- 时间｜事件｜说明
- 2026-05-02T10:04:43Z｜LIVE_RUN_FINISHED｜SIKK 主入口完成一轮运行
- 2026-05-02T10:15:28Z｜LIVE_RUN_STARTED｜SIKK 主入口开始运行
- 2026-05-02T10:15:28Z｜LIVE_RUN_FINISHED｜SIKK 主入口完成一轮运行
- 2026-05-02T10:26:10Z｜LIVE_RUN_STARTED｜SIKK 主入口开始运行
- 2026-05-02T10:26:10Z｜LIVE_RUN_FINISHED｜SIKK 主入口完成一轮运行

文档
- 实时看板：data/gmgn_candidates_live_run/live_board.md
- 纸面日报：data/gmgn_candidates_live_run/paper_live/daily_reports/paper_daily_report_20260502.md
- 钱包结构日报：data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_20260502.md

要停止或管理此作业，请给我发送一条新消息（例如“停止 SIKK Live Run Telegram 广播提醒”）。


---

## 片段 34 / stream_idx=5347 / len=5342


对，既然之前添加的模块已经实现了，就**不要删除**。  
现在正确做法不是“砍掉”，而是：

> **保留已实现模块，但重新分层管理：核心闭环必须启用，辅助模块按需启用，扩展模块默认关闭。**

也就是说，不是回退系统，而是把系统整理成清晰的运行级别。

---

# 一、现在的判断修正

之前我说“不要做 dashboard / 播报 / confirmation ticket”，这个应该改成：

```text
如果还没做，就先不做；
如果已经做了，就不要删，改成可选模块。
```

现在系统应该理解为：

```text
核心运行闭环 + 已实现辅助能力 + 后续扩展能力
```

不是把已完成的东西推倒。

---

# 二、重新划分系统模块

## A 层：必须启用，不能缺

这些是系统真正能不能工作的核心：

```text
1. 候选发现
2. K线信号
3. 钱包结构门禁
4. quote / security
5. 状态机
6. paper runner
7. token_status
8. live_board
9. paper_positions
10. daily_report
```

这一层必须稳定。

---

## B 层：已经实现就保留，但作为辅助

这些如果已经做了，就保留：

```text
1. live_dashboard.html
2. process_trace.jsonl
3. events/live_events.jsonl
4. sikk_cli.py
5. module_runner
6. skip_policy
7. notifier
8. confirmation ticket
```

但它们不是当前判断系统成熟度的核心。

它们的定位是：

```text
提高可观测性
减少人工查看成本
辅助状态跟踪
辅助未来实盘确认
```

---

## C 层：暂时不继续扩展

这些先不继续追加：

```text
1. 更复杂 dashboard
2. 更复杂机器人播报
3. 多频道通知
4. 自动实盘 broadcast
5. 复杂权限系统
6. 复杂网页交互
7. 大型数据库面板
```

---

# 三、现在系统不是要删功能，而是要“收敛使用”

你现在应该把所有模块变成这种配置：

```json
{
  "core": {
    "candidate_discovery": true,
    "kline_signal": true,
    "wallet_structure_gate": true,
    "quote_gate": true,
    "security_gate": true,
    "paper_runner": true,
    "daily_report": true
  },
  "observability": {
    "live_board_md": true,
    "token_status_md": true,
    "process_trace": true,
    "live_dashboard_html": true,
    "cli": true
  },
  "notification": {
    "enabled": false,
    "discord": false,
    "telegram": false
  },
  "confirmation": {
    "enabled": false,
    "ticket_only": true,
    "broadcast_allowed": false
  }
}
```

这样做的好处是：

```text
已实现的不删除
但不让辅助模块干扰主流程
```

---

# 四、当前阶段重新定义

现在不是简单的“最小闭环未完成”。

更准确地说：

> **系统模块已经扩展到 Runtime 雏形，但核心纸面验证闭环还需要稳定化。**

也就是：

```text
架构：已经比较完整
问题：核心运行链路还没稳定跑出连续样本
重点：不是继续加模块，而是把已有模块串稳
```

---

# 五、现在应该检查什么

你现在要做的不是删模块，而是检查这 6 个关键问题。

## 1. 主入口是否稳定

必须确认：

```bash
python sikk_live_run.py
```

或：

```bash
python -m sikk.runtime.sikk_live_orchestrator --mode once
```

能不能跑完一轮。

如果两个入口都有，建议保留一个主入口：

```text
sikk_live_run.py
```

它内部调用 Runtime。

---

## 2. 模块输出是否能被统一读取

重点检查这些文件是否真实生成：

```text
signals/<token>/signal.json
wallet_structure/<token>/wallet_structure_decision.json
quotes/<token>/quote.json
security/<token>/security.json
paper_positions.csv
```

只要有一个模块输出格式不统一，系统就会“看不到 token 当前情况”。

---

## 3. token_status 是否能合并完整状态

每个 token 必须生成：

```text
tokens/<token>/token_status.json
tokens/<token>/token_status.md
```

里面必须能看到：

```text
K线结论
钱包结构结论
quote 结论
security 结论
paper 状态
最终状态
原因
```

---

## 4. live_board 是否真正可用

`live_board.md` 或 `live_dashboard.html` 不是为了好看，而是为了回答：

```text
今天发现了哪些 token？
哪个被 BLOCK？
哪个被 PAUSE？
哪个进入 PAPER_READY？
哪个开了 paper position？
现在盈亏多少？
```

如果回答不了这些，dashboard 再漂亮也没意义。

---

## 5. paper runner 是否真实记录结果

核心文件：

```text
paper_positions.csv
```

必须有：

```text
entry_price
current_price
unrealized_pnl_pct
max_floating_profit_pct
max_drawdown_pct
wallet_structure_status
exit_reason
failure_type
```

否则日报无法判断系统效果。

---

## 6. daily_report 是否能评价系统

日报必须能回答：

```text
候选多少？
通过多少？
纸面开仓多少？
胜率多少？
平均收益多少？
最大回撤多少？
主要失败原因是什么？
WALLET_SUPPORT 是否真的比 NEUTRAL 好？
```

如果不能回答这些，系统还没进入真正验证阶段。

---

# 六、现在的最优策略

## 不删除已实现模块

```text
Runtime 保留
dashboard 保留
CLI 保留
event log 保留
process trace 保留
confirmation ticket 保留
notifier 保留
```

## 但当前只重点跑核心链路

```text
candidate → signal → wallet → quote/security → state → paper → report
```

## 辅助模块只做观察，不做决策

```text
dashboard 只展示
notifier 默认关闭
confirmation ticket 默认关闭
CLI 只查看
trace 只记录
```

---

# 七、现在应该做的具体动作

下一步不是新增功能，而是做一次系统对齐。

## 第一步：列出已有文件

让 AI / Codex 检查项目里是否存在：

```text
sikk_live_run.py
sikk/runtime/sikk_live_orchestrator.py
sikk/runtime/sikk_module_runner.py
sikk/runtime/sikk_status_builder.py
sikk/runtime/sikk_cli.py
sikk/runtime/sikk_dashboard_builder.py
sikk/runtime/sikk_notifier.py
sikk/wallet_structure/sikk_wallet_structure_gate.py
sikk/wallet_structure/sikk_candidate_wallet_structure_pipeline.py
sikk_paper_runner.py
sikk_daily_report.py
```

---

## 第二步：确认主流程只走一条

不要出现：

```text
这个脚本跑一套
那个 runtime 又跑一套
paper runner 又单独跑一套
```

统一成：

```text
sikk_live_run.py
  ↓
调用 runtime / module_runner
  ↓
生成统一输出
```

---

## 第三步：确认输出目录统一

统一到：

```text
data/gmgn_candidates_live_run/
```

不要多个目录到处散：

```text
data/reports/
data/gmgn_reports/
data/live/
data/output/
```

可以保留旧目录，但主流程只读取一个标准目录。

---

## 第四步：确认配置开关

把已经实现但暂时不想用的模块关闭：

```json
{
  "notification": {
    "enabled": false
  },
  "confirmation": {
    "enabled": false
  },
  "dashboard": {
    "enabled": true
  },
  "trace": {
    "enabled": true
  }
}
```

---

# 八、当前阶段的准确结论

现在系统不是“还没做”，而是：

> **模块已经较多，下一步要做系统收敛、主流程对齐、连续纸面验证。**

当前最重要的不是继续完善理论，也不是删除功能，而是：

```text
把已实现模块串成稳定主流程
确认每个 token 都有状态
确认 paper 结果能记录
确认日报能评价效果
连续跑 24 小时
```

---

# 九、下一步最实用任务

你可以直接让 AI / Codex 执行这个任务：

```text
检查当前项目所有已实现模块，不删除任何已实现文件。
目标是把现有模块收敛成一个稳定主入口 sikk_live_run.py。

要求：
1. 保留已有 Runtime、dashboard、CLI、trace、notifier、confirmation ticket。
2. 但 notification 和 confirmation 默认关闭。
3. 主流程只关注 candidate → signal → wallet → quote/security → state → paper → report。
4. 所有输出统一到 data/gmgn_candidates_live_run/。
5. 每个 token 必须生成 token_status.md。
6. 每轮必须生成 live_board.md。
7. paper_positions.csv 必须记录纸面仓位。
8. daily_report.md 必须能统计胜率、收益、回撤、失败原因。
9. 不新增无关功能，不做自动实盘。
10. 修复模块之间字段和路径不一致的问题。
```

---

# 最终判断

你现在处在：

```text
Runtime 已有雏形
钱包结构门禁已设计
纸面交易逻辑已设计
可观测模块已添加
但主流程需要收敛和稳定
```

所以当前工作不是“删减”，而是：

> **保留已实现模块，收敛主流程，稳定纸面验证。**


---

## 片段 35 / stream_idx=5461 / len=2194


有，但现在要**只完善最必要的部分**。  
当前不是继续扩展体系，而是把它压缩成一个能跑、能看、能复盘的最小闭环。

# 现在还需要完善的 6 个点

## 1. 一键主运行脚本

必须有一个入口：

```bash
python sikk_live_run.py
```

它负责串起来：

```text
候选发现 → K线信号 → 钱包结构门禁 → quote/security → 状态判断 → paper runner → 输出报告
```

没有这个，其他模块再完善也只是零散脚本。

---

## 2. 统一输入输出目录

现在需要固定一套最小目录：

```text
data/gmgn_candidates_live_run/
  candidates.json
  live_board.md
  daily_report.md
  paper_positions.csv

  tokens/
    <token_address>/
      token_status.md
      token_status.json

  wallet_structure/
    <token_address>/
      wallet_structure_decision.json
```

先不要再加太多目录。

---

## 3. token 状态输出

每个 token 必须能看懂：

```text
当前状态：WATCHING / PAUSE / BLOCKED / PAPER_READY / PAPER_OPEN / PAPER_CLOSED
K线信号：通过 / 未通过
钱包结构：SUPPORT / PAUSE / BLOCK / NEUTRAL
quote：通过 / 失败
security：通过 / 失败
为什么通过 / 暂停 / 阻断
是否进入纸面交易
```

这就是：

```text
tokens/<token>/token_status.md
```

---

## 4. live_board 总览

你需要一个总览文件：

```text
live_board.md
```

内容只要简单：

| Token | 状态 | 钱包结构 | K线 | Quote | Security | Paper | 原因 |
|---|---|---|---|---|---|---|---|

这个比 dashboard、机器人更重要。

---

## 5. paper_positions.csv

必须记录纸面仓位：

```text
position_id
token_address
token_symbol
entry_time
entry_price
current_price
status
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
unrealized_pnl_pct
max_floating_profit_pct
max_drawdown_pct
exit_reason
failure_type
```

没有这个，就没法知道系统有没有用。

---

## 6. daily_report.md

每天输出：

```text
发现 token 数
通过初筛数
WALLET_SUPPORT 数
WALLET_BLOCK 数
PAPER_READY 数
PAPER_OPEN 数
关闭仓位数
胜率
平均收益
最大回撤
失败原因 Top 5
```

这个是判断系统能不能进入下一阶段的依据。

---

# 现在不用完善的东西

暂时不要做：

```text
网页 dashboard
Telegram / Discord / 微信播报
confirmation ticket
自动实盘
复杂 replay
复杂历史地址库
过多角色分类
过多状态机分支
```

这些都后置。

---

# 当前最小验收标准

只要做到下面这个，就算当前阶段完成：

```bash
python sikk_live_run.py
```

运行后生成：

```text
data/gmgn_candidates_live_run/live_board.md
data/gmgn_candidates_live_run/daily_report.md
data/gmgn_candidates_live_run/paper_positions.csv
data/gmgn_candidates_live_run/tokens/<token>/token_status.md
```

并且你能看见：

```text
发现了哪个 token
为什么 BLOCK / PAUSE / PAPER_READY
纸面仓位有没有开
当前盈亏是多少
失败原因是什么
```

---

# 结论

还需要完善，但只完善这一件事：

> **最小可运行纸面验证闭环。**

不要再扩展系统。  
下一步就是把现有模块串成 `sikk_live_run.py`，让系统真的跑出结果。


---

## 片段 36 / stream_idx=5533 / len=1539


现在处在：

# Phase A → Phase B 准备前半段

更准确说：

> **SIKK-SOL 已完成“纸面交易验证系统设计”，但还没有完成“最小自动运行闭环”。**

---

## 已经明确的部分

你现在已经把核心方法论定下来了：

```text
SIKK-SOL 不是找庄家钱包脚本
而是筹码控制权状态机
```

核心判断也已经确定：

```text
钱包结构门禁
K线信号
quote / security
paper runner
失败归因
日报复盘
```

钱包结构层也已经明确：

```text
WALLET_SUPPORT
WALLET_PAUSE
WALLET_BLOCK
WALLET_NEUTRAL
```

纸面交易方向也明确：

```text
live entry price
滑点 / 手续费
纸面仓位记录
失败原因
日报统计
```

---

## 现在还没真正完成的部分

关键缺口是：

```text
系统还没有稳定自己跑起来
```

具体表现就是你刚才说的：

```text
不会自动发现 token
不会自动播报发现了哪个 token
没有统一状态文件
没有 live_board.md
不知道每个 token 当前处于什么状态
纸面交易结果还没有形成连续样本
```

所以现在不是缺更多理论，而是缺：

```text
最小运行闭环
```

---

# 当前阶段名称

我建议现在定义为：

```text
Phase A-2：最小可运行纸面验证闭环搭建阶段
```

不是：

```text
实盘阶段
复杂 Runtime 阶段
Dashboard 阶段
历史地址库阶段
自动交易阶段
```

---

# 当前最应该做什么

只做这 5 件：

```text
1. sikk_live_run.py 一键跑完整流程
2. live_board.md 输出本轮总览
3. token_status.md 输出单币状态
4. paper_positions.csv 记录纸面仓位
5. daily_report.md 输出每日复盘
```

---

# 当前不应该做什么

暂时不要做：

```text
网页 dashboard
Telegram / Discord / 微信机器人
confirmation ticket
自动实盘
复杂 replay
复杂历史地址库
过多模块拆分
过多状态枚举
```

这些现在会分散重点。

---

# 阶段判断表

| 模块 | 当前状态 |
|---|---|
| 方法论 | 已成型 |
| 钱包结构门禁 | 规则已设计，待最小实现 |
| K线信号 | 已有雏形 / 可接入 |
| quote / security | 已有雏形 / 可接入 |
| paper runner | 已有方向，待统一接入 |
| 自动运行 | 未完成 |
| 单币状态输出 | 未完成 |
| 总览输出 | 未完成 |
| 连续样本积累 | 未开始 / 刚准备 |
| 实盘 | 不应开启 |

---

# 一句话结论

你现在在：

> **从“设计完成”走向“最小可运行纸面验证系统”的阶段。**

下一步不要再扩展系统。  
直接做：

```text
sikk_live_run.py
```

让它能一键跑出：

```text
live_board.md
token_status.md
paper_positions.csv
daily_report.md
```

这一步完成后，才算进入真正的 **Phase B：连续纸面验证阶段**。


---

## 片段 37 / stream_idx=5637 / len=2922


你说得对。  
前面有些内容已经开始偏“系统扩展”，现在要收回来。

当前不要再继续做：

```text
复杂 dashboard
Discord / Telegram 播报
confirmation ticket
网页筛选
复杂 Runtime 分层
过多状态枚举
过多文件拆分
```

这些不是现在的重点。

---

# 现在最实用的重点

你现在真正需要的是：

```text
系统能自己跑
能发现 token
能告诉你发现了什么 token
能告诉你这个 token 当前为什么通过 / 暂停 / 阻断
能进入纸面交易
能记录纸面结果
能让你每天看到哪些规则有效
```

所以当前只做 **5 个实用核心功能**。

---

# 一、最小实用系统结构

当前只保留这条主线：

```text
候选发现
  ↓
K线信号
  ↓
钱包结构门禁
  ↓
quote / security 检查
  ↓
状态机
  ↓
纸面交易
  ↓
日报复盘
```

其他全部后置。

---

# 二、现在最应该先做的 5 件事

## 1. 自动跑一轮

先不要 loop、dashboard、通知器。

只要做到：

```bash
python sikk_live_run.py
```

运行后自动执行：

```text
发现候选
分析 K线
分析钱包结构
检查 quote
检查 security
更新状态
更新纸面交易
输出结果
```

这是第一优先级。

---

## 2. 输出一个总览文件

只需要一个：

```text
data/gmgn_candidates_live_run/live_board.md
```

里面显示：

```text
发现了哪些 token
每个 token 当前状态
为什么通过 / 暂停 / 阻断
是否进入纸面交易
当前纸面盈亏
```

先不要网页。

---

## 3. 每个 token 输出一个状态文件

只需要：

```text
data/gmgn_candidates_live_run/tokens/<token>/token_status.md
```

里面显示：

```text
K线结论
钱包结构结论
quote 结论
security 结论
状态机结论
paper 状态
```

这比 dashboard 更实用。

---

## 4. 钱包结构只做门禁，不要继续扩展角色

当前钱包结构只输出 4 种状态：

```text
WALLET_SUPPORT
WALLET_PAUSE
WALLET_BLOCK
WALLET_NEUTRAL
```

不要继续扩展太多身份。

核心只看：

```text
早期钱包是否清仓
同源组是否同步卖出
高结果钱包是否退出
是否出现分发
是否出现对手盘承接
```

够用了。

---

## 5. 每天输出纸面日报

只需要：

```text
data/gmgn_candidates_live_run/daily_report.md
```

统计：

```text
候选数
通过数
阻断数
纸面入场数
关闭仓位数
胜率
平均收益
最大回撤
失败原因 Top 5
```

这是最能帮助你判断系统有没有用的东西。

---

# 三、现在不要做的东西

暂时不做：

```text
Telegram / Discord / 微信播报
网页 dashboard
confirmation ticket
自动实盘
复杂 replay
复杂历史地址库
多链扩展
复杂 UI
过多测试文件
复杂模块注册器
```

这些以后再说。

---

# 四、当前最小可运行版本

现在应该把系统压缩成 4 个核心文件：

```text
sikk_live_run.py
sikk_wallet_structure_gate.py
sikk_paper_runner.py
sikk_daily_report.py
```

最多再加：

```text
sikk_config.json
```

就够了。

---

# 五、真正实用的运行结果应该长这样

运行：

```bash
python sikk_live_run.py
```

输出：

```text
本轮发现 12 个 token

$AAA
状态：BLOCKED
原因：早期钱包清仓 88%，同源组同步卖出 74

$BBB
状态：PAUSE
原因：对手盘压力 58，数据质量不足

$CCC
状态：PAPER_READY
原因：K线 S3，钱包结构 SUPPORT，quote/security 通过

$DDD
状态：PAPER_OPEN
当前浮盈：+8.4%
钱包结构：STRUCTURE_HOLDING
```

同时生成：

```text
live_board.md
tokens/<token>/token_status.md
paper_positions.csv
daily_report.md
```

这才是现在最有价值的东西。

---

# 六、当前优先级重新排序

## P0：必须先做

```text
1. sikk_live_run.py 一键跑完整流程
2. live_board.md 总览输出
3. token_status.md 单币状态输出
4. paper_positions.csv 纸面仓位记录
5. daily_report.md 日报
```

## P1：跑稳定后再做

```text
6. loop 定时运行
7. 钱包结构 delta
8. 失败归因
9. SQLite
10. replay
```

## P2：以后再做

```text
11. dashboard
12. 通知机器人
13. confirmation ticket
14. 实盘 gate
15. 历史地址库
```

---

# 七、下一步最实际的任务

现在最应该让 AI / Codex 做的是：

```text
把当前已有的候选发现、K线信号、钱包结构、quote/security、paper runner 串成一个 sikk_live_run.py。
```

要求非常简单：

```text
输入：candidates.json
输出：
- live_board.md
- token_status.md
- paper_positions.csv
- daily_report.md
```

不是继续加功能。

---

# 结论

你现在的判断是对的。

当前系统应该收缩为：

> **最小可运行纸面验证系统**

不是继续升级 Runtime、Dashboard、Webhook、确认票据。

现在唯一重点：

```text
能不能自动发现 token
能不能判断状态
能不能进入纸面交易
能不能记录结果
能不能每天复盘
```

先把这个跑稳，其他全部后置。


---

## 片段 38 / stream_idx=5836 / len=28169


# SIKK Live Runtime v0.3：5 个关键接缝定稿

这一步要解决的是：

```text
模块接口统一
输出是否过期
看板筛选搜索
paper runner 与 skip 策略协调
confirmation ticket 接入
```

核心目标：

> Runtime 不再只是“能跑”，而是能按统一协议调度各模块，并且知道哪些结果过期、哪些 token 要继续处理、哪些进入人工确认。

---

# 一、K线 / 钱包 / quote / security / paper 模块 CLI 参数统一

## 1. 标准 CLI 协议

所有模块统一支持这些参数：

```bash
--token TOKEN_ADDRESS
--symbol TOKEN_SYMBOL
--run-id RUN_ID
--base-dir data/gmgn_candidates_live_run
--output-dir MODULE_OUTPUT_DIR
--mode live
--force
```

### 通用参数解释

| 参数 | 含义 |
|---|---|
| `--token` | token 合约地址 / mint 地址 |
| `--symbol` | token 符号 |
| `--run-id` | 当前运行批次 ID |
| `--base-dir` | 总数据目录 |
| `--output-dir` | 当前模块输出目录 |
| `--mode` | `live` / `replay` / `paper` |
| `--force` | 强制重跑，忽略已有输出 |

---

## 2. 各模块统一输出文件

### K线模块

```text
data/gmgn_candidates_live_run/signals/<token>/signal.json
```

### 钱包结构模块

```text
data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json
```

### quote 模块

```text
data/gmgn_candidates_live_run/quotes/<token>/quote.json
```

### security 模块

```text
data/gmgn_candidates_live_run/security/<token>/security.json
```

### paper runner

```text
data/gmgn_candidates_live_run/paper_positions.csv
data/gmgn_candidates_live_run/paper_trades.csv
```

---

## 3. 每个模块输出必须有统一元字段

所有 JSON 输出必须包含：

```json
{
  "token_address": "TOKEN_ADDRESS",
  "token_symbol": "TOKEN",
  "module": "wallet_structure",
  "status": "OK",
  "gate": "ALLOW",
  "reason": "说明原因",
  "generated_at": "2026-05-02T12:00:00Z",
  "stale_after_sec": 600,
  "expires_at": "2026-05-02T12:10:00Z",
  "run_id": "run_20260502_120000"
}
```

这几个字段非常关键：

```text
generated_at       什么时候生成
stale_after_sec    多久后过期
expires_at         明确过期时间
status             模块是否成功
gate               允许 / 暂停 / 阻断
reason             为什么
```

---

## 4. 各模块推荐 stale_after_sec

| 模块 | stale_after_sec | 原因 |
|---|---:|---|
| K线信号 | 600 秒 | 10 分钟内有效 |
| 钱包结构 | 600 秒 | 10 分钟内有效 |
| quote | 10 秒 | meme quote 很快失效 |
| security | 1800 秒 | 安全扫描不必每分钟跑 |
| paper update | 180 秒 | 持仓 3 分钟更新一次 |
| confirmation ticket | 10 秒 | 人工确认必须短有效期 |

---

## 5. module_runner 调用 CLI 统一代码

修改 `sikk_module_runner.py` 的 `run_script()`：

```python
def run_script(
    script_path: str,
    token=[REDACTED] Any],
    run_id: str,
    base_dir: str,
    output_dir: str,
    mode: str = "live",
    force: bool = False,
) -> None:
    token_address = token["token_address"]
    token_symbol = token.get("token_symbol") or "UNKNOWN"

    cmd = [
        "python",
        script_path,
        "--token", token_address,
        "--symbol", token_symbol,
        "--run-id", run_id,
        "--base-dir", base_dir,
        "--output-dir", output_dir,
        "--mode", mode,
    ]

    if force:
        cmd.append("--force")

    subprocess.run(cmd, check=True)
```

---

## 6. 每个模块的标准 argparse 模板

每个模块脚本开头都用这个：

```python
def parse_args():
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--token", required=True)
    parser.add_argument("--symbol", default="UNKNOWN")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--base-dir", default="data/gmgn_candidates_live_run")
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--mode", choices=["live", "paper", "replay"], default="live")
    parser.add_argument("--force", action="store_true")

    return parser.parse_args()
```

---

# 二、module_runner 如何识别模块输出是否过期

现在不能只判断“文件存在”。  
要判断：

```text
文件是否存在
文件是否可读
generated_at 是否存在
expires_at 是否已过期
status 是否 OK
是否 force 重跑
```

---

## 1. 新增输出新鲜度判断

放进：

```text
sikk/runtime/sikk_module_runner.py
```

```python
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Dict, Tuple


def parse_iso_time(value: Any):
    if not value:
        return None

    try:
        text = str(value)
        if text.endswith("Z"):
            text = text.replace("Z", "+00:00")
        return datetime.fromisoformat(text)
    except Exception:
        return None


def now_utc():
    return datetime.now(timezone.utc)


def read_json_optional(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def module_output_path(module_key: str, token_address: str, base_dir: Path) -> Path | None:
    paths = {
        "kline_signal": base_dir / "signals" / token_address / "signal.json",
        "wallet_structure": base_dir / "wallet_structure" / token_address / "wallet_structure_decision.json",
        "quote": base_dir / "quotes" / token_address / "quote.json",
        "security": base_dir / "security" / token_address / "security.json",
    }

    return paths.get(module_key)


def is_module_output_fresh(
    module_key: str,
    token_address: str,
    base_dir: Path,
) -> Tuple[bool, str]:
    path = module_output_path(module_key, token_address, base_dir)

    if path is None:
        return False, "no output path rule"

    if not path.exists():
        return False, "output missing"

    data = read_json_optional(path)

    if not data:
        return False, "output unreadable"

    if data.get("status") == "ERROR":
        return False, "previous output status ERROR"

    expires_at = parse_iso_time(data.get("expires_at"))

    if expires_at:
        if now_utc() <= expires_at:
            return True, "output fresh by expires_at"
        return False, "output expired by expires_at"

    generated_at = parse_iso_time(data.get("generated_at"))
    stale_after_sec = data.get("stale_after_sec")

    if generated_at and stale_after_sec:
        age = (now_utc() - generated_at).total_seconds()
        if age <= float(stale_after_sec):
            return True, "output fresh by generated_at + stale_after_sec"
        return False, "output stale by stale_after_sec"

    return False, "missing freshness metadata"
```

---

## 2. module_runner 中使用 freshness

```python
def run_one_module(
    module_key: str,
    module_config: Mapping[str, Any],
    token=[REDACTED] Any],
    run_id: str,
    base_dir: Path,
    force: bool = False,
) -> Dict[str, Any]:

    token_address = token["token_address"]

    if not module_config.get("enabled", False):
        return {
            "module": module_key,
            "status": "SKIPPED",
            "reason": "module disabled",
        }

    # paper_runner 每轮都可能需要更新，不能简单用文件新鲜度跳过
    skip_if_fresh = module_key not in {"paper_runner"}

    if skip_if_fresh and not force:
        fresh, reason = is_module_output_fresh(module_key, token_address, base_dir)
        if fresh:
            return {
                "module": module_key,
                "status": "SKIPPED",
                "reason": reason,
            }

    try:
        mode = module_config.get("mode", "script")

        output_dir = str(module_output_path(module_key, token_address, base_dir).parent) \
            if module_output_path(module_key, token_address, base_dir) else str(base_dir)

        if mode == "script":
            run_script(
                script_path=module_config["script_path"],
                token=[REDACTED]
                run_id=run_id,
                base_dir=str(base_dir),
                output_dir=output_dir,
                mode=module_config.get("runtime_mode", "live"),
                force=force,
            )

        elif mode == "python_function":
            run_python_function(
                module_name=module_config["module_name"],
                function_name=module_config["function_name"],
                token=[REDACTED]
                run_id=run_id,
                base_dir=str(base_dir),
                output_dir=output_dir,
                force=force,
            )

        return {
            "module": module_key,
            "status": "OK",
            "reason": "module completed",
        }

    except Exception as e:
        return {
            "module": module_key,
            "status": "ERROR",
            "reason": str(e),
        }
```

---

# 三、live_dashboard.html 增加状态筛选和搜索

当前 HTML 看板只能展示。  
v0.3 要增加：

```text
按状态筛选
按钱包状态筛选
按 token 搜索
只看 PAPER_OPEN
只看 WALLET_SUPPORT
只看 BLOCKED
```

---

## 1. dashboard 增加控件

在 `sikk_dashboard_builder.py` 的 HTML 中加入：

```html
<div class="filters">
  <input id="searchInput" placeholder="搜索 Token / Address / Reason" onkeyup="filterTable()" />

  <select id="stateFilter" onchange="filterTable()">
    <option value="">全部 State</option>
    <option value="WATCHING">WATCHING</option>
    <option value="PAPER_READY">PAPER_READY</option>
    <option value="PAPER_OPEN">PAPER_OPEN</option>
    <option value="PAUSE">PAUSE</option>
    <option value="BLOCKED">BLOCKED</option>
    <option value="ERROR">ERROR</option>
  </select>

  <select id="walletFilter" onchange="filterTable()">
    <option value="">全部 Wallet</option>
    <option value="WALLET_SUPPORT">WALLET_SUPPORT</option>
    <option value="WALLET_PAUSE">WALLET_PAUSE</option>
    <option value="WALLET_BLOCK">WALLET_BLOCK</option>
    <option value="WALLET_NEUTRAL">WALLET_NEUTRAL</option>
  </select>
</div>
```

---

## 2. table row 增加 data 属性

生成每一行时改成：

```html
<tr 
  data-state="PAPER_OPEN"
  data-wallet="WALLET_SUPPORT"
  data-search="TEST TOKEN_ADDRESS 结构维持">
```

Python 里生成：

```python
rows.append(f"""
<tr
  data-state="{esc(current_state)}"
  data-wallet="{esc(wallet.get("wallet_structure_status"))}"
  data-search="{esc(str(token_symbol) + ' ' + str(token_address) + ' ' + str(t.get("latest_reason")))}"
>
  <td><a href="tokens/{esc(token_address)}/token_status.md">{esc(token_symbol)}</a></td>
  <td class="{status_class(current_state)}">{esc(current_state)}</td>
  <td class="{wallet_class(wallet.get("wallet_structure_status"))}">{esc(wallet.get("wallet_structure_status"))}</td>
  <td>{esc(wallet.get("wallet_structure_score"))}</td>
  <td>{esc(wallet.get("wallet_risk_score"))}</td>
  <td>{esc(wallet.get("counterparty_pressure_score"))}</td>
  <td>{esc(signal.get("signal_gate"))}</td>
  <td>{esc(quote.get("quote_gate"))}</td>
  <td>{esc(security.get("security_gate"))}</td>
  <td>{esc(paper.get("paper_status"))}</td>
  <td>{esc(pnl)}</td>
  <td>{esc(t.get("latest_reason"))}</td>
</tr>
""")
```

---

## 3. 增加 JS 筛选逻辑

放到 HTML 底部：

```html
<script>
function filterTable() {
  const search = document.getElementById("searchInput").value.toLowerCase();
  const state = document.getElementById("stateFilter").value;
  const wallet = document.getElementById("walletFilter").value;

  const rows = document.querySelectorAll("#tokenTable tbody tr");

  rows.forEach(row => {
    const rowState = row.getAttribute("data-state") || "";
    const rowWallet = row.getAttribute("data-wallet") || "";
    const rowSearch = (row.getAttribute("data-search") || "").toLowerCase();

    const matchSearch = !search || rowSearch.includes(search);
    const matchState = !state || rowState === state;
    const matchWallet = !wallet || rowWallet === wallet;

    row.style.display = (matchSearch && matchState && matchWallet) ? "" : "none";
  });
}
</script>
```

---

## 4. table 加 ID

```html
<table id="tokenTable">
```

---

## 5. 增加 CSS

```css
.filters {
  display: flex;
  gap: 10px;
  margin: 16px 0;
  flex-wrap: wrap;
}

.filters input, .filters select {
  background: #151820;
  color: #e7e7e7;
  border: 1px solid #2a2f3a;
  border-radius: 8px;
  padding: 8px 10px;
}
```

---

# 四、paper runner 的持仓更新和 token skip 策略如何协调

这是很关键的。  
不能因为 token 是 `BLOCKED` 就跳过它，因为：

```text
如果它还有 PAPER_OPEN 仓位，必须继续更新持仓。
```

所以 runtime 要拆成两条线：

```text
候选分析循环
paper 持仓更新循环
```

---

## 1. 两种处理优先级

### 分析处理

处理：

```text
WATCHING
PAPER_READY
PAUSE
新发现 token
```

可以跳过：

```text
BLOCKED
EXPIRED
CLOSED
```

### 持仓处理

只要有 open position，必须处理：

```text
PAPER_OPEN
PAPER_MANAGING
EXIT_MONITOR
```

无论 token 当前是不是 BLOCKED，都要继续处理。

---

## 2. 新增判断：是否有 open paper position

放进 `sikk_token_skip_policy.py`：

```python
import csv
from pathlib import Path


BASE_DIR = Path("data/gmgn_candidates_live_run")


def has_open_paper_position(token_address: str) -> bool:
    path = BASE_DIR / "paper_positions.csv"

    if not path.exists():
        return False

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = csv.DictReader(f)
        for r in rows:
            if str(r.get("token_address")) != str(token_address):
                continue

            status = str(r.get("status") or r.get("paper_status") or "").upper()

            if status in {"OPEN", "PAPER_OPEN", "PAPER_MANAGING", "EXIT_MONITOR"}:
                return True

    return False
```

---

## 3. 修改 should_process_token

```python
def should_process_token(token=[REDACTED] Any], force: bool = False) -> Tuple[bool, str]:
    if force:
        return True, "force=True"

    token_address = token["token_address"]

    # 最高优先级：有持仓必须继续处理
    if has_open_paper_position(token_address):
        return True, "open paper position requires processing"

    status = read_token_status(token_address)

    if not status:
        return True, "no previous status"

    current_state = status.get("current_state")
    last_update = parse_time(status.get("last_update"))

    if current_state in ALWAYS_PROCESS:
        return True, f"{current_state} requires continuous processing"

    if current_state in NORMAL_PROCESS:
        return True, f"{current_state} normal processing"

    cooldown = COOLDOWN_SECONDS.get(current_state)

    if cooldown is None:
        return True, f"no cooldown rule for {current_state}"

    if not last_update:
        return True, "missing last_update"

    elapsed = (now_utc() - last_update).total_seconds()

    if elapsed >= cooldown:
        return True, f"cooldown expired for {current_state}"

    return False, f"skip {current_state}, cooldown remaining {int(cooldown - elapsed)} sec"
```

---

## 4. paper runner 应该独立有 update-open 模式

统一 CLI：

```bash
python sikk_paper_runner.py --mode update-open --base-dir data/gmgn_candidates_live_run
```

或者单 token：

```bash
python sikk_paper_runner.py --mode update-token --token TOKEN --symbol TEST --base-dir data/gmgn_candidates_live_run
```

---

## 5. orchestrator 每轮先更新 open positions

在 `run_once()` 开头：

```python
def update_open_paper_positions(config: Dict[str, Any]) -> None:
    paper_config = config.get("modules", {}).get("paper_runner", {})

    if not paper_config.get("enabled", False):
        return

    script_path = paper_config.get("script_path")

    if not script_path:
        return

    try:
        subprocess.run(
            [
                "python",
                script_path,
                "--mode", "update-open",
                "--base-dir", str(BASE_DIR),
            ],
            check=True,
        )

        emit_event(
            "PAPER_UPDATED",
            "已更新所有 open paper positions",
        )

    except Exception as e:
        emit_event(
            "ERROR",
            f"更新 open paper positions 失败：{e}",
            level="ERROR",
        )
```

然后：

```python
def run_once():
    config = read_config()

    emit_event("RUN_STARTED", "SIKK-SOL 开始运行一轮")

    # 1. 先更新已有持仓
    update_open_paper_positions(config)

    # 2. 再发现 / 处理候选
    candidates = discover_candidates(config)

    ...
```

---

# 五、confirmation ticket 如何接入 PAPER_READY → READY_FOR_CONFIRMATION

这个是阶段 B 的核心。

当前阶段：

```text
Phase A：paper only
Phase B：paper + human confirmation ticket
```

所以 `PAPER_READY` 后不要直接进入实盘。  
应该生成：

```text
confirmation_ticket
```

---

## 1. 状态流重建

```text
PAPER_READY
  ↓
生成 confirmation_ticket
  ↓
READY_FOR_CONFIRMATION
  ↓
人工确认
  ├─ APPROVED → 可进入小仓实盘执行队列
  ├─ REJECTED → 回到 WATCHING / PAUSE
  └─ EXPIRED → QUOTE_STALE / EXPIRED
```

当前仍禁止自动 broadcast。

---

## 2. ticket 文件目录

```text
data/gmgn_candidates_live_run/confirmation_tickets/
  pending/
    ticket_<token>_<timestamp>.json
    ticket_<token>_<timestamp>.md
  approved/
  rejected/
  expired/
```

---

## 3. ticket JSON 标准

```json
{
  "ticket_id": "TICKET_TEST_20260502_120000",
  "token_address": "TOKEN_ADDRESS",
  "token_symbol": "TEST",
  "status": "PENDING",
  "created_at": "2026-05-02T12:00:00Z",
  "expires_at": "2026-05-02T12:00:10Z",
  "stale_after_sec": 10,

  "requested_action": "PAPER_TO_REAL_CONFIRMATION",
  "suggested_size_sol": 0.01,

  "market": {
    "price": 0.000123,
    "market_cap": 120000,
    "liquidity": 45000
  },

  "signal": {
    "signal_level": "S3",
    "signal_type": "CONTROL_BOX_BREAKOUT_PULLBACK"
  },

  "wallet_structure": {
    "wallet_structure_status": "WALLET_SUPPORT",
    "wallet_structure_score": 72,
    "wallet_risk_score": 28,
    "counterparty_pressure_score": 32,
    "reason": "早期钱包仍有部分持仓，高结果钱包未集中退出"
  },

  "quote": {
    "quote_gate": "ALLOW",
    "quote_price": 0.000123,
    "price_deviation_pct": 0.8
  },

  "security": {
    "security_gate": "ALLOW",
    "risk_level": "LOW"
  },

  "decision": {
    "allow_real_execution": false,
    "requires_human_confirmation": true,
    "broadcast_allowed": false
  }
}
```

---

## 4. 新增 `sikk_confirmation_ticket.py`

```python
from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Mapping


BASE_DIR = Path("data/gmgn_candidates_live_run")
TICKET_DIR = BASE_DIR / "confirmation_tickets"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def make_ticket_id(token_symbol: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"TICKET_{token_symbol}_{ts}"


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def create_confirmation_ticket(
    token_status: Mapping[str, Any],
    suggested_size_sol: float = 0.01,
    stale_after_sec: int = 10,
) -> Dict[str, Any]:
    token_symbol = token_status.get("token_symbol") or "UNKNOWN"
    token_address = token_status.get("token_address")

    now = datetime.now(timezone.utc)
    expires = now + timedelta(seconds=stale_after_sec)

    ticket_id = make_ticket_id(token_symbol)

    ticket = {
        "ticket_id": ticket_id,
        "token_address": token_address,
        "token_symbol": token_symbol,
        "status": "PENDING",
        "created_at": now.isoformat(),
        "expires_at": expires.isoformat(),
        "stale_after_sec": stale_after_sec,

        "requested_action": "PAPER_TO_REAL_CONFIRMATION",
        "suggested_size_sol": suggested_size_sol,

        "market": token_status.get("market", {}),
        "signal": token_status.get("signal", {}),
        "wallet_structure": token_status.get("wallet_structure", {}),
        "quote": token_status.get("quote", {}),
        "security": token_status.get("security", {}),

        "decision": {
            "allow_real_execution": False,
            "requires_human_confirmation": True,
            "broadcast_allowed": False
        }
    }

    pending_dir = TICKET_DIR / "pending"
    json_path = pending_dir / f"{ticket_id}.json"
    md_path = pending_dir / f"{ticket_id}.md"

    write_json(json_path, ticket)
    md_path.write_text(render_ticket_md(ticket), encoding="utf-8")

    return ticket


def render_ticket_md(ticket: Mapping[str, Any]) -> str:
    w = ticket.get("wallet_structure", {})
    q = ticket.get("quote", {})
    s = ticket.get("security", {})
    sig = ticket.get("signal", {})
    m = ticket.get("market", {})

    return f"""# Confirmation Ticket

## 基础信息

- Ticket：{ticket.get("ticket_id")}
- Token：${ticket.get("token_symbol")}
- Address：{ticket.get("token_address")}
- 状态：{ticket.get("status")}
- 创建时间：{ticket.get("created_at")}
- 过期时间：{ticket.get("expires_at")}
- 建议仓位：{ticket.get("suggested_size_sol")} SOL

## 市场

- 价格：{m.get("price")}
- 市值：{m.get("market_cap")}
- 池子：{m.get("liquidity")}

## 信号

- 信号等级：{sig.get("signal_level")}
- 信号类型：{sig.get("signal_type")}
- Signal Gate：{sig.get("signal_gate")}

## 钱包结构

- 钱包状态：{w.get("wallet_structure_status")}
- 结构分：{w.get("wallet_structure_score")}
- 风险分：{w.get("wallet_risk_score")}
- 对手盘压力：{w.get("counterparty_pressure_score")}
- 原因：{w.get("reason")}

## Quote / Security

- Quote Gate：{q.get("quote_gate")}
- 价格偏差：{q.get("price_deviation_pct")}
- Security Gate：{s.get("security_gate")}
- 风险等级：{s.get("risk_level")}

## 执行限制

- 允许自动实盘：False
- 需要人工确认：True
- 允许 broadcast：False
"""


def move_ticket(ticket_path: Path, target_status: str) -> Path:
    data = json.loads(ticket_path.read_text(encoding="utf-8"))
    data["status"] = target_status

    target_dir = TICKET_DIR / target_status.lower()
    target_dir.mkdir(parents=True, exist_ok=True)

    target_path = target_dir / ticket_path.name
    target_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    ticket_path.unlink(missing_ok=True)

    md_source = ticket_path.with_suffix(".md")
    if md_source.exists():
        md_target = target_dir / md_source.name
        shutil.move(str(md_source), str(md_target))

    return target_path
```

---

## 5. token_status_builder 中接入 READY_FOR_CONFIRMATION

当前 `infer_current_state()` 需要增加：

```python
def has_pending_confirmation_ticket(token_address: str) -> bool:
    ticket_dir = BASE_DIR / "confirmation_tickets" / "pending"

    if not ticket_dir.exists():
        return False

    for path in ticket_dir.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("token_address") == token_address and data.get("status") == "PENDING":
                return True
        except Exception:
            continue

    return False
```

然后在 `infer_current_state()` 中：

```python
if has_pending_confirmation_ticket(token_address):
    return "READY_FOR_CONFIRMATION"
```

需要把 `token_address` 传进去：

```python
def infer_current_state(token_address, signal, wallet, quote, security, paper):
    ...
```

---

## 6. orchestrator 里从 PAPER_READY 创建 ticket

在 `run_token()` 生成 status 后：

```python
from sikk.runtime.sikk_confirmation_ticket import create_confirmation_ticket
```

```python
if status.get("current_state") == "PAPER_READY":
    runtime_mode = config.get("runtime_mode", "paper_only")

    if runtime_mode == "human_confirmation":
        ticket = create_confirmation_ticket(status)

        emit_event(
            "CONFIRMATION_TICKET_CREATED",
            f"{token.get('token_symbol')} 已生成确认票据：{ticket.get('ticket_id')}",
            token=[REDACTED]
            data=ticket,
        )

        # 重新构建状态，让它变成 READY_FOR_CONFIRMATION
        status = build_token_status(token)
```

配置：

```json
{
  "runtime_mode": "human_confirmation"
}
```

当前默认建议：

```json
{
  "runtime_mode": "paper_only"
}
```

---

# 六、CLI 增加 ticket 命令

`sikk_cli.py` 增加：

```bash
python -m sikk.runtime.sikk_cli tickets
python -m sikk.runtime.sikk_cli approve TICKET_ID
python -m sikk.runtime.sikk_cli reject TICKET_ID
```

第一版只改文件状态，不执行交易。

```python
def cmd_tickets(args):
    ticket_dir = BASE_DIR / "confirmation_tickets" / "pending"

    if not ticket_dir.exists():
        print("暂无 pending tickets")
        return

    for path in ticket_dir.glob("*.json"):
        data = read_json(path)
        print(f"{data.get('ticket_id')} | {data.get('token_symbol')} | expires={data.get('expires_at')}")


def find_ticket(ticket_id: str) -> Path | None:
    ticket_dir = BASE_DIR / "confirmation_tickets" / "pending"

    for path in ticket_dir.glob("*.json"):
        data = read_json(path)
        if data.get("ticket_id") == ticket_id:
            return path

    return None


def cmd_approve(args):
    from sikk.runtime.sikk_confirmation_ticket import move_ticket

    path = find_ticket(args.ticket_id)

    if not path:
        print("没有找到 pending ticket")
        return

    new_path = move_ticket(path, "APPROVED")
    print(f"已批准 ticket，但当前阶段不自动 broadcast：{new_path}")


def cmd_reject(args):
    from sikk.runtime.sikk_confirmation_ticket import move_ticket

    path = find_ticket(args.ticket_id)

    if not path:
        print("没有找到 pending ticket")
        return

    new_path = move_ticket(path, "REJECTED")
    print(f"已拒绝 ticket：{new_path}")
```

argparse 增加：

```python
p_tickets = sub.add_parser("tickets")
p_tickets.set_defaults(func=cmd_tickets)

p_approve = sub.add_parser("approve")
p_approve.add_argument("ticket_id")
p_approve.set_defaults(func=cmd_approve)

p_reject = sub.add_parser("reject")
p_reject.add_argument("ticket_id")
p_reject.set_defaults(func=cmd_reject)
```

---

# 七、Runtime v0.3 最终运行流

```text
run_once()
  ↓
update_open_paper_positions()
  ↓
discover_candidates()
  ↓
for token=[REDACTED]
      ├─ 有 open paper position → 必须处理
      ├─ BLOCKED 未过冷却 → 跳过
      ├─ PAUSE 未过冷却 → 跳过
      └─ 其他 → 处理

    run_external_modules_for_token()
      ├─ kline_signal
      ├─ wallet_structure
      ├─ quote
      ├─ security
      └─ paper_runner

    build_token_status()
      ↓
    if PAPER_READY and runtime_mode == human_confirmation:
        create_confirmation_ticket()
        status → READY_FOR_CONFIRMATION

    write_process_trace()
    write_token_status.json/md

  ↓
save_live_state()
build_live_board.md
build_live_dashboard.html
emit important events
notify Discord / Telegram
```

---

# 八、当前最优开发顺序

```text
1. 统一所有模块 CLI 参数
2. 所有模块 JSON 输出增加 generated_at / stale_after_sec / expires_at
3. module_runner 改成 freshness 判断，而不是只看文件存在
4. paper runner 增加 update-open 模式
5. skip_policy 增加 has_open_paper_position()
6. dashboard 增加搜索和筛选
7. 增加 confirmation_ticket
8. CLI 增加 tickets / approve / reject
```

---

# 九、最小验收标准

运行：

```bash
python -m sikk.runtime.sikk_live_orchestrator --mode once
```

必须满足：

```text
1. 各模块使用统一 CLI 参数
2. 已存在但未过期的模块输出会跳过
3. 过期 quote 会重跑
4. BLOCKED token 不会重复跑
5. 有 open paper position 的 token 即使 BLOCKED 也会更新
6. live_dashboard.html 可以搜索 / 筛选
7. PAPER_READY 在 human_confirmation 模式下生成 ticket
8. CLI 可以查看、批准、拒绝 ticket
9. 批准 ticket 不会自动 broadcast
```

---

# 十、给 Codex / OpenClaw 的任务提示词

```text
任务：实现 SIKK Live Runtime v0.3。

当前 v0.2 已有：
- module_runner
- token_status
- process_trace
- live_dashboard.html
- token_skip_policy
- notifier

现在补齐 v0.3：

一、统一模块 CLI 参数
所有模块统一支持：
--token
--symbol
--run-id
--base-dir
--output-dir
--mode
--force

所有模块 JSON 输出必须包含：
- token_address
- token_symbol
- module
- status
- gate
- reason
- generated_at
- stale_after_sec
- expires_at
- run_id

二、module_runner 输出新鲜度判断
不要只看文件是否存在。
新增 is_module_output_fresh()：
- 文件不存在 → stale
- 文件不可读 → stale
- status=ERROR → stale
- expires_at 已过 → stale
- generated_at + stale_after_sec 已过 → stale
- force=True → 强制重跑

quote stale_after_sec = 10
kline_signal stale_after_sec = 600
wallet_structure stale_after_sec = 600
security stale_after_sec = 1800
confirmation_ticket stale_after_sec = 10

三、live_dashboard.html 增加搜索和筛选
增加：
- searchInput
- stateFilter
- walletFilter

表格 row 增加：
- data-state
- data-wallet
- data-search

JS 实现 filterTable()。

四、paper runner 和 skip 策略协调
新增 has_open_paper_position(token_address)。
如果 token 有 OPEN / PAPER_OPEN / PAPER_MANAGING / EXIT_MONITOR 仓位，即使当前状态是 BLOCKED，也必须继续处理。
run_once() 开头先执行 update_open_paper_positions()。
paper_runner 必须支持：
--mode update-open
--mode update-token

五、confirmation ticket
新增 sikk_confirmation_ticket.py。
当 current_state == PAPER_READY 且 runtime_mode == human_confirmation 时：
- 创建 confirmation ticket
- 状态进入 READY_FOR_CONFIRMATION
- ticket 10 秒过期
- ticket 只允许人工批准 / 拒绝
- 当前阶段禁止自动 broadcast

ticket 输出：
data/gmgn_candidates_live_run/confirmation_tickets/pending/<ticket_id>.json
data/gmgn_candidates_live_run/confirmation_tickets/pending/<ticket_id>.md

CLI 增加：
- tickets
- approve TICKET_ID
- reject TICKET_ID

批准 ticket 只移动到 approved，不执行实盘交易。

验收：
运行 once 后：
- dashboard 可搜索筛选
- 过期模块会重跑
- 未过期模块会跳过
- PAPER_READY 在 human_confirmation 模式下生成 ticket
- open paper position 不会被 skip policy 跳过
```

---

# 本次认知升级点

这一步把系统从 Runtime v0.2 推到 v0.3：

```text
v0.2：系统能持续跑、能看、能播报
v0.3：系统能判断输出是否过期、避免重复跑、处理持仓优先级、进入人工确认流程
```

核心升级：

> 系统开始具备“运行治理能力”，而不是简单循环执行脚本。

---

# 尚未解决问题

下一步继续补：

```text
1. confirmation ticket 过期自动清理逻辑
2. approved ticket 如何进入真实 execution gate，但仍不自动 broadcast
3. paper runner 的 update-open 真实实现
4. dashboard 增加 PnL 曲线和失败原因统计
5. 模块输出 schema 校验，防止某个模块输出字段缺失导致 Runtime 误判
```


---

## 片段 39 / stream_idx=5915 / len=222


1. K线 / 钱包 / quote / security / paper 各模块的真实 CLI 参数统一
2. module_runner 如何识别模块输出是否过期
3. live_dashboard.html 增加状态筛选和搜索
4. paper runner 的持仓更新和 token skip 策略如何协调
5. confirmation ticket 如何接入 PAPER_READY → READY_FOR_CONFIRMATION


---

## 片段 40 / stream_idx=6031 / len=30616


# SIKK Live Runtime v0.2：运行层完整接入

这一步要解决 5 个问题：

```text
1. run_external_modules_for_token() 如何实际调用 K线 / 钱包 / quote / security / paper 模块
2. live_board.md 如何转成 live_dashboard.html
3. Discord / Telegram webhook 如何配置
4. token_status.json 的状态变化如何写入 process_trace.jsonl
5. loop 模式下如何避免重复处理 BLOCKED / EXPIRED / 无变化 token
```

核心目标：

> 系统不只是“跑一轮”，而是能持续运行、记录状态变化、生成看板、必要时播报，同时避免重复无效处理。

---

# 一、Runtime v0.2 总结构

建议新增 / 修改这些文件：

```text
sikk/runtime/
  sikk_module_runner.py          # 实际调用各模块
  sikk_live_orchestrator.py      # 主控更新
  sikk_status_builder.py         # 合并 token_status
  sikk_trace_logger.py           # process_trace.jsonl
  sikk_dashboard_builder.py      # live_dashboard.html
  sikk_notifier.py               # Discord / Telegram 通知
  sikk_token_skip_policy.py      # loop 跳过策略
  sikk_cli.py                    # CLI 保留
```

数据目录：

```text
data/gmgn_candidates_live_run/
  live_state.json
  live_board.md
  live_dashboard.html

  events/
    live_events.jsonl
    latest_events.md

  tokens/
    <token_address>/
      token_status.json
      token_status.md
      process_trace.jsonl

  signals/<token>/signal.json
  wallet_structure/<token>/wallet_structure_decision.json
  quotes/<token>/quote.json
  security/<token>/security.json
  paper_positions.csv
```

---

# 二、`run_external_modules_for_token()` 如何实际调用模块

不要把模块调用全部写在 orchestrator 里。  
应该单独做：

```text
sikk/runtime/sikk_module_runner.py
```

它负责按顺序调用：

```text
K线信号模块
钱包结构模块
quote 模块
security 模块
paper runner
```

---

## 2.1 模块调用原则

每个模块都可以有 3 种接入方式：

```text
1. Python 函数调用
2. subprocess 调用独立脚本
3. 如果输出文件已存在，则只读取，不重复跑
```

v0.2 推荐：

```text
优先读取已有输出
缺失时再调用脚本
脚本失败则写 ERROR，但不中断整个 loop
```

---

## 2.2 配置文件扩展

修改：

```text
config/sikk_runtime_config.json
```

示例：

```json
{
  "candidate_provider": "file_json",
  "path": "data/gmgn_candidates_live_run/candidates.json",
  "loop_interval_sec": 600,

  "modules": {
    "kline_signal": {
      "enabled": true,
      "mode": "script",
      "script_path": "sikk_signal_engine.py"
    },
    "wallet_structure": {
      "enabled": true,
      "mode": "python_function",
      "module_name": "sikk.wallet_structure.sikk_candidate_wallet_structure_pipeline",
      "function_name": "process_one_token"
    },
    "quote": {
      "enabled": true,
      "mode": "script",
      "script_path": "sikk_quote_gate.py"
    },
    "security": {
      "enabled": true,
      "mode": "script",
      "script_path": "sikk_security_gate.py"
    },
    "paper_runner": {
      "enabled": true,
      "mode": "script",
      "script_path": "sikk_paper_runner.py"
    }
  },

  "notification": {
    "enabled": false,
    "channels": ["discord"],
    "discord_webhook_url": "",
    "telegram_bot_token": "",
    "telegram_chat_id": ""
  }
}
```

---

## 2.3 新增 `sikk_module_runner.py`

```python
from __future__ import annotations

import importlib
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


BASE_DIR = Path("data/gmgn_candidates_live_run")


def run_python_function(module_name: str, function_name: str, token=[REDACTED] Any], **kwargs) -> Any:
    module = importlib.import_module(module_name)
    fn = getattr(module, function_name)
    return fn(token, **kwargs)


def run_script(script_path: str, token=[REDACTED] Any]) -> None:
    token_address = token["token_address"]
    token_symbol = token.get("token_symbol") or "UNKNOWN"

    cmd = [
        "python",
        script_path,
        "--token",
        token_address,
        "--symbol",
        token_symbol,
    ]

    subprocess.run(cmd, check=True)


def output_exists_for_module(module_key: str, token_address: str) -> bool:
    paths = {
        "kline_signal": BASE_DIR / "signals" / token_address / "signal.json",
        "wallet_structure": BASE_DIR / "wallet_structure" / token_address / "wallet_structure_decision.json",
        "quote": BASE_DIR / "quotes" / token_address / "quote.json",
        "security": BASE_DIR / "security" / token_address / "security.json",
    }

    path = paths.get(module_key)
    return bool(path and path.exists())


def run_one_module(
    module_key: str,
    module_config: Mapping[str, Any],
    token=[REDACTED] Any],
    force: bool = False,
) -> Dict[str, Any]:
    """
    返回统一结果，不让单个模块失败拖死整个系统。
    """

    token_address = token["token_address"]

    if not module_config.get("enabled", False):
        return {
            "module": module_key,
            "status": "SKIPPED",
            "reason": "module disabled",
        }

    # paper runner 通常需要每轮更新，不用 output_exists 跳过
    skip_if_output_exists = module_key not in {"paper_runner"}

    if skip_if_output_exists and output_exists_for_module(module_key, token_address) and not force:
        return {
            "module": module_key,
            "status": "SKIPPED",
            "reason": "output exists",
        }

    try:
        mode = module_config.get("mode", "script")

        if mode == "python_function":
            run_python_function(
                module_name=module_config["module_name"],
                function_name=module_config["function_name"],
                token=[REDACTED]
            )

        elif mode == "script":
            run_script(
                script_path=module_config["script_path"],
                token=[REDACTED]
            )

        else:
            return {
                "module": module_key,
                "status": "ERROR",
                "reason": f"unsupported module mode: {mode}",
            }

        return {
            "module": module_key,
            "status": "OK",
            "reason": "module completed",
        }

    except Exception as e:
        return {
            "module": module_key,
            "status": "ERROR",
            "reason": str(e),
        }


def run_external_modules_for_token(
    token=[REDACTED] Any],
    config: Mapping[str, Any],
    force: bool = False,
) -> Dict[str, Any]:
    """
    实际模块调用顺序：
    1. K线信号
    2. 钱包结构
    3. quote
    4. security
    5. paper runner
    """

    modules = config.get("modules", {})

    order = [
        "kline_signal",
        "wallet_structure",
        "quote",
        "security",
        "paper_runner",
    ]

    results = []

    for module_key in order:
        module_config = modules.get(module_key, {"enabled": False})
        result = run_one_module(
            module_key=module_key,
            module_config=module_config,
            token=[REDACTED]
            force=force,
        )
        results.append(result)

    return {
        "token_address": token["token_address"],
        "token_symbol": token.get("token_symbol"),
        "module_results": results,
    }
```

---

## 2.4 修改 orchestrator 里的调用

在 `sikk_live_orchestrator.py` 里：

```python
from sikk.runtime.sikk_module_runner import run_external_modules_for_token
```

把原来的占位函数替换为：

```python
def run_token(token=[REDACTED] Any]) -> Dict[str, Any]:
    emit_event(
        "TOKEN_DISCOVERED",
        f"发现候选 {token.get('token_symbol')}，开始分析",
        token=[REDACTED]
        data=token,
    )

    config = read_config()

    try:
        module_result = run_external_modules_for_token(
            token=[REDACTED]
            config=config,
            force=False,
        )

        emit_event(
            "MODULES_FINISHED",
            f"{token.get('token_symbol')} 模块调用完成",
            token=[REDACTED]
            data=module_result,
        )

        status = build_token_status(token)
        write_token_status_files(status)

        write_process_trace(token, status, module_result)

        emit_event(
            "TOKEN_STATUS_UPDATED",
            f"{token.get('token_symbol')} 状态更新：{status.get('current_state')}",
            token=[REDACTED]
            data=status,
        )

        return status

    except Exception as e:
        emit_event(
            "ERROR",
            f"{token.get('token_symbol')} 处理失败：{e}",
            token=[REDACTED]
            level="ERROR",
        )

        return {
            "token_address": token.get("token_address"),
            "token_symbol": token.get("token_symbol"),
            "current_state": "ERROR",
            "latest_reason": str(e),
            "last_update": iso_now(),
        }
```

---

# 三、`token_status.json` 状态变化写入 `process_trace.jsonl`

现在每个 token 只生成 `token_status.json`，还不够。  
你需要知道：

```text
它之前是什么状态
为什么从 WATCHING 变成 PAUSE
为什么从 PAPER_READY 变成 BLOCKED
哪一轮开始触发钱包风险
```

所以每个 token 要写：

```text
data/gmgn_candidates_live_run/tokens/<token>/process_trace.jsonl
```

---

## 3.1 新增 `sikk_trace_logger.py`

```python
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


BASE_DIR = Path("data/gmgn_candidates_live_run")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json_optional(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def detect_state_change(previous: Mapping[str, Any], current: Mapping[str, Any]) -> Dict[str, Any]:
    prev_state = previous.get("current_state")
    cur_state = current.get("current_state")

    prev_wallet = previous.get("wallet_structure", {}).get("wallet_structure_status")
    cur_wallet = current.get("wallet_structure", {}).get("wallet_structure_status")

    prev_paper = previous.get("paper", {}).get("paper_status")
    cur_paper = current.get("paper", {}).get("paper_status")

    return {
        "state_changed": prev_state != cur_state,
        "wallet_changed": prev_wallet != cur_wallet,
        "paper_changed": prev_paper != cur_paper,
        "previous_state": prev_state,
        "current_state": cur_state,
        "previous_wallet_status": prev_wallet,
        "current_wallet_status": cur_wallet,
        "previous_paper_status": prev_paper,
        "current_paper_status": cur_paper,
    }


def write_process_trace(
    token=[REDACTED] Any],
    current_status: Mapping[str, Any],
    module_result: Optional[Mapping[str, Any]] = None,
    base_dir: Path = BASE_DIR,
) -> None:
    token_address = token["token_address"]
    token_dir = base_dir / "tokens" / token_address

    previous_status_path = token_dir / "token_status.json"
    previous_status = read_json_optional(previous_status_path)

    change = detect_state_change(previous_status, current_status)

    trace_row = {
        "time": iso_now(),
        "token_address": token_address,
        "token_symbol": token.get("token_symbol"),

        "state_changed": change["state_changed"],
        "wallet_changed": change["wallet_changed"],
        "paper_changed": change["paper_changed"],

        "previous_state": change["previous_state"],
        "current_state": change["current_state"],

        "previous_wallet_status": change["previous_wallet_status"],
        "current_wallet_status": change["current_wallet_status"],

        "previous_paper_status": change["previous_paper_status"],
        "current_paper_status": change["current_paper_status"],

        "latest_action": current_status.get("latest_action"),
        "latest_reason": current_status.get("latest_reason"),

        "wallet_structure": current_status.get("wallet_structure", {}),
        "signal": current_status.get("signal", {}),
        "quote": current_status.get("quote", {}),
        "security": current_status.get("security", {}),
        "paper": current_status.get("paper", {}),

        "module_result": module_result or {},
    }

    append_jsonl(token_dir / "process_trace.jsonl", trace_row)
```

---

## 3.2 orchestrator 接入 trace

在 `sikk_live_orchestrator.py` 中：

```python
from sikk.runtime.sikk_trace_logger import write_process_trace
```

注意顺序：

```text
先 build_token_status
再 write_process_trace
最后 write_token_status_files
```

因为 trace 需要读取旧的 token_status.json 对比。

```python
status = build_token_status(token)

write_process_trace(
    token=[REDACTED]
    current_status=status,
    module_result=module_result,
)

write_token_status_files(status)
```

---

# 四、loop 模式下如何避免重复处理 BLOCKED / EXPIRED token

如果不做跳过策略，loop 会每 10 分钟重复处理已经无效的 token。  
需要新增：

```text
sikk_token_skip_policy.py
```

---

## 4.1 跳过策略原则

不要全部跳过。  
要按状态分频率：

| 状态 | 处理策略 |
|---|---|
| PAPER_OPEN | 每轮都处理 |
| PAPER_READY | 每轮都处理，但检查 quote 是否过期 |
| WATCHING | 正常处理 |
| PAUSE | 降低频率，例如 15-30 分钟一次 |
| BLOCKED | 冷却 6 小时 |
| EXPIRED | 不再处理，除非重新发现 |
| ERROR | 30 分钟后重试 |
| CLOSED | 不再处理 |

---

## 4.2 新增 `sikk_token_skip_policy.py`

```python
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


BASE_DIR = Path("data/gmgn_candidates_live_run")


COOLDOWN_SECONDS = {
    "BLOCKED": 6 * 60 * 60,
    "PAUSE": 30 * 60,
    "ERROR": 30 * 60,
    "EXPIRED": 24 * 60 * 60,
    "PAPER_CLOSED": 24 * 60 * 60,
    "CLOSED": 24 * 60 * 60,
}


ALWAYS_PROCESS = {
    "PAPER_OPEN",
    "PAPER_READY",
    "READY_FOR_CONFIRMATION",
}


NORMAL_PROCESS = {
    "WATCHING",
    "UNKNOWN",
    None,
}


def parse_time(value: Any) -> datetime | None:
    if not value:
        return None

    try:
        text = str(value)
        if text.endswith("Z"):
            text = text.replace("Z", "+00:00")
        return datetime.fromisoformat(text)
    except Exception:
        return None


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def read_token_status(token_address: str) -> Dict[str, Any]:
    path = BASE_DIR / "tokens" / token_address / "token_status.json"
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def should_process_token(token=[REDACTED] Any], force: bool = False) -> Tuple[bool, str]:
    if force:
        return True, "force=True"

    token_address = token["token_address"]
    status = read_token_status(token_address)

    if not status:
        return True, "no previous status"

    current_state = status.get("current_state")
    last_update = parse_time(status.get("last_update"))

    if current_state in ALWAYS_PROCESS:
        return True, f"{current_state} requires continuous processing"

    if current_state in NORMAL_PROCESS:
        return True, f"{current_state} normal processing"

    cooldown = COOLDOWN_SECONDS.get(current_state)

    if cooldown is None:
        return True, f"no cooldown rule for {current_state}"

    if not last_update:
        return True, "missing last_update"

    elapsed = (now_utc() - last_update).total_seconds()

    if elapsed >= cooldown:
        return True, f"cooldown expired for {current_state}"

    return False, f"skip {current_state}, cooldown remaining {int(cooldown - elapsed)} sec"
```

---

## 4.3 orchestrator 中接入 skip policy

```python
from sikk.runtime.sikk_token_skip_policy import should_process_token
```

在 `run_once()` 里：

```python
for token in candidates:
    should_process, skip_reason = should_process_token(token, force=False)

    if not should_process:
        emit_event(
            "TOKEN_SKIPPED",
            f"{token.get('token_symbol')} 跳过：{skip_reason}",
            token=[REDACTED]
        )

        # 即使跳过，也可以读取旧状态写入 live_board
        old_status = load_existing_token_status(token)
        if old_status:
            status_rows.append(old_status)

        continue

    status_rows.append(run_token(token))
```

补一个函数：

```python
def load_existing_token_status(token=[REDACTED] Any]) -> Dict[str, Any] | None:
    path = BASE_DIR / "tokens" / token["token_address"] / "token_status.json"
    if not path.exists():
        return None

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
```

---

# 五、live_board.md 转 `live_dashboard.html`

当前可以做一个**静态 HTML**，不要先做 React / FastAPI。

新建：

```text
sikk/runtime/sikk_dashboard_builder.py
```

---

## 5.1 功能

读取：

```text
live_state.json
events/live_events.jsonl
```

输出：

```text
live_dashboard.html
```

---

## 5.2 代码

```python
from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path("data/gmgn_candidates_live_run")
LIVE_STATE_PATH = BASE_DIR / "live_state.json"
EVENTS_PATH = BASE_DIR / "events" / "live_events.jsonl"
DASHBOARD_PATH = BASE_DIR / "live_dashboard.html"


def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_events(limit: int = 30) -> List[Dict[str, Any]]:
    if not EVENTS_PATH.exists():
        return []

    lines = EVENTS_PATH.read_text(encoding="utf-8").splitlines()[-limit:]
    events = []

    for line in lines:
        try:
            events.append(json.loads(line))
        except Exception:
            continue

    return events


def esc(x: Any) -> str:
    return html.escape(str(x if x is not None else ""))


def status_class(state: str) -> str:
    state = str(state or "").upper()

    if state in {"PAPER_OPEN", "PAPER_READY"}:
        return "good"
    if state in {"PAUSE", "WATCHING"}:
        return "warn"
    if state in {"BLOCKED", "ERROR", "EXPIRED"}:
        return "bad"

    return "neutral"


def wallet_class(wallet_status: str) -> str:
    wallet_status = str(wallet_status or "").upper()

    if wallet_status == "WALLET_SUPPORT":
        return "good"
    if wallet_status in {"WALLET_PAUSE", "WALLET_NEUTRAL"}:
        return "warn"
    if wallet_status == "WALLET_BLOCK":
        return "bad"

    return "neutral"


def build_dashboard_html() -> str:
    state = read_json(LIVE_STATE_PATH)
    tokens = state.get("tokens", [])
    events = read_events(limit=40)

    state_counts = {}
    for t in tokens:
        st = t.get("current_state", "UNKNOWN")
        state_counts[st] = state_counts.get(st, 0) + 1

    rows = []
    for t in tokens:
        token_address = t.get("token_address")
        token_symbol = t.get("token_symbol")
        current_state = t.get("current_state")
        wallet = t.get("wallet_structure", {})
        signal = t.get("signal", {})
        quote = t.get("quote", {})
        security = t.get("security", {})
        paper = t.get("paper", {})

        pnl = paper.get("unrealized_pnl_pct") or paper.get("net_pnl_pct") or "-"

        rows.append(f"""
        <tr>
          <td><a href="tokens/{esc(token_address)}/token_status.md">{esc(token_symbol)}</a></td>
          <td class="{status_class(current_state)}">{esc(current_state)}</td>
          <td class="{wallet_class(wallet.get("wallet_structure_status"))}">{esc(wallet.get("wallet_structure_status"))}</td>
          <td>{esc(wallet.get("wallet_structure_score"))}</td>
          <td>{esc(wallet.get("wallet_risk_score"))}</td>
          <td>{esc(wallet.get("counterparty_pressure_score"))}</td>
          <td>{esc(signal.get("signal_gate"))}</td>
          <td>{esc(quote.get("quote_gate"))}</td>
          <td>{esc(security.get("security_gate"))}</td>
          <td>{esc(paper.get("paper_status"))}</td>
          <td>{esc(pnl)}</td>
          <td>{esc(t.get("latest_reason"))}</td>
        </tr>
        """)

    event_items = []
    for e in events:
        event_items.append(f"""
        <li>
          <strong>{esc(e.get("time"))}</strong>
          <span class="badge">{esc(e.get("event_type"))}</span>
          <span>{esc(e.get("token_symbol"))}</span>
          <span>{esc(e.get("message"))}</span>
        </li>
        """)

    count_cards = []
    for st, count in sorted(state_counts.items()):
        count_cards.append(f"""
        <div class="card">
          <div class="card-title">{esc(st)}</div>
          <div class="card-num">{esc(count)}</div>
        </div>
        """)

    return f"""
<!doctype html>
<html lang="zh">
<head>
  <meta charset="utf-8">
  <title>SIKK-SOL Live Dashboard</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 24px;
      background: #0f1115;
      color: #e7e7e7;
    }}
    h1, h2 {{
      margin-bottom: 8px;
    }}
    .muted {{
      color: #9aa0a6;
    }}
    .cards {{
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin: 16px 0;
    }}
    .card {{
      background: #1a1d24;
      padding: 14px 18px;
      border-radius: 10px;
      min-width: 120px;
    }}
    .card-title {{
      color: #9aa0a6;
      font-size: 12px;
    }}
    .card-num {{
      font-size: 28px;
      margin-top: 4px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 16px;
      background: #151820;
    }}
    th, td {{
      border-bottom: 1px solid #2a2f3a;
      padding: 9px;
      font-size: 13px;
      text-align: left;
    }}
    th {{
      background: #202532;
      position: sticky;
      top: 0;
    }}
    .good {{
      color: #61d394;
      font-weight: bold;
    }}
    .warn {{
      color: #ffd166;
      font-weight: bold;
    }}
    .bad {{
      color: #ef476f;
      font-weight: bold;
    }}
    .neutral {{
      color: #cfd2d6;
    }}
    a {{
      color: #8ab4f8;
      text-decoration: none;
    }}
    .events {{
      background: #151820;
      padding: 16px;
      border-radius: 10px;
    }}
    .events li {{
      margin-bottom: 8px;
    }}
    .badge {{
      background: #2a2f3a;
      padding: 2px 6px;
      border-radius: 6px;
      margin: 0 6px;
    }}
  </style>
</head>
<body>
  <h1>SIKK-SOL Live Dashboard</h1>
  <div class="muted">更新时间：{esc(state.get("last_update"))}</div>

  <div class="cards">
    <div class="card">
      <div class="card-title">Token 总数</div>
      <div class="card-num">{esc(state.get("token_count", len(tokens)))}</div>
    </div>
    {''.join(count_cards)}
  </div>

  <h2>Token 状态</h2>
  <table>
    <thead>
      <tr>
        <th>Token</th>
        <th>State</th>
        <th>Wallet</th>
        <th>结构分</th>
        <th>风险分</th>
        <th>对手盘</th>
        <th>Signal</th>
        <th>Quote</th>
        <th>Security</th>
        <th>Paper</th>
        <th>PnL</th>
        <th>Reason</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>

  <h2>最新事件</h2>
  <ul class="events">
    {''.join(event_items)}
  </ul>
</body>
</html>
"""


def write_dashboard(path: Path = DASHBOARD_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(build_dashboard_html(), encoding="utf-8")


if __name__ == "__main__":
    write_dashboard()
```

---

## 5.3 orchestrator 中自动生成 HTML

在 `build_live_board(status_rows)` 后面加：

```python
from sikk.runtime.sikk_dashboard_builder import write_dashboard
```

```python
build_live_board(status_rows)
write_dashboard()
```

---

# 六、Discord / Telegram webhook 实际配置

先做 Discord 和 Telegram，微信后置。

---

## 6.1 新增 `sikk_notifier.py`

```python
from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any, Dict


IMPORTANT_EVENTS = {
    "WALLET_SUPPORT",
    "WALLET_BLOCK",
    "PAPER_READY",
    "PAPER_OPENED",
    "PAPER_FORCE_EXIT",
    "ERROR",
    "DAILY_REPORT_READY",
}


def should_notify(event: Dict[str, Any]) -> bool:
    return event.get("event_type") in IMPORTANT_EVENTS


def format_event_message(event: Dict[str, Any]) -> str:
    time = event.get("time")
    event_type = event.get("event_type")
    token_symbol = event.get("token_symbol") or "-"
    token_address = event.get("token_address") or "-"
    message = event.get("message") or ""

    return (
        f"[{time}] {event_type}\n"
        f"Token=[REDACTED]
        f"Address: {token_address}\n"
        f"{message}"
    )


def post_json(url: str, payload: Dict[str, Any]) -> None:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req, timeout=10)


def post_discord(webhook_url: str, text: str) -> None:
    post_json(webhook_url, {"content": text})


def post_telegram(bot_token=[REDACTED] chat_id: str, text: str) -> None:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": True,
    }
    post_json(url, payload)


def notify_event(event: Dict[str, Any], config: Dict[str, Any]) -> None:
    notification = config.get("notification", {})

    if not notification.get("enabled", False):
        return

    if not should_notify(event):
        return

    text = format_event_message(event)
    channels = notification.get("channels", [])

    if "discord" in channels:
        webhook_url = notification.get("discord_webhook_url")
        if webhook_url:
            post_discord(webhook_url, text)

    if "telegram" in channels:
        bot_token=[REDACTED]
        chat_id = notification.get("telegram_chat_id")
        if bot_token and chat_id:
            post_telegram(bot_token, chat_id, text)
```

---

## 6.2 配置 Discord

`config/sikk_runtime_config.json`：

```json
{
  "notification": {
    "enabled": true,
    "channels": ["discord"],
    "discord_webhook_url": "你的 Discord Webhook URL",
    "telegram_bot_token": "",
    "telegram_chat_id": ""
  }
}
```

Discord 获取方式：

```text
Discord 频道设置
→ Integrations
→ Webhooks
→ New Webhook
→ Copy Webhook URL
```

---

## 6.3 配置 Telegram

```json
{
  "notification": {
    "enabled": true,
    "channels": ["telegram"],
    "discord_webhook_url": "",
    "telegram_bot_token": "你的 bot token",
    "telegram_chat_id": "你的 chat id"
  }
}
```

Telegram 获取方式：

```text
1. 找 BotFather 创建 bot
2. 拿到 bot_token
3. 给 bot 发一条消息
4. 用 getUpdates 查 chat_id
```

浏览器打开：

```text
https://api.telegram.org/bot<你的bot_token>/getUpdates
```

找到：

```text
chat.id
```

---

## 6.4 orchestrator 的 emit_event 接通知

修改 `emit_event()`：

```python
from sikk.runtime.sikk_notifier import notify_event
```

```python
def emit_event(...):
    ...
    with EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"[{event['time']}] {event_type}: {message}")

    try:
        config = read_config()
        notify_event(event, config)
    except Exception as e:
        print(f"[notify error] {e}")
```

---

# 七、完整运行顺序

现在系统 loop 应该这样跑：

```text
run_once()
  ↓
read_config()
  ↓
discover_candidates()
  ↓
for token in candidates:
    should_process_token()
      ├─ no → TOKEN_SKIPPED + 使用旧状态进入 live_board
      └─ yes →
          run_external_modules_for_token()
            ├─ kline_signal
            ├─ wallet_structure
            ├─ quote
            ├─ security
            └─ paper_runner
          ↓
          build_token_status()
          ↓
          write_process_trace()
          ↓
          write_token_status_files()
          ↓
          emit_event()
  ↓
save_live_state()
  ↓
build_live_board.md
  ↓
write_live_dashboard.html
```

---

# 八、当前最优开发顺序

按这个顺序做：

```text
1. 新增 sikk_module_runner.py
2. 在 orchestrator 接入 run_external_modules_for_token()
3. 新增 sikk_trace_logger.py
4. 写 process_trace.jsonl
5. 新增 sikk_token_skip_policy.py
6. loop 接入跳过策略
7. 新增 sikk_dashboard_builder.py
8. 生成 live_dashboard.html
9. 新增 sikk_notifier.py
10. 最后开启 Discord / Telegram
```

---

# 九、最小验收标准

运行：

```bash
python -m sikk.runtime.sikk_live_orchestrator --mode once
```

必须看到：

```text
live_state.json
live_board.md
live_dashboard.html
events/live_events.jsonl
tokens/<token>/token_status.json
tokens/<token>/token_status.md
tokens/<token>/process_trace.jsonl
```

运行：

```bash
python -m sikk.runtime.sikk_live_orchestrator --mode loop --interval-sec 600
```

必须满足：

```text
PAPER_OPEN 每轮更新
BLOCKED 不会每轮重复跑
PAUSE 会降低频率
ERROR 会 30 分钟后重试
EXPIRED 不再频繁处理
```

---

# 十、直接给 Codex / OpenClaw 的任务提示词

```text
任务：实现 SIKK Live Runtime v0.2。

当前 Runtime v0.1 已能读取候选、生成 live_state.json、live_board.md、token_status.json/token_status.md、events/live_events.jsonl。

现在补齐 5 个工程能力：

一、实际调用模块
新增 sikk/runtime/sikk_module_runner.py。
实现 run_external_modules_for_token(token, config, force=False)。
按顺序调用：
1. kline_signal
2. wallet_structure
3. quote
4. security
5. paper_runner

每个模块支持：
- python_function
- script
- disabled

如果对应输出文件已存在，除 paper_runner 外可以跳过。
模块失败不能拖死整轮 loop，要返回 ERROR 结果并写事件。

二、状态轨迹
新增 sikk/runtime/sikk_trace_logger.py。
每个 token 写：
data/gmgn_candidates_live_run/tokens/<token>/process_trace.jsonl

每次状态更新记录：
- previous_state
- current_state
- previous_wallet_status
- current_wallet_status
- previous_paper_status
- current_paper_status
- latest_action
- latest_reason
- wallet_structure
- signal
- quote
- security
- paper
- module_result

注意：
写 trace 前先读取旧 token_status.json，然后再覆盖新 token_status.json。

三、loop 跳过策略
新增 sikk/runtime/sikk_token_skip_policy.py。
规则：
- PAPER_OPEN / PAPER_READY 每轮处理
- WATCHING 正常处理
- PAUSE 30 分钟冷却
- BLOCKED 6 小时冷却
- ERROR 30 分钟后重试
- EXPIRED / CLOSED 24 小时冷却或跳过
orchestrator 里对每个 token 先调用 should_process_token()。
如果跳过，写 TOKEN_SKIPPED 事件，并使用旧 token_status 进入 live_board。

四、HTML 看板
新增 sikk/runtime/sikk_dashboard_builder.py。
读取 live_state.json 和 events/live_events.jsonl。
输出：
data/gmgn_candidates_live_run/live_dashboard.html

展示：
- 状态数量卡片
- token 表格
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- signal / quote / security / paper
- PnL
- latest_reason
- 最新事件

五、通知器
新增 sikk/runtime/sikk_notifier.py。
支持 Discord webhook 和 Telegram bot。
只通知重要事件：
- WALLET_SUPPORT
- WALLET_BLOCK
- PAPER_READY
- PAPER_OPENED
- PAPER_FORCE_EXIT
- ERROR
- DAILY_REPORT_READY

在 emit_event() 中调用 notify_event(event, config)，但通知失败不能中断主程序。

验收：
运行 python -m sikk.runtime.sikk_live_orchestrator --mode once 后，必须生成：
- live_state.json
- live_board.md
- live_dashboard.html
- events/live_events.jsonl
- tokens/<token>/token_status.json
- tokens/<token>/token_status.md
- tokens/<token>/process_trace.jsonl

运行 loop 时：
- BLOCKED 不会每轮重复跑
- PAUSE 会降低频率
- PAPER_OPEN 会持续更新
- ERROR 会延迟重试
```

---

# 本次认知升级点

这一步把 SIKK 从“能生成状态文件”升级为：

```text
可持续运行
可跳过无效 token
可记录状态轨迹
可生成 HTML 控制台
可对重要事件外部播报
```

核心变化：

> 系统开始具备真正的 Runtime 能力，而不只是分析能力。

---

# 尚未解决问题

下一步最值得继续补：

```text
1. K线 / 钱包 / quote / security / paper 各模块的真实 CLI 参数统一
2. module_runner 如何识别模块输出是否过期
3. live_dashboard.html 增加状态筛选和搜索
4. paper runner 的持仓更新和 token skip 策略如何协调
5. confirmation ticket 如何接入 PAPER_READY → READY_FOR_CONFIRMATION
```


---

## 片段 41 / stream_idx=6110 / len=258


1. run_external_modules_for_token() 里如何实际调用 K线 / 钱包 / quote / security / paper 模块
2. live_board.md 转 live_dashboard.html 的静态网页版本
3. Discord / Telegram webhook 的实际配置方式
4. token_status.json 中状态变化如何写入 process_trace.jsonl
5. loop 模式下如何避免重复处理已经 BLOCKED 或已过期 token


---

## 片段 42 / stream_idx=6223 / len=34159


# SIKK Live Runtime v0.1：运行层接入方案

你现在缺的是这 5 个工程接缝：

```text
1. sikk_live_orchestrator.py 如何实际接入现有候选发现模块
2. token_status.json 如何合并 K线、钱包、quote、security、paper 数据
3. sikk_cli.py 的完整命令行代码
4. live_board.md 是否需要转成网页 dashboard
5. 是否要增加 Telegram / Discord / 微信机器人播报
```

结论先给：

> 现在不要先做复杂网页，也不要先做机器人。  
> 先做 **本地运行层 + 文件看板 + CLI 查看工具**。  
> 等它能稳定跑 24 小时，再加网页 dashboard 和机器人播报。

---

# 一、推荐新增目录

```text
sikk/
  runtime/
    __init__.py
    sikk_candidate_adapter.py
    sikk_status_builder.py
    sikk_event_logger.py
    sikk_live_orchestrator.py
    sikk_cli.py
```

数据目录：

```text
data/gmgn_candidates_live_run/
  candidates.json
  live_state.json
  live_board.md

  events/
    live_events.jsonl
    latest_events.md

  tokens/
    <token_address>/
      token_status.json
      token_status.md
      process_trace.jsonl

  wallet_structure/
    <token_address>/
      wallet_structure_decision.json
      snapshots/
        latest_snapshot.json
        latest_delta.json

  reports/
    daily_report.md
```

---

# 二、候选发现模块怎么接入 orchestrator

你的候选发现模块可能现在有几种形式：

```text
1. 已经输出 candidates.json
2. 是一个 Python 函数
3. 是一个独立脚本
4. 还只是手动导出的 CSV / JSON
```

所以不要把 orchestrator 写死。  
应该做一个 **候选适配器**。

---

## 1. 新增 `sikk_candidate_adapter.py`

路径：

```text
sikk/runtime/sikk_candidate_adapter.py
```

```python
from __future__ import annotations

import csv
import importlib
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


BASE_DIR = Path("data/gmgn_candidates_live_run")
DEFAULT_CANDIDATES_JSON = BASE_DIR / "candidates.json"
DEFAULT_CANDIDATES_CSV = BASE_DIR / "candidates.csv"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_candidate(row: Dict[str, Any]) -> Dict[str, Any]:
    """
    统一候选 token 字段。
    不管你的上游叫 address、token、ca、mint，最后都转成 token_address。
    """

    token_address = (
        row.get("token_address")
        or row.get("address")
        or row.get("ca")
        or row.get("mint")
        or row.get("token")
    )

    token_symbol = (
        row.get("token_symbol")
        or row.get("symbol")
        or row.get("ticker")
        or "UNKNOWN"
    )

    return {
        "token_address": token_address,
        "token_symbol": token_symbol,
        "price": row.get("price"),
        "market_cap": row.get("market_cap") or row.get("mc") or row.get("fdv"),
        "liquidity": row.get("liquidity") or row.get("pool_liquidity"),
        "holder_count": row.get("holder_count") or row.get("holders"),
        "pool_address": row.get("pool_address"),
        "open_time": row.get("open_time") or row.get("created_at"),
        "source": row.get("source") or "UNKNOWN",
        "raw": row,
    }


def load_candidates_from_json(path: Path = DEFAULT_CANDIDATES_JSON) -> List[Dict[str, Any]]:
    if not path.exists():
        return []

    data = read_json(path)

    if isinstance(data, dict):
        rows = data.get("candidates", [])
    elif isinstance(data, list):
        rows = data
    else:
        rows = []

    candidates = [normalize_candidate(dict(r)) for r in rows]
    return [c for c in candidates if c.get("token_address")]


def load_candidates_from_csv(path: Path = DEFAULT_CANDIDATES_CSV) -> List[Dict[str, Any]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = [dict(r) for r in csv.DictReader(f)]

    candidates = [normalize_candidate(r) for r in rows]
    return [c for c in candidates if c.get("token_address")]


def load_candidates_from_python_function(
    module_name: str,
    function_name: str,
) -> List[Dict[str, Any]]:
    """
    用法示例：
    module_name = "sikk.discovery.gmgn_candidate_discovery"
    function_name = "discover_candidates"
    """
    module = importlib.import_module(module_name)
    fn = getattr(module, function_name)

    rows = fn()

    if isinstance(rows, dict):
        rows = rows.get("candidates", [])

    candidates = [normalize_candidate(dict(r)) for r in rows]
    return [c for c in candidates if c.get("token_address")]


def run_discovery_script(
    script_path: str,
    output_path: Path = DEFAULT_CANDIDATES_JSON,
) -> List[Dict[str, Any]]:
    """
    适配独立候选发现脚本。
    要求脚本运行后输出 candidates.json。
    """
    subprocess.run(["python", script_path], check=True)

    if output_path.exists():
        return load_candidates_from_json(output_path)

    return []


def discover_candidates(config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    候选发现总入口。
    优先级：
    1. Python 函数
    2. 独立脚本
    3. candidates.json
    4. candidates.csv
    """

    config = config or {}

    provider = config.get("candidate_provider", "file_json")

    if provider == "python_function":
        return load_candidates_from_python_function(
            module_name=config["module_name"],
            function_name=config["function_name"],
        )

    if provider == "script":
        return run_discovery_script(
            script_path=config["script_path"],
            output_path=Path(config.get("output_path", DEFAULT_CANDIDATES_JSON)),
        )

    if provider == "file_csv":
        return load_candidates_from_csv(
            Path(config.get("path", DEFAULT_CANDIDATES_CSV))
        )

    # 默认 JSON
    return load_candidates_from_json(
        Path(config.get("path", DEFAULT_CANDIDATES_JSON))
    )
```

---

## 2. 配置文件建议

新建：

```text
config/sikk_runtime_config.json
```

第一版用文件模式：

```json
{
  "candidate_provider": "file_json",
  "path": "data/gmgn_candidates_live_run/candidates.json",
  "loop_interval_sec": 600,
  "paper_update_interval_sec": 180
}
```

如果你现有候选发现模块是 Python 函数：

```json
{
  "candidate_provider": "python_function",
  "module_name": "sikk.discovery.gmgn_candidate_discovery",
  "function_name": "discover_candidates",
  "loop_interval_sec": 600
}
```

如果是独立脚本：

```json
{
  "candidate_provider": "script",
  "script_path": "sikk_gmgn_candidate_discovery.py",
  "output_path": "data/gmgn_candidates_live_run/candidates.json",
  "loop_interval_sec": 600
}
```

---

# 三、`token_status.json` 如何合并 K线、钱包、quote、security、paper 数据

核心原则：

> 所有模块不直接互相强耦合，而是各自输出文件；`sikk_status_builder.py` 负责读取这些文件并合并成单币状态。

---

## 1. 推荐每个模块输出

```text
K线信号：
data/gmgn_candidates_live_run/signals/<token>/signal.json

钱包结构：
data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json

Quote：
data/gmgn_candidates_live_run/quotes/<token>/quote.json

Security：
data/gmgn_candidates_live_run/security/<token>/security.json

Paper：
data/gmgn_candidates_live_run/paper_positions.csv
```

---

## 2. 新增 `sikk_status_builder.py`

路径：

```text
sikk/runtime/sikk_status_builder.py
```

```python
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional


BASE_DIR = Path("data/gmgn_candidates_live_run")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json_optional(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_csv_rows(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def find_latest_paper_position(token_address: str) -> Dict[str, Any]:
    rows = read_csv_rows(BASE_DIR / "paper_positions.csv")

    token_rows = [
        r for r in rows
        if str(r.get("token_address")) == str(token_address)
    ]

    if not token_rows:
        return {}

    # 简单按 entry_time / updated_at 排序
    token_rows.sort(
        key=lambda r: r.get("updated_at") or r.get("entry_time") or "",
        reverse=True,
    )

    return token_rows[0]


def infer_current_state(
    signal: Mapping[str, Any],
    wallet: Mapping[str, Any],
    quote: Mapping[str, Any],
    security: Mapping[str, Any],
    paper: Mapping[str, Any],
) -> str:
    paper_status = str(paper.get("status") or paper.get("paper_status") or "").upper()

    if paper_status in {"OPEN", "PAPER_OPEN", "MANAGING"}:
        return "PAPER_OPEN"

    wallet_status = wallet.get("wallet_structure_status")
    if wallet_status == "WALLET_BLOCK":
        return "BLOCKED"

    if wallet_status == "WALLET_PAUSE":
        return "PAUSE"

    signal_gate = signal.get("signal_gate") or signal.get("gate")
    quote_gate = quote.get("quote_gate") or quote.get("gate")
    security_gate = security.get("security_gate") or security.get("gate")

    if (
        wallet_status == "WALLET_SUPPORT"
        and signal_gate == "ALLOW"
        and quote_gate == "ALLOW"
        and security_gate == "ALLOW"
    ):
        return "PAPER_READY"

    return "WATCHING"


def build_token_status(
    token=[REDACTED] Any],
    base_dir: Path = BASE_DIR,
) -> Dict[str, Any]:
    token_address = token["token_address"]
    token_symbol = token.get("token_symbol") or "UNKNOWN"

    signal = read_json_optional(base_dir / "signals" / token_address / "signal.json")
    wallet = read_json_optional(base_dir / "wallet_structure" / token_address / "wallet_structure_decision.json")
    quote = read_json_optional(base_dir / "quotes" / token_address / "quote.json")
    security = read_json_optional(base_dir / "security" / token_address / "security.json")
    paper = find_latest_paper_position(token_address)

    current_state = infer_current_state(signal, wallet, quote, security, paper)

    status = {
        "token_address": token_address,
        "token_symbol": token_symbol,
        "last_update": iso_now(),

        "current_state": current_state,

        "market": {
            "price": token.get("price") or quote.get("price") or quote.get("quote_price"),
            "market_cap": token.get("market_cap"),
            "liquidity": token.get("liquidity"),
            "holder_count": token.get("holder_count"),
            "pool_address": token.get("pool_address"),
            "source": token.get("source"),
        },

        "signal": {
            "signal_level": signal.get("signal_level"),
            "signal_type": signal.get("signal_type"),
            "signal_gate": signal.get("signal_gate") or signal.get("gate") or "UNKNOWN",
            "reason": signal.get("reason"),
            "control_box_high": signal.get("control_box_high"),
            "control_box_low": signal.get("control_box_low"),
            "invalid_level": signal.get("invalid_level"),
        },

        "wallet_structure": {
            "wallet_structure_status": wallet.get("wallet_structure_status", "MISSING"),
            "wallet_structure_score": wallet.get("wallet_structure_score"),
            "wallet_risk_score": wallet.get("wallet_risk_score"),
            "counterparty_pressure_score": wallet.get("counterparty_pressure_score"),
            "data_quality_score": wallet.get("data_quality_score"),
            "wallet_structure_factor": wallet.get("wallet_structure_factor"),
            "dominant_side_status": wallet.get("dominant_side_status"),
            "chip_transfer_status": wallet.get("chip_transfer_status"),
            "reason": wallet.get("reason"),
            "support_signals": wallet.get("support_signals", []),
            "risk_signals": wallet.get("risk_signals", []),
        },

        "quote": {
            "quote_gate": quote.get("quote_gate") or quote.get("gate") or "UNKNOWN",
            "okx_price": quote.get("okx_price"),
            "gmgn_price": quote.get("gmgn_price"),
            "pool_price": quote.get("pool_price"),
            "kline_close_price": quote.get("kline_close_price"),
            "price_deviation_pct": quote.get("price_deviation_pct"),
            "reason": quote.get("reason"),
        },

        "security": {
            "security_gate": security.get("security_gate") or security.get("gate") or "UNKNOWN",
            "risk_level": security.get("risk_level"),
            "risk_flags": security.get("risk_flags", []),
            "reason": security.get("reason"),
        },

        "paper": {
            "paper_status": paper.get("status") or paper.get("paper_status") or "NONE",
            "position_id": paper.get("position_id"),
            "entry_price": paper.get("entry_price"),
            "current_price": paper.get("current_price"),
            "unrealized_pnl_pct": paper.get("unrealized_pnl_pct"),
            "net_pnl_pct": paper.get("net_pnl_pct"),
            "max_floating_profit_pct": paper.get("max_floating_profit_pct"),
            "max_drawdown_pct": paper.get("max_drawdown_pct"),
            "exit_reason": paper.get("exit_reason"),
            "failure_type": paper.get("failure_type"),
        },

        "latest_action": infer_latest_action(current_state, wallet, quote, security, paper),
        "latest_reason": infer_latest_reason(current_state, wallet, quote, security, paper),
    }

    return status


def infer_latest_action(
    current_state: str,
    wallet: Mapping[str, Any],
    quote: Mapping[str, Any],
    security: Mapping[str, Any],
    paper: Mapping[str, Any],
) -> str:
    if current_state == "BLOCKED":
        return "NO_ENTRY"
    if current_state == "PAUSE":
        return "WAIT"
    if current_state == "PAPER_READY":
        return "READY_FOR_PAPER_ENTRY"
    if current_state == "PAPER_OPEN":
        return "MONITOR_POSITION"
    return "WATCH"


def infer_latest_reason(
    current_state: str,
    wallet: Mapping[str, Any],
    quote: Mapping[str, Any],
    security: Mapping[str, Any],
    paper: Mapping[str, Any],
) -> str:
    if current_state in {"BLOCKED", "PAUSE"}:
        return wallet.get("reason") or security.get("reason") or quote.get("reason") or "等待更多证据"

    if current_state == "PAPER_READY":
        return "signal / wallet / quote / security 已通过，允许纸面入场"

    if current_state == "PAPER_OPEN":
        return paper.get("exit_reason") or "纸面仓位监控中"

    return "观察中"


def write_token_status_files(status: Mapping[str, Any], base_dir: Path = BASE_DIR) -> None:
    token_address = status["token_address"]
    token_dir = base_dir / "tokens" / token_address

    write_json(token_dir / "token_status.json", status)
    write_text(token_dir / "token_status.md", render_token_status_md(status))


def render_token_status_md(status: Mapping[str, Any]) -> str:
    m = status.get("market", {})
    sig = status.get("signal", {})
    w = status.get("wallet_structure", {})
    q = status.get("quote", {})
    sec = status.get("security", {})
    p = status.get("paper", {})

    return f"""# ${status.get("token_symbol")} Token 状态

## 当前状态

- Token：{status.get("token_address")}
- 状态：{status.get("current_state")}
- 最新动作：{status.get("latest_action")}
- 原因：{status.get("latest_reason")}
- 更新时间：{status.get("last_update")}

## 市场

- 价格：{m.get("price")}
- 市值：{m.get("market_cap")}
- 池子：{m.get("liquidity")}
- 持有人：{m.get("holder_count")}
- 来源：{m.get("source")}

## K线 / 信号

- 信号等级：{sig.get("signal_level")}
- 信号类型：{sig.get("signal_type")}
- 信号门禁：{sig.get("signal_gate")}
- 失效位：{sig.get("invalid_level")}
- 原因：{sig.get("reason")}

## 钱包结构

- 钱包状态：{w.get("wallet_structure_status")}
- 结构分：{w.get("wallet_structure_score")}
- 风险分：{w.get("wallet_risk_score")}
- 对手盘压力：{w.get("counterparty_pressure_score")}
- 数据质量：{w.get("data_quality_score")}
- 主导侧状态：{w.get("dominant_side_status")}
- 筹码迁移：{w.get("chip_transfer_status")}
- 原因：{w.get("reason")}

### 支持信号

{chr(10).join([f"- {x}" for x in w.get("support_signals", [])]) or "- 无"}

### 风险信号

{chr(10).join([f"- {x}" for x in w.get("risk_signals", [])]) or "- 无"}

## Quote

- Quote 门禁：{q.get("quote_gate")}
- OKX：{q.get("okx_price")}
- GMGN：{q.get("gmgn_price")}
- 价格偏差：{q.get("price_deviation_pct")}
- 原因：{q.get("reason")}

## Security

- Security 门禁：{sec.get("security_gate")}
- 风险等级：{sec.get("risk_level")}
- 原因：{sec.get("reason")}

## Paper

- Paper 状态：{p.get("paper_status")}
- 仓位 ID：{p.get("position_id")}
- 入场价：{p.get("entry_price")}
- 当前价：{p.get("current_price")}
- 浮盈：{p.get("unrealized_pnl_pct")}
- 净收益：{p.get("net_pnl_pct")}
- 最大浮盈：{p.get("max_floating_profit_pct")}
- 最大回撤：{p.get("max_drawdown_pct")}
- 退出原因：{p.get("exit_reason")}
- 失败归因：{p.get("failure_type")}
"""
```

---

# 四、`sikk_live_orchestrator.py` 实际接入版本

路径：

```text
sikk/runtime/sikk_live_orchestrator.py
```

```python
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from sikk.runtime.sikk_candidate_adapter import discover_candidates
from sikk.runtime.sikk_status_builder import build_token_status, write_token_status_files


BASE_DIR = Path("data/gmgn_candidates_live_run")
CONFIG_PATH = Path("config/sikk_runtime_config.json")
EVENTS_PATH = BASE_DIR / "events" / "live_events.jsonl"
LIVE_STATE_PATH = BASE_DIR / "live_state.json"
LIVE_BOARD_PATH = BASE_DIR / "live_board.md"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_config() -> Dict[str, Any]:
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    return {
        "candidate_provider": "file_json",
        "path": str(BASE_DIR / "candidates.json"),
        "loop_interval_sec": 600
    }


def emit_event(
    event_type: str,
    message: str,
    token=[REDACTED] Any] | None = None,
    level: str = "INFO",
    data: Dict[str, Any] | None = None,
) -> None:
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "time": iso_now(),
        "event_type": event_type,
        "level": level,
        "token_address": token.get("token_address") if token else None,
        "token_symbol": token.get("token_symbol") if token else None,
        "message": message,
        "data": data or {},
    }

    with EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"[{event['time']}] {event_type}: {message}")


def run_external_modules_for_token(token=[REDACTED] Any]) -> None:
    """
    这里是接入点。
    v0.1 可以先不直接调用所有模块，只读取已有输出。
    v0.2 再逐步接：
    - K线信号模块
    - 钱包结构 pipeline
    - quote 模块
    - security 模块
    - paper runner
    """

    # 示例：
    # run_kline_signal_for_token(token)
    # run_candidate_wallet_structure_pipeline_for_one_token(token)
    # run_quote_gate_for_token(token)
    # run_security_gate_for_token(token)
    # update_paper_runner_for_token(token)

    return None


def run_token(token=[REDACTED] Any]) -> Dict[str, Any]:
    emit_event(
        "TOKEN_DISCOVERED",
        f"发现候选 {token.get('token_symbol')}，开始分析",
        token=[REDACTED]
        data=token,
    )

    try:
        run_external_modules_for_token(token)

        status = build_token_status(token)
        write_token_status_files(status)

        emit_event(
            "TOKEN_STATUS_UPDATED",
            f"{token.get('token_symbol')} 状态更新：{status.get('current_state')}",
            token=[REDACTED]
            data=status,
        )

        wallet_status = status.get("wallet_structure", {}).get("wallet_structure_status")
        if wallet_status in {"WALLET_SUPPORT", "WALLET_PAUSE", "WALLET_BLOCK"}:
            emit_event(
                wallet_status,
                f"{token.get('token_symbol')} 钱包结构：{wallet_status}，原因：{status.get('wallet_structure', {}).get('reason')}",
                token=[REDACTED]
                data=status.get("wallet_structure", {}),
            )

        return status

    except Exception as e:
        emit_event(
            "ERROR",
            f"{token.get('token_symbol')} 处理失败：{e}",
            token=[REDACTED]
            level="ERROR",
        )

        return {
            "token_address": token.get("token_address"),
            "token_symbol": token.get("token_symbol"),
            "current_state": "ERROR",
            "latest_reason": str(e),
            "last_update": iso_now(),
        }


def save_live_state(status_rows: List[Dict[str, Any]]) -> None:
    LIVE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)

    state = {
        "last_update": iso_now(),
        "token_count": len(status_rows),
        "tokens": status_rows,
    }

    LIVE_STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def build_live_board(status_rows: List[Dict[str, Any]]) -> None:
    lines = []

    lines.append("# SIKK-SOL Live Board")
    lines.append("")
    lines.append(f"更新时间：{iso_now()}")
    lines.append("")

    state_counts = {}
    for r in status_rows:
        st = r.get("current_state", "UNKNOWN")
        state_counts[st] = state_counts.get(st, 0) + 1

    lines.append("## 总览")
    lines.append("")
    lines.append(f"- Token 数：{len(status_rows)}")
    for st, count in sorted(state_counts.items()):
        lines.append(f"- {st}: {count}")

    lines.append("")
    lines.append("## 当前 Token 状态")
    lines.append("")
    lines.append("| Token | State | Wallet | Signal | Quote | Security | Paper | PnL | Reason |")
    lines.append("|---|---|---|---|---|---|---|---:|---|")

    for r in status_rows:
        token=[REDACTED]
        state = r.get("current_state")
        wallet = r.get("wallet_structure", {}).get("wallet_structure_status")
        signal = r.get("signal", {}).get("signal_gate")
        quote = r.get("quote", {}).get("quote_gate")
        security = r.get("security", {}).get("security_gate")
        paper = r.get("paper", {}).get("paper_status")
        pnl = r.get("paper", {}).get("unrealized_pnl_pct") or r.get("paper", {}).get("net_pnl_pct") or "-"
        reason = r.get("latest_reason")

        lines.append(
            f"| {token} | {state} | {wallet} | {signal} | {quote} | {security} | {paper} | {pnl} | {reason} |"
        )

    LIVE_BOARD_PATH.write_text("\n".join(lines), encoding="utf-8")


def run_once() -> List[Dict[str, Any]]:
    config = read_config()

    emit_event("RUN_STARTED", "SIKK-SOL 开始运行一轮")

    candidates = discover_candidates(config)
    emit_event("CANDIDATES_LOADED", f"读取候选 token 数：{len(candidates)}")

    status_rows = []

    for token in candidates:
        status_rows.append(run_token(token))

    save_live_state(status_rows)
    build_live_board(status_rows)

    emit_event("RUN_FINISHED", f"本轮结束，处理 token 数：{len(status_rows)}")

    return status_rows


def run_loop(interval_sec: int | None = None) -> None:
    config = read_config()
    interval = interval_sec or int(config.get("loop_interval_sec", 600))

    emit_event("RUN_STARTED", f"进入 loop 模式，每 {interval} 秒运行一次")

    while True:
        run_once()
        time.sleep(interval)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["once", "loop"], default="once")
    parser.add_argument("--interval-sec", type=int, default=None)

    args = parser.parse_args()

    if args.mode == "once":
        run_once()
    else:
        run_loop(args.interval_sec)


if __name__ == "__main__":
    main()
```

---

# 五、`sikk_cli.py` 完整命令行代码

路径：

```text
sikk/runtime/sikk_cli.py
```

运行方式：

```bash
python -m sikk.runtime.sikk_cli status
python -m sikk.runtime.sikk_cli events
python -m sikk.runtime.sikk_cli inspect TOKEN_ADDRESS
python -m sikk.runtime.sikk_cli board
python -m sikk.runtime.sikk_cli run-once
python -m sikk.runtime.sikk_cli loop
```

---

## 代码

```python
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path("data/gmgn_candidates_live_run")
LIVE_STATE_PATH = BASE_DIR / "live_state.json"
LIVE_BOARD_PATH = BASE_DIR / "live_board.md"
EVENTS_PATH = BASE_DIR / "events" / "live_events.jsonl"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_events(limit: int = 20) -> List[Dict[str, Any]]:
    if not EVENTS_PATH.exists():
        return []

    lines = EVENTS_PATH.read_text(encoding="utf-8").splitlines()
    lines = lines[-limit:]

    events = []
    for line in lines:
        try:
            events.append(json.loads(line))
        except Exception:
            continue

    return events


def cmd_status(args) -> None:
    if not LIVE_STATE_PATH.exists():
        print("没有 live_state.json。请先运行：python -m sikk.runtime.sikk_cli run-once")
        return

    state = read_json(LIVE_STATE_PATH)
    tokens = state.get("tokens", [])

    counts = {}
    for t in tokens:
        st = t.get("current_state", "UNKNOWN")
        counts[st] = counts.get(st, 0) + 1

    print("SIKK-SOL 当前状态")
    print("")
    print(f"最近更新：{state.get('last_update')}")
    print(f"Token 数：{state.get('token_count')}")
    print("")

    print("状态分布：")
    for st, count in sorted(counts.items()):
        print(f"- {st}: {count}")

    print("")
    print("最新事件：")
    for e in read_events(limit=5):
        print(f"[{e.get('time')}] {e.get('event_type')} | {e.get('token_symbol')} | {e.get('message')}")


def cmd_events(args) -> None:
    events = read_events(limit=args.limit)

    if not events:
        print("暂无事件。")
        return

    for e in events:
        print(f"[{e.get('time')}] {e.get('level')} {e.get('event_type')}")
        if e.get("token_symbol"):
            print(f"Token=[REDACTED] / {e.get('token_address')}")
        print(f"Message: {e.get('message')}")
        print("-" * 80)


def cmd_inspect(args) -> None:
    token=[REDACTED]
    path = BASE_DIR / "tokens" / token / "token_status.md"
    json_path = BASE_DIR / "tokens" / token / "token_status.json"

    if path.exists():
        print(path.read_text(encoding="utf-8"))
        return

    if json_path.exists():
        print(json.dumps(read_json(json_path), ensure_ascii=False, indent=2))
        return

    print(f"没有找到 token 状态：{token}")
    print(f"预期路径：{path}")


def cmd_board(args) -> None:
    if not LIVE_BOARD_PATH.exists():
        print("没有 live_board.md。请先运行 run-once。")
        return

    print(LIVE_BOARD_PATH.read_text(encoding="utf-8"))


def cmd_run_once(args) -> None:
    from sikk.runtime.sikk_live_orchestrator import run_once
    run_once()


def cmd_loop(args) -> None:
    from sikk.runtime.sikk_live_orchestrator import run_loop
    run_loop(interval_sec=args.interval_sec)


def cmd_paths(args) -> None:
    print("SIKK Runtime 关键路径")
    print("")
    print(f"Live State: {LIVE_STATE_PATH}")
    print(f"Live Board: {LIVE_BOARD_PATH}")
    print(f"Events: {EVENTS_PATH}")
    print(f"Tokens: {BASE_DIR / 'tokens'}")
    print(f"Wallet Structure: {BASE_DIR / 'wallet_structure'}")
    print(f"Reports: {BASE_DIR / 'reports'}")


def main() -> None:
    parser = argparse.ArgumentParser(prog="sikk-cli")
    sub = parser.add_subparsers(dest="command", required=True)

    p_status = sub.add_parser("status")
    p_status.set_defaults(func=cmd_status)

    p_events = sub.add_parser("events")
    p_events.add_argument("--limit", type=int, default=20)
    p_events.set_defaults(func=cmd_events)

    p_inspect = sub.add_parser("inspect")
    p_inspect.add_argument("token")
    p_inspect.set_defaults(func=cmd_inspect)

    p_board = sub.add_parser("board")
    p_board.set_defaults(func=cmd_board)

    p_run_once = sub.add_parser("run-once")
    p_run_once.set_defaults(func=cmd_run_once)

    p_loop = sub.add_parser("loop")
    p_loop.add_argument("--interval-sec", type=int, default=600)
    p_loop.set_defaults(func=cmd_loop)

    p_paths = sub.add_parser("paths")
    p_paths.set_defaults(func=cmd_paths)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
```

---

# 六、`live_board.md` 是否需要转成网页 dashboard？

## 当前阶段：不需要先做复杂网页

现在优先级应该是：

```text
1. live_board.md
2. token_status.md
3. sikk_cli.py
4. daily_report.md
5. 稳定跑 24 小时
```

不要一开始做复杂 dashboard。  
原因：

```text
网页好看，但不会提高判断质量。
现在最大问题是系统能不能稳定跑、能不能生成状态、能不能复盘。
```

---

## 什么时候做网页 dashboard？

满足下面条件后再做：

```text
1. loop 模式能连续运行 24 小时
2. 至少处理过 30 个 token
3. token_status.json 字段稳定
4. paper_positions.csv 字段稳定
5. live_board.md 已经能满足日常观察
```

---

## 网页 dashboard 的最低版本

后续可以做一个静态 HTML，不需要先上数据库服务。

输出：

```text
data/gmgn_candidates_live_run/live_dashboard.html
```

展示：

```text
Token 表格
状态筛选
WALLET_SUPPORT / PAUSE / BLOCK 颜色标记
Paper PnL
失败原因
最新事件
```

技术路线：

```text
Python 读取 live_state.json
生成一个静态 HTML
浏览器打开即可
```

不建议一开始上：

```text
FastAPI
React
复杂数据库面板
实时 websocket
```

这些后置。

---

# 七、是否增加 Telegram / Discord / 微信机器人播报？

## 结论

现在可以设计接口，但不要作为第一优先级。

优先顺序：

```text
1. 本地 event log
2. latest_events.md
3. CLI events
4. Discord / Telegram webhook
5. 微信机器人
```

---

## 为什么不先做微信？

微信机器人通常麻烦：

```text
企业微信 webhook
个人微信限制多
稳定性差
部署麻烦
容易被风控
```

更建议先用：

```text
Discord webhook
Telegram bot
```

但你当前最应该先把本地事件日志跑通。

---

## 播报分级

不是所有事件都播报，否则会刷屏。

建议只播报：

```text
TOKEN_DISCOVERED
WALLET_SUPPORT
WALLET_BLOCK
PAPER_READY
PAPER_OPENED
PAPER_FORCE_EXIT
ERROR
DAILY_REPORT_READY
```

不播报：

```text
每一次 quote 更新
每一次普通 WATCHING
每一次无变化 paper update
```

---

## 播报配置

```json
{
  "notification": {
    "enabled": false,
    "channels": ["discord"],
    "min_level": "IMPORTANT",
    "discord_webhook_url": "",
    "telegram_bot_token": "",
    "telegram_chat_id": ""
  }
}
```

---

## 后续通知器骨架

可以加：

```text
sikk/runtime/sikk_notifier.py
```

```python
from __future__ import annotations

import json
import urllib.request
from typing import Any, Dict


IMPORTANT_EVENTS = {
    "TOKEN_DISCOVERED",
    "WALLET_SUPPORT",
    "WALLET_BLOCK",
    "PAPER_READY",
    "PAPER_OPENED",
    "PAPER_FORCE_EXIT",
    "ERROR",
    "DAILY_REPORT_READY",
}


def should_notify(event: Dict[str, Any]) -> bool:
    return event.get("event_type") in IMPORTANT_EVENTS


def post_discord(webhook_url: str, text: str) -> None:
    payload = json.dumps({"content": text}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    urllib.request.urlopen(req, timeout=10)


def format_event_message(event: Dict[str, Any]) -> str:
    token_symbol = event.get("token_symbol") or "-"
    event_type = event.get("event_type")
    message = event.get("message")
    time = event.get("time")

    return f"[{time}] {event_type} | {token_symbol}\n{message}"


def notify_event(event: Dict[str, Any], config: Dict[str, Any]) -> None:
    notification = config.get("notification", {})

    if not notification.get("enabled"):
        return

    if not should_notify(event):
        return

    text = format_event_message(event)

    if "discord" in notification.get("channels", []):
        webhook_url = notification.get("discord_webhook_url")
        if webhook_url:
            post_discord(webhook_url, text)
```

在 `emit_event()` 里后续接：

```python
# notify_event(event, config)
```

---

# 八、现在最优开发顺序

现在按这个顺序做：

```text
1. 建 config/sikk_runtime_config.json
2. 建 sikk_candidate_adapter.py
3. 建 sikk_status_builder.py
4. 改 sikk_live_orchestrator.py
5. 建 sikk_cli.py
6. 先用 candidates.json 跑通 once
7. 再接真实候选发现模块
8. 再接钱包结构 / K线 / quote / security 输出
9. 再接 paper runner
10. 最后考虑 Discord / Telegram 播报
```

---

# 九、最小验收标准

你运行：

```bash
python -m sikk.runtime.sikk_live_orchestrator --mode once
```

必须生成：

```text
data/gmgn_candidates_live_run/live_state.json
data/gmgn_candidates_live_run/live_board.md
data/gmgn_candidates_live_run/events/live_events.jsonl
data/gmgn_candidates_live_run/tokens/<token>/token_status.json
data/gmgn_candidates_live_run/tokens/<token>/token_status.md
```

然后运行：

```bash
python -m sikk.runtime.sikk_cli status
```

能看到：

```text
最近更新
token 数
状态分布
最新事件
```

运行：

```bash
python -m sikk.runtime.sikk_cli board
```

能看到总览表。

运行：

```bash
python -m sikk.runtime.sikk_cli inspect TOKEN_ADDRESS
```

能看到某个 token 的详细状态。

这才说明系统开始“活起来”。

---

# 十、下一步给 AI / Codex 的任务提示词

```text
任务：实现 SIKK Live Runtime v0.1。

当前系统已有候选发现、K线信号、钱包结构门禁、quote/security、paper runner 等模块雏形，但缺少运行控制层和可观测层。

目标：
1. 系统可以自己跑一轮
2. 系统可以读取候选 token
3. 系统可以生成每个 token 的 token_status.json / token_status.md
4. 系统可以生成 live_board.md
5. 系统可以记录 live_events.jsonl
6. 系统可以通过 CLI 查看状态、事件、单币详情
7. 当前阶段先不做复杂网页 dashboard
8. 当前阶段先不接真实自动实盘

请新增文件：
- sikk/runtime/sikk_candidate_adapter.py
- sikk/runtime/sikk_status_builder.py
- sikk/runtime/sikk_live_orchestrator.py
- sikk/runtime/sikk_cli.py

候选发现适配：
支持三种模式：
1. file_json：读取 data/gmgn_candidates_live_run/candidates.json
2. file_csv：读取 data/gmgn_candidates_live_run/candidates.csv
3. python_function：从指定 module/function 调用候选发现
4. script：运行独立候选发现脚本后读取 candidates.json

token_status 合并：
读取以下模块输出：
- signals/<token>/signal.json
- wallet_structure/<token>/wallet_structure_decision.json
- quotes/<token>/quote.json
- security/<token>/security.json
- paper_positions.csv

为每个 token 输出：
- data/gmgn_candidates_live_run/tokens/<token>/token_status.json
- data/gmgn_candidates_live_run/tokens/<token>/token_status.md

live board：
输出：
- data/gmgn_candidates_live_run/live_board.md
- data/gmgn_candidates_live_run/live_state.json

事件日志：
输出：
- data/gmgn_candidates_live_run/events/live_events.jsonl

CLI 命令：
- status
- events
- inspect TOKEN_ADDRESS
- board
- run-once
- loop
- paths

验收：
运行 python -m sikk.runtime.sikk_live_orchestrator --mode once 后，必须生成 live_state.json、live_board.md、live_events.jsonl、token_status.json、token_status.md。
```

---

# 本次认知升级点

这一步的核心升级是：

> SIKK-SOL 不只是分析系统，还必须是运行系统。

现在系统要从：

```text
分析脚本集合
```

升级为：

```text
可运行、可观察、可查询、可复盘的 Live Runtime
```

关键新增能力：

```text
自动读取候选
自动生成单币状态
自动生成总览看板
自动记录事件
CLI 随时查看
后续可接机器人播报
```

---

# 尚未解决问题

下一步需要继续补：

```text
1. run_external_modules_for_token() 里如何实际调用 K线 / 钱包 / quote / security / paper 模块
2. live_board.md 转 live_dashboard.html 的静态网页版本
3. Discord / Telegram webhook 的实际配置方式
4. token_status.json 中状态变化如何写入 process_trace.jsonl
5. loop 模式下如何避免重复处理已经 BLOCKED 或已过期 token
```


---

## 片段 43 / stream_idx=6312 / len=197


1. sikk_live_orchestrator.py 如何实际接入现有候选发现模块
2. token_status.json 如何合并 K线、钱包、quote、security、paper 数据
3. sikk_cli.py 的完整命令行代码
4. live_board.md 是否需要转成网页 dashboard
5. 是否要增加 Telegram / Discord / 微信机器人播报


---

## 片段 44 / stream_idx=6431 / len=15139


你说得对。  
现在你的系统主要是在搭建“分析模块”，但还缺一个真正让系统活起来的部分：

> **运行控制层 + 可观测层 + 播报层**

没有这三层，就会出现你说的情况：

```text
不会自己运行
不知道发现了哪个代币
不知道流程跑到哪一步
不知道某个 token 当前是什么状态
不知道为什么进 / 不进 PAPER_READY
没有地方看实时结果
```

所以现在系统必须从“分析脚本集合”升级成：

> **SIKK-SOL 实时运行控制台系统**

---

# 一、当前真正缺的不是分析逻辑，而是运行系统

你现在已经设计了很多模块：

```text
候选发现
K线分析
钱包结构门禁
quote 检查
security 扫描
paper runner
失败归因
日报
```

但缺少一个主控：

```text
谁来定时调用这些模块？
谁来记录每一步发生了什么？
谁来告诉你发现了哪个 token？
谁来生成当前 token 状态？
谁来把结果显示出来？
```

所以现在最应该新增的是：

```text
sikk_live_orchestrator.py       主控运行器
sikk_event_logger.py            事件播报器
sikk_token_status_board.py      单币状态面板
sikk_cli.py                     命令行查看工具
```

---

# 二、新系统大局应该这样重建

```text
SIKK Live Orchestrator
  ↓
定时发现候选 token
  ↓
发现后写入事件日志
  ↓
对每个 token 跑：
  1. 候选过滤
  2. K线信号
  3. 钱包结构门禁
  4. quote 检查
  5. security 检查
  6. 状态机更新
  7. paper runner 更新
  ↓
每一步都写事件日志
  ↓
生成 token_status.json
  ↓
生成 live_board.md
  ↓
你可以随时查看：
  当前发现了什么 token
  每个 token 在哪个状态
  为什么被 BLOCK / PAUSE / PAPER_READY
  当前纸面仓位盈亏
```

---

# 三、需要新增的运行目录

建议统一到：

```text
data/gmgn_candidates_live_run/
```

里面增加：

```text
data/gmgn_candidates_live_run/
  live_state.json
  live_board.md

  events/
    live_events.jsonl
    latest_events.md

  tokens/
    <token_address>/
      token_status.json
      token_status.md
      process_trace.jsonl

  runs/
    run_20260502_120000.json
    latest_run.json

  reports/
    daily_report.md
    daily_wallet_structure_report.md
```

---

# 四、第一层：主控运行器

新增：

```text
sikk_live_orchestrator.py
```

它负责让系统自己跑起来。

---

## 4.1 运行模式

需要支持三种模式：

```bash
python sikk_live_orchestrator.py --mode once
python sikk_live_orchestrator.py --mode loop
python sikk_live_orchestrator.py --mode paper-update
```

含义：

| 模式 | 作用 |
|---|---|
| once | 手动跑一轮完整流程 |
| loop | 持续循环运行 |
| paper-update | 只更新纸面持仓 |

---

## 4.2 建议运行频率

```text
候选发现：每 10 分钟
K线 / 信号：每 10 分钟
钱包结构：每 10 分钟
quote / security：每 5 分钟
paper 持仓更新：每 3 分钟
日报：每天一次
```

---

## 4.3 主控流程

```text
run_cycle()
  ↓
discover_candidates()
  ↓
emit TOKEN_DISCOVERED
  ↓
for each token=[REDACTED]
    emit SIGNAL_CHECKED

    run_wallet_structure_gate()
    emit WALLET_GATE_RESULT

    run_quote_gate()
    emit QUOTE_CHECKED

    run_security_gate()
    emit SECURITY_CHECKED

    update_state_machine()
    emit STATE_CHANGED

    update_paper_runner()
    emit PAPER_UPDATED

    build_token_status()
    emit TOKEN_STATUS_UPDATED
  ↓
build_live_board()
```

---

# 五、第二层：事件播报器

新增：

```text
sikk_event_logger.py
```

它的作用是让系统“会说话”。

每发生一件事，都写入：

```text
data/gmgn_candidates_live_run/events/live_events.jsonl
```

---

## 5.1 事件类型

```text
RUN_STARTED
RUN_FINISHED

TOKEN_DISCOVERED
TOKEN_FILTERED_OUT
TOKEN_ACCEPTED

SIGNAL_DETECTED
SIGNAL_BLOCKED

WALLET_SUPPORT
WALLET_PAUSE
WALLET_BLOCK
WALLET_NEUTRAL

QUOTE_OK
QUOTE_FAIL
SECURITY_OK
SECURITY_BLOCK

STATE_CHANGED

PAPER_OPENED
PAPER_UPDATED
PAPER_EXIT_MONITOR
PAPER_FORCE_EXIT
PAPER_CLOSED

DAILY_REPORT_READY
ERROR
```

---

## 5.2 事件格式

```json
{
  "time": "2026-05-02T12:00:00Z",
  "event_type": "TOKEN_DISCOVERED",
  "token_address": "xxx",
  "token_symbol": "TEST",
  "level": "INFO",
  "message": "发现新候选 token TEST，市值 120000，池子 45000",
  "data": {
    "market_cap": 120000,
    "liquidity": 45000,
    "holder_count": 830
  }
}
```

---

## 5.3 播报文本示例

发现 token：

```text
[12:00:03] 发现候选：$TEST
市值：120K
池子：45K
持有人：830
状态：进入初筛
```

钱包门禁通过：

```text
[12:01:12] $TEST 钱包结构：WALLET_SUPPORT
结构分：72
风险分：28
对手盘压力：32
原因：早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出
```

钱包阻断：

```text
[12:02:44] $TEST 钱包结构：WALLET_BLOCK
原因：同源组同步卖出达到 76，早期钱包剩余筹码不足
动作：BLOCKED
```

paper 入场：

```text
[12:04:21] $TEST 进入 PAPER_READY
live_entry_price：0.000123
wallet_structure_factor：1.15
quote/security：通过
```

paper 强制退出：

```text
[12:19:02] $TEST 触发 FORCE_PAPER_EXIT
原因：对手盘压力从 38 上升到 74，疑似筹码向晚期承接方转移
归因：COUNTERPARTY_ABSORBING
```

---

# 六、第三层：单币状态面板

新增：

```text
sikk_token_status_board.py
```

每个 token 都要生成：

```text
data/gmgn_candidates_live_run/tokens/<token>/token_status.json
data/gmgn_candidates_live_run/tokens/<token>/token_status.md
```

---

## 6.1 token_status.json 标准

```json
{
  "token_address": "TOKEN_ADDRESS",
  "token_symbol": "TEST",
  "last_update": "2026-05-02T12:05:00Z",

  "current_state": "PAPER_READY",
  "previous_state": "WATCHING",

  "market": {
    "price": 0.000123,
    "market_cap": 120000,
    "liquidity": 45000,
    "holder_count": 830
  },

  "signal": {
    "signal_level": "S3",
    "signal_type": "CONTROL_BOX_BREAKOUT_PULLBACK",
    "signal_gate": "ALLOW",
    "reason": "控盘箱体突破后回踩未破"
  },

  "wallet_structure": {
    "wallet_structure_status": "WALLET_SUPPORT",
    "wallet_structure_score": 72,
    "wallet_risk_score": 28,
    "counterparty_pressure_score": 32,
    "data_quality_score": 76,
    "dominant_side_status": "STRUCTURE_HOLDING",
    "chip_transfer_status": "NO_MAJOR_TRANSFER",
    "reason": "早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出"
  },

  "quote": {
    "quote_gate": "ALLOW",
    "okx_price": 0.000123,
    "gmgn_price": 0.000122,
    "price_deviation_pct": 0.8
  },

  "security": {
    "security_gate": "ALLOW",
    "risk_level": "LOW"
  },

  "paper": {
    "paper_status": "OPEN",
    "entry_price": 0.000123,
    "current_price": 0.000131,
    "unrealized_pnl_pct": 6.5,
    "max_floating_profit_pct": 12.2,
    "max_drawdown_pct": -3.1
  },

  "latest_action": "HOLD",
  "latest_reason": "钱包结构未触发退出条件"
}
```

---

## 6.2 token_status.md 展示格式

```markdown
# $TEST Token 状态

## 当前状态

- 状态：PAPER_READY
- 上次更新：2026-05-02 12:05 UTC
- 最新动作：HOLD

## 市场数据

- 市值：120K
- 池子：45K
- 持有人：830
- 当前价格：0.000123

## SIKK 信号

- 信号等级：S3
- 信号类型：控盘箱体突破回踩
- 信号结论：ALLOW

## 钱包结构

- 钱包状态：WALLET_SUPPORT
- 结构分：72
- 风险分：28
- 对手盘压力：32
- 数据质量：76
- 主导侧状态：STRUCTURE_HOLDING
- 筹码迁移：NO_MAJOR_TRANSFER

原因：

早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出。

## Quote / Security

- Quote：ALLOW
- Security：ALLOW
- 价格偏差：0.8%

## Paper 仓位

- 入场价：0.000123
- 当前价：0.000131
- 浮盈：6.5%
- 最大浮盈：12.2%
- 最大回撤：-3.1%
```

---

# 七、第四层：总览看板

新增：

```text
data/gmgn_candidates_live_run/live_board.md
```

---

## 7.1 live_board.md 示例

```markdown
# SIKK-SOL Live Board

更新时间：2026-05-02 12:10 UTC

## 总览

- 本轮发现 token：12
- 通过初筛：5
- WALLET_SUPPORT：2
- WALLET_PAUSE：1
- WALLET_BLOCK：2
- PAPER_READY：1
- PAPER_OPEN：1
- BLOCKED：4

## 当前关注 token

| Token | State | Wallet | Signal | Quote | Security | Paper PnL | Reason |
|---|---|---|---|---|---|---:|---|
| TEST | PAPER_OPEN | SUPPORT | S3 | ALLOW | ALLOW | +6.5% | 结构维持 |
| AAA | PAUSE | PAUSE | S2 | ALLOW | ALLOW | - | 对手盘压力偏高 |
| BBB | BLOCKED | BLOCK | S3 | - | - | - | 同源组同步卖出 |
```

这个文件就是你每天最该看的“控制台”。

---

# 八、第五层：命令行查看工具

新增：

```text
sikk_cli.py
```

目标是让你可以直接问系统：

```bash
python sikk_cli.py status
python sikk_cli.py events
python sikk_cli.py inspect TOKEN_ADDRESS
python sikk_cli.py board
python sikk_cli.py run-once
python sikk_cli.py loop
```

---

## 8.1 命令含义

| 命令 | 作用 |
|---|---|
| status | 查看系统当前状态 |
| events | 查看最新事件 |
| inspect TOKEN | 查看某个 token 详情 |
| board | 打开 / 输出 live_board |
| run-once | 手动跑一轮 |
| loop | 持续运行 |
| paper | 更新纸面仓位 |

---

## 8.2 CLI 示例输出

```bash
python sikk_cli.py status
```

输出：

```text
SIKK-SOL 当前状态

运行模式：loop
最近一轮：2026-05-02 12:10 UTC
发现 token：12
WATCHING：5
PAPER_READY：1
PAPER_OPEN：1
PAUSE：2
BLOCKED：4

最新事件：
[12:09] $TEST PAPER_OPEN +6.5%
[12:08] $BBB WALLET_BLOCK，同源组同步卖出
[12:07] $AAA WALLET_PAUSE，对手盘压力 58
```

---

# 九、最小主控代码骨架

新增：

```text
sikk_live_orchestrator.py
```

```python
from __future__ import annotations

import time
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List


BASE_DIR = Path("data/gmgn_candidates_live_run")
EVENTS_PATH = BASE_DIR / "events" / "live_events.jsonl"
LIVE_STATE_PATH = BASE_DIR / "live_state.json"
LIVE_BOARD_PATH = BASE_DIR / "live_board.md"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit_event(event_type: str, message: str, token=[REDACTED] | None = None, level: str = "INFO", data: dict | None = None):
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    event = {
        "time": iso_now(),
        "event_type": event_type,
        "level": level,
        "token_address": token.get("token_address") if token else None,
        "token_symbol": token.get("token_symbol") if token else None,
        "message": message,
        "data": data or {},
    }

    with EVENTS_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")

    print(f"[{event['time']}] {event_type}: {message}")


def discover_candidates() -> List[Dict[str, Any]]:
    """
    这里接你的 GMGN 候选发现逻辑。
    v1.0 可以先读取 candidates.json。
    """
    path = BASE_DIR / "candidates.json"

    if not path.exists():
        emit_event("ERROR", "没有找到 candidates.json，候选发现为空", level="ERROR")
        return []

    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        return data.get("candidates", [])

    if isinstance(data, list):
        return data

    return []


def run_token_pipeline(token=[REDACTED] Any]) -> Dict[str, Any]:
    """
    这里应该接入：
    1. K线信号
    2. 钱包结构 pipeline
    3. quote gate
    4. security gate
    5. state machine
    6. paper runner
    """

    emit_event(
        "TOKEN_DISCOVERED",
        f"发现候选 {token.get('token_symbol')}，进入分析流程",
        token=[REDACTED]
        data=token,
    )

    # v1.0 占位状态
    status = {
        "token_address": token.get("token_address"),
        "token_symbol": token.get("token_symbol"),
        "current_state": "WATCHING",
        "wallet_structure_status": "UNKNOWN",
        "signal_gate": "UNKNOWN",
        "quote_gate": "UNKNOWN",
        "security_gate": "UNKNOWN",
        "paper_status": "NONE",
        "reason": "等待模块接入",
        "last_update": iso_now(),
    }

    # 后续这里实际调用：
    # run_candidate_wallet_structure_pipeline_for_one_token(token)
    # apply_wallet_structure_gate_to_state(...)
    # update_paper_position(...)

    write_token_status(token, status)

    return status


def write_token_status(token=[REDACTED] Any], status: Dict[str, Any]):
    token_address = token.get("token_address")
    token_dir = BASE_DIR / "tokens" / token_address
    token_dir.mkdir(parents=True, exist_ok=True)

    json_path = token_dir / "token_status.json"
    md_path = token_dir / "token_status.md"

    json_path.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")

    md = f"""# ${status.get('token_symbol')} 状态

- Token：{status.get('token_address')}
- 当前状态：{status.get('current_state')}
- 钱包结构：{status.get('wallet_structure_status')}
- Signal：{status.get('signal_gate')}
- Quote：{status.get('quote_gate')}
- Security：{status.get('security_gate')}
- Paper：{status.get('paper_status')}
- 原因：{status.get('reason')}
- 更新时间：{status.get('last_update')}
"""
    md_path.write_text(md, encoding="utf-8")


def build_live_board(status_rows: List[Dict[str, Any]]):
    lines = []
    lines.append("# SIKK-SOL Live Board")
    lines.append("")
    lines.append(f"更新时间：{iso_now()}")
    lines.append("")

    lines.append("## 当前 Token 状态")
    lines.append("")
    lines.append("| Token | State | Wallet | Signal | Quote | Security | Paper | Reason |")
    lines.append("|---|---|---|---|---|---|---|---|")

    for r in status_rows:
        lines.append(
            f"| {r.get('token_symbol')} "
            f"| {r.get('current_state')} "
            f"| {r.get('wallet_structure_status')} "
            f"| {r.get('signal_gate')} "
            f"| {r.get('quote_gate')} "
            f"| {r.get('security_gate')} "
            f"| {r.get('paper_status')} "
            f"| {r.get('reason')} |"
        )

    LIVE_BOARD_PATH.write_text("\n".join(lines), encoding="utf-8")


def save_live_state(status_rows: List[Dict[str, Any]]):
    state = {
        "last_update": iso_now(),
        "token_count": len(status_rows),
        "tokens": status_rows,
    }
    LIVE_STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def run_once():
    emit_event("RUN_STARTED", "SIKK-SOL 开始运行一轮")

    candidates = discover_candidates()
    status_rows = []

    for token in candidates:
        try:
            status = run_token_pipeline(token)
            status_rows.append(status)
        except Exception as e:
            emit_event(
                "ERROR",
                f"{token.get('token_symbol')} 处理失败：{e}",
                token=[REDACTED]
                level="ERROR",
            )

    build_live_board(status_rows)
    save_live_state(status_rows)

    emit_event("RUN_FINISHED", f"本轮结束，处理 token 数：{len(status_rows)}")


def run_loop(interval_sec: int = 600):
    emit_event("RUN_STARTED", f"进入 loop 模式，每 {interval_sec} 秒运行一次")

    while True:
        run_once()
        time.sleep(interval_sec)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["once", "loop"], default="once")
    parser.add_argument("--interval-sec", type=int, default=600)

    args = parser.parse_args()

    if args.mode == "once":
        run_once()
    else:
        run_loop(args.interval_sec)
```

---

# 十、你现在应该怎么改系统

现在不是继续加分析规则，而是先补这 5 个运行能力。

## 第 1 步：先让它能跑一轮

```bash
python sikk_live_orchestrator.py --mode once
```

必须输出：

```text
live_events.jsonl
live_state.json
live_board.md
tokens/<token>/token_status.json
tokens/<token>/token_status.md
```

---

## 第 2 步：让它能持续跑

```bash
python sikk_live_orchestrator.py --mode loop --interval-sec 600
```

这样每 10 分钟跑一次。

---

## 第 3 步：让它会播报

每个阶段都必须 `emit_event()`：

```text
发现 token
K线信号
钱包结构结果
quote 结果
security 结果
状态变化
paper 入场
paper 退出
失败归因
```

---

## 第 4 步：让你能看某个 token

每个 token 必须生成：

```text
token_status.json
token_status.md
```

你以后就看这个文件：

```text
data/gmgn_candidates_live_run/tokens/<token>/token_status.md
```

---

## 第 5 步：让你看总览

每天主要看：

```text
data/gmgn_candidates_live_run/live_board.md
```

这个就是你的系统看板。

---

# 十一、现在的系统阶段重新定义

你现在不是缺“更复杂的庄家判断”。  
你缺的是：

```text
自动调度
事件播报
状态可视化
单币状态追踪
结果看板
```

所以当前阶段应该从：

```text
钱包结构门禁开发
```

升级为：

```text
SIKK Live Runtime v0.1
```

目标是：

```text
系统可以自己跑
系统可以播报发现了什么 token
系统可以告诉你每个 token 当前状态
系统可以保存每一步判断过程
系统可以让你复盘为什么进 / 不进
```

---

# 十二、最小验收标准

只要实现下面这些，就算运行层 v0.1 成立：

```text
1. python sikk_live_orchestrator.py --mode once 可以跑一轮
2. 发现 token 后写入 TOKEN_DISCOVERED 事件
3. 每个 token 生成 token_status.json
4. 每个 token 生成 token_status.md
5. 总览生成 live_board.md
6. 钱包结构状态写入 token_status
7. 状态机状态写入 token_status
8. paper 状态写入 token_status
9. 出错时写 ERROR 事件
10. loop 模式可以每 10 分钟运行一次
```

---

# 十三、最终结论

你现在的问题判断正确：

> 当前系统只有分析骨架，还没有“自动运行与可观测控制台”。

下一步最优先不是继续细化钱包分类，而是新增：

```text
sikk_live_orchestrator.py
sikk_event_logger.py
sikk_token_status_board.py
sikk_cli.py
live_board.md
token_status.md
live_events.jsonl
```

这样系统才会真正从：

```text
一堆分析脚本
```

变成：

```text
可以自己跑、会播报、能查看状态、能复盘原因的 SIKK Live Runtime
```

---

# 本次认知升级点

核心升级：

> SIKK-SOL 不能只做“分析正确”，还必须做到“运行可见”。

真正可用的交易系统必须同时具备：

```text
分析能力
运行能力
播报能力
状态可视化能力
复盘能力
```

现在缺的是后四个。

---

# 尚未解决问题

下一步需要继续补：

```text
1. sikk_live_orchestrator.py 如何实际接入现有候选发现模块
2. token_status.json 如何合并 K线、钱包、quote、security、paper 数据
3. sikk_cli.py 的完整命令行代码
4. live_board.md 是否需要转成网页 dashboard
5. 是否要增加 Telegram / Discord / 微信机器人播报
```


---

## 片段 45 / stream_idx=6622 / len=51621


# SIKK-SOL v1.0 钱包结构层：5 个工程接缝补全

下面按可落地顺序处理：

```text
1. same_source_group_id 实际生成代码
2. pipeline 如何读取 sikk_gmgn_token_report.py 输出
3. snapshots / delta 文件生成逻辑
4. paper runner 的 FORCE_PAPER_EXIT 策略
5. daily_report 如何统计钱包结构状态下的胜率和收益
```

---

# 0. 建议新增文件

建议加 3 个文件：

```text
sikk/wallet_structure/sikk_same_source_group.py
sikk/wallet_structure/sikk_wallet_snapshot.py
sikk/reporting/sikk_wallet_structure_daily_report.py
```

当前目录：

```text
sikk/
  wallet_structure/
    sikk_wallet_structure_gate.py
    sikk_candidate_wallet_structure_pipeline.py
    sikk_same_source_group.py
    sikk_wallet_snapshot.py

  reporting/
    sikk_wallet_structure_daily_report.py
```

---

# 1. `same_source_group_id` 的实际生成代码

新建：

```text
sikk/wallet_structure/sikk_same_source_group.py
```

## 1.1 功能

它负责：

```text
输入：wallet_rows
输出：
1. 给每个钱包补 same_source_group_id
2. 生成 candidate_groups.csv 需要的 group rows
3. 计算 sync_buy_score
4. 计算 sync_sell_score
```

---

## 1.2 代码

```python
from __future__ import annotations

import hashlib
import math
from collections import defaultdict, deque
from datetime import datetime, timezone
from statistics import mean, pstdev
from typing import Any, Dict, List, Mapping, Optional, Tuple


LOW_RELIABILITY_SOURCE_KEYWORDS = {
    "okx", "binance", "bybit", "coinbase", "kucoin", "gate", "mexc",
    "cex", "exchange",
    "jupiter", "raydium", "orca", "meteora", "router", "aggregator",
}


def n(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def s(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def parse_time(value: Any) -> Optional[datetime]:
    if value in (None, "", "null", "None"):
        return None

    if isinstance(value, datetime):
        return value

    text = str(value).strip()

    # 支持 ISO 格式
    try:
        if text.endswith("Z"):
            text = text.replace("Z", "+00:00")
        return datetime.fromisoformat(text)
    except ValueError:
        pass

    # 支持 Unix 秒
    try:
        ts = float(text)
        if ts > 10_000_000_000:
            ts = ts / 1000
        return datetime.fromtimestamp(ts, tz=timezone.utc)
    except ValueError:
        return None


def seconds_between(a: Any, b: Any, default: float = 999999.0) -> float:
    ta = parse_time(a)
    tb = parse_time(b)
    if not ta or not tb:
        return default
    return abs((ta - tb).total_seconds())


def coefficient_of_variation(values: List[float]) -> float:
    values = [v for v in values if v is not None]
    if not values:
        return 999.0
    avg = mean(values)
    if avg == 0:
        return 999.0
    if len(values) == 1:
        return 0.0
    return pstdev(values) / avg


def relative_diff(a: float, b: float) -> float:
    denom = max(abs(a), abs(b), 1e-9)
    return abs(a - b) / denom


def source_reliability(row: Mapping[str, Any]) -> str:
    label = s(row.get("funding_source_label")).lower()
    address = s(row.get("funding_source_address")).lower()

    joined = f"{label} {address}"

    if not label and not address:
        return "UNKNOWN"

    if any(k in joined for k in LOW_RELIABILITY_SOURCE_KEYWORDS):
        return "LOW"

    if address:
        return "HIGH"

    if label:
        return "MEDIUM"

    return "UNKNOWN"


def group_hash(token_symbol: str, token_address: str, seed: str) -> str:
    raw = f"{token_symbol}|{token_address}|{seed}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:6]


def same_source_similarity(a: Mapping[str, Any], b: Mapping[str, Any]) -> float:
    """
    钱包两两相似度，满分 100。
    v1.0 只做可运行近似，不做最终身份定性。
    """

    score = 0.0

    a_source = s(a.get("funding_source_address")).lower()
    b_source = s(b.get("funding_source_address")).lower()

    a_label = s(a.get("funding_source_label")).lower()
    b_label = s(b.get("funding_source_label")).lower()

    a_rel = source_reliability(a)
    b_rel = source_reliability(b)

    # 1. funding_source_address 相同：40
    if a_source and b_source and a_source == b_source:
        if a_rel == "LOW" or b_rel == "LOW":
            score += 10
        else:
            score += 40
    elif a_label and b_label and a_label == b_label and a_rel != "LOW" and b_rel != "LOW":
        score += 20

    # 2. funding_time 接近：15
    funding_time_diff = seconds_between(
        a.get("first_funding_time"),
        b.get("first_funding_time"),
    )
    if funding_time_diff <= 10 * 60:
        score += 15
    elif funding_time_diff <= 30 * 60:
        score += 8
    elif funding_time_diff <= 2 * 60 * 60:
        score += 3

    # 3. funding_amount 相近：10
    a_fund_amt = n(a.get("first_funding_amount_sol"))
    b_fund_amt = n(b.get("first_funding_amount_sol"))
    if a_fund_amt > 0 and b_fund_amt > 0:
        rd = relative_diff(a_fund_amt, b_fund_amt)
        if rd <= 0.25:
            score += 10
        elif rd <= 0.50:
            score += 5

    # 4. entry_time 接近：15
    entry_time_diff = seconds_between(a.get("entry_time"), b.get("entry_time"))
    if entry_time_diff <= 30:
        score += 15
    elif entry_time_diff <= 2 * 60:
        score += 10
    elif entry_time_diff <= 5 * 60:
        score += 5

    # 5. buy_amount 相近：10
    a_buy = n(a.get("buy_amount_usd"))
    b_buy = n(b.get("buy_amount_usd"))
    if a_buy > 0 and b_buy > 0:
        rd = relative_diff(a_buy, b_buy)
        if rd <= 0.25:
            score += 10
        elif rd <= 0.50:
            score += 5

    # 6. sell / hold 行为相似：10
    sold_diff = abs(n(a.get("sold_pct")) - n(b.get("sold_pct")))
    remain_diff = abs(n(a.get("remaining_pct")) - n(b.get("remaining_pct")))

    if sold_diff <= 10 and remain_diff <= 10:
        score += 10
    elif sold_diff <= 25 and remain_diff <= 25:
        score += 5

    return min(score, 100.0)


def build_similarity_graph(wallet_rows: List[Dict[str, Any]], threshold: float = 70.0) -> Dict[int, List[int]]:
    graph: Dict[int, List[int]] = defaultdict(list)

    for i in range(len(wallet_rows)):
        for j in range(i + 1, len(wallet_rows)):
            sim = same_source_similarity(wallet_rows[i], wallet_rows[j])
            wallet_rows[i].setdefault("pair_similarity", {})
            wallet_rows[j].setdefault("pair_similarity", {})
            wallet_rows[i]["pair_similarity"][s(wallet_rows[j].get("wallet_address") or wallet_rows[j].get("address"))] = sim
            wallet_rows[j]["pair_similarity"][s(wallet_rows[i].get("wallet_address") or wallet_rows[i].get("address"))] = sim

            if sim >= threshold:
                graph[i].append(j)
                graph[j].append(i)

    return graph


def connected_components(graph: Dict[int, List[int]], n_nodes: int) -> List[List[int]]:
    visited = set()
    components: List[List[int]] = []

    for i in range(n_nodes):
        if i in visited:
            continue

        q = deque([i])
        visited.add(i)
        comp = []

        while q:
            cur = q.popleft()
            comp.append(cur)

            for nxt in graph.get(cur, []):
                if nxt not in visited:
                    visited.add(nxt)
                    q.append(nxt)

        components.append(comp)

    return components


def compute_sync_buy_score(group_rows: List[Mapping[str, Any]], group_type: str) -> Tuple[float, Dict[str, float]]:
    group_size = len(group_rows)
    if group_size == 0:
        return 0.0, {}

    entry_times = [r.get("entry_time") for r in group_rows if r.get("entry_time")]
    parsed_times = [parse_time(t) for t in entry_times if parse_time(t)]

    if len(parsed_times) >= 2:
        span_sec = (max(parsed_times) - min(parsed_times)).total_seconds()
    else:
        span_sec = 999999

    if span_sec <= 30:
        buy_time_cohesion_score = 30
    elif span_sec <= 2 * 60:
        buy_time_cohesion_score = 24
    elif span_sec <= 5 * 60:
        buy_time_cohesion_score = 16
    elif span_sec <= 10 * 60:
        buy_time_cohesion_score = 8
    else:
        buy_time_cohesion_score = 0

    ranks = [n(r.get("entry_rank"), 999999) for r in group_rows]
    rank_span = max(ranks) - min(ranks) if ranks else 999999

    if rank_span <= 10:
        entry_rank_cohesion_score = 20
    elif rank_span <= 25:
        entry_rank_cohesion_score = 15
    elif rank_span <= 50:
        entry_rank_cohesion_score = 8
    else:
        entry_rank_cohesion_score = 0

    buy_amounts = [n(r.get("buy_amount_usd")) for r in group_rows if n(r.get("buy_amount_usd")) > 0]
    cv = coefficient_of_variation(buy_amounts)

    if cv <= 0.25:
        buy_amount_similarity_score = 15
    elif cv <= 0.50:
        buy_amount_similarity_score = 10
    elif cv <= 1.00:
        buy_amount_similarity_score = 5
    else:
        buy_amount_similarity_score = 0

    buy_participation_ratio = len(buy_amounts) / group_size

    if buy_participation_ratio >= 0.9:
        buy_participation_score = 20
    elif buy_participation_ratio >= 0.7:
        buy_participation_score = 14
    elif buy_participation_ratio >= 0.5:
        buy_participation_score = 8
    else:
        buy_participation_score = 0

    if group_type == "FUNDING_STRONG_GROUP":
        funding_support_score = 15
    elif group_type == "FUNDING_WEAK_GROUP":
        funding_support_score = 8
    elif group_type == "BEHAVIOR_SYNC_GROUP":
        funding_support_score = 3
    else:
        funding_support_score = 0

    breakdown = {
        "buy_time_cohesion_score": buy_time_cohesion_score,
        "entry_rank_cohesion_score": entry_rank_cohesion_score,
        "buy_amount_similarity_score": buy_amount_similarity_score,
        "buy_participation_score": buy_participation_score,
        "funding_support_score": funding_support_score,
    }

    return sum(breakdown.values()), breakdown


def compute_sync_sell_score(group_rows: List[Mapping[str, Any]]) -> Tuple[float, Dict[str, float]]:
    group_size = len(group_rows)
    if group_size == 0:
        return 0.0, {}

    sell_rows = [r for r in group_rows if n(r.get("sold_pct")) >= 20]

    sell_times = [
        parse_time(r.get("first_major_sell_time") or r.get("last_sell_time") or r.get("last_trade_time"))
        for r in sell_rows
    ]
    sell_times = [t for t in sell_times if t]

    if len(sell_times) >= 2:
        span_sec = (max(sell_times) - min(sell_times)).total_seconds()
    else:
        span_sec = 999999

    if span_sec <= 60:
        sell_time_cohesion_score = 30
    elif span_sec <= 5 * 60:
        sell_time_cohesion_score = 22
    elif span_sec <= 15 * 60:
        sell_time_cohesion_score = 12
    elif span_sec <= 30 * 60:
        sell_time_cohesion_score = 6
    else:
        sell_time_cohesion_score = 0

    sell_participation_ratio = len(sell_rows) / group_size

    if sell_participation_ratio >= 0.9:
        sell_participation_score = 25
    elif sell_participation_ratio >= 0.7:
        sell_participation_score = 18
    elif sell_participation_ratio >= 0.5:
        sell_participation_score = 10
    else:
        sell_participation_score = 0

    sold_values = [n(r.get("sold_pct")) for r in sell_rows if n(r.get("sold_pct")) > 0]
    cv = coefficient_of_variation(sold_values)

    if cv <= 0.25:
        sold_pct_similarity_score = 15
    elif cv <= 0.50:
        sold_pct_similarity_score = 10
    elif cv <= 1.00:
        sold_pct_similarity_score = 5
    else:
        sold_pct_similarity_score = 0

    total_buy = sum(n(r.get("buy_amount_usd")) for r in group_rows)
    total_sell = sum(n(r.get("sell_amount_usd")) for r in group_rows)

    group_sold_pct = (total_sell / total_buy * 100) if total_buy > 0 else 0

    if group_sold_pct >= 80:
        group_exit_pressure_score = 20
    elif group_sold_pct >= 60:
        group_exit_pressure_score = 15
    elif group_sold_pct >= 40:
        group_exit_pressure_score = 8
    else:
        group_exit_pressure_score = 0

    top_holder_exit_bonus = 0
    for r in group_rows:
        is_top_holder = str(r.get("is_top_holder")).lower() in {"true", "1", "yes"}
        sold_pct = n(r.get("sold_pct"))
        if is_top_holder and sold_pct >= 60:
            top_holder_exit_bonus = 10
            break
        if is_top_holder and sold_pct >= 30:
            top_holder_exit_bonus = max(top_holder_exit_bonus, 5)

    breakdown = {
        "sell_time_cohesion_score": sell_time_cohesion_score,
        "sell_participation_score": sell_participation_score,
        "sold_pct_similarity_score": sold_pct_similarity_score,
        "group_exit_pressure_score": group_exit_pressure_score,
        "top_holder_exit_bonus": top_holder_exit_bonus,
    }

    return sum(breakdown.values()), breakdown


def infer_group_type(group_rows: List[Mapping[str, Any]]) -> Tuple[str, str]:
    reliabilities = [source_reliability(r) for r in group_rows]

    source_addresses = [
        s(r.get("funding_source_address")).lower()
        for r in group_rows
        if s(r.get("funding_source_address"))
    ]

    unique_sources = set(source_addresses)

    if unique_sources and len(unique_sources) == 1:
        if "LOW" in reliabilities:
            return "CEX_AMBIGUOUS_GROUP", "相同资金来源但来源可靠性低，可能是 CEX/路由器/公共地址"
        return "FUNDING_STRONG_GROUP", "多个钱包来自同一非公共资金源"

    if "HIGH" in reliabilities or "MEDIUM" in reliabilities:
        return "FUNDING_WEAK_GROUP", "资金来源存在相似性，但不能确认强同源"

    return "BEHAVIOR_SYNC_GROUP", "资金来源不清晰，但买卖行为高度同步"


def apply_same_source_groups(
    token_address: str,
    token_symbol: str,
    wallet_rows: List[Dict[str, Any]],
    similarity_threshold: float = 70.0,
    min_group_size: int = 3,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    给 wallet_rows 写入 same_source_group_id / sync_buy_score / sync_sell_score。
    返回：
    - updated wallet_rows
    - candidate_groups rows
    """

    if not wallet_rows:
        return wallet_rows, []

    graph = build_similarity_graph(wallet_rows, threshold=similarity_threshold)
    components = connected_components(graph, len(wallet_rows))

    candidate_groups: List[Dict[str, Any]] = []

    for comp in components:
        if len(comp) < min_group_size:
            continue

        group_rows = [wallet_rows[i] for i in comp]
        group_type, primary_evidence = infer_group_type(group_rows)

        first_entry_time = min(
            [parse_time(r.get("entry_time")) for r in group_rows if parse_time(r.get("entry_time"))],
            default=None,
        )

        primary_source = s(group_rows[0].get("funding_source_address") or group_rows[0].get("funding_source_label"))
        seed = f"{primary_source}|{first_entry_time}"
        group_id = f"SSG_{token_symbol}_{group_hash(token_symbol, token_address, seed)}"

        sync_buy_score, buy_breakdown = compute_sync_buy_score(group_rows, group_type)
        sync_sell_score, sell_breakdown = compute_sync_sell_score(group_rows)

        buy_amounts = [n(r.get("buy_amount_usd")) for r in group_rows if n(r.get("buy_amount_usd")) > 0]
        avg_buy_amount_usd = mean(buy_amounts) if buy_amounts else 0
        buy_amount_cv = coefficient_of_variation(buy_amounts)

        entry_ranks = [n(r.get("entry_rank"), 999999) for r in group_rows]
        avg_entry_rank = mean(entry_ranks) if entry_ranks else 0

        entry_times = [parse_time(r.get("entry_time")) for r in group_rows if parse_time(r.get("entry_time"))]
        if len(entry_times) >= 2:
            entry_time_span_sec = (max(entry_times) - min(entry_times)).total_seconds()
        else:
            entry_time_span_sec = 0

        total_buy = sum(n(r.get("buy_amount_usd")) for r in group_rows)
        total_sell = sum(n(r.get("sell_amount_usd")) for r in group_rows)
        group_sold_pct = total_sell / total_buy * 100 if total_buy > 0 else 0
        group_remaining_pct = max(0, 100 - group_sold_pct)

        if sync_sell_score >= 70:
            group_risk_level = "HIGH"
        elif sync_sell_score >= 50:
            group_risk_level = "MEDIUM"
        else:
            group_risk_level = "LOW"

        if group_type == "FUNDING_STRONG_GROUP" and sync_buy_score >= 70:
            group_evidence_level = "E3"
        elif sync_buy_score >= 60 or sync_sell_score >= 60:
            group_evidence_level = "E2"
        else:
            group_evidence_level = "E1"

        wallets = []
        for idx in comp:
            wallet_address = s(wallet_rows[idx].get("wallet_address") or wallet_rows[idx].get("address"))
            wallets.append(wallet_address)

            wallet_rows[idx]["same_source_group_id"] = group_id
            wallet_rows[idx]["same_source_group_size"] = len(group_rows)
            wallet_rows[idx]["sync_buy_score"] = sync_buy_score
            wallet_rows[idx]["sync_sell_score"] = sync_sell_score
            wallet_rows[idx]["same_source_group_type"] = group_type
            wallet_rows[idx]["source_reliability"] = source_reliability(wallet_rows[idx])

        candidate_groups.append({
            "token_address": token_address,
            "group_id": group_id,
            "group_type": group_type,
            "group_size": len(group_rows),
            "wallets": ",".join(wallets),
            "primary_evidence": primary_evidence,
            "source_reliability": ",".join(sorted(set(source_reliability(r) for r in group_rows))),
            "avg_entry_rank": round(avg_entry_rank, 2),
            "entry_time_span_sec": round(entry_time_span_sec, 2),
            "avg_buy_amount_usd": round(avg_buy_amount_usd, 2),
            "buy_amount_cv": round(buy_amount_cv, 4),
            "sync_buy_score": round(sync_buy_score, 2),
            "sync_sell_score": round(sync_sell_score, 2),
            "group_remaining_pct": round(group_remaining_pct, 2),
            "group_sold_pct": round(group_sold_pct, 2),
            "group_risk_level": group_risk_level,
            "group_evidence_level": group_evidence_level,
            "reason": primary_evidence,
            "sync_buy_breakdown": buy_breakdown,
            "sync_sell_breakdown": sell_breakdown,
        })

    return wallet_rows, candidate_groups
```

---

# 2. pipeline 如何读取 `sikk_gmgn_token_report.py` 输出

你现有 `sikk_gmgn_token_report.py` 是单币钱包结构报告。  
现在 pipeline 不应该重复抓取逻辑，而应该优先读取它的输出。

## 2.1 推荐约定

让 `sikk_gmgn_token_report.py` 每个 token 输出到：

```text
data/gmgn_candidates_live_run/wallet_structure/<token_address>/
```

至少输出：

```text
early_wallet_raw.csv
wallet_classification.csv    # 可选，pipeline 也能重新 classify
candidate_groups.csv         # 可选，pipeline 也能重新生成
gmgn_note_table.csv          # 可选
token_report.json            # 可选
```

pipeline 优先读取：

```text
<token>/early_wallet_raw.csv
```

如果没有，再找：

```text
<token>/wallet_classification.csv
<token>/holders.csv
<token>/top_holders.csv
<token>/wallets.csv
```

---

## 2.2 修改 `sikk_candidate_wallet_structure_pipeline.py`

在之前的 pipeline 里替换 `fetch_or_load_token_wallet_raw()`。

```python
import csv
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional


PROJECT_ROOT = Path(".")
DEFAULT_OUTPUT_DIR = Path("data/gmgn_candidates_live_run/wallet_structure")


COLUMN_MAP = {
    # 地址
    "address": "wallet_address",
    "wallet": "wallet_address",
    "wallet_address": "wallet_address",

    # 排名 / 时间
    "rank": "entry_rank",
    "entry_rank": "entry_rank",
    "first_buy_rank": "entry_rank",
    "entry_time": "entry_time",
    "first_buy_time": "entry_time",

    # 买卖金额
    "buy": "buy_amount_usd",
    "buy_amount": "buy_amount_usd",
    "buy_amount_usd": "buy_amount_usd",
    "sell": "sell_amount_usd",
    "sell_amount": "sell_amount_usd",
    "sell_amount_usd": "sell_amount_usd",

    # 持仓 / 卖出
    "holding_pct": "holding_pct",
    "hold_pct": "holding_pct",
    "sold_pct": "sold_pct",
    "sell_pct": "sold_pct",
    "remaining_pct": "remaining_pct",
    "remain_pct": "remaining_pct",

    # 结果
    "roi": "roi_pct",
    "roi_pct": "roi_pct",
    "pnl": "pnl_usd",
    "pnl_usd": "pnl_usd",

    # 交易次数
    "trade_count": "trade_count",
    "buy_count": "buy_count",
    "sell_count": "sell_count",

    # 标签
    "is_top_holder": "is_top_holder",
    "is_top_trader": "is_top_trader",

    # 资金来源
    "funding_source": "funding_source_address",
    "funding_source_address": "funding_source_address",
    "funding_source_label": "funding_source_label",
    "first_funding_time": "first_funding_time",
    "first_funding_amount_sol": "first_funding_amount_sol",
}


def read_csv_rows(path: Path) -> List[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def normalize_wallet_row(row: Mapping[str, Any]) -> Dict[str, Any]:
    normalized: Dict[str, Any] = {}

    for k, v in row.items():
        key = k.strip()
        lower = key.lower().strip()
        mapped = COLUMN_MAP.get(lower, key)
        normalized[mapped] = v

    # 兜底计算 remaining_pct
    if "remaining_pct" not in normalized:
        sold = float(normalized.get("sold_pct") or 0)
        normalized["remaining_pct"] = max(0, 100 - sold)

    # 兜底字段
    normalized.setdefault("wallet_address", normalized.get("address", ""))
    normalized.setdefault("entry_rank", 999999)
    normalized.setdefault("buy_amount_usd", 0)
    normalized.setdefault("sell_amount_usd", 0)
    normalized.setdefault("sold_pct", 0)
    normalized.setdefault("remaining_pct", 0)
    normalized.setdefault("roi_pct", 0)
    normalized.setdefault("pnl_usd", 0)

    return normalized


def find_existing_token_report_dir(
    token_address: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Optional[Path]:
    candidates = [
        output_dir / token_address,
        Path("data/gmgn_token_reports") / token_address,
        Path("data/gmgn_reports") / token_address,
        Path("data/reports") / token_address,
    ]

    for d in candidates:
        if d.exists() and d.is_dir():
            return d

    return None


def load_wallet_rows_from_existing_report(
    token_address: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Optional[List[Dict[str, Any]]]:
    report_dir = find_existing_token_report_dir(token_address, output_dir=output_dir)
    if not report_dir:
        return None

    file_priority = [
        "early_wallet_raw.csv",
        "wallet_classification.csv",
        "holders.csv",
        "top_holders.csv",
        "wallets.csv",
    ]

    for filename in file_priority:
        path = report_dir / filename
        if path.exists():
            rows = read_csv_rows(path)
            return [normalize_wallet_row(r) for r in rows]

    return None


def run_sikk_gmgn_token_report(
    token_address: str,
    token_symbol: str,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> None:
    """
    可选：如果没有现成报告，则调用已有单币报告脚本。
    前提：你的 sikk_gmgn_token_report.py 支持这些参数。
    如果实际参数不同，改这里即可。
    """
    script = Path("sikk_gmgn_token_report.py")

    if not script.exists():
        raise FileNotFoundError("找不到 sikk_gmgn_token_report.py，无法自动生成单币报告")

    token_dir = output_dir / token_address
    token_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "python",
        str(script),
        "--token",
        token_address,
        "--symbol",
        token_symbol,
        "--output-dir",
        str(token_dir),
    ]

    subprocess.run(cmd, check=True)


def fetch_or_load_token_wallet_raw(
    token=[REDACTED] Any],
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    auto_run_report: bool = False,
) -> List[Dict[str, Any]]:
    token_address = token["token_address"]
    token_symbol = token.get("token_symbol") or token.get("symbol") or "UNKNOWN"

    # 1. 优先读取已有报告
    existing = load_wallet_rows_from_existing_report(token_address, output_dir=output_dir)
    if existing is not None:
        return existing

    # 2. 可选：自动调用 sikk_gmgn_token_report.py
    if auto_run_report:
        run_sikk_gmgn_token_report(token_address, token_symbol, output_dir=output_dir)
        existing = load_wallet_rows_from_existing_report(token_address, output_dir=output_dir)
        if existing is not None:
            return existing

    raise FileNotFoundError(
        f"没有找到 {token_address} 的钱包报告。请先运行 sikk_gmgn_token_report.py，"
        f"或开启 auto_run_report=True。"
    )
```

---

## 2.3 在 pipeline 中接入同源组

在 `process_one_token()` 中加入：

```python
from sikk.wallet_structure.sikk_same_source_group import apply_same_source_groups
```

然后修改处理流程：

```python
# 1. 获取钱包原始数据
wallet_rows = fetch_or_load_token_wallet_raw(
    token,
    output_dir=output_dir,
    auto_run_report=False,
)

# 2. 生成 same_source_group_id + candidate_groups
wallet_rows, candidate_groups = apply_same_source_groups(
    token_address=token_address,
    token_symbol=token_symbol,
    wallet_rows=wallet_rows,
)

# 3. 保存 early_wallet_raw.csv
write_csv(token_dir / "early_wallet_raw.csv", wallet_rows)

# 4. classify(w)
classifications = [classify_wallet(w) for w in wallet_rows]

# 5. 保存 wallet_classification.csv
classification_rows = []
for raw, cls in zip(wallet_rows, classifications):
    row = dict(raw)
    row.update(asdict(cls))
    classification_rows.append(row)

write_csv(token_dir / "wallet_classification.csv", classification_rows)

# 6. 保存 candidate_groups.csv
write_csv(token_dir / "candidate_groups.csv", candidate_groups)
```

---

## 2.4 聚合 metrics 时使用 candidate_groups

把原来的：

```python
same_source_group_count = int(token.get("same_source_group_count") or 0)
same_source_sync_sell_score = float(token.get("same_source_sync_sell_score") or 0)
```

改成：

```python
same_source_group_count = len(candidate_groups)

same_source_sync_sell_score = max(
    [float(g.get("sync_sell_score") or 0) for g in candidate_groups],
    default=0,
)

same_source_sync_buy_score = max(
    [float(g.get("sync_buy_score") or 0) for g in candidate_groups],
    default=0,
)
```

并写入 metrics：

```python
"same_source_group_count": same_source_group_count,
"same_source_sync_sell_score": same_source_sync_sell_score,
"same_source_sync_buy_score": same_source_sync_buy_score,
```

---

# 3. snapshots / delta 的真实文件生成逻辑

新建：

```text
sikk/wallet_structure/sikk_wallet_snapshot.py
```

---

## 3.1 功能

每次跑 token 后生成：

```text
snapshots/snapshot_<timestamp>.json
snapshots/delta_<from>__<to>.json
snapshots/latest_snapshot.json
snapshots/latest_delta.json
```

用途：

```text
单次 snapshot：记录当前钱包结构状态
delta：判断结构是否恶化、筹码是否转移
```

---

## 3.2 代码

```python
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Mapping, Optional


def now_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def n(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def pct_change(new: float, old: float) -> float:
    if old == 0:
        return 0.0
    return (new - old) / abs(old) * 100


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def build_snapshot(
    token_address: str,
    token_symbol: str,
    decision: Any,
    market_context: Optional[Mapping[str, Any]] = None,
    snapshot_time: Optional[str] = None,
) -> Dict[str, Any]:
    """
    decision: WalletStructureDecision 或同结构对象
    market_context: K线/quote/GMGN holder 等外部数据
    """

    market_context = market_context or {}
    metrics = decision.metrics

    snapshot = {
        "token_address": token_address,
        "token_symbol": token_symbol,
        "snapshot_time": snapshot_time or iso_now(),

        # 市场数据
        "price": n(market_context.get("price")),
        "market_cap": n(market_context.get("market_cap")),
        "liquidity": n(market_context.get("liquidity")),
        "holder_count": n(market_context.get("holder_count")),
        "top10_holder_pct": n(market_context.get("top10_holder_pct")),
        "top20_holder_pct": n(market_context.get("top20_holder_pct")),

        # 钱包结构核心
        "early_wallet_count": n(metrics.get("early_wallet_count")),
        "early_wallet_remaining_pct": n(metrics.get("early_wallet_remaining_pct")),
        "early_wallet_sold_pct": n(metrics.get("early_wallet_sold_pct")),

        "high_result_wallet_count": n(metrics.get("high_result_wallet_count")),
        "high_result_remaining_pct": n(metrics.get("high_result_remaining_pct")),

        "same_source_group_count": n(metrics.get("same_source_group_count")),
        "same_source_group_remaining_pct": n(metrics.get("same_source_group_remaining_pct")),
        "same_source_group_sold_pct": n(metrics.get("same_source_group_sold_pct")),
        "same_source_sync_sell_score": n(metrics.get("same_source_sync_sell_score")),
        "same_source_sync_buy_score": n(metrics.get("same_source_sync_buy_score")),

        "distribution_wallet_count": n(metrics.get("distribution_wallet_count")),
        "bagholder_whale_count": n(metrics.get("bagholder_whale_count")),
        "late_buyer_count": n(metrics.get("late_buyer_count")),
        "late_large_buyer_count": n(metrics.get("late_large_buyer_count")),
        "late_buyer_buy_amount_usd": n(metrics.get("late_buyer_buy_amount_usd")),

        # 分数
        "wallet_structure_status": decision.wallet_structure_status,
        "wallet_structure_score": decision.wallet_structure_score,
        "wallet_risk_score": decision.wallet_risk_score,
        "counterparty_pressure_score": decision.counterparty_pressure_score,
        "data_quality_score": decision.data_quality_score,

        "dominant_side_status": decision.dominant_side_status,
        "chip_transfer_status": decision.chip_transfer_status,
    }

    return snapshot


def build_delta(previous: Mapping[str, Any], current: Mapping[str, Any]) -> Dict[str, Any]:
    delta = {
        "token_address": current.get("token_address"),
        "token_symbol": current.get("token_symbol"),
        "from_snapshot": previous.get("snapshot_time"),
        "to_snapshot": current.get("snapshot_time"),

        # 市场变化
        "price_change_pct": pct_change(n(current.get("price")), n(previous.get("price"))),
        "market_cap_change_pct": pct_change(n(current.get("market_cap")), n(previous.get("market_cap"))),
        "liquidity_change_pct": pct_change(n(current.get("liquidity")), n(previous.get("liquidity"))),

        "holder_count_delta": n(current.get("holder_count")) - n(previous.get("holder_count")),
        "holder_count_delta_pct": pct_change(n(current.get("holder_count")), n(previous.get("holder_count"))),

        "top10_holder_pct_delta": n(current.get("top10_holder_pct")) - n(previous.get("top10_holder_pct")),
        "top20_holder_pct_delta": n(current.get("top20_holder_pct")) - n(previous.get("top20_holder_pct")),

        # 钱包结构变化
        "early_wallet_remaining_pct_delta": (
            n(current.get("early_wallet_remaining_pct"))
            - n(previous.get("early_wallet_remaining_pct"))
        ),
        "early_wallet_sold_pct_delta": (
            n(current.get("early_wallet_sold_pct"))
            - n(previous.get("early_wallet_sold_pct"))
        ),

        "high_result_remaining_pct_delta": (
            n(current.get("high_result_remaining_pct"))
            - n(previous.get("high_result_remaining_pct"))
        ),

        "same_source_group_remaining_pct_delta": (
            n(current.get("same_source_group_remaining_pct"))
            - n(previous.get("same_source_group_remaining_pct"))
        ),
        "same_source_group_sold_pct_delta": (
            n(current.get("same_source_group_sold_pct"))
            - n(previous.get("same_source_group_sold_pct"))
        ),

        "distribution_wallet_count_delta": (
            n(current.get("distribution_wallet_count"))
            - n(previous.get("distribution_wallet_count"))
        ),
        "bagholder_whale_count_delta": (
            n(current.get("bagholder_whale_count"))
            - n(previous.get("bagholder_whale_count"))
        ),
        "late_buyer_count_delta": (
            n(current.get("late_buyer_count"))
            - n(previous.get("late_buyer_count"))
        ),
        "late_large_buyer_count_delta": (
            n(current.get("late_large_buyer_count"))
            - n(previous.get("late_large_buyer_count"))
        ),
        "late_buyer_buy_amount_usd_delta": (
            n(current.get("late_buyer_buy_amount_usd"))
            - n(previous.get("late_buyer_buy_amount_usd"))
        ),

        # 分数变化
        "wallet_structure_score_delta": (
            n(current.get("wallet_structure_score"))
            - n(previous.get("wallet_structure_score"))
        ),
        "wallet_risk_score_delta": (
            n(current.get("wallet_risk_score"))
            - n(previous.get("wallet_risk_score"))
        ),
        "counterparty_pressure_score_delta": (
            n(current.get("counterparty_pressure_score"))
            - n(previous.get("counterparty_pressure_score"))
        ),

        "dominant_side_status_from": previous.get("dominant_side_status"),
        "dominant_side_status_to": current.get("dominant_side_status"),
        "chip_transfer_status_from": previous.get("chip_transfer_status"),
        "chip_transfer_status_to": current.get("chip_transfer_status"),
    }

    delta["delta_interpretation"] = interpret_delta(delta)

    return delta


def interpret_delta(delta: Mapping[str, Any]) -> str:
    price_change_pct = n(delta.get("price_change_pct"))
    early_sold_delta = n(delta.get("early_wallet_sold_pct_delta"))
    same_source_sold_delta = n(delta.get("same_source_group_sold_pct_delta"))
    late_large_delta = n(delta.get("late_large_buyer_count_delta"))
    top10_delta = n(delta.get("top10_holder_pct_delta"))
    holder_delta_pct = n(delta.get("holder_count_delta_pct"))
    risk_delta = n(delta.get("wallet_risk_score_delta"))
    counterparty_delta = n(delta.get("counterparty_pressure_score_delta"))

    if price_change_pct > 0 and early_sold_delta >= 10 and late_large_delta >= 1:
        return "价格上涨过程中早期钱包卖出增加，晚期大额承接增加，疑似筹码向对手盘转移"

    if same_source_sold_delta >= 20:
        return "疑似同源组卖出比例明显上升，结构侧撤退风险增加"

    if holder_delta_pct > 5 and top10_delta <= -3:
        return "持有人数增长但 Top10 持仓下降，筹码有分散迹象"

    if risk_delta >= 20 or counterparty_delta >= 25:
        return "钱包风险或对手盘压力快速上升，结构状态恶化"

    if price_change_pct > 0 and early_sold_delta <= 5 and same_source_sold_delta <= 5:
        return "价格推进过程中结构钱包未明显撤退，结构暂时维持"

    return "未发现明确结构迁移信号"


def write_snapshot_and_delta(
    token_address: str,
    token_symbol: str,
    decision: Any,
    market_context: Optional[Mapping[str, Any]],
    base_dir: Path,
) -> Dict[str, Any]:
    snapshots_dir = base_dir / token_address / "snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)

    current_snapshot = build_snapshot(
        token_address=token_address,
        token_symbol=token_symbol,
        decision=decision,
        market_context=market_context,
    )

    ts = now_ts()
    snapshot_path = snapshots_dir / f"snapshot_{ts}.json"
    latest_snapshot_path = snapshots_dir / "latest_snapshot.json"

    previous_snapshot = None
    if latest_snapshot_path.exists():
        previous_snapshot = read_json(latest_snapshot_path)

    write_json(snapshot_path, current_snapshot)
    write_json(latest_snapshot_path, current_snapshot)

    result = {
        "snapshot_path": str(snapshot_path),
        "delta_path": None,
        "snapshot": current_snapshot,
        "delta": None,
    }

    if previous_snapshot:
        delta = build_delta(previous_snapshot, current_snapshot)
        from_ts = str(previous_snapshot.get("snapshot_time", "prev")).replace(":", "").replace("-", "")
        to_ts = str(current_snapshot.get("snapshot_time", "cur")).replace(":", "").replace("-", "")

        delta_path = snapshots_dir / f"delta_{from_ts}__{to_ts}.json"
        latest_delta_path = snapshots_dir / "latest_delta.json"

        write_json(delta_path, delta)
        write_json(latest_delta_path, delta)

        result["delta_path"] = str(delta_path)
        result["delta"] = delta

    return result
```

---

## 3.3 在 pipeline 中接入 snapshot/delta

在 `process_one_token()` 的 `save_decision()` 后面加：

```python
from sikk.wallet_structure.sikk_wallet_snapshot import write_snapshot_and_delta
```

然后：

```python
market_context = {
    "price": token.get("price"),
    "market_cap": token.get("market_cap"),
    "liquidity": token.get("liquidity"),
    "holder_count": token.get("holder_count"),
    "top10_holder_pct": token.get("top10_holder_pct"),
    "top20_holder_pct": token.get("top20_holder_pct"),
}

snapshot_result = write_snapshot_and_delta(
    token_address=token_address,
    token_symbol=token_symbol,
    decision=decision,
    market_context=market_context,
    base_dir=output_dir,
)
```

summary row 里增加：

```python
"snapshot_path": snapshot_result.get("snapshot_path"),
"delta_path": snapshot_result.get("delta_path"),
```

---

# 4. paper runner 的 FORCE_PAPER_EXIT：立即退出还是先 EXIT_MONITOR？

## 4.1 v1.0 策略结论

纸面交易阶段建议：

```text
硬性结构恶化 → FORCE_PAPER_EXIT
轻度结构恶化 → EXIT_MONITOR
真实交易阶段 → 不自动卖出，只生成确认票据
```

也就是：

| 场景 | paper runner | 未来实盘 |
|---|---|---|
| WALLET_BLOCK | 立即 FORCE_PAPER_EXIT | 生成紧急退出确认 |
| sync_sell_score >= 70 | 立即 FORCE_PAPER_EXIT | 生成紧急退出确认 |
| counterparty_pressure_score >= 70 且 delta >= 25 | 立即 FORCE_PAPER_EXIT | 生成紧急退出确认 |
| early_wallet_sold_pct_delta >= 20 但仓位盈利 | EXIT_MONITOR | 提醒人工 |
| high_result_remaining_pct_delta <= -20 | EXIT_MONITOR | 提醒人工 |
| data_quality_score < 50 | EXIT_MONITOR | 暂停新动作 |

---

## 4.2 为什么 paper 可以直接 FORCE_EXIT？

因为 paper 的目标是验证规则：

```text
如果钱包结构恶化，提前退出是否能减少回撤？
```

所以纸面阶段应该大胆测试退出规则。

但实盘不能自动退出，因为真实交易存在：

```text
滑点
MEV
报价失真
假信号
落链失败
```

所以未来实盘只能：

```text
REAL_TRADE_CONFIRMATION_REQUIRED
```

---

## 4.3 推荐动作等级

```text
HOLD
EXIT_MONITOR
FORCE_PAPER_EXIT
REAL_TRADE_CONFIRMATION_REQUIRED
```

---

## 4.4 paper runner 持仓动作函数

```python
def decide_wallet_position_action(
    position: dict,
    current_decision,
    latest_delta: dict | None,
    mode: str = "paper",
) -> dict:
    """
    mode:
    - paper: 可以 FORCE_PAPER_EXIT
    - live: 不自动卖，生成 confirmation ticket
    """

    latest_delta = latest_delta or {}

    current_status = current_decision.wallet_structure_status
    metrics = current_decision.metrics

    sync_sell_score = float(metrics.get("same_source_sync_sell_score") or 0)
    counterparty_score = float(current_decision.counterparty_pressure_score or 0)
    data_quality_score = float(current_decision.data_quality_score or 0)

    counterparty_delta = float(latest_delta.get("counterparty_pressure_score_delta") or 0)
    early_sold_delta = float(latest_delta.get("early_wallet_sold_pct_delta") or 0)
    same_source_sold_delta = float(latest_delta.get("same_source_group_sold_pct_delta") or 0)
    high_result_delta = float(latest_delta.get("high_result_remaining_pct_delta") or 0)
    risk_delta = float(latest_delta.get("wallet_risk_score_delta") or 0)

    position_pnl_pct = float(position.get("unrealized_pnl_pct") or 0)

    def hard_exit(reason: str, failure_type: str) -> dict:
        if mode == "paper":
            return {
                "action": "FORCE_PAPER_EXIT",
                "failure_type": failure_type,
                "reason": reason,
            }

        return {
            "action": "REAL_TRADE_CONFIRMATION_REQUIRED",
            "failure_type": failure_type,
            "reason": reason,
        }

    # 1. 结构已经阻断
    if current_status == "WALLET_BLOCK":
        return hard_exit(
            "钱包结构状态变为 WALLET_BLOCK，纸面阶段直接模拟退出",
            "STRUCTURE_WEAKENING",
        )

    # 2. 同源组同步卖出
    if sync_sell_score >= 70 or same_source_sold_delta >= 20:
        return hard_exit(
            "疑似同源组同步卖出达到高风险阈值",
            "SAME_SOURCE_EXIT",
        )

    # 3. 对手盘压力快速上升
    if counterparty_score >= 70 and counterparty_delta >= 25:
        return hard_exit(
            "对手盘压力高且快速上升，疑似筹码向晚期承接方转移",
            "COUNTERPARTY_ABSORBING",
        )

    # 4. 早期钱包快速退出
    if early_sold_delta >= 20:
        if position_pnl_pct <= 0:
            return hard_exit(
                "早期钱包卖出增加且当前仓位未盈利",
                "WALLET_EXIT",
            )

        return {
            "action": "EXIT_MONITOR",
            "failure_type": "WALLET_EXIT",
            "reason": "早期钱包卖出增加，但当前仓位仍盈利，先进入退出观察",
        }

    # 5. 高结果钱包退出
    if high_result_delta <= -20:
        if risk_delta >= 20:
            return hard_exit(
                "高结果钱包退出且钱包风险分明显上升",
                "HIGH_RESULT_EXIT",
            )

        return {
            "action": "EXIT_MONITOR",
            "failure_type": "HIGH_RESULT_EXIT",
            "reason": "高结果钱包剩余筹码下降，进入退出观察",
        }

    # 6. 数据质量不足
    if data_quality_score < 50:
        return {
            "action": "EXIT_MONITOR",
            "failure_type": "DATA_QUALITY_FAIL",
            "reason": "当前钱包结构数据质量不足，暂停激进动作",
        }

    return {
        "action": "HOLD",
        "failure_type": None,
        "reason": "钱包结构未触发持仓退出条件",
    }
```

---

# 5. daily_report 如何统计不同 wallet_structure_status 的胜率和收益

新建：

```text
sikk/reporting/sikk_wallet_structure_daily_report.py
```

---

## 5.1 输入

建议读取：

```text
data/gmgn_candidates_live_run/paper_positions.csv
data/gmgn_candidates_live_run/paper_trades.csv
data/gmgn_candidates_live_run/risk_events.csv
data/gmgn_candidates_live_run/failure_attribution.csv
```

最低要求只要有：

```text
paper_positions.csv
```

字段至少包含：

```text
position_id
token_address
token_symbol
status
entry_time
exit_time
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
entry_price
exit_price
net_pnl_pct
net_pnl_sol
max_floating_profit_pct
max_drawdown_pct
exit_reason
failure_type
```

---

## 5.2 统计指标

按 `wallet_structure_status` 分组：

```text
总仓位数
关闭仓位数
胜率
平均收益 pct
中位数收益 pct
总收益 SOL
平均最大浮盈
平均最大回撤
最大单笔收益
最大单笔亏损
失败原因 Top 5
```

---

## 5.3 代码

```python
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean, median
from typing import Any, Dict, List, Mapping


def n(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        if value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def read_csv_rows(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def is_closed_position(row: Mapping[str, Any]) -> bool:
    status = str(row.get("status") or "").upper()
    return status in {"CLOSED", "PAPER_CLOSED", "EXITED", "FORCE_PAPER_EXIT"}


def is_win(row: Mapping[str, Any]) -> bool:
    return n(row.get("net_pnl_pct")) > 0


def group_positions_by_wallet_status(rows: List[Mapping[str, Any]]) -> Dict[str, List[Mapping[str, Any]]]:
    groups = defaultdict(list)

    for r in rows:
        status = r.get("wallet_structure_status") or "UNKNOWN"
        groups[str(status)].append(r)

    return dict(groups)


def summarize_group(rows: List[Mapping[str, Any]]) -> Dict[str, Any]:
    total_positions = len(rows)
    closed = [r for r in rows if is_closed_position(r)]

    pnl_pcts = [n(r.get("net_pnl_pct")) for r in closed]
    pnl_sols = [n(r.get("net_pnl_sol")) for r in closed]
    wins = [r for r in closed if is_win(r)]

    max_floating = [n(r.get("max_floating_profit_pct")) for r in closed]
    max_drawdowns = [n(r.get("max_drawdown_pct")) for r in closed]

    failure_counter = Counter(
        str(r.get("failure_type") or r.get("exit_reason") or "UNKNOWN")
        for r in closed
    )

    if closed:
        win_rate = len(wins) / len(closed) * 100
        avg_pnl_pct = mean(pnl_pcts)
        median_pnl_pct = median(pnl_pcts)
        total_pnl_sol = sum(pnl_sols)
        avg_max_floating_profit_pct = mean(max_floating) if max_floating else 0
        avg_max_drawdown_pct = mean(max_drawdowns) if max_drawdowns else 0
        best_trade_pct = max(pnl_pcts)
        worst_trade_pct = min(pnl_pcts)
    else:
        win_rate = 0
        avg_pnl_pct = 0
        median_pnl_pct = 0
        total_pnl_sol = 0
        avg_max_floating_profit_pct = 0
        avg_max_drawdown_pct = 0
        best_trade_pct = 0
        worst_trade_pct = 0

    return {
        "total_positions": total_positions,
        "closed_positions": len(closed),
        "win_count": len(wins),
        "win_rate_pct": round(win_rate, 2),
        "avg_pnl_pct": round(avg_pnl_pct, 2),
        "median_pnl_pct": round(median_pnl_pct, 2),
        "total_pnl_sol": round(total_pnl_sol, 6),
        "avg_max_floating_profit_pct": round(avg_max_floating_profit_pct, 2),
        "avg_max_drawdown_pct": round(avg_max_drawdown_pct, 2),
        "best_trade_pct": round(best_trade_pct, 2),
        "worst_trade_pct": round(worst_trade_pct, 2),
        "failure_top5": failure_counter.most_common(5),
    }


def build_wallet_structure_daily_report(
    paper_positions_path: Path,
    output_dir: Path,
    report_name: str = "daily_wallet_structure_report",
) -> Dict[str, Any]:
    rows = read_csv_rows(paper_positions_path)
    groups = group_positions_by_wallet_status(rows)

    status_summary = {
        status: summarize_group(group_rows)
        for status, group_rows in groups.items()
    }

    total_summary = summarize_group(rows)

    report = {
        "total_summary": total_summary,
        "by_wallet_structure_status": status_summary,
    }

    write_json(output_dir / f"{report_name}.json", report)
    write_md_report(output_dir / f"{report_name}.md", report)

    return report


def write_md_report(path: Path, report: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = []
    lines.append("# SIKK Wallet Structure Daily Report")
    lines.append("")

    total = report["total_summary"]

    lines.append("## 总览")
    lines.append("")
    lines.append(f"- 总仓位数：{total['total_positions']}")
    lines.append(f"- 已关闭仓位数：{total['closed_positions']}")
    lines.append(f"- 胜率：{total['win_rate_pct']}%")
    lines.append(f"- 平均收益：{total['avg_pnl_pct']}%")
    lines.append(f"- 中位数收益：{total['median_pnl_pct']}%")
    lines.append(f"- 总收益：{total['total_pnl_sol']} SOL")
    lines.append(f"- 平均最大浮盈：{total['avg_max_floating_profit_pct']}%")
    lines.append(f"- 平均最大回撤：{total['avg_max_drawdown_pct']}%")
    lines.append("")

    lines.append("## 按钱包结构状态统计")
    lines.append("")
    lines.append(
        "| wallet_structure_status | total | closed | win_rate | avg_pnl | median_pnl | total_sol | avg_max_profit | avg_drawdown | best | worst |"
    )
    lines.append(
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
    )

    for status, item in report["by_wallet_structure_status"].items():
        lines.append(
            f"| {status} "
            f"| {item['total_positions']} "
            f"| {item['closed_positions']} "
            f"| {item['win_rate_pct']}% "
            f"| {item['avg_pnl_pct']}% "
            f"| {item['median_pnl_pct']}% "
            f"| {item['total_pnl_sol']} "
            f"| {item['avg_max_floating_profit_pct']}% "
            f"| {item['avg_max_drawdown_pct']}% "
            f"| {item['best_trade_pct']}% "
            f"| {item['worst_trade_pct']}% |"
        )

    lines.append("")
    lines.append("## 失败原因 Top 5")
    lines.append("")

    for status, item in report["by_wallet_structure_status"].items():
        lines.append(f"### {status}")
        top5 = item.get("failure_top5") or []
        if not top5:
            lines.append("- 暂无失败样本")
        else:
            for reason, count in top5:
                lines.append(f"- {reason}: {count}")
        lines.append("")

    lines.append("## 解释")
    lines.append("")
    lines.append("- WALLET_SUPPORT 胜率高、回撤低：钱包结构门禁有效。")
    lines.append("- WALLET_SUPPORT 胜率低、亏损高：结构支持条件过松。")
    lines.append("- WALLET_BLOCK 后续仍大涨：阻断规则可能过严。")
    lines.append("- WALLET_PAUSE 样本过多：数据质量不足或规则过保守。")
    lines.append("- COUNTERPARTY_ABSORBING 亏损集中：对手盘压力阈值需要前置。")

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    build_wallet_structure_daily_report(
        paper_positions_path=Path("data/gmgn_candidates_live_run/paper_positions.csv"),
        output_dir=Path("data/gmgn_candidates_live_run/reports"),
    )
```

---

# 6. daily report 的判断标准

跑 10-30 个 token 后，主要看这几个结果。

## 6.1 如果 WALLET_SUPPORT 表现好

特征：

```text
WALLET_SUPPORT 胜率 > WALLET_NEUTRAL
WALLET_SUPPORT 平均回撤低
WALLET_SUPPORT 平均收益为正
```

说明：

```text
钱包结构门禁有效，可以继续保留。
```

---

## 6.2 如果 WALLET_SUPPORT 表现差

特征：

```text
WALLET_SUPPORT 胜率低
WALLET_SUPPORT 平均亏损
COUNTERPARTY_ABSORBING 经常出现在失败归因
```

调整：

```text
wallet_structure_score SUPPORT 阈值 65 → 70
counterparty_pressure_score 上限 40 → 30
early_wallet_remaining_pct 30 → 40
```

---

## 6.3 如果 WALLET_BLOCK 后续经常大涨

说明阻断过严。

检查：

```text
same_source_sync_sell_score 是否误判
early_wallet_sold_pct 是否过严
distribution_wallet_count 是否识别过宽
```

调整：

```text
sync_sell_score BLOCK 阈值 70 → 80
early_wallet_sold_pct 85 → 90
distribution_wallet_count >=3 → >=4
```

---

## 6.4 如果 WALLET_PAUSE 太多

分两种情况：

### 数据不足导致

```text
data_quality_score 普遍 < 50
```

先修数据采集，不调阈值。

### 规则过保守导致

```text
data_quality_score 正常
但大量 PAUSE 来自 counterparty_pressure_score 50-60
```

可以改：

```text
counterparty_pressure_score >= 60 才 PAUSE
50-59 改成 EXIT_MONITOR / WATCHING
```

---

# 7. 最终接入流程

完整链路现在应该是：

```text
sikk_gmgn_token_report.py
  ↓
early_wallet_raw.csv
  ↓
sikk_candidate_wallet_structure_pipeline.py
  ↓
apply_same_source_groups()
  ↓
wallet_classification.csv
candidate_groups.csv
  ↓
decide_wallet_structure()
  ↓
wallet_structure_decision.json
  ↓
snapshot_*.json / delta_*.json
  ↓
状态机读取 wallet_structure_decision.json
  ↓
WALLET_BLOCK / WALLET_PAUSE / WALLET_SUPPORT / WALLET_NEUTRAL
  ↓
paper runner 写入 wallet_structure_factor
  ↓
持仓中读取 latest_delta.json
  ↓
HOLD / EXIT_MONITOR / FORCE_PAPER_EXIT
  ↓
failure_attribution.csv
  ↓
daily_wallet_structure_report.md
```

---

# 8. 当前最优开发顺序

按这个顺序做：

```text
1. 加 sikk_same_source_group.py
2. 修改 pipeline，读取 sikk_gmgn_token_report.py 输出
3. pipeline 中接入 apply_same_source_groups()
4. 生成 candidate_groups.csv
5. 生成 wallet_structure_decision.json
6. 加 sikk_wallet_snapshot.py
7. 生成 snapshot / delta
8. paper runner 读取 wallet_structure_decision.json + latest_delta.json
9. paper runner 支持 EXIT_MONITOR / FORCE_PAPER_EXIT
10. daily_report 按 wallet_structure_status 统计收益
```

不要先做实盘自动卖出。  
当前阶段只验证：

```text
钱包结构门禁是否能提高 paper trading 的胜率 / 降低回撤 / 提前识别失败。
```

---

# 本次认知升级点

这次把 SIKK 钱包结构层补齐成了闭环：

```text
单币报告
→ 同源组生成
→ 同步买卖评分
→ 钱包结构门禁
→ 多轮快照 delta
→ paper 持仓退出
→ 失败归因
→ 日报统计
```

核心升级是：

> 钱包结构不再只是“入场前判断”，而是贯穿持仓全过程：入场门禁、持仓监控、失败归因、阈值校准。

---

# 尚未解决问题

下一步可以继续细化：

```text
1. sikk_gmgn_token_report.py 的真实输出字段与 COLUMN_MAP 对齐
2. same_source_group 的 CEX / 路由器过滤名单扩展
3. latest_delta.json 如何进入 paper runner 的现有更新循环
4. EXIT_MONITOR 后是否触发减仓、移动止损或缩短时间止损
5. daily_report 增加“钱包结构状态 × SIKK信号等级”的交叉统计
```


---

## 片段 46 / stream_idx=6709 / len=259


1. same_source_group_id 的实际生成代码
2. sikk_candidate_wallet_structure_pipeline.py 如何读取你现有 sikk_gmgn_token_report.py 输出
3. snapshots/delta 的真实文件生成逻辑
4. paper runner 的 FORCE_PAPER_EXIT 是否立即退出，还是先触发 EXIT_MONITOR
5. daily_report 如何统计不同 wallet_structure_status 的胜率和收益


---

## 片段 47 / stream_idx=6827 / len=67864


下面给你一套 **SIKK-SOL v1.0 钱包结构门禁层工程骨架**。  
定位是：**能接入状态机、能跑测试、能被 paper runner 使用**。真实 GMGN 抓取部分先做 adapter 占位，后面再替换成你的接口。

---

# 0. 建议目录结构

```text
sikk/
  wallet_structure/
    __init__.py
    sikk_wallet_structure_gate.py
    sikk_candidate_wallet_structure_pipeline.py

tests/
  test_sikk_wallet_structure_gate.py
```

---

# 1. `sikk_wallet_structure_gate.py` 完整代码骨架

路径建议：

```text
sikk/wallet_structure/sikk_wallet_structure_gate.py
```

```python
from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple


# =========================
# 1. 枚举定义
# =========================

class WalletRole(str, Enum):
    EARLY_BUYER = "EARLY_BUYER"
    EARLY_EXIT = "EARLY_EXIT"
    PARTIAL_HOLDER = "PARTIAL_HOLDER"
    HIGH_RESULT_WALLET = "HIGH_RESULT_WALLET"
    SAME_SOURCE_GROUP = "SAME_SOURCE_GROUP"
    DISTRIBUTION_SELLER = "DISTRIBUTION_SELLER"
    BAGHOLDER_WHALE = "BAGHOLDER_WHALE"
    RETAIL_NOISE = "RETAIL_NOISE"


class GameSide(str, Enum):
    STRUCTURE_SIDE = "STRUCTURE_SIDE"
    EXECUTION_SIDE = "EXECUTION_SIDE"
    DISTRIBUTION_SIDE = "DISTRIBUTION_SIDE"
    COUNTERPARTY_SIDE = "COUNTERPARTY_SIDE"
    NOISE_SIDE = "NOISE_SIDE"
    UNKNOWN_SIDE = "UNKNOWN_SIDE"


class WalletStructureStatus(str, Enum):
    WALLET_BLOCK = "WALLET_BLOCK"
    WALLET_PAUSE = "WALLET_PAUSE"
    WALLET_SUPPORT = "WALLET_SUPPORT"
    WALLET_NEUTRAL = "WALLET_NEUTRAL"


class DecisionAction(str, Enum):
    BLOCKED = "BLOCKED"
    PAUSE = "PAUSE"
    ALLOW_PAPER_READY = "ALLOW_PAPER_READY"
    CONTINUE_OTHER_GATES = "CONTINUE_OTHER_GATES"


class DominantSideStatus(str, Enum):
    STRUCTURE_STRENGTHENING = "STRUCTURE_STRENGTHENING"
    STRUCTURE_HOLDING = "STRUCTURE_HOLDING"
    STRUCTURE_WEAKENING = "STRUCTURE_WEAKENING"
    DISTRIBUTION_ACTIVE = "DISTRIBUTION_ACTIVE"
    COUNTERPARTY_ABSORBING = "COUNTERPARTY_ABSORBING"
    UNKNOWN = "UNKNOWN"


class ChipTransferStatus(str, Enum):
    NO_MAJOR_TRANSFER = "NO_MAJOR_TRANSFER"
    STRUCTURE_ACCUMULATION = "STRUCTURE_ACCUMULATION"
    STRUCTURE_HOLDING = "STRUCTURE_HOLDING"
    EARLY_TO_LATE_TRANSFER = "EARLY_TO_LATE_TRANSFER"
    GROUP_TO_RETAIL_TRANSFER = "GROUP_TO_RETAIL_TRANSFER"
    PROFIT_WALLET_EXIT = "PROFIT_WALLET_EXIT"
    DISTRIBUTION_TO_COUNTERPARTY = "DISTRIBUTION_TO_COUNTERPARTY"
    COUNTERPARTY_TRAPPED = "COUNTERPARTY_TRAPPED"
    UNKNOWN = "UNKNOWN"


# =========================
# 2. 数据结构
# =========================

@dataclass
class WalletClassification:
    wallet_address: str
    wallet_role: str
    game_side: str
    role_confidence: float
    reason: str


@dataclass
class ScoreBreakdown:
    wallet_structure_score: Dict[str, float] = field(default_factory=dict)
    wallet_risk_score: Dict[str, float] = field(default_factory=dict)
    counterparty_pressure_score: Dict[str, float] = field(default_factory=dict)
    data_quality_score: Dict[str, float] = field(default_factory=dict)


@dataclass
class WalletStructureDecision:
    token_address: str
    token_symbol: str

    wallet_structure_status: str
    wallet_structure_score: float
    wallet_risk_score: float
    counterparty_pressure_score: float
    data_quality_score: float
    wallet_structure_factor: float
    wallet_evidence_level: str
    decision_action: str

    dominant_side_status: str
    chip_transfer_status: str

    reason: str
    support_signals: List[str]
    risk_signals: List[str]
    metrics: Dict[str, Any]
    score_breakdown: Dict[str, Any]
    game_side_summary: Dict[str, int]

    created_at: Optional[str] = None


# =========================
# 3. 工具函数
# =========================

def n(value: Any, default: float = 0.0) -> float:
    """安全转数字。"""
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def s(value: Any, default: str = "") -> str:
    if value is None:
        return default
    return str(value)


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value in ("true", "True", "TRUE", "1", 1):
        return True
    return False


def pressure_level(value: Any) -> str:
    v = s(value, "UNKNOWN").upper()
    if v in {"LOW", "MEDIUM", "HIGH"}:
        return v
    return "UNKNOWN"


def clamp(value: float, lo: float = 0.0, hi: float = 100.0) -> float:
    return max(lo, min(hi, value))


# =========================
# 4. 钱包角色分类 classify(w)
# =========================

def role_to_game_side(role: str, w: Mapping[str, Any]) -> str:
    if role == WalletRole.EARLY_BUYER.value:
        return GameSide.STRUCTURE_SIDE.value
    if role == WalletRole.EARLY_EXIT.value:
        return GameSide.DISTRIBUTION_SIDE.value
    if role == WalletRole.PARTIAL_HOLDER.value:
        sold_pct = n(w.get("sold_pct"))
        if sold_pct >= 50:
            return GameSide.DISTRIBUTION_SIDE.value
        return GameSide.STRUCTURE_SIDE.value
    if role == WalletRole.HIGH_RESULT_WALLET.value:
        return GameSide.EXECUTION_SIDE.value
    if role == WalletRole.SAME_SOURCE_GROUP.value:
        return GameSide.EXECUTION_SIDE.value
    if role == WalletRole.DISTRIBUTION_SELLER.value:
        return GameSide.DISTRIBUTION_SIDE.value
    if role == WalletRole.BAGHOLDER_WHALE.value:
        return GameSide.COUNTERPARTY_SIDE.value
    return GameSide.NOISE_SIDE.value


def classify_wallet(w: Mapping[str, Any]) -> WalletClassification:
    """
    SIKK v1.0 钱包角色分类。
    注意：这是当前 token 内部的事件分类，不是永久身份定性。
    """

    wallet_address = s(w.get("wallet_address") or w.get("address"))

    entry_rank = n(w.get("entry_rank"), 999999)
    buy_amount_usd = n(w.get("buy_amount_usd"))
    sell_amount_usd = n(w.get("sell_amount_usd"))
    holding_pct = n(w.get("holding_pct"))
    sold_pct = n(w.get("sold_pct"))
    remaining_pct = n(w.get("remaining_pct"))
    roi_pct = n(w.get("roi_pct"))
    pnl_usd = n(w.get("pnl_usd"))

    is_top_holder = boolish(w.get("is_top_holder"))
    same_source_group_id = s(w.get("same_source_group_id"))
    same_source_group_size = n(w.get("same_source_group_size"))
    sync_buy_score = n(w.get("sync_buy_score"))
    sync_sell_score = n(w.get("sync_sell_score"))
    distribution_risk = s(w.get("distribution_risk")).upper()

    # 1. 派发 / 分发优先
    if (
        (sold_pct >= 80 and remaining_pct <= 20)
        or (buy_amount_usd > 0 and sell_amount_usd >= buy_amount_usd * 0.7)
        or (is_top_holder and sold_pct >= 60)
        or distribution_risk == "HIGH"
    ):
        role = WalletRole.DISTRIBUTION_SELLER.value
        return WalletClassification(
            wallet_address=wallet_address,
            wallet_role=role,
            game_side=role_to_game_side(role, w),
            role_confidence=0.85,
            reason="高卖出比例、Top Holder 出货或分发风险高，疑似分发/派发钱包",
        )

    # 2. 早期清仓
    if entry_rank <= 50 and sold_pct >= 85 and remaining_pct <= 15:
        role = WalletRole.EARLY_EXIT.value
        return WalletClassification(
            wallet_address=wallet_address,
            wallet_role=role,
            game_side=role_to_game_side(role, w),
            role_confidence=0.85,
            reason="早期进入后大部分清仓",
        )

    # 3. 同源组
    if (
        same_source_group_id
        and same_source_group_size >= 3
        and (sync_buy_score >= 60 or sync_sell_score >= 60)
    ):
        role = WalletRole.SAME_SOURCE_GROUP.value
        return WalletClassification(
            wallet_address=wallet_address,
            wallet_role=role,
            game_side=role_to_game_side(role, w),
            role_confidence=0.75,
            reason="存在同源组或同步买卖行为",
        )

    # 4. 高结果钱包
    if roi_pct >= 100 or pnl_usd >= 500 or (roi_pct >= 50 and remaining_pct >= 30):
        role = WalletRole.HIGH_RESULT_WALLET.value
        return WalletClassification(
            wallet_address=wallet_address,
            wallet_role=role,
            game_side=role_to_game_side(role, w),
            role_confidence=0.75,
            reason="ROI/PnL 表现明显较好",
        )

    # 5. 套牢鲸鱼
    if holding_pct >= 1 and roi_pct <= -30 and remaining_pct >= 70:
        role = WalletRole.BAGHOLDER_WHALE.value
        return WalletClassification(
            wallet_address=wallet_address,
            wallet_role=role,
            game_side=role_to_game_side(role, w),
            role_confidence=0.70,
            reason="高持仓且浮亏明显，疑似套牢鲸鱼或被动承接方",
        )

    # 6. 部分持有
    if remaining_pct >= 20 and 20 <= sold_pct < 80:
        role = WalletRole.PARTIAL_HOLDER.value
        return WalletClassification(
            wallet_address=wallet_address,
            wallet_role=role,
            game_side=role_to_game_side(role, w),
            role_confidence=0.65,
            reason="已部分卖出但仍有剩余持仓",
        )

    # 7. 早期买入
    if entry_rank <= 50 and remaining_pct > 15:
        role = WalletRole.EARLY_BUYER.value
        return WalletClassification(
            wallet_address=wallet_address,
            wallet_role=role,
            game_side=role_to_game_side(role, w),
            role_confidence=0.65,
            reason="早期进入且仍有剩余筹码",
        )

    # 8. 默认噪音
    role = WalletRole.RETAIL_NOISE.value
    return WalletClassification(
        wallet_address=wallet_address,
        wallet_role=role,
        game_side=role_to_game_side(role, w),
        role_confidence=0.40,
        reason="未发现明显结构特征，暂归为普通噪音钱包",
    )


# =========================
# 5. 分数计算
# =========================

def compute_wallet_structure_score(metrics: Mapping[str, Any]) -> Tuple[float, Dict[str, float]]:
    early_wallet_remaining_pct = n(metrics.get("early_wallet_remaining_pct"))
    high_result_wallet_count = n(metrics.get("high_result_wallet_count"))
    high_result_remaining_pct = n(metrics.get("high_result_remaining_pct"))
    same_source_group_count = n(metrics.get("same_source_group_count"))
    same_source_sync_sell_score = n(metrics.get("same_source_sync_sell_score"))
    distribution_wallet_count = n(metrics.get("distribution_wallet_count"))
    top_holder_exit_pressure = pressure_level(metrics.get("top_holder_exit_pressure"))
    top_trader_buy_sell_bias = s(metrics.get("top_trader_buy_sell_bias"), "UNKNOWN").upper()
    wallet_behavior_matches_price_action = s(metrics.get("wallet_behavior_matches_price_action"), "UNCLEAR").upper()

    # A. 早期钱包仍持有，0-25
    if early_wallet_remaining_pct >= 50:
        early_holder_score = 25
    elif early_wallet_remaining_pct >= 30:
        early_holder_score = 18
    elif early_wallet_remaining_pct >= 15:
        early_holder_score = 8
    else:
        early_holder_score = 0

    # B. 高结果钱包仍持有，0-20
    if high_result_wallet_count >= 2 and high_result_remaining_pct >= 40:
        high_result_score = 20
    elif high_result_wallet_count >= 1 and high_result_remaining_pct >= 25:
        high_result_score = 14
    elif high_result_wallet_count >= 1 and high_result_remaining_pct >= 10:
        high_result_score = 6
    else:
        high_result_score = 0

    # C. 同源组未同步卖出，0-15
    if same_source_group_count >= 1 and same_source_sync_sell_score < 30:
        same_source_support_score = 15
    elif same_source_group_count >= 1 and same_source_sync_sell_score < 50:
        same_source_support_score = 8
    elif same_source_group_count == 0:
        same_source_support_score = 5
    else:
        same_source_support_score = 0

    # D. 分发风险低，0-15
    if distribution_wallet_count == 0:
        low_distribution_score = 15
    elif distribution_wallet_count == 1:
        low_distribution_score = 10
    elif distribution_wallet_count == 2:
        low_distribution_score = 5
    else:
        low_distribution_score = 0

    # E. Top holder 压力，0-10
    if top_holder_exit_pressure == "LOW":
        holder_stability_score = 10
    elif top_holder_exit_pressure == "MEDIUM":
        holder_stability_score = 5
    else:
        holder_stability_score = 0

    # F. Top trader 未反向，0-10
    if top_trader_buy_sell_bias == "BUY_OR_HOLD":
        top_trader_score = 10
    elif top_trader_buy_sell_bias == "NEUTRAL":
        top_trader_score = 5
    else:
        top_trader_score = 0

    # G. 钱包行为与 K线不冲突，0-5
    if wallet_behavior_matches_price_action in {"TRUE", "MATCH", "YES"}:
        consistency_score = 5
    elif wallet_behavior_matches_price_action in {"UNCLEAR", "UNKNOWN"}:
        consistency_score = 2
    else:
        consistency_score = 0

    breakdown = {
        "early_holder_score": early_holder_score,
        "high_result_score": high_result_score,
        "same_source_support_score": same_source_support_score,
        "low_distribution_score": low_distribution_score,
        "holder_stability_score": holder_stability_score,
        "top_trader_score": top_trader_score,
        "consistency_score": consistency_score,
    }

    return clamp(sum(breakdown.values())), breakdown


def compute_wallet_risk_score(
    metrics: Mapping[str, Any],
    data_quality_score: float,
) -> Tuple[float, Dict[str, float]]:
    early_wallet_sold_pct = n(metrics.get("early_wallet_sold_pct"))
    same_source_sync_sell_score = n(metrics.get("same_source_sync_sell_score"))
    distribution_wallet_count = n(metrics.get("distribution_wallet_count"))
    high_result_wallet_count = n(metrics.get("high_result_wallet_count"))
    high_result_remaining_pct = n(metrics.get("high_result_remaining_pct"))
    top_holder_exit_pressure = pressure_level(metrics.get("top_holder_exit_pressure"))
    bagholder_whale_count = n(metrics.get("bagholder_whale_count"))

    # A. 早期清仓风险，0-30
    if early_wallet_sold_pct >= 85:
        early_exit_risk = 30
    elif early_wallet_sold_pct >= 70:
        early_exit_risk = 22
    elif early_wallet_sold_pct >= 50:
        early_exit_risk = 12
    else:
        early_exit_risk = 0

    # B. 同源组同步卖出风险，0-25
    if same_source_sync_sell_score >= 80:
        same_source_exit_risk = 25
    elif same_source_sync_sell_score >= 60:
        same_source_exit_risk = 18
    elif same_source_sync_sell_score >= 40:
        same_source_exit_risk = 8
    else:
        same_source_exit_risk = 0

    # C. 分发钱包风险，0-15
    if distribution_wallet_count >= 5:
        distribution_risk_score = 15
    elif distribution_wallet_count >= 3:
        distribution_risk_score = 10
    elif distribution_wallet_count >= 1:
        distribution_risk_score = 5
    else:
        distribution_risk_score = 0

    # D. 高结果钱包退出风险，0-10
    if high_result_wallet_count >= 2 and high_result_remaining_pct <= 10:
        high_result_exit_risk = 10
    elif high_result_wallet_count >= 1 and high_result_remaining_pct <= 20:
        high_result_exit_risk = 6
    else:
        high_result_exit_risk = 0

    # E. Top holder 出货，0-10
    if top_holder_exit_pressure == "HIGH":
        top_holder_exit_risk = 10
    elif top_holder_exit_pressure == "MEDIUM":
        top_holder_exit_risk = 5
    else:
        top_holder_exit_risk = 0

    # F. 套牢鲸鱼压力，0-5
    if bagholder_whale_count >= 3:
        bagholder_pressure_risk = 5
    elif bagholder_whale_count >= 1:
        bagholder_pressure_risk = 3
    else:
        bagholder_pressure_risk = 0

    # G. 数据不足风险，0-5
    if data_quality_score < 50:
        data_missing_risk = 5
    elif data_quality_score < 70:
        data_missing_risk = 3
    else:
        data_missing_risk = 0

    breakdown = {
        "early_exit_risk": early_exit_risk,
        "same_source_exit_risk": same_source_exit_risk,
        "distribution_risk_score": distribution_risk_score,
        "high_result_exit_risk": high_result_exit_risk,
        "top_holder_exit_risk": top_holder_exit_risk,
        "bagholder_pressure_risk": bagholder_pressure_risk,
        "data_missing_risk": data_missing_risk,
    }

    return clamp(sum(breakdown.values())), breakdown


def compute_counterparty_pressure_score(metrics: Mapping[str, Any]) -> Tuple[float, Dict[str, float]]:
    """
    对手盘压力分。
    优先使用 delta 字段；如果没有 delta，可以由 pipeline 传入静态近似字段。
    """

    early_wallet_sold_pct_delta = n(metrics.get("early_wallet_sold_pct_delta"))
    late_buyer_buy_amount_usd_delta = n(metrics.get("late_buyer_buy_amount_usd_delta"))
    late_large_buyer_count = n(metrics.get("late_large_buyer_count"))
    bagholder_whale_count = n(metrics.get("bagholder_whale_count"))
    price_change_pct = n(metrics.get("price_change_pct"))
    same_source_group_sold_pct_delta = n(metrics.get("same_source_group_sold_pct_delta"))
    high_result_remaining_pct_delta = n(metrics.get("high_result_remaining_pct_delta"))
    holder_count_delta_pct = n(metrics.get("holder_count_delta_pct"))
    top10_holder_pct_delta = n(metrics.get("top10_holder_pct_delta"))

    # A. 早期 → 晚期转移，0-25
    if early_wallet_sold_pct_delta >= 20 and late_buyer_buy_amount_usd_delta > 0:
        early_to_late_transfer_score = 25
    elif early_wallet_sold_pct_delta >= 10 and late_buyer_buy_amount_usd_delta > 0:
        early_to_late_transfer_score = 18
    elif early_wallet_sold_pct_delta >= 5 and late_buyer_buy_amount_usd_delta > 0:
        early_to_late_transfer_score = 10
    else:
        early_to_late_transfer_score = 0

    # B. 晚期大额买家，0-20
    if late_large_buyer_count >= 5:
        late_large_buyer_score = 20
    elif late_large_buyer_count >= 3:
        late_large_buyer_score = 14
    elif late_large_buyer_count >= 1:
        late_large_buyer_score = 6
    else:
        late_large_buyer_score = 0

    # C. 套牢鲸鱼，0-15
    if bagholder_whale_count >= 5:
        bagholder_pressure_score = 15
    elif bagholder_whale_count >= 3:
        bagholder_pressure_score = 10
    elif bagholder_whale_count >= 1:
        bagholder_pressure_score = 5
    else:
        bagholder_pressure_score = 0

    # D. 价格上涨但结构钱包卖出，0-20
    if price_change_pct > 20 and early_wallet_sold_pct_delta >= 15:
        price_up_structure_sell_score = 20
    elif price_change_pct > 10 and same_source_group_sold_pct_delta >= 10:
        price_up_structure_sell_score = 16
    elif price_change_pct > 0 and high_result_remaining_pct_delta <= -10:
        price_up_structure_sell_score = 10
    else:
        price_up_structure_sell_score = 0

    # E. 持有人增长但 Top10 下降，0-10
    if holder_count_delta_pct > 10 and top10_holder_pct_delta <= -5:
        holder_growth_top_exit_score = 10
    elif holder_count_delta_pct > 5 and top10_holder_pct_delta <= -3:
        holder_growth_top_exit_score = 6
    else:
        holder_growth_top_exit_score = 0

    # F. 高结果钱包退出，0-10
    if high_result_remaining_pct_delta <= -30:
        high_result_exit_score = 10
    elif high_result_remaining_pct_delta <= -15:
        high_result_exit_score = 6
    elif high_result_remaining_pct_delta <= -5:
        high_result_exit_score = 3
    else:
        high_result_exit_score = 0

    breakdown = {
        "early_to_late_transfer_score": early_to_late_transfer_score,
        "late_large_buyer_score": late_large_buyer_score,
        "bagholder_pressure_score": bagholder_pressure_score,
        "price_up_structure_sell_score": price_up_structure_sell_score,
        "holder_growth_top_exit_score": holder_growth_top_exit_score,
        "high_result_exit_score": high_result_exit_score,
    }

    return clamp(sum(breakdown.values())), breakdown


def compute_data_quality_score(metrics: Mapping[str, Any]) -> Tuple[float, Dict[str, float]]:
    """
    v1.0：由 pipeline 提供各类字段完整率。
    如果暂时没有完整率，就用默认保守值。
    """

    early_wallet_count = n(metrics.get("early_wallet_count"))

    holding_trade_complete_ratio = n(metrics.get("holding_trade_complete_ratio"), 0.7)
    time_field_complete_ratio = n(metrics.get("time_field_complete_ratio"), 0.7)
    result_field_complete_ratio = n(metrics.get("result_field_complete_ratio"), 0.7)
    source_field_complete_ratio = n(metrics.get("source_field_complete_ratio"), 0.3)
    top_holder_field_complete_ratio = n(metrics.get("top_holder_field_complete_ratio"), 0.5)

    # A. early_wallet_data_score，0-25
    if early_wallet_count >= 50:
        early_wallet_data_score = 25
    elif early_wallet_count >= 30:
        early_wallet_data_score = 18
    elif early_wallet_count >= 10:
        early_wallet_data_score = 10
    else:
        early_wallet_data_score = 3

    def score_ratio(ratio: float, max_score: float, thresholds: Tuple[float, float, float], scores: Tuple[float, float, float, float]) -> float:
        if ratio >= thresholds[0]:
            return scores[0]
        if ratio >= thresholds[1]:
            return scores[1]
        if ratio >= thresholds[2]:
            return scores[2]
        return scores[3]

    holding_trade_field_score = score_ratio(
        holding_trade_complete_ratio, 20, (0.9, 0.7, 0.5), (20, 14, 8, 3)
    )
    time_field_score = score_ratio(
        time_field_complete_ratio, 15, (0.9, 0.7, 0.5), (15, 10, 5, 0)
    )
    result_field_score = score_ratio(
        result_field_complete_ratio, 15, (0.9, 0.7, 0.5), (15, 10, 5, 0)
    )
    source_field_score = score_ratio(
        source_field_complete_ratio, 15, (0.8, 0.5, 0.2), (15, 8, 3, 0)
    )
    top_holder_field_score = score_ratio(
        top_holder_field_complete_ratio, 10, (0.8, 0.5, 0.0), (10, 5, 0, 0)
    )

    breakdown = {
        "early_wallet_data_score": early_wallet_data_score,
        "holding_trade_field_score": holding_trade_field_score,
        "time_field_score": time_field_score,
        "result_field_score": result_field_score,
        "source_field_score": source_field_score,
        "top_holder_field_score": top_holder_field_score,
    }

    return clamp(sum(breakdown.values())), breakdown


# =========================
# 6. 状态推断
# =========================

def infer_dominant_side_status(metrics: Mapping[str, Any]) -> str:
    early_wallet_remaining_pct_delta = n(metrics.get("early_wallet_remaining_pct_delta"))
    early_wallet_sold_pct_delta = n(metrics.get("early_wallet_sold_pct_delta"))
    same_source_group_sold_pct_delta = n(metrics.get("same_source_group_sold_pct_delta"))
    high_result_remaining_pct_delta = n(metrics.get("high_result_remaining_pct_delta"))
    distribution_wallet_count_delta = n(metrics.get("distribution_wallet_count_delta"))
    late_large_buyer_count_delta = n(metrics.get("late_large_buyer_count_delta"))
    holder_count_delta_pct = n(metrics.get("holder_count_delta_pct"))
    top10_holder_pct_delta = n(metrics.get("top10_holder_pct_delta"))
    price_change_pct = n(metrics.get("price_change_pct"))
    counterparty_pressure_score_delta = n(metrics.get("counterparty_pressure_score_delta"))

    if (
        distribution_wallet_count_delta >= 2
        or same_source_group_sold_pct_delta >= 20
        or (top10_holder_pct_delta <= -5 and price_change_pct > 0)
    ):
        return DominantSideStatus.DISTRIBUTION_ACTIVE.value

    if (
        (late_large_buyer_count_delta >= 2 and early_wallet_sold_pct_delta >= 10)
        or (holder_count_delta_pct > 5 and top10_holder_pct_delta <= -3)
    ):
        return DominantSideStatus.COUNTERPARTY_ABSORBING.value

    if (
        early_wallet_remaining_pct_delta <= -10
        or high_result_remaining_pct_delta <= -10
        or same_source_group_sold_pct_delta >= 10
    ):
        return DominantSideStatus.STRUCTURE_WEAKENING.value

    if (
        early_wallet_remaining_pct_delta >= 0
        and same_source_group_sold_pct_delta <= 5
        and counterparty_pressure_score_delta <= 10
        and price_change_pct > 0
    ):
        return DominantSideStatus.STRUCTURE_STRENGTHENING.value

    if (
        early_wallet_remaining_pct_delta > -10
        and same_source_group_sold_pct_delta < 10
    ):
        return DominantSideStatus.STRUCTURE_HOLDING.value

    return DominantSideStatus.UNKNOWN.value


def infer_chip_transfer_status(metrics: Mapping[str, Any]) -> str:
    early_wallet_sold_pct_delta = n(metrics.get("early_wallet_sold_pct_delta"))
    same_source_group_sold_pct_delta = n(metrics.get("same_source_group_sold_pct_delta"))
    high_result_remaining_pct_delta = n(metrics.get("high_result_remaining_pct_delta"))
    distribution_wallet_count_delta = n(metrics.get("distribution_wallet_count_delta"))
    late_large_buyer_count_delta = n(metrics.get("late_large_buyer_count_delta"))
    bagholder_whale_count_delta = n(metrics.get("bagholder_whale_count_delta"))
    price_change_pct = n(metrics.get("price_change_pct"))
    holder_count_delta_pct = n(metrics.get("holder_count_delta_pct"))
    top10_holder_pct_delta = n(metrics.get("top10_holder_pct_delta"))

    if early_wallet_sold_pct_delta >= 10 and late_large_buyer_count_delta >= 1:
        return ChipTransferStatus.EARLY_TO_LATE_TRANSFER.value

    if same_source_group_sold_pct_delta >= 10 and holder_count_delta_pct > 5:
        return ChipTransferStatus.GROUP_TO_RETAIL_TRANSFER.value

    if high_result_remaining_pct_delta <= -15:
        return ChipTransferStatus.PROFIT_WALLET_EXIT.value

    if distribution_wallet_count_delta >= 2 and late_large_buyer_count_delta >= 1:
        return ChipTransferStatus.DISTRIBUTION_TO_COUNTERPARTY.value

    if bagholder_whale_count_delta >= 2 and price_change_pct <= 0:
        return ChipTransferStatus.COUNTERPARTY_TRAPPED.value

    if top10_holder_pct_delta >= 0 and price_change_pct > 0:
        return ChipTransferStatus.STRUCTURE_ACCUMULATION.value

    return ChipTransferStatus.NO_MAJOR_TRANSFER.value


def infer_evidence_level(data_quality_score: float, metrics: Mapping[str, Any]) -> str:
    same_source_group_count = n(metrics.get("same_source_group_count"))
    early_wallet_count = n(metrics.get("early_wallet_count"))

    if data_quality_score >= 80 and early_wallet_count >= 30 and same_source_group_count >= 1:
        return "E3"
    if data_quality_score >= 60 and early_wallet_count >= 10:
        return "E2"
    if data_quality_score >= 40:
        return "E1"
    return "E0"


def wallet_structure_factor(status: str) -> float:
    if status == WalletStructureStatus.WALLET_BLOCK.value:
        return 0.0
    if status == WalletStructureStatus.WALLET_PAUSE.value:
        return 0.30
    if status == WalletStructureStatus.WALLET_SUPPORT.value:
        return 1.15
    return 1.0


def decision_action_for_status(status: str) -> str:
    if status == WalletStructureStatus.WALLET_BLOCK.value:
        return DecisionAction.BLOCKED.value
    if status == WalletStructureStatus.WALLET_PAUSE.value:
        return DecisionAction.PAUSE.value
    if status == WalletStructureStatus.WALLET_SUPPORT.value:
        return DecisionAction.ALLOW_PAPER_READY.value
    return DecisionAction.CONTINUE_OTHER_GATES.value


def summarize_game_side(classifications: Optional[List[WalletClassification]]) -> Dict[str, int]:
    summary = {
        "structure_side_wallet_count": 0,
        "execution_side_wallet_count": 0,
        "distribution_side_wallet_count": 0,
        "counterparty_side_wallet_count": 0,
        "noise_side_wallet_count": 0,
        "unknown_side_wallet_count": 0,
    }

    if not classifications:
        return summary

    for c in classifications:
        side = c.game_side
        if side == GameSide.STRUCTURE_SIDE.value:
            summary["structure_side_wallet_count"] += 1
        elif side == GameSide.EXECUTION_SIDE.value:
            summary["execution_side_wallet_count"] += 1
        elif side == GameSide.DISTRIBUTION_SIDE.value:
            summary["distribution_side_wallet_count"] += 1
        elif side == GameSide.COUNTERPARTY_SIDE.value:
            summary["counterparty_side_wallet_count"] += 1
        elif side == GameSide.NOISE_SIDE.value:
            summary["noise_side_wallet_count"] += 1
        else:
            summary["unknown_side_wallet_count"] += 1

    return summary


# =========================
# 7. 最终门禁决策
# =========================

def decide_wallet_structure(
    token_address: str,
    token_symbol: str,
    metrics: Mapping[str, Any],
    classifications: Optional[List[WalletClassification]] = None,
    created_at: Optional[str] = None,
) -> WalletStructureDecision:
    data_quality_score, dq_breakdown = compute_data_quality_score(metrics)
    wallet_structure_score, ws_breakdown = compute_wallet_structure_score(metrics)
    wallet_risk_score, wr_breakdown = compute_wallet_risk_score(metrics, data_quality_score)
    counterparty_pressure_score, cp_breakdown = compute_counterparty_pressure_score(metrics)

    same_source_sync_sell_score = n(metrics.get("same_source_sync_sell_score"))
    early_wallet_sold_pct = n(metrics.get("early_wallet_sold_pct"))
    early_wallet_remaining_pct = n(metrics.get("early_wallet_remaining_pct"))
    high_result_remaining_pct = n(metrics.get("high_result_remaining_pct"))
    distribution_wallet_count = n(metrics.get("distribution_wallet_count"))
    top_holder_exit_pressure = pressure_level(metrics.get("top_holder_exit_pressure"))

    support_signals: List[str] = []
    risk_signals: List[str] = []

    # 支持信号记录
    if early_wallet_remaining_pct >= 30:
        support_signals.append("EARLY_WALLETS_STILL_HOLDING")
    if high_result_remaining_pct >= 20:
        support_signals.append("HIGH_RESULT_WALLETS_STILL_HOLDING")
    if same_source_sync_sell_score < 50:
        support_signals.append("NO_STRONG_SAME_SOURCE_EXIT")
    if distribution_wallet_count <= 1:
        support_signals.append("LOW_DISTRIBUTION_RISK")

    # 风险信号记录
    if early_wallet_sold_pct >= 70:
        risk_signals.append("EARLY_WALLET_SELLING_HIGH")
    if same_source_sync_sell_score >= 60:
        risk_signals.append("SAME_SOURCE_SYNC_SELL")
    if counterparty_pressure_score >= 50:
        risk_signals.append("COUNTERPARTY_PRESSURE")
    if top_holder_exit_pressure == "HIGH":
        risk_signals.append("TOP_HOLDER_EXIT_PRESSURE_HIGH")
    if data_quality_score < 50:
        risk_signals.append("DATA_QUALITY_LOW")

    # 硬阻断
    if wallet_risk_score >= 75:
        status = WalletStructureStatus.WALLET_BLOCK.value
        reason = "钱包结构风险分达到极高区间，阻断进入 PAPER_READY"

    elif counterparty_pressure_score >= 70 and wallet_risk_score >= 50:
        status = WalletStructureStatus.WALLET_BLOCK.value
        reason = "对手盘压力高且钱包风险分偏高，疑似筹码向对手盘转移"

    elif same_source_sync_sell_score >= 70:
        status = WalletStructureStatus.WALLET_BLOCK.value
        reason = "疑似同源组同步卖出达到阻断阈值"

    elif early_wallet_sold_pct >= 85 and high_result_remaining_pct <= 10:
        status = WalletStructureStatus.WALLET_BLOCK.value
        reason = "早期钱包集中清仓且高结果钱包剩余筹码过低"

    elif distribution_wallet_count >= 3 and early_wallet_remaining_pct <= 20:
        status = WalletStructureStatus.WALLET_BLOCK.value
        reason = "分发钱包增加且早期钱包剩余筹码不足"

    # 暂停
    elif data_quality_score < 50:
        status = WalletStructureStatus.WALLET_PAUSE.value
        reason = "钱包结构数据质量不足，暂停进入 PAPER_READY"

    elif wallet_risk_score >= 50:
        status = WalletStructureStatus.WALLET_PAUSE.value
        reason = "钱包风险分处于中高风险区间，需要继续观察"

    elif counterparty_pressure_score >= 50:
        status = WalletStructureStatus.WALLET_PAUSE.value
        reason = "对手盘压力偏高，疑似出现筹码转移，需要暂停观察"

    elif top_holder_exit_pressure == "HIGH":
        status = WalletStructureStatus.WALLET_PAUSE.value
        reason = "Top Holder 出货压力高，暂停观察"

    # 支持
    elif (
        wallet_structure_score >= 65
        and wallet_risk_score <= 40
        and counterparty_pressure_score <= 40
        and data_quality_score >= 60
        and early_wallet_remaining_pct >= 30
        and same_source_sync_sell_score < 50
        and distribution_wallet_count <= 1
    ):
        status = WalletStructureStatus.WALLET_SUPPORT.value
        reason = "钱包结构支持，风险与对手盘压力可控，允许进入后续 PAPER_READY 门禁"

    else:
        status = WalletStructureStatus.WALLET_NEUTRAL.value
        reason = "钱包结构无明显支持或阻断，继续交由其他门禁判断"

    dominant_side_status = infer_dominant_side_status(metrics)
    chip_transfer_status = infer_chip_transfer_status(metrics)
    evidence_level = infer_evidence_level(data_quality_score, metrics)

    score_breakdown = ScoreBreakdown(
        wallet_structure_score=ws_breakdown,
        wallet_risk_score=wr_breakdown,
        counterparty_pressure_score=cp_breakdown,
        data_quality_score=dq_breakdown,
    )

    return WalletStructureDecision(
        token_address=token_address,
        token_symbol=token_symbol,
        wallet_structure_status=status,
        wallet_structure_score=wallet_structure_score,
        wallet_risk_score=wallet_risk_score,
        counterparty_pressure_score=counterparty_pressure_score,
        data_quality_score=data_quality_score,
        wallet_structure_factor=wallet_structure_factor(status),
        wallet_evidence_level=evidence_level,
        decision_action=decision_action_for_status(status),
        dominant_side_status=dominant_side_status,
        chip_transfer_status=chip_transfer_status,
        reason=reason,
        support_signals=support_signals,
        risk_signals=risk_signals,
        metrics=dict(metrics),
        score_breakdown=asdict(score_breakdown),
        game_side_summary=summarize_game_side(classifications),
        created_at=created_at,
    )


def save_decision(decision: WalletStructureDecision, path: str | Path) -> None:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(asdict(decision), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_decision(path: str | Path) -> WalletStructureDecision:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return WalletStructureDecision(**data)
```

---

# 2. `tests/test_sikk_wallet_structure_gate.py` 测试样例

路径：

```text
tests/test_sikk_wallet_structure_gate.py
```

```python
import pytest

from sikk.wallet_structure.sikk_wallet_structure_gate import (
    classify_wallet,
    decide_wallet_structure,
    WalletRole,
    GameSide,
    WalletStructureStatus,
)


def base_metrics(**overrides):
    data = {
        "early_wallet_count": 50,
        "early_wallet_remaining_pct": 40,
        "early_wallet_sold_pct": 60,

        "high_result_wallet_count": 2,
        "high_result_remaining_pct": 35,

        "same_source_group_count": 1,
        "same_source_sync_sell_score": 20,

        "distribution_wallet_count": 0,
        "bagholder_whale_count": 0,

        "top_holder_exit_pressure": "LOW",
        "top_trader_buy_sell_bias": "NEUTRAL",
        "wallet_behavior_matches_price_action": "MATCH",

        "holding_trade_complete_ratio": 0.9,
        "time_field_complete_ratio": 0.9,
        "result_field_complete_ratio": 0.8,
        "source_field_complete_ratio": 0.8,
        "top_holder_field_complete_ratio": 0.8,

        # delta 默认无风险
        "early_wallet_sold_pct_delta": 0,
        "late_buyer_buy_amount_usd_delta": 0,
        "late_large_buyer_count": 0,
        "price_change_pct": 0,
        "same_source_group_sold_pct_delta": 0,
        "high_result_remaining_pct_delta": 0,
        "holder_count_delta_pct": 0,
        "top10_holder_pct_delta": 0,
    }
    data.update(overrides)
    return data


# =========================
# classify_wallet 测试
# =========================

def test_classify_distribution_seller_priority():
    w = {
        "wallet_address": "W1",
        "entry_rank": 10,
        "sold_pct": 90,
        "remaining_pct": 10,
        "buy_amount_usd": 1000,
        "sell_amount_usd": 900,
        "is_top_holder": True,
    }

    result = classify_wallet(w)

    assert result.wallet_role == WalletRole.DISTRIBUTION_SELLER.value
    assert result.game_side == GameSide.DISTRIBUTION_SIDE.value


def test_classify_early_exit():
    w = {
        "wallet_address": "W2",
        "entry_rank": 20,
        "sold_pct": 86,
        "remaining_pct": 14,
        "buy_amount_usd": 1000,
        "sell_amount_usd": 500,
        "is_top_holder": False,
    }

    result = classify_wallet(w)

    # 注意：如果 sell_amount_usd >= buy_amount * 0.7，会优先被判为 DISTRIBUTION_SELLER。
    # 这里故意 sell_amount_usd = 500，避免触发派发优先级。
    assert result.wallet_role == WalletRole.EARLY_EXIT.value


def test_classify_same_source_group():
    w = {
        "wallet_address": "W3",
        "same_source_group_id": "SSG_TEST_001",
        "same_source_group_size": 4,
        "sync_buy_score": 80,
        "sync_sell_score": 20,
        "sold_pct": 10,
        "remaining_pct": 90,
        "entry_rank": 12,
    }

    result = classify_wallet(w)

    assert result.wallet_role == WalletRole.SAME_SOURCE_GROUP.value
    assert result.game_side == GameSide.EXECUTION_SIDE.value


def test_classify_high_result_wallet():
    w = {
        "wallet_address": "W4",
        "entry_rank": 60,
        "roi_pct": 120,
        "pnl_usd": 300,
        "sold_pct": 30,
        "remaining_pct": 70,
    }

    result = classify_wallet(w)

    assert result.wallet_role == WalletRole.HIGH_RESULT_WALLET.value


def test_classify_bagholder_whale():
    w = {
        "wallet_address": "W5",
        "holding_pct": 2.0,
        "roi_pct": -40,
        "remaining_pct": 90,
        "sold_pct": 10,
        "entry_rank": 120,
    }

    result = classify_wallet(w)

    assert result.wallet_role == WalletRole.BAGHOLDER_WHALE.value
    assert result.game_side == GameSide.COUNTERPARTY_SIDE.value


# =========================
# decide_wallet_structure 测试
# =========================

def test_wallet_support_case():
    decision = decide_wallet_structure(
        token_address="TOKEN1",
        token_symbol="T1",
        metrics=base_metrics(),
    )

    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_SUPPORT.value
    assert decision.wallet_structure_factor == 1.15
    assert decision.decision_action == "ALLOW_PAPER_READY"


def test_wallet_block_when_same_source_sync_sell_high():
    decision = decide_wallet_structure(
        token_address="TOKEN2",
        token_symbol="T2",
        metrics=base_metrics(
            same_source_sync_sell_score=75,
            early_wallet_remaining_pct=35,
            early_wallet_sold_pct=65,
        ),
    )

    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_BLOCK.value
    assert decision.wallet_structure_factor == 0.0


def test_wallet_block_when_early_exit_and_high_result_exit():
    decision = decide_wallet_structure(
        token_address="TOKEN3",
        token_symbol="T3",
        metrics=base_metrics(
            early_wallet_sold_pct=90,
            early_wallet_remaining_pct=10,
            high_result_remaining_pct=5,
        ),
    )

    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_BLOCK.value


def test_wallet_pause_when_data_quality_low():
    decision = decide_wallet_structure(
        token_address="TOKEN4",
        token_symbol="T4",
        metrics=base_metrics(
            early_wallet_count=5,
            holding_trade_complete_ratio=0.3,
            time_field_complete_ratio=0.2,
            result_field_complete_ratio=0.2,
            source_field_complete_ratio=0.0,
            top_holder_field_complete_ratio=0.0,
        ),
    )

    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_PAUSE.value
    assert decision.data_quality_score < 50


def test_wallet_pause_when_counterparty_pressure_high():
    decision = decide_wallet_structure(
        token_address="TOKEN5",
        token_symbol="T5",
        metrics=base_metrics(
            early_wallet_sold_pct_delta=20,
            late_buyer_buy_amount_usd_delta=5000,
            late_large_buyer_count=3,
            price_change_pct=25,
            same_source_group_sold_pct_delta=15,
            holder_count_delta_pct=12,
            top10_holder_pct_delta=-6,
        ),
    )

    assert decision.counterparty_pressure_score >= 50
    assert decision.wallet_structure_status in {
        WalletStructureStatus.WALLET_PAUSE.value,
        WalletStructureStatus.WALLET_BLOCK.value,
    }


def test_wallet_neutral_case():
    decision = decide_wallet_structure(
        token_address="TOKEN6",
        token_symbol="T6",
        metrics=base_metrics(
            early_wallet_remaining_pct=22,
            early_wallet_sold_pct=55,
            high_result_wallet_count=0,
            high_result_remaining_pct=0,
            same_source_group_count=0,
            same_source_sync_sell_score=0,
            distribution_wallet_count=1,
        ),
    )

    assert decision.wallet_structure_status == WalletStructureStatus.WALLET_NEUTRAL.value
```

运行：

```bash
pytest tests/test_sikk_wallet_structure_gate.py -q
```

---

# 3. `sikk_candidate_wallet_structure_pipeline.py` 输入输出流程

路径：

```text
sikk/wallet_structure/sikk_candidate_wallet_structure_pipeline.py
```

这个文件不要一开始写得太复杂。v1.0 只做：

```text
读取候选 token
→ 获取 / 读取钱包原始数据
→ classify(w)
→ 聚合 metrics
→ 调用 decide_wallet_structure()
→ 输出 wallet_structure_decision.json
→ 汇总 candidate_wallet_structure_summary.csv/json/md
```

代码骨架：

```python
from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional

from sikk.wallet_structure.sikk_wallet_structure_gate import (
    classify_wallet,
    decide_wallet_structure,
    save_decision,
    WalletClassification,
)


DEFAULT_INPUT_CANDIDATES = Path("data/gmgn_candidates_live_run/candidates.json")
DEFAULT_OUTPUT_DIR = Path("data/gmgn_candidates_live_run/wallet_structure")


# =========================
# 1. 基础 IO
# =========================

def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: List[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        path.write_text("", encoding="utf-8")
        return

    fieldnames = list(rows[0].keys())

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_md_summary(path: Path, rows: List[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# SIKK Candidate Wallet Structure Summary",
        "",
        "| token | status | structure | risk | counterparty | data_quality | reason |",
        "|---|---|---:|---:|---:|---:|---|",
    ]

    for r in rows:
        lines.append(
            f"| {r.get('token_symbol')} | {r.get('wallet_structure_status')} "
            f"| {r.get('wallet_structure_score')} "
            f"| {r.get('wallet_risk_score')} "
            f"| {r.get('counterparty_pressure_score')} "
            f"| {r.get('data_quality_score')} "
            f"| {r.get('reason')} |"
        )

    path.write_text("\n".join(lines), encoding="utf-8")


# =========================
# 2. 输入候选
# =========================

def load_candidates(path: Path) -> List[Dict[str, Any]]:
    """
    candidates.json 推荐格式：
    [
      {
        "token_address": "...",
        "token_symbol": "...",
        "market_cap": 123000,
        "liquidity": 42000
      }
    ]
    """
    data = read_json(path)
    if isinstance(data, dict) and "candidates" in data:
        return list(data["candidates"])
    if isinstance(data, list):
        return data
    raise ValueError(f"Unsupported candidates format: {path}")


# =========================
# 3. GMGN 数据 adapter 占位
# =========================

def fetch_or_load_token_wallet_raw(token=[REDACTED] Any]) -> List[Dict[str, Any]]:
    """
    v1.0 先做 adapter。
    后面这里替换成：
    - GMGN holder 接口
    - early buyer 数据
    - top trader 数据
    - sikk_gmgn_token_report.py 的输出读取

    临时约定：
    如果存在 data/gmgn_candidates_live_run/wallet_structure/<token>/early_wallet_raw.csv，
    则可以在这里读取 CSV。
    当前骨架返回空列表，真实项目里必须替换。
    """
    token_address = token["token_address"]
    raise NotImplementedError(
        f"请接入 GMGN 数据源或读取已有单币报告: {token_address}"
    )


# =========================
# 4. 字段完整率
# =========================

def field_complete_ratio(rows: List[Mapping[str, Any]], fields: List[str]) -> float:
    if not rows or not fields:
        return 0.0

    total = len(rows) * len(fields)
    ok = 0

    for row in rows:
        for f in fields:
            value = row.get(f)
            if value not in (None, "", "null", "None"):
                ok += 1

    return ok / total if total else 0.0


# =========================
# 5. 聚合 token 级 metrics
# =========================

def aggregate_wallet_metrics(
    token=[REDACTED] Any],
    wallet_rows: List[Mapping[str, Any]],
    classifications: List[WalletClassification],
    previous_snapshot: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """
    v1.0 聚合方法。
    后续可以拆成：
    - early_wallet metrics
    - same_source_group metrics
    - top_holder metrics
    - delta metrics
    """

    early_wallets = [
        w for w in wallet_rows
        if float(w.get("entry_rank") or 999999) <= 50
    ]

    high_result_wallets = [
        w for w in wallet_rows
        if float(w.get("roi_pct") or 0) >= 100
        or float(w.get("pnl_usd") or 0) >= 500
    ]

    distribution_wallets = [
        c for c in classifications
        if c.wallet_role == "DISTRIBUTION_SELLER"
    ]

    bagholder_wallets = [
        c for c in classifications
        if c.wallet_role == "BAGHOLDER_WHALE"
    ]

    def avg_or_zero(values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    early_remaining = avg_or_zero([
        float(w.get("remaining_pct") or 0) for w in early_wallets
    ])
    early_sold = avg_or_zero([
        float(w.get("sold_pct") or 0) for w in early_wallets
    ])

    high_result_remaining = avg_or_zero([
        float(w.get("remaining_pct") or 0) for w in high_result_wallets
    ])

    # 这几个字段后续应由 same_source_group 模块真实生成
    same_source_group_count = int(token.get("same_source_group_count") or 0)
    same_source_sync_sell_score = float(token.get("same_source_sync_sell_score") or 0)

    top_holder_exit_pressure = token.get("top_holder_exit_pressure", "UNKNOWN")
    top_trader_buy_sell_bias = token.get("top_trader_buy_sell_bias", "UNKNOWN")

    metrics: Dict[str, Any] = {
        "early_wallet_count": len(early_wallets),
        "early_wallet_remaining_pct": early_remaining,
        "early_wallet_sold_pct": early_sold,

        "high_result_wallet_count": len(high_result_wallets),
        "high_result_remaining_pct": high_result_remaining,

        "same_source_group_count": same_source_group_count,
        "same_source_sync_sell_score": same_source_sync_sell_score,

        "distribution_wallet_count": len(distribution_wallets),
        "bagholder_whale_count": len(bagholder_wallets),

        "top_holder_exit_pressure": top_holder_exit_pressure,
        "top_trader_buy_sell_bias": top_trader_buy_sell_bias,
        "wallet_behavior_matches_price_action": token.get("wallet_behavior_matches_price_action", "UNCLEAR"),

        "holding_trade_complete_ratio": field_complete_ratio(
            wallet_rows,
            ["buy_amount_usd", "sell_amount_usd", "sold_pct", "remaining_pct", "holding_pct"],
        ),
        "time_field_complete_ratio": field_complete_ratio(
            wallet_rows,
            ["entry_time", "entry_rank"],
        ),
        "result_field_complete_ratio": field_complete_ratio(
            wallet_rows,
            ["roi_pct", "pnl_usd"],
        ),
        "source_field_complete_ratio": field_complete_ratio(
            wallet_rows,
            ["funding_source_address", "same_source_group_id"],
        ),
        "top_holder_field_complete_ratio": field_complete_ratio(
            wallet_rows,
            ["is_top_holder", "is_top_trader"],
        ),

        # v1.0 如果没有快照 delta，先给 0
        "early_wallet_sold_pct_delta": 0,
        "early_wallet_remaining_pct_delta": 0,
        "late_buyer_buy_amount_usd_delta": 0,
        "late_large_buyer_count": int(token.get("late_large_buyer_count") or 0),
        "price_change_pct": float(token.get("price_change_pct") or 0),
        "same_source_group_sold_pct_delta": 0,
        "high_result_remaining_pct_delta": 0,
        "holder_count_delta_pct": 0,
        "top10_holder_pct_delta": 0,
    }

    # 如果有 previous_snapshot，后续在这里计算 delta
    if previous_snapshot:
        metrics["early_wallet_sold_pct_delta"] = (
            metrics["early_wallet_sold_pct"] - float(previous_snapshot.get("early_wallet_sold_pct") or 0)
        )
        metrics["early_wallet_remaining_pct_delta"] = (
            metrics["early_wallet_remaining_pct"] - float(previous_snapshot.get("early_wallet_remaining_pct") or 0)
        )
        metrics["high_result_remaining_pct_delta"] = (
            metrics["high_result_remaining_pct"] - float(previous_snapshot.get("high_result_remaining_pct") or 0)
        )

    return metrics


# =========================
# 6. 单 token 处理
# =========================

def process_one_token(
    token=[REDACTED] Any],
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> Dict[str, Any]:
    token_address = token["token_address"]
    token_symbol = token.get("token_symbol") or token.get("symbol") or "UNKNOWN"

    token_dir = output_dir / token_address
    token_dir.mkdir(parents=True, exist_ok=True)

    # 1. 获取钱包原始数据
    wallet_rows = fetch_or_load_token_wallet_raw(token)

    # 2. 保存 early_wallet_raw.csv
    write_csv(token_dir / "early_wallet_raw.csv", wallet_rows)

    # 3. classify(w)
    classifications = [classify_wallet(w) for w in wallet_rows]

    classification_rows = []
    for raw, cls in zip(wallet_rows, classifications):
        row = dict(raw)
        row.update(asdict(cls))
        classification_rows.append(row)

    write_csv(token_dir / "wallet_classification.csv", classification_rows)

    # 4. candidate_groups.csv
    # v1.0 先留空；后续接 same_source_group 模块。
    candidate_groups: List[Dict[str, Any]] = []
    write_csv(token_dir / "candidate_groups.csv", candidate_groups)

    # 5. gmgn_note_table.csv
    gmgn_rows = build_gmgn_note_rows(token, classification_rows)
    write_csv(token_dir / "gmgn_note_table.csv", gmgn_rows)

    # 6. 聚合 metrics
    metrics = aggregate_wallet_metrics(token, wallet_rows, classifications)

    # 7. 调用门禁
    decision = decide_wallet_structure(
        token_address=token_address,
        token_symbol=token_symbol,
        metrics=metrics,
        classifications=classifications,
        created_at=token.get("run_time"),
    )

    # 8. 保存 wallet_structure_decision.json
    save_decision(decision, token_dir / "wallet_structure_decision.json")

    # 9. 返回 summary row
    return {
        "token_address": token_address,
        "token_symbol": token_symbol,
        "wallet_structure_status": decision.wallet_structure_status,
        "wallet_structure_score": decision.wallet_structure_score,
        "wallet_risk_score": decision.wallet_risk_score,
        "counterparty_pressure_score": decision.counterparty_pressure_score,
        "data_quality_score": decision.data_quality_score,
        "wallet_structure_factor": decision.wallet_structure_factor,
        "decision_action": decision.decision_action,
        "dominant_side_status": decision.dominant_side_status,
        "chip_transfer_status": decision.chip_transfer_status,
        "reason": decision.reason,
    }


def build_gmgn_note_rows(
    token=[REDACTED] Any],
    classification_rows: List[Mapping[str, Any]],
) -> List[Dict[str, Any]]:
    token_symbol = token.get("token_symbol") or token.get("symbol") or "TOKEN"
    rows = []

    for r in classification_rows:
        wallet_address = r.get("wallet_address") or r.get("address")
        role = r.get("wallet_role")
        evidence_level = "E2" if role in {
            "HIGH_RESULT_WALLET",
            "SAME_SOURCE_GROUP",
            "DISTRIBUTION_SELLER",
        } else "E1"

        note = f"${token_symbol}@D1｜{role}｜sold={r.get('sold_pct')}｜remain={r.get('remaining_pct')}｜{evidence_level}"

        rows.append({
            "token_address": token.get("token_address"),
            "wallet_address": wallet_address,
            "gmgn_name": f"[{role}] {str(wallet_address)[:6]}...{str(wallet_address)[-4:]}",
            "gmgn_emoji": "🧩",
            "gmgn_note": note,
            "wallet_role": role,
            "evidence_level": evidence_level,
            "risk_level": "HIGH" if role == "DISTRIBUTION_SELLER" else "MEDIUM",
            "action": "WATCH",
        })

    return rows


# =========================
# 7. 批量入口
# =========================

def run_candidate_wallet_structure_pipeline(
    candidates_path: Path = DEFAULT_INPUT_CANDIDATES,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
) -> List[Dict[str, Any]]:
    candidates = load_candidates(candidates_path)

    summary_rows = []
    for token in candidates:
        try:
            row = process_one_token(token, output_dir=output_dir)
            summary_rows.append(row)
        except NotImplementedError as e:
            # v1.0 开发期允许跳过未接入数据源的 token
            summary_rows.append({
                "token_address": token.get("token_address"),
                "token_symbol": token.get("token_symbol"),
                "wallet_structure_status": "DATA_SOURCE_MISSING",
                "reason": str(e),
            })

    write_json(output_dir / "candidate_wallet_structure_summary.json", summary_rows)
    write_csv(output_dir / "candidate_wallet_structure_summary.csv", summary_rows)
    write_md_summary(output_dir / "candidate_wallet_structure_summary.md", summary_rows)

    return summary_rows


if __name__ == "__main__":
    run_candidate_wallet_structure_pipeline()
```

---

# 4. `wallet_structure_decision.json` 与状态机的实际接入点

状态机接入点应该放在：

```text
signal_gate 之后
quote/security 之前或同时
```

推荐顺序：

```text
候选 token
  ↓
K线信号 gate
  ↓
wallet_structure_gate
  ↓
quote gate
  ↓
security gate
  ↓
PAPER_READY
```

原因：

- 钱包结构如果已经 `WALLET_BLOCK`，没必要继续 quote。
- 钱包结构 `WALLET_PAUSE`，也不应直接进入 `PAPER_READY`。
- `WALLET_SUPPORT` 只是允许继续过 quote/security，不是直接开仓。

---

## 状态机接入函数骨架

建议新建或放入现有状态机文件：

```python
from pathlib import Path
from typing import Dict, Any

from sikk.wallet_structure.sikk_wallet_structure_gate import load_decision


def apply_wallet_structure_gate_to_state(
    token_address: str,
    current_state: str,
    signal_gate: str,
    quote_gate: str,
    security_gate: str,
    base_dir: str = "data/gmgn_candidates_live_run/wallet_structure",
) -> Dict[str, Any]:
    decision_path = Path(base_dir) / token_address / "wallet_structure_decision.json"

    if not decision_path.exists():
        return {
            "next_state": "WATCHING",
            "wallet_gate_status": "MISSING_DECISION",
            "reason": "缺少 wallet_structure_decision.json，不能进入 PAPER_READY",
        }

    decision = load_decision(decision_path)

    status = decision.wallet_structure_status

    if status == "WALLET_BLOCK":
        return {
            "next_state": "BLOCKED",
            "wallet_gate_status": status,
            "reason": decision.reason,
            "wallet_decision": decision,
        }

    if status == "WALLET_PAUSE":
        return {
            "next_state": "PAUSE",
            "wallet_gate_status": status,
            "reason": decision.reason,
            "wallet_decision": decision,
        }

    if status == "WALLET_SUPPORT":
        if signal_gate == "ALLOW" and quote_gate == "ALLOW" and security_gate == "ALLOW":
            return {
                "next_state": "PAPER_READY",
                "wallet_gate_status": status,
                "reason": "钱包结构支持，且 signal/quote/security 均通过",
                "wallet_decision": decision,
            }

        return {
            "next_state": "WATCHING",
            "wallet_gate_status": status,
            "reason": "钱包结构支持，但 signal/quote/security 尚未全部通过",
            "wallet_decision": decision,
        }

    # WALLET_NEUTRAL
    if signal_gate == "ALLOW" and quote_gate == "ALLOW" and security_gate == "ALLOW":
        return {
            "next_state": "PAPER_READY",
            "wallet_gate_status": status,
            "reason": "钱包结构中性，其他门禁通过",
            "wallet_decision": decision,
        }

    return {
        "next_state": current_state,
        "wallet_gate_status": status,
        "reason": "钱包结构中性，继续维持当前状态",
        "wallet_decision": decision,
    }
```

---

## 状态机动作表

| wallet 状态 | 状态机动作 |
|---|---|
| WALLET_BLOCK | `BLOCKED` |
| WALLET_PAUSE | `PAUSE` / `WATCHING` |
| WALLET_SUPPORT | 允许继续检查 quote/security/signal |
| WALLET_NEUTRAL | 不加分、不阻断 |

强制原则：

```text
WALLET_SUPPORT 不能绕过 quote_gate。
WALLET_SUPPORT 不能绕过 security_gate。
WALLET_SUPPORT 不能绕过 signal_gate。
WALLET_BLOCK 必须阻断 PAPER_READY。
```

---

# 5. paper runner 如何根据钱包结构变化触发持仓管理或提前退出

paper runner 分两层：

```text
入场前门禁
持仓中监控
```

---

## 5.1 入场前：写入 wallet_structure_factor

paper position 新增字段：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
wallet_structure_factor
wallet_structure_reason
dominant_side_status
chip_transfer_status
```

开仓时：

```python
def enrich_paper_position_with_wallet_structure(position: dict, wallet_decision) -> dict:
    position["wallet_structure_status"] = wallet_decision.wallet_structure_status
    position["wallet_structure_score"] = wallet_decision.wallet_structure_score
    position["wallet_risk_score"] = wallet_decision.wallet_risk_score
    position["counterparty_pressure_score"] = wallet_decision.counterparty_pressure_score
    position["data_quality_score"] = wallet_decision.data_quality_score
    position["wallet_structure_factor"] = wallet_decision.wallet_structure_factor
    position["wallet_structure_reason"] = wallet_decision.reason
    position["dominant_side_status"] = wallet_decision.dominant_side_status
    position["chip_transfer_status"] = wallet_decision.chip_transfer_status
    return position
```

---

## 5.2 持仓中：钱包结构恶化监控

paper runner 每次更新持仓时，重新读取最新：

```text
wallet_structure_decision.json
snapshot delta
```

然后比较：

```text
entry_wallet_structure_score
current_wallet_structure_score
entry_wallet_risk_score
current_wallet_risk_score
entry_counterparty_pressure_score
current_counterparty_pressure_score
```

---

## 5.3 持仓中动作等级

不要一上来就自动卖。v1.0 paper 阶段先分 4 档：

| 动作 | 含义 |
|---|---|
| HOLD | 继续持有 |
| EXIT_MONITOR | 进入退出观察 |
| FORCE_PAPER_EXIT | 纸面强制退出 |
| REAL_TRADE_CONFIRMATION_REQUIRED | 未来实盘时要求人工确认 |

当前阶段只对 paper 生效。

---

## 5.4 持仓管理规则

### A. 直接纸面退出

```text
current_status == WALLET_BLOCK
→ FORCE_PAPER_EXIT
```

原因：

```text
钱包结构已经转为阻断状态，纸面交易应模拟风险退出。
```

---

### B. 对手盘压力快速上升

```text
counterparty_pressure_score_delta >= 25
且 current_counterparty_pressure_score >= 70
→ FORCE_PAPER_EXIT
```

归因：

```text
COUNTERPARTY_ABSORBING
```

---

### C. 同源组同步卖出

```text
same_source_sync_sell_score >= 70
或 same_source_group_sold_pct_delta >= 20
→ FORCE_PAPER_EXIT
```

归因：

```text
SAME_SOURCE_EXIT
```

---

### D. 早期钱包快速退出

```text
early_wallet_sold_pct_delta >= 20
→ EXIT_MONITOR
```

如果同时：

```text
position_pnl_pct <= 0
```

则：

```text
FORCE_PAPER_EXIT
```

归因：

```text
WALLET_EXIT
```

---

### E. 高结果钱包退出

```text
high_result_remaining_pct_delta <= -20
→ EXIT_MONITOR
```

如果同时：

```text
wallet_risk_score_delta >= 20
```

则：

```text
FORCE_PAPER_EXIT
```

归因：

```text
HIGH_RESULT_EXIT
```

---

### F. 数据质量恶化

```text
data_quality_score < 50
```

不直接退出，但标记：

```text
EXIT_MONITOR
```

归因候选：

```text
DATA_QUALITY_FAIL
```

---

## 5.5 paper runner 持仓更新伪代码

```python
from pathlib import Path

from sikk.wallet_structure.sikk_wallet_structure_gate import load_decision


def evaluate_wallet_structure_for_open_position(
    position: dict,
    token_address: str,
    wallet_structure_dir: str = "data/gmgn_candidates_live_run/wallet_structure",
) -> dict:
    decision_path = Path(wallet_structure_dir) / token_address / "wallet_structure_decision.json"

    if not decision_path.exists():
        return {
            "action": "HOLD",
            "failure_candidate": None,
            "reason": "缺少最新钱包结构决策，暂不改变持仓",
        }

    current = load_decision(decision_path)

    entry_structure_score = float(position.get("wallet_structure_score") or 0)
    entry_risk_score = float(position.get("wallet_risk_score") or 0)
    entry_counterparty_score = float(position.get("counterparty_pressure_score") or 0)

    current_structure_score = current.wallet_structure_score
    current_risk_score = current.wallet_risk_score
    current_counterparty_score = current.counterparty_pressure_score

    wallet_structure_score_delta = current_structure_score - entry_structure_score
    wallet_risk_score_delta = current_risk_score - entry_risk_score
    counterparty_pressure_score_delta = current_counterparty_score - entry_counterparty_score

    metrics = current.metrics

    same_source_sync_sell_score = float(metrics.get("same_source_sync_sell_score") or 0)
    same_source_group_sold_pct_delta = float(metrics.get("same_source_group_sold_pct_delta") or 0)
    early_wallet_sold_pct_delta = float(metrics.get("early_wallet_sold_pct_delta") or 0)
    high_result_remaining_pct_delta = float(metrics.get("high_result_remaining_pct_delta") or 0)
    data_quality_score = current.data_quality_score
    position_pnl_pct = float(position.get("unrealized_pnl_pct") or 0)

    # 1. 钱包结构转为 BLOCK
    if current.wallet_structure_status == "WALLET_BLOCK":
        return {
            "action": "FORCE_PAPER_EXIT",
            "failure_candidate": "STRUCTURE_WEAKENING",
            "reason": current.reason,
            "current_wallet_decision": current,
        }

    # 2. 对手盘压力快速上升
    if counterparty_pressure_score_delta >= 25 and current_counterparty_score >= 70:
        return {
            "action": "FORCE_PAPER_EXIT",
            "failure_candidate": "COUNTERPARTY_ABSORBING",
            "reason": "对手盘压力快速上升，疑似筹码向晚期承接方转移",
            "current_wallet_decision": current,
        }

    # 3. 同源组同步卖出
    if same_source_sync_sell_score >= 70 or same_source_group_sold_pct_delta >= 20:
        return {
            "action": "FORCE_PAPER_EXIT",
            "failure_candidate": "SAME_SOURCE_EXIT",
            "reason": "疑似同源组同步卖出，结构侧撤退风险高",
            "current_wallet_decision": current,
        }

    # 4. 早期钱包快速退出
    if early_wallet_sold_pct_delta >= 20 and position_pnl_pct <= 0:
        return {
            "action": "FORCE_PAPER_EXIT",
            "failure_candidate": "WALLET_EXIT",
            "reason": "早期钱包快速退出且当前仓位未盈利",
            "current_wallet_decision": current,
        }

    if early_wallet_sold_pct_delta >= 20:
        return {
            "action": "EXIT_MONITOR",
            "failure_candidate": "WALLET_EXIT",
            "reason": "早期钱包卖出增加，进入退出观察",
            "current_wallet_decision": current,
        }

    # 5. 高结果钱包退出
    if high_result_remaining_pct_delta <= -20 and wallet_risk_score_delta >= 20:
        return {
            "action": "FORCE_PAPER_EXIT",
            "failure_candidate": "HIGH_RESULT_EXIT",
            "reason": "高结果钱包退出且钱包风险分明显上升",
            "current_wallet_decision": current,
        }

    if high_result_remaining_pct_delta <= -20:
        return {
            "action": "EXIT_MONITOR",
            "failure_candidate": "HIGH_RESULT_EXIT",
            "reason": "高结果钱包剩余筹码下降，进入退出观察",
            "current_wallet_decision": current,
        }

    # 6. 数据质量不足
    if data_quality_score < 50:
        return {
            "action": "EXIT_MONITOR",
            "failure_candidate": "DATA_QUALITY_FAIL",
            "reason": "当前钱包结构数据质量下降，降低判断可信度",
            "current_wallet_decision": current,
        }

    return {
        "action": "HOLD",
        "failure_candidate": None,
        "reason": "钱包结构未触发退出条件",
        "current_wallet_decision": current,
    }
```

---

# 6. failure_attribution 接入 paper runner

当 paper runner 触发 `FORCE_PAPER_EXIT` 时，写入：

```text
failure_attribution.csv
```

字段：

```text
position_id
token_address
entry_time
exit_time
failure_type
primary_reason
wallet_structure_status_at_entry
wallet_structure_score_at_entry
wallet_risk_score_at_entry
counterparty_pressure_score_at_entry
wallet_structure_status_before_exit
wallet_structure_score_before_exit
wallet_risk_score_before_exit
counterparty_pressure_score_before_exit
wallet_structure_score_delta
wallet_risk_score_delta
counterparty_pressure_score_delta
suggested_rule_adjustment
```

归因生成骨架：

```python
def build_wallet_failure_attribution(
    position: dict,
    evaluation: dict,
) -> dict:
    current = evaluation.get("current_wallet_decision")
    failure_type = evaluation.get("failure_candidate") or "STRUCTURE_FAIL"

    return {
        "position_id": position.get("position_id"),
        "token_address": position.get("token_address"),
        "entry_time": position.get("entry_time"),
        "exit_time": position.get("last_update_time"),

        "failure_type": failure_type,
        "primary_reason": evaluation.get("reason"),

        "wallet_structure_status_at_entry": position.get("wallet_structure_status"),
        "wallet_structure_score_at_entry": position.get("wallet_structure_score"),
        "wallet_risk_score_at_entry": position.get("wallet_risk_score"),
        "counterparty_pressure_score_at_entry": position.get("counterparty_pressure_score"),

        "wallet_structure_status_before_exit": getattr(current, "wallet_structure_status", None),
        "wallet_structure_score_before_exit": getattr(current, "wallet_structure_score", None),
        "wallet_risk_score_before_exit": getattr(current, "wallet_risk_score", None),
        "counterparty_pressure_score_before_exit": getattr(current, "counterparty_pressure_score", None),

        "wallet_structure_score_delta": (
            getattr(current, "wallet_structure_score", 0)
            - float(position.get("wallet_structure_score") or 0)
        ),
        "wallet_risk_score_delta": (
            getattr(current, "wallet_risk_score", 0)
            - float(position.get("wallet_risk_score") or 0)
        ),
        "counterparty_pressure_score_delta": (
            getattr(current, "counterparty_pressure_score", 0)
            - float(position.get("counterparty_pressure_score") or 0)
        ),

        "suggested_rule_adjustment": suggest_wallet_rule_adjustment(failure_type),
    }


def suggest_wallet_rule_adjustment(failure_type: str) -> str:
    if failure_type == "COUNTERPARTY_ABSORBING":
        return "检查 counterparty_pressure_score 阈值是否过松；若多次出现，考虑 >=50 即 PAUSE"
    if failure_type == "SAME_SOURCE_EXIT":
        return "确认 sync_sell_score >=70 是否已强制 WALLET_BLOCK"
    if failure_type == "WALLET_EXIT":
        return "检查 early_wallet_sold_pct_delta 是否应加入持仓中退出规则"
    if failure_type == "HIGH_RESULT_EXIT":
        return "检查 high_result_remaining_pct_delta 是否应提高风险权重"
    if failure_type == "DATA_QUALITY_FAIL":
        return "检查 data_quality_score <50 是否仍允许入场"
    return "复盘该失败样本并检查钱包结构门禁阈值"
```

---

# 7. 最小开发顺序

按这个顺序做，不要反过来：

```text
1. 先实现 sikk_wallet_structure_gate.py
2. 先跑 tests/test_sikk_wallet_structure_gate.py
3. 再接 sikk_candidate_wallet_structure_pipeline.py
4. 再生成 wallet_structure_decision.json
5. 再让状态机读取 wallet_structure_decision.json
6. 再让 paper runner 写入 wallet_structure_factor
7. 最后做持仓中钱包结构恶化监控
```

核心验收：

```text
WALLET_BLOCK 能阻断 PAPER_READY
WALLET_PAUSE 能暂停
WALLET_SUPPORT 只能允许继续过 quote/security/signal
paper position 能保存钱包结构分数
paper runner 能因钱包结构恶化触发 FORCE_PAPER_EXIT
failure_attribution 能记录钱包结构失败原因
```

---

# 本次认知升级点

这一步把系统从“钱包结构分析报告”推进为：

```text
钱包结构门禁
+ 状态机接入
+ paper runner 持仓监控
+ failure_attribution 归因闭环
```

现在钱包结构不只是看报告，而是能实际影响：

```text
是否进入 PAPER_READY
是否继续持有 paper position
失败后归因到哪类钱包结构问题
```

---

# 尚未解决问题

下一步最应该继续做：

```text
1. same_source_group_id 的实际生成代码
2. sikk_candidate_wallet_structure_pipeline.py 如何读取你现有 sikk_gmgn_token_report.py 输出
3. snapshots/delta 的真实文件生成逻辑
4. paper runner 的 FORCE_PAPER_EXIT 是否立即退出，还是先触发 EXIT_MONITOR
5. daily_report 如何统计不同 wallet_structure_status 的胜率和收益
```


---

## 片段 48 / stream_idx=6897 / len=227


1. sikk_wallet_structure_gate.py 的完整代码骨架
2. tests/test_sikk_wallet_structure_gate.py 测试样例
3. sikk_candidate_wallet_structure_pipeline.py 的输入输出流程
4. wallet_structure_decision.json 与状态机的实际接入点
5. paper runner 如何根据钱包结构变化触发持仓管理或提前退出


---

## 片段 49 / stream_idx=7280 / len=26942


# SIKK-SOL v1.0：5 个工程问题定稿

这 5 个问题要按一个原则处理：

```text
v1.0 不追求完美链上归因。
v1.0 先做“可运行、可解释、可复盘”的近似识别。
后续用 10 / 30 / 100 个 token 样本校准阈值。
```

核心目标：

```text
把钱包结构从“人工看图判断”变成状态机可读取的结构证据。
```

---

# 1. same_source_group_id 如何生成

## 1.1 定义

`same_source_group_id` 不是直接证明“同一个庄家”，而是表示：

```text
一组钱包在资金来源、入场时间、买入金额、行为节奏上高度相似，疑似属于同一执行组。
```

系统表达应该是：

```text
疑似同源组
疑似执行组
疑似协同行为组
```

不要写：

```text
庄家组
内幕组
老鼠仓组
```

---

## 1.2 v1.0 使用三类证据生成同源组

### A. 强证据：资金来源相同

字段：

```text
funding_source_address
funding_source_label
first_funding_time
first_funding_amount_sol
```

判断：

```text
多个钱包来自同一个 funding_source_address
且不是明显 CEX / 路由器 / 大型公共地址
```

这类证据最强。

---

### B. 中证据：资金来源相似 + 入场接近

字段：

```text
funding_source_label
funding_time_bucket
funding_amount_bucket
entry_time
entry_rank
buy_amount_usd
```

判断：

```text
资金来源类型相同
资金到账时间接近
买入时间接近
买入金额相近
```

---

### C. 弱证据：行为高度同步

字段：

```text
entry_time
entry_rank
buy_amount_usd
sell_time
sold_pct
remaining_pct
trade_count
```

判断：

```text
没有明确资金来源，但多个钱包在极短时间内相似买入、相似卖出。
```

这类只能作为：

```text
behavior_group
```

不能强行判为资金同源。

---

## 1.3 不要把这些地址直接当同源

以下来源必须降权：

```text
CEX 热钱包
OKX / Binance / Bybit 等交易所标签
Jupiter / Raydium / 路由器
公共中转地址
空投分发合约
高频 bot 公共地址
```

原因：

```text
多个钱包都来自 CEX，不代表它们同源。
多个钱包都经过 Jupiter，不代表它们同源。
```

所以 v1.0 要加一个字段：

```text
source_reliability
```

取值：

```text
HIGH      明确非公共资金源
MEDIUM    可疑中转或小型来源
LOW       CEX / 路由器 / 公共地址
UNKNOWN   无法判断
```

---

## 1.4 same_source_group_id 生成流程

### 第一步：生成钱包指纹

每个钱包生成 3 个 signature。

```python
funding_signature = (
    funding_source_address,
    funding_time_bucket,
    funding_amount_bucket
)

entry_signature = (
    entry_time_bucket,
    entry_rank_bucket,
    buy_amount_bucket
)

behavior_signature = (
    buy_count_bucket,
    sell_count_bucket,
    sold_pct_bucket,
    remaining_pct_bucket
)
```

---

### 第二步：计算两两相似度

每两个钱包计算：

```text
same_source_similarity_score
```

满分 100。

| 维度 | 分数 |
|---|---:|
| funding_source_address 相同 | 40 |
| funding_time 接近 | 15 |
| funding_amount 相近 | 10 |
| entry_time 接近 | 15 |
| buy_amount 相近 | 10 |
| sell / hold 行为相似 | 10 |
| 合计 | 100 |

---

### 第三步：建立边

```text
similarity_score >= 70 → 建立强边
50 <= similarity_score < 70 → 建立弱边
< 50 → 不连边
```

---

### 第四步：形成连通分组

把强边连接的钱包形成 group。

```text
group_size >= 3 → same_source_group
group_size < 3 → 暂不生成正式 group_id，只记录 pair_similarity
```

---

### 第五步：生成 group_id

格式建议：

```text
SSG_<token_symbol>_<hash前6位>
```

例如：

```text
SSG_TEST_8f3a21
```

hash 来源：

```text
token_address + primary_funding_source + first_entry_time_bucket
```

---

## 1.5 same_source_group_id 输出字段

`candidate_groups.csv` 建议字段：

```text
token_address
group_id
group_type
group_size
wallets
primary_evidence
source_reliability
avg_entry_rank
entry_time_span_sec
avg_buy_amount_usd
buy_amount_cv
sync_buy_score
sync_sell_score
group_remaining_pct
group_sold_pct
group_risk_level
group_evidence_level
reason
```

---

## 1.6 group_type 枚举

```text
FUNDING_STRONG_GROUP      强资金同源组
FUNDING_WEAK_GROUP        弱资金同源组
BEHAVIOR_SYNC_GROUP       行为同步组
CEX_AMBIGUOUS_GROUP       CEX 来源模糊组
UNKNOWN_GROUP             未知组
```

---

# 2. sync_buy_score / sync_sell_score 如何计算

这两个分数最好做成**组级分数**，不是单钱包分数。

```text
sync_buy_score：这一组钱包是否同步买入？
sync_sell_score：这一组钱包是否同步卖出？
```

范围：

```text
0 - 100
```

---

# 2.1 sync_buy_score 计算公式

## 公式

```text
sync_buy_score =
  buy_time_cohesion_score
+ entry_rank_cohesion_score
+ buy_amount_similarity_score
+ buy_participation_score
+ funding_support_score
```

权重：

| 维度 | 分数 |
|---|---:|
| 买入时间集中度 | 30 |
| 入场排名集中度 | 20 |
| 买入金额相似度 | 15 |
| 参与比例 | 20 |
| 资金来源支持 | 15 |
| 合计 | 100 |

---

## A. buy_time_cohesion_score：买入时间集中度，0-30

计算：

```text
entry_time_span_sec = max(first_buy_time) - min(first_buy_time)
```

规则：

```text
<= 30 秒     → 30
<= 2 分钟    → 24
<= 5 分钟    → 16
<= 10 分钟   → 8
> 10 分钟    → 0
```

---

## B. entry_rank_cohesion_score：入场排名集中度，0-20

计算：

```text
entry_rank_span = max(entry_rank) - min(entry_rank)
```

规则：

```text
<= 10   → 20
<= 25   → 15
<= 50   → 8
> 50    → 0
```

---

## C. buy_amount_similarity_score：买入金额相似度，0-15

用变异系数：

```text
buy_amount_cv = std(buy_amount_usd) / mean(buy_amount_usd)
```

规则：

```text
cv <= 0.25 → 15
cv <= 0.50 → 10
cv <= 1.00 → 5
cv > 1.00  → 0
```

---

## D. buy_participation_score：参与比例，0-20

计算：

```text
buy_participation_ratio = 有买入行为的钱包数 / group_size
```

规则：

```text
>= 90% → 20
>= 70% → 14
>= 50% → 8
< 50%  → 0
```

---

## E. funding_support_score：资金来源支持，0-15

规则：

```text
FUNDING_STRONG_GROUP → 15
FUNDING_WEAK_GROUP   → 8
BEHAVIOR_SYNC_GROUP  → 3
CEX_AMBIGUOUS_GROUP  → 0
UNKNOWN_GROUP        → 0
```

---

## sync_buy_score 解释

| 分数 | 解释 |
|---:|---|
| 0-39 | 无明显同步买入 |
| 40-59 | 弱同步 |
| 60-79 | 较强同步 |
| 80-100 | 高度同步买入 |

---

# 2.2 sync_sell_score 计算公式

## 公式

```text
sync_sell_score =
  sell_time_cohesion_score
+ sell_participation_score
+ sold_pct_similarity_score
+ group_exit_pressure_score
+ top_holder_exit_bonus
```

权重：

| 维度 | 分数 |
|---|---:|
| 卖出时间集中度 | 30 |
| 卖出参与比例 | 25 |
| 卖出比例相似度 | 15 |
| 组内整体退出压力 | 20 |
| Top Holder 出货加权 | 10 |
| 合计 | 100 |

---

## A. sell_time_cohesion_score：卖出时间集中度，0-30

计算：

```text
sell_time_span_sec = max(first_major_sell_time) - min(first_major_sell_time)
```

只统计：

```text
sold_pct >= 20
```

的钱包。

规则：

```text
<= 1 分钟    → 30
<= 5 分钟    → 22
<= 15 分钟   → 12
<= 30 分钟   → 6
> 30 分钟    → 0
```

---

## B. sell_participation_score：卖出参与比例，0-25

计算：

```text
sell_participation_ratio = sold_pct >= 20 的钱包数 / group_size
```

规则：

```text
>= 90% → 25
>= 70% → 18
>= 50% → 10
< 50%  → 0
```

---

## C. sold_pct_similarity_score：卖出比例相似度，0-15

计算：

```text
sold_pct_cv = std(sold_pct) / mean(sold_pct)
```

规则：

```text
cv <= 0.25 → 15
cv <= 0.50 → 10
cv <= 1.00 → 5
cv > 1.00  → 0
```

---

## D. group_exit_pressure_score：组内整体退出压力，0-20

计算：

```text
group_sold_pct = sum(sell_amount) / sum(buy_amount)
```

规则：

```text
group_sold_pct >= 80 → 20
>= 60 → 15
>= 40 → 8
< 40  → 0
```

---

## E. top_holder_exit_bonus：Top Holder 出货加权，0-10

规则：

```text
组内存在 Top Holder 且 sold_pct >= 60 → 10
组内存在 Top Holder 且 sold_pct >= 30 → 5
否则 → 0
```

---

## sync_sell_score 解释

| 分数 | 解释 | 动作倾向 |
|---:|---|---|
| 0-39 | 无明显同步卖出 | 正常 |
| 40-59 | 弱同步卖出 | 观察 |
| 60-69 | 较强同步卖出 | PAUSE |
| >=70 | 高度同步卖出 | WALLET_BLOCK |

---

# 2.3 关键应用逻辑

同源组不是天然风险。

```text
sync_buy_score 高 + sync_sell_score 低 = 可能是结构支持
sync_buy_score 高 + sync_sell_score 高 = 结构撤退风险
sync_buy_score 低 + sync_sell_score 高 = 异常同步出货
```

建议规则：

```text
if sync_sell_score >= 70:
    WALLET_BLOCK

elif sync_sell_score >= 60:
    WALLET_PAUSE

elif sync_buy_score >= 70 and sync_sell_score < 40:
    增加 wallet_structure_score

elif sync_buy_score >= 70 and sync_sell_score >= 50:
    增加 wallet_risk_score
```

---

# 3. counterparty_pressure_score 的精确字段来源

## 3.1 定义

`counterparty_pressure_score` 回答：

```text
主导侧是否正在把筹码转移给对手盘？
```

也就是判断：

```text
当前入场会不会成为早期钱包 / 结构钱包的退出流动性。
```

---

## 3.2 所需字段来源

### A. 早期钱包卖出字段

来源：

```text
early_wallet_raw.csv
wallet_classification.csv
GMGN early buyer / holder 数据
```

字段：

```text
early_wallet_sold_pct
early_wallet_remaining_pct
early_wallet_sold_pct_delta
early_exit_wallet_count
```

用途：

```text
判断早期优势筹码是否正在退出。
```

---

### B. 晚期买盘字段

来源：

```text
GMGN holder 数据
GMGN top trader
交易记录 / holder snapshot
```

字段：

```text
late_buyer_count
late_buyer_buy_amount_usd
late_buyer_ratio
late_large_buyer_count
late_large_buyer_total_buy_usd
```

定义建议：

```text
late_buyer = entry_rank > 100
或 entry_time > token_open_time + 30 分钟
```

如果是短生命周期 meme：

```text
late_buyer = entry_time > token_open_time + 10 分钟
```

---

### C. 套牢鲸鱼字段

来源：

```text
wallet_classification.csv
```

字段：

```text
bagholder_whale_count
bagholder_whale_total_holding_pct
bagholder_whale_avg_roi_pct
```

定义：

```text
holding_pct >= 1
roi_pct <= -30
remaining_pct >= 70
```

---

### D. 价格上涨但结构钱包卖出

来源：

```text
K线数据
wallet snapshot delta
```

字段：

```text
price_change_pct
volume_change_pct
early_wallet_sold_pct_delta
same_source_group_sold_pct_delta
high_result_remaining_pct_delta
```

危险结构：

```text
price_change_pct > 0
且 early_wallet_sold_pct_delta > 0
```

更危险：

```text
price_change_pct > 0
且 same_source_group_sold_pct_delta > 0
且 high_result_remaining_pct_delta < 0
```

---

### E. 持有人数增加但 Top Holder 下降

来源：

```text
GMGN holder count
Top holder snapshot
```

字段：

```text
holder_count_delta
top_holder_pct_delta
top10_holder_pct_delta
top20_holder_pct_delta
```

危险结构：

```text
holder_count_delta > 0
且 top_holder_pct_delta < 0
```

含义：

```text
筹码从集中钱包向分散钱包扩散。
```

---

### F. 高结果钱包退出

来源：

```text
wallet_classification.csv
snapshot delta
```

字段：

```text
high_result_wallet_count
high_result_remaining_pct
high_result_remaining_pct_delta
high_result_exit_count
```

---

## 3.3 counterparty_pressure_score 公式

满分 100。

```text
counterparty_pressure_score =
  early_to_late_transfer_score
+ late_large_buyer_score
+ bagholder_pressure_score
+ price_up_structure_sell_score
+ holder_growth_top_exit_score
+ high_result_exit_score
```

权重：

| 维度 | 分数 |
|---|---:|
| 早期钱包卖出给晚期买盘 | 25 |
| 晚期大额钱包增加 | 20 |
| 套牢鲸鱼增加 | 15 |
| 价格上涨但结构钱包卖出 | 20 |
| 持有人数增加但 Top Holder 下降 | 10 |
| 高结果钱包退出 | 10 |
| 合计 | 100 |

---

## A. early_to_late_transfer_score，0-25

规则：

```text
early_wallet_sold_pct_delta >= 20 且 late_buyer_buy_amount_delta > 0 → 25
early_wallet_sold_pct_delta >= 10 且 late_buyer_buy_amount_delta > 0 → 18
early_wallet_sold_pct_delta >= 5  且 late_buyer_buy_amount_delta > 0 → 10
否则 → 0
```

如果没有 delta 数据，则降级使用静态字段：

```text
early_wallet_sold_pct >= 70 且 late_buyer_ratio >= 40 → 18
early_wallet_sold_pct >= 50 且 late_buyer_ratio >= 30 → 10
否则 → 0
```

---

## B. late_large_buyer_score，0-20

规则：

```text
late_large_buyer_count >= 5 → 20
late_large_buyer_count >= 3 → 14
late_large_buyer_count >= 1 → 6
否则 → 0
```

`late_large_buyer` 初始定义：

```text
entry_rank > 100
且 buy_amount_usd >= 该 token 钱包买入金额的 P80
```

---

## C. bagholder_pressure_score，0-15

规则：

```text
bagholder_whale_count >= 5 → 15
bagholder_whale_count >= 3 → 10
bagholder_whale_count >= 1 → 5
否则 → 0
```

---

## D. price_up_structure_sell_score，0-20

规则：

```text
price_change_pct > 20
且 early_wallet_sold_pct_delta >= 15
→ 20
```

```text
price_change_pct > 10
且 same_source_group_sold_pct_delta >= 10
→ 16
```

```text
price_change_pct > 0
且 high_result_remaining_pct_delta <= -10
→ 10
```

否则：

```text
0
```

---

## E. holder_growth_top_exit_score，0-10

规则：

```text
holder_count_delta > 10%
且 top10_holder_pct_delta <= -5%
→ 10
```

```text
holder_count_delta > 5%
且 top10_holder_pct_delta <= -3%
→ 6
```

否则：

```text
0
```

---

## F. high_result_exit_score，0-10

规则：

```text
high_result_remaining_pct_delta <= -30 → 10
high_result_remaining_pct_delta <= -15 → 6
high_result_remaining_pct_delta <= -5  → 3
否则 → 0
```

如果没有 delta 数据，用静态字段：

```text
high_result_wallet_count >= 2 且 high_result_remaining_pct <= 10 → 10
high_result_wallet_count >= 1 且 high_result_remaining_pct <= 20 → 6
否则 → 0
```

---

## 3.4 counterparty_pressure_score 动作

| 分数 | 含义 | 动作 |
|---:|---|---|
| 0-29 | 对手盘压力低 | 正常 |
| 30-49 | 轻度压力 | 观察 |
| 50-69 | 中等压力 | WALLET_PAUSE |
| 70-100 | 高压力 | WALLET_BLOCK 或强 PAUSE |

门禁规则：

```text
counterparty_pressure_score >= 70
且 wallet_risk_score >= 50
→ WALLET_BLOCK
```

```text
counterparty_pressure_score >= 50
→ WALLET_PAUSE
```

---

# 4. 多轮快照 delta 如何设计

## 4.1 为什么必须做 delta

单次快照只能回答：

```text
现在是什么状态？
```

多轮快照才能回答：

```text
状态正在往哪里变化？
```

SIKK 真正有价值的是：

```text
筹码控制权变化
结构侧增强 / 减弱
派发开始 / 加速
对手盘接货
```

这些都必须靠 delta。

---

## 4.2 快照频率建议

v1.0 建议：

| token 状态 | 快照频率 |
|---|---:|
| WATCHING | 10 分钟一次 |
| PAPER_READY | 3-5 分钟一次 |
| PAPER_OPEN | 3 分钟一次 |
| 高风险 PAUSE | 5 分钟一次 |
| BLOCKED | 30-60 分钟一次，可降低频率 |

---

## 4.3 snapshot 文件结构

目录：

```text
data/gmgn_candidates_live_run/wallet_structure/<token>/snapshots/
```

每次生成：

```text
snapshot_20260502_120000.json
snapshot_20260502_120500.json
snapshot_20260502_121000.json
```

同时生成 delta：

```text
delta_20260502_120000__20260502_120500.json
```

---

## 4.4 单次 snapshot 标准

```json
{
  "token_address": "TOKEN_ADDRESS",
  "snapshot_time": "2026-05-02T12:05:00Z",
  "price": 0.000123,
  "market_cap": 120000,
  "liquidity": 45000,
  "holder_count": 1830,
  "top10_holder_pct": 28.5,
  "top20_holder_pct": 39.2,
  "early_wallet_count": 50,
  "early_wallet_remaining_pct": 42.5,
  "early_wallet_sold_pct": 57.5,
  "high_result_wallet_count": 3,
  "high_result_remaining_pct": 31.2,
  "same_source_group_count": 2,
  "same_source_group_remaining_pct": 36.1,
  "same_source_group_sold_pct": 63.9,
  "distribution_wallet_count": 1,
  "bagholder_whale_count": 0,
  "late_buyer_count": 12,
  "late_large_buyer_count": 2,
  "late_buyer_buy_amount_usd": 8500,
  "wallet_structure_score": 72,
  "wallet_risk_score": 28,
  "counterparty_pressure_score": 32,
  "data_quality_score": 76,
  "dominant_side_status": "STRUCTURE_HOLDING",
  "chip_transfer_status": "NO_MAJOR_TRANSFER"
}
```

---

## 4.5 delta 标准字段

```json
{
  "token_address": "TOKEN_ADDRESS",
  "from_snapshot": "2026-05-02T12:00:00Z",
  "to_snapshot": "2026-05-02T12:05:00Z",
  "time_delta_sec": 300,
  "price_change_pct": 12.5,
  "market_cap_change_pct": 13.1,
  "liquidity_change_pct": -2.4,
  "holder_count_delta": 95,
  "holder_count_delta_pct": 5.4,
  "top10_holder_pct_delta": -3.2,
  "top20_holder_pct_delta": -2.1,
  "early_wallet_remaining_pct_delta": -8.5,
  "early_wallet_sold_pct_delta": 8.5,
  "high_result_remaining_pct_delta": -6.0,
  "same_source_group_remaining_pct_delta": -10.2,
  "same_source_group_sold_pct_delta": 10.2,
  "distribution_wallet_count_delta": 2,
  "bagholder_whale_count_delta": 1,
  "late_buyer_count_delta": 8,
  "late_large_buyer_count_delta": 2,
  "late_buyer_buy_amount_usd_delta": 4200,
  "wallet_structure_score_delta": -14,
  "wallet_risk_score_delta": 18,
  "counterparty_pressure_score_delta": 26,
  "dominant_side_status_from": "STRUCTURE_HOLDING",
  "dominant_side_status_to": "STRUCTURE_WEAKENING",
  "chip_transfer_status": "EARLY_TO_LATE_TRANSFER",
  "delta_interpretation": "价格上涨，但早期钱包与同源组卖出增加，晚期大额买盘增加，疑似筹码向对手盘转移"
}
```

---

## 4.6 chip_transfer_status 枚举

```text
NO_MAJOR_TRANSFER              未发现明显筹码迁移
STRUCTURE_ACCUMULATION         结构侧继续吸收
STRUCTURE_HOLDING              结构侧维持
EARLY_TO_LATE_TRANSFER         早期钱包 → 晚期钱包
GROUP_TO_RETAIL_TRANSFER       同源组 → 分散钱包
PROFIT_WALLET_EXIT             高结果钱包退出
DISTRIBUTION_TO_COUNTERPARTY   派发侧 → 对手盘
COUNTERPARTY_TRAPPED           对手盘承接后被套
UNKNOWN                        不明确
```

---

## 4.7 dominant_side_status 迁移规则

### STRUCTURE_STRENGTHENING

条件：

```text
early_wallet_remaining_pct_delta >= 0
same_source_group_sold_pct_delta <= 5
counterparty_pressure_score_delta <= 10
price_change_pct > 0
```

含义：

```text
结构侧没有明显卖出，价格在推进。
```

---

### STRUCTURE_HOLDING

条件：

```text
early_wallet_remaining_pct_delta > -10
same_source_group_sold_pct_delta < 10
wallet_risk_score_delta < 10
```

含义：

```text
结构侧有轻微变化，但没有撤退。
```

---

### STRUCTURE_WEAKENING

条件：

```text
early_wallet_remaining_pct_delta <= -10
或 high_result_remaining_pct_delta <= -10
或 same_source_group_sold_pct_delta >= 10
```

含义：

```text
结构侧开始减弱。
```

---

### DISTRIBUTION_ACTIVE

条件：

```text
distribution_wallet_count_delta >= 2
或 same_source_group_sold_pct_delta >= 20
或 top10_holder_pct_delta <= -5 且 price_change_pct > 0
```

含义：

```text
存在主动派发迹象。
```

---

### COUNTERPARTY_ABSORBING

条件：

```text
late_large_buyer_count_delta >= 2
且 early_wallet_sold_pct_delta >= 10
```

或：

```text
holder_count_delta_pct > 5
且 top10_holder_pct_delta <= -3
```

含义：

```text
筹码正在向晚期对手盘扩散。
```

---

# 5. 钱包结构失败如何进入 failure_attribution

## 5.1 原则

每一笔失败交易，都要问：

```text
这次失败是不是钱包结构提前给过风险信号？
```

如果给过，但系统没拦住：

```text
门禁太松。
```

如果没给过，但事后发生结构恶化：

```text
快照频率不够，或 delta 规则不足。
```

如果结构支持但 K线失败：

```text
不是钱包结构失败，而是价格结构 / 动能失败。
```

---

## 5.2 新增失败类型

在 `failure_attribution` 中加入钱包结构相关类型：

```text
WALLET_EXIT
SAME_SOURCE_EXIT
DISTRIBUTION_ACTIVE
COUNTERPARTY_ABSORBING
STRUCTURE_WEAKENING
HIGH_RESULT_EXIT
BAGHOLDER_PRESSURE
DATA_QUALITY_FAIL
WALLET_GATE_MISSED
WALLET_FALSE_SUPPORT
```

---

## 5.3 failure_attribution 字段

```text
position_id
token_address
entry_time
exit_time
failure_type
primary_reason
secondary_reason
wallet_structure_status_at_entry
wallet_structure_score_at_entry
wallet_risk_score_at_entry
counterparty_pressure_score_at_entry
data_quality_score_at_entry
dominant_side_status_at_entry
chip_transfer_status_at_entry
wallet_structure_status_before_exit
wallet_structure_score_delta
wallet_risk_score_delta
counterparty_pressure_score_delta
early_wallet_sold_pct_delta
same_source_group_sold_pct_delta
high_result_remaining_pct_delta
distribution_wallet_count_delta
late_large_buyer_count_delta
evidence_json
suggested_rule_adjustment
created_at
```

---

## 5.4 归因规则

### A. WALLET_EXIT

条件：

```text
early_wallet_sold_pct_delta >= 20
且 position_pnl_pct < 0
```

或：

```text
early_wallet_remaining_pct 在持仓期间下降超过 20%
```

归因：

```text
早期钱包持仓明显下降，结构侧撤退导致失败。
```

---

### B. SAME_SOURCE_EXIT

条件：

```text
same_source_group_sold_pct_delta >= 20
或 sync_sell_score >= 70
```

归因：

```text
疑似同源执行组同步卖出。
```

动作建议：

```text
以后 sync_sell_score >= 70 必须 WALLET_BLOCK。
```

---

### C. DISTRIBUTION_ACTIVE

条件：

```text
distribution_wallet_count_delta >= 2
且 price_change_pct >= 0
```

或：

```text
top10_holder_pct_delta <= -5
且 holder_count_delta_pct > 5
```

归因：

```text
价格维持或上涨过程中出现筹码扩散，疑似派发。
```

---

### D. COUNTERPARTY_ABSORBING

条件：

```text
counterparty_pressure_score_delta >= 25
且 late_large_buyer_count_delta >= 2
```

归因：

```text
晚期大额承接增加，早期结构侧筹码减少，疑似成为退出流动性。
```

---

### E. STRUCTURE_WEAKENING

条件：

```text
wallet_structure_score_delta <= -20
或 wallet_risk_score_delta >= 20
```

归因：

```text
入场后钱包结构快速恶化。
```

---

### F. HIGH_RESULT_EXIT

条件：

```text
high_result_remaining_pct_delta <= -20
```

归因：

```text
高结果钱包集中退出，优势钱包撤退。
```

---

### G. BAGHOLDER_PRESSURE

条件：

```text
bagholder_whale_count_delta >= 2
且 price_change_pct <= 0
```

归因：

```text
大额承接后价格未推进，形成套牢压力。
```

---

### H. DATA_QUALITY_FAIL

条件：

```text
data_quality_score_at_entry < 50
且入场后失败
```

归因：

```text
数据质量不足仍允许入场，门禁过松。
```

---

### I. WALLET_FALSE_SUPPORT

条件：

```text
wallet_structure_status_at_entry == WALLET_SUPPORT
且 position_pnl_pct < -10
且 wallet_risk_score_delta >= 20
```

归因：

```text
钱包结构支持判断过松，未识别后续结构恶化风险。
```

---

### J. WALLET_GATE_MISSED

条件：

```text
entry 时已有以下任一风险：
counterparty_pressure_score >= 50
wallet_risk_score >= 50
sync_sell_score >= 60
data_quality_score < 50
但仍进入 PAPER_READY
```

归因：

```text
钱包结构门禁已有风险信号，但状态机没有正确拦截。
```

---

## 5.5 failure_attribution 示例

```json
{
  "position_id": "PAPER_20260502_001",
  "token_address": "TOKEN_ADDRESS",
  "failure_type": "COUNTERPARTY_ABSORBING",
  "primary_reason": "早期钱包卖出增加，晚期大额钱包承接增加，入场后价格未继续推进",
  "secondary_reason": "counterparty_pressure_score 在持仓期间从 38 上升到 74",
  "wallet_structure_status_at_entry": "WALLET_SUPPORT",
  "wallet_structure_score_at_entry": 68,
  "wallet_risk_score_at_entry": 34,
  "counterparty_pressure_score_at_entry": 38,
  "wallet_structure_status_before_exit": "WALLET_PAUSE",
  "wallet_structure_score_delta": -22,
  "wallet_risk_score_delta": 26,
  "counterparty_pressure_score_delta": 36,
  "early_wallet_sold_pct_delta": 18.5,
  "same_source_group_sold_pct_delta": 12.2,
  "late_large_buyer_count_delta": 3,
  "suggested_rule_adjustment": "当 counterparty_pressure_score_delta >= 25 且 early_wallet_sold_pct_delta >= 10 时，强制从 PAPER_OPEN 降级为 EXIT_MONITOR 或触发风控退出"
}
```

---

# 6. v1.0 直接落地的数据流

```text
GMGN wallet raw data
  ↓
wallet_classification.csv
  ↓
same_source_group_id 生成
  ↓
candidate_groups.csv
  ↓
sync_buy_score / sync_sell_score
  ↓
snapshot_*.json
  ↓
delta_*.json
  ↓
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
  ↓
wallet_structure_decision.json
  ↓
状态机
  ├─ WALLET_BLOCK → BLOCKED
  ├─ WALLET_PAUSE → PAUSE / WATCHING
  ├─ WALLET_SUPPORT → 可进入 PAPER_READY
  └─ WALLET_NEUTRAL → 继续其他门禁
  ↓
paper runner
  ↓
failure_attribution
  ↓
阈值校准
```

---

# 7. 直接给 AI / Codex 的开发指令

```text
任务：实现 SIKK-SOL v1.0 钱包结构门禁的同源组、同步分数、对手盘压力、多轮快照 delta、失败归因模块。

一、same_source_group_id

请为每个 token 的钱包生成 same_source_group_id。

输入字段：
- wallet_address
- funding_source_address
- funding_source_label
- first_funding_time
- first_funding_amount_sol
- entry_time
- entry_rank
- buy_amount_usd
- sell_amount_usd
- sold_pct
- remaining_pct
- trade_count
- buy_count
- sell_count

生成逻辑：
1. 对每个钱包生成 funding_signature、entry_signature、behavior_signature。
2. 计算钱包两两 similarity_score，满分 100。
3. 权重：
   - funding_source_address 相同：40
   - funding_time 接近：15
   - funding_amount 相近：10
   - entry_time 接近：15
   - buy_amount 相近：10
   - sell/hold 行为相似：10
4. similarity_score >= 70 建立强边。
5. group_size >= 3 生成 same_source_group_id。
6. 如果资金来源是 CEX、DEX 路由器、公共地址，则 source_reliability=LOW，并降低 group_evidence_level。
7. group_id 格式：SSG_<token_symbol>_<hash前6位>。

输出 candidate_groups.csv：
- token_address
- group_id
- group_type
- group_size
- wallets
- primary_evidence
- source_reliability
- avg_entry_rank
- entry_time_span_sec
- avg_buy_amount_usd
- buy_amount_cv
- sync_buy_score
- sync_sell_score
- group_remaining_pct
- group_sold_pct
- group_risk_level
- group_evidence_level
- reason

二、sync_buy_score

实现组级 sync_buy_score，满分 100：
- buy_time_cohesion_score：0-30
- entry_rank_cohesion_score：0-20
- buy_amount_similarity_score：0-15
- buy_participation_score：0-20
- funding_support_score：0-15

规则：
- entry_time_span <=30秒 → 30；<=2分钟 →24；<=5分钟 →16；<=10分钟 →8；否则0
- entry_rank_span <=10 →20；<=25 →15；<=50 →8；否则0
- buy_amount_cv <=0.25 →15；<=0.50 →10；<=1.00 →5；否则0
- buy_participation_ratio >=90% →20；>=70% →14；>=50% →8；否则0
- FUNDING_STRONG_GROUP →15；FUNDING_WEAK_GROUP →8；BEHAVIOR_SYNC_GROUP →3；其他0

三、sync_sell_score

实现组级 sync_sell_score，满分 100：
- sell_time_cohesion_score：0-30
- sell_participation_score：0-25
- sold_pct_similarity_score：0-15
- group_exit_pressure_score：0-20
- top_holder_exit_bonus：0-10

规则：
- sell_time_span <=1分钟 →30；<=5分钟 →22；<=15分钟 →12；<=30分钟 →6；否则0
- sell_participation_ratio >=90% →25；>=70% →18；>=50% →10；否则0
- sold_pct_cv <=0.25 →15；<=0.50 →10；<=1.00 →5；否则0
- group_sold_pct >=80 →20；>=60 →15；>=40 →8；否则0
- 组内存在 Top Holder 且 sold_pct >=60 →10；>=30 →5；否则0

应用规则：
- sync_sell_score >=70 → WALLET_BLOCK
- sync_sell_score >=60 → WALLET_PAUSE
- sync_buy_score >=70 且 sync_sell_score <40 → 增加 wallet_structure_score
- sync_buy_score >=70 且 sync_sell_score >=50 → 增加 wallet_risk_score

四、counterparty_pressure_score

实现 counterparty_pressure_score，满分 100：
- early_to_late_transfer_score：0-25
- late_large_buyer_score：0-20
- bagholder_pressure_score：0-15
- price_up_structure_sell_score：0-20
- holder_growth_top_exit_score：0-10
- high_result_exit_score：0-10

字段来源：
- early_wallet_sold_pct_delta
- early_wallet_remaining_pct_delta
- late_buyer_count_delta
- late_large_buyer_count_delta
- late_buyer_buy_amount_usd_delta
- bagholder_whale_count_delta
- price_change_pct
- holder_count_delta_pct
- top10_holder_pct_delta
- high_result_remaining_pct_delta

规则：
- early_wallet_sold_pct_delta >=20 且 late_buyer_buy_amount_delta >0 →25
- >=10 且 late_buyer_buy_amount_delta >0 →18
- >=5 且 late_buyer_buy_amount_delta >0 →10
- late_large_buyer_count >=5 →20；>=3 →14；>=1 →6
- bagholder_whale_count >=5 →15；>=3 →10；>=1 →5
- price_change_pct >20 且 early_wallet_sold_pct_delta >=15 →20
- price_change_pct >10 且 same_source_group_sold_pct_delta >=10 →16
- price_change_pct >0 且 high_result_remaining_pct_delta <=-10 →10
- holder_count_delta_pct >10 且 top10_holder_pct_delta <=-5 →10
- holder_count_delta_pct >5 且 top10_holder_pct_delta <=-3 →6
- high_result_remaining_pct_delta <=-30 →10；<=-15 →6；<=-5 →3

动作：
- counterparty_pressure_score >=70 且 wallet_risk_score >=50 → WALLET_BLOCK
- counterparty_pressure_score >=50 → WALLET_PAUSE

五、多轮快照 delta

为每个 token 生成：
data/gmgn_candidates_live_run/wallet_structure/<token>/snapshots/snapshot_<timestamp>.json
data/gmgn_candidates_live_run/wallet_structure/<token>/snapshots/delta_<from>__<to>.json

snapshot 字段至少包含：
- token_address
- snapshot_time
- price
- market_cap
- liquidity
- holder_count
- top10_holder_pct
- top20_holder_pct
- early_wallet_count
- early_wallet_remaining_pct
- early_wallet_sold_pct
- high_result_wallet_count
- high_result_remaining_pct
- same_source_group_count
- same_source_group_remaining_pct
- same_source_group_sold_pct
- distribution_wallet_count
- bagholder_whale_count
- late_buyer_count
- late_large_buyer_count
- late_buyer_buy_amount_usd
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- dominant_side_status
- chip_transfer_status

delta 字段至少包含：
- price_change_pct
- holder_count_delta_pct
- top10_holder_pct_delta
- early_wallet_remaining_pct_delta
- early_wallet_sold_pct_delta
- high_result_remaining_pct_delta
- same_source_group_remaining_pct_delta
- same_source_group_sold_pct_delta
- distribution_wallet_count_delta
- bagholder_whale_count_delta
- late_buyer_count_delta
- late_large_buyer_count_delta
- late_buyer_buy_amount_usd_delta
- wallet_structure_score_delta
- wallet_risk_score_delta
- counterparty_pressure_score_delta
- dominant_side_status_from
- dominant_side_status_to
- chip_transfer_status
- delta_interpretation

六、chip_transfer_status

实现枚举：
- NO_MAJOR_TRANSFER
- STRUCTURE_ACCUMULATION
- STRUCTURE_HOLDING
- EARLY_TO_LATE_TRANSFER
- GROUP_TO_RETAIL_TRANSFER
- PROFIT_WALLET_EXIT
- DISTRIBUTION_TO_COUNTERPARTY
- COUNTERPARTY_TRAPPED
- UNKNOWN

七、failure_attribution

新增钱包结构相关 failure_type：
- WALLET_EXIT
- SAME_SOURCE_EXIT
- DISTRIBUTION_ACTIVE
- COUNTERPARTY_ABSORBING
- STRUCTURE_WEAKENING
- HIGH_RESULT_EXIT
- BAGHOLDER_PRESSURE
- DATA_QUALITY_FAIL
- WALLET_GATE_MISSED
- WALLET_FALSE_SUPPORT

归因规则：
- early_wallet_sold_pct_delta >=20 且 position_pnl_pct <0 → WALLET_EXIT
- same_source_group_sold_pct_delta >=20 或 sync_sell_score >=70 → SAME_SOURCE_EXIT
- distribution_wallet_count_delta >=2 且 price_change_pct >=0 → DISTRIBUTION_ACTIVE
- counterparty_pressure_score_delta >=25 且 late_large_buyer_count_delta >=2 → COUNTERPARTY_ABSORBING
- wallet_structure_score_delta <=-20 或 wallet_risk_score_delta >=20 → STRUCTURE_WEAKENING
- high_result_remaining_pct_delta <=-20 → HIGH_RESULT_EXIT
- bagholder_whale_count_delta >=2 且 price_change_pct <=0 → BAGHOLDER_PRESSURE
- data_quality_score_at_entry <50 且交易失败 → DATA_QUALITY_FAIL
- entry 时 counterparty_pressure_score >=50 或 wallet_risk_score >=50 或 sync_sell_score >=60 或 data_quality_score <50，但仍进入 PAPER_READY → WALLET_GATE_MISSED
- entry 时 WALLET_SUPPORT，但交易亏损且 wallet_risk_score_delta >=20 → WALLET_FALSE_SUPPORT
```

---

# 本次认知升级点

这一步把 SIKK 的钱包结构层从“静态钱包分类”升级成了：

```text
同源组识别
+ 同步买卖评分
+ 对手盘压力识别
+ 多轮快照 delta
+ 钱包结构失败归因
```

真正的核心不是单次判断某个钱包，而是持续追踪：

```text
结构侧是否撤退
执行组是否同步卖出
高结果钱包是否离场
对手盘是否正在承接
入场后钱包结构是否恶化
```

---

# 尚未解决问题

下一步可以继续定稿：

```text
1. sikk_wallet_structure_gate.py 的完整代码骨架
2. tests/test_sikk_wallet_structure_gate.py 测试样例
3. sikk_candidate_wallet_structure_pipeline.py 的输入输出流程
4. wallet_structure_decision.json 与状态机的实际接入点
5. paper runner 如何根据钱包结构变化触发持仓管理或提前退出
```


---

## 片段 50 / stream_idx=7593 / len=15002


# SIKK-SOL 系统认知已重建

当前系统不再按“找庄家钱包脚本”理解，而应重建为：

> **SIKK-SOL 筹码控制权状态机**  
> 用钱包结构、筹码迁移、K线状态、报价安全、流动性成本、失败归因，持续判断一个 token 是否允许进入纸面交易验证。

核心变化：

```text
旧理解：识别哪个钱包是庄家
新理解：判断筹码控制权是否仍在结构侧，是否正在向对手盘转移
```

---

# 一、系统总定义

## SIKK-SOL v1.0 定位

```text
SIKK-SOL = 结构钱包行为识别 + 筹码迁移判断 + K线结构确认 + quote 安全验证 + 纸面交易复盘系统
```

它不是单纯的：

```text
量价策略
钱包跟单器
庄家识别器
自动实盘机器人
```

而是：

```text
结构智能交易验证系统
```

当前阶段：

```text
Phase A → Phase B 准备阶段
```

即：

```text
paper only → paper + human confirmation ticket
```

仍然禁止自动实盘。

---

# 二、核心认知重建

## 1. 不直接判断“庄家”

链上不能直接证明某个地址就是庄家。  
所以系统中不使用绝对裁决词：

```text
庄家
老鼠仓
内幕盘
绝对控盘
```

改用证据化语言：

```text
疑似结构侧钱包
疑似执行侧钱包
疑似同源执行组
疑似分发侧钱包
疑似对手盘承接钱包
疑似筹码转移
疑似结构侧减弱
```

---

## 2. 系统真正判断的是“筹码控制权”

核心问题不是：

```text
谁是庄？
```

而是：

```text
筹码现在在哪一侧？
早期优势钱包是否仍持有？
同源组是否同步撤退？
高结果钱包是否退出？
晚期钱包是否正在接货？
价格上涨是推进，还是出货？
当前入场是否会成为退出流动性？
```

---

## 3. 钱包结构是门禁，不是买入信号

正确逻辑：

```text
钱包结构支持
+ K线结构支持
+ quote 可靠
+ 安全扫描通过
+ 流动性可执行
+ 状态未过期
= 允许 PAPER_READY
```

错误逻辑：

```text
钱包结构好 → 直接买入
```

---

# 三、系统总架构：7 层

## 第 1 层：数据层

解决问题：

```text
数据从哪里来，字段是否完整，格式是否统一。
```

输入数据：

```text
GMGN 候选池
GMGN holder 数据
GMGN top trader
GMGN early buyer
GMGN wallet pnl
K线 1m / 5m
OKX quote
GMGN quote
GMGN pool price
安全扫描
流动性数据
```

输出：

```text
标准化 token 数据
标准化 wallet 数据
标准化 quote 数据
标准化 K线数据
```

---

## 第 2 层：钱包实体层

解决问题：

```text
单个地址是什么类型的钱包。
```

核心输出：

```text
wallet_classification.csv
```

核心字段：

```text
wallet_address
wallet_role
game_side
role_confidence
entry_rank
entry_time
sold_pct
remaining_pct
roi_pct
pnl_usd
same_source_group_id
risk_level
evidence_level
reason
```

---

## 第 3 层：当前 token 事件层

解决问题：

```text
这个钱包在当前 token 里做了什么。
```

判断内容：

```text
谁早入
谁清仓
谁部分持有
谁高收益
谁同步卖出
谁接盘
谁被套
谁可能是噪音
```

---

## 第 4 层：筹码迁移层

解决问题：

```text
筹码正在从哪一侧转移到哪一侧。
```

核心判断：

```text
结构侧是否增强
结构侧是否维持
结构侧是否减弱
派发是否活跃
对手盘是否正在承接
```

新增状态：

```text
STRUCTURE_STRENGTHENING   结构侧增强
STRUCTURE_HOLDING         结构侧维持
STRUCTURE_WEAKENING       结构侧减弱
DISTRIBUTION_ACTIVE       派发进行中
COUNTERPARTY_ABSORBING    对手盘承接中
UNKNOWN                   不明确
```

---

## 第 5 层：钱包结构门禁层

解决问题：

```text
钱包结构是否允许进入 PAPER_READY。
```

核心输出：

```text
wallet_structure_decision.json
```

核心分数：

```text
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
wallet_structure_factor
```

核心状态：

```text
WALLET_BLOCK
WALLET_PAUSE
WALLET_SUPPORT
WALLET_NEUTRAL
```

---

## 第 6 层：交易状态机层

解决问题：

```text
当前 token 应该处于什么交易状态。
```

状态流：

```text
WATCHING
  ↓
PAPER_READY
  ↓
READY_FOR_CONFIRMATION
  ↓
PAPER_OPEN
  ↓
PAPER_MANAGING
  ↓
PAPER_CLOSED
```

异常流：

```text
WALLET_BLOCK → BLOCKED
WALLET_PAUSE → PAUSE / WATCHING
QUOTE_FAIL → PAUSE_NEED_CONFIRM
SECURITY_FAIL → BLOCKED
STATE_EXPIRED → EXPIRED
```

---

## 第 7 层：复盘进化层

解决问题：

```text
系统判断是否真的有效。
```

复盘对象：

```text
10 个 token：字段完整性
30 个 token：阈值合理性
100 个 token：胜率、回撤、失败归因
```

输出：

```text
review_batch_001.csv
daily_report.md
failure_attribution.csv
threshold_adjustment_suggestions.md
```

---

# 四、v1.0 核心模块重建

## 模块 1：候选发现模块

职责：

```text
从 GMGN 新币池 / 热门池中发现候选 token。
```

输出：

```text
candidates.json
candidates.csv
```

字段：

```text
token_address
token_symbol
market_cap
liquidity
holder_count
pool_address
open_time
discovered_at
source
risk_tags
```

---

## 模块 2：K线结构模块

职责：

```text
判断价格是否出现可交易结构。
```

核心识别：

```text
吸筹窗口
控盘箱体
突破
回踩
二次推进
高低点结构
假突破
失效位
```

输出：

```text
sikk_signal_level
control_box_high
control_box_low
breakout_status
pullback_status
invalid_level
```

---

## 模块 3：钱包结构模块

职责：

```text
识别钱包角色、博弈侧、筹码迁移状态。
```

核心文件：

```text
sikk_wallet_structure_gate.py
sikk_candidate_wallet_structure_pipeline.py
```

输出目录：

```text
data/gmgn_candidates_live_run/wallet_structure/
```

每个 token 输出：

```text
early_wallet_raw.csv
wallet_classification.csv
candidate_groups.csv
gmgn_note_table.csv
wallet_structure_decision.json
```

---

## 模块 4：对手盘压力模块

职责：

```text
判断主导侧是否正在把筹码转移给对手盘。
```

新增分数：

```text
counterparty_pressure_score
```

核心观察：

```text
早期钱包卖出增加
晚期大额钱包买入增加
套牢鲸鱼增加
持有人数上涨但价格推进弱
价格上涨但 Top Holder 下降
高结果钱包退出
```

---

## 模块 5：quote 一致性模块

职责：

```text
判断纸面入场价是否真实可靠。
```

比较：

```text
OKX quote
GMGN quote
GMGN pool price
Kline close price
paper runner price
```

规则：

```text
偏差 <= 2%      → ALLOW
偏差 2% - 5%    → PAUSE_NEED_CONFIRM
偏差 > 5%       → BLOCK_QUOTE_UNRELIABLE
```

---

## 模块 6：安全扫描模块

职责：

```text
排除不可交易风险。
```

检查：

```text
honeypot
高税
黑名单
mint 风险
暂停交易风险
LP 风险
池子过浅
异常权限
```

原则：

```text
钱包结构支持不能绕过安全门禁。
```

---

## 模块 7：纸面交易 runner

职责：

```text
用实时 quote 和交易成本模拟真实入场。
```

新增字段：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
wallet_structure_factor
wallet_structure_reason
wallet_evidence_level
```

入场价模式：

```text
--entry-price-mode signal
--entry-price-mode live
```

默认：

```text
live
```

---

## 模块 8：失败归因模块

职责：

```text
每笔失败都要知道失败原因。
```

失败类型：

```text
STRUCTURE_FAIL
LIQUIDITY_FAIL
QUOTE_FAIL
SECURITY_FAIL
MOMENTUM_FAIL
WALLET_EXIT
COUNTERPARTY_ABSORBING
DISTRIBUTION_ACTIVE
STOP_LOSS
TIME_STOP
STATE_EXPIRED
EXECUTION_FAIL
```

---

## 模块 9：Replay 回放模块

职责：

```text
验证规则是否在实时条件下有效，而不是事后看起来合理。
```

回放内容：

```text
过去 24h 候选
当时 K线
当时 quote
当时钱包状态
当时门禁判断
模拟入场
模拟止损
模拟止盈
失败归因
```

---

## 模块 10：历史地址库

职责：

```text
从单币判断升级到跨币复现。
```

长期字段：

```text
address
repeat_appearance_count
historical_role
historical_roi_profile
historical_exit_behavior
cross_token_group_similarity
old_money_confidence
last_seen_token
last_seen_time
```

v1.0 暂不作为主门禁，v2.0 接入。

---

# 五、钱包角色体系重建

## v1.0 先保留 8 类

```text
EARLY_BUYER              早期买入钱包
EARLY_EXIT               早期清仓钱包
PARTIAL_HOLDER           部分持有钱包
HIGH_RESULT_WALLET       高结果钱包
SAME_SOURCE_GROUP        疑似同源组钱包
DISTRIBUTION_SELLER      疑似分发/派发钱包
BAGHOLDER_WHALE          套牢鲸鱼
RETAIL_NOISE             普通噪音钱包
```

---

## 新增博弈侧字段：game_side

```text
STRUCTURE_SIDE        疑似结构侧
EXECUTION_SIDE        疑似执行侧
DISTRIBUTION_SIDE     疑似派发侧
COUNTERPARTY_SIDE     疑似对手盘侧
NOISE_SIDE            噪音侧
UNKNOWN_SIDE          未知
```

映射：

| 钱包角色 | 博弈侧 |
|---|---|
| EARLY_BUYER | STRUCTURE_SIDE / UNKNOWN_SIDE |
| EARLY_EXIT | DISTRIBUTION_SIDE |
| PARTIAL_HOLDER | STRUCTURE_SIDE / DISTRIBUTION_SIDE |
| HIGH_RESULT_WALLET | EXECUTION_SIDE |
| SAME_SOURCE_GROUP | EXECUTION_SIDE |
| DISTRIBUTION_SELLER | DISTRIBUTION_SIDE |
| BAGHOLDER_WHALE | COUNTERPARTY_SIDE |
| RETAIL_NOISE | NOISE_SIDE |

---

# 六、核心分数体系重建

## 1. wallet_structure_score：结构支持分

回答：

```text
钱包结构是否支持继续观察 / PAPER_READY？
```

满分 100：

```text
早期钱包仍持有              25
高结果钱包仍持有            20
同源组没有同步卖出          15
分发风险低                  15
持仓结构稳定                10
Top Trader 未反向           10
钱包行为与价格不冲突         5
```

解释：

```text
0-39   结构不支持
40-64  中性 / 观察
65-79  结构支持
80-100 强结构支持，但不直接买入
```

---

## 2. wallet_risk_score：钱包风险分

回答：

```text
是否存在清仓、同步卖出、派发、撤退风险？
```

满分 100：

```text
早期钱包集中清仓            30
同源组同步卖出              25
分发钱包增加                15
高结果钱包退出              10
Top Holder 出货             10
套牢鲸鱼压力                 5
数据不足                     5
```

解释：

```text
0-39   风险可接受
40-59  中风险
60-74  高风险
75-100 极高风险，WALLET_BLOCK
```

---

## 3. counterparty_pressure_score：对手盘压力分

回答：

```text
主导侧是否正在把筹码转移给对手盘？
```

满分 100：

```text
早期钱包卖出给晚期买盘        25
晚期大额钱包增加              20
套牢鲸鱼增加                  15
价格上涨但结构钱包卖出        20
持有人数增加但 Top Holder 下降 10
高结果钱包退出                10
```

解释：

```text
0-29   暂无明显对手盘压力
30-49  观察
50-69  中等对手盘压力
70-100 高对手盘压力
```

---

## 4. data_quality_score：数据质量分

回答：

```text
这次钱包结构判断的数据够不够用？
```

满分 100：

```text
早期钱包数据完整度            25
持仓 / 买卖字段完整度          20
时间字段完整度                15
ROI / PnL 字段完整度           15
资金来源 / 同源字段完整度      15
Top Holder / Top Trader 完整度 10
```

解释：

```text
80-100 数据较完整
60-79  可用但需保守
50-59  勉强可用
<50    数据不足，WALLET_PAUSE
```

---

# 七、门禁状态重建

## WALLET_SUPPORT

含义：

```text
结构侧仍未完全退出，对手盘压力不高，钱包行为与价格没有明显冲突。
```

触发条件：

```text
wallet_structure_score >= 65
wallet_risk_score <= 40
counterparty_pressure_score <= 40
data_quality_score >= 60
early_wallet_remaining_pct >= 30
same_source_sync_sell_score < 50
distribution_wallet_count <= 1
```

动作：

```text
允许进入 PAPER_READY，但不能绕过 quote/security/K线门禁。
```

---

## WALLET_NEUTRAL

含义：

```text
没有明显结构支持，也没有明显阻断。
```

动作：

```text
继续走其他门禁，不加分、不阻断。
```

---

## WALLET_PAUSE

含义：

```text
可能发生筹码转移、数据不足、或风险偏高，需要继续观察。
```

触发条件：

```text
data_quality_score < 50
wallet_risk_score >= 50
counterparty_pressure_score >= 50
top_holder_exit_pressure == HIGH
```

动作：

```text
进入 PAUSE / WATCHING。
```

---

## WALLET_BLOCK

含义：

```text
结构侧大概率撤退，继续入场可能成为退出流动性。
```

触发条件：

```text
wallet_risk_score >= 75
counterparty_pressure_score >= 70 且 wallet_risk_score >= 50
same_source_sync_sell_score >= 70
early_wallet_sold_pct >= 85 且 high_result_remaining_pct <= 10
distribution_wallet_count >= 3 且 early_wallet_remaining_pct <= 20
```

动作：

```text
BLOCKED
```

---

# 八、状态机接入重建

状态机读取：

```text
data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json
```

逻辑：

```python
if wallet_structure_status == "WALLET_BLOCK":
    state = "BLOCKED"

elif wallet_structure_status == "WALLET_PAUSE":
    state = "PAUSE"

elif wallet_structure_status == "WALLET_SUPPORT":
    if signal_gate == "ALLOW" and quote_gate == "ALLOW" and security_gate == "ALLOW":
        state = "PAPER_READY"
    else:
        state = "WATCHING"

elif wallet_structure_status == "WALLET_NEUTRAL":
    continue_with_existing_gates()
```

---

# 九、输出文件体系重建

## 总目录

```text
data/gmgn_candidates_live_run/
```

## 钱包结构目录

```text
data/gmgn_candidates_live_run/wallet_structure/
```

## 汇总文件

```text
candidate_wallet_structure_summary.json
candidate_wallet_structure_summary.csv
candidate_wallet_structure_summary.md
```

## 单 token 文件

```text
<token_address>/
  early_wallet_raw.csv
  wallet_classification.csv
  candidate_groups.csv
  gmgn_note_table.csv
  wallet_structure_decision.json
```

## 复盘文件

```text
review_batch_001.csv
review_batch_001.md
daily_report.md
failure_attribution.csv
```

---

# 十、wallet_structure_decision.json 标准

```json
{
  "token_address": "TOKEN_ADDRESS",
  "token_symbol": "TOKEN",
  "wallet_structure_status": "WALLET_SUPPORT",
  "wallet_structure_score": 72,
  "wallet_risk_score": 28,
  "counterparty_pressure_score": 32,
  "data_quality_score": 76,
  "wallet_structure_factor": 1.15,
  "wallet_evidence_level": "E2",
  "decision_action": "ALLOW_PAPER_READY",
  "dominant_side_status": "STRUCTURE_HOLDING",
  "chip_transfer_status": "NO_MAJOR_TRANSFER",
  "reason": "早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未同步卖出，对手盘压力不高",
  "support_signals": [
    "EARLY_WALLETS_PARTIAL_HOLDING",
    "HIGH_RESULT_WALLETS_STILL_HOLDING",
    "LOW_DISTRIBUTION_RISK"
  ],
  "risk_signals": [
    "TOP_TRADER_NEUTRAL"
  ],
  "game_side_summary": {
    "structure_side_wallet_count": 8,
    "execution_side_wallet_count": 5,
    "distribution_side_wallet_count": 1,
    "counterparty_side_wallet_count": 2,
    "noise_side_wallet_count": 34
  },
  "metrics": {
    "early_wallet_count": 42,
    "early_wallet_remaining_pct": 38.5,
    "early_wallet_sold_pct": 61.5,
    "high_result_wallet_count": 3,
    "high_result_remaining_pct": 31.2,
    "same_source_group_count": 1,
    "same_source_sync_sell_score": 22,
    "distribution_wallet_count": 1,
    "bagholder_whale_count": 0,
    "top_holder_exit_pressure": "LOW",
    "top_trader_buy_sell_bias": "NEUTRAL"
  },
  "created_at": "2026-05-02T00:00:00Z"
}
```

---

# 十一、开发优先级重建

当前不要先做完整历史库，也不要先做自动实盘。

## 第一优先级

```text
1. sikk_wallet_structure_gate.py
2. classify(w) v1.0
3. wallet_structure_score
4. wallet_risk_score
5. data_quality_score
6. counterparty_pressure_score
```

---

## 第二优先级

```text
7. sikk_candidate_wallet_structure_pipeline.py
8. wallet_structure_decision.json
9. 状态机读取 wallet_structure_decision.json
10. paper runner 写入 wallet_structure_factor
```

---

## 第三优先级

```text
11. 10 个 token 复盘模板
12. 多轮快照 delta
13. failure_attribution 接入钱包结构原因
14. replay 模式
```

---

## 第四优先级

```text
15. 历史地址库
16. 跨币复现
17. 老庄画像
18. confirmation ticket
19. 小仓实盘门禁
```

---

# 十二、下一步最小可执行版本

你现在最应该让 AI / Codex / OpenClaw 做的是：

```text
实现 SIKK-SOL v1.0 钱包结构门禁层。
```

最小可执行文件：

```text
sikk_wallet_structure_gate.py
sikk_candidate_wallet_structure_pipeline.py
tests/test_sikk_wallet_structure_gate.py
tests/test_sikk_candidate_wallet_structure_pipeline.py
```

最小输出：

```text
wallet_structure_decision.json
candidate_wallet_structure_summary.csv
```

最小接入：

```text
状态机读取 WALLET_BLOCK / WALLET_PAUSE / WALLET_SUPPORT / WALLET_NEUTRAL
paper runner 写入 wallet_structure_factor
```

---

# 十三、可以直接复制给 AI 的总指令

```text
你现在负责重建 SIKK-SOL v1.0 钱包结构门禁层。

系统目标不是直接识别“庄家钱包”，而是构建一个筹码控制权状态机，用钱包结构、筹码迁移、K线结构、quote 安全、流动性成本、失败归因来判断一个 token 是否允许进入 PAPER_READY。

核心原则：
1. 不直接使用“庄家”作为结论，只使用证据化表达。
2. 钱包结构是门禁，不是独立买入信号。
3. 系统要判断筹码控制权是否仍在结构侧，是否正在向对手盘转移。
4. WALLET_SUPPORT 不能绕过 K线、quote、安全扫描。
5. 当前阶段禁止自动实盘，只允许 paper trading 和 future confirmation ticket。

请实现以下文件：
1. sikk_wallet_structure_gate.py
2. sikk_candidate_wallet_structure_pipeline.py
3. tests/test_sikk_wallet_structure_gate.py
4. tests/test_sikk_candidate_wallet_structure_pipeline.py

钱包角色 v1.0：
- EARLY_BUYER
- EARLY_EXIT
- PARTIAL_HOLDER
- HIGH_RESULT_WALLET
- SAME_SOURCE_GROUP
- DISTRIBUTION_SELLER
- BAGHOLDER_WHALE
- RETAIL_NOISE

新增 game_side：
- STRUCTURE_SIDE
- EXECUTION_SIDE
- DISTRIBUTION_SIDE
- COUNTERPARTY_SIDE
- NOISE_SIDE
- UNKNOWN_SIDE

核心分数：
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score

核心状态：
- WALLET_BLOCK
- WALLET_PAUSE
- WALLET_SUPPORT
- WALLET_NEUTRAL

状态机接入：
- WALLET_BLOCK → BLOCKED
- WALLET_PAUSE → PAUSE / WATCHING
- WALLET_SUPPORT → 只有 signal_gate、quote_gate、security_gate 都通过，才允许 PAPER_READY
- WALLET_NEUTRAL → 不加分、不阻断，继续走其他门禁

输出文件：
data/gmgn_candidates_live_run/wallet_structure/
  candidate_wallet_structure_summary.json
  candidate_wallet_structure_summary.csv
  candidate_wallet_structure_summary.md

每个 token 子目录：
  early_wallet_raw.csv
  wallet_classification.csv
  candidate_groups.csv
  gmgn_note_table.csv
  wallet_structure_decision.json

paper runner 新增字段：
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- wallet_structure_factor
- wallet_structure_reason
- wallet_evidence_level

测试要求：
1. 早期钱包集中清仓 → WALLET_BLOCK
2. 同源组同步卖出 → WALLET_BLOCK
3. 对手盘压力高 → WALLET_BLOCK 或 WALLET_PAUSE
4. 数据不足 → WALLET_PAUSE
5. 早期钱包仍持有、高结果钱包未退出、风险低 → WALLET_SUPPORT
6. 无明显结构证据 → WALLET_NEUTRAL
```

---

# 十四、最终重建结论

SIKK-SOL 现在应该被定义为：

```text
筹码控制权状态机
```

而不是：

```text
庄家钱包识别脚本
```

它的核心能力是：

```text
1. 识别早期优势钱包是否仍在
2. 判断同源执行组是否撤退
3. 判断高结果钱包是否退出
4. 判断筹码是否向晚期对手盘转移
5. 判断价格上涨是推进还是派发
6. 判断当前入场是否会成为别人退出流动性
7. 把这些判断转成 WALLET_BLOCK / WALLET_PAUSE / WALLET_SUPPORT
8. 接入状态机和纸面交易验证
```

---

# 本次认知升级点

本次系统重建的核心升级是：

> **从“找庄家”升级为“判断筹码控制权状态”。**

新的 SIKK-SOL 不再围绕单个钱包身份做绝对判断，而是围绕：

```text
结构侧
执行侧
派发侧
对手盘侧
噪音侧
```

持续判断：

```text
谁在控制筹码
谁在退出
谁在接货
谁在提供流动性
当前结构是否仍值得进入 PAPER_READY
```

---

# 尚未解决问题

下一步需要继续定稿 5 个具体工程问题：

```text
1. same_source_group_id 如何生成
2. sync_buy_score / sync_sell_score 如何计算
3. counterparty_pressure_score 的精确字段来源
4. 多轮快照 delta 如何设计
5. 钱包结构失败如何进入 failure_attribution
```


---

## 片段 51 / stream_idx=7689 / len=9389


从整体大局看，你的脚本不要理解成“找庄家脚本”，而应该理解成：

> **把链上钱包行为、筹码迁移、价格结构、报价安全、历史复现，统一转成一个可执行的结构状态判断系统。**

也就是说，脚本的核心不是直接判断：

```text
这个钱包是不是庄家？
```

而是连续回答：

```text
筹码现在在谁手里？
早期优势钱包有没有退出？
疑似执行组是否还在维护结构？
筹码是不是正在转移给对手盘？
现在入场是不是在接别人出货？
这个 token 是否允许进入 PAPER_READY？
```

---

# 一、脚本对“庄家筹码实时分析”应该怎么理解？

## 1. 不是实时识别庄家，而是实时识别筹码状态

链上不能直接证明某个地址就是庄家。  
所以系统应该避免使用绝对判断：

```text
庄家钱包
庄家正在出货
庄家正在控盘
```

应该改成证据化表达：

```text
疑似结构侧钱包
疑似执行组钱包
疑似早期优势钱包
疑似分发钱包
疑似对手盘承接钱包
疑似筹码向晚期钱包转移
```

你的脚本真正要做的是：

```text
连续追踪筹码控制权是否增强、维持、减弱、转移、崩塌。
```

---

## 2. “实时”本质是多轮快照对比

GMGN / K线 / quote / holder 数据不是一次看完就结束。  
真正有价值的是：

```text
第 1 次快照：早期钱包还持有多少
第 2 次快照：早期钱包是否开始卖
第 3 次快照：同源组是否同步卖
第 4 次快照：晚期大额钱包是否接货
第 5 次快照：价格是否还能继续推进
```

所以脚本要从“单次报告”升级为：

```text
多轮快照 → 差值变化 → 结构状态迁移
```

也就是：

```text
Snapshot A
  ↓
Snapshot B
  ↓
Delta 变化
  ↓
结构状态判断
  ↓
状态机动作
```

---

## 3. 单次数据看身份，多次数据看意图

单次钱包数据只能判断：

```text
这个钱包早入
这个钱包卖出多
这个钱包 ROI 高
这个钱包持仓大
```

但连续数据才能判断：

```text
它是不是在撤退
它是不是在维护结构
它是不是边拉边卖
它是不是接盘后被套
它是不是同源组同步操作
```

所以你的系统应该明确分成两类判断：

| 判断类型 | 数据基础 | 作用 |
|---|---|---|
| 静态身份判断 | 单次快照 | 钱包角色分类 |
| 动态行为判断 | 多轮快照 | 筹码迁移、分发、撤退、承接 |

---

# 二、钱包数据分析在系统里的位置

钱包分析不是单独存在的模块。  
它应该是整个 SIKK 系统的核心中层。

完整结构应该是：

```text
候选发现
  ↓
K线结构信号
  ↓
钱包结构分析
  ↓
筹码迁移判断
  ↓
quote / 安全扫描
  ↓
状态机
  ↓
纸面交易 / confirmation ticket
  ↓
复盘校准
```

其中钱包结构层负责回答：

```text
这个 token 的“人”是否还支持继续走？
```

K线层负责回答：

```text
这个 token 的“价格结构”是否出现可交易形态？
```

quote 层负责回答：

```text
这个 token 现在是否能按合理价格成交？
```

安全层负责回答：

```text
这个 token 是否存在交易风险、合约风险、池子风险？
```

状态机负责回答：

```text
现在应该 WATCHING、PAUSE、BLOCKED，还是 PAPER_READY？
```

---

# 三、脚本应该围绕 5 个核心问题运行

## 问题 1：谁先拿到了筹码？

对应字段：

```text
entry_rank
entry_time
buy_amount_usd
is_new_wallet
funding_source
same_source_group_id
```

目的：

```text
识别早期优势钱包、疑似执行钱包、疑似同源组。
```

如果多个钱包在极短时间内进入，并且资金来源相似、买入行为相似，就不是普通散户行为。

---

## 问题 2：早期筹码还在不在？

对应字段：

```text
early_wallet_remaining_pct
early_wallet_sold_pct
high_result_remaining_pct
same_source_group_remaining_pct
```

目的：

```text
判断结构侧是否仍有继续维护价格的动机。
```

如果早期优势钱包大部分已经清仓，那么价格再涨也可能只是晚期对手盘在追。

---

## 问题 3：筹码有没有转移给对手盘？

对应字段：

```text
late_buyer_ratio
bagholder_whale_count
new_holder_growth
top_holder_exit_pressure
counterparty_pressure_score
```

目的：

```text
判断自己入场后是否会成为别人的退出流动性。
```

典型危险结构：

```text
早期钱包卖出增加
晚期钱包买入增加
持有人数上涨
价格推进变弱
成交量放大但结构钱包退出
```

这就是对手盘承接压力。

---

## 问题 4：拉升是推进还是派发？

对应字段：

```text
price_change_pct
volume_change
early_wallet_sold_pct_delta
same_source_sync_sell_score
distribution_wallet_count
top_holder_pct_delta
```

判断逻辑：

```text
价格涨 + 结构钱包继续持有 = 推进可能性增加
价格涨 + 结构钱包同步卖出 = 边拉边卖风险增加
价格涨 + Top Holder 下降 = 派发风险增加
价格涨 + 晚期接盘增加 = 对手盘压力增加
```

---

## 问题 5：结构状态正在增强还是衰减？

最终输出应该不是一句话，而是状态：

```text
STRUCTURE_STRENGTHENING   结构增强
STRUCTURE_HOLDING         结构维持
STRUCTURE_WEAKENING       结构衰减
DISTRIBUTION_ACTIVE       派发进行中
COUNTERPARTY_ABSORBING    对手盘承接中
UNKNOWN                   不明确
```

这比简单说“好 / 坏”更适合自动交易系统。

---

# 四、脚本应该输出的不是报告，而是决策材料

你的钱包分析脚本最终应该生成 4 类东西。

## 1. 钱包分类表

```text
wallet_classification.csv
```

回答：

```text
每个钱包是谁？
它属于哪一类？
它站在哪个博弈侧？
证据等级是多少？
```

核心字段：

```text
wallet_address
wallet_role
game_side
role_confidence
remaining_pct
sold_pct
roi_pct
pnl_usd
same_source_group_id
evidence_level
risk_level
reason
```

---

## 2. 筹码迁移摘要

```text
wallet_structure_decision.json
```

回答：

```text
整个 token 的结构状态是什么？
是否支持 PAPER_READY？
是否应该 PAUSE / BLOCK？
```

核心字段：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
dominant_side_status
chip_transfer_status
decision_action
reason
```

---

## 3. GMGN 备注表

```text
gmgn_note_table.csv
```

回答：

```text
哪些钱包值得放进 GMGN 监控？
应该怎么备注？
```

格式继续用证据化表达：

```text
$TOKEN@D1｜早入｜重仓+低频｜高ROI+部分退｜CL_xxx｜E2
```

---

## 4. 纸面交易因子

写入 paper runner：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
wallet_structure_factor
wallet_structure_reason
```

这一步的意义是：

```text
让钱包结构真正影响 PAPER_READY，而不是只生成分析报告。
```

---

# 五、整体系统里还需要哪些辅助部分？

钱包结构很重要，但它不能独立决定交易。  
它必须和下面这些模块配合。

---

## 1. K线结构模块

作用：

```text
判断价格是否出现可交易结构。
```

主要看：

```text
吸筹窗口
控盘箱体
突破
回踩
二次推进
高低点结构
成交量扩张
假突破
失效位
```

钱包结构告诉你：

```text
谁在持有、谁在卖、谁在接。
```

K线结构告诉你：

```text
这些行为有没有反映到价格推进上。
```

两者必须结合。

典型判断：

```text
钱包结构支持 + K线突破回踩成功 = PAPER_READY 概率提高
钱包结构支持 + K线跌破箱体 = 不入场
钱包结构风险高 + K线拉升 = 警惕边拉边卖
```

---

## 2. 成交量 / 成交效率模块

作用：

```text
判断拉升质量。
```

不能只看价格涨，要看：

```text
上涨是否需要越来越大的成交量
放量后价格是否能保持
OBV 是否跟随
买盘是否有效推动
成交量是否只是在给出货提供流动性
```

辅助判断：

```text
价格上涨 + 成交效率下降 + 结构钱包卖出 = 派发嫌疑增加
价格上涨 + 成交效率上升 + 结构钱包持有 = 推进质量较好
```

---

## 3. quote / 多报价源一致性模块

作用：

```text
判断纸面入场价是否可靠。
```

必须比较：

```text
OKX quote
GMGN quote
GMGN pool price
K线 close price
paper runner price
```

如果价格偏差大：

```text
PAUSE_NEED_CONFIRM
```

否则纸面收益会失真。

钱包结构再好，如果 quote 不可靠，也不能进入真实交易路径。

---

## 4. 安全扫描模块

作用：

```text
排除交易不可执行或高风险 token。
```

检查：

```text
是否 honeypot
是否高税
是否可暂停交易
是否池子过浅
是否 LP 风险
是否 mint 权限异常
是否黑名单风险
```

状态机原则：

```text
wallet_structure_support 不能绕过 security_gate
```

也就是说：

```text
钱包结构支持 ≠ 可以交易
```

---

## 5. 流动性 / 滑点模块

作用：

```text
判断你能不能以合理成本进出。
```

meme token 最大的问题之一是：

```text
看起来涨了，但你真实成交吃不到。
```

所以必须有：

```text
buy_slippage_pct
sell_slippage_pct
dex_fee_pct
priority_fee_sol
failed_tx_cost_sol
quote_deviation_buffer_pct
```

否则纸面交易会高估收益。

---

## 6. 历史地址库

这是你系统的长期核心。

单币分析只能告诉你：

```text
这个地址在当前 token 做了什么。
```

历史地址库能告诉你：

```text
这个地址以前有没有出现过？
它以前是早期执行者还是接盘者？
它是否多次参与高结果 token？
它是否多次清仓后 token 崩？
它是否属于某个反复出现的结构组？
```

后续可以增加：

```text
address_history_score
repeat_appearance_count
historical_roi_profile
historical_exit_behavior
cross_token_group_similarity
old_money_confidence
```

这是从 v1.0 进入 v2.0 的关键。

---

## 7. Replay / 回放模块

作用：

```text
验证规则是不是事后看起来合理，还是实时也能成立。
```

你需要回放：

```text
过去 24h 的候选
当时的钱包状态
当时的 K线状态
当时的 quote
当时的风险扫描
当时是否应该 PAPER_READY
```

如果只看结果，容易产生幸存者偏差。  
Replay 是防止系统自欺的关键模块。

---

## 8. 失败归因模块

每笔失败都要归因：

```text
STRUCTURE_FAIL
LIQUIDITY_FAIL
QUOTE_FAIL
SECURITY_FAIL
MOMENTUM_FAIL
WALLET_EXIT
COUNTERPARTY_ABSORBING
DISTRIBUTION_ACTIVE
STOP_LOSS
TIME_STOP
```

否则你只能看到亏了，但不知道为什么亏。

长期优化不是靠感觉，而是靠：

```text
失败原因 Top 5
不同失败类型的亏损贡献
不同钱包状态下的胜率
不同结构状态下的最大回撤
```

---

# 六、系统最终应该形成 7 层理解

## 第 1 层：数据层

收集：

```text
GMGN 候选
holder 数据
top trader
early buyer
wallet pnl
K线
quote
security scan
liquidity
```

目标：

```text
保证字段完整、时间统一、格式统一。
```

---

## 第 2 层：钱包实体层

处理：

```text
钱包地址
资金来源
同源组
交易行为
持仓变化
角色分类
```

目标：

```text
把地址从“孤立地址”变成“有角色的钱包实体”。
```

---

## 第 3 层：当前 token 事件层

判断：

```text
谁早入
谁清仓
谁部分持有
谁高 ROI
谁同步卖
谁接盘
```

目标：

```text
看清当前 token 内部的筹码行为。
```

---

## 第 4 层：筹码迁移层

判断：

```text
筹码是否从早期钱包转给晚期钱包
结构侧是否减弱
对手盘是否增加
派发是否正在发生
```

目标：

```text
理解当前博弈方向。
```

---

## 第 5 层：门禁评分层

生成：

```text
wallet_structure_score
wallet_risk_score
counterparty_pressure_score
data_quality_score
wallet_structure_status
```

目标：

```text
把复杂钱包行为转成状态机可读取的决策信号。
```

---

## 第 6 层：交易状态机层

决策：

```text
BLOCKED
WATCHING
PAUSE
PAPER_READY
READY_FOR_CONFIRMATION
PAPER_OPEN
PAPER_CLOSED
```

目标：

```text
把分析结果接入交易流程。
```

---

## 第 7 层：复盘进化层

统计：

```text
10 个 token 字段完整性
30 个 token 阈值合理性
100 个 token 胜率 / 回撤 / 失败归因
```

目标：

```text
不断校准标准，而不是凭感觉改规则。
```

---

# 七、最重要的系统原则

## 原则 1：钱包结构是门禁，不是单独买入信号

不能因为钱包结构好就买。

正确逻辑：

```text
钱包结构支持
+ K线结构支持
+ quote 可靠
+ 安全扫描通过
+ 状态未过期
= 允许 PAPER_READY
```

---

## 原则 2：早期钱包退出比散户买入更重要

如果你看到：

```text
holder_count 增加
散户买入增加
价格上涨
```

但同时：

```text
early_wallet_sold_pct 上升
high_result_remaining_pct 下降
same_source_sync_sell_score 上升
```

这不是强势，可能是派发。

---

## 原则 3：同源组同步卖出是高优先级风险

同源组同步买入可能是结构支持。  
同源组同步卖出通常是结构撤退信号。

所以：

```text
same_source_sync_sell_score
```

应该是 v1.0 里面最重要的风险字段之一。

---

## 原则 4：接盘鲸鱼不一定是好事

很多时候“大钱包买入”不是利好，而是：

```text
被动承接
追涨接货
高位被套
给早期钱包退出
```

所以要看：

```text
它买入后价格是否继续推进
它买入时早期钱包是否卖出
它买入后是否迅速浮亏
```

---

## 原则 5：数据不足不能强行支持

如果：

```text
data_quality_score < 50
```

即使 K线好，也应该：

```text
WALLET_PAUSE
```

因为你不是没有风险，而是没有看清风险。

---

# 八、你当前最应该补齐的系统部分

按优先级：

```text
1. wallet_structure_decision.json 标准化
2. classify(w) v1.0 角色分类
3. wallet_structure_score / wallet_risk_score
4. counterparty_pressure_score
5. 状态机读取钱包结构门禁
6. paper runner 写入 wallet_structure_factor
7. 10 个 token 复盘模板
8. 多轮快照 delta 对比
9. 历史地址库
10. replay 模式
```

最先不要做太复杂的“庄家画像”。  
先把钱包结构变成可运行的门禁。

---

# 九、最终大局图

```text
GMGN 新币候选
  ↓
数据标准化
  ↓
K线结构分析
  ↓
钱包结构分析
  ├─ 早期钱包
  ├─ 高结果钱包
  ├─ 同源执行组
  ├─ 分发钱包
  ├─ 接盘鲸鱼
  └─ 普通噪音
  ↓
筹码迁移判断
  ├─ 结构侧增强
  ├─ 结构侧维持
  ├─ 结构侧减弱
  ├─ 派发进行中
  └─ 对手盘承接中
  ↓
门禁评分
  ├─ wallet_structure_score
  ├─ wallet_risk_score
  ├─ counterparty_pressure_score
  └─ data_quality_score
  ↓
状态机
  ├─ WALLET_BLOCK → BLOCKED
  ├─ WALLET_PAUSE → PAUSE / WATCHING
  ├─ WALLET_SUPPORT → 可进入 PAPER_READY
  └─ WALLET_NEUTRAL → 继续其他门禁
  ↓
quote / security / liquidity
  ↓
paper runner
  ↓
日报 + 失败归因 + replay
  ↓
阈值校准 + 历史地址库
```

---

# 十、简短结论

你的脚本体系应该这样理解：

> **钱包数据分析不是为了单次找出“庄家钱包”，而是为了持续判断筹码控制权是否还在结构侧、是否正在向对手盘转移、是否已经进入派发阶段。**

其他辅助模块的作用是：

```text
K线模块：验证价格结构是否配合
成交量模块：验证推进质量
quote 模块：验证入场价格是否真实
安全扫描：排除不可交易风险
流动性模块：修正真实成本
历史地址库：识别反复出现的结构钱包
replay 模块：验证规则是否实时有效
失败归因：告诉你系统错在哪里
```

最终你的 SIKK 系统不是普通交易机器人，而是：

```text
结构钱包行为识别
+ 筹码迁移判断
+ K线状态确认
+ quote 安全验证
+ 纸面交易复盘
= 结构智能交易系统
```

---

# 本次认知升级点

核心升级是：

> 你不是在做“庄家识别脚本”，而是在做“筹码控制权状态机”。

这个状态机要持续判断：

```text
结构侧是否还在
执行组是否撤退
筹码是否转移给对手盘
价格推进是否真实
当前入场是否会成为退出流动性
```

---

# 尚未解决问题

下一步最值得继续定稿：

```text
1. counterparty_pressure_score 完整公式
2. 多轮快照 delta 字段标准
3. dominant_side_status 状态迁移规则
4. 钱包结构与 K线结构如何共振
5. 钱包结构失败如何进入 failure_attribution
```


---

## 片段 52 / stream_idx=7877 / len=8286


可以。  
而且你这套 **SIKK 钱包结构门禁** 如果不加入“庄家—对手盘”视角，很多字段只会停留在表面。

但要注意一点：

> 系统里不要直接判断“谁是庄家”，而是用“主导方 / 执行方 / 承接方 / 退出方 / 被动对手盘”来表达。

这样既符合链上证据逻辑，也方便工程化。

---

# 一、正确理解方式

你可以把一个 token 里的钱包分成两套力量：

```text
主导侧：可能在组织筹码、推动价格、分发筹码的一方
对手盘侧：给主导侧提供流动性、承接筹码、追涨、被套的一方
```

SIKK 的核心不是问：

```text
谁是庄？
```

而是问：

```text
谁在主动设计局面？
谁在被动承接结果？
谁在拿走流动性？
谁在给别人退出？
谁还留有继续推动的动机？
```

这就是“庄家对手盘思维”的正确用法。

---

# 二、把钱包角色重新理解成“博弈位置”

原来的 8 类钱包可以这样升级理解：

| 钱包角色 | 表面含义 | 对手盘视角 |
|---|---|---|
| EARLY_BUYER 早期买入钱包 | 早期进入 | 可能是主导侧筹码，也可能是普通早鸟 |
| EARLY_EXIT 早期清仓钱包 | 早入后退出 | 主导侧已经完成兑现，或早鸟提前撤退 |
| PARTIAL_HOLDER 部分持有钱包 | 卖一部分留一部分 | 边兑现边保留二拉筹码 |
| HIGH_RESULT_WALLET 高结果钱包 | 高 ROI / 高利润 | 更接近有效执行者或早期优势钱包 |
| SAME_SOURCE_GROUP 疑似同源组 | 多钱包行为相似 | 可能是执行组，而不是自然散户 |
| DISTRIBUTION_SELLER 派发钱包 | 明显卖出 | 主导侧释放筹码，或大户退出 |
| BAGHOLDER_WHALE 套牢鲸鱼 | 高位重仓被套 | 被动对手盘，未来可能形成上方卖压 |
| RETAIL_NOISE 普通噪音 | 小额散户 | 流动性噪音，主要提供交易背景 |

---

# 三、最关键的判断不是“有没有庄”，而是 4 个问题

## 1. 主导侧是否还没完全退出？

看这些字段：

```text
early_wallet_remaining_pct
high_result_remaining_pct
same_source_group_remaining_pct
distribution_wallet_count
same_source_sync_sell_score
```

如果早期钱包、高结果钱包、同源组都还没完全退出，说明：

```text
主导侧可能仍有继续推动或维护结构的动机。
```

如果它们大部分已经退出，说明：

```text
价格再涨可能只是对手盘追涨，而不是主导侧继续控盘。
```

---

## 2. 对手盘是否正在接货？

看这些字段：

```text
bagholder_whale_count
new_retail_holder_growth
top_holder_exit_pressure
late_buyer_ratio
high_buy_amount_late_wallet_count
```

如果出现：

```text
早期钱包卖出
晚期大额钱包买入
持有人数上涨
价格不再有效推进
```

这通常不是好事，可能是：

```text
主导侧正在把筹码转移给对手盘。
```

---

## 3. 拉升是为了推进，还是为了出货？

看：

```text
价格上涨时 early_wallet_sold_pct 是否同步上升
same_source_sync_sell_score 是否上升
distribution_wallet_count 是否增加
Top Holder 是否下降
OBV / 成交效率是否背离
```

如果价格涨，但结构钱包同步卖出：

```text
这是边拉边卖，不是健康推进。
```

这种情况下，即使 K 线好看，也应该：

```text
WALLET_PAUSE 或 WALLET_BLOCK
```

---

## 4. 被套鲸鱼会不会成为未来压力？

`BAGHOLDER_WHALE` 不是简单利空，要分情况。

### 情况 A：被套鲸鱼在高位

```text
holding_pct 高
roi_pct 负
entry_price 高于当前价格
remaining_pct 高
```

含义：

```text
上方反弹时可能形成卖压。
```

### 情况 B：被套鲸鱼是早期大额承接

如果它不是高位追涨，而是在低位承接，且没有卖：

```text
可能是结构承接，不一定是风险。
```

所以 v1.0 先不要直接把 `BAGHOLDER_WHALE` 判死。  
应该进入：

```text
风险观察项
```

---

# 四、建议新增一个“博弈侧标签”

在 `wallet_classification.csv` 里新增字段：

```text
game_side
```

取值：

```text
STRUCTURE_SIDE        疑似结构侧
EXECUTION_SIDE        疑似执行侧
DISTRIBUTION_SIDE     疑似派发侧
COUNTERPARTY_SIDE     疑似对手盘侧
NOISE_SIDE            噪音侧
UNKNOWN_SIDE          未知
```

---

## 映射规则

| wallet_role | game_side |
|---|---|
| EARLY_BUYER | STRUCTURE_SIDE 或 UNKNOWN_SIDE |
| EARLY_EXIT | DISTRIBUTION_SIDE |
| PARTIAL_HOLDER | STRUCTURE_SIDE / DISTRIBUTION_SIDE |
| HIGH_RESULT_WALLET | EXECUTION_SIDE |
| SAME_SOURCE_GROUP | EXECUTION_SIDE |
| DISTRIBUTION_SELLER | DISTRIBUTION_SIDE |
| BAGHOLDER_WHALE | COUNTERPARTY_SIDE |
| RETAIL_NOISE | NOISE_SIDE |

---

# 五、再新增一个“对手盘压力分”

现在你已有：

```text
wallet_structure_score
wallet_risk_score
data_quality_score
```

建议增加：

```text
counterparty_pressure_score
```

它回答：

```text
当前是不是主导侧在把筹码转移给对手盘？
```

---

## counterparty_pressure_score 初始公式

满分 100。

| 维度 | 分数 |
|---|---:|
| 早期钱包卖出给晚期买盘 | 25 |
| 晚期大额钱包增加 | 20 |
| 套牢鲸鱼增加 | 15 |
| 价格上涨但结构钱包卖出 | 20 |
| 持有人数增加但 Top Holder 下降 | 10 |
| 高结果钱包退出 | 10 |

---

## 初始判断

```text
counterparty_pressure_score >= 70 → 对手盘承接压力高
50-69 → 对手盘承接压力中等
30-49 → 观察
<30 → 暂无明显对手盘压力
```

如果：

```text
counterparty_pressure_score >= 70
且 wallet_risk_score >= 50
```

动作：

```text
WALLET_BLOCK
```

如果：

```text
counterparty_pressure_score >= 50
但 wallet_structure_score >= 65
```

动作：

```text
WALLET_PAUSE
```

因为这代表：

```text
结构还在，但可能正在边拉边卖。
```

---

# 六、重新理解四种门禁状态

## 1. WALLET_SUPPORT

不是“发现庄家”。

而是：

```text
疑似结构侧仍未完全退出，对手盘压力不高，钱包行为与价格推进没有明显冲突。
```

典型结构：

```text
早期钱包仍有剩余
高结果钱包仍部分持有
同源组没有同步卖出
分发钱包少
对手盘压力低
```

---

## 2. WALLET_NEUTRAL

不是“不好”。

而是：

```text
暂时看不出主导侧，也看不出明显派发。
```

这种情况可以继续让 K 线、quote、安全层判断。

---

## 3. WALLET_PAUSE

含义变成：

```text
可能正在发生主导侧与对手盘之间的筹码转移，但证据还不够阻断。
```

典型情况：

```text
早期钱包卖出偏多
晚期买盘接入
高结果钱包部分退出
价格还没崩
数据不够完整
```

---

## 4. WALLET_BLOCK

含义变成：

```text
主导侧大概率已经把风险转移给对手盘，继续入场容易成为退出流动性。
```

典型情况：

```text
早期钱包集中清仓
同源组同步卖出
高结果钱包退出
分发钱包增加
晚期鲸鱼/散户接货
价格上涨但结构钱包卖出
```

---

# 七、对 classify(w) 的补强

原来的分类只判断“钱包是什么”。  
现在要增加一层：

```text
它在当前博弈里站在哪一边？
```

可以这样输出：

```json
{
  "wallet_address": "xxx",
  "wallet_role": "HIGH_RESULT_WALLET",
  "game_side": "EXECUTION_SIDE",
  "role_confidence": 0.78,
  "counterparty_signal": false,
  "distribution_signal": false,
  "structure_support_signal": true,
  "reason": "早期进入，高 ROI，仍有 35% 剩余筹码，未发现同步卖出"
}
```

如果是被动接货：

```json
{
  "wallet_address": "xxx",
  "wallet_role": "BAGHOLDER_WHALE",
  "game_side": "COUNTERPARTY_SIDE",
  "role_confidence": 0.72,
  "counterparty_signal": true,
  "distribution_signal": false,
  "structure_support_signal": false,
  "reason": "晚期大额买入，当前浮亏较大，仍持有高比例筹码，疑似被动承接"
}
```

---

# 八、对门禁逻辑的升级

原来的门禁：

```text
结构分 + 风险分 + 数据质量分
```

升级为：

```text
结构分 + 风险分 + 对手盘压力分 + 数据质量分
```

最终规则：

```text
if wallet_risk_score >= 75:
    WALLET_BLOCK

elif counterparty_pressure_score >= 70 and wallet_risk_score >= 50:
    WALLET_BLOCK

elif same_source_sync_sell_score >= 70:
    WALLET_BLOCK

elif early_wallet_sold_pct >= 85 and high_result_remaining_pct <= 10:
    WALLET_BLOCK

elif counterparty_pressure_score >= 50:
    WALLET_PAUSE

elif data_quality_score < 50:
    WALLET_PAUSE

elif wallet_structure_score >= 65 
     and wallet_risk_score <= 40 
     and counterparty_pressure_score <= 40 
     and data_quality_score >= 60:
    WALLET_SUPPORT

else:
    WALLET_NEUTRAL
```

---

# 九、你真正要监控的不是“庄家”，而是这 5 个结构迁移

## 1. 筹码从早期钱包 → 晚期钱包

这是最重要的风险迁移。

```text
early_wallet_sold_pct 上升
late_wallet_buy_amount 上升
holder_count 上升
price 不再有效推进
```

含义：

```text
主导侧可能正在找对手盘退出。
```

---

## 2. 筹码从同源组 → 分散散户

```text
same_source_group_remaining_pct 下降
retail_holder_count 上升
small_holder_count 上升
```

含义：

```text
筹码控制力下降。
```

---

## 3. 高结果钱包从持有 → 清仓

```text
high_result_remaining_pct 下降
high_result_wallet_count 清仓比例上升
```

含义：

```text
优势钱包退出，后续结构价值下降。
```

---

## 4. Top Holder 下降但价格上涨

```text
top_holder_pct 下降
price 上涨
volume 放大
```

含义：

```text
可能是边拉边派发。
```

---

## 5. 接盘鲸鱼出现后没有继续推进

```text
bagholder_whale_count 增加
price 横盘或下跌
volume 下降
```

含义：

```text
鲸鱼可能不是主导侧，而是被动承接。
```

---

# 十、直接加入系统的新字段

建议在 `wallet_structure_decision.json` 里增加：

```json
{
  "game_side_summary": {
    "structure_side_wallet_count": 8,
    "execution_side_wallet_count": 5,
    "distribution_side_wallet_count": 4,
    "counterparty_side_wallet_count": 6,
    "noise_side_wallet_count": 32
  },
  "counterparty_pressure_score": 58,
  "dominant_side_status": "STRUCTURE_WEAKENING",
  "chip_transfer_status": "EARLY_TO_LATE_TRANSFER",
  "market_game_interpretation": "早期钱包卖出增加，晚期承接钱包增加，疑似出现筹码向对手盘转移，需要暂停观察"
}
```

---

# 十一、dominant_side_status 状态标准

新增字段：

```text
dominant_side_status
```

取值：

```text
STRUCTURE_STRENGTHENING   结构侧增强
STRUCTURE_HOLDING         结构侧维持
STRUCTURE_WEAKENING       结构侧减弱
DISTRIBUTION_ACTIVE       派发进行中
COUNTERPARTY_ABSORBING    对手盘承接中
UNKNOWN                   未知
```

---

## 判断逻辑

### STRUCTURE_STRENGTHENING

```text
早期钱包仍持有
同源组未同步卖出
高结果钱包仍持有
分发钱包少
对手盘压力低
```

### STRUCTURE_HOLDING

```text
早期钱包部分卖出
但仍有明显剩余
高结果钱包未完全退出
价格结构未破坏
```

### STRUCTURE_WEAKENING

```text
早期钱包卖出增加
高结果钱包剩余下降
同源组开始卖出
但还没有完全派发
```

### DISTRIBUTION_ACTIVE

```text
分发钱包明显增加
同源组同步卖出
Top Holder 出货
价格仍被维持或拉升
```

### COUNTERPARTY_ABSORBING

```text
晚期大额买入增加
套牢鲸鱼增加
散户数增加
早期钱包卖出
价格推进效率下降
```

---

# 十二、最终结论

你的方向是对的。  
可以、也应该加入“庄家对手盘”思维，但要转成工程化语言：

不要写：

```text
庄家在出货
```

系统里应该写：

```text
DISTRIBUTION_ACTIVE
counterparty_pressure_score = 78
chip_transfer_status = EARLY_TO_LATE_TRANSFER
wallet_structure_status = WALLET_BLOCK
reason = 早期钱包集中卖出，晚期大额承接增加，同源组出现同步卖出，疑似筹码向对手盘转移
```

这才是 SIKK 应该采用的表达方式。

---

# 下一步建议

下一步可以直接升级你的 v1.0 标准：

```text
在原来的 wallet_structure_score / wallet_risk_score / data_quality_score 之外，
新增 counterparty_pressure_score 和 game_side 字段。
```

这样系统的判断会从：

```text
钱包有没有卖
```

升级成：

```text
筹码正在从哪一侧转移到哪一侧
谁在主动退出
谁在被动承接
当前入场是否会成为别人的退出流动性
```

---

# 本次认知升级点

这次核心升级是：

> 钱包结构门禁不是单纯识别“好钱包 / 坏钱包”，而是识别“主导侧是否仍在、对手盘是否正在接货、筹码控制权是否转移”。

这会让 SIKK 更接近你的原始目标：  
不是普通量价交易，而是结构资金行为识别。

---

# 尚未解决问题

下一步要继续定稿：

```text
1. counterparty_pressure_score 的完整计算公式
2. game_side 在 classify(w) 中的具体映射代码
3. dominant_side_status 的判断规则
4. chip_transfer_status 的状态枚举
5. 如何把这些字段接入 WALLET_BLOCK / WALLET_PAUSE / WALLET_SUPPORT
```


---

## 片段 53 / stream_idx=8108 / len=22787


# SIKK 钱包结构门禁 v1.0：5 个核心标准定稿

建议你现在就按下面这套执行。  
不要再等数据完整后才开始，也不要一次性做复杂角色系统。

v1.0 的目标是：

```text
能稳定分类钱包
能输出结构支持分
能输出钱包风险分
能判断数据质量
能让 10 个 token 样本进入复盘校准
```

---

# 1. v1.0 的 8 类钱包角色 classify(w) 判断规则

## 1.1 v1.0 先用 8 类角色

先不要做太细。v1.0 保留这 8 类：

| 角色代码 | 中文名 | 核心含义 |
|---|---|---|
| EARLY_BUYER | 早期买入钱包 | 开盘早期进入，仍可能参与结构 |
| EARLY_EXIT | 早期清仓钱包 | 早期进入但已经大部分退出 |
| PARTIAL_HOLDER | 部分持有钱包 | 买过、卖过，但仍有剩余筹码 |
| HIGH_RESULT_WALLET | 高结果钱包 | ROI / PnL 表现明显较好 |
| SAME_SOURCE_GROUP | 疑似同源组钱包 | 资金来源或行为高度相似 |
| DISTRIBUTION_SELLER | 疑似分发 / 派发钱包 | 明显卖出、转出、分发压力 |
| BAGHOLDER_WHALE | 套牢鲸鱼 | 高位重仓、浮亏或未及时退出 |
| RETAIL_NOISE | 普通噪音钱包 | 小额、晚入、低证据、无结构意义 |

---

## 1.2 classify(w) 所需输入字段

每个钱包 `w` 至少要有这些字段：

```text
wallet_address
entry_rank
entry_time
buy_amount_usd
sell_amount_usd
net_buy_usd
holding_pct
sold_pct
remaining_pct
roi_pct
pnl_usd
trade_count
buy_count
sell_count
is_new_wallet
is_top_holder
is_top_trader
funding_source
same_source_group_id
same_source_group_size
sync_buy_score
sync_sell_score
distribution_risk
data_missing_fields
```

如果字段暂时没有，就保留为空，但要进入 `data_quality_score` 扣分。

---

## 1.3 classify(w) 优先级

钱包角色不能随便按顺序判断。  
必须有优先级，否则同一个钱包可能同时符合多个角色。

建议优先级：

```text
1. DISTRIBUTION_SELLER
2. EARLY_EXIT
3. SAME_SOURCE_GROUP
4. HIGH_RESULT_WALLET
5. BAGHOLDER_WHALE
6. PARTIAL_HOLDER
7. EARLY_BUYER
8. RETAIL_NOISE
```

原因：

- 明显派发 / 清仓是最高风险，必须优先识别。
- 同源组是结构证据，优先级高于普通早期买入。
- 高结果钱包有价值，但如果它已经派发，要先归为派发。
- 普通早期买入只是基础身份，不应覆盖更强角色。

---

## 1.4 具体判断规则

### A. DISTRIBUTION_SELLER：疑似分发 / 派发钱包

触发条件之一即可：

```text
sold_pct >= 80
remaining_pct <= 20
sell_amount_usd > buy_amount_usd * 0.7
```

或：

```text
distribution_risk == HIGH
```

或：

```text
is_top_holder == true
且 sold_pct >= 60
```

含义：

> 这个钱包已经不再是支撑结构，而是潜在卖压来源。

---

### B. EARLY_EXIT：早期清仓钱包

触发条件：

```text
entry_rank <= early_rank_threshold
sold_pct >= 85
remaining_pct <= 15
```

建议初始：

```text
early_rank_threshold = 50
```

如果 GMGN 能提供前 N 个买入者，第一版可以认为：

```text
前 50 = 早期钱包
前 100 = 扩展早期钱包
```

含义：

> 早期进场，但已经大部分退出。对二拉结构不友好。

---

### C. SAME_SOURCE_GROUP：疑似同源组钱包

触发条件：

```text
same_source_group_id 不为空
same_source_group_size >= 3
```

并且满足以下任一：

```text
sync_buy_score >= 60
sync_sell_score >= 60
funding_source 相同
entry_time 接近
entry_rank 接近
```

含义：

> 这些钱包可能不是独立散户，而是一组执行钱包。

注意：

- 同源组本身不一定是坏事。
- 如果同步买入、仍持有，可能是结构支持。
- 如果同步卖出，就是高风险。

---

### D. HIGH_RESULT_WALLET：高结果钱包

触发条件之一：

```text
roi_pct >= 100
```

或：

```text
pnl_usd >= 500
```

或：

```text
roi_pct >= 50
且 remaining_pct >= 30
```

含义：

> 这个钱包在当前 token 中结果较好，可能是早期有效执行者、聪明钱包或结构参与者。

注意：

如果同时满足 `sold_pct >= 80`，优先归为：

```text
DISTRIBUTION_SELLER
```

---

### E. BAGHOLDER_WHALE：套牢鲸鱼

触发条件：

```text
holding_pct >= 1
roi_pct <= -30
remaining_pct >= 70
```

或：

```text
buy_amount_usd 较大
remaining_pct >= 80
price 已明显跌破其成本区
```

含义：

> 这个钱包可能成为上方卖压，也可能是被套承接者。

v1.0 先不要判断它是好是坏，只记录为风险结构。

---

### F. PARTIAL_HOLDER：部分持有钱包

触发条件：

```text
remaining_pct >= 20
sold_pct >= 20
sold_pct < 80
```

含义：

> 已经兑现一部分，但还没有完全退出。

这种钱包对结构判断很重要：

- 如果早期钱包大多是 `PARTIAL_HOLDER`，结构可能还没完全结束。
- 如果早期钱包大多是 `EARLY_EXIT`，风险明显升高。

---

### G. EARLY_BUYER：早期买入钱包

触发条件：

```text
entry_rank <= early_rank_threshold
remaining_pct > 15
```

建议初始：

```text
early_rank_threshold = 50
```

或按时间：

```text
entry_time <= token_open_time + 10 分钟
```

如果是极短线 meme，可以改成：

```text
entry_time <= token_open_time + 3 分钟
```

含义：

> 早期进入，并且还没完全退出。

---

### H. RETAIL_NOISE：普通噪音钱包

默认兜底分类。

触发条件：

```text
买入金额小
入场时间晚
无同源组
无高结果
无明显持仓影响
无明显派发风险
```

含义：

> 不作为结构判断核心证据。

---

## 1.5 classify(w) 伪代码

```python
def classify_wallet(w):
    """
    SIKK v1.0 钱包角色分类。
    输入：单个钱包字段。
    输出：wallet_role, role_confidence, reason
    """

    # 1. 派发 / 分发优先
    if (
        w.sold_pct >= 80
        and w.remaining_pct <= 20
    ) or (
        w.sell_amount_usd >= w.buy_amount_usd * 0.7
    ) or (
        w.is_top_holder and w.sold_pct >= 60
    ) or (
        w.distribution_risk == "HIGH"
    ):
        return "DISTRIBUTION_SELLER", 0.85, "高卖出比例或 Top Holder 出货，疑似分发/派发钱包"

    # 2. 早期清仓
    if (
        w.entry_rank <= 50
        and w.sold_pct >= 85
        and w.remaining_pct <= 15
    ):
        return "EARLY_EXIT", 0.85, "早期进入后大部分清仓"

    # 3. 同源组
    if (
        w.same_source_group_id
        and w.same_source_group_size >= 3
        and (
            w.sync_buy_score >= 60
            or w.sync_sell_score >= 60
        )
    ):
        return "SAME_SOURCE_GROUP", 0.75, "存在同源组或同步行为"

    # 4. 高结果钱包
    if (
        w.roi_pct >= 100
        or w.pnl_usd >= 500
        or (w.roi_pct >= 50 and w.remaining_pct >= 30)
    ):
        return "HIGH_RESULT_WALLET", 0.75, "ROI/PnL 表现明显较好"

    # 5. 套牢鲸鱼
    if (
        w.holding_pct >= 1
        and w.roi_pct <= -30
        and w.remaining_pct >= 70
    ):
        return "BAGHOLDER_WHALE", 0.70, "高持仓且浮亏明显，疑似套牢鲸鱼"

    # 6. 部分持有
    if (
        w.remaining_pct >= 20
        and 20 <= w.sold_pct < 80
    ):
        return "PARTIAL_HOLDER", 0.65, "已部分卖出但仍有持仓"

    # 7. 早期买入
    if (
        w.entry_rank <= 50
        and w.remaining_pct > 15
    ):
        return "EARLY_BUYER", 0.65, "早期进入且仍有剩余筹码"

    # 8. 默认噪音
    return "RETAIL_NOISE", 0.40, "未发现明显结构特征"
```

---

# 2. wallet_structure_score 初始计算公式

## 2.1 定义

`wallet_structure_score` 是结构支持分，满分 100。

它回答：

```text
钱包结构是否支持继续观察 / 进入 PAPER_READY？
```

不是买入分。  
它只表示结构是否支持。

---

## 2.2 初始权重

| 维度 | 权重 |
|---|---:|
| 早期钱包仍持有 | 25 |
| 高结果钱包仍持有 | 20 |
| 同源组没有同步卖出 | 15 |
| 分发风险低 | 15 |
| 接盘 / 持仓结构稳定 | 10 |
| Top Trader 未反向 | 10 |
| 数据与 K线不冲突 | 5 |
| 合计 | 100 |

---

## 2.3 具体计算

```text
wallet_structure_score =
  early_holder_score
+ high_result_score
+ same_source_support_score
+ low_distribution_score
+ holder_stability_score
+ top_trader_score
+ consistency_score
```

---

## 2.4 分项规则

### A. early_holder_score：早期钱包仍持有，0-25 分

```text
early_wallet_remaining_pct >= 50 → 25
30 <= early_wallet_remaining_pct < 50 → 18
15 <= early_wallet_remaining_pct < 30 → 8
early_wallet_remaining_pct < 15 → 0
```

---

### B. high_result_score：高结果钱包仍持有，0-20 分

```text
high_result_wallet_count >= 2 且 high_result_remaining_pct >= 40 → 20
high_result_wallet_count >= 1 且 high_result_remaining_pct >= 25 → 14
high_result_wallet_count >= 1 且 high_result_remaining_pct >= 10 → 6
无高结果钱包或基本清仓 → 0
```

---

### C. same_source_support_score：同源组未同步卖出，0-15 分

```text
same_source_group_count >= 1 且 same_source_sync_sell_score < 30 → 15
same_source_group_count >= 1 且 30 <= sync_sell_score < 50 → 8
same_source_group_count == 0 → 5
sync_sell_score >= 50 → 0
```

解释：

- 有同源组且没卖，是结构支持。
- 没有同源组，不加太多分，也不扣太多。
- 同源组同步卖出，直接不给分。

---

### D. low_distribution_score：分发风险低，0-15 分

```text
distribution_wallet_count == 0 → 15
distribution_wallet_count == 1 → 10
distribution_wallet_count == 2 → 5
distribution_wallet_count >= 3 → 0
```

---

### E. holder_stability_score：持仓稳定，0-10 分

```text
top_holder_exit_pressure == LOW → 10
top_holder_exit_pressure == MEDIUM → 5
top_holder_exit_pressure == HIGH → 0
```

---

### F. top_trader_score：Top Trader 未反向，0-10 分

```text
top_trader_buy_sell_bias == BUY_OR_HOLD → 10
top_trader_buy_sell_bias == NEUTRAL → 5
top_trader_buy_sell_bias == SELL → 0
```

---

### G. consistency_score：钱包与 K线 / quote 不冲突，0-5 分

```text
wallet_behavior_matches_price_action == true → 5
不明确 → 2
明显冲突 → 0
```

例子：

- 钱包仍持有，价格构筑箱体，不冲突。
- 钱包大量清仓，但 K线拉升，冲突，可能是边拉边卖。

---

## 2.5 结构支持分解释

| 分数 | 解释 |
|---:|---|
| 0-39 | 结构不支持 |
| 40-64 | 中性 / 观察 |
| 65-79 | 结构支持 |
| 80-100 | 强结构支持，但 v1.0 不直接加仓 |

---

# 3. wallet_risk_score 初始计算公式

## 3.1 定义

`wallet_risk_score` 是钱包结构风险分，满分 100。

它回答：

```text
钱包结构是否存在明显卖压、撤退、派发、数据不足风险？
```

---

## 3.2 初始权重

| 风险维度 | 权重 |
|---|---:|
| 早期钱包集中清仓 | 30 |
| 同源组同步卖出 | 25 |
| 分发 / 派发钱包增加 | 15 |
| 高结果钱包退出 | 10 |
| Top Holder 出货 | 10 |
| 套牢鲸鱼压力 | 5 |
| 数据不足 | 5 |
| 合计 | 100 |

---

## 3.3 具体计算

```text
wallet_risk_score =
  early_exit_risk
+ same_source_exit_risk
+ distribution_risk_score
+ high_result_exit_risk
+ top_holder_exit_risk
+ bagholder_pressure_risk
+ data_missing_risk
```

---

## 3.4 分项规则

### A. early_exit_risk：早期清仓风险，0-30 分

```text
early_wallet_sold_pct >= 85 → 30
70 <= early_wallet_sold_pct < 85 → 22
50 <= early_wallet_sold_pct < 70 → 12
early_wallet_sold_pct < 50 → 0
```

---

### B. same_source_exit_risk：同源组同步卖出风险，0-25 分

```text
same_source_sync_sell_score >= 80 → 25
60 <= same_source_sync_sell_score < 80 → 18
40 <= same_source_sync_sell_score < 60 → 8
sync_sell_score < 40 → 0
```

---

### C. distribution_risk_score：分发钱包风险，0-15 分

```text
distribution_wallet_count >= 5 → 15
distribution_wallet_count == 3 or 4 → 10
distribution_wallet_count == 1 or 2 → 5
distribution_wallet_count == 0 → 0
```

---

### D. high_result_exit_risk：高结果钱包退出风险，0-10 分

```text
high_result_wallet_count >= 2 且 high_result_remaining_pct <= 10 → 10
high_result_wallet_count >= 1 且 high_result_remaining_pct <= 20 → 6
否则 → 0
```

---

### E. top_holder_exit_risk：Top Holder 出货风险，0-10 分

```text
top_holder_exit_pressure == HIGH → 10
top_holder_exit_pressure == MEDIUM → 5
top_holder_exit_pressure == LOW → 0
```

---

### F. bagholder_pressure_risk：套牢鲸鱼压力，0-5 分

```text
bagholder_whale_count >= 3 → 5
bagholder_whale_count == 1 or 2 → 3
bagholder_whale_count == 0 → 0
```

---

### G. data_missing_risk：数据不足风险，0-5 分

```text
data_quality_score < 50 → 5
50 <= data_quality_score < 70 → 3
data_quality_score >= 70 → 0
```

---

## 3.5 风险分解释

| 分数 | 解释 | 动作 |
|---:|---|---|
| 0-39 | 风险可接受 | 可继续过其他门禁 |
| 40-59 | 中风险 | WATCHING / PAUSE |
| 60-74 | 高风险 | PAUSE，除非强信号共振 |
| 75-100 | 极高风险 | WALLET_BLOCK |

---

# 4. data_quality_score 如何计算

## 4.1 定义

`data_quality_score` 是数据质量分，满分 100。

它回答：

```text
这次钱包结构判断的数据够不够用？
```

注意：

数据质量分不是结构分。  
它只判断这次分析是否可靠。

---

## 4.2 初始权重

| 维度 | 权重 |
|---|---:|
| 早期钱包数据完整度 | 25 |
| 持仓 / 买卖字段完整度 | 20 |
| 时间字段完整度 | 15 |
| ROI / PnL 字段完整度 | 15 |
| 同源 / 资金来源字段完整度 | 15 |
| Top Holder / Top Trader 数据完整度 | 10 |
| 合计 | 100 |

---

## 4.3 具体计算

```text
data_quality_score =
  early_wallet_data_score
+ holding_trade_field_score
+ time_field_score
+ result_field_score
+ source_field_score
+ top_holder_field_score
```

---

## 4.4 分项规则

### A. early_wallet_data_score：早期钱包数据，0-25 分

```text
early_wallet_count >= 50 → 25
30 <= early_wallet_count < 50 → 18
10 <= early_wallet_count < 30 → 10
early_wallet_count < 10 → 3
```

---

### B. holding_trade_field_score：持仓 / 买卖字段，0-20 分

检查字段：

```text
buy_amount_usd
sell_amount_usd
net_buy_usd
sold_pct
remaining_pct
holding_pct
```

计分：

```text
完整率 >= 90% → 20
完整率 >= 70% → 14
完整率 >= 50% → 8
完整率 < 50% → 3
```

---

### C. time_field_score：时间字段，0-15 分

检查字段：

```text
entry_time
entry_rank
last_trade_time
holding_duration
```

计分：

```text
完整率 >= 90% → 15
完整率 >= 70% → 10
完整率 >= 50% → 5
完整率 < 50% → 0
```

---

### D. result_field_score：结果字段，0-15 分

检查字段：

```text
roi_pct
pnl_usd
realized_profit
unrealized_profit
```

计分：

```text
完整率 >= 90% → 15
完整率 >= 70% → 10
完整率 >= 50% → 5
完整率 < 50% → 0
```

---

### E. source_field_score：资金来源 / 同源字段，0-15 分

检查字段：

```text
funding_source
same_source_group_id
same_source_group_size
sync_buy_score
sync_sell_score
```

计分：

```text
完整率 >= 80% → 15
完整率 >= 50% → 8
完整率 >= 20% → 3
完整率 < 20% → 0
```

注意：

这项可能 v1.0 初期经常偏低，所以不要因为这一项低就完全废弃样本。  
但如果总分低于 50，就不应该直接给 `WALLET_SUPPORT`。

---

### F. top_holder_field_score：Top Holder / Top Trader 数据，0-10 分

检查字段：

```text
is_top_holder
is_top_trader
top_holder_exit_pressure
top_trader_buy_sell_bias
```

计分：

```text
完整率 >= 80% → 10
完整率 >= 50% → 5
完整率 < 50% → 0
```

---

## 4.5 数据质量分动作

| data_quality_score | 含义 | 动作 |
|---:|---|---|
| 80-100 | 数据较完整 | 可正常判断 |
| 60-79 | 可用但需保守 | 可以 SUPPORT / NEUTRAL |
| 50-59 | 勉强可用 | 不允许强 SUPPORT |
| < 50 | 数据不足 | WALLET_PAUSE |

---

# 5. 门禁最终决策规则

把三个分数合起来：

```text
wallet_structure_score
wallet_risk_score
data_quality_score
```

---

## 5.1 硬阻断规则

只要触发，直接 `WALLET_BLOCK`：

```text
wallet_risk_score >= 75
```

或：

```text
same_source_sync_sell_score >= 70
```

或：

```text
early_wallet_sold_pct >= 85
且 high_result_remaining_pct <= 10
```

或：

```text
distribution_wallet_count >= 3
且 early_wallet_remaining_pct <= 20
```

---

## 5.2 暂停规则

触发则 `WALLET_PAUSE`：

```text
data_quality_score < 50
```

或：

```text
wallet_risk_score >= 50
```

或：

```text
top_holder_exit_pressure == HIGH
```

或：

```text
高结果钱包退出明显，但早期钱包状态不清楚
```

---

## 5.3 支持规则

必须同时满足：

```text
wallet_structure_score >= 65
wallet_risk_score <= 40
data_quality_score >= 60
early_wallet_remaining_pct >= 30
same_source_sync_sell_score < 50
distribution_wallet_count <= 1
```

输出：

```text
WALLET_SUPPORT
```

---

## 5.4 中性规则

其他情况：

```text
WALLET_NEUTRAL
```

---

# 6. 第一次 10 个 token 复盘模板

第一次 10 个 token 不要重点看赚钱。  
重点看：

```text
数据是否完整
分类是否稳定
门禁是否过严
门禁是否过松
哪些字段缺失严重
哪些判断明显错
```

---

## 6.1 复盘文件建议

每次跑完 10 个 token，生成：

```text
data/gmgn_candidates_live_run/wallet_structure/review_batch_001.md
data/gmgn_candidates_live_run/wallet_structure/review_batch_001.csv
```

---

## 6.2 review_batch_001.csv 字段

```text
token_address
token_symbol
run_time
wallet_structure_status
wallet_structure_score
wallet_risk_score
data_quality_score
wallet_structure_factor
early_wallet_count
early_wallet_remaining_pct
early_wallet_sold_pct
high_result_wallet_count
high_result_remaining_pct
same_source_group_count
same_source_sync_sell_score
distribution_wallet_count
bagholder_whale_count
top_holder_exit_pressure
decision_action
decision_reason
paper_entry_allowed
paper_position_opened
max_profit_pct_after_signal
max_drawdown_pct_after_signal
close_pnl_pct
failure_type
manual_review_label
manual_review_note
threshold_adjustment_needed
```

---

## 6.3 manual_review_label 人工复盘标签

每个 token 人工打一个标签：

```text
GOOD_BLOCK        阻断正确
BAD_BLOCK         阻断过严
GOOD_SUPPORT      支持正确
BAD_SUPPORT       支持过松
GOOD_PAUSE        暂停正确
BAD_PAUSE         暂停过严
DATA_BAD          数据不足，不评价
UNCLEAR           结果不清楚
```

---

## 6.4 10 个 token 的复盘问题

每个 token 复盘时回答这 8 个问题：

```text
1. 钱包结构状态是否符合肉眼观察？
2. WALLET_BLOCK 是否真的避免了明显风险？
3. WALLET_SUPPORT 后价格是否至少出现可交易推进？
4. WALLET_PAUSE 是否因为数据不足，还是规则过于保守？
5. early_wallet_sold_pct 是否有解释力？
6. high_result_remaining_pct 是否有解释力？
7. same_source_sync_sell_score 是否误伤？
8. distribution_wallet_count 是否识别过宽或过窄？
```

---

## 6.5 10 个 token 后怎么校准？

### 如果 BAD_BLOCK 太多

说明门禁过严。  
优先调整：

```text
early_wallet_sold_pct 阈值从 85 提高到 90
wallet_risk_score BLOCK 阈值从 75 提高到 80
distribution_wallet_count >= 3 改成 >= 4
```

---

### 如果 BAD_SUPPORT 太多

说明支持条件太松。  
优先调整：

```text
wallet_structure_score SUPPORT 阈值从 65 提高到 70
wallet_risk_score 上限从 40 降到 35
early_wallet_remaining_pct 从 30 提高到 40
high_result_remaining_pct 从 20 提高到 30
```

---

### 如果 DATA_BAD 太多

说明字段采集不够。  
不要先调阈值，先修采集。

重点检查：

```text
early_wallet_raw.csv 是否完整
entry_rank 是否稳定
sold_pct / remaining_pct 是否可信
same_source_group_id 是否为空太多
ROI / PnL 是否缺失
Top Holder 数据是否能取到
```

---

### 如果 WALLET_PAUSE 太多

说明系统不敢判断。  
要区分两种情况：

#### 情况 A：数据不足导致 PAUSE

解决：

```text
提高字段采集质量
增加 GMGN 数据源
补充 early_wallet_raw
```

#### 情况 B：规则太保守导致 PAUSE

解决：

```text
降低 SUPPORT 阈值
提高风险容忍区间
减少 data_quality_score 的阻断权重
```

---

# 7. 直接可用的输出 JSON 标准

每个 token 的 `wallet_structure_decision.json` 建议长这样：

```json
{
  "token_address": "TOKEN_ADDRESS",
  "token_symbol": "TOKEN",
  "wallet_structure_status": "WALLET_SUPPORT",
  "wallet_structure_score": 72,
  "wallet_risk_score": 28,
  "data_quality_score": 76,
  "wallet_structure_factor": 1.15,
  "wallet_evidence_level": "E2",
  "decision_action": "ALLOW_PAPER_READY",
  "reason": "早期钱包仍有部分持仓，高结果钱包未集中退出，同源组未出现同步卖出，分发风险较低",
  "support_signals": [
    "EARLY_WALLETS_PARTIAL_HOLDING",
    "HIGH_RESULT_WALLETS_STILL_HOLDING",
    "LOW_DISTRIBUTION_RISK"
  ],
  "risk_signals": [
    "TOP_TRADER_NEUTRAL"
  ],
  "metrics": {
    "early_wallet_count": 42,
    "early_wallet_remaining_pct": 38.5,
    "early_wallet_sold_pct": 61.5,
    "high_result_wallet_count": 3,
    "high_result_remaining_pct": 31.2,
    "same_source_group_count": 1,
    "same_source_sync_sell_score": 22,
    "distribution_wallet_count": 1,
    "bagholder_whale_count": 0,
    "top_holder_exit_pressure": "LOW",
    "top_trader_buy_sell_bias": "NEUTRAL"
  },
  "score_breakdown": {
    "wallet_structure_score": {
      "early_holder_score": 18,
      "high_result_score": 14,
      "same_source_support_score": 15,
      "low_distribution_score": 10,
      "holder_stability_score": 10,
      "top_trader_score": 5,
      "consistency_score": 0
    },
    "wallet_risk_score": {
      "early_exit_risk": 12,
      "same_source_exit_risk": 0,
      "distribution_risk_score": 5,
      "high_result_exit_risk": 0,
      "top_holder_exit_risk": 0,
      "bagholder_pressure_risk": 0,
      "data_missing_risk": 3
    },
    "data_quality_score": {
      "early_wallet_data_score": 18,
      "holding_trade_field_score": 20,
      "time_field_score": 10,
      "result_field_score": 10,
      "source_field_score": 8,
      "top_holder_field_score": 10
    }
  },
  "created_at": "2026-05-02T00:00:00Z"
}
```

---

# 8. 直接发给 AI / Codex / OpenClaw 的开发指令

```text
任务：实现 SIKK-SOL v1.0 钱包结构门禁的初始判断标准。

一、实现 classify(w)

请实现 8 类钱包角色：
1. EARLY_BUYER：早期买入钱包
2. EARLY_EXIT：早期清仓钱包
3. PARTIAL_HOLDER：部分持有钱包
4. HIGH_RESULT_WALLET：高结果钱包
5. SAME_SOURCE_GROUP：疑似同源组钱包
6. DISTRIBUTION_SELLER：疑似分发/派发钱包
7. BAGHOLDER_WHALE：套牢鲸鱼
8. RETAIL_NOISE：普通噪音钱包

分类优先级：
1. DISTRIBUTION_SELLER
2. EARLY_EXIT
3. SAME_SOURCE_GROUP
4. HIGH_RESULT_WALLET
5. BAGHOLDER_WHALE
6. PARTIAL_HOLDER
7. EARLY_BUYER
8. RETAIL_NOISE

基础规则：
- DISTRIBUTION_SELLER：
  sold_pct >= 80 且 remaining_pct <= 20
  或 sell_amount_usd >= buy_amount_usd * 0.7
  或 is_top_holder=true 且 sold_pct >= 60
  或 distribution_risk=HIGH

- EARLY_EXIT：
  entry_rank <= 50 且 sold_pct >= 85 且 remaining_pct <= 15

- SAME_SOURCE_GROUP：
  same_source_group_id 不为空
  且 same_source_group_size >= 3
  且 sync_buy_score >= 60 或 sync_sell_score >= 60

- HIGH_RESULT_WALLET：
  roi_pct >= 100
  或 pnl_usd >= 500
  或 roi_pct >= 50 且 remaining_pct >= 30

- BAGHOLDER_WHALE：
  holding_pct >= 1
  且 roi_pct <= -30
  且 remaining_pct >= 70

- PARTIAL_HOLDER：
  remaining_pct >= 20
  且 20 <= sold_pct < 80

- EARLY_BUYER：
  entry_rank <= 50
  且 remaining_pct > 15

- RETAIL_NOISE：
  默认兜底分类

二、实现 wallet_structure_score

满分 100，分项：
- early_holder_score：0-25
- high_result_score：0-20
- same_source_support_score：0-15
- low_distribution_score：0-15
- holder_stability_score：0-10
- top_trader_score：0-10
- consistency_score：0-5

规则：
- early_wallet_remaining_pct >= 50 → 25
- 30 <= early_wallet_remaining_pct < 50 → 18
- 15 <= early_wallet_remaining_pct < 30 → 8
- early_wallet_remaining_pct < 15 → 0

- high_result_wallet_count >= 2 且 high_result_remaining_pct >= 40 → 20
- high_result_wallet_count >= 1 且 high_result_remaining_pct >= 25 → 14
- high_result_wallet_count >= 1 且 high_result_remaining_pct >= 10 → 6
- 否则 → 0

- same_source_group_count >= 1 且 sync_sell_score < 30 → 15
- same_source_group_count >= 1 且 30 <= sync_sell_score < 50 → 8
- same_source_group_count == 0 → 5
- sync_sell_score >= 50 → 0

- distribution_wallet_count == 0 → 15
- distribution_wallet_count == 1 → 10
- distribution_wallet_count == 2 → 5
- distribution_wallet_count >= 3 → 0

- top_holder_exit_pressure LOW → 10
- MEDIUM → 5
- HIGH → 0

- top_trader_buy_sell_bias BUY_OR_HOLD → 10
- NEUTRAL → 5
- SELL → 0

- wallet_behavior_matches_price_action true → 5
- unclear → 2
- conflict → 0

三、实现 wallet_risk_score

满分 100，分项：
- early_exit_risk：0-30
- same_source_exit_risk：0-25
- distribution_risk_score：0-15
- high_result_exit_risk：0-10
- top_holder_exit_risk：0-10
- bagholder_pressure_risk：0-5
- data_missing_risk：0-5

规则：
- early_wallet_sold_pct >= 85 → 30
- 70 <= early_wallet_sold_pct < 85 → 22
- 50 <= early_wallet_sold_pct < 70 → 12
- early_wallet_sold_pct < 50 → 0

- same_source_sync_sell_score >= 80 → 25
- 60 <= same_source_sync_sell_score < 80 → 18
- 40 <= same_source_sync_sell_score < 60 → 8
- < 40 → 0

- distribution_wallet_count >= 5 → 15
- distribution_wallet_count == 3 or 4 → 10
- distribution_wallet_count == 1 or 2 → 5
- distribution_wallet_count == 0 → 0

- high_result_wallet_count >= 2 且 high_result_remaining_pct <= 10 → 10
- high_result_wallet_count >= 1 且 high_result_remaining_pct <= 20 → 6
- 否则 → 0

- top_holder_exit_pressure HIGH → 10
- MEDIUM → 5
- LOW → 0

- bagholder_whale_count >= 3 → 5
- bagholder_whale_count == 1 or 2 → 3
- bagholder_whale_count == 0 → 0

- data_quality_score < 50 → 5
- 50 <= data_quality_score < 70 → 3
- data_quality_score >= 70 → 0

四、实现 data_quality_score

满分 100，分项：
- early_wallet_data_score：0-25
- holding_trade_field_score：0-20
- time_field_score：0-15
- result_field_score：0-15
- source_field_score：0-15
- top_holder_field_score：0-10

规则：
- early_wallet_count >= 50 → 25
- 30 <= early_wallet_count < 50 → 18
- 10 <= early_wallet_count < 30 → 10
- early_wallet_count < 10 → 3

字段完整率按比例计分：
- holding_trade 字段完整率 >=90% → 20，>=70% →14，>=50% →8，否则3
- time 字段完整率 >=90% →15，>=70% →10，>=50% →5，否则0
- result 字段完整率 >=90% →15，>=70% →10，>=50% →5，否则0
- source 字段完整率 >=80% →15，>=50% →8，>=20% →3，否则0
- top_holder 字段完整率 >=80% →10，>=50% →5，否则0

五、实现最终门禁状态

规则：
- wallet_risk_score >= 75 → WALLET_BLOCK
- same_source_sync_sell_score >= 70 → WALLET_BLOCK
- early_wallet_sold_pct >= 85 且 high_result_remaining_pct <= 10 → WALLET_BLOCK
- distribution_wallet_count >= 3 且 early_wallet_remaining_pct <= 20 → WALLET_BLOCK

- data_quality_score < 50 → WALLET_PAUSE
- wallet_risk_score >= 50 → WALLET_PAUSE
- top_holder_exit_pressure == HIGH → WALLET_PAUSE

- wallet_structure_score >= 65
  且 wallet_risk_score <= 40
  且 data_quality_score >= 60
  且 early_wallet_remaining_pct >= 30
  且 same_source_sync_sell_score < 50
  且 distribution_wallet_count <= 1
  → WALLET_SUPPORT

- 其他 → WALLET_NEUTRAL

六、wallet_structure_factor

- WALLET_BLOCK → 0.00
- WALLET_PAUSE → 0.30
- WALLET_NEUTRAL → 1.00
- WALLET_SUPPORT → 1.15

七、第一次 10 个 token 跑完后，生成 review_batch_001.csv

字段包括：
- token_address
- token_symbol
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- data_quality_score
- wallet_structure_factor
- early_wallet_count
- early_wallet_remaining_pct
- early_wallet_sold_pct
- high_result_wallet_count
- high_result_remaining_pct
- same_source_group_count
- same_source_sync_sell_score
- distribution_wallet_count
- bagholder_whale_count
- top_holder_exit_pressure
- decision_action
- decision_reason
- paper_entry_allowed
- paper_position_opened
- max_profit_pct_after_signal
- max_drawdown_pct_after_signal
- close_pnl_pct
- failure_type
- manual_review_label
- manual_review_note
- threshold_adjustment_needed
```

---

# 本次认知升级点

这次应该把钱包结构系统从“概念角色”推进为三套可执行标准：

```text
classify(w)：钱包角色分类
wallet_structure_score：结构支持分
wallet_risk_score：钱包风险分
data_quality_score：数据可信度
```

核心变化是：

> 先不追求判断完美，而是让每个判断都有字段、有分数、有原因、有复盘入口。

---

# 尚未解决问题

下一步还需要继续细化：

```text
1. same_source_group_id 如何生成
2. sync_buy_score / sync_sell_score 如何计算
3. top_holder_exit_pressure 如何从 GMGN 字段映射
4. wallet_behavior_matches_price_action 如何判断
5. review_batch_001 跑完后如何自动生成阈值调整建议
```


---

## 片段 54 / stream_idx=8276 / len=5195


要分化，但**不能一开始分化得太细**。

正确路线是：

> **先建立 v1.0 最小判断标准 → 跑 10-30 个代币采集真实样本 → 再用样本反推阈值和细分类标准。**

不要等完全有数据再做标准，也不要一开始就把标准设计成“终极版本”。  
最稳的是采用：

```text
基础硬规则 + 观察型软指标 + 样本回填校准
```

---

# 一、为什么不能完全等跑数据后再定标准？

因为如果没有初始标准，系统跑出来的数据会很乱：

```text
不知道哪些钱包要记录
不知道哪些行为算风险
不知道哪些字段必须保存
不知道什么叫早期钱包
不知道什么叫集中清仓
不知道什么叫同源组同步卖出
```

这样后面复盘时会发现：  
数据虽然有了，但不能直接用于判断。

所以必须先定义一个 **v1.0 基础判断框架**。

---

# 二、为什么也不能一开始标准过细？

因为你现在还不知道真实数据分布。

比如你现在直接规定：

```text
早期钱包卖出 80% = 高风险
同源组同步卖出 70分 = BLOCK
高结果钱包剩余 30% = 支持
```

这些阈值可能在某些 token 有效，在另一些 token 完全失真。

meme token 差异很大：

```text
盘子大小不同
开盘速度不同
钱包数量不同
池子深度不同
狙击强度不同
Top Holder 结构不同
GMGN 数据完整度不同
```

所以标准要先粗，再通过样本校准。

---

# 三、推荐路线：三层标准法

## 第 1 层：v1.0 硬规则，先写死

这一层不用等数据，必须先有。

它解决的是：

```text
哪些情况一定不能进？
哪些情况必须暂停？
哪些情况可以支持？
```

---

## 第 2 层：v1.0 软评分，先保守

这一层可以给初始权重，但不要太自信。

它解决的是：

```text
结构强度是多少？
风险强度是多少？
是否只是轻微支持？
是否只是轻微风险？
```

---

## 第 3 层：样本回填校准

跑完一批 token 后再调整。

它解决的是：

```text
哪个阈值太松？
哪个阈值太严？
哪些字段有用？
哪些字段噪音大？
哪些角色分类需要增加？
```

---

# 四、v1.0 先分化到什么程度？

不要一开始分到 20 个角色。  
先分到 **8 类核心角色** 就够了。

## v1.0 钱包角色分类

```text
1. EARLY_BUYER              早期买入钱包
2. EARLY_EXIT               早期清仓钱包
3. PARTIAL_HOLDER           部分持有钱包
4. HIGH_RESULT_WALLET       高结果钱包
5. SAME_SOURCE_GROUP        疑似同源组钱包
6. DISTRIBUTION_SELLER      疑似分发/派发钱包
7. BAGHOLDER_WHALE          套牢鲸鱼
8. RETAIL_NOISE             普通噪音钱包
```

先不要急着拆成：

```text
新钱包狙击
临时执行钱包
Token 接收钱包
核心资金源
可疑中转节点
结果钱包
高结果鲸鱼
接盘鲸鱼
```

这些可以在 v1.1 / v1.2 再加。

---

# 五、v1.0 先定义哪些硬判断？

## 1. 早期钱包集中清仓

先定义：

```text
early_wallet_sold_pct >= 85%
early_wallet_remaining_pct <= 15%
```

动作：

```text
WALLET_BLOCK
```

原因：

```text
早期结构钱包大部分已经退出，二拉动机下降。
```

---

## 2. 高结果钱包全部退出

先定义：

```text
high_result_wallet_count >= 2
high_result_remaining_pct <= 10%
```

动作：

```text
WALLET_BLOCK 或 WALLET_PAUSE
```

如果同时早期钱包也大量清仓：

```text
WALLET_BLOCK
```

---

## 3. 同源组同步卖出

先定义：

```text
same_source_group_count >= 1
same_source_sync_sell_score >= 70
```

动作：

```text
WALLET_BLOCK
```

原因：

```text
疑似同一批执行钱包同步撤退。
```

---

## 4. 分发钱包增加

先定义：

```text
distribution_wallet_count >= 3
early_wallet_remaining_pct <= 20%
```

动作：

```text
WALLET_BLOCK
```

原因：

```text
出现派发结构，且早期筹码支撑不足。
```

---

## 5. 数据不足

先定义：

```text
data_quality_score < 50
```

动作：

```text
WALLET_PAUSE
```

原因：

```text
证据不足，不允许直接支持入场。
```

---

# 六、v1.0 支持条件先保守

不要因为一个钱包没卖就判断支持。  
必须多个条件共振。

## WALLET_SUPPORT 初始条件

```text
wallet_structure_score >= 65
wallet_risk_score <= 40
early_wallet_remaining_pct >= 30
high_result_remaining_pct >= 20
same_source_sync_sell_score < 50
distribution_wallet_count <= 1
```

动作：

```text
允许进入 PAPER_READY
```

但注意：

```text
WALLET_SUPPORT 不能绕过 quote gate
WALLET_SUPPORT 不能绕过 security gate
WALLET_SUPPORT 不能绕过 K线信号 gate
```

它只是结构支持，不是独立买入信号。

---

# 七、先跑多少个代币再校准？

建议分三批。

## 第一批：10 个 token

目标不是看收益，而是看字段能不能采全。

检查：

```text
GMGN 数据是否稳定
early_wallet_raw.csv 是否完整
wallet_classification.csv 是否能生成
wallet_structure_decision.json 是否能生成
状态机能否读取
paper runner 能否记录 wallet_structure_factor
```

这一批重点是：

```text
流程跑通
字段完整
不要急着优化阈值
```

---

## 第二批：30 个 token

开始看结构判断是否合理。

检查：

```text
WALLET_BLOCK 是否太多
WALLET_SUPPORT 是否太宽
WALLET_PAUSE 是否过度
高结果钱包是否真的有预测价值
早期清仓比例是否和后续走势有关
```

这一批可以调整：

```text
early_wallet_sold_pct 阈值
high_result_remaining_pct 阈值
same_source_sync_sell_score 阈值
distribution_wallet_count 阈值
```

---

## 第三批：100 个 token

开始做统计验证。

统计：

```text
WALLET_SUPPORT 后续收益
WALLET_NEUTRAL 后续收益
WALLET_PAUSE 后续收益
WALLET_BLOCK 后续是否真的走弱
不同钱包结构状态的胜率
不同钱包结构状态的最大回撤
不同失败归因的占比
```

到 100 个样本后，再考虑 v1.1 标准升级。

---

# 八、你现在应该怎么做？

我建议现在这样做：

```text
先不要继续细化所有钱包角色。
先写 v1.0 钱包结构门禁。
先只保留 8 类角色。
先跑 10-30 个 token。
再根据真实输出反推更细标准。
```

也就是：

```text
先建判断框架
再用数据校准标准
最后才扩展角色体系
```

---

# 九、v1.0 应该保存哪些“待校准字段”？

即使暂时不用来决策，也要保存。  
因为后面复盘会用到。

建议保存：

```text
early_wallet_count
early_wallet_remaining_pct
early_wallet_sold_pct
high_result_wallet_count
high_result_remaining_pct
same_source_group_count
same_source_sync_buy_score
same_source_sync_sell_score
distribution_wallet_count
bagholder_whale_count
top_holder_exit_pressure
top_trader_buy_sell_bias
smart_money_participation
kol_participation
new_wallet_ratio
avg_entry_rank
avg_roi_pct
data_quality_score
```

这些字段先进入：

```text
wallet_structure_decision.json
candidate_wallet_structure_summary.csv
daily_report
```

后面就能反推：

```text
哪些字段真正有预测力
哪些字段只是噪音
哪些字段需要加权
哪些字段应该变成硬门禁
```

---

# 十、最关键原则

## 先别追求“判断很准”

现在第一目标不是准，而是：

```text
每个 token 都能稳定生成结构判断
每个判断都有字段依据
每次纸面交易都能回填结构状态
每次失败都能看出是不是钱包结构问题
```

只有这样，后面才能优化。

---

# 十一、推荐最终决策

你现在应该采用：

```text
先分化，但只做 v1.0 粗分化。
先跑数据，但不能没有标准地跑。
```

具体执行：

```text
1. 先定 8 类钱包角色
2. 先定 BLOCK / PAUSE / SUPPORT / NEUTRAL 四种门禁状态
3. 先定几个保守硬规则
4. 跑 10 个 token 检查字段完整性
5. 跑 30 个 token 校准阈值
6. 跑 100 个 token 再扩展角色分类
```

---

# 十二、直接结论

你的问题答案是：

> **要分化，但先做低复杂度分化；不要等跑完数据才定标准，也不要一开始做终极标准。**

现在最佳路线：

```text
v1.0：粗分类 + 硬规则 + 全字段保存
v1.1：根据 30 个 token 调整阈值
v1.2：根据 100 个 token 增加细角色
v2.0：接入历史地址库和跨币复现
```

---

# 本次认知升级点

这一步的核心认知是：

> 钱包结构标准不是一次性写死的，而是先用方法论给出最小判断框架，再用真实 token 样本反向校准。

你现在要做的不是“完美分类器”，而是：

```text
可运行
可记录
可复盘
可校准
```

---

# 尚未解决问题

下一步需要继续定稿：

```text
1. v1.0 的 8 类钱包角色具体 classify(w) 判断规则
2. wallet_structure_score 初始计算公式
3. wallet_risk_score 初始计算公式
4. data_quality_score 如何计算
5. 第一次 10 个 token 跑完后用什么复盘模板校准标准
```


---

## 片段 55 / stream_idx=8455 / len=14856


# SIKK 钱包结构门禁层 v1.0：下一步执行规范

你的判断是正确的。  
当前系统虽然已经有 `sikk-gmgn-structural-intelligence skill` 和 `sikk_gmgn_token_report.py`，但它们还只是**报告层 / 分析层**，没有真正变成自动交易系统的**决策门禁层**。

下一步不应该继续扩展更多概念，而应该先做：

> **v1.0 钱包结构门禁层：把钱包结构证据转成状态机和纸面交易 runner 可读取的标准判断。**

---

# 一、v1.0 的核心目标

## 当前问题

现在系统主要依赖：

```text
候选发现
K线信号
quote
安全扫描
纸面 runner
```

钱包结构只用了轻量指标，例如：

```text
早期钱包清仓比例
Top Holder 简单状态
```

但还没有正式使用：

```text
新钱包狙击
临时执行钱包
同源执行组
Token 接收钱包
分发派发钱包
结果钱包
高结果鲸鱼
接盘鲸鱼
套牢钱包
可疑中转节点
核心资金源
```

所以系统现在还是：

```text
量价 + quote 纸面交易系统
```

v1.0 的目标是升级成：

```text
量价信号 + 钱包结构门禁 + quote 安全层 + 纸面验证系统
```

---

# 二、v1.0 不做什么

这一点要明确，否则会做得太重。

## v1.0 暂时不做

```text
完整历史地址画像库
跨币老庄画像
长期地址复现评分
复杂资金路径全链路追踪
自动实盘
自动卖出
自动调参
```

## v1.0 只做一件事

```text
当前候选 token 的钱包结构是否支持进入 PAPER_READY。
```

也就是判断：

```text
这个 token 当前能不能进入纸面交易候选？
```

---

# 三、推荐新增文件结构

```text
sikk/
  wallet_structure/
    sikk_wallet_structure_gate.py
    sikk_candidate_wallet_structure_pipeline.py

tests/
  test_sikk_wallet_structure_gate.py
  test_sikk_candidate_wallet_structure_pipeline.py
```

如果你现在项目还没有 `wallet_structure/` 子目录，也可以先放在根目录：

```text
sikk_wallet_structure_gate.py
sikk_candidate_wallet_structure_pipeline.py
tests/test_sikk_wallet_structure_gate.py
tests/test_sikk_candidate_wallet_structure_pipeline.py
```

---

# 四、输出目录标准

```text
data/gmgn_candidates_live_run/wallet_structure/
```

目录结构：

```text
wallet_structure/
  candidate_wallet_structure_summary.json
  candidate_wallet_structure_summary.csv
  candidate_wallet_structure_summary.md

  <token_address>/
    early_wallet_raw.csv
    wallet_classification.csv
    candidate_groups.csv
    gmgn_note_table.csv
    wallet_structure_decision.json
```

---

# 五、整体数据流

```text
GMGN 候选 token
  ↓
sikk_candidate_wallet_structure_pipeline.py
  ↓
读取 / 生成单币钱包结构报告
  ↓
classify(w) 钱包角色分类
  ↓
聚合钱包结构证据
  ↓
sikk_wallet_structure_gate.py
  ↓
生成 wallet_structure_decision.json
  ↓
状态机读取
  ↓
WALLET_BLOCK / WALLET_PAUSE / WALLET_SUPPORT
  ↓
纸面 runner 写入 wallet_structure_factor
```

---

# 六、核心文件职责

## 1. `sikk_candidate_wallet_structure_pipeline.py`

它是候选 token 的钱包结构流水线。

### 负责：

```text
读取候选 token 列表
逐个 token 调用钱包结构分析
保存 early_wallet_raw.csv
保存 wallet_classification.csv
保存 candidate_groups.csv
保存 gmgn_note_table.csv
调用 sikk_wallet_structure_gate.py
生成 wallet_structure_decision.json
汇总生成 candidate_wallet_structure_summary.json/csv/md
```

### 输入：

```text
data/gmgn_candidates_live_run/candidates.json
data/gmgn_candidates_live_run/signals.json
GMGN wallet / holder / top trader 数据
```

### 输出：

```text
data/gmgn_candidates_live_run/wallet_structure/
```

---

## 2. `sikk_wallet_structure_gate.py`

它是核心门禁判断模块。

### 负责：

```text
接收钱包分类汇总结果
计算 wallet_structure_score
计算 wallet_risk_score
生成 wallet_structure_status
生成 wallet_structure_factor
输出状态机动作
```

### 输出动作：

```text
WALLET_BLOCK
WALLET_PAUSE
WALLET_SUPPORT
WALLET_NEUTRAL
```

---

## 3. `tests/test_sikk_wallet_structure_gate.py`

测试门禁逻辑是否稳定。

必须测试：

```text
早期钱包集中清仓 → WALLET_BLOCK
同源组同步卖出 → WALLET_BLOCK
分发钱包明显增加 → WALLET_BLOCK
高结果钱包仍持有 → WALLET_SUPPORT
早期钱包部分持有但风险不高 → WALLET_NEUTRAL / WALLET_SUPPORT
数据不足 → WALLET_PAUSE
```

---

## 4. `tests/test_sikk_candidate_wallet_structure_pipeline.py`

测试流水线是否能稳定生成文件。

必须测试：

```text
能读取候选 token
能生成 token 子目录
能生成 wallet_classification.csv
能生成 wallet_structure_decision.json
能生成 summary.json/csv/md
```

---

# 七、钱包角色分类 v1.0 标准

v1.0 不需要一次性做完整画像，但必须先有标准角色集合。

## 钱包角色枚举

```text
EARLY_SNIPER              新钱包狙击
TEMP_EXECUTOR             临时执行钱包
SAME_SOURCE_EXECUTOR      同源执行钱包
TOKEN_RECEIVER            Token 接收钱包
DISTRIBUTION_SELLER       分发派发钱包
PROFIT_WALLET             结果钱包
HIGH_RESULT_WHALE         高结果鲸鱼
BAGHOLDER_WHALE           套牢鲸鱼
EXIT_LIQUIDATOR           清仓出货钱包
SUSPICIOUS_TRANSFER_NODE  可疑中转节点
CORE_FUNDING_SOURCE       疑似核心资金源
RETAIL_NOISE              普通噪音钱包
UNKNOWN                   未知
```

---

# 八、钱包分类字段标准

`wallet_classification.csv` 建议字段：

```text
token_address
wallet_address
wallet_role
role_confidence
token_source
funding_source
entry_time
entry_rank
buy_amount_usd
sell_amount_usd
net_buy_usd
holding_pct
sold_pct
remaining_pct
roi_pct
pnl_usd
trade_count
buy_count
sell_count
is_new_wallet
is_top_holder
is_top_trader
same_source_group_id
distribution_risk
evidence_level
risk_level
gmgn_note
reason
```

---

# 九、候选结构组字段标准

`candidate_groups.csv` 建议字段：

```text
token_address
group_id
group_type
wallet_count
total_buy_usd
total_remaining_pct
total_sold_pct
avg_entry_rank
avg_roi_pct
sync_buy_score
sync_sell_score
funding_similarity_score
behavior_similarity_score
group_risk_level
group_evidence_level
reason
```

---

# 十、GMGN 备注表字段

`gmgn_note_table.csv` 建议字段：

```text
token_address
wallet_address
gmgn_name
gmgn_emoji
gmgn_note
wallet_role
evidence_level
risk_level
action
```

备注格式继续沿用你的证据化格式：

```text
$TOKEN@D1｜早入｜重仓+低频｜高ROI+部分退｜CL_xxx｜E2
```

注意：  
不要写死“庄”“老鼠仓”这类裁决词。继续使用：

```text
疑似早期执行
疑似同源组
疑似分发
疑似接盘
疑似结果钱包
```

---

# 十一、门禁决策文件标准

每个 token 必须生成：

```text
wallet_structure_decision.json
```

建议结构：

```json
{
  "token_address": "TOKEN_ADDRESS",
  "token_symbol": "TOKEN",
  "wallet_structure_status": "WALLET_SUPPORT",
  "wallet_structure_score": 72,
  "wallet_risk_score": 28,
  "wallet_structure_factor": 1.15,
  "wallet_evidence_level": "E2",
  "decision_action": "ALLOW_PAPER_READY",
  "reason": "早期钱包仍有部分持仓，高结果钱包未集中清仓，同源组未出现同步卖出",
  "support_signals": [
    "EARLY_WALLETS_PARTIAL_HOLDING",
    "HIGH_RESULT_WALLETS_STILL_HOLDING",
    "NO_SYNC_EXIT_DETECTED"
  ],
  "risk_signals": [
    "TOP_TRADER_PARTIAL_SELL"
  ],
  "metrics": {
    "early_wallet_count": 18,
    "early_wallet_remaining_pct": 42.5,
    "early_wallet_sold_pct": 57.5,
    "same_source_group_count": 2,
    "same_source_sync_sell_score": 18,
    "distribution_wallet_count": 1,
    "high_result_wallet_count": 3,
    "high_result_remaining_pct": 36.2,
    "bagholder_whale_count": 0,
    "top_holder_exit_pressure": "LOW"
  },
  "created_at": "2026-05-02T00:00:00Z"
}
```

---

# 十二、门禁状态定义

## 1. WALLET_BLOCK

含义：

```text
钱包结构明确不支持入场。
```

触发条件：

```text
早期钱包集中清仓
同源组同步卖出
分发派发钱包明显增加
高结果钱包全部退出
Top Holder 大比例出货
接盘鲸鱼明显被砸穿
核心执行组撤退
```

状态机动作：

```text
WALLET_BLOCK → BLOCKED
```

---

## 2. WALLET_PAUSE

含义：

```text
钱包结构信息不够清晰，或者风险偏高，需要继续观察。
```

触发条件：

```text
数据不足
早期钱包卖出偏多但未完全清仓
Top Trader 出现反向行为
接盘鲸鱼出现但承接不稳定
同源组行为不明
quote 与钱包行为冲突
```

状态机动作：

```text
WALLET_PAUSE → WATCHING / PAUSE
```

---

## 3. WALLET_SUPPORT

含义：

```text
钱包结构支持进入纸面交易。
```

触发条件：

```text
早期钱包仍有持仓
高结果钱包未集中退出
同源组没有同步卖出
分发风险低
接盘结构稳定
K线信号与钱包结构一致
```

状态机动作：

```text
WALLET_SUPPORT → 允许 PAPER_READY
```

---

## 4. WALLET_NEUTRAL

含义：

```text
钱包结构没有明显支持，也没有明显阻断。
```

状态机动作：

```text
WALLET_NEUTRAL → 不加分，不阻断，交给其他门禁继续判断
```

---

# 十三、评分模型 v1.0

## 结构支持分：`wallet_structure_score`

满分 100。

建议组成：

| 维度 | 分数 |
|---|---:|
| 早期钱包仍持有 | 0 - 25 |
| 高结果钱包仍持有 | 0 - 20 |
| 同源组未同步卖出 | 0 - 15 |
| 分发风险低 | 0 - 15 |
| 接盘鲸鱼承接稳定 | 0 - 10 |
| Top Trader 未反向 | 0 - 10 |
| GMGN/K线/钱包行为一致 | 0 - 5 |

---

## 钱包风险分：`wallet_risk_score`

满分 100。

建议组成：

| 风险项 | 分数 |
|---|---:|
| 早期钱包集中清仓 | 0 - 30 |
| 同源组同步卖出 | 0 - 25 |
| 分发钱包增加 | 0 - 15 |
| 高结果钱包退出 | 0 - 10 |
| Top Holder 出货 | 0 - 10 |
| 套牢鲸鱼上方压制 | 0 - 5 |
| 数据不足 | 0 - 5 |

---

# 十四、门禁规则

建议第一版用硬规则，不要一开始就用复杂机器学习。

```text
if wallet_risk_score >= 75:
    WALLET_BLOCK

elif same_source_sync_sell_score >= 70:
    WALLET_BLOCK

elif early_wallet_sold_pct >= 85 and high_result_remaining_pct <= 10:
    WALLET_BLOCK

elif distribution_wallet_count >= 3 and early_wallet_remaining_pct <= 20:
    WALLET_BLOCK

elif wallet_risk_score >= 50:
    WALLET_PAUSE

elif data_quality_score < 50:
    WALLET_PAUSE

elif wallet_structure_score >= 65 and wallet_risk_score <= 40:
    WALLET_SUPPORT

else:
    WALLET_NEUTRAL
```

---

# 十五、`wallet_structure_factor` 建议

这个字段用于纸面 runner，不建议直接决定买卖，而是作为仓位/优先级修正因子。

| 状态 | factor | 含义 |
|---|---:|---|
| WALLET_BLOCK | 0.00 | 禁止进入 |
| WALLET_PAUSE | 0.30 | 不主动入场，只观察 |
| WALLET_NEUTRAL | 1.00 | 不加不减 |
| WALLET_SUPPORT | 1.10 - 1.25 | 结构支持，提高优先级 |

建议第一版：

```text
WALLET_BLOCK   → 0.00
WALLET_PAUSE   → 0.30
WALLET_NEUTRAL → 1.00
WALLET_SUPPORT → 1.15
```

---

# 十六、状态机接入逻辑

状态机读取：

```text
wallet_structure_decision.json
```

伪代码：

```python
if wallet_decision.wallet_structure_status == "WALLET_BLOCK":
    state = "BLOCKED"
    block_reason = wallet_decision.reason

elif wallet_decision.wallet_structure_status == "WALLET_PAUSE":
    state = "PAUSE"
    pause_reason = wallet_decision.reason

elif wallet_decision.wallet_structure_status == "WALLET_SUPPORT":
    if signal_gate == "ALLOW" and quote_gate == "ALLOW" and security_gate == "ALLOW":
        state = "PAPER_READY"
    else:
        state = "WATCHING"

elif wallet_decision.wallet_structure_status == "WALLET_NEUTRAL":
    continue_with_existing_gates()
```

---

# 十七、纸面 runner 接入字段

每个纸面仓位增加：

```text
wallet_structure_status
wallet_structure_score
wallet_risk_score
wallet_structure_factor
wallet_structure_reason
wallet_evidence_level
```

`paper_positions` 表增加：

```text
wallet_structure_status TEXT
wallet_structure_score REAL
wallet_risk_score REAL
wallet_structure_factor REAL
wallet_structure_reason TEXT
wallet_evidence_level TEXT
```

日报新增统计：

```text
WALLET_SUPPORT 交易数量
WALLET_NEUTRAL 交易数量
WALLET_PAUSE 拦截数量
WALLET_BLOCK 拦截数量
不同 wallet_structure_status 的胜率
不同 wallet_structure_status 的平均收益
wallet_structure_factor 对收益的影响
```

---

# 十八、v1.0 验收标准

这一步完成后，系统必须能做到：

```text
1. 每个候选 token 都生成 wallet_structure_decision.json
2. 状态机能读取 wallet_structure_decision.json
3. WALLET_BLOCK 能阻止 PAPER_READY
4. WALLET_PAUSE 能进入观察或暂停
5. WALLET_SUPPORT 能允许进入 PAPER_READY
6. paper runner 能记录 wallet_structure_factor
7. daily report 能统计钱包结构状态下的收益表现
8. tests 能覆盖 BLOCK / PAUSE / SUPPORT / NEUTRAL 四种情况
```

---

# 十九、直接发给 AI / Codex / OpenClaw 的任务提示词

```text
任务：实现 SIKK-SOL v1.0 钱包结构门禁层。

当前已有：
1. sikk-gmgn-structural-intelligence skill
2. sikk_gmgn_token_report.py 单币钱包结构报告
3. classify(w) 钱包角色分类雏形

当前缺失：
1. sikk_wallet_structure_gate.py
2. sikk_candidate_wallet_structure_pipeline.py
3. tests/test_sikk_wallet_structure_gate.py
4. tests/test_sikk_candidate_wallet_structure_pipeline.py
5. 状态机接入 wallet_structure_decision.json
6. 纸面 runner 接入 wallet_structure_factor

目标：
把钱包结构角色分析正式接入自动交易系统，让系统从“量价 + quote 纸面交易系统”升级为“SIKK 钱包结构智能纸面交易系统”。

一、请新增 sikk_wallet_structure_gate.py

要求：
1. 定义钱包结构状态：
   - WALLET_BLOCK
   - WALLET_PAUSE
   - WALLET_SUPPORT
   - WALLET_NEUTRAL

2. 输入钱包结构汇总指标，包括：
   - early_wallet_count
   - early_wallet_remaining_pct
   - early_wallet_sold_pct
   - same_source_group_count
   - same_source_sync_sell_score
   - distribution_wallet_count
   - high_result_wallet_count
   - high_result_remaining_pct
   - bagholder_whale_count
   - top_holder_exit_pressure
   - data_quality_score

3. 输出：
   - wallet_structure_status
   - wallet_structure_score
   - wallet_risk_score
   - wallet_structure_factor
   - wallet_evidence_level
   - decision_action
   - reason
   - support_signals
   - risk_signals
   - metrics

4. 门禁规则：
   - wallet_risk_score >= 75 → WALLET_BLOCK
   - same_source_sync_sell_score >= 70 → WALLET_BLOCK
   - early_wallet_sold_pct >= 85 且 high_result_remaining_pct <= 10 → WALLET_BLOCK
   - distribution_wallet_count >= 3 且 early_wallet_remaining_pct <= 20 → WALLET_BLOCK
   - wallet_risk_score >= 50 → WALLET_PAUSE
   - data_quality_score < 50 → WALLET_PAUSE
   - wallet_structure_score >= 65 且 wallet_risk_score <= 40 → WALLET_SUPPORT
   - 其他 → WALLET_NEUTRAL

5. wallet_structure_factor：
   - WALLET_BLOCK → 0.00
   - WALLET_PAUSE → 0.30
   - WALLET_NEUTRAL → 1.00
   - WALLET_SUPPORT → 1.15

二、请新增 sikk_candidate_wallet_structure_pipeline.py

要求：
1. 读取候选 token 列表
2. 对每个 token 调用已有 sikk_gmgn_token_report.py 或相关函数
3. 生成以下文件：

data/gmgn_candidates_live_run/wallet_structure/
  candidate_wallet_structure_summary.json
  candidate_wallet_structure_summary.csv
  candidate_wallet_structure_summary.md

每个 token 子目录：
  <token>/early_wallet_raw.csv
  <token>/wallet_classification.csv
  <token>/candidate_groups.csv
  <token>/gmgn_note_table.csv
  <token>/wallet_structure_decision.json

三、钱包角色分类标准

wallet_classification.csv 至少包含：
- token_address
- wallet_address
- wallet_role
- role_confidence
- token_source
- funding_source
- entry_time
- entry_rank
- buy_amount_usd
- sell_amount_usd
- net_buy_usd
- holding_pct
- sold_pct
- remaining_pct
- roi_pct
- pnl_usd
- trade_count
- buy_count
- sell_count
- is_new_wallet
- is_top_holder
- is_top_trader
- same_source_group_id
- distribution_risk
- evidence_level
- risk_level
- gmgn_note
- reason

wallet_role 使用以下枚举：
- EARLY_SNIPER
- TEMP_EXECUTOR
- SAME_SOURCE_EXECUTOR
- TOKEN_RECEIVER
- DISTRIBUTION_SELLER
- PROFIT_WALLET
- HIGH_RESULT_WHALE
- BAGHOLDER_WHALE
- EXIT_LIQUIDATOR
- SUSPICIOUS_TRANSFER_NODE
- CORE_FUNDING_SOURCE
- RETAIL_NOISE
- UNKNOWN

四、状态机接入

状态机读取：

data/gmgn_candidates_live_run/wallet_structure/<token>/wallet_structure_decision.json

接入规则：
- WALLET_BLOCK → BLOCKED
- WALLET_PAUSE → PAUSE 或 WATCHING
- WALLET_SUPPORT → 如果 signal_gate、quote_gate、security_gate 均通过，则允许 PAPER_READY
- WALLET_NEUTRAL → 不加分、不阻断，继续走现有门禁

五、纸面 runner 接入

paper_positions 增加字段：
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- wallet_structure_factor
- wallet_structure_reason
- wallet_evidence_level

要求：
1. 每笔 paper position 必须记录钱包结构状态
2. daily report 必须统计不同 wallet_structure_status 下的收益表现
3. WALLET_BLOCK 不允许进入 paper position
4. WALLET_PAUSE 不主动开仓，只进入观察或暂停
5. WALLET_SUPPORT 可以提高候选优先级，但不能绕过 quote/security gate

六、测试

新增 tests/test_sikk_wallet_structure_gate.py，覆盖：
1. 早期钱包集中清仓 → WALLET_BLOCK
2. 同源组同步卖出 → WALLET_BLOCK
3. 分发钱包明显增加 → WALLET_BLOCK
4. 高结果钱包仍持有且风险低 → WALLET_SUPPORT
5. 数据不足 → WALLET_PAUSE
6. 中性结构 → WALLET_NEUTRAL

新增 tests/test_sikk_candidate_wallet_structure_pipeline.py，覆盖：
1. 能读取候选 token
2. 能生成 token 子目录
3. 能生成 wallet_classification.csv
4. 能生成 wallet_structure_decision.json
5. 能生成 candidate_wallet_structure_summary.json/csv/md

七、限制

当前阶段仍然禁止自动实盘。
钱包结构门禁只允许影响：
1. BLOCKED
2. PAUSE/WATCHING
3. PAPER_READY
4. paper runner 记录与统计

不得直接 broadcast 真实交易。
```

---

# 二十、当前最优开发顺序

按这个顺序做：

```text
1. sikk_wallet_structure_gate.py
2. tests/test_sikk_wallet_structure_gate.py
3. sikk_candidate_wallet_structure_pipeline.py
4. tests/test_sikk_candidate_wallet_structure_pipeline.py
5. 生成 wallet_structure_decision.json
6. 状态机读取 wallet_structure_decision.json
7. paper runner 写入 wallet_structure_factor
8. daily report 增加钱包结构统计
```

不要反过来先接状态机。  
因为状态机需要一个稳定的 `wallet_structure_decision.json` 合约。

---

# 本次认知升级点

这一步的关键不是“再分析钱包”，而是：

> 把钱包结构分析从报告层，推进到交易系统的门禁层。

也就是让系统具备这样的能力：

```text
不是因为 K线好看就入场，
而是因为 K线信号、quote、安全层、钱包结构同时没有冲突，才允许进入 PAPER_READY。
```

这才是 SIKK 和普通量价策略的分界线。

---

# 尚未解决问题

下一步还需要继续细化：

```text
1. classify(w) 的具体角色判定阈值
2. same_source_group_id 的生成逻辑
3. distribution_wallet_count 的识别标准
4. high_result_wallet 的定义
5. wallet_structure_score 的实际字段映射
6. wallet_structure_decision.json 与现有状态机文件的具体接点
7. paper runner 中 wallet_structure_factor 是否影响仓位大小，还是只做统计
```


---

## 片段 56 / stream_idx=8581 / len=1413


sikk-gmgn-structural-intelligence skill
sikk_gmgn_token_report.py 单币钱包结构报告
classify(w) 钱包角色分类雏形

还缺：

candidate_wallet_structure_pipeline.py
wallet_structure_gate.py
tests/test_sikk_wallet_structure_gate.py
状态机接入
纸面 runner 接入 wallet_structure_factor

---

九、我建议下一步优先做这个

我建议下一步直接做：

v1.0 钱包结构门禁层

目标：

把你这套“疑似结构钱包/ 早期执行钱包/ 分发派发/ 接盘鲸鱼”的skill，正式变成自动交易系统的判断标准。

具体新增文件

sikk_wallet_structure_gate.py
sikk_candidate_wallet_structure_pipeline.py
tests/test_sikk_wallet_structure_gate.py
tests/test_sikk_candidate_wallet_structure_pipeline.py

输出目录

data/gmgn_candidates_live_run/wallet_structure/

里面生成：

candidate_wallet_structure_summary.json
candidate_wallet_structure_summary.csv
candidate_wallet_structure_summary.md
<token>/early_wallet_raw.csv
<token>/wallet_classification.csv
<token>/candidate_groups.csv
<token>/gmgn_note_table.csv
<token>/wallet_structure_decision.json

状态机新增输入

状态机需要读取：

wallet_structure_decision.json

然后：

WALLET_BLOCK → BLOCKED
WALLET_PAUSE → WATCHING / PAUSE
WALLET_SUPPORT → 允许 PAPER_READY

纸面交易新增字段

每个纸面仓位增加：

wallet_structure_status
wallet_structure_score
wallet_risk_score
wallet_structure_factor
wallet_structure_reason

---

十、简短结论

你说得对。

目前还没有把之前创建的钱包结构角色skill 完整接入自动交易系统。

现在只用了轻量摘要指标，例如早期钱包清仓比例，但没有正式使用：

新钱包狙击
临时执行钱包
同源执行组
Token 接收钱包
分发派发钱包
结果钱包
高结果鲸鱼
接盘鲸鱼
套牢钱包
可疑中转节点
核心资金源

这正是下一阶段最重要的优化。

如果接入这层，系统才真正从：

量价 + quote 纸面交易系统

升级为：

SIKK 钱包结构智能自动交易系统

也就是你最初想做的核心方向。 (2/2)


---

## 片段 57 / stream_idx=8700 / len=11889


下面这段可以定稿为：

# SIKK-SOL 纸面交易验证层升级规范 v1.0  
**定位：阶段 A → 阶段 B 准备层**  
即：从 `paper only` 进入 `paper + human confirmation ticket`，但仍然不开放自动实盘。

---

## 一、当前阶段判断

你的系统现在已经不是“策略构想阶段”，而是：

> **可运行的纸面自动交易验证阶段**

但它还没有达到“小仓实盘自动化”的成熟度。  
当前最关键的问题不是信号有没有，而是：

1. **入场价是否真实**
2. **交易成本是否真实**
3. **是否能连续运行**
4. **失败样本能否归因**
5. **钱包结构证据是否真正参与决策**
6. **quote / K线 / GMGN / OKX 是否一致**
7. **是否有足够样本支撑进入实盘**

所以现在系统核心任务应该改成：

> 用连续纸面交易验证 SIKK 信号是否在真实实时条件下仍然有效。

---

# 二、升级优先级

## P0：必须先做

### 1. 实时入场价模式

新增参数：

```bash
--entry-price-mode signal
--entry-price-mode live
```

含义：

| 模式 | 用途 | 入场价来源 | 是否接近实盘 |
|---|---|---|---|
| signal | 理论策略验证 | 信号出现时的历史价格 | 否 |
| live | 实时纸面模拟 | 当前 OKX / GMGN quote | 是 |

默认值：

```bash
--entry-price-mode live
```

纸面交易报告里必须同时保留：

```text
signal_entry_price
live_entry_price
signal_pnl_pct
live_pnl_pct
entry_price_diff_pct
```

这样才能判断：

> 策略是实时可执行，还是只在历史信号价上看起来有效。

---

### 2. 交易成本模型

新增配置：

```python
meme_default_buy_slippage_pct = 3
meme_default_sell_slippage_pct = 3
priority_fee_sol = 0.0005
failed_tx_cost_sol = 0.0002
dex_fee_pct = 0.25
quote_deviation_buffer_pct = 1
```

纸面入场成本计算：

```text
paper_buy_price = live_quote_price * (1 + buy_slippage_pct + dex_fee_pct + quote_deviation_buffer_pct)
```

纸面卖出成本计算：

```text
paper_sell_price = live_quote_price * (1 - sell_slippage_pct - dex_fee_pct - quote_deviation_buffer_pct)
```

如果交易失败：

```text
position_pnl -= failed_tx_cost_sol
```

这一步非常重要。  
否则 meme token 的纸面收益会被明显高估。

---

### 3. 连续运行调度器

建议先做最小可用调度：

| 模块 | 频率 | 作用 |
|---|---:|---|
| 候选发现 + 信号扫描 | 每 10 分钟 | 找新机会 |
| quote/security 更新 | 每 5 分钟 | 判断是否可入场 |
| paper_live 持仓更新 | 每 3 分钟 | 更新浮盈、止损、止盈 |
| 日报生成 | 每天 UTC 0 点 | 输出统计结果 |

第一版不需要复杂后台服务，可以先用：

```bash
cron
```

或 Python scheduler：

```python
APScheduler
```

目标不是优雅，而是先拿到连续样本。

---

### 4. 风控熔断变量

你前面列的这些必须进入配置文件：

```python
daily_max_loss_sol = 0.05
daily_max_failed_trades = 5
max_consecutive_failures = 3
one_token_one_live_trade = True
```

触发规则：

```text
consecutive_failures >= 3 → STOP_TRADING_FOR_DAY
daily_loss_sol >= daily_max_loss_sol → STOP_TRADING_FOR_DAY
daily_failed_trades >= daily_max_failed_trades → STOP_TRADING_FOR_DAY
same_token_live_trade_exists = True → BLOCK_REENTRY
```

这里要注意：

> 单 token 只允许一笔实盘，但纸面交易可以保留多信号记录，用来评估信号质量。

也就是说：

```text
paper_signal_record：可以多次
paper_trade_position：限制一笔主仓
real_trade_position：严格一笔
```

---

# 三、P1：下一层增强

## 5. SQLite 数据库化

建议创建：

```text
paper_trading.db
```

核心表：

```text
candidates
signals
quotes
security_scans
paper_positions
paper_trades
risk_events
daily_metrics
wallet_evidence
failure_attribution
confirmation_tickets
```

---

## 6. 表结构建议

### candidates

```text
id
token_address
token_symbol
source
market_cap
liquidity
holder_count
pool_address
discovered_at
raw_payload_json
```

---

### signals

```text
id
token_address
signal_level
signal_type
sikk_phase
kline_timeframe
signal_price
signal_time
control_box_high
control_box_low
accumulation_score
structure_score
momentum_score
risk_score
raw_signal_json
```

---

### quotes

```text
id
token_address
source
quote_price
pool_price
kline_close_price
okx_price
gmgn_price
price_deviation_pct
quote_time
quote_status
```

---

### paper_positions

```text
id
token_address
entry_mode
signal_entry_price
live_entry_price
effective_entry_price
position_size_sol
entry_time
current_price
unrealized_pnl_pct
max_floating_profit_pct
max_drawdown_pct
status
exit_reason
created_at
updated_at
```

---

### paper_trades

```text
id
position_id
token_address
side
price
effective_price
slippage_pct
dex_fee_pct
priority_fee_sol
failed_tx_cost_sol
pnl_pct
pnl_sol
trade_time
tx_simulation_status
```

---

### risk_events

```text
id
token_address
event_type
risk_level
reason
trigger_value
threshold_value
action
created_at
```

---

### failure_attribution

```text
id
position_id
token_address
failure_type
primary_reason
secondary_reason
evidence_json
created_at
```

---

### wallet_evidence

```text
id
token_address
wallet_address
wallet_role
token_source
funding_source
holding_duration_type
result_performance
current_behavior
evidence_level
risk_level
action_suggestion
created_at
```

---

# 四、失败样本归因系统

每个关闭仓位都必须有归因。

## 失败类型标准字典

```text
STRUCTURE_FAIL
LIQUIDITY_FAIL
QUOTE_FAIL
SECURITY_FAIL
MOMENTUM_FAIL
WALLET_EXIT
STOP_LOSS
TIME_STOP
REENTRY_BLOCKED
STATE_EXPIRED
EXECUTION_FAIL
```

---

## 归因逻辑

| 失败类型 | 判断依据 |
|---|---|
| STRUCTURE_FAIL | 控盘箱体跌破、吸筹结构失效、无法形成二次推进 |
| LIQUIDITY_FAIL | 池子过浅、滑点过大、quote 无效 |
| QUOTE_FAIL | OKX / GMGN / K线价格偏差过大 |
| SECURITY_FAIL | 安全扫描不通过 |
| MOMENTUM_FAIL | 价格进入后无扩张，量能不足 |
| WALLET_EXIT | 早期钱包集中清仓、同源组同步卖出 |
| STOP_LOSS | 触发止损 |
| TIME_STOP | 超过最大持仓时间仍无进展 |
| STATE_EXPIRED | 信号过期 |
| EXECUTION_FAIL | 模拟成交失败、quote stale、落链失败 |

---

## 每笔失败必须输出

```json
{
  "token": "TOKEN_ADDRESS",
  "position_id": "xxx",
  "failure_type": "WALLET_EXIT",
  "primary_reason": "early_wallets_concentrated_exit",
  "secondary_reason": "momentum_weak_after_entry",
  "evidence": {
    "early_wallet_remaining_pct": 12.5,
    "top_holder_sell_pressure": "high",
    "price_drawdown_pct": -18.7,
    "quote_deviation_pct": 2.1
  }
}
```

---

# 五、钱包结构接入纸面 Runner

这是你系统和普通量价机器人的分水岭。

纸面 runner 入场前不能只看：

```text
K线
信号等级
quote
安全扫描
```

还必须看钱包结构。

---

## 入场前钱包结构检查

新增结构门禁：

```text
wallet_structure_gate
```

检查项：

| 检查项 | 通过条件 | 风险动作 |
|---|---|---|
| 早期钱包剩余筹码 | 未集中清仓 | 否则 PAUSE / BLOCK |
| 高结果钱包状态 | 仍持有或部分持有 | 若全部清仓，降级 |
| 同源组行为 | 未同步卖出 | 同步卖出则 BLOCK |
| Top Trader 行为 | 未明显反向 | 反向则 PAUSE |
| Smart/KOL 参与 | 有参与可加分，但不能单独入场 | 只做辅助证据 |
| 分发接收钱包 | 未出现明显派发 | 出现则 BLOCK |
| 接盘鲸鱼 | 接盘后未继续下杀 | 弱接盘则 PAUSE |

---

## 结构门禁输出

```json
{
  "wallet_structure_gate": "ALLOW",
  "early_wallet_status": "PARTIAL_HOLDING",
  "same_source_group_status": "NO_SYNC_EXIT",
  "top_trader_status": "NEUTRAL",
  "distribution_risk": "LOW",
  "wallet_evidence_level": "E2",
  "action": "ALLOW_PAPER_TRADE"
}
```

---

# 六、多报价源一致性验证

后续不要只信一个 quote source。

## 建议价格源

```text
OKX quote
GMGN quote
GMGN pool price
Kline close price
paper runner output price
```

---

## 偏差判断

```text
price_deviation_pct = abs(max_price - min_price) / median_price * 100
```

规则：

| 偏差 | 状态 |
|---:|---|
| ≤ 2% | ALLOW |
| 2% - 5% | PAUSE_NEED_CONFIRM |
| > 5% | BLOCK_QUOTE_UNRELIABLE |

输出：

```json
{
  "quote_consistency": "PAUSE_NEED_CONFIRM",
  "okx_price": 0.000123,
  "gmgn_price": 0.000119,
  "kline_close_price": 0.000121,
  "price_deviation_pct": 3.31
}
```

---

# 七、状态过期机制

meme token 的状态不能长期有效。

## 状态过期规则

| 状态 | 过期时间 | 过期后动作 |
|---|---:|---|
| PAPER_READY | 15 分钟 | EXPIRED |
| READY_FOR_CONFIRMATION | 10 秒 | QUOTE_STALE |
| WATCHING | 2 小时 | COOLING |
| BLOCKED | 6 小时 | 可重新检查 |
| PAUSE_NEED_CONFIRM | 10 分钟 | 重新 quote |

---

## 状态机补强

```text
WATCHING
  ↓
PAPER_READY
  ↓
READY_FOR_CONFIRMATION
  ↓
PAPER_OPEN
  ↓
PAPER_MANAGING
  ↓
PAPER_CLOSED
```

异常分支：

```text
PAPER_READY → EXPIRED
READY_FOR_CONFIRMATION → QUOTE_STALE
PAPER_OPEN → STOP_LOSS
PAPER_OPEN → TAKE_PROFIT
PAPER_OPEN → TIME_STOP
PAPER_OPEN → WALLET_EXIT
PAPER_OPEN → STRUCTURE_FAIL
```

---

# 八、Replay 模式

实盘前必须做 replay。

## replay 目标

```text
回放过去 24h 候选
按当时信号时间逐分钟重放
模拟实时 quote
模拟滑点
模拟手续费
模拟止损
模拟分批止盈
输出失败归因
```

---

## 进入小仓实盘前最低门槛

```text
至少 100 个纸面样本
至少 20 个关闭仓位
至少连续 3 天日报
live_entry 模式收益仍为正
最大回撤在可接受范围
失败归因 Top 5 清晰
连续失败熔断已验证
quote 偏差保护已验证
```

没有达到这些条件，不开放自动实盘。

---

# 九、真实成交回填字段

即使进入小仓实盘，也必须回填真实成交数据。

## real_execution_backfill

```text
trade_hash
token_address
side
intended_price
actual_fill_price
actual_slippage_pct
actual_fee_sol
priority_fee_sol
landed_success
execution_failed
failure_reason
block_time
confirmation_time
```

---

## 真实成交和纸面成交对比

```text
paper_entry_price
real_entry_price
paper_exit_price
real_exit_price
paper_pnl_pct
real_pnl_pct
execution_gap_pct
```

这会告诉你：

> 纸面系统的收益是否能真实落地。

---

# 十、当前最实际开发顺序

不要一次性全做。建议按这个顺序：

## 第 1 步：live entry price

目标：

```text
纸面入场价改为实时 quote
保留 signal 理论收益和 live 实时收益对比
```

验收标准：

```text
每笔 paper position 同时有 signal_entry_price 与 live_entry_price
日报输出两套收益
```

---

## 第 2 步：交易成本模型

目标：

```text
滑点、手续费、priority fee、失败成本进入纸面收益
```

验收标准：

```text
日报里显示 gross_pnl 与 net_pnl
每笔交易显示 cost_breakdown
```

---

## 第 3 步：定时运行

目标：

```text
系统连续跑 24 小时
自动发现候选
自动更新持仓
自动输出日报
```

验收标准：

```text
24 小时内至少生成：
candidates
signals
paper_positions
paper_trades
daily_report
risk_events
```

---

## 第 4 步：失败归因

目标：

```text
每笔关闭仓位必须有失败/成功归因
```

验收标准：

```text
daily_report 输出 failure_reason_top5
每个 PAPER_CLOSED 仓位都有 attribution
```

---

## 第 5 步：钱包结构接入

目标：

```text
纸面入场前加入 wallet_structure_gate
```

验收标准：

```text
每笔 PAPER_READY 都有 wallet_evidence_level
高风险钱包结构会触发 PAUSE / BLOCK
```

---

# 十一、可以直接发给 AI / OpenClaw / Codex 的任务提示词

下面这段可以直接复制：

```text
你现在负责升级 SIKK-SOL 纸面交易验证层。

当前系统已跑通：
1. 候选发现
2. K线处理
3. SIKK 信号
4. 状态机
5. OKX 只读报价
6. OKX 安全扫描
7. 纸面交易
8. 纸面日报
9. 风险事件记录
10. 真实交易门禁骨架

当前目标不是开放自动实盘，而是把系统从 Phase A：paper only，升级到 Phase B 准备层：paper + human confirmation ticket。

请按以下优先级实现：

P0-1：新增 entry_price_mode
- 支持 signal 与 live 两种模式
- 默认 live
- signal 使用历史信号价
- live 使用当前 OKX / GMGN quote 价格
- 每笔纸面交易同时记录：
  - signal_entry_price
  - live_entry_price
  - effective_entry_price
  - signal_pnl_pct
  - live_pnl_pct
  - entry_price_diff_pct

P0-2：加入交易成本模型
默认参数：
- buy_slippage_pct = 3
- sell_slippage_pct = 3
- dex_fee_pct = 0.25
- priority_fee_sol = 0.0005
- failed_tx_cost_sol = 0.0002
- quote_deviation_buffer_pct = 1

要求：
- 输出 gross_pnl 与 net_pnl
- 每笔交易输出 cost_breakdown
- 失败交易扣除 failed_tx_cost_sol

P0-3：加入风控熔断
新增参数：
- daily_max_loss_sol
- daily_max_failed_trades
- max_consecutive_failures = 3
- one_token_one_live_trade = true

触发规则：
- consecutive_failures >= 3 → STOP_TRADING_FOR_DAY
- daily_loss_sol >= daily_max_loss_sol → STOP_TRADING_FOR_DAY
- daily_failed_trades >= daily_max_failed_trades → STOP_TRADING_FOR_DAY
- 同一个 token 已有实盘仓位 → BLOCK_REENTRY

P0-4：加入连续定时运行
建议频率：
- 候选发现 + 信号扫描：每 10 分钟
- quote/security 更新：每 5 分钟
- paper_live 持仓更新：每 3 分钟
- 日报生成：每天 UTC 0 点

P1-1：数据库化
创建 SQLite 数据库 paper_trading.db，至少包含：
- candidates
- signals
- quotes
- security_scans
- paper_positions
- paper_trades
- risk_events
- daily_metrics
- failure_attribution
- wallet_evidence
- confirmation_tickets

P1-2：失败样本归因
每笔关闭仓位必须自动归因，类型包括：
- STRUCTURE_FAIL
- LIQUIDITY_FAIL
- QUOTE_FAIL
- SECURITY_FAIL
- MOMENTUM_FAIL
- WALLET_EXIT
- STOP_LOSS
- TIME_STOP
- REENTRY_BLOCKED
- STATE_EXPIRED
- EXECUTION_FAIL

P1-3：钱包结构接入纸面 runner
入场前新增 wallet_structure_gate，检查：
- 早期钱包是否集中清仓
- 高结果钱包是否仍持有
- 同源组是否同步卖出
- Top Trader 是否反向
- Smart/KOL 是否参与
- 是否出现分发接收钱包
- 是否出现接盘鲸鱼但无承接

输出：
- wallet_structure_gate
- early_wallet_status
- same_source_group_status
- top_trader_status
- distribution_risk
- wallet_evidence_level
- action

P1-4：多报价源一致性验证
比较：
- OKX quote
- GMGN quote
- GMGN pool price
- Kline close price
- paper runner output price

偏差规则：
- <= 2%：ALLOW
- 2% - 5%：PAUSE_NEED_CONFIRM
- > 5%：BLOCK_QUOTE_UNRELIABLE

P1-5：状态过期机制
规则：
- PAPER_READY 超过 15 分钟未入场 → EXPIRED
- READY_FOR_CONFIRMATION 超过 10 秒未执行 → QUOTE_STALE
- WATCHING 超过 2 小时无进展 → COOLING
- BLOCKED 冷却 6 小时
- PAUSE_NEED_CONFIRM 超过 10 分钟重新 quote

P2：Replay 模式
实现过去 24h 候选回放：
- 按当时信号逐分钟重放
- 模拟 quote
- 模拟滑点
- 模拟手续费
- 模拟止损
- 模拟分批止盈
- 输出失败归因

进入小仓实盘前必须满足：
- 至少 100 个纸面样本
- 至少 20 个关闭仓位
- 至少连续 3 天日报
- live_entry 模式下收益仍为正
- 最大回撤可接受
- 连续失败熔断已验证
- quote 偏差保护已验证

注意：
当前阶段禁止开放自动实盘。
所有真实交易相关功能只能生成 confirmation ticket，不允许自动 broadcast。
```

---

# 十二、你现在应该先完善的模块

优先级非常明确：

```text
1. live entry price
2. 成本模型
3. 定时连续运行
4. SQLite 纸面交易库
5. 失败归因
6. 钱包结构门禁
7. 多源 quote 偏差判断
8. replay 模式
9. confirmation ticket
10. 极小仓实盘门禁
```

当前不要把精力放在：

```text
自动调参
自动卖出实盘
复杂 AI 预测
多链扩展
完整钱包画像大系统
```

这些可以后置。  
现在最重要的是让系统产生连续、可统计、可归因的纸面样本。

---

# 本次认知升级点

你这次系统的关键升级是：

> 从“信号是否出现”升级到“信号是否能在真实报价、真实成本、连续运行、失败归因条件下仍然成立”。

这一步非常重要。  
因为很多策略在历史信号价上看起来有效，但一进入实时 quote、滑点、手续费、状态过期，就会明显失真。

---

# 尚未解决问题

当前还需要继续拆的部分：

1. **paper runner 的具体代码结构**
2. **SQLite 表的完整字段与索引**
3. **daily report 标准模板**
4. **confirmation ticket 标准格式**
5. **wallet_structure_gate 的评分规则**
6. **replay 模式的数据回放逻辑**
7. **从阶段 B 进入阶段 C 的硬性实盘准入标准**


---

## 片段 58 / stream_idx=8794 / len=3483


daily_max_loss_sol
   daily_max_failed_trades

3. 连续失败熔断
   consecutive_failures >= 3 → stop trading

4. 单token 再入场限制
   一个 token 只允许一笔实盘

5. 真实成交回填
- 交易哈希
- 实际成交价
- 实际滑点
- 实际手续费
- 是否落链成功
- 是否成交失败

---

二、当前系统成熟度评估

我会这样给你打分。

已跑通部分

候选发现：已跑通
K线处理：已跑通
SIKK 信号：已跑通
状态机：已跑通
OKX 只读报价：已跑通
OKX 安全扫描：已跑通
纸面交易：已跑通
纸面日报：已跑通
风险事件记录：已跑通
真实交易门禁：已有骨架

暂未成熟部分

连续定时运行：未启用
多轮纸面统计：刚开始
真实成交模拟精度：需要加强
滑点/手续费模型：需要加强
失败样本归因：需要加强
钱包实体结构识别：未完全接入纸面交易
多报价源偏差判断：需要加强
实盘自动卖出：未开放
自动调参：未开放

---

三、目前最需要优化的10 个方向

优化1：实时纸面入场价，不只用历史信号价

这是最高优先级。

当前高收益结果可能受到“历史信号价入场”的影响。

建议新增两种模式：

--entry-price-mode signal
--entry-price-mode live

含义：

signal：理论策略回测，用信号价
live：实盘纸面模拟，用当前 OKX/GMGN quote 价

推荐默认：

live

这样更接近真实交易。

---

优化2：加入交易成本模型

纸面交易应扣除：

买入滑点
卖出滑点
DEX fee
priority fee
报价偏差
失败成本

建议第一版：

meme_default_buy_slippage_pct = 3
meme_default_sell_slippage_pct = 3
priority_fee_sol = 0.0005
failed_tx_cost_sol = 0.0002

---

优化3：连续定时运行

现在你是手动跑一轮。

下一步应该变成定时任务：

每 10 分钟跑一次候选 + 信号
每 5 分钟更新纸面持仓
每天输出日报

建议节奏：

候选发现：每 10 分钟
PAPER_READY quote/security：每 5 分钟
纸面持仓更新：每 3 分钟
日报：每天 UTC 0 点

---

优化4：纸面交易数据库化

现在输出是JSON/CSV。

后续建议加SQLite：

paper_trading.db

表：

candidates
signals
paper_positions
paper_trades
risk_events
quotes
security_scans
daily_metrics

这样后面才能统计：

7日胜率
不同信号等级收益
不同市值区间收益
不同池子大小收益
不同时间窗口收益
不同风险标签收益

---

优化5：失败样本归因

每个失败纸面交易需要自动归因：

STRUCTURE_FAIL：结构失败
LIQUIDITY_FAIL：流动性失败
QUOTE_FAIL：报价失败
SECURITY_FAIL：安全失败
MOMENTUM_FAIL：动能不足
WALLET_EXIT：早期钱包出货
STOP_LOSS：止损
TIME_STOP：时间止损

这会直接帮助你优化策略，而不是只看盈亏。

---

优化6：钱包结构接入纸面runner

你原本SIKK 的强项是：

早期钱包结构识别
资金来源
同源组
高收益钱包
套牢鲸鱼
分发接收者
临时执行者

但当前纸面runner 更偏价格/ 信号/ quote。

后续应该让纸面入场也考虑：

早期钱包未集中清仓
高结果钱包仍持有
同源组是否同步卖出
Top Trader 是否反向
Smart/KOL 是否参与
是否出现分发卖压

这会让系统从普通量价策略，升级为你设计的“结构智能交易系统”。

---

优化7：多数据源一致性验证

当前本轮quote source 是：

OKX

后续建议：

GMGN + OKX

做这些判断：

OKX price
GMGN price
GMGN pool price
K线 close price
quote output price

如果偏差过大：

PAUSE_NEED_CONFIRM

不要直接纸面入场。

---

优化8：状态过期机制

Meme token 的信号很短。

建议：

PAPER_READY 超过 15 分钟未入场 → EXPIRED
READY_FOR_CONFIRMATION 超过 10 秒未执行 → quote stale
WATCHING 超过 2 小时无进展 → COOLING
BLOCKED 冷却 6 小时

---

优化9：实盘小仓前的replay 模式

在真实放开之前，需要做replay：

拿过去 24h 的候选
按当时信号逐分钟重放
模拟 quote / slippage / exit

这比单轮纸面更可靠。

目标：

至少 100 个纸面样本
至少 20 个关闭仓位
至少连续 3 天日报
再考虑极小仓实盘

---

优化10：交易执行层仍需保持隔离

不要现在就全自动实盘。

应该分阶段：

阶段 A：paper only
阶段 B：paper + human confirmation ticket
阶段 C：0.01 SOL 手动确认实盘
阶段 D：0.01 SOL 半自动实盘
阶段 E：小仓自动，但有熔断

当前你处在：

阶段 A → 阶段 B 的准备阶段

---

四、当前系统一张图

GMGN 新币池
  ↓
V1 候选过滤
  ↓
K线采集 1m/5m
  ↓
SIKK 吸筹窗口 / 控盘箱体
  ↓
SIKK 信号引擎
  ├─ S0/S1/S2 → WATCHING
  ├─ S3/S4 → 进入风险门禁
  └─ SX → BLOCKED
  ↓
风险门禁
  ├─ BLOCK_BUY → BLOCKED
  ├─ PAUSE_NEED_CONFIRM → PAUSE
  └─ ALLOW_PAPER_TRADE → PAPER_READY
  ↓
OKX / GMGN 只读报价安全层
  ├─ 无报价 / 高风险 → BLOCK / PAUSE
  └─ 报价安全通过 → READY_FOR_CONFIRMATION
  ↓
纸面交易 Runner
  ├─ 模拟入场
  ├─ 模拟持仓
  ├─ 模拟止损
  ├─ 模拟分批止盈
  └─ 生成日报 / 指标 / 风险事件
  ↓
未来实盘门禁
  ├─ confirmation ticket
  ├─ execution gate
  ├─ broadcast guard
  └─ 手动确认后才可进入小仓实盘

---

五、当前最实际的下一步

我建议下一步不是马上实盘，而是做这3 件事。

第一步：把纸面交易改成定时跑

建议：

每 10 分钟跑完整 pipeline
每 3-5 分钟更新 paper_live

这样24 小时后你就有第一批连续数据。

---

第二步：增加live entry price 模式

让纸面入场更接近实盘：

纸面入场价 = 当前 OKX quote / market price
而不是历史信号价

保留两个指标：

理论信号收益
实时纸面收益

这样你能看出：

策略是否真的能在实时运行中抓到，而不是事后看起来很好

---

第三步：做策略评估面板

每天输出：

候选数
PAPER_READY 数
实际纸面入场数
关闭仓位数
胜率
平均收益
最大回撤
最大浮盈
失败原因 Top 5
最佳信号类型
最差信号类型

这才是判断能否进入实盘的关键。

---

六、简短结论

现在系统已经不是“概念阶段”了。

它已经进入：

可运行的纸面自动交易验证阶段

当前最需要优化的是：

1. 纸面入场价改成实时价格模式
2. 加入滑点/ 手续费/ 失败成本
3. 开启定时连续运行
4. 强化失败样本归因
5. 把钱包结构证据接入纸面入场决策(3/4)
