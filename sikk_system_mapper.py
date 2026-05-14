#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SIKK system mapper.

Generate a paper-only module map for the research loop. This module only writes
local mapping artifacts; it does not trade, sign, broadcast, or touch secrets.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

EXPECTED_MODULES = [
    "candidate_discovery",
    "kline_signal",
    "wallet_structure",
    "okx_cluster",
    "structure_fusion",
    "state_machine",
    "paper_runner",
    "case_file",
    "auto_review",
    "unified_index",
    "telegram",
    "web_dashboard",
    "cli",
    "runtime",
    "audit",
    "harness",
    "repomix_context",
    "hermes_execution",
]

DEFAULT_OUTPUT_ROOT = Path("research_loop/mappings/sikk_module_maps")


def _slug_doc_id(doc_id: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in str(doc_id).strip())
    return cleaned or "doc"


def _module_row(module: str, source_text: str) -> Dict[str, Any]:
    present = module in source_text
    return {
        "module": module,
        "present": present,
        "surface_template": present,
        "runtime_connected": present,
        "visible_in_tg": module in {"telegram", "runtime", "paper_runner", "state_machine", "unified_index"},
        "visible_in_web": module in {"web_dashboard", "runtime", "unified_index", "auto_review"},
        "visible_in_cli": module in {"cli", "runtime", "audit", "harness", "repomix_context", "hermes_execution"},
        "has_test": False,
        "acceptance_ready": False,
        "source_trace": present,
        "field_missing": [],
        "safety_risk": False,
        "over_complexity": False,
    }


def build_system_map(*, doc_id: str, source_text: str, output_root: str | Path = DEFAULT_OUTPUT_ROOT) -> Dict[str, str]:
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    slug = _slug_doc_id(doc_id)
    json_path = root / f"{slug}_sikk_map.json"
    md_path = root / f"{slug}_sikk_map.md"

    modules = [_module_row(module, source_text) for module in EXPECTED_MODULES]
    payload = {
        "doc_id": doc_id,
        "module_count": len(modules),
        "modules": modules,
        "safety_boundary": {
            "paper_only": True,
            "real_swap_enabled": False,
            "private_key_required": False,
            "signing_enabled": False,
            "broadcast_enabled": False,
        },
        "source_trace": "repomix_context / repo scan only; no secrets.",
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# SIKK 模块映射",
        "",
        f"- doc_id: `{doc_id}`",
        f"- 模块数: {len(modules)}",
        "- 安全边界: paper-only；不执行真实 swap；不读取私钥；不签名；不广播。",
        "",
        "## 模块清单",
    ]
    for row in modules:
        status = "present" if row["present"] else "missing"
        lines.append(f"- `{row['module']}`: {status}")
    lines.extend([
        "",
        "## 说明",
        "- 本映射仅用于 research_loop 归档、review 与 gap detector 输入。",
        "- `repomix_context` 仅表示跨模型上下文包需求，不代表真实导出。",
        "",
    ])
    md_path.write_text("\n".join(lines), encoding="utf-8")

    return {"sikk_map_json": str(json_path), "sikk_map_md": str(md_path)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成 SIKK research loop 模块映射")
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--source-text", required=True)
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(build_system_map(doc_id=args.doc_id, source_text=args.source_text, output_root=args.output_root), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
