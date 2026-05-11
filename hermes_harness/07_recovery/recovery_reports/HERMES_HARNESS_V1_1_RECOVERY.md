# HERMES HARNESS V1.1 RECOVERY

## Status
No recovery required.

## Trigger condition
This file is reserved for verification failure recovery. Current final verification passed.

## Default recovery routes
- missing file: regenerate target phase artifact
- script lacking --help/--dry-run: patch script argparse contract
- failed artifact verification: inspect content and re-run verify
- surface completion risk: block DONE and generate phase recovery plan
