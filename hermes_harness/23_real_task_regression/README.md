# 23_real_task_regression — V2.1 Real Task Fixture Regression

## 定位

V2.1 将 V2.0 benchmark skeleton 升级为可回放真实任务夹具回归。

## 主要结构

- `task_fixtures/`：真实任务风格样本。
- `expected_outcomes/`：预期输出/决策。
- `error_taxonomy/`：判断错误分类。
- `regression_runs/`：每次回放运行产物。
- `memory_lifecycle_reviews/`：记忆生命周期审查。
- `meta_verification/`：元验证报告。

## 运行命令

```bash
cd /root/sikk-gmgn/hermes_harness && python3 09_scripts/hermes_v21_real_task_regression_run.py --fixture-set core --json
```

## 边界

`fixture regression passed` 只能证明夹具回放通过；不能证明线上真实任务长期可靠性。
