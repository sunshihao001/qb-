# Phase07 Handoff Rules

Phase07 输出 `phase_07_handoff_packet.json` 给 Phase08。

必须包含：phase、token_address、snapshot_id、phase_status、allow_next_stage、next_stage、required_files_for_next_stage、positive_evidence、negative_evidence、hard_negative_triggered、block_reason、missing_fields、audit_file。

若执行风险阻断，仍允许 Phase08 复盘读取，但不得允许执行。
