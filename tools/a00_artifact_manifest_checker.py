#!/usr/bin/env python3
from pathlib import Path
from a00_acceptance_status import write_json

def check_artifacts(output_dir: Path, acceptance_run_id: str, artifacts: list[tuple[str,str,Path,bool]]) -> tuple[dict, dict]:
    rows=[]; missing=[]
    for aid, phase, path, required in artifacts:
        exists=path.exists()
        row={"artifact_id": aid, "phase": phase, "artifact_type": aid, "path": str(path), "exists": exists, "required": required, "validation_status": "PRESENT" if exists else ("MISSING" if required else "OPTIONAL_MISSING")}
        rows.append(row)
        if required and not exists: missing.append(row)
    manifest={"manifest_id": f"artifact_manifest_{acceptance_run_id}", "artifacts": rows, "manifest_status": "BUILT"}
    existence={"artifact_existence_status": "PASSED" if not missing else "BLOCKED", "missing_required_artifacts": missing, "present_count": sum(1 for r in rows if r["exists"]), "required_count": sum(1 for r in rows if r["required"])}
    write_json(output_dir/"artifact_manifest/artifact_manifest.json", manifest)
    write_json(output_dir/"artifact_manifest/artifact_existence_check.json", existence)
    return manifest, existence
