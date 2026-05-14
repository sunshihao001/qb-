# Document Passport — SIKK Stable Trader OS v2.0 Design

- material_id: `stable_trader_os_v2_0_design_doc_20260511`
- title: Stable Trader OS 完整专业化系统体系设计 v2.0
- source_path: `/root/.hermes/cache/documents/doc_226b4d13f48d_Stable Trader OS 完整专业化系统体系设计 v2.0 (1).md`
- sha256: `b752a432e8692564e9e38bf32e92f8fab12d1ed7b545a52db3ccacbb9433a37c`
- ingested_at: `2026-05-11T05:18:18Z`
- source_type: markdown_uploaded_document
- authority_level: `AUTHORITATIVE_METHOD_SEED`
- target_system: `SIKK_STABLE_TRADER_OS`
- runtime_boundary: `observe_paper_only`

## Scope

本资料定义 SIKK Stable Trader OS v2.0 的系统方法论、九大平面、P00-P09 阶段、领域对象、状态机、硬否定、数据流、判断流、handoff 流、HER 执行协议与建设顺序。

## Can Influence

- `00_methodology/system_methodology_blueprint.md`
- 九大系统平面定义
- 领域对象与状态字典
- Phase Controller 合约与验收门
- Atomic Skill 候选清单
- HER 总控执行协议

## Must Not Directly Change

- 不直接生成买入/卖出判断
- 不直接修改实时策略规则
- 不授权真实交易、签名、broadcast、swap
- 不用复盘结论直接污染运行规则

## Extraction Quality

- 原始资料为完整 Markdown 文档。
- 关键结构清晰：方法论、平面、阶段、状态、流、协议、建设顺序均可直接锚定。
- 本次派生产物保留为系统方法论总纲，不作为运行数据或交易执行依据。
