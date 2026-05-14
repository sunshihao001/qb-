# V00 Context Pack

V00 是 HER 文档到功能自动化落实系统中的验证证据控制器。

## 上游入口

V00 的唯一合法入口是 F00 handoff packet。K00 handoff 只能作为上游引用，不能绕过 F00 直接启动验证。

## 核心问题

- F00 生成的 function_mapping 是否完整？
- field_model 是否有字段来源、类型、缺失策略、trace 要求？
- rule_logic 是否可执行、可测试、可反证、可失败？
- schema / input contract / output contract / handoff contract 是否合法一致？
- patch 是否真实写入并有 modified_files / diff_summary / rollback_plan？
- test plan 是否已转化为真实 test command、exit_code、stdout/stderr、passed/failed？
- replay plan 是否已转化为 replay input/output/trace/evidence/report？
- trace / audit 是否完整记录关键事件？
- gap / failure 是否如实分类？
- 是否允许进入 R00 runner binding？

## 非目标

V00 不生成主要功能代码，不接入正式 runner，不启动 live runtime，不执行 paper runtime，除非明确 safe-mode replay；不部署、不签名、不删除源文件、不把失败伪装为通过。

## 运行输出目录

`/root/sikk-gmgn/data/her_document_function_system/v00_runs/<run_id>/`

## 状态基线

没有 F00 handoff、没有命令输出、没有 exit_code、没有 stdout/stderr、没有 replay trace、没有 audit trace，均不能宣称验证通过。
