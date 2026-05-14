# H00 Queue Recovery Policy

## Purpose
H00 recovery handles queue/handoff failures without pretending downstream work executed.

## Recovery Cases

### missing_a00_handoff
- status: H00_BLOCKED
- safe_next_action: request_a00_handoff_packet
- forbidden_next_action: build_downstream_queue

### missing_readiness_certificate
- status: H00_BLOCKED
- safe_next_action: request_readiness_certificate
- forbidden_next_action: generate_queue_items

### target_not_ready
- status: ITEM_BLOCKED
- safe_next_action: REQUEST_TARGET_CAPABILITY or REROUTE_TO_BACKLOG
- forbidden_next_action: dispatch_to_execution

### missing_contract
- status: ITEM_BLOCKED
- safe_next_action: REQUEST_MISSING_CONTRACT
- forbidden_next_action: mark_handoff_ready

### blocking_gap
- status: QUEUE_BLOCKED
- safe_next_action: REROUTE_TO_RECOVERY or REROUTE_TO_U00
- forbidden_next_action: route_blocked_task_to_execution

### handoff_write_failed
- status: H00_BLOCKED
- safe_next_action: RETRY_HANDOFF_WRITE
- forbidden_next_action: claim_handoff_packet_written

### trace_missing
- status: H00_BLOCKED
- safe_next_action: rebuild_trace_audit
- forbidden_next_action: H00_ACCEPTED

## Non-negotiable Guards
- Never drop unresolved_gaps.
- Never drop accepted_risks.
- Never remove forbidden_actions.
- Never convert READY_WITH_GAPS to READY.
- Never treat QUEUE_CREATED / ITEM_QUEUED as ITEM_COMPLETED.
