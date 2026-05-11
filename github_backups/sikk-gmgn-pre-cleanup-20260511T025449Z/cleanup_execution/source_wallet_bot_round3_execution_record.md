# source_wallet_bot cleanup round3 execution record

- Plan: `research_loop/plans/data_cleanup_20260511/source_wallet_bot_archive_round3.txt`
- Archive root: `/root/sikk-archive/source_wallet_bot_round3`

## Executed moves
- `/root/sikk-gmgn/data/source_wallet_bot/legacy/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump` -> `/root/sikk-archive/source_wallet_bot_round3/legacy/7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump`
- `/root/sikk-gmgn/data/source_wallet_bot/legacy/6Xipib7UavxaXvWDhepFpU4NzypozVBPvNNjxTdXpump` -> `/root/sikk-archive/source_wallet_bot_round3/legacy/6Xipib7UavxaXvWDhepFpU4NzypozVBPvNNjxTdXpump`
- `/root/sikk-gmgn/data/source_wallet_bot/legacy/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump` -> `/root/sikk-archive/source_wallet_bot_round3/legacy/3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump`
- `/root/sikk-gmgn/data/source_wallet_bot/legacy/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump` -> `/root/sikk-archive/source_wallet_bot_round3/legacy/GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump`
- `/root/sikk-gmgn/data/source_wallet_bot/auto_tasks/wallet_structure_registry_consumption_final_20260508_022106` -> `/root/sikk-archive/source_wallet_bot_round3/auto_tasks/wallet_structure_registry_consumption_final_20260508_022106`
- `/root/sikk-gmgn/data/source_wallet_bot/ad_hoc/8jpRiwbUXLWH4yFQaF2TBDUkWDkfKWtBMX95sibTpump` -> `/root/sikk-archive/source_wallet_bot_round3/ad_hoc/8jpRiwbUXLWH4yFQaF2TBDUkWDkfKWtBMX95sibTpump`

## Skipped
- `/root/sikk-gmgn/data/source_wallet_bot/legacy/3XwDQHMKcner1GhXRqLKojrWWwNdMaruQs7g7riDpump` skipped: source_missing_already_archived_or_not_present
- `/root/sikk-gmgn/data/source_wallet_bot/legacy/EVrfnKXnX1XCT5ESvp6VJUwLFDU1Ajq1dpUrG5qUpump` skipped: source_missing_already_archived_or_not_present

## Post-run source shape
- `legacy/`: 2 children
  - `4TKYts6M7Y1RzW6xbHo92anF2LBrRMiFFsANoTr9pump`
  - `ARea51UmRfn22Ds7KwFZirSMEEn1gtBdrhW4zLeveeV1`
- `auto_tasks/`: 1 children
  - `wallet_structure_longrun_20260508_014528`
- `ad_hoc/`: 0 children

## Archive shape
- archive `legacy/`: 4 children
  - `3pCyU31quPpsVYaC5TxtXpe6sR1KXSLzk5TkZgXGpump`
  - `6Xipib7UavxaXvWDhepFpU4NzypozVBPvNNjxTdXpump`
  - `7soYuSPe1LaJ9V37W7ZGDB5Xwxi41LUWjRT3AEQGpump`
  - `GnqRKyQfcna6XbkoJMKkvUZUBQdtMb8oy5rH2ocpump`
- archive `auto_tasks/`: 1 children
  - `wallet_structure_registry_consumption_final_20260508_022106`
- archive `ad_hoc/`: 1 children
  - `8jpRiwbUXLWH4yFQaF2TBDUkWDkfKWtBMX95sibTpump`

## Verification
- `data/source_wallet_bot/` parent tree remains intact.
- Strong-preserve roots were not touched.
- This operation moved data to archive; it did not delete data.
