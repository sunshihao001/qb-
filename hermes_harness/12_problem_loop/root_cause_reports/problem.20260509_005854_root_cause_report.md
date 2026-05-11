# Root Cause Report

- created_at: 2026-05-09T00:58:54Z
- problem_id: problem.20260509_005854
- loop_id: apur.loop.20260509_005854

## 表面症状

Hermes 任务经常生成文档后停止。

## 直接原因

缺少强制 dry-run、验证裁决和状态推进产物。

## 系统根因

认知规则已经定义，但没有完全外部化为可运行的 APUR 产物链和验证入口。

## 过程根因

任务完成标准偏向“生成文件”，不足以证明“问题被解决”。

## 验证根因

缺少针对 APUR 完整链路的最终 verification report。

## 恢复根因

失败路径需要生成 failure_attribution/recovery，而不是直接停止。

## 证据链

- 12_problem_loop 与 13_problem_loop_templates 原先缺失。
- 本轮 dry-run 生成 problem_passport → learning_writeback → loop_state。

## 反证

已有 V1.3 manifesto 和 workflow，说明概念层存在，不是完全空白。

## 置信度

high

## 必须修复项

新增 APUR 目录、模板、脚本、dry-run、verification report。

## 可延后项

接入 Hermes 主 router、质量评分、失败样本 lessons learned 自动化。
