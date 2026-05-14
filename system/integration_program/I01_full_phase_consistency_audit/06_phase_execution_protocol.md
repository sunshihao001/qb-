# I01 Execution Protocol

1. Read professional build order and phase_controller_index.
2. Inventory P01-P10 input/output/handoff/acceptance/status artifacts.
3. Build phase_io_alignment_matrix.
4. Validate handoff chain continuity.
5. Validate status codes and gap propagation.
6. Validate forbidden-use inheritance and safety boundaries.
7. Detect phase boundary violations.
8. Produce fix_priority_list.
9. Produce I01 acceptance result and i01_to_i02_handoff_packet.

Hard stops: missing P01-P10 index, no phase artifacts, any live execution/signing/auto-deploy path request.
