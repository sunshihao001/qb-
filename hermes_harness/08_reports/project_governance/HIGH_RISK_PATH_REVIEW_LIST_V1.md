# High-Risk Path Human Review List V1

These paths must not be migrated automatically.

## Review items

### .git/
- risk: `high`
- current_status: `system_or_cache`
- proposed_action: `keep_in_place_no_new_writes`
- reason: system/cache directory; never migrate via governance task

### .pytest_cache/
- risk: `medium`
- current_status: `system_or_cache`
- proposed_action: `keep_in_place_no_new_writes`
- reason: system/cache directory; never migrate via governance task

### __pycache__/
- risk: `medium`
- current_status: `system_or_cache`
- proposed_action: `keep_in_place_no_new_writes`
- reason: system/cache directory; never migrate via governance task

### ai_context/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### audits/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### config/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### knowledge/
- risk: `high`
- current_status: `legacy_or_ambiguous`
- proposed_action: `map_only_pending_review`
- reason: non-canonical root with project-significant content

### logs/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### outputs/
- risk: `high`
- current_status: `legacy_or_ambiguous`
- proposed_action: `map_only_pending_review`
- reason: non-canonical root with project-significant content

### scripts/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### tasks/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### 中文导航/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### 中文目录导航/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### 结构分析/
- risk: `medium`
- current_status: `non_canonical_root`
- proposed_action: `map_only_pending_review`
- reason: root directory outside canonical route table

### 钱包数据分析/
- risk: `high`
- current_status: `legacy_or_ambiguous`
- proposed_action: `map_only_pending_review`
- reason: non-canonical root with project-significant content
