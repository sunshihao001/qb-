# SIKK Phase01 Data Fact Layer Backup

This is a unified backup package, not the live working root.

## Included
- root_sikk_gmgn/data/source_wallet_bot/: per-token Phase01 fact stores.
- root_sikk_gmgn/modules/source_wallet_bot/: runtime code, including router.
- root_sikk_gmgn/contracts/stable_trader_os/phase_01_data_fact/: contracts.
- root_sikk_gmgn/schemas/stable_trader_os/phase_01_data_fact/: schemas.
- hermes_skill/sikk-phase01-data-fact-skill/: HER governance skill.

## Restore principle
Unified backup is OK. Live runtime should still keep separated canonical paths:
- /root/sikk-gmgn/data/source_wallet_bot/
- /root/sikk-gmgn/modules/source_wallet_bot/
- /root/sikk-gmgn/contracts/stable_trader_os/phase_01_data_fact/
- /root/sikk-gmgn/schemas/stable_trader_os/phase_01_data_fact/
- /root/.hermes/profiles/sunqbfemxbot/skills/software-development/sikk-phase01-data-fact-skill/

Core rule: data is data, modules are execution, skill is governance. Backup can be unified; working directories should not be merged.
