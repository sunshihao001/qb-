# Hermes Harness V1.7 Reliability Calibration Layer

## 定位

V1.7 不是继续增加“治理检查项”，而是把 V1.6 的判断治理结果转成可度量、可回放、可校准的可靠性反馈系统。

核心升级：

```text
从：治理 Hermes 是否应该继续、停止、降级或交给人
到：记录 Hermes 上一轮预期与真实观察之间的偏差，并把偏差变成下一轮判断修正
```

## 核心判断

Hermes 的可靠性不能靠“本轮看起来更严谨”来声明；必须靠跨轮校准：

```text
expected outcome
→ observed outcome
→ calibration delta
→ judgment error rate
→ benchmark update
→ rule adjustment candidate
→ memory candidate review
→ revalidation window
→ next-run bias correction
```

## 新路由

`hermes_reliability_calibration_layer`

## 新目录

`16_reliability_calibration/`

## 插入点

V1.7 在 V1.4 runtime hook 中作为 `reliability_calibration_hook`，位于 V1.6 `judgment_governance_hook` 之后、completion audit 之前：

```text
router
→ problem_passport
→ judgment_governance_hook
→ APUR execution or abstention/handoff
→ verification
→ meta verification
→ reliability_calibration_hook
→ recovery/writeback/completion audit
```

## 必须回答的问题

1. 本轮原本期待什么结果？
2. 实际观察到什么结果？
3. 期待与观察之间的偏差是什么？
4. 偏差属于判断错误、执行错误、验证错误、记忆错误还是边界错误？
5. judgment error rate 是否上升/下降/未知？
6. 是否生成 benchmark case，供下一轮回放？
7. 是否需要 rule adjustment，而不是直接写长期记忆？
8. 记忆候选是否仍处于未验证队列？
9. 需要多久/什么条件后重新验证？
10. 下一轮应施加什么 bias correction？

## 完成定义

V1.7 完成必须同时满足：

- `reliability_calibration_state.json` 存在且 schema 合法；
- expected outcome 与 observed outcome 已分离记录；
- calibration delta 已计算并分类；
- judgment error rate 有明确 `trend`；
- benchmark update 已写入；
- rule adjustment candidate 已写入但不直接当成稳定规则；
- memory candidate review 默认 `verified_memory_allowed=false`；
- revalidation window 明确触发条件；
- next-run bias correction 明确；
- 独立测试通过。
