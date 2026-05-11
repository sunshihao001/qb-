---
artifact_type: route_simulation_output
status: verified
version: v2.0-stage11
generated_at: 2026-05-07T09:10:30Z
task_type: wallet_intel_semantic_integration
---
# Wallet-Intel 路由模拟输出 V2.0 — 阶段 11

## 模拟输入
> 我需要整理钱包数据采集分析和结构分析旧目录，把有用数据导入新体系，让 Hermes 能理解。

## 路由判断
```text
task_type = wallet_intel_semantic_integration
```

## 路由说明
- 该输入命中 Wallet-Intel 关键词：钱包数据、结构分析、旧目录、导入、新体系、Hermes 理解。
- 不能按普通目录整理处理。
- 必须进入 Wallet-Intel 专用工作流，而不是 directory_governance / ordinary_file_cleanup / generic_migration。

## 固定工作流阶段
```text
阶段 0：任务护照生成
阶段 1：旧目录只读侦察
阶段 2：文件语义分类
阶段 3：按 token 建立索引
阶段 4：数据分层归属判断
阶段 5：高价值旧数据复制 / 登记
阶段 6：旧新路径映射
阶段 7：字段字典生成
阶段 8：数据护照生成
阶段 9：Hermes 读取入口生成
阶段 10：抽样验证
阶段 11：最终整合报告
阶段 12：记忆候选写入
```

## 禁止动作
```text
扫描旧数据目录
复制旧数据
移动旧目录
删除旧目录
覆盖旧文件
修改业务代码
触发交易
读取或输出私钥、API key、token
git push
```

## 预期产物
```text
task_passport.md
legacy_readonly_scout_report.md
file_semantic_classification.csv
token_index.csv
token_layer_assignment.json
high_value_import_plan.md
legacy_path_map.csv
field_dictionary.md/json
token_data_passport.md/json
hermes_read_entry.md
import_after_validation_report.md
final_integration_report.md
candidate_memory_rules.md
```

## 完成验证标准
```text
任务护照存在；
旧目录侦察完成；
文件语义分类完成；
token 索引完成；
旧新路径映射完成；
高价值旧数据已复制或登记；
字段字典完成；
数据护照完成；
Hermes 读取入口完成；
抽样验证 3-5 个 token；
Hermes 能说明事实数据、结构证据、行为推断、handoff 数据和缺失项；
Hermes 能说明旧数据来源；
Hermes 能区分事实、证据、推断、交接；
旧目录仍然保留；
没有删除、移动、覆盖旧文件；
没有修改业务代码；
没有触发交易。
```

## 模拟边界
本次仅为路由模拟，不扫描、不复制、不迁移、不修改业务代码、不触发交易。
