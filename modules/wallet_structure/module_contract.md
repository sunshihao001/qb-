# SIKK Wallet Structure Collector / Analyzer 模块契约

## 模块名称

- 英文：`SIKK Wallet Structure Collector / Analyzer`
- 中文：`SIKK 钱包结构采集分析模块`
- 目录：`modules/wallet_structure/`

## 模块职责

本模块只负责钱包结构情报：

1. 接收 token 级分析请求。
2. 从 GMGN / 链上补查数据源采集钱包相关数据。
3. 标准化钱包字段。
4. 地址基础类型识别。
5. 当前代币行为判断。
6. Token 来源归因。
7. 资金来源归因。
8. 疑似同源关系判断。
9. 疑似分发/回流路径判断。
10. 地址角色初判。
11. 生成 GMGN 备注表。
12. 更新轻量历史地址库文件。
13. 输出 `wallet_structure_decision.json` 给主系统读取。

## 输入

主输入为一个 JSON 对象，字段见 `input_schema.json`。最小输入：

```json
{
  "token_address": "<sol token address>",
  "chain": "sol",
  "analysis_time": "ISO-8601"
}
```

## 输出

标准输出文件见 `output_schema.json`，核心文件：

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

## 不负责的内容

- 不负责 K 线策略判断。
- 不负责买入信号生成。
- 不负责自动下单。
- 不负责止盈止损。
- 不负责 Telegram 面板交互。
- 不负责 dashboard。
- 不负责 paper 交易执行。
- 不负责真实 swap。
- 不读取、写入、保存私钥。
- 不签名，不 broadcast。

## 上游模块

- token discovery / candidate source：提供 token 地址、symbol、发现时间。
- GMGN CLI / API wrapper：提供 token、holder、trader、tag、security、pool 原始数据。
- 可选链上补查器：提供 wallet age、first seen、funding edges、token transfer edges。

## 下游模块

- 主状态机：只读取 `wallet_structure_decision.json`。
- paper runner：后续只读取 `wallet_structure_factor`，不直接接受钱包模块的交易命令。
- report/explain 模块：读取 evidence_chain、CSV 证据表和 Markdown 报告。
- 历史地址库：接收经审核或低风险增量更新。

## 主系统如何调用它

建议调用方式：

```bash
python3 -m modules.wallet_structure.run   --input data/gmgn_candidates_live_run/intel-bot/logs/legacy_intel_bot/wallet_structure_input.json   --output-dir data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token_address>/
```

当前阶段先完成文件契约；实际 Python 入口在 Phase B/C 实现。

## 失败时怎么处理

- GMGN 请求失败：输出 `wallet_structure_status=WALLET_UNKNOWN`，`recommended_state_action=REQUIRE_REVIEW`。
- JSON/CSV 写入失败：返回非 0 exit code，不更新历史库。
- 关键字段缺失：不猜测，字段置 `UNKNOWN` 或 `null`，写入 `evidence_chain` 与 `pause_reasons`。
- 资金/Token 边表缺失：不强判同源或回流。

## 缺字段时怎么处理

- 字符串：`UNKNOWN`
- 数值：空值保留为 `null`，CSV 中为空或 `UNKNOWN`
- 布尔：`null` 表示未知，不等同于 false
- 角色：`普通交易钱包` 或 `噪音钱包` 仅在证据不足且低影响时使用
- 证据等级：缺少关键证据时最高不得超过 E2
- 风险等级：缺少资金/Token 路径时不得因为单个 GMGN 标签升到 R4
