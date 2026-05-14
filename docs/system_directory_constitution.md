# SIKK-GMGN 系统目录宪法

## 0. 宪法目的

本文件是 `/root/sikk-gmgn` 后续所有 Hermes 任务的目录归属规则。任何代码实现、数据采集、结构分析、报告生成、长任务推进、旧文件兼容，都必须先遵守本宪法，再谈功能实现。

核心目标：

- 固定每个阶段的输出位置。
- 固定每类资产的归属目录。
- 固定每个 Bot 的职责边界与目录边界。
- 固定每种输出的主读路径、兼容路径、禁止路径。
- 让后续任务进入数字化、反证化、统计化、工程化，而不是继续散乱写文件。

## 1. 不变边界

所有目录规则都不得突破以下边界：

- 不接真实交易。
- 不接状态机。
- 不做 paper runner。
- 不读取私钥。
- 不签名。
- 不广播。
- 不 swap。
- 不删除旧文件。
- 不移动旧文件。
- 不覆盖旧 runtime 输出。
- 旧路径只做兼容读取或复制映射，不作为新任务主写路径。
- `ca` / `CA` / `ca <token_address>` 是 Source Wallet Bot 的新钱包分析入口触发词。用户只要发送 `ca`，默认进入新钱包数据分析体系；若后面带 token address，则直接进入该 token 的分析上下文。
- Source Wallet Bot 运行结构分析前，必须先读取 `docs/source_wallet_bot/directory_governance/data_dependency_map_v1.md` 的分析问题清单，以及 `docs/source_wallet_bot/directory_governance/data_dependency_contract_v1.json` 的 `analysis_questions` / `judgment_targets`；不得绕过问题清单直接按接口可得字段做判断。
- Source Wallet Bot 接入任何上游平台/API/交易平台接口前，必须先完成 `docs/source_wallet_bot/directory_governance/interface_capability_inventory_v1.md` 的接口能力审计；禁止在接口能力清单完成前直接写采集脚本、API wrapper 或自动化判断逻辑。
- 新接口接入必须声明回答哪一类分析问题；不能回答 12 类问题之一的字段，默认不进入首版钱包结构分析合同。
- 分析问题清单只允许产出弱证据链和门禁依据，不得输出“确定庄家”“内幕钱包”“老鼠仓”“确认同伙”“必跟”“稳赢”等强定性结论。
- 标准主目录必须固定为：`data/source_wallet_bot/<mode>/<token_address>/`。
- 标准两层必须优先固定为：`wallet_data/` 与 `structure_analysis/`。
- 入口解析先看 `ca` 触发，再看 token address，再走旧路径只读补查；禁止把 `ca` 解析散写到旧目录或临时聊天目录。

## 1.1 钱包结构分析专业主目录补充规则

钱包结构分析 / 钱包数据采集 / Source Wallet Bot 的专业主目录固定为 `/root/sikk-gmgn/`，专业主数据目录固定为 `data/source_wallet_bot/`。详细执行规则见：

```text
docs/source_wallet_bot/directory_governance/wallet_structure_primary_root_policy.md
```

`/root/sikk-wallet-intel/` 只作为协同、总控、行为推断、AI Harness 与历史 runs 工作区，不再作为新增钱包结构分析主数据目录。所有新增钱包结构分析产物必须写入 `data/source_wallet_bot/<mode>/<token_address>/` 的标准 token layout。

## 1.2 AI 驱动交易结构系统总控工程补充规则

钱包结构分析不是孤立模块，而是 AI 驱动交易结构系统总控工程的事实与结构底座。总控工程核心链路固定为：

```text
Skill 能力地图 → 目标系统映射 → 自动发现缺口 → 自动补全实现 → 验证闭环
```

详细体系文件见：

```text
docs/harness/trading_structure_control/AI_DRIVEN_TRADING_STRUCTURE_CONTROL_SYSTEM.md
```

该体系遵循 Harness Engineering：skill 是可验证工作流模块，不是提示词；系统必须有控制面、循环、权限、恢复、验证与多代理分工。最终状态只能是排除、记录、风险监控、观察、纸面候选、需人工确认的实盘候选，不允许输出自动买卖或保证收益。

## 2. 总根目录

项目根目录：

```text
/root/sikk-gmgn/
```

系统级目录必须固定为：

```text
/root/sikk-gmgn/
├── docs/                         # 系统级规则、宪法、工程说明
├── modules/                      # 代码模块
├── tests/                        # 测试
├── data/                         # 所有运行数据与标准化输出
├── reports/                      # 人类可读报告总索引
├── research_loop/                # 方法轮、长任务计划、checkpoint、验收
├── imports/                      # 外部/旧包 staging 导入
├── schemas/                      # 跨模块/系统级 schema 主合同
├── contracts/                    # shared 合约、跨 Bot 合同
├── tools/                        # 项目级工具脚本；无则可为空
└── legacy_compat/                # 旧路径兼容索引；不搬旧文件，只记录映射
```

禁止后续任务在项目根目录直接散放新 JSON / CSV / Markdown 运行输出。根目录只允许保留既有兼容文件、入口脚本、项目配置和明确的顶层文档。

## 3. 资产分类与唯一主写路径

Hermes 写文件前必须先归类资产。没有归类，不允许写文件。

### 3.1 方法轮 / 研究轮

所有方法轮、推理流程、长任务计划、checkpoint 放：

```text
research_loop/
research_loop/plans/
research_loop/checkpoints/
research_loop/acceptance/
research_loop/blockers/
research_loop/state/
research_loop/task_packages/
```

规则：

- 计划：`research_loop/plans/<task_name>.md`
- checkpoint：`research_loop/checkpoints/<round_name>.md`
- 验收：`research_loop/acceptance/<task_name>_acceptance.md`
- blocker：`research_loop/blockers/<task_name>_blocker_report.md`
- 长任务状态：`research_loop/state/<task_id>/loop_state.json`
- 任务包：`research_loop/task_packages/<status>/<task_id>/`

### 3.2 方法论 / 判断规则 / 反证体系

结构推断体系进入“数字化、反证化、统计化、工程化”阶段后，方法论资产必须固定到：

```text
research_loop/methodology/
research_loop/methodology/passports/
research_loop/methodology/rules/
research_loop/methodology/counter_evidence/
research_loop/methodology/stat_models/
research_loop/methodology/audit_rules/
research_loop/methodology/field_maps/
```

- 字段映射 / 判断目标合同 / 数据依赖地图：`research_loop/methodology/field_maps/` 或 `docs/source_wallet_bot/directory_governance/`


- 方法护照：`passports/<source_id>_passport.md|json`
- 判断规则：`rules/<rule_family>.md|json`
- 反证规则：`counter_evidence/<counter_rule>.md|json`
- 统计模型说明：`stat_models/<model_name>.md|json`
- 审计规则：`audit_rules/<audit_name>.md|json`
- 字段映射：`field_maps/<map_name>.md|json|csv`

禁止把方法论散写到项目根目录或 token 运行目录。

### 3.3 代码

所有功能代码只放：

```text
modules/<bot_or_domain>/
```

示例：

```text
modules/source_wallet_bot/
modules/intel_bot/
modules/wallet_structure/
modules/strategy_gate/
```

禁止把功能代码写入 `data/`、`reports/`、`research_loop/`。

兼容说明：根目录既有 `sikk_*.py` 入口脚本暂时保留；后续新增功能代码必须进 `modules/`，根目录只允许新增薄入口脚本或 CLI wrapper。

### 3.4 测试

所有测试只放：

```text
tests/
```

命名：

```text
tests/test_<module>_<feature>.py
```

### 3.5 Schema / Contract

模块级 schema 和合同主版本放：

```text
modules/<bot>/schemas/
modules/<bot>/contracts/
```

跨 Bot / shared 合同放：

```text
contracts/shared/
contracts/bot_handoff/
schemas/shared/
```

当前兼容：若旧 schema 已在 `modules/source_wallet_bot/*.json`，保留旧路径，但新 schema 主写路径必须进入：

```text
modules/source_wallet_bot/schemas/
```

运行数据对应 schema 副本可放：

```text
data/<bot>/<mode>/<asset_id>/manifest/schema_snapshot.json
```

但它是运行副本，不是主合同源。

### 3.6 运行数据

所有运行输出只放：

```text
data/<bot>/<mode>/<asset_id>/
```

其中：

- `<bot>`：`source_wallet_bot`、`intel_bot`、`strategy_gate_bot`、`execution_risk_bot`、`review_ops_bot`、`gmgn_candidates_live_run`。
- `<mode>`：`live`、`ad_hoc`、`staging`、`legacy`、`audit`、`backtest`。
- `<asset_id>`：token address、import id、case id、run id。

禁止把新 token 输出直接写到：

```text
data/<bot>/
data/<bot>/<mode>/
```

### 3.7 报告

人类可读报告主目录：

```text
reports/<bot>/<mode>/<asset_id>/
```

如果报告是某个 token 输出包的一部分，可同时复制到：

```text
data/<bot>/<mode>/<asset_id>/structure_analysis/reports/
```

但 `reports/` 是报告总索引主目录。

### 3.8 外部包 / 旧文件 / .gz / .zip

所有导入文件先进入：

```text
imports/staging/<import_id>/
```

规则：

- `.zip`：只在 staging 检查与解压。
- `.gz`：不走文档解析；只在 staging 用 `gzip -dc` 安全展开。
- 不直接写入 live runtime。
- 不移动旧文件。
- 不删除旧文件。
- 生成 file passport 与 sha256。

### 3.9 旧文件兼容区

旧文件不移动、不删除，但兼容索引必须放：

```text
legacy_compat/manifests/
legacy_compat/path_maps/
legacy_compat/read_fallbacks/
```

规则：

- `manifests/`：记录批量 copy-only 治理 manifest。
- `path_maps/`：记录旧路径到新路径的映射。
- `read_fallbacks/`：记录哪些 reader 仍允许 fallback 旧路径。
- 兼容区只存索引和说明，不复制大体量 runtime 数据。

### 3.10 钱包数据读取优先级（强制）

凡是涉及钱包数据分析、结构分析、handoff 组装、报告生成、补查修复的读取任务，必须遵守以下读取顺序：

```text
1. 新标准入口
2. token 索引
3. 数据护照
4. 字段字典
5. 旧路径映射
6. 旧目录只读补查
```

解释：

- 新标准入口：先读 `data/source_wallet_bot/{mode}/{asset_id}/` 下的标准目录。
- token 索引：确认该 token 是否已有标准包、版本、manifest、已复制文件。
- 数据护照：确认资产边界、来源、版本、可读路径和可用性。
- 字段字典：先判断是不是字段改名 / schema 变化，而不是数据真正缺失。
- 旧路径映射：只在标准体系缺文件时，用映射定位旧路径对应的新落点。
- 旧目录只读补查：最后才允许只读补查旧目录，且不得全仓乱搜。

硬性要求：

- 先新后旧，不得反过来。
- 标准缺失才回退映射。
- 映射缺失才补查旧目录。
- 两边都没有才标记缺失。
- 不得从 dashboard、paper、reports 反推事实。
- 不得对所有旧目录做盲搜。
- 不得把 inference 当 facts。

所有钱包 reader、path resolver、fallback loader 都必须围绕这条顺序实现。

### 3.10.1 推荐实现形态

统一路径解析器应提供：

- `resolve_standard_path(...)`
- `resolve_token_index(...)`
- `resolve_passport(...)`
- `resolve_field_dict(...)`
- `resolve_legacy_mapping(...)`
- `resolve_legacy_fallback(...)`

并返回：

- `resolved_path`
- `source_tier`
- `fallback_chain`
- `missing_reason`
- `is_standard`
- `is_legacy_fallback`

这样每个 reader 不需要自己写 fallback 逻辑。

## 4. Bot 目录宪法

### 4.1 Bot 1：Source Wallet Bot

职责：事实源采集、钱包事实标准化、钱包画像、同源证据、资金/筹码/路径事实、结构证据底座、Bot2 handoff。

代码目录：

```text
modules/source_wallet_bot/
```

运行数据目录：

```text
data/source_wallet_bot/<mode>/<token_address>/
```

标准 token 输出结构：

```text
data/source_wallet_bot/<mode>/<token_address>/
├── wallet_data/
│   ├── raw/
│   ├── normalized/
│   └── summary/
├── structure_analysis/
│   ├── wallet_fact/
│   ├── intelligence/
│   ├── handoff/
│   └── reports/
└── manifest/
```

Source Wallet Bot 禁止输出：

- `PAPER_READY`
- `BLOCKED`
- `final_trade_gate`
- 交易许可
- 买卖信号
- 执行动作

### 4.2 Bot 2：Intel Bot

职责：读取 Bot1 的结构事实证据，做行为推断、反证检查、证据等级升级/降级、主导侧行为动机候选分析。

代码目录：

```text
modules/intel_bot/
```

运行目录：

```text
data/intel_bot/<mode>/<token_address>/
```

标准 token 输出结构：

```text
data/intel_bot/<mode>/<token_address>/
├── behavior_inference/
├── counter_evidence/
├── quant_scores/
├── structure_conclusion/
├── reports/
└── manifest/
```

Bot2 只能读取：

```text
data/source_wallet_bot/<mode>/<token_address>/structure_analysis/handoff/bot2_handoff_packet.json
data/source_wallet_bot/<mode>/<token_address>/manifest/token_output_manifest.json
```

以及 manifest 中声明的结构证据路径。不得回读 dashboard / paper / report 反推事实。

### 4.3 Bot 3：Strategy Gate Bot

职责：只读 Intel 输出和 shared 合同，做观察/排除/降级/待查类门禁判断。当前阶段不接交易。

目录：

```text
modules/strategy_gate_bot/
data/strategy_gate_bot/<mode>/<token_address>/
reports/strategy_gate_bot/<mode>/<token_address>/
```

禁止从 Source 私有目录直接读原始事实；必须经 Intel 输出或 shared normalized。

### 4.4 Bot 4：Execution Risk Bot

职责：未来只做纸面/风险解释与执行约束。当前阶段不接 paper runner、不接真实执行。

目录：

```text
modules/execution_risk_bot/
data/execution_risk_bot/<mode>/<token_address>/
reports/execution_risk_bot/<mode>/<token_address>/
```

当前禁止写交易动作、签名、广播、swap 相关输出。

### 4.5 Bot 5：Review Ops Bot

职责：复盘、审计、日报、仪表盘展示。只能读归档和 shared 结果，不反向污染 Source / Intel / Gate。

目录：

```text
modules/review_ops_bot/
data/review_ops_bot/<mode>/<asset_id>/
reports/review_ops_bot/<mode>/<asset_id>/
```

### 4.6 旧 live run / dashboard / paper runner

现有目录：

```text
data/gmgn_candidates_live_run/
```

规则：

- 保留现状。
- 不删除。
- 不移动。
- 不作为 Source Wallet Bot 新输出主路径。
- dashboard / paper / report 不能反推事实字段。
- 旧 token 输出如需治理，只能 copy-only 到新目录并写 manifest。

## 5. Source Wallet Bot 资产归属

### 5.1 wallet_data/raw

只放原始采集和采集输入：

```text
wallet_data/raw/gmgn_wallet_rows_raw.json
wallet_data/raw/gmgn_wallet_trade_input.json
wallet_data/raw/gmgn_wallet_profile_input.json
```

### 5.2 wallet_data/normalized

只放钱包事实标准化输出：

```text
wallet_data/normalized/wallet_trade_normalized.json
wallet_data/normalized/wallet_entity_profile_normalized.json
wallet_data/normalized/token_transfer_normalized.json
token_source_classification_base.json
wallet_data/normalized/funding_flow_normalized.json
wallet_data/normalized/funding_source_normalized.json
wallet_data/normalized/backflow_paths_normalized.json
wallet_data/normalized/gmgn_wallet_tags_normalized.json
wallet_data/normalized/wallet_snapshot_delta_source.json
wallet_data/normalized/holder_delta_normalized.json
wallet_data/normalized/quote_security_normalized.json
```

### 5.3 wallet_data/summary

只放钱包数据总览：

```text
wallet_data/summary/summary_overview.json
wallet_data/summary/summary_overview.md
```

### 5.4 structure_analysis/wallet_fact

只放结构聚合事实包：

```text
structure_analysis/wallet_fact/wallet_structure_normalized.json
structure_analysis/wallet_fact/chip_distribution_summary.json
structure_analysis/wallet_fact/same_source_groups.json
structure_analysis/wallet_fact/fund_flow_edges.csv
structure_analysis/wallet_fact/address_history.json
structure_analysis/wallet_fact/wallet_fact_package_manifest.json
```

### 5.5 structure_analysis/intelligence

只放结构证据和钱包候选判断：

```text
structure_analysis/intelligence/same_source_evidence_normalized.json
structure_analysis/intelligence/wallet_intelligence_decision.json
```

### 5.6 structure_analysis/handoff

只放 Bot2 handoff：

```text
structure_analysis/handoff/bot2_handoff_packet.json
```

### 5.7 structure_analysis/reports

只放结构分析可读报告：

```text
structure_analysis/reports/wallet_fact_report.md
structure_analysis/reports/structure_summary.md
```

### 5.8 manifest

必须存在：

```text
manifest/token_output_manifest.json
manifest/directory_layout.md
```

manifest 必须记录：

- token_address
- generated_at
- task_name
- root_dir
- target_layout
- policy
- path_mappings
- missing_sources
- old_path
- new_path
- action
- status

## 6. 路径写入门禁

任何后续 Hermes 任务在写文件前必须先判断资产类型，然后写入宪法规定目录。

默认禁止：

```text
/root/sikk-gmgn/*.json
/root/sikk-gmgn/*.csv
/root/sikk-gmgn/*.md   # 除 README/AGENTS/顶层宪法入口外
data/source_wallet_bot/*.json
modules/<bot>/*_runtime_output.json
reports/*.json
```

允许例外：

- 旧文件兼容保留。
- 入口脚本和已有项目文件。
- 宪法明确声明的主路径。

## 7. 旧路径兼容原则

旧文件不删除、不移动。

如果旧文件已经存在：

1. 保留旧文件。
2. 复制到新目录。
3. 在 manifest 写入 old_path -> new_path。
4. 后续主读新路径。
5. 旧路径只做兼容读取。

## 8. 后续任务执行门禁

每个新任务启动前必须回答四个问题：

1. 这是哪个 Bot？
2. 这是哪个阶段？代码 / 数据 / schema / 报告 / checkpoint / import / methodology / legacy_compat？
3. 资产 ID 是什么？token / run / import / case / task？
4. 主写路径是否符合本宪法？

如果不能回答，任务必须先写 plan 到：

```text
research_loop/plans/
```

不得直接写运行文件。

## 9. 强制路由 JSON

机器可读路由文件：

```text
docs/system_directory_routes.json
```

后续脚本、Hermes、子 agent 需要判断路径时，应优先读取该 JSON，而不是口头猜测。

## 10. 验收标准

目录宪法合格标准：

- 宪法文档存在。
- 路由规则 JSON 存在。
- AGENTS.md 明确要求写文件前遵守宪法。
- 系统级目录骨架存在。
- Source / Intel / Gate / Execution / Review / shared 目录骨架存在。
- 当前 token 输出模板目录存在或可由脚本创建。
- 当前 manifest 存在且 JSON 合法。
- 不改变交易 / 状态机 / paper runner。

## 11. 当前结论

现在必须先建立工程秩序，再继续加功能。任何“找钱包、加字段、加策略、接 bot、接报告”的需求，都必须先经过本宪法路由。
