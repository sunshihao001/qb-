# 工作包3审计报告：Explainability Engine

- 工作包：新增 `sikk_explainability_engine.py` 专业解释引擎、补测试、生成解释报告
- 分支：`sikk-paper-audit-20260502`
- 范围：paper-only / readonly explainability
- 安全边界：未执行真实交易、未调用 gmgn_swap/gmgn_cooking、未广播交易、未使用 yolo

## 实现内容

- 新增 `sikk_explainability_engine.py`
  - 读取既有输出：
    - `token_status.json` / `live_state.json`
    - `wallet_structure_decision.json` / `candidate_wallet_structure_summary.json`
    - dominant lifecycle / `process_trace.jsonl`
    - `quote_security/candidate_quote_security_summary.json`
    - `paper_live/paper_positions_open.json`
    - `paper_live/paper_positions_closed.json`
    - `paper_live/failure_attribution.jsonl`
  - 输出：
    - `data/gmgn_candidates_live_run/explainability_report.json`
    - `data/gmgn_candidates_live_run/explainability_report.md`
  - 对每个 token 固定回答：
    - 为什么发现
    - 为什么观察
    - 为什么支持
    - 为什么暂停
    - 为什么阻断
    - 为什么进入paper
    - 为什么退出
    - 为什么失败
    - 下一步看什么
    - 主要失效条件
    - 替代假设
  - 缺失字段/缺失文件统一标记为 `证据缺失/待复查`，不编造解释。
  - 保留原始文件引用与字段名，形成中文证据链。
  - 明确 `non_decision_note`：只解释已有结果，不重新裁决。

- 新增 `tests/test_sikk_explainability_engine.py`
  - 覆盖完整证据链：支持、进入 paper、引用原始文件。
  - 覆盖缺输入：标记 `证据缺失/待复查`，不新增结论。
  - 覆盖暂停、阻断、退出、失败归因：引用 quote/security、wallet、paper closed、failure attribution。

## 生成结果

- 解释 JSON：`data/gmgn_candidates_live_run/explainability_report.json`
- 解释 Markdown：`data/gmgn_candidates_live_run/explainability_report.md`

## 测试结果

- 指定测试：`PYTHONPATH=/root/sikk-gmgn pytest -q tests/test_sikk_explainability_engine.py`
  - 结果：`3 passed in 0.03s`

- 全量测试：`PYTHONPATH=/root/sikk-gmgn pytest -q`
  - 结果：`124 passed in 9.63s`

## 审计结论

- 验收项：不重新裁决，只解释已有结果 —— 通过。
- 验收项：缺输入显示 `证据缺失/待复查`，不编造 —— 通过。
- 验收项：中文证据链，保留原始文件引用 —— 通过。
- 验收项：paper-only，不触碰真实交易 —— 通过。
