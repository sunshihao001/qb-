# HER-DFAFS System Gap Register

## GAP-K00-CONTROLLER-BRIDGE

- severity: HIGH
- status: OPEN
- description: F00 的输入合约要求 K00 handoff 是唯一合法入口，但 canonical controllers 目录下缺少 K00 controller package 或明确 K00 bridge contract。
- impact: 任何 F00 运行若没有 K00 handoff，都必须阻断为 `F00_BLOCKED`。
- required artifact:
  - `controllers/K00_knowledge_intake_controller/` 或
  - `bridges/K00_to_F00_handoff_bridge/`
- acceptance:
  - handoff schema 存在
  - document_passport_refs/corpus_index_refs/system_mapping_refs/gap_detection_refs 可追溯
  - O00 能引用 K00 输出

## GAP-NAMING-COMPATIBILITY

- severity: MEDIUM
- status: PARTIALLY_RESOLVED
- description: 控制器资产使用 `01_f00_manifest.yaml` 等阶段前缀命名，通用检查器容易误判。
- required artifact:
  - semantic asset detection rules
- acceptance:
  - audit_result 使用语义资产检测，而非字面文件名检测。

## GAP-SYSTEM-AUDIT-ENTRYPOINT

- severity: MEDIUM
- status: RESOLVED_INITIAL
- description: 缺少系统自审固定入口。
- created artifact:
  - `system_audit/README.md`
  - `system_audit/HER_DOC_SYSTEM_AUDIT_PROTOCOL.md`
  - `system_audit/SYSTEM_STAGE_READINESS_MATRIX.md`
  - `system_audit/SYSTEM_GAP_REGISTER.md`

## GAP-AUDIT-RUNNER

- severity: MEDIUM
- status: OPEN
- description: 当前系统自审包是文件化协议与审计结果，尚未绑定独立 CLI runner。
- required artifact:
  - `tools/her_doc_system_audit.py`
- acceptance:
  - 能重新生成 audit_result
  - 能返回 READY_WITH_GAPS / BLOCKED / READY 等状态
  - 能检查 JSON/YAML 解析
