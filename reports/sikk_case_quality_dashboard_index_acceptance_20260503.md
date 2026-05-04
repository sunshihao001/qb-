# SIKK Case File 质量字段接入看板与统一索引验收报告

生成时间：2026-05-03

## 目标

把 Case File 质量、字段来源数量、缺失字段摘要接入：

- `site/dashboard_data.json`
- `site/index.html` / `site/app.js` / `site/style.css` 静态看板展示链路
- `data/gmgn_candidates_live_run/index/position_index.json`
- `data/gmgn_candidates_live_run/index/case_file_index.json`

## 修改范围

### 1. 静态看板数据

文件：`sikk_dashboard_site_builder.py`

已实现：

- 从 case manifest / paper row 聚合：
  - `case_quality_level`
  - `case_completeness_score`
  - `case_field_source_count`
  - `case_field_sources_preview`
  - `evidence_missing_fields`
  - `case_missing_fields`
- `paper_positions.open/closed` 中保留上述字段。
- 单币详情抽屉新增 `Case File 质量与证据缺口` 区块。
- 纸面仓位卡片新增：
  - `档案质量`
  - `字段来源数`
  - `缺失证据`

### 2. 统一索引

文件：`sikk_unified_view_builder.py`

已实现：

- 新增 `case_metric_from_row()`：归一化 Case File 质量摘要。
- 新增 `enrich_rows_with_dashboard_case_metrics()`：用 `site/dashboard_data.json` 中已聚合的 Case File 摘要回填 paper rows。
- `position_index.json` 的 `open_positions/closed_positions` 暴露 Case File 质量字段。
- `case_file_index.json` 的 `cases` 暴露 Case File 质量字段。
- 保持统一索引层只读边界：不采集、不报价、不交易、不签名、不广播。

### 3. 测试

文件：

- `tests/test_sikk_dashboard_site_builder.py`
- `tests/test_sikk_unified_view_builder.py`

新增/增强断言：

- dashboard paper positions 暴露 `case_quality_level` / `case_completeness_score` / `evidence_missing_fields` / `case_field_source_count`。
- app.js 包含中文展示标签：`Case File 质量与证据缺口`、`档案质量`、`字段来源数`、`缺失证据`。
- unified position/case index 暴露 Case File 质量和缺失证据。
- alert index 不包含真实交易执行动作。

## 验证结果

### 编译与专项测试

```bash
python3 -m py_compile sikk_dashboard_site_builder.py sikk_unified_view_builder.py
PYTHONPATH=. pytest -q \
  tests/test_sikk_dashboard_site_builder.py::test_dashboard_paper_positions_expose_case_file_links \
  tests/test_sikk_unified_view_builder.py::test_unified_indexes_expose_case_quality_and_missing_evidence \
  tests/test_sikk_unified_view_builder.py::test_alert_index_is_readonly_and_has_no_trade_actions -q
```

结果：

```text
... [100%]
```

### 组合回归

```bash
PYTHONPATH=. pytest -q \
  tests/test_sikk_dashboard_site_builder.py \
  tests/test_sikk_unified_view_builder.py \
  tests/test_sikk_paper_explanation_builder.py \
  tests/test_sikk_case_field_source_map.py \
  tests/test_sikk_telegram_views.py \
  tests/test_sikk_telegram_entry_gateway.py \
  tests/test_sikk_live_run.py \
  tests/test_sikk_wallet_structure_daily_report.py -q
```

结果：

```text
............................................... [100%]
```

### 重建输出

```bash
PYTHONPATH=. python3 sikk_dashboard_site_builder.py \
  --base-dir data/gmgn_candidates_live_run \
  --output-dir data/gmgn_candidates_live_run/site

PYTHONPATH=. python3 sikk_unified_view_builder.py \
  --base-dir data/gmgn_candidates_live_run
```

结果：

- 静态站重建成功：`token_count=156`
- 统一索引重建成功：9 个 index JSON 写入 `data/gmgn_candidates_live_run/index/`
- `case_file_index.json` 当前 `case_count=183`

### 抽样验收

抽样开放仓位 `LITH`：

- `case_quality_level`: `E2_部分可复盘`
- `case_completeness_score`: `66.6667`
- `evidence_missing_fields`: `发现时市值`、`入场市值`、`paper entry snapshot`
- `case_file_md`: `case_files/paper-GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump-2026-05-02T03_19_42Z.html`

静态看板 `app.js` 已包含：

- `Case File 质量与证据缺口`
- `档案质量`
- `字段来源数`
- `缺失证据`

安全扫描：`alert_forbidden_hits=[]`

## 安全边界

本次修改仅涉及本地 JSON/CSV/静态站/索引展示层：

- 未执行真实 swap。
- 未读取私钥。
- 未签名。
- 未广播。
- 未新增真实交易按钮。
- Telegram / Web / Index 仍为 paper-only、readonly 输出。

## 结论

验收通过。Case File 质量、字段来源数量、缺失字段摘要已进入静态看板与统一索引，可以支持后续 Telegram 面板继续读取这些字段做只读摘要展示。
