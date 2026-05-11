# Hermes Harness V1.1 First Priority Plan

## Priority 1: prevent Hermes from wandering

Stabilize these first:
1. startup protocol
2. task passport
3. risk/permission tiers
4. active_task_state.json
5. verification report
6. recovery report

## Current V1.1 status
- Canonical root created at `/root/sikk-gmgn/hermes_harness/`
- Legacy V1.0 docs remain at `/root/sikk-gmgn/docs/harness/ai_harness_system/`
- V1.1 control-plane, runtime, templates, scripts, reports, memory, and audit folders are present
- Core bootstrap/verification scripts run successfully

## Verification evidence
- `hermes_task_init.py` generated a standard task id
- `hermes_context_build.py` found control-plane and runtime context files
- `hermes_verify_task.py` passed with no missing runtime files
- `hermes_permission_check.py 'git push origin main'` returned `R5 DENY`
- `hermes_stale_memory_check.py` read V1.1 memory lifecycle files
- `hermes_surface_completion_audit.py` reported no surface completion risk

## Recommendation
Continue with the first-priority stabilization loop only. Do not expand into advanced routing or memory evolution until the six stability files are treated as canonical and verified.
