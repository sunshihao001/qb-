# SIKK Next Task

## 当前任务

按 Harness 工程方式落地 Phase B-0.5 本地静态可视化控制台。

## 执行顺序

1. 创建 Harness 四文件。
2. 只实现 `sikk_dashboard_site_builder.py`，先生成 `dashboard_data.json`。
3. 再生成 `site/index.html` / `site/app.js` / `site/style.css`。
4. Verifier 跑验收。
5. Auditor 审计边界。
6. 确认稳定后再接入 `sikk_live_run.py` 每轮尾部刷新 site。

## 本轮允许新增/修改

```text
SIKK_PROJECT_STATE.md
SIKK_NEXT_TASK.md
SIKK_LESSONS_LEARNED.md
SIKK_CHANGELOG.md
SIKK_TASK_PLAN.md
SIKK_BUILD_REPORT.md
SIKK_VERIFY_REPORT.md
SIKK_AUDIT_REPORT.md
AGENTS.md
data/gmgn_candidates_live_run/site/AGENTS.md
sikk_dashboard_site_builder.py
data/gmgn_candidates_live_run/site/dashboard_data.json
data/gmgn_candidates_live_run/site/index.html
data/gmgn_candidates_live_run/site/app.js
data/gmgn_candidates_live_run/site/style.css
```

## 数据来源

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

## `dashboard_data.json` 必须包含

```text
kpi
funnel
tokens
opportunities
wallet_structure_summary
wallet_missing_reasons
entry_block_reasons
paper_positions
events
```

## 验收命令

```bash
cd /root/sikk-gmgn
python3 -m py_compile sikk_dashboard_site_builder.py
python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json | head -n 80
python3 - <<'PY'
import json
from pathlib import Path
p=Path('data/gmgn_candidates_live_run/site/dashboard_data.json')
d=json.loads(p.read_text())
required=['kpi','funnel','tokens','opportunities','wallet_structure_summary','wallet_missing_reasons','entry_block_reasons','paper_positions','events']
missing=[k for k in required if k not in d]
assert not missing, missing
for f in ['index.html','app.js','style.css','dashboard_data.json']:
    assert (Path('data/gmgn_candidates_live_run/site')/f).exists(), f
print('dashboard_site_acceptance_ok')
PY
```

## 禁止范围

- 不改真实交易逻辑。
- 不接真实 swap。
- 不新增后端 / 数据库 / 登录。
- 不删除已有模块。
- 不改 paper runner 交易逻辑。
- 不输出任何 secret / token / webhook / API key 真实值。
