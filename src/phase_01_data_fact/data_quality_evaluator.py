
from pathlib import Path
from .utils import write_json
STATUS_TO_HANDOFF={'DATA_OK':'HANDOFF_READY','DATA_PARTIAL':'HANDOFF_DEGRADED','DATA_WEAK':'HANDOFF_DEGRADED','DATA_STALE':'HANDOFF_REFRESH_REQUIRED','DATA_SOURCE_CONFLICT':'HANDOFF_BLOCKED','DATA_INVALID':'HANDOFF_BLOCKED'}
def evaluate_data_quality(run_dir, missing_required_raw, missing_optional_raw, critical_missing_fields, optional_missing_fields, time_validity, warnings):
    hard=[f'missing_required_raw:{x}' for x in missing_required_raw]+[f'critical_missing_field:{x}' for x in critical_missing_fields]
    stale=time_validity.get('time_validity_status') in {'TIME_EXPIRED','TIME_STALE_WARNING'} and 'quote older' in time_validity.get('reason','')
    if stale and not hard:
        hard=[]
    degrade=[f'missing_optional_raw:{x}' for x in missing_optional_raw]+[f'optional_missing_field:{x}' for x in optional_missing_fields]+list(warnings)
    status='DATA_INVALID' if hard else ('DATA_STALE' if stale else ('DATA_PARTIAL' if degrade else 'DATA_OK'))
    out={'phase':'phase_01_data_fact','data_quality_status':status,'primary_status':status,'phase_status':status,'handoff_status':STATUS_TO_HANDOFF[status],'critical_missing_fields':critical_missing_fields,'optional_missing_fields':optional_missing_fields,'missing_required_raw':missing_required_raw,'missing_optional_raw':missing_optional_raw,'degraded_fields':degrade,'blocked_fields':hard,'hard_negative_triggered':bool(hard),'hard_negative_reasons':hard,'warnings':warnings}
    write_json(Path(run_dir)/'summary'/'data_quality_summary.json',out); return out
