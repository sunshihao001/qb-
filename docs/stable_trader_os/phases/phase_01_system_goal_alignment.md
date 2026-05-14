# Phase 01 系统总目标对齐说明

## 1. Stable Trader OS 总目标

从所有看起来像机会的结构中，连续剔除低质量、错误场景、假成交、派发风险、疲劳拖延和错误位置，只保留极少数 A+P1 且证据链未被否决的样本。

## 2. Phase 01 阶段目标

Phase 01 只负责数据事实层：

- 原始数据接收
- 字段标准化
- 来源优先级
- 缺失字段裁决
- 数据质量门禁
- Phase 02 handoff

它不负责：

- 结构角色定性
- 吸筹 / 派发 / 二段扩张判断
- 买卖点判断
- 策略通过判断
- 实盘或纸面执行

## 3. 总目标如何落到 Phase 01

- “剔除低质量” → `quality_gate_rules.json` + `missing_field_policy.json`
- “剔除假成交” → `anomaly_detection_rules.json` + trade/kline/source conflict checks
- “证据链未被否决” → raw source manifest + field source priority + runtime trace
- “先判断数据是否可靠” → `phase_01_quality_gate_schema.json`
- “再判断钱包结构” → `phase_01_to_phase_02_contract.json`

## 4. Phase 01 的完成定义

Phase 01 只有在以下资产存在且通过验收后才算系统数据层完成：

- schema
- configs
- contracts
- examples
- tests
- runtime trace schema / sample
- audit checklist
- acceptance matrix

## 5. 禁止漂移

Phase 01 禁止为了“看起来更聪明”而提前输出市场解释。所有解释性判断都必须后移到 Phase 02+，并且只能读取 Phase 01 明确交接的事实字段。
