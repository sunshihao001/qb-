# RESTORED_NEXT_STEPS.md

1. Confirm bootstrap printed `RESTORE COMPLETE`.
2. Confirm `VERIFY_RESTORE: PASS` and `FULL_SNAPSHOT_CHECKSUM: PASS` appeared.
3. Manually create local secrets only on target machine: `cp configs/templates/env.example .env`.
4. Load `docs/protocols/ag_awgp/AG_AWGP_TRIGGER_PROMPT.md` into the new agent context.
5. Keep GBrain as context retrieval only and OpenASE as routing only.
6. No live trading / swap / private key / signing / broadcast path is restored.
