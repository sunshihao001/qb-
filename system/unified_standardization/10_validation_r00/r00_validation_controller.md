# R00 Validation Controller

- producer: S00_unified_system_standardization
- consumer: R00 / HER Control Plane
- version: 0.1.0
- status: active_with_gaps
- acceptance: validates runner binding, command dry-run, input/output contract, trace, acceptance, handoff and no Phase Controller bypass.

R00 不负责交易判断，只负责系统组件是否正确绑定、运行、输出、交接。
