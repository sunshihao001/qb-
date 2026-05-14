# Bot2 Handoff Contract

## Purpose
`bot2_handoff_packet.json` is the evidence packet from Source & Wallet Intelligence Bot to Intel Bot / Bot2.

## Required sections
- `packet_id`
- `token_address`
- `created_at`
- `source_manifest_refs`
- `wallet_trade_refs`
- `wallet_profile_refs`
- `funding_flow_refs`
- `token_source_refs`
- `same_source_evidence_refs`
- `backflow_path_refs`
- `wallet_intelligence_decision_refs`
- `missing_fields_summary`
- `requires_followup_fields`
- `evidence_language_only`
- `forbidden_decision_fields`

## Forbidden fields
- PAPER_READY
- BLOCKED
- final_trade_gate
- dominant_side_control
- second_rally_motive
- buyability
- real_execution_action

## Rule
Bot1 hands off evidence; Bot2 may consume evidence but must not treat legacy L3/L4 artifacts as live facts.
