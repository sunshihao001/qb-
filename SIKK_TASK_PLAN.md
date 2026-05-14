# SIKK Task Plan

## 任务名称

Phase B-0.5 本地静态专业可视化控制台。

## Planner 输出

### 目标

在不改变真实交易/纸面交易逻辑的前提下，新增一个只读静态 site builder，把现有 SIKK live 输出汇总成 `dashboard_data.json`，并生成纯静态 `index.html/app.js/style.css`。

### 改动边界

允许新增/修改：

- `sikk_dashboard_site_builder.py`
- `data/gmgn_candidates_live_run/site/dashboard_data.json`
- `data/gmgn_candidates_live_run/site/index.html`
- `data/gmgn_candidates_live_run/site/app.js`
- `data/gmgn_candidates_live_run/site/style.css`
- Harness 报告文件

暂不接入：

- `sikk_live_run.py` 每轮尾部刷新 site

接入步骤放到验收稳定之后。

### 数据契约

`dashboard_data.json` 顶层必须包含：

- `metadata`
- `kpi`
- `funnel`
- `tokens`
- `opportunities`
- `wallet_structure_summary`
- `wallet_missing_reasons`
- `entry_block_reasons`
- `paper_positions`
- `events`

### 验收

运行：

```bash
python3 -m py_compile sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 80
```

并确认四个 site 文件存在。

### 审计点

- 是否新增真实交易路径。
- 是否修改 paper runner 逻辑。
- 是否新增后端/数据库/登录/React。
- 是否删除已有模块。
- 是否只读取现有输出。
