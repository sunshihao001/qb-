# Global Status Code Table

- `PHASE_READY`: gate passed, handoff valid.
- `PHASE_WITH_GAPS`: non-critical degraded gaps recorded, downstream may continue only when policy allows.
- `PHASE_PAUSED`: recoverable input/tool gap.
- `PHASE_REJECTED`: critical missing field, hard negative, or unsafe authorization.
- `PHASE_ERROR`: parser/tool/runtime error.
- `TOTAL_CONTROL_READY`: all total-control documents, indexes, audits, validation evidence pass.
- `PASS_WITH_ACCEPTED_GAPS`: accepted design gap exists but does not block paper-only control.

Inheritance: rejected/unsafe states block downstream; degraded gaps propagate as inherited review items; ready states require schema-valid handoff.
