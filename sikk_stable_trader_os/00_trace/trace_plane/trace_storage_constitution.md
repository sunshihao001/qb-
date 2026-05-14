# Trace Storage Constitution

Canonical trace data root: `/root/sikk-gmgn/data/trace_plane/`.

Principles:
1. Trace 数据不替代业务数据。
2. Trace 数据不修改 raw。
3. Trace 数据记录引用关系。
4. Trace 数据必须可增量写入。
5. Trace 数据必须支持按 token、phase、run_id、trace_id 回查。
6. Trace 数据必须支持 Review / Replay 复盘。
7. Trace 数据必须向 Acceptance Plane 和 Handoff Plane 提供输入。

Created at: 2026-05-11T17:13:34Z
