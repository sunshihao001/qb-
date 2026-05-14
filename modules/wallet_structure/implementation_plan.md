# wallet_structure implementation plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 将旧 `sikk_gmgn_token_report.py` 拆成 SIKK 钱包结构采集分析小模块，并输出主系统可读 `wallet_structure_decision.json`。

**Architecture:** 先保持 CSV/JSON/Markdown 文件契约，不引入数据库，不改交易执行。旧脚本作为 legacy 对照，新模块逐步拆出 source_reader、normalizer、classifier、edge_builder、decision_builder。

**Tech Stack:** Python 3 stdlib, csv/json/pathlib/subprocess, gmgn-cli, existing project output root.

---

## Phase A：文档与字段契约完成

### Task A1: 验证设计包文件

**Files:**
- Read: `modules/wallet_structure/*.md`
- Read: `modules/wallet_structure/*.csv`
- Read: `modules/wallet_structure/*.json`

**Command:**

```bash
cd /root/sikk-gmgn
find modules/wallet_structure -type f | sort
python3 -m json.tool modules/wallet_structure/input_schema.json >/tmp/input_schema.ok
python3 -m json.tool modules/wallet_structure/output_schema.json >/tmp/output_schema.ok
```

**Expected:** 所有文件存在，JSON 可解析。

### Task A2: 将字段字典作为实现源

**Files:**
- Read: `modules/wallet_structure/field_dictionary.csv`

**Objective:** 后续代码字段只从字典扩展，不在代码里随意新增不可追踪字段。

---

## Phase B：旧脚本拆分成模块

### Task B1: 创建 Python package 骨架

**Files:**
- Create: `modules/wallet_structure/__init__.py`
- Create: `modules/wallet_structure/source_reader.py`
- Create: `modules/wallet_structure/normalizer.py`
- Create: `modules/wallet_structure/role_classifier.py`
- Create: `modules/wallet_structure/edge_builder.py`
- Create: `modules/wallet_structure/decision_builder.py`
- Create: `modules/wallet_structure/run.py`

**Verification:** `python3 -m modules.wallet_structure.run --help` 返回帮助。

### Task B2: 迁移 GMGN 命令到 source_reader

**Objective:** 从旧脚本迁移 `gmgn-cli` 调用，不改变命令语义。

**Verification:** 给定 token 后能输出 raw JSON/CSV snapshot。

### Task B3: 迁移字段标准化到 normalizer

**Objective:** 将 `get_any()`、`fl()`、时间格式、标签合并等标准化逻辑集中。

**Verification:** 输出 `wallet_normalized.csv`，表头匹配 `field_dictionary.csv` 核心字段。

---

## Phase C：输出 wallet_structure_decision.json

### Task C1: 实现 role_classifier

**Objective:** 使用 `role_rule_matrix.csv` 的规则思想替代旧 `classify(w)` 硬编码散落。

**Verification:** 旧脚本能识别的角色，新模块均能输出相同或更保守角色。

### Task C2: 实现 decision_builder

**Objective:** 输出满足 `output_schema.json` 的 `wallet_structure_decision.json`。

**Verification:**

```bash
python3 -m json.tool data/gmgn_candidates_live_run/intel-bot/logs/wallet_structure/<token>/wallet_structure_decision.json
```

### Task C3: 阻断规则保护

**Objective:** 禁止单个新钱包、单个 transfer_in、单个 bundler 标签直接 block。

**Verification:** 单标签样例输出 `WALLET_PAUSE` 或 `WALLET_UNKNOWN`，不输出 `WALLET_BLOCK`。

---

## Phase D：接入主状态机

### Task D1: 主状态机只读接入

**Objective:** 主状态机只读取 `wallet_structure_decision.json`，不读取中间 CSV 作为信号。

**Important:** 本模块不直接写 `PAPER_READY`，只给 `recommended_state_action`。

### Task D2: final gate 统一裁决

**Objective:** 只有 final trade gate 才能决定是否进入 paper ready。

---

## Phase E：接入 paper runner

### Task E1: paper runner 只读 `wallet_structure_factor`

**Objective:** paper runner 不接受交易命令，只把结构侧 factor 作为风险/仓位/观察权重参考。

---

## Phase F：多快照复盘与历史库

### Task F1: 历史地址库轻量结构

**Objective:** 用 CSV/JSON 文件记录 address profile、role history、review updates，不引入数据库服务。

### Task F2: 多快照 diff

**Objective:** 对比 T+1h/T+6h/T+24h/T+72h/T+7d，发现清仓、回流、角色升级/降级。

---

## Phase G：解释模块接入

### Task G1: evidence_chain 输出稳定化

**Objective:** 每个 wallet 角色和 token-level decision 都要包含 field/rule/value/source。

### Task G2: report 解释层

**Objective:** `wallet_structure_report.md` 从 evidence_chain 生成，而不是反推事实。
