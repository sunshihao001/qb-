# High-Risk Path Review Refined V1

This is a refined human-review list. It is still advisory and does not execute migration.

## Grouped review items

### .git/
- group: `system_cache_do_not_touch`
- risk: `high`
- refined_recommended_path: `none`
- refined_action: `do_not_migrate_keep_in_place`
- rationale: System/cache directory; not a project content migration target.

### .pytest_cache/
- group: `system_cache_do_not_touch`
- risk: `medium`
- refined_recommended_path: `none`
- refined_action: `do_not_migrate_keep_in_place`
- rationale: System/cache directory; not a project content migration target.

### __pycache__/
- group: `system_cache_do_not_touch`
- risk: `medium`
- refined_recommended_path: `none`
- refined_action: `do_not_migrate_keep_in_place`
- rationale: System/cache directory; not a project content migration target.

### ai_context/
- group: `context_candidate`
- risk: `medium`
- refined_recommended_path: `docs/context/ or hermes_harness/03_task_runtime/compact_snapshots/ after classification`
- refined_action: `manual_review_before_copy_only`
- rationale: Context material may be stale or task-scoped.

### audits/
- group: `audit_candidate`
- risk: `medium`
- refined_recommended_path: `reports/audit/ or hermes_harness/10_audit/ after ownership review`
- refined_action: `manual_review_before_copy_only`
- rationale: Audit reports must preserve provenance.

### config/
- group: `configuration_candidate`
- risk: `medium`
- refined_recommended_path: `docs/config_reference/ or modules/<bot>/config/ after secret scan and ownership review`
- refined_action: `manual_review_required_no_secret_output`
- rationale: Config may contain sensitive or runtime-critical settings.

### knowledge/
- group: `documentation_or_navigation_candidate`
- risk: `high`
- refined_recommended_path: `docs/navigation_or_knowledge_review/`
- refined_action: `index_only_then_human_review`
- rationale: Likely documentation/navigation knowledge; classify before any copy.

### logs/
- group: `runtime_output_candidate`
- risk: `medium`
- refined_recommended_path: `data/legacy/{asset_id}/ or reports/legacy/{asset_id}/ after classification`
- refined_action: `manifest_only_then_copy_only_if_needed`
- rationale: Runtime outputs/logs may be historical evidence; do not move.

### outputs/
- group: `runtime_output_candidate`
- risk: `high`
- refined_recommended_path: `data/legacy/{asset_id}/ or reports/legacy/{asset_id}/ after classification`
- refined_action: `manifest_only_then_copy_only_if_needed`
- rationale: Runtime outputs/logs may be historical evidence; do not move.

### scripts/
- group: `script_candidate`
- risk: `medium`
- refined_recommended_path: `tools/ or modules/<bot_or_domain>/ after code ownership review`
- refined_action: `manual_review_before_copy_only`
- rationale: Scripts may be entrypoints or helpers; ownership must be known before standardization.

### tasks/
- group: `task_state_candidate`
- risk: `medium`
- refined_recommended_path: `research_loop/task_packages/ or research_loop/state/ after classification`
- refined_action: `manual_review_before_copy_only`
- rationale: Task files may define long-running state; preserve context.

### 中文导航/
- group: `documentation_or_navigation_candidate`
- risk: `medium`
- refined_recommended_path: `docs/navigation_or_knowledge_review/`
- refined_action: `index_only_then_human_review`
- rationale: Likely documentation/navigation knowledge; classify before any copy.

### 中文目录导航/
- group: `documentation_or_navigation_candidate`
- risk: `medium`
- refined_recommended_path: `docs/navigation_or_knowledge_review/`
- refined_action: `index_only_then_human_review`
- rationale: Likely documentation/navigation knowledge; classify before any copy.

### 结构分析/
- group: `domain_analysis_candidate`
- risk: `medium`
- refined_recommended_path: `research_loop/methodology/ or reports/source_wallet_bot/legacy/ after classification`
- refined_action: `manual_review_required_before_copy_only`
- rationale: Domain-significant Chinese analysis directories; high semantic risk.

### 钱包数据分析/
- group: `domain_analysis_candidate`
- risk: `high`
- refined_recommended_path: `research_loop/methodology/ or reports/source_wallet_bot/legacy/ after classification`
- refined_action: `manual_review_required_before_copy_only`
- rationale: Domain-significant Chinese analysis directories; high semantic risk.
