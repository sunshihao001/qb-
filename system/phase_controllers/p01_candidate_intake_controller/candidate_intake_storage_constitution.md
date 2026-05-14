# P01 Storage Constitution

System package root: `/root/sikk-gmgn/system/phase_controllers/p01_candidate_intake_controller/`

Runtime data root: `/root/sikk-gmgn/data/phase_controllers/p01_candidate_intake/`

Raw candidate inputs are immutable. Duplicate discoveries append source events and must not overwrite first discovery context. Runtime outputs may only hand off to P02_SOURCE_DATA_FACT_CONTROLLER.
