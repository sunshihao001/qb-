# System Constitution

## 用途
定义 AI 调节设计系统 V1.0 的最高规则。System First，Model Second。

## 适用范围
适用于 HER / Hermes 的目标理解、任务拆解、执行、验证、恢复、记忆写入和复盘。

## 核心原则
1. 模型不是可靠同事，而是不稳定执行部件。
2. Prompt 不是人格设定，而是控制面的一部分。
3. 每个任务必须进入受控执行循环。
4. 工具调用必须有权限边界。
5. 上下文必须分层治理。
6. 错误路径必须作为主路径设计。
7. 验证必须独立，不能让执行者自己证明自己完成。
8. 所有输出必须可复盘。
9. 只有验证通过的规则，才能写入长期记忆。

## 禁止行为
- 跳过目标护照直接执行。
- 跳过控制面路由直接改代码、建 workflow 或跑数据。
- 跳过验证声称完成。
- 把未验证内容写成长期规则。
- 把业务代码、方法论、运行数据、复盘报告混在一起。
- 对钱包结构 / Wallet-Intel / source_wallet_bot / 结构分析任务另建并行主系统；必须先进入 Wallet-Intel 语义路由并修改既有 canonical 系统。

## Wallet-Intel / 钱包结构强制底层规则
- 命中钱包结构、钱包数据、source_wallet_bot、Wallet-Intel、字段字典、数据护照、旧路径映射、handoff、筹码/同源/结构证据时，必须先执行：

```text
读取 01_control_plane/task_routing_policy.md
→ route_decision = wallet_intel_semantic_integration
→ 生成 task_passport
→ 读取 11_workflows/wallet_intel_semantic_integration.workflow.md
→ 确认 canonical_route
→ 再进行任何代码或数据动作
```

- 钱包结构 canonical route 固定为：

```text
modules/source_wallet_bot
→ sikk_candidate_wallet_structure_pipeline.py
→ sikk_wallet_structure_gate.py
→ sikk_candidate_state_machine.py / sikk_live_run.py
```

- 钱包结构专业化主目录固定为：

```text
/root/sikk-gmgn/
```

- 钱包结构 / 钱包数据采集 / Source Wallet Bot 的唯一新主写数据路径固定为：

```text
/root/sikk-gmgn/data/source_wallet_bot/<mode>/<token_address>/
```

- 该 token 目录只承接钱包数据、钱包事实、结构证据、结构推断、handoff、报告副本和 manifest；不得承接交易状态机、paper runner、dashboard 主输出、私钥/签名/广播/swap、研究笔记、任务票或 Wallet-Intel 协同日志。

- `/root/sikk-wallet-intel/` 只作为 Wallet-Intel 协同 / 总控 / 行为推断工作区，不作为新钱包结构分析主事实目录、主采集目录或 Source Wallet Bot 主写目录。

- `sikk_sol_full_auto_workflow.py` 只能作为 `legacy_compat_one_shot`，不得升级为主入口或第二套钱包结构分析系统。

## 检查标准
- 是否识别任务类型。
- 是否读取控制面。
- 是否拆分阶段。
- 是否定义验证方式。
- 是否有恢复路径。
- 是否生成复盘与记忆沉淀判断。
