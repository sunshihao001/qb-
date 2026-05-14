#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI wrapper for Wallet Structure Governance registry consumption."""
from __future__ import annotations

import argparse
import json

from modules.wallet_structure_governance.consumption import consume_runtime_registry


def main() -> None:
    parser = argparse.ArgumentParser(description='Consume Wallet-Structure runtime adapter registry')
    parser.add_argument('--project-root', default='.')
    parser.add_argument('--registry-path', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    result = consume_runtime_registry(project_root=args.project_root, registry_path=args.registry_path, output_dir=args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
