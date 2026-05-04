# SIKK 网站实战档案链接修复验收报告（2026-05-03）

## 问题

用户反馈：代币的具体实战档案代码不全，在网站上无法打开。

侦察结果确认：

- `site/dashboard_data.json` 里的 `case_file_md` 原来指向 `data/gmgn_candidates_live_run/paper_live/case_files/*.md`。
- 手机/浏览器访问静态站点 `/site/index.html` 时，这类项目内路径不在静态站点根目录下，点击会 404 或不可访问。
- `.md` 直接由 `python3 -m http.server` 提供时可能没有 UTF-8 charset，中文在浏览器中会乱码。

## 修改文件

- `sikk_dashboard_site_builder.py`
  - 新增 `publish_case_files_for_site()`：把 paper case files 发布到 `site/case_files/`。
  - 写入 `dashboard_data.json` 前，自动把 `case_file_md/case_file_json` 改成网站可访问相对路径。
  - 对 `.md` 实战档案额外生成 `.html` 阅读页，带 `<meta charset="utf-8">`，避免手机浏览器中文乱码。
  - 保留原始 `.md` 与 `.json` 文件副本。
- `tests/test_sikk_dashboard_site_builder.py`
  - 加强测试：要求网站 payload 使用 `case_files/*.html/json` 相对路径，且文件真实复制/生成。

## 输出文件

- `data/gmgn_candidates_live_run/site/dashboard_data.json`
- `data/gmgn_candidates_live_run/site/case_files/*.html`
- `data/gmgn_candidates_live_run/site/case_files/*.md`
- `data/gmgn_candidates_live_run/site/case_files/*.json`

## 验收命令

```bash
python3 -m py_compile sikk_dashboard_site_builder.py
PYTHONPATH=. pytest -q tests/test_sikk_dashboard_site_builder.py::test_dashboard_paper_positions_expose_case_file_links -q
PYTHONPATH=. python3 sikk_dashboard_site_builder.py --base-dir data/gmgn_candidates_live_run --output-dir data/gmgn_candidates_live_run/site
PYTHONPATH=. pytest -q tests/test_sikk_dashboard_site_builder.py tests/test_sikk_telegram_entry_gateway.py tests/test_sikk_telegram_bot_handler_phase_4_7.py tests/test_sikk_telegram_views.py tests/test_sikk_unified_view_builder.py tests/test_sikk_live_run.py tests/test_sikk_wallet_structure_daily_report.py tests/test_sikk_system_audit.py -q
```

## 验收结果

- 单测：PASS
- 相关回归：48 passed
- 重建 site：PASS
- case rows：183
- static publish missing：[]
- 浏览器验证：PASS

浏览器实际验证 LITH：

- 列表搜索：`LITH`
- 详情抽屉：打开成功
- 实战档案链接：`case_files/paper-GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump-2026-05-02T03_19_42Z.html`
- 页面标题：`Paper Case File: $LITH`
- 中文内容：可读，包含 `纸面入场`、`持仓过程`

## 手机访问

主页面：

```text
http://96.126.130.99:8765/index.html
```

LITH 实战档案例子：

```text
http://96.126.130.99:8765/case_files/paper-GC3T8XboCofhBPs5U48DJgp6cxxMeu1CBZXgB2dopump-2026-05-02T03_19_42Z.html
```

也可以在主页面搜索代币，打开单币详情后点击 `实战档案`。

## 安全边界

PASS：

- 未执行真实 swap。
- 未读取私钥。
- 未签名。
- 未广播。
- 未新增真实交易按钮。
- 本次只改静态站点文件发布与只读展示。
