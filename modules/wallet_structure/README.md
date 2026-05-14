# SIKK 钱包结构采集分析模块

## 1. 模块定位

`modules/wallet_structure` 是 SIKK-GMGN 主系统中的独立小模块：`SIKK Wallet Structure Collector / Analyzer`。

它把旧 `sikk_gmgn_token_report.py` 的单币报告能力整理为可复用、可验收、可被主系统只读调用的钱包结构情报模块。

## 2. 模块解决的问题

- 从 GMGN/链上数据源采集钱包结构相关字段。
- 将浅层 GMGN 字段标准化为钱包画像字段。
- 识别疑似结构执行钱包、同源执行组、分发/回流路径、结果钱包、接盘鲸鱼等角色。
- 输出 GMGN 备注表，便于人工复核与外部备注。
- 输出 `wallet_structure_decision.json`，供主系统判断是否继续观察、暂停、阻断或允许进入后续 paper 流程。

## 3. 模块不解决的问题

- 不做 K 线策略。
- 不生成买入信号。
- 不执行自动下单。
- 不处理止盈止损。
- 不做 Telegram 面板或 dashboard。
- 不执行 paper runner。
- 不执行真实 swap。
- 不读取、保存、签名或广播任何私钥/交易。

## 4. 输入

输入契约见：`input_schema.json`。

最小输入：

```json
{
  "token_address": "<sol token address>",
  "chain": "sol",
  "analysis_time": "2026-05-04T14:00:00Z"
}
```

## 5. 输出

输出契约见：`output_schema.json`。

标准文件：

- `wallet_raw_snapshot.csv`
- `wallet_normalized.csv`
- `wallet_role_classification.csv`
- `wallet_funding_edges.csv`
- `wallet_token_flow_edges.csv`
- `same_source_groups.csv`
- `distribution_paths.csv`
- `backflow_paths.csv`
- `gmgn_note_table.csv`
- `wallet_structure_decision.json`
- `wallet_structure_report.md`

## 6. 文件结构

```text
modules/wallet_structure/
├── README.md
├── module_contract.md
├── input_schema.json
├── output_schema.json
├── field_dictionary.csv
├── role_rule_matrix.csv
├── evidence_level_matrix.csv
├── gmgn_note_dictionary.csv
├── gap_register.csv
├── extension_backlog.csv
├── legacy_mapping.md
├── module_flow.md
└── implementation_plan.md
```

## 7. 如何运行

当前阶段是设计包，正式 CLI 在 Phase B/C 实现。建议未来命令：

```bash
python3 -m modules.wallet_structure.run   --input data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_structure_input.json   --output-dir data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token_address>/
```

设计包验收命令：

```bash
find modules/wallet_structure -type f | sort
python3 -m json.tool modules/wallet_structure/input_schema.json
python3 -m json.tool modules/wallet_structure/output_schema.json
head -n 5 modules/wallet_structure/field_dictionary.csv
head -n 5 modules/wallet_structure/role_rule_matrix.csv
head -n 5 modules/wallet_structure/gap_register.csv
```

## 8. 如何接入主系统

主系统只读取：

```text
wallet_structure_decision.json
```

主系统不得读取本模块内部中间字段作为直接买入信号。本模块只给结构侧状态和原因：

- `WALLET_SUPPORT`
- `WALLET_PAUSE`
- `WALLET_BLOCK`
- `WALLET_UNKNOWN`

交易侧最终是否进入 paper 或真实流程，必须由主系统的 final gate 决定。

## 9. 如何验收

- 目录和 13 个设计文件存在。
- JSON schema 可被 `python3 -m json.tool` 解析。
- CSV 表头符合任务要求。
- 角色规则不使用“肯定庄家”语言。
- `wallet_structure_decision.json` 字段已在 `output_schema.json` 中定义。
- P0/P1/P2/P3 缺口和扩展已分类。
