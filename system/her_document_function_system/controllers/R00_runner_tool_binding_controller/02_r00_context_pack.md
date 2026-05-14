# R00 Context Pack

R00 is the HER Runner / Tool Binding controller. It consumes only V00-validated function assets and creates safe binding evidence for CLI, HER controller calls, orchestrator steps, tool bindings, Telegram command design, report/dashboard bindings, and safe dry-run jobs.

R00 is not a live runner, paper runtime launcher, wallet executor, deployer, or total acceptance controller. It must not bind unvalidated functions or treat a binding plan as binding evidence.

Core proof chain:

```text
V00 handoff + validation evidence
→ binding target inventory
→ interface scan
→ binding decision
→ command contract
→ binding specs
→ safe dry-run evidence
→ trace/audit
→ acceptance
→ downstream handoff
```
