---
artifact_type: task_routing_rule
status: verified
version: v2.0-stage1
generated_at: 2026-05-07T05:48:09Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 任务路由规则 V2.0 — 阶段 1

## 1. 目标
让 Hermes 能识别 Wallet-Intel 钱包数据语义整合任务，并固定路由到专用工作流，而不是按普通目录整理任务处理。

## 2. 固定 task_type

```text
task_type = wallet_intel_semantic_integration
```

## 3. 路由触发关键词
用户目标、任务名称、文件名、阶段描述、验收描述或上下文中命中以下任一关键词时，必须触发本路由：

```text
钱包数据
钱包采集
钱包事实
钱包画像
钱包交易
结构分析
同源证据
筹码分析
主导侧行为
handoff
旧目录导入
数据整合
wallet intel
source wallet bot
intel bot
旧路径映射
字段字典
数据护照
```

## 4. 路由判定规则

### 4.1 必须进入 Wallet-Intel 工作流
凡是命中以上关键词，且任务目标涉及以下任一动作，必须进入：

```text
wallet_intel_semantic_integration
```

动作包括：

- 设计钱包数据体系
- 整理钱包数据语义层
- 导入旧目录钱包数据
- 建立新旧路径映射
- 建立数据护照
- 建立字段字典
- 检查钱包事实层
- 检查同源证据 / 结构证据
- 检查推断层 / 结论层
- 生成 handoff 包
- 验证 Hermes 是否按 token 理解数据
- 修改或接入 GMGN/OKX collector 到既有钱包结构系统
- 判断 `sikk_sol_full_auto_workflow.py` 与 canonical 钱包系统的主从关系

### 4.2 不得按普通目录整理处理
命中 Wallet-Intel 关键词后，禁止直接路由为：

```text
directory_governance
ordinary_file_cleanup
generic_migration
generic_report_generation
```

如果任务同时涉及目录治理，处理顺序必须是：

```text
Wallet-Intel 语义路由
→ 任务护照
→ 语义分层判断
→ 目录治理作为子步骤
```

不能反过来先按目录整理执行。

### 4.3 不得直接跳代码或创建并行主系统
命中 Wallet-Intel / 钱包结构关键词后，禁止直接进入：

```text
ad_hoc_code_change
new_parallel_workflow
standalone_full_auto_wallet_system
```

必须先生成任务护照并读取固定 workflow。GMGN/OKX collector、CA 分析、K线/筹码/cluster 增强等能力必须接入既有 canonical 钱包结构路线：

```text
modules/source_wallet_bot
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
→ sikk_candidate_state_machine.py / sikk_live_run.py
```

钱包结构专业化主目录与新主写数据路径固定为：

```text
main_project: /root/sikk-gmgn/
new_primary_data_root: /root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

`new_primary_data_root` 只允许承接以下语义层：

```text
wallet_data/raw
wallet_data/normalized
wallet_data/summary
structure_analysis/wallet_fact
structure_analysis/intelligence
structure_analysis/handoff
structure_analysis/reports
manifest
```

不得把以下内容写入 `new_primary_data_root`：

```text
trading_state_machine
paper_runner_output
dashboard_primary_output
private_key_or_signing_or_broadcast_or_swap
research_notes
task_tickets
wallet_intel_collaboration_logs
```

`/root/sikk-wallet-intel/` 仅为 Wallet-Intel 协同 / 总控 / 行为推断工作区；不得作为新钱包结构分析主事实目录、主采集目录或 Source Wallet Bot canonical 数据目录。

`data/gmgn_candidates_live_run/` 仅保留 legacy runtime / dashboard / paper 兼容，不作为新的 Source Wallet Bot 钱包结构主写路径。

`sikk_sol_full_auto_workflow.py` 只允许作为 `legacy_compat_one_shot` 兼容路线，不得作为主入口扩展。

## 5. 路由输出合同
路由器必须输出：

```text
route_decision: wallet_intel_semantic_integration
matched_keywords: [...]
reason: 命中 Wallet-Intel 钱包数据语义整合任务
not_generic_directory_task: true
required_workflow: 11_workflows/wallet_intel_semantic_integration.workflow.md
required_boundaries:
  - 不扫描旧数据目录，除非任务护照授权
  - 不复制旧数据，除非任务护照授权
  - 不移动旧目录
  - 不删除旧目录
  - 不覆盖旧文件
  - 不触发交易
```

## 6. 优先级
Wallet-Intel 路由优先级高于普通目录治理。

```text
wallet_intel_semantic_integration > directory_governance
```

原因：钱包数据整合是语义治理任务，不是文件搬运任务。

## 7. 验证要求
每次新增或修改路由规则后，必须用路由测试样例验证：

- 正例必须命中 `wallet_intel_semantic_integration`
- 反例不得误命中
- 混合任务必须先进入 Wallet-Intel，再把目录治理作为子步骤
- 失败时必须进入路由失败恢复规则
