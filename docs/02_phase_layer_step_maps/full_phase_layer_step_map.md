# Full Phase Layer Step Map

## phase_00_system_constitution

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P00_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_01_data_fact

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P01_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_02_wallet_structure

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P02_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_03_chip_control

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P03_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_04_scenario_recognition

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P04_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_05_structure_position

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P05_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_06_strategy_gate

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P06_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_07_execution_risk

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P07_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_08_review_learning

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P08_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit

## phase_09_system_upgrade

- layer: Phase Controller
- input: `sikk_stable_trader_os/02_phase_controllers/P09_*/phase_input_contract.json`
- output: `phase_output_contract.json` required files
- steps: load context -> validate input -> execute bound skills/tools -> write outputs -> run acceptance -> emit handoff
- acceptance: `phase_acceptance_gate.yaml`
- blocking status: schema failure, unsafe execution authorization, hard negative when mapped as block
- handoff: `phase_handoff_packet.schema.json`
- downstream reader: next phase or total-control audit
