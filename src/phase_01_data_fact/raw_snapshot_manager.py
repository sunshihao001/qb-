
from pathlib import Path
import shutil
from .utils import REQUIRED_RAW, OPTIONAL_RAW, sha256_file, write_json, write_csv, utc_now
def create_raw_snapshot(raw_input_dir, run_dir, snapshot_time=None):
    raw_dir=Path(raw_input_dir); run=Path(run_dir); copied=run/'raw'/'copied_raw_files'; copied.mkdir(parents=True,exist_ok=True)
    snapshot_id='phase01_'+(snapshot_time or utc_now()).replace(':','').replace('-','')
    rows=[]
    for name in REQUIRED_RAW+OPTIONAL_RAW:
        src=raw_dir/name; row={'raw_file':name,'required':name in REQUIRED_RAW,'source_path':str(src),'copied_path':'missing','sha256':'missing','status':'missing'}
        if src.exists():
            dst=copied/name
            if dst.exists(): dst=copied/f'{snapshot_id}_{name}'
            shutil.copy2(src,dst); row.update({'copied_path':str(dst),'sha256':sha256_file(dst),'status':'copied'})
        rows.append(row)
    manifest={'phase':'phase_01_data_fact','snapshot_id':snapshot_id,'snapshot_time':snapshot_time or utc_now(),'raw_input_dir':str(raw_dir),'copied_raw_files_dir':str(copied),'files':rows}
    write_json(run/'raw'/'snapshot_manifest.json',manifest); write_json(run/'raw'/'inventory'/'snapshot_manifest.json',manifest); write_csv(run/'raw'/'raw_file_inventory.csv',rows,['raw_file','required','source_path','copied_path','sha256','status']); write_csv(run/'raw'/'inventory'/'raw_file_inventory.csv',rows,['raw_file','required','source_path','copied_path','sha256','status'])
    return manifest
