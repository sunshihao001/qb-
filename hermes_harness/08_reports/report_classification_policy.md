# Report Classification Policy

## 用途
区分过程报告和最终报告，防止所有报告混放。

## 报告分类目录

```text
09_reports/
├── scan_reports/
├── phase_reports/
├── verification_reports/
├── recovery_reports/
├── final_reports/
└── audit_reports/
```

## 每份报告必须说明
- 这是过程报告，还是最终报告？
- 是否经过验证？
- 是否可以作为后续任务输入？
- 是否可写入记忆？

## 规则
1. 过程报告不能冒充最终报告。
2. 未验证报告不能作为 verified memory 来源。
3. final_reports 必须引用 verification_reports。
4. recovery_reports 必须引用失败点和恢复动作。
