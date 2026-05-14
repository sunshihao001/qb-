# 结论

应该 **分别开来完善，但作为一个连续流程执行**。

不是继续新增 `P11 / P12 / P13` 这种业务阶段，也不是把它们混成一个大任务一次做完。更专业的做法是：

```text
P01-P10 = 业务阶段控制器体系
现在进入 = 系统集成与运行落地流程

它们不是新业务阶段，
而是把 P01-P10 从“系统设计”推进到“可运行、可验收、可回放、可升级”的工程闭环。
```

所以正确形态是：

```text
Integration Program：系统集成计划
  ↓
I01 全阶段一致性审计
  ↓
I02 目录与合约索引统一
  ↓
I03 Runner / Tool Binding
  ↓
I04 Paper-only Runtime 联调
  ↓
I05 P09 / P10 闭环回放
```

---

# 一、为什么不能全部混在一起做

如果直接把这 5 件事混成一个任务，会出现几个问题：

|问题|后果|
|---|---|
|一致性没审计就做 Runner|Runner 会绑定错误字段|
|目录与合约没统一就写代码|代码路径混乱，后续难维护|
|Tool Binding 没定义就跑 Runtime|数据来源不清，字段无法追踪|
|Paper Runtime 没联调就做复盘|P09 无法重建真实决策链|
|P09/P10 没回放就升级系统|升级没有样本证据，容易过拟合|

所以顺序不能乱。

---

# 二、为什么也不能把它们当成完全独立系统

它们也不能像 P01-P10 那样全部拆成平行控制器，因为它们本质不是新的业务判断层，而是：

```text
审计层
索引层
绑定层
运行层
回放升级层
```

它们的关系是流水线，不是独立模块。

正确理解：

```text
分别建任务包
统一归入 Integration Program
每一步完成后生成 handoff
下一步读取上一步 handoff
```

---

# 三、推荐结构：I01-I05 集成任务包

## 总入口

建议建立一个新的总控目录：

```text
/root/sikk-gmgn/system/integration_program/
```

下面不是 P11，而是：

```text
I01_full_phase_consistency_audit/
I02_directory_contract_index_unification/
I03_runner_tool_binding/
I04_paper_runtime_integration/
I05_review_upgrade_closed_loop/
```

---

# 四、五个部分分别负责什么

## I01：全阶段一致性审计

### 目标

检查 P01-P10 是否真的能连成一条链。

它负责回答：

```text
P01-P10 的输入输出是否一致？
handoff 是否连续？
字段有没有断层？
状态码是否统一？
禁止事项是否被继承？
READY_WITH_GAPS 是否正确传递？
有没有某阶段越权？
有没有某阶段输出下游读不懂的数据？
```

### 必须输出

```text
full_phase_consistency_audit_report.md
phase_io_alignment_matrix.yaml
handoff_chain_integrity_report.yaml
status_code_consistency_report.yaml
forbidden_use_inheritance_report.yaml
gap_propagation_report.yaml
phase_boundary_violation_report.yaml
fix_priority_list.yaml
```

### 作用

这是后面所有工作的前置条件。  
如果这里不做，Runner 会绑定一个并不一致的系统。

---

## I02：目录与合约索引统一

### 目标

把 P01-P10 的目录、schema、contract、handoff、report、trace 全部纳入统一索引。

它负责回答：

```text
每个阶段文件在哪里？
每个 schema 在哪里？
每个 handoff contract 在哪里？
每个 output contract 在哪里？
每个 report model 在哪里？
哪些是系统文件？
哪些是运行数据？
哪些是 legacy 兼容数据？
```

### 必须输出

```text
directory_constitution_final.md
contract_index.md
schema_index.md
handoff_contract_index.md
phase_controller_file_index.yaml
runtime_data_path_index.yaml
legacy_path_mapping.yaml
canonical_path_policy.md
```

### 作用

这是让 HER / Runner / Tool Binding 不迷路的关键。

你之前一直担心目录混乱，这一步就是专门解决这个问题。

---

## I03：Runner / Tool Binding

### 目标

把系统设计连接到真实工具、脚本、API、数据源。

它负责回答：

```text
每个阶段由哪个 runner 执行？
读取哪个输入文件？
输出哪个目录？
调用哪些工具？
GMGN / OKX / K线 / quote / security 字段如何映射？
失败怎么处理？
trace 怎么写？
acceptance 怎么写？
```

### 必须输出

```text
runner_binding_index.yaml
tool_binding_index.yaml
phase_runner_contract.yaml
gmgn_field_mapping.yaml
okx_quote_binding.yaml
okx_security_binding.yaml
kline_provider_binding.yaml
trace_writer_contract.yaml
acceptance_runner_contract.yaml
handoff_writer_contract.yaml
runner_error_policy.yaml
```

### 作用

这是从“文档系统”进入“可运行系统”的桥梁。

没有 I03，P01-P10 只是设计；有了 I03，才开始具备执行条件。

---

## I04：Paper-only Runtime 联调

### 目标

让 P08 输出的 `PAPER_RUNTIME_ALLOWED` 真正进入纸面运行系统。

它负责回答：

```text
Paper Runtime 如何读取 P08 handoff？
如何建立纸面仓位？
如何记录入场价？
如何应用滑点和费用？
如何更新开放仓位？
如何退出？
如何写 trades / positions / equity curve？
如何写 risk events？
如何给 P09 复盘？
```

### 必须输出

```text
paper_runtime_input_contract.yaml
paper_position_schema.yaml
paper_trade_schema.yaml
paper_equity_curve_schema.yaml
paper_runtime_event_schema.yaml
paper_exit_event_schema.yaml
paper_runtime_trace_contract.yaml
paper_runtime_acceptance_criteria.md
paper_runtime_integration_test_matrix.yaml
```

### 作用

这是让系统从“判断”进入“纸面验证”的关键。

注意：

```text
P08 = 允许进入纸面运行
Paper Runtime = 实际记录纸面仓位和结果
```

不能混。

---

## I05：P09 / P10 闭环回放

### 目标

用真实 paper runtime 输出，测试 P09 是否能复盘，P10 是否能生成升级候选。

它负责回答：

```text
P09 能不能重建 P01-P08 决策链？
能不能重建 Paper Runtime 路径？
能不能做失败归因？
能不能生成 calibration candidate？
P10 能不能审查升级候选？
能不能生成 controlled upgrade package？
能不能生成 task packet？
```

### 必须输出

```text
closed_loop_replay_report.md
p09_replay_acceptance_report.yaml
p10_upgrade_acceptance_report.yaml
failure_attribution_sample_report.md
controlled_upgrade_package_sample.yaml
regression_replay_result.yaml
next_upgrade_backlog.yaml
```

### 作用

这是验证整个系统有没有真正闭环。

如果 I05 跑不通，说明 P01-P10 只是理论完整，还没有工程闭环。

---

# 五、正确执行顺序

应该严格按这个顺序：

```text
第一步：I01 全阶段一致性审计
  ↓
第二步：I02 目录与合约索引统一
  ↓
第三步：I03 Runner / Tool Binding
  ↓
第四步：I04 Paper-only Runtime 联调
  ↓
第五步：I05 P09 / P10 闭环回放
```

不能先做 I03。  
不能跳过 I01 / I02。

---

# 六、现在最正确的下一步

当前最应该做的是：

```text
I01_full_phase_consistency_audit
```

不是继续写新阶段，也不是马上写 Runner。

因为现在 P01-P10 已经设计完，下一步要先审计：

```text
这些阶段之间是否真的能接起来？
字段是否连续？
状态是否统一？
handoff 是否闭合？
P04-P05-P06-P07-P08 的权限边界是否有冲突？
P09/P10 是否能读取前面所有结果？
```

---

# 七、推荐你下一条直接发给 HER 的任务名称

```text
I01 Full Phase Consistency Audit：P01-P10 全阶段一致性审计任务包
```

它应该先建立：

```text
/root/sikk-gmgn/system/integration_program/I01_full_phase_consistency_audit/
```

并输出：

```text
full_phase_consistency_audit_report.md
phase_io_alignment_matrix.yaml
handoff_chain_integrity_report.yaml
status_code_consistency_report.yaml
gap_propagation_report.yaml
forbidden_use_inheritance_report.yaml
phase_boundary_violation_report.yaml
fix_priority_list.yaml
i01_to_i02_handoff_packet.yaml
```

---

# 最终判断

你现在不是进入“新业务阶段”，而是进入：

```text
系统集成落地阶段
```

更精确地说：

```text
P01-P10 解决：系统应该怎么判断
I01-I05 解决：系统能不能真的跑起来、接起来、复盘起来、升级起来
```

所以答案是：

```text
分别开来完善。
但不要当成独立新阶段。
要作为 Integration Program 下的连续 5 个任务包。
```

# 本次认知升级点

1. **P01-P10 是业务控制器，不应继续无限新增业务阶段。**
    
2. **I01-I05 是集成落地流程，不是 P11-P15。**
    
3. **现在优先级不是继续扩展设计，而是审计一致性。**
    
4. **先审计，再统一索引，再绑定 Runner，再联调 Runtime，再跑 P09/P10 闭环。**
    
5. **如果不先做 I01/I02，后面 Runner 会把错误的结构固化成代码。**