# SIKK 输出目录治理规范

## 任务名称

输出目录治理。

## 范围

本规范只治理钱包数据与结构分析输出目录，不重写钱包判断逻辑，不重写结构分析逻辑，不接交易、不接状态机、不做 paper runner。

## 新模板目录

每个 token 目录下新增两个标准模板目录：

```text
<token_dir>/wallet_data/
<token_dir>/structure_analysis/
```

### wallet_data/

只放钱包事实、钱包标准化、钱包证据数据。

允许文件类型：

- `wallet_trade_normalized.json`
- `wallet_entity_profile_normalized.json`
- `same_source_evidence_normalized.json`
- `wallet_intelligence_decision.json`
- `wallet_structure_normalized.json`
- `chip_distribution_summary.json`
- `same_source_groups.json`
- `fund_flow_edges.csv`
- `address_history.json`
- `wallet_fact_report.md`
- `wallet_fact_package_manifest.json`

### structure_analysis/

只放结构聚合、角色分类、结构快照、GMGN 备注与结构结论。

允许文件类型：

- `early_wallet_raw.csv`
- `wallet_classification.csv`
- `candidate_groups.csv`
- `gmgn_note_table.csv`
- `wallet_structure_decision.json`
- `wallet_structure_summary.md`
- `snapshots/*.json`

## 兼容规则

1. 不删除旧文件。
2. 不移动旧文件。
3. 旧路径继续保留兼容。
4. 治理时只复制到新目录。
5. 新输出优先写入新目录。
6. 如必须兼容旧调用方，可同时写旧目录或保留读取 fallback。
7. `manifest` 必须记录旧路径到新路径映射。

## manifest 要求

每次治理必须生成：

```text
<output_root>/directory_governance_manifest.json
```

必须包含：

- `task_name`
- `generated_at`
- `mode`
- `safety_boundaries`
- `new_directory_templates`
- `mappings[]`

每条 `mappings[]` 至少包含：

- `token_address`
- `category`: `wallet_data` 或 `structure_analysis`
- `old_path`
- `new_path`
- `action`: 固定为 `copied`
- `sha256`
- `size_bytes`

## 禁止事项

- 不接交易。
- 不接状态机。
- 不做 paper runner。
- 不读取私钥。
- 不签名。
- 不广播。
- 不 swap。
- 不把结构结论改写成买卖信号。
