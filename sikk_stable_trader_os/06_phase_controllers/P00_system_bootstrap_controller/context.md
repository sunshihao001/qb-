# P00 系统建造与方法论编译控制器

文件编号：P00-CONTEXT-001  
阶段编号：P00_system_bootstrap_controller  
阶段名称：系统建造与方法论编译控制器  
版本：v1.0-institutional  
状态：REQUIRED_BEFORE_ALL_BUSINESS_PHASES  
适用系统：SIKK Stable Trader OS  
安全边界：paper-only，禁止真实交易  
上游阶段：K00_knowledge_intake_taskization  
下游阶段：Governance Plane / Domain Plane / Data Plane / Control Plane / P01-P10  

## 1. 阶段定位

P00 不是普通阶段说明文档。P00 是 SIKK Stable Trader OS 的系统建造控制器，负责把 K00 生成的知识资产、Phase Controller 候选规格、方法论蓝图、治理要求、领域要求、数据要求和旧系统资产，编译成正式系统结构。

P00 必须解决：文档未消费、任务包未执行、阶段说明不可调度、文件级验收冒充系统验收、P01 被提前启动、状态源不唯一、领域对象未注册、数据字段无来源、方法论无 trace matrix、下游无 handoff。

## 2. P00 核心定义

P00 是系统编译器。它读取 system_methodology_blueprint.md、K00 phase_controller_candidate_spec、K00_to_P00_handoff_packet、existing project files，然后编译生成 current_system_state.json、phase_registry.yaml、system_asset_index.json、trace matrices、plane outputs、P01-P10 controller stubs、handoff registry 与 next_stage_decision.json。

默认情况下，在 Data Plane 和 Control Plane 未通过验收之前，P01 必须保持 BLOCKED_BY_DATA_PLANE。

## 3. P00 权限边界

P00 可以创建系统控制文件、阶段注册表、P01-P10 controller stub、系统资产索引、trace matrix、handoff registry，并裁决下一合法阶段。

P00 不可以执行真实交易、输出买卖指令、直接运行 P01、直接运行钱包结构分析、跳过 Governance/Domain/Data/Control Plane，或把文件级验收等同于系统级验收。

## 4. P00 核心问题树

- 方法论是否存在、被抽取、映射、消费。
- K00 是否生成 candidate spec 与 handoff packet，是否被 P00 消费。
- Governance/Domain/Data/Control/Trace/Acceptance/Handoff Plane 是否存在。
- K00/P00/P01-P10 是否注册，P01 是否被正确阻断。
- 当前唯一权威阶段、blocking gaps、next legal stage 是否明确。

## 5. P00 编译链路

Step 1 读取 K00 handoff；Step 2 读取 system_methodology_blueprint；Step 3 扫描系统结构；Step 4 识别状态分裂；Step 5 建立 current_system_state；Step 6 建立 phase_registry；Step 7 建立 system_asset_index；Step 8 标记 K00 资产消费；Step 9-12 编译治理/领域/数据/控制平面；Step 13 生成 P01-P10 stubs；Step 14-17 生成 trace、handoff、report 与状态回写。

## 6. P00 成功标准

P00 成功必须意味着：方法论被系统文件覆盖；K00 资产被 P00 消费；阶段注册；P01 正确阻断；Data Plane 任务生成；Control Plane 建立；trace matrix 能解释要求实现；handoff registry 能解释上游产物交给谁。

## 7. 默认安全裁决

```json
{"paper_only": true, "real_trade_enabled": false, "p01_runtime_connection_allowed": false, "real_order_allowed": false, "private_key_allowed": false, "auto_trade_allowed": false}
```

## 8. P00 最终输出判断

必须明确：P00 是否验收通过、P01 是否仍被阻断、阻断原因、下一合法阶段、系统平面状态、K00 资产消费状态、是否允许进入 P01。除非 Data Plane 和 Control Plane 均通过验收，否则 P01 不允许启动。
