# Path Migration Matrix V1

This matrix is advisory only. No migration is executed.

## Matrix

### .git/
- status: `system_or_cache`
- recommended_path: `none`
- recommended_action: `keep_in_place_no_new_writes`
- risk: `high`
- requires_human_review: `True`
- reason: system/cache directory; never migrate via governance task

### .pytest_cache/
- status: `system_or_cache`
- recommended_path: `none`
- recommended_action: `keep_in_place_no_new_writes`
- risk: `medium`
- requires_human_review: `True`
- reason: system/cache directory; never migrate via governance task

### __pycache__/
- status: `system_or_cache`
- recommended_path: `none`
- recommended_action: `keep_in_place_no_new_writes`
- risk: `medium`
- requires_human_review: `True`
- reason: system/cache directory; never migrate via governance task

### ai_context/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### audits/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### config/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### contracts/
- status: `canonical_root`
- recommended_path: `contracts/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### data/
- status: `canonical_root`
- recommended_path: `data/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### docs/
- status: `canonical_root`
- recommended_path: `docs/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### hermes_harness/
- status: `canonical_root`
- recommended_path: `hermes_harness/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### imports/
- status: `canonical_root`
- recommended_path: `imports/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### knowledge/
- status: `legacy_or_ambiguous`
- recommended_path: `legacy_compat/path_maps/ + possible reports/data/research_loop mapping`
- recommended_action: `map_only_pending_review`
- risk: `high`
- requires_human_review: `True`
- reason: non-canonical root with project-significant content

### legacy_compat/
- status: `canonical_root`
- recommended_path: `legacy_compat/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### logs/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### modules/
- status: `canonical_root`
- recommended_path: `modules/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### outputs/
- status: `legacy_or_ambiguous`
- recommended_path: `legacy_compat/path_maps/ + possible reports/data/research_loop mapping`
- recommended_action: `map_only_pending_review`
- risk: `high`
- requires_human_review: `True`
- reason: non-canonical root with project-significant content

### reports/
- status: `canonical_root`
- recommended_path: `reports/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### research_loop/
- status: `canonical_root`
- recommended_path: `research_loop/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### schemas/
- status: `canonical_root`
- recommended_path: `schemas/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### scripts/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### tasks/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### tests/
- status: `canonical_root`
- recommended_path: `tests/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### tools/
- status: `canonical_root`
- recommended_path: `tools/`
- recommended_action: `retain`
- risk: `low`
- requires_human_review: `False`
- reason: existing canonical or harmless project root

### 中文导航/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### 中文目录导航/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### 结构分析/
- status: `non_canonical_root`
- recommended_path: `pending_classification`
- recommended_action: `map_only_pending_review`
- risk: `medium`
- requires_human_review: `True`
- reason: root directory outside canonical route table

### 钱包数据分析/
- status: `legacy_or_ambiguous`
- recommended_path: `legacy_compat/path_maps/ + possible reports/data/research_loop mapping`
- recommended_action: `map_only_pending_review`
- risk: `high`
- requires_human_review: `True`
- reason: non-canonical root with project-significant content
