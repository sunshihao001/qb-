# O00 CLI Recovery Policy

Failure types: missing_registry, missing_config, invalid_registry, invalid_config, missing_sample, sample_expected_output_missing, safe_mode_missing, forbidden_action_detected, pipeline_run_creation_failed, stage_dispatch_failed, trace_write_failed, final_report_missing.

Recovery decisions: FIX_INPUT_PATH, RECREATE_REGISTRY, RECREATE_CONFIG, RUN_VALIDATE_CONFIG, RUN_INIT, ROUTE_TO_U00, BLOCK_COMMAND, RETRY_COMMAND.
