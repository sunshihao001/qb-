#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CLI wrapper for Wallet Structure module maturity scan."""
from __future__ import annotations

import argparse
import json

from modules.module_maturity_governance import scan_module_maturity


def main() -> None:
    parser = argparse.ArgumentParser(description='Scan Wallet Structure module maturity')
    parser.add_argument('--project-root', default='.')
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    result = scan_module_maturity(project_root=args.project_root, output_dir=args.output_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
