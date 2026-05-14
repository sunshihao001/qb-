# Intel Bot 钱包结构研究工作流 2小时升级版 - 最终报告

## 1. 本次任务目标

将旧的 SIKK-GMGN 钱包结构采集分析系统整理为 Intel Bot 内部的专业结构地址研究子系统，只做结构情报分析，不做交易执行。

## 2. 旧系统可复用逻辑

- 事实源接收与导出链路
- 钱包实体画像
- 当前 token 行为分析
- 同源关系分析
- 历史地址库复查
- 评分与证据等级
- GMGN 备注输出
- 多轮快照 delta
- wallet_structure_decision 交接文件

## 3. 旧系统缺口

- 原始事实源接收合同不完整
- 缺少统一 normalized 合约
- 时间锚点不统一
- 同源组规则未独立成文
- 历史地址库未结构化
- GMGN 备注标准未固定
- delta 与 failure attribution 回流不足

## 4. Intel Bot 小模块体系

共设计 11 个模块：

- 1. wallet_source_reader
- 2. wallet_normalized_adapter
- 3. wallet_entity_profiler
- 4. current_token_behavior_analyzer
- 5. same_source_group_analyzer
- 6. chip_transfer_analyzer
- 7. historical_wallet_profiler
- 8. wallet_structure_scorer
- 9. wallet_decision_builder
- 10. gmgn_note_exporter
- 11. wallet_review_feedback

## 5. 分析命令镜头

共设计 10 个命令镜头：

- /SCAN_WALLET_SOURCE
- /DEEP_WALLET_ROLE
- /TRACE_SAME_SOURCE
- /TRACE_BACKFLOW
- /DELTA_CHIP
- /HYP_DOMINANT_INTENT
- /ANGLE_WALLET_PATTERN
- /CHALLENGE_SCORE
- /BUILD_GMGN_NOTE
- /BUILD_WALLET_DECISION

## 6. 后续任务包

建议优先落地：
- normalized 合约
- source reader
- entity profiler
- current token behavior analyzer
- same-source group analyzer
- chip transfer analyzer
- historical wallet profiler
- wallet_structure_decision 合约
- GMGN note 规则
- review feedback

## 7. 风险与禁止事项确认

- 不修改状态机
- 不修改 paper runner
- 不开启实盘
- 不读取私钥
- 不签名
- 不广播
- 不 swap
- 不删除旧文件

## 8. 下一阶段建议

先实现 read-only 的 legacy 钱包情报索引层，再逐步补齐 normalized 合约与查询入口，最后再做 Telegram 展示与导出。
