# Automated Trading Workflow Safety Boundary｜自动化交易工作流安全边界

updated_at: `2026-05-11T12:27:50.411792Z`

## 1. 边界原则

自动化交易工作流在当前系统阶段只允许形成 **只读研究 → 结构分析 → 门禁判断 → 风险状态 → 纸面执行意图 → 人工确认票据 → 复盘回写** 的闭环。

它不授权真实交易自动化。任何真实交易、签名、广播、swap、密钥读取都必须由独立权限系统、独立 planbook、独立人工确认和独立审计开启；当前任务执行包默认全部禁止。

## 2. 默认 Permission Manifest

```json
{
  "paper_only": true,
  "read_only_research": true,
  "real_trade_enabled": false,
  "signing_enabled": false,
  "broadcast_enabled": false,
  "auto_swap_enabled": false,
  "secret_access": "not_requested_not_used"
}
```

## 3. 强制停止条件

- 请求或读取私钥、助记词、API secret。
- 构造真实签名交易。
- 广播交易。
- 自动 swap。
- 固定 CA 被 discovery 覆盖。
- token_address 与输入 CA 不一致。
- P05/P06 出现 hard negative 后仍进入正向候选。
- 缺少核心证据却输出确定性买入结论。

## 4. 允许输出

- `OBSERVE_ONLY`
- `RISK_MONITOR`
- `REJECTED`
- `PAPER_CANDIDATE`
- `PAPER_INTENT_REQUIRES_HUMAN_CONFIRMATION`

## 5. 禁止输出

- `BUY_NOW`
- `AUTO_BUY`
- `REAL_TRADE_READY`
- `SIGN_AND_SEND`
- `BROADCAST_READY`
- `EXECUTE_SWAP`

## 6. Gate 规则

每个阶段完成后必须执行：

1. 检查 permission manifest。
2. 检查 output contract。
3. 检查 evidence manifest。
4. 检查 gap register。
5. 检查 handoff packet。
6. 决定 continue/degrade/stop。

只有 `PASS` 或 `PASS_WITH_DEGRADED_GAPS` 且无 blocker 时，HER 才能继续下一阶段。
