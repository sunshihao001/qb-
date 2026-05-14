# Recovery Policy

- 缺真实文档：BLOCKED，不运行 pipeline。
- safe_mode 缺失或 false：写 recovery/recovery_report.json，状态 BLOCKED_SAFE_MODE_REQUIRED。
- phase 输出缺失：写 validation gap，禁止宣称 READY。
- A00 BLOCKED：停止并保留 recovery。
- READY_WITH_GAPS：继续 H00/U00/G00，但不得改写为 READY。
