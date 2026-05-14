     1|     1|# SIKK Changelog
     2|     2|
     3|     3|## 2026-05-03
     4|     4|
     5|     5|- 启动 Phase B-0.5 Harness 落地：文件驱动、分阶段、可验收、可审计。
     6|     6|- 创建 Harness 四文件：`SIKK_PROJECT_STATE.md`、`SIKK_NEXT_TASK.md`、`SIKK_LESSONS_LEARNED.md`、`SIKK_CHANGELOG.md`。
     7|     7|- 当前任务收敛为：先实现 `sikk_dashboard_site_builder.py` 与 `site/dashboard_data.json`，再生成静态 UI。
     8|     8|- 固定安全边界：paper/readiness/observability only；不真实 swap、不私钥、不自动 broadcast。
     9|     9|
    10|
    11|## 2026-05-03 追加
    12|
    13|- 新增 `sikk_dashboard_site_builder.py`，生成 `site/dashboard_data.json/index.html/app.js/style.css`。
    14|- 新增 `tests/test_sikk_dashboard_site_builder.py`。
    15|- 在 `tests/test_sikk_live_run.py` 增加静态 site 刷新回归测试。
    16|- `sikk_live_run.py` 每轮尾部刷新静态 site；site 失败只写事件，不中断主流程。
    17|- 验收：`9 passed in 0.09s`。
    18|- 审计：未新增真实交易、私钥、自动 broadcast、后端、数据库、登录系统。
    19|

## 2026-05-03 Paper JSON/CSV Sync

- 新增 `sync_paper_position_csvs(root)`。
- 每轮 `sikk_live_run.py` 在 paper runner 后强制从 JSON 重建：
  - `paper_live/paper_positions_open.csv`
  - `paper_live/paper_positions_closed.csv`
- `paper_paths` / manifest now include:
  - `open_positions_csv`
  - `closed_positions_csv`
- `build_wallet_structure_daily_report(...)` 使用刚重建的 closed CSV，避免读取旧 CSV。
- 新增 TDD 回归测试：
  - `test_paper_position_json_csv_sync_rebuilds_open_and_stale_closed_csv`
  - `test_sikk_live_run_syncs_paper_position_csvs_before_reports`
- 标准单轮验证通过：open JSON/CSV = 3/3，closed JSON/CSV = 95/95。
