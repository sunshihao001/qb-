# ChatGPT Share 69f75c79 关键摘录（已过滤 UI / 无密钥）

标题：Branch · Branch · Branch · Branch · Branch · 纸面交易优化方案


## 1. SIKK Case File 数据补全与证据链回填系统

来源路径：`[571]`；长度：20815


对，这说明现在 **Case File 已经能生成页面，但只是“外壳成型”，数据证据链还没有补齐**。

你这个链接里的仓位：

```text
paper-ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1-2026-05-03T10_09_28Z.html
```

应该被当成一个正式验收样本。  
现在要让 Hermes 做的不是“把页面美化一下”，而是建立：

```text
SIKK Case File 数据补全与证据链回填系统
```

下面是可以直接复制到 Hermes 的完整任务书。

---

```text
任务名称：
SIKK Case File 数据补全与证据链回填系统 v1.0

项目目录：
/root/sikk-gmgn

当前问题：
当前 Case File 页面已经可以打开，例如：

http://96.126.130.99:8765/case_files/paper-ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1-2026-05-03T10_09_28Z.html

但页面里大量关键字段仍然显示：
- 待补
- UNKNOWN
- DATA_INSUFFICIENT
- 证据不足
- 未接入
- 空字段

这说明当前 Case File 只是生成了结构，但没有完整回填：
1. 发现阶段数据
2. 信号阶段数据
3. 市值路径
4. 钱包结构
5. quote/security
6. 入场证据
7. 持仓 journal
8. 当前/退出数据
9. 自动复盘
10. 策略调整建议
11. 字段来源追踪

目标：
建立 Case File 数据补全系统，使每一个 paper case 不只是 HTML 页面，而是完整的策略实战证据档案。

核心验收样本：
paper-ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1-2026-05-03T10_09_28Z

最终目标：
打开对应 Case File 后，必须能看到：
- 代币当前市值
- 发现时间
- 发现市值
- 信号时间
- 信号市值
- 入场时间
- 入场价格
- 入场市值
- 买入 SOL 数量
- 估算 token 数量
- 当前价格 / 当前市值 / 当前收益
- 退出时间 / 退出市值 / 退出原因，如果已关闭
- 钱包结构状态
- 钱包结构分
- 钱包风险分
- 对手盘压力
- 数据质量分
- 入场原因自然语言解释
- 钱包结构自然语言解释
- 持仓过程自然语言解释
- 自动复盘
- 策略调整建议
- 每个字段的数据来源
- 仍然缺失的字段清单
- case_completeness_score
- 是否可进入核心策略统计

严格边界：
1. 不执行真实 swap。
2. 不新增真实交易按钮。
3. 不新增 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST。
4. 不读取私钥。
5. 不写入私钥。
6. 不打印 TELEGRAM_BOT_TOKEN。
7. 不删除已有模块。
8. 不破坏 sikk_live_run.py 主入口。
9. 不破坏 paper runner 现有交易逻辑。
10. 不做无关重构。
11. 本任务只做数据补全、证据回填、Case File 展示、自动复盘和审计。

认知角色：
1. Case File 数据架构师：
负责定义每个 Case File 必须有哪些字段、字段从哪里来、缺失时如何标记。

2. 纸面交易复盘专家：
负责判断每笔仓位是否具备复盘价值，是否能进入核心策略统计。

3. 钱包筹码结构分析专家：
负责钱包结构、同源组、对手盘压力、筹码迁移、主导侧生命周期字段的接入和解释。

4. 市值路径审计员：
负责 discovery_market_cap_usd、signal_market_cap_usd、entry_market_cap_usd、current_market_cap_usd、exit_market_cap_usd 的回填和解释。

5. UI 信息架构专家：
负责 Case File HTML 页面中的结构、缺失字段提示、证据来源展示、阶段完整度显示。

6. 中文解释专家：
负责把字段转为自然语言解释，不能只堆字段。

7. 安全边界官：
负责确认没有真实交易入口、没有私钥、没有 webhook 泄露。

8. 测试验收官：
负责 py_compile、pytest、真实样本验证、HTML 内容检查、字段完整度检查。

阶段执行规则：
1. 按 Phase 顺序执行。
2. 每个 Phase 必须有报告。
3. 每个 Phase 必须运行验收命令。
4. 每个 Phase 必须针对 ARea51 样本验证。
5. 验收失败不得进入下一阶段。
6. 失败时只修失败项，不扩展新功能。
7. 每个 Phase 完成后更新：
   - SIKK_CHANGELOG.md
   - SIKK_PROJECT_STATE.md
   - SIKK_LESSONS_LEARNED.md
   - SIKK_NEXT_TASK.md

==================================================
Phase 0：Case File 现状侦察
==================================================

目标：
只检查当前 ARea51 Case File 的 HTML / JSON / position / index 数据状态，不修改代码。

检查样本：
paper-ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1-2026-05-03T10_09_28Z

需要检查：
1. HTML 文件实际路径
2. 对应 JSON case file 是否存在
3. 对应 paper position 是否存在于 open / closed
4. 对应 position 是否存在于 position_index.json
5. 对应 token 是否存在于 token_detail_index.json
6. 对应 wallet_structure_decision 是否存在
7. 对应 auto_review 是否存在
8. 对应 position_journal 是否存在
9. 当前 HTML 中有多少 “待补 / UNKNOWN / DATA_INSUFFICIENT”
10. 哪些阶段字段缺失最多

建议检查命令：

cd /root/sikk-gmgn

find data/gmgn_candidates_live_run -type f | grep -i "ARea51\|paper-ARea51" | sort

grep -R "待补\|UNKNOWN\|DATA_INSUFFICIENT\|证据不足\|未接入" \
  data/gmgn_candidates_live_run/site/case_files \
  data/gmgn_candidates_live_run/paper_live/case_files \
  2>/dev/null | grep -i "ARea51" | head -n 100

python3 - <<'PY'
from pathlib import Path
target = "ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1"
base = Path("data/gmgn_candidates_live_run")
for p in base.rglob("*"):
    if p.is_file() and target.lower() in str(p).lower():
        print(p)
PY

输出：
reports/case_data_backfill/PHASE_0_READINESS_REPORT.md

报告必须包含：
1. ARea51 HTML 路径
2. ARea51 JSON 路径
3. ARea51 position 来源
4. 当前缺失字段统计
5. 当前缺失阶段统计
6. 当前可用数据源
7. 当前不可回填字段
8. Phase 1 应实现的字段来源映射

禁止：
- 不修改代码
- 不生成新逻辑
- 不改数据

==================================================
Phase 1：Case Field Source Map 字段来源映射
==================================================

目标：
建立 Case File 字段来源映射，明确每个字段应该从哪里读取，不能继续“想到什么补什么”。

新增文件：
- sikk_case_field_source_map.py
- tests/test_sikk_case_field_source_map.py
- docs/SIKK_CASE_FIELD_SOURCE_MAP.md

字段来源必须分组：

A. 基础字段
- position_id
- token_symbol
- token_address
- status
来源优先级：
1. paper_positions_open.json / paper_positions_closed.json
2. position_index.json
3. case_files/*.json

B. 发现阶段字段
- candidate_discovered_at
- discovery_source
- discovery_price
- discovery_market_cap_usd
- discovery_liquidity_usd
- discovery_holder_count
来源优先级：
1. token_status.json
2. candidate_states.json
3. gmgn_new_token_filter/token_candidates.json
4. position_index.json
5. case_json

C. 信号阶段字段
- signal_time
- signal_level
- signal_type
- signal_price
- signal_market_cap_usd
- signal_reason
来源优先级：
1. candidate_signal_summary.json
2. candidate_states.json
3. position_index.json
4. case_json

D. 钱包结构字段
- wallet_decision_time
- wallet_structure_status
- wallet_structure_score
- wallet_risk_score
- counterparty_pressure_score
- data_quality_score
- early_wallet_remaining_pct
- early_wallet_sold_pct
- same_source_sync_sell_score
- wallet_support_signals
- wallet_risk_signals
- wallet_reason
来源优先级：
1. wallet_structure/<token>/wallet_structure_decision.json
2. wallet_structure/candidate_wallet_structure_summary.json
3. position_index.json
4. case_json

E. quote/security 字段
- quote_check_time
- quote_source
- quote_price
- gmgn_price
- okx_price
- kline_close_price
- price_deviation_pct
- quote_gate
- security_gate
- security_risk_level
- security_flags
来源优先级：
1. quote_security/candidate_quote_security_summary.json
2. token_status.json
3. position_index.json

F. 入场字段
- paper_entry_time
- entry_price
- entry_raw_quote_price
- entry_simulated_price
- entry_market_cap_usd
- entry_liquidity_usd
- entry_holder_count
- paper_size_sol
- paper_size_usd
- estimated_token_amount
来源优先级：
1. paper_positions_open.json / paper_positions_closed.json
2. paper_trades.csv
3. position_index.json
4. case_json

G. 当前持仓字段
- current_price
- current_market_cap_usd
- unrealized_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
来源优先级：
1. paper_positions_open.json
2. position_journal/<position_id>.jsonl
3. position_index.json

H. 退出字段
- exit_time
- exit_price
- exit_market_cap_usd
- net_pnl_pct
- exit_trigger
- exit_reason_code
- trade_result_type
- failure_type
来源优先级：
1. paper_positions_closed.json
2. paper_trades.csv
3. position_index.json
4. case_json

I. 复盘字段
- strategy_fit_result
- entry_quality_review
- wallet_gate_review
- exit_quality_review
- risk_management_review
- strategy_adjustment_suggestion
- open_questions
来源优先级：
1. auto_reviews/<position_id>_review.json
2. case_json
3. rule-based fallback

J. 文件路径字段
- case_file_json
- case_file_md
- case_file_html
- auto_review_json
- auto_review_md
来源优先级：
1. case_file_index.json
2. auto_review_index.json
3. filesystem scan

每个字段必须有：
- field_name
- field_group
- required_for_high_quality
- source_priority
- fallback_value
- display_label_zh
- missing_reason_zh

验收命令：

cd /root/sikk-gmgn

python3 -m py_compile sikk_case_field_source_map.py
python3 -m pytest tests/test_sikk_case_field_source_map.py -q

输出：
reports/case_data_backfill/PHASE_1_FIELD_SOURCE_MAP_REPORT.md

==================================================
Phase 2：Case 数据完整度审计器
==================================================

目标：
实现一个独立审计器，扫描每个 Case File，计算完整度，列出缺失字段和来源。

新增文件：
- sikk_case_data_completeness_auditor.py
- tests/test_sikk_case_data_completeness_auditor.py

输入：
- data/gmgn_candidates_live_run/index/position_index.json
- data/gmgn_candidates_live_run/index/token_detail_index.json
- data/gmgn_candidates_live_run/paper_live/case_files/*.json
- data/gmgn_candidates_live_run/site/case_files/*.html

输出：
data/gmgn_candidates_live_run/reports/case_data_completeness/
- case_completeness_summary.json
- case_completeness_summary.csv
- case_completeness_summary.md
- per_case/<position_id>_missing_fields.json
- per_case/<position_id>_source_trace.json

每个 case 必须计算：
- case_completeness_score
- stage_completeness
- missing_required_fields
- missing_optional_fields
- source_trace
- case_quality
- strategy_review_eligible
- next_backfill_action

stage_completeness 分组：
- basic
- discovery
- pattern
- signal
- wallet
- quote_security
- entry
- holding
- exit
- review
- file_links

case_quality 规则：
HIGH：
- basic、signal、entry、wallet、quote_security、review 都 >= 80
- discovery、market_cap_path 至少 >= 70

MEDIUM：
- basic、entry、signal 存在
- wallet 或 discovery 有部分缺失

LOW：
- paper_entry_time 存在
- 但 entry_market_cap_usd 或 wallet_structure_status 缺失

INVALID：
- position_id / token_address / paper_entry_time 缺失

ARea51 样本必须单独输出：
per_case/paper-ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1-2026-05-03T10_09_28Z_missing_fields.json

验收命令：

cd /root/sikk-gmgn

python3 -m py_compile sikk_case_data_completeness_auditor.py

python3 sikk_case_data_completeness_auditor.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/reports/case_data_completeness

python3 - <<'PY'
import json
from pathlib import Path

p = Path("data/gmgn_candidates_live_run/reports/case_data_completeness/case_completeness_summary.json")
assert p.exists(), "missing summary"
d = json.loads(p.read_text())
print("cases:", len(d.get("cases", [


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 2. SIKK Telegram 中文专业控制台

来源路径：`[1008]`；长度：19359


你现在要做的不是“让 Hermes 帮你写一个 TG 面板”，而是建立一套 **Hermes 多角色、多阶段、可验收的交互系统工程流程**。

目标应定义为：

```text
SIKK Telegram 中文专业控制台
=
统一索引层
+ 中文状态语言层
+ Telegram 中文面板层
+ Callback 点击交互层
+ 单币/单仓位详情层
+ Case File / Auto Review 复盘层
+ 系统健康 / 风险提醒层
+ 测试验收层
```

重点不是“写几个按钮”，而是让 TG 成为你手机端的 **SIKK 操作观察台**。

---

# 一、先建立 Hermes 里的“认知角色体系”

你可以给 Hermes 一个固定角色组。不是让它幻想角色，而是让每个角色对应一个具体责任。

## 角色 1：交互总设计师

职责：

```text
负责整体交互路径：
系统总览 → 开放仓位 → 单仓位详情 → 入场证据 → 钱包结构 → 持仓过程 → 自动复盘 → 下一步动作
```

它判断：

```text
用户应该先看到什么？
哪些信息放第一页？
哪些信息点击后展开？
哪些状态必须高亮？
哪些按钮不能出现？
```

---

## 角色 2：信息架构师

职责：

```text
负责字段层级、数据对象、页面结构。
```

它判断：

```text
System / Token / Position / Case File / Auto Review / Alert 如何分层？
每个对象需要哪些字段？
字段缺失时如何显示？
```

---

## 角色 3：Telegram 交互设计师

职责：

```text
负责 TG 菜单、按钮、分页、返回路径、中文消息长度。
```

它判断：

```text
每页最多显示几个仓位？
按钮如何命名？
callback_data 如何缩短？
如何避免 TG 消息太长？
```

---

## 角色 4：交互 AI 编程大师

职责：

```text
负责把交互设计落成 Python 代码。
```

它实现：

```text
sikk_telegram_views.py
sikk_telegram_callback_index.py
sikk_telegram_interactive_bot.py
sikk_telegram_zh.py
```

---

## 角色 5：UI 文案专家

职责：

```text
负责中文文案、状态翻译、自然语言解释。
```

它保证：

```text
不是显示 HOLD_WITH_DATA_RISK
而是显示：带数据风险持有

不是显示 UNKNOWN
而是显示：待补 / 证据不足
```

---

## 角色 6：数据质量审计员

职责：

```text
负责判断字段是否完整、样本是否能复盘。
```

它输出：

```text
case_quality
strategy_review_eligible
evidence_missing_fields
next_action
```

---

## 角色 7：安全边界官

职责：

```text
负责检查是否出现真实交易风险。
```

它禁止：

```text
BUY
SELL
SWAP
EXECUTE
APPROVE
BROADCAST
私钥
真实交易按钮
```

---

## 角色 8：测试验收官

职责：

```text
负责 py_compile、pytest、TG 视图测试、按钮测试、文本检查。
```

它必须输出：

```text
PASS / FAIL
失败项
修复建议
是否允许进入下一阶段
```

---

# 二、在 Hermes 里先设置长期目标

先发：

```text
/branch

创建 SIKK Telegram 中文专业控制台分支。

本分支目标：
把 SIKK Telegram 从静态广播升级为中文可点击专业控制台。

严格边界：
- 不执行真实 swap
- 不新增交易按钮
- 不新增 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST
- 不读取私钥
- 不写入私钥
- 不删除已有模块
- 不破坏 paper runner
- 不破坏 sikk_live_run.py
```

然后发：

```text
/goal

当前长期目标：

实现 SIKK Telegram 中文专业控制台。

用户可见内容必须全部中文化：
- 面板中文
- 按钮中文
- 状态中文
- 复盘中文
- 下一步动作中文
- 风险提醒中文

底层 Telegram slash command 可以保留英文：
/sikk
/open
/closed
/token
/position
/review
/health
/alerts
/refresh

但同时必须支持中文自然语言触发：
系统总览
开放仓位
已关闭仓位
纸面统计
策略复盘
风险提醒
系统健康
刷新数据
查看 LITH
代币 LITH
仓位 <position_id>

第一硬验收闭环：

Telegram 输入：
/sikk

显示中文主菜单。

点击：
开放仓位

显示中文开放仓位列表。

点击：
LITH

显示 LITH 中文仓位详情，包括：
- 入场时间
- 入场价格
- 仓位规模
- 当前收益
- 最大回撤
- 样本质量
- 缺失证据
- 下一步动作

点击：
入场证据

显示 LITH 入场证据中文解释。

点击：
自动复盘

显示 LITH 自动复盘中文解释。
```

---

# 三、整体工程阶段

不要一次让 Hermes 全做。按 10 个阶段推进。

```text
Phase 0：侦察当前 TG / index / paper 数据状态
Phase 1：统一中文术语层 sikk_telegram_zh.py
Phase 2：Telegram callback index 短 ID 层
Phase 3：中文视图函数层 sikk_telegram_views.py
Phase 4：Telegram bot handler 层
Phase 5：中文自然语言触发词
Phase 6：TG 面板合集第一闭环
Phase 7：系统健康 / 风险提醒 / 复盘面板
Phase 8：测试与安全审计
Phase 9：tmux 长期运行
Phase 10：纳入 SIKK 项目状态文档
```

---

# 四、Phase 0：侦察，不写代码

这一阶段只看当前文件，不能改。

发给 Hermes：

```text
/codebase_inspection

Phase 0：SIKK Telegram 中文专业控制台侦察。

只检查，不修改代码。

检查目录：
/root/sikk-gmgn

检查文件是否存在：
- sikk_unified_view_builder.py
- sikkctl.py
- sikk_telegram_interactive_bot.py
- sikk_telegram_views.py
- sikk_telegram_callback_index.py
- sikk_telegram_zh.py
- tests/test_sikk_telegram_views.py
- tests/test_sikk_telegram_callback_index.py
- tests/test_sikk_telegram_zh.py

检查数据是否存在：
- data/gmgn_candidates_live_run/index/system_index.json
- data/gmgn_candidates_live_run/index/token_detail_index.json
- data/gmgn_candidates_live_run/index/position_index.json
- data/gmgn_candidates_live_run/index/case_file_index.json
- data/gmgn_candidates_live_run/index/auto_review_index.json
- data/gmgn_candidates_live_run/index/alert_index.json
- data/gmgn_candidates_live_run/telegram/callback_index.json

重点检查 LITH 是否存在于：
- token_detail_index.json
- position_index.json
- case_file_index.json
- auto_review_index.json

输出：
SIKK_TG_CHINESE_PHASE0_READINESS_REPORT.md

报告必须包含：
1. 已有文件
2. 缺失文件
3. 当前 TG 是否只是广播
4. 是否已有 callback query
5. 是否已有中文映射
6. LITH 是否能被索引查询
7. Phase 1 应修改/新增哪些文件
8. Phase 1 验收命令

禁止修改代码。
```

验收标准：

```text
必须生成 SIKK_TG_CHINESE_PHASE0_READINESS_REPORT.md。
不能改任何代码。
```

---

# 五、Phase 1：中文术语层

目标：先把所有状态、动作、质量、风险统一中文化。

## 要新增文件

```text
sikk_telegram_zh.py
tests/test_sikk_telegram_zh.py
```

发给 Hermes：

```text
/codex

Phase 1：实现 Telegram 中文术语层。

目标：
新增 sikk_telegram_zh.py，统一所有 TG 用户可见中文文案。

新增文件：
- sikk_telegram_zh.py
- tests/test_sikk_telegram_zh.py

sikk_telegram_zh.py 必须包含：

1. STATE_ZH
用于仓位状态：
OPEN → 开放
CLOSED → 已关闭
PAUSED → 暂停
EXPIRED → 已过期
ERROR → 异常

2. ACTION_ZH
用于动作：
HOLD → 持有
HOLD_WITH_DATA_RISK → 带数据风险持有
EXIT_MONITOR → 退出观察
FORCE_PAPER_EXIT → 纸面强制退出
WAIT_SIGNAL → 等待信号
WAIT_WALLET → 等待钱包结构
WAIT_QUOTE → 等待报价
WAIT_SECURITY → 等待安全检查
BACKFILL_WALLET_AND_MARKET_CAP → 补齐钱包结构与市值路径
COOLING → 冷却观察
IGNORE → 忽略

3. QUALITY_ZH
HIGH → 高
MEDIUM → 中
LOW → 低
INVALID → 无效

4. ENTRY_CONTEXT_ZH
EARLY_ENTRY → 早期入场
NORMAL_ENTRY → 正常入场
LATE_ENTRY → 偏晚入场
CHASE_ENTRY → 追高入场
UNKNOWN_ENTRY → 入场上下文未知

5. ALERT_TYPE_ZH
NEW_PAPER_ENTRY → 新增纸面入场
PAPER_EXIT → 纸面退出
FORCE_EXIT → 纸面强制退出
EXIT_MONITOR → 退出观察
HOLD_WITH_DATA_RISK → 带数据风险持有
DATA_BACKFILL_REQUIRED → 需要补齐数据
WALLET_COVERAGE_LOW → 钱包结构覆盖率偏低
CASE_QUALITY_LOW → 低质量样本
BIG_WIN → 右尾大赢家
BIG_LOSS → 大亏损
FALSE_EXIT_SUSPECTED → 疑似过早退出

6. 工具函数：
- zh(value, mapping, default="待补")
- format_pct(value)
- format_usd(value)
- format_sol(value)
- format_time(value)
- missing_text(value, default="待补")
- truncate_text(text, limit=3000)
- safe_text(text)

要求：
所有缺失值统一显示为“待补”。
所有 UNKNOWN / None / "" 不能直接显示给用户。
所有英文状态必须有中文映射。

测试：
tests/test_sikk_telegram_zh.py 必须测试：
- 状态中文映射
- 动作中文映射
- 缺失值显示为待补
- 百分比格式
- USD 格式
- SOL 格式
- 超长文本截断

验收命令：

cd /root/sikk-gmgn

python3 -m py_compile sikk_telegram_zh.py

python3 -m pytest tests/test_sikk_telegram_zh.py -q

完成后输出：
SIKK_TG_CHINESE_PHASE1_ZH_REPORT.md

报告必须包含：
1. 新增文件
2. 中文映射清单
3. 测试结果
4. 未完成项
```

---

# 六、Phase 2：Callback 短 ID 层

目标：TG 点击按钮不能直接塞长地址和中文，必须用短 ID。

## 要实现

```text
sikk_telegram_callback_index.py
tests/test_sikk_telegram_callback_index.py
```

发给 Hermes：

```text
/codex

Phase 2：实现 Telegram Callback 短 ID 索引层。

目标：
生成 data/gmgn_candidates_live_run/telegram/callback_index.json。
所有 TG 按钮只使用短 callback_data，不直接使用长 position_id、token_address 或中文文本。

修改/新增：
- sikk_telegram_callback_index.py
- tests/test_sikk_telegram_callback_index.py

读取：
- data/gmgn_candidates_live_run/index/token_detail_index.json
- data/gmgn_candidates_live_run/index/position_index.json
- data/gmgn_candidates_live_run/index/case_file_index.json
- data/gmgn_candidates_live_run/index/auto_review_index.json

输出：
- data/gmgn_candidates_live_run/telegram/callback_index.json

格式：
{
  "T1": {
    "type": "token",
    "token_symbol": "LITH",
    "token_address": "..."
  },
  "P1": {
    "type": "position",
    "position_id": "PAPER_LITH_xxx",
    "token_symbol": "LITH"
  },
  "C1": {
    "type": "case_file",
    "position_id": "PAPER_LITH_xxx",
    "path": "..."
  },
  "R1": {
    "type": "auto_review",
    "position_id": "PAPER_LITH_xxx",
    "path": "..."
  }
}

短 ID 规则：
- Token：T1, T2, T3
- Position：P1, P2, P3
- Case File：C1, C2, C3
- Auto Review：R1, R2, R3

允许 callback_data：
- panel:main
- panel:open:0
- panel:closed:0
- panel:stats
- panel:review
- panel:health
- panel:alerts:0
- tok:T1
- pos:P1
- entry:P1
- wallet:P1
- journal:P1
- review:R1
- case:C1
- back:main
- back:open
- refresh:main

禁止：
- callback_data 中出现长 token 地址
- callback_data 中出现完整 position_id
- callback_data 中出现中文长文本

验收命令：

cd /root/sikk-gmgn

python3 -m py_compile sikk_telegram_callback_index.py

python3 sikk_unified_view_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/index

python3 sikk_telegram_callback_index.py \
  --base-dir data/gmgn_candidates_live_run \
  --index-dir data/gmgn_candidates_live_run/index \
  --output-dir data/gmgn_candidates_live_run/telegram

python3 -m pytest tests/test_sikk_telegram_callback_index.py -q

python3 - <<'PY'
import json
from pathlib import Path
p = Path("data/gmgn_candidates_live_run/telegram/callback_index.json")
assert p.exists(), "callback_index missing"
d = json.loads(p.read_text())
print("callback items:", len(d))
print("has token:", any(v.get("type") == "token" for v in d.values()))
print("has position:", any(v.get("type") == "position" for v in d.values()))
assert d
PY

完成后输出：
SIKK_TG_CHINESE_PHASE2_CALLBACK_REPORT.md
```

---

# 七、Phase 3：中文视图函数层

目标：先实现所有中文面板的文本和按钮，不急着接 bot。

## 要实现

```text
sikk_telegram_views.py
tests/test_sikk_telegram_views.py
```

这是最重要一层。

发给 Hermes：

```text
/codex

Phase 3：实现 Telegram 中文面板视图函数。

目标：
实现 sikk_telegram_views.py。
所有函数返回：
- text: 中文面板文本
- inline_keyboard: 中文按钮结构

必须读取：
- data/gmgn_candidates_live_run/index/system_index.json
- data/gmgn_candidates_live_run/index/token_detail_index.json
- data/gmgn_candidates_live_run/index/position_index.json
- data/gmgn_candidates_live_run/index/case_file_index.json
- data/gmgn_candidates_live_run/index/auto_review_index.json
- data/gmgn_candidates_live_run/index/alert_index.json
- data/gmgn_candidates_live_run/telegram/callback_index.json

必须使用：
- sikk_telegram_zh.py

实现函数：

1. render_main_menu()
面板名：S


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 3. SIKK Telegram 中文专业控制台

来源路径：`[1312]`；长度：14803


可以做，而且你现在应该把目标明确成：

# SIKK Telegram 中文专业控制台

不是简单 `/sikk_open` 这种英文命令，而是：

```text
Telegram 里所有用户可见内容全部中文化：
- 命令说明中文
- 菜单中文
- 按钮中文
- 面板中文
- 状态解释中文
- 下一步动作中文
- 复盘结论中文
```

但有一个技术限制必须先说清楚：**Telegram 官方 Bot Command 的斜杠命令本身只能使用英文小写字母、数字和下划线，长度 1-32；不能真正注册 `/系统总览` 这种中文斜杠命令。** 所以正确做法是：底层保留 `/sikk`、`/open` 这类英文命令作为入口，但用户界面、按钮、命令菜单描述、普通中文消息触发词全部中文化。也就是说，你在 TG 里可以点 **「系统总览」**、输入 **「开放仓位」**、输入 **「查看LITH」**，但正式 slash command 仍需用英文格式。citeturn228738search0turn228738search2

---

# 一、最终目标

你要实现的是这个交互效果：

```text
用户输入：/sikk
或输入：系统总览

机器人显示：

SIKK 专业控制台

运行状态：正常
数据更新时间：2026-05-03 07:55 UTC
当前开放仓位：3
累计关闭仓位：163
已关闭胜率：31.90%
平均收益率：6.675%
低质量样本：37
需要处理事项：5

请选择要查看的模块：
[开放仓位] [纸面统计]
[代币查询] [风险提醒]
[系统健康] [策略复盘]
[刷新]
```

然后：

```text
点击 [开放仓位]
  ↓
显示所有开放仓位
  ↓
点击 [LITH -13.87%]
  ↓
进入 LITH 仓位详情
  ↓
点击 [入场证据] / [钱包证据] / [持仓记录] / [自动复盘] / [完整档案]
```

这才是你要的 **TG 面板合集**。

---

# 二、命令设计：用户可见全中文，底层命令英文

## 1. 底层 slash commands

Telegram 限制下，建议注册这些英文命令，但描述全部中文：

| 底层命令 | 中文描述 | 用户实际理解 |
|---|---|---|
| `/sikk` | 打开 SIKK 中文控制台 | 系统总览 |
| `/open` | 查看当前开放纸面仓位 | 开放仓位 |
| `/closed` | 查看已关闭纸面仓位 | 已关闭仓位 |
| `/token` | 查询指定代币 | 代币查询 |
| `/position` | 查询指定纸面仓位 | 仓位查询 |
| `/review` | 查看策略复盘总结 | 策略复盘 |
| `/health` | 查看系统健康与数据缺失 | 系统健康 |
| `/alerts` | 查看风险提醒 | 风险提醒 |
| `/refresh` | 刷新索引和面板数据 | 刷新数据 |

但在用户界面中，不显示英文主导，而显示中文按钮。

---

## 2. 中文自然语言触发词

同时支持用户直接输入中文：

```text
系统总览
开放仓位
已关闭仓位
纸面统计
策略复盘
风险提醒
系统健康
刷新数据
查看 LITH
查看LITH
代币 LITH
仓位 PAPER_LITH_xxx
```

这样你手机上不用记英文命令。

---

# 三、TG 面板合集总结构

建议分成 10 个中文面板。

```text
M0 系统总览面板
M1 开放仓位面板
M2 已关闭仓位面板
M3 单代币详情面板
M4 单仓位详情面板
M5 入场证据面板
M6 钱包结构面板
M7 持仓过程面板
M8 自动复盘面板
M9 系统健康面板
M10 风险提醒面板
```

对应按钮路径：

```text
系统总览
  ├─ 开放仓位
  │   └─ 单仓位详情
  │       ├─ 入场证据
  │       ├─ 钱包结构
  │       ├─ 持仓过程
  │       ├─ 自动复盘
  │       └─ 完整档案
  ├─ 纸面统计
  ├─ 策略复盘
  ├─ 风险提醒
  └─ 系统健康
```

---

# 四、每个面板具体显示什么

## M0：系统总览面板

触发：

```text
/sikk
系统总览
主页
```

显示：

```text
SIKK 专业控制台

运行状态：正常
数据更新时间：2026-05-03 07:55 UTC

纸面仓位：
- 当前开放：3
- 累计关闭：163
- 已关闭胜率：31.90%
- 已关闭平均收益率：6.675%

数据质量：
- 低质量样本：37
- 待补数据样本：5
- 钱包结构覆盖率：14%

当前重点：
- 1 个开放仓位处于「带数据风险持有」
- LITH 缺少入场市值与钱包结构字段
- 钱包结构覆盖率偏低

下一步建议：
优先补齐开放仓位的市值路径和钱包结构字段。
```

按钮：

```text
[开放仓位] [已关闭仓位]
[纸面统计] [策略复盘]
[风险提醒] [系统健康]
[刷新数据]
```

---

## M1：开放仓位面板

触发：

```text
/open
开放仓位
```

显示：

```text
当前开放纸面仓位：3

1. LITH
- 当前收益：-13.87%
- 入场时间：2026-04-28 17:46 UTC
- 入场价格：0.000021063508
- 入场市值：待补
- 仓位：0.085319 SOL
- 最大回撤：-21.99%
- 动作：带数据风险持有
- 样本质量：低

2. XXX
- 当前收益：...
```

按钮：

```text
[LITH｜-13.87%｜低质量]
[XXX｜+4.21%｜中质量]
[上一页] [下一页]
[返回首页] [刷新]
```

---

## M2：已关闭仓位面板

触发：

```text
/closed
已关闭仓位
```

显示：

```text
已关闭纸面仓位

累计关闭：163
胜率：31.90%
平均收益率：6.675%

最近关闭：
1. AALIEN
- 收益：+679.39%
- 退出原因：钱包结构触发
- 结果类型：右尾大赢家

2. GRUMP
- 收益：-98.31%
- 退出原因：钱包结构触发
- 结果类型：大亏损
```

按钮：

```text
[AALIEN｜+679.39%]
[GRUMP｜-98.31%]
[上一页] [下一页]
[返回首页]
```

---

## M3：单代币详情面板

触发：

```text
点击某个 Token
查看 LITH
代币 LITH
/token LITH
```

显示：

```text
LITH 代币详情

地址：
GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump

当前状态：开放持仓
当前市值：待补
最新钱包状态：证据不足
最新信号等级：S4 强确认

仓位统计：
- 总仓位：1
- 开放仓位：1
- 已关闭仓位：0
- 当前收益：-13.87%
- 最大回撤：-21.99%

样本质量：
- 等级：低
- 是否进入核心策略统计：否

缺失证据：
- 发现时市值
- 入场时市值
- 钱包结构状态
- 钱包结构分
- 对手盘压力

下一步：
补齐市值路径和钱包结构后再复盘。
```

按钮：

```text
[查看仓位详情]
[入场证据]
[钱包结构]
[持仓过程]
[自动复盘]
[完整档案]
[返回开放仓位]
```

---

## M4：单仓位详情面板

这是最核心。

显示：

```text
LITH 纸面仓位详情

仓位编号：
PAPER_LITH_xxx

状态：开放
策略：SIKK-B 控盘箱体突破回踩
信号：S4 强确认

入场信息：
- 入场时间：2026-04-28 17:46 UTC
- 入场价格：0.000021063508
- 入场市值：待补
- 仓位规模：0.085319 SOL
- 估算代币数量：待补

当前信息：
- 当前价格：0.000018142653
- 当前收益：-13.87%
- 最大回撤：-21.99%
- 当前动作：带数据风险持有

证据质量：
- 样本质量：低
- 复盘资格：否
- 缺失字段：发现时市值、入场市值、钱包结构

系统解释：
当前不是强证据持有，而是在关键字段缺失情况下继续观察。该仓位需要补齐数据后才能判断 SIKK-B 入场是否有效。
```

按钮：

```text
[入场证据]
[钱包结构]
[持仓过程]
[自动复盘]
[完整档案]
[返回代币]
[返回首页]
```

---

## M5：入场证据面板

显示：

```text
LITH 入场证据

策略：SIKK-B 控盘箱体突破回踩
信号等级：S4 强确认

发现阶段：
- 发现时间：待补
- 发现市值：待补

信号阶段：
- 信号时间：待补
- 信号市值：待补

入场阶段：
- 入场时间：2026-04-28 17:46 UTC
- 入场价格：0.000021063508
- 入场市值：待补
- 仓位：0.085319 SOL

入场上下文：
未知

解释：
当前无法判断该仓位是早期入场、正常入场、偏晚入场还是追高入场，因为发现市值和入场市值字段缺失。

下一步：
补齐 discovery_market_cap_usd 和 entry_market_cap_usd。
```

按钮：

```text
[钱包结构]
[持仓过程]
[自动复盘]
[返回仓位详情]
```

---

## M6：钱包结构面板

显示：

```text
LITH 钱包结构

钱包状态：证据不足
结构分：待补
风险分：待补
对手盘压力：待补
数据质量：低

早期钱包：
- 剩余比例：待补
- 已卖比例：待补

同源组：
- 同源组数量：待补
- 同步卖出分：待补

高结果钱包：
- 剩余比例：待补

解释：
当前钱包结构证据不足，不能判断结构侧是否仍然控筹，也不能判断是否发生主动派发或接盘方承接。

下一步：
补齐钱包结构快照，至少需要 entry_wallet_structure_status、wallet_structure_score、wallet_risk_score、counterparty_pressure_score。
```

按钮：

```text
[入场证据]
[持仓过程]
[自动复盘]
[返回仓位详情]
```

---

## M7：持仓过程面板

显示最近 journal：

```text
LITH 持仓过程

当前记录数：5

最近变化：
1. 2026-05-03 05:58
- 价格：0.000017363255
- 浮盈：-17.57%
- 动作：持有

2. 2026-05-03 06:54
- 价格：0.000016431090
- 浮盈：-21.99%
- 动作：持有

3. 2026-05-03 07:55
- 价格：0.000018142653
- 浮盈：-13.87%
- 动作：持有

过程解释：
该仓位曾扩大到约 -21.99% 回撤，随后修复到 -13.87%。当前不是单边持续恶化，但由于钱包和市值字段缺失，不能确认这是有效修复还是弱反弹。
```

按钮：

```text
[入场证据]
[钱包结构]
[自动复盘]
[返回仓位详情]
```

---

## M8：自动复盘面板

显示：

```text
LITH 自动复盘

策略适配结果：
结论不足

入场质量：
数据不足，无法判断是否追高。

钱包门禁：
钱包结构证据缺失，无法判断入场时是否应允许纸面验证。

风险控制：
最大回撤达到 -21.99%，且关键证据缺失，应标记为数据风险持有，而不是普通持有。

主要问题：
- 入场市值缺失
- 发现市值缺失
- 钱包结构缺失
- 生命周期未知

策略调整建议：
先补齐市值路径和钱包结构字段，再判断这笔仓位是否属于有效 SIKK-B 样本。当前不应纳入核心策略胜率和收益统计。
```

按钮：

```text
[完整档案]
[返回仓位详情]
[返回首页]
```

---

## M9：系统健康面板

显示：

```text
SIKK 系统健康

数据源状态：
- paper_positions_open：正常
- paper_positions_closed：正常
- strategy_metrics：正常
- failure_attribution：正常
- case_files：部分缺失
- auto_reviews：部分缺失
- wallet_structure：覆盖率偏低

覆盖率：
- 钱包结构覆盖率：14%
- Case File 覆盖率：待统计
- 自动复盘覆盖率：待统计

主要问题：
1. 多个仓位缺少入场市值。
2. 多个仓位缺少钱包结构。
3. 开放仓位中存在低质量样本。
4. LITH 当前需要数据补齐。

下一步系统动作：
优先修复 market_cap_context 与 wallet_structure 接入。
```

按钮：

```text
[风险提醒]
[纸面统计]
[返回首页]
[刷新]
```

---

## M10：风险提醒面板

显示：

```text
风险提醒

1. LITH
等级：中
类型：带数据风险持有
说明：开放仓位最大回撤曾达到 -21.99%，但市值和钱包结构字段缺失。
下一步：补齐市值路径和钱包结构。

2. 钱包结构覆盖率偏低
等级：高
说明：当前钱包结构接入率不足，影响策略复盘质量。
下一步：检查 wallet_structure pipeline。

3. 低质量样本过多
等级：中
说明：部分仓位不能进入核心策略统计。
下一步：补齐 entry snapshot。
```

按钮：

```text
[LITH 详情]
[系统健康]
[返回首页]
```

---

# 五、中文 callback 命名策略

用户看到中文，内部 callback 仍然用短码。

例如按钮显示：

```text
[开放仓位]
```

内部 callback：

```text
panel:open:0
```

按钮显示：

```text
[LITH｜-13.87%｜低质量]
```

内部 callback：

```text
pos:P12
```

不要把中文或长地址塞进 callback_data，Telegram callback_data 有长度限制，稳定做法是短 ID：

```json
{
  "P12": {
    "type": "position",
    "position_id": "PAPER_LITH_xxx",
    "token_symbol": "LITH"
  }
}
```

---

# 六、中文状态映射表

实现时不要直接显示英文状态。要统一映射。

```python
STATE_ZH = {
    "OPEN": "开放",
    "CLOSED": "已关闭",
    "HOLD": "持有",
    "HOLD_WITH_DATA_RISK": "带数据风险持有",
    "EXIT_MONITOR": "退出观察",
    "FORCE_PAPER_EXIT": "纸面强制退出",
    "LOW": "低",
    "MEDIUM": "中",
    "HIGH": "高",
    "INVALID": "无效",
    "WALLET_SUPPORT": "钱包结构支持",
    "WALLET_BLOCK": "钱包结构阻断",
    "WALLET_PAUSE": "钱包结构暂停",
    "UNKNOWN_ENTRY": "入场上下文未知",
    "EARLY_ENTRY": "早期入场",
    "NORMAL_ENTRY": "正常入场",
    "LATE_ENTRY": "偏晚入场",
    "CHASE_ENTRY": "追高入场",
}
```

---

# 七、给 Hermes 的完整落地任务书

你可以直接复制：

```text
任务：实现 SIKK Telegram 中文专业控制台面板合集。

当前目标：
把 Telegram 从“英文命令 + 静态广播文本”升级为“全中文可点击专业控制台”。

重要说明：
Telegram 官方 slash command 本身只能使用英文小写字母、数字和下划线，因此底层命令保留 /sikk、/open、/closed 等英文格式。
但用户可见内容必须全部中文化：
- 命令描述中文
- 消息内容中文
- 按钮中文
- 状态中文
- 复盘中文
- 下一步动作中文
同时支持中文自然语言触发词：
- 系统总览
- 开放仓位
- 已关闭仓位
- 纸面统计
- 策略复盘
- 风险提醒
- 系统健康
- 刷新数据
- 查看 LITH
- 代币 LITH

严格边界：
1. 不执行真实 swap。
2. 不新增交易按钮。
3. 不新增 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST。
4. 不读取私钥。
5. 不写入私钥。
6. 不删除已有模块。
7. 不破坏 paper runner。
8. 不破坏 sikk_live_run.py。
9. Telegram 只做查询、展示、复盘、诊断。

依赖数据：
所有 Telegram 面板必须读取统一索引：
- data/gmgn_candidates_live_run/index/system_index.json
- data/gmgn_candidates_live_run/index/token_detail_index.json
- data/gmgn_candidates_live_run/index/position_index.json
- data/gmgn_candidates_live_run/index/case_file_index.json
- data/gmgn_candidates_live_run/index/auto_review_index.json
- data/gmgn_candidates_live_run/index/alert_index.json

如果 index 不存在，先运行：
python3 sikk_unified_view_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/index

新增 / 修改文件：
- sikk_telegram_interactive_bot.py
- sikk_telegram_views.py
- sikk_telegram_callback_index.py
- sikk_telegram_zh.py
- tests/test_sikk_telegram_views.py
- tests/test_sikk_telegram_callback_index.py
- tests/test_sikk_telegram_zh.py

新增 sikk_telegram_zh.py：
用于统一中文映射。

必须包含：
1. STATE_ZH
2. ACTION_ZH
3. QUALITY_ZH
4. ENTRY_CONTEXT_ZH
5. ALERT_TYPE_ZH
6. format_pct()
7. format_usd()
8. format_sol()
9. safe_text()
10. truncate_text()

一、底层命令

支持：
- /sikk：系统总览
- /open：开放仓位
- /closed：已关闭仓位
- /token <symbol_or_address>：代币查询
- /position <position_id>：仓位查询
- /review：策略复盘
- /health：系统健康
- /alerts：风险提醒
- /refresh：刷新数据

命令描述必须中文。

二、中文自然语言触发

支持普通消息：
- 系统总览 → render_main_menu
- 开放仓位 → render_open_positions
- 已关闭仓位 → render_closed_positions
- 纸面统计 → render_paper_stats
- 策略复盘 → render_review
- 风险提醒 → render_alerts
- 系统健康 → render_health
- 刷新数据 → rebuild index + render_main_menu
- 查看 LITH / 查看LITH / 代币 LITH → render_token_detail
- 仓位 <position_id> → render_position_detail

三、必须实现的中文面板

M0 系统总览面板：
函数：
render_main_menu()

显示：
- 运行状态
- 数据更


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 4. 文档驱动型自动化落地流程

来源路径：`[1546]`；长度：10156


对，这个流程是正确方向。  
但要再升级一层：**不能只是“按标题执行”，而要把每个标题变成一个可验证的工程单元。**

你要在 Hermes 里建立：

# 文档驱动型自动化落地流程

核心逻辑：

```text
Share 文档
  ↓
标题结构识别
  ↓
每个标题生成 Section Task
  ↓
每个 Section Task 绑定代码文件 / 数据文件 / 验收命令
  ↓
逐节实现
  ↓
逐节测试
  ↓
逐节归档
  ↓
再进入下一节
```

这样 AI 就不会一次性读太多、想太多、改太散。

---

# 一、完整流程应分成 6 个阶段

## 阶段 A：文档接收与标题结构识别

目标：  
**只识别文档结构，不实现代码。**

输入：

```text
ChatGPT share 链接
文章链接
Markdown 文档
项目设计文档
```

输出：

```text
docs/imported/<doc_id>_raw.md
docs/imported/<doc_id>_outline.json
docs/imported/<doc_id>_section_index.md
```

只做三件事：

```text
1. 抓取文档内容
2. 提取标题层级
3. 给每个标题生成 section_id
```

不要让 AI 这一步写代码。

---

## 阶段 B：标题任务化

目标：  
把每一个标题变成工程任务。

每节生成：

```text
tasks/<doc_id>/<section_id>_task.md
```

每个 task 必须包含：

```text
1. 本节目标
2. 本节涉及的系统模块
3. 需要读取的文件
4. 允许修改的文件
5. 禁止修改的文件
6. 新增字段
7. 输出文件
8. 验收命令
9. 测试命令
10. 完成标准
```

---

## 阶段 C：单节实现

目标：  
一次只做一个标题对应的任务。

执行顺序：

```text
读取 section task
  ↓
Repomix 打包相关代码
  ↓
代码库侦察
  ↓
实现本节改动
  ↓
运行测试
  ↓
输出真实结果
```

---

## 阶段 D：单节验收

每节完成后必须生成：

```text
reports/<doc_id>/<section_id>_acceptance_report.md
```

必须包含：

```text
1. 修改文件列表
2. 新增文件列表
3. 实际运行命令
4. 测试结果
5. 输出文件是否存在
6. 样例输出
7. 未完成项
8. 是否允许进入下一节
```

---

## 阶段 E：节间记忆更新

每节完成后更新：

```text
SIKK_CHANGELOG.md
SIKK_LESSONS_LEARNED.md
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
```

目的：

```text
让下一节知道上一节已经做了什么
防止重复实现
防止 AI 忘记上下文
```

---

## 阶段 F：整篇文档收束审计

整篇文档所有标题完成后，生成：

```text
reports/<doc_id>/FINAL_DOCUMENT_IMPLEMENTATION_AUDIT.md
```

审计内容：

```text
1. 哪些标题已实现
2. 哪些标题只部分实现
3. 哪些标题跳过
4. 哪些代码文件被修改
5. 是否有测试
6. 是否有真实输出
7. 是否破坏现有模块
8. 是否引入真实交易风险
9. 下一轮优化方向
```

---

# 二、推荐目录结构

在 `/root/sikk-gmgn` 下建：

```text
docs/
  imported/
    doc_001_raw.md
    doc_001_outline.json
    doc_001_section_index.md

tasks/
  doc_001/
    S001_task.md
    S002_task.md
    S003_task.md

reports/
  doc_001/
    S001_acceptance_report.md
    S002_acceptance_report.md
    FINAL_DOCUMENT_IMPLEMENTATION_AUDIT.md

ai_context/
  doc_001/
    S001_context.xml
    S002_context.xml

state/
  doc_001_progress.json
```

---

# 三、Hermes 多模板体系

你现在需要 7 个固定模板。

---

## 模板 1：文档接收模板

用于阶段 A。

```text
/contract

任务：接收并解析 share 文档，但不实现代码。

输入：
<粘贴 share 链接或文档内容>

目标：
1. 读取文档内容。
2. 提取标题层级。
3. 生成 section_id。
4. 不做代码修改。
5. 不输出泛泛总结，只输出结构化标题索引。

输出文件：
- docs/imported/<doc_id>_raw.md
- docs/imported/<doc_id>_outline.json
- docs/imported/<doc_id>_section_index.md

outline.json 结构：
{
  "doc_id": "...",
  "title": "...",
  "sections": [
    {
      "section_id": "S001",
      "heading": "...",
      "level": 1,
      "parent_id": null,
      "summary": "...",
      "implementation_relevance": "HIGH/MEDIUM/LOW",
      "suggested_module": "..."
    }
  ]
}

禁止：
- 不写代码
- 不改项目文件
- 不执行测试
- 不扩展设计

完成后输出：
DOC_IMPORT_REPORT.md
```

---

## 模板 2：标题任务化模板

用于阶段 B。

```text
/codebase_inspection

任务：把文档标题转成可执行工程任务。

读取：
- docs/imported/<doc_id>_section_index.md
- docs/imported/<doc_id>_outline.json
- SIKK_PROJECT_STATE.md

只处理 section_id = <SXXX>。

目标：
为该标题生成任务文件：
tasks/<doc_id>/<SXXX>_task.md

任务文件必须包含：

1. 本节标题
2. 本节目标
3. 本节为什么重要
4. 涉及模块
5. 输入文件
6. 输出文件
7. 允许修改文件
8. 禁止修改文件
9. 新增字段
10. 实现步骤
11. 验收命令
12. 测试命令
13. 完成标准
14. 风险边界

禁止：
- 不改代码
- 不实现功能
- 不跳到下一节

完成后输出：
SECTION_TASK_BUILD_REPORT.md
```

---

## 模板 3：Repomix 上下文模板

用于阶段 C 前。

```text
/background

任务：为当前 section 生成 Repomix 上下文包。

读取：
tasks/<doc_id>/<SXXX>_task.md

目标：
根据该 section task 中的“允许修改文件”和“需要读取文件”，生成精准上下文包。

输出：
ai_context/<doc_id>/<SXXX>_context.xml

要求：
1. 只打包本节相关代码。
2. 排除 data/gmgn_candidates_live_run 大型运行数据。
3. 排除 .env、token、webhook、private key。
4. 输出文件清单。
5. 不改代码。

命令参考：
cat ai_context/<doc_id>/<SXXX>_files.txt | repomix --stdin \
  --output ai_context/<doc_id>/<SXXX>_context.xml

完成后输出：
REPO_CONTEXT_BUILD_REPORT.md
```

---

## 模板 4：单节实现模板

用于真正写代码。

```text
/codex

任务：实现单节工程任务。

读取：
1. tasks/<doc_id>/<SXXX>_task.md
2. ai_context/<doc_id>/<SXXX>_context.xml
3. SIKK_PROJECT_STATE.md
4. SIKK_LESSONS_LEARNED.md

只实现 section_id = <SXXX>。

严格要求：
1. 只修改任务文件中允许修改的文件。
2. 不处理其他标题。
3. 不扩展无关功能。
4. 不删除已有模块。
5. 不改变真实交易逻辑。
6. 不新增 swap / execute / approve / broadcast 按钮。
7. 不读取或写入私钥。

完成后必须运行：
- py_compile
- 对应 pytest
- 任务文件中指定的真实运行命令

完成后输出：
reports/<doc_id>/<SXXX>_implementation_report.md

报告必须包含：
1. 修改文件
2. 新增文件
3. 实现内容
4. 运行命令
5. 测试结果
6. 输出文件
7. 样例输出
8. 失败项
```

---

## 模板 5：单节验收模板

用于验收。

```text
/dogfood

任务：验收 section_id = <SXXX> 的实现结果。

读取：
- tasks/<doc_id>/<SXXX>_task.md
- reports/<doc_id>/<SXXX>_implementation_report.md

必须执行：
1. py_compile
2. pytest
3. 真实运行命令
4. 检查输出文件存在
5. 抽样打印输出内容
6. 检查关键字段存在
7. 检查是否违反安全边界

输出：
reports/<doc_id>/<SXXX>_acceptance_report.md

报告必须包含：
- PASS / FAIL
- 失败原因
- 需要修复的文件
- 是否允许进入下一节

规则：
如果 FAIL：
只修本节失败点，不允许进入下一节。
```

---

## 模板 6：失败修复模板

验收失败时使用。

```text
/codex

任务：只修复 section_id = <SXXX> 的验收失败项。

读取：
- reports/<doc_id>/<SXXX>_acceptance_report.md
- tasks/<doc_id>/<SXXX>_task.md

严格限制：
1. 只修 FAIL 项。
2. 不新增新功能。
3. 不重构无关模块。
4. 不进入下一节。
5. 修复后重新运行验收命令。

完成后更新：
reports/<doc_id>/<SXXX>_fix_report.md
```

---

## 模板 7：节间状态更新模板

每节 PASS 后用。

```text
/codebase_inspection

任务：完成 section_id = <SXXX> 后更新项目状态。

读取：
- tasks/<doc_id>/<SXXX>_task.md
- reports/<doc_id>/<SXXX>_acceptance_report.md

更新：
- SIKK_CHANGELOG.md
- SIKK_LESSONS_LEARNED.md
- SIKK_PROJECT_STATE.md
- SIKK_NEXT_TASK.md
- state/<doc_id>_progress.json

progress.json 必须记录：
{
  "doc_id": "...",
  "completed_sections": ["S001"],
  "current_section": "S002",
  "failed_sections": [],
  "last_completed_at": "...",
  "next_allowed_section": "S002"
}

禁止：
- 不改业务代码
- 不实现新功能

完成后输出：
SECTION_STATE_UPDATE_REPORT.md
```

---

# 四、总控命令：长时间计划

这是你可以直接给 Hermes 的主控命令。

```text
/background

任务：执行文档驱动型自动化落地流程。

当前目标：
把 share 文档中的内容逐节落实到 SIKK 项目中，但必须每次只处理一个标题，不允许一次性全读全改。

执行规则：

阶段 A：文档接收
1. 只读取 share 链接或原始文档。
2. 提取标题结构。
3. 生成 docs/imported/<doc_id>_outline.json。
4. 不改代码。

阶段 B：标题任务化
1. 每次只选择一个 section。
2. 生成 tasks/<doc_id>/<section_id>_task.md。
3. 不改代码。

阶段 C：单节执行
1. 根据 section task 生成 Repomix 上下文。
2. 只实现当前 section 相关改动。
3. 运行测试。
4. 验证输出。
5. 生成 acceptance report。

阶段 D：完成标记
1. PASS 后更新 progress.json。
2. 更新 SIKK_PROJECT_STATE.md。
3. 更新 SIKK_NEXT_TASK.md。
4. 再进入下一 section。

强制规则：
1. 每次只做一个 section。
2. 每个 section 必须有验收报告。
3. 验收失败不允许进入下一节。
4. 不允许真实 swap。
5. 不允许新增交易按钮。
6. 不允许删除已有模块。
7. 不允许一次性处理整篇文档。
8. 不允许只输出方案不落地。

当前先执行阶段 A。
完成后停止，并输出 DOC_IMPORT_REPORT.md。
```

---

# 五、标题执行的“状态机”

你可以让 Hermes 按这个状态机跑。

```text
PENDING
  ↓
OUTLINED
  ↓
TASK_CREATED
  ↓
CONTEXT_BUILT
  ↓
IMPLEMENTING
  ↓
TESTING
  ↓
ACCEPTED
  ↓
STATE_UPDATED
  ↓
NEXT_SECTION
```

失败状态：

```text
IMPLEMENT_FAILED
TEST_FAILED
OUTPUT_MISSING
SAFETY_BLOCKED
NEEDS_HUMAN_REVIEW
```

`state/<doc_id>_progress.json` 示例：

```json
{
  "doc_id": "sikk_interaction_doc_001",
  "status": "IN_PROGRESS",
  "current_section": "S003",
  "sections": {
    "S001": {
      "heading": "统一索引层",
      "status": "ACCEPTED",
      "acceptance_report": "reports/doc_001/S001_acceptance_report.md"
    },
    "S002": {
      "heading": "CLI 查询层",
      "status": "ACCEPTED",
      "acceptance_report": "reports/doc_001/S002_acceptance_report.md"
    },
    "S003": {
      "heading": "Telegram 点击交互",
      "status": "TASK_CREATED",
      "task_file": "tasks/doc_001/S003_task.md"
    }
  },
  "last_updated": "2026-05-03T00:00:00Z"
}
```

---

# 六、多模块怎么分工

你提到“多模板，多模块运用”，可以这样固定分工。

| 阶段 | Hermes 命令 / Skill | 作用 |
|---|---|---|
| 文档抓取 | `/conversation_transcript_ingestio` 或普通读取 | 读取 share 文档 |
| 标题识别 | `/codebase_inspection` | 不改代码，只建结构 |
| 任务板 | `/kanban` | 把标题转成任务 |
| 上下文打包 | Bash + Repomix | 打包相关代码 |
| 代码实现 | `/codex` | 写 Python / CLI / Bot |
| 前端实现 | `/claude_design` | Web 页面、Drawer、样式 |
| Web 测试 | `/dogfood` | 点击测试、UI 验收 |
| 长任务 | `/background` | 后台逐节跑 |
| 状态检查 | `/agents` | 看运行中任务 |
| 纠偏 | `/steer` | 不打断地修方向 |
| 停止 | `/stop` | 失控时停 |
| 回滚 | `/rollback` | 改坏文件时恢复 |
| 上下文压缩 | `/compress` | 每节结束后压缩 |
| Skill 重载 | `/reload_skills` | 修改 skill 后刷新 |

---

# 七、应用到你当前 SIKK 项目，标题顺序建议

你的交互系统文档可以按这个标题序列执行：

```text
S001：统一索引层 sikk_unified_view_builder.py
S002：CLI 查询层 sikkctl.py
S003：Case Quality Gate
S004：Paper Entry Snapshot
S005：Paper Lifecycle Case File
S006：Auto Review
S007：Telegram Callback Index
S008：Telegram Views
S009：Telegram Interactive Bot
S010：Web Token / Position Drawer
S011：Web Lifecycle Timeline
S012：Alert System
S013：Runtime 自动刷新
S014：Final Audit
```

必须先做：

```text
S001 → S002
```

因为 TG 和 Web 都要依赖统一索引。

---

# 八、每节验收必须有“真实样例”

以 S002 CLI 为例，验收不能只说“实现了”。

必须贴：

```bash
python3 sikkctl.py token LITH
```

真实输出必须包含：

```text
Token: LITH
Status: OPEN
Entry Time: 2026-04-28 17:46:00 UTC
Entry Price: 0.000021063508
Entry MC: UNKNOWN
Size: 0.085319 SOL
Current PnL: -13.8669%
Case Quality: LOW
Missing Fields:
- discovery_market_cap_usd
- entry_market_cap_usd
- entry_wallet_structure_status
Next Action:
BACKFILL_WALLET_AND_MARKET_CAP
```

没有真实样例，就不能算完成。

---

# 九、你可以直接发给 Hermes 的最终版

```text
/goal

当前长期目标：
建立 SIKK 文档驱动型自动化落地系统。

以后处理任何 share 文档或设计文档，都不能一次性全读全改。
必须按标题逐节执行。

固定流程：
1. 读取文档
2. 提取标题结构
3. 为每个标题生成 section_id
4. 每次只处理一个 section
5. 生成 section task
6. 用 Repomix 打包相关代码
7. 只实现当前 section
8. 跑测试
9. 验证输出
10. 生成 acceptance report
11. PASS 后更新 progress.jso


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 5. SIKK-SOL 专业交互系统

来源路径：`[1883]`；长度：9565


你截图里的 HER / Hermes 命令可以理解成 **4 类**：

```text
1. 会话管理命令：控制当前对话、上下文、模型、回滚
2. 任务调度命令：后台运行、查看 Agent、排队、长期目标
3. 工程执行 Skill：代码检查、Codex、Claude Code、设计、测试
4. 专用工具 Skill：GMGN、GitHub、Repomix/代码库、Hindsight、网页 UI 等
```

你现在做 SIKK-SOL，最重要的不是把所有命令都用上，而是形成固定工作流。

---

# 一、最核心的 Hermes 系统命令

## 1. `/new`

作用：

```text
开启一个全新会话。
清空当前会话历史。
适合重新开始一个完全独立任务。
```

SIKK 用法：

```text
当你要从“纸面交易优化”切换到“Telegram 交互系统”时，可以 /new。
```

但一般不要频繁用，容易丢上下文。

---

## 2. `/branch`

作用：

```text
从当前会话创建分支。
保留当前上下文，但可以走另一条路线。
```

SIKK 用法：

```text
当前主线：纸面交易系统
分支 1：Telegram 点击交互
分支 2：Web Visual Console
分支 3：Repomix + Hermes 工作流
```

你现在很适合用 `/branch`，因为 SIKK 已经不是单线任务。

---

## 3. `/compress`

作用：

```text
手动压缩当前对话上下文。
防止上下文太长导致 Agent 变笨。
```

SIKK 用法：

```text
每完成一个 Phase 后执行 /compress。
例如：
Phase 1 unified index 完成 → /compress
Phase 2 sikkctl 完成 → /compress
```

---

## 4. `/rollback`

作用：

```text
查看或恢复文件系统 checkpoint。
如果 Agent 改坏代码，可以回滚。
```

SIKK 用法：

```text
Codex 大改后测试失败、文件乱了，用 /rollback。
```

这是高价值命令。

---

## 5. `/stop`

作用：

```text
停止所有正在运行的后台任务。
```

SIKK 用法：

```text
如果 /background 长任务跑偏，或者 Agent 一直循环改代码，立刻 /stop。
```

---

## 6. `/approve` 和 `/deny`

作用：

```text
/approve：批准一个被标记为危险的命令
/deny：拒绝危险命令
```

SIKK 用法：

```text
涉及 rm、修改系统服务、安装包、重启、写环境变量时，Hermes 可能要求批准。
```

你的项目里涉及真实交易边界，遇到任何 swap / private key / gmgn_swap 类动作，默认 `/deny`。

---

# 二、任务调度命令

## 1. `/background`

作用：

```text
把一个 prompt 放到后台运行。
适合长时间任务。
```

SIKK 用法：

```text
/background

执行 Phase 1：统一索引层。
只实现 sikk_unified_view_builder.py 和测试。
完成后输出报告，不进入 Phase 2。
```

注意：

```text
/background 不是让它无限干活。
必须给明确边界。
```

---

## 2. `/agents`

作用：

```text
查看当前活跃 Agent 和后台任务。
```

SIKK 用法：

```text
你启动 /background 后，用 /agents 看它是否还在跑。
```

---

## 3. `/queue`

作用：

```text
把下一条 prompt 排队，不打断当前运行。
```

SIKK 用法：

```text
当前 Agent 正在跑测试。
你可以 /queue 追加：
完成后请输出失败项和下一步，不要继续扩展功能。
```

---

## 4. `/steer`

作用：

```text
在下一次工具调用后插入一条引导信息，不直接中断任务。
```

SIKK 用法：

```text
Agent 跑着跑着方向偏了，可以 /steer：

注意：不要新增真实交易按钮，只修复 sikkctl.py token LITH 的输出字段。
```

---

## 5. `/goal`

作用：

```text
设置长期目标，Hermes 会跨轮次保持目标。
```

SIKK 用法：

```text
/goal

SIKK 当前长期目标：
把系统从文件分散、命令分散，升级为统一索引 + CLI + Telegram 点击 + Web 可视化 + 自动复盘的专业交互系统。
严格禁止真实 swap。
当前第一验收目标：python3 sikkctl.py token LITH 可以一条命令显示完整纸面实战信息。
```

这个命令非常适合你当前项目。

---

## 6. `/status`

作用：

```text
查看当前 session 信息。
```

用来确认当前会话是否还是你正在工作的那个 SIKK 分支。

---

## 7. `/resume`

作用：

```text
恢复之前命名过的 session。
```

配合 `/title` 使用。

建议你给 SIKK 会话命名：

```text
/title SIKK Professional Interaction System
```

后面可以 `/resume` 回来。

---

# 三、模型和运行控制命令

## 1. `/model`

作用：

```text
切换当前会话模型。
```

SIKK 用法：

```text
复杂代码生成：选择强代码模型
审计 / 架构理解：选择强推理模型
简单命令生成：可用较快模型
```

---

## 2. `/reasoning`

作用：

```text
调整 reasoning effort 和显示设置。
```

SIKK 用法：

```text
做系统设计、审计、复杂 bug 排查时，提高 reasoning。
做小修、小命令时降低。
```

---

## 3. `/fast`

作用：

```text
切换快速模式。
```

SIKK 用法：

```text
查状态、看文件、跑小命令可以 fast。
复杂代码生成不要随便 fast。
```

---

## 4. `/yolo`

作用：

```text
跳过危险命令审批。
```

对你当前项目：

```text
不建议开启。
```

原因：

```text
你的项目里有 GMGN、swap、交易相关 skill。
/yolo 可能让危险操作少一道确认。
```

SIKK 目前仍然是 paper + human confirmation 阶段，不要让执行层失控。

---

# 四、维护类命令

## 1. `/reload_skills`

作用：

```text
重新扫描 ~/.hermes/skills/。
新增或修改 skill 后使用。
```

SIKK 用法：

```text
你修改了 sikk-gmgn-structural-intelligence skill 后，执行 /reload_skills。
```

---

## 2. `/reload_mcp`

作用：

```text
重新加载 MCP servers。
```

SIKK 用法：

```text
如果你接了 GitHub、文件系统、数据库、GMGN 或其他 MCP 工具，配置改完后用。
```

---

## 3. `/curator`

作用：

```text
后台 skill 维护，包括 status、run、pin、archive。
```

SIKK 用法：

```text
整理长期 skill、固定关键 skill、归档过时 skill。
```

不是你现在最优先的命令。

---

## 4. `/debug`

作用：

```text
上传 debug report，包含系统信息和日志。
```

SIKK 用法：

```text
Hermes 网关异常、TG 不响应、命令菜单卡住、MCP 不加载时用。
```

---

## 5. `/restart`

作用：

```text
优雅重启 gateway。
```

SIKK 用法：

```text
Hermes 长时间卡住、菜单不刷新、命令不响应，可以 /restart。
```

---

# 五、你截图里的工程类 Skill

这些是你最该用的。

## 1. `/codebase_inspection`

作用：

```text
检查代码库结构、文件、依赖、行数。
通常适合“只看不改”。
```

SIKK 用法：

```text
/codebase_inspection

只检查 SIKK 项目中与 Telegram 交互有关的文件，不修改代码。
输出当前已有模块、缺失模块、应该修改哪些文件、验收命令。
```

这是每个 Phase 的第一步。

---

## 2. `/codex`

作用：

```text
委托 OpenAI Codex CLI 做代码实现。
适合写 Python、测试、CLI、数据聚合逻辑。
```

SIKK 用法：

```text
/codex

实现 sikk_unified_view_builder.py 和 tests/test_sikk_unified_view_builder.py。
只允许修改这两个文件。
完成后运行 py_compile、pytest、真实生成 index。
```

适合：

```text
sikkctl.py
sikk_unified_view_builder.py
sikk_telegram_callback_index.py
sikk_paper_auto_reviewer.py
```

---

## 3. `/claude_code`

作用：

```text
委托 Claude Code CLI 做代码任务。
```

SIKK 用法：

```text
可用于大范围代码理解、重构、前端交互、长文件修改。
```

但你要强约束它：

```text
只改指定文件，不允许重构交易核心。
```

---

## 4. `/claude_design`

作用：

```text
设计一次性 HTML artifact / 页面。
```

SIKK 用法：

```text
适合重做 Visual Console 页面：
index.html
app.js
style.css
```

不适合写 paper runner 核心逻辑。

---

## 5. `/dogfood`

作用：

```text
对 web app 做探索测试，找 bug。
```

SIKK 用法：

```text
Web Visual Console 做完后，用 /dogfood 测试：
点击 Token
点击 Position
打开 Drawer
检查 JS 报错
检查搜索筛选
```

---

## 6. `/github_code_review`

作用：

```text
审查 PR / diff / inline comments。
```

SIKK 用法：

```text
如果你把 SIKK 放到 GitHub，改完一个 Phase 后可以审查 diff。
```

---

## 7. `/github_auth`

作用：

```text
GitHub 登录 / token / SSH 设置。
```

和 SIKK 代码托管有关，不是日常核心。

---

# 六、GMGN 相关命令理解

截图里有：

```text
/gmgn_market
/gmgn_portfolio
/gmgn_token
/gmgn_track
/gmgn_swap
/gmgn_cooking
```

## 可以用的只读类

### `/gmgn_market`

```text
查 crypto / meme token 价格、图表、市场信息。
```

### `/gmgn_portfolio`

```text
分析钱包地址。
```

### `/gmgn_token`

```text
研究某个 crypto / meme token。
```

### `/gmgn_track`

```text
获取实时买卖活动。
```

这些可以用于研究和数据理解。

---

## 高风险类

### `/gmgn_swap`

```text
[FINANCIAL EXECUTION] 买卖 meme token。
```

### `/gmgn_cooking`

```text
[FINANCIAL EXECUTION] 创建 / launch 相关。
```

你当前阶段不建议使用这两个。

SIKK 当前边界应该是：

```text
paper only
paper + human confirmation
不自动真实 swap
不使用 gmgn_swap
```

---

# 七、Repomix 不是菜单命令，是 Bash 命令

你截图背景里有：

```bash
./make_ai_context.sh index
```

这是正确方向。

它不是 HER slash 命令，而是 shell 命令。

正确组合是：

```text
Bash 跑 Repomix 打包代码上下文
Hermes 读取 ai_context/*.xml
Codex 根据上下文写代码
Dogfood / pytest 验收
```

你的标准流程应该是：

```bash
cd /root/sikk-gmgn
./make_ai_context.sh index
```

然后给 Hermes：

```text
/codebase_inspection

读取 ai_context/sikk_phase1_unified_index.xml。
只做侦察，不修改代码。
输出 Phase 1 Readiness Report。
```

再：

```text
/codex

读取 ai_context/sikk_phase1_unified_index.xml 和 Phase 1 报告。
实现 sikk_unified_view_builder.py。
运行验收命令。
```

---

# 八、你当前 SIKK 最推荐的命令组合

## 第一套：做一个阶段开发

```text
/branch
/title SIKK Phase 1 Unified Index
/goal
/codebase_inspection
/codex
/dogfood 或 pytest 验收
/compress
```

---

## 第二套：长任务但不失控

```text
/background
/agents
/queue
/steer
/stop
/rollback
```

用法：

```text
/background 执行 Phase 1
/agents 看状态
/steer 纠偏
/stop 停止失控任务
/rollback 回滚坏改动
```

---

## 第三套：Web 面板开发

```text
/claude_design
/dogfood
/codebase_inspection
```

---

## 第四套：代码实现

```text
/codebase_inspection
/codex
/rollback
```

---

## 第五套：Skill 维护

```text
/hermes_agent_skill_authoring
/reload_skills
/curator
```

---

# 九、按你的 SIKK 目标，命令使用顺序应该是这样

## Step 1：新建分支

```text
/branch

创建 SIKK Professional Interaction System 分支。
本分支只做统一索引、CLI、TG 点击、Web 点击和自动复盘入口。
禁止真实 swap。
```

---

## Step 2：设置长期目标

```text
/goal

当前目标：
实现 SIKK 专业交互系统。
第一硬验收：
python3 sikkctl.py token LITH
必须一条命令显示 LITH 的入场时间、入场价格、仓位 SOL、当前收益、case_quality、缺失字段、next_action、case file 路径。
```

---

## Step 3：先跑 Repomix

这是 Bash，不是 slash：

```bash
cd /root/sikk-gmgn
./make_ai_context.sh index
```

---

## Step 4：让 Hermes 只侦察

```text
/codebase_inspection

读取 ai_context/sikk_phase1_unified_index.xml。
只检查，不修改代码。
输出：
1. 当前数据流
2. 现有字段来源
3. 需要实现哪些文件
4. Phase 1 验收命令
```

---

## Step 5：让 Codex 实现

```text
/codex

根据 Phase 1 报告实现 sikk_unified_view_builder.py。
只允许新增/修改：
- sikk_unified_view_builder.py
- tests/test_sikk_unified_view_builder.py

完成后运行真实验收命令。
```

---

## Step 6：验证

```text
/dogfood

验证 Phase 1。
必须运行：
python3 sikk_unified_view_builder.py ...
检查 index 文件是否生成。
检查 LITH 是否进入 token_detail_index。
```

---

## Step 7：压缩上下文

```text
/compress
```

---

# 十、你不应该乱用的命令

## `/yolo`

不建议。

原因：

```text
会跳过危险命令审批。
SIKK 有金融执行边界，不适合。
```

## `/gmgn_swap`

当前不要用。

```text
它是金融执行。
你现在仍是 paper / human confirmation 阶段。
```

## `/approve`

不要随便点。

```text
涉及 swap、private key、webhook、rm -rf、系统服务修改，先看清楚。
```

---

# 十一、你现在输入“列出可用的”是对的，但下一步应该这样问

不要只问：

```text
列出可用的
```

要问 Hermes：

```text
/commands

只筛选并解释与当前 SIKK 项目相关的命令：
- 代码库检查
- Codex 开发
- Claude 设计
- 后台任务
- Agent 状态
- 回滚
- Telegram / Web / GitHub / GMGN 相关
并给出每个命令在 SIKK Phase 1-8 中的使用场景。
```

---

# 十二、给你一份 SIKK 命令速查表

| 命令 | 用途 | SIKK 用法 |
|---|---|---|
| `/branch` | 开分支 | 每个大方向单独分支 |
| `/goal` | 长期目标 | 固定 SIKK 总目标 |
| `/background` | 后台长任务 | 每个 Phase 长跑 |
| `/agents` | 看任务 | 监控后台 Agent |
| `/stop` | 停止任务 | Agent 跑偏时停 |
| `/rollback` | 回滚 | 改坏代码时恢复 |
| `/compress` | 压缩上下文 | 每个 Phase 完成后用 |
| `/codebase_inspection` | 只看代码 | 每个 Phase 开始前用 |
| `/codex` | 写代码 | Python / CLI / 索引层 |
| `/claude_design` | 做前端 | Web Visual Console |
| `/dogfood` | 测试 Web | 点击、抽屉、筛选 |
| `/reload_skills` | 重载 skill | 修改 skill 后用 |
| `/debug` | 故障报告 | Hermes 异常时用 |
| `/restart` | 重启网关 |


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 6. SIKK-SOL 专业交互系统

来源路径：`[2288]`；长度：14910


可以。**Repomix 正好补上 Hermes 当前最大短板：让 AI 一次性理解项目代码结构，但又不把整个聊天上下文塞爆。**

它的定位不是替代 Hermes，而是作为：

```text
Repomix = 代码库压缩/打包层
Hermes = Agent 调度/执行层
tmux = 进程隔离层
SIKK_PROJECT_STATE.md = 长期记忆层
```

Repomix 官方定位就是把整个代码库打包成一个适合 AI 阅读的文件；它支持 token 统计、包含/排除规则、`.gitignore` / `.repomixignore`、Secretlint 安全检查、`--compress` 压缩，以及把特定文件列表通过 stdin 传入打包。citeturn229613view0turn282889view0

---

# 一、Repomix 在 SIKK 里的正确作用

你之前的问题是：

```text
Hermes 只看到你当前说的话
但它不一定真正理解：
- 当前有哪些文件
- 哪些模块已经实现
- 字段在哪里生成
- Telegram / Web / CLI / paper runner 之间怎么接
- 哪些文件不能乱改
```

Repomix 可以解决：

```text
把当前代码库按任务打包成 AI-friendly 上下文文件
让 Hermes / Codex / Claude Code 先读完整代码上下文
再开始修改
```

但是要注意：

> **不要每次都把整个 `/root/sikk-gmgn` 全部打包给 AI。**

正确方式是：

```text
按阶段打包
按任务打包
按文件组打包
```

例如：

```text
Phase 1：统一索引层，只打包 paper / dashboard / case / index 相关文件
Phase 2：CLI，只打包 index + sikkctl 相关文件
Phase 3：Telegram，只打包 tg bot / views / index 相关文件
Phase 4：Web，只打包 dashboard site 相关文件
```

---

# 二、先安装 Repomix

在 VPS 上执行：

```bash
cd /root/sikk-gmgn

npx repomix@latest --version
```

如果你要长期用：

```bash
npm install -g repomix
repomix --version
```

官方文档给出的快速运行方式是 `npx repomix@latest`，全局安装可用 `npm install -g repomix`，默认会生成 `repomix-output.xml`。citeturn282889view0

---

# 三、必须先创建 `.repomixignore`

这是关键。  
你的项目里有日志、数据、Telegram、可能还有配置文件，不能直接全打包。

在 `/root/sikk-gmgn` 创建：

```bash
nano .repomixignore
```

写入：

```gitignore
# runtime data
data/gmgn_candidates_live_run/**/*.json
data/gmgn_candidates_live_run/**/*.jsonl
data/gmgn_candidates_live_run/**/*.csv
data/gmgn_candidates_live_run/**/*.md
data/gmgn_candidates_live_run/site/**
data/gmgn_candidates_live_run/index/**
data/gmgn_candidates_live_run/telegram/**

# logs / cache
*.log
__pycache__/
.pytest_cache/
.mypy_cache/
.cache/
tmp/
temp/

# secrets / env
.env
.env.*
*.key
*.pem
*.secret
*secret*
*private*
*token*
*webhook*
*api_key*

# venv / deps
venv/
.venv/
node_modules/

# git
.git/
```

原因：

```text
Repomix 负责给 AI 看代码，不负责给 AI 看全部运行数据。
运行数据应该通过抽样文件、sikkctl 输出、readiness report 单独提供。
```

Repomix 虽然有 Secretlint 安全检查，但你不能完全依赖工具自动过滤敏感内容；必须先用 `.repomixignore` 主动排除敏感目录和运行数据。Repomix 官方也强调它支持 `.repomixignore` / `.gitignore` 规则和 Secretlint 安全检查。citeturn282889view0

---

# 四、SIKK 推荐的 Repomix 打包目录

建议新建一个上下文目录：

```bash
mkdir -p /root/sikk-gmgn/ai_context
```

以后所有 Repomix 输出放这里：

```text
ai_context/
  sikk_full_architecture.xml
  sikk_phase1_unified_index.xml
  sikk_phase2_cli.xml
  sikk_phase3_telegram.xml
  sikk_phase4_web_console.xml
  sikk_phase5_runtime_integration.xml
```

---

# 五、不要全量打包，按任务打包

## 1. 全局结构侦察包

只在开始时做一次：

```bash
cd /root/sikk-gmgn

repomix \
  --compress \
  --output ai_context/sikk_full_architecture.xml \
  --ignore "data/**,*.log,__pycache__/**,.pytest_cache/**,node_modules/**,venv/**,.venv/**"
```

用途：

```text
给 Hermes 做总览侦察
不是直接让它改代码
```

`--compress` 会用 Tree-sitter 提取关键代码元素，减少 token，同时保留结构，这适合让 AI 快速理解大型代码库。citeturn282889view0

---

## 2. Phase 1：统一索引层上下文包

```bash
cd /root/sikk-gmgn

repomix \
  --include "sikk_paper_live_runner.py,sikk_dashboard_site_builder.py,sikk_paper_lifecycle_recorder.py,sikk_paper_explanation_builder.py,sikk_paper_auto_reviewer.py,sikk_wallet_structure_gate.py,sikk_wallet_structure_snapshot.py,tests/test_sikk_paper_live_runner.py,tests/test_sikk_dashboard_site_builder.py,tests/test_sikk_paper_auto_reviewer.py" \
  --output ai_context/sikk_phase1_unified_index.xml
```

用途：

```text
让 Hermes 理解：
- paper position 数据在哪里
- case file 怎么生成
- dashboard_data 怎么生成
- wallet 字段在哪里
然后实现 sikk_unified_view_builder.py
```

Repomix 支持 `--include` 指定 glob / 文件，`--ignore` 排除路径。citeturn282889view0

---

## 3. Phase 2：CLI 查询层上下文包

```bash
cd /root/sikk-gmgn

repomix \
  --include "sikk_unified_view_builder.py,sikkctl.py,tests/test_sikk_unified_view_builder.py,tests/test_sikkctl.py,SIKK_PROJECT_STATE.md,SIKK_NEXT_TASK.md,SIKK_LESSONS_LEARNED.md" \
  --output ai_context/sikk_phase2_cli.xml
```

用途：

```text
实现 / 修复：
python3 sikkctl.py token LITH
python3 sikkctl.py open
python3 sikkctl.py position <id>
```

---

## 4. Phase 3：Telegram 交互层上下文包

```bash
cd /root/sikk-gmgn

repomix \
  --include "sikk_unified_view_builder.py,sikkctl.py,sikk_telegram_interactive_bot.py,sikk_telegram_views.py,sikk_telegram_callback_index.py,tests/test_sikk_telegram_views.py,tests/test_sikk_telegram_callback_index.py" \
  --output ai_context/sikk_phase3_telegram.xml
```

用途：

```text
实现：
/sikk
/sikk_open
点击 LITH
点击 Position
点击 Case File
```

---

## 5. Phase 4：Web Visual Console 上下文包

```bash
cd /root/sikk-gmgn

repomix \
  --include "sikk_dashboard_site_builder.py,sikk_unified_view_builder.py,data/gmgn_candidates_live_run/site/index.html,data/gmgn_candidates_live_run/site/app.js,data/gmgn_candidates_live_run/site/style.css,tests/test_sikk_dashboard_site_builder.py" \
  --output ai_context/sikk_phase4_web_console.xml
```

用途：

```text
让 Web 读取统一 index
Token 可点击
Position 可点击
显示 Lifecycle / Evidence / Journal / Review
```

---

# 六、更专业：用 `git ls-files` 精确打包

Repomix 支持通过 stdin 输入文件列表。官方示例包括 `git ls-files "*.ts" | repomix --stdin`，这种方式适合精确控制哪些文件给 AI。citeturn282889view0

你可以给 SIKK 创建文件清单：

```bash
cat > ai_context/phase1_files.txt <<'EOF'
sikk_paper_live_runner.py
sikk_dashboard_site_builder.py
sikk_paper_lifecycle_recorder.py
sikk_paper_explanation_builder.py
sikk_paper_auto_reviewer.py
sikk_wallet_structure_gate.py
sikk_wallet_structure_snapshot.py
tests/test_sikk_paper_live_runner.py
tests/test_sikk_dashboard_site_builder.py
tests/test_sikk_paper_auto_reviewer.py
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
SIKK_LESSONS_LEARNED.md
SIKK_CHANGELOG.md
EOF
```

然后：

```bash
cd /root/sikk-gmgn

cat ai_context/phase1_files.txt | repomix --stdin \
  --output ai_context/sikk_phase1_unified_index.xml
```

这个比 `--include` 更稳。

---

# 七、Repomix + Hermes 的标准工作流

## 第 1 层：tmux 隔离

```bash
tmux new -s sikk-builder -c /root/sikk-gmgn
```

---

## 第 2 层：生成 Repomix 上下文

```bash
cd /root/sikk-gmgn

cat ai_context/phase1_files.txt | repomix --stdin \
  --output ai_context/sikk_phase1_unified_index.xml
```

---

## 第 3 层：让 Hermes 先读上下文，不写代码

复制给 Hermes：

```text
/codebase_inspection

请先读取 ai_context/sikk_phase1_unified_index.xml。

任务：
只做代码库侦察，不修改代码。

目标：
理解当前 SIKK paper runner、case file、dashboard builder、wallet structure 之间的数据流。

必须输出：
1. 当前 paper position 字段在哪里生成
2. case file 字段在哪里生成
3. dashboard_data.json 字段在哪里生成
4. 哪些字段可以用于统一索引
5. 实现 sikk_unified_view_builder.py 需要读取哪些文件
6. Phase 1 需要修改哪些文件
7. 验收命令

输出：
SIKK_REPOMIX_PHASE1_READINESS_REPORT.md

禁止修改代码。
```

---

## 第 4 层：让 Hermes 开发

```text
/codex

请读取：
1. ai_context/sikk_phase1_unified_index.xml
2. SIKK_REPOMIX_PHASE1_READINESS_REPORT.md

执行 Phase 1：
实现 sikk_unified_view_builder.py 和 tests/test_sikk_unified_view_builder.py。

严格目标：
生成：
data/gmgn_candidates_live_run/index/system_index.json
data/gmgn_candidates_live_run/index/token_detail_index.json
data/gmgn_candidates_live_run/index/position_index.json
data/gmgn_candidates_live_run/index/case_file_index.json
data/gmgn_candidates_live_run/index/alert_index.json

验收：
python3 -m py_compile sikk_unified_view_builder.py
python3 sikk_unified_view_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/index

完成后必须贴出：
- 修改文件列表
- 运行命令
- index 文件列表
- position 数量
- token 数量
- LITH 是否进入索引
- 失败项

禁止：
- 真实 swap
- 交易按钮
- 删除已有模块
- 修改真实交易逻辑
```

---

# 八、Repomix 在长任务中的正确分工

你之前说要“长时间计划”。  
用 Repomix 后，可以这样分：

```text
Phase 0：全局 Repomix 包 → 架构侦察
Phase 1：索引层 Repomix 包 → 实现 unified index
Phase 2：CLI Repomix 包 → 实现 sikkctl
Phase 3：TG Repomix 包 → 实现 telegram views / bot
Phase 4：Web Repomix 包 → 实现 Visual Console
Phase 5：Runtime Repomix 包 → 接入主流程
Phase 6：Diff Repomix 包 → 审计改动
```

---

# 九、用 Repomix 做变更审计

Repomix 支持包含 git logs 和 diffs；官方文档给出 `--include-logs`、`--include-diffs` 的用法。citeturn282889view0

每个 Phase 完成后，生成一个“改动审计包”：

```bash
cd /root/sikk-gmgn

repomix \
  --include-logs \
  --include-diffs \
  --output ai_context/sikk_phase1_diff_review.xml
```

然后给 Hermes：

```text
/codebase_inspection

请读取 ai_context/sikk_phase1_diff_review.xml。

任务：
审计 Phase 1 改动。

检查：
1. 是否新增真实交易功能
2. 是否删除已有模块
3. 是否破坏 paper runner
4. 是否破坏 dashboard builder
5. 是否生成 index 文件
6. 是否有测试
7. 是否有安全风险
8. 是否符合 Phase 1 目标

只输出审计报告，不修改代码。
```

---

# 十、给 SIKK 创建 Repomix 配置文件

执行：

```bash
cd /root/sikk-gmgn
repomix --init
```

Repomix 官方支持 `repomix --init` 初始化配置。citeturn282889view0

然后你可以维护：

```text
repomix.config.json
```

建议策略：

```json
{
  "output": {
    "filePath": "ai_context/repomix-output.xml",
    "style": "xml"
  },
  "ignore": {
    "customPatterns": [
      "data/**",
      "*.log",
      "__pycache__/**",
      ".pytest_cache/**",
      "node_modules/**",
      "venv/**",
      ".venv/**",
      ".env",
      ".env.*",
      "*secret*",
      "*private*",
      "*token*",
      "*webhook*",
      "*api_key*"
    ]
  },
  "security": {
    "enableSecurityCheck": true
  }
}
```

字段名可能随版本变化，实际以 `repomix --init` 生成的配置结构为准；你可以让 Hermes 先读取生成后的 `repomix.config.json` 再微调。

---

# 十一、推荐新增脚本：`make_ai_context.sh`

创建：

```bash
nano /root/sikk-gmgn/make_ai_context.


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 7. SIKK-SOL 专业交互系统

来源路径：`[2486]`；长度：19455


可以。你现在应该用 **“目标倒推 + 多层 Hermes 命令 + 长任务分段验收”** 的方式来发布任务。

核心原则：

```text
不要再让 Hermes 做“一个大任务”。
要让 Hermes 按目标拆成多个阶段，每个阶段必须有：
目标 → 文件 → 命令 → 输出 → 验收 → 失败修复 → 更新记录
```

下面这套可以直接复制到 Hermes / TG 里使用。

---

# 一、总目标定义

先在 Hermes 里设置长期目标。

```text
/goal

SIKK-SOL 当前长期目标：

把 SIKK-SOL 从“模块堆叠系统”升级为“专业交互式策略验证系统”。

最终目标不是简单展示数据，而是做到：

1. 一个命令可以查看系统状态。
2. 一个命令可以查看开放纸面仓位。
3. 一个命令可以查看某个 token 的完整实战信息。
4. Telegram 可以点击进入开放仓位、Token、Position、Case File、Auto Review。
5. Web Visual Console 可以点击 Token / Position，查看生命周期、入场证据、钱包证据、持仓记录、自动复盘。
6. 每笔纸面仓位都能回答：
   - 什么时候发现
   - 发现时市值
   - 什么时候入场
   - 入场时市值
   - 买了多少 SOL
   - 估算买了多少 token
   - 为什么入场
   - 为什么持有
   - 为什么退出
   - 策略哪里有不足
   - 下一步该怎么调整
7. 所有入口必须读取统一索引，不允许各自去读分散文件。

严格边界：

- 不执行真实 swap
- 不新增交易按钮
- 不新增 execute / approve / broadcast 按钮
- 不读取私钥
- 不写入私钥
- 不删除已有模块
- 不破坏 sikk_live_run.py 主入口
- 不破坏 paper runner 交易逻辑
- 本阶段只做查询、展示、复盘、诊断、交互优化

当前首要验收目标：

python3 sikkctl.py token LITH

必须一条命令显示：
- LITH 当前状态
- 入场时间
- 入场价格
- 入场市值
- 仓位 SOL
- 当前收益
- case_quality
- evidence_missing_fields
- next_action
- case file 路径
```

---

# 二、开独立任务分支

```text
/branch

创建 SIKK Professional Interaction System 分支。

本分支只处理交互系统专业化，不改真实交易逻辑。

目标：
实现统一索引层、CLI 查询层、Telegram 点击交互层、Web Visual Console 点击详情层、Case File / Auto Review 入口和 Alert System。

禁止：
- 真实 swap
- 交易按钮
- 自动实盘
- 删除已有模块
- 大规模无关重构
```

---

# 三、创建任务板

```text
/kanban

创建 SIKK Professional Interaction System 任务板。

任务必须按阶段执行，不允许一次性大爆改。

Phase 0：项目侦察
- 检查当前数据文件、代码文件、Telegram 广播、Web dashboard、paper case file 是否存在。
- 输出 SIKK_INTERACTION_READINESS_REPORT.md。
- 不修改代码。

Phase 1：统一索引层
- 新增 sikk_unified_view_builder.py。
- 输出 index/system_index.json、token_detail_index.json、position_index.json、case_file_index.json、alert_index.json。
- 所有交互入口后续必须读取 index。

Phase 2：CLI 查询层
- 新增 sikkctl.py。
- 支持 status、latest、open、token、position、case、review、health、rebuild-index。
- 必须以 LITH 作为验收样本。

Phase 3：Telegram Callback Index + Views
- 新增 sikk_telegram_callback_index.py。
- 新增 sikk_telegram_views.py。
- 生成 callback_index.json。
- 实现主菜单、开放仓位、Token 详情、Position 详情、Case File 摘要视图。

Phase 4：Telegram Interactive Bot
- 新增 sikk_telegram_interactive_bot.py。
- 实现 /sikk、/sikk_open、/sikk_token、/sikk_position、callback query。
- Telegram 只做查询，不做交易。

Phase 5：Web Visual Console 交互升级
- Web 读取统一 index。
- Token 可点击。
- Position 可点击。
- Drawer 增加 Overview / Lifecycle / Evidence / Journal / Review。
- LOW quality 和 HOLD_WITH_DATA_RISK 高亮。

Phase 6：Case Quality + Auto Review 接入
- 每笔 position 显示 case_quality、strategy_review_eligible、evidence_missing_fields、next_action。
- LITH 必须显示 LOW + HOLD_WITH_DATA_RISK + BACKFILL_WALLET_AND_MARKET_CAP。

Phase 7：Alert System
- 生成 alert_index.json。
- 支持 NEW_PAPER_ENTRY、PAPER_EXIT、HOLD_WITH_DATA_RISK、DATA_BACKFILL_REQUIRED、CASE_QUALITY_LOW、BIG_WIN、BIG_LOSS、FALSE_EXIT_SUSPECTED。

Phase 8：Runtime Integration
- sikk_live_run.py 每轮结束后自动刷新 index 和 dashboard。
- 失败不能中断主流程，只写事件。

Phase 9：测试与审计
- py_compile
- pytest
- 安全 grep
- 输出最终审计报告

每个 Phase 完成后必须输出：
1. 修改文件列表
2. 运行命令
3. 真实输出样例
4. 验收是否通过
5. 失败项
6. 下一步
```

---

# 四、长时间执行总控命令

这个适合你让 Hermes 按多小时任务运行。

```text
/background

执行 SIKK Professional Interaction System 长任务，但必须分阶段推进，不能一次性重构。

执行规则：

1. 每次只执行一个 Phase。
2. 每个 Phase 完成后必须停止并输出验收报告。
3. 每个 Phase 必须真实运行命令，不允许只描述方案。
4. 如果某个 Phase 失败，只修失败点，不允许扩展新功能。
5. 每个 Phase 都要更新：
   - SIKK_CHANGELOG.md
   - SIKK_LESSONS_LEARNED.md
   - 对应 PHASE_REPORT.md

当前从 Phase 0 开始：
只做项目侦察，不修改代码。

完成 Phase 0 后输出：
SIKK_INTERACTION_READINESS_REPORT.md
```

之后用：

```text
/agents
```

看运行状态。

如果发现它乱改，马上：

```text
/stop
```

---

# 五、Phase 0：侦察命令

先不要写代码。

```text
/codebase_inspection

Phase 0：SIKK 交互系统侦察。

只检查，不修改任何代码。

检查项目目录：
/root/sikk-gmgn

检查内容：

1. 当前是否存在：
- sikk_live_run.py
- sikk_paper_live_runner.py
- sikk_dashboard_site_builder.py
- sikk_paper_lifecycle_recorder.py
- sikk_paper_explanation_builder.py
- sikk_paper_auto_reviewer.py
- sikk_unified_view_builder.py
- sikkctl.py
- sikk_telegram_interactive_bot.py
- sikk_telegram_views.py
- sikk_telegram_callback_index.py

2. 当前是否存在数据：
- data/gmgn_candidates_live_run/paper_live/paper_positions_open.json
- data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json
- data/gmgn_candidates_live_run/paper_live/case_files/
- data/gmgn_candidates_live_run/paper_live/auto_reviews/
- data/gmgn_candidates_live_run/tokens/*/token_status.json
- data/gmgn_candidates_live_run/wallet_structure/*/wallet_structure_decision.json
- data/gmgn_candidates_live_run/events/live_events.jsonl
- data/gmgn_candidates_live_run/site/
- data/gmgn_candidates_live_run/index/

3. 检查 LITH 是否存在于：
- paper open
- paper closed
- case files
- auto reviews
- token index
- dashboard data

4. 输出报告：
SIKK_INTERACTION_READINESS_REPORT.md

报告必须包含：
- 已有模块
- 缺失模块
- 已有数据
- 缺失数据
- LITH 当前能否被统一查询
- 当前最小落地路径
- Phase 1 应修改哪些文件
- Phase 1 验收命令

禁止修改任何代码。
```

---

# 六、Phase 1：统一索引层命令

```text
/codex

Phase 1：实现 SIKK 统一索引层。

目标：
新增 sikk_unified_view_builder.py，把分散的 paper、token、wallet、case、review、event 数据聚合成统一 index，供 CLI、TG、Web 共同读取。

新增文件：
- sikk_unified_view_builder.py
- tests/test_sikk_unified_view_builder.py

输出目录：
data/gmgn_candidates_live_run/index/

输出文件：
- system_index.json
- token_detail_index.json
- position_index.json
- latest_open_positions.json
- latest_closed_positions.json
- case_file_index.json
- auto_review_index.json
- alert_index.json

读取来源：
- paper_live/paper_positions_open.json
- paper_live/paper_positions_closed.json
- paper_live/paper_trades.csv
- paper_live/case_files/*.json
- paper_live/auto_reviews/*.json
- tokens/*/token_status.json
- wallet_structure/*/wallet_structure_decision.json
- events/live_events.jsonl

position_index.json 每个 position 必须包含：
- position_id
- token_symbol
- token_address
- status
- strategy_name
- signal_level
- signal_type
- candidate_discovered_at
- discovery_market_cap_usd
- signal_time
- signal_market_cap_usd
- wallet_decision_time
- entry_wallet_structure_status
- entry_wallet_structure_score
- entry_wallet_risk_score
- entry_counterparty_pressure_score
- paper_entry_time
- entry_price
- entry_market_cap_usd
- paper_size_sol
- paper_size_usd
- estimated_token_amount
- current_price
- current_market_cap_usd
- exit_time
- exit_price
- exit_market_cap_usd
- unrealized_pnl_pct
- net_pnl_pct
- max_floating_profit_pct
- max_drawdown_pct
- case_quality
- strategy_review_eligible
- evidence_missing_fields
- paper_action
- next_action
- case_file_json
- case_file_md
- auto_review_json
- auto_review_md

token_detail_index.json 每个 token 必须包含：
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
- latest_auto_review_md
- case_quality_distribution
- positions
- recent_events
- next_action

system_index.json 必须包含：
- runtime_status
- last_update
- candidate_count
- open_positions
- closed_positions
- wallet_coverage_rate
- case_file_count
- auto_review_count
- low_quality_case_count
- action_needed_count
- latest_events
- next_system_action

验收命令：

cd /root/sikk-gmgn

python3 -m py_compile sikk_unified_view_builder.py

python3 sikk_unified_view_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/index

python3 - <<'PY'
import json
from pathlib import Path

base = Path("data/gmgn_candidates_live_run/index")
required = [
    "system_index.json",
    "token_detail_index.json",
    "position_index.json",
    "latest_open_positions.json",
    "latest_closed_positions.json",
    "case_file_index.json",
    "auto_review_index.json",
    "alert_index.json",
]
for name in required:
    p = base / name
    print(name, p.exists())
    assert p.exists(), name

pos = json.loads((base / "position_index.json").read_text())
tok = json.loads((base / "token_detail_index.json").read_text())
print("positions:", len(pos))
print("tokens:", len(tok))

lith_found = any(
    str(v.get("token_symbol", "")).upper() == "LITH"
    or "LITH" in str(k).upper()
    for k, v in tok.items()
)
print("LITH in token index:", lith_found)
print("unified index OK")
PY

完成后输出：
SIKK_INTERACTION_PHASE_1_INDEX_REPORT.md

报告必须贴出：
- 修改文件
- 生成文件
- position 数量
- token 数量
- LITH 是否进入索引
- 失败项
```

---

# 七、Phase 2：CLI 查询层命令

```text
/codex

Phase 2：实现 sikkctl CLI 查询层。

目标：
让用户不再翻多个 JSON / CSV / MD 文件。
必须一条命令查看系统、开放仓位、Token、Position、Case File、Review。

新增文件：
- sikkctl.py
- tests/test_sikkctl.py

支持命令：
- python3 sikkctl.py status
- python3 sikkctl.py latest
- python3 sikkctl.py open
- python3 sikkctl.py closed --limit 20
- python3 sikkctl.py token <symbol_or_address>
- python3 sikkctl.py position <position_id>
- python3 sikkctl.py case <symbol_or_position_id>
- python3 sikkctl.py review
- python3 sikkctl.py health
- python3 sikkctl.py rebuild-index

数据来源：
只读取 data/gmgn_candidates_live_run/index/
不要直接读分散原始文件，除非 rebuild-index。

重点验收样本：
LITH。

python3 sikkctl.py token LITH 必须显示：
- token 地址
- 当前状态
- 开放仓位数量
- 入场时间
- 入场价格
- 入场市值
- 仓位 SO


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 8. SIKK-SOL 专业交互系统

来源路径：`[2914]`；长度：16334


对。你现在要做的不是单独优化 Telegram、网站、命令行，而是把整套系统升级成：

# SIKK-SOL Professional Interaction System  
# 专业交互系统

核心目标：

```text
让系统从“文件很多、命令很多、信息分散”
升级为：

一个统一交互入口
一套统一状态语言
一套统一详情页
一套统一复盘链路
一套统一告警和下一步动作
```

也就是说，以后你不应该再问：

```text
我该去哪个文件看？
我要跑哪个命令？
这个 token 到底什么情况？
这笔纸面仓位为什么买？
为什么退出？
数据缺什么？
下一步该干什么？
```

系统必须主动告诉你。

---

# 一、专业交互系统的总架构

你应该把 SIKK 交互层分成 5 个入口：

```text
1. Web Visual Console      桌面专业控制台
2. Telegram Console        手机交互控制台
3. CLI sikkctl             服务器命令行控制台
4. Daily / Case Reports    自动复盘报告
5. Event / Alert System    状态变化与风险提醒
```

它们都不能各自读一堆散乱文件。

所有入口都必须读取同一套统一索引：

```text
data/gmgn_candidates_live_run/index/
  system_index.json
  token_detail_index.json
  position_index.json
  latest_open_positions.json
  latest_closed_positions.json
  case_file_index.json
  alert_index.json
```

结构变成：

```text
原始模块输出
  ↓
统一索引层 sikk_unified_view_builder.py
  ↓
Web / Telegram / CLI / Report / Alert
```

这一步是专业化的基础。

---

# 二、交互系统要服务的 7 个核心场景

## 场景 1：我现在系统有没有正常运行？

入口：

```text
Web：首页 Command Center
TG：/sikk
CLI：python3 sikkctl.py status
```

必须显示：

```text
系统运行状态
最近更新时间
候选数量
钱包结构接入率
开放仓位
关闭仓位
今日新增入场
今日退出
当前异常模块
下一步系统动作
```

---

## 场景 2：现在有哪些开放纸面仓位？

入口：

```text
Web：Paper Lab → Open Positions
TG：/sikk_open
CLI：python3 sikkctl.py open
```

每个仓位必须显示：

```text
Token
入场时间
入场价格
入场市值
当前价格
当前市值
仓位 SOL
估算 token 数量
当前收益
最大浮盈
最大回撤
钱包状态
case_quality
next_action
```

---

## 场景 3：点击一个 token 后，我要知道它完整发生了什么

入口：

```text
Web：点击 Token
TG：点击 Token 按钮
CLI：python3 sikkctl.py token LITH
```

必须展示：

```text
当前市值
当前状态
所有纸面仓位
最新钱包结构
信号等级
策略类型
累计收益
开放仓位
关闭仓位
最新 Case File
缺失字段
下一步动作
```

---

## 场景 4：点击一个 position 后，我要知道这笔仓位为什么买、为什么持有、为什么退出

入口：

```text
Web：点击 Position
TG：点击 Position 按钮
CLI：python3 sikkctl.py position <position_id>
```

必须展示完整生命周期：

```text
发现 → 初筛 → 盘型 → 信号 → 钱包 → Quote → 入场 → 持仓 → 风险 → 退出 → 复盘
```

---

## 场景 5：我想知道策略哪里有问题

入口：

```text
Web：Review Lab
TG：/sikk_review
CLI：python3 sikkctl.py review
```

必须展示：

```text
右尾依赖
剔除 Top 1 / Top 2 后收益
按 token 聚合表现
按市值分桶表现
按 market_cap_context_status 表现
钱包退出误杀率
失败归因 Top
当前最需要调整的策略参数
```

---

## 场景 6：数据缺失在哪里？

入口：

```text
Web：System Health
TG：/sikk_health
CLI：python3 sikkctl.py health
```

必须展示：

```text
wallet_structure coverage
token_status coverage
paper entry snapshot coverage
case file coverage
auto review coverage
缺失字段 Top
LOW quality cases
DATA_BACKFILL_REQUIRED cases
```

---

## 场景 7：系统要提醒我什么？

入口：

```text
TG alert
Web alert banner
CLI latest
```

提醒类型：

```text
NEW_PAPER_ENTRY
PAPER_EXIT
FORCE_EXIT
EXIT_MONITOR
HOLD_WITH_DATA_RISK
DATA_BACKFILL_REQUIRED
WALLET_COVERAGE_LOW
CASE_QUALITY_LOW
BIG_WIN
BIG_LOSS
FALSE_EXIT_SUSPECTED
```

---

# 三、统一交互语言：状态、动作、质量、风险

专业化的关键是统一术语。  
所有入口都必须使用同一套状态语言。

## 1. 仓位状态

```text
OPEN
CLOSED
EXPIRED
PAUSED
ERROR
```

## 2. 行为动作

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
OPEN_PAPER_POSITION
COOLING
IGNORE
```

## 3. Case 质量

```text
HIGH
MEDIUM
LOW
INVALID
```

## 4. 复盘资格

```text
strategy_review_eligible: true / false
limited_confidence: true / false
```

## 5. 入场市值上下文

```text
EARLY_ENTRY
NORMAL_ENTRY
LATE_ENTRY
CHASE_ENTRY
UNKNOWN_ENTRY
```

## 6. 钱包退出策略结果

```text
WALLET_EXIT_HOLD
WALLET_EXIT_MONITOR
WALLET_FORCE_EXIT
WALLET_DATA_INSUFFICIENT
```

## 7. 交易结果类型

```text
BIG_WIN
WIN
SMALL_WIN
FLAT
SMALL_LOSS
LOSS
BIG_LOSS
UNCLASSIFIED
```

---

# 四、Web Visual Console 专业交互设计

Web 端是主控制台，适合桌面深度分析。

## 1. 左侧导航

```text
Command Center
Open Positions
Token Explorer
Position Explorer
Paper Lab
Review Lab
Wallet Structure
System Health
Events
Settings / Safety
```

---

## 2. Command Center 首页

必须有 4 层：

### A. 顶部系统状态卡

```text
Runtime Status
Last Update
Token Count
Wallet Coverage
Open Positions
Closed Positions
Win Rate
Avg PnL
Case Quality Coverage
```

### B. 流程漏斗

```text
Candidates
→ Signal Ready
→ Wallet Support
→ Quote/Security Pass
→ Paper Ready
→ Paper Open
→ Paper Closed
→ Case File Generated
→ Auto Review Generated
```

### C. 当前关键提醒

```text
3 个 OPEN 仓位
1 个 HOLD_WITH_DATA_RISK
7 个 LOW quality case
wallet coverage 低于 80%
最新 FORCE_EXIT 需要 shadow hold 验证
```

### D. 下一步动作

```text
BACKFILL_WALLET_AND_MARKET_CAP: 5
FIX_WALLET_STRUCTURE_PIPELINE: 2
REVIEW_FORCE_EXIT_POLICY: 1
```

---

## 3. Open Positions 页面

每行必须可点击。

字段：

```text
Token
Status
Entry Time
Entry MC
Current MC
MC Change
Size SOL
Token Amount
PnL
Max Profit
Max Drawdown
Wallet
Case Quality
Action
```

点击后打开 Position Detail Drawer。

---

## 4. Token Detail Drawer

分区：

```text
Overview
Positions
Market Cap Path
Wallet Structure
Signals
Case Files
Auto Reviews
Events
Missing Data
Next Action
```

必须显示：

```text
这个 token 有几笔仓位
哪笔还开放
哪笔收益最大
哪笔亏损最大
是否重复入场过多
最新钱包状态
是否 LOW quality
是否可纳入策略统计
```

---

## 5. Position Detail Drawer

这是最重要的详情页。

必须显示完整时间线：

```text
S0 发现
S1 初筛
S2 盘型
S3 信号
S4 钱包
S5 Quote/Security
S6 入场决策
S7 纸面入场
S8 持仓过程
S9 风险变化
S10 退出决策
S11 纸面退出
S12 自动复盘
```

每个阶段可以展开：

```text
结构化字段
自然语言解释
风险点
缺失字段
下一步动作
```

---

## 6. Review Lab

这个页面不是看单币，而是看策略问题。

必须有：

```text
Right Tail Dependency
Token-Level Statistics
Entry Market Cap Buckets
Market Cap Context Performance
Wallet Exit Effectiveness
Failure Attribution
Case Quality Distribution
Strategy Adjustment Suggestions
```

---

## 7. System Health

必须能回答：

```text
数据是不是完整？
哪些模块没输出？
哪些字段缺失最多？
哪些 case 不能复盘？
哪个 pipeline 断了？
```

字段：

```text
candidate_count
token_status_count
wallet_decision_count
paper_position_count
case_file_count
auto_review_count
wallet_coverage_rate
case_quality_distribution
missing_fields_top
stale_warnings
next_system_action
```

---

# 五、Telegram Professional Console 交互设计

TG 是手机端，不要堆长文本。  
核心是“点进去看”。

## 1. 主菜单 `/sikk`

显示：

```text
SIKK Live Console

Runtime: OK
Last Update: 2026-05-03 07:55 UTC

Open: 3
Closed: 163
Win Rate: 31.90%
Avg PnL: 6.675%
Low Quality Cases: 7
Action Needed: 5
```

按钮：

```text
[开放仓位] [Token 查询]
[风险提醒] [复盘总结]
[系统健康] [刷新]
```

---

## 2. `/sikk_open`

每页最多 8 个仓位。

按钮示例：

```text
[LITH -13.87% | LOW]
[AALIEN CLOSED +679%]
[下一页] [返回]
```

点击 LITH 进入 Position Detail。

---

## 3. Position Detail

TG 里分 3 屏，不要一次发太长。

### 第一屏：核心状态

```text
LITH Position

Status: OPEN
Action: HOLD_WITH_DATA_RISK
Case Quality: LOW

Entry:
Time: 2026-04-28 17:46 UTC
Price: 0.000021063508
Size: 0.085319 SOL
Entry MC: UNKNOWN

Current:
Price: 0.000018142653
PnL: -13.87%
Max DD: -21.99%

Next:
BACKFILL_WALLET_AND_MARKET_CAP
```

按钮：

```text
[入场证据]
[钱包证据]
[持仓过程]
[自动复盘]
[Case File]
[返回]
```

### 第二屏：入场证据

```text
发现市值
信号市值
入场市值
入场位置
信号原因
盘型解释
```

### 第三屏：自动复盘

```text
策略适配
入场质量
钱包门禁
风险控制
调整建议
```

---

# 六、CLI sikkctl 专业命令设计

CLI 是最快排查工具。

## 主命令

```bash
python3 sikkctl.py status
python3 sikkctl.py latest
python3 sikkctl.py open
python3 sikkctl.py token LITH
python3 sikkctl.py position <position_id>
python3 sikkctl.py case LITH
python3 sikkctl.py review
python3 sikkctl.py health
python3 sikkctl.py rebuild-index
```

---

## `sikkctl.py latest`

必须输出：

```text
SIKK Latest

Open Positions: 3
Risk Attention: 1
Latest Entry: XXX
Latest Exit: YYY
Worst Open Position: LITH -13.87%
Action Needed:
- LITH: BACKFILL_WALLET_AND_MARKET_CAP
- wallet coverage low
```

---

## `sikkctl.py token LITH`

必须输出：

```text
Token: LITH
Address: ...
Current State: OPEN
Total Positions: 1
Open Positions: 1
Closed Positions: 0

Latest Position:
Entry Time: ...
Entry Price: ...
Entry MC: UNKNOWN
Size: 0.085319 SOL
Current PnL: -13.87%
Case Quality: LOW
Missing Fields:
- discovery_market_cap_usd
- entry_market_cap_usd
- entry_wallet_structure_status

Next Action:
BACKFILL_WALLET_AND_MARKET_CAP

Case File:
...
```

---

# 七、统一索引层必须先做

如果没有统一索引，Web、TG、CLI 会继续乱。

必须实现：

```text
sikk_unified_view_builder.py
```

输出：

```text
data/gmgn_candidates_live_run/index/
  system_index.json
  token_detail_index.json
  position_index.json
  latest_open_positions.json
  latest_closed_positions.json
  case_file_index.json
  alert_index.json
```

每次主流程结束后自动执行：

```bash
python3 sikk_unified_view_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/index
```

然后再刷新：

```bash
python3 sikk_dashboard_site_builder.py ...
```

Telegram 也读这个索引。

---

# 八、专业化交互必须有“信息层级”

以后不要把所有信息一次性展示。

每个入口都按这个层级：

```text
Level 1：总览
Level 2：列表
Level 3：单 token
Level 4：单 position
Level 5：case file
Level 6：auto review
Level 7：raw data
```

用户路径：

```text
/sikk
  → 开放仓位
    → LITH
      → 入场证据
      → 钱包证据
      → 自动复盘
      → Case File
```

Web 路径：

```text
Command Center
  → Open Positions
    → LITH Position Drawer
      → Lifecycle Timeline
        → S7 Paper Entry
        → S12 Auto Review
```

CLI 路径：

```bash
sikk latest
sikk open
sikk token LITH
sikk position <id>
sikk case LITH
```

---

# 九、给 Hermes / OpenClaw 的总任务书

下面这段可以直接复制。

```text
任务：实现 SIKK-SOL Professional Interaction System，统一 Web、Telegram、CLI 的专业交互体验。

当前问题：
SIKK 已经有 paper runner、wallet structure、dashboard、telegram broadcast、case file、auto review 等模块，但交互体验仍然分散。
用户要查看一个 token 或 paper position，需要中转多个命令和多个 JSON / CSV / MD 文件。
Telegram 目前只能广播文本，不能点击进入不同代币和仓位。
Web 端不能完整表达单


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 9. 摘录

来源路径：`[3510]`；长度：10920


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
  --output-dir data/gmgn_candidates_


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 10. 摘录

来源路径：`[4137]`；长度：16640


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
3. failure_type 只用于亏损或无效交易，不要把盈利交易标记为 f


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 11. 摘录

来源路径：`[4511]`；长度：13739


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
- token_amoun


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）


## 12. 摘录

来源路径：`[4656]`；长度：21762


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
print("tokens:", len(d


……（长文已截断，保留核心前段；原始 payload 在 /tmp/chatgpt_share_69f75c79_payloads.txt）
