# 中英目录映射表

更新时间：2026-05-06T03:48:15+00:00

## 原则

- 底层真实路径保留英文，避免脚本、测试、路由和兼容层大范围失效。
- 中文名只作为展示名、文档名、路由说明和人类可读别名。
- 所有自动化仍以英文真实路径为准。

## 映射表

### data/source_wallet_bot
- 中文展示名：数据/钱包事实
- 用途：钱包事实采集、标准化、同源关系、资金路径、地址历史
- 写入策略：new_primary_write_path

### data/intel_bot
- 中文展示名：数据/行为推断
- 用途：主导侧行为动机推断、筹码控制状态、行为解释
- 写入策略：new_primary_write_path

### research_loop/methodology
- 中文展示名：研究循环/方法论库
- 用途：判断逻辑、反证规则、量化模型、字段合约、输出合约
- 写入策略：method_library

### research_loop/structure_analysis
- 中文展示名：研究循环/结构分析流水线
- 用途：护照、逻辑库、字段合约、模块地图、反证、量化、推断、输出、任务票、状态
- 写入策略：workflow_pipeline

### legacy_compat
- 中文展示名：旧路径兼容层
- 用途：old_path→new_path 映射、fallback 说明、只读兼容索引
- 写入策略：index_only

### imports
- 中文展示名：导入暂存区
- 用途：外部资料 staging 导入、历史包、原始导入文件
- 写入策略：staging_only

### reports
- 中文展示名：报告区
- 用途：审计、验收、汇总、人类可读输出
- 写入策略：human_readable

### docs
- 中文展示名：文档区
- 用途：系统宪法、目录规则、协议、设计说明、使用方法
- 写入策略：documentation

### contracts
- 中文展示名：合同区
- 用途：Bot 交接合同、模块合同、输出合约、权责边界
- 写入策略：contracts

### schemas
- 中文展示名：Schema区
- 用途：JSON schema、manifest schema、统一数据结构
- 写入策略：schemas

### modules
- 中文展示名：代码模块区
- 用途：collector、router、normalizer、validator、inference engine
- 写入策略：code

### scripts
- 中文展示名：脚本区
- 用途：迁移脚本、导入脚本、整理脚本、校验脚本
- 写入策略：scripts

### tests
- 中文展示名：测试区
- 用途：pytest、合约测试、路由测试、校验器测试
- 写入策略：tests

### tools
- 中文展示名：工具区
- 用途：通用辅助工具
- 写入策略：tools

### knowledge
- 中文展示名：知识库
- 用途：吸收后的长期知识、规则摘要、经验沉淀
- 写入策略：knowledge

### ai_context
- 中文展示名：AI上下文材料
- 用途：上下文导出、辅助理解材料
- 写入策略：context

### audits
- 中文展示名：审计区
- 用途：历史审计材料
- 写入策略：audit

### data/gmgn_candidates_live_run
- 中文展示名：历史运行冻结区
- 用途：旧 live run、混合输出、历史保留
- 写入策略：legacy_keep_in_place

### outputs
- 中文展示名：旧输出区
- 用途：旧输出，后续不作为主写路径
- 写入策略：legacy_keep_in_place

### 结构分析
- 中文展示名：旧结构分析资料区
- 用途：旧结构分析备份/参考
- 写入策略：legacy_keep_in_place

### 钱包数据分析
- 中文展示名：旧钱包数据分析区
- 用途：旧钱包数据分析备份/参考
- 写入策略：legacy_keep_in_place

## 目录使用规则

1. 数据类结果写入 data/ 下对应英文真实路径。
2. 方法论写入 research_loop/methodology/ 或 research_loop/structure_analysis/。
3. 代码写入 modules/、scripts/、tests/、tools/。
4. legacy 只做兼容索引，不做主写路径。
5. 中文目录名仅用于展示，不替代真实文件系统路径。