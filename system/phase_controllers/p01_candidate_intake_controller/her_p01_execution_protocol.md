# HER P01 Execution Protocol v3.0

1. Read professional_build_order.md
2. Read phase_controller_index.yaml
3. Read Handoff Plane output handoff_packet
4. Read Acceptance Plane output acceptance_result_packet
5. Read Trace Plane output trace_handoff_packet
6. Read P01 controller context
7. Validate P01 input contract
8. Receive candidate raw input
9. Save raw_candidate_input or source reference
10. Create candidate_source_event
11. Normalize token identity
12. Validate chain and token_address
13. Generate candidate_id
14. Execute dedup resolution
15. Build candidate_master_record
16. Build discovery_context
17. Build intake_time_context
18. Score source_quality
19. Score intake_quality
20. Execute hard negative rules
21. Build p01_gap_report
22. Generate p02_data_request_packet
23. Write P01 trace
24. Generate candidate_registry
25. Generate candidate_intake_report
26. Generate p01_to_p02_handoff_packet
27. Execute P01 acceptance
28. Handoff only to P02

Forbidden: no Handoff, no Acceptance, no Trace, no token_address, no source_context, no evidence, no scenario, no strategy gate, no paper ready, no runtime, no live execution.
