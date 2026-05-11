# Path Standard Verification V1

## Status
PASSED

## Results
```json
[
  {
    "path": "/root/sikk-gmgn/hermes_harness/08_reports/project_governance/CANONICAL_PATH_STANDARD_V1.md",
    "exists": true,
    "readable": true,
    "valid_json": null,
    "excerpt": "     1|# Canonical Path Standard V1\n     2|\n     3|## Purpose\n     4|\n     5|This standard defines where future Hermes/SIKK outputs should be read from and written to. It does not move old files.\n     6|\n     7|## Core rule\n     8|\n     9|Every new artifact must answer four questions before write:\n    10|\n    11|1. Bot / domain?\n    12|2. Asset class?\n    13|3. Asset ID?\n    14|4. Canonical write path?\n    15|\n    16|## Canonical roots\n    17|\n    18|- `hermes_harness/` — Hermes control plane, r"
  },
  {
    "path": "/root/sikk-gmgn/hermes_harness/08_reports/project_governance/PATH_MIGRATION_MATRIX_V1.md",
    "exists": true,
    "readable": true,
    "valid_json": null,
    "excerpt": "     1|# Path Migration Matrix V1\n     2|\n     3|This matrix is advisory only. No migration is executed.\n     4|\n     5|## Matrix\n     6|\n     7|### .git/\n     8|- status: `system_or_cache`\n     9|- recommended_path: `none`\n    10|- recommended_action: `keep_in_place_no_new_writes`\n    11|- risk: `high`\n    12|- requires_human_review: `True`\n    13|- reason: system/cache directory; never migrate via governance task\n    14|\n    15|### .pytest_cache/\n    16|- status: `system_or_cache`\n    17|- rec"
  },
  {
    "path": "/root/sikk-gmgn/hermes_harness/08_reports/project_governance/PATH_MIGRATION_MATRIX_V1.json",
    "exists": true,
    "readable": true,
    "valid_json": true,
    "excerpt": "     1|[\n     2|  {\n     3|    \"current_path\": \".git/\",\n     4|    \"status\": \"system_or_cache\",\n     5|    \"recommended_path\": \"none\",\n     6|    \"recommended_action\": \"keep_in_place_no_new_writes\",\n     7|    \"risk\": \"high\",\n     8|    \"requires_human_review\": true,\n     9|    \"reason\": \"system/cache directory; never migrate via governance task\"\n    10|  },\n    11|  {\n    12|    \"current_path\": \".pytest_cache/\",\n    13|    \"status\": \"system_or_cache\",\n    14|    \"recommended_path\": \"none\",\n    "
  },
  {
    "path": "/root/sikk-gmgn/hermes_harness/08_reports/project_governance/LEGACY_KEEP_IN_PLACE_POLICY_V1.md",
    "exists": true,
    "readable": true,
    "valid_json": null,
    "excerpt": "     1|# Legacy Keep-In-Place Policy V1\n     2|\n     3|## Purpose\n     4|\n     5|Legacy paths remain readable and traceable, but are not automatically moved, renamed, or deleted.\n     6|\n     7|## Hard rules\n     8|\n     9|- Do not delete legacy files.\n    10|- Do not move legacy directories.\n    11|- Do not rename core files.\n    12|- Do not make legacy runtime directories the new main write path.\n    13|- Use copy-only mapping if future standardization is approved.\n    14|- Record `old_path ->"
  },
  {
    "path": "/root/sikk-gmgn/hermes_harness/08_reports/project_governance/HIGH_RISK_PATH_REVIEW_LIST_V1.md",
    "exists": true,
    "readable": true,
    "valid_json": null,
    "excerpt": "     1|# High-Risk Path Human Review List V1\n     2|\n     3|These paths must not be migrated automatically.\n     4|\n     5|## Review items\n     6|\n     7|### .git/\n     8|- risk: `high`\n     9|- current_status: `system_or_cache`\n    10|- proposed_action: `keep_in_place_no_new_writes`\n    11|- reason: system/cache directory; never migrate via governance task\n    12|\n    13|### .pytest_cache/\n    14|- risk: `medium`\n    15|- current_status: `system_or_cache`\n    16|- proposed_action: `keep_in_plac"
  },
  {
    "path": "/root/sikk-gmgn/hermes_harness/08_reports/project_governance/HIGH_RISK_PATH_REVIEW_LIST_V1.json",
    "exists": true,
    "readable": true,
    "valid_json": true,
    "excerpt": "     1|[\n     2|  {\n     3|    \"current_path\": \".git/\",\n     4|    \"status\": \"system_or_cache\",\n     5|    \"recommended_path\": \"none\",\n     6|    \"recommended_action\": \"keep_in_place_no_new_writes\",\n     7|    \"risk\": \"high\",\n     8|    \"requires_human_review\": true,\n     9|    \"reason\": \"system/cache directory; never migrate via governance task\"\n    10|  },\n    11|  {\n    12|    \"current_path\": \".pytest_cache/\",\n    13|    \"status\": \"system_or_cache\",\n    14|    \"recommended_path\": \"none\",\n    "
  }
]
```
