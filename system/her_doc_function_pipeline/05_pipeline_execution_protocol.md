# Pipeline Execution Protocol

O00.0 read inputs
O00.1 create run_id/output dirs
O00.2 copy raw document
O00.3 write operator_goal.json
O00.4 run K00
O00.5 validate K00
O00.6 run F00
O00.7 validate F00
O00.8 run V00
O00.9 validate V00
O00.10 run A00
O00.11 if BLOCKED write recovery and stop
O00.12 if READY_WITH_GAPS continue H00
O00.13 run H00
O00.14 run U00
O00.15 run G00
O00.16 write run_summary
O00.17 write final_report
O00.18 write trace/audit
