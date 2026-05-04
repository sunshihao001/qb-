# S03：旧 GMGN / OKX 钱包结构系统作为正式上游 → 网站待补字段回填任务

文档来源: `docs/imported/chatgpt_share_69f809c6_section_index.md`
原始链接: https://chatgpt.com/share/69f809c6-e7ac-83ab-823a-02d6cd8e5426
Section: S03
优先级: P0

## 本节目标

把 GPT 文档里“旧 GMGN / OKX 钱包结构系统可以作为正式上游数据源，但不能直接把旧 AI 文字判断当事实”的方法，落成当前项目的字段盘点与回填路线。

本节不直接开启真实交易，不改 swap/broadcast，不新增主入口。

## 涉及模块

需要读取/侦察：

- `sikk_live_run.py`
- `sikk_dashboard_builder.py` 或当前生成 `site/dashboard_data.json` 的模块
- `sikk_wallet_structure_gate.py`
- `sikk_candidate_wallet_structure_pipeline.py`
- `sikk_same_source_grouping.py`
- `sikk_wallet_structure_snapshot.py`
- `sikk_wallet_structure_daily_report.py`
- `sikk_okx_cluster_holding_analyzer.py`
- `sikk_okx_cluster_delta.py`
- `sikk_paper_live_runner.py`
- `sikk_paper_explanation_builder.py`
- `sikk_case_data_backfill.py`
- `sikk_case_data_completeness_auditor.py`
- `sikk_unified_view_builder.py`
- `data/gmgn_candidates_live_run/site/dashboard_data.json`
- `data/gmgn_candidates_live_run/paper_live/*.json/csv`
- `data/gmgn_candidates_live_run/paper_live/case_files/*.json`
- `data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_*.csv/json/md`
- `data/gmgn_candidates_live_run/okx_cluster/` 如存在

## 允许修改的文件

第一轮只做审计，默认不改代码。允许新增报告与矩阵：

- `reports/chatgpt_share_69f809c6/S03_field_source_matrix.csv`
- `reports/chatgpt_share_69f809c6/S03_field_source_matrix.md`
- `reports/chatgpt_share_69f809c6/S03_missing_fields_backfill_plan.md`
- `reports/chatgpt_share_69f809c6/S03_acceptance_report.md`

如后续进入实现轮，才允许改：

- dashboard builder 相关文件
- case data backfill 相关文件
- unified view builder 相关文件
- 对应 tests

## 禁止修改的文件/行为

- 禁止改真实交易逻辑
- 禁止新增 BUY / SELL / SWAP / EXECUTE / APPROVE / BROADCAST
- 禁止读取/写入/打印私钥、bot token、webhook_url
- 禁止新增并行主入口替代 `sikk_live_run.py`
- 禁止删除已有 runtime/dashboard/notifier/paper runner 模块
- 禁止把旧 AI 判断“疑似庄家/必跟/确定同源”直接写进事实字段

## 新增字段/矩阵字段

`S03_field_source_matrix.csv` 至少包含：

- `展示入口`
- `字段名`
- `当前值示例`
- `是否待补`
- `字段类型`
- `当前来源文件`
- `可回填来源文件`
- `source_trace_required`
- `缺失原因`
- `是否原始事实`
- `是否AI推断`
- `evidence_level_required`
- `可否用于门禁`
- `可否用于CaseFile复盘`
- `建议动作`

字段类型枚举：

- `TOKEN_BASIC`
- `MARKET_CAP_CONTEXT`
- `WALLET_STRUCTURE`
- `OKX_CLUSTER`
- `QUOTE_SECURITY`
- `PAPER_POSITION`
- `CASE_FILE`
- `AUTO_REVIEW`
- `DASHBOARD_DISPLAY`
- `AI_EXPLANATION`

## 输入文件

- `data/gmgn_candidates_live_run/site/dashboard_data.json`
- `data/gmgn_candidates_live_run/live_state.json`
- `data/gmgn_candidates_live_run/live_run_manifest.json`
- `data/gmgn_candidates_live_run/paper_live/paper_positions_open.json`
- `data/gmgn_candidates_live_run/paper_live/paper_positions_closed.json`
- `data/gmgn_candidates_live_run/paper_live/paper_positions_open.csv`
- `data/gmgn_candidates_live_run/paper_live/paper_positions_closed.csv`
- `data/gmgn_candidates_live_run/paper_live/case_files/case_files_manifest.json`
- `data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_*.csv`
- `data/gmgn_candidates_live_run/reports/wallet_structure_daily_report_*.json`

## 输出文件

- `reports/chatgpt_share_69f809c6/S03_field_source_matrix.csv`
- `reports/chatgpt_share_69f809c6/S03_field_source_matrix.md`
- `reports/chatgpt_share_69f809c6/S03_missing_fields_backfill_plan.md`
- `reports/chatgpt_share_69f809c6/S03_acceptance_report.md`

## 验收命令

```bash
cd /root/sikk-gmgn
PYTHONPATH=/root/sikk-gmgn python3 sikk_live_run.py --mode once --output-root data/gmgn_candidates_live_run --limit 5 --quote-sources none
python3 - <<'PY'
import json
from pathlib import Path
p=Path('data/gmgn_candidates_live_run/site/dashboard_data.json')
print('dashboard_data_exists=', p.exists())
print('dashboard_data_size=', p.stat().st_size if p.exists() else 0)
if p.exists():
    data=json.loads(p.read_text())
    print('top_keys=', sorted(data.keys())[:30])
    print('token_count=', len(data.get('tokens', [])))
PY
```

如生成矩阵脚本后，追加：

```bash
test -f reports/chatgpt_share_69f809c6/S03_field_source_matrix.csv
head -20 reports/chatgpt_share_69f809c6/S03_field_source_matrix.md
```

## 测试命令

当前审计轮不要求新增 pytest。若进入实现轮，必须新增或更新相关 tests，并运行：

```bash
PYTHONPATH=/root/sikk-gmgn python3 -m pytest -q
```

## 完成标准

- 已列出 dashboard/site/case/paper 中所有明显“待补/缺失/unknown/待查”字段。
- 每个字段至少有一个分类：可直接回填、需重新计算、只能AI解释、不可还原、应继续待补。
- 每个可回填字段都指出具体来源文件和 `source_trace`。
- 每个 AI 推断字段都要求 `AI_INFERRED` 与 `evidence_level`。
- 报告明确说明哪些旧 GMGN/OKX 数据可以用，哪些不能直接用。
- 主入口 smoke run 成功。
- 安全开关仍为 paper-only/no-swap/no-broadcast。

## 风险边界

本节只建立字段来源与回填计划，不进行真实交易。任何字段补全不得改变真实交易状态，不得把 dashboard 展示字段当买入信号。
