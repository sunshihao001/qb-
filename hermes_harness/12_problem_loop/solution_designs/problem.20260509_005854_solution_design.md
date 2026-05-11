# Solution Design

- created_at: 2026-05-09T00:58:54Z
- problem_id: problem.20260509_005854
- loop_id: apur.loop.20260509_005854

## 方案目标

把 APUR 从认知设计补齐为可审计、可 dry-run、可验证的 Hermes Harness 子系统。

## 修改范围

仅 `/root/sikk-gmgn/hermes_harness/`。

## 新增文件

- 控制面策略
- 12_problem_loop 运行产物目录
- 13_problem_loop_templates 模板
- 09_scripts APUR 脚本
- verification checklist/report
- final report

## 更新文件

必要时更新 README/索引。

## 新增脚本

hermes_problem_loop_run.py 以及各阶段 wrapper。

## 执行步骤

创建目录 → 写模板 → 写脚本 → dry-run → 验证 → 写报告 → 记忆队列。

## 验证步骤

检查产物存在、脚本 --help/--dry-run、JSON 可解析、memory queue 写入、无业务代码修改。

## 风险边界

不读密钥、不交易、不删除、不 git push、不接入 Telegram/Hindsight。

## 回滚方式

删除本轮新增 APUR 文件或按 git diff 回退；不影响业务代码。
