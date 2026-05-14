# HER_DOC Full Trading System Gap Scan — 总目标 / 阶段目标准备工作扫描

- doc_id: `HER_DOC_FULL_TRADING_SYSTEM_GAP_SCAN_20260514`
- created_at: `2026-05-14T10:12:05+00:00`
- scope: `/root/sikk-gmgn` 全交易体系
- mode: HER_DOC safe-mode audit/gap mode
- safety_boundary: paper-only / observe-only / no swap / no private key / no signature / no broadcast

## 用户目标

根据 SIKK 交易结构系统的总目标，扫描全交易体系的每一个系统层、阶段和 runtime 流程，回答：

1. 离“方法论里的总目标”还差哪些准备工作；
2. 每个阶段的阶段目标还差哪些准备；
3. 哪些缺少部件需要发给 GPT 做专业研究；
4. GPT 返回资料后应该补充到哪些系统体系数据、字段合约、规则库、runner、验收或 handoff。

## 总目标定义

SIKK 交易结构系统不是两套系统，而是一套 HER 总控闭环交易结构系统。目标是让真实代币数据按阶段通过：

```text
候选接入
→ 源数据事实
→ 钱包实体
→ 筹码结构
→ 证据控制
→ 场景识别
→ 策略门禁
→ 执行风控
→ 复盘回放
→ 系统升级
```

要求输出可追踪的分析、判断、推理和 paper-only 决策，并通过 Review/Upgrade 回流到方法论、控制器、数据平面和 runner。

## 扫描对象

### 系统层

- HER 总控
- K00 知识摄取 / KV cache
- Methodology Plane
- P00 系统建造 / 方法论编译
- Governance Plane
- Domain Plane
- Data Plane
- Full Control Plane
- Trace Plane
- Acceptance Plane
- Handoff Plane
- Runner / Tool Binding
- Paper-only Runtime
- Review / Upgrade Loop

### 业务阶段

- P01 Candidate Intake / 候选接入
- P02 Source Data Fact / 源数据事实
- P03 Wallet Entity / 钱包实体
- P04 Chip Structure / 筹码结构
- P05 Evidence Control / 证据控制
- P06 Scenario Recognition / 场景识别
- P07 Strategy Gate / 策略门禁
- P08 Execution Risk / 执行风控
- P09 Review Replay / 复盘回放
- P10 Self Upgrade / 系统自升级

### 当前 runtime 流程

- `sikk_live_run.py`
- `run_sikk_gmgn_pipeline.py`
- GMGN candidate discovery
- Kline / signal
- state machine
- wallet-structure gate
- quote/security
- paper live runner
- failure attribution
- daily report
- dashboard / static site
- unified index

## 必须输出的扫描结论

每个系统层和业务阶段都必须输出：

```text
stage_id
stage_goal
current_assets_found
current_runtime_binding
acceptance_status:
  file_level
  structure_level
  semantic_level
  consumption_level
  runtime_level
missing_preparations
missing_research_materials_for_gpt
suggested_gpt_research_prompt
where_to_apply_returned_materials
priority
blocking_policy
```

## 不允许的结论

- 不允许把 READY_WITH_GAPS 说成 ACCEPTED
- 不允许把 paper-ready 说成实盘授权
- 不允许把 wallet support 说成买入信号
- 不允许让 review 结果直接修改实时规则
- 不允许生成真实交易命令

## 预期最终产物

- `full_trading_system_gap_matrix.json/md`
- `stage_goal_preparation_gap_report.json/md`
- `gpt_research_request_pack.json/md`
- `methodology_total_goal_gap_summary.json/md`
- `her_doc_full_gap_scan_verification.json`
