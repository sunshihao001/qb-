# GPT Share 69f74bb3 全自动流程吸收与落地报告

来源：<https://chatgpt.com/share/69f74bb3-6220-83a4-abd9-171c49c3ce69>
标题：Branch · Branch · Branch · Branch · Branch · 纸面交易优化方案
处理时间：2026-05-03

## 1. 文章护照

- 来源链接：ChatGPT share 69f74bb3
- 主题类型：SIKK Telegram 中文专业控制台 / 全自动阶段化工程流程
- 适用项目：`/root/sikk-gmgn`
- 是否真实读取：是
- 是否完整读取：已读取 share HTML 与 React stream，有效正文存在
- 核心目标：把 SIKK Telegram 从静态广播升级成手机端中文专业控制台，并由 Hermes 自动完成侦察、实现、测试、验收。

## 2. 核心设计认知

该 share 强调：任务不是“写几个 TG 按钮”，而是建立 Hermes 多角色、多阶段、可验收的交互系统工程流程。

标准目标架构：

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

## 3. 角色体系

- 交互总设计师：负责总览 → 仓位 → 详情 → 证据 → 复盘路径。
- 信息架构师：负责 System / Token / Position / Case / Auto Review / Alert 分层。
- Telegram 交互设计师：负责菜单、按钮、分页、返回路径、callback 短码。
- 交互 AI 编程大师：负责实现 Python 代码。
- UI 文案专家：负责中文状态语言。
- 数据质量审计员：负责字段完整性、样本质量、缺失证据。
- 安全边界官：禁止真实交易入口。
- 测试验收官：负责 py_compile、pytest、按钮/文本/安全测试。

## 4. 本次已自动落地的最小闭环

新增文件：

- `sikk_telegram_zh.py`
- `sikk_telegram_views.py`
- `tests/test_sikk_telegram_views.py`

使用现有文件：

- `sikk_unified_view_builder.py`
- `data/gmgn_candidates_live_run/index/*.json`

已实现能力：

- 中文术语层：`HOLD_WITH_DATA_RISK` → `带数据风险持有`，`UNKNOWN` → `待补 / 证据不足`。
- 中文自然语言触发映射：系统总览、开放仓位、风险提醒、系统健康、刷新数据。
- 中文主菜单：显示候选数、开放仓位、关闭仓位、风险提醒、安全关闭状态。
- 开放纸面仓位列表：显示 `LITH｜-24.2518%｜待补 / 证据不足` 等按钮。
- 仓位详情页：显示入场时间、入场价格、仓位规模、当前收益、最大回撤、样本质量、缺失证据、下一步动作。
- 风险提醒页：显示只读 alert 列表。
- callback_data 保持短码：`list:open:0`、`pos:P1`、`alert:A1`、`menu:main`。

## 5. 验收结果

测试命令：

```bash
PYTHONPATH=. pytest -q tests/test_sikk_telegram_views.py tests/test_sikk_unified_view_builder.py tests/test_sikk_query.py tests/test_sikk_dashboard_site_builder.py -q
```

结果：

```text
............................                                             [100%]
```

真实输出样例：

```text
【SIKK 中文专业控制台】
模式：只读观察 / paper-only
真实交易：关闭
广播交易：关闭
候选代币：156
开放纸面仓位：5
已关闭纸面仓位：178
风险提醒：6
```

```text
【LITH 纸面仓位详情】
仓位状态：开放纸面仓位
入场时间：2026-04-28 17:46:00 UTC
入场价格：2.1063508e-05
仓位规模：0.085319 SOL
当前收益：-24.2518%
最大回撤：待补
样本质量：待补 / 证据不足
钱包结构：待补 / 证据不足
缺失证据：待补
下一步动作：观察
安全边界：只读复盘，不执行真实交易。
```

## 6. 安全审计

- 未新增真实交易按钮。
- 未读取私钥。
- 未签名。
- 未广播。
- callback_data 不含中文长文本，不塞长地址。
- 本次新增模块只读渲染 payload，不连接 Telegram，不发消息。

## 7. 下一阶段建议

- Phase 4：接入真实 Telegram bot handler，但只处理只读 payload。
- Phase 5：中文自然语言触发词扩展到 “查看 LITH / 代币 LITH / 仓位 P1”。
- Phase 6：Case File / Auto Review 按钮详情页。
- Phase 7：`sikk_live_run.py` 每轮结束自动刷新 index + TG callback index。
