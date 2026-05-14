
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .models import WalletStructureInput
from .decision_builder import build_bundle_from_request

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='SIKK wallet structure module runner')
    parser.add_argument('--token-address', required=False, help='Solana token address')
    parser.add_argument('--token-symbol', default='')
    parser.add_argument('--chain', default='sol')
    parser.add_argument('--analysis-time', default='')
    parser.add_argument('--discovery-time', default='')
    parser.add_argument('--output-dir', default='')
    parser.add_argument('--max-wallets', type=int, default=100)
    parser.add_argument('--include-funding-source', action='store_true')
    parser.add_argument('--include-token-flow', action='store_true')
    parser.add_argument('--update-history', action='store_true')
    parser.add_argument('--output-gmgn-notes', action='store_true', default=True)
    parser.add_argument('--input-json', default='')
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    if args.input_json:
        request = json.loads(Path(args.input_json).read_text(encoding='utf-8'))
    else:
        request = WalletStructureInput(
            token_address=args.token_address or '',
            token_symbol=args.token_symbol,
            chain=args.chain,
            discovery_time=args.discovery_time or None,
            analysis_time=args.analysis_time or None,
            max_wallets=args.max_wallets,
            include_funding_source=args.include_funding_source,
            include_token_flow=args.include_token_flow,
            update_history=args.update_history,
            output_gmgn_notes=args.output_gmgn_notes,
        ).to_dict()
    if not request.get('token_address'):
        raise SystemExit('--token-address or --input-json with token_address is required')
    out = build_bundle_from_request(request, output_dir=args.output_dir)
    print(json.dumps(out, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
