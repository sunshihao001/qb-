from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .kpp_total_runner import ROOT

DEFAULT_SEARCH_ROOTS = [
    ROOT / 'data/knowledge_processing_program/telegram_upload_productization/test_runs',
    ROOT / 'data/knowledge_processing_program/telegram_upload_productization/runs',
    ROOT / 'data/knowledge_processing_program/automation_chain/test_e2e_run',
    ROOT / 'data/knowledge_processing_program/automation_chain/manual_replay',
]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def find_run_root(run_id: str, search_roots: list[str | Path] | None = None) -> Path | None:
    roots = [Path(p) for p in (search_roots or DEFAULT_SEARCH_ROOTS)]
    for root in roots:
        direct = root / run_id
        if (direct / 'K08/telegram_status_panel.json').exists():
            return direct
        if root.exists():
            for panel in root.glob(f'**/{run_id}/K08/telegram_status_panel.json'):
                return panel.parents[1]
    # Fallback bounded search under KPP data root.
    base = ROOT / 'data/knowledge_processing_program'
    if base.exists():
        for panel in base.glob(f'**/{run_id}/K08/telegram_status_panel.json'):
            return panel.parents[1]
    return None


def _candidate_count(panel: dict[str, Any]) -> int:
    refs = panel.get('artifact_index', {}).get('K05', [])
    return len([ref for ref in refs if 'candidate' in str(ref)])


def render_status(run_root: Path) -> str:
    panel = _load_json(run_root / 'K08/telegram_status_panel.json')
    return (
        f"run_id: {panel.get('run_id')}\n"
        f"doc_id: {panel.get('doc_id')}\n"
        f"status: {panel.get('overall_status')}\n"
        f"current_stage: {panel.get('current_stage')}\n"
        f"progress_percent: {panel.get('progress_percent')}\n"
        f"governance_queue_status: {panel.get('governance_queue_status')}\n"
        f"next_action: {panel.get('next_action')}"
    )


def render_panel(run_root: Path) -> str:
    panel = _load_json(run_root / 'K08/telegram_status_panel.json')
    blockers = panel.get('blockers', [])
    gaps = panel.get('degraded_gaps', [])
    return (
        f"KPP Panel\n"
        f"run_id: {panel.get('run_id')}\n"
        f"status: {panel.get('overall_status')}\n"
        f"current_stage: {panel.get('current_stage')}\n"
        f"stage_count: {len(panel.get('stage_statuses', []))}\n"
        f"candidate_count: {_candidate_count(panel)}\n"
        f"gap_count: {len(gaps)}\n"
        f"blocker_count: {len(blockers)}\n"
        f"handoff_status: {panel.get('handoff_status')}\n"
        f"governance_queue_status: {panel.get('governance_queue_status')}\n"
        f"commands: {' / '.join(panel.get('query_commands', []))}"
    )


def render_handoff(run_root: Path) -> str:
    panel = _load_json(run_root / 'K08/telegram_status_panel.json')
    handoff = _load_json(run_root / 'K07/handoff_packet.json')
    entry = _load_json(run_root / 'K08/governance_queue_entry.json')
    return (
        f"KPP Handoff\n"
        f"run_id: {panel.get('run_id')}\n"
        f"handoff_status: {panel.get('handoff_status')}\n"
        f"handoff_path: {run_root / 'K07/handoff_packet.json'}\n"
        f"queue_entry_id: {entry.get('queue_entry_id')}\n"
        f"governance_status: {entry.get('status')}\n"
        f"next_action: {panel.get('next_action')}\n"
        f"artifact_index_keys: {', '.join(sorted(handoff.get('artifact_index', {}).keys()))}"
    )


def handle_kpp_command(command_text: str, search_roots: list[str | Path] | None = None) -> str:
    parts = command_text.strip().split()
    if len(parts) < 2:
        return '用法: /kpp_status <run_id> 或 /kpp_panel <run_id> 或 /kpp_handoff <run_id>'
    command, run_id = parts[0], parts[1]
    run_root = find_run_root(run_id, search_roots=search_roots)
    if not run_root:
        return f'KPP run not found: {run_id}'
    if command == '/kpp_status':
        return render_status(run_root)
    if command == '/kpp_panel':
        return render_panel(run_root)
    if command == '/kpp_handoff':
        return render_handoff(run_root)
    if command == '/kpp_report':
        summary = run_root / 'K08/final_run_summary.md'
        return summary.read_text() if summary.exists() else render_panel(run_root)
    if command == '/kpp_candidates':
        entry = _load_json(run_root / 'K08/governance_queue_entry.json')
        return json.dumps(entry.get('candidate_refs', {}), ensure_ascii=False, indent=2)
    if command == '/kpp_governance':
        entry = _load_json(run_root / 'K08/governance_queue_entry.json')
        return json.dumps({'queue_entry_id': entry.get('queue_entry_id'), 'status': entry.get('status'), 'policy': entry.get('governance_policy'), 'p00_routing': entry.get('p00_routing')}, ensure_ascii=False, indent=2)
    return f'Unsupported KPP command: {command}'


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='+')
    args = parser.parse_args(argv)
    print(handle_kpp_command(' '.join(args.command)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
