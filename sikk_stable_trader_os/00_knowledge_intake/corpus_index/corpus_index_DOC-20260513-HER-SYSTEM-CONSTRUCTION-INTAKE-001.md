# Corpus Index — DOC-20260513-HER-SYSTEM-CONSTRUCTION-INTAKE-001

## section_index
- S1 Core identity definition: HER as a controlled runtime system, not a chat summarizer.
- S2 Core system rules: phase controller definition and required contracts/state/handoff.
- S3 Upload document processing principles: all uploads must enter K00 first.
- S4 K00 Knowledge Intake & Taskization: raw, registry, passport, index, mapping, gaps, package, state, acceptance, handoff.
- S5 Target Phase Controller execution: only after K00 acceptance + handoff, and only under contract checks.
- S6 Final reply format and execution boundaries.

## key_objects
- HER controlled runtime chain
- Phase Controller
- K00 Knowledge Intake & Taskization
- document passport
- corpus index
- system mapping
- gap detection
- phase task package
- phase state
- handoff packet

## core_rules
- All uploads must pass through K00.
- No direct entry to PXX/IXX/Runner/Paper/Live.
- Do not overwrite raw uploads.
- Do not treat chat context as system state.
- Do not declare READY without acceptance and trace.

## key_assertions
- Phase Controller must include input contract, output contract, execution protocol, acceptance gate, trace requirements, recovery policy, and handoff packet.
- Missing any required structure means the controller is not complete.
- K00 acceptance requires raw + registry + passport + index + mapping + gaps + task package + state + handoff + trace/audit.

## input_requirements
- source_name
- source_type
- raw_path
- received_at
- content_hash

## output_requirements
- file-backed K00 assets
- acceptance result
- handoff packet
- trace/audit record

## forbidden_actions
- summary-only handling
- direct downstream execution
- runner start
- paper/live start
- production rule mutation

## acceptance_requirements
- preserve raw
- register source
- passport the document
- index the corpus
- map the system planes
- detect gaps
- package the target phase
- write phase state
- write acceptance
- write handoff

## trace_requirements
- record content hash
- record write locations
- record acceptance basis
- record blocked/allowed downstream actions

## handoff_requirements
- from_phase
- to_phase
- source refs
- passport refs
- corpus refs
- mapping refs
- gap refs
- package refs
- state refs
- acceptance refs

## schema_candidates
- document passport YAML
- system mapping JSON
- gap detection JSON
- phase state JSON
- handoff packet JSON

## controller_candidates
- K00 Knowledge Intake & Taskization
- P00 System Bootstrap Controller

## runtime_risk_flags
- No production execution risk.
- Design-only downstream routing only.
- No runner/tool binding permitted from this document.
