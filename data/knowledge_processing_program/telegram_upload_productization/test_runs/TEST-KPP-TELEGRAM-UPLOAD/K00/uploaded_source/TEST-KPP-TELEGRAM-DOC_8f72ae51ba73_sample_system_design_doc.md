# KPP Sample System Design Doc

## Purpose
This document defines a sample HER system-building material used to verify the Knowledge Processing Program automation chain.

## Controller Candidate
Create a candidate-only controller called sample_kpp_controller. It must not mutate production runtime without governance review.

## Schema Candidate
The controller candidate requires input_contract, output_contract, acceptance_gate, validation_report, and handoff_packet.

## Governance
All derived outputs must enter P00/governance review before any runtime integration.
