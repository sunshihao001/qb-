# Problem Passport

- created_at: 2026-05-09T00:58:54Z
- problem_id: problem.20260509_005854
- loop_id: apur.loop.20260509_005854

## 原始问题

Hermes 任务经常只生成文档，没有真正形成闭环。

## 用户真实意图

用户要求 Hermes 不再停留在文档生成，而是形成可执行、可验证、可恢复、可复盘的问题解决闭环。

## 问题类型

- 闭环失败问题
- 验证缺失问题
- 执行断点问题
- 系统设计问题

## 影响范围

Hermes Harness 任务入口、控制面、执行循环、验证恢复、记忆写回。

## 当前证据

- 已存在 V1.3 manifesto/control/workflow/schema/checklist/recovery。
- 本轮新增 APUR 运行产物目录、模板、脚本和 dry-run。

## 缺失证据

- 真实线上任务路由 hook 尚未接入。
- 问题解决质量评分尚未建立。

## 初步风险

如果只生成文档而无 dry-run 和验证报告，会继续产生假完成。

## 是否允许自动执行

允许：仅限 hermes_harness 内 dry-run 写文件；不修改业务代码、不读密钥、不触发交易。

## 下一步：进入自动理解器
