     1|     1|# SIKK Audit Report
     2|     2|
     3|     3|## 审计时间
     4|     4|
     5|     5|2026-05-03T02:50Z
     6|     6|
     7|     7|## 审计范围
     8|     8|
     9|     9|本轮新增/生成内容：
    10|    10|
    11|    11|- `sikk_dashboard_site_builder.py`
    12|    12|- `tests/test_sikk_dashboard_site_builder.py`
    13|    13|- `data/gmgn_candidates_live_run/site/dashboard_data.json`
    14|    14|- `data/gmgn_candidates_live_run/site/index.html`
    15|    15|- `data/gmgn_candidates_live_run/site/app.js`
    16|    16|- `data/gmgn_candidates_live_run/site/style.css`
    17|    17|- Harness 文档与 AGENTS 约束文件
    18|    18|
    19|    19|## 审计命令
    20|    20|
    21|    21|```bash
    22|    22|python3 - <<'PY'
    23|    23|from pathlib import Path
    24|    24|files=[
    25|    25|  Path('sikk_dashboard_site_builder.py'),
    26|    26|  Path('data/gmgn_candidates_live_run/site/index.html'),
    27|    27|  Path('data/gmgn_candidates_live_run/site/app.js'),
    28|    28|  Path('data/gmgn_candidates_live_run/site/style.css'),
    29|    29|  Path('tests/test_sikk_dashboard_site_builder.py'),
    30|    30|]
    31|    31|needles=['gmgn-cli swap','gmgn-cli multi-swap','order strategy create','onchainos swap execute','swap execute','private key','api key','bot_token','webhook_url','SECRET','PRIVATE_KEY']
    32|    32|for f in files:
    33|    33|    text=f.read_text(encoding='utf-8', errors='replace')
    34|    34|    hits=[n for n in needles if n.lower() in text.lower()]
    35|    35|    print(f'{f}: hits={hits}')
    36|    36|PY
    37|    37|```
    38|    38|
    39|    39|结果：新增 builder/site/test 文件均无命中危险执行或密钥字段。
    40|    40|
    41|    41|```bash
    42|    42|python3 - <<'PY'
    43|    43|from pathlib import Path
    44|    44|text=Path('sikk_dashboard_site_builder.py').read_text(encoding='utf-8')
    45|    45|assert 'subprocess' not in text
    46|    46|assert 'requests' not in text
    47|    47|assert 'socket' not in text
    48|    48|assert 'gmgn-cli swap' not in text
    49|    49|assert 'onchainos swap execute' not in text
    50|    50|assert 'write_site_files' in text
    51|    51|assert 'DASHBOARD_BOUNDARY' in text
    52|    52|print('audit_static_builder_no_execution_paths_ok')
    53|    53|PY
    54|    54|```
    55|    55|
    56|    56|结果：通过。
    57|    57|
    58|    58|## 审计结论
    59|    59|
    60|    60|通过。
    61|    61|
    62|    62|本轮新增 builder 是只读聚合器：
    63|    63|
    64|    64|- 读取 `data/gmgn_candidates_live_run` 现有输出。
    65|    65|- 只写 `data/gmgn_candidates_live_run/site/*` 静态文件。
    66|    66|- 不调用 `subprocess`。
    67|    67|- 不导入 `requests` 或网络库。
    68|    68|- 不新增后端、数据库、登录系统。
    69|    69|- 不新增真实交易按钮。
    70|    70|- 不新增 GMGN/OKX swap execution 路径。
    71|    71|- 不读取、保存或输出私钥/API key/bot token/webhook URL。
    72|    72|
    73|    73|## 仍需保留的边界
    74|    74|
    75|    75|- 当前 site 仅用于观察、筛选、复盘。
    76|    76|- `priority_level` 仅用于 dashboard 排序，不是买入信号。
    77|    77|- `WALLET_SUPPORT` 不能绕过 signal/quote/security/paper gates。
    78|    78|- `NO_WALLET_INPUT` 是复查提示，不是安全许可。
    79|    79|
    80|    80|## 待下一步处理
    81|    81|
    82|    82|稳定后再接入 `sikk_live_run.py` 每轮尾部刷新 site。接入时必须保证：
    83|    83|
    84|    84|- dashboard site 生成失败不能中断主流程。
    85|    85|- 失败只写事件或 warning。
    86|    86|- 不改变 paper runner / state machine / quote/security 决策逻辑。
    87|    87|- 不引入真实交易执行能力。
    88|    88|
    89|
    90|## 接入后追加审计
    91|
    92|追加审计范围：
    93|
    94|- `sikk_live_run.py`
    95|- `sikk_dashboard_site_builder.py`
    96|- `tests/test_sikk_live_run.py`
    97|- `tests/test_sikk_dashboard_site_builder.py`
    98|- `site/index.html/app.js/style.css`
    99|
   100|追加审计结果：
   101|
   102|```text
   103|sikk_dashboard_site_builder.py: hits=[]
   104|sikk_live_run.py: hits=[]
   105|tests/test_sikk_dashboard_site_builder.py: hits=[]
   106|tests/test_sikk_live_run.py: hits=[]
   107|data/gmgn_candidates_live_run/site/index.html: hits=[]
   108|data/gmgn_candidates_live_run/site/app.js: hits=[]
   109|data/gmgn_candidates_live_run/site/style.css: hits=[]
   110|final_audit_live_run_site_integration_ok
   111|```
   112|
   113|接入方式审计：
   114|
   115|- `sikk_live_run.py` 只在每轮尾部调用 `_write_static_dashboard_site(root)`。
   116|- `_write_static_dashboard_site` 只刷新 `root/site/*` 静态文件。
   117|- site 生成失败会写 `STATIC_DASHBOARD_SITE_ERROR`，不会中断主流程。
   118|- 未新增真实 swap、私钥、签名、broadcast、交易按钮、后端、数据库或登录。
   119|

## Paper JSON/CSV 同步追加审计

审计范围：

- `sikk_live_run.py`
- `tests/test_sikk_live_run.py`

安全 grep：

```text
sikk_live_run.py: hits=[]
tests/test_sikk_live_run.py: hits=[]
paper_sync_audit_ok
```

边界确认：

- `sync_paper_position_csvs(root)` 只从 JSON 重建 CSV。
- 不改变 paper 仓位状态。
- 不执行真实 swap。
- 不读取私钥/API key/bot token/webhook。
- `live_run_manifest.json` 仍为：`real_swap_enabled=false`、`broadcast_allowed=false`、`confirmation_enabled=false`。
