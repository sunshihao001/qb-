     1|     1|# SIKK Verify Report
     2|     2|
     3|     3|## 验收时间
     4|     4|
     5|     5|2026-05-03T02:50Z
     6|     6|
     7|     7|## 验收范围
     8|     8|
     9|     9|Phase B-0.5 静态 dashboard site：
    10|    10|
    11|    11|- `sikk_dashboard_site_builder.py`
    12|    12|- `data/gmgn_candidates_live_run/site/dashboard_data.json`
    13|    13|- `data/gmgn_candidates_live_run/site/index.html`
    14|    14|- `data/gmgn_candidates_live_run/site/app.js`
    15|    15|- `data/gmgn_candidates_live_run/site/style.css`
    16|    16|- `tests/test_sikk_dashboard_site_builder.py`
    17|    17|
    18|    18|## 验收命令与结果
    19|    19|
    20|    20|```bash
    21|    21|python3 -m py_compile sikk_dashboard_site_builder.py
    22|    22|```
    23|    23|
    24|    24|结果：通过。
    25|    25|
    26|    26|```bash
    27|    27|python3 sikk_dashboard_site_builder.py \
    28|    28|  --base-dir data/gmgn_candidates_live_run \
    29|    29|  --output-dir data/gmgn_candidates_live_run/site
    30|    30|```
    31|    31|
    32|    32|结果：通过，输出：
    33|    33|
    34|    34|```text
    35|    35|status: ok
    36|    36|output_dir: data/gmgn_candidates_live_run/site
    37|    37|token_count: 130
    38|    38|site_files: dashboard_data.json, index.html, app.js, style.css
    39|    39|```
    40|    40|
    41|    41|```bash
    42|    42|python3 -m json.tool data/gmgn_candidates_live_run/site/dashboard_data.json
    43|    43|```
    44|    44|
    45|    45|结果：JSON 可解析。
    46|    46|
    47|    47|```bash
    48|    48|python3 -m pytest tests/test_sikk_dashboard_site_builder.py -q
    49|    49|```
    50|    50|
    51|    51|结果：
    52|    52|
    53|    53|```text
    54|    54|3 passed in 0.05s
    55|    55|```
    56|    56|
    57|    57|## 数据契约检查
    58|    58|
    59|    59|`dashboard_data.json` 已包含必需顶层字段：
    60|    60|
    61|    61|- `kpi`
    62|    62|- `funnel`
    63|    63|- `tokens`
    64|    64|- `opportunities`
    65|    65|- `wallet_structure_summary`
    66|    66|- `wallet_missing_reasons`
    67|    67|- `entry_block_reasons`
    68|    68|- `paper_positions`
    69|    69|- `events`
    70|    70|
    71|    71|额外包含：
    72|    72|
    73|    73|- `metadata`
    74|    74|
    75|    75|## 当前数据摘要
    76|    76|
    77|    77|- token_count：130
    78|    78|- open_positions：2
    79|    79|- closed_positions：2
    80|    80|- 输出目录：`data/gmgn_candidates_live_run/site`
    81|    81|
    82|    82|## 静态文件检查
    83|    83|
    84|    84|以下文件存在：
    85|    85|
    86|    86|- `data/gmgn_candidates_live_run/site/dashboard_data.json`
    87|    87|- `data/gmgn_candidates_live_run/site/index.html`
    88|    88|- `data/gmgn_candidates_live_run/site/app.js`
    89|    89|- `data/gmgn_candidates_live_run/site/style.css`
    90|    90|
    91|    91|## Verifier 结论
    92|    92|
    93|    93|通过。当前静态 dashboard site 可以从现有 live run 输出生成数据层和纯静态页面文件。
    94|    94|
    95|    95|边界保持：只读观察、纸面验证、不执行真实 swap、不读取私钥、不自动 broadcast。
    96|    96|
    97|
    98|## 接入后追加验收
    99|
   100|接入 `sikk_live_run.py` 每轮尾部刷新 site 后，追加运行：
   101|
   102|```bash
   103|python3 -m py_compile sikk_dashboard_site_builder.py sikk_live_run.py
   104|python3 -m pytest tests/test_sikk_dashboard_site_builder.py tests/test_sikk_live_run.py -q
   105|python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
   106|```
   107|
   108|结果：
   109|
   110|```text
   111|9 passed in 0.09s
   112|final_static_site_verify_ok
   113|token_count 130
   114|```
   115|
   116|新增回归测试：
   117|
   118|- `test_sikk_live_run_refreshes_static_dashboard_site`
   119|
   120|该测试确认：
   121|
   122|- `run_live_once(...)` 会生成 `site/dashboard_data.json`
   123|- 会生成 `site/index.html`
   124|- 会生成 `site/app.js`
   125|- 会生成 `site/style.css`
   126|- manifest/runtime 输出包含 `site_dashboard_data_json`
   127|- site 数据层可以读取 paper open position
   128|

## Paper JSON/CSV 同步追加验收

时间：2026-05-03

TDD 红灯：新增测试先失败：

```text
ImportError: cannot import name 'sync_paper_position_csvs'
open csv missing
```

实现后验收：

```bash
python3 -m py_compile sikk_live_run.py sikk_dashboard_site_builder.py
python3 -m pytest tests/test_sikk_live_run.py tests/test_sikk_dashboard_site_builder.py -q
```

结果：

```text
11 passed in 0.13s
```

标准单轮主流程：

```bash
python3 sikk_live_run.py --output-root data/gmgn_candidates_live_run --limit 50 --quote-sources okx --default-quote-amount-sol 0.01 --mode once
```

运行成功，关键输出：

```text
paper_positions_open json_rows 3 csv_rows 3 csv_exists True
paper_positions_closed json_rows 95 csv_rows 95 csv_exists True
site_keys_ok True
site_token_count 137
manifest_paper_csvs data/gmgn_candidates_live_run/paper_live/paper_positions_open.csv data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv
safety False False False
```
