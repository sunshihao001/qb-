# HER_DOC 自动化修复路线 / Auto Repair Route

## 最高认知

> 最高认知： SIKK 交易结构系统的目标不是生成流程图，也不是把每个阶段文档写漂亮。 最终目标是： 让真实 token / candidate batch 在 HER 总控闭环下， 按 P01-P10 完成事实采集、钱包结构推理、筹码结构推理、证据与反证控制、场景识别、策略门禁、paper-only 执行风控、P09 复盘回放、P10 受控升级。 所以当前正确选择不是直接分阶段补全， 而是先使用 HER_DOC-skill 对全体系做目标差距扫描， 找出总目标还差什么、每个阶段还差什么、R00 为什么还不能跑真实 token、哪些缺口需要 GPT 深研、哪些缺口可以 HER 直接落地。 流程不是目的。 流程是为了让代币判断不跳步、不硬猜、可反证、可验收、可回放、可升级。

## 当前结论

- 当前不是“直接分阶段补全文档”的阶段。
- 当前是“HER_DOC 全体系目标差距扫描 → 缺口分流 → 自动化修复任务包 → 验收”的阶段。
- 状态保持：`READY_WITH_GAPS`，不能标记为 `ACCEPTED`，更不能标记为实盘可用。
- 修复方向：优先让真实 token / candidate batch 可以按 P01-P10 产生可追踪证据，而不是继续写漂亮模板。

## 一、HER 可以直接落地的任务

### AUTO_REPAIR_001_RUNTIME_RUNNER_REGISTRY — 建立 R00/07_runners 运行器注册与 P01-P10 phase_runner_binding
- 优先级：`P0_BLOCKING`
- HER_DOC 阶段：`F00→V00→A00→H00`
- 应用场景：每轮 sikk_live_run.py 或 fixed candidate batch 运行前，总控可根据 phase_runner_binding 判断哪个 runner 可合法执行。
- 目标文件/目录：
  - `sikk_stable_trader_os/07_runners/runner_registry.yaml`
  - `sikk_stable_trader_os/07_runners/phase_runner_binding.yaml`
  - `sikk_stable_trader_os/07_runners/runner_failure_policy.yaml`
  - `sikk_stable_trader_os/07_runners/validation_runner_registry.yaml`
- 验收：
  - 文件级 PASS
  - 结构级 PASS
  - runner 不得绕过 Phase Controller
  - 仍为 paper-only
- 仍缺数据/证据：
  - 真实 token batch 下每个 phase runner 的运行证据
  - runner 输出与 phase_output_index 的消费证据

### AUTO_REPAIR_002_GOAL_CONTEXT_LOADING — 补 runtime goal context loading 与 goal consumption report
- 优先级：`P0_BLOCKING`
- HER_DOC 阶段：`F00→V00→A00`
- 应用场景：每轮 runtime 读取 operator_goal、phase_goal、methodology_goal、acceptance_goal、forbidden_action_policy，并写 consumption report。
- 目标文件/目录：
  - `sikk_stable_trader_os/00_control/runtime_goal_context.schema.json`
  - `sikk_stable_trader_os/00_trace/goal_consumption_report.schema.json`
  - `modules/her_runtime_bridge/goal_context_loader.py`
- 验收：
  - goal→phase→runner→artifact→acceptance 可追踪
  - 缺 goal 时降级 READY_WITH_GAPS，不假装 ACCEPTED
- 仍缺数据/证据：
  - runtime 实际调用记录
  - 每轮 token/candidate run_id 的 goal consumption JSON

### AUTO_REPAIR_003_PHASE_OUTPUT_INDEX_TRACE — 补 phase_output_index 与 runner_execution_trace 自动写入
- 优先级：`P0_BLOCKING`
- HER_DOC 阶段：`F00→V00→A00→H00`
- 应用场景：每个 P01-P10 阶段输出后写入统一索引和 trace，dashboard/验收/复盘都读这一层。
- 目标文件/目录：
  - `sikk_stable_trader_os/00_control/phase_output_index.json`
  - `sikk_stable_trader_os/00_trace/runner_execution_trace.yaml`
  - `modules/her_runtime_bridge/phase_output_indexer.py`
- 验收：
  - 每个 token/run_id 有 phase_id、runner_id、input_ref、output_ref、status、evidence_level
  - 索引失败不得影响 paper-only 主流程
- 仍缺数据/证据：
  - 真实 runtime 输出路径覆盖率
  - 失败重试/恢复 trace

### AUTO_REPAIR_004_WALLET_STRUCTURE_RUNTIME_EVIDENCE — 修复/接通 P03-P04 钱包结构与筹码结构 runtime evidence
- 优先级：`P0_BLOCKING`
- HER_DOC 阶段：`F00→V00→A00`
- 应用场景：真实 token/candidate batch 必须有钱包实体、同源组、资金路径、筹码库存、派发进度、主导侧成本区 evidence。
- 目标文件/目录：
  - `data/gmgn_candidates_live_run/wallet_structure/`
  - `data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/`
  - `modules/wallet_structure/`
  - `sikk_stable_trader_os/00_data/wallet_structure_field_contract.yaml`
- 验收：
  - P03/P04 不能只靠空目录或摘要
  - WALLET_SUPPORT 不等于买入信号
  - 缺钱包事实时 P07 不得 PAPER_READY
- 仍缺数据/证据：
  - 最新 live run 的 wallet_structure summary 是否存在
  - GMGN wallet facts 原始来源质量
  - 筹码字段覆盖率

### AUTO_REPAIR_005_HANDOFF_CONSUMPTION_ACCEPTANCE — 补 P01-P10 handoff consumption status 与消费级/运行级 acceptance runner
- 优先级：`P0_BLOCKING`
- HER_DOC 阶段：`V00→A00→H00`
- 应用场景：上游阶段输出只有被下游正式读取并产出消费证据后，才允许从 READY_WITH_GAPS 升级。
- 目标文件/目录：
  - `sikk_stable_trader_os/09_handoff/handoff_consumption_status.json`
  - `sikk_stable_trader_os/08_acceptance/runtime_acceptance_rules.yaml`
  - `modules/her_runtime_bridge/runtime_acceptance_runner.py`
- 验收：
  - 五级验收完整输出：文件/结构/语义/消费/运行
  - 禁止把 READY_WITH_GAPS 说成 ACCEPTED
- 仍缺数据/证据：
  - downstream_executed=true 的实际证据
  - 每阶段消费失败原因

### AUTO_REPAIR_006_REVIEW_TO_P10_UPGRADE_LOOP — 绑定 P09 复盘回放 → P10 受控升级候选 → shadow validation → approval package
- 优先级：`P1_HIGH`
- HER_DOC 阶段：`U00→G00→A00`
- 应用场景：paper failure attribution 不直接改规则，而是生成升级候选、回滚计划、shadow 验证和人工审批包。
- 目标文件/目录：
  - `sikk_stable_trader_os/02_phase_controllers/P10_self_upgrade/`
  - `sikk_stable_trader_os/00_governance/review_to_upgrade_policy.yaml`
  - `data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl`
- 验收：
  - review result 不得直接 mutate live rules
  - P10 只产出候选/审批/回滚/shadow 证据
- 仍缺数据/证据：
  - 足够 paper closed cases
  - 失败样本 replay 结果
  - shadow validation 通过率

## 二、需要 GPT 深研后再回填的缺口

### AUTO_REPAIR_004_WALLET_STRUCTURE_RUNTIME_EVIDENCE — 修复/接通 P03-P04 钱包结构与筹码结构 runtime evidence
- 优先级：`P0_BLOCKING`
- 需要 GPT 深研：
  - 钱包角色字段全集
  - 同源组/资金路径反证规则
  - 主导侧成本区与派发进度计算模型
  - 筹码库存可信度等级
- 回填位置：
  - `data/gmgn_candidates_live_run/wallet_structure/`
  - `data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/`
  - `modules/wallet_structure/`
  - `sikk_stable_trader_os/00_data/wallet_structure_field_contract.yaml`

### AUTO_REPAIR_006_REVIEW_TO_P10_UPGRADE_LOOP — 绑定 P09 复盘回放 → P10 受控升级候选 → shadow validation → approval package
- 优先级：`P1_HIGH`
- 需要 GPT 深研：
  - 失败归因分类标准
  - shadow validation 样本设计
  - 规则升级收益/风险评估模型
- 回填位置：
  - `sikk_stable_trader_os/02_phase_controllers/P10_self_upgrade/`
  - `sikk_stable_trader_os/00_governance/review_to_upgrade_policy.yaml`
  - `data/gmgn_candidates_live_run/paper_live/failure_attribution.jsonl`

## 三、P0 阻断项先后顺序

1. `AUTO_REPAIR_001_RUNTIME_RUNNER_REGISTRY` — 建立 R00/07_runners 运行器注册与 P01-P10 phase_runner_binding
2. `AUTO_REPAIR_002_GOAL_CONTEXT_LOADING` — 补 runtime goal context loading 与 goal consumption report
3. `AUTO_REPAIR_003_PHASE_OUTPUT_INDEX_TRACE` — 补 phase_output_index 与 runner_execution_trace 自动写入
4. `AUTO_REPAIR_004_WALLET_STRUCTURE_RUNTIME_EVIDENCE` — 修复/接通 P03-P04 钱包结构与筹码结构 runtime evidence
5. `AUTO_REPAIR_005_HANDOFF_CONSUMPTION_ACCEPTANCE` — 补 P01-P10 handoff consumption status 与消费级/运行级 acceptance runner

## 四、为什么 R00 现在还不能跑真实 token

R00/真实 token batch 不能被称为专业化完成，原因不是系统没有方向，而是缺少运行级证据链：

- R00/07_runners 未完整建立
- runtime goal context loading 未完整接入
- phase_output_index / runner_execution_trace 未自动化
- P01-P10 handoff consumption 未完整证明
- wallet_structure runtime evidence 缺失/未接通
- 消费级/运行级 acceptance runner 缺失或未落地

因此当前可运行边界仍然是：`paper-only / observe / read-only quote-security`。

## 五、专业轻机构级完成标准还需要什么

- 真实 token/candidate batch 每轮 P01-P10 分阶段输出
- 每阶段 required fields + source + evidence_level + missing_policy
- 钱包结构与筹码结构原始事实、推理证据、反证证据
- 策略门禁与 paper-only 执行风控的可追踪 ticket
- P09/P10 review-upgrade 闭环证据

## 六、下一合法执行顺序

1. 先落地 `AUTO_REPAIR_001_RUNTIME_RUNNER_REGISTRY`：建立 runner registry 与 phase_runner_binding。
2. 再落地 `AUTO_REPAIR_002_GOAL_CONTEXT_LOADING`：runtime 每轮加载最高认知、总目标、阶段目标、禁区 policy。
3. 再落地 `AUTO_REPAIR_003_PHASE_OUTPUT_INDEX_TRACE`：每阶段输出写 phase_output_index 与 runner_execution_trace。
4. 并行修复 `AUTO_REPAIR_004_WALLET_STRUCTURE_RUNTIME_EVIDENCE`：补 P03-P04 钱包/筹码证据。
5. 再落地 `AUTO_REPAIR_005_HANDOFF_CONSUMPTION_ACCEPTANCE`：五级验收与 handoff consumption。
6. 最后接 `AUTO_REPAIR_006_REVIEW_TO_P10_UPGRADE_LOOP`：P09→P10 受控升级，禁止复盘直接改 live rules。

## 七、安全边界

- paper_only: `True`
- no_real_swap: `True`
- no_private_key: `True`
- no_signing: `True`
- no_broadcast: `True`
- ready_with_gaps_not_accepted: `True`

## 八、当前状态

- status: `READY_WITH_GAPS_AUTO_REPAIR_PACKAGE_READY`
- overall_status: `NOT_COMPLETE_READY_WITH_GAPS`
- judgement: 现在不能称为专业化完成，只能称为已具备系统骨架与 paper runtime，正在进入 R00 收编和数据完整性补全阶段。
