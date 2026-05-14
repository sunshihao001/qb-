# P01 Acceptance Criteria

## P01_READY
all required candidate master, source event, identity, dedup, gap, P02 request, handoff outputs exist; no blocking or critical gaps; all candidates have trace; downstream route is P02 only.

## P01_READY_WITH_GAPS
identity usable but non-blocking HIGH/MEDIUM/LOW gaps exist; P02 request carries gaps; limitations include CANDIDATE_ONLY, NO_EVIDENCE, NO_SCENARIO, NO_STRATEGY_GATE, LIVE_EXECUTION_FORBIDDEN.

## P01_REJECTED
token_address missing/invalid, source_type missing, candidate_id failure, unresolved identity conflict.

## P01_BLOCKED
unsupported chain, live execution request, bypass P02, bypass handoff/acceptance/trace, forbidden output detected.
