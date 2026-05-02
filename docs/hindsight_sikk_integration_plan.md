# Hindsight × Hermes / SIKK 长期记忆接入方案

> 范围：把 Hindsight 作为可选的外部长期记忆层，用于 Hermes/SIKK 的项目事实、策略设计决策、运行复盘和钱包结构经验沉淀。默认只读/只写记忆，不参与真实 swap 执行。

## 1. Hindsight 核心模型

Hindsight 是 agent memory 系统，不是普通 RAG。它提供三类操作：

- `retain`：写入原始内容，由 Hindsight 抽取 facts/entities/relationships；不要预摘要。
- `recall`：按 query 检索事实，适合 Hermes/SIKK 自己继续推理。
- `reflect`：让 Hindsight 基于记忆直接综合回答，适合复盘、模式归纳、长期项目问答。

关键隔离单元是 `Memory Bank`：

- bank 之间完全隔离。
- 推荐为 SIKK 建独立 bank，避免和个人闲聊/其他项目混杂。
- 多主题用 tags 区分，而不是 metadata 过滤。

## 2. 推荐 bank 设计

### 2.1 Hermes/SIKK 主 bank

建议：

```text
bank_id = sikk-gmgn-main
```

用途：保存 SIKK-GMGN / SIKK-SOL 长期项目知识。

推荐 retain_mission：

```text
Always extract durable SIKK-GMGN/SIKK-SOL technical decisions, pipeline architecture, wallet-structure methodology, paper-trading validation results, runtime issues, API/tooling constraints, and user preferences about output format. Ignore greetings, transient command progress, raw logs without decisions, and one-off temporary task state.
```

推荐 observations_mission：

```text
Identify stable SIKK methodology patterns, recurring runtime failures, wallet-structure evidence patterns, decision-rule changes, and contradictions with prior assumptions. Focus on durable rules and verified outcomes; ignore ephemeral candidate-token noise unless it changes strategy design.
```

推荐 reflect_mission：

```text
You are a skeptical senior SIKK trading-system architect. Ground answers in retained project decisions, verified test results, and explicit safety boundaries. Prefer paper/readiness framing, avoid deterministic trade advice, and highlight uncertainty when evidence is incomplete.
```

Disposition：

```json
{
  "skepticism": 4,
  "literalism": 4,
  "empathy": 2
}
```

### 2.2 可选分 bank

如后续数据量大，可拆：

- `sikk-runtime-runs`：运行日志、每日复盘、失败归因。
- `sikk-wallet-structure`：钱包结构模式、角色分类、same-source/分发/回流经验。
- `sikk-dev-memory`：代码架构、测试、工具链、部署问题。

第一阶段建议只建 `sikk-gmgn-main`，用 tags 区分主题，避免过早复杂化。

## 3. 推荐 tags 体系

每次 retain 至少带：

```text
project:sikk-gmgn
scope:project
```

按内容追加：

```text
topic:wallet-structure
topic:paper-trading
topic:runtime
topic:quote-security
topic:state-machine
topic:gmgn-filter
topic:okx
topic:hermes
type:decision
type:run-report
type:failure-attribution
type:methodology
type:code-change
```

示例：

- 代码设计决策：`project:sikk-gmgn, topic:state-machine, type:decision`
- 运行报告：`project:sikk-gmgn, topic:runtime, type:run-report`
- 钱包结构复盘：`project:sikk-gmgn, topic:wallet-structure, type:failure-attribution`

## 4. 什么应该写入 Hindsight

### 应该 retain

- SIKK 方法论变更：例如 observe/soft/hard wallet gate 的默认策略。
- 稳定架构决策：例如 paper/readiness 边界、真实 swap 禁止默认开启。
- 关键测试结论：例如 `112 passed`，某类 bug 已覆盖回归测试。
- 运行复盘：每日 paper live 表现、失败归因、钱包结构胜率统计。
- 可复用故障经验：OKX/GMGN 某命令限制、字段映射坑、数据源异常模式。
- 用户长期偏好：中文优先、避免“庄家”标签等。

### 不应该 retain

- 单次命令的普通 stdout。
- 临时代币噪声：没有进入策略规则的普通候选币。
- API key、bot token、私钥、webhook_url。
- 未确认的猜测。
- 可以从文件直接读取的完整大 JSON/CSV 原文。

## 5. Hermes 接入方式建议

### 第一阶段：外部 sidecar，不改 Hermes 核心

先启动 Hindsight API，写一个本地桥接脚本：

```text
scripts/hindsight_retain_sikk.py
scripts/hindsight_recall_sikk.py
scripts/hindsight_reflect_sikk.py
```

Hermes 通过 terminal 调这些脚本。优点：

- 不改 Hermes 内置 memory provider。
- 不影响当前 Telegram gateway。
- 可随时停用。
- 适合先验证 Hindsight 对 SIKK 的价值。

### 第二阶段：SIKK Runtime 自动 retain

在 `sikk_live_run.py` 或 cron 结束后，把以下摘要 retain：

```text
live_run_manifest.json
live_board.md
wallet_structure_daily_report_YYYYMMDD.md
paper_daily_report_YYYYMMDD.md
关键 failure_attribution 摘要
```

只写摘要和结构化结论，不写全量行情数据。

### 第三阶段：Hermes 入口 recall

在回答 SIKK 相关复杂问题前，Hermes 可执行：

```bash
python3 scripts/hindsight_recall_sikk.py "wallet structure observe mode default decision"
```

然后结合项目文件和当前运行结果回答。

## 6. 本地部署建议

### Docker 快速启动

需要 LLM API key，例如 OpenAI/Groq 等。不要把真实 key 写入 repo。

```bash
export HINDSIGHT_API_LLM_PROVIDER=groq
export HINDSIGHT_API_LLM_API_KEY="填在本地环境，不贴到聊天"

docker run --rm -it --pull always \
  -p 8888:8888 \
  -p 9999:9999 \
  -e HINDSIGHT_API_LLM_PROVIDER="$HINDSIGHT_API_LLM_PROVIDER" \
  -e HINDSIGHT_API_LLM_API_KEY="$HINDSIGHT_API_LLM_API_KEY" \
  -v "$HOME/.hindsight-docker:/home/hindsight/.pg0" \
  ghcr.io/vectorize-io/hindsight:latest
```

访问：

- API：`http://localhost:8888`
- Control Plane：`http://localhost:9999`

### pip 本机启动

```bash
pip install hindsight-api
export HINDSIGHT_API_LLM_PROVIDER=groq
export HINDSIGHT_API_LLM_API_KEY="填在本地环境，不贴到聊天"
hindsight-api --host 127.0.0.1 --port 8888
```

客户端：

```bash
pip install hindsight-client
```

## 7. SIKK retain 格式

推荐 retain JSON conversation/document array，不预摘要。对于运行报告，可以保留 Markdown 摘要：

```python
client.retain(
    bank_id="sikk-gmgn-main",
    content=report_markdown,
    context="SIKK live run report: candidate discovery, wallet structure, quote/security and paper/readiness summary",
    document_id="sikk-live-run-2026-05-02T125807Z",
    metadata={"source": "sikk_live_run", "output_root": "data/gmgn_candidates_live_run"},
    tags=["project:sikk-gmgn", "topic:runtime", "type:run-report"],
    retain_async=False,
)
```

注意：Hindsight 文档里强调 `document_id` 要稳定。对于同一份每日报告可以用同一个 document_id 覆盖更新；对于每轮运行保留历史，则用 run_id。

## 8. SIKK recall / reflect 使用策略

### recall：供 Hermes 自己推理

适合：

- “上次 wallet gate 为什么默认 observe？”
- “以前 OKX token-scan 有什么坑？”
- “最近 paper 失败主要归因是什么？”

推荐：

```text
budget=mid
tags=[project:sikk-gmgn]
tags_match=any_strict
include_chunks=true  # 需要引用原文时开启
```

### reflect：让 Hindsight 直接综合

适合：

- “总结过去 7 天 SIKK paper live 暴露的问题。”
- “钱包结构门禁是否应该从 observe 升到 soft？”
- “根据历史失败归因，下一步优先优化什么？”

推荐带 schema，让输出稳定。

## 9. 安全边界

- Hindsight 只做长期记忆、检索、复盘，不授权真实交易。
- 不 retain 私钥、API key、bot token、webhook_url。
- 不把 Hindsight reflect 结果作为买入/卖出指令。
- 对于交易相关结论，必须继续经过 SIKK 状态机、quote/security、paper validation、人类确认层。
- Hindsight 的记忆可能过期，回答时要结合当前文件/运行结果验证。

## 10. 第一阶段落地任务

1. 安装/确认 `hindsight-client`。
2. 创建 `/root/sikk-gmgn/docs/hindsight_sikk_integration_plan.md`。
3. 创建脚本草案：
   - `scripts/hindsight_retain_sikk.py`
   - `scripts/hindsight_recall_sikk.py`
4. 脚本默认读取：
   - `HINDSIGHT_BASE_URL=http://localhost:8888`
   - `HINDSIGHT_BANK_ID=sikk-gmgn-main`
5. 若 Hindsight API 未启动，脚本应友好报错，不影响 SIKK 主流程。
6. 先手动 retain 一份 pipeline report，验证 recall 可用后，再考虑接入 live_run。
