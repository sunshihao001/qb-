---
artifact_type: control_policy
status: verified
version: v1.1
valid_until: null
---
# Input Contract Policy

Inputs must be classified before processing: natural_language, file_path, url, archive, screenshot, log, command_output, existing_report, old_task_state, code_directory. File paths are read-only first; archives get manifest first; logs get error extraction first.
