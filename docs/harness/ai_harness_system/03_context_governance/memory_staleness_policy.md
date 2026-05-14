# Memory Staleness Policy

## 用途
为 Hermes 本地记忆建立过期审查机制，防止长期记忆污染。

## 记忆状态
- candidate：候选，未验证。
- verified：已验证，可调用。
- stale：可能过期，需要复查。
- superseded：已被新规则替代。
- rejected：拒绝写入。
- archived：归档，不参与默认调用。

## 记忆元数据

```json
{
  "status": "verified",
  "validity": "stable",
  "last_verified_at": "2026-05-06T18:30:00Z",
  "stale_check_required": true,
  "stale_reason": null,
  "superseded_by": null
}
```

## 规则
1. verified memory 必须有来源和验证状态。
2. stale_check_required=true 的记忆必须周期性复查。
3. superseded memory 不得再作为默认规则调用。
4. rejected memory 不得写入长期记忆。
5. archived memory 只能作为历史参考。
