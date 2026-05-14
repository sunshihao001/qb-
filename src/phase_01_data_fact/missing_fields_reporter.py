
from pathlib import Path
def write_missing_fields_report(run_dir, quality):
    p=Path(run_dir)/'summary'/'missing_fields_report.md'; p.parent.mkdir(parents=True,exist_ok=True)
    lines=['# P01 missing_fields_report','','## critical_missing_fields']
    lines += [f'- {x}' for x in quality.get('critical_missing_fields',[])] or ['- none']
    for title,key in [('optional_missing_fields','optional_missing_fields'),('degraded_fields','degraded_fields'),('blocked_fields','blocked_fields')]:
        lines += ['',f'## {title}']; lines += [f'- {x}' for x in quality.get(key,[])] or ['- none']
    lines += ['','## unknown_fields','- not_scanned_in_skeleton']
    p.write_text('\n'.join(lines)+'\n',encoding='utf-8'); return p
