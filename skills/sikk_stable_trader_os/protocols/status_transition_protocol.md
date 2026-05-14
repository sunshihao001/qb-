# Status Transition Protocol

## Global principles

- 上游 hard negative 不能被下游正向分覆盖。
- `READY_WITH_GAPS` 不等于 `READY`。
- `PAPER_READY` 不等于实盘授权。
- 缺失字段必须降级或阻断，不能伪装为 0。

## Terminal safety states

- `BLOCK_REAL_TRADE`
- `OBSERVE_ONLY`
- `PAPER_ONLY`
- `REQUIRES_MANUAL_CONFIRMATION`
